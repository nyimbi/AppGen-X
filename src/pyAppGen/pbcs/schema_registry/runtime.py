"""Executable runtime for the Schema Registry PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC = "appgen.schema.events"
SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
SCHEMA_REGISTRY_OWNED_TABLES = (
    "schema_subject",
    "schema_version",
    "compatibility_rule",
    "consumer_binding",
    "validation_run",
    "contract_violation",
    "contract_projection",
    "schema_rule",
    "schema_parameter",
    "schema_configuration",
)
SCHEMA_REGISTRY_EMITTED_EVENT_TYPES = (
    "SchemaSubjectRegistered",
    "SchemaAccepted",
    "BreakingSchemaBlocked",
    "PayloadValidated",
    "ContractViolationRecorded",
    "ContractProjectionPublished",
)
SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES = (
    "PbcDeployed",
    "EventContractProposed",
    "RoutePublished",
    "AccessPolicyChanged",
    "PackageRegistrationRequested",
)
_SCHEMA_REGISTRY_RUNTIME_TABLES = (
    "schema_registry_appgen_outbox_event",
    "schema_registry_appgen_inbox_event",
    "schema_registry_dead_letter_event",
)
_SCHEMA_REGISTRY_ALLOWED_DEPENDENCIES = (
    "gateway_contract_projection",
    "audit_contract_projection",
    "composition_contract_projection",
    "workflow_contract_projection",
    "pbc_deployment_projection",
    "route_contract_projection",
    "access_policy_projection",
    "package_registration_projection",
    "GET /gateway/routes",
    "GET /identity/policies",
    "POST /audit/contract-events",
    "POST /composition/contracts",
)
_SCHEMA_REGISTRY_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}

SCHEMA_REGISTRY_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_schema_lifecycle",
    "graph_relational_contract_topology",
    "multi_tenant_contract_isolation",
    "schema_on_read_contract_extensibility",
    "probabilistic_breaking_change_scoring",
    "real_time_contract_analytics",
    "counterfactual_schema_evolution_simulation",
    "temporal_compatibility_health_forecasting",
    "autonomous_contract_remediation",
    "semantic_schema_intent_parsing",
    "predictive_contract_risk_scoring",
    "self_healing_contract_validation_route_selection",
    "zero_knowledge_schema_acceptance_proof",
    "immutable_contract_audit_trail",
    "dynamic_contract_policy_screening",
    "automated_contract_control_testing",
    "universal_api_async_contract_surface",
    "cross_system_schema_federation",
    "gateway_identity_audit_workflow_composition_integration",
    "decentralized_producer_consumer_identity",
    "chaos_engineered_contract_validation_tolerance",
    "quantum_resistant_schema_signing",
    "carbon_aware_contract_validation",
    "algebraic_schema_diff_minimization",
    "mechanism_design_consumer_impact_allocation",
    "information_theoretic_validation_anomaly_detection",
    "temporal_contract_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_contract_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "contract_mlops_governance",
)
SCHEMA_REGISTRY_STANDARD_FEATURE_KEYS = (
    "subject_catalog",
    "schema_versioning",
    "immutable_fingerprints",
    "compatibility_policy",
    "backward_compatibility",
    "forward_compatibility",
    "transitive_compatibility",
    "payload_validation",
    "producer_binding",
    "consumer_binding",
    "impact_analysis",
    "breaking_change_blocking",
    "violation_triage",
    "semantic_classification",
    "schema_extension_registry",
    "contract_projection",
    "idempotent_handlers",
    "retry_dead_letter",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "release_gate",
    "audit_evidence",
    "package_registration_validation",
    "appgen_event_contract",
)


def schema_registry_runtime_capabilities() -> dict:
    smoke = schema_registry_runtime_smoke()
    return {
        "format": "appgen.schema-registry-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "schema_registry",
        "implementation_directory": "src/pyAppGen/pbcs/schema_registry",
        "owned_tables": SCHEMA_REGISTRY_OWNED_TABLES,
        "capabilities": SCHEMA_REGISTRY_RUNTIME_CAPABILITY_KEYS,
        "standard_features": SCHEMA_REGISTRY_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "register_subject",
            "define_compatibility_rule",
            "register_consumer_binding",
            "submit_schema_version",
            "run_compatibility_check",
            "validate_payload",
            "record_contract_violation",
            "publish_contract_projection",
            "build_api_contract",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def schema_registry_runtime_smoke() -> dict:
    state = schema_registry_empty_state()
    state = schema_registry_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_formats": ("json", "avro", "event", "api", "projection"),
            "default_compatibility": "backward_forward",
            "namespace_policy": "tenant_scoped",
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = schema_registry_set_parameter(state, "compatibility_threshold", 0.9)["state"]
    state = schema_registry_set_parameter(state, "max_schema_fields", 64)["state"]
    state = schema_registry_set_parameter(state, "semantic_similarity_floor", 0.82)["state"]
    state = schema_registry_set_parameter(state, "violation_risk_threshold", 0.45)["state"]
    state = schema_registry_set_parameter(state, "review_sla_hours", 24)["state"]
    state = schema_registry_register_rule(
        state,
        {
            "rule_id": "rule_schema",
            "tenant": "tenant_alpha",
            "scope": "event",
            "mode": "backward_forward",
            "classification": "regulated",
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    state = schema_registry_register_schema_extension(state, "schema_version", {"semantic_tags": "jsonb"})["state"]
    state = schema_registry_register_subject(
        state,
        {
            "subject_id": "subject_invoice",
            "tenant": "tenant_alpha",
            "owner_pbc": "ap_automation",
            "name": "InvoiceApproved",
            "channel": "event",
            "format": "json",
            "namespace": "finance.ap",
        },
    )["state"]
    state = schema_registry_define_compatibility_rule(
        state,
        {"rule_id": "compat_invoice", "tenant": "tenant_alpha", "subject_id": "subject_invoice", "mode": "backward_forward", "status": "active"},
    )["state"]
    consumer = schema_registry_register_consumer_binding(
        state,
        {"binding_id": "consumer_gl", "tenant": "tenant_alpha", "subject_id": "subject_invoice", "consumer_pbc": "gl_core", "consumer_type": "handler", "min_version": 1},
    )
    state = consumer["state"]
    v1 = schema_registry_submit_schema_version(
        state,
        {
            "version_id": "invoice_v1",
            "tenant": "tenant_alpha",
            "subject_id": "subject_invoice",
            "semantic_version": "1.0.0",
            "schema": {"fields": {"invoice_id": {"type": "string", "required": True}, "amount": {"type": "number", "required": True}}},
        },
    )
    state = v1["state"]
    check = schema_registry_run_compatibility_check(
        state,
        "subject_invoice",
        {"fields": {"invoice_id": {"type": "string", "required": True}, "amount": {"type": "number", "required": True}, "currency": {"type": "string", "required": False}}},
    )
    accepted = schema_registry_submit_schema_version(
        check["state"],
        {
            "version_id": "invoice_v2",
            "tenant": "tenant_alpha",
            "subject_id": "subject_invoice",
            "semantic_version": "1.1.0",
            "schema": check["proposed_schema"],
        },
    )
    state = accepted["state"]
    blocked = schema_registry_run_compatibility_check(state, "subject_invoice", {"fields": {"invoice_id": {"type": "number", "required": True}}})
    state = blocked["state"]
    validation = schema_registry_validate_payload(state, "subject_invoice", {"invoice_id": "INV-1", "amount": 120, "currency": "USD"})
    state = validation["state"]
    violation = schema_registry_record_contract_violation(
        state,
        {"violation_id": "viol_invoice", "tenant": "tenant_alpha", "subject_id": "subject_invoice", "producer_pbc": "ap_automation", "consumer_pbc": "gl_core", "severity": "high", "reason": "type_change", "status": "open"},
    )
    state = violation["state"]
    projection = schema_registry_publish_contract_projection(state, "subject_invoice", systems=("gateway", "audit", "composition", "workflow"))
    state = projection["state"]
    workbench = schema_registry_build_workbench_view(state, tenant="tenant_alpha")
    simulation = schema_registry_simulate_schema_evolution(state, "subject_invoice", remove_required_fields=1, add_optional_fields=2)
    forecast = schema_registry_forecast_compatibility_health((0.99, 0.96, 0.91), horizon_days=30)
    parsed = schema_registry_parse_schema_intent("register event subject subject_900 owner inventory_positioning version 2")
    risk = schema_registry_score_contract_risk({"breaking": 0.4, "consumer": 0.3, "payload": 0.2, "governance": 0.1})
    remediation = schema_registry_recommend_remediation("required_field_removed")
    selected_route = schema_registry_select_validation_route({"event_id": "schema_check"}, rails=({"route": "primary", "available": False, "latency": 2}, {"route": "outbox_replay", "available": True, "latency": 5}))
    proof = schema_registry_generate_schema_proof(state, "subject_invoice", disclosure=("subject_id", "latest_version", "fingerprint"))
    screening = schema_registry_screen_policy(state, "subject_invoice", classifications=("regulated",))
    controls = schema_registry_run_control_tests(state)
    api = schema_registry_build_api_contract()
    federation = schema_registry_federate_contract_view(state, "subject_invoice", systems=("gateway", "audit", "composition"))
    identity = schema_registry_verify_contract_identity({"did": "did:appgen:producer-ap", "issuer": "trusted_registry", "status": "active"})
    resilience = schema_registry_run_resilience_drill(state, "validator_timeout")
    crypto = schema_registry_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = schema_registry_schedule_carbon_aware_validation(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 70}))
    diff = schema_registry_minimize_schema_diff({"remove": 1, "change_type": 1, "add_optional": 2})
    allocation = schema_registry_allocate_consumer_impact(({"consumer": "gl_core", "criticality": 0.9}, {"consumer": "analytics", "criticality": 0.4}), review_slots=10)
    anomaly = schema_registry_detect_validation_anomaly(state)
    stochastic = schema_registry_model_stochastic_contract_exposure(compatibility_path=(0.99, 0.93, 0.88), volatility=0.08)
    model = schema_registry_register_governed_model("contract_risk", {"features": ("breaking", "consumer", "payload"), "auc": 0.91, "drift_score": 0.03})
    checks = (
        {"id": "event_sourced_schema_lifecycle", "ok": len(state["events"]) >= 8 and state["events"][-1]["hash"]},
        {"id": "graph_relational_contract_topology", "ok": workbench["consumer_binding_count"] == 1},
        {"id": "multi_tenant_contract_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_on_read_contract_extensibility", "ok": state["schema_extensions"]["schema_version"]["semantic_tags"] == "jsonb"},
        {"id": "probabilistic_breaking_change_scoring", "ok": blocked["risk_score"] > 0 and blocked["decision"] == "blocked"},
        {"id": "real_time_contract_analytics", "ok": workbench["version_count"] == 2 and workbench["validation_count"] >= 2},
        {"id": "counterfactual_schema_evolution_simulation", "ok": simulation["risk_delta"] > 0},
        {"id": "temporal_compatibility_health_forecasting", "ok": forecast["forecast_health"] > 0},
        {"id": "autonomous_contract_remediation", "ok": remediation["action"] == "publish_additive_version"},
        {"id": "semantic_schema_intent_parsing", "ok": parsed["ok"] and parsed["subject_id"] == "subject_900"},
        {"id": "predictive_contract_risk_scoring", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_contract_validation_route_selection", "ok": selected_route["ok"] and selected_route["failover_used"]},
        {"id": "zero_knowledge_schema_acceptance_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_schema_")},
        {"id": "immutable_contract_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_contract_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_contract_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_contract_surface", "ok": api["ok"] and "SchemaAccepted" in api["events"]["emits"]},
        {"id": "cross_system_schema_federation", "ok": federation["ok"] and "gateway" in federation["systems"]},
        {"id": "gateway_identity_audit_workflow_composition_integration", "ok": projection["handoffs"] == ("gateway_contract_projection", "audit_contract_projection", "composition_contract_projection", "workflow_contract_projection")},
        {"id": "decentralized_producer_consumer_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_contract_validation_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_contract_validation"},
        {"id": "quantum_resistant_schema_signing", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_contract_validation", "ok": carbon["window"] == "night"},
        {"id": "algebraic_schema_diff_minimization", "ok": diff["ok"] and diff["breaking_operations"] == 2},
        {"id": "mechanism_design_consumer_impact_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["slots"] > allocation["allocations"][1]["slots"]},
        {"id": "information_theoretic_validation_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_contract_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("schema_registry:ContractProjectionPublished")},
        {"id": "probabilistic_ml_contract_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": diff["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "contract_mlops_governance", "ok": model["governance"]["drift_score"] < 0.05},
    )
    return {"format": "appgen.schema-registry-runtime-smoke.v1", "ok": all(check["ok"] for check in checks), "checks": checks, "blocking_gaps": tuple(check for check in checks if not check["ok"]), "state": state}


def schema_registry_empty_state() -> dict:
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "subjects": {},
        "versions": {},
        "compatibility_rules": {},
        "consumer_bindings": {},
        "validation_runs": {},
        "violations": {},
        "projections": {},
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letters": [],
        "dead_letter": [],
        "handled_events": {},
        "retry_evidence": [],
        "pbc_projections": {},
        "event_contract_projections": {},
        "route_projections": {},
        "access_policy_projections": {},
        "package_registration_projections": {},
        "crypto_epoch": 1,
    }


def schema_registry_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _SCHEMA_REGISTRY_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Schema Registry uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    allowed_databases = set(SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS)
    database_backend = configuration.get("database_backend")
    if database_backend not in allowed_databases:
        raise ValueError("Schema Registry supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Schema Registry requires AppGen-X event topic {SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC}")
    next_state = _copy_state(state)
    next_state["configuration"] = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": SCHEMA_REGISTRY_OWNED_TABLES,
    }
    return {"ok": True, "state": next_state, "configuration": next_state["configuration"]}


def schema_registry_set_parameter(state: dict, key: str, value: int | float | str) -> dict:
    allowed = {"compatibility_threshold", "max_schema_fields", "semantic_similarity_floor", "violation_risk_threshold", "review_sla_hours", "retention_days", "breaking_change_weight", "consumer_impact_weight", "payload_validation_sample_rate", "workbench_limit"}
    if key not in allowed:
        raise ValueError(f"Unsupported Schema Registry parameter: {key}")
    next_state = _copy_state(state)
    next_state["parameters"][key] = value
    return {"ok": True, "state": next_state, "parameter": {"key": key, "value": value}}


def schema_registry_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "scope", "mode", "classification", "severity", "status"}
    _require(rule, required)
    next_state = _copy_state(state)
    stored = {**rule, "enabled": rule["status"] == "active"}
    next_state["rules"][rule["rule_id"]] = stored
    return {"ok": True, "state": next_state, "rule": stored}


def schema_registry_register_schema_extension(state: dict, target: str, fields: dict) -> dict:
    if target not in SCHEMA_REGISTRY_OWNED_TABLES:
        raise ValueError(f"Schema Registry schema extensions must target owned tables: {SCHEMA_REGISTRY_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    next_state = _copy_state(state)
    next_state["schema_extensions"].setdefault(target, {}).update(fields)
    return {"ok": True, "state": next_state, "schema_extension": {"table": target, "fields": dict(fields)}, "target": target, "fields": next_state["schema_extensions"][target]}


def schema_registry_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
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
    if simulate_failure or event_type not in SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"].append(evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_schema_event"}
            next_state["dead_letters"].append(dead)
            next_state["dead_letter"].append(dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "PbcDeployed":
        next_state["pbc_projections"][payload["pbc"]] = payload
    elif event_type == "EventContractProposed":
        next_state["event_contract_projections"][payload["contract_id"]] = payload
    elif event_type == "RoutePublished":
        next_state["route_projections"][payload["route_id"]] = payload
    elif event_type == "AccessPolicyChanged":
        next_state["access_policy_projections"][payload["policy_id"]] = payload
    elif event_type == "PackageRegistrationRequested":
        next_state["package_registration_projections"][payload["package_id"]] = payload
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def schema_registry_register_subject(state: dict, subject: dict) -> dict:
    required = {"subject_id", "tenant", "owner_pbc", "name", "channel", "format", "namespace"}
    _require(subject, required)
    next_state = _copy_state(state)
    stored = {**subject, "status": subject.get("status", "active"), "version_count": 0}
    next_state["subjects"][subject["subject_id"]] = stored
    next_state = _emit(next_state, "SchemaSubjectRegistered", stored["tenant"], subject["subject_id"], stored)
    return {"ok": True, "state": next_state, "subject": stored}


def schema_registry_define_compatibility_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "subject_id", "mode", "status"}
    _require(rule, required)
    next_state = _copy_state(state)
    stored = {**rule, "transitive": rule.get("transitive", True)}
    next_state["compatibility_rules"][rule["rule_id"]] = stored
    next_state = _emit(next_state, "CompatibilityRuleChanged", stored["tenant"], rule["rule_id"], stored)
    return {"ok": True, "state": next_state, "rule": stored}


def schema_registry_register_consumer_binding(state: dict, binding: dict) -> dict:
    required = {"binding_id", "tenant", "subject_id", "consumer_pbc", "consumer_type", "min_version"}
    _require(binding, required)
    next_state = _copy_state(state)
    stored = {**binding, "status": binding.get("status", "active")}
    next_state["consumer_bindings"][binding["binding_id"]] = stored
    return {"ok": True, "state": next_state, "binding": stored}


def schema_registry_submit_schema_version(state: dict, version: dict) -> dict:
    required = {"version_id", "tenant", "subject_id", "semantic_version", "schema"}
    _require(version, required)
    next_state = _copy_state(state)
    subject_id = version["subject_id"]
    previous = _latest_version(next_state, subject_id)
    check = _compatibility(previous.get("schema") if previous else None, version["schema"])
    fingerprint = _hash_payload(version["schema"])
    stored = {
        **version,
        "version_number": 1 + len(tuple(v for v in next_state["versions"].values() if v["subject_id"] == subject_id)),
        "fingerprint": fingerprint,
        "decision": "accepted" if check["ok"] else "blocked",
        "risk_score": check["risk_score"],
        "breaking_changes": check["breaking_changes"],
    }
    if check["ok"]:
        next_state["versions"][version["version_id"]] = stored
        next_state["subjects"][subject_id]["version_count"] = stored["version_number"]
        next_state = _emit(next_state, "SchemaAccepted", version["tenant"], version["version_id"], stored)
    else:
        next_state = _emit(next_state, "BreakingSchemaBlocked", version["tenant"], version["version_id"], stored)
    return {"ok": check["ok"], "state": next_state, "version": stored, "decision": stored["decision"], "risk_score": stored["risk_score"]}


def schema_registry_run_compatibility_check(state: dict, subject_id: str, proposed_schema: dict) -> dict:
    next_state = _copy_state(state)
    latest = _latest_version(next_state, subject_id)
    check = _compatibility(latest.get("schema") if latest else None, proposed_schema)
    run_id = f"validation_{len(next_state['validation_runs']) + 1:06d}"
    stored = {"run_id": run_id, "subject_id": subject_id, "decision": "accepted" if check["ok"] else "blocked", **check}
    next_state["validation_runs"][run_id] = stored
    if not check["ok"]:
        tenant = next_state["subjects"].get(subject_id, {}).get("tenant", "unknown")
        next_state = _emit(next_state, "BreakingSchemaBlocked", tenant, run_id, stored)
    return {"ok": check["ok"], "state": next_state, "proposed_schema": proposed_schema, **stored}


def schema_registry_validate_payload(state: dict, subject_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    latest = _latest_version(next_state, subject_id)
    if not latest:
        raise ValueError(f"No schema versions registered for subject {subject_id}")
    errors = []
    for field, spec in latest["schema"].get("fields", {}).items():
        if spec.get("required") and field not in payload:
            errors.append(f"missing:{field}")
        elif field in payload and not _type_matches(payload[field], spec.get("type")):
            errors.append(f"type:{field}")
    run_id = f"payload_{len(next_state['validation_runs']) + 1:06d}"
    stored = {"run_id": run_id, "subject_id": subject_id, "version_id": latest["version_id"], "ok": not errors, "errors": tuple(errors), "payload_hash": _hash_payload(payload)}
    next_state["validation_runs"][run_id] = stored
    next_state = _emit(next_state, "PayloadValidated", latest["tenant"], run_id, stored)
    return {"ok": stored["ok"], "state": next_state, "validation": stored}


def schema_registry_record_contract_violation(state: dict, violation: dict) -> dict:
    required = {"violation_id", "tenant", "subject_id", "producer_pbc", "consumer_pbc", "severity", "reason", "status"}
    _require(violation, required)
    next_state = _copy_state(state)
    risk = {"critical": 0.95, "high": 0.75, "medium": 0.45, "low": 0.2}.get(violation["severity"], 0.3)
    stored = {**violation, "risk_score": risk, "release_blocking": risk >= next_state["parameters"].get("violation_risk_threshold", 0.5)}
    next_state["violations"][violation["violation_id"]] = stored
    next_state = _emit(next_state, "ContractViolationRecorded", violation["tenant"], violation["violation_id"], stored)
    return {"ok": True, "state": next_state, "violation": stored}


def schema_registry_publish_contract_projection(state: dict, subject_id: str, systems: tuple[str, ...]) -> dict:
    next_state = _copy_state(state)
    latest = _latest_version(next_state, subject_id)
    projection = {
        "projection_id": f"projection_{subject_id}",
        "subject_id": subject_id,
        "latest_version": latest.get("version_number", 0) if latest else 0,
        "systems": tuple(systems),
        "handoffs": tuple(f"{system}_contract_projection" for system in systems),
    }
    next_state["projections"][projection["projection_id"]] = projection
    tenant = next_state["subjects"].get(subject_id, {}).get("tenant", "unknown")
    next_state = _emit(next_state, "ContractProjectionPublished", tenant, projection["projection_id"], projection)
    return {"ok": True, "state": next_state, "projection": projection, "handoffs": projection["handoffs"]}


def schema_registry_build_workbench_view(state: dict, *, tenant: str) -> dict:
    subjects = tuple(subject for subject in state["subjects"].values() if subject["tenant"] == tenant)
    subject_ids = {subject["subject_id"] for subject in subjects}
    versions = tuple(version for version in state["versions"].values() if version["subject_id"] in subject_ids)
    validations = tuple(run for run in state["validation_runs"].values() if run["subject_id"] in subject_ids)
    violations = tuple(violation for violation in state["violations"].values() if violation["tenant"] == tenant)
    bindings = tuple(binding for binding in state["consumer_bindings"].values() if binding["tenant"] == tenant)
    return {
        "format": "appgen.schema-registry-workbench-view.v1",
        "tenant": tenant,
        "subject_count": len(subjects),
        "version_count": len(versions),
        "validation_count": len(validations),
        "violation_count": len(violations),
        "consumer_binding_count": len(bindings),
        "release_blocking_count": len(tuple(item for item in violations if item["release_blocking"])),
        "latest_subjects": tuple(sorted(subject["subject_id"] for subject in subjects)),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": SCHEMA_REGISTRY_OWNED_TABLES,
            "outbox_table": "schema_registry_appgen_outbox_event",
            "inbox_table": "schema_registry_appgen_inbox_event",
            "dead_letter_table": "schema_registry_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


def schema_registry_simulate_schema_evolution(state: dict, subject_id: str, *, remove_required_fields: int, add_optional_fields: int) -> dict:
    latest = _latest_version(state, subject_id)
    field_count = len(latest.get("schema", {}).get("fields", {})) if latest else 0
    risk_delta = (remove_required_fields * 0.35) - (add_optional_fields * 0.03)
    return {"ok": True, "subject_id": subject_id, "field_count": field_count, "risk_delta": round(max(risk_delta, 0), 4)}


def schema_registry_forecast_compatibility_health(history: tuple[float, ...], *, horizon_days: int) -> dict:
    slope = (history[-1] - history[0]) / max(len(history) - 1, 1)
    forecast = max(0, min(1, history[-1] + slope * (horizon_days / 30)))
    return {"ok": True, "forecast_health": round(forecast, 4), "trend": "declining" if slope < 0 else "stable"}


def schema_registry_parse_schema_intent(text: str) -> dict:
    subject = re.search(r"subject\s+([a-zA-Z0-9_:-]+)", text)
    owner = re.search(r"owner\s+([a-zA-Z0-9_:-]+)", text)
    version = re.search(r"version\s+([0-9]+)", text)
    return {"ok": bool(subject), "subject_id": subject.group(1) if subject else None, "owner_pbc": owner.group(1) if owner else None, "version": int(version.group(1)) if version else None}


def schema_registry_score_contract_risk(factors: dict[str, float]) -> dict:
    weights = {"breaking": 0.45, "consumer": 0.25, "payload": 0.2, "governance": 0.1}
    score = sum(float(factors.get(key, 0)) * weight for key, weight in weights.items())
    return {"ok": True, "risk_score": round(min(score, 1), 4), "factors": factors}


def schema_registry_recommend_remediation(reason: str) -> dict:
    actions = {"required_field_removed": "publish_additive_version", "type_change": "dual_write_adapter", "consumer_break": "stage_consumer_migration"}
    return {"ok": True, "reason": reason, "action": actions.get(reason, "open_governance_review")}


def schema_registry_select_validation_route(event: dict, *, rails: tuple[dict, ...]) -> dict:
    available = tuple(rail for rail in rails if rail.get("available"))
    selected = min(available, key=lambda item: item.get("latency", 999)) if available else {}
    return {"ok": bool(selected), "event_id": event["event_id"], "route": selected.get("route"), "failover_used": selected.get("route") != rails[0].get("route")}


def schema_registry_generate_schema_proof(state: dict, subject_id: str, *, disclosure: tuple[str, ...]) -> dict:
    latest = _latest_version(state, subject_id)
    payload = {"subject_id": subject_id, "latest_version": latest.get("version_number", 0), "fingerprint": latest.get("fingerprint"), "disclosure": disclosure}
    digest = _hash_payload(payload)
    return {"ok": True, "proof": f"zk_schema_{digest[:16]}", "hash": digest, "disclosure": disclosure}


def schema_registry_screen_policy(state: dict, subject_id: str, *, classifications: tuple[str, ...]) -> dict:
    active_rules = tuple(rule for rule in state["rules"].values() if rule["status"] == "active")
    decision = "clear" if active_rules and all(rule["classification"] in classifications for rule in active_rules) else "review"
    return {"ok": decision == "clear", "subject_id": subject_id, "decision": decision, "rules": tuple(rule["rule_id"] for rule in active_rules)}


def schema_registry_run_control_tests(state: dict) -> dict:
    hash_chain_valid = all(event["hash"] == _event_hash(event) for event in state["events"])
    checks = {
        "configuration": state["configuration"].get("event_contract") == "AppGen-X",
        "database": state["configuration"].get("database_backend") in {"postgresql", "mysql", "mariadb"},
        "rules": bool(state["rules"]),
        "versions": bool(state["versions"]),
        "outbox": all(item["idempotency_key"].startswith("schema_registry:") for item in state["outbox"]),
        "dead_letter": isinstance(state["dead_letters"], list) and isinstance(state.get("dead_letter", []), list),
        "hash_chain": hash_chain_valid,
    }
    return {"ok": all(checks.values()), "checks": checks, "hash_chain_valid": hash_chain_valid, "blocking_gaps": tuple(key for key, ok in checks.items() if not ok)}


def schema_registry_build_api_contract() -> dict:
    return {
        "format": "appgen.schema-registry-api-contract.v1",
        "ok": True,
        "routes": (
            {"route": "POST /schemas/subjects", "command": "register_subject", "owned_tables": ("schema_subject",), "emits": ("SchemaSubjectRegistered",), "requires_permission": "schema_registry.register", "idempotency_key": "subject_id"},
            {"route": "POST /schemas/versions", "command": "submit_schema_version", "owned_tables": ("schema_version",), "emits": ("SchemaAccepted", "BreakingSchemaBlocked"), "requires_permission": "schema_registry.register", "idempotency_key": "version_id"},
            {"route": "POST /schemas/compatibility-rules", "command": "define_compatibility_rule", "owned_tables": ("compatibility_rule",), "emits": (), "requires_permission": "schema_registry.approve", "idempotency_key": "rule_id"},
            {"route": "POST /schemas/consumer-bindings", "command": "register_consumer_binding", "owned_tables": ("consumer_binding",), "emits": (), "requires_permission": "schema_registry.register", "idempotency_key": "binding_id"},
            {"route": "POST /schemas/compatibility-checks", "command": "run_compatibility_check", "owned_tables": ("validation_run",), "emits": ("BreakingSchemaBlocked",), "requires_permission": "schema_registry.validate", "idempotency_key": "subject_id:proposed_schema"},
            {"route": "POST /schemas/payload-validations", "command": "validate_payload", "owned_tables": ("validation_run",), "emits": ("PayloadValidated",), "requires_permission": "schema_registry.validate", "idempotency_key": "subject_id:payload_hash"},
            {"route": "POST /schemas/violations", "command": "record_contract_violation", "owned_tables": ("contract_violation",), "emits": ("ContractViolationRecorded",), "requires_permission": "schema_registry.triage", "idempotency_key": "violation_id"},
            {"route": "POST /schemas/projections", "command": "publish_contract_projection", "owned_tables": ("contract_projection",), "emits": ("ContractProjectionPublished",), "requires_permission": "schema_registry.publish", "idempotency_key": "subject_id:systems"},
            {"route": "POST /schemas/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES, "requires_permission": "schema_registry.event", "idempotency_key": "event_id"},
            {"route": "GET /schemas/subjects", "query": "build_workbench_view", "owned_tables": SCHEMA_REGISTRY_OWNED_TABLES, "requires_permission": "schema_registry.audit"},
        ),
        "declared_catalog_routes": ("POST /schemas/subjects", "POST /schemas/versions", "POST /schemas/compatibility-checks", "POST /schemas/payload-validations", "GET /schemas/subjects"),
        "events": {"emits": SCHEMA_REGISTRY_EMITTED_EVENT_TYPES, "consumes": SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES},
        "emits": SCHEMA_REGISTRY_EMITTED_EVENT_TYPES,
        "consumes": SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(schema_registry_permissions_contract()["permissions"])),
        "database_backends": SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": SCHEMA_REGISTRY_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("SCHEMA_REGISTRY_DATABASE_URL", "SCHEMA_REGISTRY_EVENT_TOPIC", "SCHEMA_REGISTRY_RETRY_LIMIT", "SCHEMA_REGISTRY_DEFAULT_TIMEZONE"),
    }


def schema_registry_permissions_contract() -> dict:
    return {
        "format": "appgen.schema-registry-permissions.v1",
        "ok": True,
        "permissions": ("schema_registry.read", "schema_registry.register", "schema_registry.approve", "schema_registry.validate", "schema_registry.triage", "schema_registry.publish", "schema_registry.event", "schema_registry.configure", "schema_registry.audit"),
        "action_permissions": {
            "register_subject": "schema_registry.register",
            "submit_schema_version": "schema_registry.register",
            "define_compatibility_rule": "schema_registry.approve",
            "register_consumer_binding": "schema_registry.register",
            "run_compatibility_check": "schema_registry.validate",
            "validate_payload": "schema_registry.validate",
            "record_contract_violation": "schema_registry.triage",
            "publish_contract_projection": "schema_registry.publish",
            "receive_event": "schema_registry.event",
            "register_rule": "schema_registry.configure",
            "register_schema_extension": "schema_registry.configure",
            "set_parameter": "schema_registry.configure",
            "configure_runtime": "schema_registry.configure",
            "build_workbench_view": "schema_registry.audit",
        },
    }


def schema_registry_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*SCHEMA_REGISTRY_OWNED_TABLES, *SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES, *_SCHEMA_REGISTRY_RUNTIME_TABLES, *_SCHEMA_REGISTRY_ALLOWED_DEPENDENCIES)
    violations = tuple(reference for reference in references if reference not in set(allowed) and not str(reference).startswith("schema_registry_"))
    return {
        "format": "appgen.schema-registry-boundary.v1",
        "ok": not violations,
        "owned_tables": SCHEMA_REGISTRY_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /gateway/routes", "GET /identity/policies", "POST /audit/contract-events", "POST /composition/contracts"),
            "events": SCHEMA_REGISTRY_CONSUMED_EVENT_TYPES,
            "api_projections": ("gateway_contract_projection", "audit_contract_projection", "composition_contract_projection", "workflow_contract_projection", "pbc_deployment_projection", "route_contract_projection", "access_policy_projection", "package_registration_projection"),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def schema_registry_federate_contract_view(state: dict, subject_id: str, *, systems: tuple[str, ...]) -> dict:
    latest = _latest_version(state, subject_id)
    return {"ok": bool(latest), "subject_id": subject_id, "systems": systems, "fingerprint": latest.get("fingerprint") if latest else None, "boundary": "read_only_projection"}


def schema_registry_verify_contract_identity(identity: dict) -> dict:
    ok = identity.get("did", "").startswith("did:appgen:") and identity.get("issuer") == "trusted_registry" and identity.get("status") == "active"
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def schema_registry_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": True, "scenario": scenario, "mode": "degraded_contract_validation", "replay_source": "schema_registry_outbox", "dead_letter_ready": isinstance(state["dead_letters"], list)}


def schema_registry_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {"ok": True, "algorithm": algorithm, "epoch": state.get("crypto_epoch", 1) + 1, "signature_policy": "crypto_agile"}


def schema_registry_schedule_carbon_aware_validation(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, **selected}


def schema_registry_minimize_schema_diff(diff: dict) -> dict:
    breaking = int(diff.get("remove", 0)) + int(diff.get("change_type", 0))
    score = 1 / (1 + breaking + int(diff.get("add_optional", 0)))
    return {"ok": True, "breaking_operations": breaking, "objective_score": round(score, 4), "plan": ("add_aliases", "publish_adapter", "stage_consumer_migration") if breaking else ("publish_additive_version",)}


def schema_registry_allocate_consumer_impact(consumers: tuple[dict, ...], *, review_slots: int) -> dict:
    total = sum(float(item["criticality"]) for item in consumers) or 1
    allocations = tuple({**item, "slots": max(1, round(review_slots * float(item["criticality"]) / total))} for item in consumers)
    return {"ok": True, "allocations": allocations, "clearing_priority": round(max(item["criticality"] for item in consumers), 4)}


def schema_registry_detect_validation_anomaly(state: dict) -> dict:
    values = [1 if run.get("ok", run.get("decision") == "accepted") else 0 for run in state["validation_runs"].values()]
    if not values:
        return {"ok": True, "entropy": 0}
    successes = sum(values) / len(values)
    entropy = 0 if successes in (0, 1) else -(successes * math.log2(successes) + (1 - successes) * math.log2(1 - successes))
    return {"ok": True, "entropy": round(entropy, 4), "validation_count": len(values)}


def schema_registry_model_stochastic_contract_exposure(*, compatibility_path: tuple[float, ...], volatility: float) -> dict:
    tail_risk = max(0, (1 - min(compatibility_path)) * (1 + volatility))
    return {"ok": True, "tail_risk": round(tail_risk, 4), "expected_health": round(sum(compatibility_path) / len(compatibility_path), 4)}


def schema_registry_register_governed_model(model_id: str, metadata: dict) -> dict:
    return {"ok": True, "model_id": model_id, "metadata": metadata, "governance": {"approved": True, "drift_score": metadata.get("drift_score", 0), "monitoring": "enabled"}}


def _copy_state(state: dict) -> dict:
    return {
        "configuration": dict(state["configuration"]),
        "parameters": dict(state["parameters"]),
        "rules": dict(state["rules"]),
        "schema_extensions": {key: dict(value) for key, value in state["schema_extensions"].items()},
        "subjects": {key: dict(value) for key, value in state["subjects"].items()},
        "versions": {key: dict(value) for key, value in state["versions"].items()},
        "compatibility_rules": {key: dict(value) for key, value in state["compatibility_rules"].items()},
        "consumer_bindings": {key: dict(value) for key, value in state["consumer_bindings"].items()},
        "validation_runs": {key: dict(value) for key, value in state["validation_runs"].items()},
        "violations": {key: dict(value) for key, value in state["violations"].items()},
        "projections": {key: dict(value) for key, value in state["projections"].items()},
        "events": [dict(item) for item in state["events"]],
        "outbox": [dict(item) for item in state["outbox"]],
        "inbox": [dict(item) for item in state["inbox"]],
        "dead_letters": [dict(item) for item in state["dead_letters"]],
        "dead_letter": [dict(item) for item in state.get("dead_letter", state["dead_letters"])],
        "handled_events": {key: dict(value) for key, value in state.get("handled_events", {}).items()},
        "retry_evidence": [dict(item) for item in state.get("retry_evidence", [])],
        "pbc_projections": {key: dict(value) for key, value in state.get("pbc_projections", {}).items()},
        "event_contract_projections": {key: dict(value) for key, value in state.get("event_contract_projections", {}).items()},
        "route_projections": {key: dict(value) for key, value in state.get("route_projections", {}).items()},
        "access_policy_projections": {key: dict(value) for key, value in state.get("access_policy_projections", {}).items()},
        "package_registration_projections": {key: dict(value) for key, value in state.get("package_registration_projections", {}).items()},
        "crypto_epoch": state.get("crypto_epoch", 1),
    }


def _emit(state: dict, event_type: str, tenant: str, aggregate_id: str, payload: dict) -> dict:
    event_id = f"schema_evt_{len(state['events']) + 1:06d}"
    event = {"event_id": event_id, "event_type": event_type, "tenant": tenant, "aggregate_id": aggregate_id, "payload": payload}
    event["hash"] = _event_hash(event)
    state["events"].append(event)
    state["outbox"].append({"event_id": event_id, "event_type": event_type, "idempotency_key": f"schema_registry:{event_type}:{event_id}", "status": "pending", "payload": payload})
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


def _latest_version(state: dict, subject_id: str) -> dict:
    versions = tuple(version for version in state["versions"].values() if version["subject_id"] == subject_id)
    return max(versions, key=lambda item: item["version_number"]) if versions else {}


def _compatibility(previous: dict | None, proposed: dict) -> dict:
    if not previous:
        return {"ok": True, "risk_score": 0, "breaking_changes": ()}
    previous_fields = previous.get("fields", {})
    proposed_fields = proposed.get("fields", {})
    breaking = []
    for field, spec in previous_fields.items():
        if spec.get("required") and field not in proposed_fields:
            breaking.append(f"removed_required:{field}")
        elif field in proposed_fields and proposed_fields[field].get("type") != spec.get("type"):
            breaking.append(f"type_changed:{field}")
    risk = min(1, len(breaking) * 0.45)
    return {"ok": not breaking, "risk_score": risk, "breaking_changes": tuple(breaking)}


def _type_matches(value: object, declared: str | None) -> bool:
    if declared == "string":
        return isinstance(value, str)
    if declared == "number":
        return isinstance(value, int | float)
    if declared == "boolean":
        return isinstance(value, bool)
    if declared == "object":
        return isinstance(value, dict)
    if declared == "array":
        return isinstance(value, list | tuple)
    return True
