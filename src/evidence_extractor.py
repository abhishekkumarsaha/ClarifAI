"""
ClarifAI Evidence Extractor
===========================

Purpose:
    Convert a news-search result into usable evidence.

Evidence priority:

    1. Content supplied by Currents
    2. Direct publisher article extraction
    3. Google News wrapper resolution + publisher extraction
    4. Currents description
    5. Unavailable

Important:
    Failure to extract an article is NOT evidence that
    the article or claim is fake.
"""

import html
import re
from urllib.parse import urlparse, unquote

import requests
import trafilatura


# ============================================================
# CONFIGURATION
# ============================================================

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/151.0.0.0 "
    "Safari/537.36 "
    "ClarifAI/1.0"
)


REQUEST_TIMEOUT = 20


GOOGLE_NEWS_HOSTS = {
    "news.google.com",
    "www.news.google.com",
}


# ============================================================
# HTTP SESSION
# ============================================================

def _create_session():
    """
    Create a reusable HTTP session.
    """

    session = requests.Session()

    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": (
                "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "*/*;q=0.8"
            ),
            "Accept-Language": (
                "en-US,en;q=0.9"
            ),
        }
    )

    return session


# ============================================================
# URL HELPERS
# ============================================================

def is_google_news_url(url):
    """
    Return True when the URL belongs to Google News.
    """

    if not url:
        return False

    try:

        parsed = urlparse(url)

        return (
            parsed.netloc.lower()
            in GOOGLE_NEWS_HOSTS
        )

    except Exception:

        return False


def _clean_url(url):
    """
    Clean HTML entities and URL encoding.
    """

    if not url:
        return ""

    url = html.unescape(url)

    url = unquote(url)

    return url.strip()


def _extract_canonical_url(page_html):
    """
    Try to find the original publisher URL from
    canonical/OG metadata inside a Google News page.
    """

    if not page_html:
        return None

    # --------------------------------------------------------
    # <link rel="canonical" href="...">
    # --------------------------------------------------------

    canonical_patterns = [
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',
        r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
    ]

    for pattern in canonical_patterns:

        match = re.search(
            pattern,
            page_html,
            flags=re.IGNORECASE,
        )

        if match:

            candidate = _clean_url(
                match.group(1)
            )

            if (
                candidate.startswith(
                    "http://"
                )
                or candidate.startswith(
                    "https://"
                )
            ):

                if not is_google_news_url(
                    candidate
                ):

                    return candidate

    # --------------------------------------------------------
    # og:url
    # --------------------------------------------------------

    og_patterns = [
        r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:url["\']',
    ]

    for pattern in og_patterns:

        match = re.search(
            pattern,
            page_html,
            flags=re.IGNORECASE,
        )

        if match:

            candidate = _clean_url(
                match.group(1)
            )

            if (
                candidate.startswith(
                    "http://"
                )
                or candidate.startswith(
                    "https://"
                )
            ):

                if not is_google_news_url(
                    candidate
                ):

                    return candidate

    return None


# ============================================================
# GOOGLE NEWS URL RESOLUTION
# ============================================================

def resolve_article_url(url):
    """
    Resolve a Google News wrapper URL into the
    original publisher URL whenever possible.

    Resolution strategy:

        1. Normal HTTP redirects
        2. Canonical URL in Google News HTML
        3. og:url metadata
        4. Return original URL if unresolved
    """

    if not url:

        return url

    url = _clean_url(url)

    if not is_google_news_url(url):

        return url

    session = _create_session()

    try:

        response = session.get(
            url,
            timeout=15,
            allow_redirects=True,
        )

        # ----------------------------------------------------
        # Method 1: HTTP redirect
        # ----------------------------------------------------

        resolved = _clean_url(
            response.url
        )

        if (
            resolved
            and not is_google_news_url(
                resolved
            )
        ):

            return resolved

        # ----------------------------------------------------
        # Method 2: canonical / OG metadata
        # ----------------------------------------------------

        resolved = _extract_canonical_url(
            response.text
        )

        if resolved:

            return resolved

    except Exception:

        pass

    # --------------------------------------------------------
    # Could not resolve
    # --------------------------------------------------------

    return url


# ============================================================
# PUBLISHER EXTRACTION
# ============================================================

def _extract_from_publisher(
    url,
    supplied_title="",
):
    """
    Attempt to extract the readable article from
    a publisher URL.
    """

    if not url:

        return {
            "success": False,
            "content": "",
            "final_url": "",
            "title": supplied_title,
            "method": "none",
            "error": "No URL supplied.",
        }

    session = _create_session()

    try:

        response = session.get(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        response.raise_for_status()

        final_url = response.url

        # ----------------------------------------------------
        # Do not try to parse Google News as publisher content
        # ----------------------------------------------------

        if is_google_news_url(
            final_url
        ):

            return {
                "success": False,
                "content": "",
                "final_url": final_url,
                "title": supplied_title,
                "method": "google_news_wrapper",
                "error": (
                    "URL remained a Google News "
                    "wrapper."
                ),
            }

        # ----------------------------------------------------
        # Precision extraction
        # ----------------------------------------------------

        content = trafilatura.extract(
            response.text,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
        )

        # ----------------------------------------------------
        # Recall fallback
        # ----------------------------------------------------

        if not content:

            content = trafilatura.extract(
                response.text,
                include_comments=False,
                include_tables=True,
                favor_recall=True,
            )

        if content:

            content = content.strip()

        # ----------------------------------------------------
        # Minimum usable length
        # ----------------------------------------------------

        if content and len(content) >= 100:

            title = supplied_title

            try:

                metadata = (
                    trafilatura.extract_metadata(
                        response.text
                    )
                )

                if (
                    metadata
                    and metadata.title
                ):

                    title = metadata.title

            except Exception:

                pass

            return {
                "success": True,
                "content": content,
                "final_url": final_url,
                "title": title,
                "method": "publisher_extraction",
                "error": "",
            }

        return {
            "success": False,
            "content": "",
            "final_url": final_url,
            "title": supplied_title,
            "method": "publisher_extraction",
            "error": (
                "Publisher page was reached, "
                "but readable article content "
                "could not be extracted."
            ),
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "content": "",
            "final_url": url,
            "title": supplied_title,
            "method": "publisher_extraction",
            "error": "Publisher request timed out.",
        }

    except requests.exceptions.HTTPError as error:

        return {
            "success": False,
            "content": "",
            "final_url": url,
            "title": supplied_title,
            "method": "publisher_extraction",
            "error": str(error),
        }

    except Exception as error:

        return {
            "success": False,
            "content": "",
            "final_url": url,
            "title": supplied_title,
            "method": "publisher_extraction",
            "error": str(error),
        }


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_article(
    url,
    supplied_content="",
    supplied_description="",
    supplied_title="",
):
    """
    Extract evidence from a news-search result.

    Returns a structured dictionary.

    Evidence quality:

        FULL_ARTICLE
        SUMMARY_ONLY
        UNAVAILABLE
    """

    original_url = _clean_url(
        url
    )

    # ========================================================
    # 1. CURRents CONTENT
    # ========================================================

    if supplied_content:

        content = str(
            supplied_content
        ).strip()

        if len(content) >= 100:

            return {
                "success": True,
                "content": content,
                "original_url": original_url,
                "final_url": original_url,
                "title": supplied_title,
                "method": "currents_content",
                "evidence_quality": (
                    "FULL_ARTICLE"
                ),
                "error": "",
            }

    # ========================================================
    # 2. RESOLVE GOOGLE NEWS URL
    # ========================================================

    resolved_url = resolve_article_url(
        original_url
    )

    # ========================================================
    # 3. DIRECT PUBLISHER EXTRACTION
    # ========================================================

    publisher_result = (
        _extract_from_publisher(
            resolved_url,
            supplied_title,
        )
    )

    if publisher_result.get(
        "success",
        False,
    ):

        publisher_result[
            "original_url"
        ] = original_url

        publisher_result[
            "evidence_quality"
        ] = "FULL_ARTICLE"

        return publisher_result

    extraction_error = (
        publisher_result.get(
            "error",
            "Extraction failed.",
        )
    )

    # ========================================================
    # 4. DESCRIPTION FALLBACK
    # ========================================================

    if supplied_description:

        description = str(
            supplied_description
        ).strip()

        if len(description) >= 50:

            return {
                "success": True,
                "content": description,
                "original_url": original_url,
                "final_url": resolved_url,
                "title": supplied_title,
                "method": "currents_description",
                "evidence_quality": (
                    "SUMMARY_ONLY"
                ),
                "error": (
                    "Full article unavailable; "
                    "using news description."
                ),
            }

    # ========================================================
    # 5. UNAVAILABLE
    # ========================================================

    return {
        "success": False,
        "content": "",
        "original_url": original_url,
        "final_url": resolved_url,
        "title": supplied_title,
        "method": "none",
        "evidence_quality": (
            "UNAVAILABLE"
        ),
        "error": extraction_error,
    }