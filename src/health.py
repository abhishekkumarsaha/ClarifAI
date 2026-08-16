"""
ClarifAI Backend Health Check
"""

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


def check_environment():

    return {
        "currents_api": bool(
            os.getenv("CURRENTS_API_KEY")
        ),

        "openrouter_api": bool(
            os.getenv("OPENROUTER_API_KEY")
        ),

        "openrouter_model": bool(
            os.getenv("OPENROUTER_MODEL")
        ),
    }


def backend_health():

    environment = check_environment()

    return {
        "status": (
            "healthy"
            if all(environment.values())
            else "degraded"
        ),

        "environment": environment,
    }
