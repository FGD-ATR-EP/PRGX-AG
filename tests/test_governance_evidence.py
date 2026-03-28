import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from prgx_ag.services.governance_evidence import (
    append_audit_event,
    create_signed_governance_evidence_bundle,
)


def test_governance_evidence_bundle_is_signed(tmp_path: Path) -> None:
    repo_root = tmp_path
    (repo_root / '.prgx-ag/audit').mkdir(parents=True)
    (repo_root / '.prgx-ag/evidence').mkdir(parents=True)
    (repo_root / '.prgx-ag/evidence/medical_research_findings.json').write_text(
        json.dumps([{'id': 'med-1', 'summary': 'finding'}]),
        encoding='utf-8',
    )

    append_audit_event(
        repo_root / '.prgx-ag/audit/audit_log.jsonl',
        event='porisjem.fix_completed',
        actor='PRGX2',
        details={'envelope_id': 'abc', 'verification_status': 'passed'},
    )

    path = create_signed_governance_evidence_bundle(
        repo_root,
        audit_window_hours=24,
        fix_plan_metadata={'envelope_id': 'abc', 'fix_count': 1},
        medical_findings_path='.prgx-ag/evidence/medical_research_findings.json',
        profile_name='staging',
    )

    payload = json.loads(path.read_text(encoding='utf-8'))
    assert payload['profile'] == 'staging'
    assert payload['fix_plan_metadata']['fix_count'] == 1
    assert payload['audit_records']
    assert payload['medical_research_findings']
    assert payload['signature']['algorithm'] == 'sha256'


# ---------------------------------------------------------------------------
# append_audit_event tests
# ---------------------------------------------------------------------------

def test_append_audit_event_creates_parent_directory(tmp_path: Path) -> None:
    log_path = tmp_path / 'deep' / 'nested' / 'audit_log.jsonl'
    assert not log_path.parent.exists()

    append_audit_event(log_path, event='test.event', actor='PRGX1', details={})

    assert log_path.parent.exists()
    assert log_path.exists()


def test_append_audit_event_fields_are_correct(tmp_path: Path) -> None:
    log_path = tmp_path / 'audit_log.jsonl'
    append_audit_event(
        log_path,
        event='test.created',
        actor='PRGX3',
        details={'key': 'value', 'count': 42},
    )

    record = json.loads(log_path.read_text(encoding='utf-8').strip())
    assert record['event'] == 'test.created'
    assert record['actor'] == 'PRGX3'
    assert record['details'] == {'key': 'value', 'count': 42}
    assert 'ts' in record
    # ts must be a parseable ISO timestamp
    datetime.fromisoformat(record['ts'])


def test_append_audit_event_appends_multiple_entries(tmp_path: Path) -> None:
    log_path = tmp_path / 'audit_log.jsonl'
    for i in range(3):
        append_audit_event(log_path, event=f'event.{i}', actor='PRGX2', details={'i': i})

    lines = [l for l in log_path.read_text(encoding='utf-8').splitlines() if l.strip()]
    assert len(lines) == 3
    events = [json.loads(l)['event'] for l in lines]
    assert events == ['event.0', 'event.1', 'event.2']


# ---------------------------------------------------------------------------
# create_signed_governance_evidence_bundle tests
# ---------------------------------------------------------------------------

def test_bundle_with_missing_audit_log_returns_empty_records(tmp_path: Path) -> None:
    # No audit log created; bundle should still succeed with empty audit_records
    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=24,
        fix_plan_metadata={'envelope_id': 'x'},
        medical_findings_path='.prgx-ag/evidence/medical_research_findings.json',
        profile_name='development',
    )
    payload = json.loads(path.read_text(encoding='utf-8'))
    assert payload['audit_records'] == []


def test_bundle_with_missing_medical_findings_returns_empty_list(tmp_path: Path) -> None:
    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=24,
        fix_plan_metadata={'envelope_id': 'x'},
        medical_findings_path='nonexistent/medical.json',
        profile_name='production',
    )
    payload = json.loads(path.read_text(encoding='utf-8'))
    assert payload['medical_research_findings'] == []


def test_bundle_creates_compliance_directory(tmp_path: Path) -> None:
    compliance_dir = tmp_path / '.prgx-ag' / 'artifacts' / 'compliance'
    assert not compliance_dir.exists()

    create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=24,
        fix_plan_metadata={},
        medical_findings_path='nonexistent.json',
        profile_name='staging',
    )

    assert compliance_dir.exists()
    assert any(compliance_dir.iterdir())


def test_bundle_signature_is_sha256_of_canonical_payload(tmp_path: Path) -> None:
    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=12,
        fix_plan_metadata={'envelope_id': 'abc', 'fix_count': 2},
        medical_findings_path='nonexistent.json',
        profile_name='production',
    )
    bundle = json.loads(path.read_text(encoding='utf-8'))

    # Reconstruct the canonical payload (same fields, no signature key)
    signature_block = bundle.pop('signature')
    canonical = json.dumps(bundle, ensure_ascii=False, sort_keys=True)
    expected_digest = hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    assert signature_block['algorithm'] == 'sha256'
    assert signature_block['digest'] == expected_digest


def test_bundle_stores_profile_name_and_window(tmp_path: Path) -> None:
    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=48,
        fix_plan_metadata={},
        medical_findings_path='nonexistent.json',
        profile_name='production',
    )
    payload = json.loads(path.read_text(encoding='utf-8'))
    assert payload['profile'] == 'production'
    assert payload['audit_window_hours'] == 48


def test_bundle_excludes_old_audit_records(tmp_path: Path) -> None:
    audit_log = tmp_path / '.prgx-ag' / 'audit' / 'audit_log.jsonl'
    audit_log.parent.mkdir(parents=True)

    # Write a record with a very old timestamp (48 hours ago)
    old_ts = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    recent_ts = datetime.now(timezone.utc).isoformat()

    old_record = json.dumps({'ts': old_ts, 'event': 'old.event', 'actor': 'X', 'details': {}})
    recent_record = json.dumps({'ts': recent_ts, 'event': 'recent.event', 'actor': 'Y', 'details': {}})
    audit_log.write_text(old_record + '\n' + recent_record + '\n', encoding='utf-8')

    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=24,
        fix_plan_metadata={},
        medical_findings_path='nonexistent.json',
        profile_name='development',
    )
    payload = json.loads(path.read_text(encoding='utf-8'))
    events = [r['event'] for r in payload['audit_records']]
    assert 'recent.event' in events
    assert 'old.event' not in events


def test_bundle_skips_malformed_json_lines_in_audit_log(tmp_path: Path) -> None:
    audit_log = tmp_path / '.prgx-ag' / 'audit' / 'audit_log.jsonl'
    audit_log.parent.mkdir(parents=True)

    recent_ts = datetime.now(timezone.utc).isoformat()
    good_record = json.dumps({'ts': recent_ts, 'event': 'good.event', 'actor': 'A', 'details': {}})
    audit_log.write_text(
        'NOT VALID JSON\n' + good_record + '\n' + '{broken\n',
        encoding='utf-8',
    )

    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=24,
        fix_plan_metadata={},
        medical_findings_path='nonexistent.json',
        profile_name='staging',
    )
    payload = json.loads(path.read_text(encoding='utf-8'))
    assert len(payload['audit_records']) == 1
    assert payload['audit_records'][0]['event'] == 'good.event'


def test_bundle_skips_audit_records_without_ts_field(tmp_path: Path) -> None:
    audit_log = tmp_path / '.prgx-ag' / 'audit' / 'audit_log.jsonl'
    audit_log.parent.mkdir(parents=True)

    recent_ts = datetime.now(timezone.utc).isoformat()
    no_ts = json.dumps({'event': 'no.ts', 'actor': 'A', 'details': {}})
    with_ts = json.dumps({'ts': recent_ts, 'event': 'with.ts', 'actor': 'B', 'details': {}})
    audit_log.write_text(no_ts + '\n' + with_ts + '\n', encoding='utf-8')

    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=24,
        fix_plan_metadata={},
        medical_findings_path='nonexistent.json',
        profile_name='development',
    )
    payload = json.loads(path.read_text(encoding='utf-8'))
    events = [r['event'] for r in payload['audit_records']]
    assert 'with.ts' in events
    assert 'no.ts' not in events


def test_bundle_includes_compliance_statement(tmp_path: Path) -> None:
    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=24,
        fix_plan_metadata={},
        medical_findings_path='nonexistent.json',
        profile_name='staging',
    )
    payload = json.loads(path.read_text(encoding='utf-8'))
    assert 'compliance_statement' in payload
    assert len(payload['compliance_statement']) > 0


def test_bundle_returns_valid_path_that_exists(tmp_path: Path) -> None:
    path = create_signed_governance_evidence_bundle(
        tmp_path,
        audit_window_hours=24,
        fix_plan_metadata={'test': True},
        medical_findings_path='nonexistent.json',
        profile_name='development',
    )
    assert isinstance(path, Path)
    assert path.exists()
    assert path.suffix == '.json'