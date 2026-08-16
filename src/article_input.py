"""
ClarifAI Article Input Handling
Normalizes pasted articles and URL-extracted articles
into a common format.
"""

from datetime import datetime, timezone

from .article_extractor import ArticleData

def create_pasted_article(
    title: str,
    article_text: str,
) -> ArticleData:
    """
    Create an ArticleData object from manually pasted content.
    """

    title = (title or "").strip()
    article_text = (article_text or "").strip()

    if not article_text:
        raise ValueError("Article text cannot be empty.")

    if len(article_text.split()) < 50:
        raise ValueError(
            "Please provide a longer article. "
            "At least 50 words are recommended for analysis."
        )

    if not title:
        title = "Untitled Article"

    return ArticleData(
        title=title,
        article_text=article_text,
        source_url="",
        source_domain="Manual Input",
        input_method="paste",
        word_count=len(article_text.split()),
        extracted_at=datetime.now(timezone.utc).isoformat(),
    )