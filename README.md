# ai-angular-assistant

AI-powered Angular application integrating OpenAI APIs to enable chatbot interaction, text summarization, and intelligent content generation.

## Job Application Hub

Paste multiple job descriptions, get match analysis, tailored summary, cover letter text, and PDFs.

### Prerequisites

- Node.js 18+
- Python 3.10+ (for PDF generation)
- ReportLab: `python -m pip install -r scripts/requirements-pdf.txt`

### Run the hub

```bash
npm install
npm run job-hub
```

Open **http://localhost:3920**

### Paste multiple JDs

Separate each job description with a line containing only `---` or `=====`, then click **Analyze all**.

### PDF output

Generated files are saved locally to `output/` (not committed to git):

- `Subodh_Patil_Resume_[Company].pdf`
- `Subodh_Patil_CoverLetter_[Company].pdf`

### Angular app

```bash
npm start
```

Runs the Angular dev server at http://localhost:4200

## Project structure

| Path | Description |
|------|-------------|
| `src/` | Angular application |
| `tools/job-application-hub/` | Job Application Hub UI |
| `server/job-application-server.mjs` | Local server for hub + PDF API |
| `scripts/` | PDF generators (Python ReportLab, Node pdfkit) |

## Push to GitHub

```bash
git add .
git commit -m "Your message"
git push origin main
```

Remote: https://github.com/SubodhP7029/ai-angular-assistant
