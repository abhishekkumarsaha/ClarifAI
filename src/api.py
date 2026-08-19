"""
ClarifAI FastAPI Backend
========================

HTTP bridge between the React/Vite frontend and the
existing ClarifAI Python verification system.

Routes:
    GET  /
    GET  /health
    GET  /api/health
    GET  /api/news
    POST /api/analyze
    POST /api/verify
"""

from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .health import backend_health
from .live_news import get_live_news
from .verification_service import verify_news_claim


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="ClarifAI API",
    description=(
        "ML-powered news verification and live news "
        "intelligence backend."
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class AnalyzeRequest(BaseModel):
    claim: str = Field(
        ...,
        min_length=3,
        max_length=10000,
        description="News claim or article title to verify.",
    )

    url: str | None = Field(
        default=None,
        max_length=5000,
        description="Optional direct article URL.",
    )

    max_articles: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum evidence articles.",
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


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health() -> dict[str, Any]:

    return backend_health()


# Frontend compatibility route.
# The React frontend historically calls /api/health.
@app.get("/api/health")
def api_health() -> dict[str, Any]:

    return backend_health()


# ============================================================
# LIVE NEWS
# ============================================================

@app.get("/api/news")
def latest_news(
    query: str = Query(
        default="",
        max_length=500,
    ),
    timespan: str = Query(
        default="1h",
        max_length=20,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=20,
    ),
) -> dict[str, Any]:

    try:

        articles = get_live_news(
            query=query,
            timespan=timespan,
            max_records=limit,
        )

        return {
            "success": True,
            "articles": articles,
            "count": len(articles),
            "query": query,
            "timespan": timespan,
        }

    except Exception as error:

        print(
            "Live news error:",
            repr(error),
        )

        # The news feed should not crash the whole UI.
        return {
            "success": False,
            "articles": [],
            "count": 0,
            "query": query,
            "timespan": timespan,
            "error": (
                "Live news services are "
                "currently unavailable."
            ),
        }


# ============================================================
# VERIFY / ANALYZE
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
                detail="Verification returned no result.",
            )

        return result

    except Exception as error:
        print(
            "ClarifAI verification error:",
            repr(error),
        )

        raise HTTPException(
            status_code=500,
            detail=f"ClarifAI verification failed: {error}",
        )


# ============================================================
# VERIFY ALIAS
# ============================================================

@app.post("/api/verify")
def verify(
    request: AnalyzeRequest,
) -> dict[str, Any]:

    return analyze(request)