"""
ClarifAI Evidence Pipeline
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

    selected = rank_articles(
        articles,
        limit=max_articles,
    )

    evidence = []

    for article in selected:

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

        # ----------------------------------------------------
        # If full extraction failed, preserve metadata
        # as usable limited evidence.
        # ----------------------------------------------------

        content = extraction.get(
            "content",
            "",
        )

        quality = extraction.get(
            "evidence_quality",
            "UNAVAILABLE",
        )

        if (
            not content
            and (
                article.get(
                    "title",
                    ""
                )
                or article.get(
                    "description",
                    ""
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

                "ml_analysis": None,
            }
        )

    return evidence