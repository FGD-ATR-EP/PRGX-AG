# Bug Fix Proposal

## Scope
Major structural fix: migrate repository from static-only docs layout into complete Python backend architecture for PRGX-AG Nexus while preserving governance documentation intent.

## Findings
1. Backend architecture existed only as narrative, not executable modules.
2. No strict schemas, no event bus runtime, no orchestrator, and no policy tests.
3. Missing CLI, RSI loop, and triad-agent integration.

## Proposed fixes
1. Add `src/prgx_ag` modular backend with strict Pydantic models and async AetherBus.
2. Implement PRGX1/PRGX2/PRGX3 agents with Patimokkha-enforced healing flow.
3. Add orchestrator + RSI engine + bounded learning state.
4. Add pytest coverage for policy, bus, agents, RSI, and full cycle.

## Expected impact
- Architecture is now executable and testable.
- Harmful intents are programmatically blocked before write operations.
- Repository now supports production-style governance flow and self-healing cycle.

## Rollback
Revert this change set if consumers require previous static-only documentation repository state.

## 2026-03-17 Major structural fix
- Implemented full hybrid PRGX-AG architecture (.prgx-ag governance + GitHub workflows + Python runtime triad).
- Added strict schemas, event-driven nexus wiring, safe fix executor guardrails, RSI bounded learning, and manifest/policy loaders.
- Added deterministic pytest coverage for policy, bus, triad behavior, manifest loading, translation matrix, and full cycle flow.

## 2026-03-17 Bug fix and documentation alignment
- Fixed pytest execution bug by adding `pythonpath = ["src"]` in `pyproject.toml`, so test imports work without manual environment overrides.
- Updated README system architecture into database/state-aligned ER diagram based on `.prgx-ag` data sources.
- Removed completed-recommendation noise and replaced with forward-only EN/TH backlog proposals.

## 2026-03-17 Triad hardening and architecture completion pass
- Added explicit PRGX1 read-only scan methods for dependency, structure, and integrity drift observation.
- Added integrity scanner + healing intent builder + finding/narrative schemas to complete Porisjem role boundaries.
- Extended orchestrator with `PRGXAGNexus` naming, shutdown support, and compatibility alias.
- Updated README with full Porisjem/AETHERIUM framing, refreshed architecture diagram context, and new EN/TH future backlog items.

## 2026-03-17 README architecture/data-store alignment refresh
- Refined README system architecture to mirror the actual `.prgx-ag` data layout, including policy, manifest, workflow, state, and audit relationships.
- Removed completed-recommendation overlap from bilingual backlog sections and replaced it with new forward-looking EN/TH enhancement proposals.

## 2026-03-18 Source recovery fix
- Repaired `src/prgx_ag/agents/prgx1_sentry.py` after a diff artifact and concatenated multi-file patch content were accidentally committed into the module body.
- Restored the file to valid Python source so import, compile, and packaging pipelines can load the PRGX1 agent again.

## 2026-03-18 Workflow governance gate alignment
- Promoted `.github/workflows/prgx-test.yml` as the canonical repository-health gate with a consistent early `python -m compileall src` sanity check.
- Standardized Python setup/install patterns across the PRGX scan, nightly, and healing workflows to reduce dependency drift and simplify triage.
- Removed the generic GitHub Pages deployment workflow because it deployed the entire repository root instead of a dedicated static-site artifact, which was not appropriate for this repository health model.

## 2026-03-18 Governed healing pipeline expansion
- Extended healing fix-plan entries with machine-readable metadata for fix class, rationale, verification commands, rollback hints, and source issue provenance.
- Upgraded executor and narrative layers so applied fix classes, verification state, and rollback guidance remain visible to reviewers and automation.
- Reworked the PR healing workflow to keep `.github/workflows/prgx-heal-pr.yml` as the entry point while adding post-fix verification, blocked/revert behavior, and dynamic PR branch metadata generation.
- Refreshed README architecture documentation to mirror the concrete `.prgx-ag` data stores/workflows and removed completed-recommendation sections from both English and Thai text.

## 2026-03-18 Structured Patimokkha rule evaluation refactor
- Replaced flat blocked-token matching with explicit policy rule objects carrying scope, severity, allow-context hints, and recommended actions.
- Extended audit outputs with structured match evidence so reviewers can see which field matched, which rule fired, and whether the outcome was allow, contextual review, or reject.
- Added regression tests for defensive narratives, safe exported commands, and malicious payloads hidden inside metadata.

## 2026-03-18 Governed repair pipeline regression hardening
- Added deeper Nexus/Mechanic/Patimokkha integration coverage, including realistic governed repair payloads, protected-path enforcement, invalid fix plans, duplicate fixes, traversal attempts, and empty plan rejections.
- Added PR/report narrative regressions for `github_bridge.py` and `narrative_builder.py` so audit metadata, rollback guidance, and changed-file summaries remain stable.
- Strengthened `.github/workflows/prgx-test.yml` and README release guidance so governed integration tests run as a required quality gate before broader matrix testing.

## 2026-03-18 Repair engine bounded-safety expansion
- Introduced explicit governed fix classes (`create_empty_init`, `manifest_sync`, `dependency_bump`) with validator metadata instead of relying on generic empty-file writes.
- Added dependency allowlist policy data so automatic manifest edits are limited to preapproved package/range pairs and minor-only bump rules.
- Captured per-fix snapshots, rollback metadata, and post-fix verification results so PR narratives can explain safety, validation, and deterministic reversion paths.

## 2026-03-18 Repository metadata and test-noise cleanup
- Removed the unused `pytest-asyncio` configuration path from `pyproject.toml` so the test suite no longer emits an unknown-config warning in environments that do not install that plugin.
- Rewrote `README.md` to keep the architecture summary aligned with the actual `.prgx-ag` governance assets and to explicitly exclude completed-suggestion lists from both English and Thai summaries.
- Replaced leftover demo metadata in `index.html` and `package.json` with repository-accurate PRGX-AG descriptions.


## 2026-03-18 Workflow reliability and repository-noise cleanup
- Fixed `.github/workflows/main.yml` so it installs the dev toolchain required by `pytest`, `ruff`, and `mypy`, adds an explicit compile sanity check, and stops uploading hidden `.prgx-ag` artifacts without opting in.
- Standardized workflow caching and runner setup across `main.yml`, `prgx-scan.yml`, `prgx-nightly.yml`, `prgx-test.yml`, and `prgx-heal-pr.yml` to reduce drift between the primary gate and the auxiliary automation jobs.
- Tightened `proof-html.yml` to run only for HTML/workflow changes, added pull-request coverage, and removed redundant workflow noise so the repository health signals stay focused on the actual system structure.
- Removed an unused `pytest` import from `tests/test_pipeline_integration.py` so `ruff check .` passes consistently in local and CI validation.


## 2026-03-19 Documentation conflict reconciliation
- Corrected `AGENTS.md` so the repository is described as a hybrid Python backend plus governance-documentation project instead of a static/documentation-only repository.
- Reframed the public README positioning to avoid overstating production adoption while still documenting the executable backend architecture already present in `src/prgx_ag/`.
- Added a terminology mapping table so domain names such as Patimokkha, Porisjem, AetherBus, GemOfWisdom, Inspira, and Firma are explicitly connected to standard software concepts.
- Clarified why `package.json` and `index.html` exist at the repository root and documented them as metadata/proofing artifacts rather than primary backend runtime files.
- Softened public maturity language to reflect an early-stage project with limited community traction instead of implying broad production validation.


## 2026-03-20 Workflow environment mapping for deployment readiness
- Added explicit GitHub Environment wiring so workflow runs can target `development`, `staging`, or `production` with consistent branch-based defaults.
- Documented the required environment names, protection guidance, and suggested environment-scoped secrets for future deployment/promotion jobs.
- Kept the README release/deployment guidance aligned with the workflow configuration so operators can create matching repository environments in GitHub settings.

## 2026-03-28 Dry-run side-effect hardening and maintenance follow-through
- Updated `src/prgx_ag/services/fix_executor.py` so `dry_run=True` verification is fully in-memory and no longer creates directories or writes temporary files.
- Added regression coverage in `tests/test_prgx2_mechanic.py` to verify dry-run dependency bumps keep repository content and directory state unchanged.
- Clarified the `wire_subscriptions()` compatibility comment in `src/prgx_ag/orchestrator/nexus.py` to avoid ambiguous wording drift in future edits.
- Completed the previously proposed task set from 2026-03-19: typo/text polish, dry-run bug fix, comment/doc alignment, and dry-run regression testing.

## 2026-03-28 CI workflow bug-fix and reliability hardening pass
- Fixed `.github/workflows/proof-html.yml` by adding an explicit checkout step so HTML validation runs against repository content instead of an empty workspace.
- Corrected `.github/workflows/main.yml` dispatch-mode behavior so `mode=scan-only` no longer runs the test phase unexpectedly.
- Added explicit job timeouts across all active workflows to prevent stuck CI jobs from consuming unlimited runner time.
- Removed unused `GITHUB_TOKEN` environment exports from scheduled automation jobs where the token is not directly consumed by runtime commands.

## 2026-03-28 Documentation governance and policy-file alignment refresh
- Updated `README.md` system architecture ER diagram to align more explicitly with the repository-backed `.prgx-ag` data model, including dependency allowlist and legacy path-list mirrors.
- Removed completed-recommendation mixing by defining forward-looking-only proposal sections in both English and Thai.
- Added `SECURITY.md` to define vulnerability reporting, response targets, scope boundaries, and safe-harbor expectations.
- Added `COPYRIGHT.md` to document repository copyright ownership and third-party notice expectations.

## 2026-03-28 Typed environment profiles and signed governance evidence
- Added typed runtime profiles (`development`, `staging`, `production`) in `src/prgx_ag/config.py` with per-profile auto-repair thresholds and audit verbosity controls.
- Fixed a governance consistency bug in `PRGX3Diplomat` by building fix plans against the scanned repository target (instead of relying on process CWD), then enforcing profile-aware fix caps and issue-count gates.
- Added signed governance evidence artifact generation in `src/prgx_ag/services/governance_evidence.py`, bundling audit-log slices, fix-plan metadata, and medical research findings references.
- Updated GitHub workflows to pass runtime-profile/audit-window settings and include evidence artifacts in CI uploads so environment behavior remains aligned with governance expectations.

## 2026-04-02 Workflow consistency and stale-governance hardening
- Fixed `.github/workflows/main.yml` by removing a duplicated `environment:` key that risked workflow parsing/maintenance drift and by aligning branch-derived environment mapping to use `PRGX_BRANCH_CONTEXT` consistently.
- Rebuilt `.github/workflows/stale.yml` as an explicit governance workflow with manual dispatch, top-level permissions, concurrency, timeout, and modern `actions/stale@v10` settings.
- Standardized stale lifecycle behavior with concrete stale/close windows, clear issue/PR messaging, exempt governance/security labels, and automatic stale-label removal on new activity.

## 2026-04-02 README architecture refocus and proposal hygiene update
- Reworked `README.md` architecture coverage to include an Augmented Perception Layer high-level module flow (Genesis, Manifest, BioVision, Governor, PRGX, Tachyon, Edge/WASM) tied directly to repository-backed `.prgx-ag` data stores.
- Removed completed-recommendation style sections from bilingual README content so active backlog/proposals do not mix with already-finished work items.
- Added explicit "Open Problems & Required Fixes" plus forward proposal backlogs (EN/TH) to keep unresolved risks, required remediations, and next-step feature proposals visible in one operational section.

## 2026-04-09 Web console operationalization and documentation/legal refresh
- Rebuilt root `index.html` from static text into an operational console that loads repository metadata, capability summaries, validation commands, and live previews of core governance documents.
- Added `web/app.js` and `web/styles.css` to make the console function without a build system while keeping repository-root static hosting compatibility.
- Reconciled repository governance/legal docs by updating `README.md`, `SECURITY.md`, and `COPYRIGHT.md` and by adding a concrete `LICENSE` file.
- Removed stale/ambiguous top-level documentation wording and replaced it with current repository positioning and release-check guidance.

## 2026-04-15 Repository hygiene pass: typo/grammar/docs alignment and bug fix
- Fixed intent-target normalization in `src/prgx_ag/services/translation_matrix.py` so parent-directory (`..`) segments are removed from generated metadata paths.
- Added regression tests for traversal-like target input plus `ManifestLoader` missing-file and invalid-YAML error contracts.
- Updated `README.md` wording and kept only forward-looking bilingual proposals, explicitly removing completed suggestion overlap between English and Thai sections.

## 2026-04-15 Operational dashboard UX and telemetry-structure refresh
- Rebuilt `index.html` into a true operator-oriented dashboard layout with persistent sidebar navigation, KPI cards, 24-hour throughput chart area, live status table, and recent-alert queue.
- Replaced legacy `web/app.js` document-preview rendering with operational telemetry rendering (KPIs, searchable task table, alert feed, command copy actions, and snapshot refresh behavior).
- Reworked `web/styles.css` into a responsive console design system that supports desktop and tablet/mobile layouts while preserving no-build static hosting.

## 2026-04-16 CI governance typo/consistency gates and policy docs refresh
- Added `scripts/ci/check_typos.py` to enforce automatic typo checks for governance documentation and Python annotations (docstrings/comments) in CI.
- Added `scripts/ci/check_console_docs_consistency.py` to prevent drift between README Operational Console descriptions and `index.html` dashboard semantics.
- Updated `.github/workflows/prgx-test.yml` to run both new documentation-integrity checks before governed integration/test matrix execution.
- Refreshed `README.md`, `SECURITY.md`, `LICENSE`, and `index.html` metadata text so repository security/legal/console descriptions stay consistent with the new controls.

## 2026-04-21 Workflow contract realignment and README structure sync
- Refactored all active GitHub workflows to match the actual hybrid codebase responsibilities (Python runtime, web console assets, governance automation) with clearer triggers, scoped paths, and consistent concurrency/timeout behavior.
- Updated CI quality coverage to include Node web-console tests (`npm run test:web`) alongside existing Python compile/lint/type/test checks.
- Hardened Pages deployment to publish only a dedicated static-site bundle (`index.html` + `web/`) instead of uploading the entire repository.
- Expanded `.prgx-ag/workflows/*.yaml` governance contracts with explicit runtime profile, mode, dry-run semantics, verification commands, and artifact scopes.
- Rewrote `README.md` sections to mirror current repository structure and the updated workflow map.
