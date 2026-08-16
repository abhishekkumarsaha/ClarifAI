from live_news import get_live_news


print("\n========================================")
print("       CLARIFAI LIVE NEWS TEST")
print("========================================")


try:

    articles = get_live_news(
        timespan="1h",
        max_records=10,
    )

    print(
        f"\nArticles received: {len(articles)}"
    )

    for index, article in enumerate(
        articles,
        start=1,
    ):

        print(
            f"\n{index}. {article['title']}"
        )

        print(
            "   Source:",
            article["domain"],
        )

        print(
            "   URL:",
            article["url"],
        )

        print(
            "   Seen:",
            article["seendate"],
        )

    print(
        "\n========================================"
    )
    print("       LIVE NEWS TEST PASSED")
    print("========================================")

except Exception as error:

    print(
        "\nLIVE NEWS TEST FAILED:"
    )

    print(error)