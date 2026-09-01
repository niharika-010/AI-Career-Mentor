import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.schemas.resume_intelligence import (
    ParsedResumeIntelligence,
    FieldWithConfidence,
    ContactInfo,
)
from app.services.resume_intelligence.section_classifier import section_classifier
from app.services.resume_intelligence.contact_extractor import contact_extractor
from app.services.resume_intelligence.skills_taxonomy import skills_taxonomy_extractor
from app.services.resume_intelligence.education_extractor import education_extractor
from app.services.resume_intelligence.experience_extractor import experience_extractor
from app.services.resume_intelligence.project_extractor import project_extractor
from app.services.resume_intelligence.certification_extractor import certification_extractor
from app.services.resume_intelligence.achievement_extractor import achievement_extractor
from app.services.resume_intelligence.language_extractor import language_extractor
from app.services.resume_intelligence.llm_fallback import llm_fallback_service


class ResumeIntelligenceEngine:
    """Master Resume Intelligence Engine.
    Executes modular deterministic, NLP, and fallback extractors to produce normalized Pydantic output.
    """

    def extract_summary(self, classified_sections: Dict[str, List[str]], full_text: str) -> FieldWithConfidence[Optional[str]]:
        """Extract professional summary block."""
        if "summary" in classified_sections:
            summary_text = " ".join(classified_sections["summary"]).strip()
            if len(summary_text) > 20:
                return FieldWithConfidence(value=summary_text[:1000], confidence=0.95, source="summary_section")

        # Heuristic fallback: Text between header and first major section
        lines = [l.strip() for l in full_text.split("\n") if l.strip()]
        if len(lines) > 2:
            body = " ".join(lines[1:5])
            if 30 < len(body) < 500:
                return FieldWithConfidence(value=body, confidence=0.75, source="heuristic_header_summary")

        return FieldWithConfidence(value=None, confidence=0.0, source="unknown")

    def _calculate_overall_confidence(
        self,
        contact: ContactInfo,
        summary: FieldWithConfidence,
        skills: List[Any],
        education: List[Any],
        experience: List[Any],
    ) -> float:
        """Calculates weighted aggregate parser confidence score."""
        scores = []
        weights = []

        # Contact Name
        scores.append(contact.name.confidence)
        weights.append(2.0)

        # Contact Email
        scores.append(contact.email.confidence)
        weights.append(2.0)

        # Summary
        if summary.value:
            scores.append(summary.confidence)
            weights.append(1.0)

        # Skills
        if skills:
            avg_skill_conf = sum(s.confidence for s in skills) / len(skills)
            scores.append(avg_skill_conf)
            weights.append(2.5)

        # Education
        if education:
            avg_edu_conf = sum(e.confidence for e in education) / len(education)
            scores.append(avg_edu_conf)
            weights.append(1.5)

        # Experience
        if experience:
            avg_exp_conf = sum(ex.confidence for ex in experience) / len(experience)
            scores.append(avg_exp_conf)
            weights.append(2.5)

        if not scores:
            return 0.0

        total_weight = sum(weights)
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        return round(weighted_sum / total_weight, 2)

    def parse_text(self, raw_text: str) -> ParsedResumeIntelligence:
        """
        Executes full deterministic and NLP extraction workflow over resume text.
        """
        if not raw_text or not raw_text.strip():
            return ParsedResumeIntelligence(
                overall_confidence=0.0,
                extraction_method="deterministic_nlp",
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

        # 1. Section Classification
        classified = section_classifier.classify_sections(raw_text)

        # 2. Extract Contact Details
        contact = contact_extractor.extract(classified, raw_text)

        # 3. Extract Summary
        summary = self.extract_summary(classified, raw_text)

        # 4. Extract Skills (Technical & Soft)
        skills = skills_taxonomy_extractor.extract_skills(classified, raw_text)

        # 5. Extract Education
        education = education_extractor.extract(classified, raw_text)

        # 6. Extract Experience
        experience = experience_extractor.extract(classified, raw_text)

        # 7. Extract Projects
        projects = project_extractor.extract(classified, raw_text)

        # 8. Extract Certifications
        certifications = certification_extractor.extract(classified, raw_text)

        # 9. Extract Achievements
        achievements = achievement_extractor.extract(classified, raw_text)

        # 10. Extract Languages
        languages = language_extractor.extract(classified, raw_text)

        # 11. Calculate Overall Confidence Score
        overall_conf = self._calculate_overall_confidence(contact, summary, skills, education, experience)

        result = ParsedResumeIntelligence(
            contact=contact,
            summary=summary,
            skills=skills,
            education=education,
            experience=experience,
            projects=projects,
            certifications=certifications,
            achievements=achievements,
            languages=languages,
            overall_confidence=overall_conf,
            extraction_method="deterministic_nlp",
            extracted_at=datetime.now(timezone.utc).isoformat(),
        )

        return result


resume_intelligence_engine = ResumeIntelligenceEngine()
