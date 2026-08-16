from src.article_analyzer import analyze_pasted_article


def main():

    title = "Government announces new education initiative"

    article = """
    The government announced a new education initiative today.
    The program aims to improve digital learning facilities and
    provide students with access to modern educational resources.
    Officials said the initiative will focus on improving access
    to technology and supporting educational institutions.
    Students will receive additional digital learning resources
    as part of the program.
    """

    try:

        result = analyze_pasted_article(
            title,
            article,
        )

        print("\n========================================")
        print("        CLARIFAI BACKEND TEST")
        print("========================================")

        print("Prediction:", result.get("prediction"))
        print("Confidence:", result.get("confidence"))
        print("Confidence Level:", result.get("confidence_level"))
        print("Input Method:", result.get("input_method"))
        print("Word Count:", result.get("word_count"))

        print("\nSignals:")

        for signal in result.get("signals", []):
            print(" •", signal)

        print("\nAI Explanation:")

        explanation = result.get("ai_explanation")

        if explanation:
            print(explanation)
        else:
            print("Unavailable")

        print("\n========================================")
        print("        BACKEND TEST PASSED")
        print("========================================")

    except Exception as error:

        print("\n========================================")
        print("        BACKEND TEST FAILED")
        print("========================================")

        print(error)


if __name__ == "__main__":
    main()