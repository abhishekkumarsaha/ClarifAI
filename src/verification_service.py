"""
ClarifAI Verification Service

Pipeline:

Claim
    -> Currents live search
    -> Evidence extraction
    -> ML analysis
    -> Evidence aggregation
    -> AI verification/explanation
    -> Final structured result
"""

from .news_search import search_current_news
from .evidence_pipeline import collect_evidence
from .ml_evidence_analyzer import analyze_evidence as analyze_ml_evidence
from .evidence_analyzer import analyze_evidence as aggregate_evidence
from .ai_explainer import generate_verification_explanation


def _confidence_level(confidence):
    """Convert 0-100 confidence to a readable level."""

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
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


def _safe_float(value, default=0.0):
    """Safely convert a value to float."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _build_fallback(
    claim,
    evidence,
    evidence_summary,
    articles_found,
    error_message,
):
    """
    Safe result returned when the AI layer fails.

    We NEVER call a claim true/false simply because
    the AI layer failed.
    """

    return {
        "success": True,
        "claim": claim,

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


def verify_news_claim(
    claim,
    max_articles=5,
):
    """
    Complete ClarifAI verification pipeline.
    """

    # ========================================================
    # 1. VALIDATE CLAIM
    # ========================================================

    claim = str(
        claim or ""
    ).strip()

    if not claim:

        return {
            "success": False,
            "claim": "",
            "error": "Please enter a news claim.",
        }

    # ========================================================
    # 2. NORMALIZE ARTICLE LIMIT
    # ========================================================

    try:
        max_articles = int(
            max_articles
        )
    except (TypeError, ValueError):
        max_articles = 5

    max_articles = max(
        1,
        min(
            max_articles,
            10,
        ),
    )

    # ========================================================
    # 3. LIVE NEWS SEARCH
    # ========================================================

    print()
    print("Running ClarifAI...")
    print()

    try:

        articles = search_current_news(
            claim,
            max_results=10,
        )

    except Exception as error:

        return {
            "success": False,
            "claim": claim,
            "error": (
                "Live news search failed: "
                f"{error}"
            ),
        }

    if not isinstance(
        articles,
        list,
    ):

        articles = []

    # ========================================================
    # 4. EXTRACT ARTICLE EVIDENCE
    # ========================================================

    try:

        evidence = collect_evidence(
            articles,
            max_articles=max_articles,
        )

    except Exception as error:

        return {
            "success": False,
            "claim": claim,
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
    # 5. RUN CALIBRATED SVM
    # ========================================================

    try:

        evidence_with_ml = analyze_ml_evidence(
            evidence
        )

    except Exception as error:

        return {
            "success": False,
            "claim": claim,
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
    # 6. AGGREGATE EVIDENCE
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
                if item.get(
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
    # 7. NO EVIDENCE
    # ========================================================

    if not evidence_with_ml:

        return {
            "success": True,

            "claim": claim,

            "verdict": "UNVERIFIED",

            "confidence": 0.0,

            "confidence_level": "Very Low",

            "summary": (
                "ClarifAI could not find "
                "sufficient current evidence "
                "to evaluate this claim."
            ),

            "why": [
                (
                    "No successfully extracted "
                    "articles were available for "
                    "verification."
                )
            ],

            "supporting_evidence": [],

            "contradicting_evidence": [],

            "ml_interpretation": (
                "No ML analysis was possible "
                "because no article evidence "
                "was successfully extracted."
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
    # 8. AI VERIFICATION
    # ========================================================

    try:

        ai_result = generate_verification_explanation(
            claim=claim,
            evidence=evidence_with_ml,
            ml_results=evidence_with_ml,
            evidence_summary=evidence_summary,
        )

    except Exception as error:

        return _build_fallback(
            claim=claim,
            evidence=evidence_with_ml,
            evidence_summary=evidence_summary,
            articles_found=len(articles),
            error_message=str(error),
        )

    # ========================================================
    # 9. AI FAILURE FALLBACK
    # ========================================================

    if not isinstance(
        ai_result,
        dict,
    ):

        return _build_fallback(
            claim=claim,
            evidence=evidence_with_ml,
            evidence_summary=evidence_summary,
            articles_found=len(articles),
            error_message=(
                "Invalid response from AI explanation layer."
            ),
        )

    if not ai_result.get(
        "success",
        False,
    ):

        return _build_fallback(
            claim=claim,
            evidence=evidence_with_ml,
            evidence_summary=evidence_summary,
            articles_found=len(articles),
            error_message=ai_result.get(
                "error",
                "AI explanation unavailable.",
            ),
        )

    # ========================================================
    # 10. GET AI EXPLANATION
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
            claim=claim,
            evidence=evidence_with_ml,
            evidence_summary=evidence_summary,
            articles_found=len(articles),
            error_message=(
                "AI returned an invalid explanation structure."
            ),
        )

    # ========================================================
    # 11. VERDICT
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
    # 12. CONFIDENCE
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
    # 13. FINAL RESPONSE
    # ========================================================

    return {
        "success": True,

        "claim": claim,

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
            item.get("ml_analysis")
            for item in evidence_with_ml
            if item.get("ml_analysis")
        ],

        "ai_available": True,
    }