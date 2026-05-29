"""Standalone workbench forms, wizards, controls, and datastore tests."""

from .. import controls, forms, repository, runtime, ui, wizards


def test_forms_surface_route_publication_and_configuration_without_stream_picker():
    catalog = forms.api_gateway_mesh_form_catalog()
    validation = forms.api_gateway_mesh_validate_form_payload(
        "route_publication",
        {
            "tenant": "tenant-alpha",
            "route_id": "orders-v2",
            "service_id": "svc-orders",
            "host": "api.example.com",
            "path": "/orders",
            "method": "POST",
            "protocol": "http",
            "version": "v2",
            "rollback_route_version": "v1",
            "canary_percent": 10,
            "status": "draft",
        },
    )
    invalid = forms.api_gateway_mesh_validate_form_payload(
        "configuration_change",
        {
            "database_backend": "sqlite",
            "event_topic": runtime.API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_methods": ("GET",),
            "allowed_protocols": ("http",),
            "allowed_regions": ("us-east",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )

    assert catalog["ok"] is True
    assert len(catalog["forms"]) >= 6
    assert not catalog["invalid_tables"]
    assert validation["ok"] is True
    assert validation["mutation_preview"]["event_contract"] == "AppGen-X"
    assert validation["mutation_preview"]["stream_engine_picker_visible"] is False
    assert invalid["ok"] is False
    assert invalid["invalid_choices"] == ("database_backend",)


def test_wizards_plan_onboarding_and_block_unsafe_publication_steps():
    catalog = wizards.api_gateway_mesh_wizard_catalog()
    ready_plan = wizards.api_gateway_mesh_plan_wizard(
        "service_onboarding_to_publication",
        {"service_id": "svc-orders", "route_id": "orders-v2", "identity_verified": True},
    )
    blocked_plan = wizards.api_gateway_mesh_plan_wizard(
        "service_onboarding_to_publication",
        {"service_id": "svc-orders", "route_id": "orders-v2", "identity_verified": False},
    )

    assert catalog["ok"] is True
    assert len(catalog["wizards"]) >= 3
    assert not catalog["missing_form_bindings"]
    assert ready_plan["ok"] is True
    assert all(step["ready"] for step in ready_plan["steps"])
    publish_step = next(step for step in blocked_plan["steps"] if step["step_id"] == "publish_route")
    assert publish_step["ready"] is False
    assert "identity_verified" in publish_step["blocked_by"]


def test_controls_enforce_owned_boundary_and_release_evidence():
    state = runtime.api_gateway_mesh_runtime_smoke()["state"]
    catalog = controls.api_gateway_mesh_control_catalog()
    center = controls.api_gateway_mesh_control_center(state)
    accepted = controls.api_gateway_mesh_mutation_preview("read", "service_route", {})
    rejected = controls.api_gateway_mesh_mutation_preview("update", "foreign_shared_table", {})

    assert catalog["ok"] is True
    assert len(catalog["controls"]) >= 5
    assert center["ok"] is True
    assert center["release"]["ok"] is True
    assert center["accepted_boundary"]["ok"] is True
    assert center["rejected_boundary"]["ok"] is False
    assert accepted["ok"] is True
    assert rejected["ok"] is False
    assert accepted["event_contract"] == "AppGen-X"
    assert accepted["stream_engine_picker_visible"] is False


def test_repository_persists_database_backed_gateway_state():
    smoke = repository.smoke_test()
    manifest = repository.repository_manifest()

    assert smoke["ok"] is True
    assert manifest["ok"] is True
    assert "api_gateway_mesh_service_registration" in smoke["persisted"]["persisted_tables"]
    assert smoke["services"][0]["service_id"] == "svc_smoke"
    assert smoke["routes"][0]["status"] == "published"
    assert smoke["loaded"]["configuration"]["event_contract"] == "AppGen-X"


def test_ui_exposes_forms_wizards_and_controls_in_workbench_contract():
    contract = ui.api_gateway_mesh_ui_contract()
    smoke = ui.smoke_test()

    assert contract["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]
    assert "GatewayFormsConsole" in contract["fragments"]
    assert "GatewayWizardConsole" in contract["fragments"]
    assert "GatewayControlCenter" in contract["fragments"]
    assert smoke["ok"] is True
