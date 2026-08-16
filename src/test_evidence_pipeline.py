from .news_search import search_current_news
from .evidence_pipeline import collect_evidence


print("\n========================================")
print("       CLARIFAI EVIDENCE TEST")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


articles = search_current_news(
    claim,
    max_results=10,
)


print(
    f"\nSearch results: {len(articles)}"
)


evidence = collect_evidence(
    articles,
    max_articles=5,
)


successful = 0


for index, item in enumerate(
    evidence,
    start=1,
):

    print(
        f"\n{index}. {item['title']}"
    )

    print(
        "Source:",
        item["source"],
    )

    print(
        "Extraction:",
        item["extraction_success"],
    )

    print(
        "Characters:",
        len(
            item["content"]
        ),
    )

    if item["extraction_success"]:
        successful += 1


print(
    "\n========================================"
)

print(
    "Articles analyzed:",
    len(evidence),
)

print(
    "Successful extractions:",
    successful,
)

print(
    "EVIDENCE PIPELINE TEST COMPLETE"
)