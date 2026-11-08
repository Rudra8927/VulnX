from collections import deque
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag

from core.scope import same_origin


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.items.append(href)


async def crawl(client, base, max_pages=15, max_depth=2):
    queue = deque([(base + "/", 0)])
    seen, pages = set(), []
    while queue and len(seen) < max_pages:
        url, depth = queue.popleft()
        url = urldefrag(url)[0]
        if url in seen:
            continue
        seen.add(url)
        try:
            response = await client.get(url, follow_redirects=False)
            pages.append({
                "url": url,
                "status": response.status_code,
                "content_type": response.headers.get("content-type", ""),
            })
            if depth < max_depth and "text/html" in response.headers.get("content-type", "").lower():
                parser = Links()
                try:
                    parser.feed(response.text[:500000])
                except Exception:
                    pass
                for href in parser.items:
                    destination = urldefrag(urljoin(url, href))[0]
                    if same_origin(base, destination) and destination not in seen:
                        queue.append((destination, depth + 1))
        except Exception:
            continue
    return pages
