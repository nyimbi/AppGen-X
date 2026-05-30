"""Focused standalone one-PBC tests for nonprofit_program_impact."""

from pathlib import Path

from .. import controls
from .. import forms
from .. import release_evidence
from .. import standalone
from .. import ui
from .. import wizards
from ..manifest import PBC_MANIFEST


def test_forms_catalog_and_payload_validation():
    catalog = forms.nonprofit_program_impact_form_catalog()
    assert catalog["ok"] is True
    assert "program_portfolio_setup" in catalog["form_ids"]

    valid = forms.nonprofit_program_impact_validate_form_payload(
        "beneficiary_enrollment",
        {
            "tenant": "tenant-smoke",
            "program_id": "PROGRAM-001",
            "beneficiary_id": "BEN-001",
            "beneficiary_type": "person",
            "age_band": "youth",
            "geography": "Nairobi",
            "vulnerability_score": 65,
            "consent_status": "consented",
        },
    )
    invalid = forms.nonprofit_program_impact_validate_form_payload(
        "assistant_document_intake",
        {
            "document_text": "Narrative memo.",
            "instructions": "",
            "target_entity": "not_real",
            "requested_action": "update",
        },
    )
    assert valid["ok"] is True
    assert invalid["ok"] is False
    assert "target_entity" in invalid["invalid_choices"]


def test_wizards_controls_and_ui_bindings_are_executable():
    smoke = standalone.nonprofit_program_impact_standalone_app_smoke()
    catalog = wizards.nonprofit_program_impact_wizard_catalog()
    plan = wizards.nonprofit_program_impact_plan_wizard(
        "beneficiary_service_journey",
        {"beneficiary_id": "BEN-001", "episode_id": "EP-001"},
    )
    blocked = wizards.nonprofit_program_impact_plan_wizard("donor_reporting_cycle", {"program_id": "PROGRAM-001"})
    control_center = controls.nonprofit_program_impact_control_center(smoke["state"])
    ui_contract = ui.nonprofit_program_impact_ui_contract()
    rendered = ui.nonprofit_program_impact_render_workbench(
        smoke["state"],
        tenant="tenant-smoke",
        principal_permissions=tuple(dict.fromkeys(ui_contract["action_permissions"].values())),
    )

    assert smoke["ok"] is True
    assert catalog["ok"] is True
    assert not catalog["missing_form_bindings"]
    assert plan["ok"] is True
    assert all(step["ready"] for step in plan["steps"])
    assert any(step["blocked_by"] for step in blocked["steps"])
    assert control_center["ok"] is True
    assert control_center["assistant_guardrails"]["preview_only"] is True
    assert rendered["ok"] is True
    assert rendered["metrics"]["program_count"] == 1


def test_standalone_contract_and_release_evidence_are_ready():
    contract = standalone.nonprofit_program_impact_standalone_app_contract()
    smoke = standalone.nonprofit_program_impact_standalone_app_smoke()
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()

    assert contract["ok"] is True
    assert smoke["ok"] is True
    assert evidence["forms"]["ok"] is True
    assert evidence["wizards"]["ok"] is True
    assert evidence["controls"]["ok"] is True
    assert evidence["assistant"]["ok"] is True
    assert evidence["standalone"]["ok"] is True
    assert all(evidence["docs_present"].values())
    assert validation["ok"] is True


def test_manifest_and_docs_reference_standalone_surface():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True

    assert "tests/test_standalone.py" in PBC_MANIFEST["tests"]
    assert "README.md" in PBC_MANIFEST["docs"]
    assert "ImpactControlCenter" in PBC_MANIFEST["ui_fragments"]
