import pytest
from app.services.pdf_generator import pdf_report_generator

def test_pdf_generator_header_and_structure():
    pdf_bytes = pdf_report_generator.generate_report(
        candidate_name="John Doe",
        target_role="Machine Learning Engineer",
        overall_score=82.0,
        ats_score=91.0,
        confidence_score=94.0,
        selection_likelihood="STRONG MATCH",
        matched_skills=["Python", "SQL", "Machine Learning"],
        missing_skills=["Docker", "AWS"],
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    # PDF Magic Number Header Verification
    assert pdf_bytes.startswith(b"%PDF-")


def test_pdf_generator_custom_payload():
    pdf_bytes = pdf_report_generator.generate_report(
        candidate_name="Jane Smith",
        target_role="AI Engineer",
        overall_score=95.0,
        ats_score=98.0,
        confidence_score=96.0,
        selection_likelihood="VERY HIGH MATCH",
        matched_skills=["Python", "PyTorch", "FastAPI", "Docker", "LLMs"],
        missing_skills=["Kubernetes"],
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF-")
