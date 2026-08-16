"""
ClarifAI Article Extraction
Extracts article content and metadata from public URLs.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
import trafilatura


@dataclass
class ArticleData:
    title: str
    article_text: str
    source_url: str
    source_domain: str
    input_method: str
    word_count: int
    extracted_at: str


def validate_url(url: str) -> bool:
    """Validate that the input is an HTTP/HTTPS URL."""
    if not url:
        return False

    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def extract_article(url: str, timeout: int = 15) -> ArticleData:
    """
    Fetch and extract an article from a public URL.

    Raises:
        ValueError: for invalid URLs or insufficient article content.
        RuntimeError: for network/extraction failures.
    """

    url = url.strip()

    if not validate_url(url):
        raise ValueError("Please enter a valid HTTP or HTTPS article URL.")

    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
                )
            },
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "The website took too long to respond. "
            "Please try again or paste the article manually."
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Unable to access this article: {exc}"
        )

    downloaded = response.text

    if not downloaded:
        raise RuntimeError(
            "The webpage returned no readable content."
        )

    # Extract article text and metadata
    extracted_text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        include_links=False,
        favor_precision=True,
    )

    metadata = trafilatura.extract_metadata(downloaded)

    if not extracted_text:
        raise ValueError(
            "Could not extract the main article content. "
            "The website may block automated extraction. "
            "Please paste the article manually."
        )

    extracted_text = extracted_text.strip()

    # Avoid sending extremely small/non-article pages to the ML model.
    if len(extracted_text.split()) < 50:
        raise ValueError(
            "The extracted content is too short for reliable analysis. "
            "Please paste the article manually."
        )

    title = ""

    if metadata and metadata.title:
        title = metadata.title.strip()

    if not title:
        title = "Untitled Article"

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return ArticleData(
        title=title,
        article_text=extracted_text,
        source_url=url,
        source_domain=domain,
        input_method="url",
        word_count=len(extracted_text.split()),
        extracted_at=datetime.now(timezone.utc).isoformat(),
    )