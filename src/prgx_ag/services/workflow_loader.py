from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class SelfHealingWorkflowConfig:
    dry_run: bool


def load_self_healing_workflow_config(repo_root: Path) -> SelfHealingWorkflowConfig:
    workflow_path = repo_root / ".prgx-ag/workflows/self_healing.yaml"
    if not workflow_path.exists():
        return SelfHealingWorkflowConfig(dry_run=True)

    data = yaml.safe_load(workflow_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return SelfHealingWorkflowConfig(dry_run=True)

    raw_dry_run: Any = data.get("dry_run", True)
    if isinstance(raw_dry_run, bool):
        return SelfHealingWorkflowConfig(dry_run=raw_dry_run)
    if isinstance(raw_dry_run, str):
        normalized = raw_dry_run.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return SelfHealingWorkflowConfig(dry_run=True)
        if normalized in {"0", "false", "no", "off"}:
            return SelfHealingWorkflowConfig(dry_run=False)
    return SelfHealingWorkflowConfig(dry_run=True)
