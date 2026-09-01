import re
from typing import Optional, Tuple


class IndustryTitleExtractor:
    """Normalizes Job Title and infers Industry classification domain."""

    INDUSTRY_TAXONOMY = [
        ("AI & Machine Learning", [r"\b(?:AI|ML|Machine Learning|Deep Learning|NLP|LLM|Data Science|PyTorch|TensorFlow)\b"]),
        ("Fintech & Payments", [r"\b(?:Fintech|Banking|Payments|Trading|Financial|Crypto|Blockchain)\b"]),
        ("Healthcare & BioTech", [r"\b(?:Healthcare|HealthTech|BioTech|Medical|HIPAA|Clinical)\b"]),
        ("Cloud & Infrastructure", [r"\b(?:Cloud Infrastructure|DevOps|Kubernetes|AWS|GCP|Azure|Site Reliability)\b"]),
        ("Cybersecurity", [r"\b(?:Cybersecurity|InfoSec|SOC|Security|Penetration Testing|Network Security)\b"]),
        ("E-Commerce & Retail", [r"\b(?:E-Commerce|Marketplace|Retail|D2C|Cart)\b"]),
        ("Software & SaaS", [r"\b(?:Software|SaaS|Web Application|Platform|Full Stack)\b"]),
    ]

    def normalize_title(self, title: Optional[str], raw_text: str) -> Tuple[str, str]:
        raw_t = title.strip() if title else ""
        
        if not raw_t:
            # Fallback to first line if title not provided
            lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
            raw_t = lines[0] if lines else "Software Professional"

        # Clean title
        clean_title = re.sub(r"\s*[\-\|@]\s*.*$", "", raw_t).strip()
        if len(clean_title) < 50:
            words = clean_title.split()
            formatted_words = []
            for w in words:
                if w.upper() in ["AI", "ML", "AWS", "GCP", "QA", "UI", "UX", "IT", "HR", "LLM", "NLP"]:
                    formatted_words.append(w.upper())
                else:
                    formatted_words.append(w.capitalize())
            clean_title = " ".join(formatted_words)
        else:
            clean_title = raw_t[:50]

        return clean_title, raw_t

    def infer_industry(self, raw_text: str) -> str:
        for industry_name, patterns in self.INDUSTRY_TAXONOMY:
            for pat in patterns:
                if re.search(pat, raw_text, re.IGNORECASE):
                    return industry_name
        return "Technology & Software"


industry_title_extractor = IndustryTitleExtractor()
