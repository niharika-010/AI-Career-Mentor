import re
from typing import Dict, List, Tuple
from app.schemas.resume_intelligence import SkillItem


class SkillsTaxonomyExtractor:
    """Comprehensive Skill Taxonomy Extractor categorized into Technical and Soft Skills."""

    TECHNICAL_SKILLS_TAXONOMY = {
        "languages": [
            "Python", "JavaScript", "TypeScript", "C++", "C#", "Java", "Go", "Golang", "Rust",
            "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R", "Dart", "Elixir", "Haskell", "Perl",
            "Shell", "Bash", "PowerShell", "SQL", "HTML5", "CSS3", "Sass", "GraphQL"
        ],
        "frameworks": [
            "React", "React.js", "Next.js", "Vue", "Vue.js", "Angular", "Svelte", "Node.js",
            "Express", "Express.js", "NestJS", "FastAPI", "Django", "Flask", "Spring", "Spring Boot",
            "ASP.NET", ".NET Core", "Laravel", "Ruby on Rails", "Tailwind CSS", "Bootstrap",
            "Material UI", "Chakra UI", "Redux", "Zustand", "PyTorch", "TensorFlow", "Keras"
        ],
        "databases": [
            "PostgreSQL", "Postgres", "MySQL", "MariaDB", "MongoDB", "Redis", "Elasticsearch",
            "Cassandra", "DynamoDB", "SQLite", "Neo4j", "Oracle", "Microsoft SQL Server", "Snowflake",
            "BigQuery", "Supabase", "Firebase"
        ],
        "cloud_devops": [
            "AWS", "Amazon Web Services", "Google Cloud", "GCP", "Microsoft Azure", "Docker",
            "Kubernetes", "K8s", "Terraform", "Ansible", "Jenkins", "GitHub Actions", "GitLab CI",
            "CircleCI", "Nginx", "Apache", "Helm", "Cloudflare", "Serverless", "Prometheus", "Grafana"
        ],
        "data_ai": [
            "Pandas", "NumPy", "Scikit-Learn", "OpenCV", "NLTK", "spaCy", "Hugging Face", "LangChain",
            "LlamaIndex", "Apache Spark", "Airflow", "Kafka", "Databricks", "MLflow"
        ],
        "tools_other": [
            "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence", "Postman", "Swagger",
            "REST API", "Microservices", "System Design", "Agile", "Scrum", "CI/CD", "TDD", "Webpack", "Vite"
        ],
    }

    SOFT_SKILLS_TAXONOMY = [
        "Leadership", "Team Leadership", "Communication", "Cross-Functional Collaboration",
        "Problem Solving", "Critical Thinking", "Project Management", "Time Management",
        "Mentorship", "Stakeholder Management", "Agile", "Scrum", "Conflict Resolution",
        "Analytical Thinking", "Strategic Planning", "Adaptability", "Public Speaking",
        "Negotiation", "Customer Service", "Technical Writing"
    ]

    def extract_skills(self, classified_sections: Dict[str, List[str]], full_text: str) -> List[SkillItem]:
        extracted: Dict[str, SkillItem] = {}

        # Helper to scan text and record skills
        def scan_text(text: str, default_confidence: float, source_name: str):
            text_upper = f" {text.upper()} "
            
            # Scan Technical Taxonomy
            for subcat, skill_list in self.TECHNICAL_SKILLS_TAXONOMY.items():
                for skill in skill_list:
                    # Match exact word boundaries
                    pattern = r"(?<![A-Za-z0-9_#+])" + re.escape(skill.upper()) + r"(?![A-Za-z0-9_#+])"
                    if re.search(pattern, text_upper):
                        canonical_name = skill
                        if canonical_name not in extracted or extracted[canonical_name].confidence < default_confidence:
                            extracted[canonical_name] = SkillItem(
                                name=canonical_name,
                                category="technical",
                                subcategory=subcat,
                                confidence=default_confidence,
                                source=source_name,
                            )

            # Scan Soft Skills
            for soft_skill in self.SOFT_SKILLS_TAXONOMY:
                pattern = r"\b" + re.escape(soft_skill.upper()) + r"\b"
                if re.search(pattern, text_upper):
                    if soft_skill not in extracted or extracted[soft_skill].confidence < default_confidence:
                        extracted[soft_skill] = SkillItem(
                            name=soft_skill,
                            category="soft",
                            subcategory="soft_skills",
                            confidence=default_confidence,
                            source=source_name,
                        )

        # 1. High confidence scan in 'skills' section (0.98)
        if "skills" in classified_sections:
            skills_text = "\n".join(classified_sections["skills"])
            scan_text(skills_text, 0.98, "skills_section")

        # 2. Experience section scan (0.90)
        if "experience" in classified_sections:
            exp_text = "\n".join(classified_sections["experience"])
            scan_text(exp_text, 0.90, "experience_section")

        # 3. Projects section scan (0.88)
        if "projects" in classified_sections:
            proj_text = "\n".join(classified_sections["projects"])
            scan_text(proj_text, 0.88, "projects_section")

        # 4. Summary section scan (0.85)
        if "summary" in classified_sections:
            summ_text = "\n".join(classified_sections["summary"])
            scan_text(summ_text, 0.85, "summary_section")

        # 5. Full text fallback scan (0.80)
        scan_text(full_text, 0.80, "full_text_heuristic")

        return list(extracted.values())


skills_taxonomy_extractor = SkillsTaxonomyExtractor()
