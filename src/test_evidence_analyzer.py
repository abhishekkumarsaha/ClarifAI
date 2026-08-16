from .news_search import search_current_news
from .evidence_pipeline import collect_evidence
from .ml_evidence_analyzer import analyze_evidence


print("\n========================================")
print("     CLARIFAI EVIDENCE ANALYZER TEST")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


if not claim:
    print("No claim entered.")
    raise SystemExit(1)


# ------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------

articles = search_current_news(
    claim,
    max_results=10,
)


print(
    f"\nSearch results: {len(articles)}"
)


# ------------------------------------------------------------
# EXTRACTION
# ------------------------------------------------------------

evidence = collect_evidence(
    articles,
    max_articles=5,
)


print(
    f"Evidence collected: {len(evidence)}"
)


# ------------------------------------------------------------
# ML ANALYSIS
# ------------------------------------------------------------

analyzed = analyze_evidence(
    evidence
)


# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------

print(
    "\n========================================"
)


successful = [
    item
    for item in analyzed
    if item.get(
        "extraction_success",
        False,
    )
]


print(
    "Articles found:",
    len(analyzed),
)


print(
    "Articles extracted:",
    len(successful),
)


# ------------------------------------------------------------
# UNIQUE SOURCES
# ------------------------------------------------------------

from urllib.parse import urlparse


domains = set()


for item in successful:

    url = (
        item.get("final_url")
        or item.get("url")
        or ""
    )

    if url:

        try:

            domain = (
                urlparse(url)
                .netloc
                .lower()
                .replace(
                    "www.",
                    "",
                )
            )

            if domain:
                domains.add(domain)

        except Exception:
            pass


print(
    "Independent sources:",
    len(domains),
)


print(
    "\nDomains:"
)


for domain in sorted(domains):

    print(
        " •",
        domain,
    )


# ------------------------------------------------------------
# ML SUMMARY
# ------------------------------------------------------------

real_count = 0
fake_count = 0


for item in analyzed:

    result = item.get(
        "ml_analysis"
    )

    if not isinstance(
        result,
        dict,
    ):
        continue

    prediction = str(
        result.get(
            "prediction",
            "",
        )
    ).upper()

    if prediction == "REAL":

        real_count += 1

    elif prediction == "FAKE":

        fake_count += 1


print(
    "\nML REAL:",
    real_count,
)


print(
    "ML FAKE:",
    fake_count,
)


# ------------------------------------------------------------
# ARTICLE DETAILS
# ------------------------------------------------------------

print(
    "\nArticle details:"
)


for index, item in enumerate(
    analyzed,
    start=1,
):

    title = (
        item.get("article_title")
        or item.get("title")
        or "Unknown title"
    )

    source = (
        item.get("source")
        or "Unknown source"
    )

    extracted = item.get(
        "extraction_success",
        False,
    )

    print(
        f"\n{index}. {title}"
    )

    print(
        "Source:",
        source,
    )

    print(
        "Extraction:",
        extracted,
    )


print(
    "\n========================================"
)

print(
    "EVIDENCE ANALYZER TEST COMPLETE"
)

print(
    "========================================"
)