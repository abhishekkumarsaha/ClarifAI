from predict import clean_text
from explain import explain_prediction


title = "Government announces new education program"

article = """
The government announced a new education initiative
to improve digital learning facilities across the country.
Students will receive access to new educational resources.
"""


combined_text = f"{title} {article}"

cleaned_text = clean_text(combined_text)

features = explain_prediction(
    cleaned_text,
    top_n=10
)


print("\n===================================")
print("       CLARIFAI EXPLANATION")
print("===================================")

for item in features:

    print(
        f'{item["feature"]} '
        f'→ contribution: {item["contribution"]}'
    )

print("===================================")