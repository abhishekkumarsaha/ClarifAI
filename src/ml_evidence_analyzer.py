"""
ClarifAI ML Evidence Analyzer

Runs the existing ClarifAI ML analyzer
against every successfully extracted article.
"""

from .clarifai_engine import analyze_news


def analyze_evidence(
    evidence,
):
    """
    Run the existing calibrated ML pipeline
    on extracted evidence articles.
    """

    analyzed = []

    for item in evidence:

        if not item.get(
            "extraction_success",
            False,
        ):

            item["ml_analysis"] = None

            analyzed.append(item)

            continue

        try:

            title = (
                item.get("article_title")
                or item.get("title")
                or ""
            )

            article_text = (
                item.get("content")
                or ""
            )

            # IMPORTANT:
            # Your existing function signature is:
            # analyze_news(title, article)

            result = analyze_news(
                title,
                article_text,
            )

            item["ml_analysis"] = result

        except Exception as error:

            item["ml_analysis"] = {
                "error": str(error)
            }

        analyzed.append(item)

    return analyzed