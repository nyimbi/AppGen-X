"""Focused app-surface tests for the oil_gas_field_operations PBC."""

from .. import agent, controls, forms, permissions, release_evidence, routes, services, ui, wizards


def test_forms_catalog_and_payload_validation():
    catalog = forms.oil_gas_field_operations_form_catalog()
    assert catalog["ok"] is True
    assert "morning_review_request" in catalog["form_ids"]

    valid = forms.oil_gas_field_operations_validate_form_payload(
        "daily_production_capture",
        {
            "well_id": "OG-7H",
            "production_date": "2026-05-29",
            "oil_bbl": 140.0,
            "gas_mcf": 650.0,
            "water_bbl": 90.0,
            "gas_disposition": "sales",
            "oil_disposition": "sold",
            "measurement_basis": "allocated",
            "production_test_state": "allocation_approved",
            "downtime_hours": 1.0,
        },
    )
    invalid = forms.oil_gas_field_operations_validate_form_payload(
        "daily_production_capture",
        {
            "well_id": "OG-7H",
            "production_date": "2026-05-29",
            "oil_bbl": 140.0,
            "gas_mcf": 650.0,
            "water_bbl": 90.0,
            "gas_disposition": "not_real",
            "oil_disposition": "sold",
            "measurement_basis": "allocated",
            "production_test_state": "allocation_approved",
            "downtime_hours": 1.0,
        },
    )
    assert valid["ok"] is True
    assert invalid["ok"] is False
    assert "gas_disposition" in invalid["invalid_choices"]


def test_wizard_catalog_and_plan_are_bound_to_known_forms():
    catalog = wizards.oil_gas_field_operations_wizard_catalog()
    plan = wizards.oil_gas_field_operations_plan_wizard(
        "morning_production_review",
        {"well_id": "OG-7H", "production_date": "2026-05-29"},
    )
    blocked_plan = wizards.oil_gas_field_operations_plan_wizard("morning_production_review", {})

    assert catalog["ok"] is True
    assert not catalog["missing_form_bindings"]
    assert plan["ok"] is True
    assert all(step["ready"] for step in plan["steps"])
    assert any(step["blocked_by"] for step in blocked_plan["steps"])


def test_controls_and_assistant_preview_are_executable():
    control_center = controls.oil_gas_field_operations_control_center(
        {
            "wells": {"OG-7H": {"well_id": "OG-7H", "integrity_risk": "watch"}},
            "production_records": {
                "OG-7H:2026-05-29": {
                    "well_id": "OG-7H",
                    "production_test_state": "allocation_approved",
                    "oil_disposition": "sold",
                    "gas_disposition": "sales",
                    "deferred_oil_bbl": 14.0,
                }
            },
        }
    )
    preview = agent.oil_gas_field_operations_assistant_preview(
        {
            "document_text": "Prepare the morning route review for OG-7H.",
            "instructions": "Read only.",
            "target_entity": "production_reading",
            "requested_action": "read",
            "payload": {"well_id": "OG-7H", "production_date": "2026-05-29"},
        }
    )

    assert control_center["ok"] is True
    assert control_center["assistant_guardrails"]["preview_only"] is True
    assert control_center["assistant_guardrails"]["boundary_ok"] is True
    assert preview["ok"] is True
    assert preview["permission"] == "oil_gas_field_operations.create"
    assert preview["requires_confirmation"] is False
    assert preview["mutation_preview"]["boundary"]["ok"] is True


def test_service_route_ui_and_release_evidence_cover_new_app_surface():
    service_manifest = services.service_operation_manifest()
    route_contracts = routes.api_route_contracts()
    ui_contract = ui.oil_gas_field_operations_ui_contract()
    permission_manifest = permissions.permission_manifest()
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()

    assert service_manifest["ok"] is True
    assert "query_oil_gas_field_operations_controls" in service_manifest["query_operations"]
    assert "query_oil_gas_field_operations_assistant_preview" in service_manifest["query_operations"]
    assert route_contracts["ok"] is True
    assert any(item["path"].endswith("/controls") for item in route_contracts["contracts"])
    assert any(item["path"].endswith("/assistant/document-preview") for item in route_contracts["contracts"])
    assert ui_contract["ok"] is True
    assert ui_contract["forms"]
    assert ui_contract["wizards"]
    assert ui_contract["controls"]
    assert "oil_gas_field_operations.admin" in permission_manifest["permissions"]
    assert evidence["forms"]["ok"] is True
    assert evidence["wizards"]["ok"] is True
    assert evidence["controls"]["ok"] is True
    assert evidence["assistant"]["ok"] is True
    assert all(evidence["docs_present"].values())
    assert validation["ok"] is True
