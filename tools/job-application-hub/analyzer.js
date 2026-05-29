/** JD parsing and resume matching */

function splitJobDescriptions(text, autoSplit) {
  const trimmed = text.trim();
  if (!trimmed) return [];

  if (!autoSplit) return [trimmed];

  const parts = trimmed
    .split(/\n(?:-{3,}|={3,})\n/g)
    .map((p) => p.trim())
    .filter(Boolean);

  return parts.length ? parts : [trimmed];
}

function extractCompany(jd) {
  const patterns = [
    /(?:about|join|at)\s+([A-Za-z][A-Za-z0-9.-]{1,30})\b/i,
    /company[:\s]+([A-Za-z][A-Za-z0-9.\s&-]{1,40})/i,
    /^([A-Za-z][A-Za-z0-9.-]{1,25})\s+connects\b/im,
    /^([A-Za-z][A-Za-z0-9.-]{1,25})\s+is\s+(?:a|an)\b/im,
  ];
  for (const re of patterns) {
    const m = jd.match(re);
    if (m?.[1]) {
      const name = m[1].trim().replace(/\s+/g, " ");
      if (!/^(the|we|our|this)$/i.test(name)) return name;
    }
  }
  return null;
}

function extractRoleTitle(jd) {
  const patterns = [
    /job\s*title[:\s]+(.+?)(?:\n|$)/i,
    /position[:\s]+(.+?)(?:\n|$)/i,
    /role[:\s]+(.+?)(?:\n|$)/i,
    /hiring[:\s]+(.+?)(?:\n|$)/i,
  ];
  for (const re of patterns) {
    const m = jd.match(re);
    if (m?.[1]) return m[1].trim().replace(/\s+/g, " ");
  }
  const firstLine = jd.split("\n")[0]?.trim();
  if (firstLine && firstLine.length < 80 && !firstLine.includes(".")) {
    return firstLine;
  }
  return "Role Not Specified";
}

function jdContains(jdLower, aliases) {
  return aliases.some((a) => {
    const term = a.toLowerCase();
    if (term.length <= 3) {
      return new RegExp(`\\b${escapeRegex(term)}\\b`, "i").test(jdLower);
    }
    return jdLower.includes(term);
  });
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function analyzeJob(jdText, index) {
  const jd = jdText.trim();
  const jdLower = jd.toLowerCase();
  const company = extractCompany(jd) || null;
  const roleTitle = extractRoleTitle(jd);
  const identifier = company || roleTitle;

  const matched = [];
  for (const skill of RESUME.skills) {
    if (jdContains(jdLower, [skill.name, ...skill.aliases])) {
      matched.push(skill.name);
    }
  }

  const missing = [];
  for (const item of RESUME.jdWatchlist) {
    if (jdContains(jdLower, [item.name, ...item.aliases])) {
      if (item.has === false) {
        missing.push({
          name: item.name,
          suggestion: suggestGap(item.name),
        });
      } else if (item.has === "partial") {
        missing.push({
          name: item.name + " (partial)",
          suggestion: "Mention familiarity honestly and link any related work.",
        });
      }
    }
  }

  const jdSkillCount = matched.length + missing.length;
  const rawScore =
    jdSkillCount === 0
      ? 55
      : Math.round((matched.length / Math.max(jdSkillCount, 1)) * 100);

  const reactRequired = jdContains(jdLower, ["react"]);
  const angularMentioned = jdContains(jdLower, ["angular"]);
  let score = rawScore;
  if (reactRequired && !angularMentioned) score = Math.min(score, 68);
  if (angularMentioned) score = Math.min(100, score + 8);
  if (jdContains(jdLower, ["typescript"])) score = Math.min(100, score + 5);
  if (jdContains(jdLower, ["openai", "ai", "llm", "machine learning"])) {
    score = Math.min(100, score + 6);
  }

  const label = score >= 75 ? "strong" : score >= 50 ? "moderate" : "weak";
  const labelText =
    score >= 75 ? "Strong match" : score >= 50 ? "Moderate match" : "Weak match";

  const summary = buildSummary(company, roleTitle, jdLower, matched);
  const coverLetter = buildCoverLetter(company, roleTitle, jdLower);
  const tips = buildTips(missing, jdLower, reactRequired);
  const skillsGrouped = buildSkillsGrouped(jdLower, matched);

  return {
    index,
    jd,
    company,
    roleTitle,
    identifier,
    score,
    label,
    labelText,
    matched,
    missing,
    summary,
    coverLetter,
    tips,
    skillsGrouped,
    cursorPrompt: buildCursorPrompt(jd),
  };
}

function buildSummary(company, roleTitle, jdLower, matched) {
  const co = company ? ` at ${company}` : "";
  const aiBit = jdContains(jdLower, ["ai", "llm", "openai", "train"])
    ? " I have hands-on experience integrating OpenAI APIs and building AI chatbot UIs that align with improving real-world model training workflows."
    : "";
  const reactNote = jdContains(jdLower, ["react"])
    ? " While my production depth is in Angular, my TypeScript, component architecture, and state management skills transfer directly to React-based UI engineering."
    : "";

  const top = matched.slice(0, 5).join(", ") || "TypeScript, HTML5, CSS3, Angular";

  return (
    `I am a senior frontend engineer with ${RESUME.experienceYears} years of experience building scalable, responsive, and accessible web applications using ${top}. ` +
    `I translate complex requirements into user-centric interfaces, collaborate cross-functionally with product, design, and backend teams, and champion performance optimization, code reviews, and reusable component patterns.` +
    aiBit +
    reactNote +
    ` I am excited to contribute as a ${roleTitle}${co}.`
  );
}

function buildCoverLetter(company, roleTitle, jdLower) {
  const co = company || "your organization";
  const p1 =
    `I am writing to apply for the ${roleTitle} position at ${co}. With ${RESUME.experienceYears} years of frontend experience, I specialize in building clean, responsive, and accessible interfaces with TypeScript, JavaScript, HTML5, and CSS/SCSS, with deep strength in Angular and component-driven architecture.` +
    (jdContains(jdLower, ["ai", "llm", "train"])
      ? " I am particularly interested in contributing domain expertise to improve how AI systems learn and perform through high-quality, real-world input."
      : " I am excited about the opportunity to deliver seamless, user-centric solutions in a remote, collaborative environment.");

  const p2 =
    "At Hoonar Tekwurks Consulting, I build reusable component libraries, integrate REST APIs, and deliver AI-powered experiences including chatbot UIs and OpenAI API integrations. " +
    "My AI Smart Assistant Dashboard project demonstrates RxJS reactive patterns, NgRx state management, and workflow automation. " +
    "Across roles, I have improved performance through lazy loading, OnPush change detection, and bundle optimization, while participating in code reviews and Agile delivery.";

  const p3 =
    `I would welcome the chance to discuss how my UI engineering strengths can support ${co}'s goals. Thank you for your consideration.`;

  return { p1, p2, p3 };
}

function buildTips(missing, jdLower, reactRequired) {
  const tips = [];
  if (reactRequired) {
    tips.push(
      "Add a small React + TypeScript portfolio (component library + responsive page) and link it on your resume/LinkedIn before applying."
    );
  } else {
    tips.push(
      "Highlight Angular enterprise modules, NgRx/RxJS, and measurable performance wins (lazy loading, bundle size) in bullets."
    );
  }
  if (jdContains(jdLower, ["accessibility", "a11y", "wcag"])) {
    tips.push(
      "In interviews, walk through a concrete A11y fix (focus order, ARIA labels, contrast) you implemented on a real screen."
    );
  } else {
    tips.push(
      "Prepare 2 stories: cross-functional delivery with PM/design/backend, and debugging a complex UI issue with Chrome DevTools."
    );
  }
  if (missing.some((m) => m.name.includes("Playwright") || m.name.includes("Cypress"))) {
    tips.push(
      "Quick win: add one Playwright or Cypress smoke test to a sample app and mention it under Testing on your resume."
    );
  } else if (jdContains(jdLower, ["ai", "llm"])) {
    tips.push(
      "Quick win: emphasize OpenAI integration, prompt patterns, and how you validated chatbot UX quality in the AI Smart Assistant project."
    );
  } else {
    tips.push(
      "Quick win: tailor the first 3 skill rows on your resume to mirror the JD keywords in the same order they appear."
    );
  }
  return tips;
}

function suggestGap(name) {
  const map = {
    React: "Build 1–2 React+TS demos (hooks, components, API integration) and add to skills once real.",
    "Vue.js": "Optional: small Vue todo/dashboard to show framework breadth.",
    Playwright: "Add a basic E2E test suite to a sample app; list under Testing.",
    Cypress: "Same as Playwright — one happy-path E2E flow is enough to mention honestly.",
    Docker: "Only claim if you containerized an app; otherwise skip or say 'exposure'.",
    AWS: "Mention only if you deployed to S3/CloudFront or similar; otherwise omit.",
  };
  return map[name] || `Address ${name} with a small learning project or honest 'exposure' framing.`;
}

function buildSkillsGrouped(jdLower, matched) {
  const core = ["TypeScript", "JavaScript", "HTML5", "CSS3", "SCSS"];
  const frameworks = [];
  if (jdContains(jdLower, ["react"])) frameworks.push("Angular (primary); React (learning)");
  else frameworks.push("Angular (v2–17)", "AngularJS");
  if (jdContains(jdLower, ["bootstrap"])) frameworks.push("Bootstrap 5");
  frameworks.push("Angular Material", "PrimeNG");

  const state = ["RxJS", "NgRx", "Reactive Patterns", "State Management"];
  const ai = jdContains(jdLower, ["ai", "openai", "llm"])
    ? ["OpenAI API", "LLM Integration", "Prompt Engineering", "AI Chatbots"]
    : [];
  const tooling = ["Git", "CI/CD", "Webpack", "Angular CLI", "Chrome DevTools", "Postman"];
  const testing = ["Jasmine", "Karma", "Jest (Familiarity)"];

  const reorder = (arr) => {
    const m = new Set(matched.map((x) => x.toLowerCase()));
    return [...arr].sort((a, b) => {
      const aHit = [...m].some((x) => a.toLowerCase().includes(x)) ? 0 : 1;
      const bHit = [...m].some((x) => b.toLowerCase().includes(x)) ? 0 : 1;
      return aHit - bHit;
    });
  };

  return {
    "Core Technologies": reorder(core).join(", "),
    "Frameworks & UI": frameworks.join(", "),
    "State & Architecture": state.join(", "),
    ...(ai.length ? { "AI & APIs": ai.join(", ") } : {}),
    "Tooling & Delivery": tooling.join(", "),
    Testing: testing.join(", "),
    "Matched from JD": matched.slice(0, 12).join(", ") || "—",
  };
}

function buildCursorPrompt(jd) {
  return `ANALYZE_JD_PDF::\n${jd}`;
}

function analysisToMarkdown(result) {
  const co = result.company || result.identifier;
  let md = `## ${result.roleTitle} — ${co}\n\n`;
  md += `**Match:** ${result.score}% (${result.labelText})\n\n`;
  md += `### Matched skills\n`;
  result.matched.forEach((s) => (md += `- ? ${s}\n`));
  md += `\n### Missing / weak\n`;
  result.missing.forEach((s) => (md += `- ? ${s.name} — ${s.suggestion}\n`));
  md += `\n### Summary\n${result.summary}\n\n`;
  md += `### Cover letter\n${result.coverLetter.p1}\n\n${result.coverLetter.p2}\n\n${result.coverLetter.p3}\n\n`;
  md += `### Tips\n`;
  result.tips.forEach((t) => (md += `- ${t}\n`));
  return md;
}
