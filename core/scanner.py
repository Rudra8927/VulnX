import os
import ssl
import socket
import uuid
import asyncio
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin

import dns.resolver
import httpx

from core.scope import normalize_target, public_host
from core.crawler import crawl
from modules.http_checks import inspect, make

PATHS = {
    "/.git/HEAD": ["ref: refs/"],
    "/.env": ["db_", "secret=", "api_key="],
    "/backup.zip": ["application/zip", "pk"],
    "/phpinfo.php": ["php version", "phpinfo()"],
    "/server-status": ["server uptime", "total accesses"],
}


class Scanner:
    def __init__(self):
        self.timeout = float(os.getenv("VULNX_TIMEOUT", "8"))
        self.pages = int(os.getenv("VULNX_MAX_PAGES", "15"))
        self.depth = int(os.getenv("VULNX_MAX_DEPTH", "2"))
        self.sem = asyncio.Semaphore(int(os.getenv("VULNX_CONCURRENCY", "2")))

    async def scan(self, raw):
        target = normalize_target(raw)
        parsed = urlparse(target)
        host = parsed.hostname
        if not public_host(host):
            raise ValueError("Target must resolve exclusively to public IP addresses. Private, loopback and unresolved hosts are blocked.")
        findings, metadata = [], {"host": host}
        try:
            metadata["dns_a"] = [str(item) for item in dns.resolver.resolve(host, "A", lifetime=self.timeout)]
        except Exception as error:
            metadata["dns_note"] = str(error)[:120]
        if parsed.scheme == "https":
            try:
                context = ssl.create_default_context()
                with socket.create_connection((host, parsed.port or 443), timeout=self.timeout) as connection:
                    with context.wrap_socket(connection, server_hostname=host) as tls:
                        cert = tls.getpeercert()
                        metadata["tls"] = {
                            "version": tls.version(), "cipher": tls.cipher()[0],
                            "not_after": cert.get("notAfter"),
                        }
            except Exception as error:
                findings.append(make("TLS inspection failed", "Medium", "TLS", str(error),
                    "Review certificate validity, hostname and TLS listener.", target))
        headers = {"User-Agent": os.getenv("VULNX_USER_AGENT", "VulnX/1.0 authorized assessment")}
        async with httpx.AsyncClient(timeout=self.timeout, headers=headers, verify=True, max_redirects=3) as client:
            try:
                async with self.sem:
                    response = await client.get(target + "/", follow_redirects=True)
                metadata["http_status"] = response.status_code
                metadata["final_url"] = str(response.url)
                findings.extend(inspect(target + "/", response))
            except Exception as error:
                findings.append(make("Homepage request failed", "High", "Reachability", str(error)[:200],
                    "Check site availability and TLS configuration.", target))
            pages = await crawl(client, target, self.pages, self.depth)
            for path, markers in PATHS.items():
                try:
                    async with self.sem:
                        response = await client.get(urljoin(target, path), follow_redirects=False)
                    body = response.text[:3000].lower()
                    if response.status_code == 200 and any(marker in body for marker in markers):
                        findings.append(make("Potentially exposed sensitive resource",
                            "High" if path in ("/.git/HEAD", "/.env", "/backup.zip") else "Medium",
                            "Public exposure", "GET " + path + " returned HTTP 200 with a matching content indicator.",
                            "Restrict public access if unintended; rotate exposed secrets and review access logs.",
                            urljoin(target, path)))
                except Exception:
                    continue
        unique, seen = [], set()
        for finding in findings:
            key = (finding["title"], finding["url"], finding["evidence"])
            if key not in seen:
                seen.add(key)
                unique.append(finding)
        return {
            "scan_id": str(uuid.uuid4())[:8],
            "target": target,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "meta": metadata,
            "pages": pages,
            "findings": unique,
        }
