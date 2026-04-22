from pathlib import Path

from prgx_ag.services.workflow_loader import load_self_healing_workflow_config


def test_load_self_healing_workflow_config_defaults_when_missing(tmp_path: Path) -> None:
    config = load_self_healing_workflow_config(tmp_path)
    assert config.dry_run is True


def test_load_self_healing_workflow_config_reads_dry_run(tmp_path: Path) -> None:
    workflow_path = tmp_path / ".prgx-ag/workflows/self_healing.yaml"
    workflow_path.parent.mkdir(parents=True)
    workflow_path.write_text("name: self_healing\ndry_run: false\n", encoding="utf-8")

    config = load_self_healing_workflow_config(tmp_path)
    assert config.dry_run is False
