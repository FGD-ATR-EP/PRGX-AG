/**
 * Tests for web/app.js – operational dashboard telemetry rendering.
 *
 * Strategy: web/app.js is a plain script (no ES module exports) that calls
 * bootstrap() at load time. We read it as text, strip the trailing
 * `bootstrap()` auto-call, and evaluate it inside the jsdom window so every
 * top-level function is promoted to `window.*` and can be called directly.
 */

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Minimal full-page DOM matching the elements app.js expects. */
function buildDashboardHTML() {
  return `
    <div id="generated-at"></div>
    <input id="search-input" type="search" />
    <button id="refresh-btn" type="button">Refresh</button>

    <!-- KPI cards -->
    <p id="kpi-health" class="kpi-value"></p>
    <small id="kpi-health-note"></small>
    <p id="kpi-streams" class="kpi-value"></p>
    <small id="kpi-streams-note"></small>
    <p id="kpi-alerts" class="kpi-value danger"></p>
    <small id="kpi-alerts-note"></small>
    <p id="kpi-records" class="kpi-value"></p>
    <small id="kpi-records-note"></small>

    <!-- Chart -->
    <div id="chart-bars"></div>

    <!-- Task table -->
    <p id="task-summary" class="pill"></p>
    <table>
      <tbody id="status-rows"></tbody>
    </table>

    <!-- Alert list -->
    <ul id="alert-list"></ul>

    <!-- Commands -->
    <div id="command-list"></div>

    <!-- Metadata -->
    <span id="repo-version"></span>
  `;
}

/** Load app.js source and evaluate it in window scope WITHOUT running bootstrap. */
function loadAppScript() {
  const scriptPath = path.resolve(__dirname, "../../web/app.js");
  let src = fs.readFileSync(scriptPath, "utf8");
  // Remove the bare `bootstrap();` auto-invocation at the very end so we
  // control when (and whether) it runs per test.
  src = src.replace(/^bootstrap\(\);\s*$/m, "");
  // eslint-disable-next-line no-eval
  window.eval(src);
}

// ---------------------------------------------------------------------------
// setText
// ---------------------------------------------------------------------------

describe("setText", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
  });

  it("sets textContent of an existing element", () => {
    window.setText("kpi-health", "99.82%");
    expect(document.getElementById("kpi-health").textContent).toBe("99.82%");
  });

  it("overwrites existing textContent", () => {
    document.getElementById("kpi-streams").textContent = "old";
    window.setText("kpi-streams", "12");
    expect(document.getElementById("kpi-streams").textContent).toBe("12");
  });

  it("does nothing when element id does not exist", () => {
    expect(() => window.setText("non-existent-id", "value")).not.toThrow();
  });

  it("sets empty string without error", () => {
    window.setText("kpi-health", "");
    expect(document.getElementById("kpi-health").textContent).toBe("");
  });
});

// ---------------------------------------------------------------------------
// statusPill
// ---------------------------------------------------------------------------

describe("statusPill", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
  });

  it("returns a span with the correct status class and text for 'running'", () => {
    const html = window.statusPill("running");
    expect(html).toContain('class="status-pill status-running"');
    expect(html).toContain(">running<");
  });

  it("normalises status to lowercase", () => {
    const html = window.statusPill("COMPLETED");
    expect(html).toContain("status-completed");
    expect(html).toContain(">completed<");
  });

  it("handles 'failed' status", () => {
    const html = window.statusPill("failed");
    expect(html).toContain("status-failed");
  });

  it("handles 'queued' status", () => {
    const html = window.statusPill("queued");
    expect(html).toContain("status-queued");
    expect(html).toContain(">queued<");
  });

  it("handles mixed-case 'Running'", () => {
    const html = window.statusPill("Running");
    expect(html).toContain("status-running");
    expect(html).toContain(">running<");
  });
});

// ---------------------------------------------------------------------------
// stampSnapshotTime
// ---------------------------------------------------------------------------

describe("stampSnapshotTime", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
  });

  it("sets generated-at to a string starting with 'snapshot:'", () => {
    window.stampSnapshotTime();
    const text = document.getElementById("generated-at").textContent;
    expect(text).toMatch(/^snapshot:/);
  });

  it("includes 'UTC' in the timestamp", () => {
    window.stampSnapshotTime();
    const text = document.getElementById("generated-at").textContent;
    expect(text).toContain("UTC");
  });

  it("generates a timestamp in YYYY-MM-DD HH:MM:SS format", () => {
    window.stampSnapshotTime();
    const text = document.getElementById("generated-at").textContent;
    // e.g. "snapshot: 2026-04-15 13:42:10 UTC"
    expect(text).toMatch(/snapshot: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC/);
  });

  it("does not include the literal 'T' date separator from ISO string", () => {
    window.stampSnapshotTime();
    const text = document.getElementById("generated-at").textContent;
    // The ISO 'T' separator should be replaced with a space
    expect(text).not.toMatch(/\d{4}-\d{2}-\d{2}T/);
  });
});

// ---------------------------------------------------------------------------
// renderKpis
// ---------------------------------------------------------------------------

describe("renderKpis", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
    window.renderKpis();
  });

  it("sets kpi-health to a percentage value", () => {
    const text = document.getElementById("kpi-health").textContent;
    expect(text).toMatch(/^\d+\.\d{2}%$/);
    expect(text).toBe("99.82%");
  });

  it("populates kpi-health-note", () => {
    const text = document.getElementById("kpi-health-note").textContent;
    expect(text.length).toBeGreaterThan(0);
  });

  it("sets kpi-streams to '12' (the hardcoded stream count)", () => {
    const text = document.getElementById("kpi-streams").textContent;
    expect(text).toBe("12");
  });

  it("populates kpi-streams-note", () => {
    expect(document.getElementById("kpi-streams-note").textContent.length).toBeGreaterThan(0);
  });

  it("sets kpi-alerts to the count of non-info alerts (2)", () => {
    // alertData has 1 critical + 1 warning = 2 non-info alerts
    const text = document.getElementById("kpi-alerts").textContent;
    expect(text).toBe("2");
  });

  it("populates kpi-alerts-note", () => {
    expect(document.getElementById("kpi-alerts-note").textContent.length).toBeGreaterThan(0);
  });

  it("sets kpi-records as a value ending in 'K'", () => {
    const text = document.getElementById("kpi-records").textContent;
    expect(text).toMatch(/^\d+\.\d+K$/);
  });

  it("computes the correct 24h record total (6520 records -> '6.5K')", () => {
    // throughput24h sums to: 120+140+105+…+390 = 6520
    const text = document.getElementById("kpi-records").textContent;
    expect(text).toBe("6.5K");
  });

  it("populates kpi-records-note", () => {
    expect(document.getElementById("kpi-records-note").textContent.length).toBeGreaterThan(0);
  });
});

// ---------------------------------------------------------------------------
// renderChart
// ---------------------------------------------------------------------------

describe("renderChart", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
    window.renderChart();
  });

  it("renders exactly 24 bar elements (one per hour)", () => {
    const bars = document.querySelectorAll("#chart-bars .chart-bar");
    expect(bars).toHaveLength(24);
  });

  it("adds 'is-current' class only to the last bar", () => {
    const bars = document.querySelectorAll("#chart-bars .chart-bar");
    const currentBars = Array.from(bars).filter((b) => b.classList.contains("is-current"));
    expect(currentBars).toHaveLength(1);
    expect(currentBars[0]).toBe(bars[bars.length - 1]);
  });

  it("sets a non-empty height style on every bar", () => {
    const bars = document.querySelectorAll("#chart-bars .chart-bar");
    bars.forEach((bar) => {
      expect(bar.style.height).toMatch(/\d+(\.\d+)?%/);
    });
  });

  it("peak bar (value=390, last element) has 100% height", () => {
    const bars = document.querySelectorAll("#chart-bars .chart-bar");
    const lastBar = bars[bars.length - 1];
    expect(lastBar.style.height).toBe("100%");
  });

  it("sets a tooltip title on each bar containing 'records/min'", () => {
    const bars = document.querySelectorAll("#chart-bars .chart-bar");
    bars.forEach((bar) => {
      expect(bar.title).toContain("records/min");
    });
  });

  it("formats bar titles with zero-padded hour numbers", () => {
    const bars = document.querySelectorAll("#chart-bars .chart-bar");
    // First bar should say "Hour 00:"
    expect(bars[0].title).toContain("Hour 00:");
    // Tenth bar (index 9) should say "Hour 09:"
    expect(bars[9].title).toContain("Hour 09:");
  });

  it("clears existing bars before re-rendering", () => {
    window.renderChart();
    const bars = document.querySelectorAll("#chart-bars .chart-bar");
    expect(bars).toHaveLength(24);
  });

  it("minimum bar height is at least 8% (floor for small values)", () => {
    const bars = document.querySelectorAll("#chart-bars .chart-bar");
    bars.forEach((bar) => {
      const pct = parseFloat(bar.style.height);
      expect(pct).toBeGreaterThanOrEqual(8);
    });
  });

  it("does nothing when chart-bars container is absent", () => {
    document.getElementById("chart-bars").remove();
    expect(() => window.renderChart()).not.toThrow();
  });
});

// ---------------------------------------------------------------------------
// renderTasks
// ---------------------------------------------------------------------------

describe("renderTasks", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
  });

  it("renders all 5 tasks when called with no query", () => {
    window.renderTasks();
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(5);
  });

  it("renders all 5 tasks when called with empty string", () => {
    window.renderTasks("");
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(5);
  });

  it("renders status pills inside table cells", () => {
    window.renderTasks();
    const pills = document.querySelectorAll("#status-rows .status-pill");
    expect(pills).toHaveLength(5);
  });

  it("filters by task name (case-insensitive)", () => {
    window.renderTasks("audit");
    const rows = document.querySelectorAll("#status-rows tr");
    // "Global Audit Ingestion" matches "audit"
    expect(rows).toHaveLength(1);
    expect(rows[0].textContent).toContain("Global Audit Ingestion");
  });

  it("filters by process ID", () => {
    window.renderTasks("PRX-9918");
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(1);
    expect(rows[0].textContent).toContain("Daily Compliance Report");
  });

  it("filters by status", () => {
    window.renderTasks("failed");
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(1);
    expect(rows[0].textContent).toContain("Data Stream Validation");
  });

  it("filters by region (partial match)", () => {
    window.renderTasks("eu-west");
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(1);
    expect(rows[0].textContent).toContain("Data Stream Validation");
  });

  it("returns 0 rows for a query with no matches", () => {
    window.renderTasks("zzz-no-match");
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(0);
  });

  it("trims whitespace from query before filtering", () => {
    window.renderTasks("  audit  ");
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(1);
  });

  it("updates task-summary with running/failed/shown counts", () => {
    window.renderTasks();
    const summary = document.getElementById("task-summary").textContent;
    // 2 running, 1 failed, 5 shown
    expect(summary).toContain("2 running");
    expect(summary).toContain("1 failed");
    expect(summary).toContain("5 shown");
  });

  it("task-summary 'shown' count reflects filtered results, not total", () => {
    window.renderTasks("running");
    const summary = document.getElementById("task-summary").textContent;
    // Running matches on status field - "Global Audit Ingestion" (running) + "Cloud Mirror Sync" (running)
    expect(summary).toContain("2 shown");
    // running/failed counts always reflect full taskData
    expect(summary).toContain("2 running");
    expect(summary).toContain("1 failed");
  });

  it("clears previous rows before re-rendering", () => {
    window.renderTasks();
    window.renderTasks("audit");
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(1);
  });

  it("formats updatedAt by replacing T with space and removing trailing Z", () => {
    window.renderTasks("PRX-9921");
    const row = document.querySelector("#status-rows tr");
    expect(row.textContent).toContain("2026-04-15 13:42:10");
    expect(row.textContent).not.toContain("T");
    expect(row.textContent).not.toContain("Z");
  });

  it("wraps PID in a code element", () => {
    window.renderTasks("PRX-9921");
    const code = document.querySelector("#status-rows tr td code");
    expect(code).not.toBeNull();
    expect(code.textContent).toBe("PRX-9921");
  });

  it("does nothing when status-rows tbody is absent", () => {
    document.getElementById("status-rows").remove();
    expect(() => window.renderTasks()).not.toThrow();
  });
});

// ---------------------------------------------------------------------------
// renderAlerts
// ---------------------------------------------------------------------------

describe("renderAlerts", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
    window.renderAlerts();
  });

  it("renders exactly 3 alert list items", () => {
    const items = document.querySelectorAll("#alert-list li");
    expect(items).toHaveLength(3);
  });

  it("assigns alert-card class to each item", () => {
    const items = document.querySelectorAll("#alert-list .alert-card");
    expect(items).toHaveLength(3);
  });

  it("applies severity-specific class (alert-critical)", () => {
    const critical = document.querySelector(".alert-critical");
    expect(critical).not.toBeNull();
    expect(critical.querySelector("strong").textContent).toBe("Connection Timeout");
  });

  it("applies severity-specific class (alert-warning)", () => {
    const warning = document.querySelector(".alert-warning");
    expect(warning).not.toBeNull();
    expect(warning.querySelector("strong").textContent).toBe("Latency Threshold");
  });

  it("applies severity-specific class (alert-info)", () => {
    const info = document.querySelector(".alert-info");
    expect(info).not.toBeNull();
    expect(info.querySelector("strong").textContent).toBe("Backup Complete");
  });

  it("shows severity label in uppercase", () => {
    const critical = document.querySelector(".alert-critical");
    expect(critical.querySelector("small").textContent).toBe("CRITICAL");
  });

  it("displays the alert age in alert-head", () => {
    const critical = document.querySelector(".alert-critical");
    const head = critical.querySelector(".alert-head");
    expect(head.textContent).toContain("2m ago");
  });

  it("displays the alert detail paragraph", () => {
    const warning = document.querySelector(".alert-warning");
    expect(warning.querySelector("p").textContent).toContain("450ms SLA");
  });

  it("clears existing alerts before re-rendering", () => {
    window.renderAlerts();
    const items = document.querySelectorAll("#alert-list li");
    expect(items).toHaveLength(3);
  });

  it("does nothing when alert-list is absent", () => {
    document.getElementById("alert-list").remove();
    expect(() => window.renderAlerts()).not.toThrow();
  });
});

// ---------------------------------------------------------------------------
// renderCommands
// ---------------------------------------------------------------------------

describe("renderCommands", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
    window.renderCommands();
  });

  it("renders one command-item div per validation command (3 total)", () => {
    const items = document.querySelectorAll("#command-list .command-item");
    expect(items).toHaveLength(3);
  });

  it("each command item contains a code element with the command text", () => {
    const items = document.querySelectorAll("#command-list .command-item");
    const codeTexts = Array.from(items).map((item) => item.querySelector("code").textContent);
    expect(codeTexts).toContain("python -m compileall src");
    expect(codeTexts).toContain("pytest -q --maxfail=1");
    expect(codeTexts).toContain(
      "pytest -q tests/test_pipeline_integration.py tests/test_nexus_cycle.py --maxfail=1"
    );
  });

  it("each command item contains a Copy button", () => {
    const buttons = document.querySelectorAll("#command-list .command-item button");
    expect(buttons).toHaveLength(3);
    buttons.forEach((btn) => {
      expect(btn.textContent).toBe("Copy");
      expect(btn.type).toBe("button");
    });
  });

  it("clears existing items before re-rendering", () => {
    window.renderCommands();
    const items = document.querySelectorAll("#command-list .command-item");
    expect(items).toHaveLength(3);
  });

  it("does nothing when command-list container is absent", () => {
    document.getElementById("command-list").remove();
    expect(() => window.renderCommands()).not.toThrow();
  });

  it("Copy button changes text to 'Copied' on successful clipboard write", async () => {
    const writeText = jest.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", {
      value: { writeText },
      configurable: true,
      writable: true
    });

    jest.useFakeTimers();
    const btn = document.querySelector("#command-list .command-item button");
    btn.click();
    await Promise.resolve(); // flush microtasks
    await Promise.resolve();
    expect(btn.textContent).toBe("Copied");

    jest.runAllTimers();
    expect(btn.textContent).toBe("Copy");
    jest.useRealTimers();
  });

  it("Copy button changes text to 'Failed' on clipboard write rejection", async () => {
    Object.defineProperty(navigator, "clipboard", {
      value: { writeText: jest.fn().mockRejectedValue(new Error("denied")) },
      configurable: true,
      writable: true
    });

    jest.useFakeTimers();
    const btn = document.querySelector("#command-list .command-item button");
    btn.click();
    await Promise.resolve();
    await Promise.resolve();
    expect(btn.textContent).toBe("Failed");

    jest.runAllTimers();
    expect(btn.textContent).toBe("Copy");
    jest.useRealTimers();
  });
});

// ---------------------------------------------------------------------------
// loadMetadata
// ---------------------------------------------------------------------------

describe("loadMetadata", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
  });

  afterEach(() => {
    global.fetch = undefined;
  });

  it("sets repo-version from parsed package.json version field", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ version: "1.2.3" })
    });
    await window.loadMetadata();
    expect(document.getElementById("repo-version").textContent).toBe("1.2.3");
  });

  it("sets repo-version to 'unknown' when version field is missing", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({})
    });
    await window.loadMetadata();
    expect(document.getElementById("repo-version").textContent).toBe("unknown");
  });

  it("sets repo-version to 'unknown' when fetch returns non-OK status", async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: false, status: 404 });
    await window.loadMetadata();
    expect(document.getElementById("repo-version").textContent).toBe("unknown");
  });

  it("sets repo-version to 'unknown' when fetch rejects (network error)", async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error("network failure"));
    await window.loadMetadata();
    expect(document.getElementById("repo-version").textContent).toBe("unknown");
  });

  it("fetches package.json with cache: no-store option", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ version: "0.3.0" })
    });
    await window.loadMetadata();
    expect(global.fetch).toHaveBeenCalledWith("./package.json", { cache: "no-store" });
  });
});

// ---------------------------------------------------------------------------
// wireSearch
// ---------------------------------------------------------------------------

describe("wireSearch", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
    window.renderTasks();
    window.wireSearch();
  });

  it("filters tasks when search input fires an 'input' event", () => {
    const input = document.getElementById("search-input");
    input.value = "audit";
    input.dispatchEvent(new window.Event("input", { bubbles: true }));
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(1);
  });

  it("shows all tasks when search query is cleared", () => {
    const input = document.getElementById("search-input");

    input.value = "audit";
    input.dispatchEvent(new window.Event("input", { bubbles: true }));
    expect(document.querySelectorAll("#status-rows tr")).toHaveLength(1);

    input.value = "";
    input.dispatchEvent(new window.Event("input", { bubbles: true }));
    expect(document.querySelectorAll("#status-rows tr")).toHaveLength(5);
  });

  it("does nothing when search-input element is absent", () => {
    document.getElementById("search-input").remove();
    expect(() => window.wireSearch()).not.toThrow();
  });
});

// ---------------------------------------------------------------------------
// wireRefresh
// ---------------------------------------------------------------------------

describe("wireRefresh", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
    window.renderTasks();
    window.wireRefresh();
  });

  it("updates generated-at timestamp on Refresh click", () => {
    document.getElementById("generated-at").textContent = "old value";
    document.getElementById("refresh-btn").click();
    const text = document.getElementById("generated-at").textContent;
    expect(text).toMatch(/^snapshot:/);
  });

  it("re-renders KPI values on Refresh click", () => {
    document.getElementById("kpi-health").textContent = "";
    document.getElementById("refresh-btn").click();
    expect(document.getElementById("kpi-health").textContent).toBe("99.82%");
  });

  it("re-renders tasks (respecting current search value) on Refresh click", () => {
    const input = document.getElementById("search-input");
    input.value = "audit";
    document.getElementById("refresh-btn").click();
    const rows = document.querySelectorAll("#status-rows tr");
    expect(rows).toHaveLength(1);
  });

  it("re-renders all tasks when search input is empty on Refresh click", () => {
    document.getElementById("refresh-btn").click();
    expect(document.querySelectorAll("#status-rows tr")).toHaveLength(5);
  });

  it("does nothing when refresh-btn element is absent", () => {
    document.getElementById("refresh-btn").remove();
    expect(() => window.wireRefresh()).not.toThrow();
  });
});

// ---------------------------------------------------------------------------
// bootstrap (integration)
// ---------------------------------------------------------------------------

describe("bootstrap", () => {
  beforeEach(() => {
    document.body.innerHTML = buildDashboardHTML();
    loadAppScript();
  });

  it("populates all KPI elements after bootstrap()", () => {
    window.bootstrap();
    expect(document.getElementById("kpi-health").textContent).toBe("99.82%");
    expect(document.getElementById("kpi-streams").textContent).toBe("12");
    expect(document.getElementById("kpi-alerts").textContent).toBe("2");
    expect(document.getElementById("kpi-records").textContent).toMatch(/K$/);
  });

  it("renders 24 chart bars after bootstrap()", () => {
    window.bootstrap();
    expect(document.querySelectorAll("#chart-bars .chart-bar")).toHaveLength(24);
  });

  it("renders 5 task rows after bootstrap()", () => {
    window.bootstrap();
    expect(document.querySelectorAll("#status-rows tr")).toHaveLength(5);
  });

  it("renders 3 alert cards after bootstrap()", () => {
    window.bootstrap();
    expect(document.querySelectorAll("#alert-list .alert-card")).toHaveLength(3);
  });

  it("renders 3 command items after bootstrap()", () => {
    window.bootstrap();
    expect(document.querySelectorAll("#command-list .command-item")).toHaveLength(3);
  });

  it("sets snapshot timestamp after bootstrap()", () => {
    window.bootstrap();
    const text = document.getElementById("generated-at").textContent;
    expect(text).toMatch(/^snapshot:/);
  });

  it("wires the refresh button so it updates the snapshot on click", () => {
    window.bootstrap();
    document.getElementById("generated-at").textContent = "stale";
    document.getElementById("refresh-btn").click();
    expect(document.getElementById("generated-at").textContent).toMatch(/^snapshot:/);
  });

  it("wires the search input so it filters rows on input event", () => {
    window.bootstrap();
    const input = document.getElementById("search-input");
    input.value = "failed";
    input.dispatchEvent(new window.Event("input", { bubbles: true }));
    expect(document.querySelectorAll("#status-rows tr")).toHaveLength(1);
  });
});