"""
ClarifAI Verification Engine

Combines:
- user claim
- current evidence
- ML signals

The final explanation is generated separately.
"""

from .evidence_analyzer import analyze_evidence


def build_verification_context(
    claim,
    evidence,
):
    analysis = analyze_evidence(
        evidence
    )

    return {
        "claim": claim,

        "articles_found": analysis[
            "articles_found"
        ],

        "articles_extracted": analysis[
            "articles_extracted"
        ],

        "independent_domains": analysis[
            "independent_domains"
        ],

        "domains": analysis[
            "domains"
        ],

        "ml_real_count": analysis[
            "ml_real_count"
        ],

        "ml_fake_count": analysis[
            "ml_fake_count"
        ],

        "average_ml_confidence": analysis[
            "average_ml_confidence"
        ],

        "evidence_articles": analysis[
            "evidence_articles"
        ],
    }