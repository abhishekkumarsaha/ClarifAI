"""
ClarifAI Source Ranking

Ranks news candidates before expensive article extraction.
"""

from urllib.parse import urlparse


# Domains that generally provide useful
# established-news evidence.
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
}


def get_domain(url):
    try:
        return (
            urlparse(url)
            .netloc
            .lower()
            .replace("www.", "")
        )
    except Exception:
        return ""


def rank_articles(
    articles,
    limit=5,
):
    """
    Rank current-news candidates.

    Factors:
    - known news domains
    - description availability
    - URL availability
    """

    ranked = []

    for article in articles:

        url = article.get(
            "url",
            "",
        )

        domain = get_domain(
            url
        )

        score = 0

        if domain in HIGH_VALUE_DOMAINS:
            score += 5

        if article.get(
            "description"
        ):
            score += 1

        if article.get(
            "published_at"
        ):
            score += 1

        if url:
            score += 1

        ranked.append(
            (
                score,
                article,
            )
        )

    ranked.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        article
        for score, article
        in ranked[:limit]
    ]