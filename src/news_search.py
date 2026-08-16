"""
ClarifAI Live News Search
=========================

Currents-powered live news retrieval.

The user can enter a natural-language claim.
ClarifAI converts it into a few focused search
queries before calling Currents.

No Google News fallback is used.
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


CURRENTS_API_KEY = (
    os.getenv("CURRENTS_API_KEY")
    or os.getenv("CURRENT_API_KEY")
)

SEARCH_URL = (
    "https://api.currentsapi.services/v1/search"
)

LATEST_URL = (
    "https://api.currentsapi.services/v1/latest-news"
)

TIMEOUT = 20


# ============================================================
# STOPWORDS
# ============================================================

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "being",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "for",
    "from",
    "had",
    "has",
    "have",
    "he",
    "her",
    "his",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "its",
    "me",
    "my",
    "of",
    "on",
    "or",
    "our",
    "said",
    "she",
    "so",
    "that",
    "the",
    "their",
    "them",
    "there",
    "they",
    "this",
    "to",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "will",
    "with",
    "would",
    "you",
    "your",
    "stopped",
    "stop",
    "calling",
    "call",
    "about",
    "heard",
    "think",
    "thought",
    "today",
    "yesterday",
}


# ============================================================
# URL → SOURCE
# ============================================================

def _source_from_url(url):

    if not url:
        return "Unknown"

    try:

        hostname = urlparse(
            url
        ).netloc.lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        return hostname

    except Exception:

        return "Unknown"


# ============================================================
# API KEY
# ============================================================

def _check_key():

    if not CURRENTS_API_KEY:

        raise RuntimeError(
            "CURRENTS_API_KEY is missing "
            "from .env"
        )


# ============================================================
# NORMALIZE ARTICLE
# ============================================================

def _normalize(article):

    url = (
        article.get("url")
        or ""
    ).strip()

    return {

        "id": article.get(
            "id",
            "",
        ),

        "title": (
            article.get("title")
            or ""
        ).strip(),

        "description": (
            article.get("description")
            or ""
        ).strip(),

        "url": url,

        "source": _source_from_url(
            url
        ),

        "author": (
            article.get("author")
            or ""
        ).strip(),

        "published_at": (
            article.get("published")
            or ""
        ).strip(),

        "category": article.get(
            "category",
            [],
        ),

        "language": article.get(
            "language",
            "en",
        ),

        "image": article.get(
            "image",
            "",
        ),

        "provider": "Currents",

        "content": "",
    }


# ============================================================
# QUERY GENERATOR
# ============================================================

def build_search_queries(claim):
    """
    Convert a conversational claim into a few
    focused Currents search queries.

    Example:

    Input:
        Netflix co-founder Reed Hastings on why
        he stopped calling CEOs Ted Sarandos
        & Greg Peters

    Output:
        Netflix Reed Hastings
        Reed Hastings Ted Sarandos
        Netflix Ted Sarandos Greg Peters
    """

    claim = str(claim).strip()

    if not claim:
        return []

    # --------------------------------------------------------
    # Clean punctuation
    # --------------------------------------------------------

    cleaned = re.sub(
        r"[^A-Za-z0-9&'\-\s]",
        " ",
        claim,
    )

    cleaned = cleaned.replace(
        "&",
        " and ",
    )

    words = cleaned.split()

    # --------------------------------------------------------
    # Remove common conversational words
    # --------------------------------------------------------

    meaningful = []

    for word in words:

        normalized = (
            word
            .strip("-'")
            .lower()
        )

        if not normalized:
            continue

        if normalized in STOPWORDS:
            continue

        if len(normalized) <= 2:
            continue

        meaningful.append(
            word.strip("-'")
        )

    # Remove duplicates while preserving order.
    unique = []

    seen = set()

    for word in meaningful:

        key = word.lower()

        if key not in seen:

            seen.add(key)
            unique.append(word)

    # --------------------------------------------------------
    # Detect likely named entities
    # --------------------------------------------------------

    proper_words = []

    for word in words:

        cleaned_word = word.strip(
            "-'"
        )

        if not cleaned_word:
            continue

        # Capitalized words are useful entity candidates.
        if (
            cleaned_word[0].isupper()
            and cleaned_word.lower()
            not in STOPWORDS
        ):

            if (
                cleaned_word.lower()
                not in {
                    "I",
                }
            ):

                proper_words.append(
                    cleaned_word
                )

    # Unique proper nouns.
    proper_unique = []

    seen = set()

    for word in proper_words:

        key = word.lower()

        if key not in seen:

            seen.add(key)
            proper_unique.append(word)

    queries = []

    # --------------------------------------------------------
    # Query 1 — strongest general entity query
    # --------------------------------------------------------

    if len(unique) >= 2:

        query = " ".join(
            unique[:4]
        )

        queries.append(query)

    # --------------------------------------------------------
    # Query 2 — proper-name query
    # --------------------------------------------------------

    if len(proper_unique) >= 2:

        query = " ".join(
            proper_unique[:4]
        )

        if query not in queries:

            queries.append(query)

    # --------------------------------------------------------
    # Query 3 — entity combination
    # --------------------------------------------------------

    if len(unique) >= 4:

        query = " ".join(
            unique[:6]
        )

        if query not in queries:

            queries.append(query)

    # --------------------------------------------------------
    # Very short claims
    # --------------------------------------------------------

    if not queries:

        fallback = " ".join(
            unique[:5]
        )

        if fallback:

            queries.append(
                fallback
            )

    # --------------------------------------------------------
    # Final cleanup
    # --------------------------------------------------------

    final_queries = []

    seen = set()

    for query in queries:

        query = query.strip()

        key = query.lower()

        if (
            query
            and key not in seen
        ):

            seen.add(key)

            final_queries.append(
                query
            )

    return final_queries[:3]


# ============================================================
# SINGLE CURRENTS SEARCH
# ============================================================

def search_currents(
    query,
    max_results=10,
):

    _check_key()

    query = str(query).strip()

    if not query:
        return []

    params = {

        "keywords": query,

        "language": "en",

        "page_number": 1,

        "page_size": min(
            int(max_results),
            20,
        ),
    }

    headers = {

        "Authorization":
            f"Bearer {CURRENTS_API_KEY}",
    }

    response = requests.get(

        SEARCH_URL,

        params=params,

        headers=headers,

        timeout=TIMEOUT,
    )

    if response.status_code == 401:

        raise RuntimeError(
            "Currents authentication failed."
        )

    if response.status_code == 429:

        raise RuntimeError(
            "Currents API rate limit reached."
        )

    response.raise_for_status()

    data = response.json()

    if data.get("status") not in {
        None,
        "ok",
        200,
        "200",
    }:

        raise RuntimeError(
            data
        )

    articles = (
        data.get("news")
        or []
    )

    results = []

    for article in articles:

        normalized = _normalize(
            article
        )

        if not normalized["url"]:
            continue

        if not normalized["title"]:
            continue

        results.append(
            normalized
        )

    return results


# ============================================================
# PUBLIC SEARCH
# ============================================================

def search_current_news(
    claim,
    max_results=10,
):
    """
    Main ClarifAI live-news search.

    Performs up to three focused searches
    and combines/deduplicates results.
    """

    queries = build_search_queries(
        claim
    )

    if not queries:
        return []

    print(
        "\nClarifAI search queries:"
    )

    for index, query in enumerate(
        queries,
        start=1,
    ):

        print(
            f"  {index}. {query}"
        )

    results = []

    seen_urls = set()

    for query in queries:

        current = search_currents(
            query,
            max_results=max_results,
        )

        for article in current:

            url = article.get(
                "url",
                "",
            )

            if not url:
                continue

            if url in seen_urls:
                continue

            seen_urls.add(url)

            results.append(
                article
            )

            if len(results) >= max_results:

                return results[
                    :max_results
                ]

    return results[
        :max_results
    ]


# ============================================================
# LATEST NEWS
# ============================================================

def get_latest_news(
    max_results=10,
    language="en",
):

    _check_key()

    params = {

        "language": language,

        "page_size": min(
            int(max_results),
            20,
        ),
    }

    headers = {

        "Authorization":
            f"Bearer {CURRENTS_API_KEY}",
    }

    response = requests.get(

        LATEST_URL,

        params=params,

        headers=headers,

        timeout=TIMEOUT,
    )

    if response.status_code == 401:

        raise RuntimeError(
            "Currents authentication failed."
        )

    if response.status_code == 429:

        raise RuntimeError(
            "Currents API rate limit reached."
        )

    response.raise_for_status()

    data = response.json()

    return [

        _normalize(article)

        for article in (
            data.get("news")
            or []
        )

    ][:max_results]


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def get_latest_currents_news(
    max_results=10,
):

    return get_latest_news(
        max_results=max_results
    )