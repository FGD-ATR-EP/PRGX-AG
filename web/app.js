const validationCommands = [
  "python -m compileall src",
  "pytest -q --maxfail=1",
  "pytest -q tests/test_pipeline_integration.py tests/test_nexus_cycle.py --maxfail=1"
];

const taskData = [
  {
    task: "Global Audit Ingestion",
    pid: "PRX-9921",
    status: "running",
    region: "us-east-1",
    updatedAt: "2026-04-15T13:42:10Z"
  },
  {
    task: "Daily Compliance Report",
    pid: "PRX-9918",
    status: "completed",
    region: "us-central",
    updatedAt: "2026-04-15T13:39:54Z"
  },
  {
    task: "Data Stream Validation",
    pid: "PRX-9882",
    status: "failed",
    region: "eu-west-1",
    updatedAt: "2026-04-15T13:36:22Z"
  },
  {
    task: "Cloud Mirror Sync",
    pid: "PRX-9877",
    status: "running",
    region: "ap-southeast-1",
    updatedAt: "2026-04-15T13:35:31Z"
  },
  {
    task: "Dependency Drift Scan",
    pid: "PRX-9869",
    status: "queued",
    region: "global",
    updatedAt: "2026-04-15T13:31:08Z"
  }
];

const alertData = [
  {
    severity: "critical",
    title: "Connection Timeout",
    detail: "External API node 'Alpha-7' is unresponsive. Auto-failover switched to standby.",
    age: "2m ago"
  },
  {
    severity: "warning",
    title: "Latency Threshold",
    detail: "European stream cluster crossed 450ms SLA. Throughput throttling enabled.",
    age: "16m ago"
  },
  {
    severity: "info",
    title: "Backup Complete",
    detail: "Nightly governance state archive completed and signed successfully.",
    age: "1h ago"
  }
];

const throughput24h = [
  120, 140, 105, 180, 220, 270, 240, 210, 250, 260, 230, 280, 320, 300, 275, 330, 360, 350, 310,
  295, 345, 375, 365, 390
];

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = value;
  }
}

function renderCommands() {
  const list = document.getElementById("command-list");
  if (!list) return;

  list.textContent = "";
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
      } catch {
        button.textContent = "Failed";
      }
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1000);
    });

    wrapper.append(code, button);
    list.append(wrapper);
  });
}

function renderChart() {
  const container = document.getElementById("chart-bars");
  if (!container) return;

  const peak = Math.max(...throughput24h);
  container.textContent = "";

  // Create accessible description element
  const descriptionId = "chart-desc";
  const existingDesc = document.getElementById(descriptionId);
  if (existingDesc) {
    existingDesc.remove();
  }

  const description = document.createElement("div");
  description.id = descriptionId;
  description.className = "sr-only";

  let descriptionText = "24-hour processing volume data: ";
  throughput24h.forEach((value, index) => {
    const hourLabel = String(index).padStart(2, "0");
    const formattedValue = value.toLocaleString();
    const isCurrent = index === throughput24h.length - 1;
    descriptionText += `Hour ${hourLabel}: ${formattedValue} records per minute${isCurrent ? " (current hour)" : ""}. `;
  });

  description.textContent = descriptionText.trim();
  container.setAttribute("aria-describedby", descriptionId);
  container.parentNode.insertBefore(description, container);

  throughput24h.forEach((value, index) => {
    const bar = document.createElement("div");
    bar.className = "chart-bar";
    if (index === throughput24h.length - 1) {
      bar.classList.add("is-current");
    }

    const height = `${Math.max((value / peak) * 100, 8)}%`;
    bar.style.height = height;
    bar.title = `Hour ${String(index).padStart(2, "0")}: ${value.toLocaleString()} records/min`;
    container.append(bar);
  });
}

function statusPill(status) {
  const safe = status.toLowerCase();
  return `<span class="status-pill status-${safe}">${safe}</span>`;
}

function renderTasks(query = "") {
  const tbody = document.getElementById("status-rows");
  if (!tbody) return;

  const search = query.trim().toLowerCase();
  const rows = taskData.filter((row) => {
    if (!search) return true;
    return [row.task, row.pid, row.status, row.region].some((value) =>
      value.toLowerCase().includes(search)
    );
  });

  tbody.textContent = "";
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.task}</td>
      <td><code>${row.pid}</code></td>
      <td>${statusPill(row.status)}</td>
      <td>${row.region}</td>
      <td>${row.updatedAt.replace("T", " ").replace("Z", "")}</td>
    `;
    tbody.append(tr);
  });

  const running = taskData.filter((row) => row.status === "running").length;
  const failed = taskData.filter((row) => row.status === "failed").length;
  setText("task-summary", `${running} running • ${failed} failed • ${rows.length} shown`);
}

function renderAlerts() {
  const list = document.getElementById("alert-list");
  if (!list) return;

  list.textContent = "";
  alertData.forEach((alert) => {
    const li = document.createElement("li");
    li.className = `alert-card alert-${alert.severity}`;
    li.innerHTML = `
      <div class="alert-head">
        <strong>${alert.title}</strong>
        <span>${alert.age}</span>
      </div>
      <p>${alert.detail}</p>
      <small>${alert.severity.toUpperCase()}</small>
    `;
    list.append(li);
  });
}

function renderKpis() {
  const pendingAlerts = alertData.filter((item) => item.severity !== "info").length;
  const streams = 12;
  const records24h = throughput24h.reduce((sum, value) => sum + value, 0);
  const health = 99.82;

  setText("kpi-health", `${health.toFixed(2)}%`);
  setText("kpi-health-note", "+0.2% from previous 24h window");

  setText("kpi-streams", String(streams));
  setText("kpi-streams-note", "4 core / 8 auxiliary streams online");

  setText("kpi-alerts", String(pendingAlerts));
  setText("kpi-alerts-note", "1 critical, 1 warning requires response");

  setText("kpi-records", `${(records24h / 1000).toFixed(1)}K`);
  setText("kpi-records-note", "rolling total in the last 24 hours");
}

async function loadMetadata() {
  try {
    const response = await fetch("./package.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`package.json returned ${response.status}`);

    const pkg = await response.json();
    setText("repo-version", pkg.version ?? "unknown");
  } catch {
    setText("repo-version", "unknown");
  }
}

function stampSnapshotTime() {
  const now = new Date();
  const utcTime = now.toISOString().replace("T", " ").slice(0, 19);
  setText("generated-at", `snapshot: ${utcTime} UTC`);
}

function wireSearch() {
  const input = document.getElementById("search-input");
  if (!input) return;

  input.addEventListener("input", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement)) return;
    renderTasks(target.value);
  });
}

function wireRefresh() {
  const btn = document.getElementById("refresh-btn");
  if (!btn) return;

  btn.addEventListener("click", () => {
    stampSnapshotTime();
    renderKpis();
    renderTasks((document.getElementById("search-input") || {}).value || "");
  });
}

function bootstrap() {
  stampSnapshotTime();
  renderKpis();
  renderChart();
  renderTasks();
  renderAlerts();
  renderCommands();
  loadMetadata();
  wireSearch();
  wireRefresh();
}

bootstrap();