from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.schemas.job_intelligence import ParsedJobIntelligence
from app.services.job_intelligence.section_classifier import job_section_classifier
from app.services.job_intelligence.skills_tech_extractor import skills_tech_extractor
from app.services.job_intelligence.experience_education_extractor import experience_education_extractor
from app.services.job_intelligence.industry_title_extractor import industry_title_extractor
from app.services.job_intelligence.llm_fallback import job_llm_fallback_service


class JobIntelligenceEngine:
    """Master Job Description Intelligence Engine.
    Executes modular deterministic & NLP extractors with source_text attribution.
    """

    def _calculate_overall_confidence(
        self,
        required_skills: list,
        experience_conf: float,
        education_conf: float,
        technologies: list,
    ) -> float:
        scores = []
        weights = []

        if required_skills:
            scores.append(sum(s.confidence for s in required_skills) / len(required_skills))
            weights.append(3.0)

        if technologies:
            scores.append(sum(t.confidence for t in technologies) / len(technologies))
            weights.append(2.0)

        scores.append(experience_conf)
        weights.append(2.5)

        scores.append(education_conf)
        weights.append(1.5)

        if not scores:
            return 0.0

        return round(sum(s * w for s, w in zip(scores, weights)) / sum(weights), 2)

    def parse_text(
        self,
        raw_text: str,
        title: Optional[str] = None,
        company_name: Optional[str] = None,
    ) -> ParsedJobIntelligence:
        if not raw_text or not raw_text.strip():
            return ParsedJobIntelligence(
                overall_confidence=0.0,
                extraction_method="deterministic_nlp",
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )

        # 1. Section Classification
        classified = job_section_classifier.classify_sections(raw_text)

        # 2. Title & Industry
        clean_title, raw_t = industry_title_extractor.normalize_title(title, raw_text)
        industry = industry_title_extractor.infer_industry(raw_text)

        # 3. Skills, Technologies, Tools, Keywords, Soft Skills, Responsibilities
        (
            req_skills,
            pref_skills,
            responsibilities,
            keywords,
            soft_skills,
            tools,
            technologies,
        ) = skills_tech_extractor.extract(classified, raw_text)

        # 4. Experience, Education, Certifications
        exp_req = experience_education_extractor.extract_experience(raw_text)
        edu_req = experience_education_extractor.extract_education(raw_text)
        certs = experience_education_extractor.extract_certifications(raw_text)

        # 5. Overall Confidence
        overall_conf = self._calculate_overall_confidence(
            req_skills, exp_req.confidence, edu_req.confidence, technologies
        )

        return ParsedJobIntelligence(
            job_title=clean_title,
            raw_title=raw_t,
            company_name=company_name,
            industry=industry,
            required_skills=req_skills,
            preferred_skills=pref_skills,
            responsibilities=responsibilities,
            experience_requirement=exp_req,
            education_requirement=edu_req,
            certifications=certs,
            technical_keywords=keywords,
            soft_skills=soft_skills,
            tools=tools,
            technologies=technologies,
            overall_confidence=overall_conf,
            extraction_method="deterministic_nlp",
            extracted_at=datetime.now(timezone.utc).isoformat(),
        )


job_intelligence_engine = JobIntelligenceEngine()
