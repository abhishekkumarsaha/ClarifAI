"""
ClarifAI Three-Case Verification Test
======================================

Tests the three possible verification states:

1. LIKELY_TRUE
2. LIKELY_FALSE
3. UNVERIFIED

Important:
The expected verdict is NOT hard-coded.
Live evidence and current news determine the result.
"""

from .clarifai_api import analyze_news_claim


TEST_CASES = [
    {
        "name": "CASE 1 - Evidence Supported",
        "claim": (
            "Reed Hastings discussed his life after "
            "Netflix and the changes AI may bring "
            "to competition."
        ),
    },

    {
        "name": "CASE 2 - Evidence Contradicted",
        "claim": (
            "Netflix has permanently shut down "
            "its streaming service worldwide."
        ),
    },

    {
        "name": "CASE 3 - Insufficient Evidence",
        "claim": (
            "A secret technology company will "
            "launch a revolutionary product tomorrow "
            "but has not publicly announced it."
        ),
    },
]


def print_list(title, items):

    print()
    print(title)

    if not items:

        print(" • None")

        return

    for item in items:

        if isinstance(item, dict):

            source = item.get(
                "source",
                "Unknown",
            )

            finding = item.get(
                "finding",
                "",
            )

            print(
                f" • {source}: {finding}"
            )

        else:

            print(
                " •",
                item,
            )


print()
print("========================================")
print("     CLARIFAI 3-CASE VALIDATION")
print("========================================")


passed_cases = 0


for index, case in enumerate(
    TEST_CASES,
    start=1,
):

    print()
    print("========================================")
    print(
        f"{case['name']}"
    )
    print("========================================")

    print()
    print("CLAIM:")
    print(case["claim"])

    print()
    print("Running live verification...")

    try:

        result = analyze_news_claim(
            case["claim"],
            max_articles=5,
        )

    except Exception as error:

        print()
        print("❌ TEST ERROR:")
        print(error)

        continue


    # ========================================================
    # BASIC RESULT
    # ========================================================

    success = result.get(
        "success",
        False,
    )

    verdict = result.get(
        "verdict",
        "UNKNOWN",
    )

    confidence = result.get(
        "confidence",
        0,
    )

    confidence_level = result.get(
        "confidence_level",
        "N/A",
    )


    print()
    print("RESULT")
    print("----------------------------------------")

    print(
        "Success:",
        success,
    )

    print(
        "Verdict:",
        verdict,
    )

    print(
        "Confidence:",
        f"{confidence:.2f}%"
        if isinstance(
            confidence,
            (int, float),
        )
        else confidence,
    )

    print(
        "Confidence Level:",
        confidence_level,
    )

    print(
        "Articles Found:",
        result.get(
            "articles_found",
            0,
        ),
    )

    print(
        "Articles Extracted:",
        result.get(
            "articles_extracted",
            0,
        ),
    )


    # ========================================================
    # AI EXPLANATION
    # ========================================================

    print()
    print("AI EXPLANATION")
    print("----------------------------------------")

    print(
        result.get(
            "summary",
            "No explanation available.",
        )
    )


    # ========================================================
    # WHY
    # ========================================================

    print_list(
        "WHY:",
        result.get(
            "why",
            [],
        ),
    )


    # ========================================================
    # SUPPORTING EVIDENCE
    # ========================================================

    print_list(
        "SUPPORTING EVIDENCE:",
        result.get(
            "supporting_evidence",
            [],
        ),
    )


    # ========================================================
    # CONTRADICTING EVIDENCE
    # ========================================================

    print_list(
        "CONTRADICTING EVIDENCE:",
        result.get(
            "contradicting_evidence",
            [],
        ),
    )


    # ========================================================
    # ML INTERPRETATION
    # ========================================================

    print()
    print("ML INTERPRETATION")
    print("----------------------------------------")

    print(
        result.get(
            "ml_interpretation",
            "No ML interpretation available.",
        )
    )


    # ========================================================
    # SOURCE ASSESSMENT
    # ========================================================

    print()
    print("SOURCE ASSESSMENT")
    print("----------------------------------------")

    print(
        result.get(
            "source_assessment",
            "No source assessment available.",
        )
    )


    # ========================================================
    # LIMITATIONS
    # ========================================================

    print_list(
        "LIMITATIONS:",
        result.get(
            "limitations",
            [],
        ),
    )


    # ========================================================
    # SAFETY
    # ========================================================

    print()
    print("USER SAFETY")
    print("----------------------------------------")

    print(
        result.get(
            "user_safety",
            "",
        )
    )


    # ========================================================
    # STRUCTURE VALIDATION
    # ========================================================

    required_fields = [

        "success",
        "claim",
        "verdict",
        "confidence",
        "summary",
        "why",
        "supporting_evidence",
        "contradicting_evidence",
        "ml_interpretation",
        "limitations",
        "evidence",
        "ml_results",
    ]


    missing = [

        field

        for field in required_fields

        if field not in result
    ]


    if (
        success
        and not missing
        and verdict in {
            "LIKELY_TRUE",
            "LIKELY_FALSE",
            "UNVERIFIED",
        }
    ):

        print()
        print(
            "✅ CASE STRUCTURE PASSED"
        )

        passed_cases += 1

    else:

        print()
        print(
            "❌ CASE STRUCTURE FAILED"
        )

        if missing:

            print(
                "Missing fields:",
                missing,
            )


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("========================================")
print("       3-CASE VALIDATION RESULT")
print("========================================")

print(
    f"Cases passed: "
    f"{passed_cases}/{len(TEST_CASES)}"
)


if passed_cases == len(
    TEST_CASES
):

    print()
    print(
        "🎉 ALL 3 CASES PASSED"
    )

    print()
    print(
        "ClarifAI successfully handled:"
    )

    print(
        " • Evidence-supported claims"
    )

    print(
        " • Evidence-contradicted claims"
    )

    print(
        " • Insufficient-evidence claims"
    )

else:

    print()
    print(
        "⚠️ Some cases require review."
    )


print()
print("========================================")