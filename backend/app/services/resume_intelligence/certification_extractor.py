import re
from typing import Dict, List, Optional
from app.schemas.resume_intelligence import CertificationItem


class CertificationExtractor:
    """Extracts candidate certifications and licensing details."""

    KNOWN_ISSUERS = [
        "AWS", "Amazon Web Services", "Google Cloud", "GCP", "Microsoft", "Azure",
        "Scrum.org", "Scrum Alliance", "PMI", "CompTIA", "Oracle", "Cisco", "Kubernetes", "CNCF"
    ]

    YEAR_REGEX = r"\b(19\d{2}|20\d{2})\b"

    def extract(self, classified_sections: Dict[str, List[str]], full_text: str) -> List[CertificationItem]:
        cert_lines = classified_sections.get("certifications", [])
        if not cert_lines:
            lines = full_text.split("\n")
            cert_lines = [l.strip() for l in lines if any(w in l.lower() for w in ["certified", "certification", "aws certified", "pmp", "scrum master"])]

        if not cert_lines:
            return []

        certifications: List[CertificationItem] = []
        for line in cert_lines:
            stripped = line.strip()
            if not stripped or len(stripped) < 5:
                continue

            clean_name = re.sub(r"^[•\-\*]\s*", "", stripped)
            
            # Issuer detection
            issuer = None
            for iss in self.KNOWN_ISSUERS:
                if re.search(r"\b" + re.escape(iss) + r"\b", clean_name, re.IGNORECASE):
                    issuer = iss
                    break

            # Date detection
            date_match = re.search(self.YEAR_REGEX, clean_name)
            issue_date = date_match.group(1) if date_match else None

            certifications.append(
                CertificationItem(
                    name=clean_name,
                    issuer=issuer,
                    date=issue_date,
                    confidence=0.90 if issuer else 0.82,
                    source="certifications_section",
                )
            )

        return certifications[:6]


certification_extractor = CertificationExtractor()
