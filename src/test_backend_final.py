"""
ClarifAI Final Backend Integration Test
"""

from .health import backend_health
from .news_search import build_search_queries
from .clarifai_api import analyze_news_claim


print()
print("========================================")
print("       CLARIFAI BACKEND FINAL TEST")
print("========================================")


# ============================================================
# 1. HEALTH CHECK
# ============================================================

print()
print("[1/4] Backend health")

health = backend_health()

print(
    "Status:",
    health["status"],
)

for key, value in health["environment"].items():

    print(
        f"{key}:",
        "OK" if value else "MISSING",
    )


if health["status"] != "healthy":

    print()
    print(
        "WARNING: Backend environment is incomplete."
    )


# ============================================================
# 2. QUERY GENERATION
# ============================================================

print()
print("[2/4] Query generation")


test_claim = (
    "Netflix co-founder Reed Hastings "
    "on why he stopped calling CEOs "
    "Ted Sarandos and Greg Peters"
)


queries = build_search_queries(
    test_claim
)


print(
    "Generated:",
    len(queries),
    "queries",
)


for query in queries:

    print(
        " •",
        query,
    )


if not queries:

    raise RuntimeError(
        "Query generation failed."
    )


# ============================================================
# 3. COMPLETE LIVE VERIFICATION
# ============================================================

print()
print("[3/4] Live verification")

print(
    "Running ClarifAI..."
)


result = analyze_news_claim(
    test_claim,
    max_articles=5,
)


if not result.get(
    "success"
):

    raise RuntimeError(
        result.get(
            "error",
            "Verification failed.",
        )
    )


print()
print(
    "Verdict:",
    result.get(
        "verdict",
        "UNKNOWN",
    ),
)


print(
    "Confidence:",
    result.get(
        "confidence",
        0,
    ),
)


print(
    "Confidence Level:",
    result.get(
        "confidence_level",
        "N/A",
    ),
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


# ============================================================
# 4. RESPONSE STRUCTURE
# ============================================================

print()
print("[4/4] Response structure")


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


missing_fields = [

    field

    for field in required_fields

    if field not in result
]


if missing_fields:

    print(
        "Missing fields:"
    )

    for field in missing_fields:

        print(
            " •",
            field,
        )

    raise RuntimeError(
        "Backend response structure is incomplete."
    )


print(
    "All required fields present."
)


print()
print("========================================")
print("     CLARIFAI BACKEND FINAL TEST PASSED")
print("========================================")