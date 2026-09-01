import io
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

logger = logging.getLogger("app.services.pdf_generator")

class PDFReportGenerator:
    """Generates professional, multi-page PDF Resume Analysis Reports using ReportLab."""

    def generate_report(
        self,
        candidate_name: str = "John Doe",
        target_role: str = "Machine Learning Engineer",
        overall_score: float = 82.0,
        ats_score: float = 91.0,
        confidence_score: float = 94.0,
        selection_likelihood: str = "STRONG MATCH",
        matched_skills: Optional[List[str]] = None,
        missing_skills: Optional[List[str]] = None,
        strengths: Optional[List[str]] = None,
        weaknesses: Optional[List[str]] = None,
        recommended_actions: Optional[List[str]] = None,
        interview_questions: Optional[List[Dict[str, Any]]] = None,
        weekly_roadmap: Optional[List[Dict[str, Any]]] = None,
    ) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#4F46E5"),
            alignment=TA_LEFT,
            fontName="Helvetica-Bold",
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#64748B"),
            alignment=TA_LEFT,
            fontName="Helvetica-Bold",
        )
        h2_style = ParagraphStyle(
            "Heading2Custom",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1E293B"),
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "BodyCustom",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#334155"),
            fontName="Helvetica",
        )
        badge_style = ParagraphStyle(
            "BadgeStyle",
            parent=styles["Normal"],
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#047857"),
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        )

        story = []

        # 1. Header & Title Block
        story.append(Paragraph("AI CAREER ASSISTANT", subtitle_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph("Resume Analysis Report", title_style))
        story.append(Spacer(1, 10))

        # Metadata Table
        meta_data = [
            [
                Paragraph("<b>Candidate Name:</b>", body_style),
                Paragraph(candidate_name, body_style),
                Paragraph("<b>Date:</b>", body_style),
                Paragraph(datetime.now().strftime("%B %d, %Y"), body_style),
            ],
            [
                Paragraph("<b>Target Role:</b>", body_style),
                Paragraph(target_role, body_style),
                Paragraph("<b>Report Status:</b>", body_style),
                Paragraph("Final Evaluation", body_style),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[100, 180, 80, 180])
        meta_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(meta_table)
        story.append(Spacer(1, 12))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=12))

        # 2. Key Metrics & Selection Likelihood Box
        metrics_data = [
            [
                Paragraph("<font size=8 color='#64748B'><b>OVERALL MATCH</b></font>", body_style),
                Paragraph("<font size=8 color='#64748B'><b>ATS SCORE</b></font>", body_style),
                Paragraph("<font size=8 color='#64748B'><b>CONFIDENCE</b></font>", body_style),
                Paragraph("<font size=8 color='#64748B'><b>SELECTION LIKELIHOOD</b></font>", body_style),
            ],
            [
                Paragraph(f"<font size=18 color='#4F46E5'><b>{int(overall_score)}/100</b></font>", body_style),
                Paragraph(f"<font size=18 color='#059669'><b>{int(ats_score)}/100</b></font>", body_style),
                Paragraph(f"<font size=18 color='#D97706'><b>{int(confidence_score)}/100</b></font>", body_style),
                Paragraph(f"<b>{selection_likelihood}</b>", badge_style),
            ],
        ]
        metrics_table = Table(metrics_data, colWidths=[130, 130, 130, 150])
        metrics_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF2FF")),
                ("BOX", (0, 0), (-1, -1), 1.5, colors.HexColor("#6366F1")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(metrics_table)
        story.append(Spacer(1, 14))

        # 3. Skills Analysis Section
        story.append(Paragraph("Skills Analysis", h2_style))
        m_skills = matched_skills or ["Python", "SQL", "Machine Learning", "FastAPI"]
        g_skills = missing_skills or ["Docker", "AWS", "Kubernetes"]

        matched_str = " &nbsp;&nbsp;&nbsp; ".join([f"<font color='#059669'><b>&#10004;</b> {s}</font>" for s in m_skills])
        missing_str = " &nbsp;&nbsp;&nbsp; ".join([f"<font color='#DC2626'><b>&#9888;</b> {s}</font>" for s in g_skills])

        skills_data = [
            [Paragraph("<b>Matched Skills:</b>", body_style), Paragraph(matched_str, body_style)],
            [Paragraph("<b>Missing Skills:</b>", body_style), Paragraph(missing_str, body_style)],
        ]
        skills_table = Table(skills_data, colWidths=[110, 430])
        skills_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        story.append(skills_table)
        story.append(Spacer(1, 14))

        # 4. Strengths & Weaknesses
        story.append(Paragraph("Strengths & Areas for Improvement", h2_style))
        s_list = strengths or [
            "Strong core proficiency in Python and statistical machine learning.",
            "Verified degree alignment in Computer Science & AI.",
            "Solid experience designing RESTful APIs.",
        ]
        w_list = weaknesses or [
            "Lacks explicit production Docker containerization experience.",
            "Cloud deployment (AWS/GCP) skills are missing from target JD requirements.",
        ]

        strengths_formatted = "<br/>".join([f"&bull; {s}" for s in s_list])
        weaknesses_formatted = "<br/>".join([f"&bull; {w}" for w in w_list])

        sw_data = [
            [Paragraph("<b>Key Strengths</b>", body_style), Paragraph("<b>Key Areas for Improvement</b>", body_style)],
            [Paragraph(strengths_formatted, body_style), Paragraph(weaknesses_formatted, body_style)],
        ]
        sw_table = Table(sw_data, colWidths=[270, 270])
        sw_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#D1FAE5")),
                ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FEE2E2")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FAFAFA")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        story.append(sw_table)
        story.append(Spacer(1, 14))

        # 5. Recommended Actions
        story.append(Paragraph("Recommended Actions", h2_style))
        actions = recommended_actions or [
            "Complete a 1-week Docker containerization course and add a containerized ML API project.",
            "Deploy the containerized FastAPI endpoint on AWS EC2/ECS.",
            "Highlight quantified throughput performance metrics in experience bullet points.",
        ]
        actions_formatted = "<br/>".join([f"<b>{i+1}.</b> {act}" for i, act in enumerate(actions)])
        story.append(Paragraph(actions_formatted, body_style))
        story.append(Spacer(1, 14))

        # 6. Interview Preparation Questions
        story.append(Paragraph("Targeted Interview Preparation", h2_style))
        i_questions = interview_questions or [
            {
                "q": "Explain how you would deploy a machine learning model into production.",
                "cat": "Technical",
                "diff": "Intermediate",
                "why": "The JD requires ML deployment experience.",
            },
            {
                "q": "Describe a situation where you resolved a critical production bug under tight deadline pressure.",
                "cat": "Behavioral",
                "diff": "Intermediate",
                "why": "Assesses incident management and communication.",
            },
        ]
        iq_rows: List[List[Any]] = [["#", "Category", "Difficulty", "Question & Rationale"]]
        for idx, item in enumerate(i_questions):
            q_text = item.get("q") or item.get("question", "")
            cat = item.get("cat") or item.get("category", "General")
            diff = item.get("diff") or item.get("difficulty", "Intermediate")
            why = item.get("why") or item.get("why_this_question", "")
            content = f"<b>{q_text}</b><br/><font color='#64748B'><i>Why: {why}</i></font>"
            iq_rows.append([str(idx + 1), cat, diff, Paragraph(content, body_style)])

        iq_table = Table(iq_rows, colWidths=[25, 80, 80, 355])
        iq_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        story.append(iq_table)
        story.append(Spacer(1, 14))

        # 7. Skill Gap Roadmap
        story.append(Paragraph("4-Week Skill Gap Roadmap", h2_style))
        roadmap_steps = weekly_roadmap or [
            {"week": 1, "title": "Docker Fundamentals", "milestone": "Dockerized Microservice Sandbox"},
            {"week": 2, "title": "AWS Basics & EC2", "milestone": "AWS Staging Environment"},
            {"week": 3, "title": "Deploy ML API on Cloud", "milestone": "Automated Cloud API"},
            {"week": 4, "title": "Docker + AWS Capstone", "milestone": "Complete Capstone Integration"},
        ]
        rm_rows: List[List[Any]] = [["Week", "Milestone Focus Title", "Target Milestone Goal"]]
        for step in roadmap_steps:
            w_num = f"Week {step.get('week', step.get('week_number', 1))}"
            title = step.get("title", "")
            m_goal = step.get("milestone", step.get("project_milestone", ""))
            rm_rows.append([w_num, title, m_goal])

        rm_table = Table(rm_rows, colWidths=[70, 230, 240])
        rm_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3E8FF")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8B4FE")),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(rm_table)

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

pdf_report_generator = PDFReportGenerator()
