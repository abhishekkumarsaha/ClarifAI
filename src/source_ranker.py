"""
ClarifAI Source Ranking
=======================

Ranks evidence sources before expensive extraction.
"""

from urllib.parse import urlparse


HIGH_VALUE_DOMAINS = {
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "bbc.co.uk",
    "thehindu.com",
    "indianexpress.com",
    "ndtv.com",
    "theguardian.com",
    "npr.org",
    "aljazeera.com",
    "hindustantimes.com",
    "timesofindia.indiatimes.com",
    "news18.com",
    "deccanherald.com",
    "telegraphindia.com",
    "economictimes.indiatimes.com",
    "moneycontrol.com",
    "livemint.com",
}

LOW_VALUE_DOMAINS = {
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "youtube.com",
    "tiktok.com",
    "reddit.com",
}


def get_domain(url: str) -> str:
    try:
        hostname = urlparse(str(url or "")).netloc.lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        return hostname

    except Exception:
        return ""


def _domain_score(domain: str) -> int:
    if domain in HIGH_VALUE_DOMAINS:
        return 6

    if domain in LOW_VALUE_DOMAINS:
        return -3

    if domain:
        return 1

    return 0


def rank_articles(
    articles,
    limit=5,
):
    """
    Rank news candidates using:

    1. Publisher reputation
    2. Article description
    3. Publication timestamp
    4. Valid URL
    5. Available title
    """

    if not isinstance(articles, list):
        return []

    ranked = []

    for index, article in enumerate(articles):

        if not isinstance(article, dict):
            continue

        url = str(article.get("url", "") or "").strip()

        domain = get_domain(url)

        score = _domain_score(domain)

        if article.get("title") or article.get("headline"):
            score += 1

        if article.get("description") or article.get("snippet"):
            score += 1

        if article.get("published_at") or article.get("publication_date"):
            score += 1

        if url:
            score += 1

        ranked.append(
            {
                "score": score,
                "index": index,
                "article": article,
            }
        )

    ranked.sort(
        key=lambda item: (
            item["score"],
            -item["index"],
        ),
        reverse=True,
    )

    return [
        item["article"]
        for item in ranked[: max(1, int(limit))]
    ]