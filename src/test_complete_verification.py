from .verification_service import (
    verify_news_claim,
)


print()
print("========================================")
print("       CLARIFAI FINAL VERIFICATION")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


print()
print("Running ClarifAI...")
print()


result = verify_news_claim(
    claim,
    max_articles=5,
)


if not result.get(
    "success"
):

    print(
        "VERIFICATION FAILED"
    )

    print(
        "Stage:",
        result.get(
            "stage"
        ),
    )

    print(
        "Error:",
        result.get(
            "error"
        ),
    )

    raise SystemExit


print(
    "========================================"
)

print(
    "VERDICT:",
    result.get(
        "verdict"
    ),
)

print(
    "CONFIDENCE:",
    f"{result.get('confidence', 0):.2f}%"
)

print()

print(
    "SUMMARY:"
)

print(
    result.get(
        "summary",
        "",
    )
)

print()

print(
    "WHY:"
)

for reason in result.get(
    "why",
    [],
):

    print(
        " •",
        reason,
    )

print()

print(
    "ML INTERPRETATION:"
)

print(
    result.get(
        "ml_interpretation",
        "",
    )
)

print()

print(
    "SOURCE ASSESSMENT:"
)

print(
    result.get(
        "source_assessment",
        "",
    )
)

print()

print(
    "SUPPORTING EVIDENCE:"
)

for item in result.get(
    "supporting_evidence",
    [],
):

    print(
        " •",
        item,
    )

print()

print(
    "CONTRADICTING EVIDENCE:"
)

for item in result.get(
    "contradicting_evidence",
    [],
):

    print(
        " •",
        item,
    )

print()

print(
    "LIMITATIONS:"
)

for item in result.get(
    "limitations",
    [],
):

    print(
        " •",
        item,
    )

print()

print(
    "EVIDENCE:"
)

print(
    "Articles found:",
    result.get(
        "articles_found",
        0,
    ),
)

print(
    "Articles extracted:",
    result.get(
        "articles_extracted",
        0,
    ),
)

source_metadata = result.get(
    "source_metadata",
    {},
)

print(
    "Independent sources:",
    source_metadata.get(
        "independent_sources",
        0,
    ),
)

print()

print(
    "USER SAFETY:"
)

print(
    result.get(
        "user_safety",
        "",
    )
)

print()
print("========================================")
print("       FINAL VERIFICATION COMPLETE")
print("========================================")