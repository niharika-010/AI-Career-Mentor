import re
from typing import Dict, List, Tuple


class SectionClassifier:
    """Classifies document lines into normalized section blocks using regex and heuristic patterns."""
    
    SECTION_PATTERNS = {
        "summary": [
            r"^(?:professional\s+)?summary$",
            r"^profile$",
            r"^(?:career\s+)?objective$",
            r"^about\s+me$",
            r"^executive\s+summary$",
            r"^overview$",
        ],
        "skills": [
            r"^(?:technical\s+)?skills$",
            r"^core\s+competencies$",
            r"^technologies$",
            r"^skills\s+&\s+tools$",
            r"^expertise$",
            r"^technical\s+expertise$",
            r"^domain\s+knowledge$",
        ],
        "experience": [
            r"^(?:work\s+)?experience$",
            r"^professional\s+experience$",
            r"^employment\s+history$",
            r"^work\s+history$",
            r"^relevant\s+experience$",
            r"^career\s+history$",
        ],
        "education": [
            r"^education$",
            r"^academic\s+background$",
            r"^qualifications$",
            r"^education\s+&\s+credentials$",
        ],
        "projects": [
            r"^projects$",
            r"^personal\s+projects$",
            r"^key\s+projects$",
            r"^academic\s+projects$",
            r"^technical\s+projects$",
        ],
        "certifications": [
            r"^certifications?$",
            r"^licenses?\s+&\s+certifications?$",
            r"^credentials$",
            r"^courses\s+&\s+certifications$",
        ],
        "achievements": [
            r"^achievements?$",
            r"^awards?\s+&\s+honors?$",
            r"^honors?$",
            r"^accomplishments?$",
            r"^key\s+achievements?$",
        ],
        "languages": [
            r"^languages?$",
            r"^spoken\s+languages?$",
            r"^language\s+proficiency$",
        ],
    }

    def is_heading(self, line: str) -> Tuple[bool, str]:
        """Check if a line matches a known section heading."""
        cleaned = line.strip().lower()
        cleaned = re.sub(r"[^\w\s&]", "", cleaned).strip()

        if not cleaned or len(line.strip()) > 45:
            return False, ""

        for section_key, patterns in self.SECTION_PATTERNS.items():
            for pat in patterns:
                if re.match(pat, cleaned, re.IGNORECASE):
                    return True, section_key

        return False, ""

    def classify_sections(self, raw_text: str) -> Dict[str, List[str]]:
        """Splits raw document text into clean section line blocks."""
        lines = raw_text.split("\n")
        classified: Dict[str, List[str]] = {"header": []}
        current_section = "header"

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            is_head, sec_key = self.is_heading(stripped)
            if is_head:
                current_section = sec_key
                if current_section not in classified:
                    classified[current_section] = []
            else:
                classified[current_section].append(stripped)

        return classified


section_classifier = SectionClassifier()
