from .news_search import search_current_news


print("\n========================================")
print("      CLARIFAI CURRENTS RAW TEST")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


results = search_current_news(
    claim,
    max_results=5,
)


print(
    f"\nResults returned: {len(results)}"
)


for index, article in enumerate(
    results,
    start=1,
):

    print("\n----------------------------------------")
    print(f"ARTICLE {index}")
    print("----------------------------------------")

    print(
        "Title:",
        article.get("title", "")
    )

    print(
        "Source:",
        article.get("source", "")
    )

    print(
        "URL:",
        article.get("url", "")
    )

    print(
        "Published:",
        article.get("published_at", "")
    )

    print(
        "Provider:",
        article.get("provider", "")
    )

    description = article.get(
        "description",
        ""
    )

    content = article.get(
        "content",
        ""
    )

    print(
        "\nDescription characters:",
        len(description)
    )

    print(
        "Content characters:",
        len(content)
    )

    print(
        "\nDescription preview:"
    )

    print(
        description[:500]
    )

    print(
        "\nContent preview:"
    )

    print(
        content[:500]
    )


print(
    "\n========================================"
)
print(
    "       RAW TEST COMPLETE"
)
print(
    "========================================"
)