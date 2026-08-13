from clarifai_engine import analyze_news


title = """
Government announces new education program
"""

article = """
The government announced a new education initiative
to improve digital learning facilities across the country.
Students will receive access to new educational resources.
"""


result = analyze_news(
    title,
    article
)


print("\n======================================")
print("             CLARIFAI")
print("======================================")

if result["success"]:

    print(
        "Prediction:",
        result["prediction"]
    )

    print(
        "Model Confidence:",
        f'{result["confidence"]}%'
    )

    print(
        "Confidence Level:",
        result["confidence_level"]
    )

    print("\nKey Model Signals:")

    for signal in result["signals"]:

        print(
            f'  • {signal["feature"]}'
        )

else:

    print(
        "Error:",
        result["error"]
    )

print("======================================")