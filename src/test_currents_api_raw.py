"""
ClarifAI - Raw Currents API Diagnostic
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(
    PROJECT_ROOT / ".env"
)


API_KEY = (
    os.getenv("CURRENTS_API_KEY")
    or os.getenv("CURRENT_API_KEY")
)


URL = "https://api.currentsapi.services/v1/search"


print()
print("========================================")
print("       CURRENTS RAW API TEST")
print("========================================")


if not API_KEY:

    print("\nERROR: CURRENTS_API_KEY not found.")
    raise SystemExit


claim = input(
    "\nEnter search query: "
).strip()


headers = {
    "Authorization": API_KEY,
}


params = {
    "keywords": claim,
    "language": "en",
    "page_size": 10,
}


print("\nRequesting Currents...")


try:

    response = requests.get(
        URL,
        headers=headers,
        params=params,
        timeout=20,
    )

    print(
        "\nHTTP Status:",
        response.status_code,
    )

    print(
        "Request URL:",
        response.url,
    )

    print(
        "\nRaw response:"
    )

    print(
        response.text[:5000]
    )

except Exception as error:

    print(
        "\nREQUEST FAILED:"
    )

    print(error)

    raise SystemExit


print()
print("========================================")
print("       RAW TEST COMPLETE")
print("========================================")