from .ai_explainer import (
    generate_verification_explanation,
)


print()
print("========================================")
print("       CLARIFAI AI EXPLAINER TEST")
print("========================================")


claim = """
Netflix co-founder Reed Hastings stopped
calling CEOs Ted Sarandos and Greg Peters.
"""


evidence = [

    {
        "source": "Example News Source A",

        "title": (
            "Reed Hastings discusses life "
            "after Netflix"
        ),

        "description": (
            "Reed Hastings discusses his "
            "post-Netflix activities."
        ),

        "published_at":
            "2026-08-14",

        "url":
            "https://example.com/article-a",

        "evidence_quality":
            "FULL_ARTICLE",

        "content": """
        Reed Hastings discussed his life
        after Netflix and changes in his
        professional activities.
        The article does not mention
        Ted Sarandos or Greg Peters.
        """,
    },

    {
        "source": "Example News Source B",

        "title": (
            "Netflix leadership discusses "
            "company strategy"
        ),

        "description": (
            "Netflix executives discuss "
            "company leadership."
        ),

        "published_at":
            "2026-08-14",

        "url":
            "https://example.com/article-b",

        "evidence_quality":
            "FULL_ARTICLE",

        "content": """
        Netflix leadership discussed
        company strategy and management.
        The article does not establish
        why Reed Hastings stopped calling
        Ted Sarandos or Greg Peters.
        """,
    },
]


ml_results = [

    {
        "source":
            "Example News Source A",

        "prediction":
            "FAKE",

        "confidence":
            99.1,

        "confidence_level":
            "Very High",

        "signals": [
            {
                "feature": "example",
                "contribution": -0.1,
            }
        ],

        "success":
            True,
    }
]


evidence_summary = {

    "total_articles": 2,

    "independent_sources": 2,

    "full_article_sources": 2,

    "headline_only_sources": 0,
}


result = (
    generate_verification_explanation(

        claim=claim,

        evidence=evidence,

        ml_results=ml_results,

        evidence_summary=
            evidence_summary,
    )
)


if not result.get(
    "success"
):

    print()
    print(
        "AI EXPLAINER FAILED:"
    )

    print(
        result.get(
            "error"
        )
    )

    raise SystemExit(1)


explanation = result[
    "explanation"
]


print()
print(
    "VERDICT:",
    explanation.get(
        "verdict"
    ),
)

print(
    "CONFIDENCE:",
    explanation.get(
        "confidence"
    ),
)

print()

print(
    "SUMMARY:"
)

print(
    explanation.get(
        "summary"
    )
)

print()

print(
    "WHY:"
)

for reason in explanation.get(
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
    explanation.get(
        "ml_interpretation"
    )
)

print()

print(
    "LIMITATIONS:"
)

for limitation in explanation.get(
    "limitations",
    [],
):

    print(
        " •",
        limitation,
    )

print()
print("========================================")
print("       AI EXPLAINER TEST PASSED")
print("========================================")