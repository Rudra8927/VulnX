from types import SimpleNamespace
from modules.http_checks import inspect


def test_missing_headers_are_reported():
    response = SimpleNamespace(headers={}, status_code=200)
    findings = inspect("https://example.test/", response)
    titles = {item["title"] for item in findings}
    assert "Missing content-security-policy" in titles
    assert "Missing x-content-type-options" in titles


def test_http_target_is_flagged():
    response = SimpleNamespace(headers={}, status_code=200)
    findings = inspect("http://example.test/", response)
    assert any(item["title"] == "Website served over HTTP" for item in findings)
