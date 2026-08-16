"""
ClarifAI Public Backend API
===========================

This is the single public interface that the
frontend should use.

Frontend
    ↓
analyze_news_claim()
    ↓
verification_service
    ↓
Live News + Evidence + ML + AI Explanation
"""


from .verification_service import (
    verify_news_claim,
)


def analyze_news_claim(
    claim,
    max_articles=5,
):
    """
    Analyze a natural-language news claim.

    Parameters
    ----------
    claim : str
        News claim entered by the user.

    max_articles : int
        Maximum number of live evidence articles.

    Returns
    -------
    dict
        Structured ClarifAI verification result.
    """

    claim = str(
        claim or ""
    ).strip()

    # --------------------------------------------------------
    # Input validation
    # --------------------------------------------------------

    if not claim:

        return {
            "success": False,
            "error": (
                "Please enter a news claim."
            ),
        }

    # --------------------------------------------------------
    # Validate article count
    # --------------------------------------------------------

    try:

        max_articles = int(
            max_articles
        )

    except (
        TypeError,
        ValueError,
    ):

        max_articles = 5

    max_articles = max(
        1,
        min(
            max_articles,
            10,
        ),
    )

    # --------------------------------------------------------
    # Run complete ClarifAI backend
    # --------------------------------------------------------

    return verify_news_claim(
        claim=claim,
        max_articles=max_articles,
    )