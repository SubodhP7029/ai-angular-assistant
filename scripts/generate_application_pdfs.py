from __future__ import annotations

import os
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=18,
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#333333"),
            spaceAfter=10,
        ),
        "h": ParagraphStyle(
            "h",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#111827"),
        ),
        "p": ParagraphStyle(
            "p",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=12,
            textColor=colors.HexColor("#111827"),
        ),
        "p_small": ParagraphStyle(
            "p_small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.0,
            leading=11,
            textColor=colors.HexColor("#111827"),
        ),
        "muted": ParagraphStyle(
            "muted",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.0,
            leading=11,
            textColor=colors.HexColor("#374151"),
        ),
    }


def _header_block(styles, name: str, title: str, contact_line: str):
    return [
        Paragraph(name, styles["title"]),
        Paragraph(f"<b>{title}</b>", styles["subtitle"]),
        Paragraph(contact_line, styles["muted"]),
        Spacer(1, 8),
    ]


def _section_title(styles, text: str):
    return [Paragraph(text, styles["h"])]


def _bullets(styles, items: list[str], font="p_small"):
    lf = ListFlowable(
        [
            ListItem(Paragraph(item, styles[font]), leftIndent=10, value="bullet")
            for item in items
        ],
        bulletType="bullet",
        leftIndent=14,
        bulletFontName="Helvetica",
        bulletFontSize=8,
        bulletOffsetY=1,
    )
    return [lf]


def build_resume_pdf(out_path: str):
    styles = _styles()

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title="Subodh Patil - Resume",
        author="Subodh Raghunath Patil",
    )

    name = "Subodh Raghunath Patil"
    role_title = "Senior Frontend Engineer | Angular | AI-Powered Applications"
    contact_line = (
        "Pune, India | +91-8149488965 | subodhpatil10@gmail.com | "
        "LinkedIn: linkedin.com/in/subodh-patil-56b691196"
    )

    tailored_summary = (
        "I’m a senior frontend engineer with 8+ years of experience building clean, responsive, "
        "and reusable UI components with expert-level HTML, CSS/SCSS, and JavaScript/TypeScript, "
        "primarily in Angular. I translate design files into accessible, high-performance interfaces, "
        "integrate UI with APIs for dynamic experiences, and troubleshoot complex frontend issues end-to-end. "
        "Recently, I’ve also delivered AI-powered Angular experiences (OpenAI API integrations) that improve "
        "user workflows through chat and smart search."
    )

    skills = (
        "Angular, TypeScript, JavaScript, HTML5, CSS3, SCSS, RxJS, REST APIs, "
        "Reusable Components, Lazy Loading, State Management, Performance Optimization, "
        "Accessibility-minded UI, Git, Agile/Scrum, Jira, Postman, OpenAI API, LLM Integration"
    )

    story = []
    story += _header_block(styles, name, role_title, contact_line)

    story += _section_title(styles, "Summary (Tailored)")
    story += [Paragraph(tailored_summary, styles["p"])]

    story += _section_title(styles, "Core Skills")
    story += [Paragraph(skills, styles["p"])]

    story += _section_title(styles, "Experience")
    story += [
        Paragraph("<b>Consultant</b> — Hoonar Tekwurks Consulting (2022–Present)", styles["p"]),
        *_bullets(
            styles,
            [
                "Built Angular applications with responsive UI, reusable components, and API integrations for data-driven experiences.",
                "Implemented chatbot UIs and OpenAI API integrations to support intelligent assistance workflows.",
                "Collaborated with designers and backend teams to deliver integrated, high-quality UI modules.",
            ],
        ),
        Spacer(1, 4),
        Paragraph("<b>Software Engineer</b> — Angular Minds (2021–2022)", styles["p"]),
        *_bullets(
            styles,
            [
                "Delivered enterprise Angular modules with modular, reusable UI components and REST API consumption.",
                "Improved performance through optimization and best practices in Angular architecture.",
            ],
        ),
        Spacer(1, 4),
        Paragraph("<b>Frontend Developer</b> — RegalarTech (2020–2021)", styles["p"]),
        *_bullets(
            styles,
            [
                "Developed responsive UI and integrated APIs; improved frontend performance and reliability.",
            ],
        ),
        Spacer(1, 4),
        Paragraph("<b>Software Engineer</b> — Datacapten Technologies (2018–2020)", styles["p"]),
        *_bullets(
            styles,
            [
                "Built dashboards and dynamic UI features for business modules with a focus on usability.",
            ],
        ),
    ]

    story += _section_title(styles, "Selected Projects")
    story += *_bullets(
        styles,
        [
            "<b>AI Smart Assistant Dashboard</b> — Angular + OpenAI API; chatbot UX, smart search, and workflow automation.",
            "<b>QuestNet BI Platform</b> — BI dashboards and enterprise reporting interfaces.",
            "<b>UBO Compliance Platform</b> — compliance dashboards and workflow-based enterprise modules.",
        ],
        font="p",
    )

    story += _section_title(styles, "Education")
    story += [
        Paragraph(
            "B.E. Computer Science — Pune Vidyarthi Griha's College of Engineering",
            styles["p"],
        )
    ]

    doc.build(story)


def build_cover_letter_pdf(out_path: str):
    styles = _styles()

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=1.9 * cm,
        rightMargin=1.9 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Subodh Patil - Cover Letter",
        author="Subodh Raghunath Patil",
    )

    today = date.today().strftime("%B %d, %Y")
    name = "Subodh Raghunath Patil"
    contact = "Pune, India | +91-8149488965 | subodhpatil10@gmail.com | linkedin.com/in/subodh-patil-56b691196"

    role = "Frontend Developer (HTML, CSS) — Contractor (Remote)"
    recipient = "Hiring Team"

    p1 = (
        f"I’m writing to apply for the {role}. With 8+ years of frontend experience, I specialize in building "
        "clean, responsive, and reusable interfaces using expert-level HTML, CSS/SCSS, and JavaScript/TypeScript—"
        "primarily with Angular. I’m excited about this opportunity because it combines real-world frontend delivery "
        "with shaping next-generation AI systems through high-quality domain input."
    )
    p2 = (
        "In my current role as a Consultant at Hoonar Tekwurks Consulting, I translate design requirements into "
        "accessible UI components, collaborate closely with designers and backend teams, and integrate front-end "
        "modules with APIs to power data-driven experiences. I’ve also delivered AI-powered Angular experiences, "
        "including chatbot UIs and OpenAI API integrations, which required careful UX, performance, and reliability "
        "considerations. Across roles, I’ve built modular component libraries, optimized performance, and debugged "
        "complex issues in production-facing applications."
    )
    p3 = (
        "I’d welcome the chance to discuss how my frontend expertise—especially in UI component quality, responsiveness, "
        "and collaboration—can contribute to your training workflows and product outcomes. Thank you for your time and "
        "consideration."
    )

    story = []

    # Header table for a clean look
    header = Table(
        [[Paragraph(f"<b>{name}</b>", styles["p"]), Paragraph(today, styles["p"])]],
        colWidths=[11.5 * cm, 4.0 * cm],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.HexColor("#E5E7EB")),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ]
        )
    )
    story.append(header)
    story.append(Spacer(1, 8))
    story.append(Paragraph(contact, styles["muted"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph(f"{recipient},", styles["p"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(p1, styles["p"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(p2, styles["p"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(p3, styles["p"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Sincerely,", styles["p"]))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>Subodh Patil</b>", styles["p"]))
    story.append(Paragraph("+91-8149488965 | subodhpatil10@gmail.com", styles["muted"]))

    doc.build(story)


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(root, "output")
    os.makedirs(out_dir, exist_ok=True)

    resume_path = os.path.join(out_dir, "Subodh_Patil_Resume.pdf")
    cover_path = os.path.join(out_dir, "Subodh_Patil_Cover_Letter.pdf")

    build_resume_pdf(resume_path)
    build_cover_letter_pdf(cover_path)

    print(f"Wrote: {resume_path}")
    print(f"Wrote: {cover_path}")


if __name__ == "__main__":
    main()

