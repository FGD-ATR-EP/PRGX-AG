# PRGX-AG Governance Runtime

PRGX-AG คือ **hybrid repository** ที่รวม Python backend runtime และ governance assets ไว้ในที่เดียว เพื่อรองรับวงจรสแกน วิเคราะห์ นำเสนอเจตนาแก้ไข และซ่อมแบบมีนโยบายกำกับ.

## Repository Positioning
- **This repository is:** implementation-ready governance runtime สำหรับ local และ CI.
- **This repository is not:** static-docs-only site และไม่อ้างว่าเป็นบริการ production-scale ที่ deploy ในวงกว้างแล้ว.
- **Current maturity:** architecture-complete, มี automated tests, และมี policy-driven repair workflows.

## Core Runtime Capabilities
- **PRGX1 Sentry:** read-only scanning สำหรับ drift / integrity.
- **PRGX3 Diplomat:** แปล findings ไปเป็น intent / narrative ที่ review ได้.
- **PRGX2 Mechanic:** execute การแก้ไขแบบ bounded ตาม policy.
- **Nexus Orchestrator:** ควบคุม healing cycle และ event flow.
- **Patimokkha Policy Engine:** บล็อก intent ที่เสี่ยงก่อน execute.
- **RSI Layer:** บันทึก bounded learning artifacts (`GemOfWisdom`) อย่างปลอดภัย.

## Repository Layout
- `src/prgx_ag/` — runtime modules (agents, orchestrator, policy, schemas, services, utils).
- `tests/` — unit/integration/regression tests ของ runtime + CI scripts + web console behavior.
- `.prgx-ag/workflows/` — workflow contracts ฝั่ง governance runtime (`scan_only`, `self_healing`, `dependency_repair`, `structure_repair`).
- `.github/workflows/` — GitHub Actions pipelines สำหรับ scan/test/nightly/heal-pr/security/pages.
- `scripts/ci/` — consistency & typo guard scripts สำหรับ docs/console alignment.
- `index.html` + `web/` — static operational console สำหรับ monitoring metadata และ quick validation.

## CI/CD Workflow Map (Updated)
- `prgx-scan.yml` — scan-only gate สำหรับ runtime/governance path changes.
- `prgx-test.yml` — quality gates (compile, typo, docs-consistency, lint, mypy, web test, pytest).
- `prgx-nightly.yml` — scheduled observational + once cycle พร้อม artifact upload.
- `prgx-heal-pr.yml` — governed healing run ที่สร้าง PR อัตโนมัติเมื่อผ่าน verification.
- `main.yml` — manual/scheduled runtime-cycle orchestration สำหรับ operator.
- `codeql.yml` — CodeQL analysis สำหรับ `python` และ `javascript-typescript`.
- `proof-html.yml` — proof checks สำหรับ `index.html` และ `web/`.
- `static.yml` — deploy static console bundle (`index.html`, `web/`, `package.json`) ไป GitHub Pages.
- `auto-assign.yml`, `stale.yml`, `summary.yml` — repository governance automation.

## Operational Console (`index.html`)
หน้า `index.html` เป็น interactive operator-oriented dashboard (ไม่ต้อง build):
- แสดง runtime health และ task status สำหรับงานกำกับดูแล,
- แสดง kpi cards, a 24-hour throughput chart, และ recent alert queue,
- มี copy-ready validation commands สำหรับการตรวจสอบอย่างรวดเร็ว,
- loads repository version from `package.json`.

Run locally:

```bash
python -m http.server 8080
# open http://localhost:8080/index.html
```

## Local Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
npm ci
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
python scripts/ci/check_typos.py
python scripts/ci/check_console_docs_consistency.py
npm run test:web
pytest -q --maxfail=1
pytest -q tests/test_pipeline_integration.py tests/test_nexus_cycle.py --maxfail=1
```

## Governance Workflow Contracts (`.prgx-ag/workflows`)
- `scan_only.yaml`: read-only scan/report profile.
- `self_healing.yaml`: scan → intent translation → policy audit → safe fix → verify → report → RSI feedback.
- `dependency_repair.yaml`: dependency-focused bounded fixes + verification commands.
- `structure_repair.yaml`: structure-focused bounded fixes + verification commands.

## Security and Compliance
- Vulnerability disclosure: `SECURITY.md`
- Copyright and ownership: `COPYRIGHT.md`
- License: `LICENSE` (MIT)

## Thai Summary (สรุประบบภาษาไทย)
- รีโปนี้เป็น runtime + governance assets ที่ออกแบบให้วงจรซ่อมทำงานได้ใน local/CI โดยมี policy ควบคุม.
- โครงสร้าง workflow ถูกแยกชัดเจนระหว่าง GitHub CI pipelines และ runtime governance contracts.
- README นี้สะท้อนโครงสร้างฐานโค้ดล่าสุดให้ตรงกับไฟล์ที่รันจริงในรีโป.
