from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.verification_service import verify_news_claim
from src.health import backend_health


app = FastAPI(
    title="ClarifAI API",
    version="1.0.0",
    description="AI-assisted news verification API",
)


class AnalyzeRequest(BaseModel):
    claim: str = Field(
        ...,
        min_length=3,
        max_length=5000,
    )

    max_articles: int = Field(
        default=5,
        ge=1,
        le=10,
    )


@app.get("/api")
def root():
    return {
        "name": "ClarifAI",
        "status": "online",
        "version": "1.0.0",
    }


@app.get("/api/health")
def health():
    return backend_health()


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):

    try:

        result = verify_news_claim(
            request.claim,
            max_articles=request.max_articles,
        )

        if not result.get("success", False):

            raise HTTPException(
                status_code=500,
                detail=result.get(
                    "error",
                    "Analysis failed.",
                ),
            )

        return result

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )