"""뉴스 본문 스크래퍼."""

from __future__ import annotations

from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover
    BeautifulSoup = None


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)

SELECTORS = {
    "bbc.com": "div[data-component='text-block'] p",
    "cbsnews.com": ".content__body p",
    "abcnews.go.com": "div[data-testid='prism-article-body'] p",
    "cnn.com": ".article__content p",
    "npr.org": ".storytext p",
    "csis.org": ".wysiwyg-wrapper",
}


class _ParagraphParser(HTMLParser):
    """HTML에서 p 텍스트를 단순 추출한다."""

    def __init__(self) -> None:
        super().__init__()
        self._in_p = False
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:  # noqa: ARG002
        if tag.lower() == "p":
            self._in_p = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "p":
            self._in_p = False

    def handle_data(self, data: str) -> None:
        if self._in_p:
            text = data.strip()
            if text:
                self._parts.append(text)

    def result(self) -> str:
        return " ".join(self._parts).strip()


class NewsScraper:
    """도메인별 본문을 수집한다."""

    def scrap(self, ctx: object, raw_url: str) -> list[str]:  # noqa: ARG002
        domain = self._extract_domain(raw_url)
        selector = SELECTORS.get(domain)
        if not selector:
            raise ValueError("scrap invalid url")

        html = self._fetch_html(raw_url)
        content = self._parse_content(html, selector)
        if not content:
            raise ValueError("scrap parse fail")

        return [content]

    def _extract_domain(self, raw_url: str) -> str:
        parsed = urlparse(raw_url)
        hostname = (parsed.hostname or "").lower()
        if hostname.startswith("www."):
            hostname = hostname[4:]
        return hostname

    def _fetch_html(self, raw_url: str) -> str:
        req = Request(raw_url, headers={"User-Agent": DEFAULT_USER_AGENT})
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="ignore")

    def _parse_content(self, html: str, selector: str) -> str:
        # bs4가 있으면 selector 기반 파싱, 없으면 p 태그 기반으로 동작한다.
        if BeautifulSoup is not None:
            soup = BeautifulSoup(html, "html.parser")
            nodes = soup.select(selector)
            texts = [node.get_text(" ", strip=True) for node in nodes if node.get_text(strip=True)]
            return " ".join(texts).strip()

        parser = _ParagraphParser()
        parser.feed(html)
        return parser.result()
