# -*- coding: utf-8 -*-
"""Generate tailored resume + cover letter PDFs from JSON config (Job Application Hub)."""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

NAVY = colors.HexColor("#0f2d55")
BLUE = colors.HexColor("#2563eb")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748b")

BULLET = "\u2022"

CANDIDATE = {
    "name": "Subodh Raghunath Patil",
    "title": "Senior Frontend Engineer | Angular | AI-Powered Applications",
    "location": "Pune, India",
    "phone": "+91-8149488965",
    "email": "subodhpatil10@gmail.com",
    "linkedin": "linkedin.com/in/subodh-patil-56b691196",
}


def _safe_id(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s.strip())
    return re.sub(r"_+", "_", s).strip("_")[:40] or "Role"


def _styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "name",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=26,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=4,
        ),
        "title": ParagraphStyle(
            "title",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BLUE,
            spaceAfter=5,
        ),
        "contact": ParagraphStyle(
            "contact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=MUTED,
            spaceAfter=6,
        ),
        "h": ParagraphStyle(
            "h",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=14,
            textColor=NAVY,
            spaceAfter=3,
            spaceBefore=8,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=14,
            textColor=SLATE,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=14,
            textColor=SLATE,
            alignment=TA_JUSTIFY,
            leftIndent=12,
            spaceAfter=2,
        ),
        "right": ParagraphStyle(
            "right",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=14,
            textColor=SLATE,
            alignment=TA_RIGHT,
        ),
        "skill_label": ParagraphStyle(
            "skill_label",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.8,
            leading=13,
            textColor=NAVY,
        ),
        "skill_val": ParagraphStyle(
            "skill_val",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=13,
            textColor=SLATE,
        ),
    }


def _section_hr():
    t = Table([[""]], colWidths=["100%"])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1.2, NAVY)]))
    return t


def _header_block(st, story):
    story.append(Paragraph(CANDIDATE["name"], st["name"]))
    story.append(Paragraph(CANDIDATE["title"], st["title"]))
    story.append(
        Paragraph(
            f"{CANDIDATE['location']} | {CANDIDATE['phone']} | {CANDIDATE['email']} | {CANDIDATE['linkedin']}",
            st["contact"],
        )
    )
    t1 = Table([[""]], colWidths=["100%"])
    t1.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1.2, NAVY)]))
    story.append(t1)
    t2 = Table([[""]], colWidths=["100%"])
    t2.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, BLUE)]))
    story.append(t2)
    story.append(Spacer(1, 6))


def _section(st, story, title: str):
    story.append(Paragraph(title.upper(), st["h"]))
    story.append(_section_hr())
    story.append(Spacer(1, 4))


DEFAULT_EXP = [
    {
        "role": "Consultant",
        "company": "Hoonar Tekwurks Consulting",
        "dates": "2022-Present",
        "bullets": [
            "Built Angular/TypeScript apps with reusable component libraries, RxJS/NgRx, and REST API integrations.",
            "Delivered AI chatbot UIs and OpenAI API integrations; improved workflows via smart search and automation.",
            "Optimized performance (lazy loading, OnPush, bundle splitting) and led code reviews in Agile teams.",
        ],
    },
    {
        "role": "Software Engineer",
        "company": "Angular Minds",
        "dates": "2021-2022",
        "bullets": [
            "Developed enterprise Angular modules with reusable components and CI/CD deployment workflows.",
            "Reduced technical debt and improved performance through refactoring and optimization.",
        ],
    },
    {
        "role": "Frontend Developer",
        "company": "RegalarTech",
        "dates": "2020-2021",
        "bullets": [
            "Delivered responsive UI, API integration, cross-browser fixes, and performance improvements.",
        ],
    },
    {
        "role": "Software Engineer",
        "company": "Datacapten Technologies",
        "dates": "2018-2020",
        "bullets": [
            "Built BI dashboards and dynamic business modules with Node.js exposure.",
        ],
    },
]

DEFAULT_PROJECTS = [
    "AI Smart Assistant Dashboard - Angular, OpenAI API, chatbot, NgRx, RxJS, workflow automation.",
    "QuestNet BI Platform - BI dashboards, enterprise reporting, real-time visualizations.",
    "UBO Compliance Platform - compliance dashboards, role-based UI, complex NgRx state.",
]


def build_resume(out_path: str, cfg: dict):
    st = _styles()
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
    )
    story = []
    _header_block(st, story)

    _section(st, story, "Professional Summary")
    story.append(Paragraph(cfg.get("summary", ""), st["body"]))

    _section(st, story, "Technical Skills")
    skills = cfg.get("skillsGrouped") or {}
    rows = []
    for label, value in skills.items():
        rows.append(
            [
                Paragraph(f"{label}:", st["skill_label"]),
                Paragraph(str(value), st["skill_val"]),
            ]
        )
    if rows:
        t = Table(rows, colWidths=[45 * mm, 120 * mm])
        t.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(t)

    _section(st, story, "Professional Experience")
    for e in cfg.get("experience") or DEFAULT_EXP:
        left = Paragraph(f"<b>{e['role']}</b> - {e['company']}", st["body"])
        right = Paragraph(e["dates"], st["right"])
        row = Table([[left, right]], colWidths=["70%", "30%"])
        row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
        story.append(row)
        for b in e.get("bullets", []):
            story.append(Paragraph(b, st["bullet"], bulletText=BULLET))
        story.append(Spacer(1, 4))

    _section(st, story, "Key Projects")
    for p in cfg.get("projects") or DEFAULT_PROJECTS:
        story.append(Paragraph(p, st["bullet"], bulletText=BULLET))

    _section(st, story, "Education")
    story.append(
        Paragraph(
            "B.E. Computer Science - Pune Vidyarthi Griha's College of Engineering<br/>"
            "<font color='#64748b'>Savitribai Phule Pune University | 2014-2018</font>",
            st["body"],
        )
    )

    doc.build(story)


def build_cover(out_path: str, cfg: dict):
    st = _styles()
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    company = cfg.get("company") or "Hiring Team"
    role = cfg.get("roleTitle") or "Frontend Role"
    cl = cfg.get("coverLetter") or {}
    today = date.today().strftime("%B %d, %Y")

    story = []
    story.append(
        Paragraph(
            CANDIDATE["name"],
            ParagraphStyle("ln", parent=st["name"], fontSize=16, leading=22, spaceAfter=4),
        )
    )
    t = Table([[""]], colWidths=["100%"])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1.2, BLUE)]))
    story.append(t)
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            f"{CANDIDATE['location']} | {CANDIDATE['phone']} | {CANDIDATE['email']} | {CANDIDATE['linkedin']}",
            st["contact"],
        )
    )
    story.append(Spacer(1, 14))
    story.append(Paragraph(today, st["body"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Hiring Manager, {company}", st["body"]))
    story.append(Paragraph("Remote", ParagraphStyle("m", parent=st["body"], textColor=MUTED)))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"<b><font color='#2563eb'>Re:</font></b> {role} - {company}", st["body"]))
    story.append(Spacer(1, 10))
    for key in ("p1", "p2", "p3"):
        if cl.get(key):
            story.append(Paragraph(cl[key], st["body"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Sincerely,", st["body"]))
    story.append(Spacer(1, 16))
    story.append(Paragraph(f"<b>{CANDIDATE['name']}</b>", st["body"]))
    story.append(
        Paragraph(
            f"{CANDIDATE['phone']} | {CANDIDATE['email']}<br/>{CANDIDATE['linkedin']}<br/>{CANDIDATE['location']}",
            ParagraphStyle("sig", parent=st["body"], textColor=MUTED, alignment=TA_LEFT),
        )
    )
    doc.build(story)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_pdfs_from_config.py <config.json>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8-sig") as f:
        cfg = json.load(f)

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(root, "output")
    os.makedirs(out_dir, exist_ok=True)

    ident = _safe_id(cfg.get("identifier") or cfg.get("company") or "Role")
    resume_path = os.path.join(out_dir, f"Subodh_Patil_Resume_{ident}.pdf")
    cover_path = os.path.join(out_dir, f"Subodh_Patil_CoverLetter_{ident}.pdf")

    build_resume(resume_path, cfg)
    build_cover(cover_path, cfg)

    print(f"Wrote: {resume_path}")
    print(f"Wrote: {cover_path}")


if __name__ == "__main__":
    main()
