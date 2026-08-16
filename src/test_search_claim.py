from .news_search import search_current_news


print("\n========================================")
print("       CLARIFAI CLAIM SEARCH TEST")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


if not claim:
    print("No claim entered.")
    raise SystemExit


try:

    results = search_current_news(
        claim,
        max_results=10,
    )

    print(
        f"\nResults found: {len(results)}"
    )

    for index, article in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n{index}. {article['title']}"
        )

        print(
            "Source:",
            article["source"],
        )

        print(
            "Provider:",
            article["provider"],
        )

        print(
            "Published:",
            article["published_at"],
        )

        print(
            "URL:",
            article["url"],
        )


    print(
        "\n========================================"
    )

    print(
        "CLAIM SEARCH TEST PASSED"
    )

except Exception as error:

    print(
        "\nCLAIM SEARCH FAILED:"
    )

    print(error)