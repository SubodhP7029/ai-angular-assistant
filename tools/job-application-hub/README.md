# Job Application Hub

Paste multiple job descriptions, get match analysis, tailored summary, cover letter, and PDFs.

## Start

From project root:

```powershell
npm run job-hub
```

Open in browser: **http://localhost:3920**

## Paste multiple JDs

Separate jobs with a line containing only:

```
---
```

or

```
=====
```

Then click **Analyze all**.

## PDFs

Requires Python 3.12+ and ReportLab:

```powershell
python -m pip install reportlab
```

PDFs are written to `output/` as:

- `Subodh_Patil_Resume_[Company].pdf`
- `Subodh_Patil_CoverLetter_[Company].pdf`

## Open without server

You can open `index.html` directly for analysis only (PDF buttons need the server).

For full features, always use `npm run job-hub`.
