"""
ClarifAI Live News Backend

Primary:
    GDELT

Fallback:
    Google News RSS

The UI should only interact with get_live_news().
"""

import time
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus


GDELT_URL = (
    "https://api.gdeltproject.org/api/v2/doc/doc"
)

GOOGLE_NEWS_URL = (
    "https://news.google.com/rss"
)


def _get_gdelt_news(
    query="",
    timespan="1h",
    max_records=10,
):
    """Try GDELT first."""

    params = {
        "query": query if query.strip() else "news",
        "mode": "artlist",
        "format": "json",
        "maxrecords": max_records,
        "timespan": timespan,
        "sort": "datedesc",
    }

    response = requests.get(
        GDELT_URL,
        params=params,
        timeout=15,
        headers={
            "User-Agent": "ClarifAI/1.0"
        },
    )

    # Explicitly handle rate limiting.
    if response.status_code == 429:
        raise RuntimeError(
            "GDELT rate limit reached."
        )

    response.raise_for_status()

    data = response.json()

    articles = data.get(
        "articles",
        [],
    )

    results = []

    for article in articles:

        url = article.get(
            "url",
            "",
        ).strip()

        if not url:
            continue

        results.append(
            {
                "title": article.get(
                    "title",
                    "Untitled Article",
                ),
                "url": url,
                "domain": article.get(
                    "domain",
                    "Unknown",
                ),
                "language": article.get(
                    "language",
                    "",
                ),
                "seendate": article.get(
                    "seendate",
                    "",
                ),
                "provider": "GDELT",
            }
        )

    return results


def _get_google_news(
    query="",
    max_records=10,
):
    """
    Fallback live-news source using Google News RSS.
    No API key required.
    """

    if query.strip():

        encoded_query = quote_plus(
            query.strip()
        )

        url = (
            f"{GOOGLE_NEWS_URL}/search"
            f"?q={encoded_query}"
            f"&hl=en-IN"
            f"&gl=IN"
            f"&ceid=IN:en"
        )

    else:

        url = (
            f"{GOOGLE_NEWS_URL}"
            f"?hl=en-IN"
            f"&gl=IN"
            f"&ceid=IN:en"
        )

    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "ClarifAI/1.0"
            )
        },
    )

    response.raise_for_status()

    root = ET.fromstring(
        response.content
    )

    results = []

    channel = root.find("channel")

    if channel is None:
        return results

    for item in channel.findall("item"):

        if len(results) >= max_records:
            break

        title_element = item.find("title")
        link_element = item.find("link")
        date_element = item.find(
            "pubDate"
        )
        source_element = item.find(
            "source"
        )

        title = (
            title_element.text.strip()
            if title_element is not None
            and title_element.text
            else "Untitled Article"
        )

        url = (
            link_element.text.strip()
            if link_element is not None
            and link_element.text
            else ""
        )

        published = (
            date_element.text.strip()
            if date_element is not None
            and date_element.text
            else ""
        )

        domain = (
            source_element.text.strip()
            if source_element is not None
            and source_element.text
            else "Google News"
        )

        if not url:
            continue

        results.append(
            {
                "title": title,
                "url": url,
                "domain": domain,
                "language": "en",
                "seendate": published,
                "provider": "Google News RSS",
            }
        )

    return results


def get_live_news(
    query="",
    timespan="1h",
    max_records=10,
):
    """
    Get current news.

    GDELT is attempted first.
    Google News RSS automatically becomes the
    fallback if GDELT is unavailable/rate-limited.
    """

    # --------------------------------------------------------
    # Try GDELT
    # --------------------------------------------------------

    try:

        results = _get_gdelt_news(
            query=query,
            timespan=timespan,
            max_records=max_records,
        )

        if results:

            return results

    except Exception as error:

        print(
            "GDELT unavailable:",
            error,
        )

    # Small delay before fallback.
    time.sleep(0.5)

    # --------------------------------------------------------
    # Google News fallback
    # --------------------------------------------------------

    try:

        results = _get_google_news(
            query=query,
            max_records=max_records,
        )

        if results:

            return results

    except Exception as error:

        print(
            "Google News RSS unavailable:",
            error,
        )

    # --------------------------------------------------------
    # Nothing available
    # --------------------------------------------------------

    raise RuntimeError(
        "Live news services are currently unavailable."
    )