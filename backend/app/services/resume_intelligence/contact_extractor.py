import re
from typing import Dict, Any, Optional
from app.schemas.resume_intelligence import ContactInfo, FieldWithConfidence

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except ImportError:
    nlp = None


class ContactExtractor:
    """Extracts candidate contact details (Name, Email, Phone, LinkedIn, GitHub, Portfolio, Location)."""

    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    PHONE_REGEX = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    LINKEDIN_REGEX = r"(?:https?://)?(?:www\.)?linkedin\.com/in/([A-Za-z0-9_-]+)/?"
    GITHUB_REGEX = r"(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_-]+)/?"
    PORTFOLIO_REGEX = r"https?://(?:www\.)?(?!linkedin\.com|github\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[^\s]*)?"

    def extract_name(self, header_lines: list, full_text: str) -> FieldWithConfidence[Optional[str]]:
        """Extract candidate full name from top header lines using spaCy or heuristics."""
        candidate_lines = header_lines[:5] if header_lines else full_text.split("\n")[:5]

        for line in candidate_lines:
            line_str = line.strip()
            if not line_str or re.search(self.EMAIL_REGEX, line_str) or re.search(self.PHONE_REGEX, line_str):
                continue
            if "linkedin.com" in line_str or "github.com" in line_str or "http" in line_str:
                continue

            # Check spaCy PERSON entity line by line
            if nlp:
                doc = nlp(line_str)
                for ent in doc.ents:
                    if ent.label_ == "PERSON" and 1 <= len(ent.text.strip().split()) <= 4:
                        clean_val = ent.text.strip().title()
                        if not any(w in clean_val.lower() for w in ["resume", "curriculum", "vitae", "profile", "cv"]):
                            return FieldWithConfidence(value=clean_val, confidence=0.95, source="spacy_ner_person")

            # Fallback line matching
            clean_line_prefix = re.sub(r"^(?:Dr\.|Mr\.|Ms\.|Mrs\.|Prof\.)\s+", "", line_str, flags=re.IGNORECASE).strip()
            if len(clean_line_prefix) < 40 and re.match(r"^[A-Za-z\s\.\-']+$", clean_line_prefix):
                words = clean_line_prefix.split()
                if 1 <= len(words) <= 4:
                    return FieldWithConfidence(value=clean_line_prefix.title(), confidence=0.82, source="heuristic_header")

        return FieldWithConfidence(value=None, confidence=0.0, source="unknown")

    def extract_email(self, text: str) -> FieldWithConfidence[Optional[str]]:
        match = re.search(self.EMAIL_REGEX, text)
        if match:
            return FieldWithConfidence(value=match.group(0).lower(), confidence=0.99, source="regex_email")
        return FieldWithConfidence(value=None, confidence=0.0, source="unknown")

    def extract_phone(self, text: str) -> FieldWithConfidence[Optional[str]]:
        match = re.search(self.PHONE_REGEX, text)
        if match:
            phone_str = match.group(0).strip()
            if len(re.sub(r"\D", "", phone_str)) >= 7:
                return FieldWithConfidence(value=phone_str, confidence=0.95, source="regex_phone")
        return FieldWithConfidence(value=None, confidence=0.0, source="unknown")

    def extract_linkedin(self, text: str) -> FieldWithConfidence[Optional[str]]:
        match = re.search(self.LINKEDIN_REGEX, text, re.IGNORECASE)
        if match:
            url = match.group(0)
            if not url.startswith("http"):
                url = f"https://{url}"
            return FieldWithConfidence(value=url, confidence=0.98, source="regex_linkedin")
        return FieldWithConfidence(value=None, confidence=0.0, source="unknown")

    def extract_github(self, text: str) -> FieldWithConfidence[Optional[str]]:
        match = re.search(self.GITHUB_REGEX, text, re.IGNORECASE)
        if match:
            url = match.group(0)
            if not url.startswith("http"):
                url = f"https://{url}"
            return FieldWithConfidence(value=url, confidence=0.98, source="regex_github")
        return FieldWithConfidence(value=None, confidence=0.0, source="unknown")

    def extract_portfolio(self, text: str) -> FieldWithConfidence[Optional[str]]:
        match = re.search(self.PORTFOLIO_REGEX, text, re.IGNORECASE)
        if match:
            return FieldWithConfidence(value=match.group(0), confidence=0.90, source="regex_portfolio")
        return FieldWithConfidence(value=None, confidence=0.0, source="unknown")

    def extract_location(self, header_lines: list, full_text: str) -> FieldWithConfidence[Optional[str]]:
        """Extract city, state, country location from header or text using spaCy GPE or regex."""
        target_text = "\n".join(header_lines[:5]) if header_lines else full_text[:500]

        # 1. spaCy GPE / LOC entity check
        if nlp:
            doc = nlp(target_text)
            locs = [ent.text.strip() for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
            if locs:
                return FieldWithConfidence(value=", ".join(locs[:2]), confidence=0.88, source="spacy_ner_gpe")

        # 2. City, State / Country regex (e.g. San Francisco, CA or New York, USA)
        loc_match = re.search(r"\b([A-Z][a-zA-Z\s]+,\s*[A-Z]{2}\b|[A-Z][a-zA-Z\s]+,\s*[A-Z][a-zA-Z\s]+)", target_text)
        if loc_match:
            return FieldWithConfidence(value=loc_match.group(0).strip(), confidence=0.80, source="regex_location")

        return FieldWithConfidence(value=None, confidence=0.0, source="unknown")

    def extract(self, classified_sections: Dict[str, list], full_text: str) -> ContactInfo:
        header_lines = classified_sections.get("header", [])
        return ContactInfo(
            name=self.extract_name(header_lines, full_text),
            email=self.extract_email(full_text),
            phone=self.extract_phone(full_text),
            linkedin_url=self.extract_linkedin(full_text),
            github_url=self.extract_github(full_text),
            portfolio_url=self.extract_portfolio(full_text),
            location=self.extract_location(header_lines, full_text),
        )


contact_extractor = ContactExtractor()
