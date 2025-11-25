"""
Pydantic schemas for API request/response validation
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Request schema for analysis"""
    language: Literal["en", "yo", "ig", "ha"] = Field(
        default="en",
        description="Language for response (en=English, yo=Yoruba, ig=Igbo, ha=Hausa)"
    )


class FruitClassificationResult(BaseModel):
    """Result of fruit classification"""
    is_mango: bool
    variety: Optional[str] = None
    confidence: float
    notes: Optional[str] = None


class RipenessResult(BaseModel):
    """Result of ripeness detection"""
    ripeness_stage: Literal["underripe", "ripe", "overripe", "spoiled"]
    confidence: float
    color_description: Optional[str] = None
    recommendation: Optional[str] = None
    days_to_optimal: Optional[int] = None


class DiseaseResult(BaseModel):
    """Result of disease detection"""
    is_diseased: bool
    diseases_detected: List[str] = []
    confidence: float
    severity: Optional[Literal["low", "medium", "high"]] = None
    treatment: Optional[str] = None
    preventive_measures: Optional[str] = None


class Recommendation(BaseModel):
    """Buying/consumption recommendation"""
    action: Literal["buy", "buy_wait", "eat_soon", "avoid", "discard", "unknown"]
    message: str
    reason: str


class FullAnalysisResponse(BaseModel):
    """Complete analysis response"""
    language: str
    analysis_mode: Literal["online", "offline"]
    fruit_classification: Optional[dict] = None
    ripeness: Optional[dict] = None
    disease: Optional[dict] = None
    recommendation: Optional[dict] = None
    message: Optional[str] = None
    error: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    mode: Literal["online", "offline"]
    openai_configured: bool
    supported_languages: List[str]
