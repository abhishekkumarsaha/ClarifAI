"""
ClarifAI Verification Service
=============================

Pipeline:

Normal claim:
    Claim
        -> Currents live search
        -> Evidence extraction
        -> ML analysis
        -> Evidence aggregation
        -> AI verification/explanation
        -> Final structured result

URL:
    Article URL
        -> Direct article extraction
        -> Extract title/content/source
        -> Search current independent evidence
        -> Add original article as primary evidence
        -> Evidence extraction
        -> ML analysis
        -> Evidence aggregation
        -> AI verification/explanation
        -> Final structured result

Important:
    A URL being successfully extracted does NOT mean
    the article is true.

    The original article is treated as evidence and
    compared against independent current reporting.
"""


from urllib.parse import urlparse

from .news_search import search_current_news
from .article_extractor import extract_article, validate_url
from .evidence_pipeline import collect_evidence
from .evidence_pipeline import collect_evidence
from .ml_evidence_analyzer import (
    analyze_evidence as analyze_ml_evidence,
)
from .evidence_analyzer import (
    analyze_evidence as aggregate_evidence,
)
from .ai_explainer import (
    generate_verification_explanation,
)


# ============================================================
# HELPERS
# ============================================================

def _confidence_level(confidence):
    """Convert 0-100 confidence to a readable level."""

    try:
        confidence = float(confidence)

    except (
        TypeError,
        ValueError,
    ):
        confidence = 0.0

    if confidence >= 90:
        return "Very High"

    if confidence >= 75:
        return "High"

    if confidence >= 55:
        return "Moderate"

    if confidence >= 35:
        return "Low"

    return "Very Low"


def _safe_float(
    value,
    default=0.0,
):
    """Safely convert a value to float."""

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return default


def _is_article_url(value):
    """
    Return True when the supplied input is a valid
    HTTP/HTTPS URL.
    """

    if not value:
        return False

    try:
        return validate_url(
            str(value).strip()
        )

    except Exception:
        return False


def _domain_from_url(url):
    """Extract a clean domain from a URL."""

    if not url:
        return "Unknown"

    try:
        hostname = urlparse(
            str(url)
        ).netloc.lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        return hostname or "Unknown"

    except Exception:
        return "Unknown"


def _build_fallback(
    claim,
    evidence,
    evidence_summary,
    articles_found,
    error_message,
    input_type="claim",
    source_url="",
    article_title="",
    source_domain="",
):
    """
    Safe result returned when the AI layer fails.

    We NEVER call a claim true/false simply because
    the AI layer failed.
    """

    return {
        "success": True,

        "input_type": input_type,

        "claim": claim,

        "source_url": source_url,

        "source_domain": source_domain,

        "article_title": article_title,

        "verdict": "UNVERIFIED",

        "confidence": 0.0,

        "confidence_level": "Very Low",

        "summary": (
            "ClarifAI found current evidence, "
            "but could not generate a reliable "
            "AI verification assessment."
        ),

        "why": [
            (
                "The AI explanation layer was "
                "unavailable or returned an invalid "
                "response."
            )
        ],

        "supporting_evidence": [],

        "contradicting_evidence": [],

        "ml_interpretation": (
            "The ML classifier provides linguistic "
            "signals only. Its prediction is not "
            "treated as factual proof."
        ),

        "source_assessment": (
            f"{evidence_summary.get('independent_domains', 0)} "
            "independent publisher domains were found."
        ),

        "limitations": [
            error_message
        ],

        "user_safety": (
            "Do not treat an unverified claim "
            "as established fact."
        ),

        "evidence": evidence,

        "evidence_summary": evidence_summary,

        "articles_found": articles_found,

        "articles_extracted": (
            evidence_summary.get(
                "articles_extracted",
                0,
            )
        ),

        "ml_results": [
            item.get("ml_analysis")
            for item in evidence
            if item.get("ml_analysis")
        ],

        "ai_available": False,
    }


# ============================================================
# MAIN VERIFICATION FUNCTION
# ============================================================
def _is_url(value):
    """Return True when the input is a valid HTTP/HTTPS URL."""

    value = str(value or "").strip()

    if not value:
        return False

    try:
        parsed = urlparse(value)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False
def verify_news_claim(
    claim,
    max_articles=5,
):
    """
    Complete ClarifAI verification pipeline.

    Supports:

        1. Normal natural-language claims
        2. Direct article URLs
    """

    # ========================================================
    # 1. VALIDATE INPUT
    # ========================================================

    original_input = str(
        claim or ""
    ).strip()

    if not original_input:

        return {
            "success": False,
            "input_type": "claim",
            "claim": "",
            "error": "Please enter a news claim or article URL.",
        }

    # ========================================================
    # 2. DETERMINE INPUT TYPE
    # ========================================================

    input_type = "claim"

    source_article = None

    source_url = ""

    article_title = ""

    source_domain = ""

    search_query = original_input

    # ========================================================
    # 3. URL MODE
    # ========================================================

    if _is_article_url(
        original_input
    ):

        input_type = "url"

        source_url = original_input

        print()
        print("=" * 60)
        print("ClarifAI URL VERIFICATION")
        print("=" * 60)
        print("URL:")
        print(source_url)
        print()

        # ----------------------------------------------------
        # DIRECT ARTICLE EXTRACTION
        # ----------------------------------------------------

        try:
            extracted = extract_article(source_url)
        except Exception as error:
            return {
                "success": False,
                "input_type": "url",
                "claim": original_input,
                "source_url": source_url,
                "error": f"Article extraction failed: {error}",
            }

        # Current article_extractor.py returns ArticleData.
        # Older versions may return a dictionary, so support both.
        if isinstance(extracted, dict):
            extraction_success = extracted.get("success", True)
            article_title = (
                extracted.get("title", "") or "Untitled Article"
            )
            article_content = extracted.get("content", "") or ""
            final_url = extracted.get("final_url", "") or source_url
            original_article_url = (
                extracted.get("original_url", "") or source_url
            )
            evidence_quality = extracted.get(
                "evidence_quality", "FULL_ARTICLE"
            )
            extraction_method = extracted.get(
                "method", "article_extractor"
            )
            extraction_error = extracted.get("error", "")
        else:
            extraction_success = True
            article_title = (
                getattr(extracted, "title", "") or "Untitled Article"
            )
            article_content = getattr(
                extracted, "article_text", ""
            ) or ""
            final_url = (
                getattr(extracted, "source_url", "") or source_url
            )
            original_article_url = final_url
            evidence_quality = "FULL_ARTICLE"
            extraction_method = "trafilatura"
            extraction_error = ""

        if not extraction_success:
            return {
                "success": False,
                "input_type": "url",
                "claim": original_input,
                "source_url": source_url,
                "error": (
                    extraction_error
                    or "Unable to extract article content."
                ),
                "extraction_method": extraction_method,
                "evidence_quality": evidence_quality,
            }

        if len(article_content.split()) < 50:
            return {
                "success": False,
                "input_type": "url",
                "claim": original_input,
                "source_url": source_url,
                "error": (
                    "The extracted article content is too short "
                    "for reliable verification."
                ),
                "extraction_method": extraction_method,
                "evidence_quality": evidence_quality,
            }

        source_domain = _domain_from_url(final_url)

        source_article = {
            "title": article_title,
            "source": source_domain,
            "url": final_url,
            "original_url": original_article_url,
            "content": article_content,
            "description": "",
            "published_at": "",
            "provider": "Direct Publisher",
            "input_method": "url",
            "evidence_quality": evidence_quality,
        }

        # ----------------------------------------------------
        # SEARCH USING ARTICLE TITLE
        # ----------------------------------------------------
        #
        # IMPORTANT:
        #
        # We do NOT change the user's original claim.
        #
        # The title is used only to discover related
        # current evidence.
        # ----------------------------------------------------

        search_query = article_title

        print(
            "Article title:",
            article_title,
        )

        print(
            "Source:",
            source_domain,
        )

        print(
            "Extracted words:",
            len(
                article_content.split()
            ),
        )

        print("Evidence quality:", evidence_quality)

        print()

    # ========================================================
    # 4. NORMAL CLAIM MODE
    # ========================================================

    else:

        input_type = "claim"

        search_query = original_input

        print()
        print("=" * 60)
        print("ClarifAI CLAIM VERIFICATION")
        print("=" * 60)
        print("Claim:")
        print(original_input)
        print()

    # ========================================================
    # 5. NORMALIZE ARTICLE LIMIT
    # ========================================================

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

    # ========================================================
    # ========================================================
    # 6. LIVE NEWS / INDEPENDENT EVIDENCE SEARCH
    # ========================================================

    print()
    print("Running ClarifAI...")
    print()

    try:
        articles = search_current_news(
            search_query,
            max_results=10,
        )
    except Exception as error:
        # In URL mode, the directly extracted article remains
        # usable evidence even when independent search fails.
        if source_article:
            articles = []
        else:
            return {
                "success": False,
                "input_type": input_type,
                "claim": original_input,
                "error": (
                    "Live news search failed: "
                    f"{error}"
                ),
            }

    if not isinstance(articles, list):
        articles = []

    # 7. URL MODE — ADD ORIGINAL ARTICLE
    # ========================================================

    if source_article:

        # Avoid duplicate URL if the live search
        # already returned the same article.

        original_url_normalized = (
            source_article.get(
                "url",
                "",
            )
            .rstrip("/")
            .lower()
        )

        filtered_articles = []

        for article in articles:

            if not isinstance(
                article,
                dict,
            ):
                continue

            article_url = (
                str(
                    article.get(
                        "url",
                        "",
                    )
                )
                .rstrip("/")
                .lower()
            )

            if (
                article_url
                == original_url_normalized
            ):
                continue

            filtered_articles.append(
                article
            )

        # Original user article is always first.
        articles = [
            source_article,
            *filtered_articles,
        ]

    # ========================================================
    # 8. NO SEARCH RESULTS
    # ========================================================

    if not articles:

        if source_article:

            # We still have the user's article.
            articles = [
                source_article
            ]

        else:

            return {
                "success": True,

                "input_type": input_type,

                "claim": original_input,

                "source_url": "",

                "article_title": "",

                "source_domain": "",

                "verdict": "UNVERIFIED",

                "confidence": 0.0,

                "confidence_level": "Very Low",

                "summary": (
                    "ClarifAI could not find "
                    "current evidence to evaluate "
                    "this claim."
                ),

                "why": [
                    (
                        "No current news evidence "
                        "was returned by the search provider."
                    )
                ],

                "supporting_evidence": [],

                "contradicting_evidence": [],

                "ml_interpretation": (
                    "No ML evidence was available."
                ),

                "source_assessment": (
                    "No current sources were found."
                ),

                "limitations": [
                    (
                        "Live news search returned "
                        "no usable results."
                    )
                ],

                "user_safety": (
                    "Do not treat an unverified "
                    "claim as established fact."
                ),

                "evidence": [],

                "evidence_summary": {
                    "articles_found": 0,
                    "articles_extracted": 0,
                    "independent_domains": 0,
                    "domains": [],
                },

                "articles_found": 0,

                "articles_extracted": 0,

                "ml_results": [],

                "ai_available": False,
            }

    print(
        "News articles discovered:",
        len(articles),
    )

    # ========================================================
    # 9. EXTRACT ARTICLE EVIDENCE
    # ========================================================

    try:

        evidence = collect_evidence(
            articles,
            max_articles=max_articles,
        )

    except Exception as error:

        return {
            "success": False,

            "input_type": input_type,

            "claim": original_input,

            "source_url": source_url,

            "article_title": article_title,

            "source_domain": source_domain,

            "error": (
                "Evidence extraction failed: "
                f"{error}"
            ),
        }

    if not isinstance(
        evidence,
        list,
    ):

        evidence = []

    # ========================================================
    # 10. RUN CALIBRATED SVM
    # ========================================================

    try:

        evidence_with_ml = analyze_ml_evidence(
            evidence
        )

    except Exception as error:

        return {
            "success": False,

            "input_type": input_type,

            "claim": original_input,

            "source_url": source_url,

            "article_title": article_title,

            "source_domain": source_domain,

            "error": (
                "ML evidence analysis failed: "
                f"{error}"
            ),
        }

    if not isinstance(
        evidence_with_ml,
        list,
    ):

        evidence_with_ml = evidence

    # ========================================================
    # 11. AGGREGATE EVIDENCE
    # ========================================================

    try:

        evidence_summary = aggregate_evidence(
            evidence_with_ml
        )

    except Exception as error:

        evidence_summary = {
            "articles_found": len(
                evidence_with_ml
            ),

            "articles_extracted": sum(
                1
                for item in evidence_with_ml
                if isinstance(
                    item,
                    dict,
                )
                and item.get(
                    "extraction_success",
                    False,
                )
            ),

            "independent_domains": 0,

            "domains": [],

            "ml_real_count": 0,

            "ml_fake_count": 0,

            "average_ml_confidence": 0.0,

            "error": str(error),
        }

    # ========================================================
    # 12. NO USABLE EVIDENCE
    # ========================================================

    if not evidence_with_ml:

        return {
            "success": True,

            "input_type": input_type,

            "claim": original_input,

            "source_url": source_url,

            "article_title": article_title,

            "source_domain": source_domain,

            "verdict": "UNVERIFIED",

            "confidence": 0.0,

            "confidence_level": "Very Low",

            "summary": (
                "ClarifAI could not find "
                "sufficient usable evidence "
                "to evaluate this claim."
            ),

            "why": [
                (
                    "No successfully extracted "
                    "articles were available "
                    "for verification."
                )
            ],

            "supporting_evidence": [],

            "contradicting_evidence": [],

            "ml_interpretation": (
                "No ML analysis was possible "
                "because no usable article "
                "evidence was available."
            ),

            "source_assessment": (
                "No usable article sources "
                "were available."
            ),

            "limitations": [
                (
                    "Current search results did "
                    "not provide usable article "
                    "content."
                )
            ],

            "user_safety": (
                "Do not treat an unverified "
                "claim as established fact."
            ),

            "evidence": [],

            "evidence_summary": evidence_summary,

            "articles_found": len(
                articles
            ),

            "articles_extracted": 0,

            "ml_results": [],

            "ai_available": False,
        }

    # ========================================================
    # 13. AI VERIFICATION
    # ========================================================

    print(
        "Generating evidence-grounded verification..."
    )

    try:

        ai_result = (
            generate_verification_explanation(
                claim=original_input,
                evidence=evidence_with_ml,
                ml_results=evidence_with_ml,
                evidence_summary=evidence_summary,
            )
        )

    except Exception as error:

        return _build_fallback(
            claim=original_input,

            evidence=evidence_with_ml,

            evidence_summary=evidence_summary,

            articles_found=len(
                articles
            ),

            error_message=str(
                error
            ),

            input_type=input_type,

            source_url=source_url,

            article_title=article_title,

            source_domain=source_domain,
        )

    # ========================================================
    # 14. AI FAILURE FALLBACK
    # ========================================================

    if not isinstance(
        ai_result,
        dict,
    ):

        return _build_fallback(
            claim=original_input,

            evidence=evidence_with_ml,

            evidence_summary=evidence_summary,

            articles_found=len(
                articles
            ),

            error_message=(
                "Invalid response from "
                "AI explanation layer."
            ),

            input_type=input_type,

            source_url=source_url,

            article_title=article_title,

            source_domain=source_domain,
        )

    if not ai_result.get(
        "success",
        False,
    ):

        return _build_fallback(
            claim=original_input,

            evidence=evidence_with_ml,

            evidence_summary=evidence_summary,

            articles_found=len(
                articles
            ),

            error_message=ai_result.get(
                "error",
                "AI explanation unavailable.",
            ),

            input_type=input_type,

            source_url=source_url,

            article_title=article_title,

            source_domain=source_domain,
        )

    # ========================================================
    # 15. GET AI EXPLANATION
    # ========================================================

    explanation = ai_result.get(
        "explanation",
        {},
    )

    if not isinstance(
        explanation,
        dict,
    ):

        return _build_fallback(
            claim=original_input,

            evidence=evidence_with_ml,

            evidence_summary=evidence_summary,

            articles_found=len(
                articles
            ),

            error_message=(
                "AI returned an invalid "
                "explanation structure."
            ),

            input_type=input_type,

            source_url=source_url,

            article_title=article_title,

            source_domain=source_domain,
        )

    # ========================================================
    # 16. VERDICT
    # ========================================================

    verdict = str(
        explanation.get(
            "verdict",
            "UNVERIFIED",
        )
    ).upper().strip()

    if verdict not in {
        "LIKELY_TRUE",
        "LIKELY_FALSE",
        "UNVERIFIED",
    }:

        verdict = "UNVERIFIED"

    # ========================================================
    # 17. CONFIDENCE
    # ========================================================

    confidence = _safe_float(
        explanation.get(
            "confidence",
            0,
        )
    )

    # AI may return 0.90 instead of 90.

    if 0 <= confidence <= 1:

        confidence *= 100

    confidence = max(
        0.0,
        min(
            100.0,
            confidence,
        ),
    )

    confidence = round(
        confidence,
        2,
    )

    confidence_level = explanation.get(
        "confidence_level"
    )

    if not confidence_level:

        confidence_level = _confidence_level(
            confidence
        )

    # ========================================================
    # 18. FINAL STRUCTURED RESPONSE
    # ========================================================

    return {
        "success": True,

        "input_type": input_type,

        "claim": original_input,

        "source_url": source_url,

        "source_domain": source_domain,

        "article_title": article_title,

        "verdict": verdict,

        "confidence": confidence,

        "confidence_level": confidence_level,

        "summary": explanation.get(
            "summary",
            "",
        ),

        "why": explanation.get(
            "why",
            [],
        ),

        "supporting_evidence": explanation.get(
            "supporting_evidence",
            [],
        ),

        "contradicting_evidence": explanation.get(
            "contradicting_evidence",
            [],
        ),

        "ml_interpretation": explanation.get(
            "ml_interpretation",
            "",
        ),

        "source_assessment": explanation.get(
            "source_assessment",
            "",
        ),

        "limitations": explanation.get(
            "limitations",
            [],
        ),

        "user_safety": explanation.get(
            "user_safety",
            "",
        ),

        "evidence": evidence_with_ml,

        "evidence_summary": evidence_summary,

        "articles_found": len(
            articles
        ),

        "articles_extracted": (
            evidence_summary.get(
                "articles_extracted",
                0,
            )
        ),

        "ml_results": [
            item.get(
                "ml_analysis"
            )
            for item in evidence_with_ml
            if isinstance(
                item,
                dict,
            )
            and item.get(
                "ml_analysis"
            )
        ],

        "ai_available": True,
    }


