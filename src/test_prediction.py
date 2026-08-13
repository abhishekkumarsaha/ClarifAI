from predict import predict_news


# =========================================================
# TEST NEWS ARTICLE
# =========================================================

title = """
Government announces new measures to improve digital education
"""

article = """
The government announced a new initiative today
to improve digital education across schools and colleges.
The program will provide students with access to
new learning resources and technology.
"""


# =========================================================
# MAKE PREDICTION
# =========================================================

result = predict_news(
    title,
    article
)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\n===================================")
print("          CLARIFAI RESULT")
print("===================================")

if result["success"]:

    print(
        "Prediction:",
        result["prediction"]
    )

    print(
        "Confidence:",
        f'{result["confidence"]}%'
    )

    print(
        "Confidence Level:",
        result["confidence_level"]
    )

else:

    print(
        "Error:",
        result["error"]
    )

print("===================================")