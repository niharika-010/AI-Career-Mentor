import re
from typing import Dict, List
from app.schemas.resume_intelligence import SpokenLanguageItem


class LanguageExtractor:
    """Extracts spoken languages and proficiency levels from document text."""

    SPOKEN_LANGUAGES = [
        "English", "Spanish", "French", "German", "Mandarin", "Chinese",
        "Japanese", "Hindi", "Portuguese", "Italian", "Russian", "Arabic",
        "Korean", "Dutch", "Swedish", "Polish"
    ]

    PROFICIENCY_LEVELS = [
        "Native", "Bilingual", "Fluent", "Full Professional", "Professional Working",
        "Intermediate", "Elementary", "Basic", "Conversational"
    ]

    def extract(self, classified_sections: Dict[str, List[str]], full_text: str) -> List[SpokenLanguageItem]:
        lang_lines = classified_sections.get("languages", [])
        if not lang_lines:
            lines = full_text.split("\n")
            lang_lines = [l.strip() for l in lines if "language" in l.lower() or any(lang.lower() in l.lower() for lang in self.SPOKEN_LANGUAGES)]

        if not lang_lines:
            return []

        block_text = "\n".join(lang_lines)
        found_languages: Dict[str, SpokenLanguageItem] = {}

        for lang in self.SPOKEN_LANGUAGES:
            pattern = r"\b" + re.escape(lang) + r"\b"
            if re.search(pattern, block_text, re.IGNORECASE):
                # Detect proficiency nearby
                prof = None
                for level in self.PROFICIENCY_LEVELS:
                    if re.search(r"\b" + re.escape(lang) + r"\b.*?" + re.escape(level), block_text, re.IGNORECASE | re.DOTALL):
                        prof = level
                        break
                
                found_languages[lang] = SpokenLanguageItem(
                    language=lang,
                    proficiency=prof or "Proficient",
                    confidence=0.92,
                    source="languages_section" if "languages" in classified_sections else "full_text_parser",
                )

        return list(found_languages.values())


language_extractor = LanguageExtractor()
