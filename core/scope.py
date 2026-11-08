from urllib.parse import urlparse, urljoin
import ipaddress
import socket


def normalize_target(raw):
    raw = raw.strip()
    if not raw:
        raise ValueError("Target is required")
    if "://" not in raw:
        raw = "https://" + raw
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Only valid HTTP/HTTPS URLs are supported")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in URLs are not allowed")
    return f"{parsed.scheme}://{parsed.netloc}"


def same_origin(base, candidate):
    a, b = urlparse(base), urlparse(candidate)
    return (a.scheme, a.hostname, a.port) == (b.scheme, b.hostname, b.port)


def public_host(host):
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, None)}
    except OSError:
        return False
    return bool(addresses) and all(ipaddress.ip_address(x).is_global for x in addresses)


def safe_link(base, href):
    candidate = urljoin(base, href)
    return candidate if same_origin(base, candidate) else None
