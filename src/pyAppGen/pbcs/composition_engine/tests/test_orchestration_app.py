"""Focused orchestration-flow tests for the composition_engine slice."""

from .. import runtime


def _configure_state():
    state = runtime.composition_engine_empty_state()
    state = runtime.composition_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": runtime.COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_targets": ("web", "admin"),
            "allowed_layout_modes": ("grid", "flow"),
            "publication_mode": "side_effect_free_plan",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = runtime.composition_engine_set_parameter(state, "route_budget", 24)["state"]
    state = runtime.composition_engine_register_rule(
        state,
        {
            "rule_id": "workspace_release_rule",
            "tenant": "tenant_app",
            "scope": "workspace",
            "required_fragments": ("CompositionWorkbench",),
            "allowed_meshes": ("platform", "relationship"),
            "route_policy": "balanced",
            "requires_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    state = runtime.composition_engine_receive_event(
        state,
        {
            "event_id": "evt_schema_app",
            "event_type": "SchemaAccepted",
            "payload": {"tenant": "tenant_app", "schema_id": "CustomerProfile", "owner_pbc": "customer_360"},
        },
    )["state"]
    return state


def test_one_pbc_composition_orchestration_flow_is_executable():
    state = _configure_state()
    state = runtime.composition_engine_create_workspace(
        state,
        {
            "workspace_id": "ws_app",
            "tenant": "tenant_app",
            "name": "Customer Ops Console",
            "owner": "ops_owner",
            "target": "web",
        },
    )["state"]
    state = runtime.composition_engine_select_pbc(
        state,
        "ws_app",
        {"pbc": "customer_360", "mesh": "relationship", "reason": "customer-service operators need one bounded workbench"},
    )["state"]
    state = runtime.composition_engine_register_component(
        state,
        {
            "component_id": "cmp_ops",
            "tenant": "tenant_app",
            "pbc": "customer_360",
            "fragment": "CompositionWorkbench",
            "permissions": ("composition_engine.compose",),
            "schemas": ("CustomerProfile",),
        },
    )["state"]
    state = runtime.composition_engine_register_ui_fragment(
        state,
        {
            "fragment_id": "frag_ops",
            "tenant": "tenant_app",
            "component_id": "cmp_ops",
            "route": "/customers/ops",
            "slots": ("main",),
            "events": ("CustomerProfile",),
        },
    )["state"]
    state = runtime.composition_engine_bind_layout(
        state,
        {
            "binding_id": "bind_ops",
            "tenant": "tenant_app",
            "workspace_id": "ws_app",
            "page": "ops_home",
            "slot": "main",
            "fragment_id": "frag_ops",
            "projection": "customer_profile_projection",
        },
    )["state"]

    impact = runtime.composition_engine_preview_selection_impact(state, "ws_app", ("customer_360",))
    validation = runtime.composition_engine_validate_composition_plan(state, "ws_app")
    state = validation["state"]
    dsl = runtime.composition_engine_generate_composition_dsl(state, "ws_app")
    state = dsl["state"]
    smoke_plan = runtime.composition_engine_build_smoke_plan(state, "ws_app")
    lineage = runtime.composition_engine_build_artifact_lineage(state, "ws_app")
    documentation = runtime.composition_engine_build_documentation_matrix(state, "ws_app")
    security = runtime.composition_engine_build_security_review(state, "ws_app")
    preview = runtime.composition_engine_assistant_document_preview(
        "Compose a customer operations workbench with auditable publication steps.",
        "Preview an update to the composition workspace only.",
        action="update",
        target_table="composition_engine_composition_workspace",
    )
    rehearsal = runtime.composition_engine_release_rehearsal(state, "ws_app")
    notes = runtime.composition_engine_build_release_notes(rehearsal["state"], "ws_app")
    controls = runtime.composition_engine_build_control_center(rehearsal["state"], workspace_id="ws_app")

    assert impact["ok"] is True
    assert validation["ok"] is True
    assert dsl["ok"] is True
    assert smoke_plan["ok"] is True
    assert lineage["ok"] is True
    assert documentation["ok"] is True
    assert security["ok"] is True
    assert preview["ok"] is True
    assert preview["crud_plan"]["requires_confirmation"] is True
    assert rehearsal["ok"] is True
    assert not rehearsal["release_freeze"]
    assert notes["ok"] is True
    assert controls["ok"] is True
    assert controls["assistant_guardrails"]["crud_plan"]["boundary"]["ok"] is True
