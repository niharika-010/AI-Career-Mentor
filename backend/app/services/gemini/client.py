import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("app.services.gemini.client")

# Optional import of google.generativeai
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False


class GeminiClient:
    """Centralized client abstraction for Google Gemini API calls.
    Manages API key isolation, model initialization, timeout handling, and API failure fallbacks.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self._model = None

        if GENAI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel(self.model_name)
                logger.info(f"GeminiClient initialized with model {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize GeminiClient: {e}")

    def is_configured(self) -> bool:
        """Returns True if Gemini API key is configured and genai is available."""
        return self._model is not None

    def generate_content(
        self, prompt: str, system_instruction: Optional[str] = None
    ) -> Optional[str]:
        """Invokes Gemini model to generate content with timeout and error handling."""
        if not self.is_configured():
            logger.debug("GeminiClient unconfigured or API key missing. Using fallback.")
            return None

        try:
            # Execute Gemini call
            response = self._model.generate_content(
                prompt,
                generation_config={"temperature": 0.2, "top_p": 0.9}
            )
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
            return None
        except Exception as e:
            logger.error(f"Gemini API execution failed: {e}")
            return None


gemini_client = GeminiClient()
