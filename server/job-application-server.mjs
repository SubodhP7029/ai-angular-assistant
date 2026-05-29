import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import http from "node:http";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const HUB_DIR = path.join(ROOT, "tools", "job-application-hub");
const OUTPUT_DIR = path.join(ROOT, "output");
const PYTHON_SCRIPT = path.join(ROOT, "scripts", "generate_pdfs_from_config.py");
const PORT = Number(process.env.JOB_HUB_PORT || 3920);

function sendJson(res, status, data) {
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  });
  res.end(JSON.stringify(data));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}"));
      } catch (e) {
        reject(e);
      }
    });
    req.on("error", reject);
  });
}

function serveStatic(req, res, filePath, contentType) {
  if (!fs.existsSync(filePath)) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }
  res.writeHead(200, { "Content-Type": contentType });
  fs.createReadStream(filePath).pipe(res);
}

function runPython(configPath) {
  return new Promise((resolve, reject) => {
    const py = process.platform === "win32" ? "python" : "python3";
    const child = spawn(py, [PYTHON_SCRIPT, configPath], {
      cwd: ROOT,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let out = "";
    let err = "";
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", (d) => (err += d));
    child.on("close", (code) => {
      if (code === 0) resolve(out.trim());
      else reject(new Error(err || out || `Python exited ${code}`));
    });
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    });
    res.end();
    return;
  }

  if (url.pathname === "/api/health" && req.method === "GET") {
    sendJson(res, 200, { ok: true });
    return;
  }

  const staticNames = [
    "/",
    "/index.html",
    "/styles.css",
    "/app.js",
    "/analyzer.js",
    "/resume-data.js",
  ];
  if (staticNames.includes(url.pathname)) {
    const fileName = url.pathname === "/" ? "index.html" : url.pathname.slice(1);
    const file = path.join(HUB_DIR, fileName);
    const ext = path.extname(file);
    const types = {
      ".html": "text/html; charset=utf-8",
      ".css": "text/css; charset=utf-8",
      ".js": "application/javascript; charset=utf-8",
    };
    serveStatic(req, res, file, types[ext] || "text/plain");
    return;
  }

  if (url.pathname === "/api/generate-pdfs" && req.method === "POST") {
    try {
      const body = await readBody(req);
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
      const tmp = path.join(OUTPUT_DIR, `_config_${Date.now()}.json`);
      fs.writeFileSync(tmp, JSON.stringify(body, null, 2), "utf8");
      const result = await runPython(tmp);
      fs.unlinkSync(tmp);
      const lines = result.split("\n").filter(Boolean);
      const resume = lines.find((l) => l.includes("Resume")) || lines[0];
      const cover = lines.find((l) => l.includes("Cover")) || lines[1];
      sendJson(res, 200, {
        ok: true,
        resume: path.basename(resume?.replace("Wrote: ", "") || ""),
        cover: path.basename(cover?.replace("Wrote: ", "") || ""),
        message: result,
      });
    } catch (e) {
      sendJson(res, 500, { error: e.message });
    }
    return;
  }

  res.writeHead(404);
  res.end("Not found");
});

fs.mkdirSync(OUTPUT_DIR, { recursive: true });

server.listen(PORT, () => {
  console.log(`Job Application Hub: http://localhost:${PORT}`);
  console.log(`Static UI: http://localhost:${PORT}/`);
  console.log(`PDF output: ${OUTPUT_DIR}`);
});
