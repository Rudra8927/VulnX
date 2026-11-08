def make(title, severity, category, evidence, fix, url):
    return {
        "title": title, "severity": severity, "category": category,
        "evidence": str(evidence)[:350], "remediation": fix, "url": url,
    }


def inspect(url, response):
    findings = []
    headers = {key.lower(): value for key, value in response.headers.items()}
    checks = [
        ("content-security-policy", "Medium", "Deploy a Content-Security-Policy suited to the application."),
        ("x-content-type-options", "Low", "Set X-Content-Type-Options: nosniff."),
        ("referrer-policy", "Low", "Set a restrictive Referrer-Policy."),
        ("permissions-policy", "Info", "Define browser features using Permissions-Policy."),
    ]
    if url.startswith("https://"):
        checks.append(("strict-transport-security", "Medium", "Enable HSTS after validating HTTPS."))
    for key, severity, fix in checks:
        if key not in headers:
            findings.append(make("Missing " + key, severity, "HTTP headers", key + " not observed", fix, url))
    csp = headers.get("content-security-policy", "")
    if csp and "frame-ancestors" not in csp.lower():
        findings.append(make(
            "CSP lacks frame-ancestors", "Medium", "HTTP headers",
            "No frame-ancestors directive observed",
            "Add an appropriate frame-ancestors directive to reduce clickjacking risk.", url,
        ))
    if headers.get("server"):
        findings.append(make("Server banner disclosed", "Info", "Information disclosure",
                              headers["server"], "Minimize unnecessary version details.", url))
    if headers.get("x-powered-by"):
        findings.append(make("Technology banner disclosed", "Low", "Information disclosure",
                              headers["x-powered-by"], "Remove unnecessary X-Powered-By header.", url))
    cookie = response.headers.get("set-cookie", "")
    if cookie:
        low = cookie.lower()
        for attr, fix in [
            ("secure", "Set Secure on cookies served over HTTPS."),
            ("httponly", "Set HttpOnly where JavaScript does not need cookie access."),
            ("samesite", "Set an appropriate SameSite policy."),
        ]:
            if attr not in low:
                findings.append(make("Cookie may lack " + attr.title(),
                    "Medium" if attr == "secure" else "Low", "Cookies",
                    "Set-Cookie response did not show " + attr, fix, url))
    if url.startswith("http://"):
        findings.append(make("Website served over HTTP", "Medium", "Transport security",
            "Plaintext HTTP URL", "Serve the site over HTTPS and redirect HTTP to HTTPS.", url))
    return findings
