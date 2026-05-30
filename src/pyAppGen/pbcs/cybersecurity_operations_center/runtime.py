"""Executable runtime for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any

from .models import (
    ALERT_STATES,
    ALERT_TRANSITIONS,
    APPGEN_EVENT_CONTRACT,
    AssetExposure,
    BUSINESS_TABLES,
    ContainmentAction,
    ControlAssertion,
    EVENT_TABLES,
    GovernedModel,
    HIGH_RISK_CONTAINMENT_ACTIONS,
    MODEL_REGISTRY,
    OWNED_TABLES,
    PARAMETER_BOUNDS,
    PERMISSIONS,
    PLAYBOOK_STAGES,
    PlaybookRun,
    PolicyRule,
    RULE_NAMES,
    ResponseEvidence,
    RuntimeParameter,
    SchemaExtension,
    SecurityAlert,
    SecurityIncident,
    ThreatIntel,
    default_parameter_records,
    default_policy_bundle,
    model_contracts,
    stable_digest,
    table_schema_map,
    table_sql_definitions,
    utc_now,
)
from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_OPERATIONS,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    DOMAIN_WORKBENCH_VIEWS,
    domain_depth_contract,
)
from .soc_control import SOC_CONTROL_CAPABILITIES, improve1_soc_control_contract

PBC_KEY = "cybersecurity_operations_center"
SCHEMA_MAP = table_schema_map()

ALERT_TABLE = f"{PBC_KEY}_security_alert"
INCIDENT_TABLE = f"{PBC_KEY}_security_incident"
ASSET_TABLE = f"{PBC_KEY}_asset_exposure"
THREAT_INTEL_TABLE = f"{PBC_KEY}_threat_intel"
PLAYBOOK_TABLE = f"{PBC_KEY}_playbook_run"
CONTAINMENT_TABLE = f"{PBC_KEY}_containment_action"
EVIDENCE_TABLE = f"{PBC_KEY}_response_evidence"
POLICY_TABLE = f"{PBC_KEY}_cybersecurity_operations_center_policy_rule"
PARAMETER_TABLE = f"{PBC_KEY}_cybersecurity_operations_center_runtime_parameter"
SCHEMA_EXTENSION_TABLE = f"{PBC_KEY}_cybersecurity_operations_center_schema_extension"
CONTROL_ASSERTION_TABLE = f"{PBC_KEY}_cybersecurity_operations_center_control_assertion"
GOVERNED_MODEL_TABLE = f"{PBC_KEY}_cybersecurity_operations_center_governed_model"
OUTBOX_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"

CYBERSECURITY_OPERATIONS_CENTER_OWNED_TABLES = OWNED_TABLES
CYBERSECURITY_OPERATIONS_CENTER_RUNTIME_TABLES = OWNED_TABLES
CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES = (
    "CybersecurityOperationsCenterCreated",
    "CybersecurityOperationsCenterUpdated",
    "CybersecurityOperationsCenterApproved",
    "CybersecurityOperationsCenterExceptionOpened",
)
CYBERSECURITY_OPERATIONS_CENTER_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
CYBERSECURITY_OPERATIONS_CENTER_STANDARD_FEATURE_KEYS = (
    "security_alert_management",
    "cybersecurity_operations_center_workflow",
    "cybersecurity_operations_center_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
)
CYBERSECURITY_OPERATIONS_CENTER_RUNTIME_CAPABILITY_KEYS = tuple(
    capability.replace(" ", "_") for capability in DOMAIN_ADVANCED_CAPABILITIES
)
CYBERSECURITY_OPERATIONS_CENTER_UI_FRAGMENT_KEYS = (
    "CybersecurityOperationsCenterWorkbench",
    "CybersecurityOperationsCenterDetail",
    "CybersecurityOperationsCenterAssistantPanel",
)
CYBERSECURITY_OPERATIONS_CENTER_BUSINESS_TABLES = BUSINESS_TABLES


def _copy(state: dict[str, Any]) -> dict[str, Any]:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _parse_timestamp(value: str | None) -> datetime:
    if not value:
        return datetime.fromisoformat(utc_now())
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _table(state: dict[str, Any], table_name: str) -> dict[str, dict[str, Any]]:
    return state["tables"][table_name]


def _store_record(state: dict[str, Any], table_name: str, record: dict[str, Any]) -> dict[str, Any]:
    _table(state, table_name)[record["id"]] = dict(record)
    return _table(state, table_name)[record["id"]]


def _record_event(
    state: dict[str, Any],
    event_type: str,
    aggregate_id: str,
    tenant: str,
    payload: dict[str, Any],
    status: str = "queued",
) -> dict[str, Any]:
    event = {
        "id": f"evt-{stable_digest(event_type, aggregate_id, payload)[:12]}",
        "tenant": tenant,
        "event_type": event_type,
        "topic": CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
        "aggregate_id": aggregate_id,
        "payload": dict(payload),
        "idempotency_key": stable_digest(event_type, aggregate_id, payload),
        "created_at": utc_now(),
        "status": status,
    }
    _store_record(state, OUTBOX_TABLE, event)
    state["outbox"].append(event)
    return event


def _append_dead_letter(state: dict[str, Any], event: dict[str, Any], reason: str) -> dict[str, Any]:
    dead_letter = {
        "id": f"dead-{stable_digest(event, reason)[:12]}",
        "tenant": event.get("tenant", "default"),
        "event_type": event.get("event_type", "unknown"),
        "topic": event.get("topic", CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC),
        "payload": dict(event),
        "idempotency_key": event.get("idempotency_key") or stable_digest(event),
        "created_at": utc_now(),
        "status": "failed",
        "failure_reason": reason,
        "retry_policy": {"max_attempts": 5},
    }
    _store_record(state, DEAD_LETTER_TABLE, dead_letter)
    state["dead_letter"].append(dead_letter)
    return dead_letter


def _append_timeline_entry(
    state: dict[str, Any],
    case_id: str,
    case_type: str,
    action: str,
    actor: str,
    summary: str,
    related_ids: tuple[str, ...] = (),
) -> dict[str, Any]:
    entry = {
        "at": utc_now(),
        "case_id": case_id,
        "case_type": case_type,
        "action": action,
        "actor": actor,
        "summary": summary,
        "related_ids": related_ids,
    }
    state["timeline"].append(entry)
    return entry


def _transition_allowed(current_status: str, next_status: str) -> bool:
    return next_status in ALERT_TRANSITIONS.get(current_status, set())


def _lane_for_alert(alert: dict[str, Any]) -> str:
    status = alert["status"]
    if status == "suppressed":
        return "suppressed"
    if status in {"escalated", "contained"}:
        return "urgent"
    if alert["severity"] == "critical" or alert["confidence"] >= 0.85:
        return "urgent"
    if alert["severity"] == "low" and alert["confidence"] < 0.55:
        return "watchlist"
    return "backlog"


def _alert_cluster_key(payload: dict[str, Any]) -> str:
    detection = payload.get("detection_context", {})
    return stable_digest(
        payload.get("tenant", "default"),
        payload.get("asset_ref"),
        payload.get("principal_ref"),
        payload.get("indicator_value"),
        detection.get("detection_rule_id"),
        detection.get("evidence_checksum"),
    )[:12]


def _find_duplicate_alert(
    state: dict[str, Any],
    payload: dict[str, Any],
    dedup_window_hours: int,
) -> dict[str, Any] | None:
    detection = payload.get("detection_context", {})
    checksum = detection.get("evidence_checksum")
    rule_id = detection.get("detection_rule_id")
    if not checksum and not rule_id:
        return None
    now = _parse_timestamp(detection.get("detection_timestamp"))
    for record in _table(state, ALERT_TABLE).values():
        if record["tenant"] != payload.get("tenant", "default"):
            continue
        existing_detection = record.get("detection_context", {})
        if existing_detection.get("detection_rule_id") != rule_id:
            continue
        if existing_detection.get("evidence_checksum") != checksum:
            continue
        if record.get("asset_ref") != payload.get("asset_ref"):
            continue
        existing_time = _parse_timestamp(existing_detection.get("detection_timestamp"))
        if abs((now - existing_time).total_seconds()) > dedup_window_hours * 3600:
            continue
        return record
    return None


def _explainable_incident_score(alerts: list[dict[str, Any]], payload: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    severity_weights = {"low": 0.2, "medium": 0.45, "high": 0.7, "critical": 0.95}
    asset_criticality_weights = {"low": 0.2, "medium": 0.45, "high": 0.7, "critical": 0.95}
    severity = max((severity_weights.get(alert["severity"], 0.45) for alert in alerts), default=0.3)
    repeat_factor = min(1.0, len(alerts) / 4)
    containment_factor = 1.0 if payload.get("containment_required") else 0.35
    business_factor = asset_criticality_weights.get(payload.get("asset_criticality", "medium"), 0.45)
    score = round((severity * 0.35) + (repeat_factor * 0.2) + (containment_factor * 0.2) + (business_factor * 0.25), 4)
    return score, {
        "severity_factor": severity,
        "repeat_detection_factor": repeat_factor,
        "containment_factor": containment_factor,
        "business_criticality_factor": business_factor,
    }


def _incident_preview(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    alert_ids = tuple(payload.get("alert_ids", ()))
    alerts = [record for record in _table(state, ALERT_TABLE).values() if record["id"] in alert_ids]
    policy = state["policy"]
    score, factors = _explainable_incident_score(alerts, payload)
    blockers = []
    if len(alerts) < policy["promotion_cluster_threshold"] and payload.get("asset_criticality") != "critical":
        blockers.append("promotion_cluster_threshold_not_met")
    if not alerts:
        blockers.append("no_alerts_selected")
    should_promote = not blockers or (payload.get("containment_required") and payload.get("asset_criticality") in {"high", "critical"})
    return {
        "ok": True,
        "alert_count": len(alerts),
        "should_promote": should_promote,
        "blockers": tuple(blockers),
        "explainable_score": score,
        "score_factors": factors,
        "linked_alert_ids": alert_ids,
    }


def _compute_metrics(state: dict[str, Any], tenant: str) -> dict[str, Any]:
    alerts = [record for record in _table(state, ALERT_TABLE).values() if record["tenant"] == tenant]
    incidents = [record for record in _table(state, INCIDENT_TABLE).values() if record["tenant"] == tenant]
    evidences = [record for record in _table(state, EVIDENCE_TABLE).values() if record["tenant"] == tenant]
    playbooks = [record for record in _table(state, PLAYBOOK_TABLE).values() if record["tenant"] == tenant]
    duplicates = sum(1 for record in alerts if record.get("duplicate_of"))
    suppressed = sum(1 for record in alerts if record["status"] == "suppressed")
    false_positives = sum(1 for record in alerts if record.get("false_positive"))
    promoted = sum(1 for record in alerts if record.get("incident_id"))
    reopened = sum(1 for record in alerts if record["status"] == "reopened")
    breakpoint_runs = sum(1 for record in playbooks if record["breakpoint_required"])
    evidence_ready = sum(1 for record in evidences if record["redaction_status"] == "ready_for_release")
    return {
        "lane_counts": {
            "urgent": sum(1 for alert in alerts if alert["lane"] == "urgent"),
            "backlog": sum(1 for alert in alerts if alert["lane"] == "backlog"),
            "watchlist": sum(1 for alert in alerts if alert["lane"] == "watchlist"),
            "suppressed": sum(1 for alert in alerts if alert["lane"] == "suppressed"),
        },
        "incident_counts": {
            "open": sum(1 for incident in incidents if incident["status"] != "closed"),
            "closed": sum(1 for incident in incidents if incident["status"] == "closed"),
        },
        "detection_quality": {
            "duplicate_rate": round(duplicates / len(alerts), 4) if alerts else 0.0,
            "suppression_rate": round(suppressed / len(alerts), 4) if alerts else 0.0,
            "false_positive_rate": round(false_positives / len(alerts), 4) if alerts else 0.0,
            "promotion_rate": round(promoted / len(alerts), 4) if alerts else 0.0,
            "reopened_rate": round(reopened / len(alerts), 4) if alerts else 0.0,
        },
        "automation_effectiveness": {
            "playbook_runs": len(playbooks),
            "breakpoint_frequency": round(breakpoint_runs / len(playbooks), 4) if playbooks else 0.0,
        },
        "evidence_readiness": {
            "ready_for_release": evidence_ready,
            "needs_review": sum(1 for record in evidences if record["redaction_status"] != "ready_for_release"),
        },
    }


def _build_case_detail(state: dict[str, Any], case_id: str) -> dict[str, Any]:
    incident = _table(state, INCIDENT_TABLE).get(case_id)
    if incident:
        alerts = [record for record in _table(state, ALERT_TABLE).values() if record.get("incident_id") == case_id]
        evidence = [record for record in _table(state, EVIDENCE_TABLE).values() if record["case_id"] == case_id]
        containment_actions = [
            record for record in _table(state, CONTAINMENT_TABLE).values() if record.get("incident_id") == case_id
        ]
        graph_edges = tuple(
            {"from": case_id, "to": item["id"], "relation": relation}
            for relation, records in (
                ("alert", alerts),
                ("evidence", evidence),
                ("containment_action", containment_actions),
            )
            for item in records
        )
        return {
            "ok": True,
            "case_type": "incident",
            "case": incident,
            "alerts": tuple(alerts),
            "evidence": tuple(evidence),
            "containment_actions": tuple(containment_actions),
            "timeline": tuple(entry for entry in state["timeline"] if entry["case_id"] == case_id),
            "relationship_graph": {"nodes": (incident, *alerts, *evidence, *containment_actions), "edges": graph_edges},
            "event_lineage": tuple(
                record for record in _table(state, OUTBOX_TABLE).values() if record.get("aggregate_id") in {case_id, *(item["id"] for item in alerts)}
            ),
        }
    alert = _table(state, ALERT_TABLE).get(case_id)
    if not alert:
        return {"ok": False, "reason": "case_not_found", "case_id": case_id, "side_effects": ()}
    evidence = [record for record in _table(state, EVIDENCE_TABLE).values() if record["id"] in alert.get("evidence_ids", [])]
    return {
        "ok": True,
        "case_type": "alert",
        "case": alert,
        "alerts": (alert,),
        "evidence": tuple(evidence),
        "containment_actions": (),
        "timeline": tuple(
            {"case_id": alert["id"], "case_type": "alert", **entry}
            for entry in alert.get("lineage", ())
        ),
        "relationship_graph": {
            "nodes": (alert, *evidence),
            "edges": tuple({"from": alert["id"], "to": item["id"], "relation": "evidence"} for item in evidence),
        },
        "event_lineage": tuple(
            record for record in _table(state, OUTBOX_TABLE).values() if record.get("aggregate_id") == alert["id"]
        ),
    }


def cybersecurity_operations_center_empty_state() -> dict[str, Any]:
    tables = {table: {} for table in OWNED_TABLES}
    state = {
        "tables": tables,
        "configuration": {
            "database_backend": "postgresql",
            "event_topic": CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
        },
        "policy": default_policy_bundle(),
        "parameters": {record["parameter_name"]: record for record in default_parameter_records()},
        "rules": {},
        "schema_extensions": {},
        "timeline": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
        "metrics_snapshots": [],
        "notices": [],
    }
    for parameter in state["parameters"].values():
        _store_record(state, PARAMETER_TABLE, parameter)
    return state


def cybersecurity_operations_center_configure_runtime(state: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    backend = config.get("database_backend", "postgresql")
    event_topic = config.get("event_topic", CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC)
    ok = (
        backend in CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS
        and event_topic == CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        **next_state["configuration"],
        **dict(config),
        "database_backend": backend,
        "event_topic": event_topic,
        "event_contract": APPGEN_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
    }
    if not ok:
        next_state["notices"].append("runtime_configuration_invalid")
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def cybersecurity_operations_center_set_parameter(
    state: dict[str, Any],
    name: str,
    value: Any,
    actor: str = "system",
    rationale: str = "updated",
) -> dict[str, Any]:
    next_state = _copy(state)
    if name not in PARAMETER_BOUNDS:
        return {"ok": False, "state": next_state, "reason": "unknown_parameter", "side_effects": ()}
    minimum, maximum = PARAMETER_BOUNDS[name]
    ok = minimum <= value <= maximum
    parameter = RuntimeParameter(
        id=f"param-{name}",
        tenant="default",
        code=name.upper(),
        status="active" if ok else "rejected",
        parameter_name=name,
        value=value,
        minimum=minimum,
        maximum=maximum,
        rationale=rationale,
    ).to_row()
    _store_record(next_state, PARAMETER_TABLE, parameter)
    if ok:
        next_state["parameters"][name] = parameter
        _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[1], parameter["id"], "default", {"parameter_name": name, "actor": actor})
    return {"ok": ok, "state": next_state, "parameter": parameter, "side_effects": ()}


def cybersecurity_operations_center_register_rule(
    state: dict[str, Any],
    rule: dict[str, Any],
    actor: str = "system",
) -> dict[str, Any]:
    next_state = _copy(state)
    rule_name = rule.get("rule_name") or rule.get("rule_id") or "security_alert_policy"
    if rule_name not in RULE_NAMES:
        return {"ok": False, "state": next_state, "reason": "unknown_rule", "side_effects": ()}
    simulation_preview = {
        "dedup_window_hours": rule.get("policy", {}).get("dedup_window_hours", next_state["policy"]["dedup_window_hours"]),
        "promotion_cluster_threshold": rule.get("policy", {}).get("promotion_cluster_threshold", next_state["policy"]["promotion_cluster_threshold"]),
    }
    compiled = PolicyRule(
        id=rule.get("id", f"rule-{rule_name}"),
        tenant=rule.get("tenant", "default"),
        code=rule_name.upper(),
        status="active",
        rule_name=rule_name,
        policy=rule.get("policy", {}),
        simulation_preview=simulation_preview,
    ).to_row()
    _store_record(next_state, POLICY_TABLE, compiled)
    next_state["rules"][compiled["rule_name"]] = compiled
    next_state["policy"] = {**next_state["policy"], **compiled["policy"]}
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[2], compiled["id"], compiled["tenant"], {"rule_name": rule_name, "actor": actor})
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def cybersecurity_operations_center_register_schema_extension(
    state: dict[str, Any],
    table: str,
    fields: dict[str, str],
    actor: str = "system",
) -> dict[str, Any]:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    extension = SchemaExtension(
        id=f"schema-extension-{stable_digest(owned_name, fields)[:8]}",
        tenant="default",
        code=owned_name.upper(),
        status="proposed",
        target_table=owned_name,
        fields=dict(fields),
    ).to_row()
    _store_record(next_state, SCHEMA_EXTENSION_TABLE, extension)
    next_state["schema_extensions"][owned_name] = dict(fields)
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[1], extension["id"], "default", {"table": owned_name, "actor": actor})
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def cybersecurity_operations_center_receive_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    idempotency_key = event.get("idempotency_key") or event.get("event_id") or stable_digest(event)
    if idempotency_key in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idempotency_key)
    if event.get("event_type") not in CYBERSECURITY_OPERATIONS_CENTER_CONSUMED_EVENT_TYPES:
        dead_letter = _append_dead_letter(next_state, event, "unsupported_event_type")
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": DEAD_LETTER_TABLE,
            "dead_letter": dead_letter,
            "side_effects": (),
        }

    inbox_event = {
        "id": f"inbox-{stable_digest(idempotency_key)[:12]}",
        "tenant": event.get("tenant", "default"),
        "event_type": event["event_type"],
        "topic": event.get("topic", CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC),
        "payload": dict(event.get("payload", {})),
        "idempotency_key": idempotency_key,
        "created_at": utc_now(),
        "status": "processed",
    }
    _store_record(next_state, INBOX_TABLE, inbox_event)
    next_state["inbox"].append(inbox_event)

    effect = "inbox_recorded"
    if event["event_type"] == "PolicyChanged":
        incoming_policy = dict(event.get("payload", {}))
        next_state["policy"] = {**next_state["policy"], **incoming_policy}
        effect = "policy_updated"
    elif event["event_type"] == "AuditEventSealed":
        sealed_bundle_id = event.get("payload", {}).get("sealed_bundle_id")
        evidence_id = event.get("payload", {}).get("evidence_id")
        evidence = _table(next_state, EVIDENCE_TABLE).get(evidence_id)
        if evidence:
            evidence["sealed_bundle_id"] = sealed_bundle_id or f"bundle-{evidence_id}"
            evidence["redaction_status"] = "ready_for_release"
            evidence["updated_at"] = utc_now()
            effect = "evidence_sealed"
        else:
            effect = "seal_notice_without_local_evidence"
    elif event["event_type"] == "OperationalKpiChanged":
        snapshot = _compute_metrics(next_state, event.get("tenant", "default"))
        next_state["metrics_snapshots"].append({"at": utc_now(), "metrics": snapshot})
        effect = "metrics_refreshed"

    next_state["notices"].append(effect)
    return {"ok": True, "duplicate": False, "effect": effect, "state": next_state, "side_effects": ()}


def cybersecurity_operations_center_command_security_alert(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    items = payload.get("items") or (payload,)
    created = []
    duplicates = []
    rejected = []
    for item in items:
        detection = dict(item.get("detection_context", {}))
        required_detection_fields = {"source_event_id", "detection_timestamp", "detection_rule_id"}
        missing = tuple(sorted(field for field in required_detection_fields if not detection.get(field)))
        if missing:
            rejected.append({"payload": dict(item), "reason": "missing_detection_context", "missing": missing})
            continue
        duplicate = _find_duplicate_alert(next_state, item, next_state["policy"]["dedup_window_hours"])
        alert_id = item.get("id") or f"alert-{stable_digest(item, utc_now())[:10]}"
        validation_only = bool(item.get("validation_only") or payload.get("validation_only"))
        cluster_id = duplicate.get("cluster_id") if duplicate else _alert_cluster_key(item)
        record = SecurityAlert(
            id=alert_id,
            tenant=item.get("tenant", "default"),
            code=item.get("code", alert_id.upper()),
            status="deduplicated" if duplicate else item.get("status", "new"),
            severity=item.get("severity", "medium"),
            confidence=float(item.get("confidence", detection.get("confidence", 0.5))),
            asset_ref=item.get("asset_ref", "unknown"),
            principal_ref=item.get("principal_ref", "unknown"),
            indicator_value=item.get("indicator_value", "unknown"),
            blast_radius=item.get("blast_radius", "single_asset"),
            assignee=item.get("assignee"),
            lane="backlog",
            previous_status=duplicate["status"] if duplicate else None,
            incident_id=None,
            duplicate_of=duplicate["id"] if duplicate else None,
            cluster_id=cluster_id,
            suppression={},
            false_positive=dict(item.get("false_positive", {})),
            detection_context=detection,
            enrichment=dict(item.get("enrichment", {})),
            evidence_ids=list(item.get("evidence_ids", ())),
            lineage=[],
        ).to_row()
        record["lane"] = _lane_for_alert(record)
        record["lineage"].append(
            {
                "at": utc_now(),
                "action": "create_alert",
                "actor": item.get("actor", "sensor"),
                "reason": "duplicate_merged" if duplicate else "new_intake",
            }
        )
        if validation_only:
            created.append({"validation_only": True, "record": record})
            continue
        _store_record(next_state, ALERT_TABLE, record)
        _append_timeline_entry(
            next_state,
            record["id"],
            "alert",
            "create_alert",
            item.get("actor", "sensor"),
            "Security alert ingested",
        )
        _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[0], record["id"], record["tenant"], {"status": record["status"], "cluster_id": cluster_id})
        created.append(record)
        if duplicate:
            duplicates.append({"duplicate_id": record["id"], "primary_id": duplicate["id"], "reason": "matching detection rule and checksum within dedup window"})
    return {
        "ok": not rejected,
        "state": next_state,
        "created": tuple(created),
        "duplicates": tuple(duplicates),
        "rejected": tuple(rejected),
        "side_effects": (),
    }


def cybersecurity_operations_center_transition_alert(
    state: dict[str, Any],
    alert_id: str,
    next_status: str,
    actor: str,
    reason: str,
) -> dict[str, Any]:
    next_state = _copy(state)
    alert = _table(next_state, ALERT_TABLE).get(alert_id)
    if not alert:
        return {"ok": False, "state": next_state, "reason": "alert_not_found", "side_effects": ()}
    if next_status not in ALERT_STATES or not _transition_allowed(alert["status"], next_status):
        return {"ok": False, "state": next_state, "reason": "invalid_transition", "current_status": alert["status"], "side_effects": ()}
    previous_status = alert["status"]
    alert["previous_status"] = previous_status
    alert["status"] = next_status
    alert["lane"] = _lane_for_alert(alert)
    alert["updated_at"] = utc_now()
    alert["version"] += 1
    alert["lineage"].append({"at": utc_now(), "action": "transition_alert", "actor": actor, "from": previous_status, "to": next_status, "reason": reason})
    _append_timeline_entry(next_state, alert["id"], "alert", "transition_alert", actor, f"{previous_status} -> {next_status}")
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[1], alert["id"], alert["tenant"], {"from": previous_status, "to": next_status, "reason": reason})
    return {"ok": True, "state": next_state, "record": alert, "side_effects": ()}


def cybersecurity_operations_center_enrich_security_alert(
    state: dict[str, Any],
    alert_id: str,
    enrichment: dict[str, Any],
    actor: str,
) -> dict[str, Any]:
    next_state = _copy(state)
    alert = _table(next_state, ALERT_TABLE).get(alert_id)
    if not alert:
        return {"ok": False, "state": next_state, "reason": "alert_not_found", "side_effects": ()}
    alert["enrichment"] = {**alert.get("enrichment", {}), **dict(enrichment)}
    alert["updated_at"] = utc_now()
    alert["version"] += 1
    if alert["status"] in {"new", "deduplicated", "reopened"}:
        alert["previous_status"] = alert["status"]
        alert["status"] = "enriched"
    alert["lane"] = _lane_for_alert(alert)
    alert["lineage"].append({"at": utc_now(), "action": "enrich_alert", "actor": actor, "fields": tuple(sorted(enrichment))})
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[1], alert["id"], alert["tenant"], {"action": "enrich_alert", "fields": tuple(sorted(enrichment))})
    return {"ok": True, "state": next_state, "record": alert, "side_effects": ()}


def cybersecurity_operations_center_suppress_security_alert(
    state: dict[str, Any],
    alert_id: str,
    suppression: dict[str, Any],
    actor: str,
) -> dict[str, Any]:
    next_state = _copy(state)
    alert = _table(next_state, ALERT_TABLE).get(alert_id)
    if not alert:
        return {"ok": False, "state": next_state, "reason": "alert_not_found", "side_effects": ()}
    alert["suppression"] = {
        "reason": suppression.get("reason", "analyst_tuning"),
        "scope": suppression.get("scope", "rule"),
        "duration_days": suppression.get("duration_days", 7),
        "owner": suppression.get("owner", actor),
        "review_at": suppression.get("review_at", utc_now()),
    }
    return cybersecurity_operations_center_transition_alert(next_state, alert_id, "suppressed", actor, alert["suppression"]["reason"])


def cybersecurity_operations_center_record_security_incident(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    preview = _incident_preview(state, payload)
    if payload.get("validation_only"):
        return {**preview, "state": _copy(state), "side_effects": ()}
    next_state = _copy(state)
    if not preview["should_promote"]:
        return {"ok": False, "state": next_state, "reason": "promotion_blocked", "preview": preview, "side_effects": ()}
    incident_id = payload.get("id") or f"incident-{stable_digest(payload, utc_now())[:10]}"
    incident = SecurityIncident(
        id=incident_id,
        tenant=payload.get("tenant", "default"),
        code=payload.get("code", incident_id.upper()),
        status=payload.get("status", "open"),
        title=payload.get("title", "Correlated security incident"),
        severity=payload.get("severity", "high"),
        explainable_score=preview["explainable_score"],
        commander=payload.get("commander"),
        communications_owner=payload.get("communications_owner"),
        evidence_owner=payload.get("evidence_owner"),
        containment_owner=payload.get("containment_owner"),
        promotion_summary={
            "score_factors": preview["score_factors"],
            "cluster_threshold": len(payload.get("alert_ids", ())),
            "containment_required": payload.get("containment_required", False),
        },
        alert_ids=list(payload.get("alert_ids", ())),
        evidence_ids=[],
        containment_action_ids=[],
        timeline=[],
        closure_checklist={
            "evidence_complete": False,
            "containment_validated": False,
            "severity_confirmed": False,
            "lessons_recorded": False,
            "follow_up_linked": False,
        },
    ).to_row()
    incident["timeline"].append(
        {"at": utc_now(), "action": "promote_incident", "actor": payload.get("actor", "analyst"), "summary": "Incident promoted from alert cluster"}
    )
    _store_record(next_state, INCIDENT_TABLE, incident)
    for alert_id in incident["alert_ids"]:
        alert = _table(next_state, ALERT_TABLE).get(alert_id)
        if alert:
            alert["incident_id"] = incident_id
            alert["previous_status"] = alert["status"]
            alert["status"] = "escalated"
            alert["lane"] = "urgent"
            alert["updated_at"] = utc_now()
            alert["version"] += 1
            alert["lineage"].append({"at": utc_now(), "action": "link_incident", "actor": payload.get("actor", "analyst"), "incident_id": incident_id})
    _append_timeline_entry(next_state, incident_id, "incident", "promote_incident", payload.get("actor", "analyst"), "Incident promoted from alert cluster", tuple(incident["alert_ids"]))
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[0], incident_id, incident["tenant"], {"alert_ids": incident["alert_ids"], "score": incident["explainable_score"]})
    return {"ok": True, "state": next_state, "record": incident, "preview": preview, "side_effects": ()}


def cybersecurity_operations_center_review_asset_exposure(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    asset_ref = payload.get("asset_ref", "unknown")
    open_alert_ids = [record["id"] for record in _table(next_state, ALERT_TABLE).values() if record["asset_ref"] == asset_ref and record["status"] != "closed"]
    open_incident_ids = [record["id"] for record in _table(next_state, INCIDENT_TABLE).values() if asset_ref in payload.get("related_assets", (asset_ref,)) and record["status"] != "closed"]
    exposure = AssetExposure(
        id=payload.get("id", f"asset-{stable_digest(asset_ref, utc_now())[:8]}"),
        tenant=payload.get("tenant", "default"),
        code=payload.get("code", asset_ref.upper().replace("-", "_")),
        status=payload.get("status", "active"),
        asset_ref=asset_ref,
        criticality=payload.get("criticality", "medium"),
        internet_exposed=bool(payload.get("internet_exposed", False)),
        open_alert_ids=open_alert_ids,
        open_incident_ids=open_incident_ids,
        containment_action_ids=[
            record["id"] for record in _table(next_state, CONTAINMENT_TABLE).values() if record.get("alert_id") in open_alert_ids
        ],
    ).to_row()
    _store_record(next_state, ASSET_TABLE, exposure)
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[1], exposure["id"], exposure["tenant"], {"asset_ref": asset_ref})
    return {"ok": True, "state": next_state, "record": exposure, "side_effects": ()}


def cybersecurity_operations_center_approve_threat_intel(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    intel = ThreatIntel(
        id=payload.get("id", f"intel-{stable_digest(payload, utc_now())[:8]}"),
        tenant=payload.get("tenant", "default"),
        code=payload.get("code", payload.get("indicator_value", "INTEL").upper().replace(".", "_")),
        status=payload.get("status", "draft"),
        indicator_value=payload.get("indicator_value", ""),
        observed_fact=dict(payload.get("observed_fact", {})),
        assessed_relationship=dict(payload.get("assessed_relationship", {})),
        campaign_context=dict(payload.get("campaign_context", {})),
        analyst_inference=dict(payload.get("analyst_inference", {})),
        confidence=float(payload.get("confidence", 0.5)),
        expires_at=payload.get("expires_at"),
        source_provenance=payload.get("source_provenance", "internal"),
        recommendation_preview={
            "candidate_playbooks": payload.get("candidate_playbooks", ("isolate_host",)),
            "requires_human_confirmation": True,
            "auto_execute": False,
        },
    ).to_row()
    _store_record(next_state, THREAT_INTEL_TABLE, intel)
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[2], intel["id"], intel["tenant"], {"indicator_value": intel["indicator_value"]})
    return {"ok": True, "state": next_state, "record": intel, "side_effects": ()}


def cybersecurity_operations_center_simulate_playbook_run(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    stage = payload.get("stage", PLAYBOOK_STAGES[0])
    if stage not in PLAYBOOK_STAGES:
        return {"ok": False, "state": next_state, "reason": "unknown_playbook_stage", "side_effects": ()}
    checkpoint_statuses = {
        checkpoint: ("complete" if PLAYBOOK_STAGES.index(checkpoint) < PLAYBOOK_STAGES.index(stage) else "pending")
        for checkpoint in PLAYBOOK_STAGES
    }
    checkpoint_statuses[stage] = payload.get("checkpoint_status", "running")
    breakpoint_required = stage in {"analyst_approval", "containment"} or bool(payload.get("breakpoint_required", False))
    preview = {
        "stage": stage,
        "checkpoint_statuses": checkpoint_statuses,
        "breakpoint_required": breakpoint_required,
        "requires_human_confirmation": breakpoint_required,
    }
    if payload.get("validation_only"):
        return {"ok": True, "state": next_state, "preview": preview, "side_effects": ()}
    playbook_run = PlaybookRun(
        id=payload.get("id", f"playbook-{stable_digest(payload, utc_now())[:8]}"),
        tenant=payload.get("tenant", "default"),
        code=payload.get("code", payload.get("template_name", "PLAYBOOK").upper()),
        status=payload.get("status", "running"),
        template_name=payload.get("template_name", "containment"),
        stage=stage,
        checkpoint_statuses=checkpoint_statuses,
        breakpoint_required=breakpoint_required,
        requires_human_confirmation=breakpoint_required,
        related_incident_id=payload.get("related_incident_id"),
        related_alert_id=payload.get("related_alert_id"),
        notes=list(payload.get("notes", ())),
    ).to_row()
    _store_record(next_state, PLAYBOOK_TABLE, playbook_run)
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[1], playbook_run["id"], playbook_run["tenant"], {"stage": stage, "breakpoint_required": breakpoint_required})
    return {"ok": True, "state": next_state, "record": playbook_run, "preview": preview, "side_effects": ()}


def cybersecurity_operations_center_create_containment_action(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    action_type = payload.get("action_type", "investigate")
    approval_path = HIGH_RISK_CONTAINMENT_ACTIONS.get(action_type, "no_approval")
    approved_by = payload.get("approved_by")
    if approval_path != "no_approval" and not approved_by:
        status = "pending_approval"
    else:
        status = payload.get("status", "ready")
    action = ContainmentAction(
        id=payload.get("id", f"containment-{stable_digest(payload, utc_now())[:8]}"),
        tenant=payload.get("tenant", "default"),
        code=payload.get("code", action_type.upper()),
        status=status,
        incident_id=payload.get("incident_id"),
        alert_id=payload.get("alert_id"),
        action_type=action_type,
        approval_path=approval_path,
        approved_by=approved_by,
        risk_level=payload.get("risk_level", "high" if approval_path != "no_approval" else "low"),
        rollback_instructions=payload.get("rollback_instructions", "Restore affected service and re-enable access after validation."),
        outcome_summary=payload.get("outcome_summary", ""),
    ).to_row()
    _store_record(next_state, CONTAINMENT_TABLE, action)
    if action["incident_id"]:
        incident = _table(next_state, INCIDENT_TABLE).get(action["incident_id"])
        if incident:
            incident["containment_action_ids"].append(action["id"])
            incident["timeline"].append({"at": utc_now(), "action": "create_containment_action", "actor": payload.get("actor", "analyst"), "summary": action_type})
    event_type = CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[2 if status != "pending_approval" else 1]
    _record_event(next_state, event_type, action["id"], action["tenant"], {"approval_path": approval_path, "status": status})
    return {"ok": True, "state": next_state, "record": action, "side_effects": ()}


def cybersecurity_operations_center_record_response_evidence(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    evidence = ResponseEvidence(
        id=payload.get("id", f"evidence-{stable_digest(payload, utc_now())[:8]}"),
        tenant=payload.get("tenant", "default"),
        code=payload.get("code", "EVIDENCE"),
        status=payload.get("status", "collected"),
        case_id=payload.get("case_id", ""),
        source_system=payload.get("source_system", "unknown"),
        checksum=payload.get("checksum", stable_digest(payload.get("storage_reference", ""), payload.get("source_system", ""))),
        acquired_at=payload.get("acquired_at", utc_now()),
        storage_reference=payload.get("storage_reference", "vault://pending"),
        redaction_status=payload.get("redaction_status", "needs_review"),
        admissibility_notes=payload.get("admissibility_notes", ""),
        handling_history=list(
            payload.get(
                "handling_history",
                (
                    {
                        "at": utc_now(),
                        "actor": payload.get("actor", "analyst"),
                        "action": "collect",
                        "summary": "Evidence collected into owned store",
                    },
                ),
            )
        ),
        request_status=payload.get("request_status", "collected"),
        sealed_bundle_id=payload.get("sealed_bundle_id"),
    ).to_row()
    _store_record(next_state, EVIDENCE_TABLE, evidence)
    incident = _table(next_state, INCIDENT_TABLE).get(evidence["case_id"])
    if incident:
        incident["evidence_ids"].append(evidence["id"])
        incident["timeline"].append({"at": utc_now(), "action": "record_response_evidence", "actor": payload.get("actor", "analyst"), "summary": evidence["source_system"]})
    alert = _table(next_state, ALERT_TABLE).get(evidence["case_id"])
    if alert:
        alert["evidence_ids"].append(evidence["id"])
        alert["lineage"].append({"at": utc_now(), "action": "record_response_evidence", "actor": payload.get("actor", "analyst"), "evidence_id": evidence["id"]})
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[1], evidence["id"], evidence["tenant"], {"case_id": evidence["case_id"], "checksum": evidence["checksum"]})
    return {"ok": True, "state": next_state, "record": evidence, "side_effects": ()}


def cybersecurity_operations_center_create_control_assertion(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    assertion = ControlAssertion(
        id=payload.get("id", f"control-{stable_digest(payload, utc_now())[:8]}"),
        tenant=payload.get("tenant", "default"),
        code=payload.get("code", "CONTROL"),
        status=payload.get("status", "active"),
        control_name=payload.get("control_name", "stale_high_severity_alerts"),
        control_status=payload.get("control_status", "passing"),
        evidence=dict(payload.get("evidence", {})),
    ).to_row()
    _store_record(next_state, CONTROL_ASSERTION_TABLE, assertion)
    if assertion["control_status"] != "passing":
        _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[3], assertion["id"], assertion["tenant"], {"control_name": assertion["control_name"]})
    return {"ok": True, "state": next_state, "record": assertion, "side_effects": ()}


def cybersecurity_operations_center_record_governed_model(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    model = GovernedModel(
        id=payload.get("id", f"model-{stable_digest(payload, utc_now())[:8]}"),
        tenant=payload.get("tenant", "default"),
        code=payload.get("code", payload.get("model_name", "MODEL").upper()),
        status=payload.get("status", "approved"),
        model_name=payload.get("model_name", "triage-summary"),
        intended_use=payload.get("intended_use", "Analyst summary drafting"),
        guardrails=dict(payload.get("guardrails", {"requires_human_confirmation": True, "cites_sources": True})),
    ).to_row()
    _store_record(next_state, GOVERNED_MODEL_TABLE, model)
    _record_event(next_state, CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES[2], model["id"], model["tenant"], {"model_name": model["model_name"]})
    return {"ok": True, "state": next_state, "record": model, "side_effects": ()}


def cybersecurity_operations_center_query_workbench(state: dict[str, Any], filters: dict[str, Any] | None = None) -> dict[str, Any]:
    filters = dict(filters or {})
    tenant = filters.get("tenant", "default")
    limit = filters.get("limit") or state["parameters"]["workbench_limit"]["value"]
    view = cybersecurity_operations_center_build_workbench_view(state, tenant=tenant)
    view["filters"] = filters
    view["records"] = tuple(_table(state, ALERT_TABLE).values())[:limit]
    view["read_only"] = True
    return view


def cybersecurity_operations_center_generate_handoff_packet(
    state: dict[str, Any],
    tenant: str = "default",
    actor: str = "assistant",
) -> dict[str, Any]:
    alerts = [
        record for record in _table(state, ALERT_TABLE).values()
        if record["tenant"] == tenant and record["status"] not in {"closed", "suppressed"}
    ]
    incidents = [
        record for record in _table(state, INCIDENT_TABLE).values()
        if record["tenant"] == tenant and record["status"] != "closed"
    ]
    packet = {
        "tenant": tenant,
        "summary": f"{len(alerts)} active alerts and {len(incidents)} active incidents require handoff.",
        "open_questions": tuple(
            f"Confirm next checkpoint for {incident['id']}" for incident in incidents if not incident.get("containment_owner")
        ),
        "pending_approvals": tuple(
            action["id"] for action in _table(state, CONTAINMENT_TABLE).values() if action["tenant"] == tenant and action["status"] == "pending_approval"
        ),
        "pending_evidence": tuple(
            evidence["id"] for evidence in _table(state, EVIDENCE_TABLE).values() if evidence["tenant"] == tenant and evidence["redaction_status"] != "ready_for_release"
        ),
        "next_checkpoints": tuple(
            {"case_id": incident["id"], "next_action": incident["timeline"][-1]["summary"] if incident["timeline"] else "Review ownership"}
            for incident in incidents
        ),
        "citations": tuple(
            {"record_id": record["id"], "table": ALERT_TABLE if "severity" in record else INCIDENT_TABLE}
            for record in (*alerts[:3], *incidents[:3])
        ),
        "generated_by": actor,
    }
    return {"ok": True, "packet": packet, "side_effects": ()}


def cybersecurity_operations_center_run_advanced_assessment(
    state: dict[str, Any],
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = dict(payload or {})
    tenant = payload.get("tenant", "default")
    metrics = _compute_metrics(state, tenant)
    lane_counts = metrics["lane_counts"]
    risk_score = min(1.0, round((lane_counts["urgent"] * 0.18) + (metrics["detection_quality"]["duplicate_rate"] * 0.22) + (metrics["automation_effectiveness"]["breakpoint_frequency"] * 0.1), 4))
    return {
        "ok": True,
        "tenant": tenant,
        "score": risk_score,
        "explanations": (
            "urgent_queue_pressure",
            "duplicate_alert_drag",
            "playbook_breakpoint_overhead",
        ),
        "predictive_backlog_risk": "elevated" if risk_score >= 0.7 else "stable",
        "anomaly_cards": (
            {
                "kind": "suppression_spike",
                "triggered": metrics["detection_quality"]["suppression_rate"] >= 0.4,
            },
            {
                "kind": "duplicate_spike",
                "triggered": metrics["detection_quality"]["duplicate_rate"] >= 0.35,
            },
        ),
        "payload": payload,
        "side_effects": (),
    }


def cybersecurity_operations_center_parse_document_instruction(document: str, instruction: str) -> dict[str, Any]:
    text = f"{document}\n{instruction}".lower()
    candidate_actions = []
    if "alert" in text:
        candidate_actions.append("create_security_alert")
    if "incident" in text or "escalate" in text:
        candidate_actions.append("record_security_incident")
    if "evidence" in text:
        candidate_actions.append("record_response_evidence")
    if "contain" in text or "isolate" in text:
        candidate_actions.append("create_containment_action")
    if not candidate_actions:
        candidate_actions.append("review_asset_exposure")
    return {
        "ok": True,
        "candidate_tables": (ALERT_TABLE, INCIDENT_TABLE, EVIDENCE_TABLE),
        "candidate_actions": tuple(dict.fromkeys(candidate_actions)),
        "instruction": instruction,
        "document_digest": stable_digest(document, instruction),
        "requires_human_confirmation": True,
        "guardrails": {"owned_tables_only": True, "cite_source_records": True},
        "side_effects": (),
    }


def cybersecurity_operations_center_build_schema_contract() -> dict[str, Any]:
    model_defs = model_contracts()
    migrations = tuple(
        {
            "path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql",
            "operation": "create_owned_table",
            "table": item["table"],
            "backend_allowlist": CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS,
        }
        for item in model_defs
    )
    table_contracts = tuple(
        {
            "table": item["table"],
            "fields": item["fields"],
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
            "description": item["description"],
        }
        for item in model_defs
    )
    return {
        "format": "appgen.cybersecurity-operations-center-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": migrations,
        "models": model_defs,
        "ddl": table_sql_definitions(),
        "datastore_backends": CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS,
        "database_backends": CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": OWNED_TABLES,
    }


def cybersecurity_operations_center_build_service_contract() -> dict[str, Any]:
    return {
        "format": "appgen.cybersecurity-operations-center-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_security_alert",
            "transition_alert",
            "enrich_security_alert",
            "suppress_security_alert",
            "record_security_incident",
            "review_asset_exposure",
            "approve_threat_intel",
            "simulate_playbook_run",
            "create_containment_action",
            "record_response_evidence",
            "create_control_assertion",
            "record_governed_model",
        ),
        "query_methods": (
            "query_workbench",
            "build_workbench_view",
            "build_case_detail",
            "generate_handoff_packet",
            "run_advanced_assessment",
            "parse_document_instruction",
        ),
        "domain_operations": DOMAIN_OPERATIONS,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": APPGEN_EVENT_CONTRACT,
    }


def cybersecurity_operations_center_build_api_contract() -> dict[str, Any]:
    routes = (
        "POST /security-alerts",
        "POST /security-alerts/triage",
        "POST /security-alerts/enrich",
        "POST /security-alerts/suppress",
        "POST /security-incidents",
        "POST /security-incidents/promote",
        "POST /asset-exposures",
        "POST /threat-intels",
        "POST /playbook-runs",
        "POST /containment-actions",
        "POST /response-evidence",
        "GET /cybersecurity-operations-center-workbench",
        "GET /cybersecurity-operations-center/case-detail",
    )
    return {
        "format": "appgen.cybersecurity-operations-center-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": routes,
        "event_contract": APPGEN_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "owned_tables": OWNED_TABLES,
    }


def cybersecurity_operations_center_build_release_evidence() -> dict[str, Any]:
    schema = cybersecurity_operations_center_build_schema_contract()
    service = cybersecurity_operations_center_build_service_contract()
    api = cybersecurity_operations_center_build_api_contract()
    smoke = cybersecurity_operations_center_runtime_smoke()
    soc_control = improve1_soc_control_contract()
    checks = (
        {"id": "pbc_source_artifact_contract", "ok": schema["ok"] and service["ok"] and api["ok"]},
        {"id": "pbc_implementation_release_audit", "ok": smoke["ok"]},
        {"id": "pbc_generation_smoke_audit", "ok": smoke["ok"] and smoke["generated_app"]["ok"]},
        {"id": "alert_lifecycle", "ok": smoke["checks_by_id"]["transition_alert"]},
        {"id": "incident_promotion", "ok": smoke["checks_by_id"]["record_security_incident"]},
        {"id": "evidence_custody", "ok": smoke["checks_by_id"]["record_response_evidence"]},
        {"id": "playbook_breakpoints", "ok": smoke["checks_by_id"]["simulate_playbook_run"]},
        {"id": "soc_improve1_controls", "ok": soc_control["ok"]},
    )
    return {
        "format": "appgen.cybersecurity-operations-center-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "schema": schema,
            "service": service,
            "api": api,
            "events": {
                "contract": APPGEN_EVENT_CONTRACT,
                "emits": CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES,
                "consumes": CYBERSECURITY_OPERATIONS_CENTER_CONSUMED_EVENT_TYPES,
            },
            "workbench_views": DOMAIN_WORKBENCH_VIEWS,
            "ui": CYBERSECURITY_OPERATIONS_CENTER_UI_FRAGMENT_KEYS,
            "soc_improve1_controls": soc_control,
        },
        "blocking_gaps": tuple(check["id"] for check in checks if not check["ok"]),
    }


def cybersecurity_operations_center_permissions_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": {
            "operator": ("cybersecurity_operations_center.read", "cybersecurity_operations_center.create", "cybersecurity_operations_center.update"),
            "approver": ("cybersecurity_operations_center.read", "cybersecurity_operations_center.approve"),
            "auditor": ("cybersecurity_operations_center.read",),
            "admin": PERMISSIONS,
        },
        "side_effects": (),
    }


def cybersecurity_operations_center_build_workbench_view(
    state: dict[str, Any],
    tenant: str = "default",
) -> dict[str, Any]:
    alerts = [record for record in _table(state, ALERT_TABLE).values() if record["tenant"] == tenant]
    incidents = [record for record in _table(state, INCIDENT_TABLE).values() if record["tenant"] == tenant]
    evidence = [record for record in _table(state, EVIDENCE_TABLE).values() if record["tenant"] == tenant]
    lanes = {
        "urgent": tuple(alert for alert in alerts if alert["lane"] == "urgent"),
        "backlog": tuple(alert for alert in alerts if alert["lane"] == "backlog"),
        "watchlist": tuple(alert for alert in alerts if alert["lane"] == "watchlist"),
        "suppressed": tuple(alert for alert in alerts if alert["lane"] == "suppressed"),
    }
    supervisor = {
        "assignment_load": tuple(
            {"assignee": assignee or "unassigned", "count": sum(1 for alert in alerts if alert.get("assignee") == assignee)}
            for assignee in {alert.get("assignee") for alert in alerts}
        ),
        "overdue_triage": tuple(alert["id"] for alert in alerts if alert["status"] == "new" and alert["severity"] in {"high", "critical"}),
    }
    evidence_review = tuple(record for record in evidence if record["redaction_status"] != "ready_for_release")
    metrics = _compute_metrics(state, tenant)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "ui_fragments": CYBERSECURITY_OPERATIONS_CENTER_UI_FRAGMENT_KEYS,
        "lanes": lanes,
        "incident_cards": tuple(incidents),
        "supervisor_lane": supervisor,
        "evidence_review_lane": evidence_review,
        "metrics": metrics,
        "forms": (
            "alert_intake_form",
            "incident_promotion_form",
            "evidence_request_form",
            "containment_approval_form",
        ),
        "wizards": (
            "alert_triage_wizard",
            "incident_promotion_wizard",
            "playbook_run_wizard",
            "shift_handoff_wizard",
        ),
        "controls": (
            "severity_lane_filter",
            "confidence_slider",
            "suppression_review_queue",
            "event_lineage_panel",
        ),
        "side_effects": (),
    }


def cybersecurity_operations_center_build_case_detail(
    state: dict[str, Any],
    case_id: str,
) -> dict[str, Any]:
    detail = _build_case_detail(state, case_id)
    detail["side_effects"] = ()
    return detail


def cybersecurity_operations_center_verify_owned_table_boundary(references: tuple[str, ...] = ()) -> dict[str, Any]:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": OWNED_TABLES,
        "shared_table_access": False,
    }


def cybersecurity_operations_center_runtime_capabilities() -> dict[str, Any]:
    domain = domain_depth_contract()
    smoke = cybersecurity_operations_center_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "command_security_alert",
        "transition_alert",
        "enrich_security_alert",
        "suppress_security_alert",
        "record_security_incident",
        "review_asset_exposure",
        "approve_threat_intel",
        "simulate_playbook_run",
        "create_containment_action",
        "record_response_evidence",
        "create_control_assertion",
        "record_governed_model",
        "query_workbench",
        "build_workbench_view",
        "build_case_detail",
        "generate_handoff_packet",
        "run_advanced_assessment",
        "parse_document_instruction",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "improve1_soc_control_contract",
    )
    return {
        "format": "appgen.cybersecurity-operations-center-runtime-capabilities.v2",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": OWNED_TABLES,
        "allowed_database_backends": CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS,
        "standard_features": CYBERSECURITY_OPERATIONS_CENTER_STANDARD_FEATURE_KEYS,
        "capabilities": CYBERSECURITY_OPERATIONS_CENTER_RUNTIME_CAPABILITY_KEYS,
        "improve1_soc_control_capabilities": tuple(capability.slug for capability in SOC_CONTROL_CAPABILITIES),
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS,
        "event_contract": APPGEN_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def cybersecurity_operations_center_runtime_smoke() -> dict[str, Any]:
    state = cybersecurity_operations_center_empty_state()
    cfg = cybersecurity_operations_center_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
        },
    )
    param = cybersecurity_operations_center_set_parameter(cfg["state"], "workbench_limit", 80, actor="ops-lead")
    rule = cybersecurity_operations_center_register_rule(
        param["state"],
        {"rule_name": "security_alert_policy", "policy": {"dedup_window_hours": 6}},
        actor="ops-lead",
    )
    alert_create = cybersecurity_operations_center_command_security_alert(
        rule["state"],
        {
            "tenant": "tenant-smoke",
            "code": "ALERT-001",
            "severity": "critical",
            "confidence": 0.92,
            "asset_ref": "srv-prod-01",
            "principal_ref": "alice",
            "indicator_value": "198.51.100.4",
            "actor": "sensor",
            "detection_context": {
                "source_event_id": "evt-001",
                "detection_timestamp": utc_now(),
                "detection_rule_id": "sigma-001",
                "evidence_checksum": "sha256:abc",
            },
        },
    )
    alert = alert_create["created"][0]
    enrich = cybersecurity_operations_center_enrich_security_alert(alert_create["state"], alert["id"], {"asset_criticality": "critical"}, actor="analyst")
    triage = cybersecurity_operations_center_transition_alert(enrich["state"], alert["id"], "triaged", actor="analyst", reason="Validated malicious behavior")
    incident = cybersecurity_operations_center_record_security_incident(
        triage["state"],
        {
            "tenant": "tenant-smoke",
            "alert_ids": [alert["id"]],
            "asset_criticality": "critical",
            "containment_required": True,
            "commander": "soc-lead",
            "title": "Critical host compromise",
            "actor": "analyst",
        },
    )
    evidence = cybersecurity_operations_center_record_response_evidence(
        incident["state"],
        {
            "tenant": "tenant-smoke",
            "case_id": incident["record"]["id"],
            "source_system": "edr",
            "storage_reference": "vault://evidence/1",
            "actor": "analyst",
        },
    )
    containment = cybersecurity_operations_center_create_containment_action(
        evidence["state"],
        {
            "tenant": "tenant-smoke",
            "incident_id": incident["record"]["id"],
            "action_type": "host_isolation",
            "approved_by": "supervisor",
            "actor": "analyst",
        },
    )
    playbook = cybersecurity_operations_center_simulate_playbook_run(
        containment["state"],
        {
            "tenant": "tenant-smoke",
            "template_name": "host-isolation",
            "stage": "analyst_approval",
            "related_incident_id": incident["record"]["id"],
        },
    )
    consumed = cybersecurity_operations_center_receive_event(
        playbook["state"],
        {
            "tenant": "tenant-smoke",
            "event_type": "AuditEventSealed",
            "idempotency_key": "smoke-seal",
            "payload": {"evidence_id": evidence["record"]["id"], "sealed_bundle_id": "bundle-smoke"},
        },
    )
    workbench = cybersecurity_operations_center_build_workbench_view(consumed["state"], tenant="tenant-smoke")
    detail = cybersecurity_operations_center_build_case_detail(consumed["state"], incident["record"]["id"])
    handoff = cybersecurity_operations_center_generate_handoff_packet(consumed["state"], tenant="tenant-smoke")
    assessment = cybersecurity_operations_center_run_advanced_assessment(consumed["state"], {"tenant": "tenant-smoke"})
    soc_control = improve1_soc_control_contract()
    generated_app = {
        "ok": workbench["ok"] and detail["ok"] and handoff["ok"],
        "workbench": workbench["route"],
        "detail_case_type": detail["case_type"],
    }
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "command_security_alert", "ok": alert_create["ok"]},
        {"id": "enrich_security_alert", "ok": enrich["ok"]},
        {"id": "transition_alert", "ok": triage["ok"]},
        {"id": "record_security_incident", "ok": incident["ok"]},
        {"id": "record_response_evidence", "ok": evidence["ok"]},
        {"id": "create_containment_action", "ok": containment["ok"]},
        {"id": "simulate_playbook_run", "ok": playbook["ok"]},
        {"id": "receive_event", "ok": consumed["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "build_case_detail", "ok": detail["ok"]},
        {"id": "generate_handoff_packet", "ok": handoff["ok"]},
        {"id": "run_advanced_assessment", "ok": assessment["ok"]},
        {"id": "improve1_soc_control_contract", "ok": soc_control["ok"]},
    )
    return {
        "format": "appgen.cybersecurity-operations-center-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "checks_by_id": {check["id"]: check["ok"] for check in checks},
        "configuration": cfg,
        "generated_app": generated_app,
        "workbench": workbench,
        "detail": detail,
        "handoff": handoff,
        "assessment": assessment,
        "soc_control": soc_control,
        "side_effects": (),
    }
