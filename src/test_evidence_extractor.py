from .evidence_extractor import extract_article


print("\n========================================")
print("     CLARIFAI EVIDENCE EXTRACTOR")
print("========================================")


url = input(
    "\nPaste an article URL: "
).strip()


result = extract_article(
    url
)


if result["success"]:

    content = result["content"]

    print(
        "\nEXTRACTION SUCCESS"
    )

    print(
        "Characters:",
        len(content),
    )

    print(
        "\nFirst 1000 characters:\n"
    )

    print(
        content[:1000]
    )

else:

    print(
        "\nEXTRACTION FAILED"
    )

    print(
        "Reason:",
        result["error"],
    )