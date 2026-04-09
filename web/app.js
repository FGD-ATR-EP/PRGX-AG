const capabilities = [
  "Policy-gated repair execution (PRGX2 Mechanic + Patimokkha)",
  "Read-only repository drift detection (PRGX1 Sentry)",
  "Intent translation and reviewer narratives (PRGX3 Diplomat)",
  "Workflow orchestration and event routing (PRGX-AG Nexus)",
  "Governance evidence and audit-trail generation",
  "Profile-driven runtime controls (development/staging/production)"
];

const validationCommands = [
  "python -m compileall src",
  "pytest -q --maxfail=1",
  "pytest -q tests/test_pipeline_integration.py tests/test_nexus_cycle.py --maxfail=1"
];

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

function renderCapabilities() {
  const list = document.getElementById("capability-list");
  if (!list) return;
  capabilities.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  });
}

function renderCommands() {
  const list = document.getElementById("command-list");
  if (!list) return;

  validationCommands.forEach((command) => {
    const wrapper = document.createElement("div");
    wrapper.className = "command-item";

    const code = document.createElement("code");
    code.textContent = command;

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = "Copy";
    button.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(command);
        button.textContent = "Copied";
        setTimeout(() => {
          button.textContent = "Copy";
        }, 1200);
      } catch {
        button.textContent = "Failed";
        setTimeout(() => {
          button.textContent = "Copy";
        }, 1200);
      }
    });

    wrapper.append(code, button);
    list.appendChild(wrapper);
  });
}

async function loadPreview(path, targetId, limit = 900) {
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`${path} -> ${response.status}`);
    }
    const text = await response.text();
    setText(targetId, `${text.slice(0, limit)}${text.length > limit ? "\n…" : ""}`);
    return text;
  } catch (error) {
    setText(targetId, `Unable to load ${path}: ${String(error)}`);
    return "";
  }
}

async function loadMetadata() {
  const pkgText = await loadPreview("./package.json", "repo-version", 10000);

  let version = "unknown";
  try {
    const pkg = JSON.parse(pkgText);
    version = pkg.version ?? "unknown";
  } catch {
    // Keep unknown.
  }

  const now = new Date();
  setText("repo-version", `version: ${version}`);
  setText("last-updated", `updated: ${now.toISOString().slice(0, 10)}`);
}

async function bootstrap() {
  renderCapabilities();
  renderCommands();

  await Promise.all([
    loadPreview("./README.md", "readme-preview"),
    loadPreview("./SECURITY.md", "security-preview"),
    loadPreview("./COPYRIGHT.md", "copyright-preview"),
    loadMetadata()
  ]);
}

bootstrap();
