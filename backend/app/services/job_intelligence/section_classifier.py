import re
from typing import Dict, List, Tuple


class JobSectionClassifier:
    """Classifies job description text lines into normalized structural section blocks."""

    SECTION_PATTERNS = {
        "responsibilities": [
            r"^(?:key\s+)?responsibilities$",
            r"^duties(?:\s+&\s+responsibilities)?$",
            r"^what\s+you(?:'ll|\s+will)\s+do$",
            r"^the\s+role$",
            r"^role\s+description$",
            r"^core\s+responsibilities$",
        ],
        "required_qualifications": [
            r"^(?:minimum\s+)?requirements$",
            r"^(?:required\s+)?qualifications$",
            r"^what\s+we(?:'re|\s+are)\s+looking\s+for$",
            r"^what\s+you(?:'ll|\s+will)\s+need$",
            r"^must\s+haves?$",
            r"^basic\s+qualifications$",
            r"^required\s+skills$",
        ],
        "preferred_qualifications": [
            r"^preferred\s+(?:qualifications|skills)$",
            r"^nice\s+to\s+haves?$",
            r"^bonus\s+(?:points|qualifications|skills)$",
            r"^desired\s+qualifications$",
            r"^pluses?$",
            r"^additional\s+qualifications$",
        ],
        "about_company": [
            r"^about\s+(?:us|the\s+company)$",
            r"^company\s+overview$",
            r"^who\s+we\s+are$",
        ],
        "benefits": [
            r"^benefits(?:\s+&\s+perks)?$",
            r"^what\s+we\s+offer$",
            r"^perks$",
            r"^compensation$",
        ],
    }

    def is_heading(self, line: str) -> Tuple[bool, str]:
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


job_section_classifier = JobSectionClassifier()
