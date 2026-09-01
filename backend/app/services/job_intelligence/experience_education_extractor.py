import re
from typing import Dict, List, Tuple, Optional
from app.schemas.job_intelligence import (
    JobExperienceRequirement,
    JobEducationRequirement,
    RequirementItem,
)
from app.services.job_intelligence.requirement_classifier import requirement_classifier


class ExperienceEducationExtractor:
    """Extracts Experience Requirements, Education Requirements, and Certifications with exact source_text."""

    YOE_REGEX = r"\b(\d+)(?:\s*(?:to|-)\s*(\d+))?\s*\+?\s*(?:years?|yrs?)(?:\s*of)?\s*(?:relevant\s+|professional\s+)?experience\b"
    
    DEGREE_PATTERNS = [
        (r"\b(?:Ph\.?D\.?|Doctorate)\b", "Ph.D."),
        (r"\b(?:Master(?:'s)?|M\.?S\.?|M\.?T\.?ech|MBA)\b", "Master's"),
        (r"\b(?:Bachelor(?:'s)?|B\.?S\.?|B\.?T\.?ech|B\.?A\.?|B\.?E\.?)\b", "Bachelor's"),
        (r"\b(?:Associate(?:'s)?|A\.?S\.?)\b", "Associate's"),
    ]

    MAJORS = [
        "Computer Science", "Software Engineering", "Data Science", "Information Technology",
        "Electrical Engineering", "Computer Engineering", "Mathematics", "Statistics", "Physics"
    ]

    CERT_KEYWORDS = [
        "AWS Certified", "AWS Solutions Architect", "Google Cloud Certified",
        "Azure Certified", "PMP", "Certified Scrum Master", "CSM", "CISSP", "CKA"
    ]

    def extract_experience(self, raw_text: str) -> JobExperienceRequirement:
        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
        
        min_years = 0.0
        max_years = None
        source_text = ""

        # Search YOE regex
        match = re.search(self.YOE_REGEX, raw_text, re.IGNORECASE)
        if match:
            min_years = float(match.group(1))
            if match.group(2):
                max_years = float(match.group(2))
            
            # Find line snippet
            for l in lines:
                if re.search(self.YOE_REGEX, l, re.IGNORECASE):
                    source_text = l
                    break

        # Seniority level determination (prioritizing title keywords)
        text_lower = raw_text.lower()
        first_line_lower = lines[0].lower() if lines else ""
        
        if "principal" in first_line_lower or "staff" in first_line_lower:
            seniority = "Principal"
        elif "lead" in first_line_lower:
            seniority = "Lead"
        elif "senior" in first_line_lower:
            seniority = "Senior"
        elif "principal" in text_lower or "staff" in text_lower:
            seniority = "Principal"
        elif "lead" in text_lower and "engineer" in text_lower:
            seniority = "Lead"
        elif min_years >= 5.0 or "senior" in text_lower:
            seniority = "Senior"
        elif 2.0 <= min_years < 5.0 or "mid" in text_lower:
            seniority = "Mid-Level"
        elif min_years > 0 or "junior" in text_lower or "entry" in text_lower:
            seniority = "Entry-Level"
        else:
            seniority = "Unspecified"

        return JobExperienceRequirement(
            min_years=min_years,
            max_years=max_years,
            seniority_level=seniority,
            confidence=0.92 if min_years > 0 else 0.70,
            source_text=source_text or ("Experience requirements specified" if min_years > 0 else ""),
        )

    def extract_education(self, raw_text: str) -> JobEducationRequirement:
        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]

        detected_degree = "Unspecified"
        detected_major = None
        source_text = ""

        for pat, canonical in self.DEGREE_PATTERNS:
            if re.search(pat, raw_text, re.IGNORECASE):
                detected_degree = canonical
                for l in lines:
                    if re.search(pat, l, re.IGNORECASE):
                        source_text = l
                        break
                break

        for major in self.MAJORS:
            if re.search(r"\b" + re.escape(major) + r"\b", raw_text, re.IGNORECASE):
                detected_major = major
                break

        req_type = requirement_classifier.classify_requirement(source_text) if source_text else "required"

        return JobEducationRequirement(
            degree_level=detected_degree,
            field_of_study=detected_major,
            requirement_type=req_type,
            confidence=0.90 if detected_degree != "Unspecified" else 0.65,
            source_text=source_text,
        )

    def extract_certifications(self, raw_text: str) -> List[RequirementItem]:
        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
        certs: List[RequirementItem] = []

        for cert in self.CERT_KEYWORDS:
            pattern = r"\b" + re.escape(cert) + r"\b"
            if re.search(pattern, raw_text, re.IGNORECASE):
                snippet = ""
                for l in lines:
                    if re.search(pattern, l, re.IGNORECASE):
                        snippet = l
                        break
                
                req_type = requirement_classifier.classify_requirement(snippet)
                certs.append(
                    RequirementItem(
                        name=cert,
                        category="certification",
                        requirement_type=req_type,
                        confidence=0.92,
                        source_text=snippet or f"Certification requirement: {cert}",
                    )
                )

        return certs


experience_education_extractor = ExperienceEducationExtractor()
