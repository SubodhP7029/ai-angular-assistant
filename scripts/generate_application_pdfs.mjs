import fs from "node:fs";
import path from "node:path";
import PDFDocument from "pdfkit";

const root = path.resolve(import.meta.dirname, "..");
const outDir = path.join(root, "output");
fs.mkdirSync(outDir, { recursive: true });

const candidate = {
  name: "Subodh Raghunath Patil",
  title: "Senior Frontend Engineer | Angular | AI-Powered Applications",
  location: "Pune, India",
  phone: "+91-8149488965",
  email: "subodhpatil10@gmail.com",
  linkedIn: "linkedin.com/in/subodh-patil-56b691196",
};

// Avoid ugly line breaks like "high-\nquality" in PDFs.
// Note: Some PDF viewers still break on hyphenated words during text extraction,
// so we prefer unhyphenated phrases for the cover letter body.
const normalize = (s) =>
  s
    .replaceAll("front-end", "front end")
    .replaceAll("end-to-end", "end to end")
    .replaceAll("high-quality", "high quality")
    .replaceAll("AI-powered", "AI powered");

// Tailored to JD: Frontend Developer (HTML, CSS) contractor, AI training context.
const tailoredSummary =
  normalize(
    "I’m a senior frontend engineer with 8+ years of experience building clean, responsive, and reusable UI components using expert-level HTML, CSS/SCSS, and JavaScript/TypeScript—primarily in Angular. I translate design requirements into accessible, high-performance interfaces, integrate UIs with APIs for dynamic experiences, and troubleshoot complex frontend issues end-to-end. Recently, I’ve also delivered AI-powered Angular experiences (OpenAI API integrations) that improve user workflows through chat and smart search."
  );

const skillsLine =
  "Angular, TypeScript, JavaScript, HTML5, CSS3, SCSS, RxJS, REST APIs, Reusable Components, Lazy Loading, State Management, Performance Optimization, Git, Agile/Scrum, Jira, Postman, OpenAI API, LLM Integration";

function drawHeader(doc) {
  doc.font("Helvetica-Bold").fontSize(18).text(candidate.name, { lineGap: 2 });
  doc.font("Helvetica").fontSize(11).text(candidate.title);
  doc
    .moveDown(0.3)
    .fontSize(9.5)
    .fillColor("#374151")
    .text(
      `${candidate.location} | ${candidate.phone} | ${candidate.email} | LinkedIn: ${candidate.linkedIn}`
    )
    .fillColor("#111827");
  doc.moveDown(0.6);
  doc
    .moveTo(doc.page.margins.left, doc.y)
    .lineTo(doc.page.width - doc.page.margins.right, doc.y)
    .strokeColor("#E5E7EB")
    .stroke();
  doc.moveDown(0.8);
}

function sectionTitle(doc, title) {
  doc.font("Helvetica-Bold").fontSize(11).fillColor("#111827").text(title);
  doc.moveDown(0.35);
}

function bullets(doc, items) {
  const indent = 12;
  items.forEach((t) => {
    const x = doc.x;
    const y = doc.y;
    doc.circle(x + 2, y + 5, 1.4).fill("#111827");
    doc
      .fillColor("#111827")
      .font("Helvetica")
      .fontSize(9.6)
      .text(t, x + indent, y, { width: doc.page.width - doc.page.margins.right - (x + indent) });
    doc.moveDown(0.25);
  });
  doc.moveDown(0.3);
}

function buildResume(outPath) {
  const doc = new PDFDocument({
    size: "A4",
    margins: { top: 42, left: 44, right: 44, bottom: 42 },
    info: {
      Title: "Subodh Patil - Resume",
      Author: candidate.name,
    },
  });
  doc.pipe(fs.createWriteStream(outPath));

  drawHeader(doc);

  sectionTitle(doc, "Summary (Tailored)");
  doc.font("Helvetica").fontSize(9.8).text(tailoredSummary, { lineGap: 2, paragraphGap: 4 });
  doc.moveDown(0.6);

  sectionTitle(doc, "Core Skills");
  doc.font("Helvetica").fontSize(9.6).text(skillsLine, { lineGap: 2 });
  doc.moveDown(0.6);

  sectionTitle(doc, "Experience");
  doc.font("Helvetica-Bold").fontSize(10).text("Consultant — Hoonar Tekwurks Consulting (2022–Present)");
  bullets(doc, [
    "Built Angular applications with responsive UI, reusable components, and REST API integrations for data-driven experiences.",
    "Implemented chatbot UIs and OpenAI API integrations to support intelligent assistance workflows.",
    normalize("Partnered with designers and backend developers to deliver integrated, high-quality UI modules."),
  ]);

  doc.font("Helvetica-Bold").fontSize(10).text("Software Engineer — Angular Minds (2021–2022)");
  bullets(doc, [
    "Delivered enterprise Angular modules with modular, reusable UI components and REST API consumption.",
    "Improved performance through optimization and best practices in Angular architecture.",
  ]);

  doc.font("Helvetica-Bold").fontSize(10).text("Frontend Developer — RegalarTech (2020–2021)");
  bullets(doc, ["Developed responsive UI and integrated APIs; improved frontend performance and reliability."]);

  doc.font("Helvetica-Bold").fontSize(10).text("Software Engineer — Datacapten Technologies (2018–2020)");
  bullets(doc, ["Built dashboards and dynamic UI features for business modules with a focus on usability."]);

  sectionTitle(doc, "Selected Projects");
  bullets(doc, [
    normalize("AI Smart Assistant Dashboard — Angular + OpenAI API; chatbot UX, smart search, and workflow automation."),
    "QuestNet BI Platform — Business intelligence dashboards and enterprise reporting interfaces.",
    "UBO Compliance Platform — Compliance dashboards and workflow-based enterprise modules.",
  ]);

  sectionTitle(doc, "Education");
  doc
    .font("Helvetica")
    .fontSize(9.8)
    .text("B.E. Computer Science — Pune Vidyarthi Griha's College of Engineering");

  doc.end();
}

function buildCoverLetter(outPath) {
  const doc = new PDFDocument({
    size: "A4",
    // Slightly wider text block to reduce awkward wraps.
    margins: { top: 50, left: 48, right: 48, bottom: 50 },
    info: {
      Title: "Subodh Patil - Cover Letter",
      Author: candidate.name,
    },
  });
  doc.pipe(fs.createWriteStream(outPath));

  doc.font("Helvetica-Bold").fontSize(14).text(candidate.name);
  doc.font("Helvetica").fontSize(9.8).fillColor("#374151").text(
    `${candidate.location} | ${candidate.phone} | ${candidate.email} | ${candidate.linkedIn}`
  );
  doc.fillColor("#111827").moveDown(0.8);

  const today = new Date().toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "2-digit",
  });
  doc.font("Helvetica").fontSize(9.8).text(today);
  doc.moveDown(0.8);

  doc.font("Helvetica").fontSize(9.8).text("Hiring Team,");
  doc.moveDown(0.8);

  const role = "Frontend Developer (HTML, CSS) — Contractor (Remote)";
  const p1 =
    normalize(
      `I’m writing to apply for the ${role}. With 8+ years of frontend experience, I specialize in building clean, responsive, and reusable interfaces using expert-level HTML, CSS/SCSS, and JavaScript/TypeScript—primarily with Angular. I’m excited about this opportunity because it combines real-world frontend delivery with shaping next-generation AI systems through high quality domain input.`
    );
  const p2 =
    normalize(
      "In my current role as a Consultant at Hoonar Tekwurks Consulting, I translate design requirements into accessible UI components, collaborate closely with designers and backend teams, and integrate front end modules with APIs to power data-driven experiences. I’ve also delivered AI powered Angular experiences, including chatbot UIs and OpenAI API integrations, which required careful UX, performance, and reliability considerations. Across roles, I’ve built modular component libraries, optimized performance, and debugged complex issues in production-facing applications."
    );
  const p3 =
    "I’d welcome the chance to discuss how my frontend expertise—especially in UI component quality, responsiveness, and collaboration—can contribute to your training workflows and product outcomes. Thank you for your time and consideration.";

  doc.font("Helvetica").fontSize(9.8).text(p1, { lineGap: 2, paragraphGap: 6 });
  doc.moveDown(0.8);
  doc.text(p2, { lineGap: 2, paragraphGap: 6 });
  doc.moveDown(0.8);
  doc.text(p3, { lineGap: 2, paragraphGap: 6 });
  doc.moveDown(1.2);

  doc.text("Sincerely,");
  doc.moveDown(1.8);
  doc.font("Helvetica-Bold").text("Subodh Patil");
  doc.font("Helvetica").fillColor("#374151").text(`${candidate.phone} | ${candidate.email}`);
  doc.fillColor("#111827");

  doc.end();
}

const resumePath = path.join(outDir, "Subodh_Patil_Resume.pdf");
const coverPath = path.join(outDir, "Subodh_Patil_Cover_Letter.pdf");

buildResume(resumePath);
buildCoverLetter(coverPath);

console.log(`Wrote: ${resumePath}`);
console.log(`Wrote: ${coverPath}`);

