"""
ClarifAI Google News URL Resolver Test
======================================
"""

from .news_search import (
    search_current_news,
)

from .evidence_extractor import (
    resolve_article_url,
    is_google_news_url,
)


print()
print("========================================")
print("       CLARIFAI URL RESOLVER TEST")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


if not claim:

    print(
        "\nNo claim entered."
    )

    raise SystemExit


try:

    results = search_current_news(
        claim,
        max_results=5,
    )

except Exception as error:

    print(
        "\nSEARCH FAILED:"
    )

    print(error)

    raise SystemExit


print(
    f"\nResults returned: {len(results)}"
)


resolved_count = 0


for index, article in enumerate(
    results,
    start=1,
):

    title = article.get(
        "title",
        "",
    )

    original_url = article.get(
        "url",
        "",
    )

    print()
    print("----------------------------------------")
    print(
        f"ARTICLE {index}"
    )
    print("----------------------------------------")

    print(
        "Title:",
        title,
    )

    print(
        "Source:",
        article.get(
            "source",
            "",
        ),
    )

    print(
        "\nOriginal URL:"
    )

    print(
        original_url
    )

    print(
        "\nGoogle News wrapper:",
        is_google_news_url(
            original_url
        ),
    )

    resolved_url = (
        resolve_article_url(
            original_url
        )
    )

    print(
        "\nResolved URL:"
    )

    print(
        resolved_url
    )

    is_resolved = (
        resolved_url
        and
        resolved_url != original_url
        and
        not is_google_news_url(
            resolved_url
        )
    )

    print(
        "\nPublisher URL resolved:",
        bool(is_resolved),
    )

    if is_resolved:

        resolved_count += 1


print()
print("========================================")
print("       RESOLUTION SUMMARY")
print("========================================")

print(
    "Total articles:",
    len(results),
)

print(
    "Publisher URLs resolved:",
    resolved_count,
)

if resolved_count > 0:

    print(
        "\nURL RESOLUTION WORKING"
    )

else:

    print(
        "\nGoogle News URLs could not be "
        "resolved automatically."
    )

print()
print("========================================")
print("       RESOLVER TEST COMPLETE")
print("========================================")