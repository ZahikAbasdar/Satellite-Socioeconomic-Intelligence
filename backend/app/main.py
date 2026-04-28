"""
Satellite-Driven Socioeconomic Intelligence
FastAPI Backend — Main Application
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import logging
import time

from src.model import get_predictor
from src.pipeline import extract_features_from_image, extract_features_from_region
from src.utils import (
    get_trend_data,
    get_feature_breakdown,
    generate_heatmap_data,
    get_comparative_data,
    generate_ai_insight,
    GLOBAL_REGIONS,
)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Satellite Socioeconomic Intelligence API",
    description="AI-powered socioeconomic development prediction from satellite data.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Warm up model on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Warming up ML model...")
    get_predictor()
    logger.info("Model ready.")


# ── Request / Response Models ─────────────────────────────────────────────────

class RegionRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    region_name: Optional[str] = "Unknown Region"


class PredictionResponse(BaseModel):
    success: bool
    score: float
    percentage: float
    category: str
    category_color: str
    category_icon: str
    confidence: float
    region_name: str
    trend: dict
    features: list
    heatmap_data: list
    comparative: list
    insight: str
    processing_time_ms: float


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_ready": True,
        "version": "2.0.0",
        "endpoints": ["/health", "/predict", "/analyze-region", "/regions"],
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    region_name: str = Query(default="Uploaded Image"),
):
    """
    Predict socioeconomic development score from an uploaded satellite image.
    """
    t0 = time.perf_counter()

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image_bytes = await file.read()
    if len(image_bytes) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 20 MB).")

    try:
        features_arr = extract_features_from_image(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Image processing error: {e}")

    predictor = get_predictor()
    result = predictor.predict(features_arr)

    score = result["score"]
    trend = get_trend_data(score)
    features_breakdown = get_feature_breakdown(result["feature_importance"])

    # Use center-of-image lat/lon as (0,0) placeholder for heatmap
    heatmap = generate_heatmap_data(0.0, 0.0, radius=1.5)
    comparative = get_comparative_data(score, region_name)
    insight = generate_ai_insight(score, result["category"], result["feature_importance"], region_name)

    elapsed = (time.perf_counter() - t0) * 1000

    return PredictionResponse(
        success=True,
        score=score,
        percentage=result["percentage"],
        category=result["category"],
        category_color=result["category_color"],
        category_icon=result["category_icon"],
        confidence=result["confidence"],
        region_name=region_name,
        trend=trend,
        features=features_breakdown,
        heatmap_data=heatmap,
        comparative=comparative,
        insight=insight,
        processing_time_ms=round(elapsed, 2),
    )


@app.post("/analyze-region", response_model=PredictionResponse)
async def analyze_region(body: RegionRequest):
    """
    Analyze socioeconomic development for a geographic coordinate.
    """
    t0 = time.perf_counter()

    features_arr = extract_features_from_region(body.lat, body.lon, body.region_name)
    predictor = get_predictor()
    result = predictor.predict(features_arr)

    score = result["score"]
    trend = get_trend_data(score)
    features_breakdown = get_feature_breakdown(result["feature_importance"])
    heatmap = generate_heatmap_data(body.lat, body.lon)
    comparative = get_comparative_data(score, body.region_name)
    insight = generate_ai_insight(score, result["category"], result["feature_importance"], body.region_name)

    elapsed = (time.perf_counter() - t0) * 1000

    return PredictionResponse(
        success=True,
        score=score,
        percentage=result["percentage"],
        category=result["category"],
        category_color=result["category_color"],
        category_icon=result["category_icon"],
        confidence=result["confidence"],
        region_name=body.region_name,
        trend=trend,
        features=features_breakdown,
        heatmap_data=heatmap,
        comparative=comparative,
        insight=insight,
        processing_time_ms=round(elapsed, 2),
    )


@app.get("/regions")
async def list_regions():
    """Return list of predefined global regions for quick analysis."""
    return {"regions": GLOBAL_REGIONS}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
