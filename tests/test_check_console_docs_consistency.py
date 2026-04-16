"""Tests for scripts/ci/check_console_docs_consistency.py."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts/ci to import path so the module can be imported directly.
_CI_DIR = Path(__file__).resolve().parents[1] / "scripts" / "ci"
if str(_CI_DIR) not in sys.path:
    sys.path.insert(0, str(_CI_DIR))

import check_console_docs_consistency as cdcc  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FULL_README_SECTION = """\
## Operational Console (`index.html`)

This is an operator-oriented dashboard for runtime health monitoring.
It shows task status and kpi cards for at-a-glance visibility.
A 24-hour throughput chart is displayed for trend analysis.
The recent alert queue lists the latest governance alerts.
Copy-ready validation commands are shown in the command panel.
The page loads repository version from `package.json` on startup.

## Other Section
"""

_FULL_INDEX_HTML = """\
<!DOCTYPE html>
<html>
<head>
  <meta name="description" content="Operational dashboard for PRGX-AG runtime health, task status, governance alerts, and quick validation commands." />
  <title>PRGX-AG Operational Dashboard</title>
</head>
<body>
  <!-- Task execution state from orchestrator telemetry -->
  <div>Records Processed (24h)</div>
  <div>Recent Alerts</div>
  <div>Governance Snapshot</div>
  <div>quick validation commands</div>
  <span id="repo-version"></span>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# _extract_operational_console_block
# ---------------------------------------------------------------------------

def test_extract_block_returns_lowercased_content() -> None:
    result = cdcc._extract_operational_console_block(_FULL_README_SECTION)
    assert result == result.lower()


def test_extract_block_contains_section_content() -> None:
    result = cdcc._extract_operational_console_block(_FULL_README_SECTION)
    assert "operator-oriented dashboard" in result


def test_extract_block_stops_before_next_section() -> None:
    result = cdcc._extract_operational_console_block(_FULL_README_SECTION)
    # "Other Section" belongs to the next ## heading and must not appear in the block
    assert "other section" not in result


def test_extract_block_raises_when_section_missing() -> None:
    readme_without_section = "# README\n\nNo console section here.\n"
    with pytest.raises(RuntimeError, match="Operational Console"):
        cdcc._extract_operational_console_block(readme_without_section)


def test_extract_block_works_when_section_at_end_of_file() -> None:
    readme_end_of_file = (
        "## Operational Console (`index.html`)\n"
        "Some operator-oriented dashboard content here.\n"
    )
    result = cdcc._extract_operational_console_block(readme_end_of_file)
    assert "operator-oriented dashboard" in result


def test_extract_block_lowercases_mixed_case_content() -> None:
    readme = (
        "## Operational Console (`index.html`)\n"
        "OPERATOR-ORIENTED DASHBOARD with KPI Cards.\n\n"
        "## Next\n"
    )
    result = cdcc._extract_operational_console_block(readme)
    assert "operator-oriented dashboard" in result
    assert "kpi cards" in result


def test_extract_block_empty_section_returns_empty_string() -> None:
    readme = "## Operational Console (`index.html`)\n\n## Next\n"
    result = cdcc._extract_operational_console_block(readme)
    assert result.strip() == ""


# ---------------------------------------------------------------------------
# _missing_markers
# ---------------------------------------------------------------------------

def test_missing_markers_returns_empty_when_all_present() -> None:
    text = "operator-oriented dashboard with runtime health and task status"
    markers = ["operator-oriented dashboard", "runtime health", "task status"]
    result = cdcc._missing_markers(text, markers)
    assert result == []


def test_missing_markers_returns_absent_markers() -> None:
    text = "operator-oriented dashboard"
    markers = ["operator-oriented dashboard", "runtime health"]
    result = cdcc._missing_markers(text, markers)
    assert result == ["runtime health"]


def test_missing_markers_is_case_insensitive() -> None:
    text = "OPERATOR-ORIENTED DASHBOARD"
    markers = ["operator-oriented dashboard"]
    result = cdcc._missing_markers(text, markers)
    assert result == []


def test_missing_markers_marker_case_insensitive_too() -> None:
    text = "operator-oriented dashboard"
    markers = ["Operator-Oriented Dashboard"]
    result = cdcc._missing_markers(text, markers)
    assert result == []


def test_missing_markers_all_absent_returns_all() -> None:
    text = "completely unrelated content"
    markers = ["runtime health", "task status", "kpi cards"]
    result = cdcc._missing_markers(text, markers)
    assert set(result) == {"runtime health", "task status", "kpi cards"}


def test_missing_markers_empty_markers_list() -> None:
    result = cdcc._missing_markers("some text", [])
    assert result == []


def test_missing_markers_empty_text_returns_all_markers() -> None:
    markers = ["runtime health", "task status"]
    result = cdcc._missing_markers("", markers)
    assert result == markers


def test_missing_markers_partial_match_not_sufficient() -> None:
    # "runtime" alone should not satisfy "runtime health"
    text = "runtime monitoring"
    markers = ["runtime health"]
    result = cdcc._missing_markers(text, markers)
    assert result == ["runtime health"]


# ---------------------------------------------------------------------------
# main() – integration using monkeypatched file paths
# ---------------------------------------------------------------------------

def test_main_returns_zero_when_all_markers_present(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(_FULL_README_SECTION, encoding="utf-8")
    index = tmp_path / "index.html"
    index.write_text(_FULL_INDEX_HTML, encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)

    result = cdcc.main()
    assert result == 0


def test_main_returns_one_when_readme_section_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("# README\n\nNo console section.\n", encoding="utf-8")
    index = tmp_path / "index.html"
    index.write_text(_FULL_INDEX_HTML, encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)

    result = cdcc.main()
    assert result == 1


def test_main_returns_one_when_readme_marker_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # README section exists but is missing "kpi cards"
    readme_text = (
        "## Operational Console (`index.html`)\n"
        "An operator-oriented dashboard for runtime health.\n"
        "Shows task status and 24-hour throughput chart.\n"
        "Recent alert queue and copy-ready validation commands.\n"
        "Loads repository version from `package.json`.\n\n"
        "## Next\n"
    )
    readme = tmp_path / "README.md"
    readme.write_text(readme_text, encoding="utf-8")
    index = tmp_path / "index.html"
    index.write_text(_FULL_INDEX_HTML, encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)
    monkeypatch.setattr(cdcc, "README_MARKERS", ["kpi cards", "operator-oriented dashboard"])

    result = cdcc.main()
    assert result == 1


def test_main_returns_one_when_index_marker_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(_FULL_README_SECTION, encoding="utf-8")
    # index.html is missing "Recent Alerts"
    index_text = (
        '<html><head><meta name="description" content="Operational dashboard for PRGX-AG runtime health"/>'
        "</head><body>"
        "<title>Operational Dashboard</title>"
        "<!-- Task execution state from orchestrator telemetry -->"
        "<div>Records Processed (24h)</div>"
        "<div>Governance Snapshot</div>"
        "<div>quick validation commands</div>"
        '<span id="repo-version"></span>'
        "</body></html>"
    )
    index = tmp_path / "index.html"
    index.write_text(index_text, encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)

    result = cdcc.main()
    assert result == 1


def test_main_prints_pass_message_on_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(_FULL_README_SECTION, encoding="utf-8")
    index = tmp_path / "index.html"
    index.write_text(_FULL_INDEX_HTML, encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)

    cdcc.main()
    captured = capsys.readouterr()
    assert "passed" in captured.out.lower()


def test_main_prints_failure_message_when_section_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("# README\nNo console section.\n", encoding="utf-8")
    index = tmp_path / "index.html"
    index.write_text(_FULL_INDEX_HTML, encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)

    cdcc.main()
    captured = capsys.readouterr()
    assert "failed" in captured.out.lower()


def test_main_prints_missing_readme_markers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    readme_text = (
        "## Operational Console (`index.html`)\n"
        "An operator-oriented dashboard.\n\n"
        "## Next\n"
    )
    readme = tmp_path / "README.md"
    readme.write_text(readme_text, encoding="utf-8")
    index = tmp_path / "index.html"
    index.write_text(_FULL_INDEX_HTML, encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)
    # Force a missing README marker
    monkeypatch.setattr(cdcc, "README_MARKERS", ["kpi cards"])
    monkeypatch.setattr(cdcc, "INDEX_MARKERS", [])

    cdcc.main()
    captured = capsys.readouterr()
    assert "kpi cards" in captured.out


def test_main_prints_missing_index_markers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(_FULL_README_SECTION, encoding="utf-8")
    index = tmp_path / "index.html"
    index.write_text("<html></html>", encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)
    monkeypatch.setattr(cdcc, "README_MARKERS", [])
    monkeypatch.setattr(cdcc, "INDEX_MARKERS", ["Governance Snapshot"])

    cdcc.main()
    captured = capsys.readouterr()
    assert "Governance Snapshot" in captured.out


def test_main_returns_one_when_both_readme_and_index_markers_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    readme_text = (
        "## Operational Console (`index.html`)\n"
        "Minimal content.\n\n"
        "## Next\n"
    )
    readme = tmp_path / "README.md"
    readme.write_text(readme_text, encoding="utf-8")
    index = tmp_path / "index.html"
    index.write_text("<html></html>", encoding="utf-8")

    monkeypatch.setattr(cdcc, "README", readme)
    monkeypatch.setattr(cdcc, "INDEX", index)
    monkeypatch.setattr(cdcc, "README_MARKERS", ["kpi cards"])
    monkeypatch.setattr(cdcc, "INDEX_MARKERS", ["Governance Snapshot"])

    result = cdcc.main()
    assert result == 1


def test_main_uses_readme_and_index_module_constants(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Verify the module-level README and INDEX constants default to Path objects
    assert isinstance(cdcc.README, Path)
    assert isinstance(cdcc.INDEX, Path)
    assert cdcc.README.name == "README.md"
    assert cdcc.INDEX.name == "index.html"