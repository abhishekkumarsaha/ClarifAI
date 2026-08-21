import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.verification_service import verify_news_claim
from src.health import backend_health
from src.news_search import get_latest_news


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="ClarifAI API",
    version="1.0.0",
    description="AI-assisted news verification API",
)


# ============================================================
# CORS
# ============================================================

default_origins = [
    # Local Vite
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5175",
    "http://127.0.0.1:5175",

    # Production frontend
    "https://clarifai-frontend.vercel.app",
]

production_origins = os.getenv(
    "FRONTEND_URL",
    "https://clarifai-frontend.vercel.app",
).strip()

allowed_origins = default_origins.copy()

if production_origins:
    for origin in production_origins.split(","):
        origin = origin.strip()

        if origin and origin not in allowed_origins:
            allowed_origins.append(origin)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class AnalyzeRequest(BaseModel):

    claim: str = Field(
        ...,
        min_length=3,
        max_length=10000,
        description="News claim or article URL to verify.",
    )

    max_articles: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of evidence articles.",
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root() -> dict[str, Any]:

    return {
        "name": "ClarifAI",
        "service": "News Verification API",
        "status": "online",
        "version": "1.0.0",
    }


@app.get("/api")
def api_root() -> dict[str, Any]:

    return {
        "name": "ClarifAI",
        "service": "News Verification API",
        "status": "online",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health() -> dict[str, Any]:

    return backend_health()


@app.get("/api/health")
def api_health() -> dict[str, Any]:

    return backend_health()


# ============================================================
# LIVE NEWS
# ============================================================

@app.get("/api/news")
def news() -> dict[str, Any]:

    try:

        articles = get_latest_news(
            limit=6,
        )

        return {
            "success": True,
            "articles": articles,
            "count": len(articles),
        }

    except Exception as error:

        print(
            "Live news error:",
            repr(error),
        )

        return {
            "success": False,
            "articles": [],
            "count": 0,
            "error": (
                "Live news services are "
                "currently unavailable."
            ),
        }


# ============================================================
# ANALYZE
# ============================================================

@app.post("/api/analyze")
def analyze(
    request: AnalyzeRequest,
) -> dict[str, Any]:

    claim = request.claim.strip()

    if not claim:

        raise HTTPException(
            status_code=400,
            detail="Claim cannot be empty.",
        )

    try:

        result = verify_news_claim(
            claim,
            max_articles=request.max_articles,
        )

        if result is None:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Verification returned "
                    "no result."
                ),
            )

        return result

    except HTTPException:
        raise

    except Exception as error:

        print(
            "ClarifAI verification error:",
            repr(error),
        )

        error_text = str(error)

        if (
            "429" in error_text
            or "rate limit" in error_text.lower()
        ):

            raise HTTPException(
                status_code=429,
                detail=(
                    "External API rate limit "
                    "reached. Please try again later."
                ),
            )

        raise HTTPException(
            status_code=500,
            detail="ClarifAI verification failed.",
        )


# ============================================================
# VERIFY ALIAS
# ============================================================

@app.post("/api/verify")
def verify(
    request: AnalyzeRequest,
) -> dict[str, Any]:

    return analyze(request)


# ============================================================
# OPTIONS / CORS TEST
# ============================================================

@app.options("/{path:path}")
def cors_preflight(path: str):

    return {
        "status": "ok",
        "path": path,
    }


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )