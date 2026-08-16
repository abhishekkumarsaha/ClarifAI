from article_analyzer import analyze_pasted_article


title = "Government announces new education initiative"

article = """
The government announced a new education initiative today.
The program aims to improve digital learning facilities and
provide students with access to modern educational resources.
Officials said the initiative will focus on improving access
to technology and supporting educational institutions.
The program will provide additional resources to schools and
students across the country.
"""


try:
    result = analyze_pasted_article(
        title,
        article,
    )

    print("\n======================================")
    print("       CLARIFAI UNIFIED TEST")
    print("======================================")

    print("Prediction:", result.get("prediction"))
    print("Confidence:", result.get("confidence"))
    print("Confidence Level:", result.get("confidence_level"))
    print("Word Count:", result.get("word_count"))
    print("Input Method:", result.get("input_method"))

    print("\nSignals:")

    for signal in result.get("signals", []):
        print(" •", signal)

    print("\n======================================")
    print("TEST SUCCESSFUL")
    print("======================================")

except Exception as error:

    print("\n======================================")
    print("TEST FAILED")
    print("======================================")
    print(error)