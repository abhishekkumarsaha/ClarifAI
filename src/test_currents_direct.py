from .news_search import search_current_news


print()
print("========================================")
print("       CLARIFAI DIRECT CURRENTS TEST")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


if not claim:
    print("\nNo claim entered.")
    raise SystemExit


try:

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

        print()
        print("----------------------------------------")
        print(
            f"ARTICLE {index}"
        )
        print("----------------------------------------")

        print(
            "Title:",
            article.get(
                "title",
                "",
            ),
        )

        print(
            "Source:",
            article.get(
                "source",
                "",
            ),
        )

        print(
            "Provider:",
            article.get(
                "provider",
                "",
            ),
        )

        print(
            "Published:",
            article.get(
                "published_at",
                "",
            ),
        )

        print("\nURL:")

        print(
            article.get(
                "url",
                "",
            )
        )

        url = article.get(
            "url",
            "",
        )

        print(
            "\nGoogle News URL:",
            "news.google.com" in url,
        )

        print("\nDescription:")

        print(
            article.get(
                "description",
                "",
            )[:300]
        )

    print()
    print("========================================")
    print("       DIRECT CURRENTS TEST PASSED")
    print("========================================")

except Exception as error:

    print()
    print("========================================")
    print("       DIRECT CURRENTS TEST FAILED")
    print("========================================")

    print(
        type(error).__name__,
        ":",
        error,
    )