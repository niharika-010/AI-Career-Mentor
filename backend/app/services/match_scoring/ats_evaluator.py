import re
from typing import Dict, Any, Tuple


class ATSEvaluator:
    """Evaluates ATS formatting readability, section compliance, and contact info completeness."""

    STANDARD_SECTIONS = ["summary", "skills", "experience", "education", "projects"]

    def calculate_ats_score(
        self, raw_text: str, resume_intelligence: Dict[str, Any]
    ) -> Tuple[float, str]:
        score = 0.0
        reasons = []

        # 1. Contact Information Completeness (25 pts)
        contact = resume_intelligence.get("contact", {})
        contact_pts = 0
        if contact.get("name", {}).get("value"):
            contact_pts += 7
        if contact.get("email", {}).get("value"):
            contact_pts += 7
        if contact.get("phone", {}).get("value"):
            contact_pts += 6
        if contact.get("linkedin_url", {}).get("value") or contact.get("github_url", {}).get("value"):
            contact_pts += 5

        score += contact_pts
        reasons.append(f"Contact Completeness: {contact_pts}/25 pts")

        # 2. Standard Section Headers (25 pts)
        sections = resume_intelligence.get("sections", {})
        if not sections and raw_text:
            text_lower = raw_text.lower()
            found_count = sum(1 for s in self.STANDARD_SECTIONS if s in text_lower)
            sec_pts = round((found_count / len(self.STANDARD_SECTIONS)) * 25, 1)
        else:
            sec_pts = 25.0 if len(sections) >= 4 else round(len(sections) * 6.0, 1)

        score += sec_pts
        reasons.append(f"Section Structure: {sec_pts}/25 pts")

        # 3. Text Length & Formatting (25 pts)
        word_count = len(raw_text.split()) if raw_text else 0
        if 200 <= word_count <= 1500:
            len_pts = 25.0
        elif 100 <= word_count < 200 or 1500 < word_count <= 2500:
            len_pts = 18.0
        else:
            len_pts = 10.0

        score += len_pts
        reasons.append(f"Length & Formatting: {len_pts}/25 pts")

        # 4. Action Bullets & Structure (25 pts)
        bullet_lines = [l for l in raw_text.split("\n") if l.strip().startswith(("•", "-", "*", "–")) or len(l.strip()) > 30]
        if len(bullet_lines) >= 6:
            bullet_pts = 25.0
        elif len(bullet_lines) >= 3:
            bullet_pts = 18.0
        else:
            bullet_pts = 10.0

        score += bullet_pts
        reasons.append(f"Bullet Structure: {bullet_pts}/25 pts")

        final_ats_score = min(100.0, max(0.0, round(score, 1)))
        explanation = " | ".join(reasons)

        return final_ats_score, explanation


ats_evaluator = ATSEvaluator()
