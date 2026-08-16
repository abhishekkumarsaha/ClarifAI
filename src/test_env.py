import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL")

print("\n================================")
print("       CLARIFAI ENV TEST")
print("================================")

if api_key:
    print("API Key: FOUND")
    print("API Key preview:", api_key[:8] + "..." + api_key[-4:])
else:
    print("API Key: NOT FOUND")

if model:
    print("Model: FOUND")
    print("Model:", model)
else:
    print("Model: NOT FOUND")