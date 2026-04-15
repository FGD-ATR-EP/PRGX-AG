# PRGX-AG Governance Runtime

PRGX-AG is a **hybrid Python backend + governance-documentation repository**. The executable runtime lives in `src/prgx_ag/` and the policy/manifests/audit workflow data lives in `.prgx-ag/`.

## Repository Positioning
- **This repository is:** implementation-ready governance runtime for local/CI operation.
- **This repository is not:** a static-docs-only site and not a claim of proven large-scale production adoption.
- **Current maturity:** architecture-complete with automated tests and governed repair flow; still early-stage in ecosystem adoption.

## Core Runtime Capabilities
- **PRGX1 Sentry:** read-only repository drift and integrity scanning.
- **PRGX3 Diplomat:** finding translation, healing-intent generation, and reviewer narrative output.
- **PRGX2 Mechanic:** bounded fix execution with policy and path controls.
- **Nexus Orchestrator:** event routing and healing-cycle coordination.
- **Patimokkha Policy Engine:** blocks unsafe/destructive intent prior to execution.
- **RSI Layer:** bounded learning artifacts (`GemOfWisdom`) tied to governance-safe updates.

## Repository Layout
- `src/prgx_ag/` — Python runtime, agents, orchestration, policy evaluators, schemas, and services.
- `.prgx-ag/` — policy, manifests, workflows, state, and audit log data used by runtime.
- `tests/` — unit/integration regression coverage.
- `index.html` + `web/` — static operational console for repository metadata and validation quick checks.
- `SECURITY.md`, `COPYRIGHT.md`, `LICENSE` — security disclosure and legal terms.

## Operational Console (`index.html`)
The root `index.html` is an interactive repository console (no build step required):
- shows runtime capability summary,
- provides copy-ready validation commands,
- previews `README.md`, `SECURITY.md`, and `COPYRIGHT.md`,
- loads repository version from `package.json`.

Run locally with:

```bash
python -m http.server 8080
# open http://localhost:8080/index.html
```

## Local Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## CLI Usage
```bash
python -m prgx_ag.main --once
python -m prgx_ag.main --continuous --interval 10
python -m prgx_ag.main --scan-only
```

## Release Check Sequence
```bash
python -m compileall src
pytest -q --maxfail=1
pytest -q tests/test_pipeline_integration.py tests/test_nexus_cycle.py --maxfail=1
```

## Open Problems & Required Fixes (Forward-Looking Only)
> This section lists only active work items to keep finished work separate.

### English (EN)
- Add automated typo checks for governance docs and Python comments in CI.
- Expand integration coverage for failure handling in GitHub/report generation paths.

### ภาษาไทย (TH)
- เพิ่มการตรวจสะกดคำอัตโนมัติสำหรับเอกสาร governance และคอมเมนต์ในโค้ดภายใน CI
- เพิ่มการทดสอบแบบบูรณาการในกรณี failure ของเส้นทาง GitHub/report generation

## Security and Compliance
- Vulnerability disclosure process: `SECURITY.md`
- Copyright and ownership notice: `COPYRIGHT.md`
- Open-source license terms: `LICENSE`

## Thai Summary (สรุประบบภาษาไทย)
- รีโปนี้เป็นแบบผสม: Python runtime ที่รันได้จริง + governance assets ใน `.prgx-ag`.
- วงจรทำงานหลัก: PRGX1 ตรวจจับ → PRGX3 แปลเจตนาแก้ไข → PRGX2 ดำเนินการแบบมีขอบเขต → Nexus บันทึกหลักฐานและวงจรเรียนรู้.
- `index.html` ใช้เป็นหน้า operational console สำหรับตรวจสอบความพร้อมของระบบและเอกสารหลักแบบรวดเร็ว.
