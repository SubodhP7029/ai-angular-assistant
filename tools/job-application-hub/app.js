const API_BASE = "http://localhost:3920";

const $ = (id) => document.getElementById(id);

let lastResults = [];

function showToast(msg) {
  const el = $("toast");
  el.textContent = msg;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 2800);
}

async function checkServer() {
  const el = $("serverStatus");
  try {
    const r = await fetch(`${API_BASE}/api/health`, { signal: AbortSignal.timeout(2000) });
    if (r.ok) {
      el.textContent = "Server online — PDF generation available";
      el.className = "status online";
      return true;
    }
  } catch {
    /* offline */
  }
  el.textContent = "Server offline — analysis works; run npm run job-hub for PDFs";
  el.className = "status offline";
  return false;
}

function renderResults(results) {
  lastResults = results;
  $("emptyState").classList.add("hidden");
  const container = $("resultsContainer");
  container.classList.remove("hidden");
  container.innerHTML = "";

  results.forEach((r, i) => {
    const card = document.createElement("article");
    card.className = "jd-card";
    const fileId = safeFileId(r.company || r.identifier);

    card.innerHTML = `
      <div class="jd-card-header">
        <div>
          <h2>${escapeHtml(r.roleTitle)}</h2>
          <p class="jd-meta">${r.company ? escapeHtml(r.company) : "Company not detected"} · Job ${i + 1}</p>
        </div>
        <span class="score-badge ${r.label}">${r.score}% · ${r.labelText}</span>
      </div>
      <div class="jd-card-body">
        <div class="jd-section">
          <h3>Matched skills</h3>
          <ul>${r.matched.map((s) => `<li class="skill-ok">? ${escapeHtml(s)}</li>`).join("") || "<li>—</li>"}</ul>
        </div>
        <div class="jd-section">
          <h3>Missing / weak</h3>
          <ul>${
            r.missing.length
              ? r.missing
                  .map(
                    (s) =>
                      `<li class="skill-miss">? ${escapeHtml(s.name)} — ${escapeHtml(s.suggestion)}</li>`
                  )
                  .join("")
              : "<li>None detected from watchlist</li>"
          }</ul>
        </div>
        <div class="jd-section">
          <h3>Tailored summary</h3>
          <p>${escapeHtml(r.summary)}</p>
        </div>
        <div class="jd-section">
          <h3>Cover letter</h3>
          <p>${escapeHtml(r.coverLetter.p1)}</p>
          <p style="margin-top:0.5rem">${escapeHtml(r.coverLetter.p2)}</p>
          <p style="margin-top:0.5rem">${escapeHtml(r.coverLetter.p3)}</p>
        </div>
        <div class="jd-section">
          <h3>Gaps & tips</h3>
          <ul>${r.tips.map((t) => `<li>${escapeHtml(t)}</li>`).join("")}</ul>
        </div>
        <div class="jd-section collapsible">
          <h3>Cursor prompt</h3>
          <pre>${escapeHtml(r.cursorPrompt)}</pre>
        </div>
      </div>
      <div class="card-actions">
        <button type="button" class="btn small ghost" data-copy="${i}">Copy Cursor prompt</button>
        <button type="button" class="btn small ghost" data-md="${i}">Copy Markdown</button>
        <button type="button" class="btn small secondary" data-pdf="${i}">Generate PDFs</button>
      </div>
    `;

    container.appendChild(card);
  });

  container.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const i = Number(btn.dataset.copy);
      copyText(lastResults[i].cursorPrompt);
      showToast("Cursor prompt copied");
    });
  });

  container.querySelectorAll("[data-md]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const i = Number(btn.dataset.md);
      copyText(analysisToMarkdown(lastResults[i]));
      showToast("Markdown copied");
    });
  });

  container.querySelectorAll("[data-pdf]").forEach((btn) => {
    btn.addEventListener("click", () => generatePdf(Number(btn.dataset.pdf)));
  });
}

function escapeHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function safeFileId(s) {
  return String(s)
    .replace(/[^A-Za-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 40) || "Role";
}

async function copyText(text) {
  await navigator.clipboard.writeText(text);
}

function runAnalyze() {
  const text = $("jdBulkInput").value;
  const autoSplit = $("autoSplit").checked;
  const chunks = splitJobDescriptions(text, autoSplit);
  $("splitCount").textContent = String(chunks.length);

  if (!chunks.length) {
    showToast("Paste at least one job description");
    return;
  }

  const results = chunks.map((jd, i) => analyzeJob(jd, i));
  renderResults(results);
  showToast(`Analyzed ${results.length} job(s)`);
}

async function generatePdf(index) {
  const r = lastResults[index];
  if (!r) return;

  try {
    const res = await fetch(`${API_BASE}/api/generate-pdfs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        company: r.company || r.identifier,
        roleTitle: r.roleTitle,
        summary: r.summary,
        coverLetter: r.coverLetter,
        skillsGrouped: r.skillsGrouped,
        identifier: safeFileId(r.company || r.identifier),
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "PDF generation failed");
    showToast(`PDFs saved: ${data.resume}`);
  } catch (e) {
    showToast(e.message || "Start server: npm run job-hub");
  }
}

async function generateAllPdfs() {
  if (!lastResults.length) {
    showToast("Analyze jobs first");
    return;
  }
  for (let i = 0; i < lastResults.length; i++) {
    await generatePdf(i);
  }
}

function exportMarkdown() {
  if (!lastResults.length) {
    showToast("Nothing to export");
    return;
  }
  const md = lastResults.map(analysisToMarkdown).join("\n---\n\n");
  const blob = new Blob([md], { type: "text/markdown" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `job-analysis-${Date.now()}.md`;
  a.click();
  URL.revokeObjectURL(a.href);
  showToast("Markdown downloaded");
}

function previewSplit() {
  const chunks = splitJobDescriptions($("jdBulkInput").value, $("autoSplit").checked);
  $("splitCount").textContent = String(chunks.length);
  showToast(`${chunks.length} job block(s) detected`);
}

function loadSample() {
  $("jdBulkInput").value = `About micro1
micro1 connects domain experts to frontier AI development.

Job Title: UI Engineer
Job Type: Contractor
Location: Remote

Key Responsibilities:
- Design scalable UI components using React and TypeScript
- Collaborate with PMs, designers, and backend engineers
- Champion accessibility and performance optimization
- Conduct code reviews

Requirements:
- 3+ years React and TypeScript
- HTML5, CSS3, Git, Agile
- Accessibility and cross-browser compatibility

---
Position: Web UI Developer
Type: Contract
Location: Remote

Requirements:
- Expert HTML, CSS, JavaScript
- Angular, responsive UI, REST APIs
- Unit testing methodologies`;
  previewSplit();
}

const CURSOR_TEMPLATE = `You are a job application assistant for Subodh Raghunath Patil.

Paste a job description after:
ANALYZE_JD_PDF::`;

$("btnAnalyzeAll").addEventListener("click", runAnalyze);
$("btnSplitPreview").addEventListener("click", previewSplit);
$("btnGenerateAllPdfs").addEventListener("click", generateAllPdfs);
$("btnExportMarkdown").addEventListener("click", exportMarkdown);
$("btnLoadSample").addEventListener("click", loadSample);
$("btnCopyCursorTemplate").addEventListener("click", () => {
  copyText(CURSOR_TEMPLATE);
  showToast("Template copied");
});

checkServer();
setInterval(checkServer, 15000);
