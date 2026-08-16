from .news_search import search_currents


print("\n========================================")
print("       CLARIFAI CURRENTS TEST")
print("========================================")


try:

    results = search_currents(
        "India latest news",
        max_results=5,
    )

    print(
        f"\nResults received: {len(results)}"
    )

    for index, article in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n{index}. {article['title']}"
        )

        print(
            "Provider:",
            article["provider"],
        )

        print(
            "Source:",
            article["source"],
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
        "CURRENTS TEST PASSED"
    )

except Exception as error:

    print(
        "\nCURRENTS TEST FAILED:"
    )

    print(error)