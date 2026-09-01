import os
import json
from typing import Dict, Any, Optional
import httpx


class JobLLMFallbackService:
    """Secondary Gemini LLM Structured Extraction Fallback for Job Descriptions.
    Invoked ONLY when deterministic & NLP extraction is insufficient.
    """

    def is_fallback_needed(self, parsed_intelligence: Dict[str, Any]) -> bool:
        req_skills = parsed_intelligence.get("required_skills", [])
        techs = parsed_intelligence.get("technologies", [])
        overall_conf = parsed_intelligence.get("overall_confidence", 0.0)

        # Trigger fallback if no skills/technologies found or overall confidence < 0.65
        if not req_skills and not techs:
            return True
        if overall_conf < 0.65:
            return True
        return False

    async def fallback_extract(self, raw_text: str) -> Optional[Dict[str, Any]]:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None

        prompt = f"""
        Extract structured Job Description requirements from the text below.
        CRITICAL: Do NOT invent requirements. Only extract explicit statements from text.
        Return strictly valid JSON with these keys:
        - job_title (string)
        - company_name (string or null)
        - industry (string)
        - required_skills (list of objects with name, source_text)
        - preferred_skills (list of objects with name, source_text)
        - responsibilities (list of objects with name, source_text)
        - min_experience_years (number)
        - education_level (string)

        Job Posting Text:
        {raw_text[:3000]}
        """

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"}
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    text_resp = data["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(text_resp)
        except Exception:
            return None

        return None


job_llm_fallback_service = JobLLMFallbackService()
