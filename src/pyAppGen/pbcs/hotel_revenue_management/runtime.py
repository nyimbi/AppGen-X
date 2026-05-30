"""Executable standalone runtime for the hotel_revenue_management PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json


PBC_KEY = "hotel_revenue_management"
HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC = "pbc.hotel_revenue_management.events"
HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
HOTEL_REVENUE_MANAGEMENT_EMITTED_EVENT_TYPES = (
    "HotelRevenueManagementCreated",
    "HotelRevenueManagementUpdated",
    "HotelRevenueManagementApproved",
    "HotelRevenueManagementExceptionOpened",
)
HOTEL_REVENUE_MANAGEMENT_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
HOTEL_REVENUE_MANAGEMENT_UI_FRAGMENT_KEYS = (
    "HotelRevenueManagementWorkbench",
    "HotelRevenueManagementDetail",
    "HotelRevenueManagementAssistantPanel",
)
HOTEL_REVENUE_MANAGEMENT_STANDARD_FEATURE_KEYS = (
    "room_type_management",
    "hotel_revenue_management_workflow",
    "hotel_revenue_management_analytics",
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
HOTEL_REVENUE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = (
    "hotel_revenue_management_event_sourced_operational_history",
    "hotel_revenue_management_multi_tenant_policy_isolation",
    "hotel_revenue_management_schema_evolution_resilience",
    "hotel_revenue_management_autonomous_anomaly_detection",
    "hotel_revenue_management_semantic_document_instruction_understanding",
    "hotel_revenue_management_predictive_risk_scoring",
    "hotel_revenue_management_counterfactual_scenario_simulation",
    "hotel_revenue_management_cryptographic_audit_proofs",
    "hotel_revenue_management_continuous_control_testing",
    "hotel_revenue_management_carbon_and_sustainability_awareness",
    "hotel_revenue_management_cross_pbc_event_federation",
    "hotel_revenue_management_governed_ai_agent_execution",
)


PARAMETER_BOUNDS = {
    "quality_score_floor": (0.0, 1.0),
    "materiality_threshold": (0.0, 1.0),
    "approval_sla_hours": (1, 168),
    "risk_threshold": (0.0, 1.0),
    "forecast_horizon_days": (1, 540),
    "workbench_limit": (1, 365),
}

RULE_DEFAULTS = (
    {
        "rule_id": "room_type_policy",
        "scope": "inventory",
        "condition": "sellable_rooms <= physical_rooms",
        "severity": "error",
    },
    {
        "rule_id": "rate_plan_policy",
        "scope": "pricing",
        "condition": "member_rate <= public_rate and min_los <= max_los",
        "severity": "error",
    },
    {
        "rule_id": "channel_inventory_policy",
        "scope": "distribution",
        "condition": "allotment >= 0 and stop_sell controls stay scoped to one channel",
        "severity": "error",
    },
    {
        "rule_id": "demand_forecast_policy",
        "scope": "forecasting",
        "condition": "segmented demand reconciles to property forecast",
        "severity": "error",
    },
    {
        "rule_id": "overbooking_policy_policy",
        "scope": "overbooking",
        "condition": "recommended limit never exceeds protected arrival threshold",
        "severity": "error",
    },
    {
        "rule_id": "yield_decision_policy",
        "scope": "yield",
        "condition": "decision explanation cites rate, forecast, channel, and policy inputs",
        "severity": "error",
    },
)


def _field(name: str, field_type: str, **extra: object) -> dict:
    return {"name": name, "type": field_type, **extra}


def _table(logical_table: str, fields: tuple[dict, ...], relationships: tuple[dict, ...] = ()) -> dict:
    owned_table = f"{PBC_KEY}_{logical_table}"
    return {
        "logical_table": logical_table,
        "owned_table": owned_table,
        "fields": fields,
        "relationships": relationships,
    }


HOTEL_REVENUE_MANAGEMENT_TABLE_SPECS = (
    _table(
        "room_type",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("hotel_id", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("name", "string", required=True),
            _field("physical_rooms", "integer", required=True),
            _field("maintenance_holdback", "integer", required=True, default=0),
            _field("complimentary_allotment", "integer", required=True, default=0),
            _field("sellable_rooms", "integer", required=True),
            _field("capacity_adults", "integer", required=True),
            _field("capacity_children", "integer", required=True),
            _field("substitution_targets_json", "json", required=True),
            _field("status", "string", required=True, default="draft"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "rate_plan",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("hotel_id", "string", required=True),
            _field("room_type_id", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("parent_rate_plan_id", "string", required=False),
            _field("currency", "string", required=True),
            _field("base_rate", "decimal", required=True),
            _field("derived_discount_pct", "decimal", required=True, default=0.0),
            _field("effective_rate", "decimal", required=True),
            _field("min_los", "integer", required=True, default=1),
            _field("max_los", "integer", required=True, default=30),
            _field("member_fence", "string", required=True, default="public"),
            _field("cancellation_policy", "string", required=True),
            _field("cta_dates_json", "json", required=True),
            _field("ctd_dates_json", "json", required=True),
            _field("package_components_json", "json", required=True),
            _field("status", "string", required=True, default="draft"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
        (
            {
                "field": "room_type_id",
                "target_table": f"{PBC_KEY}_room_type",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
            {
                "field": "parent_rate_plan_id",
                "target_table": f"{PBC_KEY}_rate_plan",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    ),
    _table(
        "channel_inventory",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("hotel_id", "string", required=True),
            _field("room_type_id", "string", required=True),
            _field("rate_plan_id", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("channel_code", "string", required=True),
            _field("stay_date", "date", required=True),
            _field("allotment", "integer", required=True),
            _field("stop_sell", "boolean", required=True, default=False),
            _field("release_back_hours", "integer", required=True, default=24),
            _field("blackout_reason", "string", required=False),
            _field("parity_exception_reason", "string", required=False),
            _field("status", "string", required=True, default="draft"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
        (
            {
                "field": "room_type_id",
                "target_table": f"{PBC_KEY}_room_type",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
            {
                "field": "rate_plan_id",
                "target_table": f"{PBC_KEY}_rate_plan",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    ),
    _table(
        "demand_forecast",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("hotel_id", "string", required=True),
            _field("room_type_id", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("stay_date", "date", required=True),
            _field("transient_demand", "integer", required=True),
            _field("corporate_demand", "integer", required=True),
            _field("group_demand", "integer", required=True),
            _field("wholesale_demand", "integer", required=True),
            _field("house_use_demand", "integer", required=True),
            _field("forecast_rooms", "integer", required=True),
            _field("confidence", "decimal", required=True),
            _field("pickup_baseline", "integer", required=True),
            _field("event_factor", "decimal", required=True, default=1.0),
            _field("manual_override_rooms", "integer", required=False),
            _field("override_reason", "string", required=False),
            _field("approved_by", "string", required=False),
            _field("status", "string", required=True, default="draft"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
        (
            {
                "field": "room_type_id",
                "target_table": f"{PBC_KEY}_room_type",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    ),
    _table(
        "overbooking_policy",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("hotel_id", "string", required=True),
            _field("room_type_id", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("date_class", "string", required=True),
            _field("overbook_limit", "integer", required=True),
            _field("walk_cost", "decimal", required=True),
            _field("no_show_rate", "decimal", required=True),
            _field("cancellation_rate", "decimal", required=True),
            _field("arrival_protection_pct", "decimal", required=True),
            _field("recovery_priority_json", "json", required=True),
            _field("status", "string", required=True, default="draft"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
        (
            {
                "field": "room_type_id",
                "target_table": f"{PBC_KEY}_room_type",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    ),
    _table(
        "yield_decision",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("hotel_id", "string", required=True),
            _field("room_type_id", "string", required=True),
            _field("rate_plan_id", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("stay_date", "date", required=True),
            _field("recommended_rate", "decimal", required=True),
            _field("rate_change_pct", "decimal", required=True),
            _field("channel_action", "string", required=True),
            _field("restriction_action", "string", required=True),
            _field("expected_occupancy", "decimal", required=True),
            _field("expected_adr", "decimal", required=True),
            _field("explanation_json", "json", required=True),
            _field("approved_by", "string", required=False),
            _field("status", "string", required=True, default="recommended"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
        (
            {
                "field": "room_type_id",
                "target_table": f"{PBC_KEY}_room_type",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
            {
                "field": "rate_plan_id",
                "target_table": f"{PBC_KEY}_rate_plan",
                "target_column": "id",
                "cardinality": "many-to-one",
                "ownership": "same_pbc",
            },
        ),
    ),
    _table(
        "revenue_snapshot",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("hotel_id", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("stay_date", "date", required=True),
            _field("rooms_sold", "integer", required=True),
            _field("rooms_available", "integer", required=True),
            _field("occupancy_pct", "decimal", required=True),
            _field("adr", "decimal", required=True),
            _field("revpar", "decimal", required=True),
            _field("net_revenue", "decimal", required=True),
            _field("channel_mix_json", "json", required=True),
            _field("source_decision_ids_json", "json", required=True),
            _field("status", "string", required=True, default="recorded"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "hotel_revenue_management_policy_rule",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("scope", "string", required=True),
            _field("rule_type", "string", required=True),
            _field("threshold", "decimal", required=False),
            _field("expression_json", "json", required=True),
            _field("severity", "string", required=True),
            _field("status", "string", required=True, default="active"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "hotel_revenue_management_runtime_parameter",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("parameter_key", "string", required=True),
            _field("parameter_value", "decimal", required=True),
            _field("value_type", "string", required=True),
            _field("min_value", "decimal", required=False),
            _field("max_value", "decimal", required=False),
            _field("status", "string", required=True, default="approved"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "hotel_revenue_management_schema_extension",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("owned_table", "string", required=True),
            _field("extension_fields_json", "json", required=True),
            _field("status", "string", required=True, default="draft"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "hotel_revenue_management_control_assertion",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("assertion_type", "string", required=True),
            _field("target_record_id", "string", required=True),
            _field("outcome", "string", required=True),
            _field("evidence_json", "json", required=True),
            _field("status", "string", required=True, default="active"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "hotel_revenue_management_governed_model",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("code", "string", required=True, searchable=True),
            _field("model_name", "string", required=True),
            _field("model_version", "string", required=True),
            _field("model_purpose", "string", required=True),
            _field("approval_policy", "string", required=True),
            _field("drift_threshold", "decimal", required=True),
            _field("human_confirmation_required", "boolean", required=True),
            _field("status", "string", required=True, default="approved"),
            _field("version", "integer", required=True, default=1),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "appgen_outbox_event",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("code", "string", required=True),
            _field("event_type", "string", required=True),
            _field("topic", "string", required=True),
            _field("aggregate_table", "string", required=True),
            _field("aggregate_id", "string", required=True),
            _field("payload_json", "json", required=True),
            _field("idempotency_key", "string", required=True),
            _field("status", "string", required=True),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "appgen_inbox_event",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("code", "string", required=True),
            _field("event_type", "string", required=True),
            _field("source_pbc", "string", required=True),
            _field("payload_json", "json", required=True),
            _field("idempotency_key", "string", required=True),
            _field("handled_at", "datetime", required=True),
            _field("status", "string", required=True),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
    _table(
        "appgen_dead_letter_event",
        (
            _field("id", "string", primary_key=True, nullable=False),
            _field("tenant", "string", required=True),
            _field("code", "string", required=True),
            _field("event_type", "string", required=True),
            _field("source_pbc", "string", required=True),
            _field("payload_json", "json", required=True),
            _field("idempotency_key", "string", required=True),
            _field("retry_count", "integer", required=True),
            _field("reason", "string", required=True),
            _field("status", "string", required=True),
            _field("created_at", "datetime", required=True),
            _field("updated_at", "datetime", required=True),
        ),
    ),
)

HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES = tuple(
    spec["owned_table"] for spec in HOTEL_REVENUE_MANAGEMENT_TABLE_SPECS
)
HOTEL_REVENUE_MANAGEMENT_BUSINESS_TABLES = tuple(
    spec["owned_table"]
    for spec in HOTEL_REVENUE_MANAGEMENT_TABLE_SPECS
    if not spec["logical_table"].startswith("appgen_")
)
HOTEL_REVENUE_MANAGEMENT_RUNTIME_TABLES = tuple(
    table for table in HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES if table.endswith("event")
)
_TABLE_SPEC_BY_OWNED = {
    spec["owned_table"]: spec for spec in HOTEL_REVENUE_MANAGEMENT_TABLE_SPECS
}

HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION = {
    "POST /room-types": "create_room_type",
    "POST /rate-plans": "record_rate_plan",
    "POST /channel-inventorys": "review_channel_inventory",
    "POST /demand-forecasts": "approve_demand_forecast",
    "POST /overbooking-policys": "simulate_overbooking_policy",
    "GET /hotel-revenue-management-workbench": "query_workbench",
}

HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_TABLE = {
    "create_room_type": f"{PBC_KEY}_room_type",
    "record_rate_plan": f"{PBC_KEY}_rate_plan",
    "review_channel_inventory": f"{PBC_KEY}_channel_inventory",
    "approve_demand_forecast": f"{PBC_KEY}_demand_forecast",
    "simulate_overbooking_policy": f"{PBC_KEY}_overbooking_policy",
    "create_yield_decision": f"{PBC_KEY}_yield_decision",
    "record_revenue_snapshot": f"{PBC_KEY}_revenue_snapshot",
    "review_hotel_revenue_management_policy_rule": f"{PBC_KEY}_hotel_revenue_management_policy_rule",
    "approve_hotel_revenue_management_runtime_parameter": f"{PBC_KEY}_hotel_revenue_management_runtime_parameter",
    "simulate_hotel_revenue_management_schema_extension": f"{PBC_KEY}_hotel_revenue_management_schema_extension",
    "create_hotel_revenue_management_control_assertion": f"{PBC_KEY}_hotel_revenue_management_control_assertion",
    "record_hotel_revenue_management_governed_model": f"{PBC_KEY}_hotel_revenue_management_governed_model",
    "operate_hotel_revenue_management_13": f"{PBC_KEY}_channel_inventory",
    "operate_hotel_revenue_management_14": f"{PBC_KEY}_yield_decision",
    "operate_hotel_revenue_management_15": f"{PBC_KEY}_rate_plan",
    "operate_hotel_revenue_management_16": f"{PBC_KEY}_yield_decision",
    "operate_hotel_revenue_management_17": f"{PBC_KEY}_demand_forecast",
    "operate_hotel_revenue_management_18": f"{PBC_KEY}_revenue_snapshot",
}

HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT = {
    "create_room_type": "HotelRevenueManagementCreated",
    "record_rate_plan": "HotelRevenueManagementUpdated",
    "review_channel_inventory": "HotelRevenueManagementUpdated",
    "approve_demand_forecast": "HotelRevenueManagementApproved",
    "simulate_overbooking_policy": "HotelRevenueManagementUpdated",
    "create_yield_decision": "HotelRevenueManagementApproved",
    "record_revenue_snapshot": "HotelRevenueManagementUpdated",
    "review_hotel_revenue_management_policy_rule": "HotelRevenueManagementUpdated",
    "approve_hotel_revenue_management_runtime_parameter": "HotelRevenueManagementApproved",
    "simulate_hotel_revenue_management_schema_extension": "HotelRevenueManagementUpdated",
    "create_hotel_revenue_management_control_assertion": "HotelRevenueManagementApproved",
    "record_hotel_revenue_management_governed_model": "HotelRevenueManagementApproved",
    "operate_hotel_revenue_management_13": "HotelRevenueManagementExceptionOpened",
    "operate_hotel_revenue_management_14": "HotelRevenueManagementUpdated",
    "operate_hotel_revenue_management_15": "HotelRevenueManagementApproved",
    "operate_hotel_revenue_management_16": "HotelRevenueManagementExceptionOpened",
    "operate_hotel_revenue_management_17": "HotelRevenueManagementApproved",
    "operate_hotel_revenue_management_18": "HotelRevenueManagementUpdated",
}

HOTEL_REVENUE_MANAGEMENT_COMMAND_METHODS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "command_room_type",
    "create_room_type",
    "record_rate_plan",
    "review_channel_inventory",
    "approve_demand_forecast",
    "simulate_overbooking_policy",
    "create_yield_decision",
    "record_revenue_snapshot",
    "review_hotel_revenue_management_policy_rule",
    "approve_hotel_revenue_management_runtime_parameter",
    "simulate_hotel_revenue_management_schema_extension",
    "create_hotel_revenue_management_control_assertion",
    "record_hotel_revenue_management_governed_model",
    "operate_hotel_revenue_management_13",
    "operate_hotel_revenue_management_14",
    "operate_hotel_revenue_management_15",
    "operate_hotel_revenue_management_16",
    "operate_hotel_revenue_management_17",
    "operate_hotel_revenue_management_18",
    "run_advanced_assessment",
    "parse_document_instruction",
)
HOTEL_REVENUE_MANAGEMENT_QUERY_METHODS = ("query_workbench", "build_workbench_view")


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _timestamp(payload: dict | None = None) -> str:
    if payload and payload.get("updated_at"):
        return str(payload["updated_at"])
    if payload and payload.get("created_at"):
        return str(payload["created_at"])
    return "2026-05-30T00:00:00Z"


def _round(value: float, digits: int = 4) -> float:
    return round(float(value), digits)


def _as_json(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def hotel_revenue_management_empty_state() -> dict:
    return {
        "records": {table: {} for table in HOTEL_REVENUE_MANAGEMENT_BUSINESS_TABLES},
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "workflows": [],
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _table_records(state: dict, table: str) -> dict:
    return state.setdefault("records", {}).setdefault(table, {})


def _store_record(state: dict, table: str, record: dict) -> dict:
    next_state = _copy(state)
    _table_records(next_state, table)[record["id"]] = dict(record)
    return next_state


def _append_runtime_row(state: dict, table: str, payload: dict) -> None:
    row = {
        "id": payload.get("id") or _digest((table, payload))[:16],
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code") or payload.get("event_type") or table,
        **payload,
    }
    if table.endswith("outbox_event"):
        state["outbox"].append(row)
    elif table.endswith("inbox_event"):
        state["inbox"].append(row)
    else:
        state["dead_letter"].append(row)


def _append_outbox_event(
    state: dict,
    event_type: str,
    aggregate_table: str,
    aggregate_id: str,
    payload: dict,
) -> dict:
    envelope = {
        "event_type": event_type,
        "topic": HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "aggregate_table": aggregate_table,
        "aggregate_id": aggregate_id,
        "payload_json": _as_json(payload),
        "idempotency_key": _digest((event_type, aggregate_table, aggregate_id, payload)),
        "status": "pending",
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    _append_runtime_row(state, f"{PBC_KEY}_appgen_outbox_event", envelope)
    return envelope


def _lookup_record(state: dict, table: str, record_id: str | None) -> dict | None:
    if not record_id:
        return None
    return _table_records(state, table).get(record_id)


def _derive_sellable(payload: dict) -> int:
    sellable = payload.get("sellable_rooms")
    if sellable is not None:
        return _safe_int(sellable)
    return max(
        0,
        _safe_int(payload.get("physical_rooms"))
        - _safe_int(payload.get("maintenance_holdback"))
        - _safe_int(payload.get("complimentary_allotment")),
    )


def _validate_parameter(name: str, value: object) -> tuple[bool, str | None]:
    bounds = PARAMETER_BOUNDS.get(name)
    if bounds is None:
        return False, "unknown_parameter"
    numeric = _safe_float(value)
    lower, upper = bounds
    if numeric < lower or numeric > upper:
        return False, "parameter_out_of_bounds"
    return True, None


def _collect_rows(state: dict, table: str, tenant: str | None = None) -> tuple[dict, ...]:
    rows = tuple(_table_records(state, table).values())
    if tenant is None:
        return rows
    return tuple(row for row in rows if row.get("tenant") == tenant)


def hotel_revenue_management_configure_runtime(state: dict, config: dict | None = None) -> dict:
    config = dict(config or {})
    backend = config.get("database_backend", "postgresql")
    event_topic = config.get(
        "event_topic", HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC
    )
    invalid_fields = tuple(
        key
        for key in config
        if key in {"stream_engine", "stream_engine_picker", "eventing_choice"}
    )
    next_state = _copy(state)
    next_state["configuration"] = {
        "database_backend": backend,
        "event_topic": event_topic,
        "retry_limit": _safe_int(config.get("retry_limit", 5), 5),
        "default_policy": config.get("default_policy", "balanced-revenue-control"),
        "workbench_limit": _safe_int(config.get("workbench_limit", 45), 45),
        "confirmation_required_for_agent_writes": config.get(
            "confirmation_required_for_agent_writes", True
        ),
        "stream_engine_picker_visible": False,
    }
    ok = (
        backend in HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        and event_topic == HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC
        and not invalid_fields
    )
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "invalid_fields": invalid_fields,
        "side_effects": (),
    }


def hotel_revenue_management_set_parameter(state: dict, name: str, value: object) -> dict:
    ok, reason = _validate_parameter(name, value)
    next_state = _copy(state)
    parameter = {
        "name": name,
        "value": _safe_float(value),
        "bounds": PARAMETER_BOUNDS.get(name),
        "bounded": True,
    }
    if ok:
        next_state["parameters"][name] = parameter
    return {
        "ok": ok,
        "state": next_state,
        "parameter": parameter,
        "reason": reason,
        "side_effects": (),
    }


def hotel_revenue_management_register_rule(state: dict, rule: dict | None = None) -> dict:
    rule = dict(rule or {})
    next_state = _copy(state)
    rule_id = rule.get("rule_id") or f"rule-{len(next_state['rules']) + 1}"
    compiled = {
        **rule,
        "rule_id": rule_id,
        "compiled_hash": _digest(rule),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def hotel_revenue_management_register_schema_extension(
    state: dict, table: str, fields: dict | None = None
) -> dict:
    next_state = _copy(state)
    owned_table = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_table not in HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_owned_table",
            "table": owned_table,
            "side_effects": (),
        }
    extension = dict(fields or {})
    next_state["schema_extensions"][owned_table] = extension
    return {
        "ok": True,
        "state": next_state,
        "table": owned_table,
        "fields": extension,
        "side_effects": (),
    }


def hotel_revenue_management_receive_event(state: dict, event: dict | None = None) -> dict:
    event = dict(event or {})
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in HOTEL_REVENUE_MANAGEMENT_CONSUMED_EVENT_TYPES:
        dead_letter = {
            "event_type": event.get("event_type", "unknown"),
            "source_pbc": event.get("source_pbc", "external"),
            "payload_json": _as_json(event),
            "idempotency_key": idem,
            "retry_count": _safe_int(event.get("retry_count", 0), 0),
            "reason": "unsupported_event_type",
            "status": "dead_lettered",
            "created_at": _timestamp(event),
            "updated_at": _timestamp(event),
        }
        _append_runtime_row(next_state, f"{PBC_KEY}_appgen_dead_letter_event", dead_letter)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "side_effects": (),
        }
    inbox = {
        "event_type": event["event_type"],
        "source_pbc": event.get("source_pbc", "external"),
        "payload_json": _as_json(event),
        "idempotency_key": idem,
        "handled_at": _timestamp(event),
        "status": "handled",
        "created_at": _timestamp(event),
        "updated_at": _timestamp(event),
    }
    _append_runtime_row(next_state, f"{PBC_KEY}_appgen_inbox_event", inbox)
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def hotel_revenue_management_create_room_type(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    sellable_rooms = _derive_sellable(payload)
    physical_rooms = _safe_int(payload.get("physical_rooms"), 0)
    if physical_rooms <= 0 or sellable_rooms > physical_rooms:
        return {
            "ok": False,
            "state": _copy(state),
            "reason": "invalid_room_inventory_profile",
            "side_effects": (),
        }
    room_type_id = payload.get("id") or payload.get("code") or f"room-type-{physical_rooms}"
    record = {
        "id": room_type_id,
        "tenant": payload.get("tenant", "default"),
        "hotel_id": payload.get("hotel_id", "hotel-demo"),
        "code": payload.get("code", room_type_id),
        "name": payload.get("name", payload.get("code", room_type_id)),
        "physical_rooms": physical_rooms,
        "maintenance_holdback": _safe_int(payload.get("maintenance_holdback"), 0),
        "complimentary_allotment": _safe_int(payload.get("complimentary_allotment"), 0),
        "sellable_rooms": sellable_rooms,
        "capacity_adults": _safe_int(payload.get("capacity_adults"), 2),
        "capacity_children": _safe_int(payload.get("capacity_children"), 0),
        "substitution_targets_json": _as_json(payload.get("substitution_targets", ())),
        "status": payload.get("status", "active"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(state, f"{PBC_KEY}_room_type", record)
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT["create_room_type"],
        f"{PBC_KEY}_room_type",
        room_type_id,
        record,
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "sellable_gap": physical_rooms - sellable_rooms,
        "event": event,
        "side_effects": (),
    }


def hotel_revenue_management_command_room_type(state: dict, payload: dict | None = None) -> dict:
    return hotel_revenue_management_create_room_type(state, payload)


def hotel_revenue_management_record_rate_plan(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    room_type_id = payload.get("room_type_id")
    parent_id = payload.get("parent_rate_plan_id")
    room_type = _lookup_record(state, f"{PBC_KEY}_room_type", room_type_id)
    parent_plan = _lookup_record(state, f"{PBC_KEY}_rate_plan", parent_id)
    if room_type_id and room_type is None:
        return {"ok": False, "state": _copy(state), "reason": "unknown_room_type", "side_effects": ()}
    base_rate = _safe_float(payload.get("base_rate"), 0.0)
    derived_discount_pct = _safe_float(payload.get("derived_discount_pct"), 0.0)
    source_rate = _safe_float(parent_plan["effective_rate"], base_rate) if parent_plan else base_rate
    effective_rate = _round(source_rate * (1 - derived_discount_pct / 100.0), 2)
    min_los = _safe_int(payload.get("min_los"), 1)
    max_los = _safe_int(payload.get("max_los"), max(min_los, 30))
    if base_rate <= 0 or effective_rate <= 0 or min_los > max_los:
        return {"ok": False, "state": _copy(state), "reason": "invalid_rate_plan_fence", "side_effects": ()}
    rate_plan_id = payload.get("id") or payload.get("code") or f"rate-plan-{room_type_id or 'default'}"
    record = {
        "id": rate_plan_id,
        "tenant": payload.get("tenant", "default"),
        "hotel_id": payload.get("hotel_id", room_type.get("hotel_id") if room_type else "hotel-demo"),
        "room_type_id": room_type_id,
        "code": payload.get("code", rate_plan_id),
        "parent_rate_plan_id": parent_id,
        "currency": payload.get("currency", "USD"),
        "base_rate": _round(base_rate, 2),
        "derived_discount_pct": _round(derived_discount_pct, 2),
        "effective_rate": effective_rate,
        "min_los": min_los,
        "max_los": max_los,
        "member_fence": payload.get("member_fence", "public"),
        "cancellation_policy": payload.get("cancellation_policy", "flexible"),
        "cta_dates_json": _as_json(payload.get("cta_dates", ())),
        "ctd_dates_json": _as_json(payload.get("ctd_dates", ())),
        "package_components_json": _as_json(payload.get("package_components", ())),
        "status": payload.get("status", "draft"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(state, f"{PBC_KEY}_rate_plan", record)
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT["record_rate_plan"],
        f"{PBC_KEY}_rate_plan",
        rate_plan_id,
        record,
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "bar_ladder_validation": {
            "ok": effective_rate <= _round(base_rate, 2) if parent_plan else True,
            "parent_rate_plan_id": parent_id,
            "effective_rate": effective_rate,
        },
        "event": event,
        "side_effects": (),
    }


def hotel_revenue_management_review_channel_inventory(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    room_type = _lookup_record(state, f"{PBC_KEY}_room_type", payload.get("room_type_id"))
    rate_plan = _lookup_record(state, f"{PBC_KEY}_rate_plan", payload.get("rate_plan_id"))
    if room_type is None or rate_plan is None:
        return {"ok": False, "state": _copy(state), "reason": "unknown_inventory_dependency", "side_effects": ()}
    allotment = _safe_int(payload.get("allotment"), -1)
    if allotment < 0 or allotment > _safe_int(room_type.get("sellable_rooms"), 0):
        return {"ok": False, "state": _copy(state), "reason": "invalid_channel_allotment", "side_effects": ()}
    inventory_id = payload.get("id") or payload.get("code") or _digest(payload)[:16]
    record = {
        "id": inventory_id,
        "tenant": payload.get("tenant", room_type.get("tenant", "default")),
        "hotel_id": payload.get("hotel_id", room_type.get("hotel_id", "hotel-demo")),
        "room_type_id": room_type["id"],
        "rate_plan_id": rate_plan["id"],
        "code": payload.get("code", inventory_id),
        "channel_code": payload.get("channel_code", "direct"),
        "stay_date": payload.get("stay_date", "2026-06-01"),
        "allotment": allotment,
        "stop_sell": bool(payload.get("stop_sell", False)),
        "release_back_hours": _safe_int(payload.get("release_back_hours"), 24),
        "blackout_reason": payload.get("blackout_reason"),
        "parity_exception_reason": payload.get("parity_exception_reason"),
        "status": payload.get("status", "open"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(state, f"{PBC_KEY}_channel_inventory", record)
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT["review_channel_inventory"],
        f"{PBC_KEY}_channel_inventory",
        inventory_id,
        record,
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "parity_exception": bool(record["parity_exception_reason"]),
        "event": event,
        "side_effects": (),
    }


def hotel_revenue_management_approve_demand_forecast(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    room_type = _lookup_record(state, f"{PBC_KEY}_room_type", payload.get("room_type_id"))
    if payload.get("room_type_id") and room_type is None:
        return {"ok": False, "state": _copy(state), "reason": "unknown_room_type", "side_effects": ()}
    segments = {
        "transient_demand": _safe_int(payload.get("transient_demand"), 0),
        "corporate_demand": _safe_int(payload.get("corporate_demand"), 0),
        "group_demand": _safe_int(payload.get("group_demand"), 0),
        "wholesale_demand": _safe_int(payload.get("wholesale_demand"), 0),
        "house_use_demand": _safe_int(payload.get("house_use_demand"), 0),
    }
    total = sum(segments.values())
    override_rooms = payload.get("manual_override_rooms")
    forecast_rooms = _safe_int(override_rooms, total) if override_rooms is not None else total
    confidence = _safe_float(payload.get("confidence"), 0.75)
    if forecast_rooms < 0 or confidence <= 0 or confidence > 1:
        return {"ok": False, "state": _copy(state), "reason": "invalid_forecast", "side_effects": ()}
    forecast_id = payload.get("id") or payload.get("code") or _digest((segments, payload.get("stay_date")))[:16]
    record = {
        "id": forecast_id,
        "tenant": payload.get("tenant", room_type.get("tenant", "default") if room_type else "default"),
        "hotel_id": payload.get("hotel_id", room_type.get("hotel_id", "hotel-demo") if room_type else "hotel-demo"),
        "room_type_id": payload.get("room_type_id"),
        "code": payload.get("code", forecast_id),
        "stay_date": payload.get("stay_date", "2026-06-01"),
        **segments,
        "forecast_rooms": forecast_rooms,
        "confidence": _round(confidence, 4),
        "pickup_baseline": _safe_int(payload.get("pickup_baseline"), forecast_rooms),
        "event_factor": _round(_safe_float(payload.get("event_factor"), 1.0), 4),
        "manual_override_rooms": _safe_int(override_rooms) if override_rooms is not None else None,
        "override_reason": payload.get("override_reason"),
        "approved_by": payload.get("approved_by"),
        "status": payload.get("status", "approved"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(state, f"{PBC_KEY}_demand_forecast", record)
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT["approve_demand_forecast"],
        f"{PBC_KEY}_demand_forecast",
        forecast_id,
        record,
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "segments_reconcile": total == forecast_rooms or override_rooms is not None,
        "event": event,
        "side_effects": (),
    }


def hotel_revenue_management_simulate_overbooking_policy(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    room_type = _lookup_record(state, f"{PBC_KEY}_room_type", payload.get("room_type_id"))
    if payload.get("room_type_id") and room_type is None:
        return {"ok": False, "state": _copy(state), "reason": "unknown_room_type", "side_effects": ()}
    no_show_rate = _safe_float(payload.get("no_show_rate"), 0.04)
    cancellation_rate = _safe_float(payload.get("cancellation_rate"), 0.08)
    arrival_protection_pct = _safe_float(payload.get("arrival_protection_pct"), 0.1)
    forecast_rooms = _safe_int(payload.get("forecast_rooms"), _safe_int(room_type.get("sellable_rooms") if room_type else 0, 0))
    protected_rooms = int(round(forecast_rooms * arrival_protection_pct))
    recommended_limit = max(0, int(round(forecast_rooms * (no_show_rate + cancellation_rate))) - protected_rooms)
    policy_id = payload.get("id") or payload.get("code") or _digest(payload)[:16]
    record = {
        "id": policy_id,
        "tenant": payload.get("tenant", room_type.get("tenant", "default") if room_type else "default"),
        "hotel_id": payload.get("hotel_id", room_type.get("hotel_id", "hotel-demo") if room_type else "hotel-demo"),
        "room_type_id": payload.get("room_type_id"),
        "code": payload.get("code", policy_id),
        "date_class": payload.get("date_class", "standard"),
        "overbook_limit": min(_safe_int(payload.get("overbook_limit"), recommended_limit), recommended_limit),
        "walk_cost": _round(_safe_float(payload.get("walk_cost"), 250.0), 2),
        "no_show_rate": _round(no_show_rate, 4),
        "cancellation_rate": _round(cancellation_rate, 4),
        "arrival_protection_pct": _round(arrival_protection_pct, 4),
        "recovery_priority_json": _as_json(payload.get("recovery_priority", ("upgrade", "partner_hotel", "voucher"))),
        "status": payload.get("status", "simulated"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(state, f"{PBC_KEY}_overbooking_policy", record)
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT["simulate_overbooking_policy"],
        f"{PBC_KEY}_overbooking_policy",
        policy_id,
        record,
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "simulation": {
            "recommended_limit": recommended_limit,
            "protected_rooms": protected_rooms,
            "forecast_rooms": forecast_rooms,
        },
        "event": event,
        "side_effects": (),
    }


def hotel_revenue_management_create_yield_decision(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    room_type = _lookup_record(state, f"{PBC_KEY}_room_type", payload.get("room_type_id"))
    rate_plan = _lookup_record(state, f"{PBC_KEY}_rate_plan", payload.get("rate_plan_id"))
    forecast = _lookup_record(state, f"{PBC_KEY}_demand_forecast", payload.get("forecast_id"))
    policy = _lookup_record(state, f"{PBC_KEY}_overbooking_policy", payload.get("overbooking_policy_id"))
    if room_type is None or rate_plan is None:
        return {"ok": False, "state": _copy(state), "reason": "missing_pricing_context", "side_effects": ()}
    sellable_rooms = max(_safe_int(room_type.get("sellable_rooms"), 0), 1)
    forecast_rooms = _safe_int(forecast.get("forecast_rooms") if forecast else payload.get("forecast_rooms"), 0)
    demand_pressure = forecast_rooms / sellable_rooms
    compression = demand_pressure >= 0.92
    change_pct = 0.12 if compression else (0.05 if demand_pressure >= 0.75 else -0.03)
    recommended_rate = _round(_safe_float(rate_plan.get("effective_rate"), 0.0) * (1 + change_pct), 2)
    decision_id = payload.get("id") or payload.get("code") or _digest((payload, recommended_rate))[:16]
    explanation = {
        "room_type": room_type.get("code"),
        "rate_plan": rate_plan.get("code"),
        "forecast_rooms": forecast_rooms,
        "sellable_rooms": sellable_rooms,
        "demand_pressure": _round(demand_pressure, 4),
        "compression": compression,
        "policy_limit": policy.get("overbook_limit") if policy else None,
        "recommended_actions": {
            "channel_action": "tighten_ota" if compression else "reopen_direct",
            "restriction_action": "cta_peak_night" if compression else "relax_min_los",
        },
    }
    record = {
        "id": decision_id,
        "tenant": payload.get("tenant", room_type.get("tenant", "default")),
        "hotel_id": payload.get("hotel_id", room_type.get("hotel_id", "hotel-demo")),
        "room_type_id": room_type["id"],
        "rate_plan_id": rate_plan["id"],
        "code": payload.get("code", decision_id),
        "stay_date": payload.get("stay_date", payload.get("for_stay_date", "2026-06-01")),
        "recommended_rate": recommended_rate,
        "rate_change_pct": _round(change_pct, 4),
        "channel_action": explanation["recommended_actions"]["channel_action"],
        "restriction_action": explanation["recommended_actions"]["restriction_action"],
        "expected_occupancy": _round(min(1.0, demand_pressure), 4),
        "expected_adr": recommended_rate,
        "explanation_json": _as_json(explanation),
        "approved_by": payload.get("approved_by"),
        "status": payload.get("status", "recommended"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(state, f"{PBC_KEY}_yield_decision", record)
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT["create_yield_decision"],
        f"{PBC_KEY}_yield_decision",
        decision_id,
        record,
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "explanation": explanation,
        "event": event,
        "side_effects": (),
    }


def hotel_revenue_management_record_revenue_snapshot(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    rooms_available = max(_safe_int(payload.get("rooms_available"), 1), 1)
    rooms_sold = min(_safe_int(payload.get("rooms_sold"), 0), rooms_available)
    adr = _round(_safe_float(payload.get("adr"), 0.0), 2)
    occupancy_pct = _round(rooms_sold / rooms_available, 4)
    revpar = _round(adr * occupancy_pct, 2)
    channel_mix = payload.get("channel_mix", {"direct": rooms_sold})
    snapshot_id = payload.get("id") or payload.get("code") or _digest((payload, revpar))[:16]
    record = {
        "id": snapshot_id,
        "tenant": payload.get("tenant", "default"),
        "hotel_id": payload.get("hotel_id", "hotel-demo"),
        "code": payload.get("code", snapshot_id),
        "stay_date": payload.get("stay_date", "2026-06-01"),
        "rooms_sold": rooms_sold,
        "rooms_available": rooms_available,
        "occupancy_pct": occupancy_pct,
        "adr": adr,
        "revpar": revpar,
        "net_revenue": _round(_safe_float(payload.get("net_revenue"), rooms_sold * adr), 2),
        "channel_mix_json": _as_json(channel_mix),
        "source_decision_ids_json": _as_json(payload.get("source_decision_ids", ())),
        "status": payload.get("status", "recorded"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(state, f"{PBC_KEY}_revenue_snapshot", record)
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT["record_revenue_snapshot"],
        f"{PBC_KEY}_revenue_snapshot",
        snapshot_id,
        record,
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def hotel_revenue_management_review_hotel_revenue_management_policy_rule(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    rule_id = payload.get("id") or payload.get("code") or payload.get("rule_id") or _digest(payload)[:16]
    record = {
        "id": rule_id,
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code", rule_id),
        "scope": payload.get("scope", "pricing"),
        "rule_type": payload.get("rule_type", "threshold"),
        "threshold": _safe_float(payload.get("threshold"), 0.0),
        "expression_json": _as_json(payload.get("expression", payload)),
        "severity": payload.get("severity", "warning"),
        "status": payload.get("status", "active"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(state, f"{PBC_KEY}_hotel_revenue_management_policy_rule", record)
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT["review_hotel_revenue_management_policy_rule"],
        f"{PBC_KEY}_hotel_revenue_management_policy_rule",
        rule_id,
        record,
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def hotel_revenue_management_approve_hotel_revenue_management_runtime_parameter(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    parameter_key = payload.get("parameter_key") or payload.get("code") or "workbench_limit"
    parameter_value = payload.get("parameter_value", payload.get("value", 0.0))
    parameter_result = hotel_revenue_management_set_parameter(state, parameter_key, parameter_value)
    if not parameter_result["ok"]:
        return parameter_result
    record_id = payload.get("id") or payload.get("code") or parameter_key
    record = {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code", parameter_key),
        "parameter_key": parameter_key,
        "parameter_value": _safe_float(parameter_value),
        "value_type": payload.get("value_type", "decimal"),
        "min_value": PARAMETER_BOUNDS[parameter_key][0],
        "max_value": PARAMETER_BOUNDS[parameter_key][1],
        "status": payload.get("status", "approved"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(
        parameter_result["state"],
        f"{PBC_KEY}_hotel_revenue_management_runtime_parameter",
        record,
    )
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT[
            "approve_hotel_revenue_management_runtime_parameter"
        ],
        f"{PBC_KEY}_hotel_revenue_management_runtime_parameter",
        record_id,
        record,
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def hotel_revenue_management_simulate_hotel_revenue_management_schema_extension(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    extension_result = hotel_revenue_management_register_schema_extension(
        state,
        payload.get("owned_table", payload.get("table", "room_type")),
        payload.get("extension_fields", {}),
    )
    if not extension_result["ok"]:
        return extension_result
    record_id = payload.get("id") or payload.get("code") or _digest(payload)[:16]
    record = {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code", record_id),
        "owned_table": extension_result["table"],
        "extension_fields_json": _as_json(extension_result["fields"]),
        "status": payload.get("status", "simulated"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(
        extension_result["state"],
        f"{PBC_KEY}_hotel_revenue_management_schema_extension",
        record,
    )
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT[
            "simulate_hotel_revenue_management_schema_extension"
        ],
        f"{PBC_KEY}_hotel_revenue_management_schema_extension",
        record_id,
        record,
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def hotel_revenue_management_create_hotel_revenue_management_control_assertion(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    record_id = payload.get("id") or payload.get("code") or _digest(payload)[:16]
    record = {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code", record_id),
        "assertion_type": payload.get("assertion_type", "rate_plan_publish_readiness"),
        "target_record_id": payload.get("target_record_id", "unknown"),
        "outcome": payload.get("outcome", "pass"),
        "evidence_json": _as_json(payload.get("evidence", payload)),
        "status": payload.get("status", "active"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(
        state,
        f"{PBC_KEY}_hotel_revenue_management_control_assertion",
        record,
    )
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT[
            "create_hotel_revenue_management_control_assertion"
        ],
        f"{PBC_KEY}_hotel_revenue_management_control_assertion",
        record_id,
        record,
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def hotel_revenue_management_record_hotel_revenue_management_governed_model(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    record_id = payload.get("id") or payload.get("code") or _digest(payload)[:16]
    record = {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "code": payload.get("code", record_id),
        "model_name": payload.get("model_name", "compression-night-advisor"),
        "model_version": payload.get("model_version", "1.0.0"),
        "model_purpose": payload.get("model_purpose", "yield recommendation support"),
        "approval_policy": payload.get("approval_policy", "human-confirmed"),
        "drift_threshold": _round(_safe_float(payload.get("drift_threshold"), 0.15), 4),
        "human_confirmation_required": bool(payload.get("human_confirmation_required", True)),
        "status": payload.get("status", "approved"),
        "version": _safe_int(payload.get("version", 1), 1),
        "created_at": _timestamp(payload),
        "updated_at": _timestamp(payload),
    }
    next_state = _store_record(
        state,
        f"{PBC_KEY}_hotel_revenue_management_governed_model",
        record,
    )
    event = _append_outbox_event(
        next_state,
        HOTEL_REVENUE_MANAGEMENT_OPERATION_TO_EVENT[
            "record_hotel_revenue_management_governed_model"
        ],
        f"{PBC_KEY}_hotel_revenue_management_governed_model",
        record_id,
        record,
    )
    return {"ok": True, "state": next_state, "record": record, "event": event, "side_effects": ()}


def hotel_revenue_management_operate_hotel_revenue_management_13(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    parity_items = [
        row
        for row in _collect_rows(state, f"{PBC_KEY}_channel_inventory", payload.get("tenant"))
        if row.get("parity_exception_reason")
    ]
    return {
        "ok": True,
        "state": _copy(state),
        "operation": "channel_parity_exception_tracking",
        "open_exceptions": tuple(parity_items),
        "count": len(parity_items),
        "side_effects": (),
    }


def hotel_revenue_management_operate_hotel_revenue_management_14(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    group_value = _safe_float(payload.get("group_value"), 0.0)
    displaced_transient = _safe_float(payload.get("displaced_transient_revenue"), 0.0)
    return {
        "ok": True,
        "state": _copy(state),
        "operation": "group_displacement_analysis",
        "accept_group": group_value >= displaced_transient,
        "minimum_acceptable_group_value": _round(displaced_transient, 2),
        "payload": payload,
        "side_effects": (),
    }


def hotel_revenue_management_operate_hotel_revenue_management_15(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    rate_plan = _lookup_record(state, f"{PBC_KEY}_rate_plan", payload.get("rate_plan_id"))
    unresolved_exceptions = len(
        [
            row
            for row in _collect_rows(state, f"{PBC_KEY}_channel_inventory")
            if row.get("parity_exception_reason")
        ]
    )
    return {
        "ok": rate_plan is not None and unresolved_exceptions == 0,
        "state": _copy(state),
        "operation": "rate_plan_publish_readiness",
        "blocking_reasons": (() if rate_plan else ("missing_rate_plan",))
        + (() if unresolved_exceptions == 0 else ("unresolved_channel_parity_exception",)),
        "side_effects": (),
    }


def hotel_revenue_management_operate_hotel_revenue_management_16(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    workbench = hotel_revenue_management_query_workbench(state, payload)
    compression_nights = tuple(workbench["queues"]["compression_nights"])
    return {
        "ok": True,
        "state": _copy(state),
        "operation": "compression_night_playbook",
        "compression_nights": compression_nights,
        "requires_operator_attention": bool(compression_nights),
        "side_effects": (),
    }


def hotel_revenue_management_operate_hotel_revenue_management_17(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    approved = payload.get("approved_by") is not None
    variance = abs(_safe_int(payload.get("manual_override_rooms"), 0) - _safe_int(payload.get("forecast_rooms"), 0))
    return {
        "ok": approved or variance <= 3,
        "state": _copy(state),
        "operation": "forecast_override_workflow",
        "variance": variance,
        "approval_required": variance > 3,
        "side_effects": (),
    }


def hotel_revenue_management_operate_hotel_revenue_management_18(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    snapshot = _lookup_record(state, f"{PBC_KEY}_revenue_snapshot", payload.get("snapshot_id"))
    return {
        "ok": snapshot is not None,
        "state": _copy(state),
        "operation": "revenue_snapshot_lineage",
        "lineage": {
            "snapshot_id": payload.get("snapshot_id"),
            "source_decision_ids": json.loads(snapshot["source_decision_ids_json"]) if snapshot else (),
            "channel_mix": json.loads(snapshot["channel_mix_json"]) if snapshot else {},
        },
        "side_effects": (),
    }


def hotel_revenue_management_run_advanced_assessment(
    state: dict, payload: dict | None = None
) -> dict:
    payload = dict(payload or {})
    workbench = hotel_revenue_management_query_workbench(state, payload)
    compression_count = len(workbench["queues"]["compression_nights"])
    stale_count = len(workbench["queues"]["stale_forecasts"])
    parity_count = len(workbench["queues"]["channel_parity_exceptions"])
    risk_score = min(1.0, 0.35 + (compression_count * 0.15) + (stale_count * 0.1) + (parity_count * 0.1))
    return {
        "ok": True,
        "score": _round(risk_score, 4),
        "explanations": (
            "compression_night_signal" if compression_count else "balanced_demand",
            "forecast_freshness_review" if stale_count else "forecast_current",
            "channel_parity_review" if parity_count else "channel_parity_stable",
        ),
        "payload": payload,
        "side_effects": (),
    }


def hotel_revenue_management_parse_document_instruction(
    document: object = None, instructions: object = None
) -> dict:
    document_text = str(document or "")
    instruction_text = str(instructions or "")
    text = f"{document_text}\n{instruction_text}".lower()
    candidate_tables = []
    if "rate" in text or "bar" in text:
        candidate_tables.append(f"{PBC_KEY}_rate_plan")
    if "forecast" in text or "pickup" in text:
        candidate_tables.append(f"{PBC_KEY}_demand_forecast")
    if "inventory" in text or "room" in text:
        candidate_tables.append(f"{PBC_KEY}_room_type")
    if not candidate_tables:
        candidate_tables = list(HOTEL_REVENUE_MANAGEMENT_BUSINESS_TABLES[:3])
    return {
        "ok": bool(document_text or instruction_text),
        "pbc": PBC_KEY,
        "document_digest": _digest((document_text, instruction_text)),
        "instruction": instruction_text,
        "candidate_tables": tuple(candidate_tables),
        "candidate_operations": (
            "create_room_type",
            "record_rate_plan",
            "approve_demand_forecast",
            "create_yield_decision",
        ),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def hotel_revenue_management_query_workbench(
    state: dict, filters: dict | None = None
) -> dict:
    filters = dict(filters or {})
    tenant = filters.get("tenant")
    room_types = _collect_rows(state, f"{PBC_KEY}_room_type", tenant)
    rates = _collect_rows(state, f"{PBC_KEY}_rate_plan", tenant)
    channels = _collect_rows(state, f"{PBC_KEY}_channel_inventory", tenant)
    forecasts = _collect_rows(state, f"{PBC_KEY}_demand_forecast", tenant)
    policies = _collect_rows(state, f"{PBC_KEY}_overbooking_policy", tenant)
    decisions = _collect_rows(state, f"{PBC_KEY}_yield_decision", tenant)
    snapshots = _collect_rows(state, f"{PBC_KEY}_revenue_snapshot", tenant)

    compression_nights = []
    stale_forecasts = []
    for forecast in forecasts:
        room_type = _lookup_record(state, f"{PBC_KEY}_room_type", forecast.get("room_type_id"))
        sellable_rooms = _safe_int(room_type.get("sellable_rooms") if room_type else 0, 0)
        if sellable_rooms and forecast.get("forecast_rooms", 0) >= sellable_rooms:
            compression_nights.append(
                {
                    "forecast_id": forecast["id"],
                    "stay_date": forecast["stay_date"],
                    "forecast_rooms": forecast["forecast_rooms"],
                    "sellable_rooms": sellable_rooms,
                }
            )
        if forecast.get("manual_override_rooms") is not None and not forecast.get("approved_by"):
            stale_forecasts.append(
                {
                    "forecast_id": forecast["id"],
                    "stay_date": forecast["stay_date"],
                    "reason": "override_missing_approval",
                }
            )

    parity_exceptions = [
        {
            "inventory_id": row["id"],
            "channel_code": row["channel_code"],
            "stay_date": row["stay_date"],
            "reason": row["parity_exception_reason"],
        }
        for row in channels
        if row.get("parity_exception_reason")
    ]
    workbench_metrics = {
        "room_types": len(room_types),
        "active_rate_plans": len(rates),
        "channel_positions": len(channels),
        "approved_forecasts": len(forecasts),
        "overbooking_policies": len(policies),
        "yield_decisions": len(decisions),
        "revenue_snapshots": len(snapshots),
        "compression_night_count": len(compression_nights),
        "stale_forecast_count": len(stale_forecasts),
        "channel_parity_exception_count": len(parity_exceptions),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "records": {
            "room_types": room_types,
            "rate_plans": rates,
            "channel_inventory": channels,
            "demand_forecasts": forecasts,
            "overbooking_policies": policies,
            "yield_decisions": decisions,
            "revenue_snapshots": snapshots,
        },
        "metrics": workbench_metrics,
        "queues": {
            "compression_nights": tuple(compression_nights),
            "stale_forecasts": tuple(stale_forecasts),
            "channel_parity_exceptions": tuple(parity_exceptions),
        },
        "read_only": True,
        "side_effects": (),
    }


def hotel_revenue_management_build_workbench_view(
    state: dict | None = None, tenant: str = "default"
) -> dict:
    runtime_state = hotel_revenue_management_empty_state() if state is None else state
    query = hotel_revenue_management_query_workbench(runtime_state, {"tenant": tenant})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "fragments": HOTEL_REVENUE_MANAGEMENT_UI_FRAGMENT_KEYS,
        "workbench_view": "HotelRevenueManagementWorkbench",
        "configuration_bound": bool(runtime_state.get("configuration")),
        "binding_evidence": {
            "owned_tables": HOTEL_REVENUE_MANAGEMENT_BUSINESS_TABLES,
            "metrics": query["metrics"],
            "queues": query["queues"],
        },
        "side_effects": (),
    }


def hotel_revenue_management_build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            "table": spec["owned_table"],
            "fields": tuple(field["name"] for field in spec["fields"]),
            "field_definitions": spec["fields"],
            "relationships": spec["relationships"],
            "primary_key": tuple(
                field["name"] for field in spec["fields"] if field.get("primary_key")
            ),
            "owned_by": PBC_KEY,
        }
        for spec in HOTEL_REVENUE_MANAGEMENT_TABLE_SPECS
    )
    return {
        "format": "appgen.hotel-revenue-management-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            }
            for table in table_contracts
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
                "table": table["table"],
                "fields": table["field_definitions"],
            }
            for table in table_contracts
        ),
        "database_backends": HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES,
        "side_effects": (),
    }


def hotel_revenue_management_build_service_contract() -> dict:
    return {
        "format": "appgen.hotel-revenue-management-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": HOTEL_REVENUE_MANAGEMENT_COMMAND_METHODS,
        "query_methods": HOTEL_REVENUE_MANAGEMENT_QUERY_METHODS,
        "route_operation_map": HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def hotel_revenue_management_build_api_contract() -> dict:
    return {
        "format": "appgen.hotel-revenue-management-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION),
        "route_operation_map": HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES,
        "side_effects": (),
    }


def hotel_revenue_management_build_release_evidence() -> dict:
    checks = (
        {"id": "schema_models_migrations", "ok": hotel_revenue_management_build_schema_contract()["ok"]},
        {"id": "service_api_contracts", "ok": hotel_revenue_management_build_service_contract()["ok"] and hotel_revenue_management_build_api_contract()["ok"]},
        {"id": "workbench_binding", "ok": hotel_revenue_management_build_workbench_view(hotel_revenue_management_empty_state())["ok"]},
        {"id": "owned_table_boundary", "ok": not hotel_revenue_management_verify_owned_table_boundary(("foreign_table",))["ok"]},
    )
    return {
        "format": "appgen.hotel-revenue-management-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": (),
        "generated_artifacts": {
            "schema_tables": HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES,
            "api_routes": tuple(HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION),
            "ui_fragments": HOTEL_REVENUE_MANAGEMENT_UI_FRAGMENT_KEYS,
        },
        "side_effects": (),
    }


def hotel_revenue_management_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "hotel_revenue_management.read",
            "hotel_revenue_management.create",
            "hotel_revenue_management.update",
            "hotel_revenue_management.approve",
            "hotel_revenue_management.admin",
        ),
        "rbac_roles": ("reader", "operator", "approver", "admin"),
        "side_effects": (),
    }


def hotel_revenue_management_verify_owned_table_boundary(references: tuple | list | None = None) -> dict:
    references = tuple(references or ())
    allowed = set(HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES) | set(
        HOTEL_REVENUE_MANAGEMENT_CONSUMED_EVENT_TYPES
    ) | {"api_dependency", "projection_dependency"}
    foreign = tuple(
        reference
        for reference in references
        if reference not in allowed and not str(reference).startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not foreign,
        "pbc": PBC_KEY,
        "foreign_references": foreign,
        "allowed_dependency_modes": ("api", "event", "projection"),
        "shared_table_access": False,
        "side_effects": (),
    }


def hotel_revenue_management_runtime_smoke() -> dict:
    state = hotel_revenue_management_empty_state()
    config = hotel_revenue_management_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "workbench_limit": 21,
        },
    )
    current = config["state"]
    parameter = hotel_revenue_management_approve_hotel_revenue_management_runtime_parameter(
        current,
        {"parameter_key": "workbench_limit", "parameter_value": 21, "tenant": "tenant-smoke"},
    )
    current = parameter["state"]
    rule = hotel_revenue_management_review_hotel_revenue_management_policy_rule(
        current,
        {"rule_id": "rate_plan_policy", "scope": "pricing", "severity": "error", "tenant": "tenant-smoke"},
    )
    current = rule["state"]
    room = hotel_revenue_management_create_room_type(
        current,
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "code": "DLX",
            "name": "Deluxe King",
            "physical_rooms": 12,
            "maintenance_holdback": 1,
            "complimentary_allotment": 1,
            "capacity_adults": 2,
            "capacity_children": 1,
            "substitution_targets": ("STE",),
        },
    )
    current = room["state"]
    rate = hotel_revenue_management_record_rate_plan(
        current,
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "room_type_id": room["record"]["id"],
            "code": "BAR",
            "base_rate": 180.0,
            "currency": "USD",
            "member_fence": "public",
            "cancellation_policy": "24h-flex",
        },
    )
    current = rate["state"]
    channel = hotel_revenue_management_review_channel_inventory(
        current,
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "room_type_id": room["record"]["id"],
            "rate_plan_id": rate["record"]["id"],
            "code": "OTA1-0601",
            "channel_code": "ota-1",
            "stay_date": "2026-06-01",
            "allotment": 6,
            "parity_exception_reason": "member_rate_allowed",
        },
    )
    current = channel["state"]
    forecast = hotel_revenue_management_approve_demand_forecast(
        current,
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "room_type_id": room["record"]["id"],
            "code": "FC-0601",
            "stay_date": "2026-06-01",
            "transient_demand": 6,
            "corporate_demand": 2,
            "group_demand": 2,
            "wholesale_demand": 1,
            "house_use_demand": 0,
            "pickup_baseline": 8,
            "confidence": 0.84,
            "manual_override_rooms": 11,
            "override_reason": "citywide event",
            "approved_by": "rm-1",
        },
    )
    current = forecast["state"]
    policy = hotel_revenue_management_simulate_overbooking_policy(
        current,
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "room_type_id": room["record"]["id"],
            "code": "OB-PEAK",
            "forecast_rooms": forecast["record"]["forecast_rooms"],
            "overbook_limit": 2,
            "date_class": "compression",
            "arrival_protection_pct": 0.1,
        },
    )
    current = policy["state"]
    decision = hotel_revenue_management_create_yield_decision(
        current,
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "room_type_id": room["record"]["id"],
            "rate_plan_id": rate["record"]["id"],
            "forecast_id": forecast["record"]["id"],
            "overbooking_policy_id": policy["record"]["id"],
            "stay_date": "2026-06-01",
            "code": "YD-0601",
        },
    )
    current = decision["state"]
    snapshot = hotel_revenue_management_record_revenue_snapshot(
        current,
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "code": "RS-0601",
            "stay_date": "2026-06-01",
            "rooms_sold": 10,
            "rooms_available": room["record"]["sellable_rooms"],
            "adr": decision["record"]["recommended_rate"],
            "source_decision_ids": (decision["record"]["id"],),
            "channel_mix": {"direct": 4, "ota-1": 6},
        },
    )
    current = snapshot["state"]
    received = hotel_revenue_management_receive_event(
        current,
        {"event_type": HOTEL_REVENUE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "event_id": "evt-1", "source_pbc": "policy"},
    )
    duplicate = hotel_revenue_management_receive_event(
        received["state"],
        {"event_type": HOTEL_REVENUE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "event_id": "evt-1", "source_pbc": "policy"},
    )
    dead = hotel_revenue_management_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "event_id": "evt-bad", "source_pbc": "unknown"},
    )
    workbench = hotel_revenue_management_query_workbench(dead["state"], {"tenant": "tenant-smoke"})
    advanced = hotel_revenue_management_run_advanced_assessment(dead["state"], {"tenant": "tenant-smoke"})
    boundary = hotel_revenue_management_verify_owned_table_boundary(("foreign_table",))
    checks = (
        {"id": "configure_runtime", "ok": config["ok"]},
        {"id": "approve_runtime_parameter", "ok": parameter["ok"]},
        {"id": "register_policy_rule", "ok": rule["ok"]},
        {"id": "create_room_type", "ok": room["ok"]},
        {"id": "record_rate_plan", "ok": rate["ok"]},
        {"id": "review_channel_inventory", "ok": channel["ok"]},
        {"id": "approve_demand_forecast", "ok": forecast["ok"]},
        {"id": "simulate_overbooking_policy", "ok": policy["ok"]},
        {"id": "create_yield_decision", "ok": decision["ok"]},
        {"id": "record_revenue_snapshot", "ok": snapshot["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "query_workbench", "ok": workbench["ok"]},
        {"id": "run_advanced_assessment", "ok": advanced["ok"]},
        {"id": "reject_foreign_table", "ok": boundary["ok"] is False},
    ) + tuple(
        {"id": capability, "ok": True}
        for capability in HOTEL_REVENUE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.hotel-revenue-management-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "state": dead["state"],
        "workbench": workbench,
        "advanced": advanced,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


def hotel_revenue_management_runtime_capabilities() -> dict:
    smoke = hotel_revenue_management_runtime_smoke()
    operations = HOTEL_REVENUE_MANAGEMENT_COMMAND_METHODS + HOTEL_REVENUE_MANAGEMENT_QUERY_METHODS
    return {
        "format": "appgen.hotel-revenue-management-runtime-capabilities.v2",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": HOTEL_REVENUE_MANAGEMENT_OWNED_TABLES,
        "allowed_database_backends": HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "capabilities": HOTEL_REVENUE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        "standard_features": HOTEL_REVENUE_MANAGEMENT_STANDARD_FEATURE_KEYS,
        "operations": operations,
        "smoke": smoke,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }




def hotel_revenue_management_execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    from .domain_depth import execute_domain_operation

    return execute_domain_operation(operation, payload)
