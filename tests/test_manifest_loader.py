from pathlib import Path

import pytest

from prgx_ag.services.manifest_loader import ManifestLoader


def test_manifest_loader_reads_expected_structure(tmp_path: Path) -> None:
    manifest = tmp_path / '.prgx-ag/manifests/expected_structure.yaml'
    manifest.parent.mkdir(parents=True)
    manifest.write_text('paths:\n  - src\n', encoding='utf-8')
    loader = ManifestLoader(tmp_path)
    data = loader.load_expected_structure()
    assert data['paths'] == ['src']


def test_manifest_loader_reads_dependency_policy(tmp_path: Path) -> None:
    manifest = tmp_path / '.prgx-ag/allowlists/dependency_policy.yaml'
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        'manifest_rules:\n'
        '  pyproject.toml:\n'
        '    allowed_packages:\n'
        '      - pydantic\n'
        'packages:\n'
        '  pydantic:\n'
        '    allowed_range: ">=2.6,<3"\n'
        '    bump_policy: minor-only\n',
        encoding='utf-8',
    )
    loader = ManifestLoader(tmp_path)
    data = loader.load_dependency_policy()
    assert data['packages']['pydantic']['allowed_range'] == '>=2.6,<3'


def test_manifest_loader_raises_for_missing_manifest(tmp_path: Path) -> None:
    loader = ManifestLoader(tmp_path)
    with pytest.raises(FileNotFoundError):
        loader.load_expected_structure()


def test_manifest_loader_raises_for_non_mapping_yaml(tmp_path: Path) -> None:
    manifest = tmp_path / '.prgx-ag/manifests/expected_structure.yaml'
    manifest.parent.mkdir(parents=True)
    manifest.write_text('- src\n- tests\n', encoding='utf-8')

    loader = ManifestLoader(tmp_path)
    with pytest.raises(ValueError):
        loader.load_expected_structure()
