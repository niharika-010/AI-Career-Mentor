import re


class RequirementClassifier:
    """Classifies whether a requirement snippet is 'required' or 'preferred'."""

    PREFERRED_KEYWORDS = [
        r"\bnice\s+to\s+have\b",
        r"\bpreferred\b",
        r"\bbonus\b",
        r"\bplus\b",
        r"\boptional\b",
        r"\bdesirable\b",
        r"\bideal(?:ly)?\b",
        r"\badvantage(?:ous)?\b",
        r"\bhelpful\b",
        r"\ba\s+plus\b",
    ]

    REQUIRED_KEYWORDS = [
        r"\bmust\s+have\b",
        r"\brequired\b",
        r"\bminimum\b",
        r"\bessential\b",
        r"\bmandatory\b",
        r"\bat\s+least\b",
        r"\bstrong\b",
        r"\bproven\b",
    ]

    def classify_requirement(self, text_snippet: str, section_name: str = "general") -> str:
        """Determines if the snippet or section indicates a required or preferred requirement."""
        if section_name == "preferred_qualifications":
            return "preferred"

        snippet_lower = text_snippet.lower()

        # Check explicit preferred keywords in snippet
        for kw in self.PREFERRED_KEYWORDS:
            if re.search(kw, snippet_lower):
                return "preferred"

        # Default to required unless in preferred context
        return "required"


requirement_classifier = RequirementClassifier()
