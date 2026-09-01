import re
from typing import Dict, List, Optional
from app.schemas.resume_intelligence import ProjectItem


class ProjectExtractor:
    """Extracts candidate technical projects (Title, Description, Tech Stack, URLs)."""

    URL_REGEX = r"https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[^\s]*)?"

    def extract(self, classified_sections: Dict[str, List[str]], full_text: str) -> List[ProjectItem]:
        proj_lines = classified_sections.get("projects", [])
        if not proj_lines:
            return []

        projects: List[ProjectItem] = []
        current_title: Optional[str] = None
        current_desc_lines: List[str] = []
        current_url: Optional[str] = None

        for line in proj_lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Check if line contains a URL
            url_match = re.search(self.URL_REGEX, stripped)
            if url_match and not current_url:
                current_url = url_match.group(0)

            # Heuristic for project header: Short title line or bold/dash separator
            if len(stripped) < 50 and not stripped.startswith(("•", "-", "*")) and not current_title:
                current_title = stripped.rstrip(":")
            elif stripped.startswith(("•", "-", "*")) or len(stripped) > 20:
                clean_line = re.sub(r"^[•\-\*]\s*", "", stripped)
                current_desc_lines.append(clean_line)

            if len(current_desc_lines) >= 3 and current_title:
                projects.append(
                    ProjectItem(
                        title=current_title,
                        description=" ".join(current_desc_lines),
                        url=current_url,
                        confidence=0.88,
                        source="projects_section",
                    )
                )
                current_title = None
                current_desc_lines = []
                current_url = None

        if current_title or current_desc_lines:
            projects.append(
                ProjectItem(
                    title=current_title or "Portfolio Project",
                    description=" ".join(current_desc_lines) if current_desc_lines else "Candidate personal software project.",
                    url=current_url,
                    confidence=0.85,
                    source="projects_section",
                )
            )

        return projects[:5]


project_extractor = ProjectExtractor()
