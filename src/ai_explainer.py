"""
ClarifAI AI Verification Engine

Uses OpenRouter to interpret:

1. Current news evidence
2. Publisher/source information
3. ClarifAI ML signals

The AI does NOT replace the ML model.

The AI does NOT treat ML prediction as factual proof.
"""

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

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


# ============================================================
# JSON PARSER
# ============================================================

def _parse_json(text):
    """
    Parse JSON from an AI response.

    Handles:

    normal JSON
    markdown JSON
    surrounding text
    """

    if not text:

        return None

    text = str(
        text
    ).strip()

    # --------------------------------------------------------
    # Direct parse
    # --------------------------------------------------------

    try:

        return json.loads(
            text
        )

    except json.JSONDecodeError:

        pass

    # --------------------------------------------------------
    # Remove markdown fences
    # --------------------------------------------------------

    if "```" in text:

        text = (
            text
            .replace(
                "```json",
                "",
            )
            .replace(
                "```JSON",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )

        try:

            return json.loads(
                text
            )

        except json.JSONDecodeError:

            pass

    # --------------------------------------------------------
    # Extract JSON object
    # --------------------------------------------------------

    start = text.find(
        "{"
    )

    end = text.rfind(
        "}"
    )

    if (
        start >= 0
        and end > start
    ):

        candidate = text[
            start:end + 1
        ]

        try:

            return json.loads(
                candidate
            )

        except json.JSONDecodeError:

            pass

    return None


# ============================================================
# CONFIDENCE
# ============================================================

def _normalize_confidence(
    value,
):
    """Normalize confidence to 0-100."""

    try:

        confidence = float(
            value
        )

    except (
        TypeError,
        ValueError,
    ):

        confidence = 0.0

    if 0 <= confidence <= 1:

        confidence *= 100

    return round(
        max(
            0,
            min(
                100,
                confidence,
            ),
        ),
        2,
    )


def _confidence_level(
    confidence,
):

    if confidence >= 90:
        return "Very High"

    if confidence >= 75:
        return "High"

    if confidence >= 55:
        return "Moderate"

    if confidence >= 35:
        return "Low"

    return "Very Low"


# ============================================================
# BUILD AI PROMPT
# ============================================================

def _build_prompt(
    claim,
    evidence,
    evidence_summary,
):
    """
    Build a compact evidence-grounded prompt.
    """

    articles = []

    for index, item in enumerate(
        evidence or [],
        start=1,
    ):

        if not isinstance(
            item,
            dict,
        ):

            continue

        ml = item.get(
            "ml_analysis"
        )

        articles.append(
            {
                "id":
                    index,

                "source":
                    item.get(
                        "source",
                        "Unknown",
                    ),

                "title":
                    item.get(
                        "title",
                        item.get(
                            "article_title",
                            "",
                        ),
                    ),

                "published_at":
                    item.get(
                        "published_at",
                        "",
                    ),

                "url":
                    item.get(
                        "url",
                        "",
                    ),

                "description":
                    item.get(
                        "description",
                        "",
                    ),

                "content":
                    (
                        item.get(
                            "content",
                            "",
                        ) or ""
                    )[:5000],

                "ml_prediction":
                    (
                        ml.get(
                            "prediction"
                        )
                        if isinstance(
                            ml,
                            dict,
                        )
                        else None
                    ),

                "ml_confidence":
                    (
                        ml.get(
                            "confidence"
                        )
                        if isinstance(
                            ml,
                            dict,
                        )
                        else None
                    ),

                "ml_signals":
                    (
                        ml.get(
                            "signals",
                            [],
                        )
                        if isinstance(
                            ml,
                            dict,
                        )
                        else []
                    ),
            }
        )

    evidence_json = json.dumps(
        articles,
        indent=2,
        ensure_ascii=False,
    )

    summary_json = json.dumps(
        evidence_summary or {},
        indent=2,
        ensure_ascii=False,
    )

    return f"""
You are ClarifAI's final news verification
and explanation engine.

USER CLAIM:
{claim}

CURRENT EVIDENCE:
{evidence_json}

EVIDENCE SUMMARY:
{summary_json}

Your job is to determine whether the CURRENT
EVIDENCE supports, contradicts, or fails to
establish the user's claim.

==================================================
IMPORTANT
==================================================

The ClarifAI ML classifier is NOT a fact checker.

Its REAL/FAKE prediction only represents
linguistic patterns learned from historical
training data.

NEVER use an ML prediction alone to establish
whether a claim is true or false.

Current evidence and source reporting are
more important.

Do not invent information.

Do not invent sources.

Do not invent quotations.

Do not assume that an article supports a claim
just because the headline contains similar words.

Check whether the article content actually
addresses the claim.

Consider:

- source independence
- article content
- publication time
- direct support
- direct contradiction
- unrelated evidence
- missing evidence

==================================================
ALLOWED VERDICTS
==================================================

LIKELY_TRUE
LIKELY_FALSE
UNVERIFIED

Use UNVERIFIED when evidence is insufficient,
unrelated, conflicting, or ambiguous.

==================================================
RETURN ONLY JSON
==================================================

Return exactly this JSON structure:

{{
  "verdict": "UNVERIFIED",
  "confidence": 0,
  "summary": "Short explanation.",
  "why": [
    "Reason 1",
    "Reason 2"
  ],
  "supporting_evidence": [
    {{
      "source": "source name",
      "finding": "What the source actually supports."
    }}
  ],
  "contradicting_evidence": [
    {{
      "source": "source name",
      "finding": "What the source actually contradicts."
    }}
  ],
  "ml_interpretation": "Explain the ML signals without treating them as factual evidence.",
  "source_assessment": "Assess source quality and independence.",
  "limitations": [
    "Limitation."
  ],
  "user_safety": "Appropriate caution for the user."
}}

Confidence must be a number from 0 to 100.

Return ONLY JSON.
"""


# ============================================================
# OPENROUTER REQUEST
# ============================================================

def _call_openrouter(
    prompt,
    api_key,
    model,
    strict=False,
):
    """
    Call OpenRouter and request a strict JSON response.
    """

    system_message = """
You are ClarifAI's evidence-grounded news verification engine.

Return ONLY one valid JSON object.

Rules:
- No markdown.
- No code fences.
- No commentary.
- No text before JSON.
- No text after JSON.
- All strings must use valid JSON escaping.
- Do not invent evidence.
- Use only the supplied evidence.
"""

    if strict:
        system_message += """
IMPORTANT:
The previous response was invalid JSON.

You MUST return syntactically valid JSON.
Double-check commas, quotes, brackets, and escaping
before responding.
"""

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.0,
        "max_tokens": 1800,

        # Important: request structured JSON when
        # the selected OpenRouter model supports it.
        "response_format": {
            "type": "json_object"
        },
    }

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "ClarifAI",
        },
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    choices = data.get("choices", [])

    if not choices:
        raise RuntimeError(
            "OpenRouter returned no choices."
        )

    message = choices[0].get("message", {})

    content = message.get("content", "")

    if isinstance(content, list):
        content = "".join(
            str(part.get("text", ""))
            if isinstance(part, dict)
            else str(part)
            for part in content
        )

    if not content:
        raise RuntimeError(
            "OpenRouter returned empty content."
        )

    return str(content).strip()


# ============================================================
# MAIN FUNCTION
# ============================================================

def generate_verification_explanation(
    claim,
    evidence,
    ml_results=None,
    evidence_summary=None,
):
    """
    Generate final evidence-grounded AI explanation.
    """

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    model = os.getenv(
        "OPENROUTER_MODEL",
        "openrouter/free",
    )

    if not api_key:

        return {
            "success": False,
            "error":
                "OPENROUTER_API_KEY is missing.",
        }

    if not model:

        return {
            "success": False,
            "error":
                "OPENROUTER_MODEL is missing.",
        }

    # --------------------------------------------------------
    # BUILD PROMPT
    # --------------------------------------------------------

    prompt = _build_prompt(
        claim=claim,
        evidence=evidence,
        evidence_summary=evidence_summary,
    )

    # --------------------------------------------------------
    # FIRST ATTEMPT
    # --------------------------------------------------------

    try:

        raw_response = _call_openrouter(

            prompt,

            api_key,

            model,

            strict=False,
        )

        parsed = _parse_json(
            raw_response
        )

    except Exception as error:

        return {
            "success": False,
            "error":
                str(error),
        }

    # --------------------------------------------------------
    # SECOND ATTEMPT
    # --------------------------------------------------------

    if parsed is None:

        try:

            raw_response = _call_openrouter(

                prompt,

                api_key,

                model,

                strict=True,
            )

            parsed = _parse_json(
                raw_response
            )

        except Exception as error:

            return {
                "success": False,
                "error":
                    (
                        "AI JSON retry failed: "
                        f"{error}"
                    ),
            }

    # --------------------------------------------------------
    # STILL INVALID
    # --------------------------------------------------------

    if parsed is None:

        return {
            "success": False,
            "error":
                "AI response was not valid JSON.",
            "raw":
                raw_response[:2000]
                if raw_response
                else "",
        }

    # ========================================================
    # NORMALIZE VERDICT
    # ========================================================

    verdict = str(
        parsed.get(
            "verdict",
            "UNVERIFIED",
        )
    ).upper().strip()

    if verdict not in {
        "LIKELY_TRUE",
        "LIKELY_FALSE",
        "UNVERIFIED",
    }:

        verdict = "UNVERIFIED"

    # ========================================================
    # NORMALIZE CONFIDENCE
    # ========================================================

    confidence = _normalize_confidence(
        parsed.get(
            "confidence",
            0,
        )
    )

    # ========================================================
    # NORMALIZE
    # ========================================================

    parsed["verdict"] = (
        verdict
    )

    parsed["confidence"] = (
        confidence
    )

    parsed["confidence_level"] = (
        _confidence_level(
            confidence
        )
    )

    parsed["summary"] = str(
        parsed.get(
            "summary",
            "",
        )
    )

    parsed["why"] = (
        parsed.get(
            "why",
            [],
        )
        if isinstance(
            parsed.get(
                "why",
                [],
            ),
            list,
        )
        else []
    )

    parsed[
        "supporting_evidence"
    ] = (
        parsed.get(
            "supporting_evidence",
            [],
        )
        if isinstance(
            parsed.get(
                "supporting_evidence",
                [],
            ),
            list,
        )
        else []
    )

    parsed[
        "contradicting_evidence"
    ] = (
        parsed.get(
            "contradicting_evidence",
            [],
        )
        if isinstance(
            parsed.get(
                "contradicting_evidence",
                [],
            ),
            list,
        )
        else []
    )

    parsed[
        "ml_interpretation"
    ] = str(
        parsed.get(
            "ml_interpretation",
            "",
        )
    )

    parsed[
        "source_assessment"
    ] = str(
        parsed.get(
            "source_assessment",
            "",
        )
    )

    parsed[
        "limitations"
    ] = (
        parsed.get(
            "limitations",
            [],
        )
        if isinstance(
            parsed.get(
                "limitations",
                [],
            ),
            list,
        )
        else []
    )

    parsed[
        "user_safety"
    ] = str(
        parsed.get(
            "user_safety",
            "",
        )
    )

    # ========================================================
    # NO EVIDENCE SAFETY
    # ========================================================

    if not evidence:

        parsed["verdict"] = (
            "UNVERIFIED"
        )

        parsed["confidence"] = (
            0.0
        )

        parsed[
            "confidence_level"
        ] = "Very Low"

        parsed[
            "summary"
        ] = (
            "ClarifAI could not find "
            "sufficient current evidence "
            "to evaluate this claim."
        )

    # ========================================================
    # RETURN
    # ========================================================

    return {
        "success":
            True,

        "explanation":
            parsed,
    }


# ============================================================
# COMPATIBILITY WRAPPER
# ============================================================

def generate_ai_explanation(
    claim,
    evidence,
    ml_results=None,
    evidence_summary=None,
):
    """
    Compatibility wrapper.
    """

    return generate_verification_explanation(

        claim=claim,

        evidence=evidence,

        ml_results=ml_results,

        evidence_summary=evidence_summary,
    )


# ============================================================
# LEGACY ML EXPLANATION
# ============================================================

def generate_explanation(
    title,
    article_text,
    prediction,
    confidence,
    signals,
):
    """
    Compatibility function for your earlier
    ML-only explanation feature.
    """

    result = (
        generate_verification_explanation(

            claim=title,

            evidence=[
                {
                    "title":
                        title,

                    "source":
                        "ClarifAI ML",

                    "content":
                        article_text,

                    "extraction_success":
                        True,
                }
            ],

            ml_results=[
                {
                    "ml_analysis":
                        {
                            "prediction":
                                prediction,

                            "confidence":
                                confidence,

                            "signals":
                                signals,
                        }
                }
            ],

            evidence_summary={
                "articles_found":
                    1,

                "articles_extracted":
                    1,

                "independent_domains":
                    1,
            },
        )
    )

    if not result.get(
        "success",
        False,
    ):

        return None

    explanation = result.get(
        "explanation",
        {},
    )

    return explanation.get(
        "summary"
    )