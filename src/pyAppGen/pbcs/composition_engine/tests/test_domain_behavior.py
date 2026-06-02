"""Executable domain behavior coverage for the Composition Engine PBC."""

from .. import agent, routes, runtime, ui
from ..repository import CompositionEngineRepository
from ..standalone import CompositionEngineStandaloneApp


TENANT = "tenant_behavior"
WORKSPACE = "ws_behavior"


def _configuration(retry_limit=3):
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
        "retry_limit": retry_limit,
        "allowed_targets": ("web", "admin", "mobile"),
        "allowed_layout_modes": ("grid", "flow", "dashboard"),
        "publication_mode": "side_effect_free_plan",
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def _configured_state():
    state = runtime.composition_engine_empty_state()
    state = runtime.composition_engine_configure_runtime(state, _configuration())["state"]
    for key, value in (
        ("max_fragments_per_page", 12),
        ("release_risk_threshold", 0.35),
        ("layout_density_target", 0.72),
        ("route_budget", 24),
        ("preview_batch_limit", 50),
    ):
        state = runtime.composition_engine_set_parameter(state, key, value)["state"]
    state = runtime.composition_engine_register_rule(
        state,
        {
            "rule_id": "composition_engine.behavior.release_gate",
            "tenant": TENANT,
            "scope": "workspace",
            "required_fragments": ("CompositionWorkbench",),
            "allowed_meshes": ("platform", "relationship", "operations"),
            "route_policy": "schema_validated",
            "requires_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    state = runtime.composition_engine_register_schema_extension(
        state, "layout_binding", {"responsive_rules": "jsonb", "preview_constraints": "jsonb"}
    )["state"]
    for event in (
        {
            "event_id": "schema_behavior",
            "event_type": "SchemaAccepted",
            "idempotency_key": "schema:behavior",
            "payload": {"tenant": TENANT, "schema_id": "CustomerProfile", "owner_pbc": "customer_360"},
        },
        {
            "event_id": "route_behavior",
            "event_type": "RoutePublished",
            "idempotency_key": "route:behavior",
            "payload": {"tenant": TENANT, "route_id": "customers_behavior", "service_id": "customer_service"},
        },
        {
            "event_id": "audit_behavior",
            "event_type": "AuditEventSealed",
            "idempotency_key": "audit:behavior",
            "payload": {"tenant": TENANT, "audit_id": "audit_behavior", "source_pbc": "audit_ledger"},
        },
        {
            "event_id": "policy_behavior",
            "event_type": "AccessPolicyChanged",
            "idempotency_key": "policy:behavior",
            "payload": {"tenant": TENANT, "policy_id": "policy_behavior", "permission": "composition_engine.publish"},
        },
    ):
        received = runtime.composition_engine_receive_event(state, event)
        assert received["ok"] is True
        state = received["state"]
    duplicate = runtime.composition_engine_receive_event(
        state,
        {
            "event_id": "schema_behavior",
            "event_type": "SchemaAccepted",
            "idempotency_key": "schema:behavior",
            "payload": {"tenant": TENANT, "schema_id": "CustomerProfile", "owner_pbc": "customer_360"},
        },
    )
    assert duplicate["duplicate"] is True
    return state


def _built_state():
    state = _configured_state()
    state = runtime.composition_engine_create_workspace(
        state,
        {
            "workspace_id": WORKSPACE,
            "tenant": TENANT,
            "name": "Customer Operations Console",
            "owner": "ops_user",
            "target": "web",
        },
    )["state"]
    state = runtime.composition_engine_select_pbc(
        state,
        WORKSPACE,
        {"pbc": "customer_360", "mesh": "relationship", "reason": "profile operations workspace"},
    )["state"]
    state = runtime.composition_engine_select_pbc(
        state,
        WORKSPACE,
        {"pbc": "workflow_orchestration", "mesh": "platform", "reason": "approval workflow stitching"},
    )["state"]
    state = runtime.composition_engine_register_component(
        state,
        {
            "component_id": "cmp_behavior_customer",
            "tenant": TENANT,
            "pbc": "customer_360",
            "fragment": "CompositionWorkbench",
            "permissions": ("composition_engine.compose", "customer_360.read"),
            "schemas": ("CustomerProfile",),
        },
    )["state"]
    state = runtime.composition_engine_register_ui_fragment(
        state,
        {
            "fragment_id": "frag_behavior_customer",
            "tenant": TENANT,
            "component_id": "cmp_behavior_customer",
            "route": "/customers/behavior",
            "slots": ("main",),
            "events": ("CustomerProfile",),
        },
    )["state"]
    state = runtime.composition_engine_bind_layout(
        state,
        {
            "binding_id": "bind_behavior_main",
            "tenant": TENANT,
            "workspace_id": WORKSPACE,
            "page": "home",
            "slot": "main",
            "fragment_id": "frag_behavior_customer",
            "projection": "customer_profile_projection",
        },
    )["state"]
    validation = runtime.composition_engine_validate_composition_plan(state, WORKSPACE)
    assert validation["ok"] is True
    state = validation["state"]
    dsl = runtime.composition_engine_generate_composition_dsl(state, WORKSPACE)
    assert dsl["ok"] is True
    assert dsl["artifact"]["dsl"]["event_contract"] == "AppGen-X"
    state = dsl["state"]
    publication = runtime.composition_engine_publish_composition(state, WORKSPACE)
    assert publication["ok"] is True
    return publication["state"]


def test_runtime_composes_workspace_dsl_release_ui_agent_and_repository_evidence():
    state = _built_state()
    impact = runtime.composition_engine_preview_selection_impact(
        state, WORKSPACE, ("customer_360", "workflow_orchestration", "audit_ledger")
    )
    workbench = runtime.composition_engine_build_workbench_view(state, tenant=TENANT)
    smoke_plan = runtime.composition_engine_build_smoke_plan(state, WORKSPACE)
    lineage = runtime.composition_engine_build_artifact_lineage(state, WORKSPACE)
    documentation = runtime.composition_engine_build_documentation_matrix(state, WORKSPACE)
    security = runtime.composition_engine_build_security_review(state, WORKSPACE)
    notes = runtime.composition_engine_build_release_notes(state, WORKSPACE)
    rehearsal = runtime.composition_engine_release_rehearsal(state, WORKSPACE)
    control_center = runtime.composition_engine_build_control_center(state, workspace_id=WORKSPACE)
    rendered = ui.composition_engine_render_workbench(
        state,
        tenant=TENANT,
        principal_permissions=(
            "composition_engine.read",
            "composition_engine.compose",
            "composition_engine.approve",
            "composition_engine.publish",
            "composition_engine.audit",
            "composition_engine.event",
            "composition_engine.configure",
        ),
    )
    document_plan = agent.document_instruction_plan(
        "Compose a customer_360 and workflow_orchestration console on page home.",
        "Preview release readiness and keep changes inside composition-owned records.",
    )
    crud_plan = agent.datastore_crud_plan(
        "update",
        "composition_engine_release_evidence",
        {"workspace_id": WORKSPACE, "status": "review"},
    )
    route_plan = agent.route_agent_request("review release readiness for the customer workspace")
    route_contract = routes.dispatch_route(
        "GET",
        "/api/pbc/composition_engine/composition/release-evidence",
        {"workspace_id": WORKSPACE},
    )
    repository = CompositionEngineRepository()
    try:
        assert repository.apply_migrations() == ("001_initial.sql",)
        synced = repository.sync_state(state)
        summary = repository.workspace_summary(tenant=TENANT)
        workspace = repository.fetch_workspace(WORKSPACE)
        outbox_rows = repository.list_rows(runtime.COMPOSITION_ENGINE_RUNTIME_TABLES[0], tenant=TENANT)
        assert synced["ok"] is True
        assert summary["workspace_count"] == 1
        assert summary["published_count"] == 1
        assert summary["release_evidence_count"] == 1
        assert workspace["workspace_id"] == WORKSPACE
        assert tuple(workspace["selected_pbcs"]) == ("customer_360", "workflow_orchestration")
        assert len(outbox_rows) >= 7
    finally:
        repository.close()
    assert impact["ok"] is True
    assert "audit_ledger" in impact["added_pbcs"]
    assert workbench["published_count"] == 1
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert smoke_plan["ok"] is True
    assert lineage["ok"] is True
    assert documentation["ok"] is True
    assert security["ok"] is True
    assert notes["ok"] is True
    assert rehearsal["ok"] is True
    assert control_center["ok"] is True
    assert rendered["ok"] is True
    assert "publish_composition" in rendered["visible_actions"]
    assert document_plan["ok"] is True
    assert document_plan["citations"]
    assert crud_plan["ok"] is True
    assert crud_plan["requires_confirmation"] is True
    assert crud_plan["event_contract"] == "AppGen-X"
    assert crud_plan["stream_engine_picker_visible"] is False
    assert route_plan["operation"] == "release_rehearsal"
    assert route_contract["ok"] is True
    assert route_contract["result"]["query"] == "build_release_evidence"


def test_standalone_app_forms_wizard_dispatch_and_controls_are_functional():
    app = CompositionEngineStandaloneApp(bootstrap=True)
    try:
        wizard = app.run_wizard(
            "bootstrap_composition",
            {
                "workspace": {
                    "tenant": TENANT,
                    "workspace_id": WORKSPACE,
                    "name": "Standalone Behavior Console",
                    "owner": "ops_user",
                    "target": "web",
                },
                "select_pbc": {
                    "pbc": "customer_360",
                    "mesh": "relationship",
                    "reason": "customer console",
                },
                "register_component": {
                    "tenant": TENANT,
                    "component_id": "cmp_standalone_behavior",
                    "pbc": "customer_360",
                    "fragment": "CompositionWorkbench",
                    "permissions": ("composition_engine.compose",),
                    "schemas": ("CustomerProfile",),
                    "fragment_id": "frag_standalone_behavior",
                    "route": "/customers/standalone-behavior",
                    "slots": ("main",),
                    "events": ("CustomerProfile",),
                },
                "bind_layout": {
                    "tenant": TENANT,
                    "binding_id": "bind_standalone_behavior",
                    "page": "home",
                    "slot": "main",
                    "fragment_id": "frag_standalone_behavior",
                    "projection": "customer_profile_projection",
                },
                "validate": {"workspace_id": WORKSPACE},
            },
        )
        dispatched = app.dispatch(
            "GET",
            "/api/pbc/composition_engine/composition/rehearsal",
            {"workspace_id": WORKSPACE},
        )
        assistant = app.assistant_preview(
            "Update release evidence for the composed customer workspace.",
            "Preview an update to the release evidence only.",
            action="update",
            target_table="composition_engine_release_evidence",
            payload={"workspace_id": WORKSPACE},
        )
        rendered = app.render_workbench(tenant=TENANT)
        controls = app.control_center(workspace_id=WORKSPACE)
        release_snapshot = app.release_snapshot()
        assert wizard["ok"] is True
        assert dispatched["ok"] is True
        assert dispatched["operation"] == "release_rehearsal"
        assert assistant["ok"] is True
        assert assistant["preview"]["requires_human_confirmation"] is True
        assert rendered["ok"] is True
        assert rendered["shell"]["database_backed"] is True
        assert WORKSPACE == app.repository.fetch_workspace(WORKSPACE)["workspace_id"]
        assert controls["ok"] is True
        assert release_snapshot["ok"] is True
        assert release_snapshot["release_evidence"]["ok"] is True
    finally:
        app.close()


def test_retry_dead_letter_boundary_and_configuration_contracts_are_enforced():
    state = runtime.composition_engine_empty_state()
    state = runtime.composition_engine_configure_runtime(state, _configuration(retry_limit=3))["state"]
    envelope = {
        "event_id": "unsupported_behavior",
        "event_type": "UnsupportedCompositionEvent",
        "idempotency_key": "unsupported:behavior",
        "payload": {"tenant": TENANT},
    }
    first = runtime.composition_engine_receive_event(state, envelope, simulate_failure=True)
    second = runtime.composition_engine_receive_event(first["state"], envelope, simulate_failure=True)
    third = runtime.composition_engine_receive_event(second["state"], envelope, simulate_failure=True)
    failed_state = third["state"]
    allowed_boundary = runtime.composition_engine_verify_owned_table_boundary(
        (
            "composition_workspace",
            "composition_engine_appgen_outbox_event",
            "SchemaAccepted",
            "gateway_composition_projection",
            "POST /audit/composition-events",
        )
    )
    blocked_boundary = runtime.composition_engine_verify_owned_table_boundary(("customer_360_internal_table",))
    assert first["handler"]["status"] == "retrying"
    assert second["handler"]["attempts"] == 2
    assert third["handler"]["status"] == "dead_letter"
    assert failed_state["dead_letter"][0]["reason"] == "unsupported_or_failed_composition_event"
    assert allowed_boundary["ok"] is True
    assert blocked_boundary["ok"] is False
    assert blocked_boundary["violations"] == ("customer_360_internal_table",)
    for payload, expected in (
        ({**_configuration(), "database_backend": "sqlite"}, "PostgreSQL, MySQL, or MariaDB"),
        ({**_configuration(), "stream_engine": "kafka"}, "AppGen-X event contract"),
        ({**_configuration(), "event_topic": "custom.topic"}, runtime.COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC),
    ):
        try:
            runtime.composition_engine_configure_runtime(runtime.composition_engine_empty_state(), payload)
        except ValueError as exc:
            assert expected in str(exc)
        else:
            raise AssertionError(f"configuration unexpectedly accepted {payload}")


def test_advanced_composition_controls_release_evidence_and_proofs_are_executable():
    smoke = runtime.composition_engine_runtime_smoke()
    state = smoke["state"]
    proof = runtime.composition_engine_generate_publication_proof(
        state, "ws_alpha", disclosure=("workspace_id", "version", "route_count")
    )
    federation = runtime.composition_engine_federate_composition_view(
        state, "ws_alpha", systems=("identity", "gateway", "schema", "workflow", "audit")
    )
    identity = runtime.composition_engine_verify_publisher_identity(
        {"did": "did:appgen:publisher-ops", "issuer": "trusted_registry", "status": "active"}
    )
    resilience = runtime.composition_engine_run_resilience_drill(state, "publication_timeout")
    crypto = runtime.composition_engine_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.composition_engine_schedule_carbon_aware_build(
        ({"window": "day", "carbon": 180}, {"window": "night", "carbon": 70})
    )
    optimized = runtime.composition_engine_optimize_layout(
        ({"slot": "main", "density": 0.8, "risk": 0.2}, {"slot": "side", "density": 0.6, "risk": 0.1})
    )
    allocation = runtime.composition_engine_allocate_fragment_slots(
        ({"fragment": "customer", "priority": 0.9}, {"fragment": "analytics", "priority": 0.5}), slots=10
    )
    anomaly = runtime.composition_engine_detect_composition_anomaly(state)
    stochastic = runtime.composition_engine_model_stochastic_release_exposure(
        release_path=(0.9, 0.95, 0.98), volatility=0.08
    )
    model = runtime.composition_engine_register_governed_model(
        "composition_risk", {"features": ("schema", "route", "layout"), "auc": 0.91, "drift_score": 0.03}
    )
    controls = runtime.composition_engine_run_control_tests(state)
    release = runtime.composition_engine_build_release_evidence()
    assert smoke["ok"] is True
    assert proof["ok"] is True
    assert proof["proof"].startswith("zk_composition_")
    assert federation["ok"] is True
    assert federation["handoffs"] == (
        "identity_composition_projection",
        "gateway_composition_projection",
        "schema_composition_projection",
        "workflow_composition_projection",
        "audit_composition_projection",
    )
    assert identity["ok"] is True
    assert resilience["mode"] == "degraded_composition_publication"
    assert crypto["epoch"] == 2
    assert carbon["window"] == "night"
    assert optimized["slot"] == "side"
    assert allocation["allocations"][0]["slots"] > allocation["allocations"][1]["slots"]
    assert anomaly["entropy"] >= 0
    assert stochastic["tail_risk"] > 0
    assert model["governance"]["drift_score"] < 0.05
    assert controls["ok"] is True
    assert controls["hash_chain_valid"] is True
    assert release["ok"] is True
    assert release["api"]["event_contract"] == "AppGen-X"
    assert release["api"]["stream_engine_picker_visible"] is False
    assert release["schema"]["datastore_backends"] == runtime.COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
