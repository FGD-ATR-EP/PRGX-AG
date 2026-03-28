import pytest

from prgx_ag.config import RUNTIME_PROFILES, RuntimeProfile, Settings


def test_runtime_profiles_have_distinct_controls() -> None:
    development = RUNTIME_PROFILES['development']
    staging = RUNTIME_PROFILES['staging']
    production = RUNTIME_PROFILES['production']

    assert development.max_auto_fix_items > staging.max_auto_fix_items > production.max_auto_fix_items
    assert development.max_issue_count_for_auto_fix > staging.max_issue_count_for_auto_fix > production.max_issue_count_for_auto_fix
    assert production.audit_verbosity == 'forensic'


def test_settings_exposes_profile() -> None:
    settings = Settings(PRGX_RUNTIME_PROFILE='staging')
    assert settings.profile.name == 'staging'
    assert settings.profile.evidence_signature_required is True


def test_settings_default_runtime_profile_is_development() -> None:
    settings = Settings()
    assert settings.runtime_profile == 'development'
    assert settings.profile.name == 'development'


def test_settings_audit_window_hours_default_is_24() -> None:
    settings = Settings()
    assert settings.audit_window_hours == 24


def test_settings_medical_findings_path_default() -> None:
    settings = Settings()
    assert settings.medical_findings_path == '.prgx-ag/evidence/medical_research_findings.json'


def test_settings_profile_development_fields() -> None:
    settings = Settings(PRGX_RUNTIME_PROFILE='development')
    profile = settings.profile
    assert profile.name == 'development'
    assert profile.max_auto_fix_items == 20
    assert profile.max_issue_count_for_auto_fix == 60
    assert profile.audit_verbosity == 'compact'
    assert profile.evidence_signature_required is False


def test_settings_profile_production_fields() -> None:
    settings = Settings(PRGX_RUNTIME_PROFILE='production')
    profile = settings.profile
    assert profile.name == 'production'
    assert profile.max_auto_fix_items == 5
    assert profile.max_issue_count_for_auto_fix == 12
    assert profile.audit_verbosity == 'forensic'
    assert profile.evidence_signature_required is True


def test_runtime_profile_all_audit_verbosities_distinct() -> None:
    verbosities = {p.audit_verbosity for p in RUNTIME_PROFILES.values()}
    assert verbosities == {'compact', 'standard', 'forensic'}


@pytest.mark.parametrize(
    ('profile_name', 'expected_sig_required'),
    [
        ('development', False),
        ('staging', True),
        ('production', True),
    ],
)
def test_runtime_profile_evidence_signature_requirements(
    profile_name: str, expected_sig_required: bool
) -> None:
    profile = RUNTIME_PROFILES[profile_name]  # type: ignore[literal-required]
    assert profile.evidence_signature_required is expected_sig_required


def test_settings_audit_window_hours_boundary_minimum() -> None:
    settings = Settings(PRGX_AUDIT_WINDOW_HOURS='1')
    assert settings.audit_window_hours == 1


def test_settings_audit_window_hours_custom_value() -> None:
    settings = Settings(PRGX_AUDIT_WINDOW_HOURS='48')
    assert settings.audit_window_hours == 48


def test_runtime_profile_is_pydantic_model() -> None:
    dev = RUNTIME_PROFILES['development']
    assert isinstance(dev, RuntimeProfile)


def test_all_profile_names_match_keys() -> None:
    for key, profile in RUNTIME_PROFILES.items():
        assert profile.name == key