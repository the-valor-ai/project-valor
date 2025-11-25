"""
AI Service for Valor - Integrates OpenAI Vision API with offline fallback
"""
import base64
import io
import json
import re
from typing import Dict, Literal, Optional
from PIL import Image
import openai
from app.config import settings, get_translation


class ValorAIService:
    """
    AI Service that handles:
    1. Fruit/vegetable classification and identification
    2. Ripeness detection (underripe/ripe/overripe/spoiled)
    3. Disease detection and health assessment
    """

    def __init__(self):
        if not settings.use_offline_mode and settings.openai_api_key:
            openai.api_key = settings.openai_api_key
        self.use_offline = settings.use_offline_mode

    def _encode_image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def _build_prompt(self, analysis_type: str, language: str = "en") -> str:
        """Build prompts for different analysis types"""

        if analysis_type == "fruit_classification":
            return """You are an expert agricultural AI assistant specializing in fruit and vegetable identification.

Analyze this image and determine:
1. What type of fruit or vegetable is this?
2. What variety or cultivar might it be?
3. Confidence score (0-100 percent)

IMPORTANT: Respond with ONLY valid JSON. No extra text. Use this exact format:
{
    "fruit_type": "mango",
    "variety": "Kent",
    "confidence": 95,
    "notes": "large yellow fruit with smooth skin"
}

Replace values but keep structure. Use "unknown" for variety if unclear."""

        elif analysis_type == "ripeness":
            return """You are an expert in fruit and vegetable ripeness assessment.

Analyze this produce image and classify its ripeness stage:
- underripe: Not ready to eat, needs more time to ripen
- ripe: Perfect for consumption, optimal eating quality
- overripe: Very soft, past peak quality, consume immediately
- spoiled: Rotten, moldy, unsafe to eat

Consider:
- Skin color changes (green to yellow/red/brown)
- Surface texture (smooth to spotted to moldy)
- Visual firmness indicators
- Signs of decay

IMPORTANT: Respond with ONLY valid JSON. No extra text before or after. Use this exact format:
{
    "ripeness_stage": "ripe",
    "confidence": 90,
    "color_description": "yellow with slight green at stem",
    "recommendation": "ready to eat today",
    "days_to_optimal": null
}

Replace the values but keep the structure. Use null (not "null") for days_to_optimal if already ripe or spoiled."""

        elif analysis_type == "disease":
            return """You are an expert plant pathologist specializing in fruit and vegetable diseases.

Analyze this produce for diseases or defects. Common issues include:
- Anthracnose: Dark sunken spots, black lesions
- Powdery Mildew: White powdery coating
- Bacterial spots: Dark spots with halos
- Stem/blossom end rot: Decay from ends
- Fungal infections: Mold, fuzzy growth
- Physical damage: Bruising, cuts, insect damage

IMPORTANT: Respond with ONLY valid JSON. No extra text. Use this exact format:
{
    "is_diseased": false,
    "diseases_detected": [],
    "confidence": 85,
    "severity": "low",
    "treatment": "No treatment needed",
    "preventive_measures": "Store in cool dry place"
}

Replace values but keep structure. Use empty array [] if no diseases detected."""

        return ""

    async def analyze_with_openai(
        self,
        image: Image.Image,
        analysis_type: Literal["fruit_classification", "ripeness", "disease"],
        language: str = "en"
    ) -> Dict:
        """Use OpenAI Vision API for analysis"""

        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")

        # Convert image to base64
        base64_image = self._encode_image_to_base64(image)

        # Build prompt
        prompt = self._build_prompt(analysis_type, language)

        try:
            # Call OpenAI Vision API
            response = openai.chat.completions.create(
                model="gpt-4o",  # or gpt-4-vision-preview
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.2  # Lower temperature for more consistent results
            )

            # Extract JSON from response
            result_text = response.choices[0].message.content

            # Try to parse JSON (handle potential markdown code blocks)
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            # Clean up common JSON formatting issues
            result_text = result_text.strip()

            # Try to parse JSON
            try:
                result = json.loads(result_text)
                return result
            except json.JSONDecodeError as je:
                # If JSON parsing fails, try to fix common issues
                print(f"JSON Parse Error: {str(je)}")
                print(f"Raw response: {result_text[:200]}...")

                # Try to extract JSON object using regex
                import re
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result_text, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group(0))
                        return result
                    except:
                        pass

                # If all else fails, return error with raw text
                return {
                    "error": f"Failed to parse JSON: {str(je)}",
                    "raw_response": result_text[:500],
                    "fallback_used": False
                }

        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            return {"error": str(e), "fallback_used": False}

    def analyze_offline(
        self,
        image: Image.Image,
        analysis_type: Literal["fruit_classification", "ripeness", "disease"]
    ) -> Dict:
        """Offline fallback using local models (placeholder for now)"""

        # TODO: Implement with TFLite/ONNX models for mobile deployment
        return {
            "error": "Offline mode not yet implemented",
            "message": "Please connect to internet for AI analysis",
            "fallback_used": True
        }

    async def full_analysis(
        self,
        image: Image.Image,
        language: str = "en"
    ) -> Dict:
        """
        Perform complete analysis pipeline:
        1. Fruit/vegetable classification
        2. Ripeness detection
        3. Disease detection
        """

        results = {
            "language": language,
            "analysis_mode": "offline" if self.use_offline else "online"
        }

        try:
            if self.use_offline:
                # Use offline models
                fruit_result = self.analyze_offline(image, "fruit_classification")
                results["fruit_classification"] = fruit_result

                if not fruit_result.get("error"):
                    results["ripeness"] = self.analyze_offline(image, "ripeness")
                    results["disease"] = self.analyze_offline(image, "disease")

            else:
                # Use OpenAI Vision API
                # Step 1: Fruit Classification
                fruit_result = await self.analyze_with_openai(
                    image, "fruit_classification", language
                )
                results["fruit_classification"] = fruit_result

                # Only proceed if classification succeeded
                if not fruit_result.get("error"):
                    # Step 2: Ripeness Detection
                    ripeness_result = await self.analyze_with_openai(
                        image, "ripeness", language
                    )
                    results["ripeness"] = ripeness_result

                    # Step 3: Disease Detection
                    disease_result = await self.analyze_with_openai(
                        image, "disease", language
                    )
                    results["disease"] = disease_result

                    # Add recommendations only if no errors
                    if not ripeness_result.get("error") and not disease_result.get("error"):
                        results["recommendation"] = self._generate_recommendation(
                            ripeness_result, disease_result, language
                        )
                    else:
                        results["recommendation"] = {
                            "action": "retry",
                            "message": "Some analysis failed, please retry",
                            "reason": "Incomplete analysis due to errors"
                        }
                else:
                    results["message"] = "Could not identify produce type"

            return results

        except Exception as e:
            return {
                "error": str(e),
                "message": "Analysis failed. Please try again."
            }

    def _generate_recommendation(
        self,
        ripeness: Dict,
        disease: Dict,
        language: str
    ) -> Dict:
        """Generate buying/consumption recommendation based on analysis"""

        is_diseased = disease.get("is_diseased", False)
        ripeness_stage = ripeness.get("ripeness_stage", "unknown")

        # Decision logic
        if is_diseased:
            return {
                "action": "avoid",
                "message": get_translation("avoid_advice", language),
                "reason": f"Disease detected: {', '.join(disease.get('diseases_detected', []))}"
            }

        if ripeness_stage == "spoiled":
            return {
                "action": "discard",
                "message": get_translation("discard_advice", language),
                "reason": "Produce is spoiled"
            }

        if ripeness_stage == "ripe":
            return {
                "action": "buy",
                "message": get_translation("buy_advice", language),
                "reason": "Perfect ripeness for consumption"
            }

        if ripeness_stage == "underripe":
            days = ripeness.get("days_to_optimal", 3)
            return {
                "action": "buy_wait",
                "message": get_translation("wait_advice", language),
                "reason": f"Wait approximately {days} days before eating"
            }

        if ripeness_stage == "overripe":
            return {
                "action": "eat_soon",
                "message": "Eat within 24 hours",
                "reason": "Overripe but still consumable"
            }

        return {
            "action": "unknown",
            "message": "Unable to generate recommendation",
            "reason": "Incomplete analysis"
        }


# Singleton instance
ai_service = ValorAIService()
