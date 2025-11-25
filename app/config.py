"""
Configuration management for Valor AI
"""
import os
from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Model Configuration
    use_offline_mode: bool = os.getenv("USE_OFFLINE_MODE", "false").lower() == "true"

    # Language Configuration
    default_language: Literal["en", "yo", "ig", "ha"] = "en"

    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))

    # Model Paths (for offline mode)
    fruit_model_path: str = "models/fruit_classifier.h5"
    ripeness_model_path: str = "models/ripeness_classifier.h5"
    disease_model_path: str = "models/disease_classifier.h5"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Language translations for responses
LANGUAGE_TRANSLATIONS = {
    "en": {
        "produce_detected": "Produce detected",
        "not_produce": "Could not identify produce type",
        "underripe": "Underripe",
        "ripe": "Ripe",
        "overripe": "Overripe",
        "spoiled": "Spoiled",
        "healthy": "Healthy",
        "diseased": "Diseased",
        "confidence": "Confidence",
        "recommendation": "Recommendation",
        "buy_advice": "Good to buy",
        "wait_advice": "Wait a few days before consuming",
        "avoid_advice": "Avoid purchasing, quality compromised",
        "discard_advice": "Discard immediately, spoiled"
    },
    "yo": {
        "produce_detected": "A ri eso",
        "not_produce": "Ko ri iru eso",
        "underripe": "Ko ti pon",
        "ripe": "Ti pon dada",
        "overripe": "Ti pon ju",
        "spoiled": "Ti baje",
        "healthy": "O dara",
        "diseased": "O ni arun",
        "confidence": "Igbagbo",
        "recommendation": "Imoran",
        "buy_advice": "O dara lati ra",
        "wait_advice": "Duro fun ojo die ki o to je e",
        "avoid_advice": "Mase ra, didara ti baje",
        "discard_advice": "Da sile lesekese, ti baje"
    },
    "ig": {
        "produce_detected": "Achopụtara mkpuru",
        "not_produce": "Achọpụtaghị ụdị mkpuru",
        "underripe": "Ochaghi acha",
        "ripe": "Achaala nke oma",
        "overripe": "Achaala nke ukwuu",
        "spoiled": "Emebiela",
        "healthy": "O di mma",
        "diseased": "O nwere oria",
        "confidence": "Ntukwasi obi",
        "recommendation": "Ndumod",
        "buy_advice": "O di mma izuta",
        "wait_advice": "Chere ubochi ole na ole tupu iri ya",
        "avoid_advice": "Azula, ogo emebiela",
        "discard_advice": "Tufuo ozugbo, emebiela"
    },
    "ha": {
        "produce_detected": "An gano kayan lambu",
        "not_practice": "Ba a gano irin kayan lambu ba",
        "underripe": "Bai nuna ba",
        "ripe": "Ya nuna sosai",
        "overripe": "Ya wuce nuna",
        "spoiled": "Ya lalace",
        "healthy": "Yana da lafiya",
        "diseased": "Yana da cuta",
        "confidence": "Aminci",
        "recommendation": "Shawarar",
        "buy_advice": "Yana da kyau a saya",
        "wait_advice": "Jira kwanaki kadan kafin ci",
        "avoid_advice": "Kada ka saya, inganci ya lalace",
        "discard_advice": "Zubar da shi nan take, ya lalace"
    }
}

def get_translation(key: str, language: str = "en") -> str:
    """Get translation for a given key and language"""
    return LANGUAGE_TRANSLATIONS.get(language, LANGUAGE_TRANSLATIONS["en"]).get(key, key)
