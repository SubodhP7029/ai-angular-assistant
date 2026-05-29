from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ACCENT = colors.HexColor("#2563eb")
GRAY = colors.HexColor("#6b7280")
TEXT = colors.HexColor("#111827")
HR = ACCENT


def _safe_identifier(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[^A-Za-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:40] or "Role"


def _styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "name",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=22,
            textColor=TEXT,
            spaceAfter=2,
            alignment=TA_LEFT,
        ),
        "title": ParagraphStyle(
            "title",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=ACCENT,
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "contact": ParagraphStyle(
            "contact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10,
            textColor=GRAY,
            spaceAfter=8,
            alignment=TA_LEFT,
        ),
        "h": ParagraphStyle(
            "h",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=11,
            textColor=ACCENT,
            spaceAfter=3,
            spaceBefore=8,
            alignment=TA_LEFT,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=2,
        ),
        "muted": ParagraphStyle(
            "muted",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            textColor=GRAY,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "right": ParagraphStyle(
            "right",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            textColor=TEXT,
            alignment=TA_RIGHT,
        ),
    }


def _hr_table(line_color=HR):
    t = Table([[""]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (-1, -1), 0.6, line_color),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return t


@dataclass(frozen=True)
class Candidate:
    name: str
    title: str
    location: str
    phone: str
    email: str
    linkedin: str


def build_resume_pdf(out_path: str, identifier: str, company_name: str, role_title: str):
    st = _styles()
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title=f"Resume - {company_name}",
        author="Subodh Raghunath Patil",
    )

    c = Candidate(
        name="Subodh Raghunath Patil",
        title="Senior Frontend Engineer | Angular | AI-Powered Applications",
        location="Pune, India",
        phone="+91-8149488965",
        email="subodhpatil10@gmail.com",
        linkedin="linkedin.com/in/subodh-patil-56b691196",
    )

    # Tailored to: micro1 UI Engineer (React + TypeScript)
    summary = (
        "I’m a senior frontend engineer with 8+ years of experience building scalable, responsive, and accessible "
        "web UIs using TypeScript, modern JavaScript (ES6+), HTML5, and CSS/SCSS, with deep experience in Angular and "
        "strong transferable component-driven UI architecture practices. I translate complex business requirements "
        "into user-centric interfaces, collaborate cross-functionally with product/design/backend teams, and improve "
        "performance and usability through careful debugging and optimization using Chrome DevTools. I regularly "
        "contribute through code reviews, documentation, and reusable component patterns, and I’ve built AI-powered "
        "Angular experiences (OpenAI integrations) aligned with micro1’s mission of improving next-generation AI systems."
    )

    # Skills reordered for this JD (React is a gap; don't claim it).
    skills = [
        "TypeScript",
        "JavaScript (ES6+)",
        "HTML5",
        "CSS3",
        "SCSS",
        "Responsive Design",
        "Accessibility (A11y)",
        "Reusable Components",
        "Performance Optimization",
        "State Management",
        "RxJS",
        "NgRx",
        "Git",
        "Agile/Scrum",
        "Chrome DevTools",
        "REST APIs",
        "JSON/XML",
        "Postman",
        "Angular",
        "OpenAI API / LLM Integration",
    ]

    exp = [
        {
            "company": "Hoonar Tekwurks Consulting",
            "role": "Consultant",
            "dates": "2022–Present",
            "bullets": [
                "Designed and delivered scalable, responsive UI components in Angular/TypeScript with strong HTML/CSS foundations, translating complex requirements into usable interfaces.",
                "Applied accessibility-minded UI patterns and performance optimization using Chrome DevTools profiling and targeted refactors.",
                "Integrated UI modules with REST APIs (JSON/XML), implemented RxJS reactive patterns, and debugged complex UI/UX issues across environments.",
                "Led code reviews and contributed to team documentation and standards to maintain high code quality in a fast-paced Agile environment.",
            ],
        },
        {
            "company": "Angular Minds",
            "role": "Software Engineer",
            "dates": "2021–2022",
            "bullets": [
                "Developed enterprise, modular UI architectures with reusable components, shared styling systems, and consistent UX patterns.",
                "Improved performance and maintainability through optimization, refactoring, and disciplined component boundaries.",
                "Worked within deployment workflows and team processes using Git and Agile practices.",
            ],
        },
        {
            "company": "RegalarTech",
            "role": "Frontend Developer",
            "dates": "2020–2021",
            "bullets": [
                "Delivered responsive UI screens and API integrations, focusing on usability and measurable performance improvements.",
            ],
        },
        {
            "company": "Datacapten Technologies",
            "role": "Software Engineer",
            "dates": "2018–2020",
            "bullets": [
                "Built dashboard-driven business modules with dynamic UI behavior and data visualization experiences.",
            ],
        },
    ]

    projects = [
        "AI Smart Assistant Dashboard — Angular + OpenAI API; chatbot UX, smart search, workflow automation; RxJS reactive patterns.",
        "QuestNet BI Platform — BI dashboards, enterprise reporting, real-time data visualizations.",
        "UBO Compliance Platform — compliance dashboards, role-based UI, complex state management, workflow enterprise modules.",
    ]

    story = []

    # Header
    story.append(Paragraph(c.name, st["name"]))
    story.append(Paragraph(c.title, st["title"]))
    story.append(
        Paragraph(
            f"{c.location} | {c.phone} | {c.email} | {c.linkedin}",
            st["contact"],
        )
    )

    def section(title: str):
        story.append(Paragraph(title.upper(), st["h"]))
        story.append(_hr_table())
        story.append(Spacer(1, 4))

    section("Professional Summary")
    story.append(Paragraph(summary, st["body"]))

    section("Technical Skills")
    story.append(Paragraph(", ".join(skills), st["body"]))

    section("Professional Experience")
    for e in exp:
        # Table row: role+company left, dates right
        left = Paragraph(f"<b>{e['role']}</b> — {e['company']}", st["body"])
        right = Paragraph(e["dates"], st["right"])
        t = Table([[left, right]], colWidths=[140 * mm, 30 * mm])
        t.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]
            )
        )
        story.append(t)
        for b in e["bullets"]:
            story.append(Paragraph(b, st["bullet"], bulletText="•"))
        story.append(Spacer(1, 4))

    section("Key Projects")
    for p in projects:
        story.append(Paragraph(p, st["bullet"], bulletText="•"))

    story.append(Spacer(1, 4))
    section("Education")
    story.append(
        Paragraph(
            "B.E. Computer Science — Pune Vidyarthi Griha's College of Engineering",
            st["body"],
        )
    )

    doc.build(story)


def build_cover_letter_pdf(out_path: str, identifier: str, company_name: str, role_title: str):
    st = _styles()
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"Cover Letter - {company_name}",
        author="Subodh Raghunath Patil",
    )

    c = Candidate(
        name="Subodh Raghunath Patil",
        title="Senior Frontend Engineer | Angular | AI-Powered Applications",
        location="Pune, India",
        phone="+91-8149488965",
        email="subodhpatil10@gmail.com",
        linkedin="linkedin.com/in/subodh-patil-56b691196",
    )

    today = date.today().strftime("%B %d, %Y")
    role = role_title
    company = company_name

    p1 = (
        f"I’m writing to apply for the {role} role at {company}. I bring 8+ years of experience building scalable, "
        "responsive, and accessible web interfaces with TypeScript, modern JavaScript, HTML5, and CSS/SCSS, with deep "
        "strength in component-driven UI development and performance optimization. I’m excited by this role because it "
        "focuses on robust UI architecture, usability, and high engineering standards."
    )
    p2 = (
        "In my current role at Hoonar Tekwurks Consulting, I build reusable UI components in Angular/TypeScript, "
        "translate complex requirements into user-centric interfaces, integrate with REST APIs, and troubleshoot UI/UX "
        "issues across environments. I regularly apply RxJS reactive patterns and state management to keep UI behavior "
        "predictable and scalable, and I use Chrome DevTools to diagnose performance bottlenecks. I also participate in "
        "code reviews and cross-functional Agile collaboration to maintain consistent quality and delivery."
    )
    p3 = (
        "I would welcome the opportunity to discuss how my frontend engineering experience can help you deliver "
        "high-quality, accessible, and performant UI components. Thank you for your time and consideration."
    )

    story = []

    # Letterhead
    story.append(Paragraph(c.name, st["name"]))
    story.append(_hr_table(line_color=ACCENT))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"{c.location} | {c.phone} | {c.email} | {c.linkedin}", st["contact"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph(today, st["body"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(f"Hiring Manager, {company}", st["body"]))
    story.append(Paragraph("Remote", st["muted"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph(f"<b>Re:</b> {role} — {company}", st["body"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(p1, st["body"]))
    story.append(Paragraph(p2, st["body"]))
    story.append(Paragraph(p3, st["body"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Sincerely,", st["body"]))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>Subodh Raghunath Patil</b>", st["body"]))
    story.append(
        Paragraph(
            "+91-8149488965 | subodhpatil10@gmail.com<br/>"
            "linkedin.com/in/subodh-patil-56b691196<br/>"
            "Pune, India",
            st["muted"],
        )
    )

    doc.build(story)


def main():
    company_name = "micro1"
    role_title = "UI Engineer — Contractor (Remote)"
    identifier = _safe_identifier(company_name)

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(root, "output")
    os.makedirs(out_dir, exist_ok=True)

    resume_path = os.path.join(out_dir, f"Subodh_Patil_Resume_{identifier}.pdf")
    cover_path = os.path.join(out_dir, f"Subodh_Patil_CoverLetter_{identifier}.pdf")

    build_resume_pdf(resume_path, identifier, company_name=company_name, role_title=role_title)
    build_cover_letter_pdf(cover_path, identifier, company_name=company_name, role_title=role_title)

    print(f"Wrote: {resume_path}")
    print(f"Wrote: {cover_path}")


if __name__ == "__main__":
    main()

