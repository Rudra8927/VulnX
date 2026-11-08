import pytest
from core.scope import normalize_target, same_origin


def test_normalize_target_adds_https():
    assert normalize_target("example.com") == "https://example.com"


def test_normalize_rejects_unsupported_scheme():
    with pytest.raises(ValueError):
        normalize_target("ftp://example.com")


def test_normalize_rejects_credentials():
    with pytest.raises(ValueError):
        normalize_target("https://user:pass@example.com")


def test_same_origin():
    assert same_origin("https://example.com", "https://example.com/path")
    assert not same_origin("https://example.com", "https://other.example")
