class ExplanationGenerator:
    """Generates context-aware human-readable explanations for semantic resume-job matches."""

    SPECIAL_EXPLANATIONS = {
        ("scikit-learn", "machine learning"): "Scikit-learn is directly associated with machine learning model development.",
        ("sklearn", "machine learning"): "Scikit-learn is a core Python library for machine learning algorithms.",
        ("pytorch", "deep learning"): "PyTorch is an industry-standard deep learning framework.",
        ("fastapi", "rest api"): "FastAPI is built specifically for building high-performance REST APIs.",
        ("react", "frontend"): "React is a leading library for building dynamic frontend user interfaces.",
        ("postgresql", "relational database"): "PostgreSQL is a powerful open-source relational database system.",
        ("docker", "containerization"): "Docker is the industry standard tool for application containerization.",
        ("kubernetes", "container orchestration"): "Kubernetes provides automated container orchestration and deployment.",
    }

    def generate_match_explanation(
        self, resume_item: str, job_req: str, similarity: float, is_match: bool
    ) -> str:
        r_clean = resume_item.strip().lower()
        j_clean = job_req.strip().lower()

        # Check special domain explanation map
        if (r_clean, j_clean) in self.SPECIAL_EXPLANATIONS:
            return self.SPECIAL_EXPLANATIONS[(r_clean, j_clean)]
        if (j_clean, r_clean) in self.SPECIAL_EXPLANATIONS:
            return self.SPECIAL_EXPLANATIONS[(j_clean, r_clean)]

        sim_pct = int(round(similarity * 100))

        if is_match:
            if r_clean == j_clean:
                return f"Exact match for required skill '{job_req}'."
            elif similarity >= 0.85:
                return f"'{resume_item}' demonstrates strong semantic alignment with required skill '{job_req}' ({sim_pct}% match)."
            elif similarity >= 0.70:
                return f"'{resume_item}' is closely related to required capability '{job_req}' ({sim_pct}% match)."
            else:
                return f"'{resume_item}' provides relevant experience matching '{job_req}' ({sim_pct}% match)."
        else:
            return f"Candidate experience '{resume_item}' has low semantic overlap with '{job_req}' ({sim_pct}% match)."

    def generate_unmatched_explanation(self, job_req: str) -> str:
        return f"Job requirement '{job_req}' was not explicitly covered or matched in candidate profile."


explanation_generator = ExplanationGenerator()
