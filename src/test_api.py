import requests


URL = "http://127.0.0.1:8000/api/analyze"


claim = input(
    "Enter a news claim: "
).strip()


response = requests.post(
    URL,
    json={
        "claim": claim,
        "max_articles": 5,
    },
    timeout=180,
)


print("\nStatus:", response.status_code)

print("\nResponse:")

print(
    response.json()
)