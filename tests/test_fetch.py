import pytest

from signalforge.fetch import _require_public_host, canonicalize_url, fetch_text


def test_canonicalize_url_strips_tracking_and_fragment():
    assert canonicalize_url("HTTPS://Example.COM/a/?utm_source=x&b=2#part") == "https://example.com/a/?b=2"


@pytest.mark.parametrize("url", ["file:///etc/passwd", "https://user:pass@example.org/", "/relative"])
def test_rejects_unsafe_url_forms(url):
    with pytest.raises(ValueError):
        canonicalize_url(url)


def test_blocks_private_destination(monkeypatch):
    monkeypatch.setattr("signalforge.fetch.socket.getaddrinfo", lambda *a, **k: [(0, 0, 0, "", ("127.0.0.1", 0))])
    with pytest.raises(ValueError, match="non-public"):
        _require_public_host("localhost")


def test_extracts_text_and_ignores_script(monkeypatch):
    class Headers:
        def get_content_charset(self):
            return "utf-8"

        def get(self, name):
            return None

    class Response:
        headers = Headers()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def geturl(self):
            return "https://example.org/page"

        def read(self, limit):
            return b"<p>Visible</p><script>ignored()</script>"

    monkeypatch.setattr("signalforge.fetch._require_public_host", lambda host: None)
    class Opener:
        def open(self, *args, **kwargs):
            return Response()

    monkeypatch.setattr("signalforge.fetch.build_opener", lambda *args: Opener())
    assert fetch_text("https://example.org/page") == "Visible"


def test_decodes_gzip_response(monkeypatch):
    import gzip

    class Headers:
        def get_content_charset(self):
            return "utf-8"

        def get(self, name):
            return "gzip" if name == "Content-Encoding" else None

    class Response:
        headers = Headers()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self, limit):
            return gzip.compress(b"<p>This readable page contains a sufficiently long paragraph.</p>")

    class Opener:
        def open(self, *args, **kwargs):
            return Response()

    monkeypatch.setattr("signalforge.fetch._require_public_host", lambda host: None)
    monkeypatch.setattr("signalforge.fetch.build_opener", lambda *args: Opener())
    assert fetch_text("https://example.org/page").startswith("This readable page")
