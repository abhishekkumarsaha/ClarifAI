"""
ClarifAI Evidence Relevance Layer

Determines whether retrieved article content
actually relates to the user's claim.

The AI does NOT decide the final truth value here.
It only classifies evidence relevance.
"""


import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

load_dotenv(
    PROJECT_ROOT / ".env"
)


OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)


def _parse_json(text):

    text = (
        text
        .strip()
    )

    if text.startswith(
        "```"
    ):

        text = (
            text
            .replace(
                "```json",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )

    return json.loads(
        text
    )


def classify_evidence(
    claim,
    article,
):
    """
    Classify one article as:

    SUPPORTS
    CONTRADICTS
    RELATED
    IRRELEVANT
    """

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    model = os.getenv(
        "OPENROUTER_MODEL"
    )

    if not api_key or not model:

        return {
            "success": False,
            "classification": "UNKNOWN",
            "reason": "OpenRouter credentials missing.",
        }

    title = (
        article.get("title")
        or article.get(
            "article_title",
            "",
        )
    )

    content = (
        article.get("content")
        or ""
    )

    prompt = f"""
You are ClarifAI's evidence relevance analyzer.

User claim:

{claim}

Article title:

{title}

Article content:

{content[:10000]}

Classify the article in relation to the claim.

Allowed classifications:

SUPPORTS
CONTRADICTS
RELATED
IRRELEVANT

Definitions:

SUPPORTS:
The article contains evidence that directly supports
the factual claim.

CONTRADICTS:
The article contains evidence that directly conflicts
with the factual claim.

RELATED:
The article discusses the same person, organization,
event, or topic but does not establish whether the claim
is true or false.

IRRELEVANT:
The article does not meaningfully address the claim.

IMPORTANT:

- Do not infer facts that are not in the article.
- Do not treat mentioning the same person as evidence.
- Do not treat the ML prediction as evidence.
- Do not decide the final verdict.
- Be conservative.

Return ONLY valid JSON:

{{
  "classification": "SUPPORTS",
  "relevance_score": 0.95,
  "reason": "Short explanation."
}}
"""

    try:

        response = requests.post(
            OPENROUTER_URL,

            headers={
                "Authorization":
                    f"Bearer {api_key}",

                "Content-Type":
                    "application/json",

                "HTTP-Referer":
                    "http://localhost:8501",

                "X-Title":
                    "ClarifAI",
            },

            json={
                "model": model,

                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You classify evidence "
                            "conservatively."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],

                "temperature": 0,

                "max_tokens": 200,
            },

            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        content = (
            data["choices"][0]
            ["message"]
            ["content"]
        )

        result = _parse_json(
            content
        )

        classification = str(
            result.get(
                "classification",
                "IRRELEVANT",
            )
        ).upper()

        if classification not in {
            "SUPPORTS",
            "CONTRADICTS",
            "RELATED",
            "IRRELEVANT",
        }:

            classification = (
                "IRRELEVANT"
            )

        return {
            "success": True,

            "classification":
                classification,

            "relevance_score":
                result.get(
                    "relevance_score",
                    0,
                ),

            "reason":
                result.get(
                    "reason",
                    "",
                ),
        }

    except Exception as error:

        return {
            "success": False,

            "classification":
                "UNKNOWN",

            "relevance_score":
                0,

            "reason":
                str(error),
        }