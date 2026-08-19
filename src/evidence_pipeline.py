"""
ClarifAI Evidence Pipeline
==========================

Search results are ranked and converted into
structured evidence.

When a user directly submits an article URL,
that original article is always preserved as
primary evidence.
"""

from .source_ranker import rank_articles

from .evidence_extractor import (
    extract_article,
)


def collect_evidence(
    articles,
    max_articles=5,
):

    if not articles:
        return []

    # ========================================================
    # IDENTIFY USER-SUBMITTED ARTICLE
    # ========================================================

    original_article = None

    for article in articles:

        if not isinstance(
            article,
            dict,
        ):
            continue

        if article.get(
            "input_method"
        ) == "url":

            original_article = article
            break

    # ========================================================
    # RANK SEARCH RESULTS
    # ========================================================

    selected = rank_articles(
        articles,
        limit=max_articles,
    )

    if not isinstance(
        selected,
        list,
    ):
        selected = []

    # ========================================================
    # ALWAYS PRESERVE ORIGINAL URL ARTICLE
    # ========================================================

    if original_article:

        original_url = (
            str(
                original_article.get(
                    "url",
                    "",
                )
            )
            .rstrip("/")
            .lower()
        )

        # Remove duplicate copy.
        selected = [
            article
            for article in selected
            if str(
                article.get(
                    "url",
                    "",
                )
            )
            .rstrip("/")
            .lower()
            != original_url
        ]

        # Original article always goes first.
        selected.insert(
            0,
            original_article,
        )

        # Respect requested evidence limit.
        selected = selected[
            :max_articles
        ]

    # ========================================================
    # EXTRACT EVIDENCE
    # ========================================================

    evidence = []

    for article in selected:

        if not isinstance(
            article,
            dict,
        ):
            continue

        extraction = extract_article(

            url=article.get(
                "url",
                "",
            ),

            supplied_content=article.get(
                "content",
                "",
            ),

            supplied_description=article.get(
                "description",
                "",
            ),

            supplied_title=article.get(
                "title",
                "",
            ),
        )

        # ====================================================
        # EXTRACTION RESULT
        # ====================================================

        content = extraction.get(
            "content",
            "",
        )

        quality = extraction.get(
            "evidence_quality",
            "UNAVAILABLE",
        )

        # ====================================================
        # HEADLINE/DESCRIPTION FALLBACK
        # ====================================================

        if (
            not content
            and (
                article.get(
                    "title",
                    "",
                )
                or article.get(
                    "description",
                    "",
                )
            )
        ):

            title = article.get(
                "title",
                "",
            )

            description = article.get(
                "description",
                "",
            )

            content = (
                f"Headline: {title}\n\n"
                f"Description: {description}"
            )

            quality = "HEADLINE_ONLY"

        # ====================================================
        # BUILD EVIDENCE OBJECT
        # ====================================================

        evidence.append(
            {
                "title": article.get(
                    "title",
                    "",
                ),

                "source": article.get(
                    "source",
                    "Unknown",
                ),

                "url": article.get(
                    "url",
                    "",
                ),

                "published_at": article.get(
                    "published_at",
                    "",
                ),

                "provider": article.get(
                    "provider",
                    "Currents",
                ),

                "content": content,

                "extraction_success": bool(
                    extraction.get(
                        "success",
                        False,
                    )
                ),

                "extraction_method": (
                    extraction.get(
                        "method",
                        "none",
                    )
                ),

                "evidence_quality": quality,

                "extraction_error": (
                    extraction.get(
                        "error",
                        "",
                    )
                ),

                "original_url": (
                    extraction.get(
                        "original_url",
                        article.get(
                            "url",
                            "",
                        ),
                    )
                ),

                "final_url": (
                    extraction.get(
                        "final_url",
                        article.get(
                            "url",
                            "",
                        ),
                    )
                ),

                "article_title": (
                    extraction.get(
                        "title",
                        article.get(
                            "title",
                            "",
                        ),
                    )
                ),

                "input_method": article.get(
                    "input_method",
                    "search",
                ),

                "ml_analysis": None,
            }
        )

    return evidence