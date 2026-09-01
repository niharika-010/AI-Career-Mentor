from typing import Dict, Any, List


class EvidenceCollector:
    """Collects machine-generated evidence directly from extracted resume and job intelligence objects."""

    def collect_evidence(
        self,
        resume_intelligence: Dict[str, Any],
        job_intelligence: Dict[str, Any],
        raw_resume_text: str = "",
        raw_job_text: str = "",
    ) -> Dict[str, List[str]]:
        evidence: Dict[str, List[str]] = {
            "matched_skills": [],
            "missing_skills": [],
            "experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "ats": [],
            "keywords": [],
        }

        # 1. Skills Evidence
        cand_skills = [s.get("name", "").strip() for s in resume_intelligence.get("skills", []) if s.get("name")]
        job_req_skills = [s.get("name", "").strip() for s in job_intelligence.get("required_skills", []) if s.get("name")]
        job_techs = [t.get("name", "").strip() for t in job_intelligence.get("technologies", []) if t.get("name")]
        all_job_skills = list(set(job_req_skills + job_techs))

        cand_skills_lower = {s.lower() for s in cand_skills}
        for req in all_job_skills:
            if req.lower() in cand_skills_lower or any(req.lower() in c for c in cand_skills_lower):
                evidence["matched_skills"].append(f"Requirement '{req}' matched in profile skills ({', '.join(cand_skills[:5])}).")
            else:
                evidence["missing_skills"].append(f"Required skill '{req}' not explicitly listed in candidate skills.")

        # 2. Experience Evidence
        cand_yoe = float(resume_intelligence.get("experience_years", 0.0) or 0.0)
        job_exp_req = job_intelligence.get("experience_requirement", {})
        job_min_yoe = float(job_exp_req.get("min_years", 0.0) or 0.0)
        seniority = job_exp_req.get("seniority_level", "Unspecified")

        evidence["experience"].append(f"Candidate has {cand_yoe:.1f} YOE vs Job minimum requirement of {job_min_yoe:.1f} YOE.")
        evidence["experience"].append(f"Target seniority level: {seniority}.")
        for exp in resume_intelligence.get("experience", [])[:3]:
            title = exp.get("job_title", "Software Role")
            evidence["experience"].append(f"Extracted Role: '{title}'.")

        # 3. Projects Evidence
        cand_projs = resume_intelligence.get("projects", [])
        if cand_projs:
            for proj in cand_projs[:3]:
                p_title = proj.get("title", "Project")
                p_techs = proj.get("technologies", [])
                evidence["projects"].append(f"Project '{p_title}' utilizing tech: {', '.join(p_techs)}.")
        else:
            evidence["projects"].append("No explicit projects section extracted from candidate profile.")

        # 4. Education Evidence
        cand_edu = resume_intelligence.get("education", [])
        job_edu_req = job_intelligence.get("education_requirement", {})
        cand_degree = cand_edu[0].get("degree", "Unspecified") if cand_edu else "Unspecified"
        cand_field = cand_edu[0].get("field_of_study", "Unspecified") if cand_edu else "Unspecified"
        job_degree = job_edu_req.get("degree_level", "Unspecified")

        evidence["education"].append(f"Candidate degree: '{cand_degree}' in '{cand_field}'.")
        evidence["education"].append(f"Job degree requirement: '{job_degree}'.")

        # 5. Certifications Evidence
        cand_certs = resume_intelligence.get("certifications", [])
        job_certs = job_intelligence.get("certifications", [])
        cand_cert_names = [c.get("name", "") for c in cand_certs]
        job_cert_names = [c.get("name", "") for c in job_certs]

        if cand_cert_names:
            evidence["certifications"].append(f"Candidate certifications: {', '.join(cand_cert_names)}.")
        else:
            evidence["certifications"].append("Candidate has no certifications listed.")

        if job_cert_names:
            evidence["certifications"].append(f"Job requested certifications: {', '.join(job_cert_names)}.")

        # 6. ATS Signals Evidence
        contact = resume_intelligence.get("contact", {})
        sections = resume_intelligence.get("sections", {})
        evidence["ats"].append(f"Contact Info Extracted: Name={bool(contact.get('name'))}, Email={bool(contact.get('email'))}, Phone={bool(contact.get('phone'))}.")
        evidence["ats"].append(f"Structural Section Headers Count: {len(sections)}.")

        # 7. Keywords Evidence
        job_kws = [k.get("name", "") for k in job_intelligence.get("technical_keywords", []) if k.get("name")]
        if job_kws:
            matched_kws = [kw for kw in job_kws if kw.lower() in cand_skills_lower]
            evidence["keywords"].append(f"Matched {len(matched_kws)} of {len(job_kws)} domain technical keywords: {', '.join(matched_kws)}.")
        else:
            evidence["keywords"].append("No specific domain technical keywords listed in job description.")

        return evidence


evidence_collector = EvidenceCollector()
