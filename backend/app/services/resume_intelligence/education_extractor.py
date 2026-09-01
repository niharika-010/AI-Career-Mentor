import re
from typing import Dict, List, Optional
from app.schemas.resume_intelligence import EducationItem

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except ImportError:
    nlp = None


class EducationExtractor:
    """Extracts candidate education history (Degree, Institution, Major, Dates, GPA)."""

    DEGREE_PATTERNS = [
        (r"\b(?:Ph\.?D\.?|Doctor of Philosophy)\b", "Ph.D."),
        (r"\b(?:Master(?:'s)?|M\.?S\.?|M\.?T\.?ech|M\.?A\.?|MBA)\b", "Master's Degree"),
        (r"\b(?:Bachelor(?:'s)?|B\.?S\.?|B\.?T\.?ech|B\.?A\.?|B\.?E\.?|B\.?S\.?C\.?)\b", "Bachelor's Degree"),
        (r"\b(?:Associate(?:'s)?|A\.?S\.?|A\.?A\.?)\b", "Associate's Degree"),
        (r"\b(?:High\s+School\s+Diploma|GED)\b", "High School Diploma"),
    ]

    MAJORS = [
        "Computer Science", "Software Engineering", "Data Science", "Information Technology",
        "Electrical Engineering", "Computer Engineering", "Mechanical Engineering",
        "Business Administration", "Mathematics", "Statistics", "Physics", "Cybersecurity",
        "Artificial Intelligence", "Finance", "Economics"
    ]

    GPA_REGEX = r"\b(?:GPA:?\s*)?([0-3]\.\d{1,2}|4\.0)(?:\s*/\s*4\.0)?\b"
    YEAR_RANGE_REGEX = r"\b(19\d{2}|20\d{2})\s*(?:[-–]|to)\s*(19\d{2}|20\d{2}|Present)\b"
    SINGLE_YEAR_REGEX = r"\b(19\d{2}|20\d{2})\b"

    def extract(self, classified_sections: Dict[str, List[str]], full_text: str) -> List[EducationItem]:
        edu_lines = classified_sections.get("education", [])
        if not edu_lines:
            # Search full text lines if section not explicit
            lines = full_text.split("\n")
            edu_lines = [l.strip() for l in lines if any(w in l.lower() for w in ["university", "college", "bachelor", "master", "degree", "bs", "ms", "gpa"])]

        if not edu_lines:
            return []

        items: List[EducationItem] = []
        block_text = "\n".join(edu_lines)

        # 1. Degree Detection
        detected_degree = None
        for pat, canonical in self.DEGREE_PATTERNS:
            if re.search(pat, block_text, re.IGNORECASE):
                detected_degree = canonical
                break

        # 2. Field of Study / Major
        detected_major = None
        for major in self.MAJORS:
            if re.search(r"\b" + re.escape(major) + r"\b", block_text, re.IGNORECASE):
                detected_major = major
                break

        # 3. Institution / University Name
        detected_institution = None
        # Check spaCy ORG entity
        if nlp:
            doc = nlp(block_text)
            for ent in doc.ents:
                if ent.label_ == "ORG" and any(u in ent.text.lower() for u in ["university", "college", "institute", "school", "academy", "polytechnic"]):
                    detected_institution = ent.text.strip()
                    break

        if not detected_institution:
            inst_match = re.search(r"\b([A-Z][A-Za-z\s]+(?:University|College|Institute|Academy|School))\b", block_text)
            if inst_match:
                detected_institution = inst_match.group(1).strip()

        # 4. GPA Extraction
        gpa_match = re.search(self.GPA_REGEX, block_text, re.IGNORECASE)
        detected_gpa = gpa_match.group(1) if gpa_match else None

        # 5. Dates / Graduation Year
        start_date, end_date = None, None
        range_match = re.search(self.YEAR_RANGE_REGEX, block_text, re.IGNORECASE)
        if range_match:
            start_date, end_date = range_match.group(1), range_match.group(2)
        else:
            single_match = re.search(self.SINGLE_YEAR_REGEX, block_text)
            if single_match:
                end_date = single_match.group(1)

        if detected_degree or detected_institution or detected_major:
            items.append(
                EducationItem(
                    degree=detected_degree or "Higher Education",
                    institution=detected_institution,
                    field_of_study=detected_major,
                    start_date=start_date,
                    end_date=end_date,
                    gpa=detected_gpa,
                    confidence=0.90 if (detected_degree and detected_institution) else 0.78,
                    source="education_section" if "education" in classified_sections else "full_text_parser",
                )
            )

        return items


education_extractor = EducationExtractor()
