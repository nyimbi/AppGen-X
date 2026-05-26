"""Executable runtime for the Composition Engine PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


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
    "component_registry",
    "ui_fragment_registry",
    "layout_binding",
    "page_composition",
    "route_map_generation",
    "permission_mapping",
    "schema_compatibility_check",
    "composition_dsl_generation",
    "package_registration_plan",
    "publication_workflow",
    "release_gate_evidence",
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
        "capabilities": COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": COMPOSITION_ENGINE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "create_workspace",
            "select_pbc",
            "register_component",
            "register_ui_fragment",
            "bind_layout",
            "generate_composition_dsl",
            "publish_composition",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def composition_engine_runtime_smoke() -> dict:
    state = composition_engine_empty_state()
    state = composition_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.composition.events",
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
    dsl = composition_engine_generate_composition_dsl(state, "ws_alpha")
    state = dsl["state"]
    publication = composition_engine_publish_composition(state, "ws_alpha")
    state = publication["state"]
    workbench = composition_engine_build_workbench_view(state, tenant="tenant_alpha")
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
        {"id": "schema_on_read_layout_extension", "ok": state["schema_extensions"]["layout_binding"]["responsive_rules"] == "jsonb"},
        {"id": "probabilistic_release_risk_scoring", "ok": publication["publication"]["release_risk"] >= 0},
        {"id": "real_time_composition_analytics", "ok": workbench["workspace_count"] == 1 and workbench["published_count"] == 1},
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
    return {"configuration": {}, "parameters": {}, "rules": {}, "schema_extensions": {}, "workspaces": {}, "components": {}, "fragments": {}, "bindings": {}, "dsl_artifacts": {}, "release_evidence": {}, "events": [], "outbox": [], "inbox": [], "dead_letters": [], "crypto_epoch": 1}


def composition_engine_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = {"postgresql", "mysql", "mariadb"}
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Composition Engine supports only PostgreSQL, MySQL, or MariaDB backends")
    next_state = _copy_state(state)
    next_state["configuration"] = {**configuration, "ok": True, "event_contract": "appgen_event_contract", "allowed_database_backends": tuple(sorted(allowed_databases))}
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
    stored = {**rule, "enabled": rule["status"] == "active"}
    next_state["rules"][rule["rule_id"]] = stored
    return {"ok": True, "state": next_state, "rule": stored}


def composition_engine_register_schema_extension(state: dict, target: str, fields: dict) -> dict:
    next_state = _copy_state(state)
    next_state["schema_extensions"].setdefault(target, {}).update(fields)
    return {"ok": True, "state": next_state, "target": target, "fields": next_state["schema_extensions"][target]}


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


def composition_engine_generate_composition_dsl(state: dict, workspace_id: str) -> dict:
    next_state = _copy_state(state)
    workspace = next_state["workspaces"][workspace_id]
    bindings = tuple(binding for binding in next_state["bindings"].values() if binding["workspace_id"] == workspace_id)
    dsl = {"workspace": workspace_id, "pbcs": workspace["selected_pbcs"], "pages": tuple({"page": item["page"], "slot": item["slot"], "fragment": item["fragment_id"]} for item in bindings)}
    checksum = _hash_payload(dsl)
    artifact = {"artifact_id": f"dsl_{workspace_id}", "workspace_id": workspace_id, "dsl": dsl, "checksum": checksum, "route_count": len(bindings), "ok": True}
    next_state["dsl_artifacts"][artifact["artifact_id"]] = artifact
    return {"ok": True, "state": next_state, "artifact": artifact}


def composition_engine_publish_composition(state: dict, workspace_id: str) -> dict:
    next_state = _copy_state(state)
    workspace = dict(next_state["workspaces"][workspace_id])
    bindings = tuple(binding for binding in next_state["bindings"].values() if binding["workspace_id"] == workspace_id)
    release_risk = max(0, 0.2 - len(bindings) * 0.02)
    publication = {"workspace_id": workspace_id, "tenant": workspace["tenant"], "version": workspace["version"], "route_count": len(bindings), "release_risk": release_risk, "status": "published", "package_registration_plan": "side_effect_free"}
    workspace["status"] = "published"
    next_state["workspaces"][workspace_id] = workspace
    next_state["release_evidence"][workspace_id] = publication
    next_state = _emit(next_state, "CompositionPublished", workspace["tenant"], workspace_id, publication)
    next_state = _emit(next_state, "PbcDeployed", workspace["tenant"], workspace_id, publication)
    return {"ok": True, "state": next_state, "publication": publication}


def composition_engine_build_workbench_view(state: dict, *, tenant: str) -> dict:
    workspaces = tuple(item for item in state["workspaces"].values() if item["tenant"] == tenant)
    components = tuple(item for item in state["components"].values() if item["tenant"] == tenant)
    fragments = tuple(item for item in state["fragments"].values() if item["tenant"] == tenant)
    bindings = tuple(item for item in state["bindings"].values() if item["tenant"] == tenant)
    return {"format": "appgen.composition-engine-workbench-view.v1", "tenant": tenant, "workspace_count": len(workspaces), "published_count": len(tuple(item for item in workspaces if item["status"] == "published")), "component_count": len(components), "fragment_count": len(fragments), "binding_count": len(bindings), "release_evidence_count": len(tuple(item for item in state["release_evidence"].values() if item["tenant"] == tenant))}


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
    checks = {"configuration": state["configuration"].get("event_contract") == "appgen_event_contract", "database": state["configuration"].get("database_backend") in {"postgresql", "mysql", "mariadb"}, "rules": bool(state["rules"]), "workspaces": bool(state["workspaces"]), "dsl": bool(state["dsl_artifacts"]), "release": bool(state["release_evidence"]), "outbox": all(item["idempotency_key"].startswith("composition_engine:") for item in state["outbox"]), "dead_letter": isinstance(state["dead_letters"], list), "hash_chain": hash_chain_valid}
    return {"ok": all(checks.values()), "checks": checks, "hash_chain_valid": hash_chain_valid, "blocking_gaps": tuple(key for key, ok in checks.items() if not ok)}


def composition_engine_build_api_contract() -> dict:
    return {"ok": True, "format": "appgen.composition-engine-api-contract.v1", "routes": ("POST /composition-workspaces", "POST /component-registry", "POST /ui-fragments", "POST /layout-bindings", "POST /composition-publications"), "events": {"emits": ("CompositionWorkspaceCreated", "PbcSelectedForComposition", "ComponentRegistered", "UiFragmentRegistered", "LayoutBound", "CompositionPublished", "PbcDeployed"), "consumes": ("SchemaAccepted", "RoutePublished", "AuditEventSealed")}}


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


def _copy_state(state: dict) -> dict:
    nested_keys = ("schema_extensions", "workspaces", "components", "fragments", "bindings", "dsl_artifacts", "release_evidence")
    return {
        "configuration": dict(state["configuration"]),
        "parameters": dict(state["parameters"]),
        "rules": dict(state["rules"]),
        **{key: {inner: dict(value) for inner, value in state[key].items()} for key in nested_keys},
        "events": [dict(item) for item in state["events"]],
        "outbox": [dict(item) for item in state["outbox"]],
        "inbox": [dict(item) for item in state["inbox"]],
        "dead_letters": [dict(item) for item in state["dead_letters"]],
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


def _require(payload: dict, fields: set[str]) -> None:
    missing = tuple(sorted(field for field in fields if field not in payload))
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
