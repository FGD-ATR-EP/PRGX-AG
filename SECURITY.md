# Security Policy

## Supported Versions

PRGX-AG is maintained as a rolling mainline project.

| Version | Supported |
| --- | --- |
| `main` / latest commit | ✅ |
| historical tags/commits | ❌ |

## Reporting a Vulnerability

Please report vulnerabilities privately before public disclosure.

1. Open a **GitHub Private Vulnerability Report** (preferred) or use repository-maintainer private contact.
2. Include:
   - affected module/file and branch or commit hash,
   - clear reproduction steps or proof of concept,
   - expected vs actual behavior,
   - impact assessment (confidentiality/integrity/availability).
3. Avoid public exploit disclosure until a fix or mitigation is available.

## Response Targets

- Initial acknowledgment: within **3 business days**.
- Validation and risk triage: within **7 business days** for confirmed reports.
- Disclosure timeline: coordinated based on severity and fix complexity.

## In-Scope Security Surfaces

- Policy enforcement and bounded repair in `src/prgx_ag/policy` and `src/prgx_ag/services`.
- Runtime orchestration/events in `src/prgx_ag/orchestrator` and `src/prgx_ag/core`.
- Governance state integrity in `.prgx-ag/`.
- Automation workflows under `.github/workflows/`.

## Safe Harbor

Good-faith research is welcome. Please do **not** perform:
- destructive or availability-impacting tests,
- unauthorized data exfiltration attempts,
- social-engineering against maintainers,
- attacks against third-party infrastructure.

If you act in good faith under this policy, reports are treated as authorized security research.
