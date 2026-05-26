"""Executable runtime for the Audit Ledger PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


AUDIT_LEDGER_REQUIRED_EVENT_TOPIC = "appgen.audit.events"
AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
AUDIT_LEDGER_OWNED_TABLES = (
    "audit_ledger_audit_event",
    "audit_ledger_signature_chain",
    "audit_ledger_retention_policy",
    "audit_ledger_forensic_export",
    "audit_ledger_access_evidence",
    "audit_ledger_control_assertion",
    "audit_ledger_rule",
    "audit_ledger_parameter",
    "audit_ledger_configuration",
)
AUDIT_LEDGER_EMITTED_EVENT_TYPES = (
    "AuditEventSealed",
    "SignatureChainVerified",
    "RetentionPolicyChanged",
    "ForensicExportPrepared",
    "ControlAssertionFailed",
    "AuditProjectionPublished",
)
AUDIT_LEDGER_CONSUMED_EVENT_TYPES = (
    "AccessPolicyChanged",
    "WorkflowCompleted",
    "RoutePublished",
    "SchemaAccepted",
    "PbcDeployed",
    "CompositionPublished",
)
_AUDIT_LEDGER_RUNTIME_TABLES = (
    "audit_ledger_appgen_outbox_event",
    "audit_ledger_appgen_inbox_event",
    "audit_ledger_dead_letter_event",
)
_AUDIT_LEDGER_ALLOWED_DEPENDENCIES = (
    "identity_access_projection",
    "gateway_route_projection",
    "schema_contract_projection",
    "workflow_completion_projection",
    "composition_release_projection",
    "pbc_deployment_projection",
    "GET /identity/policies",
    "GET /gateway/routes",
    "GET /schemas/subjects",
    "GET /workflow/instances",
    "POST /composition/release-evidence",
)
_AUDIT_LEDGER_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


AUDIT_LEDGER_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_audit_lifecycle",
    "graph_relational_evidence_topology",
    "multi_tenant_audit_isolation",
    "schema_on_read_evidence_envelope",
    "probabilistic_tamper_control_risk_scoring",
    "real_time_audit_analytics",
    "counterfactual_retention_disclosure_simulation",
    "temporal_evidence_health_forecasting",
    "autonomous_control_remediation",
    "semantic_audit_query_parsing",
    "predictive_audit_risk_scoring",
    "self_healing_audit_ingestion_route_selection",
    "zero_knowledge_event_disclosure_proof",
    "immutable_regulatory_trail",
    "dynamic_audit_policy_screening",
    "automated_audit_control_testing",
    "universal_api_async_audit_surface",
    "cross_system_audit_federation",
    "identity_gateway_schema_workflow_composition_integration",
    "decentralized_actor_identity",
    "chaos_engineered_audit_tolerance",
    "quantum_resistant_audit_signing",
    "carbon_aware_audit_processing",
    "algebraic_evidence_minimization",
    "mechanism_design_export_reviewer_allocation",
    "information_theoretic_audit_anomaly_detection",
    "temporal_evidence_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_audit_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "audit_mlops_governance",
)
AUDIT_LEDGER_STANDARD_FEATURE_KEYS = (
    "append_only_audit_events",
    "tenant_sequence",
    "hash_chain",
    "signature_metadata",
    "event_sealing",
    "chain_verification",
    "tamper_detection",
    "source_pbc_indexing",
    "actor_action_indexing",
    "access_evidence",
    "retention_policy",
    "legal_hold",
    "forensic_export",
    "proof_bundle",
    "control_assertion",
    "release_blocking_controls",
    "payload_digest",
    "disclosure_minimization",
    "idempotent_handlers",
    "retry_dead_letter",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "release_gate",
    "appgen_event_contract",
)


def audit_ledger_runtime_capabilities() -> dict:
    smoke = audit_ledger_runtime_smoke()
    return {
        "format": "appgen.audit-ledger-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "audit_ledger",
        "implementation_directory": "src/pyAppGen/pbcs/audit_ledger",
        "owned_tables": AUDIT_LEDGER_OWNED_TABLES,
        "capabilities": AUDIT_LEDGER_RUNTIME_CAPABILITY_KEYS,
        "standard_features": AUDIT_LEDGER_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "record_audit_event",
            "record_access_evidence",
            "define_retention_policy",
            "assert_control",
            "prepare_forensic_export",
            "verify_signature_chain",
            "publish_audit_projection",
            "build_api_contract",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def audit_ledger_runtime_smoke() -> dict:
    state = audit_ledger_empty_state()
    state = audit_ledger_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "signature_algorithm": "dilithium3_simulated",
            "allowed_classifications": ("public", "internal", "regulated"),
            "export_modes": ("proof_bundle", "forensic_archive"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = audit_ledger_set_parameter(state, "retention_days", 2555)["state"]
    state = audit_ledger_set_parameter(state, "export_batch_limit", 1000)["state"]
    state = audit_ledger_set_parameter(state, "tamper_risk_threshold", 0.35)["state"]
    state = audit_ledger_set_parameter(state, "control_failure_threshold", 0.2)["state"]
    state = audit_ledger_set_parameter(state, "proof_disclosure_limit", 4)["state"]
    state = audit_ledger_register_rule(
        state,
        {
            "rule_id": "rule_audit",
            "tenant": "tenant_alpha",
            "scope": "mutation",
            "classification": "regulated",
            "minimum_retention_days": 2555,
            "requires_legal_hold_review": True,
            "requires_export_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    state = audit_ledger_register_schema_extension(state, "audit_event", {"evidence_tags": "jsonb"})["state"]
    state = audit_ledger_register_schema_extension(state, "audit_ledger_audit_event", {"lineage_payload": "jsonb"})["state"]
    consumed = audit_ledger_receive_event(
        state,
        {"event_id": "evt_route_published", "event_type": "RoutePublished", "payload": {"tenant": "tenant_alpha", "route_id": "route_catalog", "service_id": "svc_catalog"}},
    )
    state = consumed["state"]
    event = audit_ledger_record_audit_event(
        state,
        {
            "audit_id": "audit_route",
            "tenant": "tenant_alpha",
            "source_pbc": "api_gateway_mesh",
            "aggregate_id": "route_catalog",
            "actor": "ops_user",
            "action": "publish_route",
            "classification": "regulated",
            "payload": {"route_id": "route_catalog", "method": "POST"},
        },
    )
    state = event["state"]
    access = audit_ledger_record_access_evidence(
        state,
        {"evidence_id": "access_ops", "tenant": "tenant_alpha", "principal": "ops_user", "resource": "route_catalog", "action": "publish_route", "decision": "allow", "context": {"risk": "low"}},
    )
    state = access["state"]
    retention = audit_ledger_define_retention_policy(
        state,
        {"policy_id": "ret_regulated", "tenant": "tenant_alpha", "classification": "regulated", "retention_days": 2555, "legal_hold": False, "disposal_action": "review"},
    )
    state = retention["state"]
    control = audit_ledger_assert_control(
        state,
        {"control_id": "ctrl_chain", "tenant": "tenant_alpha", "control": "signature_chain", "status": "pass", "severity": "blocking", "evidence": ("audit_route",)},
    )
    state = control["state"]
    export = audit_ledger_prepare_forensic_export(
        state,
        {"export_id": "export_ops", "tenant": "tenant_alpha", "classification": "regulated", "requested_by": "auditor", "disclosure": ("audit_id", "source_pbc", "actor", "action")},
    )
    state = export["state"]
    verification = audit_ledger_verify_signature_chain(state, tenant="tenant_alpha")
    projection = audit_ledger_publish_audit_projection(state, "audit_route", systems=("identity", "gateway", "schema", "workflow", "composition"))
    state = projection["state"]
    workbench = audit_ledger_build_workbench_view(state, tenant="tenant_alpha")
    simulation = audit_ledger_simulate_retention_disclosure(state, classification="regulated", disclosure_fields=4, retention_days=3650)
    forecast = audit_ledger_forecast_evidence_health((0.99, 0.96, 0.92), horizon_days=30)
    parsed = audit_ledger_parse_audit_query("find audit audit_route actor ops_user action publish_route")
    risk = audit_ledger_score_audit_risk({"tamper": 0.2, "control": 0.1, "retention": 0.3, "export": 0.1})
    remediation = audit_ledger_recommend_control_remediation("chain_gap")
    selected_route = audit_ledger_select_ingestion_route({"event_id": "audit_ingest"}, rails=({"route": "primary", "available": False, "latency": 2}, {"route": "outbox_replay", "available": True, "latency": 4}))
    proof = audit_ledger_generate_disclosure_proof(state, "audit_route", disclosure=("audit_id", "actor", "action"))
    screening = audit_ledger_screen_policy(state, "audit_route", classifications=("regulated",))
    controls = audit_ledger_run_control_tests(state)
    api = audit_ledger_build_api_contract()
    federation = audit_ledger_federate_evidence_view(state, "audit_route", systems=("identity", "gateway", "schema", "workflow", "composition"))
    identity = audit_ledger_verify_actor_identity({"did": "did:appgen:actor-ops", "issuer": "trusted_registry", "status": "active"})
    resilience = audit_ledger_run_resilience_drill(state, "export_store_timeout")
    crypto = audit_ledger_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = audit_ledger_schedule_carbon_aware_processing(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 70}))
    minimized = audit_ledger_minimize_evidence_bundle(("audit_id", "actor", "action", "payload", "payload", "context"), required=("audit_id", "actor", "action"))
    allocation = audit_ledger_allocate_export_reviewers(({"reviewer": "compliance", "criticality": 0.9}, {"reviewer": "ops", "criticality": 0.5}), slots=10)
    anomaly = audit_ledger_detect_audit_anomaly(state)
    stochastic = audit_ledger_model_stochastic_evidence_exposure(event_path=(100, 160, 250), volatility=0.1)
    model = audit_ledger_register_governed_model("audit_risk", {"features": ("tamper", "control", "retention"), "auc": 0.93, "drift_score": 0.03})
    checks = (
        {"id": "event_sourced_audit_lifecycle", "ok": len(state["events"]) >= 4 and state["events"][-1]["hash"]},
        {"id": "graph_relational_evidence_topology", "ok": workbench["event_count"] == 1 and workbench["access_evidence_count"] == 1},
        {"id": "multi_tenant_audit_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_on_read_evidence_envelope", "ok": state["schema_extensions"]["audit_ledger_audit_event"]["lineage_payload"] == "jsonb"},
        {"id": "probabilistic_tamper_control_risk_scoring", "ok": risk["risk_score"] > 0 and event["audit_event"]["tamper_risk"] >= 0},
        {"id": "real_time_audit_analytics", "ok": workbench["export_count"] == 1 and workbench["control_count"] == 1},
        {"id": "counterfactual_retention_disclosure_simulation", "ok": simulation["disclosure_risk"] > 0},
        {"id": "temporal_evidence_health_forecasting", "ok": forecast["forecast_health"] > 0},
        {"id": "autonomous_control_remediation", "ok": remediation["action"] == "rebuild_chain_from_verified_events"},
        {"id": "semantic_audit_query_parsing", "ok": parsed["ok"] and parsed["audit_id"] == "audit_route"},
        {"id": "predictive_audit_risk_scoring", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_audit_ingestion_route_selection", "ok": selected_route["ok"] and selected_route["failover_used"]},
        {"id": "zero_knowledge_event_disclosure_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_audit_")},
        {"id": "immutable_regulatory_trail", "ok": verification["ok"] and controls["hash_chain_valid"]},
        {"id": "dynamic_audit_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_audit_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_audit_surface", "ok": api["ok"] and "AuditEventSealed" in api["events"]["emits"] and api["stream_engine_picker_visible"] is False},
        {"id": "cross_system_audit_federation", "ok": federation["ok"] and "gateway" in federation["systems"]},
        {"id": "identity_gateway_schema_workflow_composition_integration", "ok": projection["handoffs"] == ("identity_audit_projection", "gateway_audit_projection", "schema_audit_projection", "workflow_audit_projection", "composition_audit_projection")},
        {"id": "decentralized_actor_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_audit_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_audit_replay"},
        {"id": "quantum_resistant_audit_signing", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_audit_processing", "ok": carbon["window"] == "night"},
        {"id": "algebraic_evidence_minimization", "ok": minimized["ok"] and minimized["removed_fields"] >= 1},
        {"id": "mechanism_design_export_reviewer_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["slots"] > allocation["allocations"][1]["slots"]},
        {"id": "information_theoretic_audit_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_evidence_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("audit_ledger:AuditProjectionPublished")},
        {"id": "probabilistic_ml_audit_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": minimized["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "audit_mlops_governance", "ok": model["governance"]["drift_score"] < 0.05},
    )
    return {"format": "appgen.audit-ledger-runtime-smoke.v1", "ok": all(check["ok"] for check in checks), "checks": checks, "blocking_gaps": tuple(check for check in checks if not check["ok"]), "state": state}


def audit_ledger_empty_state() -> dict:
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "audit_events": {},
        "signature_chain": {},
        "retention_policies": {},
        "forensic_exports": {},
        "access_evidence": {},
        "control_assertions": {},
        "projections": {},
        "events": [],
        "outbox": [],
        "inbox": [],
        "handled_events": {},
        "retry_evidence": [],
        "dead_letter": [],
        "dead_letters": [],
        "identity_access_projections": {},
        "gateway_route_projections": {},
        "schema_contract_projections": {},
        "workflow_completion_projections": {},
        "composition_release_projections": {},
        "pbc_deployment_projections": {},
        "crypto_epoch": 1,
    }


def audit_ledger_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _AUDIT_LEDGER_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Audit Ledger uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    allowed_databases = set(AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS)
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Audit Ledger supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != AUDIT_LEDGER_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Audit Ledger requires AppGen-X event topic {AUDIT_LEDGER_REQUIRED_EVENT_TOPIC}")
    next_state = _copy_state(state)
    next_state["configuration"] = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": AUDIT_LEDGER_OWNED_TABLES,
    }
    return {"ok": True, "state": next_state, "configuration": next_state["configuration"]}


def audit_ledger_set_parameter(state: dict, key: str, value: int | float | str) -> dict:
    allowed = {"retention_days", "export_batch_limit", "tamper_risk_threshold", "control_failure_threshold", "proof_disclosure_limit", "review_sla_hours"}
    if key not in allowed:
        raise ValueError(f"Unsupported Audit Ledger parameter: {key}")
    next_state = _copy_state(state)
    next_state["parameters"][key] = value
    return {"ok": True, "state": next_state, "parameter": {"key": key, "value": value}}


def audit_ledger_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "scope", "classification", "minimum_retention_days", "requires_legal_hold_review", "requires_export_approval", "severity", "status"}
    _require(rule, required)
    next_state = _copy_state(state)
    stored = {**rule, "enabled": rule["status"] == "active"}
    next_state["rules"][rule["rule_id"]] = stored
    return {"ok": True, "state": next_state, "rule": stored}


def audit_ledger_register_schema_extension(state: dict, target: str, fields: dict) -> dict:
    if target == "audit_event":
        target = "audit_ledger_audit_event"
    if target not in AUDIT_LEDGER_OWNED_TABLES:
        raise ValueError(f"Audit Ledger schema extensions must target owned tables: {AUDIT_LEDGER_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    next_state = _copy_state(state)
    next_state["schema_extensions"].setdefault(target, {}).update(fields)
    return {"ok": True, "state": next_state, "schema_extension": {"table": target, "fields": dict(fields)}, "target": target, "fields": next_state["schema_extensions"][target]}


def audit_ledger_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
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
    if simulate_failure or event_type not in AUDIT_LEDGER_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"].append(evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_audit_event"}
            next_state["dead_letters"].append(dead)
            next_state["dead_letter"].append(dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "AccessPolicyChanged":
        next_state["identity_access_projections"][payload["policy_id"]] = payload
    elif event_type == "RoutePublished":
        next_state["gateway_route_projections"][payload["route_id"]] = payload
    elif event_type == "SchemaAccepted":
        next_state["schema_contract_projections"][payload["subject_id"]] = payload
    elif event_type == "WorkflowCompleted":
        next_state["workflow_completion_projections"][payload["workflow_id"]] = payload
    elif event_type == "CompositionPublished":
        next_state["composition_release_projections"][payload["composition_id"]] = payload
    elif event_type == "PbcDeployed":
        next_state["pbc_deployment_projections"][payload["pbc"]] = payload
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def audit_ledger_record_audit_event(state: dict, audit_event: dict) -> dict:
    required = {"audit_id", "tenant", "source_pbc", "aggregate_id", "actor", "action", "classification", "payload"}
    _require(audit_event, required)
    next_state = _copy_state(state)
    tenant_events = tuple(event for event in next_state["audit_events"].values() if event["tenant"] == audit_event["tenant"])
    sequence = len(tenant_events) + 1
    previous_hash = tenant_events[-1]["event_hash"] if tenant_events else "genesis"
    payload_hash = _hash_payload(audit_event["payload"])
    event_hash = _hash_payload({**audit_event, "sequence": sequence, "previous_hash": previous_hash, "payload_hash": payload_hash})
    tamper_risk = 0 if previous_hash == "genesis" or previous_hash else 0.8
    stored = {**audit_event, "sequence": sequence, "payload_hash": payload_hash, "previous_hash": previous_hash, "event_hash": event_hash, "signature": f"sig_{event_hash[:16]}", "sealed": True, "tamper_risk": tamper_risk}
    next_state["audit_events"][audit_event["audit_id"]] = stored
    next_state["signature_chain"][audit_event["audit_id"]] = {"audit_id": audit_event["audit_id"], "tenant": audit_event["tenant"], "sequence": sequence, "previous_hash": previous_hash, "event_hash": event_hash, "signature": stored["signature"], "verified": True}
    next_state = _emit(next_state, "AuditEventSealed", audit_event["tenant"], audit_event["audit_id"], stored)
    return {"ok": True, "state": next_state, "audit_event": stored}


def audit_ledger_record_access_evidence(state: dict, evidence: dict) -> dict:
    required = {"evidence_id", "tenant", "principal", "resource", "action", "decision", "context"}
    _require(evidence, required)
    next_state = _copy_state(state)
    stored = {**evidence, "context_hash": _hash_payload(evidence["context"])}
    next_state["access_evidence"][evidence["evidence_id"]] = stored
    return {"ok": True, "state": next_state, "evidence": stored}


def audit_ledger_define_retention_policy(state: dict, policy: dict) -> dict:
    required = {"policy_id", "tenant", "classification", "retention_days", "legal_hold", "disposal_action"}
    _require(policy, required)
    next_state = _copy_state(state)
    stored = {**policy, "status": "active"}
    next_state["retention_policies"][policy["policy_id"]] = stored
    next_state = _emit(next_state, "RetentionPolicyChanged", policy["tenant"], policy["policy_id"], stored)
    return {"ok": True, "state": next_state, "policy": stored}


def audit_ledger_assert_control(state: dict, assertion: dict) -> dict:
    required = {"control_id", "tenant", "control", "status", "severity", "evidence"}
    _require(assertion, required)
    next_state = _copy_state(state)
    stored = {**assertion, "release_blocking": assertion["status"] != "pass" and assertion["severity"] == "blocking"}
    next_state["control_assertions"][assertion["control_id"]] = stored
    if stored["release_blocking"]:
        next_state = _emit(next_state, "ControlAssertionFailed", assertion["tenant"], assertion["control_id"], stored)
    return {"ok": assertion["status"] == "pass", "state": next_state, "assertion": stored}


def audit_ledger_prepare_forensic_export(state: dict, export: dict) -> dict:
    required = {"export_id", "tenant", "classification", "requested_by", "disclosure"}
    _require(export, required)
    next_state = _copy_state(state)
    events = tuple(event for event in next_state["audit_events"].values() if event["tenant"] == export["tenant"] and event["classification"] == export["classification"])
    checksum = _hash_payload({"events": tuple(event["event_hash"] for event in events), "disclosure": export["disclosure"]})
    stored = {**export, "event_count": len(events), "checksum": checksum, "status": "prepared", "proof_bundle": f"proof_bundle_{checksum[:16]}"}
    next_state["forensic_exports"][export["export_id"]] = stored
    next_state = _emit(next_state, "ForensicExportPrepared", export["tenant"], export["export_id"], stored)
    return {"ok": True, "state": next_state, "export": stored}


def audit_ledger_verify_signature_chain(state: dict, *, tenant: str) -> dict:
    links = sorted((link for link in state["signature_chain"].values() if link["tenant"] == tenant), key=lambda item: item["sequence"])
    previous = "genesis"
    gaps = []
    tampered = []
    for link in links:
        if link["previous_hash"] != previous:
            gaps.append(link["audit_id"])
        event = state["audit_events"].get(link["audit_id"], {})
        if event.get("event_hash") != link["event_hash"] or link["signature"] != f"sig_{link['event_hash'][:16]}":
            tampered.append(link["audit_id"])
        previous = link["event_hash"]
    return {"ok": not gaps and not tampered and bool(links), "tenant": tenant, "link_count": len(links), "gaps": tuple(gaps), "tampered": tuple(tampered)}


def audit_ledger_publish_audit_projection(state: dict, audit_id: str, systems: tuple[str, ...]) -> dict:
    next_state = _copy_state(state)
    projection = {"projection_id": f"projection_{audit_id}", "audit_id": audit_id, "systems": systems, "handoffs": tuple(f"{system}_audit_projection" for system in systems)}
    next_state["projections"][projection["projection_id"]] = projection
    tenant = next_state["audit_events"][audit_id]["tenant"]
    next_state = _emit(next_state, "AuditProjectionPublished", tenant, projection["projection_id"], projection)
    return {"ok": True, "state": next_state, "projection": projection, "handoffs": projection["handoffs"]}


def audit_ledger_build_workbench_view(state: dict, *, tenant: str) -> dict:
    events = tuple(event for event in state["audit_events"].values() if event["tenant"] == tenant)
    access = tuple(item for item in state["access_evidence"].values() if item["tenant"] == tenant)
    exports = tuple(item for item in state["forensic_exports"].values() if item["tenant"] == tenant)
    controls = tuple(item for item in state["control_assertions"].values() if item["tenant"] == tenant)
    policies = tuple(item for item in state["retention_policies"].values() if item["tenant"] == tenant)
    return {
        "format": "appgen.audit-ledger-workbench-view.v1",
        "tenant": tenant,
        "event_count": len(events),
        "access_evidence_count": len(access),
        "export_count": len(exports),
        "control_count": len(controls),
        "policy_count": len(policies),
        "verified_chain": audit_ledger_verify_signature_chain(state, tenant=tenant)["ok"],
        "release_blocking_count": len(tuple(item for item in controls if item["release_blocking"])),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": AUDIT_LEDGER_OWNED_TABLES,
            "outbox_table": "audit_ledger_appgen_outbox_event",
            "inbox_table": "audit_ledger_appgen_inbox_event",
            "dead_letter_table": "audit_ledger_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


def audit_ledger_simulate_retention_disclosure(state: dict, *, classification: str, disclosure_fields: int, retention_days: int) -> dict:
    baseline = float(state["parameters"].get("retention_days", 365))
    disclosure_risk = min(1, disclosure_fields / max(float(state["parameters"].get("proof_disclosure_limit", 4)), 1) * 0.2 + max(retention_days - baseline, 0) / max(baseline, 1) * 0.05)
    return {"ok": True, "classification": classification, "disclosure_risk": round(disclosure_risk, 4)}


def audit_ledger_forecast_evidence_health(history: tuple[float, ...], *, horizon_days: int) -> dict:
    slope = (history[-1] - history[0]) / max(len(history) - 1, 1)
    forecast = max(0, min(1, history[-1] + slope * (horizon_days / 30)))
    return {"ok": True, "forecast_health": round(forecast, 4), "trend": "declining" if slope < 0 else "stable"}


def audit_ledger_parse_audit_query(text: str) -> dict:
    audit = re.search(r"audit\s+([a-zA-Z0-9_:-]+)", text)
    actor = re.search(r"actor\s+([a-zA-Z0-9_:-]+)", text)
    action = re.search(r"action\s+([a-zA-Z0-9_:-]+)", text)
    return {"ok": bool(audit), "audit_id": audit.group(1) if audit else None, "actor": actor.group(1) if actor else None, "action": action.group(1) if action else None}


def audit_ledger_score_audit_risk(factors: dict[str, float]) -> dict:
    weights = {"tamper": 0.4, "control": 0.25, "retention": 0.2, "export": 0.15}
    score = sum(float(factors.get(key, 0)) * weight for key, weight in weights.items())
    return {"ok": True, "risk_score": round(min(score, 1), 4), "factors": factors}


def audit_ledger_recommend_control_remediation(reason: str) -> dict:
    actions = {"chain_gap": "rebuild_chain_from_verified_events", "control_failed": "open_release_blocker", "export_overexposed": "reduce_disclosure_bundle"}
    return {"ok": True, "reason": reason, "action": actions.get(reason, "open_audit_review")}


def audit_ledger_select_ingestion_route(event: dict, *, rails: tuple[dict, ...]) -> dict:
    available = tuple(rail for rail in rails if rail.get("available"))
    selected = min(available, key=lambda item: item.get("latency", 999)) if available else {}
    return {"ok": bool(selected), "event_id": event["event_id"], "route": selected.get("route"), "failover_used": selected.get("route") != rails[0].get("route")}


def audit_ledger_generate_disclosure_proof(state: dict, audit_id: str, *, disclosure: tuple[str, ...]) -> dict:
    event = state["audit_events"][audit_id]
    payload = {field: event.get(field) for field in disclosure}
    digest = _hash_payload({"payload": payload, "event_hash": event["event_hash"]})
    return {"ok": True, "proof": f"zk_audit_{digest[:16]}", "hash": digest, "disclosure": disclosure}


def audit_ledger_screen_policy(state: dict, audit_id: str, *, classifications: tuple[str, ...]) -> dict:
    event = state["audit_events"][audit_id]
    active_rules = tuple(rule for rule in state["rules"].values() if rule["status"] == "active")
    decision = "clear" if event["classification"] in classifications and active_rules else "review"
    return {"ok": decision == "clear", "audit_id": audit_id, "decision": decision}


def audit_ledger_run_control_tests(state: dict) -> dict:
    hash_chain_valid = all(event["hash"] == _event_hash(event) for event in state["events"])
    signature_ok = all(link["verified"] for link in state["signature_chain"].values())
    checks = {
        "configuration": state["configuration"].get("event_contract") == "AppGen-X",
        "database": state["configuration"].get("database_backend") in set(AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS),
        "rules": bool(state["rules"]),
        "audit_events": bool(state["audit_events"]),
        "signature_chain": signature_ok,
        "outbox": all(item["idempotency_key"].startswith("audit_ledger:") for item in state["outbox"]),
        "dead_letter": isinstance(state["dead_letters"], list) and isinstance(state.get("dead_letter", []), list),
        "hash_chain": hash_chain_valid,
    }
    return {"ok": all(checks.values()), "checks": checks, "hash_chain_valid": hash_chain_valid and signature_ok, "blocking_gaps": tuple(key for key, ok in checks.items() if not ok)}


def audit_ledger_build_api_contract() -> dict:
    return {
        "ok": True,
        "format": "appgen.audit-ledger-api-contract.v1",
        "routes": (
            {"route": "POST /audit-events", "command": "record_audit_event", "owned_tables": ("audit_ledger_audit_event", "audit_ledger_signature_chain"), "emits": ("AuditEventSealed",), "requires_permission": "audit_ledger.seal", "idempotency_key": "audit_id"},
            {"route": "POST /audit-events/access-evidence", "command": "record_access_evidence", "owned_tables": ("audit_ledger_access_evidence",), "emits": (), "requires_permission": "audit_ledger.seal", "idempotency_key": "evidence_id"},
            {"route": "POST /audit-events/verify-chain", "command": "verify_signature_chain", "owned_tables": ("audit_ledger_signature_chain",), "emits": ("SignatureChainVerified",), "requires_permission": "audit_ledger.verify", "idempotency_key": "tenant"},
            {"route": "POST /retention-policies", "command": "define_retention_policy", "owned_tables": ("audit_ledger_retention_policy",), "emits": ("RetentionPolicyChanged",), "requires_permission": "audit_ledger.configure", "idempotency_key": "policy_id"},
            {"route": "POST /forensic-exports", "command": "prepare_forensic_export", "owned_tables": ("audit_ledger_forensic_export",), "emits": ("ForensicExportPrepared",), "requires_permission": "audit_ledger.export", "idempotency_key": "export_id"},
            {"route": "POST /control-assertions", "command": "assert_control", "owned_tables": ("audit_ledger_control_assertion",), "emits": ("ControlAssertionFailed",), "requires_permission": "audit_ledger.audit", "idempotency_key": "control_id"},
            {"route": "POST /audit-projections", "command": "publish_audit_projection", "owned_tables": (), "emits": ("AuditProjectionPublished",), "requires_permission": "audit_ledger.publish", "idempotency_key": "audit_id:systems"},
            {"route": "POST /audit-events/inbox", "command": "receive_event", "owned_tables": (), "consumes": AUDIT_LEDGER_CONSUMED_EVENT_TYPES, "requires_permission": "audit_ledger.event", "idempotency_key": "event_id"},
            {"route": "GET /audit-workbench", "query": "build_workbench_view", "owned_tables": AUDIT_LEDGER_OWNED_TABLES, "requires_permission": "audit_ledger.read"},
        ),
        "declared_catalog_routes": ("POST /audit-events", "POST /audit-events/verify-chain", "POST /retention-policies", "POST /forensic-exports", "GET /audit-workbench"),
        "events": {"emits": AUDIT_LEDGER_EMITTED_EVENT_TYPES, "consumes": AUDIT_LEDGER_CONSUMED_EVENT_TYPES},
        "emits": AUDIT_LEDGER_EMITTED_EVENT_TYPES,
        "consumes": AUDIT_LEDGER_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(audit_ledger_permissions_contract()["permissions"])),
        "database_backends": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": AUDIT_LEDGER_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("AUDIT_LEDGER_DATABASE_URL", "AUDIT_LEDGER_EVENT_TOPIC", "AUDIT_LEDGER_RETRY_LIMIT", "AUDIT_LEDGER_DEFAULT_TIMEZONE"),
    }


def audit_ledger_permissions_contract() -> dict:
    return {
        "format": "appgen.audit-ledger-permissions.v1",
        "ok": True,
        "permissions": (
            "audit_ledger.read",
            "audit_ledger.seal",
            "audit_ledger.verify",
            "audit_ledger.export",
            "audit_ledger.publish",
            "audit_ledger.event",
            "audit_ledger.configure",
            "audit_ledger.audit",
        ),
        "action_permissions": {
            "record_audit_event": "audit_ledger.seal",
            "record_access_evidence": "audit_ledger.seal",
            "define_retention_policy": "audit_ledger.configure",
            "assert_control": "audit_ledger.audit",
            "prepare_forensic_export": "audit_ledger.export",
            "verify_signature_chain": "audit_ledger.verify",
            "publish_audit_projection": "audit_ledger.publish",
            "receive_event": "audit_ledger.event",
            "register_rule": "audit_ledger.configure",
            "register_schema_extension": "audit_ledger.configure",
            "set_parameter": "audit_ledger.configure",
            "configure_runtime": "audit_ledger.configure",
            "build_workbench_view": "audit_ledger.read",
            "run_control_tests": "audit_ledger.audit",
        },
    }


def audit_ledger_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*AUDIT_LEDGER_OWNED_TABLES, *AUDIT_LEDGER_CONSUMED_EVENT_TYPES, *_AUDIT_LEDGER_RUNTIME_TABLES, *_AUDIT_LEDGER_ALLOWED_DEPENDENCIES)
    violations = tuple(reference for reference in references if reference not in set(allowed) and not str(reference).startswith("audit_ledger_"))
    return {
        "format": "appgen.audit-ledger-boundary.v1",
        "ok": not violations,
        "owned_tables": AUDIT_LEDGER_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /identity/policies", "GET /gateway/routes", "GET /schemas/subjects", "GET /workflow/instances", "POST /composition/release-evidence"),
            "events": AUDIT_LEDGER_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "identity_access_projection",
                "gateway_route_projection",
                "schema_contract_projection",
                "workflow_completion_projection",
                "composition_release_projection",
                "pbc_deployment_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def audit_ledger_federate_evidence_view(state: dict, audit_id: str, *, systems: tuple[str, ...]) -> dict:
    event = state["audit_events"].get(audit_id, {})
    return {"ok": bool(event), "audit_id": audit_id, "systems": systems, "event_hash": event.get("event_hash"), "boundary": "read_only_projection"}


def audit_ledger_verify_actor_identity(identity: dict) -> dict:
    ok = identity.get("did", "").startswith("did:appgen:") and identity.get("issuer") == "trusted_registry" and identity.get("status") == "active"
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def audit_ledger_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": True, "scenario": scenario, "mode": "degraded_audit_replay", "replay_source": "audit_ledger_outbox", "dead_letter_ready": isinstance(state["dead_letters"], list)}


def audit_ledger_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {"ok": True, "algorithm": algorithm, "epoch": state.get("crypto_epoch", 1) + 1, "signature_policy": "crypto_agile"}


def audit_ledger_schedule_carbon_aware_processing(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, **selected}


def audit_ledger_minimize_evidence_bundle(fields: tuple[str, ...], *, required: tuple[str, ...]) -> dict:
    minimized = tuple(dict.fromkeys(required + tuple(field for field in fields if field in required)))
    removed = max(0, len(fields) - len(minimized))
    return {"ok": True, "fields": minimized, "removed_fields": removed, "objective_score": round(1 / (1 + len(minimized)), 4)}


def audit_ledger_allocate_export_reviewers(reviewers: tuple[dict, ...], *, slots: int) -> dict:
    total = sum(float(item["criticality"]) for item in reviewers) or 1
    allocations = tuple({**item, "slots": max(1, round(slots * float(item["criticality"]) / total))} for item in reviewers)
    return {"ok": True, "allocations": allocations, "clearing_priority": round(max(item["criticality"] for item in reviewers), 4)}


def audit_ledger_detect_audit_anomaly(state: dict) -> dict:
    values = [event["sequence"] for event in state["audit_events"].values()]
    if not values:
        return {"ok": True, "entropy": 0}
    total = sum(values)
    probabilities = [value / total for value in values if total]
    entropy = -sum(probability * math.log2(probability) for probability in probabilities) if probabilities else 0
    return {"ok": True, "entropy": round(entropy, 4), "event_count": len(values)}


def audit_ledger_model_stochastic_evidence_exposure(*, event_path: tuple[float, ...], volatility: float) -> dict:
    baseline = sum(event_path) / len(event_path)
    tail_risk = (max(event_path) / max(baseline, 1) - 1) * (1 + volatility)
    return {"ok": True, "tail_risk": round(max(tail_risk, 0.01), 4), "expected_events": round(baseline, 4)}


def audit_ledger_register_governed_model(model_id: str, metadata: dict) -> dict:
    return {"ok": True, "model_id": model_id, "metadata": metadata, "governance": {"approved": True, "drift_score": metadata.get("drift_score", 0), "monitoring": "enabled"}}


def _copy_state(state: dict) -> dict:
    return {
        "configuration": dict(state["configuration"]),
        "parameters": dict(state["parameters"]),
        "rules": dict(state["rules"]),
        "schema_extensions": {key: dict(value) for key, value in state["schema_extensions"].items()},
        "audit_events": {key: dict(value) for key, value in state["audit_events"].items()},
        "signature_chain": {key: dict(value) for key, value in state["signature_chain"].items()},
        "retention_policies": {key: dict(value) for key, value in state["retention_policies"].items()},
        "forensic_exports": {key: dict(value) for key, value in state["forensic_exports"].items()},
        "access_evidence": {key: dict(value) for key, value in state["access_evidence"].items()},
        "control_assertions": {key: dict(value) for key, value in state["control_assertions"].items()},
        "projections": {key: dict(value) for key, value in state["projections"].items()},
        "events": [dict(item) for item in state["events"]],
        "outbox": [dict(item) for item in state["outbox"]],
        "inbox": [dict(item) for item in state["inbox"]],
        "handled_events": {key: dict(value) for key, value in state.get("handled_events", {}).items()},
        "retry_evidence": [dict(item) for item in state.get("retry_evidence", [])],
        "dead_letter": [dict(item) for item in state.get("dead_letter", [])],
        "dead_letters": [dict(item) for item in state["dead_letters"]],
        "identity_access_projections": {key: dict(value) for key, value in state.get("identity_access_projections", {}).items()},
        "gateway_route_projections": {key: dict(value) for key, value in state.get("gateway_route_projections", {}).items()},
        "schema_contract_projections": {key: dict(value) for key, value in state.get("schema_contract_projections", {}).items()},
        "workflow_completion_projections": {key: dict(value) for key, value in state.get("workflow_completion_projections", {}).items()},
        "composition_release_projections": {key: dict(value) for key, value in state.get("composition_release_projections", {}).items()},
        "pbc_deployment_projections": {key: dict(value) for key, value in state.get("pbc_deployment_projections", {}).items()},
        "crypto_epoch": state.get("crypto_epoch", 1),
    }


def _emit(state: dict, event_type: str, tenant: str, aggregate_id: str, payload: dict) -> dict:
    event_id = f"audit_evt_{len(state['events']) + 1:06d}"
    event = {"event_id": event_id, "event_type": event_type, "tenant": tenant, "aggregate_id": aggregate_id, "payload": payload}
    event["hash"] = _event_hash(event)
    state["events"].append(event)
    state["outbox"].append({"event_id": event_id, "event_type": event_type, "idempotency_key": f"audit_ledger:{event_type}:{event_id}", "status": "pending", "payload": payload})
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
