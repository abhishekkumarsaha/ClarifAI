"""
ClarifAI Unified Article Analyzer
"""

from src.article_input import create_pasted_article
from src.article_extractor import extract_article
from src.clarifai_engine import analyze_news
from src.ai_explainer import generate_explanation


def _attach_ai_explanation(article, result):

    prediction = result.get("prediction", "")
    confidence = result.get("confidence", 0)
    signals = result.get("signals", [])

    confidence_value = float(confidence)

    if confidence_value <= 1:
        confidence_value *= 100

    explanation = generate_explanation(
        title=article.title,
        article_text=article.article_text,
        prediction=prediction,
        confidence=confidence_value,
        signals=signals,
    )

    result["ai_explanation"] = explanation

    return result


def analyze_pasted_article(title: str, article_text: str):

    article = create_pasted_article(
        title=title,
        article_text=article_text,
    )

    result = analyze_news(
        article.title,
        article.article_text,
    )

    result["title"] = article.title
    result["article_text"] = article.article_text
    result["source_url"] = article.source_url
    result["source_domain"] = article.source_domain
    result["input_method"] = article.input_method
    result["word_count"] = article.word_count

    return _attach_ai_explanation(article, result)


def analyze_article_url(url: str):

    article = extract_article(url)

    result = analyze_news(
        article.title,
        article.article_text,
    )

    result["title"] = article.title
    result["article_text"] = article.article_text
    result["source_url"] = article.source_url
    result["source_domain"] = article.source_domain
    result["input_method"] = article.input_method
    result["word_count"] = article.word_count

    return _attach_ai_explanation(article, result)