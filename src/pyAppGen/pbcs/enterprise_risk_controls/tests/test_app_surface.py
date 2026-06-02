"""Focused app-surface tests for the enterprise_risk_controls PBC."""

from .. import agent
from .. import controls
from .. import forms
from .. import permissions
from .. import release_evidence
from .. import routes
from .. import services
from .. import ui
from .. import wizards


def test_forms_catalog_and_payload_validation():
    catalog = forms.enterprise_risk_controls_form_catalog()
    assert catalog["ok"] is True
    assert "document_instruction_intake" in catalog["form_ids"]

    valid = forms.enterprise_risk_controls_validate_form_payload(
        "document_instruction_intake",
        {
            "document_text": "Increase evidence retention for critical issues.",
            "instructions": "Update the risk runtime parameter for evidence retention.",
            "target_entity": "risk_runtime_parameter",
            "requested_action": "update",
        },
    )
    invalid = forms.enterprise_risk_controls_validate_form_payload(
        "document_instruction_intake",
        {
            "document_text": "Missing fields example.",
            "instructions": "",
            "target_entity": "not_real",
            "requested_action": "update",
        },
    )
    assert valid["ok"] is True
    assert invalid["ok"] is False
    assert "target_entity" in invalid["invalid_choices"]


def test_wizard_catalog_and_plan_are_bound_to_known_forms():
    catalog = wizards.enterprise_risk_controls_wizard_catalog()
    plan = wizards.enterprise_risk_controls_plan_wizard("risk_intake", {"risk_code": "RISK-100"})
    blocked_plan = wizards.enterprise_risk_controls_plan_wizard("risk_intake", {})

    assert catalog["ok"] is True
    assert not catalog["missing_form_bindings"]
    assert plan["ok"] is True
    assert all(step["ready"] for step in plan["steps"])
    assert any(step["blocked_by"] for step in blocked_plan["steps"][1:])


def test_controls_and_assistant_preview_are_executable():
    control_center = controls.enterprise_risk_controls_control_center()
    preview = agent.enterprise_risk_controls_assistant_preview(
        {
            "document_text": "Tighten the remediation deadline for high-severity issues.",
            "instructions": "Update the remediation parameter to 30 days.",
            "target_entity": "risk_runtime_parameter",
            "requested_action": "update",
            "payload": {"name": "critical_remediation_sla_days", "value": 30},
        }
    )

    assert control_center["ok"] is True
    assert control_center["assistant_guardrails"]["preview_only"] is True
    assert control_center["assistant_guardrails"]["boundary_ok"] is True
    assert preview["ok"] is True
    assert preview["permission"] == "enterprise_risk_controls.configure"
    assert preview["requires_confirmation"] is True
    assert preview["mutation_preview"]["boundary"]["ok"] is True


def test_service_route_ui_and_release_evidence_cover_new_app_surface():
    service_manifest = services.service_operation_manifest()
    route_contracts = routes.api_route_contracts()
    ui_contract = ui.enterprise_risk_controls_ui_contract()
    permission_manifest = permissions.permission_manifest()
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()

    assert service_manifest["ok"] is True
    assert "query_enterprise_risk_controls_controls" in service_manifest["query_operations"]
    assert "query_enterprise_risk_controls_assistant_preview" in service_manifest["query_operations"]
    assert route_contracts["ok"] is True
    assert any(item["path"].endswith("/controls") for item in route_contracts["contracts"])
    assert any(item["path"].endswith("/assistant/document-preview") for item in route_contracts["contracts"])
    assert ui_contract["ok"] is True
    assert ui_contract["forms"]
    assert ui_contract["wizards"]
    assert ui_contract["controls"]
    assert "query_enterprise_risk_controls_assistant_preview" in permission_manifest["action_permissions"]
    assert evidence["forms"]["ok"] is True
    assert evidence["wizards"]["ok"] is True
    assert evidence["controls"]["ok"] is True
    assert evidence["assistant"]["ok"] is True
    assert all(evidence["docs_present"].values())
    assert validation["ok"] is True
