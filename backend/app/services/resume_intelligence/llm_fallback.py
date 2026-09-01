import os
import json
from typing import Dict, Any, Optional
import httpx


class LLMFallbackService:
    """Secondary Gemini LLM Structured Extraction Fallback.
    Invoked ONLY when deterministic & NLP extraction is insufficient or missing key fields.
    """

    def is_fallback_needed(self, parsed_intelligence: Dict[str, Any]) -> bool:
        """Determines if deterministic/NLP extraction confidence is insufficient."""
        contact = parsed_intelligence.get("contact", {})
        name_conf = contact.get("name", {}).get("confidence", 0.0) if isinstance(contact.get("name"), dict) else getattr(contact.get("name"), "confidence", 0.0)
        email_conf = contact.get("email", {}).get("confidence", 0.0) if isinstance(contact.get("email"), dict) else getattr(contact.get("email"), "confidence", 0.0)

        has_exp = len(parsed_intelligence.get("experience", [])) > 0
        has_skills = len(parsed_intelligence.get("skills", [])) > 0

        # Trigger fallback if candidate name & email missing/low confidence or both experience & skills are missing
        if name_conf < 0.5 and email_conf < 0.5:
            return True
        if not has_exp and not has_skills:
            return True
        return False

    async def fallback_extract(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """
        Attempts structured JSON extraction using Gemini API if key is available.
        Returns dictionary of extracted fields or None if unavailable/failed.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None

        prompt = f"""
        Extract structured candidate JSON from the following resume text.
        Return strictly valid JSON with these keys:
        - name (string)
        - email (string)
        - phone (string)
        - summary (string)
        - skills (list of strings)
        - education (list of objects with degree, institution, field_of_study, gpa, end_date)
        - experience (list of objects with job_title, company, start_date, end_date, responsibilities)

        Resume Text:
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


llm_fallback_service = LLMFallbackService()
