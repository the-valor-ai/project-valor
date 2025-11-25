"""
Valor AI - Fruit and Vegetable Quality Analysis API

A FastAPI application for analyzing produce quality using AI vision models.

Features:
- Multi-stage AI analysis (Classification, Ripeness, Disease Detection)
- Multi-language support (English, Yoruba, Igbo, Hausa)
- Online (OpenAI) and offline modes
- Image upload and camera capture support
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
import uvicorn
from typing import Optional

from app.config import settings
from app.ai_service import ai_service
from app.schemas import FullAnalysisResponse, HealthCheckResponse

# Initialize FastAPI app
app = FastAPI(
    title="Valor AI - Produce Quality Analysis API",
    description="""
    Valor AI: Agricultural Quality Assessment System

    This API provides AI-powered analysis of fruits and vegetables for:
    - Classification and identification
    - Ripeness assessment
    - Disease and defect detection

    Features:
    - Multi-language support (English, Yoruba, Igbo, Hausa)
    - Online analysis via OpenAI Vision API and offline support 

    Target Accuracy: 85%+ across all models
    Response Time: Under 5 seconds
    """,
    version="1.5.0",
    contact={
        "name": "Valor AI Team",
        "email": "thevalorai@gmail.com"
    },
    # license_info={
    #     "name": "MIT License"
    # }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get(
    "/",
    response_model=dict,
    summary="Welcome Endpoint"
)
async def root():
    """API root endpoint with status information"""
    return {
        "message": "Valor AI - Produce Quality Analysis API",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
        "mode": "offline" if settings.use_offline_mode else "online"
    }


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check"
)
async def health_check():
    """Check API health and configuration status"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "mode": "offline" if settings.use_offline_mode else "online",
        "openai_configured": bool(settings.openai_api_key),
        "supported_languages": ["en", "yo", "ig", "ha"]
    }


@app.post(
    "/analyze/full",
    response_model=FullAnalysisResponse,
    summary="Full Produce Analysis",
    description="Complete analysis: Classification, Ripeness, Disease Detection"
)
async def analyze_full(
    file: UploadFile = File(..., description="Produce image (JPEG/PNG)"),
    language: Optional[str] = Form("en", description="Response language: en, yo, ig, ha")
):
    """
    Complete produce analysis pipeline.

    Performs three-stage analysis:
    1. Fruit/vegetable classification
    2. Ripeness assessment
    3. Disease detection

    Parameters:
    - file: Image file (JPEG/PNG)
    - language: Response language (en/yo/ig/ha)

    Returns complete analysis with recommendations.
    """
    try:
        if language not in ["en", "yo", "ig", "ha"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {language}. Use: en, yo, ig, ha"
            )

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        try:
            image = Image.open(BytesIO(contents)).convert("RGB")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image format. Use JPEG or PNG. Error: {str(e)}"
            )

        result = await ai_service.full_analysis(image, language)
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post(
    "/analyze/classify",
    summary="Classification Only",
    description="Identify produce type"
)
async def classify_fruit(
    file: UploadFile = File(..., description="Produce image"),
    language: Optional[str] = Form("en")
):
    """
    Identify produce type only.

    Fast endpoint for classification without ripeness or disease analysis.
    """
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")

        if settings.use_offline_mode:
            result = ai_service.analyze_offline(image, "fruit_classification")
        else:
            result = await ai_service.analyze_with_openai(
                image, "fruit_classification", language
            )

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/analyze/ripeness",
    summary="Ripeness Detection Only",
    description="Analyze ripeness stage"
)
async def analyze_ripeness(
    file: UploadFile = File(..., description="Produce image"),
    language: Optional[str] = Form("en")
):
    """
    Analyze ripeness stage only.

    Classifies produce as:
    - underripe
    - ripe
    - overripe
    - spoiled
    """
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")

        if settings.use_offline_mode:
            result = ai_service.analyze_offline(image, "ripeness")
        else:
            result = await ai_service.analyze_with_openai(
                image, "ripeness", language
            )

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/analyze/disease",
    summary="Disease Detection Only",
    description="Check for diseases and defects"
)
async def analyze_disease(
    file: UploadFile = File(..., description="Produce image"),
    language: Optional[str] = Form("en")
):
    """
    Detect diseases and defects.

    Identifies common issues:
    - Anthracnose
    - Powdery mildew
    - Bacterial spots
    - Fungal infections
    - Physical damage
    """
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")

        if settings.use_offline_mode:
            result = ai_service.analyze_offline(image, "disease")
        else:
            result = await ai_service.analyze_with_openai(
                image, "disease", language
            )

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info"
    )
