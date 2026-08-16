from .news_search import search_current_news
from .evidence_pipeline import collect_evidence
from .ml_evidence_analyzer import analyze_evidence
from .evidence_analyzer import analyze_evidence as aggregate


print()
print("=" * 40)
print("       CLARIFAI DOMAIN TEST")
print("=" * 40)


claim = (
    "Reed Hastings on life after Netflix "
    "and the coming creative destruction"
)


print("\nSearching...")

articles = search_current_news(
    claim,
    max_results=5,
)


print(
    "Search results:",
    len(articles),
)


evidence = collect_evidence(
    articles,
    max_articles=5,
)


print(
    "Extracted:",
    len(evidence),
)


evidence = analyze_evidence(
    evidence
)


print()
print("ARTICLE URL DATA")
print("-" * 40)


for index, item in enumerate(
    evidence,
    start=1,
):

    print(
        f"\n{index}. "
        f"{item.get('title', '')}"
    )

    print(
        "source:",
        repr(item.get("source")),
    )

    print(
        "url:",
        repr(item.get("url")),
    )

    print(
        "final_url:",
        repr(item.get("final_url")),
    )

    print(
        "article_url:",
        repr(item.get("article_url")),
    )

    print(
        "source_url:",
        repr(item.get("source_url")),
    )


print()
print("=" * 40)
print("AGGREGATED RESULT")
print("=" * 40)


summary = aggregate(
    evidence
)


print(
    "Independent sources:",
    summary.get(
        "independent_domains"
    ),
)


print(
    "Domains:",
    summary.get(
        "domains"
    ),
)