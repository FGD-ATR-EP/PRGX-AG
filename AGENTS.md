# AGENTS Status and Roles

## Current repository status
- Repository type: hybrid Python backend and governance-documentation project.
- Current focus: keeping the executable backend, architecture specification, governance flow, and repository metadata aligned.
- Delivery posture: implementation-ready repository with policy-driven repair workflows; not presented as a broadly adopted production service.
- Last maintenance update: documentation consistency and repository-positioning alignment pass.

## Roles
- **Maintainer Agent**: keeps runtime modules, docs, and architecture contracts consistent with implementation intent.
- **Validation Agent**: runs repository checks (format/tests/links/basic consistency) before release.
- **Governance Agent**: reviews policy, telemetry, and alignment model changes for compliance impact.

## Operational rules
- Do not commit `node_modules/`.
- Keep README architecture, glossary, and repository-positioning notes synced with endpoint/entity changes.
- Log major structural fixes in `BUGFIX_PROPOSAL.md`.
