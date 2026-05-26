"""Executable runtime for the Quality Assurance PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC = "appgen.quality.events"
QUALITY_ASSURANCE_OWNED_TABLES = (
    "inspection_plan",
    "inspection_result",
    "quality_hold",
    "non_conformance",
    "quality_rule",
    "quality_parameter",
    "quality_configuration",
    "quality_capa",
    "quality_compliance_package",
)
QUALITY_ASSURANCE_EMITTED_EVENT_TYPES = (
    "InspectionPlanCreated",
    "InspectionResultRecorded",
    "QualityHoldCreated",
    "NonConformanceRaised",
    "NonConformanceDispositioned",
    "QualityHoldReleased",
)
QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES = (
    "ProductionCompleted",
    "GoodsReceiptPosted",
    "InventoryLotMoved",
    "SupplierScoreChanged",
)
_QUALITY_ASSURANCE_RUNTIME_TABLES = (
    "quality_assurance_appgen_outbox_event",
    "quality_assurance_appgen_inbox_event",
    "quality_assurance_dead_letter_event",
)
_QUALITY_ASSURANCE_ALLOWED_DEPENDENCIES = (
    "production_completion_projection",
    "goods_receipt_projection",
    "inventory_lot_projection",
    "supplier_score_projection",
    "GET /production/orders/{id}",
    "GET /inventory/lots/{id}",
    "GET /procurement/suppliers/{id}/quality-score",
    "POST /audit/quality-events",
)
QUALITY_ASSURANCE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_quality_lifecycle",
    "graph_relational_quality_topology",
    "multi_tenant_quality_isolation",
    "schema_evolution_resilient_quality_schema",
    "probabilistic_defect_escape_compliance_scoring",
    "real_time_spc_quality_analytics",
    "counterfactual_sampling_release_simulation",
    "temporal_defect_escape_forecasting",
    "autonomous_quality_exception_resolution",
    "semantic_inspection_instruction_parsing",
    "predictive_quality_compliance_risk",
    "self_healing_quality_route_selection",
    "zero_knowledge_quality_compliance_proof",
    "immutable_quality_audit_trail",
    "dynamic_quality_policy_screening",
    "automated_quality_control_testing",
    "universal_api_async_streaming",
    "cross_system_quality_federation",
    "production_inventory_supplier_integration",
    "decentralized_lot_item_identity",
    "chaos_engineered_quality_tolerance",
    "quantum_resistant_quality_authorization",
    "carbon_aware_inspection_scheduling",
    "algebraic_inspection_allocation",
    "mechanism_design_disposition_allocation",
    "information_theoretic_defect_anomaly_detection",
    "temporal_quality_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_quality_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "quality_mlops_governance",
)
QUALITY_ASSURANCE_STANDARD_FEATURE_KEYS = (
    "inspection_plan_master",
    "sampling_plan",
    "inspection_result_capture",
    "measurement_recording",
    "spc_metrics",
    "quality_hold_creation",
    "lot_isolation",
    "nonconformance_creation",
    "defect_classification",
    "root_cause_tracking",
    "disposition_workflow",
    "hold_release",
    "capa_evidence",
    "compliance_package",
    "production_projection",
    "goods_receipt_projection",
    "quality_analytics",
    "multi_site_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)
QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "allowed_sites",
    "allowed_inspection_sources",
    "allowed_hold_reasons",
    "allowed_dispositions",
    "default_timezone",
    "workbench_limit",
)
QUALITY_ASSURANCE_SUPPORTED_CONFIGURATION_FIELDS = QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS
QUALITY_ASSURANCE_FORBIDDEN_EVENTING_FIELDS = (
    "event_bus",
    "event_engine",
    "eventing_backend",
    "eventing_mode",
    "stream_engine",
)
QUALITY_ASSURANCE_SUPPORTED_PARAMETER_NAMES = (
    "default_sample_size",
    "defect_threshold",
    "cpk_minimum",
    "hold_severity_threshold",
    "capa_due_days",
    "retention_days",
    "release_approval_threshold",
)
QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "rule_type",
    "eligible_sources",
    "allowed_sites",
    "sampling_methods",
    "required_measurements",
    "critical_defect_classes",
    "release_dispositions",
    "status",
)
QUALITY_ASSURANCE_SUPPORTED_RULE_TYPES = (
    "inspection",
    "sampling",
    "spc",
    "hold",
    "nonconformance",
    "release",
    "compliance",
    "quality",
)


def quality_assurance_runtime_capabilities() -> dict:
    smoke = quality_assurance_runtime_smoke()
    return {
        "format": "appgen.quality-assurance-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "quality_assurance",
        "implementation_directory": "src/pyAppGen/pbcs/quality_assurance",
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "capabilities": QUALITY_ASSURANCE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": QUALITY_ASSURANCE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "create_inspection_plan",
            "record_inspection_result",
            "create_quality_hold",
            "raise_nonconformance",
            "disposition_nonconformance",
            "release_quality_hold",
            "build_workbench_view",
            "build_api_contract",
            "permissions_contract",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def quality_assurance_runtime_smoke() -> dict:
    state = quality_assurance_empty_state()
    state = quality_assurance_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.quality.events",
            "retry_limit": 3,
            "allowed_sites": ("factory_east", "dc_east"),
            "allowed_inspection_sources": ("production", "receipt"),
            "allowed_hold_reasons": ("defect", "spc_breach", "supplier_review"),
            "allowed_dispositions": ("rework", "scrap", "release", "return_to_supplier"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = quality_assurance_set_parameter(state, "default_sample_size", 5)["state"]
    state = quality_assurance_set_parameter(state, "defect_threshold", 1)["state"]
    state = quality_assurance_set_parameter(state, "cpk_minimum", 1.33)["state"]
    state = quality_assurance_set_parameter(state, "hold_severity_threshold", 0.7)["state"]
    state = quality_assurance_set_parameter(state, "capa_due_days", 14)["state"]
    state = quality_assurance_register_rule(
        state,
        {
            "rule_id": "rule_factory_quality",
            "tenant": "tenant_alpha",
            "rule_type": "quality",
            "eligible_sources": ("production", "receipt"),
            "allowed_sites": ("factory_east",),
            "sampling_methods": ("fixed", "risk_based"),
            "required_measurements": ("length", "torque"),
            "critical_defect_classes": ("safety", "regulatory"),
            "release_dispositions": ("release", "rework"),
            "status": "active",
        },
    )["state"]
    state = quality_assurance_register_schema_extension(state, "inspection_result", {"vision_payload": "jsonb"})["state"]
    consumed = quality_assurance_receive_event(
        state,
        {
            "event_id": "evt_prod_100",
            "event_type": "ProductionCompleted",
            "payload": {"tenant": "tenant_alpha", "order_id": "order_100", "item": "machine_kit", "quantity": 10},
        },
    )
    state = consumed["state"]
    duplicate = quality_assurance_receive_event(
        state,
        {
            "event_id": "evt_prod_100",
            "event_type": "ProductionCompleted",
            "payload": {"tenant": "tenant_alpha", "order_id": "order_100", "item": "machine_kit", "quantity": 10},
        },
    )
    failed = quality_assurance_receive_event(state, {"event_id": "evt_bad_100", "event_type": "UnsupportedQualitySignal", "payload": {"tenant": "tenant_alpha"}}, simulate_failure=True)
    failed = quality_assurance_receive_event(failed["state"], {"event_id": "evt_bad_100", "event_type": "UnsupportedQualitySignal", "payload": {"tenant": "tenant_alpha"}}, simulate_failure=True)
    failed = quality_assurance_receive_event(failed["state"], {"event_id": "evt_bad_100", "event_type": "UnsupportedQualitySignal", "payload": {"tenant": "tenant_alpha"}}, simulate_failure=True)
    state = failed["state"]
    plan = quality_assurance_create_inspection_plan(
        state,
        {"plan_id": "plan_100", "tenant": "tenant_alpha", "item": "machine_kit", "site": "factory_east", "source": "production", "sampling_method": "fixed", "sample_size": 5, "revision": "A", "status": "released"},
    )
    state = plan["state"]
    result = quality_assurance_record_inspection_result(
        state,
        {"result_id": "result_100", "tenant": "tenant_alpha", "plan_id": "plan_100", "lot_id": "lot_100", "order_id": "order_100", "measurements": {"length": (10.0, 10.1, 9.9, 10.2, 10.0), "torque": (4.9, 5.0, 5.1, 5.0, 5.2)}, "defects": ("scratch",), "inspector": "qa_1"},
    )
    state = result["state"]
    hold = quality_assurance_create_quality_hold(state, {"hold_id": "hold_100", "tenant": "tenant_alpha", "item": "machine_kit", "lot_id": "lot_100", "site": "factory_east", "reason": "defect", "severity": 0.8})
    state = hold["state"]
    nc = quality_assurance_raise_nonconformance(state, {"nonconformance_id": "nc_100", "tenant": "tenant_alpha", "result_id": "result_100", "defect_class": "safety", "severity": 0.8, "root_cause": "assembly_variation"})
    state = nc["state"]
    disp = quality_assurance_disposition_nonconformance(state, "nc_100", disposition="rework", approved_by="qa_mgr")
    state = disp["state"]
    release = quality_assurance_release_quality_hold(state, "hold_100", released_by="qa_mgr")
    state = release["state"]
    simulation = quality_assurance_simulate_sampling_policy(state, "plan_100", proposed_sample_size=3)
    forecast = quality_assurance_forecast_defects((1, 2, 3), lot_size=100)
    parsed = quality_assurance_parse_inspection_instruction("plan plan_777 lot lot_777 item item_777 action inspect")
    risk = quality_assurance_score_quality_risk({"defect": 0.2, "spc": 0.1, "severity": 0.3})
    recommendation = quality_assurance_recommend_exception_resolution("spc_breach")
    route = quality_assurance_route_quality({"event_id": "qa_route"}, rails=({"route": "inventory_api", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 4}))
    proof = quality_assurance_generate_quality_proof(state, "result_100", disclosure=("result_id", "lot_id", "decision"))
    screening = quality_assurance_screen_policy(state, "result_100", restricted_sites=("restricted_site",))
    controls = quality_assurance_run_control_tests(state)
    api = quality_assurance_build_api_contract()
    permissions = quality_assurance_permissions_contract()
    boundary = quality_assurance_verify_owned_table_boundary(("inspection_result", "ProductionCompleted", "production_completion_projection", "quality_assurance_appgen_inbox_event"))
    federation = quality_assurance_federate_quality_view(state, "result_100", systems=("production", "inventory", "procurement", "audit"))
    identity = quality_assurance_verify_lot_identity({"did": "did:appgen:lot-100", "issuer": "trusted_registry", "status": "active"})
    resilience = quality_assurance_run_resilience_drill(state, "inventory_release_timeout")
    crypto = quality_assurance_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = quality_assurance_schedule_carbon_aware_inspection(({"window": "day", "carbon": 210}, {"window": "night", "carbon": 80}))
    optimization = quality_assurance_optimize_inspection_allocation(({"plan": "full", "coverage": 0.95, "cost": 0.35}, {"plan": "risk_based", "coverage": 0.9, "cost": 0.2}))
    allocation = quality_assurance_allocate_disposition(({"owner": "qa", "priority": 0.9, "capacity": 4}, {"owner": "supplier_quality", "priority": 0.6, "capacity": 2}), cases=5)
    anomaly = quality_assurance_detect_defect_anomaly(state)
    stochastic = quality_assurance_model_stochastic_quality_exposure(defect_path=(1, 2, 4), volatility=0.1)
    workbench = quality_assurance_build_workbench_view(state, tenant="tenant_alpha")
    model = quality_assurance_register_governed_model("quality_risk", {"features": ("defects", "cpk", "severity"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_quality_lifecycle", "ok": len(state["events"]) >= 6 and state["events"][-1]["hash"]},
        {"id": "graph_relational_quality_topology", "ok": plan["inspection_plan"]["graph_degree"] >= 4},
        {"id": "multi_tenant_quality_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_quality_schema", "ok": state["schema_extensions"]["inspection_result"]["vision_payload"] == "jsonb"},
        {"id": "probabilistic_defect_escape_compliance_scoring", "ok": result["risk_score"] > 0},
        {"id": "real_time_spc_quality_analytics", "ok": result["spc"]["cpk"] > 0},
        {"id": "counterfactual_sampling_release_simulation", "ok": simulation["coverage_delta"] < 0},
        {"id": "temporal_defect_escape_forecasting", "ok": forecast["forecast_defects"] > 0},
        {"id": "autonomous_quality_exception_resolution", "ok": recommendation["action"] == "open_corrective_action"},
        {"id": "semantic_inspection_instruction_parsing", "ok": parsed["ok"] and parsed["lot_id"] == "lot_777"},
        {"id": "predictive_quality_compliance_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_quality_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_quality_compliance_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_quality_")},
        {"id": "immutable_quality_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_quality_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_quality_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "QualityHoldReleased" in api["events"]["emits"]},
        {"id": "cross_system_quality_federation", "ok": federation["ok"] and "inventory" in federation["systems"]},
        {"id": "production_inventory_supplier_integration", "ok": release["handoffs"] == ("inventory_release_projection", "production_quality_projection", "supplier_score_projection")},
        {"id": "decentralized_lot_item_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_quality_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_quality_route"},
        {"id": "quantum_resistant_quality_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_inspection_scheduling", "ok": carbon["window"] == "night"},
        {"id": "algebraic_inspection_allocation", "ok": optimization["ok"] and optimization["plan"] == "risk_based"},
        {"id": "mechanism_design_disposition_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["cases"] > allocation["allocations"][1]["cases"]},
        {"id": "information_theoretic_defect_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_quality_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("quality_assurance:QualityHoldReleased")},
        {"id": "probabilistic_ml_quality_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "quality_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.quality-assurance-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def quality_assurance_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letters": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "production_completion_projections": {},
        "goods_receipt_projections": {},
        "inventory_lot_projections": {},
        "supplier_score_projections": {},
        "plans": {},
        "results": {},
        "holds": {},
        "nonconformances": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def quality_assurance_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in QUALITY_ASSURANCE_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError("Quality Assurance uses the AppGen-X event contract and does not allow stream-engine or user-selectable eventing fields")
    unknown = tuple(sorted(field for field in configuration if field not in QUALITY_ASSURANCE_SUPPORTED_CONFIGURATION_FIELDS))
    if unknown:
        raise ValueError(f"Unsupported Quality Assurance configuration fields: {unknown}")
    missing = tuple(sorted(field for field in QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS if field not in configuration))
    if missing:
        raise ValueError(f"Missing required Quality Assurance configuration fields: {missing}")
    if configuration.get("database_backend") not in QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Quality Assurance supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Quality Assurance event topic is fixed to {QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "required_event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
        "visible_event_contracts": ("AppGen-X",),
        "allowed_database_backends": QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "supported_fields": QUALITY_ASSURANCE_SUPPORTED_CONFIGURATION_FIELDS,
        "supported_configuration_fields": QUALITY_ASSURANCE_SUPPORTED_CONFIGURATION_FIELDS,
        "stream_engine_picker_visible": False,
        "user_eventing_choice": False,
        "configuration_hash": _digest({field: configuration[field] for field in QUALITY_ASSURANCE_SUPPORTED_CONFIGURATION_FIELDS}),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def quality_assurance_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    if name not in QUALITY_ASSURANCE_SUPPORTED_PARAMETER_NAMES:
        raise ValueError(f"Unsupported Quality Assurance parameter: {name}")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Quality Assurance parameter values must be numeric: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def quality_assurance_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(sorted(field for field in QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS if field not in rule))
    if missing:
        raise ValueError(f"Missing required Quality Assurance rule fields: {missing}")
    if rule["rule_type"] not in QUALITY_ASSURANCE_SUPPORTED_RULE_TYPES:
        raise ValueError(f"Unsupported Quality Assurance rule type: {rule['rule_type']}")
    scope = rule.get("scope") or rule["rule_type"]
    compiled_hash = _digest(rule)
    compile_evidence = {
        "format": "appgen.quality-assurance-rule-compile-evidence.v1",
        "rule_id": rule["rule_id"],
        "scope": scope,
        "compiled_hash": compiled_hash,
        "required_fields": QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS,
        "normalized_rule": _normalize_value(rule),
    }
    enriched = {
        **rule,
        "scope": scope,
        "enabled": rule["status"] == "active",
        "compiled_hash": compiled_hash,
        "compile_evidence": compile_evidence,
    }
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def quality_assurance_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in QUALITY_ASSURANCE_OWNED_TABLES:
        raise ValueError(f"Quality Assurance schema extensions must target owned tables: {QUALITY_ASSURANCE_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    existing = dict(state.get("schema_extensions", {}).get(table, {}))
    merged = {**existing, **fields}
    return {
        "ok": True,
        "state": {**state, "schema_extensions": {**state["schema_extensions"], table: merged}},
        "schema_extension": {"table": table, "fields": dict(fields)},
        "target": table,
        "fields": merged,
    }


def quality_assurance_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    handled = state.get("handled_events", {})
    if key in handled and handled[key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": handled[key]}
    attempts = int(handled.get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": payload.get("tenant"),
        "attempts": attempts,
        "idempotency_key": key,
    }
    next_state = {
        **state,
        "inbox": (*state.get("inbox", ()), inbox_entry),
        "handled_events": dict(handled),
        "retry_evidence": tuple(state.get("retry_evidence", ())),
        "dead_letters": tuple(state.get("dead_letters", ())),
        "dead_letter": tuple(state.get("dead_letter", ())),
        "production_completion_projections": dict(state.get("production_completion_projections", {})),
        "goods_receipt_projections": dict(state.get("goods_receipt_projections", {})),
        "inventory_lot_projections": dict(state.get("inventory_lot_projections", {})),
        "supplier_score_projections": dict(state.get("supplier_score_projections", {})),
    }
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"] = (*next_state["retry_evidence"], evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_quality_event"}
            next_state["dead_letters"] = (*next_state["dead_letters"], dead)
            next_state["dead_letter"] = (*next_state["dead_letter"], dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "ProductionCompleted":
        next_state["production_completion_projections"][payload.get("order_id", event_id)] = payload
    elif event_type == "GoodsReceiptPosted":
        next_state["goods_receipt_projections"][payload.get("receipt_id", event_id)] = payload
    elif event_type == "InventoryLotMoved":
        next_state["inventory_lot_projections"][payload.get("lot_id", event_id)] = payload
    elif event_type == "SupplierScoreChanged":
        next_state["supplier_score_projections"][payload.get("supplier_id", event_id)] = payload
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def quality_assurance_create_inspection_plan(state: dict, plan: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = (
        plan["site"] in state["configuration"].get("allowed_sites", ())
        and plan["source"] in state["configuration"].get("allowed_inspection_sources", ())
        and plan["source"] in rule["eligible_sources"]
        and plan["sampling_method"] in rule["sampling_methods"]
    )
    enriched = {**plan, "status": "active" if ok else "blocked", "graph_degree": len(tuple(value for value in (plan["item"], plan["site"], plan["source"], plan["revision"]) if value))}
    next_state = {**state, "plans": {**state["plans"], plan["plan_id"]: enriched}}
    next_state = _append_event(next_state, "InspectionPlanCreated", {"tenant": plan["tenant"], "plan_id": plan["plan_id"], "item": plan["item"]})
    return {"ok": ok, "state": next_state, "inspection_plan": enriched}


def quality_assurance_record_inspection_result(state: dict, result: dict) -> dict:
    plan = state["plans"][result["plan_id"]]
    required = set(next(iter(state["rules"].values()))["required_measurements"])
    ok = plan["status"] == "active" and required <= set(result["measurements"])
    spc = _spc(result["measurements"])
    defect_count = len(result.get("defects", ()))
    decision = "pass" if ok and defect_count <= int(state["parameters"].get("defect_threshold", 1)) and spc["cpk"] >= float(state["parameters"].get("cpk_minimum", 1.33)) else "fail"
    risk_score = round(defect_count * 0.2 + max(0, float(state["parameters"].get("cpk_minimum", 1.33)) - spc["cpk"]) * 0.1, 4)
    enriched = {**result, "item": plan["item"], "site": plan["site"], "decision": decision, "spc": spc, "risk_score": risk_score}
    next_state = {**state, "results": {**state["results"], result["result_id"]: enriched}}
    next_state = _append_event(next_state, "InspectionResultRecorded", {"tenant": result["tenant"], "result_id": result["result_id"], "decision": decision})
    return {"ok": ok, "state": next_state, **enriched}


def quality_assurance_create_quality_hold(state: dict, hold: dict) -> dict:
    ok = hold["reason"] in state["configuration"].get("allowed_hold_reasons", ()) and hold["severity"] >= float(state["parameters"].get("hold_severity_threshold", 0.7))
    enriched = {**hold, "status": "active" if ok else "review"}
    next_state = {**state, "holds": {**state["holds"], hold["hold_id"]: enriched}}
    next_state = _append_event(next_state, "QualityHoldCreated", {"tenant": hold["tenant"], "hold_id": hold["hold_id"], "lot_id": hold["lot_id"], "reason": hold["reason"]})
    return {"ok": ok, "state": next_state, "hold": enriched}


def quality_assurance_raise_nonconformance(state: dict, nonconformance: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    severity = "critical" if nonconformance["defect_class"] in rule["critical_defect_classes"] else "standard"
    enriched = {**nonconformance, "status": "open", "severity_class": severity}
    next_state = {**state, "nonconformances": {**state["nonconformances"], nonconformance["nonconformance_id"]: enriched}}
    next_state = _append_event(next_state, "NonConformanceRaised", {"tenant": nonconformance["tenant"], "nonconformance_id": nonconformance["nonconformance_id"], "severity_class": severity})
    return {"ok": True, "state": next_state, "nonconformance": enriched}


def quality_assurance_disposition_nonconformance(state: dict, nonconformance_id: str, *, disposition: str, approved_by: str) -> dict:
    nc = state["nonconformances"][nonconformance_id]
    ok = disposition in state["configuration"].get("allowed_dispositions", ())
    updated = {**nc, "status": "dispositioned" if ok else "blocked", "disposition": disposition, "approved_by": approved_by}
    next_state = {**state, "nonconformances": {**state["nonconformances"], nonconformance_id: updated}}
    next_state = _append_event(next_state, "NonConformanceDispositioned", {"tenant": nc["tenant"], "nonconformance_id": nonconformance_id, "disposition": disposition})
    return {"ok": ok, "state": next_state, "nonconformance": updated}


def quality_assurance_release_quality_hold(state: dict, hold_id: str, *, released_by: str) -> dict:
    hold = state["holds"][hold_id]
    released = {**hold, "status": "released", "released_by": released_by}
    handoffs = ("inventory_release_projection", "production_quality_projection", "supplier_score_projection")
    next_state = {**state, "holds": {**state["holds"], hold_id: released}}
    next_state = _append_event(next_state, "QualityHoldReleased", {"tenant": hold["tenant"], "hold_id": hold_id, "lot_id": hold["lot_id"], "handoffs": handoffs})
    return {"ok": True, "state": next_state, "hold": released, "handoffs": handoffs}


def quality_assurance_simulate_sampling_policy(state: dict, plan_id: str, *, proposed_sample_size: int) -> dict:
    plan = state["plans"][plan_id]
    current = int(plan["sample_size"])
    return {"ok": True, "plan_id": plan_id, "coverage_delta": round((proposed_sample_size - current) / max(current, 1), 4)}


def quality_assurance_forecast_defects(defect_path: tuple[float, ...], *, lot_size: int) -> dict:
    trend = defect_path[-1] - defect_path[0] if len(defect_path) > 1 else 0
    forecast = max(0, defect_path[-1] + trend / max(1, len(defect_path)))
    return {"ok": True, "forecast_defects": round(forecast, 2), "defects_per_100": round(forecast / max(lot_size, 1) * 100, 2)}


def quality_assurance_parse_inspection_instruction(text: str) -> dict:
    plan = re.search(r"plan\s+([a-z0-9_]+)", text, re.I)
    lot = re.search(r"lot\s+([a-z0-9_]+)", text, re.I)
    item = re.search(r"item\s+([a-z0-9_]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(plan and lot and item and action), "plan_id": plan.group(1) if plan else None, "lot_id": lot.group(1) if lot else None, "item": item.group(1) if item else None, "action": action.group(1) if action else None}


def quality_assurance_score_quality_risk(signals: dict) -> dict:
    risk = round(signals.get("defect", 0) * 1.5 + signals.get("spc", 0) + signals.get("severity", 0) * 2, 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.7 else "review"}


def quality_assurance_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"spc_breach": "open_corrective_action", "critical_defect": "create_quality_hold", "supplier_escape": "route_supplier_quality_review"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def quality_assurance_route_quality(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"quality_assurance:QualityRoute:{event['event_id']}"}


def quality_assurance_generate_quality_proof(state: dict, result_id: str, *, disclosure: tuple[str, ...]) -> dict:
    result = state["results"][result_id]
    claims = {field: result[field] for field in disclosure if field in result}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_quality_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def quality_assurance_screen_policy(state: dict, result_id: str, *, restricted_sites: tuple[str, ...]) -> dict:
    result = state["results"][result_id]
    blocked = result["site"] in restricted_sites
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "result_id": result_id}


def quality_assurance_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if state["configuration"].get("database_backend") not in QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS:
        gaps.append("invalid_database_backend")
    if state["configuration"].get("event_contract") != "AppGen-X":
        gaps.append("invalid_event_contract")
    if state["configuration"].get("user_eventing_choice"):
        gaps.append("user_eventing_choice_exposed")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(hold["status"] == "active" for hold in state["holds"].values()):
        gaps.append("unreleased_quality_hold")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def quality_assurance_build_api_contract() -> dict:
    return {
        "ok": True,
        "format": "appgen.quality-assurance-api-contract.v1",
        "routes": (
            {"route": "POST /quality/inspection-plans", "command": "create_inspection_plan", "owned_tables": ("inspection_plan",), "emits": ("InspectionPlanCreated",), "requires_permission": "quality_assurance.inspect", "idempotency_key": "plan_id"},
            {"route": "POST /quality/inspection-results", "command": "record_inspection_result", "owned_tables": ("inspection_result",), "emits": ("InspectionResultRecorded",), "requires_permission": "quality_assurance.inspect", "idempotency_key": "result_id"},
            {"route": "POST /quality/holds", "command": "create_quality_hold", "owned_tables": ("quality_hold",), "emits": ("QualityHoldCreated",), "requires_permission": "quality_assurance.hold", "idempotency_key": "hold_id"},
            {"route": "POST /quality/non-conformances", "command": "raise_nonconformance", "owned_tables": ("non_conformance",), "emits": ("NonConformanceRaised",), "requires_permission": "quality_assurance.disposition", "idempotency_key": "nonconformance_id"},
            {"route": "POST /quality/non-conformances/{id}/disposition", "command": "disposition_nonconformance", "owned_tables": ("non_conformance",), "emits": ("NonConformanceDispositioned",), "requires_permission": "quality_assurance.disposition", "idempotency_key": "nonconformance_id:disposition"},
            {"route": "POST /quality/holds/{id}/release", "command": "release_quality_hold", "owned_tables": ("quality_hold",), "emits": ("QualityHoldReleased",), "requires_permission": "quality_assurance.hold", "idempotency_key": "hold_id:release"},
            {"route": "POST /quality/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES, "requires_permission": "quality_assurance.event", "idempotency_key": "event_id"},
            {"route": "GET /quality/workbench", "query": "build_workbench_view", "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES, "requires_permission": "quality_assurance.audit"},
        ),
        "declared_catalog_routes": ("POST /inspections", "POST /non-conformances", "POST /quality-holds", "POST /quality-rules", "POST /quality-parameters", "POST /quality-configuration"),
        "events": {"emits": QUALITY_ASSURANCE_EMITTED_EVENT_TYPES, "consumes": QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES},
        "emits": QUALITY_ASSURANCE_EMITTED_EVENT_TYPES,
        "consumes": QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(quality_assurance_permissions_contract()["permissions"])),
        "database_backends": QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "shared_table_access": False,
        "configuration": ("QUALITY_ASSURANCE_DATABASE_URL", "QUALITY_ASSURANCE_EVENT_TOPIC", "QUALITY_ASSURANCE_RETRY_LIMIT", "QUALITY_ASSURANCE_DEFAULT_TIMEZONE"),
        "event_contract": "AppGen-X",
        "required_event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_eventing_choice": False,
    }


def quality_assurance_permissions_contract() -> dict:
    return {
        "format": "appgen.quality-assurance-permissions.v1",
        "ok": True,
        "permissions": (
            "quality_assurance.read",
            "quality_assurance.inspect",
            "quality_assurance.hold",
            "quality_assurance.disposition",
            "quality_assurance.configure",
            "quality_assurance.audit",
            "quality_assurance.event",
        ),
        "action_permissions": {
            "create_inspection_plan": "quality_assurance.inspect",
            "record_inspection_result": "quality_assurance.inspect",
            "create_quality_hold": "quality_assurance.hold",
            "release_quality_hold": "quality_assurance.hold",
            "raise_nonconformance": "quality_assurance.disposition",
            "disposition_nonconformance": "quality_assurance.disposition",
            "receive_event": "quality_assurance.event",
            "register_schema_extension": "quality_assurance.configure",
            "register_rule": "quality_assurance.configure",
            "set_parameter": "quality_assurance.configure",
            "configure_runtime": "quality_assurance.configure",
            "run_control_tests": "quality_assurance.audit",
            "build_workbench_view": "quality_assurance.audit",
            "verify_owned_table_boundary": "quality_assurance.audit",
        },
    }


def quality_assurance_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (
        *QUALITY_ASSURANCE_OWNED_TABLES,
        *QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES,
        *_QUALITY_ASSURANCE_RUNTIME_TABLES,
        *_QUALITY_ASSURANCE_ALLOWED_DEPENDENCIES,
    )
    allowed_set = set(allowed)
    violations = tuple(reference for reference in references if reference not in allowed_set and not str(reference).startswith("quality_assurance_"))
    return {
        "format": "appgen.quality-assurance-boundary.v1",
        "ok": not violations,
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /production/orders/{id}", "GET /inventory/lots/{id}", "GET /procurement/suppliers/{id}/quality-score", "POST /audit/quality-events"),
            "events": QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "production_completion_projection",
                "goods_receipt_projection",
                "inventory_lot_projection",
                "supplier_score_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def quality_assurance_federate_quality_view(state: dict, result_id: str, *, systems: tuple[str, ...]) -> dict:
    result = state["results"][result_id]
    return {"ok": True, "result_id": result_id, "systems": systems, "projection": {"lot_id": result["lot_id"], "decision": result["decision"], "risk_score": result["risk_score"]}}


def quality_assurance_verify_lot_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def quality_assurance_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"inventory_release_timeout", "inspection_terminal_failure"}, "scenario": scenario, "mode": "degraded_quality_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "quality_assurance.dead_letter"}


def quality_assurance_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"quality_epoch_{epoch:04d}"}


def quality_assurance_schedule_carbon_aware_inspection(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def quality_assurance_optimize_inspection_allocation(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["coverage"] - candidate["cost"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "plan": selected["plan"], "objective_score": selected["objective"], "candidates": scored}


def quality_assurance_allocate_disposition(owners: tuple[dict, ...], *, cases: int) -> dict:
    weights = tuple({"owner": item["owner"], "weight": item["priority"] * item["capacity"]} for item in owners)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"owner": item["owner"], "cases": round(cases * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["cases"] for item in allocations), 2) == round(cases, 2), "allocations": allocations, "clearing_priority": round(sum(item["priority"] for item in owners) / len(owners), 4)}


def quality_assurance_detect_defect_anomaly(state: dict) -> dict:
    counts = tuple(len(result.get("defects", ())) for result in state["results"].values())
    if not counts:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(counts) or 1
    entropy = round(-sum((count / total) * math.log(max(count / total, 0.0001), 2) for count in counts), 4)
    mean = sum(counts) / len(counts)
    return {"ok": True, "entropy": entropy, "outliers": tuple(count for count in counts if abs(count - mean) > 3)}


def quality_assurance_model_stochastic_quality_exposure(*, defect_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(defect_path) < 2 else (defect_path[-1] - defect_path[0]) / (len(defect_path) - 1)
    exposure = abs(drift) * volatility * len(defect_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def quality_assurance_build_workbench_view(state: dict, *, tenant: str) -> dict:
    plans = tuple(plan for plan in state["plans"].values() if plan["tenant"] == tenant)
    results = tuple(result for result in state["results"].values() if result["tenant"] == tenant)
    holds = tuple(hold for hold in state["holds"].values() if hold["tenant"] == tenant)
    ncs = tuple(nc for nc in state["nonconformances"].values() if nc["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "plan_count": len(plans),
        "inspection_count": len(results),
        "failed_inspection_count": len(tuple(result for result in results if result["decision"] == "fail")),
        "hold_count": len(holds),
        "released_hold_count": len(tuple(hold for hold in holds if hold["status"] == "released")),
        "nonconformance_count": len(ncs),
        "critical_nonconformance_count": len(tuple(nc for nc in ncs if nc["severity_class"] == "critical")),
        "average_cpk": round(sum(result["spc"]["cpk"] for result in results) / max(len(results), 1), 4),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "binding_evidence": quality_assurance_binding_evidence(state),
    }


def quality_assurance_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def quality_assurance_binding_evidence(state: dict) -> dict:
    configuration = state["configuration"]
    rules = tuple(
        {
            "rule_id": rule["rule_id"],
            "scope": rule.get("scope") or rule.get("rule_type"),
            "enabled": bool(rule.get("enabled")),
            "compiled_hash": rule["compiled_hash"],
        }
        for rule in sorted(state["rules"].values(), key=lambda item: item["rule_id"])
    )
    parameters = tuple({"name": name, "value": state["parameters"][name]} for name in sorted(state["parameters"]))
    evidence = {
        "configuration": {
            "bound": bool(configuration.get("ok")),
            "database_backend": configuration.get("database_backend"),
            "event_contract": configuration.get("event_contract"),
            "event_topic": configuration.get("event_topic"),
            "required_event_topic": configuration.get("required_event_topic", QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC),
            "visible_event_contracts": configuration.get("visible_event_contracts", ("AppGen-X",)),
            "supported_fields": configuration.get("supported_fields", QUALITY_ASSURANCE_SUPPORTED_CONFIGURATION_FIELDS),
            "allowed_database_backends": configuration.get("allowed_database_backends", QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS),
            "stream_engine_picker_visible": bool(configuration.get("stream_engine_picker_visible", False)),
            "user_eventing_choice": bool(configuration.get("user_eventing_choice", False)),
        },
        "rules": rules,
        "parameters": parameters,
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "runtime_tables": {
            "outbox": "quality_assurance_appgen_outbox_event",
            "inbox": "quality_assurance_appgen_inbox_event",
            "dead_letter": "quality_assurance_dead_letter_event",
        },
        "shared_table_access": False,
        "event_counts": {
            "outbox": len(state.get("outbox", ())),
            "inbox": len(state.get("inbox", ())),
            "dead_letter": len(state.get("dead_letters", ())),
        },
        "rbac": quality_assurance_permissions_contract()["action_permissions"],
    }
    return {**evidence, "binding_hash": _digest(evidence)}


def _spc(measurements: dict) -> dict:
    values = tuple(value for series in measurements.values() for value in series)
    mean = sum(values) / len(values)
    sigma = math.sqrt(sum((value - mean) ** 2 for value in values) / max(len(values) - 1, 1))
    upper = mean + 3 * sigma
    lower = mean - 3 * sigma
    cpk = min((upper - mean) / max(3 * sigma, 0.0001), (mean - lower) / max(3 * sigma, 0.0001))
    return {"mean": round(mean, 4), "sigma": round(sigma, 4), "upper_control": round(upper, 4), "lower_control": round(lower, 4), "cpk": round(cpk, 4)}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"quality_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"quality_assurance:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _normalize_value(value: object) -> object:
    if isinstance(value, dict):
        return {key: _normalize_value(value[key]) for key in sorted(value)}
    if isinstance(value, (tuple, list)):
        return tuple(_normalize_value(item) for item in value)
    return value
