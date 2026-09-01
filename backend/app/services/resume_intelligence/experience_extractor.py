import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from app.schemas.resume_intelligence import ExperienceItem

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except ImportError:
    nlp = None


class ExperienceExtractor:
    """Extracts candidate work experience entries (Title, Company, Dates, Duration, Bullet points)."""

    TITLES = sorted([
        "Senior Software Engineer", "Software Engineer", "Full Stack Developer", "Backend Engineer",
        "Frontend Engineer", "Lead Developer", "Engineering Manager", "Data Scientist",
        "Data Engineer", "DevOps Engineer", "Cloud Architect", "Product Manager",
        "UI/UX Designer", "QA Engineer", "Systems Architect", "Solution Architect",
        "Software Developer", "Technical Lead", "Staff Engineer", "Principal Engineer",
        "Lead AI Researcher", "AI Researcher", "Research Scientist", "Machine Learning Engineer"
    ], key=len, reverse=True)

    TITLE_PATTERN = r"\b(?:Senior|Lead|Principal|Staff|Chief|Head|Manager|Director|Associate|Junior)?\s*(?:AI|ML|Data|Software|Systems|Cloud|Frontend|Backend|Full Stack|Security|Research)?\s*(?:Engineer|Developer|Researcher|Scientist|Architect|Manager|Lead|Consultant|Analyst)\b"
    DATE_RANGE_REGEX = r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|[0-1]?\d)[a-z]*[\s,./-]*(?:19|20)\d{2})\s*(?:[-–]|to)\s*(Present|Current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|[0-1]?\d)[a-z]*[\s,./-]*(?:19|20)\d{2})\b"
    YEAR_RANGE_REGEX = r"\b(19\d{2}|20\d{2})\s*(?:[-–]|to)\s*(Present|Current|19\d{2}|20\d{2})\b"

    def _calculate_months(self, start_str: str, end_str: str) -> Optional[int]:
        """Calculates total months between two date strings."""
        try:
            start_year_match = re.search(r"\b(19\d{2}|20\d{2})\b", start_str)
            if not start_year_match:
                return None
            start_year = int(start_year_match.group(1))
            start_month = 1

            if end_str.lower() in ["present", "current"]:
                end_year = datetime.now().year
                end_month = datetime.now().month
            else:
                end_year_match = re.search(r"\b(19\d{2}|20\d{2})\b", end_str)
                if not end_year_match:
                    return None
                end_year = int(end_year_match.group(1))
                end_month = 12

            months = (end_year - start_year) * 12 + (end_month - start_month) + 1
            return max(months, 1)
        except Exception:
            return None

    def extract(self, classified_sections: Dict[str, List[str]], full_text: str) -> List[ExperienceItem]:
        exp_lines = classified_sections.get("experience", [])
        if not exp_lines:
            lines = full_text.split("\n")
            exp_lines = [l.strip() for l in lines if any(w in l.lower() for w in ["developer", "engineer", "manager", "architect", "lead", "designer", "consultant", "researcher"])]

        if not exp_lines:
            return []

        entries: List[ExperienceItem] = []
        current_title: Optional[str] = None
        current_company: Optional[str] = None
        current_start: Optional[str] = None
        current_end: Optional[str] = None
        current_bullets: List[str] = []
        is_current = False

        for line in exp_lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Check if line contains a date range
            range_match = re.search(self.DATE_RANGE_REGEX, stripped, re.IGNORECASE) or re.search(self.YEAR_RANGE_REGEX, stripped, re.IGNORECASE)
            
            # Check for job title matching
            matched_title = None
            for t in self.TITLES:
                if re.search(r"\b" + re.escape(t) + r"\b", stripped, re.IGNORECASE):
                    matched_title = t
                    break

            if not matched_title:
                title_match = re.search(self.TITLE_PATTERN, stripped, re.IGNORECASE)
                if title_match:
                    matched_title = title_match.group(0).strip().title()

            # Pipe separator check for "Title | Company"
            if "|" in stripped:
                parts = [p.strip() for p in stripped.split("|") if p.strip()]
                if len(parts) >= 2:
                    is_p0_date = bool(re.search(self.DATE_RANGE_REGEX, parts[0], re.IGNORECASE) or re.search(self.YEAR_RANGE_REGEX, parts[0], re.IGNORECASE))
                    if not matched_title and not is_p0_date and len(parts[0]) < 40:
                        matched_title = parts[0]
                    
                    is_p1_date_or_loc = bool(re.search(self.DATE_RANGE_REGEX, parts[1], re.IGNORECASE) or re.search(self.YEAR_RANGE_REGEX, parts[1], re.IGNORECASE))
                    if not is_p1_date_or_loc and len(parts[1]) < 40:
                        if not any(loc in parts[1].lower() for loc in ["san francisco", "san jose", "boston", "ny", "ca", "ma", "usa"]):
                            current_company = parts[1]

            if range_match or matched_title:
                is_new_entry = False
                if matched_title and current_title and matched_title != current_title:
                    is_new_entry = True
                elif range_match and current_start:
                    is_new_entry = True

                # Flush previous entry if new title or new date range found
                if is_new_entry and (current_title or current_company):
                    duration = self._calculate_months(current_start or "2020", current_end or "Present") if current_start else None
                    entries.append(
                        ExperienceItem(
                            job_title=current_title or "Software Professional",
                            company=current_company or "Enterprise Organization",
                            start_date=current_start,
                            end_date=current_end,
                            is_current=is_current,
                            duration_months=duration,
                            responsibilities=current_bullets[:6],
                            confidence=0.88,
                            source="experience_section",
                        )
                    )
                    current_bullets = []
                    current_title = None
                    current_company = None
                    current_start = None
                    current_end = None
                    is_current = False

                if matched_title:
                    current_title = matched_title

                if range_match:
                    current_start = range_match.group(1)
                    current_end = range_match.group(2)
                    is_current = current_end.lower() in ["present", "current"]

                # Extract company using spaCy ORG or separator heuristic
                if not current_company:
                    at_match = re.search(r"\b(?:at|@|,)\s+([A-Z][A-Za-z0-9\s&]{2,30})\b", stripped)
                    if at_match:
                        current_company = at_match.group(1).strip()
                    elif nlp:
                        doc = nlp(stripped)
                        for ent in doc.ents:
                            if ent.label_ == "ORG" and ent.text.strip().lower() not in [t.lower() for t in self.TITLES]:
                                current_company = ent.text.strip()
                                break

            elif stripped.startswith(("•", "-", "*", "–")) or len(stripped) > 20:
                clean_bullet = re.sub(r"^[•\-\*–]\s*", "", stripped)
                if len(clean_bullet) > 10:
                    current_bullets.append(clean_bullet)

        # Flush final entry
        if current_title or current_company or current_bullets:
            duration = self._calculate_months(current_start or "2020", current_end or "Present") if current_start else None
            entries.append(
                ExperienceItem(
                    job_title=current_title or "Software Professional",
                    company=current_company or "Enterprise Organization",
                    start_date=current_start,
                    end_date=current_end,
                    is_current=is_current,
                    duration_months=duration,
                    responsibilities=current_bullets[:6],
                    confidence=0.88,
                    source="experience_section",
                )
            )

        return entries[:5]


experience_extractor = ExperienceExtractor()
