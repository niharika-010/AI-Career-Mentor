import re
from typing import Dict, List, Tuple
from app.schemas.job_intelligence import RequirementItem
from app.services.job_intelligence.requirement_classifier import requirement_classifier


class SkillsTechExtractor:
    """Extracts Skills, Technologies, Tools, Soft Skills, Technical Keywords, and Responsibilities with exact source_text snippets."""

    TECHNOLOGIES = [
        "Python", "JavaScript", "TypeScript", "C++", "C#", "Java", "Go", "Golang", "Rust",
        "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R", "SQL", "HTML", "CSS",
        "React", "Next.js", "Vue", "Angular", "Node.js", "Express", "FastAPI", "Django",
        "Flask", "Spring Boot", ".NET", "PostgreSQL", "MySQL", "MongoDB", "Redis",
        "Elasticsearch", "Cassandra", "DynamoDB", "SQLite", "Snowflake", "BigQuery",
        "AWS", "GCP", "Azure", "Docker", "Kubernetes", "PyTorch", "TensorFlow"
    ]

    TOOLS = [
        "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence", "Postman",
        "Swagger", "Jenkins", "Terraform", "Ansible", "Helm", "Prometheus", "Grafana",
        "Figma", "VS Code", "Webpack", "Vite"
    ]

    TECHNICAL_KEYWORDS = [
        "REST API", "GraphQL", "Microservices", "System Design", "CI/CD", "TDD",
        "Agile", "Scrum", "DevOps", "Serverless", "Event-Driven Architecture",
        "Distributed Systems", "Object-Oriented Programming", "Machine Learning",
        "Natural Language Processing", "NLP", "LLM", "RAG", "Data Pipelines", "ETL"
    ]

    SOFT_SKILLS = [
        "Leadership", "Team Leadership", "Communication", "Collaboration",
        "Problem Solving", "Critical Thinking", "Mentorship", "Stakeholder Management",
        "Agile", "Time Management", "Adaptability", "Conflict Resolution"
    ]

    def _find_snippet_containing_word(self, word: str, lines: List[str]) -> str:
        """Finds exact line in JD text containing the extracted word for source_text attribution."""
        pattern = r"\b" + re.escape(word.upper()) + r"\b"
        for line in lines:
            if re.search(pattern, line.upper()):
                return line.strip()
        return f"Requirement specified for {word}"

    def extract(self, classified_sections: Dict[str, List[str]], raw_text: str) -> Tuple[
        List[RequirementItem],  # required_skills
        List[RequirementItem],  # preferred_skills
        List[RequirementItem],  # responsibilities
        List[RequirementItem],  # technical_keywords
        List[RequirementItem],  # soft_skills
        List[RequirementItem],  # tools
        List[RequirementItem]   # technologies
    ]:
        all_lines = [l.strip() for l in raw_text.split("\n") if l.strip()]

        required_skills: List[RequirementItem] = []
        preferred_skills: List[RequirementItem] = []
        responsibilities: List[RequirementItem] = []
        technical_keywords: List[RequirementItem] = []
        soft_skills: List[RequirementItem] = []
        tools: List[RequirementItem] = []
        technologies: List[RequirementItem] = []

        seen_skills = set()

        # 1. Responsibilities Extraction
        resp_lines = classified_sections.get("responsibilities", [])
        for line in resp_lines:
            clean_resp = re.sub(r"^[•\-\*]\s*", "", line).strip()
            if len(clean_resp) > 15:
                responsibilities.append(
                    RequirementItem(
                        name=clean_resp[:150],
                        category="responsibility",
                        requirement_type="required",
                        confidence=0.92,
                        source_text=line,
                    )
                )

        pref_lines = classified_sections.get("preferred_qualifications", [])
        pref_text = "\n".join(pref_lines).lower()

        # 2. Extract Technologies
        for tech in self.TECHNOLOGIES:
            pattern = r"(?<![A-Za-z0-9_#+])" + re.escape(tech.upper()) + r"(?![A-Za-z0-9_#+])"
            if re.search(pattern, raw_text.upper()):
                snippet = self._find_snippet_containing_word(tech, all_lines)
                
                # Check if tech appears in preferred section
                in_pref_section = bool(re.search(pattern, pref_text))
                req_type = "preferred" if in_pref_section else requirement_classifier.classify_requirement(snippet)

                item = RequirementItem(
                    name=tech,
                    category="technology",
                    requirement_type=req_type,
                    confidence=0.95,
                    source_text=snippet,
                )
                technologies.append(item)

                if tech not in seen_skills:
                    seen_skills.add(tech)
                    if req_type == "required":
                        required_skills.append(item)
                    else:
                        preferred_skills.append(item)

        # 3. Extract Tools
        for tool in self.TOOLS:
            pattern = r"\b" + re.escape(tool.upper()) + r"\b"
            if re.search(pattern, raw_text.upper()):
                snippet = self._find_snippet_containing_word(tool, all_lines)
                in_pref_section = bool(re.search(pattern, pref_text))
                req_type = "preferred" if in_pref_section else requirement_classifier.classify_requirement(snippet)

                item = RequirementItem(
                    name=tool,
                    category="tool",
                    requirement_type=req_type,
                    confidence=0.92,
                    source_text=snippet,
                )
                tools.append(item)

                if tool not in seen_skills:
                    seen_skills.add(tool)
                    if req_type == "required":
                        required_skills.append(item)
                    else:
                        preferred_skills.append(item)

        # 4. Extract Technical Keywords
        for kw in self.TECHNICAL_KEYWORDS:
            pattern = r"\b" + re.escape(kw.upper()) + r"\b"
            if re.search(pattern, raw_text.upper()):
                snippet = self._find_snippet_containing_word(kw, all_lines)
                req_type = requirement_classifier.classify_requirement(snippet)

                item = RequirementItem(
                    name=kw,
                    category="keyword",
                    requirement_type=req_type,
                    confidence=0.90,
                    source_text=snippet,
                )
                technical_keywords.append(item)

        # 5. Extract Soft Skills
        for soft in self.SOFT_SKILLS:
            pattern = r"\b" + re.escape(soft.upper()) + r"\b"
            if re.search(pattern, raw_text.upper()):
                snippet = self._find_snippet_containing_word(soft, all_lines)
                req_type = requirement_classifier.classify_requirement(snippet)

                item = RequirementItem(
                    name=soft,
                    category="soft_skill",
                    requirement_type=req_type,
                    confidence=0.88,
                    source_text=snippet,
                )
                soft_skills.append(item)

        return (
            required_skills,
            preferred_skills,
            responsibilities[:10],
            technical_keywords,
            soft_skills,
            tools,
            technologies,
        )


skills_tech_extractor = SkillsTechExtractor()
