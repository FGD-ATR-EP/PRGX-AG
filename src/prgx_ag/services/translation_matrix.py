from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from prgx_ag.schemas import EthicalStatus, Intent

TERM_MAP: dict[str, str] = {
    "Parajika": "SYSTEM_HALT_IMMEDIATE",
    "Nirodha": "GRACEFUL_SHUTDOWN",
    "Sati": "ENABLE_DEEP_MONITORING",
    "Metta": "OPTIMIZE_UX_RESPONSE",
    "Sanghadisesa": "SUSPEND_AND_AUDIT",
}

STATUS_MAP: dict[EthicalStatus, str] = {
    EthicalStatus.CLEAN: "System stable and ethically aligned.",
    EthicalStatus.MINOR_INFRACTION: "Minor breach detected; corrective guidance required.",
    EthicalStatus.MAJOR_VIOLATION: "Major governance breach; constrained remediation required.",
    EthicalStatus.PARAJIKA: "Critical violation; immediate halt and audit required.",
}

STATUS_TO_TERM: dict[EthicalStatus, str] = {
    EthicalStatus.CLEAN: "Sati",
    EthicalStatus.MINOR_INFRACTION: "Sati",
    EthicalStatus.MAJOR_VIOLATION: "Sanghadisesa",
    EthicalStatus.PARAJIKA: "Parajika",
}

STATUS_TO_ACTION: dict[EthicalStatus, str] = {
    EthicalStatus.CLEAN: "Monitor repository state",
    EthicalStatus.MINOR_INFRACTION: "Apply monitored remediation",
    EthicalStatus.MAJOR_VIOLATION: "Constrain execution and audit before repair",
    EthicalStatus.PARAJIKA: "Halt execution and escalate immediately",
}

_HIGH_RISK_TOKENS: tuple[str, ...] = (
    "delete_core",
    "shutdown_nexus",
    "rm -rf",
    "drop table",
    "wipe repository",
    "destroy core",
)


def translate_internal_term(term: str) -> str:
    return TERM_MAP.get(term, "UNMAPPED_TERM")


def translate_status(status: EthicalStatus) -> str:
    return STATUS_MAP[status]


def _safe_text(
    value: object,
    *,
    default: str = "unspecified",
    max_len: int = 240,
) -> str:
    if isinstance(value, str):
        text = value
    elif value is None:
        text = ""
    else:
        text = str(value)

    text = " ".join(text.split()).strip()
    if not text:
        return default

    return text[:max_len]


def _normalize_target(value: object) -> str:
    raw = _safe_text(value, default="repository", max_len=300).replace("\\", "/")
    parts = [part for part in raw.split("/") if part not in ("", ".", "..")]
    normalized = "/".join(parts)
    return normalized or "repository"


def _normalize_issue_list(
    value: object,
    *,
    max_items: int = 50,
    max_len: int = 240,
) -> list[str]:
    if not isinstance(value, list):
        return []

    normalized: list[str] = []
    seen: set[str] = set()

    for item in value:
        text = _safe_text(item, default="", max_len=max_len)
        if not text or text in seen:
            continue

        seen.add(text)
        normalized.append(text)

        if len(normalized) >= max_items:
            break

    return normalized


def _derive_categories(
    dependency_issues: list[str],
    structural_issues: list[str],
    integrity_issues: list[str],
) -> list[str]:
    categories: list[str] = []

    if dependency_issues:
        categories.append("dependency")
    if structural_issues:
        categories.append("structural")
    if integrity_issues:
        categories.append("integrity")

    return categories


def _derive_issue_count(
    findings: dict[str, object],
    dependency_issues: list[str],
    structural_issues: list[str],
    integrity_issues: list[str],
) -> int:
    raw = findings.get("issue_count")
    if isinstance(raw, int) and raw >= 0:
        return raw

    return len(dependency_issues) + len(structural_issues) + len(integrity_issues)


def _contains_high_risk_signal(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in _HIGH_RISK_TOKENS)


def _derive_status(
    summary: str,
    target: str,
    dependency_issues: list[str],
    structural_issues: list[str],
    integrity_issues: list[str],
) -> EthicalStatus:
    combined_text = " ".join(
        [
            summary,
            target,
            *dependency_issues,
            *structural_issues,
            *integrity_issues,
        ]
    )

    if _contains_high_risk_signal(combined_text):
        return EthicalStatus.PARAJIKA

    if integrity_issues and any(
        issue.lower().startswith("missing critical file:")
        or issue.lower().startswith("integrity drift detected:")
        for issue in integrity_issues
    ):
        return EthicalStatus.MAJOR_VIOLATION

    if dependency_issues or structural_issues or integrity_issues:
        return EthicalStatus.MINOR_INFRACTION

    return EthicalStatus.CLEAN


def _build_description(
    status: EthicalStatus,
    target: str,
    summary: str,
    issue_count: int,
    categories: list[str],
) -> str:
    category_text = ",".join(categories) if categories else "none"
    action = STATUS_TO_ACTION[status]
    return (
        f"{action} for {target}: "
        f"{summary} | categories={category_text} | issues={issue_count}"
    )


def build_healing_intent(findings: dict[str, object]) -> Intent:
    if not isinstance(findings, dict):
        findings = {}

    summary = _safe_text(
        findings.get("summary"),
        default="repository scan completed",
        max_len=200,
    )
    target = _normalize_target(findings.get("target"))

    dependency_issues = _normalize_issue_list(findings.get("dependency_issues"))
    structural_issues = _normalize_issue_list(findings.get("structural_issues"))
    integrity_issues = _normalize_issue_list(findings.get("integrity_issues"))

    categories = _derive_categories(
        dependency_issues,
        structural_issues,
        integrity_issues,
    )
    issue_count = _derive_issue_count(
        findings,
        dependency_issues,
        structural_issues,
        integrity_issues,
    )

    requires_fix_raw = findings.get("requires_fix")
    if isinstance(requires_fix_raw, bool):
        requires_fix = requires_fix_raw
    else:
        requires_fix = issue_count > 0

    status = _derive_status(
        summary,
        target,
        dependency_issues,
        structural_issues,
        integrity_issues,
    )
    internal_term = STATUS_TO_TERM[status]
    exported_command = translate_internal_term(internal_term)

    metadata: dict[str, Any] = {
        "translation_version": "v2",
        "source_report_type": "prgx1_issue_report",
        "source_summary": summary,
        "target": target,
        "requires_fix": requires_fix,
        "issue_count": issue_count,
        "categories": categories,
        "ethical_status": status.value,
        "status_message": translate_status(status),
        "internal_term": internal_term,
        "exported_command": exported_command,
        "dependency_issues": dependency_issues,
        "structural_issues": structural_issues,
        "integrity_issues": integrity_issues,
    }

    return Intent(
        id=f"intent-{uuid4()}",
        source_agent="PRGX3",
        description=_build_description(
            status=status,
            target=target,
            summary=summary,
            issue_count=issue_count,
            categories=categories,
        ),
        target_firma=target,
        metadata=metadata,
        timestamp=datetime.now(timezone.utc),
    )
