"""Bounded HTTP fetching and readable-text extraction."""

from __future__ import annotations

import ipaddress
import re
import socket
import zlib
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

MAX_BYTES = 1_000_000
TIMEOUT_SECONDS = 12


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(
        self, request: Request, response: object, code: int, message: str,
        headers: object, new_url: str,
    ) -> Request | None:
        return None


class FetchError(ValueError):
    """A transient fetch failure that may be retried once."""


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.hidden = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg", "nav", "footer"}:
            self.hidden += 1
        elif tag in {"p", "li", "h1", "h2", "h3", "h4", "br", "div", "article", "section", "tr", "td", "dt", "dd"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg", "nav", "footer"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            self.parts.append(data)


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError("Only absolute HTTP(S) source URLs are allowed")
    if parts.username or parts.password:
        raise ValueError("URLs containing credentials are not allowed")
    host = parts.hostname.lower().rstrip(".")
    port = parts.port
    scheme = parts.scheme.lower()
    netloc = host if port is None or (scheme == "https" and port == 443) or (scheme == "http" and port == 80) else f"{host}:{port}"
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    pairs = sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                   if not k.lower().startswith("utm_"))
    return urlunsplit((scheme, netloc, path, urlencode(pairs, doseq=True), ""))


def _require_public_host(host: str) -> None:
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)}
    except OSError as exc:
        raise ValueError(f"Could not resolve source host: {host}") from exc
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise ValueError("Source resolves to a non-public network address")


def fetch_text(url: str) -> str:
    """Fetch a public page with a timeout and strict response-size cap."""
    normalized = canonicalize_url(url)
    parts = urlsplit(normalized)
    _require_public_host(parts.hostname or "")
    request = Request(normalized, headers={
        "User-Agent": "SignalForge/0.1 (+research CLI)",
        "Accept-Encoding": "identity",
    })
    try:
        with build_opener(_NoRedirect).open(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                raise ValueError("Source response exceeds 1 MB limit")
            charset = response.headers.get_content_charset() or "utf-8"
            encoding = (response.headers.get("Content-Encoding") or "identity").lower()
    except (HTTPError, URLError, TimeoutError) as exc:
        if isinstance(exc, HTTPError) and exc.code in {301, 302, 303, 307, 308}:
            raise ValueError("Redirected sources are not fetched; use the final public URL") from exc
        raise FetchError(f"Unable to fetch source ({type(exc).__name__})") from exc
    if encoding == "gzip":
        decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        body = decoder.decompress(body, MAX_BYTES + 1)
    elif encoding == "deflate":
        body = zlib.decompressobj().decompress(body, MAX_BYTES + 1)
    elif encoding not in {"identity", ""}:
        raise ValueError(f"Unsupported content encoding: {encoding}")
    if len(body) > MAX_BYTES:
        raise ValueError("Decompressed source exceeds 1 MB limit")
    parser = _TextExtractor()
    parser.feed(body.decode(charset, errors="replace"))
    return re.sub(r"[ \t]+", " ", "".join(parser.parts)).strip()
