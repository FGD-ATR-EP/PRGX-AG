from prgx_ag.schemas.enums import EthicalStatus
from prgx_ag.services.translation_matrix import (
    build_healing_intent,
    translate_internal_term,
    translate_status,
)


def test_translation_matrix_mappings() -> None:
    assert translate_internal_term('Parajika') == 'SYSTEM_HALT_IMMEDIATE'
    assert 'stable' in translate_status(EthicalStatus.CLEAN).lower()


def test_build_healing_intent_normalizes_parent_directory_segments() -> None:
    intent = build_healing_intent(
        {
            "summary": "dependency mismatch",
            "target": "../src/./prgx_ag/../services",
            "dependency_issues": ["version drift"],
        }
    )
    assert intent.metadata["target"] == "src/prgx_ag/services"
