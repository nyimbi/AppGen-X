"""Deterministic operational slice for the water_wastewater_operations PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json

PBC_KEY = "water_wastewater_operations"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
EMITTED_EVENT_TYPES = (
    "WaterWastewaterOperationsCreated",
    "WaterWastewaterOperationsUpdated",
    "WaterWastewaterOperationsApproved",
    "WaterWastewaterOperationsExceptionOpened",
)
CONSUMED_EVENT_TYPES = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")

BASE_BUSINESS_TABLES = (
    "treatment_plant",
    "process_unit",
    "source_water_observation",
    "production_run",
    "distribution_zone",
    "pressure_quality_sample",
    "pump_operation",
    "valve_operation",
    "sewer_collection_area",
    "lift_station",
    "wastewater_treatment_batch",
    "discharge_permit",
    "lab_compliance_case",
    "operations_incident",
    "flushing_program",
    "hydrant_asset",
    "asset_isolation_plan",
    "scada_projection",
    "water_wastewater_operations_policy_rule",
    "water_wastewater_operations_runtime_parameter",
    "water_wastewater_operations_schema_extension",
    "water_wastewater_operations_control_assertion",
    "water_wastewater_operations_governed_model",
)
BASE_RUNTIME_TABLES = (
    "appgen_outbox_event",
    "appgen_inbox_event",
    "appgen_dead_letter_event",
)
BUSINESS_TABLES = tuple(f"{PBC_KEY}_{name}" for name in BASE_BUSINESS_TABLES)
RUNTIME_TABLES = tuple(f"{PBC_KEY}_{name}" for name in BASE_RUNTIME_TABLES)
OWNED_TABLES = BUSINESS_TABLES + RUNTIME_TABLES

STANDARD_FEATURES = (
    "treatment_plant_management",
    "process_unit_configuration",
    "source_water_monitoring",
    "production_and_distribution_management",
    "pressure_quality_sampling",
    "pump_valve_operations",
    "sewer_collection_monitoring",
    "lift_station_overflow_prevention",
    "wastewater_treatment_compliance",
    "discharge_permit_management",
    "lab_compliance_and_chain_of_custody",
    "incident_and_advisory_management",
    "flushing_and_hydrant_programs",
    "asset_isolation",
    "scada_projection_boundary",
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
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
)
ADVANCED_CAPABILITIES = (
    "water_wastewater_operations_event_sourced_operational_history",
    "water_wastewater_operations_multi_tenant_policy_isolation",
    "water_wastewater_operations_schema_evolution_resilience",
    "water_wastewater_operations_autonomous_anomaly_detection",
    "water_wastewater_operations_semantic_document_instruction_understanding",
    "water_wastewater_operations_predictive_risk_scoring",
    "water_wastewater_operations_counterfactual_scenario_simulation",
    "water_wastewater_operations_cryptographic_audit_proofs",
    "water_wastewater_operations_continuous_control_testing",
    "water_wastewater_operations_carbon_and_sustainability_awareness",
    "water_wastewater_operations_cross_pbc_event_federation",
    "water_wastewater_operations_governed_ai_agent_execution",
)
RULES = (
    "treatment_state_policy",
    "sampling_compliance_policy",
    "pressure_response_policy",
    "pump_reliability_policy",
    "overflow_escalation_policy",
    "hydrant_flushing_policy",
    "agent_governance_policy",
    "scada_projection_freshness_policy",
)
PARAMETER_SPECS = {
    "min_distribution_pressure_psi": {"minimum": 20, "maximum": 80, "default": 35, "unit": "psi"},
    "min_disinfectant_residual_mg_l": {"minimum": 0.0, "maximum": 4.0, "default": 0.2, "unit": "mg/L"},
    "max_turbidity_ntu": {"minimum": 0.1, "maximum": 10.0, "default": 1.0, "unit": "NTU"},
    "lift_station_overflow_risk_pct": {"minimum": 50, "maximum": 100, "default": 85, "unit": "percent"},
    "hydrant_min_flow_gpm": {"minimum": 250, "maximum": 2500, "default": 750, "unit": "gpm"},
    "incident_notification_minutes": {"minimum": 5, "maximum": 240, "default": 60, "unit": "minutes"},
    "scada_projection_freshness_minutes": {"minimum": 1, "maximum": 240, "default": 15, "unit": "minutes"},
    "workbench_limit": {"minimum": 10, "maximum": 500, "default": 50, "unit": "records"},
}

API_ROUTE_SPECS = (
    {"route": "POST /water-ops/treatment-plants", "command": "register_treatment_plant"},
    {"route": "POST /water-ops/process-units", "command": "configure_process_unit"},
    {"route": "POST /water-ops/source-water", "command": "record_source_water_observation"},
    {"route": "POST /water-ops/production-runs", "command": "record_production_run"},
    {"route": "POST /water-ops/distribution-zones", "command": "define_distribution_zone"},
    {"route": "POST /water-ops/pressure-quality-samples", "command": "record_pressure_quality_sample"},
    {"route": "POST /water-ops/pump-operations", "command": "record_pump_operation"},
    {"route": "POST /water-ops/valve-operations", "command": "record_valve_operation"},
    {"route": "POST /water-ops/sewer-collection-areas", "command": "register_sewer_collection_area"},
    {"route": "POST /water-ops/lift-stations", "command": "register_lift_station"},
    {"route": "POST /water-ops/wastewater-treatment-batches", "command": "record_wastewater_treatment_batch"},
    {"route": "POST /water-ops/discharge-permits", "command": "register_discharge_permit"},
    {"route": "POST /water-ops/lab-compliance-cases", "command": "record_lab_compliance_case"},
    {"route": "POST /water-ops/incidents", "command": "report_operations_incident"},
    {"route": "POST /water-ops/flushing-programs", "command": "plan_flushing_program"},
    {"route": "POST /water-ops/hydrants", "command": "inspect_hydrant_asset"},
    {"route": "POST /water-ops/isolation-plans", "command": "create_asset_isolation_plan"},
    {"route": "POST /water-ops/scada-projections", "command": "project_scada_snapshot"},
    {"route": "GET /water-ops/workbench", "query": "query_workbench"},
    {"route": "GET /water-ops/release-evidence", "query": "build_release_evidence"},
)

UI_FRAGMENTS = (
    "WaterWastewaterOperationsWorkbench",
    "WaterWastewaterOperationsDetail",
    "WaterWastewaterOperationsAssistantPanel",
)
WORKBENCH_SECTIONS = (
    "treatment_command_center",
    "distribution_zone_status",
    "pressure_quality_compliance",
    "pump_and_valve_operations",
    "sewer_and_lift_station_risk",
    "incident_and_advisory_queue",
    "flushing_and_hydrant_programs",
    "asset_isolation_readiness",
    "scada_projection_health",
    "release_evidence",
)
FORM_DEFINITIONS = (
    "TreatmentPlantForm",
    "ProcessUnitForm",
    "PressureQualitySampleForm",
    "IncidentReportForm",
    "DischargePermitForm",
    "IsolationPlanForm",
)
WIZARD_DEFINITIONS = (
    "BoilWaterAdvisoryWizard",
    "OverflowResponseWizard",
    "HydrantFlushingWizard",
    "AssetIsolationWizard",
    "LabComplianceReviewWizard",
)
CONTROL_DEFINITIONS = (
    "PlantModeControl",
    "PermitRiskControl",
    "PressureAlertControl",
    "PumpStandbyControl",
    "OverflowRiskControl",
    "GovernedActionApprovalControl",
)
AGENT_SKILLS = (
    {
        "name": "water_wastewater_operations_sample_interpreter",
        "purpose": "Summarize pressure and quality samples against permit and public health thresholds.",
    },
    {
        "name": "water_wastewater_operations_incident_narrator",
        "purpose": "Draft concise incident timelines and regulator-ready narratives from owned evidence.",
    },
    {
        "name": "water_wastewater_operations_isolation_planner",
        "purpose": "Preview valve sequencing and affected-service impact for governed isolation plans.",
    },
    {
        "name": "water_wastewater_operations_scada_projection_reviewer",
        "purpose": "Explain projected telemetry freshness and operational risk without mutating external historian data.",
    },
)

DOMAIN_OPERATION_SPECS = {
    "register_treatment_plant": {
        "table": "treatment_plant",
        "event_type": EMITTED_EVENT_TYPES[0],
        "required_fields": ("plant_code", "plant_name", "utility_type", "operating_state"),
        "summary_field": "plant_code",
    },
    "configure_process_unit": {
        "table": "process_unit",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("plant_code", "unit_code", "process_stage", "status"),
        "summary_field": "unit_code",
    },
    "record_source_water_observation": {
        "table": "source_water_observation",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("observation_code", "plant_code", "source_name", "observed_at"),
        "summary_field": "observation_code",
    },
    "record_production_run": {
        "table": "production_run",
        "event_type": EMITTED_EVENT_TYPES[0],
        "required_fields": ("run_code", "plant_code", "produced_volume_m3"),
        "summary_field": "run_code",
    },
    "define_distribution_zone": {
        "table": "distribution_zone",
        "event_type": EMITTED_EVENT_TYPES[0],
        "required_fields": ("zone_code", "zone_name", "service_population"),
        "summary_field": "zone_code",
    },
    "record_pressure_quality_sample": {
        "table": "pressure_quality_sample",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("sample_code", "zone_code", "sample_point", "collected_at"),
        "summary_field": "sample_code",
    },
    "record_pump_operation": {
        "table": "pump_operation",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("operation_code", "asset_code", "plant_code", "status"),
        "summary_field": "asset_code",
    },
    "record_valve_operation": {
        "table": "valve_operation",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("operation_code", "valve_code", "zone_code", "action"),
        "summary_field": "valve_code",
    },
    "register_sewer_collection_area": {
        "table": "sewer_collection_area",
        "event_type": EMITTED_EVENT_TYPES[0],
        "required_fields": ("area_code", "service_area", "critical_customers"),
        "summary_field": "area_code",
    },
    "register_lift_station": {
        "table": "lift_station",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("station_code", "service_area", "wet_well_level_pct"),
        "summary_field": "station_code",
    },
    "record_wastewater_treatment_batch": {
        "table": "wastewater_treatment_batch",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("batch_code", "plant_code", "influent_flow_mld"),
        "summary_field": "batch_code",
    },
    "register_discharge_permit": {
        "table": "discharge_permit",
        "event_type": EMITTED_EVENT_TYPES[2],
        "required_fields": ("permit_code", "plant_code", "outfall_code", "parameter_limits"),
        "summary_field": "permit_code",
    },
    "record_lab_compliance_case": {
        "table": "lab_compliance_case",
        "event_type": EMITTED_EVENT_TYPES[2],
        "required_fields": ("case_code", "sample_code", "parameter", "result_value"),
        "summary_field": "case_code",
    },
    "report_operations_incident": {
        "table": "operations_incident",
        "event_type": EMITTED_EVENT_TYPES[3],
        "required_fields": ("incident_code", "incident_type", "severity", "started_at"),
        "summary_field": "incident_code",
    },
    "plan_flushing_program": {
        "table": "flushing_program",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("program_code", "zone_code", "hydrant_codes"),
        "summary_field": "program_code",
    },
    "inspect_hydrant_asset": {
        "table": "hydrant_asset",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("hydrant_code", "zone_code", "inspection_date", "flow_gpm"),
        "summary_field": "hydrant_code",
    },
    "create_asset_isolation_plan": {
        "table": "asset_isolation_plan",
        "event_type": EMITTED_EVENT_TYPES[2],
        "required_fields": ("plan_code", "asset_code", "valve_sequence"),
        "summary_field": "plan_code",
    },
    "project_scada_snapshot": {
        "table": "scada_projection",
        "event_type": EMITTED_EVENT_TYPES[1],
        "required_fields": ("projection_code", "asset_code", "captured_at", "tags"),
        "summary_field": "projection_code",
    },
}
DOMAIN_OPERATIONS = tuple(DOMAIN_OPERATION_SPECS)


def _hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def prefixed_table(base_name: str) -> str:
    return base_name if base_name.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{base_name}"


def empty_state() -> dict:
    return {
        "records": {table: {} for table in OWNED_TABLES},
        "parameters": {
            name: {
                "name": name,
                "value": spec["default"],
                "bounded": True,
                "unit": spec["unit"],
            }
            for name, spec in PARAMETER_SPECS.items()
        },
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "governed_actions": [],
        "release_evidence": {},
        "idempotency_keys": set(),
    }


def _copy_state(state: dict | None) -> dict:
    copied = deepcopy(state or empty_state())
    copied["idempotency_keys"] = set((state or {}).get("idempotency_keys", set()))
    copied.setdefault("records", {})
    for table in OWNED_TABLES:
        copied["records"].setdefault(table, {})
    copied.setdefault("parameters", {})
    copied.setdefault("rules", {})
    copied.setdefault("schema_extensions", {})
    copied.setdefault("configuration", {})
    copied.setdefault("inbox", [])
    copied.setdefault("outbox", [])
    copied.setdefault("dead_letter", [])
    copied.setdefault("governed_actions", [])
    copied.setdefault("release_evidence", {})
    return copied


def validate_backend(database_backend: str) -> None:
    if database_backend not in ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Water/Wastewater Operations supports only PostgreSQL, MySQL, or MariaDB")


def configure_runtime(state: dict | None, config: dict | None) -> dict:
    next_state = _copy_state(state)
    configuration = dict(config or {})
    invalid_fields = tuple(
        field
        for field in configuration
        if field in {"stream_engine", "stream_processor", "runtime_profile", "broker", "state_store"}
        or "stream" in field
    )
    if invalid_fields:
        raise ValueError(
            "Water/Wastewater Operations does not allow stream-engine or user-selectable eventing fields"
        )
    database_backend = configuration.get("database_backend", "postgresql")
    validate_backend(database_backend)
    event_topic = configuration.get("event_topic", REQUIRED_EVENT_TOPIC)
    if event_topic != REQUIRED_EVENT_TOPIC:
        raise ValueError("Water/Wastewater Operations event topic is fixed to AppGen-X")
    next_state["configuration"] = {
        "database_backend": database_backend,
        "event_topic": REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "owned_tables": OWNED_TABLES,
        "stream_engine_picker_visible": False,
        "user_eventing_choice": False,
        "retry_limit": int(configuration.get("retry_limit", 5)),
    }
    return {"ok": True, "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def set_parameter(state: dict | None, name: str, value: object) -> dict:
    if name not in PARAMETER_SPECS:
        raise ValueError("Unsupported Water/Wastewater Operations parameter")
    spec = PARAMETER_SPECS[name]
    numeric_value = float(value)
    if not spec["minimum"] <= numeric_value <= spec["maximum"]:
        raise ValueError(f"Parameter {name} must stay within configured bounds")
    next_state = _copy_state(state)
    next_state["parameters"][name] = {
        "name": name,
        "value": numeric_value,
        "bounded": True,
        "minimum": spec["minimum"],
        "maximum": spec["maximum"],
        "unit": spec["unit"],
    }
    return {"ok": True, "state": next_state, "parameter": next_state["parameters"][name], "side_effects": ()}


def register_rule(state: dict | None, rule: dict | None) -> dict:
    payload = dict(rule or {})
    if any(key in payload for key in ("stream_engine", "stream_processor", "runtime_profile")):
        return {"ok": False, "rule": payload, "reason": "stream_eventing_forbidden", "side_effects": ()}
    rule_id = str(payload.get("rule_id") or payload.get("policy_area") or "unnamed_rule")
    next_state = _copy_state(state)
    compiled = {
        **payload,
        "rule_id": rule_id,
        "compiled": True,
        "compiled_hash": _hash(payload),
        "event_contract": "AppGen-X",
        "requires_human_confirmation": True,
    }
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def register_schema_extension(state: dict | None, table: str, fields: dict | None) -> dict:
    target = prefixed_table(table)
    if target not in OWNED_TABLES:
        raise ValueError("Water/Wastewater Operations schema extensions must target owned tables")
    next_state = _copy_state(state)
    next_state["schema_extensions"][target] = dict(fields or {})
    return {"ok": True, "state": next_state, "table": target, "fields": next_state["schema_extensions"][target], "side_effects": ()}


def receive_event(state: dict | None, event: dict | None) -> dict:
    payload = dict(event or {})
    next_state = _copy_state(state)
    idempotency_key = str(payload.get("idempotency_key") or payload.get("event_id") or _hash(payload))
    if idempotency_key in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "idempotency_key": idempotency_key, "side_effects": ()}
    next_state["idempotency_keys"].add(idempotency_key)
    envelope = {
        "event_id": payload.get("event_id", idempotency_key),
        "event_type": payload.get("event_type"),
        "payload": dict(payload.get("payload") or {}),
        "idempotency_key": idempotency_key,
    }
    if envelope["event_type"] not in CONSUMED_EVENT_TYPES:
        dead_letter = {
            **envelope,
            "status": "dead_letter",
            "reason": "unknown_event_type",
            "dead_letter_table": RUNTIME_TABLES[2],
            "retry_policy": {"max_attempts": 5},
        }
        next_state["dead_letter"].append(dead_letter)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": RUNTIME_TABLES[2],
            "retry_policy": dead_letter["retry_policy"],
            "side_effects": (),
        }
    next_state["inbox"].append({**envelope, "status": "processed"})
    return {"ok": True, "duplicate": False, "state": next_state, "inbox_table": RUNTIME_TABLES[1], "side_effects": ()}


def _value(state: dict, parameter_name: str) -> float:
    return float(state["parameters"][parameter_name]["value"])


def _require(payload: dict, required_fields: tuple[str, ...]) -> None:
    missing = tuple(field for field in required_fields if payload.get(field) in (None, "", (), [], {}))
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


def _record_id(payload: dict, summary_field: str) -> str:
    return str(payload.get("id") or payload.get(summary_field) or payload.get("code") or _hash(payload)[:12])


def _hydraulic_impact(payload: dict) -> dict:
    affected_connections = int(payload.get("affected_connections", 0))
    critical_customers = tuple(payload.get("critical_customers", ()))
    return {
        "affected_connections": affected_connections,
        "critical_customers": critical_customers,
        "customer_impact": "elevated" if affected_connections or critical_customers else "contained",
    }


def _incident_flags(payload: dict) -> dict:
    incident_type = str(payload.get("incident_type", "incident"))
    severity = str(payload.get("severity", "medium"))
    requires_regulatory_notice = incident_type in {"overflow", "boil_water", "permit_exceedance"}
    public_health_impact = incident_type in {"boil_water", "contamination", "main_break"}
    return {
        "incident_type": incident_type,
        "severity": severity,
        "requires_regulatory_notice": requires_regulatory_notice,
        "public_health_impact": public_health_impact,
        "command_center_lane": "critical" if severity in {"high", "critical"} else "standard",
    }


def _sample_status(state: dict, payload: dict) -> tuple[str, dict]:
    min_pressure = _value(state, "min_distribution_pressure_psi")
    min_residual = _value(state, "min_disinfectant_residual_mg_l")
    max_turbidity = _value(state, "max_turbidity_ntu")
    pressure = float(payload.get("pressure_psi", min_pressure))
    residual = float(payload.get("disinfectant_residual_mg_l", min_residual))
    turbidity = float(payload.get("turbidity_ntu", 0.0))
    risk_reasons = []
    if pressure < min_pressure:
        risk_reasons.append("low_pressure")
    if residual < min_residual:
        risk_reasons.append("low_residual")
    if turbidity > max_turbidity:
        risk_reasons.append("high_turbidity")
    if not payload.get("chain_of_custody_complete", True):
        risk_reasons.append("missing_chain_of_custody")
    if not payload.get("holding_time_ok", True):
        risk_reasons.append("holding_time_exceeded")
    status = "action_required" if risk_reasons else "in_range"
    return status, {
        "pressure_psi": pressure,
        "disinfectant_residual_mg_l": residual,
        "turbidity_ntu": turbidity,
        "risk_reasons": tuple(risk_reasons),
        "requires_resample": bool(risk_reasons),
    }


def _select_event_type(operation: str, payload: dict, summary: dict) -> str:
    if operation in {"register_discharge_permit", "record_lab_compliance_case", "create_asset_isolation_plan"}:
        return EMITTED_EVENT_TYPES[2]
    if operation == "report_operations_incident" or summary.get("requires_regulatory_notice"):
        return EMITTED_EVENT_TYPES[3]
    if payload.get("status") == "updated":
        return EMITTED_EVENT_TYPES[1]
    return DOMAIN_OPERATION_SPECS[operation]["event_type"]


def _store_record(
    state: dict,
    operation: str,
    payload: dict,
    *,
    summary: dict,
    projections: dict | None = None,
    evidence: dict | None = None,
    status: str = "active",
    approval_required: bool = False,
) -> dict:
    spec = DOMAIN_OPERATION_SPECS[operation]
    table = prefixed_table(spec["table"])
    tenant = str(payload.get("tenant", "default"))
    record_id = _record_id(payload, spec["summary_field"])
    next_state = _copy_state(state)
    record = {
        "id": record_id,
        "tenant": tenant,
        "code": record_id,
        "status": status,
        "version": 1,
        "table": table,
        "operation": operation,
        "payload": dict(payload),
        "summary": dict(summary),
        "projections": dict(projections or {}),
        "evidence": dict(evidence or {}),
        "requires_human_confirmation": approval_required,
        "evidence_hash": _hash((operation, payload, summary, projections, evidence, status)),
    }
    next_state["records"][table][record_id] = record
    if approval_required:
        next_state["governed_actions"].append(
            {
                "record_id": record_id,
                "table": table,
                "operation": operation,
                "approval_required": True,
                "status": "pending_confirmation",
            }
        )
    event_type = _select_event_type(operation, payload, summary)
    outbox_event = {
        "event_id": _hash((event_type, record_id)),
        "event_type": event_type,
        "topic": REQUIRED_EVENT_TOPIC,
        "payload": {
            "pbc": PBC_KEY,
            "domain_event": operation,
            "table": table,
            "record_id": record_id,
            "tenant": tenant,
            "summary": dict(summary),
        },
        "idempotency_key": _hash((operation, record_id, payload)),
    }
    next_state["outbox"].append(outbox_event)
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "target_table": table,
        "owned_tables": (table,),
        "emitted_event": event_type,
        "event_contract": "AppGen-X",
        "idempotency_key": outbox_event["idempotency_key"],
        "evidence_hash": record["evidence_hash"],
        "side_effects": (),
    }


def run_domain_operation(state: dict | None, operation: str, payload: dict | None) -> dict:
    if operation not in DOMAIN_OPERATION_SPECS:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    payload = dict(payload or {})
    _require(payload, DOMAIN_OPERATION_SPECS[operation]["required_fields"])
    current_state = _copy_state(state)

    if operation == "register_treatment_plant":
        summary = {
            "plant_code": payload["plant_code"],
            "operating_state": payload["operating_state"],
            "process_mode": payload.get("process_mode", "normal"),
            "distribution_zones": tuple(payload.get("distribution_zones", ())),
            "command_center_status": payload.get("operating_state", "normal"),
        }
        return _store_record(current_state, operation, payload, summary=summary)

    if operation == "configure_process_unit":
        summary = {
            "unit_code": payload["unit_code"],
            "process_stage": payload["process_stage"],
            "status": payload["status"],
            "bypass_allowed": bool(payload.get("bypass_allowed", False)),
            "critical_control_point": bool(payload.get("critical_control_point", True)),
        }
        return _store_record(current_state, operation, payload, summary=summary)

    if operation == "record_source_water_observation":
        turbidity = float(payload.get("turbidity_ntu", 0.0))
        rainfall = float(payload.get("rainfall_mm", 0.0))
        industrial_load = float(payload.get("industrial_load_index", 0.0))
        anomaly_score = round(min(1.0, (turbidity / 10.0) + (rainfall / 100.0) + (industrial_load / 50.0)), 4)
        summary = {
            "observation_code": payload["observation_code"],
            "source_name": payload["source_name"],
            "anomaly_score": anomaly_score,
            "operator_review_required": anomaly_score >= 0.5,
            "raw_water_watch": anomaly_score >= 0.5,
        }
        evidence = {"observed_values": {"turbidity_ntu": turbidity, "rainfall_mm": rainfall, "industrial_load_index": industrial_load}}
        return _store_record(current_state, operation, payload, summary=summary, evidence=evidence)

    if operation == "record_production_run":
        produced_volume = float(payload["produced_volume_m3"])
        delivered_volume = float(payload.get("delivered_volume_m3", produced_volume))
        district_loss_pct = 0.0 if produced_volume == 0 else round(max(0.0, 1 - (delivered_volume / produced_volume)) * 100, 3)
        summary = {
            "run_code": payload["run_code"],
            "produced_volume_m3": produced_volume,
            "delivered_volume_m3": delivered_volume,
            "district_loss_pct": district_loss_pct,
            "non_revenue_water_alert": district_loss_pct >= 15.0,
        }
        return _store_record(current_state, operation, payload, summary=summary)

    if operation == "define_distribution_zone":
        summary = {
            "zone_code": payload["zone_code"],
            "zone_name": payload["zone_name"],
            "service_population": int(payload["service_population"]),
            "critical_customers": tuple(payload.get("critical_customers", ())),
            "hydraulic_projection_only": True,
        }
        return _store_record(current_state, operation, payload, summary=summary)

    if operation == "record_pressure_quality_sample":
        if payload.get("approval_status") == "approved" and not (payload.get("chain_of_custody_complete") and payload.get("holding_time_ok", True)):
            raise ValueError("Water/Wastewater Operations cannot approve a sample without custody and holding-time evidence")
        status, sample_summary = _sample_status(current_state, payload)
        sample_summary.update({
            "sample_code": payload["sample_code"],
            "zone_code": payload["zone_code"],
            "sample_point": payload["sample_point"],
        })
        return _store_record(current_state, operation, payload, summary=sample_summary, status=status, approval_required=bool(sample_summary["risk_reasons"]))

    if operation == "record_pump_operation":
        runtime_hours = float(payload.get("runtime_hours", 0.0))
        standby_available = bool(payload.get("standby_available", True))
        vibration_index = float(payload.get("vibration_index", 0.0))
        summary = {
            "asset_code": payload["asset_code"],
            "status": payload["status"],
            "duty_role": payload.get("duty_role", "duty"),
            "runtime_hours": runtime_hours,
            "standby_available": standby_available,
            "alert": runtime_hours >= 20 or not standby_available or vibration_index >= 7.5,
        }
        return _store_record(current_state, operation, payload, summary=summary)

    if operation == "record_valve_operation":
        valve_sequence = tuple(payload.get("linked_valves", (payload["valve_code"],)))
        summary = {
            "valve_code": payload["valve_code"],
            "action": payload["action"],
            "valve_sequence": valve_sequence,
            "isolation_ready": payload["action"] in {"close", "open", "exercise"},
            **_hydraulic_impact(payload),
        }
        return _store_record(current_state, operation, payload, summary=summary)

    if operation == "register_sewer_collection_area":
        summary = {
            "area_code": payload["area_code"],
            "service_area": payload["service_area"],
            "critical_customers": tuple(payload.get("critical_customers", ())),
            "projection_only_dependencies": ("gis_network", "customer_registry"),
        }
        return _store_record(current_state, operation, payload, summary=summary)

    if operation == "register_lift_station":
        wet_well_level = float(payload["wet_well_level_pct"])
        risk_threshold = _value(current_state, "lift_station_overflow_risk_pct")
        summary = {
            "station_code": payload["station_code"],
            "wet_well_level_pct": wet_well_level,
            "generator_available": bool(payload.get("generator_available", True)),
            "overflow_risk": wet_well_level >= risk_threshold or not payload.get("generator_available", True),
        }
        status = "action_required" if summary["overflow_risk"] else "active"
        return _store_record(current_state, operation, payload, summary=summary, status=status, approval_required=summary["overflow_risk"])

    if operation == "record_wastewater_treatment_batch":
        effluent_bod = float(payload.get("effluent_bod_mg_l", 0.0))
        permit_limit = float(payload.get("permit_bod_limit_mg_l", effluent_bod))
        summary = {
            "batch_code": payload["batch_code"],
            "influent_flow_mld": float(payload["influent_flow_mld"]),
            "effluent_bod_mg_l": effluent_bod,
            "permit_bod_limit_mg_l": permit_limit,
            "permit_risk": "high" if effluent_bod > permit_limit else "controlled",
        }
        status = "violation_risk" if summary["permit_risk"] == "high" else "active"
        return _store_record(current_state, operation, payload, summary=summary, status=status, approval_required=summary["permit_risk"] == "high")

    if operation == "register_discharge_permit":
        summary = {
            "permit_code": payload["permit_code"],
            "outfall_code": payload["outfall_code"],
            "parameter_count": len(payload["parameter_limits"]),
            "effective_status": payload.get("effective_status", "active"),
        }
        return _store_record(current_state, operation, payload, summary=summary, approval_required=True)

    if operation == "record_lab_compliance_case":
        if payload.get("certified") and not payload.get("chain_of_custody_complete", False):
            raise ValueError("Water/Wastewater Operations lab certification requires complete chain-of-custody evidence")
        holding_time_ok = bool(payload.get("holding_time_ok", True))
        result_value = float(payload["result_value"])
        limit_value = float(payload.get("limit_value", result_value))
        summary = {
            "case_code": payload["case_code"],
            "sample_code": payload["sample_code"],
            "parameter": payload["parameter"],
            "result_value": result_value,
            "limit_value": limit_value,
            "qualified_result": bool(payload.get("qualified_result", False)),
            "requires_resample": (result_value > limit_value) or not holding_time_ok,
        }
        status = "non_compliant" if summary["requires_resample"] else "accepted"
        return _store_record(current_state, operation, payload, summary=summary, status=status, approval_required=summary["requires_resample"])

    if operation == "report_operations_incident":
        summary = {
            "incident_code": payload["incident_code"],
            **_incident_flags(payload),
            **_hydraulic_impact(payload),
        }
        return _store_record(current_state, operation, payload, summary=summary, status="open", approval_required=summary["public_health_impact"] or summary["requires_regulatory_notice"])

    if operation == "plan_flushing_program":
        hydrant_codes = tuple(payload["hydrant_codes"])
        summary = {
            "program_code": payload["program_code"],
            "zone_code": payload["zone_code"],
            "hydrant_count": len(hydrant_codes),
            "expected_water_loss_m3": round(float(payload.get("expected_flow_m3", 0.0)) * max(1, len(hydrant_codes)), 3),
            "discoloration_watch": bool(payload.get("discoloration_watch", False)),
        }
        return _store_record(current_state, operation, payload, summary=summary)

    if operation == "inspect_hydrant_asset":
        min_flow = _value(current_state, "hydrant_min_flow_gpm")
        flow_gpm = float(payload["flow_gpm"])
        summary = {
            "hydrant_code": payload["hydrant_code"],
            "flow_gpm": flow_gpm,
            "condition": payload.get("condition", "serviceable"),
            "follow_up_required": flow_gpm < min_flow or payload.get("condition") not in {None, "serviceable"},
        }
        status = "repair_required" if summary["follow_up_required"] else "serviceable"
        return _store_record(current_state, operation, payload, summary=summary, status=status)

    if operation == "create_asset_isolation_plan":
        valve_sequence = tuple(payload["valve_sequence"])
        if not valve_sequence:
            raise ValueError("Water/Wastewater Operations isolation plans require a valve sequence")
        summary = {
            "plan_code": payload["plan_code"],
            "asset_code": payload["asset_code"],
            "valve_sequence": valve_sequence,
            "verification_complete": bool(payload.get("verification_complete", False)),
            **_hydraulic_impact(payload),
        }
        status = "ready" if summary["verification_complete"] else "draft"
        return _store_record(current_state, operation, payload, summary=summary, status=status, approval_required=True)

    if operation == "project_scada_snapshot":
        freshness_minutes = float(payload.get("freshness_minutes", 0.0))
        max_freshness = _value(current_state, "scada_projection_freshness_minutes")
        summary = {
            "projection_code": payload["projection_code"],
            "asset_code": payload["asset_code"],
            "tag_count": len(payload["tags"]),
            "freshness_minutes": freshness_minutes,
            "projection_only": True,
            "historian_boundary": "projection_only",
            "stale_projection": freshness_minutes > max_freshness,
        }
        status = "stale" if summary["stale_projection"] else "current"
        return _store_record(current_state, operation, payload, summary=summary, status=status)

    raise AssertionError(f"Unhandled domain operation: {operation}")


def preview_domain_operation(operation: str, payload: dict | None) -> dict:
    if operation not in DOMAIN_OPERATION_SPECS:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    payload = dict(payload or {})
    spec = DOMAIN_OPERATION_SPECS[operation]
    table = prefixed_table(spec["table"])
    evidence_hash = _hash((operation, payload, table))
    try:
        _require(payload, spec["required_fields"])
        preview = run_domain_operation(empty_state(), operation, payload)
        evidence_hash = preview["evidence_hash"]
        event_type = preview["emitted_event"]
    except ValueError:
        event_type = spec["event_type"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": table,
        "owned_tables": (table,),
        "read_tables": (),
        "emitted_event": event_type,
        "event_contract": "AppGen-X",
        "idempotency_key": _hash((PBC_KEY, operation, sorted(payload.items()))),
        "rules_evaluated": RULES[:4],
        "parameters_read": tuple(PARAMETER_SPECS)[:4],
        "permission": f"{PBC_KEY}.operate",
        "evidence_hash": evidence_hash,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def all_records_for_tenant(state: dict | None, tenant: str = "default") -> dict[str, list[dict]]:
    current_state = _copy_state(state)
    return {
        table: [record for record in mapping.values() if record.get("tenant") == tenant]
        for table, mapping in current_state["records"].items()
    }


def build_workbench_view(state: dict | None, tenant: str = "default", filters: dict | None = None) -> dict:
    current_state = _copy_state(state)
    records = all_records_for_tenant(current_state, tenant=tenant)
    samples = records[prefixed_table("pressure_quality_sample")]
    incidents = records[prefixed_table("operations_incident")]
    pumps = records[prefixed_table("pump_operation")]
    lift_stations = records[prefixed_table("lift_station")]
    hydrants = records[prefixed_table("hydrant_asset")]
    scada = records[prefixed_table("scada_projection")]
    treatment_batches = records[prefixed_table("wastewater_treatment_batch")]
    governed_pending = tuple(item for item in current_state["governed_actions"] if item["status"] == "pending_confirmation")
    command_center = {
        "plants_online": len(records[prefixed_table("treatment_plant")]),
        "process_units_configured": len(records[prefixed_table("process_unit")]),
        "distribution_zones": len(records[prefixed_table("distribution_zone")]),
        "samples_requiring_action": sum(1 for record in samples if record["summary"].get("risk_reasons")),
        "pump_alerts": sum(1 for record in pumps if record["summary"].get("alert")),
        "lift_station_overflow_risk": sum(1 for record in lift_stations if record["summary"].get("overflow_risk")),
        "permit_risk_batches": sum(1 for record in treatment_batches if record["summary"].get("permit_risk") == "high"),
        "open_incidents": len([record for record in incidents if record["status"] == "open"]),
        "hydrant_follow_up": sum(1 for record in hydrants if record["summary"].get("follow_up_required")),
        "stale_scada_projections": sum(1 for record in scada if record["summary"].get("stale_projection")),
        "governed_actions_pending": len(governed_pending),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "filters": dict(filters or {}),
        "command_center": command_center,
        "sections": WORKBENCH_SECTIONS,
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "records": records,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "read_only": True,
        "side_effects": (),
    }


def query_workbench(state: dict | None, filters: dict | None = None, tenant: str = "default") -> dict:
    return build_workbench_view(state, tenant=tenant, filters=filters)


def run_advanced_assessment(state: dict | None, payload: dict | None = None) -> dict:
    tenant = str((payload or {}).get("tenant", "default"))
    workbench = build_workbench_view(state, tenant=tenant)
    command_center = workbench["command_center"]
    raw_score = 0.72
    raw_score -= min(0.2, command_center["samples_requiring_action"] * 0.02)
    raw_score -= min(0.15, command_center["open_incidents"] * 0.03)
    raw_score -= min(0.08, command_center["stale_scada_projections"] * 0.02)
    score = round(max(0.0, raw_score), 4)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "score": score,
        "command_center": command_center,
        "recommendations": (
            "prioritize pressure and disinfectant residual exceptions",
            "confirm overflow-risk lift stations before peak flows",
            "refresh stale SCADA projections before issuing governed commands",
        ),
        "side_effects": (),
    }


def parse_document_instruction(document: str, instruction: str) -> dict:
    combined = f"{document} {instruction}".lower()
    candidate_tables = [
        prefixed_table("pressure_quality_sample"),
        prefixed_table("operations_incident"),
        prefixed_table("asset_isolation_plan"),
    ]
    if "permit" in combined:
        candidate_tables.insert(0, prefixed_table("discharge_permit"))
    if "hydrant" in combined or "flush" in combined:
        candidate_tables.insert(0, prefixed_table("flushing_program"))
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _hash(document),
        "instruction": instruction,
        "candidate_tables": tuple(dict.fromkeys(candidate_tables)),
        "skills_confirmation_required": tuple(skill["name"] for skill in AGENT_SKILLS),
        "requires_human_confirmation": True,
        "crud_mode": "governed_datastore_crud",
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def build_sample_interpretation_preview(state: dict | None, sample_code: str) -> dict:
    record = _copy_state(state)["records"][prefixed_table("pressure_quality_sample")].get(sample_code)
    if record is None:
        return {"ok": False, "reason": "unknown_sample", "sample_code": sample_code, "side_effects": ()}
    summary = record["summary"]
    return {
        "ok": True,
        "sample_code": sample_code,
        "narrative": "Sample review stays within the PBC boundary and cites owned sample evidence.",
        "evidence": {
            "pressure_psi": summary["pressure_psi"],
            "disinfectant_residual_mg_l": summary["disinfectant_residual_mg_l"],
            "turbidity_ntu": summary["turbidity_ntu"],
            "risk_reasons": summary["risk_reasons"],
        },
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def build_incident_narrative_preview(state: dict | None, incident_code: str) -> dict:
    record = _copy_state(state)["records"][prefixed_table("operations_incident")].get(incident_code)
    if record is None:
        return {"ok": False, "reason": "unknown_incident", "incident_code": incident_code, "side_effects": ()}
    summary = record["summary"]
    return {
        "ok": True,
        "incident_code": incident_code,
        "narrative": f"Incident {incident_code} is {summary['severity']} severity with {summary['command_center_lane']} command-center routing.",
        "evidence": summary,
        "requires_human_confirmation": True,
        "public_notice_submission_allowed": False,
        "side_effects": (),
    }


def route_specs() -> tuple[dict, ...]:
    return API_ROUTE_SPECS


def permission_surface() -> dict:
    action_permissions = {
        "configure_runtime": f"{PBC_KEY}.admin",
        "set_parameter": f"{PBC_KEY}.admin",
        "register_rule": f"{PBC_KEY}.admin",
        "register_schema_extension": f"{PBC_KEY}.admin",
        "receive_event": f"{PBC_KEY}.event",
        "query_workbench": f"{PBC_KEY}.read",
        "build_schema_contract": f"{PBC_KEY}.audit",
        "build_service_contract": f"{PBC_KEY}.audit",
        "build_release_evidence": f"{PBC_KEY}.audit",
        "run_advanced_assessment": f"{PBC_KEY}.read",
        "parse_document_instruction": f"{PBC_KEY}.read",
    }
    for operation in DOMAIN_OPERATIONS:
        action_permissions[operation] = f"{PBC_KEY}.operate"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.operate",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
            f"{PBC_KEY}.event",
            f"{PBC_KEY}.audit",
        ),
        "roles": ("operator", "approver", "compliance", "auditor"),
        "action_permissions": action_permissions,
        "side_effects": (),
    }


def verify_owned_table_boundary(references: tuple[str, ...] | list[str] | None) -> dict:
    references = tuple(references or ())
    violations = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not violations,
        "pbc": PBC_KEY,
        "violations": violations,
        "invalid_references": violations,
        "allowed_tables": OWNED_TABLES,
        "shared_table_access": False,
        "side_effects": (),
    }


def schema_table_contracts() -> tuple[dict, ...]:
    business = tuple(
        {
            "table": table,
            "fields": (
                "id",
                "tenant",
                "code",
                "status",
                "version",
                "payload",
                "summary",
                "projections",
                "evidence_hash",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in BUSINESS_TABLES
    )
    runtime = (
        {
            "table": RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "topic", "payload", "idempotency_key", "published_at", "audit_hash"),
            "primary_key": ("event_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "status", "audit_hash"),
            "primary_key": ("event_id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "reason", "audit_hash"),
            "primary_key": ("event_id",),
            "owned_by": PBC_KEY,
        },
    )
    return business + runtime


def schema_migration_contracts() -> tuple[dict, ...]:
    return tuple(
        {
            "path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql",
            "operation": "create_owned_table",
            "table": table["table"],
            "backend_allowlist": ALLOWED_DATABASE_BACKENDS,
        }
        for table in schema_table_contracts()
    )


def schema_model_contracts() -> tuple[dict, ...]:
    return tuple(
        {
            "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
            "table": table["table"],
            "fields": table["fields"],
        }
        for table in schema_table_contracts()
    )


def seed_records() -> tuple[dict, ...]:
    return (
        {"table": prefixed_table("treatment_plant"), "code": "PLANT-SEED", "status": "normal"},
        {"table": prefixed_table("distribution_zone"), "code": "ZONE-SEED", "status": "active"},
        {"table": prefixed_table("discharge_permit"), "code": "PERMIT-SEED", "status": "active"},
    )


def release_smoke_scenarios() -> dict:
    state = empty_state()
    state = configure_runtime(state, {"database_backend": "postgresql", "event_topic": REQUIRED_EVENT_TOPIC, "retry_limit": 5})["state"]
    state = set_parameter(state, "workbench_limit", 75)["state"]
    state = register_rule(state, {"rule_id": "permit_response", "policy_area": "sampling_compliance", "requires_confirmation": True})["state"]
    operation_payloads = (
        ("register_treatment_plant", {"tenant": "tenant_smoke", "plant_code": "WT-1", "plant_name": "North WTP", "utility_type": "drinking_water", "operating_state": "normal"}),
        ("configure_process_unit", {"tenant": "tenant_smoke", "plant_code": "WT-1", "unit_code": "DIS-1", "process_stage": "disinfection", "status": "online"}),
        ("record_pressure_quality_sample", {"tenant": "tenant_smoke", "sample_code": "SAMPLE-1", "zone_code": "ZONE-1", "sample_point": "DP-17", "collected_at": "2026-05-30T06:00:00Z", "pressure_psi": 28, "disinfectant_residual_mg_l": 0.12, "turbidity_ntu": 1.4, "chain_of_custody_complete": True, "holding_time_ok": True}),
        ("record_pump_operation", {"tenant": "tenant_smoke", "operation_code": "PUMP-1", "asset_code": "P-17", "plant_code": "WT-1", "status": "running", "runtime_hours": 22, "standby_available": False}),
        ("report_operations_incident", {"tenant": "tenant_smoke", "incident_code": "INC-1", "incident_type": "boil_water", "severity": "critical", "started_at": "2026-05-30T06:10:00Z", "affected_connections": 2400}),
        ("create_asset_isolation_plan", {"tenant": "tenant_smoke", "plan_code": "ISO-1", "asset_code": "MAIN-22", "valve_sequence": ("V-11", "V-12"), "affected_connections": 2400, "verification_complete": True}),
        ("project_scada_snapshot", {"tenant": "tenant_smoke", "projection_code": "SCADA-1", "asset_code": "LIFT-9", "captured_at": "2026-05-30T06:11:00Z", "freshness_minutes": 6, "tags": ("wet_well_level", "pump_a_status")}),
        ("register_discharge_permit", {"tenant": "tenant_smoke", "permit_code": "NPDES-9", "plant_code": "WWTP-4", "outfall_code": "001", "parameter_limits": {"bod_mg_l": 25, "tss_mg_l": 30}}),
        ("record_lab_compliance_case", {"tenant": "tenant_smoke", "case_code": "LAB-1", "sample_code": "SAMPLE-1", "parameter": "chlorine_residual", "result_value": 0.12, "limit_value": 0.2, "holding_time_ok": True, "chain_of_custody_complete": True}),
    )
    scenarios = []
    for operation, payload in operation_payloads:
        result = run_domain_operation(state, operation, payload)
        state = result["state"]
        scenarios.append({
            "operation": operation,
            "target_table": result["target_table"],
            "emitted_event": result["emitted_event"],
            "record_id": result["record"]["id"],
        })
    workbench = build_workbench_view(state, tenant="tenant_smoke")
    return {"ok": all(scenario["record_id"] for scenario in scenarios) and workbench["ok"], "scenarios": tuple(scenarios), "workbench": workbench, "state": state, "side_effects": ()}
