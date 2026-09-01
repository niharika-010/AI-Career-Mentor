import re
from typing import Dict, List
from app.schemas.resume_intelligence import AchievementItem


class AchievementExtractor:
    """Extracts candidate awards, honors, and key accomplishments."""

    def extract(self, classified_sections: Dict[str, List[str]], full_text: str) -> List[AchievementItem]:
        ach_lines = classified_sections.get("achievements", [])
        if not ach_lines:
            lines = full_text.split("\n")
            ach_lines = [l.strip() for l in lines if any(w in l.lower() for w in ["award", "awarded", "first place", "winner", "hackathon", "dean's list", "honor"])]

        if not ach_lines:
            return []

        achievements: List[AchievementItem] = []
        for line in ach_lines:
            stripped = line.strip()
            if not stripped or len(stripped) < 5:
                continue

            clean_title = re.sub(r"^[•\-\*]\s*", "", stripped)
            date_match = re.search(r"\b(19\d{2}|20\d{2})\b", clean_title)
            ach_date = date_match.group(1) if date_match else None

            achievements.append(
                AchievementItem(
                    title=clean_title,
                    description=None,
                    date=ach_date,
                    confidence=0.88,
                    source="achievements_section",
                )
            )

        return achievements[:6]


achievement_extractor = AchievementExtractor()
