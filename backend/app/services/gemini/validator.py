import json
import re
import logging
from typing import Type, TypeVar, Optional, Dict
from pydantic import BaseModel, ValidationError

logger = logging.getLogger("app.services.gemini.validator")

T = TypeVar("T", bound=BaseModel)


class StructuredOutputValidator:
    """Validates raw LLM response strings against Pydantic schemas."""

    @staticmethod
    def extract_json(raw_text: str) -> Optional[Dict]:
        """Extracts JSON dict from raw LLM output string."""
        if not raw_text:
            return None

        # Clean markdown fenced code blocks if present
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)

        # Attempt direct JSON parse
        try:
            return json.loads(cleaned)
        except Exception:
            pass

        # Match first brace pair { ... }
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass

        return None

    def validate_and_parse(self, raw_text: str, target_model: Type[T]) -> Optional[T]:
        """Parses raw LLM text and validates against target Pydantic schema T."""
        json_obj = self.extract_json(raw_text)
        if not json_obj:
            logger.warning(f"Failed to extract JSON from LLM response for model {target_model.__name__}")
            return None

        try:
            return target_model.model_validate(json_obj)
        except ValidationError as ve:
            logger.warning(f"Pydantic validation failed for {target_model.__name__}: {ve}")
            return None


structured_output_validator = StructuredOutputValidator()
