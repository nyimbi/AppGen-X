"""Executable runtime and standalone state engine for the energy_grid_operations PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib

from .energy_grid_control import ENERGY_GRID_CONTROL_CAPABILITIES, improve1_energy_grid_control_contract

PBC_KEY = "energy_grid_operations"
PBC_LABEL = "Energy Grid Operations"
ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC = "pbc.energy_grid_operations.events"
ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES = (
    "EnergyGridOperationsCreated",
    "EnergyGridOperationsUpdated",
    "EnergyGridOperationsApproved",
    "EnergyGridOperationsExceptionOpened",
)
ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
ENERGY_GRID_OPERATIONS_STANDARD_FEATURE_KEYS = (
    "grid_asset_management",
    "energy_grid_operations_workflow",
    "energy_grid_operations_analytics",
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
    "standalone_one_pbc_app",
)
ENERGY_GRID_OPERATIONS_RUNTIME_CAPABILITY_KEYS = (
    "energy_grid_operations_event_sourced_operational_history",
    "energy_grid_operations_multi_tenant_policy_isolation",
    "energy_grid_operations_schema_evolution_resilience",
    "energy_grid_operations_autonomous_anomaly_detection",
    "energy_grid_operations_semantic_document_instruction_understanding",
    "energy_grid_operations_predictive_risk_scoring",
    "energy_grid_operations_counterfactual_scenario_simulation",
    "energy_grid_operations_cryptographic_audit_proofs",
    "energy_grid_operations_continuous_control_testing",
    "energy_grid_operations_carbon_and_sustainability_awareness",
    "energy_grid_operations_cross_pbc_event_federation",
    "energy_grid_operations_governed_ai_agent_execution",
)
ENERGY_GRID_OPERATIONS_UI_FRAGMENT_KEYS = (
    "EnergyGridOperationsWorkbench",
    "EnergyGridOperationsSwitchingWorkbench",
    "EnergyGridOperationsOutageWorkbench",
    "EnergyGridOperationsGovernanceWorkbench",
    "EnergyGridOperationsAssistantPanel",
)
GRID_ASSET_TYPES = (
    "substation",
    "feeder",
    "breaker",
    "recloser",
    "switch",
    "transformer",
    "regulator",
    "capacitor_bank",
    "der_intertie",
    "mobile_substation",
)
SWITCH_ACTIONS = ("open", "close", "verify", "ground", "tag", "test")
DISPATCH_OBJECTIVE_TYPES = (
    "load_relief",
    "voltage_support",
    "der_curtailment",
    "restoration_support",
)
CONSTRAINT_TYPES = (
    "thermal",
    "voltage",
    "crew_safety",
    "switching_window",
    "stability",
)

BUSINESS_TABLE_SPECS = (
    {
        "entity": "grid_asset",
        "table": "energy_grid_operations_grid_asset",
        "id_key": "asset_id",
        "fields": (
            "asset_id",
            "tenant",
            "asset_type",
            "asset_name",
            "voltage_kv",
            "parent_asset_id",
            "substation_id",
            "feeder_id",
            "normal_state",
            "phases",
            "protection_zone",
            "gis_reference",
            "scada_points",
            "quality_score",
            "status",
            "version",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Utility asset hierarchy for substations, feeders, breakers, reclosers, and DER interties.",
    },
    {
        "entity": "load_forecast",
        "table": "energy_grid_operations_load_forecast",
        "id_key": "forecast_id",
        "fields": (
            "forecast_id",
            "tenant",
            "feeder_id",
            "horizon_hours",
            "forecast_mw",
            "peak_mw",
            "confidence",
            "weather_scenario",
            "risk_band",
            "status",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Feeder and substation demand forecasts with operational confidence and weather context.",
    },
    {
        "entity": "switching_order",
        "table": "energy_grid_operations_switching_order",
        "id_key": "switching_order_id",
        "fields": (
            "switching_order_id",
            "tenant",
            "feeder_id",
            "substation_id",
            "clearance_id",
            "hold_points",
            "step_count",
            "simulation_status",
            "simulation_findings",
            "status",
            "requested_by",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Ordered switching plans with hold points, clearance evidence, and pre-execution simulation findings.",
    },
    {
        "entity": "dispatch_instruction",
        "table": "energy_grid_operations_dispatch_instruction",
        "id_key": "dispatch_instruction_id",
        "fields": (
            "dispatch_instruction_id",
            "tenant",
            "objective_type",
            "feeder_id",
            "target_asset_id",
            "expected_load_shift_mw",
            "telemetry_freshness_seconds",
            "conflicts",
            "rollback_conditions",
            "status",
            "approved_by",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Constraint-aware dispatch instructions for load relief, voltage support, DER control, and restoration support.",
    },
    {
        "entity": "outage_event",
        "table": "energy_grid_operations_outage_event",
        "id_key": "outage_event_id",
        "fields": (
            "outage_event_id",
            "tenant",
            "feeder_id",
            "substation_id",
            "cause",
            "affected_customers",
            "restoration_priority",
            "eta_minutes",
            "crew_status",
            "status",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Outage events with restoration priority, ETA, crew status, and workbench impact.",
    },
    {
        "entity": "reliability_constraint",
        "table": "energy_grid_operations_reliability_constraint",
        "id_key": "constraint_id",
        "fields": (
            "constraint_id",
            "tenant",
            "constraint_type",
            "scope_id",
            "scope_level",
            "severity",
            "limit_value",
            "status",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Reliability, thermal, voltage, switching window, and crew-safety constraints used during dispatch and restoration.",
    },
    {
        "entity": "grid_topology",
        "table": "energy_grid_operations_grid_topology",
        "id_key": "topology_id",
        "fields": (
            "topology_id",
            "tenant",
            "feeder_id",
            "source_asset_id",
            "segment_count",
            "normally_open_ties",
            "backfeed_paths",
            "phase_map",
            "status",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Phase-aware feeder topology projections for normal and contingency switching analysis.",
    },
    {
        "entity": "energy_grid_operations_policy_rule",
        "table": "energy_grid_operations_energy_grid_operations_policy_rule",
        "id_key": "rule_id",
        "fields": (
            "rule_id",
            "tenant",
            "scope",
            "policy_version",
            "compiled_hash",
            "required_approver_role",
            "status",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Policy rules that govern switching approval, dispatch authority, and restoration overrides.",
    },
    {
        "entity": "energy_grid_operations_runtime_parameter",
        "table": "energy_grid_operations_energy_grid_operations_runtime_parameter",
        "id_key": "parameter_name",
        "fields": (
            "parameter_name",
            "tenant",
            "value",
            "datatype",
            "minimum",
            "maximum",
            "status",
            "approved_by",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Bounded runtime parameters that control horizon, workbench limits, and risk tolerances.",
    },
    {
        "entity": "energy_grid_operations_schema_extension",
        "table": "energy_grid_operations_energy_grid_operations_schema_extension",
        "id_key": "extension_id",
        "fields": (
            "extension_id",
            "tenant",
            "target_table",
            "new_fields",
            "compatibility_result",
            "status",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Schema extension proposals for new field equipment classes and telemetry attributes.",
    },
    {
        "entity": "energy_grid_operations_control_assertion",
        "table": "energy_grid_operations_energy_grid_operations_control_assertion",
        "id_key": "assertion_id",
        "fields": (
            "assertion_id",
            "tenant",
            "control_name",
            "scope_id",
            "assertion_status",
            "evidence_summary",
            "review_required",
            "status",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Operational and release controls proving safe switching, restoration, and approval evidence.",
    },
    {
        "entity": "energy_grid_operations_governed_model",
        "table": "energy_grid_operations_energy_grid_operations_governed_model",
        "id_key": "model_id",
        "fields": (
            "model_id",
            "tenant",
            "model_kind",
            "approval_scope",
            "training_boundary",
            "deployment_status",
            "status",
            "created_at",
            "updated_at",
            "payload",
        ),
        "description": "Governed models and agents used to score risk or assist grid operators with bounded actions.",
    },
)
EVENT_TABLE_SPECS = (
    {
        "entity": "appgen_outbox_event",
        "table": "energy_grid_operations_appgen_outbox_event",
        "id_key": "event_id",
        "fields": ("event_id", "tenant", "event_type", "topic", "idempotency_key", "occurred_at", "payload"),
        "description": "AppGen-X outbox events emitted by owned commands.",
    },
    {
        "entity": "appgen_inbox_event",
        "table": "energy_grid_operations_appgen_inbox_event",
        "id_key": "event_id",
        "fields": ("event_id", "tenant", "event_type", "source_pbc", "idempotency_key", "occurred_at", "payload"),
        "description": "AppGen-X inbox events consumed by this PBC.",
    },
    {
        "entity": "appgen_dead_letter_event",
        "table": "energy_grid_operations_appgen_dead_letter_event",
        "id_key": "event_id",
        "fields": ("event_id", "tenant", "event_type", "reason", "idempotency_key", "occurred_at", "payload"),
        "description": "Dead-letter evidence for exhausted or unknown consumed events.",
    },
)

ENERGY_GRID_OPERATIONS_BUSINESS_TABLES = tuple(spec["table"] for spec in BUSINESS_TABLE_SPECS)
ENERGY_GRID_OPERATIONS_OWNED_TABLES = ENERGY_GRID_OPERATIONS_BUSINESS_TABLES + tuple(
    spec["table"] for spec in EVENT_TABLE_SPECS
)
ENERGY_GRID_OPERATIONS_RUNTIME_TABLES = ENERGY_GRID_OPERATIONS_OWNED_TABLES
ENTITY_TO_TABLE = {spec["entity"]: spec["table"] for spec in BUSINESS_TABLE_SPECS + EVENT_TABLE_SPECS}
ENTITY_SPECS = {spec["entity"]: spec for spec in BUSINESS_TABLE_SPECS + EVENT_TABLE_SPECS}

PARAMETER_DEFINITIONS = (
    {
        "name": "quality_score_floor",
        "datatype": "float",
        "default": 0.72,
        "minimum": 0.0,
        "maximum": 1.0,
        "description": "Minimum acceptable asset data quality score before the workbench permits energization-sensitive workflows.",
    },
    {
        "name": "materiality_threshold",
        "datatype": "float",
        "default": 8.0,
        "minimum": 0.0,
        "maximum": 500.0,
        "description": "MW change or customer impact threshold that triggers supervisory review.",
    },
    {
        "name": "approval_sla_hours",
        "datatype": "integer",
        "default": 4,
        "minimum": 1,
        "maximum": 72,
        "description": "Maximum time to hold high-risk approvals before escalation.",
    },
    {
        "name": "risk_threshold",
        "datatype": "float",
        "default": 0.68,
        "minimum": 0.0,
        "maximum": 1.0,
        "description": "Risk threshold above which switching and dispatch requests open operator exceptions.",
    },
    {
        "name": "forecast_horizon_days",
        "datatype": "integer",
        "default": 7,
        "minimum": 1,
        "maximum": 30,
        "description": "Maximum planning horizon for packaged load forecasts.",
    },
    {
        "name": "workbench_limit",
        "datatype": "integer",
        "default": 25,
        "minimum": 5,
        "maximum": 250,
        "description": "Maximum queue and table rows shown in the standalone workbench.",
    },
)
RULE_DEFINITIONS = (
    {
        "rule_id": "grid_asset_policy",
        "scope": "asset_quality",
        "required_fields": ("asset_id", "tenant", "asset_type", "feeder_id", "substation_id", "voltage_kv", "normal_state"),
        "required_approver_role": "grid_supervisor",
    },
    {
        "rule_id": "load_forecast_policy",
        "scope": "forecast_confidence",
        "required_fields": ("forecast_id", "tenant", "feeder_id", "forecast_mw", "peak_mw", "confidence"),
        "required_approver_role": "dispatch_supervisor",
    },
    {
        "rule_id": "switching_order_policy",
        "scope": "switching_safety",
        "required_fields": ("switching_order_id", "tenant", "feeder_id", "steps", "clearance_id"),
        "required_approver_role": "control_room_supervisor",
    },
    {
        "rule_id": "dispatch_instruction_policy",
        "scope": "dispatch_conflict_check",
        "required_fields": ("dispatch_instruction_id", "tenant", "objective_type", "feeder_id", "target_asset_id"),
        "required_approver_role": "system_dispatcher",
    },
    {
        "rule_id": "outage_event_policy",
        "scope": "restoration_priority",
        "required_fields": ("outage_event_id", "tenant", "feeder_id", "cause", "affected_customers"),
        "required_approver_role": "restoration_lead",
    },
    {
        "rule_id": "reliability_constraint_policy",
        "scope": "constraint_activation",
        "required_fields": ("constraint_id", "tenant", "constraint_type", "scope_id", "severity", "limit_value"),
        "required_approver_role": "reliability_engineer",
    },
)
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy_version": "grid-policy-2026.05",
    "simulation_depth": "phase_aware",
    "storm_mode_enabled": False,
    "tenant_isolation": "strict",
}
PERMISSION_MAP = {
    "view_workbench": "energy_grid_operations.read",
    "create_grid_asset": "energy_grid_operations.create",
    "record_load_forecast": "energy_grid_operations.create",
    "review_switching_order": "energy_grid_operations.update",
    "approve_dispatch_instruction": "energy_grid_operations.approve",
    "simulate_outage_event": "energy_grid_operations.update",
    "create_reliability_constraint": "energy_grid_operations.update",
    "record_grid_topology": "energy_grid_operations.update",
    "review_energy_grid_operations_policy_rule": "energy_grid_operations.admin",
    "approve_energy_grid_operations_runtime_parameter": "energy_grid_operations.admin",
    "simulate_energy_grid_operations_schema_extension": "energy_grid_operations.admin",
    "create_energy_grid_operations_control_assertion": "energy_grid_operations.approve",
    "record_energy_grid_operations_governed_model": "energy_grid_operations.admin",
    "receive_event": "energy_grid_operations.admin",
    "configure_runtime": "energy_grid_operations.admin",
}
DOMAIN_OPERATIONS = (
    "create_grid_asset",
    "record_load_forecast",
    "review_switching_order",
    "approve_dispatch_instruction",
    "simulate_outage_event",
    "create_reliability_constraint",
    "record_grid_topology",
    "review_energy_grid_operations_policy_rule",
    "approve_energy_grid_operations_runtime_parameter",
    "simulate_energy_grid_operations_schema_extension",
    "create_energy_grid_operations_control_assertion",
    "record_energy_grid_operations_governed_model",
)
SUPPORT_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "receive_event",
)
QUERY_OPERATIONS = (
    "build_workbench_view",
    "query_timeline",
)
OPERATION_ENTITY_MAP = {
    "create_grid_asset": "grid_asset",
    "record_load_forecast": "load_forecast",
    "review_switching_order": "switching_order",
    "approve_dispatch_instruction": "dispatch_instruction",
    "simulate_outage_event": "outage_event",
    "create_reliability_constraint": "reliability_constraint",
    "record_grid_topology": "grid_topology",
    "review_energy_grid_operations_policy_rule": "energy_grid_operations_policy_rule",
    "approve_energy_grid_operations_runtime_parameter": "energy_grid_operations_runtime_parameter",
    "simulate_energy_grid_operations_schema_extension": "energy_grid_operations_schema_extension",
    "create_energy_grid_operations_control_assertion": "energy_grid_operations_control_assertion",
    "record_energy_grid_operations_governed_model": "energy_grid_operations_governed_model",
}
OPERATION_EVENT_MAP = {
    "create_grid_asset": "EnergyGridOperationsCreated",
    "record_load_forecast": "EnergyGridOperationsUpdated",
    "review_switching_order": "EnergyGridOperationsUpdated",
    "approve_dispatch_instruction": "EnergyGridOperationsApproved",
    "simulate_outage_event": "EnergyGridOperationsUpdated",
    "create_reliability_constraint": "EnergyGridOperationsCreated",
    "record_grid_topology": "EnergyGridOperationsUpdated",
    "review_energy_grid_operations_policy_rule": "EnergyGridOperationsUpdated",
    "approve_energy_grid_operations_runtime_parameter": "EnergyGridOperationsApproved",
    "simulate_energy_grid_operations_schema_extension": "EnergyGridOperationsUpdated",
    "create_energy_grid_operations_control_assertion": "EnergyGridOperationsUpdated",
    "record_energy_grid_operations_governed_model": "EnergyGridOperationsApproved",
}


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _copy_state(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _stamp(state: dict) -> str:
    state["clock"] = int(state.get("clock", 0)) + 1
    minute, second = divmod(state["clock"], 60)
    return f"2026-05-29T00:{minute:02d}:{second:02d}Z"


def _entity_spec(entity: str) -> dict:
    return ENTITY_SPECS[entity]


def _parameter_definition(name: str) -> dict | None:
    return next((item for item in PARAMETER_DEFINITIONS if item["name"] == name), None)


def _rule_definition(rule_id: str) -> dict | None:
    return next((item for item in RULE_DEFINITIONS if item["rule_id"] == rule_id), None)


def _required(payload: dict, fields: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(field for field in fields if payload.get(field) in (None, "", (), []))


def _compile_rule(rule: dict) -> dict:
    required = tuple(rule.get("required_fields", ()))
    compiled_hash = _digest((rule.get("rule_id"), rule.get("scope"), required))
    return {
        "rule_id": rule.get("rule_id"),
        "scope": rule.get("scope", "domain"),
        "required_fields": required,
        "required_approver_role": rule.get("required_approver_role", "grid_supervisor"),
        "status": rule.get("status", "active"),
        "compiled_hash": compiled_hash,
        "event_contract": "AppGen-X",
    }


def _default_rules() -> dict:
    return {rule["rule_id"]: _compile_rule(rule) for rule in RULE_DEFINITIONS}


def _parameter_state(definition: dict, value: object | None = None, tenant: str = "tenant_demo") -> dict:
    return {
        "name": definition["name"],
        "tenant": tenant,
        "value": definition["default"] if value is None else value,
        "datatype": definition["datatype"],
        "minimum": definition["minimum"],
        "maximum": definition["maximum"],
        "status": "approved",
    }


def _default_parameters() -> dict:
    return {item["name"]: _parameter_state(item) for item in PARAMETER_DEFINITIONS}


def energy_grid_operations_empty_state() -> dict:
    return {
        "clock": 0,
        "configuration": dict(DEFAULT_CONFIGURATION),
        "parameters": _default_parameters(),
        "rules": _default_rules(),
        "records": {spec["entity"]: {} for spec in BUSINESS_TABLE_SPECS},
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
        "audit_log": [],
        "workbench_notes": [],
    }


def _tenant_records(state: dict, entity: str, tenant: str | None = None) -> tuple[dict, ...]:
    records = tuple(state.get("records", {}).get(entity, {}).values())
    if tenant is None:
        return records
    return tuple(record for record in records if record.get("tenant") == tenant)


def _store_record(
    state: dict,
    entity: str,
    payload: dict,
    *,
    status: str,
    summary: str,
    extra: dict | None = None,
) -> tuple[dict, dict]:
    spec = _entity_spec(entity)
    next_state = _copy_state(state)
    timestamp = _stamp(next_state)
    record_id = payload.get(spec["id_key"]) or payload.get("id") or _digest((entity, payload))[:12]
    existing = next_state["records"][entity].get(record_id)
    version = int(existing["version"] + 1) if existing else 1
    record = {
        spec["id_key"]: record_id,
        "id": record_id,
        "entity": entity,
        "table": spec["table"],
        "tenant": payload.get("tenant", "tenant_demo"),
        "code": payload.get("code", record_id),
        "status": status,
        "version": version,
        "summary": summary,
        "created_at": existing["created_at"] if existing else timestamp,
        "updated_at": timestamp,
        "payload": dict(payload),
    }
    if extra:
        record.update(extra)
    next_state["records"][entity][record_id] = record
    next_state["audit_log"].append(
        {
            "timestamp": timestamp,
            "entity": entity,
            "record_id": record_id,
            "status": status,
            "summary": summary,
        }
    )
    return next_state, record


def _emit_event(state: dict, event_type: str, operation: str, record: dict) -> dict:
    event = {
        "event_id": _digest((event_type, operation, record.get("id"), record.get("version")))[:20],
        "event_type": event_type,
        "topic": ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "pbc": PBC_KEY,
        "operation": operation,
        "tenant": record.get("tenant"),
        "entity": record.get("entity"),
        "record_id": record.get("id"),
        "idempotency_key": _digest((record.get("entity"), record.get("id"), operation)),
        "occurred_at": _stamp(state),
        "payload": {
            "summary": record.get("summary"),
            "status": record.get("status"),
            "table": record.get("table"),
        },
    }
    state["outbox"].append(event)
    return event


def _parameter_value(state: dict, name: str) -> object:
    return state.get("parameters", {}).get(name, {}).get("value")


def _rule_result(rule_id: str, payload: dict) -> dict:
    rule = _rule_definition(rule_id)
    required = tuple(rule.get("required_fields", ())) if rule else ()
    missing = _required(payload, required)
    return {
        "rule_id": rule_id,
        "required_fields": required,
        "missing_fields": missing,
        "passed": not missing,
    }


def _quality_score(payload: dict) -> float:
    optional_fields = ("gis_reference", "scada_points", "protection_zone", "phases")
    present = sum(1 for field in optional_fields if payload.get(field))
    return round(min(1.0, 0.68 + (present * 0.08)), 2)


def _active_constraints(state: dict, tenant: str, feeder_id: str | None = None) -> tuple[dict, ...]:
    constraints = [
        record
        for record in _tenant_records(state, "reliability_constraint", tenant)
        if record.get("status") == "active"
    ]
    if feeder_id:
        constraints = [
            item
            for item in constraints
            if item.get("scope_id") in {feeder_id, item.get("payload", {}).get("substation_id")}
        ]
    return tuple(constraints)


def _switching_simulation(state: dict, payload: dict) -> dict:
    issues: list[str] = []
    steps = tuple(payload.get("steps", ()))
    tenant = payload.get("tenant", "tenant_demo")
    feeder_id = payload.get("feeder_id")
    missing_topology = not any(
        topology.get("feeder_id") == feeder_id
        for topology in _tenant_records(state, "grid_topology", tenant)
    )
    if missing_topology:
        issues.append("missing_topology")
    if not steps:
        issues.append("missing_steps")
    if steps and not any(step.get("hold_point") for step in steps):
        issues.append("missing_hold_point")
    if steps and not any(step.get("action") == "open" for step in steps):
        issues.append("missing_open_step")
    opened = False
    for step in steps:
        action = step.get("action")
        if action not in SWITCH_ACTIONS:
            issues.append(f"invalid_action:{action}")
        if action == "close" and not opened:
            issues.append("close_before_isolation")
        if action == "open":
            opened = True
    if payload.get("creates_backfeed"):
        issues.append("backfeed_risk")
    findings = tuple(dict.fromkeys(issues))
    hold_points = tuple(step.get("description", f"step-{index + 1}") for index, step in enumerate(steps) if step.get("hold_point"))
    return {
        "ok": not findings,
        "hold_points": hold_points,
        "step_count": len(steps),
        "simulation_findings": findings,
        "simulation_status": "clear" if not findings else "blocked",
        "impacted_feeders": (feeder_id,) if feeder_id else (),
        "constraint_count": len(_active_constraints(state, tenant, feeder_id)),
    }


def _dispatch_conflicts(state: dict, payload: dict) -> tuple[str, ...]:
    conflicts: list[str] = []
    tenant = payload.get("tenant", "tenant_demo")
    feeder_id = payload.get("feeder_id")
    if payload.get("objective_type") not in DISPATCH_OBJECTIVE_TYPES:
        conflicts.append("unsupported_objective")
    telemetry_age = int(payload.get("telemetry_freshness_seconds", 0))
    if telemetry_age > 300:
        conflicts.append("stale_telemetry")
    expected_shift = float(payload.get("expected_load_shift_mw", 0.0))
    if expected_shift > float(_parameter_value(state, "materiality_threshold") or 0.0):
        conflicts.append("materiality_threshold_exceeded")
    switching_orders = [
        record
        for record in _tenant_records(state, "switching_order", tenant)
        if record.get("feeder_id") == feeder_id and record.get("status") in {"ready_for_dispatch", "execution_hold"}
    ]
    if switching_orders:
        conflicts.append("switching_window_conflict")
    if any(item.get("severity") in {"high", "critical"} for item in _active_constraints(state, tenant, feeder_id)):
        conflicts.append("active_reliability_constraint")
    return tuple(dict.fromkeys(conflicts))


def _workbench_cards(view: dict) -> tuple[dict, ...]:
    return (
        {"key": "assets", "label": "Assets", "value": view["asset_count"]},
        {"key": "switching", "label": "Switching Orders", "value": view["switching_order_count"]},
        {"key": "dispatch", "label": "Dispatch Instructions", "value": view["dispatch_instruction_count"]},
        {"key": "outages", "label": "Active Outages", "value": view["active_outage_count"]},
        {"key": "constraints", "label": "Active Constraints", "value": view["active_constraint_count"]},
        {"key": "exceptions", "label": "Exceptions", "value": view["exception_count"]},
        {"key": "events", "label": "Events", "value": view["outbox_count"] + view["inbox_count"]},
    )


def energy_grid_operations_operation_preview(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation in QUERY_OPERATIONS:
        return {
            "ok": True,
            "operation": operation,
            "operation_kind": "query",
            "owned_tables": (),
            "read_tables": ENERGY_GRID_OPERATIONS_BUSINESS_TABLES,
            "permission": PERMISSION_MAP.get("view_workbench", f"{PBC_KEY}.read"),
            "event_contract": "AppGen-X",
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
            "side_effects": (),
        }
    entity = OPERATION_ENTITY_MAP.get(operation)
    if operation in SUPPORT_OPERATIONS:
        entity = entity or "energy_grid_operations_runtime_parameter"
    if entity is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation, "side_effects": ()}
    event_type = OPERATION_EVENT_MAP.get(operation, ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES[1])
    rule_ids = tuple(
        rule["rule_id"]
        for rule in RULE_DEFINITIONS
        if rule["scope"].split("_")[0] in operation
    )
    return {
        "ok": True,
        "operation": operation,
        "operation_kind": "command",
        "owned_tables": (_entity_spec(entity)["table"], ENTITY_TO_TABLE["appgen_outbox_event"]),
        "read_tables": (),
        "permission": PERMISSION_MAP.get(operation, f"{PBC_KEY}.admin"),
        "emitted_event": event_type,
        "rule_ids": rule_ids,
        "parameter_names": tuple(item["name"] for item in PARAMETER_DEFINITIONS[:3]),
        "event_contract": "AppGen-X",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "payload_keys": tuple(sorted(payload)),
        "side_effects": (),
    }


def energy_grid_operations_configure_runtime(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    config = dict(DEFAULT_CONFIGURATION)
    config.update(state.get("configuration", {}))
    config.update(payload.get("configuration", payload))
    ok = (
        config.get("database_backend") in ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS
        and config.get("event_topic", ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC) == ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC
    )
    next_state = _copy_state(state)
    next_state["configuration"] = {
        **config,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    next_state["workbench_notes"].append(
        f"runtime-configured:{next_state['configuration']['database_backend']}:{next_state['configuration']['default_policy_version']}"
    )
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def energy_grid_operations_set_parameter(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    name = payload.get("name")
    value = payload.get("value")
    definition = _parameter_definition(name)
    if definition is None:
        return {"ok": False, "state": _copy_state(state), "reason": "unknown_parameter", "name": name, "side_effects": ()}
    next_state = _copy_state(state)
    if value is None or value < definition["minimum"] or value > definition["maximum"]:
        return {
            "ok": False,
            "state": next_state,
            "reason": "parameter_out_of_bounds",
            "name": name,
            "allowed_range": (definition["minimum"], definition["maximum"]),
            "side_effects": (),
        }
    next_state["parameters"][name] = _parameter_state(definition, value=value, tenant=payload.get("tenant", "tenant_demo"))
    return {"ok": True, "state": next_state, "parameter": next_state["parameters"][name], "side_effects": ()}


def energy_grid_operations_register_rule(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    rule = dict(payload.get("rule", payload))
    rule_id = rule.get("rule_id")
    definition = _rule_definition(rule_id) if rule_id else None
    if definition is None and not rule_id:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_rule_id", "side_effects": ()}
    next_state = _copy_state(state)
    merged = dict(definition or {})
    merged.update(rule)
    compiled = _compile_rule(merged)
    next_state["rules"][compiled["rule_id"]] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def energy_grid_operations_receive_event(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    envelope = dict(payload.get("envelope", payload))
    next_state = _copy_state(state)
    event_type = envelope.get("event_type")
    event_id = envelope.get("event_id") or _digest(envelope)[:20]
    idem = envelope.get("idempotency_key") or _digest((event_type, event_id, envelope.get("payload")))
    if idem in next_state["idempotency_keys"]:
        return {
            "ok": True,
            "duplicate": True,
            "state": next_state,
            "event_id": event_id,
            "idempotency_key": idem,
            "side_effects": (),
        }
    next_state["idempotency_keys"].add(idem)
    inbox_entry = {
        "event_id": event_id,
        "tenant": envelope.get("payload", {}).get("tenant", "tenant_demo"),
        "event_type": event_type,
        "source_pbc": envelope.get("source_pbc", envelope.get("source", "external")),
        "idempotency_key": idem,
        "occurred_at": envelope.get("occurred_at", _stamp(next_state)),
        "payload": dict(envelope.get("payload", {})),
    }
    if event_type not in ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES:
        dead_letter = {
            "event_id": event_id,
            "tenant": inbox_entry["tenant"],
            "event_type": event_type,
            "reason": "unknown_consumed_event",
            "idempotency_key": idem,
            "occurred_at": inbox_entry["occurred_at"],
            "payload": dict(envelope),
        }
        next_state["dead_letter"].append(dead_letter)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": ENTITY_TO_TABLE["appgen_dead_letter_event"],
            "idempotency_key": idem,
            "side_effects": (),
        }
    next_state["inbox"].append(inbox_entry)
    impacts: list[str] = []
    if event_type == "PolicyChanged":
        policy_version = envelope.get("payload", {}).get("policy_version", DEFAULT_CONFIGURATION["default_policy_version"])
        next_state["configuration"]["default_policy_version"] = policy_version
        for entity in ("switching_order", "dispatch_instruction"):
            for record in next_state["records"][entity].values():
                if record.get("status") in {"ready_for_dispatch", "approved"}:
                    record["review_required"] = True
                    impacts.append(record["id"])
    elif event_type == "AuditEventSealed":
        target_record_id = envelope.get("payload", {}).get("record_id")
        seal = envelope.get("payload", {}).get("seal_id", "seal-generated")
        for entity_records in next_state["records"].values():
            if target_record_id in entity_records:
                entity_records[target_record_id]["audit_seal"] = seal
                impacts.append(target_record_id)
                break
    elif event_type == "OperationalKpiChanged":
        updated_threshold = envelope.get("payload", {}).get("risk_threshold")
        if updated_threshold is not None:
            param_result = energy_grid_operations_set_parameter(next_state, {"name": "risk_threshold", "value": updated_threshold})
            next_state = param_result["state"]
            impacts.append("risk_threshold")
    return {
        "ok": True,
        "duplicate": False,
        "state": next_state,
        "inbox_entry": inbox_entry,
        "review_impacts": tuple(impacts),
        "idempotency_key": idem,
        "side_effects": (),
    }


def _finalize_command(
    state: dict,
    *,
    operation: str,
    entity: str,
    record: dict,
    event_type: str,
    rule_ids: tuple[str, ...],
    parameter_names: tuple[str, ...],
    warnings: tuple[str, ...] = (),
    simulation: dict | None = None,
) -> dict:
    event = _emit_event(state, event_type, operation, record)
    workbench = energy_grid_operations_build_workbench_view(state, {"tenant": record.get("tenant")})
    return {
        "ok": True,
        "state": state,
        "operation": operation,
        "operation_kind": "command",
        "target_table": _entity_spec(entity)["table"],
        "owned_tables": (_entity_spec(entity)["table"], ENTITY_TO_TABLE["appgen_outbox_event"]),
        "record": record,
        "event": event,
        "emitted_event": event_type,
        "idempotency_key": event["idempotency_key"],
        "permission": PERMISSION_MAP.get(operation, f"{PBC_KEY}.admin"),
        "rule_decisions": tuple(_rule_result(rule_id, record.get("payload", {})) for rule_id in rule_ids),
        "parameters_read": tuple(
            {"name": name, "value": _parameter_value(state, name)} for name in parameter_names
        ),
        "warnings": warnings,
        "simulation": simulation,
        "workbench": workbench,
        "side_effects": (),
    }


def energy_grid_operations_create_grid_asset(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    missing = _required(payload, _rule_definition("grid_asset_policy")["required_fields"])
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if payload.get("asset_type") not in GRID_ASSET_TYPES:
        return {"ok": False, "state": _copy_state(state), "reason": "invalid_asset_type", "side_effects": ()}
    quality_score = _quality_score(payload)
    status = "active" if quality_score >= float(_parameter_value(state, "quality_score_floor")) else "review_required"
    next_state, record = _store_record(
        state,
        "grid_asset",
        payload,
        status=status,
        summary=f"{payload['asset_type']} {payload.get('asset_name', payload['asset_id'])} on feeder {payload['feeder_id']}",
        extra={
            "asset_type": payload["asset_type"],
            "asset_name": payload.get("asset_name", payload["asset_id"]),
            "voltage_kv": payload["voltage_kv"],
            "parent_asset_id": payload.get("parent_asset_id"),
            "substation_id": payload["substation_id"],
            "feeder_id": payload["feeder_id"],
            "normal_state": payload["normal_state"],
            "phases": tuple(payload.get("phases", ("A", "B", "C"))),
            "protection_zone": payload.get("protection_zone", payload["feeder_id"]),
            "gis_reference": payload.get("gis_reference"),
            "scada_points": tuple(payload.get("scada_points", ())),
            "quality_score": quality_score,
        },
    )
    warnings = ("asset_quality_requires_review",) if status != "active" else ()
    return _finalize_command(
        next_state,
        operation="create_grid_asset",
        entity="grid_asset",
        record=record,
        event_type="EnergyGridOperationsCreated",
        rule_ids=("grid_asset_policy",),
        parameter_names=("quality_score_floor", "workbench_limit"),
        warnings=warnings,
    )


def energy_grid_operations_record_load_forecast(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    missing = _required(payload, _rule_definition("load_forecast_policy")["required_fields"])
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    confidence = float(payload.get("confidence", 0.0))
    risk_band = "watch" if confidence < float(_parameter_value(state, "risk_threshold")) else "stable"
    next_state, record = _store_record(
        state,
        "load_forecast",
        payload,
        status="published",
        summary=f"Forecast {payload['forecast_id']} for feeder {payload['feeder_id']}",
        extra={
            "feeder_id": payload["feeder_id"],
            "horizon_hours": int(payload.get("horizon_hours", 24)),
            "forecast_mw": float(payload["forecast_mw"]),
            "peak_mw": float(payload["peak_mw"]),
            "confidence": confidence,
            "weather_scenario": payload.get("weather_scenario", "normal"),
            "risk_band": risk_band,
        },
    )
    return _finalize_command(
        next_state,
        operation="record_load_forecast",
        entity="load_forecast",
        record=record,
        event_type="EnergyGridOperationsUpdated",
        rule_ids=("load_forecast_policy",),
        parameter_names=("forecast_horizon_days", "risk_threshold"),
    )


def energy_grid_operations_review_switching_order(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    missing = _required(payload, _rule_definition("switching_order_policy")["required_fields"])
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    simulation = _switching_simulation(state, payload)
    status = "ready_for_dispatch" if simulation["ok"] else "blocked"
    event_type = "EnergyGridOperationsUpdated" if simulation["ok"] else "EnergyGridOperationsExceptionOpened"
    next_state, record = _store_record(
        state,
        "switching_order",
        payload,
        status=status,
        summary=f"Switching order {payload['switching_order_id']} for feeder {payload['feeder_id']}",
        extra={
            "feeder_id": payload["feeder_id"],
            "substation_id": payload.get("substation_id"),
            "clearance_id": payload["clearance_id"],
            "hold_points": simulation["hold_points"],
            "step_count": simulation["step_count"],
            "simulation_status": simulation["simulation_status"],
            "simulation_findings": simulation["simulation_findings"],
            "requested_by": payload.get("requested_by", "dispatcher"),
            "review_required": not simulation["ok"],
        },
    )
    return _finalize_command(
        next_state,
        operation="review_switching_order",
        entity="switching_order",
        record=record,
        event_type=event_type,
        rule_ids=("switching_order_policy",),
        parameter_names=("risk_threshold", "approval_sla_hours"),
        warnings=simulation["simulation_findings"],
        simulation=simulation,
    )


def energy_grid_operations_approve_dispatch_instruction(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    missing = _required(payload, _rule_definition("dispatch_instruction_policy")["required_fields"])
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    conflicts = _dispatch_conflicts(state, payload)
    status = "approved" if not conflicts else "blocked"
    event_type = "EnergyGridOperationsApproved" if not conflicts else "EnergyGridOperationsExceptionOpened"
    next_state, record = _store_record(
        state,
        "dispatch_instruction",
        payload,
        status=status,
        summary=f"Dispatch {payload['dispatch_instruction_id']} for feeder {payload['feeder_id']}",
        extra={
            "objective_type": payload["objective_type"],
            "feeder_id": payload["feeder_id"],
            "target_asset_id": payload["target_asset_id"],
            "expected_load_shift_mw": float(payload.get("expected_load_shift_mw", 0.0)),
            "telemetry_freshness_seconds": int(payload.get("telemetry_freshness_seconds", 0)),
            "conflicts": conflicts,
            "rollback_conditions": tuple(payload.get("rollback_conditions", ())),
            "approved_by": payload.get("approved_by", "system_dispatcher"),
        },
    )
    return _finalize_command(
        next_state,
        operation="approve_dispatch_instruction",
        entity="dispatch_instruction",
        record=record,
        event_type=event_type,
        rule_ids=("dispatch_instruction_policy",),
        parameter_names=("materiality_threshold", "risk_threshold"),
        warnings=conflicts,
    )


def energy_grid_operations_simulate_outage_event(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    missing = _required(payload, _rule_definition("outage_event_policy")["required_fields"])
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    affected_customers = int(payload.get("affected_customers", 0))
    restoration_priority = "critical" if affected_customers >= 5000 else "high" if affected_customers >= 1000 else "standard"
    eta_minutes = int(payload.get("eta_minutes", 180 if restoration_priority == "critical" else 90))
    next_state, record = _store_record(
        state,
        "outage_event",
        payload,
        status=payload.get("status", "restoration_in_progress"),
        summary=f"Outage {payload['outage_event_id']} on feeder {payload['feeder_id']}",
        extra={
            "feeder_id": payload["feeder_id"],
            "substation_id": payload.get("substation_id"),
            "cause": payload["cause"],
            "affected_customers": affected_customers,
            "restoration_priority": restoration_priority,
            "eta_minutes": eta_minutes,
            "crew_status": payload.get("crew_status", "dispatched"),
        },
    )
    return _finalize_command(
        next_state,
        operation="simulate_outage_event",
        entity="outage_event",
        record=record,
        event_type="EnergyGridOperationsUpdated",
        rule_ids=("outage_event_policy",),
        parameter_names=("materiality_threshold", "approval_sla_hours"),
    )


def energy_grid_operations_create_reliability_constraint(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    missing = _required(payload, _rule_definition("reliability_constraint_policy")["required_fields"])
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if payload.get("constraint_type") not in CONSTRAINT_TYPES:
        return {"ok": False, "state": _copy_state(state), "reason": "invalid_constraint_type", "side_effects": ()}
    next_state, record = _store_record(
        state,
        "reliability_constraint",
        payload,
        status=payload.get("status", "active"),
        summary=f"{payload['constraint_type']} constraint on {payload['scope_id']}",
        extra={
            "constraint_type": payload["constraint_type"],
            "scope_id": payload["scope_id"],
            "scope_level": payload.get("scope_level", "feeder"),
            "severity": payload["severity"],
            "limit_value": payload["limit_value"],
        },
    )
    return _finalize_command(
        next_state,
        operation="create_reliability_constraint",
        entity="reliability_constraint",
        record=record,
        event_type="EnergyGridOperationsCreated",
        rule_ids=("reliability_constraint_policy",),
        parameter_names=("risk_threshold",),
    )


def energy_grid_operations_record_grid_topology(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    required = ("topology_id", "tenant", "feeder_id", "source_asset_id")
    missing = _required(payload, required)
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    segments = tuple(payload.get("energized_sections", ()))
    next_state, record = _store_record(
        state,
        "grid_topology",
        payload,
        status=payload.get("status", "published"),
        summary=f"Topology {payload['topology_id']} for feeder {payload['feeder_id']}",
        extra={
            "feeder_id": payload["feeder_id"],
            "source_asset_id": payload["source_asset_id"],
            "segment_count": len(segments),
            "normally_open_ties": tuple(payload.get("normally_open_ties", ())),
            "backfeed_paths": tuple(payload.get("backfeed_paths", ())),
            "phase_map": dict(payload.get("phase_map", {})),
        },
    )
    return _finalize_command(
        next_state,
        operation="record_grid_topology",
        entity="grid_topology",
        record=record,
        event_type="EnergyGridOperationsUpdated",
        rule_ids=("grid_asset_policy",),
        parameter_names=("workbench_limit",),
    )


def energy_grid_operations_review_energy_grid_operations_policy_rule(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    rule = dict(payload.get("rule", payload))
    registered = energy_grid_operations_register_rule(state, {"rule": rule})
    if not registered["ok"]:
        return registered
    compiled = registered["rule"]
    next_state, record = _store_record(
        registered["state"],
        "energy_grid_operations_policy_rule",
        {
            "rule_id": compiled["rule_id"],
            "tenant": rule.get("tenant", "tenant_demo"),
            "scope": compiled["scope"],
            "policy_version": rule.get("policy_version", DEFAULT_CONFIGURATION["default_policy_version"]),
            "required_approver_role": compiled["required_approver_role"],
            "compiled_hash": compiled["compiled_hash"],
            **rule,
        },
        status=compiled["status"],
        summary=f"Policy rule {compiled['rule_id']} reviewed",
        extra={
            "scope": compiled["scope"],
            "policy_version": rule.get("policy_version", DEFAULT_CONFIGURATION["default_policy_version"]),
            "compiled_hash": compiled["compiled_hash"],
            "required_approver_role": compiled["required_approver_role"],
        },
    )
    return _finalize_command(
        next_state,
        operation="review_energy_grid_operations_policy_rule",
        entity="energy_grid_operations_policy_rule",
        record=record,
        event_type="EnergyGridOperationsUpdated",
        rule_ids=(compiled["rule_id"],),
        parameter_names=("approval_sla_hours",),
    )


def energy_grid_operations_approve_energy_grid_operations_runtime_parameter(state: dict, payload: dict | None = None) -> dict:
    parameter_result = energy_grid_operations_set_parameter(state, payload)
    if not parameter_result["ok"]:
        return parameter_result
    parameter = parameter_result["parameter"]
    next_state, record = _store_record(
        parameter_result["state"],
        "energy_grid_operations_runtime_parameter",
        {
            "parameter_name": parameter["name"],
            "tenant": payload.get("tenant", "tenant_demo"),
            "value": parameter["value"],
            "approved_by": payload.get("approved_by", "grid_admin"),
        },
        status="approved",
        summary=f"Runtime parameter {parameter['name']} approved",
        extra={
            "value": parameter["value"],
            "datatype": parameter["datatype"],
            "minimum": parameter["minimum"],
            "maximum": parameter["maximum"],
            "approved_by": payload.get("approved_by", "grid_admin"),
        },
    )
    return _finalize_command(
        next_state,
        operation="approve_energy_grid_operations_runtime_parameter",
        entity="energy_grid_operations_runtime_parameter",
        record=record,
        event_type="EnergyGridOperationsApproved",
        rule_ids=(),
        parameter_names=(parameter["name"],),
    )


def energy_grid_operations_simulate_energy_grid_operations_schema_extension(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    target_table = payload.get("target_table")
    new_fields = tuple(payload.get("new_fields", ()))
    if target_table not in ENERGY_GRID_OPERATIONS_BUSINESS_TABLES:
        return {"ok": False, "state": _copy_state(state), "reason": "unknown_owned_table", "target_table": target_table, "side_effects": ()}
    compatibility_result = "compatible" if new_fields and all("name" in field and "datatype" in field for field in new_fields) else "blocked"
    next_state, record = _store_record(
        state,
        "energy_grid_operations_schema_extension",
        {
            "extension_id": payload.get("extension_id", _digest((target_table, new_fields))[:12]),
            "tenant": payload.get("tenant", "tenant_demo"),
            "target_table": target_table,
            "new_fields": new_fields,
            "compatibility_result": compatibility_result,
        },
        status="simulated" if compatibility_result == "compatible" else "blocked",
        summary=f"Schema extension against {target_table}",
        extra={
            "target_table": target_table,
            "new_fields": new_fields,
            "compatibility_result": compatibility_result,
        },
    )
    return _finalize_command(
        next_state,
        operation="simulate_energy_grid_operations_schema_extension",
        entity="energy_grid_operations_schema_extension",
        record=record,
        event_type="EnergyGridOperationsUpdated",
        rule_ids=(),
        parameter_names=("workbench_limit",),
        warnings=() if compatibility_result == "compatible" else ("schema_extension_blocked",),
    )


def energy_grid_operations_create_energy_grid_operations_control_assertion(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    required = ("assertion_id", "tenant", "control_name", "scope_id", "assertion_status")
    missing = _required(payload, required)
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    next_state, record = _store_record(
        state,
        "energy_grid_operations_control_assertion",
        payload,
        status=payload.get("status", "recorded"),
        summary=f"Control assertion {payload['control_name']} for {payload['scope_id']}",
        extra={
            "control_name": payload["control_name"],
            "scope_id": payload["scope_id"],
            "assertion_status": payload["assertion_status"],
            "evidence_summary": payload.get("evidence_summary", "operator evidence captured"),
            "review_required": bool(payload.get("review_required", False)),
        },
    )
    return _finalize_command(
        next_state,
        operation="create_energy_grid_operations_control_assertion",
        entity="energy_grid_operations_control_assertion",
        record=record,
        event_type="EnergyGridOperationsUpdated",
        rule_ids=(),
        parameter_names=("quality_score_floor",),
    )


def energy_grid_operations_record_energy_grid_operations_governed_model(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    required = ("model_id", "tenant", "model_kind", "approval_scope", "training_boundary")
    missing = _required(payload, required)
    if missing:
        return {"ok": False, "state": _copy_state(state), "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    next_state, record = _store_record(
        state,
        "energy_grid_operations_governed_model",
        payload,
        status=payload.get("status", "approved"),
        summary=f"Governed model {payload['model_id']} recorded",
        extra={
            "model_kind": payload["model_kind"],
            "approval_scope": payload["approval_scope"],
            "training_boundary": payload["training_boundary"],
            "deployment_status": payload.get("deployment_status", "shadow"),
        },
    )
    return _finalize_command(
        next_state,
        operation="record_energy_grid_operations_governed_model",
        entity="energy_grid_operations_governed_model",
        record=record,
        event_type="EnergyGridOperationsApproved",
        rule_ids=(),
        parameter_names=("risk_threshold",),
    )


def energy_grid_operations_query_timeline(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    tenant = payload.get("tenant")
    records = tuple(
        entry for entry in state.get("audit_log", ()) if tenant in (None, state.get("configuration", {}).get("tenant"), payload.get("tenant"))
    )
    return {
        "ok": True,
        "timeline": records,
        "outbox": tuple(state.get("outbox", ())),
        "inbox": tuple(state.get("inbox", ())),
        "dead_letter": tuple(state.get("dead_letter", ())),
        "side_effects": (),
    }


def energy_grid_operations_build_workbench_view(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    tenant = payload.get("tenant", "tenant_demo")
    assets = _tenant_records(state, "grid_asset", tenant)
    forecasts = _tenant_records(state, "load_forecast", tenant)
    switching_orders = _tenant_records(state, "switching_order", tenant)
    dispatch_instructions = _tenant_records(state, "dispatch_instruction", tenant)
    outages = _tenant_records(state, "outage_event", tenant)
    constraints = _tenant_records(state, "reliability_constraint", tenant)
    topology = _tenant_records(state, "grid_topology", tenant)
    assertions = _tenant_records(state, "energy_grid_operations_control_assertion", tenant)
    exceptions = tuple(
        record
        for collection in (switching_orders, dispatch_instructions, assertions)
        for record in collection
        if record.get("status") in {"blocked", "review_required"} or record.get("review_required") is True
    )
    view = {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "asset_count": len(assets),
        "feeder_count": len({asset.get("feeder_id") for asset in assets if asset.get("feeder_id")}),
        "substation_count": len({asset.get("substation_id") for asset in assets if asset.get("substation_id")}),
        "load_forecast_count": len(forecasts),
        "switching_order_count": len(switching_orders),
        "dispatch_instruction_count": len(dispatch_instructions),
        "active_outage_count": len([item for item in outages if item.get("status") != "restored"]),
        "active_constraint_count": len([item for item in constraints if item.get("status") == "active"]),
        "topology_count": len(topology),
        "control_assertion_count": len(assertions),
        "exception_count": len(exceptions),
        "outbox_count": len([event for event in state.get("outbox", ()) if event.get("tenant") == tenant]),
        "inbox_count": len([event for event in state.get("inbox", ()) if event.get("tenant") == tenant]),
        "dead_letter_count": len([event for event in state.get("dead_letter", ()) if event.get("tenant") == tenant]),
        "configuration_bound": bool(state.get("configuration")),
        "parameters_bound": len(state.get("parameters", {})),
        "rules_bound": len(state.get("rules", {})),
        "owned_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
        "event_contract": "AppGen-X",
        "queues": {
            "switching_review": tuple(record["id"] for record in switching_orders if record.get("status") != "ready_for_dispatch")[:5],
            "dispatch_conflicts": tuple(record["id"] for record in dispatch_instructions if record.get("status") != "approved")[:5],
            "restoration_priority": tuple(record["id"] for record in sorted(outages, key=lambda item: item.get("affected_customers", 0), reverse=True))[:5],
            "exceptions": tuple(record["id"] for record in exceptions)[:5],
        },
    }
    view["cards"] = _workbench_cards(view)
    return view


def energy_grid_operations_query_workbench(state: dict, payload: dict | None = None) -> dict:
    return energy_grid_operations_build_workbench_view(state, payload)


def energy_grid_operations_build_schema_contract() -> dict:
    tables = tuple(
        {
            "table": spec["table"],
            "entity": spec["entity"],
            "fields": spec["fields"],
            "primary_key": (spec["id_key"],),
            "owned_by": PBC_KEY,
            "description": spec["description"],
        }
        for spec in BUSINESS_TABLE_SPECS + EVENT_TABLE_SPECS
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in spec["entity"].split("_")),
            "table": spec["table"],
            "id_field": spec["id_key"],
            "fields": spec["fields"],
        }
        for spec in BUSINESS_TABLE_SPECS + EVENT_TABLE_SPECS
    )
    return {
        "format": "appgen.energy-grid-operations-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": tables,
        "models": models,
        "migrations": (
            {
                "path": "pbcs/energy_grid_operations/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "backend_allowlist": ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "owned_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
        "database_backends": ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def energy_grid_operations_build_service_contract() -> dict:
    return {
        "format": "appgen.energy-grid-operations-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": SUPPORT_OPERATIONS + DOMAIN_OPERATIONS,
        "query_methods": QUERY_OPERATIONS,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "shared_table_access": False,
    }


def energy_grid_operations_build_api_contract() -> dict:
    routes = (
        "POST /grid-assets",
        "POST /load-forecasts",
        "POST /switching-orders",
        "POST /dispatch-instructions",
        "POST /outage-events",
        "GET /energy-grid-operations-workbench",
    )
    return {
        "format": "appgen.energy-grid-operations-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": routes,
        "declared_catalog_routes": routes,
        "event_contract": "AppGen-X",
        "required_event_topic": ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "owned_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
        "shared_table_access": False,
    }


def energy_grid_operations_permissions_contract() -> dict:
    roles = {
        "operator": (
            "energy_grid_operations.read",
            "energy_grid_operations.create",
            "energy_grid_operations.update",
        ),
        "dispatcher": (
            "energy_grid_operations.read",
            "energy_grid_operations.create",
            "energy_grid_operations.update",
            "energy_grid_operations.approve",
        ),
        "grid_admin": (
            "energy_grid_operations.read",
            "energy_grid_operations.create",
            "energy_grid_operations.update",
            "energy_grid_operations.approve",
            "energy_grid_operations.admin",
        ),
        "auditor": (
            "energy_grid_operations.read",
            "energy_grid_operations.approve",
        ),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSION_MAP,
        "permission_set": tuple(sorted(set(PERMISSION_MAP.values()))),
        "roles": roles,
        "side_effects": (),
    }


def energy_grid_operations_verify_owned_table_boundary(references: tuple[str, ...] | list[str] = ()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref not in ENERGY_GRID_OPERATIONS_OWNED_TABLES
        and ref.endswith(("table", "event"))
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
        "shared_table_access": False,
    }


def energy_grid_operations_build_release_evidence() -> dict:
    energy_grid_control = improve1_energy_grid_control_contract()
    checks = (
        {"id": "owned_tables_prefixed", "ok": all(table.startswith(f"{PBC_KEY}_") for table in ENERGY_GRID_OPERATIONS_OWNED_TABLES)},
        {"id": "schema_models_present", "ok": bool(energy_grid_operations_build_schema_contract()["models"])},
        {"id": "service_contract_present", "ok": energy_grid_operations_build_service_contract()["ok"]},
        {"id": "api_contract_present", "ok": energy_grid_operations_build_api_contract()["ok"]},
        {"id": "permissions_present", "ok": bool(energy_grid_operations_permissions_contract()["permission_set"])},
        {"id": "rule_catalog_present", "ok": bool(RULE_DEFINITIONS)},
        {"id": "parameter_catalog_present", "ok": bool(PARAMETER_DEFINITIONS)},
        {"id": "energy_grid_improve1_control_contract", "ok": energy_grid_control["ok"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.energy-grid-operations-release-evidence.v2",
        "ok": not blocking_gaps,
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema": energy_grid_operations_build_schema_contract(),
        "service": energy_grid_operations_build_service_contract(),
        "api": energy_grid_operations_build_api_contract(),
        "permissions": energy_grid_operations_permissions_contract(),
        "energy_grid_control": energy_grid_control,
        "side_effects": (),
    }


def energy_grid_operations_runtime_capabilities() -> dict:
    smoke = energy_grid_operations_runtime_smoke()
    return {
        "format": "appgen.energy-grid-operations-runtime-capabilities.v2",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
        "allowed_database_backends": ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": ENERGY_GRID_OPERATIONS_STANDARD_FEATURE_KEYS,
        "capabilities": ENERGY_GRID_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        "improve1_energy_grid_control_capabilities": tuple(capability.slug for capability in ENERGY_GRID_CONTROL_CAPABILITIES),
        "operations": SUPPORT_OPERATIONS + DOMAIN_OPERATIONS + QUERY_OPERATIONS + ("improve1_energy_grid_control_contract",),
        "database_backends": ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "smoke": smoke,
        "side_effects": (),
    }


def energy_grid_operations_runtime_smoke() -> dict:
    state = energy_grid_operations_empty_state()
    configured = energy_grid_operations_configure_runtime(state, {"configuration": DEFAULT_CONFIGURATION})
    parameter = energy_grid_operations_approve_energy_grid_operations_runtime_parameter(
        configured["state"],
        {"name": "workbench_limit", "value": 30, "tenant": "tenant_smoke", "approved_by": "grid_admin"},
    )
    rule = energy_grid_operations_review_energy_grid_operations_policy_rule(
        parameter["state"],
        {
            "rule": {
                "rule_id": "switching_order_policy",
                "tenant": "tenant_smoke",
                "policy_version": "grid-policy-2026.05",
            }
        },
    )
    asset = energy_grid_operations_create_grid_asset(
        rule["state"],
        {
            "asset_id": "asset_smoke",
            "tenant": "tenant_smoke",
            "asset_type": "breaker",
            "asset_name": "Breaker 101",
            "voltage_kv": 33,
            "substation_id": "sub_smoke",
            "feeder_id": "feeder_smoke",
            "normal_state": "closed",
            "phases": ("A", "B", "C"),
        },
    )
    topology = energy_grid_operations_record_grid_topology(
        asset["state"],
        {
            "topology_id": "topology_smoke",
            "tenant": "tenant_smoke",
            "feeder_id": "feeder_smoke",
            "source_asset_id": "asset_smoke",
            "energized_sections": ("section_1", "section_2"),
            "normally_open_ties": ("tie_1",),
        },
    )
    constraint = energy_grid_operations_create_reliability_constraint(
        topology["state"],
        {
            "constraint_id": "constraint_smoke",
            "tenant": "tenant_smoke",
            "constraint_type": "thermal",
            "scope_id": "feeder_smoke",
            "severity": "medium",
            "limit_value": 55.0,
        },
    )
    switching = energy_grid_operations_review_switching_order(
        constraint["state"],
        {
            "switching_order_id": "switch_smoke",
            "tenant": "tenant_smoke",
            "feeder_id": "feeder_smoke",
            "substation_id": "sub_smoke",
            "clearance_id": "clr_smoke",
            "requested_by": "dispatcher",
            "steps": (
                {"sequence": 1, "action": "open", "target": "asset_smoke", "hold_point": True, "description": "Open breaker"},
                {"sequence": 2, "action": "verify", "target": "asset_smoke", "description": "Verify isolation"},
            ),
        },
    )
    dispatch = energy_grid_operations_approve_dispatch_instruction(
        switching["state"],
        {
            "dispatch_instruction_id": "dispatch_smoke",
            "tenant": "tenant_smoke",
            "objective_type": "voltage_support",
            "feeder_id": "feeder_smoke",
            "target_asset_id": "asset_smoke",
            "expected_load_shift_mw": 5.0,
            "telemetry_freshness_seconds": 120,
            "rollback_conditions": ("restore_normal_after_window",),
        },
    )
    outage = energy_grid_operations_simulate_outage_event(
        dispatch["state"],
        {
            "outage_event_id": "outage_smoke",
            "tenant": "tenant_smoke",
            "feeder_id": "feeder_smoke",
            "substation_id": "sub_smoke",
            "cause": "storm_trip",
            "affected_customers": 1200,
        },
    )
    event = energy_grid_operations_receive_event(
        outage["state"],
        {"envelope": {"event_type": "PolicyChanged", "event_id": "policy_smoke", "payload": {"tenant": "tenant_smoke", "policy_version": "grid-policy-2026.06"}}},
    )
    workbench = energy_grid_operations_build_workbench_view(event["state"], {"tenant": "tenant_smoke"})
    energy_grid_control = improve1_energy_grid_control_contract()
    boundary = energy_grid_operations_verify_owned_table_boundary(ENERGY_GRID_OPERATIONS_OWNED_TABLES + ("foreign_table",))
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "approve_runtime_parameter", "ok": parameter["ok"]},
        {"id": "review_policy_rule", "ok": rule["ok"]},
        {"id": "create_grid_asset", "ok": asset["ok"]},
        {"id": "record_topology", "ok": topology["ok"]},
        {"id": "create_constraint", "ok": constraint["ok"]},
        {"id": "review_switching_order", "ok": switching["ok"]},
        {"id": "approve_dispatch_instruction", "ok": dispatch["ok"]},
        {"id": "simulate_outage_event", "ok": outage["ok"]},
        {"id": "receive_event", "ok": event["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"] and workbench["asset_count"] >= 1},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "improve1_energy_grid_control_contract", "ok": energy_grid_control["ok"]},
    )
    return {
        "format": "appgen.energy-grid-operations-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "checks_by_id": {check["id"]: check["ok"] for check in checks},
        "configuration": configured,
        "asset": asset,
        "switching": switching,
        "dispatch": dispatch,
        "outage": outage,
        "event": event,
        "workbench": workbench,
        "energy_grid_control": energy_grid_control,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }
