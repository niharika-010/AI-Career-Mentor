import re
from typing import Dict, Any, List, Tuple


class ClaimValidator:
    """Validates generated explanations against deterministic scores and extracted evidence to block contradictions and unsupported claims."""

    SCORE_CONTRADICTIONS = {
        "high_score_prohibited": [
            "unqualified", "poor fit", "no matching skills", "completely missing",
            "fails requirement", "zero experience", "unusable format"
        ],
        "low_score_prohibited": [
            "perfect candidate", "flawless fit", "exceeds all requirements",
            "100% match", "completely qualified", "ideal fit"
        ]
    }

    def validate_explanation(
        self,
        explanation_text: str,
        score: float,
        evidence_list: List[str],
        allowed_tokens: List[str] = None,
    ) -> Tuple[bool, str, List[str]]:
        """Validates that explanation text aligns with score and contains no unsupported claims.
        Returns (is_valid, sanitized_text, list_of_violations).
        """
        violations: List[str] = []
        text_lower = explanation_text.lower()

        # 1. Non-contradiction check
        if score >= 80.0:
            for term in self.SCORE_CONTRADICTIONS["high_score_prohibited"]:
                if term in text_lower:
                    violations.append(f"Contradiction: High score ({score:.1f}) contains negative claim '{term}'.")
        elif score < 60.0:
            for term in self.SCORE_CONTRADICTIONS["low_score_prohibited"]:
                if term in text_lower:
                    violations.append(f"Contradiction: Low score ({score:.1f}) contains exaggerated positive claim '{term}'.")

        # 2. Unsupported Skill Claim Validation
        if allowed_tokens:
            # Look for technical capital words or tech terms mentioned in text
            evidence_str = " ".join(evidence_list).lower()
            tokens_str = " ".join(allowed_tokens).lower()

            words = re.findall(r'\b[A-Za-z0-9+#\.-]{3,}\b', explanation_text)
            for w in words:
                w_lower = w.lower()
                # If word looks like a technical keyword but is nowhere in evidence or allowed tokens, flag it
                if w_lower in ["kubernetes", "aws", "gcp", "azure", "docker", "python", "react", "graphql", "tensorflow", "pytorch"]:
                    if w_lower not in evidence_str and w_lower not in tokens_str:
                        violations.append(f"Unsupported Claim: Technical term '{w}' mentioned in explanation but missing from extracted evidence.")

        sanitized_text = explanation_text
        if violations:
            # Fallback to grounded evidence text if violations exist
            sanitized_text = f"Evaluated Score: {score:.1f}/100. Grounded Evidence: " + " | ".join(evidence_list[:2])

        is_valid = len(violations) == 0
        return is_valid, sanitized_text, violations


claim_validator = ClaimValidator()
