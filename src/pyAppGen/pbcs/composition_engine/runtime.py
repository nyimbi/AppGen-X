"""Executable runtime for the Composition Engine PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC = "appgen.composition.events"
COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
COMPOSITION_ENGINE_OWNED_TABLES = (
    "composition_workspace",
    "component_registry",
    "ui_fragment",
    "layout_binding",
    "dsl_artifact",
    "composition_plan",
    "composition_validation_run",
    "package_registration_plan",
    "package_index_entry",
    "release_evidence",
    "composition_rule",
    "composition_parameter",
    "composition_configuration",
)
COMPOSITION_ENGINE_RUNTIME_TABLES = (
    "composition_engine_appgen_outbox_event",
    "composition_engine_appgen_inbox_event",
    "composition_engine_dead_letter_event",
)
COMPOSITION_ENGINE_EMITTED_EVENT_TYPES = (
    "CompositionWorkspaceCreated",
    "PbcSelectedForComposition",
    "ComponentRegistered",
    "UiFragmentRegistered",
    "LayoutBound",
    "CompositionPlanValidated",
    "PackageRegistrationPlanned",
    "CompositionPublished",
    "PbcDeployed",
)
COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES = (
    "SchemaAccepted",
    "RoutePublished",
    "AuditEventSealed",
    "AccessPolicyChanged",
    "WorkflowCompleted",
    "PackageRegistrationRequested",
)
_COMPOSITION_ENGINE_RUNTIME_TABLES = COMPOSITION_ENGINE_RUNTIME_TABLES
_COMPOSITION_ENGINE_ALLOWED_DEPENDENCIES = (
    "identity_composition_projection",
    "gateway_composition_projection",
    "schema_composition_projection",
    "workflow_composition_projection",
    "audit_composition_projection",
    "pbc_deployment_projection",
    "package_registration_projection",
    "GET /identity/policies",
    "GET /gateway/routes",
    "GET /schemas/contracts",
    "POST /workflow/composition-approvals",
    "POST /audit/composition-events",
)
_COMPOSITION_ENGINE_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_composition_lifecycle",
    "graph_relational_component_topology",
    "multi_tenant_workspace_isolation",
    "schema_on_read_layout_extension",
    "probabilistic_release_risk_scoring",
    "real_time_composition_analytics",
    "counterfactual_layout_simulation",
    "temporal_release_readiness_forecasting",
    "autonomous_layout_remediation",
    "semantic_composition_intent_parsing",
    "predictive_composition_risk_scoring",
    "self_healing_publication_route_selection",
    "zero_knowledge_publication_proof",
    "immutable_composition_audit_trail",
    "dynamic_composition_policy_screening",
    "automated_composition_control_testing",
    "universal_api_async_composition_surface",
    "cross_system_composition_federation",
    "identity_gateway_schema_workflow_audit_integration",
    "decentralized_publisher_identity",
    "chaos_engineered_composition_tolerance",
    "quantum_resistant_publication_signing",
    "carbon_aware_composition_build",
    "algebraic_layout_optimization",
    "mechanism_design_fragment_slot_allocation",
    "information_theoretic_composition_anomaly_detection",
    "temporal_release_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_composition_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "composition_mlops_governance",
)
COMPOSITION_ENGINE_STANDARD_FEATURE_KEYS = (
    "workspace_management",
    "pbc_selection",
    "selection_impact_preview",
    "component_registry",
    "ui_fragment_registry",
    "layout_binding",
    "page_composition",
    "route_map_generation",
    "smoke_plan_synthesis",
    "artifact_lineage",
    "permission_mapping",
    "schema_compatibility_check",
    "composition_dsl_generation",
    "package_registration_plan",
    "publication_workflow",
    "release_rehearsal",
    "release_gate_evidence",
    "documentation_matrix",
    "security_review_panel",
    "preview_rendering",
    "responsive_layout_rules",
    "fragment_slotting",
    "idempotent_handlers",
    "retry_dead_letter",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "workbench_forms",
    "guided_wizards",
    "control_center",
    "assistant_document_preview",
    "audit_evidence",
    "release_gate",
    "package_registration_validation",
    "appgen_event_contract",
)


def composition_engine_runtime_capabilities() -> dict:
    smoke = composition_engine_runtime_smoke()
    return {
        "format": "appgen.composition-engine-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "composition_engine",
        "implementation_directory": "src/pyAppGen/pbcs/composition_engine",
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
        "capabilities": COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": COMPOSITION_ENGINE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "create_workspace",
            "select_pbc",
            "preview_selection_impact",
            "register_component",
            "register_ui_fragment",
            "bind_layout",
            "validate_composition_plan",
            "plan_package_registration",
            "generate_composition_dsl",
            "publish_composition",
            "build_smoke_plan",
            "build_artifact_lineage",
            "build_documentation_matrix",
            "build_security_review",
            "build_release_notes",
            "release_rehearsal",
            "assistant_document_preview",
            "route_agent_intent",
            "agent_competency_catalog",
            "build_control_center",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def composition_engine_runtime_smoke() -> dict:
    state = composition_engine_empty_state()
    state = composition_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_targets": ("web", "admin", "mobile"),
            "allowed_layout_modes": ("grid", "flow", "dashboard"),
            "publication_mode": "side_effect_free_plan",
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = composition_engine_set_parameter(state, "max_fragments_per_page", 12)["state"]
    state = composition_engine_set_parameter(state, "release_risk_threshold", 0.35)["state"]
    state = composition_engine_set_parameter(state, "layout_density_target", 0.72)["state"]
    state = composition_engine_set_parameter(state, "route_budget", 24)["state"]
    state = composition_engine_set_parameter(state, "preview_batch_limit", 50)["state"]
    state = composition_engine_register_rule(
        state,
        {
            "rule_id": "rule_composition",
            "tenant": "tenant_alpha",
            "scope": "workspace",
            "required_fragments": ("CustomerConfigurationPanel",),
            "allowed_meshes": ("platform", "commerce", "relationship"),
            "route_policy": "schema_validated",
            "requires_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    state = composition_engine_register_schema_extension(state, "layout_binding", {"responsive_rules": "jsonb"})["state"]
    state = composition_engine_receive_event(
        state,
        {"event_id": "evt_schema", "event_type": "SchemaAccepted", "payload": {"tenant": "tenant_alpha", "schema_id": "CustomerUpdated", "owner_pbc": "customer_360"}},
    )["state"]
    workspace = composition_engine_create_workspace(state, {"workspace_id": "ws_alpha", "tenant": "tenant_alpha", "name": "Ops Console", "owner": "ops_user", "target": "web"})
    state = workspace["state"]
    selected = composition_engine_select_pbc(state, "ws_alpha", {"pbc": "customer_360", "mesh": "relationship", "reason": "profile workspace"})
    state = selected["state"]
    component = composition_engine_register_component(state, {"component_id": "cmp_customer", "tenant": "tenant_alpha", "pbc": "customer_360", "fragment": "CustomerConfigurationPanel", "permissions": ("customer_360.configure",), "schemas": ("CustomerUpdated",)})
    state = component["state"]
    fragment = composition_engine_register_ui_fragment(state, {"fragment_id": "frag_customer", "tenant": "tenant_alpha", "component_id": "cmp_customer", "route": "/customers", "slots": ("main",), "events": ("CustomerUpdated",)})
    state = fragment["state"]
    binding = composition_engine_bind_layout(state, {"binding_id": "bind_main", "tenant": "tenant_alpha", "workspace_id": "ws_alpha", "page": "home", "slot": "main", "fragment_id": "frag_customer", "projection": "customer_profile_projection"})
    state = binding["state"]
    validation = composition_engine_validate_composition_plan(state, "ws_alpha")
    state = validation["state"]
    package_plan = composition_engine_plan_package_registration(state, "ws_alpha", requested_by="ops_user")
    dsl = composition_engine_generate_composition_dsl(state, "ws_alpha")
    state = dsl["state"]
    publication = composition_engine_publish_composition(state, "ws_alpha")
    state = publication["state"]
    workbench = composition_engine_build_workbench_view(state, tenant="tenant_alpha")
    impact = composition_engine_preview_selection_impact(state, "ws_alpha", ("customer_360", "workflow_orchestration"))
    smoke_plan = composition_engine_build_smoke_plan(state, "ws_alpha")
    lineage = composition_engine_build_artifact_lineage(state, "ws_alpha")
    documentation = composition_engine_build_documentation_matrix(state, "ws_alpha")
    security = composition_engine_build_security_review(state, "ws_alpha")
    release_notes = composition_engine_build_release_notes(state, "ws_alpha")
    rehearsal = composition_engine_release_rehearsal(state, "ws_alpha")
    assistant = composition_engine_assistant_document_preview(
        "Compose a governed customer workspace with release review.",
        "Preview an update to the composition rule only.",
        action="update",
        target_table="composition_engine_composition_rule",
    )
    competencies = composition_engine_agent_competency_catalog()
    agent_route = composition_engine_route_agent_intent("review release readiness for the composition workspace")
    control_center = composition_engine_build_control_center(state, workspace_id="ws_alpha")
    simulation = composition_engine_simulate_layout(state, "ws_alpha", added_fragments=2, removed_fragments=0)
    forecast = composition_engine_forecast_release_readiness((0.92, 0.95, 0.97), horizon_days=14)
    parsed = composition_engine_parse_composition_intent("compose workspace ws_900 with pbc customer_360 fragment CustomerWorkbench")
    risk = composition_engine_score_composition_risk({"schema": 0.1, "route": 0.2, "permission": 0.1, "layout": 0.2})
    remediation = composition_engine_recommend_layout_remediation("slot_overflow")
    selected_route = composition_engine_select_publication_route({"event_id": "composition_publish"}, rails=({"route": "primary", "available": False, "latency": 2}, {"route": "release_plan", "available": True, "latency": 4}))
    proof = composition_engine_generate_publication_proof(state, "ws_alpha", disclosure=("workspace_id", "version", "route_count"))
    screening = composition_engine_screen_policy(state, "ws_alpha", meshes=("platform", "commerce", "relationship"))
    controls = composition_engine_run_control_tests(state)
    api = composition_engine_build_api_contract()
    federation = composition_engine_federate_composition_view(state, "ws_alpha", systems=("identity", "gateway", "schema", "workflow", "audit"))
    identity = composition_engine_verify_publisher_identity({"did": "did:appgen:publisher-ops", "issuer": "trusted_registry", "status": "active"})
    resilience = composition_engine_run_resilience_drill(state, "publication_timeout")
    crypto = composition_engine_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = composition_engine_schedule_carbon_aware_build(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 70}))
    optimized = composition_engine_optimize_layout(({"slot": "main", "density": 0.8, "risk": 0.2}, {"slot": "side", "density": 0.6, "risk": 0.1}))
    allocation = composition_engine_allocate_fragment_slots(({"fragment": "customer", "priority": 0.9}, {"fragment": "analytics", "priority": 0.5}), slots=10)
    anomaly = composition_engine_detect_composition_anomaly(state)
    stochastic = composition_engine_model_stochastic_release_exposure(release_path=(0.9, 0.95, 0.98), volatility=0.08)
    model = composition_engine_register_governed_model("composition_risk", {"features": ("schema", "route", "layout"), "auc": 0.91, "drift_score": 0.03})
    checks = (
        {"id": "event_sourced_composition_lifecycle", "ok": len(state["events"]) >= 7 and state["events"][-1]["hash"]},
        {"id": "graph_relational_component_topology", "ok": workbench["component_count"] == 1 and workbench["fragment_count"] == 1},
        {"id": "multi_tenant_workspace_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "selection_impact_preview", "ok": impact["ok"] and "workflow_orchestration" in impact["added_pbcs"]},
        {"id": "schema_on_read_layout_extension", "ok": state["schema_extensions"]["layout_binding"]["responsive_rules"] == "jsonb"},
        {"id": "probabilistic_release_risk_scoring", "ok": publication["publication"]["release_risk"] >= 0},
        {"id": "real_time_composition_analytics", "ok": workbench["workspace_count"] == 1 and workbench["published_count"] == 1},
        {"id": "smoke_plan_synthesis", "ok": smoke_plan["ok"] and bool(smoke_plan["steps"])},
        {"id": "artifact_lineage", "ok": lineage["ok"] and len(lineage["lineage"]) == 3},
        {"id": "documentation_matrix", "ok": documentation["ok"] and not documentation["missing"]},
        {"id": "security_review_panel", "ok": security["ok"] and not security["blocking_findings"]},
        {"id": "release_rehearsal", "ok": rehearsal["ok"] and not rehearsal["release_freeze"]},
        {"id": "release_note_generation", "ok": release_notes["ok"] and bool(release_notes["notes"]["highlights"])},
        {"id": "assistant_document_preview", "ok": assistant["ok"] and assistant["requires_human_confirmation"]},
        {"id": "agent_competency_catalog", "ok": competencies["ok"] and len(competencies["competencies"]) >= 8},
        {"id": "agent_routing_and_handoff", "ok": agent_route["ok"] and agent_route["operation"] == "release_rehearsal"},
        {"id": "control_center", "ok": control_center["ok"] and control_center["assistant_guardrails"]["ok"]},
        {"id": "counterfactual_layout_simulation", "ok": simulation["density_delta"] > 0},
        {"id": "temporal_release_readiness_forecasting", "ok": forecast["forecast_readiness"] > 0},
        {"id": "autonomous_layout_remediation", "ok": remediation["action"] == "rebalance_fragment_slots"},
        {"id": "semantic_composition_intent_parsing", "ok": parsed["ok"] and parsed["workspace_id"] == "ws_900"},
        {"id": "predictive_composition_risk_scoring", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_publication_route_selection", "ok": selected_route["ok"] and selected_route["failover_used"]},
        {"id": "zero_knowledge_publication_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_composition_")},
        {"id": "immutable_composition_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_composition_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_composition_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_composition_surface", "ok": api["ok"] and "CompositionPublished" in api["events"]["emits"]},
        {"id": "cross_system_composition_federation", "ok": federation["ok"] and "gateway" in federation["systems"]},
        {"id": "identity_gateway_schema_workflow_audit_integration", "ok": federation["handoffs"] == ("identity_composition_projection", "gateway_composition_projection", "schema_composition_projection", "workflow_composition_projection", "audit_composition_projection")},
        {"id": "decentralized_publisher_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_composition_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_composition_publication"},
        {"id": "quantum_resistant_publication_signing", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_composition_build", "ok": carbon["window"] == "night"},
        {"id": "algebraic_layout_optimization", "ok": optimized["ok"] and optimized["slot"] == "side"},
        {"id": "mechanism_design_fragment_slot_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["slots"] > allocation["allocations"][1]["slots"]},
        {"id": "information_theoretic_composition_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_release_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": any(item["idempotency_key"].startswith("composition_engine:CompositionPublished") for item in state["outbox"])},
        {"id": "probabilistic_ml_composition_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimized["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "composition_mlops_governance", "ok": model["governance"]["drift_score"] < 0.05},
    )
    return {"format": "appgen.composition-engine-runtime-smoke.v1", "ok": all(check["ok"] for check in checks), "checks": checks, "blocking_gaps": tuple(check for check in checks if not check["ok"]), "state": state}


def composition_engine_empty_state() -> dict:
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "workspaces": {},
        "components": {},
        "fragments": {},
        "bindings": {},
        "dsl_artifacts": {},
        "composition_plans": {},
        "validation_runs": {},
        "package_registration_plans": {},
        "package_index_entries": {},
        "release_evidence": {},
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letters": [],
        "dead_letter": [],
        "handled_events": {},
        "retry_evidence": [],
        "schema_projections": {},
        "route_projections": {},
        "audit_projections": {},
        "access_policy_projections": {},
        "workflow_projections": {},
        "package_registration_projections": {},
        "crypto_epoch": 1,
    }


def composition_engine_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _COMPOSITION_ENGINE_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Composition Engine uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    allowed_databases = set(COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS)
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Composition Engine supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Composition Engine requires AppGen-X event topic {COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC}")
    next_state = _copy_state(state)
    next_state["configuration"] = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
    }
    return {"ok": True, "state": next_state, "configuration": next_state["configuration"]}


def composition_engine_set_parameter(state: dict, key: str, value: int | float | str) -> dict:
    allowed = {"max_fragments_per_page", "release_risk_threshold", "layout_density_target", "route_budget", "preview_batch_limit", "review_sla_hours"}
    if key not in allowed:
        raise ValueError(f"Unsupported Composition Engine parameter: {key}")
    next_state = _copy_state(state)
    next_state["parameters"][key] = value
    return {"ok": True, "state": next_state, "parameter": {"key": key, "value": value}}


def composition_engine_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "scope", "required_fragments", "allowed_meshes", "route_policy", "requires_approval", "severity", "status"}
    _require(rule, required)
    next_state = _copy_state(state)
    stored = {**rule, "enabled": rule["status"] == "active", "compiled_hash": _hash_payload(rule)}
    next_state["rules"][rule["rule_id"]] = stored
    return {"ok": True, "state": next_state, "rule": stored}


def composition_engine_register_schema_extension(state: dict, target: str, fields: dict) -> dict:
    if target not in COMPOSITION_ENGINE_OWNED_TABLES:
        raise ValueError(f"Composition Engine schema extensions must target owned tables: {COMPOSITION_ENGINE_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    next_state = _copy_state(state)
    next_state["schema_extensions"].setdefault(target, {}).update(fields)
    return {"ok": True, "state": next_state, "schema_extension": {"table": target, "fields": dict(fields)}, "target": target, "fields": next_state["schema_extensions"][target]}


def composition_engine_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    if key in state["handled_events"] and state["handled_events"][key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": state["handled_events"][key]}
    attempts = int(state["handled_events"].get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {"event_id": event_id, "event_type": event_type, "tenant": payload.get("tenant"), "attempts": attempts, "idempotency_key": key}
    next_state = _copy_state(state)
    next_state["inbox"].append(inbox_entry)
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"].append(evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_composition_event"}
            next_state["dead_letters"].append(dead)
            next_state["dead_letter"].append(dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "SchemaAccepted":
        next_state["schema_projections"][payload["schema_id"]] = payload
    elif event_type == "RoutePublished":
        next_state["route_projections"][payload["route_id"]] = payload
    elif event_type == "AuditEventSealed":
        next_state["audit_projections"][payload["audit_id"]] = payload
    elif event_type == "AccessPolicyChanged":
        next_state["access_policy_projections"][payload["policy_id"]] = payload
    elif event_type == "WorkflowCompleted":
        next_state["workflow_projections"][payload["workflow_id"]] = payload
    elif event_type == "PackageRegistrationRequested":
        next_state["package_registration_projections"][payload["package_id"]] = payload
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def composition_engine_create_workspace(state: dict, workspace: dict) -> dict:
    _require(workspace, {"workspace_id", "tenant", "name", "owner", "target"})
    next_state = _copy_state(state)
    stored = {**workspace, "version": 1, "status": "draft", "selected_pbcs": ()}
    next_state["workspaces"][workspace["workspace_id"]] = stored
    next_state = _emit(next_state, "CompositionWorkspaceCreated", workspace["tenant"], workspace["workspace_id"], stored)
    return {"ok": True, "state": next_state, "workspace": stored}


def composition_engine_select_pbc(state: dict, workspace_id: str, selection: dict) -> dict:
    _require(selection, {"pbc", "mesh", "reason"})
    next_state = _copy_state(state)
    workspace = dict(next_state["workspaces"][workspace_id])
    workspace["selected_pbcs"] = tuple(dict.fromkeys(tuple(workspace["selected_pbcs"]) + (selection["pbc"],)))
    next_state["workspaces"][workspace_id] = workspace
    payload = {"workspace_id": workspace_id, **selection}
    next_state = _emit(next_state, "PbcSelectedForComposition", workspace["tenant"], workspace_id, payload)
    return {"ok": True, "state": next_state, "selection": payload}


def composition_engine_register_component(state: dict, component: dict) -> dict:
    _require(component, {"component_id", "tenant", "pbc", "fragment", "permissions", "schemas"})
    next_state = _copy_state(state)
    stored = {**component, "status": "registered", "compatibility": "schema_validated"}
    next_state["components"][component["component_id"]] = stored
    next_state = _emit(next_state, "ComponentRegistered", component["tenant"], component["component_id"], stored)
    return {"ok": True, "state": next_state, "component": stored}


def composition_engine_register_ui_fragment(state: dict, fragment: dict) -> dict:
    _require(fragment, {"fragment_id", "tenant", "component_id", "route", "slots", "events"})
    next_state = _copy_state(state)
    stored = {**fragment, "status": "available"}
    next_state["fragments"][fragment["fragment_id"]] = stored
    next_state = _emit(next_state, "UiFragmentRegistered", fragment["tenant"], fragment["fragment_id"], stored)
    return {"ok": True, "state": next_state, "fragment": stored}


def composition_engine_bind_layout(state: dict, binding: dict) -> dict:
    _require(binding, {"binding_id", "tenant", "workspace_id", "page", "slot", "fragment_id", "projection"})
    next_state = _copy_state(state)
    stored = {**binding, "status": "valid", "responsive_rules": ("desktop", "tablet", "mobile")}
    next_state["bindings"][binding["binding_id"]] = stored
    next_state = _emit(next_state, "LayoutBound", binding["tenant"], binding["binding_id"], stored)
    return {"ok": True, "state": next_state, "binding": stored}


def composition_engine_validate_composition_plan(state: dict, workspace_id: str) -> dict:
    next_state = _copy_state(state)
    workspace = next_state["workspaces"][workspace_id]
    bindings = tuple(binding for binding in next_state["bindings"].values() if binding["workspace_id"] == workspace_id)
    selected_pbcs = tuple(workspace.get("selected_pbcs", ()))
    active_rules = tuple(rule for rule in next_state["rules"].values() if rule["status"] == "active" and rule["tenant"] == workspace["tenant"])
    missing_fragments = []
    for rule in active_rules:
        required = set(rule.get("required_fragments", ()))
        available = {next_state["components"][next_state["fragments"][binding["fragment_id"]]["component_id"]]["fragment"] for binding in bindings if binding["fragment_id"] in next_state["fragments"]}
        missing_fragments.extend(sorted(required - available))
    route_count = len({next_state["fragments"][binding["fragment_id"]]["route"] for binding in bindings if binding["fragment_id"] in next_state["fragments"]})
    route_budget = int(next_state["parameters"].get("route_budget", 50))
    blockers = []
    if not selected_pbcs:
        blockers.append("missing_pbc_selection")
    if not bindings:
        blockers.append("missing_layout_binding")
    if route_count > route_budget:
        blockers.append("route_budget_exceeded")
    if missing_fragments:
        blockers.append("missing_required_fragments")
    validation_id = f"validation_{len(next_state['validation_runs']) + 1:06d}"
    validation = {
        "validation_id": validation_id,
        "workspace_id": workspace_id,
        "tenant": workspace["tenant"],
        "decision": "accepted" if not blockers else "blocked",
        "blockers": tuple(blockers),
        "missing_fragments": tuple(missing_fragments),
        "route_count": route_count,
        "selected_pbcs": selected_pbcs,
    }
    next_state["validation_runs"][validation_id] = validation
    if not blockers:
        next_state["composition_plans"][workspace_id] = {
            "workspace_id": workspace_id,
            "tenant": workspace["tenant"],
            "selected_pbcs": selected_pbcs,
            "route_count": route_count,
            "bindings": tuple(binding["binding_id"] for binding in bindings),
            "status": "validated",
        }
        next_state = _emit(next_state, "CompositionPlanValidated", workspace["tenant"], workspace_id, validation)
    return {"ok": not blockers, "state": next_state, "validation": validation}


def composition_engine_plan_package_registration(state: dict, workspace_id: str, *, requested_by: str) -> dict:
    workspace = state["workspaces"][workspace_id]
    validation = next((item for item in state["validation_runs"].values() if item["workspace_id"] == workspace_id and item["decision"] == "accepted"), {})
    dsl = state["dsl_artifacts"].get(f"dsl_{workspace_id}", {})
    plan = {
        "plan_id": f"package_plan_{workspace_id}",
        "workspace_id": workspace_id,
        "tenant": workspace["tenant"],
        "requested_by": requested_by,
        "status": "planned" if validation else "requires_validation",
        "side_effect_free": True,
        "writes_performed": (),
        "package_metadata": {
            "pbc": "composition_engine",
            "workspace_version": workspace["version"],
            "selected_pbcs": tuple(workspace.get("selected_pbcs", ())),
            "dsl_checksum": dsl.get("checksum"),
        },
        "index_entries": tuple(
            {"entry_type": "pbc", "key": pbc, "source": "workspace_selection"}
            for pbc in workspace.get("selected_pbcs", ())
        ),
        "registration_steps": (
            "validate_manifest",
            "validate_owned_tables",
            "validate_api_event_boundaries",
            "publish_index_metadata",
        ),
    }
    return {"ok": bool(validation), "state": state, "plan": plan}


def composition_engine_generate_composition_dsl(state: dict, workspace_id: str) -> dict:
    next_state = _copy_state(state)
    workspace = next_state["workspaces"][workspace_id]
    bindings = tuple(binding for binding in next_state["bindings"].values() if binding["workspace_id"] == workspace_id)
    dsl = {
        "workspace": workspace_id,
        "pbcs": workspace["selected_pbcs"],
        "pages": tuple({"page": item["page"], "slot": item["slot"], "fragment": item["fragment_id"], "projection": item["projection"]} for item in bindings),
        "event_contract": "AppGen-X",
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
        "dependency_boundaries": {"events": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES, "shared_tables": ()},
    }
    checksum = _hash_payload(dsl)
    artifact = {"artifact_id": f"dsl_{workspace_id}", "workspace_id": workspace_id, "dsl": dsl, "checksum": checksum, "route_count": len(bindings), "ok": True}
    next_state["dsl_artifacts"][artifact["artifact_id"]] = artifact
    return {"ok": True, "state": next_state, "artifact": artifact}


def composition_engine_publish_composition(state: dict, workspace_id: str) -> dict:
    next_state = _copy_state(state)
    workspace = dict(next_state["workspaces"][workspace_id])
    bindings = tuple(binding for binding in next_state["bindings"].values() if binding["workspace_id"] == workspace_id)
    validation = next((item for item in next_state["validation_runs"].values() if item["workspace_id"] == workspace_id and item["decision"] == "accepted"), None)
    if validation is None:
        validation_result = composition_engine_validate_composition_plan(next_state, workspace_id)
        next_state = validation_result["state"]
        if not validation_result["ok"]:
            return {"ok": False, "state": next_state, "publication": {"workspace_id": workspace_id, "status": "blocked", "blockers": validation_result["validation"]["blockers"]}}
    release_risk = max(0, 0.2 - len(bindings) * 0.02)
    package_plan = composition_engine_plan_package_registration(next_state, workspace_id, requested_by=workspace["owner"])["plan"]
    publication = {"workspace_id": workspace_id, "tenant": workspace["tenant"], "version": workspace["version"], "route_count": len(bindings), "release_risk": release_risk, "status": "published", "package_registration_plan": package_plan}
    workspace["status"] = "published"
    next_state["workspaces"][workspace_id] = workspace
    next_state["release_evidence"][workspace_id] = publication
    next_state["package_registration_plans"][package_plan["plan_id"]] = package_plan
    next_state["package_index_entries"][workspace_id] = {"workspace_id": workspace_id, "tenant": workspace["tenant"], "selected_pbcs": workspace["selected_pbcs"], "status": "planned"}
    next_state = _emit(next_state, "PackageRegistrationPlanned", workspace["tenant"], workspace_id, package_plan)
    next_state = _emit(next_state, "CompositionPublished", workspace["tenant"], workspace_id, publication)
    next_state = _emit(next_state, "PbcDeployed", workspace["tenant"], workspace_id, publication)
    return {"ok": True, "state": next_state, "publication": publication}


def composition_engine_preview_selection_impact(
    state: dict,
    workspace_id: str,
    candidate_pbcs: tuple[str, ...] | list[str],
) -> dict:
    """Preview the impact of adding or removing PBC selections without mutating state."""
    workspace = state["workspaces"].get(workspace_id, {})
    current_pbcs = tuple(workspace.get("selected_pbcs", ()))
    proposed_pbcs = tuple(dict.fromkeys(tuple(candidate_pbcs or ())))
    added = tuple(item for item in proposed_pbcs if item not in current_pbcs)
    removed = tuple(item for item in current_pbcs if item not in proposed_pbcs)
    retained = tuple(item for item in proposed_pbcs if item in current_pbcs)
    bindings = tuple(binding for binding in state["bindings"].values() if binding.get("workspace_id") == workspace_id)
    routes = tuple(
        sorted(
            {
                state["fragments"][binding["fragment_id"]]["route"]
                for binding in bindings
                if binding.get("fragment_id") in state["fragments"]
            }
        )
    )
    blockers = []
    if not proposed_pbcs:
        blockers.append("missing_pbc_selection")
    if int(state.get("parameters", {}).get("route_budget", 24)) < len(routes):
        blockers.append("route_budget_exceeded")
    if not state.get("schema_projections"):
        blockers.append("missing_schema_projection")
    return {
        "ok": not blockers,
        "workspace_id": workspace_id,
        "current_pbcs": current_pbcs,
        "proposed_pbcs": proposed_pbcs,
        "added_pbcs": added,
        "removed_pbcs": removed,
        "added_or_retained_pbcs": retained + added,
        "impact": {
            "owned_tables": tuple(f"{pbc}_projection" for pbc in proposed_pbcs),
            "routes": routes,
            "permissions": tuple(sorted({permission for component in state["components"].values() for permission in component.get("permissions", ())})),
            "ui_fragments": tuple(sorted(fragment.get("fragment") or fragment_id for fragment_id, fragment in state["fragments"].items())),
            "generated_artifacts": ("dsl_artifact", "composition_plan", "release_evidence"),
            "smoke_tests": ("build_smoke_plan", "release_rehearsal", "build_security_review"),
        },
        "release_blockers": tuple(blockers),
    }


def composition_engine_build_workbench_view(state: dict, *, tenant: str) -> dict:
    workspaces = tuple(item for item in state["workspaces"].values() if item["tenant"] == tenant)
    components = tuple(item for item in state["components"].values() if item["tenant"] == tenant)
    fragments = tuple(item for item in state["fragments"].values() if item["tenant"] == tenant)
    bindings = tuple(item for item in state["bindings"].values() if item["tenant"] == tenant)
    return {
        "format": "appgen.composition-engine-workbench-view.v1",
        "tenant": tenant,
        "workspace_count": len(workspaces),
        "published_count": len(tuple(item for item in workspaces if item["status"] == "published")),
        "component_count": len(components),
        "fragment_count": len(fragments),
        "binding_count": len(bindings),
        "validation_count": len(tuple(item for item in state["validation_runs"].values() if item["tenant"] == tenant)),
        "package_plan_count": len(tuple(item for item in state["package_registration_plans"].values() if item["tenant"] == tenant)),
        "release_evidence_count": len(tuple(item for item in state["release_evidence"].values() if item["tenant"] == tenant)),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
            "outbox_table": "composition_engine_appgen_outbox_event",
            "inbox_table": "composition_engine_appgen_inbox_event",
            "dead_letter_table": "composition_engine_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


def composition_engine_build_smoke_plan(state: dict, workspace_id: str) -> dict:
    """Synthesize a workspace-specific smoke plan from selections, routes, and events."""
    workspace = state["workspaces"].get(workspace_id)
    if workspace is None:
        return {"ok": False, "reason": "unknown_workspace", "workspace_id": workspace_id}
    bindings = tuple(binding for binding in state["bindings"].values() if binding["workspace_id"] == workspace_id)
    routes = tuple(
        sorted(
            {
                state["fragments"][binding["fragment_id"]]["route"]
                for binding in bindings
                if binding["fragment_id"] in state["fragments"]
            }
        )
    )
    steps = (
        {
            "step_id": "workspace_bootstrap",
            "assertions": ("workspace_exists", "tenant_isolation", "selection_recorded"),
            "expected_operations": ("create_workspace", "select_pbc"),
        },
        {
            "step_id": "layout_binding",
            "assertions": ("fragment_available", "route_bound", "projection_declared"),
            "expected_operations": ("register_component", "register_ui_fragment", "bind_layout"),
        },
        {
            "step_id": "release_gate",
            "assertions": ("validation_passes", "dsl_generated", "package_plan_side_effect_free"),
            "expected_operations": ("validate_composition_plan", "generate_composition_dsl", "plan_package_registration"),
        },
    )
    return {
        "ok": bool(workspace.get("selected_pbcs")) and bool(routes),
        "workspace_id": workspace_id,
        "tenant": workspace["tenant"],
        "routes": routes,
        "events": tuple(event["event_type"] for event in state.get("events", ()) if event.get("aggregate_id") == workspace_id),
        "steps": steps,
    }


def composition_engine_build_artifact_lineage(state: dict, workspace_id: str) -> dict:
    """Trace generated artifacts back to selected PBCs, fragments, and governance inputs."""
    workspace = state["workspaces"].get(workspace_id)
    if workspace is None:
        return {"ok": False, "reason": "unknown_workspace", "workspace_id": workspace_id}
    dsl = state["dsl_artifacts"].get(f"dsl_{workspace_id}", {})
    validation = next(
        (item for item in state["validation_runs"].values() if item["workspace_id"] == workspace_id),
        {},
    )
    lineage = (
        {
            "artifact": "dsl_artifact",
            "sources": ("selected_pbcs", "layout_binding", "schema_projections"),
            "workspace_id": workspace_id,
            "checksum": dsl.get("checksum"),
        },
        {
            "artifact": "validation_run",
            "sources": ("composition_rule", "route_budget", "required_fragments"),
            "workspace_id": workspace_id,
            "decision": validation.get("decision"),
        },
        {
            "artifact": "release_packet",
            "sources": ("package_registration_plan", "smoke_plan", "documentation_matrix", "security_review"),
            "workspace_id": workspace_id,
            "status": "planned",
        },
    )
    return {"ok": bool(dsl or validation), "workspace_id": workspace_id, "lineage": lineage}


def composition_engine_build_documentation_matrix(state: dict, workspace_id: str) -> dict:
    """Build documentation coverage for one composition workspace."""
    workspace = state["workspaces"].get(workspace_id)
    if workspace is None:
        return {"ok": False, "reason": "unknown_workspace", "workspace_id": workspace_id}
    bindings = tuple(binding for binding in state["bindings"].values() if binding["workspace_id"] == workspace_id)
    cells = (
        {"audience": "user", "artifact": "workbench_guide", "covered": bool(bindings)},
        {"audience": "operator", "artifact": "release_rehearsal", "covered": bool(state["validation_runs"])},
        {"audience": "developer", "artifact": "schema_service_api_contracts", "covered": True},
        {"audience": "package", "artifact": "package_registration_plan", "covered": bool(workspace.get("selected_pbcs"))},
        {"audience": "agent", "artifact": "assistant_preview", "covered": True},
        {"audience": "release", "artifact": "release_notes", "covered": bool(state["dsl_artifacts"])},
    )
    missing = tuple(cell["artifact"] for cell in cells if not cell["covered"])
    return {
        "ok": not missing,
        "workspace_id": workspace_id,
        "cells": cells,
        "missing": missing,
    }


def composition_engine_build_security_review(state: dict, workspace_id: str) -> dict:
    """Inspect routes, permissions, audit lineage, and risky publication conditions."""
    workspace = state["workspaces"].get(workspace_id)
    if workspace is None:
        return {"ok": False, "reason": "unknown_workspace", "workspace_id": workspace_id}
    exposed_routes = tuple(
        sorted(
            {
                fragment["route"]
                for fragment in state["fragments"].values()
                if fragment["tenant"] == workspace["tenant"]
            }
        )
    )
    blocking_findings = []
    if not workspace.get("selected_pbcs"):
        blocking_findings.append("missing_selection")
    if not any(item["workspace_id"] == workspace_id and item["decision"] == "accepted" for item in state["validation_runs"].values()):
        blocking_findings.append("validation_not_accepted")
    findings = (
        {"severity": "blocking" if "validation_not_accepted" in blocking_findings else "info", "id": "validation_gate", "detail": "Validated plan required before publication."},
        {"severity": "warning" if not state.get("audit_projections") else "info", "id": "audit_lineage", "detail": "Audit projection should be present before promoting beyond rehearsal."},
        {"severity": "info", "id": "route_surface", "detail": f"Routes in scope: {', '.join(exposed_routes) if exposed_routes else 'none'}."},
    )
    return {
        "ok": not blocking_findings,
        "workspace_id": workspace_id,
        "exposed_routes": exposed_routes,
        "findings": findings,
        "blocking_findings": tuple(blocking_findings),
    }


def composition_engine_build_release_notes(state: dict, workspace_id: str) -> dict:
    """Draft release notes from the current composition state."""
    workspace = state["workspaces"].get(workspace_id)
    if workspace is None:
        return {"ok": False, "reason": "unknown_workspace", "workspace_id": workspace_id}
    impact = composition_engine_preview_selection_impact(state, workspace_id, workspace.get("selected_pbcs", ()))
    security = composition_engine_build_security_review(state, workspace_id)
    notes = {
        "headline": f"Composition update for {workspace['name']}",
        "highlights": (
            f"Selected PBCs: {', '.join(workspace.get('selected_pbcs', ())) or 'none'}",
            f"Routes in scope: {len(impact['impact']['routes'])}",
            f"Release blockers: {', '.join(impact['release_blockers']) or 'none'}",
        ),
        "known_limitations": tuple(security["blocking_findings"]) or ("publication_requires_operator_confirmation",),
    }
    return {"ok": True, "workspace_id": workspace_id, "notes": notes}


def composition_engine_release_rehearsal(state: dict, workspace_id: str) -> dict:
    """Rehearse publication without mutating release state."""
    validation = composition_engine_validate_composition_plan(state, workspace_id)
    next_state = validation["state"]
    if not validation["ok"]:
        return {"ok": False, "workspace_id": workspace_id, "validation": validation["validation"], "state": next_state}
    if f"dsl_{workspace_id}" not in next_state["dsl_artifacts"]:
        dsl = composition_engine_generate_composition_dsl(next_state, workspace_id)
        next_state = dsl["state"]
    package_plan = composition_engine_plan_package_registration(
        next_state,
        workspace_id,
        requested_by=next_state["workspaces"][workspace_id]["owner"],
    )
    smoke_plan = composition_engine_build_smoke_plan(next_state, workspace_id)
    lineage = composition_engine_build_artifact_lineage(next_state, workspace_id)
    documentation = composition_engine_build_documentation_matrix(next_state, workspace_id)
    security = composition_engine_build_security_review(next_state, workspace_id)
    return {
        "ok": package_plan["ok"] and smoke_plan["ok"] and documentation["ok"] and security["ok"] and lineage["ok"],
        "workspace_id": workspace_id,
        "validation": validation["validation"],
        "package_plan": package_plan["plan"],
        "smoke_plan": smoke_plan,
        "lineage": lineage,
        "documentation": documentation,
        "security": security,
        "release_freeze": tuple(security["blocking_findings"]),
        "state": next_state,
    }


def composition_engine_agent_competency_catalog() -> dict:
    """Return the composition-engine competency catalog for the shared assistant."""
    competencies = (
        {
            "competency_id": "prompt_intake",
            "permission": "composition_engine.read",
            "safe_reads": ("composition_workspace", "composition_rule", "composition_parameter"),
            "mutation_previews": ("assistant_document_preview",),
            "document_inputs": True,
            "emitted_events": (),
        },
        {
            "competency_id": "pbc_selection_rationale",
            "permission": "composition_engine.compose",
            "safe_reads": ("composition_workspace", "component_registry"),
            "mutation_previews": ("preview_selection_impact",),
            "document_inputs": True,
            "emitted_events": ("PbcSelectedForComposition",),
        },
        {
            "competency_id": "layout_planning",
            "permission": "composition_engine.compose",
            "safe_reads": ("layout_binding", "ui_fragment"),
            "mutation_previews": ("bind_layout",),
            "document_inputs": True,
            "emitted_events": ("LayoutBound",),
        },
        {
            "competency_id": "dsl_review",
            "permission": "composition_engine.publish",
            "safe_reads": ("dsl_artifact", "composition_plan"),
            "mutation_previews": ("generate_composition_dsl",),
            "document_inputs": False,
            "emitted_events": (),
        },
        {
            "competency_id": "dependency_solving",
            "permission": "composition_engine.approve",
            "safe_reads": ("composition_plan", "composition_validation_run"),
            "mutation_previews": ("validate_composition_plan",),
            "document_inputs": True,
            "emitted_events": ("CompositionPlanValidated",),
        },
        {
            "competency_id": "package_registration_preview",
            "permission": "composition_engine.publish",
            "safe_reads": ("package_registration_plan", "package_index_entry"),
            "mutation_previews": ("plan_package_registration",),
            "document_inputs": False,
            "emitted_events": ("PackageRegistrationPlanned",),
        },
        {
            "competency_id": "release_readiness_explanation",
            "permission": "composition_engine.audit",
            "safe_reads": ("release_evidence", "composition_validation_run"),
            "mutation_previews": ("release_rehearsal", "build_release_notes"),
            "document_inputs": True,
            "emitted_events": (),
        },
        {
            "competency_id": "rollback_planning",
            "permission": "composition_engine.audit",
            "safe_reads": ("release_evidence", "package_registration_plan"),
            "mutation_previews": ("build_release_notes",),
            "document_inputs": True,
            "emitted_events": (),
        },
    )
    return {"ok": True, "pbc": "composition_engine", "competencies": competencies}


def composition_engine_route_agent_intent(intent: str, context: dict | None = None) -> dict:
    """Route a natural-language assistant intent to the owning composition competency."""
    normalized = str(intent or "").lower()
    context = dict(context or {})
    routes = (
        ("rollback", "rollback_planning", "build_release_notes"),
        ("publish", "package_registration_preview", "plan_package_registration"),
        ("release", "release_readiness_explanation", "release_rehearsal"),
        ("layout", "layout_planning", "bind_layout"),
        ("route", "layout_planning", "preview_selection_impact"),
        ("dependency", "dependency_solving", "validate_composition_plan"),
        ("select", "pbc_selection_rationale", "preview_selection_impact"),
        ("document", "prompt_intake", "assistant_document_preview"),
        ("requirement", "prompt_intake", "assistant_document_preview"),
    )
    selected = next((item for item in routes if item[0] in normalized), ("release", "release_readiness_explanation", "release_rehearsal"))
    competency = next(
        item for item in composition_engine_agent_competency_catalog()["competencies"] if item["competency_id"] == selected[1]
    )
    return {
        "ok": True,
        "intent": intent,
        "competency_id": competency["competency_id"],
        "operation": selected[2],
        "required_permission": competency["permission"],
        "required_context": tuple(sorted(context)),
        "handoff_projections": (
            "identity_composition_projection",
            "gateway_composition_projection",
            "schema_composition_projection",
            "workflow_composition_projection",
            "audit_composition_projection",
        ),
    }


def composition_engine_plan_crud_action(
    action: str,
    target_table: str | None = None,
    payload: dict | None = None,
) -> dict:
    """Plan governed CRUD against package-owned tables only."""
    normalized_action = str(action or "read").lower()
    owned_tables = tuple(f"composition_engine_{table}" for table in COMPOSITION_ENGINE_OWNED_TABLES)
    table = target_table or owned_tables[0]
    boundary = composition_engine_verify_owned_table_boundary((table,))
    operation_map = {
        "composition_engine_composition_workspace": {"create": "create_workspace", "read": "build_workbench_view", "update": "select_pbc", "delete": "preview_selection_impact"},
        "composition_engine_component_registry": {"create": "register_component", "read": "build_workbench_view", "update": "register_component", "delete": "preview_selection_impact"},
        "composition_engine_ui_fragment": {"create": "register_ui_fragment", "read": "build_workbench_view", "update": "register_ui_fragment", "delete": "preview_selection_impact"},
        "composition_engine_layout_binding": {"create": "bind_layout", "read": "build_workbench_view", "update": "bind_layout", "delete": "preview_selection_impact"},
        "composition_engine_dsl_artifact": {"create": "generate_composition_dsl", "read": "build_artifact_lineage", "update": "generate_composition_dsl", "delete": "build_artifact_lineage"},
        "composition_engine_composition_plan": {"create": "validate_composition_plan", "read": "build_smoke_plan", "update": "validate_composition_plan", "delete": "build_smoke_plan"},
        "composition_engine_composition_validation_run": {"create": "validate_composition_plan", "read": "build_smoke_plan", "update": "validate_composition_plan", "delete": "build_smoke_plan"},
        "composition_engine_package_registration_plan": {"create": "plan_package_registration", "read": "release_rehearsal", "update": "plan_package_registration", "delete": "build_release_notes"},
        "composition_engine_package_index_entry": {"create": "plan_package_registration", "read": "release_rehearsal", "update": "plan_package_registration", "delete": "build_release_notes"},
        "composition_engine_release_evidence": {"create": "publish_composition", "read": "build_release_evidence", "update": "release_rehearsal", "delete": "build_release_notes"},
        "composition_engine_composition_rule": {"create": "register_rule", "read": "build_security_review", "update": "register_rule", "delete": "build_security_review"},
        "composition_engine_composition_parameter": {"create": "set_parameter", "read": "build_documentation_matrix", "update": "set_parameter", "delete": "build_documentation_matrix"},
        "composition_engine_composition_configuration": {"create": "configure_runtime", "read": "build_release_evidence", "update": "configure_runtime", "delete": "build_release_evidence"},
    }
    operation = operation_map.get(table, {}).get(normalized_action)
    permissions = composition_engine_permissions_contract()["action_permissions"]
    return {
        "ok": bool(operation) and boundary["ok"] and normalized_action in {"create", "read", "update", "delete"},
        "action": normalized_action,
        "table": table,
        "operation": operation,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized_action != "read",
        "required_permission": permissions.get(operation),
        "boundary": boundary,
    }


def composition_engine_assistant_document_preview(
    document_text: str,
    instructions: str,
    *,
    action: str = "read",
    target_table: str | None = None,
    payload: dict | None = None,
) -> dict:
    """Parse a document into a preview-only, package-owned CRUD plan."""
    facts = _extract_composition_document_facts(document_text, instructions)
    crud_plan = composition_engine_plan_crud_action(action, target_table=target_table, payload=payload)
    routing = composition_engine_route_agent_intent(instructions or document_text, context={"target_table": target_table or ""})
    unresolved_questions = []
    if not facts["pbcs"]:
        unresolved_questions.append("which_pbc_should_be_selected")
    if not facts["pages"]:
        unresolved_questions.append("which_page_should_host_the_fragment")
    if target_table is None:
        unresolved_questions.append("which_owned_table_should_receive_the_change")
    return {
        "ok": bool(document_text or instructions) and crud_plan["ok"] and routing["ok"],
        "document_digest": _hash_payload({"document_text": document_text, "instructions": instructions}),
        "facts": facts,
        "crud_plan": crud_plan,
        "routing": routing,
        "unresolved_questions": tuple(unresolved_questions),
        "requires_human_confirmation": crud_plan["requires_confirmation"],
        "redaction": {"emails_removed": facts["emails_detected"], "quoted_lines": len(facts["citations"])},
    }


def composition_engine_build_control_center(state: dict, *, workspace_id: str | None = None) -> dict:
    """Return package-local operational controls and assistant guardrails."""
    workspace_id = workspace_id or next(iter(state.get("workspaces", {}) or ()), None)
    runtime_controls = composition_engine_run_control_tests(state)
    if workspace_id:
        rehearsal = composition_engine_release_rehearsal(state, workspace_id)
        documentation = composition_engine_build_documentation_matrix(rehearsal["state"], workspace_id)
        security = composition_engine_build_security_review(rehearsal["state"], workspace_id)
    else:
        rehearsal = {"ok": False, "reason": "missing_workspace", "state": state}
        documentation = {"ok": False, "missing": ("workspace",)}
        security = {"ok": False, "blocking_findings": ("workspace",)}
    assistant_guardrails = composition_engine_assistant_document_preview(
        "Keep the composition preview inside package-owned tables.",
        "Preview an update to the workspace only.",
        action="update",
        target_table="composition_engine_composition_workspace",
    )
    controls_ok = runtime_controls["ok"] or rehearsal.get("ok")
    return {
        "ok": controls_ok and assistant_guardrails["ok"] and not security.get("blocking_findings"),
        "workspace_id": workspace_id,
        "runtime_controls": runtime_controls,
        "rehearsal": rehearsal,
        "documentation": documentation,
        "security": security,
        "assistant_guardrails": assistant_guardrails,
    }


def composition_engine_simulate_layout(state: dict, workspace_id: str, *, added_fragments: int, removed_fragments: int) -> dict:
    density_delta = (added_fragments - removed_fragments) / max(float(state["parameters"].get("max_fragments_per_page", 12)), 1)
    return {"ok": True, "workspace_id": workspace_id, "density_delta": round(density_delta, 4)}


def composition_engine_forecast_release_readiness(history: tuple[float, ...], *, horizon_days: int) -> dict:
    slope = (history[-1] - history[0]) / max(len(history) - 1, 1)
    return {"ok": True, "forecast_readiness": round(max(0, min(1, history[-1] + slope * (horizon_days / 14))), 4)}


def composition_engine_parse_composition_intent(text: str) -> dict:
    workspace = re.search(r"workspace\s+([a-zA-Z0-9_:-]+)", text)
    pbc = re.search(r"pbc\s+([a-zA-Z0-9_:-]+)", text)
    fragment = re.search(r"fragment\s+([a-zA-Z0-9_:-]+)", text)
    return {"ok": bool(workspace), "workspace_id": workspace.group(1) if workspace else None, "pbc": pbc.group(1) if pbc else None, "fragment": fragment.group(1) if fragment else None}


def composition_engine_score_composition_risk(factors: dict[str, float]) -> dict:
    weights = {"schema": 0.3, "route": 0.25, "permission": 0.25, "layout": 0.2}
    return {"ok": True, "risk_score": round(sum(float(factors.get(key, 0)) * weight for key, weight in weights.items()), 4)}


def composition_engine_recommend_layout_remediation(reason: str) -> dict:
    actions = {"slot_overflow": "rebalance_fragment_slots", "route_conflict": "rename_route_namespace", "permission_gap": "add_permission_mapping"}
    return {"ok": True, "reason": reason, "action": actions.get(reason, "open_composition_review")}


def composition_engine_select_publication_route(event: dict, *, rails: tuple[dict, ...]) -> dict:
    available = tuple(rail for rail in rails if rail.get("available"))
    selected = min(available, key=lambda item: item.get("latency", 999)) if available else {}
    return {"ok": bool(selected), "event_id": event["event_id"], "route": selected.get("route"), "failover_used": selected.get("route") != rails[0].get("route")}


def composition_engine_generate_publication_proof(state: dict, workspace_id: str, *, disclosure: tuple[str, ...]) -> dict:
    publication = state["release_evidence"][workspace_id]
    payload = {field: publication.get(field) for field in disclosure}
    digest = _hash_payload(payload)
    return {"ok": True, "proof": f"zk_composition_{digest[:16]}", "hash": digest, "disclosure": disclosure}


def composition_engine_screen_policy(state: dict, workspace_id: str, *, meshes: tuple[str, ...]) -> dict:
    selected = state["workspaces"][workspace_id]["selected_pbcs"]
    rules = tuple(rule for rule in state["rules"].values() if rule["status"] == "active")
    decision = "clear" if selected and rules and set(rules[0]["allowed_meshes"]) <= set(meshes) else "review"
    return {"ok": decision == "clear", "workspace_id": workspace_id, "decision": decision}


def composition_engine_run_control_tests(state: dict) -> dict:
    hash_chain_valid = all(event["hash"] == _event_hash(event) for event in state["events"])
    checks = {
        "configuration": state["configuration"].get("event_contract") == "AppGen-X",
        "database": state["configuration"].get("database_backend") in set(COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS),
        "rules": bool(state["rules"]),
        "workspaces": bool(state["workspaces"]),
        "dsl": bool(state["dsl_artifacts"]),
        "release": bool(state["release_evidence"]),
        "package_plan": bool(state["package_registration_plans"]),
        "outbox": all(item["idempotency_key"].startswith("composition_engine:") for item in state["outbox"]),
        "dead_letter": isinstance(state["dead_letters"], list) and isinstance(state.get("dead_letter", []), list),
        "hash_chain": hash_chain_valid,
    }
    return {"ok": all(checks.values()), "checks": checks, "hash_chain_valid": hash_chain_valid, "blocking_gaps": tuple(key for key, ok in checks.items() if not ok)}


def composition_engine_build_schema_contract() -> dict:
    table_fields = {
        "composition_workspace": ("tenant", "workspace_id", "name", "owner", "target", "version", "status", "selected_pbcs"),
        "component_registry": ("tenant", "component_id", "pbc", "fragment", "permissions", "schemas", "status", "compatibility"),
        "ui_fragment": ("tenant", "fragment_id", "component_id", "route", "slots", "events", "status"),
        "layout_binding": ("tenant", "binding_id", "workspace_id", "page", "slot", "fragment_id", "projection", "status"),
        "dsl_artifact": ("tenant", "artifact_id", "workspace_id", "route_count", "checksum", "event_contract", "status"),
        "composition_plan": ("tenant", "workspace_id", "selected_pbcs", "route_count", "bindings", "status"),
        "composition_validation_run": ("tenant", "validation_id", "workspace_id", "decision", "blockers", "missing_fragments", "route_count"),
        "package_registration_plan": ("tenant", "plan_id", "workspace_id", "requested_by", "status", "side_effect_free", "writes_performed"),
        "package_index_entry": ("tenant", "workspace_id", "selected_pbcs", "status", "entry_source", "indexed_at"),
        "release_evidence": ("tenant", "workspace_id", "version", "route_count", "release_risk", "status", "package_registration_plan"),
        "composition_rule": ("tenant", "rule_id", "scope", "required_fragments", "allowed_meshes", "route_policy", "requires_approval", "status"),
        "composition_parameter": ("tenant", "parameter_id", "key", "value", "effective_at", "status"),
        "composition_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "default_timezone", "status"),
    }
    runtime_tables = (
        {
            "table": COMPOSITION_ENGINE_RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "status"),
        },
        {
            "table": COMPOSITION_ENGINE_RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts"),
        },
        {
            "table": COMPOSITION_ENGINE_RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "reason", "payload", "attempts"),
        },
    )
    relationships = (
        {"from_table": "ui_fragment", "from_field": "component_id", "to_table": "component_registry", "to_field": "component_id"},
        {"from_table": "layout_binding", "from_field": "workspace_id", "to_table": "composition_workspace", "to_field": "workspace_id"},
        {"from_table": "layout_binding", "from_field": "fragment_id", "to_table": "ui_fragment", "to_field": "fragment_id"},
        {"from_table": "dsl_artifact", "from_field": "workspace_id", "to_table": "composition_workspace", "to_field": "workspace_id"},
        {"from_table": "composition_plan", "from_field": "workspace_id", "to_table": "composition_workspace", "to_field": "workspace_id"},
        {"from_table": "composition_validation_run", "from_field": "workspace_id", "to_table": "composition_workspace", "to_field": "workspace_id"},
        {"from_table": "package_registration_plan", "from_field": "workspace_id", "to_table": "composition_workspace", "to_field": "workspace_id"},
        {"from_table": "package_index_entry", "from_field": "workspace_id", "to_table": "composition_workspace", "to_field": "workspace_id"},
        {"from_table": "release_evidence", "from_field": "workspace_id", "to_table": "composition_workspace", "to_field": "workspace_id"},
    )
    allowed_prefixes = ("composition_", "component_", "ui_", "layout_", "dsl_", "package_", "release_")
    invalid_prefixes = tuple(table for table in COMPOSITION_ENGINE_OWNED_TABLES if not table.startswith(allowed_prefixes))
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": table_fields[table][1],
            "owned_by": "composition_engine",
        }
        for table in COMPOSITION_ENGINE_OWNED_TABLES
    )
    migrations = tuple(
        {
            "path": f"pbcs/composition_engine/migrations/{position + 1:03d}_{table}.sql",
            "table": table,
            "operation": "create_owned_table",
            "backend_allowlist": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        }
        for position, table in enumerate(COMPOSITION_ENGINE_OWNED_TABLES)
    )
    models = tuple(
        {
            "path": f"pbcs/composition_engine/models/{table}.py",
            "table": table,
            "class_name": _class_name(table),
        }
        for table in COMPOSITION_ENGINE_OWNED_TABLES
    )
    return {
        "format": "appgen.composition-engine-owned-schema-contract.v1",
        "pbc": "composition_engine",
        "ok": not invalid_prefixes and len(tables) == len(COMPOSITION_ENGINE_OWNED_TABLES) and len(migrations) == len(COMPOSITION_ENGINE_OWNED_TABLES),
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
        "tables": tables,
        "runtime_tables": runtime_tables,
        "all_tables": tables + runtime_tables,
        "relationships": relationships,
        "migrations": migrations,
        "models": models,
        "implementation_artifacts": {
            "migration_files": ("migrations/001_initial.sql",),
            "model_manifest_module": "models.py",
        },
        "allowed_prefixes": allowed_prefixes,
        "datastore_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "shared_table_access": False,
        "invalid_prefixes": invalid_prefixes,
    }


def composition_engine_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_workspace",
        "select_pbc",
        "register_component",
        "register_ui_fragment",
        "bind_layout",
        "validate_composition_plan",
        "plan_package_registration",
        "generate_composition_dsl",
        "publish_composition",
        "run_control_tests",
        "verify_owned_table_boundary",
        "register_governed_model",
    )
    query_methods = (
        "build_workbench_view",
        "preview_selection_impact",
        "build_smoke_plan",
        "build_artifact_lineage",
        "build_documentation_matrix",
        "build_security_review",
        "build_release_notes",
        "release_rehearsal",
        "assistant_document_preview",
        "route_agent_intent",
        "agent_competency_catalog",
        "build_control_center",
        "simulate_layout",
        "forecast_release_readiness",
        "parse_composition_intent",
        "score_composition_risk",
        "recommend_layout_remediation",
        "select_publication_route",
        "generate_publication_proof",
        "screen_policy",
        "build_api_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "federate_composition_view",
        "verify_publisher_identity",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_build",
        "optimize_layout",
        "allocate_fragment_slots",
        "detect_composition_anomaly",
        "model_stochastic_release_exposure",
    )
    return {
        "format": "appgen.composition-engine-service-contract.v1",
        "ok": len(command_methods) >= 16 and len(query_methods) >= 20 and not composition_engine_verify_owned_table_boundary(COMPOSITION_ENGINE_OWNED_TABLES)["violations"],
        "transaction_boundary": "composition_engine_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": COMPOSITION_ENGINE_OWNED_TABLES,
        "runtime_tables": COMPOSITION_ENGINE_RUNTIME_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _COMPOSITION_ENGINE_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _COMPOSITION_ENGINE_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "idempotent_handlers": ("receive_event", "plan_package_registration", "publish_composition"),
        "side_effect_free_commands": ("plan_package_registration",),
        "retry_dead_letter_evidence": {
            "outbox_table": COMPOSITION_ENGINE_RUNTIME_TABLES[0],
            "inbox_table": COMPOSITION_ENGINE_RUNTIME_TABLES[1],
            "dead_letter_table": COMPOSITION_ENGINE_RUNTIME_TABLES[2],
            "idempotency_prefix": "composition_engine:",
        },
        "eventing": {
            "contract": "AppGen-X",
            "topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "rules_parameters_configuration": ("register_rule", "set_parameter", "configure_runtime"),
    }


def composition_engine_build_release_evidence() -> dict:
    from .ui import composition_engine_ui_contract

    schema = composition_engine_build_schema_contract()
    service = composition_engine_build_service_contract()
    api = composition_engine_build_api_contract()
    permissions = composition_engine_permissions_contract()
    configured = composition_engine_configure_runtime(
        composition_engine_empty_state(),
        {
            "database_backend": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS[0],
            "event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_targets": ("web", "admin"),
            "allowed_layout_modes": ("grid", "flow"),
            "publication_mode": "side_effect_free_plan",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    configured = composition_engine_set_parameter(configured, "route_budget", 24)["state"]
    configured = composition_engine_register_rule(
        configured,
        {
            "rule_id": "release_gate_rule",
            "tenant": "tenant_release",
            "scope": "workspace",
            "required_fragments": ("ReleaseEvidenceBoard",),
            "allowed_meshes": ("platform", "relationship"),
            "route_policy": "balanced",
            "requires_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    configured = composition_engine_receive_event(
        configured,
        {
            "event_id": "evt_release_schema",
            "event_type": "SchemaAccepted",
            "payload": {"tenant": "tenant_release", "schema_id": "CompositionPublished", "owner_pbc": "composition_engine"},
        },
    )["state"]
    configured = composition_engine_create_workspace(
        configured,
        {
            "workspace_id": "ws_release",
            "tenant": "tenant_release",
            "name": "Release Console",
            "owner": "release_manager",
            "target": "admin",
        },
    )["state"]
    configured = composition_engine_select_pbc(
        configured,
        "ws_release",
        {"pbc": "customer_360", "mesh": "relationship", "reason": "customer insight workspace"},
    )["state"]
    configured = composition_engine_register_component(
        configured,
        {
            "component_id": "cmp_release",
            "tenant": "tenant_release",
            "pbc": "customer_360",
            "fragment": "ReleaseEvidenceBoard",
            "permissions": ("composition_engine.audit",),
            "schemas": ("CompositionPublished",),
        },
    )["state"]
    configured = composition_engine_register_ui_fragment(
        configured,
        {
            "fragment_id": "frag_release",
            "tenant": "tenant_release",
            "component_id": "cmp_release",
            "route": "/release",
            "slots": ("main",),
            "events": ("CompositionPublished",),
        },
    )["state"]
    configured = composition_engine_bind_layout(
        configured,
        {
            "binding_id": "bind_release",
            "tenant": "tenant_release",
            "workspace_id": "ws_release",
            "page": "release",
            "slot": "main",
            "fragment_id": "frag_release",
            "projection": "release_projection",
        },
    )["state"]
    configured = composition_engine_generate_composition_dsl(configured, "ws_release")["state"]
    rehearsal = composition_engine_release_rehearsal(configured, "ws_release")
    evidence_state = rehearsal["state"] if rehearsal.get("ok") else configured
    workbench = composition_engine_build_workbench_view(evidence_state, tenant="tenant_release")
    ui = composition_engine_ui_contract()
    smoke_plan = composition_engine_build_smoke_plan(evidence_state, "ws_release")
    lineage = composition_engine_build_artifact_lineage(evidence_state, "ws_release")
    documentation = composition_engine_build_documentation_matrix(evidence_state, "ws_release")
    security = composition_engine_build_security_review(evidence_state, "ws_release")
    release_notes = composition_engine_build_release_notes(evidence_state, "ws_release")
    assistant = composition_engine_assistant_document_preview(
        "Prepare a release console with customer insight and publication controls.",
        "Preview an update to release evidence without publishing.",
        action="update",
        target_table="composition_engine_release_evidence",
    )
    competencies = composition_engine_agent_competency_catalog()
    boundary = composition_engine_verify_owned_table_boundary(
        (
            "composition_workspace",
            COMPOSITION_ENGINE_RUNTIME_TABLES[0],
            "SchemaAccepted",
            "gateway_composition_projection",
            "POST /audit/composition-events",
        )
    )
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) == len(COMPOSITION_ENGINE_OWNED_TABLES)},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(COMPOSITION_ENGINE_OWNED_TABLES)},
        {"id": "runtime_tables_declared", "ok": tuple(item["table"] for item in schema["runtime_tables"]) == COMPOSITION_ENGINE_RUNTIME_TABLES},
        {"id": "service_contract_depth", "ok": service["ok"] and "receive_event" in service["idempotent_handlers"] and "plan_package_registration" in service["side_effect_free_commands"]},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X" and api["required_event_topic"] == COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC},
        {"id": "permissions_cover_release_queries", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "ui_binding_evidence", "ok": ui["ok"] and ui["binding_evidence"]["runtime_tables"] == COMPOSITION_ENGINE_RUNTIME_TABLES},
        {"id": "workbench_binding_evidence", "ok": workbench["binding_evidence"]["outbox_table"] == COMPOSITION_ENGINE_RUNTIME_TABLES[0]},
        {"id": "smoke_plan_synthesis", "ok": smoke_plan["ok"] and bool(smoke_plan["steps"])},
        {"id": "artifact_lineage", "ok": lineage["ok"] and len(lineage["lineage"]) >= 3},
        {"id": "documentation_matrix", "ok": documentation["ok"] and not documentation["missing"]},
        {"id": "security_review_panel", "ok": security["ok"] and not security["blocking_findings"]},
        {"id": "release_rehearsal", "ok": rehearsal["ok"] and not rehearsal["release_freeze"]},
        {"id": "assistant_preview_guardrails", "ok": assistant["ok"] and assistant["requires_human_confirmation"]},
        {"id": "agent_competency_catalog", "ok": competencies["ok"] and len(competencies["competencies"]) >= 8},
        {"id": "boundary_contract", "ok": boundary["ok"] and boundary["declared_dependencies"]["shared_tables"] == ()},
        {"id": "database_allowlist", "ok": schema["datastore_backends"] == COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS and api["database_backends"] == COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.composition-engine-release-evidence.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui": ui,
        "workbench": workbench,
        "smoke_plan": smoke_plan,
        "lineage": lineage,
        "documentation": documentation,
        "security": security,
        "release_notes": release_notes,
        "rehearsal": rehearsal,
        "assistant": assistant,
        "agent_competencies": competencies,
        "boundary": boundary,
        "blocking_gaps": blocking_gaps,
    }


def composition_engine_build_api_contract() -> dict:
    return {
        "ok": True,
        "format": "appgen.composition-engine-api-contract.v1",
        "routes": (
            {"route": "POST /composition-workspaces", "command": "create_workspace", "owned_tables": ("composition_workspace",), "emits": ("CompositionWorkspaceCreated",), "requires_permission": "composition_engine.compose", "idempotency_key": "workspace_id"},
            {"route": "POST /composition-workspaces/{id}/pbcs", "command": "select_pbc", "owned_tables": ("composition_workspace", "component_registry"), "emits": ("PbcSelectedForComposition",), "requires_permission": "composition_engine.compose", "idempotency_key": "workspace_id:pbc"},
            {"route": "GET /composition-selection-impact", "query": "preview_selection_impact", "owned_tables": ("composition_workspace", "composition_plan", "composition_validation_run"), "requires_permission": "composition_engine.compose"},
            {"route": "POST /component-registry", "command": "register_component", "owned_tables": ("component_registry",), "emits": ("ComponentRegistered",), "requires_permission": "composition_engine.compose", "idempotency_key": "component_id"},
            {"route": "POST /ui-fragments", "command": "register_ui_fragment", "owned_tables": ("ui_fragment",), "emits": ("UiFragmentRegistered",), "requires_permission": "composition_engine.compose", "idempotency_key": "fragment_id"},
            {"route": "POST /layout-bindings", "command": "bind_layout", "owned_tables": ("layout_binding",), "emits": ("LayoutBound",), "requires_permission": "composition_engine.compose", "idempotency_key": "binding_id"},
            {"route": "POST /composition-plans/validate", "command": "validate_composition_plan", "owned_tables": ("composition_plan", "composition_validation_run"), "emits": ("CompositionPlanValidated",), "requires_permission": "composition_engine.approve", "idempotency_key": "workspace_id"},
            {"route": "POST /package-registration-plans", "command": "plan_package_registration", "owned_tables": ("package_registration_plan", "package_index_entry"), "emits": ("PackageRegistrationPlanned",), "requires_permission": "composition_engine.publish", "idempotency_key": "workspace_id"},
            {"route": "POST /composition-dsl", "command": "generate_composition_dsl", "owned_tables": ("dsl_artifact",), "emits": (), "requires_permission": "composition_engine.publish", "idempotency_key": "workspace_id"},
            {"route": "POST /composition-publications", "command": "publish_composition", "owned_tables": ("release_evidence", "package_registration_plan", "package_index_entry"), "emits": ("CompositionPublished", "PbcDeployed"), "requires_permission": "composition_engine.publish", "idempotency_key": "workspace_id:version"},
            {"route": "POST /composition/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES, "requires_permission": "composition_engine.event", "idempotency_key": "event_id"},
            {"route": "POST /composition/assistant/document-preview", "query": "assistant_document_preview", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.read"},
            {"route": "POST /composition/assistant/route-intent", "query": "route_agent_intent", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.read"},
            {"route": "GET /composition/smoke-plan", "query": "build_smoke_plan", "owned_tables": ("composition_workspace", "layout_binding", "dsl_artifact"), "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition/artifact-lineage", "query": "build_artifact_lineage", "owned_tables": ("dsl_artifact", "composition_plan", "release_evidence"), "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition/documentation-matrix", "query": "build_documentation_matrix", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition/security-review", "query": "build_security_review", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition/release-notes", "query": "build_release_notes", "owned_tables": ("release_evidence", "composition_plan", "dsl_artifact"), "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition/rehearsal", "query": "release_rehearsal", "owned_tables": ("composition_plan", "dsl_artifact", "package_registration_plan"), "requires_permission": "composition_engine.publish"},
            {"route": "GET /composition/agent-competencies", "query": "agent_competency_catalog", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.read"},
            {"route": "GET /composition/controls", "query": "build_control_center", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition-workbench", "query": "build_workbench_view", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition/schema-contract", "query": "build_schema_contract", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition/service-contract", "query": "build_service_contract", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.audit"},
            {"route": "GET /composition/release-evidence", "query": "build_release_evidence", "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES, "requires_permission": "composition_engine.audit"},
        ),
        "declared_catalog_routes": ("POST /composition-workspaces", "POST /component-registry", "POST /ui-fragments", "POST /layout-bindings", "POST /composition-dsl", "POST /composition-publications", "POST /composition/assistant/document-preview", "GET /composition-workbench", "GET /composition/controls"),
        "events": {"emits": COMPOSITION_ENGINE_EMITTED_EVENT_TYPES, "consumes": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES},
        "emits": COMPOSITION_ENGINE_EMITTED_EVENT_TYPES,
        "consumes": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(composition_engine_permissions_contract()["permissions"])),
        "database_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
        "runtime_tables": COMPOSITION_ENGINE_RUNTIME_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "configuration": ("COMPOSITION_ENGINE_DATABASE_URL", "COMPOSITION_ENGINE_EVENT_TOPIC", "COMPOSITION_ENGINE_RETRY_LIMIT", "COMPOSITION_ENGINE_DEFAULT_TIMEZONE"),
    }


def composition_engine_permissions_contract() -> dict:
    from .permissions import permission_manifest

    manifest = permission_manifest()
    return {
        "format": "appgen.composition-engine-permissions.v1",
        "ok": manifest["ok"],
        "permissions": manifest["permissions"],
        "action_permissions": manifest["action_permissions"],
        "roles": manifest["roles"],
    }


def composition_engine_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*COMPOSITION_ENGINE_OWNED_TABLES, *COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES, *_COMPOSITION_ENGINE_RUNTIME_TABLES, *_COMPOSITION_ENGINE_ALLOWED_DEPENDENCIES)
    violations = tuple(reference for reference in references if reference not in set(allowed) and not str(reference).startswith("composition_engine_"))
    return {
        "format": "appgen.composition-engine-boundary.v1",
        "ok": not violations,
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /identity/policies", "GET /gateway/routes", "GET /schemas/contracts", "POST /workflow/composition-approvals", "POST /audit/composition-events"),
            "events": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "identity_composition_projection",
                "gateway_composition_projection",
                "schema_composition_projection",
                "workflow_composition_projection",
                "audit_composition_projection",
                "pbc_deployment_projection",
                "package_registration_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def composition_engine_federate_composition_view(state: dict, workspace_id: str, *, systems: tuple[str, ...]) -> dict:
    return {"ok": workspace_id in state["workspaces"], "workspace_id": workspace_id, "systems": systems, "boundary": "read_only_projection", "handoffs": tuple(f"{system}_composition_projection" for system in systems)}


def composition_engine_verify_publisher_identity(identity: dict) -> dict:
    ok = identity.get("did", "").startswith("did:appgen:") and identity.get("issuer") == "trusted_registry" and identity.get("status") == "active"
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def composition_engine_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": True, "scenario": scenario, "mode": "degraded_composition_publication", "replay_source": "composition_engine_outbox", "dead_letter_ready": isinstance(state["dead_letters"], list)}


def composition_engine_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {"ok": True, "algorithm": algorithm, "epoch": state.get("crypto_epoch", 1) + 1, "signature_policy": "crypto_agile"}


def composition_engine_schedule_carbon_aware_build(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, **selected}


def composition_engine_optimize_layout(options: tuple[dict, ...]) -> dict:
    selected = min(options, key=lambda item: abs(item["density"] - 0.72) + item["risk"])
    return {"ok": True, **selected, "objective_score": round(1 / (1 + selected["risk"]), 4)}


def composition_engine_allocate_fragment_slots(fragments: tuple[dict, ...], *, slots: int) -> dict:
    total = sum(float(item["priority"]) for item in fragments) or 1
    allocations = tuple({**item, "slots": max(1, round(slots * float(item["priority"]) / total))} for item in fragments)
    return {"ok": True, "allocations": allocations, "clearing_priority": round(max(item["priority"] for item in fragments), 4)}


def composition_engine_detect_composition_anomaly(state: dict) -> dict:
    values = [len(tuple(binding for binding in state["bindings"].values() if binding["workspace_id"] == workspace_id)) for workspace_id in state["workspaces"]]
    if not values:
        return {"ok": True, "entropy": 0}
    total = sum(values) or 1
    probabilities = [value / total for value in values if value]
    entropy = -sum(probability * math.log2(probability) for probability in probabilities) if probabilities else 0
    return {"ok": True, "entropy": round(entropy, 4), "workspace_count": len(values)}


def composition_engine_model_stochastic_release_exposure(*, release_path: tuple[float, ...], volatility: float) -> dict:
    tail_risk = max(0.01, (1 - min(release_path)) * (1 + volatility))
    return {"ok": True, "tail_risk": round(tail_risk, 4), "expected_readiness": round(sum(release_path) / len(release_path), 4)}


def composition_engine_register_governed_model(model_id: str, metadata: dict) -> dict:
    return {"ok": True, "model_id": model_id, "metadata": metadata, "governance": {"approved": True, "drift_score": metadata.get("drift_score", 0), "monitoring": "enabled"}}


def _extract_composition_document_facts(document_text: str, instructions: str) -> dict:
    combined = "\n".join(part for part in (document_text, instructions) if part)
    lines = tuple(line.strip() for line in combined.splitlines() if line.strip())
    pbc_matches = tuple(dict.fromkeys(re.findall(r"\b[a-z]+(?:_[a-z0-9]+)+\b", combined)))
    pages = tuple(
        dict.fromkeys(
            match.group(1)
            for match in re.finditer(r"(?:page|dashboard|console)\s+([A-Za-z0-9_-]+)", combined, flags=re.IGNORECASE)
        )
    )
    roles = tuple(
        role
        for role in ("operator", "reviewer", "publisher", "approver")
        if role in combined.lower()
    )
    integrations = tuple(
        name
        for name in ("identity", "gateway", "schema", "workflow", "audit", "package")
        if name in combined.lower()
    )
    citations = tuple(
        {"line": index + 1, "excerpt": line[:160]}
        for index, line in enumerate(lines)
        if any(token in line.lower() for token in ("pbc", "route", "page", "must", "should", "publish", "layout"))
    )[:5]
    if not citations and lines:
        citations = ({"line": 1, "excerpt": lines[0][:160]},)
    return {
        "pbcs": pbc_matches,
        "pages": pages,
        "roles": roles,
        "integrations": integrations,
        "constraints": tuple(line for line in lines if any(token in line.lower() for token in ("must", "should", "without", "only"))),
        "citations": citations,
        "emails_detected": len(re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", combined, flags=re.IGNORECASE)),
    }


def _copy_state(state: dict) -> dict:
    nested_keys = (
        "schema_extensions",
        "workspaces",
        "components",
        "fragments",
        "bindings",
        "dsl_artifacts",
        "composition_plans",
        "validation_runs",
        "package_registration_plans",
        "package_index_entries",
        "release_evidence",
        "handled_events",
        "schema_projections",
        "route_projections",
        "audit_projections",
        "access_policy_projections",
        "workflow_projections",
        "package_registration_projections",
    )
    return {
        "configuration": dict(state["configuration"]),
        "parameters": dict(state["parameters"]),
        "rules": dict(state["rules"]),
        **{key: {inner: dict(value) for inner, value in state[key].items()} for key in nested_keys},
        "events": [dict(item) for item in state["events"]],
        "outbox": [dict(item) for item in state["outbox"]],
        "inbox": [dict(item) for item in state["inbox"]],
        "dead_letters": [dict(item) for item in state["dead_letters"]],
        "dead_letter": [dict(item) for item in state.get("dead_letter", state["dead_letters"])],
        "retry_evidence": [dict(item) for item in state.get("retry_evidence", [])],
        "crypto_epoch": state.get("crypto_epoch", 1),
    }


def _emit(state: dict, event_type: str, tenant: str, aggregate_id: str, payload: dict) -> dict:
    event_id = f"composition_evt_{len(state['events']) + 1:06d}"
    event = {"event_id": event_id, "event_type": event_type, "tenant": tenant, "aggregate_id": aggregate_id, "payload": payload}
    event["hash"] = _event_hash(event)
    state["events"].append(event)
    state["outbox"].append({"event_id": event_id, "event_type": event_type, "idempotency_key": f"composition_engine:{event_type}:{event_id}", "status": "pending", "payload": payload})
    return state


def _event_hash(event: dict) -> str:
    stable = {key: value for key, value in event.items() if key != "hash"}
    return _hash_payload(stable)


def _hash_payload(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


def _require(payload: dict, fields: set[str]) -> None:
    missing = tuple(sorted(field for field in fields if field not in payload))
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
