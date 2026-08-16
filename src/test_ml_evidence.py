from .news_search import search_current_news
from .evidence_pipeline import collect_evidence
from .ml_evidence_analyzer import analyze_evidence

print("\n========================================")
print("      CLARIFAI ML EVIDENCE TEST")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


articles = search_current_news(
    claim,
    max_results=10,
)


evidence = collect_evidence(
    articles,
    max_articles=5,
)


results = analyze_evidence(
    evidence
)


for index, item in enumerate(
    results,
    start=1,
):

    print(
        f"\n{index}. {item['title']}"
    )

    ml = item.get(
        "ml_analysis"
    )

    if ml:

        print(
            "ML Result:",
            ml,
        )

    else:

        print(
            "ML Result: unavailable"
        )


print(
    "\n========================================"
)

print(
    "ML + EVIDENCE TEST COMPLETE"
)