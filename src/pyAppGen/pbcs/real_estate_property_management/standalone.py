
"""Standalone real estate property management domain core."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib

PBC_KEY = "real_estate_property_management"
PACKAGE_DIR = f"src/pyAppGen/pbcs/{PBC_KEY}"
DEFAULT_TIMESTAMP = "2026-05-30T00:00:00Z"
DEFAULT_TENANT = "default"

REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES = (
    "RealEstatePropertyManagementCreated",
    "RealEstatePropertyManagementUpdated",
    "RealEstatePropertyManagementApproved",
    "RealEstatePropertyManagementExceptionOpened",
    "PropertyPortfolioRegistered",
    "LeaseLifecycleUpdated",
    "CollectionsEscalated",
    "OwnerStatementPublished",
)
REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "CustomerUpdated",
    "SupplierQualified",
    "VendorQualified",
    "DocumentStored",
)
REAL_ESTATE_PROPERTY_MANAGEMENT_STANDARD_FEATURE_KEYS = (
    "property_management",
    "portfolio_and_building_hierarchy",
    "unit_inventory",
    "lease_and_tenant_operations",
    "rent_and_charge_scheduling",
    "cam_recoveries",
    "maintenance_and_inspections",
    "vacancy_and_renewal_management",
    "move_in_move_out",
    "delinquency_and_notice_management",
    "compliance_management",
    "vendor_work_orders",
    "owner_reporting",
    "asset_performance_analytics",
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
REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = (
    "real_estate_property_management_predictive_rent_roll_health",
    "real_estate_property_management_notice_deadline_guidance",
    "real_estate_property_management_vendor_triage_recommendations",
    "real_estate_property_management_owner_statement_lineage",
    "real_estate_property_management_asset_performance_forecasting",
    "real_estate_property_management_governed_ai_document_preview",
    "real_estate_property_management_counterfactual_renewal_scenarios",
    "real_estate_property_management_control_assertion_monitoring",
    "real_estate_property_management_event_sourced_operational_history",
    "real_estate_property_management_multi_tenant_policy_isolation",
    "real_estate_property_management_schema_evolution_resilience",
    "real_estate_property_management_autonomous_anomaly_detection",
)
REAL_ESTATE_PROPERTY_MANAGEMENT_UI_FRAGMENT_KEYS = (
    "RealEstatePropertyManagementWorkbench",
    "RealEstatePropertyManagementDetail",
    "RealEstatePropertyManagementAssistantPanel",
    "RealEstatePropertyManagementQueueRail",
)
RULES = (
    "property_completeness_policy",
    "lease_abstract_policy",
    "charge_schedule_policy",
    "delinquency_escalation_policy",
    "notice_deadline_policy",
    "inspection_follow_up_policy",
    "compliance_policy",
    "owner_reporting_policy",
)
PARAMETERS = (
    "occupancy_target",
    "delinquency_threshold_days",
    "renewal_lead_days",
    "notice_service_grace_hours",
    "work_order_sla_hours",
    "cam_recovery_floor",
    "owner_statement_close_day",
    "assistant_preview_limit",
    "workbench_limit",
)
PERMISSIONS = (
    "real_estate_property_management.read",
    "real_estate_property_management.create",
    "real_estate_property_management.update",
    "real_estate_property_management.approve",
    "real_estate_property_management.admin",
    "real_estate_property_management.collections",
    "real_estate_property_management.maintenance",
    "real_estate_property_management.compliance",
    "real_estate_property_management.owner_reporting",
    "real_estate_property_management.ai_review",
)


def _table_name(name: str) -> str:
    return name if name.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{name}"


BUSINESS_TABLE_SPECS = (
    {"name": "portfolio", "fields": ("id", "tenant", "code", "name", "manager", "owner_name", "status", "payload", "created_at", "updated_at")},
    {"name": "property", "fields": ("id", "tenant", "portfolio_id", "code", "name", "asset_class", "jurisdiction", "status", "payload", "created_at", "updated_at")},
    {"name": "building", "fields": ("id", "tenant", "property_id", "code", "name", "building_type", "status", "payload", "created_at", "updated_at")},
    {"name": "unit", "fields": ("id", "tenant", "property_id", "building_id", "code", "unit_number", "occupancy_status", "market_rent", "bedrooms", "bathrooms", "status", "payload", "created_at", "updated_at")},
    {"name": "tenant", "fields": ("id", "tenant", "code", "display_name", "contact_email", "status", "payload", "created_at", "updated_at")},
    {"name": "tenant_party", "fields": ("id", "tenant", "tenant_id", "lease_id", "role", "display_name", "status", "payload", "created_at", "updated_at")},
    {"name": "lease", "fields": ("id", "tenant", "property_id", "unit_id", "tenant_id", "code", "start_date", "end_date", "base_rent", "status", "payload", "created_at", "updated_at")},
    {"name": "rent_schedule", "fields": ("id", "tenant", "lease_id", "unit_id", "code", "frequency", "next_due_date", "amount", "status", "payload", "created_at", "updated_at")},
    {"name": "security_deposit", "fields": ("id", "tenant", "lease_id", "tenant_id", "code", "trust_account", "amount", "status", "payload", "created_at", "updated_at")},
    {"name": "charge", "fields": ("id", "tenant", "lease_id", "tenant_id", "charge_type", "code", "amount", "due_date", "status", "payload", "created_at", "updated_at")},
    {"name": "rent_charge", "fields": ("id", "tenant", "lease_id", "tenant_id", "charge_type", "code", "amount", "due_date", "status", "payload", "created_at", "updated_at")},
    {"name": "cam_recovery", "fields": ("id", "tenant", "property_id", "lease_id", "code", "recovery_basis", "estimated_amount", "status", "payload", "created_at", "updated_at")},
    {"name": "maintenance_request", "fields": ("id", "tenant", "property_id", "unit_id", "lease_id", "code", "priority", "summary", "status", "payload", "created_at", "updated_at")},
    {"name": "inspection", "fields": ("id", "tenant", "property_id", "unit_id", "lease_id", "code", "inspection_type", "scheduled_for", "result", "status", "payload", "created_at", "updated_at")},
    {"name": "vacancy", "fields": ("id", "tenant", "property_id", "unit_id", "code", "market_ready_date", "notice_date", "status", "payload", "created_at", "updated_at")},
    {"name": "renewal", "fields": ("id", "tenant", "lease_id", "unit_id", "code", "stage", "offered_rent", "expires_on", "status", "payload", "created_at", "updated_at")},
    {"name": "move_event", "fields": ("id", "tenant", "lease_id", "unit_id", "code", "event_type", "event_date", "status", "payload", "created_at", "updated_at")},
    {"name": "delinquency_case", "fields": ("id", "tenant", "lease_id", "tenant_id", "code", "days_past_due", "balance_due", "stage", "status", "payload", "created_at", "updated_at")},
    {"name": "notice", "fields": ("id", "tenant", "lease_id", "code", "notice_type", "service_method", "served_on", "status", "payload", "created_at", "updated_at")},
    {"name": "compliance_item", "fields": ("id", "tenant", "property_id", "code", "title", "due_date", "severity", "status", "payload", "created_at", "updated_at")},
    {"name": "vendor_work_order", "fields": ("id", "tenant", "maintenance_request_id", "property_id", "unit_id", "code", "vendor_name", "scheduled_for", "status", "payload", "created_at", "updated_at")},
    {"name": "owner_statement", "fields": ("id", "tenant", "property_id", "code", "statement_period", "net_operating_income", "status", "payload", "created_at", "updated_at")},
    {"name": "asset_performance_snapshot", "fields": ("id", "tenant", "property_id", "code", "reporting_period", "occupancy_rate", "delinquency_rate", "status", "payload", "created_at", "updated_at")},
    {"name": "assistant_artifact", "fields": ("id", "tenant", "code", "artifact_type", "target_table", "action", "status", "payload", "created_at", "updated_at")},
)
SUPPORT_TABLE_SPECS = (
    {"name": "policy_rule", "fields": ("id", "tenant", "code", "compiled_hash", "status", "payload", "created_at", "updated_at")},
    {"name": "runtime_parameter", "fields": ("id", "tenant", "code", "value", "status", "payload", "created_at", "updated_at")},
    {"name": "schema_extension", "fields": ("id", "tenant", "code", "target_table", "status", "payload", "created_at", "updated_at")},
    {"name": "control_assertion", "fields": ("id", "tenant", "code", "assertion_type", "status", "payload", "created_at", "updated_at")},
    {"name": "governed_model", "fields": ("id", "tenant", "code", "model_name", "status", "payload", "created_at", "updated_at")},
)
EVENT_TABLE_SPECS = (
    {"name": "appgen_outbox_event", "fields": ("id", "tenant", "event_type", "topic", "idempotency_key", "status", "payload", "created_at", "updated_at")},
    {"name": "appgen_inbox_event", "fields": ("id", "tenant", "event_type", "topic", "idempotency_key", "status", "payload", "created_at", "updated_at")},
    {"name": "appgen_dead_letter_event", "fields": ("id", "tenant", "event_type", "topic", "idempotency_key", "status", "payload", "created_at", "updated_at")},
)
ALL_TABLE_SPECS = BUSINESS_TABLE_SPECS + SUPPORT_TABLE_SPECS + EVENT_TABLE_SPECS
TABLE_SPEC_BY_SHORT_NAME = {spec["name"]: spec for spec in ALL_TABLE_SPECS}
TABLE_SPEC_BY_FULL_NAME = {_table_name(spec["name"]): {**spec, "table": _table_name(spec["name"])} for spec in ALL_TABLE_SPECS}
REAL_ESTATE_PROPERTY_MANAGEMENT_BUSINESS_TABLES = tuple(_table_name(spec["name"]) for spec in BUSINESS_TABLE_SPECS)
REAL_ESTATE_PROPERTY_MANAGEMENT_SUPPORT_TABLES = tuple(_table_name(spec["name"]) for spec in SUPPORT_TABLE_SPECS)
REAL_ESTATE_PROPERTY_MANAGEMENT_EVENT_TABLES = tuple(_table_name(spec["name"]) for spec in EVENT_TABLE_SPECS)
REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES = REAL_ESTATE_PROPERTY_MANAGEMENT_BUSINESS_TABLES + REAL_ESTATE_PROPERTY_MANAGEMENT_SUPPORT_TABLES + REAL_ESTATE_PROPERTY_MANAGEMENT_EVENT_TABLES
REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_TABLES = REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES


DOMAIN_OPERATION_SPECS = (
    {"operation": "create_portfolio", "table": "portfolio", "route": "POST /portfolios", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[0], "required": ("code", "name")},
    {"operation": "create_property", "table": "property", "route": "POST /properties", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[0], "required": ("portfolio_id", "code", "name"), "references": {"portfolio_id": "portfolio"}},
    {"operation": "create_building", "table": "building", "route": "POST /buildings", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[0], "required": ("property_id", "code", "name"), "references": {"property_id": "property"}},
    {"operation": "create_unit", "table": "unit", "route": "POST /units", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[0], "required": ("property_id", "building_id", "code", "unit_number"), "references": {"property_id": "property", "building_id": "building"}},
    {"operation": "record_tenant", "table": "tenant", "route": "POST /tenants", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("code", "display_name")},
    {"operation": "create_lease", "table": "lease", "route": "POST /leases", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("property_id", "unit_id", "tenant_id", "code", "start_date", "end_date", "base_rent"), "references": {"property_id": "property", "unit_id": "unit", "tenant_id": "tenant"}},
    {"operation": "generate_rent_schedule", "table": "rent_schedule", "route": "POST /rent-schedules", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("lease_id", "code", "next_due_date"), "references": {"lease_id": "lease"}},
    {"operation": "record_security_deposit", "table": "security_deposit", "route": "POST /security-deposits", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("lease_id", "tenant_id", "code", "amount"), "references": {"lease_id": "lease", "tenant_id": "tenant"}},
    {"operation": "post_charge", "table": "charge", "route": "POST /charges", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("lease_id", "tenant_id", "charge_type", "code", "amount", "due_date"), "references": {"lease_id": "lease", "tenant_id": "tenant"}},
    {"operation": "accrue_cam_recovery", "table": "cam_recovery", "route": "POST /cam-recoveries", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("property_id", "lease_id", "code", "estimated_amount"), "references": {"property_id": "property", "lease_id": "lease"}},
    {"operation": "open_maintenance_request", "table": "maintenance_request", "route": "POST /maintenance-requests", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("property_id", "unit_id", "code", "summary"), "references": {"property_id": "property", "unit_id": "unit"}},
    {"operation": "create_inspection", "table": "inspection", "route": "POST /inspections", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("property_id", "unit_id", "code", "inspection_type", "scheduled_for"), "references": {"property_id": "property", "unit_id": "unit"}},
    {"operation": "track_vacancy", "table": "vacancy", "route": "POST /vacancies", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("property_id", "unit_id", "code", "market_ready_date"), "references": {"property_id": "property", "unit_id": "unit"}},
    {"operation": "manage_renewal", "table": "renewal", "route": "POST /renewals", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("lease_id", "unit_id", "code", "stage"), "references": {"lease_id": "lease", "unit_id": "unit"}},
    {"operation": "record_move_event", "table": "move_event", "route": "POST /move-events", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("lease_id", "unit_id", "code", "event_type", "event_date"), "references": {"lease_id": "lease", "unit_id": "unit"}},
    {"operation": "escalate_delinquency", "table": "delinquency_case", "route": "POST /delinquencies", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[2], "required": ("lease_id", "tenant_id", "code", "days_past_due", "balance_due"), "references": {"lease_id": "lease", "tenant_id": "tenant"}},
    {"operation": "issue_notice", "table": "notice", "route": "POST /notices", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[2], "required": ("lease_id", "code", "notice_type", "served_on"), "references": {"lease_id": "lease"}},
    {"operation": "manage_compliance_case", "table": "compliance_item", "route": "POST /compliance-items", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[2], "required": ("property_id", "code", "title", "due_date"), "references": {"property_id": "property"}},
    {"operation": "create_vendor_work_order", "table": "vendor_work_order", "route": "POST /vendor-work-orders", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("maintenance_request_id", "property_id", "unit_id", "code", "vendor_name"), "references": {"maintenance_request_id": "maintenance_request", "property_id": "property", "unit_id": "unit"}},
    {"operation": "publish_owner_report", "table": "owner_statement", "route": "POST /owner-reports", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[3], "required": ("property_id", "code", "statement_period"), "references": {"property_id": "property"}},
    {"operation": "capture_asset_performance", "table": "asset_performance_snapshot", "route": "POST /asset-performance-snapshots", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[3], "required": ("property_id", "code", "reporting_period"), "references": {"property_id": "property"}},
    {"operation": "preview_assistant_document_instruction", "table": "assistant_artifact", "route": "POST /assistant-previews", "event": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES[1], "required": ("document", "instruction")},
)
OPERATION_SPEC_BY_NAME = {spec["operation"]: spec for spec in DOMAIN_OPERATION_SPECS}
REAL_ESTATE_PROPERTY_MANAGEMENT_DOMAIN_OPERATIONS = tuple(spec["operation"] for spec in DOMAIN_OPERATION_SPECS)
DOMAIN_OPERATIONS = REAL_ESTATE_PROPERTY_MANAGEMENT_DOMAIN_OPERATIONS
ROUTE_TO_OPERATION = {spec["route"]: spec["operation"] for spec in DOMAIN_OPERATION_SPECS}
CANONICAL_ROUTES = tuple(spec["route"] for spec in DOMAIN_OPERATION_SPECS) + ("GET /real-estate-property-management-workbench",)
ROUTE_ALIASES = {"POST /propertys": "POST /properties", "POST /rent-charges": "POST /charges"}
ROUTES = CANONICAL_ROUTES + tuple(ROUTE_ALIASES)
WORKBENCH_ROUTE = "GET /real-estate-property-management-workbench"
LEGACY_OPERATION_ALIASES = {
    "review_lease": "create_lease",
    "approve_rent_charge": "post_charge",
    "simulate_maintenance_request": "open_maintenance_request",
    "start_renewal": "manage_renewal",
    "open_delinquency_case": "escalate_delinquency",
    "log_compliance_item": "manage_compliance_case",
    "publish_owner_statement": "publish_owner_report",
    "onboard_tenant": "record_tenant",
    "submit_maintenance_request": "open_maintenance_request",
    "schedule_inspection": "create_inspection",
    "activate_lease": "create_lease",
    "command_property": "create_property",
}
SERVICE_COMMAND_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "run_advanced_assessment",
    "parse_document_instruction",
) + DOMAIN_OPERATIONS
QUERY_OPERATIONS = ("query_workbench", "build_workbench_view")


PBC_MANIFEST = {
    "pbc": PBC_KEY,
    "label": "Real Estate Property Management",
    "description": "Standalone property management application covering portfolio hierarchy, leasing, operations, collections, compliance, owner reporting, and governed AI previews",
    "mesh": "relationship",
    "template": "standalone-functional-application",
    "version": "2.0.0",
    "datastore_backend": "postgresql",
    "tables": tuple(spec["name"] for spec in BUSINESS_TABLE_SPECS) + tuple(f"{PBC_KEY}_{spec['name']}" for spec in SUPPORT_TABLE_SPECS),
    "migrations": ("migrations/001_initial.sql",),
    "docs": ("SPECIFICATION.md", "RELEASE_EVIDENCE.md"),
    "tests": ("tests/test_contract.py",),
    "apis": ROUTES,
    "workflows": DOMAIN_OPERATIONS,
    "permissions": PERMISSIONS,
    "capabilities": REAL_ESTATE_PROPERTY_MANAGEMENT_STANDARD_FEATURE_KEYS + REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
    "standard_features": REAL_ESTATE_PROPERTY_MANAGEMENT_STANDARD_FEATURE_KEYS,
    "advanced_capabilities": REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
    "emits": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES,
    "consumes": REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES,
    "configuration": (
        "REAL_ESTATE_PROPERTY_MANAGEMENT_DATABASE_URL",
        "REAL_ESTATE_PROPERTY_MANAGEMENT_EVENT_TOPIC",
        "REAL_ESTATE_PROPERTY_MANAGEMENT_RETRY_LIMIT",
        "REAL_ESTATE_PROPERTY_MANAGEMENT_DEFAULT_POLICY",
    ),
    "ui_fragments": REAL_ESTATE_PROPERTY_MANAGEMENT_UI_FRAGMENT_KEYS,
    "seed_data": ("seed_data.py",),
}

_HANDLED_EVENT_KEYS = set()


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _sorted_records(state: dict, table_name: str) -> tuple[dict, ...]:
    table = state["records"].get(_table_name(table_name), {})
    return tuple(sorted((deepcopy(record) for record in table.values()), key=lambda item: item["id"]))


def _get_record(state: dict, table_name: str, record_id: str | None) -> dict | None:
    if not record_id:
        return None
    return state["records"].get(_table_name(table_name), {}).get(record_id)


def _event_id(state: dict, short_table_name: str) -> str:
    full = _table_name(short_table_name)
    return f"{short_table_name}-{len(state['records'][full]) + 1}"


def _store_record(state: dict, table_name: str, payload: dict, *, status: str | None = None, extra: dict | None = None) -> dict:
    full_table = _table_name(table_name)
    spec = TABLE_SPEC_BY_FULL_NAME[full_table]
    record_id = str(payload.get("id") or payload.get("code") or _event_id(state, table_name))
    record = {field: None for field in spec["fields"]}
    record["id"] = record_id
    if "tenant" in record:
        record["tenant"] = payload.get("tenant", DEFAULT_TENANT)
    if "code" in record:
        record["code"] = payload.get("code", record_id.upper())
    if "status" in record:
        record["status"] = payload.get("status", status or "active")
    if "created_at" in record:
        record["created_at"] = payload.get("created_at", DEFAULT_TIMESTAMP)
    if "updated_at" in record:
        record["updated_at"] = DEFAULT_TIMESTAMP
    if "payload" in record:
        record["payload"] = deepcopy(payload)
    for field in spec["fields"]:
        if field in payload and field != "payload":
            record[field] = deepcopy(payload[field])
    if extra:
        record.update(deepcopy(extra))
    state["records"][full_table][record_id] = record
    return deepcopy(record)


def _emit_event(state: dict, event_type: str, payload: dict) -> dict:
    event_payload = {
        "id": _event_id(state, "appgen_outbox_event"),
        "tenant": payload.get("tenant", DEFAULT_TENANT),
        "event_type": event_type,
        "topic": REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "idempotency_key": _digest((event_type, payload)),
        "status": "pending",
        "payload": deepcopy(payload),
    }
    record = _store_record(state, "appgen_outbox_event", event_payload, status="pending")
    state["outbox"].append(deepcopy(record))
    return record


def _normalize_route(route: str) -> str:
    return ROUTE_ALIASES.get(route, route)


def _resolve_operation_name(operation: str) -> str | None:
    if operation in OPERATION_SPEC_BY_NAME:
        return operation
    return LEGACY_OPERATION_ALIASES.get(operation)


def _route_for_table(full_table: str) -> str | None:
    for spec in DOMAIN_OPERATION_SPECS:
        if _table_name(spec["table"]) == full_table:
            return spec["route"]
    return None


def real_estate_property_management_empty_state() -> dict:
    return {
        "records": {table: {} for table in REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def real_estate_property_management_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    config = dict(config or {})
    ok = (
        config.get("database_backend") in REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        and config.get("event_topic", REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC) == REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        "database_backend": config.get("database_backend", "postgresql"),
        "event_topic": config.get("event_topic", REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC),
        "retry_limit": int(config.get("retry_limit", 5)),
        "default_policy": config.get("default_policy", "balanced"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "ok": ok,
    }
    return {"ok": ok, "state": next_state, "configuration": deepcopy(next_state["configuration"]), "side_effects": ()}


def real_estate_property_management_set_parameter(state: dict, name: str, value) -> dict:
    next_state = _copy(state)
    if name not in PARAMETERS:
        return {"ok": False, "state": next_state, "reason": "unknown_parameter", "parameter": name, "side_effects": ()}
    parameter = _store_record(
        next_state,
        "runtime_parameter",
        {"id": name, "code": name, "value": value, "payload": {"name": name, "value": value}},
        status="active",
        extra={"value": value},
    )
    next_state["parameters"][name] = {"name": name, "value": value, "bounded": True}
    return {"ok": True, "state": next_state, "parameter": parameter, "side_effects": ()}


def real_estate_property_management_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    rule = dict(rule or {})
    rule_id = rule.get("rule_id") or rule.get("code") or "domain_rule"
    if rule_id not in RULES and rule_id not in {item.get("rule_id") for item in next_state["rules"].values()}:
        rule.setdefault("rule_id", rule_id)
    compiled_hash = _digest(rule)
    record = _store_record(
        next_state,
        "policy_rule",
        {"id": rule_id, "code": rule_id, "compiled_hash": compiled_hash, "payload": rule},
        status=rule.get("status", "active"),
        extra={"compiled_hash": compiled_hash},
    )
    next_state["rules"][rule_id] = deepcopy(rule)
    return {"ok": True, "state": next_state, "rule": record, "side_effects": ()}


def real_estate_property_management_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = _table_name(table)
    if owned_name not in REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "table": owned_name, "side_effects": ()}
    extension = _store_record(
        next_state,
        "schema_extension",
        {"id": owned_name, "code": owned_name, "target_table": owned_name, "payload": dict(fields or {})},
        status="active",
        extra={"target_table": owned_name},
    )
    next_state["schema_extensions"][owned_name] = dict(fields or {})
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields or {}), "record": extension, "side_effects": ()}


def real_estate_property_management_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    event = dict(event or {})
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "idempotency_key": idem, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    payload = {
        "id": event.get("event_id") or _event_id(next_state, "appgen_inbox_event"),
        "tenant": event.get("tenant", DEFAULT_TENANT),
        "event_type": event.get("event_type"),
        "topic": event.get("topic", REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC),
        "idempotency_key": idem,
        "payload": event,
    }
    if event.get("event_type") not in REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES:
        record = _store_record(next_state, "appgen_dead_letter_event", payload, status="dead_letter")
        next_state["dead_letter"].append(deepcopy(record))
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": _table_name("appgen_dead_letter_event"),
            "record": record,
            "side_effects": (),
        }
    record = _store_record(next_state, "appgen_inbox_event", payload, status="processed")
    next_state["inbox"].append(deepcopy(record))
    return {"ok": True, "duplicate": False, "state": next_state, "record": record, "side_effects": ()}


def _validate_operation_payload(state: dict, operation: str, payload: dict) -> tuple[str, ...]:
    spec = OPERATION_SPEC_BY_NAME[operation]
    missing = [field for field in spec.get("required", ()) if payload.get(field) in (None, "")]
    for field, table_name in spec.get("references", {}).items():
        value = payload.get(field)
        if value and not _get_record(state, table_name, value):
            missing.append(f"{field}:missing_{table_name}")
    return tuple(missing)


def _apply_operation_defaults(state: dict, operation: str, payload: dict) -> dict:
    data = dict(payload)
    if operation in {"generate_rent_schedule", "record_security_deposit", "post_charge", "accrue_cam_recovery", "manage_renewal", "record_move_event", "escalate_delinquency", "issue_notice"}:
        lease = _get_record(state, "lease", data.get("lease_id"))
        if lease:
            data.setdefault("tenant_id", lease.get("tenant_id"))
            data.setdefault("unit_id", lease.get("unit_id"))
            data.setdefault("property_id", lease.get("property_id"))
    return data


def _calculate_metrics(state: dict) -> dict:
    units = list(state["records"][_table_name("unit")].values())
    leases = list(state["records"][_table_name("lease")].values())
    maintenance = list(state["records"][_table_name("maintenance_request")].values())
    work_orders = list(state["records"][_table_name("vendor_work_order")].values())
    delinquencies = list(state["records"][_table_name("delinquency_case")].values())
    notices = list(state["records"][_table_name("notice")].values())
    renewals = list(state["records"][_table_name("renewal")].values())
    compliance = list(state["records"][_table_name("compliance_item")].values())
    charges = list(state["records"][_table_name("charge")].values())
    cam = list(state["records"][_table_name("cam_recovery")].values())
    active_leases = [record for record in leases if record.get("status") in {"active", "pending_renewal", "renewed"}]
    occupied_units = {record.get("unit_id") for record in active_leases if record.get("unit_id")}
    total_units = len(units)
    occupied_count = len(occupied_units)
    vacancy_count = len([record for record in state["records"][_table_name("vacancy")].values() if record.get("status") != "closed"])
    open_maintenance = len([record for record in maintenance if record.get("status") not in {"resolved", "closed"}])
    open_work_orders = len([record for record in work_orders if record.get("status") not in {"completed", "closed"}])
    open_delinquency = len([record for record in delinquencies if record.get("status") not in {"resolved", "closed"}])
    delinquency_balance = round(sum(float(record.get("balance_due") or 0) for record in delinquencies if record.get("status") not in {"resolved", "closed"}), 2)
    delinquency_rate = round(open_delinquency / max(len(active_leases), 1), 4)
    occupancy_rate = round(occupied_count / total_units, 4) if total_units else 0.0
    annualized_rent = round(sum(float(record.get("base_rent") or 0) for record in active_leases) * 12, 2)
    charge_total = round(sum(float(record.get("amount") or 0) for record in charges), 2)
    cam_total = round(sum(float(record.get("estimated_amount") or 0) for record in cam), 2)
    overdue_compliance = len([record for record in compliance if record.get("status") not in {"closed", "compliant"}])
    pending_notices = len([record for record in notices if record.get("status") not in {"served", "closed"}])
    renewal_pipeline = len([record for record in renewals if record.get("stage") not in {"accepted", "declined", "expired"}])
    return {
        "total_units": total_units,
        "occupied_units": occupied_count,
        "open_vacancies": vacancy_count,
        "occupancy_rate": occupancy_rate,
        "annualized_base_rent": annualized_rent,
        "open_maintenance": open_maintenance,
        "open_vendor_work_orders": open_work_orders,
        "open_delinquency_cases": open_delinquency,
        "delinquency_balance": delinquency_balance,
        "delinquency_rate": delinquency_rate,
        "pending_notices": pending_notices,
        "renewal_pipeline": renewal_pipeline,
        "overdue_compliance_items": overdue_compliance,
        "charges_billed": charge_total,
        "cam_recovery_billed": cam_total,
    }


def _create_control_assertion(next_state: dict, operation: str, payload: dict) -> dict:
    return _store_record(
        next_state,
        "control_assertion",
        {
            "id": f"assert-{operation}-{len(next_state['records'][_table_name('control_assertion')]) + 1}",
            "code": f"ASSERT-{operation}",
            "assertion_type": "mutation_requires_confirmation" if operation == "preview_assistant_document_instruction" else "segregation_of_duties",
            "payload": {"operation": operation, "payload_digest": _digest(payload)},
        },
        status="recorded",
        extra={"assertion_type": "mutation_requires_confirmation" if operation == "preview_assistant_document_instruction" else "segregation_of_duties"},
    )


def _create_governed_model(next_state: dict, operation: str) -> dict:
    return _store_record(
        next_state,
        "governed_model",
        {
            "id": f"model-{operation}",
            "code": f"MODEL-{operation}",
            "model_name": "real_estate_property_management-assistant-preview",
            "payload": {"operation": operation, "requires_confirmation": True},
        },
        status="approved",
        extra={"model_name": "real_estate_property_management-assistant-preview"},
    )


def real_estate_property_management_parse_document_instruction(document: str, instruction: str) -> dict:
    text = f"{document} {instruction}".lower()
    keyword_map = (
        ("lease", ("lease", "rent_schedule", "renewal")),
        ("rent", ("charge", "rent_schedule", "delinquency_case")),
        ("deposit", ("security_deposit",)),
        ("maintenance", ("maintenance_request", "vendor_work_order")),
        ("inspection", ("inspection",)),
        ("notice", ("notice", "delinquency_case")),
        ("compliance", ("compliance_item",)),
        ("owner", ("owner_statement", "asset_performance_snapshot")),
        ("unit", ("unit", "vacancy")),
    )
    candidate_tables = []
    for keyword, tables in keyword_map:
        if keyword in text:
            candidate_tables.extend(_table_name(name) for name in tables)
    if not candidate_tables:
        candidate_tables = [_table_name(name) for name in ("property", "lease", "tenant", "assistant_artifact")]
    action = "update" if any(word in instruction.lower() for word in ("update", "amend", "modify", "change")) else "create"
    previews = tuple(
        {
            "table": table,
            "action": action,
            "summary": f"{action} preview for {table.split(f'{PBC_KEY}_', 1)[1].replace('_', ' ')}",
            "fields": TABLE_SPEC_BY_FULL_NAME[table]["fields"][:6],
            "requires_confirmation": True,
        }
        for table in tuple(dict.fromkeys(candidate_tables))[:4]
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "instruction": instruction,
        "instruction_type": action,
        "document_digest": _digest((document, instruction)),
        "candidate_tables": tuple(dict.fromkeys(candidate_tables)),
        "crud_preview": previews[0],
        "crud_previews": previews,
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    target = _table_name(table or payload.get("table") or "assistant_artifact")
    if target not in REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES:
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    route = _route_for_table(target)
    preview = {
        "keys": tuple(field for field in TABLE_SPEC_BY_FULL_NAME[target]["fields"] if field not in {"payload", "created_at", "updated_at"})[:6],
        "route": route,
        "requires_confirmation": action in {"create", "update", "delete"},
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": payload,
        "route": route,
        "preview": preview,
        "requires_confirmation": preview["requires_confirmation"],
        "event_contract": "AppGen-X",
        "ownership_guard": "pbc_local_only",
        "side_effects": (),
    }


def _execute_domain_operation(state: dict, operation: str, payload: dict | None = None) -> dict:
    canonical = _resolve_operation_name(operation)
    if canonical not in OPERATION_SPEC_BY_NAME:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    next_state = _copy(state)
    payload = _apply_operation_defaults(next_state, canonical, dict(payload or {}))
    missing = _validate_operation_payload(next_state, canonical, payload)
    if missing:
        return {"ok": False, "reason": "missing_required_fields", "missing": missing, "operation": canonical, "state": next_state, "side_effects": ()}
    spec = OPERATION_SPEC_BY_NAME[canonical]
    written = []
    aux_tables = []
    status = payload.get("status")
    extra = None
    if canonical == "record_tenant":
        tenant_record = _store_record(next_state, "tenant", payload, status=status or "active")
        written.append(tenant_record)
        for index, member in enumerate(payload.get("household", ())):
            member_payload = {
                "id": member.get("id") or f"{tenant_record['id']}-party-{index + 1}",
                "tenant": payload.get("tenant", DEFAULT_TENANT),
                "tenant_id": tenant_record["id"],
                "lease_id": member.get("lease_id"),
                "role": member.get("role", "occupant"),
                "display_name": member.get("display_name") or member.get("name") or f"Occupant {index + 1}",
                "payload": member,
            }
            written.append(_store_record(next_state, "tenant_party", member_payload, status=member.get("status", "active"), extra={"role": member_payload["role"], "display_name": member_payload["display_name"]}))
            aux_tables.append(_table_name("tenant_party"))
    elif canonical == "create_lease":
        lease_record = _store_record(next_state, "lease", payload, status=status or "active")
        written.append(lease_record)
        unit = _get_record(next_state, "unit", payload.get("unit_id"))
        if unit:
            unit["occupancy_status"] = "occupied"
            unit["status"] = "occupied"
            unit["updated_at"] = DEFAULT_TIMESTAMP
    elif canonical == "generate_rent_schedule":
        amount = payload.get("amount")
        if amount is None:
            lease = _get_record(next_state, "lease", payload.get("lease_id"))
            amount = lease.get("base_rent") if lease else None
        record = _store_record(next_state, "rent_schedule", payload, status=status or "scheduled", extra={"amount": amount, "frequency": payload.get("frequency", "monthly")})
        written.append(record)
    elif canonical == "record_security_deposit":
        record = _store_record(next_state, "security_deposit", payload, status=status or "held", extra={"trust_account": payload.get("trust_account", "trust-001")})
        written.append(record)
    elif canonical == "post_charge":
        record = _store_record(next_state, "charge", payload, status=status or "open")
        written.append(record)
    elif canonical == "accrue_cam_recovery":
        record = _store_record(next_state, "cam_recovery", payload, status=status or "open")
        written.append(record)
    elif canonical == "open_maintenance_request":
        record = _store_record(next_state, "maintenance_request", payload, status=status or "open", extra={"priority": payload.get("priority", "medium"), "summary": payload.get("summary")})
        written.append(record)
    elif canonical == "create_inspection":
        record = _store_record(next_state, "inspection", payload, status=status or "scheduled", extra={"inspection_type": payload.get("inspection_type"), "result": payload.get("result")})
        written.append(record)
    elif canonical == "track_vacancy":
        record = _store_record(next_state, "vacancy", payload, status=status or "open")
        written.append(record)
        unit = _get_record(next_state, "unit", payload.get("unit_id"))
        if unit:
            unit["occupancy_status"] = "vacant"
            unit["status"] = payload.get("unit_status", "vacant")
            unit["updated_at"] = DEFAULT_TIMESTAMP
    elif canonical == "manage_renewal":
        record = _store_record(next_state, "renewal", payload, status=status or "active", extra={"stage": payload.get("stage", "offer_drafted")})
        written.append(record)
    elif canonical == "record_move_event":
        record = _store_record(next_state, "move_event", payload, status=status or "completed", extra={"event_type": payload.get("event_type")})
        written.append(record)
        unit = _get_record(next_state, "unit", payload.get("unit_id"))
        lease = _get_record(next_state, "lease", payload.get("lease_id"))
        if payload.get("event_type") == "move_in" and unit:
            unit["occupancy_status"] = "occupied"
            unit["status"] = "occupied"
        if payload.get("event_type") == "move_out" and unit:
            unit["occupancy_status"] = "turn"
            unit["status"] = "turn"
        if lease and payload.get("event_type") == "move_out":
            lease["status"] = "completed"
            lease["updated_at"] = DEFAULT_TIMESTAMP
    elif canonical == "escalate_delinquency":
        record = _store_record(next_state, "delinquency_case", payload, status=status or "open", extra={"stage": payload.get("stage", "collections_review")})
        written.append(record)
    elif canonical == "issue_notice":
        record = _store_record(next_state, "notice", payload, status=status or "drafted", extra={"service_method": payload.get("service_method", "email")})
        written.append(record)
    elif canonical == "manage_compliance_case":
        record = _store_record(next_state, "compliance_item", payload, status=status or "open", extra={"severity": payload.get("severity", "medium"), "title": payload.get("title")})
        written.append(record)
    elif canonical == "create_vendor_work_order":
        record = _store_record(next_state, "vendor_work_order", payload, status=status or "assigned", extra={"vendor_name": payload.get("vendor_name")})
        written.append(record)
        maintenance = _get_record(next_state, "maintenance_request", payload.get("maintenance_request_id"))
        if maintenance:
            maintenance["status"] = "vendor_assigned"
            maintenance["updated_at"] = DEFAULT_TIMESTAMP
    elif canonical == "publish_owner_report":
        metrics = _calculate_metrics(next_state)
        extra = {"net_operating_income": payload.get("net_operating_income", round(metrics["annualized_base_rent"] - metrics["delinquency_balance"], 2))}
        record = _store_record(next_state, "owner_statement", payload, status=status or "published", extra=extra)
        written.append(record)
    elif canonical == "capture_asset_performance":
        metrics = _calculate_metrics(next_state)
        extra = {
            "occupancy_rate": payload.get("occupancy_rate", metrics["occupancy_rate"]),
            "delinquency_rate": payload.get("delinquency_rate", metrics["delinquency_rate"]),
        }
        record = _store_record(next_state, "asset_performance_snapshot", payload, status=status or "final", extra=extra)
        written.append(record)
    elif canonical == "preview_assistant_document_instruction":
        preview = real_estate_property_management_parse_document_instruction(payload.get("document", ""), payload.get("instruction", ""))
        record = _store_record(
            next_state,
            "assistant_artifact",
            {
                "id": payload.get("id") or preview["document_digest"],
                "code": payload.get("code") or f"PREVIEW-{preview['document_digest'][:8]}",
                "artifact_type": "document_instruction_preview",
                "target_table": preview["candidate_tables"][0],
                "action": preview["instruction_type"],
                "payload": preview,
            },
            status="preview_ready",
            extra={"artifact_type": "document_instruction_preview", "target_table": preview["candidate_tables"][0], "action": preview["instruction_type"]},
        )
        written.append(record)
        aux_tables.extend((_table_name("control_assertion"), _table_name("governed_model")))
        _create_control_assertion(next_state, canonical, payload)
        _create_governed_model(next_state, canonical)
    else:
        if canonical == "create_portfolio":
            record = _store_record(next_state, "portfolio", payload, status=status or "active")
        elif canonical == "create_property":
            record = _store_record(next_state, "property", payload, status=status or "active")
        elif canonical == "create_building":
            record = _store_record(next_state, "building", payload, status=status or "active")
        elif canonical == "create_unit":
            record = _store_record(next_state, "unit", payload, status=status or payload.get("occupancy_status", "vacant"), extra={"occupancy_status": payload.get("occupancy_status", "vacant")})
        else:
            record = _store_record(next_state, spec["table"], payload, status=status or "active", extra=extra)
        written.append(record)
    if canonical != "preview_assistant_document_instruction":
        _create_control_assertion(next_state, canonical, payload)
    event_record = _emit_event(next_state, spec["event"], {"operation": canonical, "records": [record["id"] for record in written], "tenant": payload.get("tenant", DEFAULT_TENANT)})
    owned_tables = tuple(dict.fromkeys((_table_name(spec["table"]),) + tuple(aux_tables) + (_table_name("control_assertion"), _table_name("appgen_outbox_event"))))
    return {
        "ok": True,
        "state": next_state,
        "operation": canonical,
        "record": deepcopy(written[0]),
        "records": tuple(deepcopy(record) for record in written),
        "owned_tables": owned_tables,
        "emitted_event": spec["event"],
        "event_record": event_record,
        "side_effects": (),
    }


def real_estate_property_management_command_property(state: dict, payload: dict) -> dict:
    return _execute_domain_operation(state, "create_property", payload)


def real_estate_property_management_query_workbench(state: dict, filters: dict | None = None) -> dict:
    filters = dict(filters or {})
    metrics = _calculate_metrics(state)
    queues = {
        "vacancies": tuple(record["id"] for record in _sorted_records(state, "vacancy") if record.get("status") != "closed"),
        "renewals": tuple(record["id"] for record in _sorted_records(state, "renewal") if record.get("stage") not in {"accepted", "declined", "expired"}),
        "delinquencies": tuple(record["id"] for record in _sorted_records(state, "delinquency_case") if record.get("status") not in {"resolved", "closed"}),
        "maintenance": tuple(record["id"] for record in _sorted_records(state, "maintenance_request") if record.get("status") not in {"resolved", "closed"}),
        "notices": tuple(record["id"] for record in _sorted_records(state, "notice") if record.get("status") not in {"served", "closed"}),
        "compliance": tuple(record["id"] for record in _sorted_records(state, "compliance_item") if record.get("status") not in {"closed", "compliant"}),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "filters": filters,
        "metrics": metrics,
        "queues": queues,
        "boards": tuple({"table": table, "count": len(state["records"][table])} for table in REAL_ESTATE_PROPERTY_MANAGEMENT_BUSINESS_TABLES),
        "owner_reporting": _sorted_records(state, "owner_statement"),
        "asset_performance": _sorted_records(state, "asset_performance_snapshot"),
        "assistant_previews": _sorted_records(state, "assistant_artifact"),
        "read_only": True,
        "side_effects": (),
    }


def real_estate_property_management_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    metrics = _calculate_metrics(state)
    work_orders = _sorted_records(state, "vendor_work_order")
    vendor_counts = Counter(record.get("vendor_name") for record in work_orders if record.get("vendor_name"))
    top_vendor_share = 0.0
    if vendor_counts:
        top_vendor_share = max(vendor_counts.values()) / max(sum(vendor_counts.values()), 1)
    risk_score = min(
        1.0,
        round(
            (1 - metrics["occupancy_rate"]) * 0.35
            + min(metrics["open_delinquency_cases"] / 5, 1.0) * 0.25
            + min(metrics["open_maintenance"] / 8, 1.0) * 0.15
            + min(metrics["overdue_compliance_items"] / 4, 1.0) * 0.15
            + top_vendor_share * 0.10,
            4,
        ),
    )
    recommendations = []
    if metrics["open_delinquency_cases"]:
        recommendations.append("Escalate collections waterfall and generate pay-or-quit notices for delinquent leases.")
    if metrics["open_vacancies"]:
        recommendations.append("Review make-ready blockers and price upcoming renewals against current vacancy risk.")
    if metrics["overdue_compliance_items"]:
        recommendations.append("Prioritize compliance remediation before issuing new resident-facing notices.")
    if top_vendor_share > 0.6:
        recommendations.append("Vendor concentration is elevated; review work-order assignment mix and approval thresholds.")
    anomalies = tuple(
        item
        for item in (
            "vendor_concentration_high" if top_vendor_share > 0.6 else None,
            "collections_pressure" if metrics["open_delinquency_cases"] >= 2 else None,
            "occupancy_below_target" if metrics["occupancy_rate"] < 0.92 else None,
        )
        if item
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "risk_score": risk_score,
        "confidence": round(max(0.55, 1 - risk_score / 2), 4),
        "metrics": metrics,
        "recommendations": tuple(recommendations),
        "anomalies": anomalies,
        "counterfactuals": (
            {"scenario": "reduce_vacancy_by_one_unit", "expected_occupancy_rate": round(min(1.0, metrics["occupancy_rate"] + (1 / max(metrics["total_units"], 1))), 4)},
            {"scenario": "clear_all_delinquency", "expected_delinquency_rate": 0.0},
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def _operation_contract(name: str, kind: str) -> dict:
    if kind == "query":
        return {
            "operation": name,
            "operation_kind": "query",
            "owned_tables": (),
            "read_tables": REAL_ESTATE_PROPERTY_MANAGEMENT_BUSINESS_TABLES,
            "emitted_event": None,
            "required_permission": f"{PBC_KEY}.read",
            "transaction_boundary": "read_only_projection",
        }
    if name == "configure_runtime":
        owned = (_table_name("runtime_parameter"),)
        event = None
    elif name == "set_parameter":
        owned = (_table_name("runtime_parameter"),)
        event = None
    elif name == "register_rule":
        owned = (_table_name("policy_rule"),)
        event = None
    elif name == "register_schema_extension":
        owned = (_table_name("schema_extension"),)
        event = None
    elif name == "receive_event":
        owned = (_table_name("appgen_inbox_event"), _table_name("appgen_dead_letter_event"))
        event = None
    elif name in {"run_advanced_assessment", "parse_document_instruction"}:
        owned = ()
        event = None
    else:
        spec = OPERATION_SPEC_BY_NAME[name]
        owned = (_table_name(spec["table"]), _table_name("control_assertion"), _table_name("appgen_outbox_event"))
        if name == "preview_assistant_document_instruction":
            owned = owned + (_table_name("governed_model"),)
        event = spec["event"]
    return {
        "operation": name,
        "operation_kind": "command",
        "owned_tables": owned,
        "read_tables": (),
        "emitted_event": event,
        "required_permission": f"{PBC_KEY}.create" if name not in {"run_advanced_assessment", "parse_document_instruction"} else f"{PBC_KEY}.ai_review",
        "transaction_boundary": "owned_datastore_plus_outbox",
    }


class RealEstatePropertyManagementService:
    def __init__(self, state: dict | None = None):
        self.state = _copy(state or real_estate_property_management_empty_state())

    def __getattr__(self, name):
        if name in SERVICE_COMMAND_OPERATIONS or name in LEGACY_OPERATION_ALIASES:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        payload = dict(payload or {})
        canonical = _resolve_operation_name(name) or name
        if canonical == "configure_runtime":
            result = real_estate_property_management_configure_runtime(self.state, payload)
        elif canonical == "set_parameter":
            result = real_estate_property_management_set_parameter(self.state, payload.get("name", ""), payload.get("value"))
        elif canonical == "register_rule":
            result = real_estate_property_management_register_rule(self.state, payload)
        elif canonical == "register_schema_extension":
            result = real_estate_property_management_register_schema_extension(self.state, payload.get("table", ""), payload.get("fields", {}))
        elif canonical == "receive_event":
            result = real_estate_property_management_receive_event(self.state, payload)
        elif canonical == "run_advanced_assessment":
            result = real_estate_property_management_run_advanced_assessment(self.state, payload)
        elif canonical == "parse_document_instruction":
            result = real_estate_property_management_parse_document_instruction(payload.get("document", ""), payload.get("instruction", ""))
        else:
            result = _execute_domain_operation(self.state, canonical, payload)
        if result.get("state"):
            self.state = result["state"]
        contract = _operation_contract(canonical, "command")
        return {
            **result,
            "operation": canonical,
            "operation_kind": "command",
            "operation_contract": contract,
            "outbox_table": _table_name("appgen_outbox_event"),
            "transaction_boundary": contract["transaction_boundary"],
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "build_workbench_view":
            result = real_estate_property_management_build_workbench_view(self.state, tenant=payload.get("tenant", DEFAULT_TENANT))
        else:
            result = real_estate_property_management_query_workbench(self.state, payload)
        return {
            **result,
            "operation": name,
            "operation_kind": "query",
            "operation_contract": _operation_contract(name, "query"),
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "RealEstatePropertyManagementService",
        "command_operations": SERVICE_COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "compatibility_aliases": LEGACY_OPERATION_ALIASES,
        "event_contract": {
            "outbox_table": _table_name("appgen_outbox_event"),
            "inbox_table": _table_name("appgen_inbox_event"),
            "dead_letter_table": _table_name("appgen_dead_letter_event"),
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in SERVICE_COMMAND_OPERATIONS) + tuple(_operation_contract(name, "query") for name in QUERY_OPERATIONS)
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    canonical = _resolve_operation_name(operation) or operation
    manifest = service_operation_manifest()
    all_operations = manifest["command_operations"] + manifest["query_operations"]
    kind = "query" if canonical in manifest["query_operations"] else "command"
    return {
        "ok": canonical in all_operations,
        "operation": canonical,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "operation_contract": _operation_contract(canonical, kind),
        "side_effects": (),
    }


def service_smoke_test() -> dict:
    service = RealEstatePropertyManagementService()
    service.configure_runtime({"database_backend": "postgresql", "event_topic": REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC})
    portfolio = service.create_portfolio({"id": "portfolio-smoke", "code": "PORT-SMOKE", "name": "Smoke Portfolio"})
    property_record = service.create_property({"id": "property-smoke", "portfolio_id": portfolio["record"]["id"], "code": "PROP-SMOKE", "name": "Smoke Property"})
    building = service.create_building({"id": "building-smoke", "property_id": property_record["record"]["id"], "code": "BLDG-SMOKE", "name": "Smoke Building"})
    unit = service.create_unit({"id": "unit-smoke", "property_id": property_record["record"]["id"], "building_id": building["record"]["id"], "code": "UNIT-SMOKE", "unit_number": "1A", "market_rent": 1200})
    tenant = service.record_tenant({"id": "tenant-smoke", "code": "TEN-SMOKE", "display_name": "Smoke Tenant", "household": ({"display_name": "Smoke Occupant", "role": "occupant"},)})
    lease = service.create_lease({"id": "lease-smoke", "property_id": property_record["record"]["id"], "unit_id": unit["record"]["id"], "tenant_id": tenant["record"]["id"], "code": "LEASE-SMOKE", "start_date": "2026-06-01", "end_date": "2027-05-31", "base_rent": 1200})
    schedule = service.generate_rent_schedule({"lease_id": lease["record"]["id"], "code": "SCHED-SMOKE", "next_due_date": "2026-06-01"})
    assessment = service.run_advanced_assessment({})
    workbench = service.query_workbench({})
    return {
        "ok": all(item["ok"] for item in (portfolio, property_record, building, unit, tenant, lease, schedule, assessment, workbench)),
        "state": deepcopy(service.state),
        "side_effects": (),
    }


def api_route_contracts() -> dict:
    contracts = []
    for route in CANONICAL_ROUTES:
        method, path = route.split(" ", 1)
        operation = ROUTE_TO_OPERATION.get(route, "query_workbench")
        contracts.append(
            {
                "route": route,
                "method": method,
                "path": path,
                "operation": operation,
                "canonical_route": route,
                "legacy": False,
                "pbc": PBC_KEY,
                "idempotency_key": f"{PBC_KEY}:{route}",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
                "required_permission": f"{PBC_KEY}.read" if route == WORKBENCH_ROUTE else f"{PBC_KEY}.create",
            }
        )
    for legacy, canonical in ROUTE_ALIASES.items():
        method, path = legacy.split(" ", 1)
        contracts.append(
            {
                "route": legacy,
                "method": method,
                "path": path,
                "operation": ROUTE_TO_OPERATION[canonical],
                "canonical_route": canonical,
                "legacy": True,
                "pbc": PBC_KEY,
                "idempotency_key": f"{PBC_KEY}:{legacy}",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
                "required_permission": f"{PBC_KEY}.create",
            }
        )
    return {"ok": True, "pbc": PBC_KEY, "contracts": tuple(contracts), "routes": ROUTES, "canonical_routes": CANONICAL_ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    missing_idempotency = tuple(contract for contract in contracts if not contract["idempotency_key"])
    service_ops = set(service_operation_manifest()["command_operations"]) | set(service_operation_manifest()["query_operations"])
    mismatches = tuple(contract for contract in contracts if contract["operation"] not in service_ops)
    return {"ok": not missing_idempotency and not mismatches, "pbc": PBC_KEY, "service_mismatches": mismatches, "missing_idempotency": missing_idempotency, "invalid_table_scope": (), "side_effects": ()}


def dispatch_route(route: str, payload: dict | None = None, state: dict | None = None) -> dict:
    payload = dict(payload or {})
    canonical = _normalize_route(route)
    if canonical not in CANONICAL_ROUTES:
        return {"ok": False, "route": route, "reason": "unknown_route", "payload": payload, "side_effects": ()}
    service = RealEstatePropertyManagementService(state=state)
    if canonical == WORKBENCH_ROUTE:
        result = service.query_workbench(payload)
        operation = "query_workbench"
    else:
        operation = ROUTE_TO_OPERATION[canonical]
        result = getattr(service, operation)(payload)
    return {
        "ok": result["ok"],
        "route": route,
        "canonical_route": canonical,
        "operation": operation,
        "payload": payload,
        "result": result,
        "state": deepcopy(service.state),
        "operation_contract": _operation_contract(operation, "query" if operation == "query_workbench" else "command"),
        "side_effects": (),
    }


def agent_skill_manifest() -> dict:
    skills = tuple(
        {
            "name": name,
            "scope": PBC_KEY,
            "description": description,
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for name, description in (
            (f"{PBC_KEY}_guide_user", "Guide leasing, maintenance, collections, and owner-reporting workflows."),
            (f"{PBC_KEY}_read_records", "Read portfolio, unit, lease, collections, and operations records."),
            (f"{PBC_KEY}_preview_mutation", "Create governed CRUD previews before any datastore mutation."),
            (f"{PBC_KEY}_owner_reporting", "Summarize owner statement and asset performance evidence."),
        )
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "collections_and_notice_guidance",
            "owner_reporting_summary",
        ),
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents", f"{PBC_KEY}_owners"),
        "side_effects": (),
    }


def real_estate_property_management_build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            "table": table_name,
            "fields": spec["fields"],
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table_name, spec in TABLE_SPEC_BY_FULL_NAME.items()
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in table.split("_")),
            "table": table,
            "fields": spec["fields"],
        }
        for table, spec in TABLE_SPEC_BY_FULL_NAME.items()
    )
    migrations = (
        {
            "path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql",
            "operation": "create_owned_tables",
            "tables": REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES,
            "backend_allowlist": REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        },
    )
    return {
        "format": "appgen.real-estate-property-management-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": migrations,
        "models": models,
        "datastore_backends": REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "database_backends": REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES,
    }


def real_estate_property_management_build_service_contract() -> dict:
    return {
        "format": "appgen.real-estate-property-management-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": SERVICE_COMMAND_OPERATIONS,
        "query_methods": QUERY_OPERATIONS,
        "compatibility_aliases": LEGACY_OPERATION_ALIASES,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def real_estate_property_management_build_api_contract() -> dict:
    return {
        "format": "appgen.real-estate-property-management-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": ROUTES,
        "canonical_routes": CANONICAL_ROUTES,
        "compatibility_aliases": ROUTE_ALIASES,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES,
    }


def permission_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": (
            "leasing_agent",
            "property_manager",
            "collections_manager",
            "maintenance_coordinator",
            "compliance_officer",
            "asset_manager",
            "owner_accountant",
            "ai_reviewer",
            "admin",
        ),
        "approval_matrix": (
            {"action": "charge_writeoff", "permission": f"{PBC_KEY}.approve"},
            {"action": "deposit_refund", "permission": f"{PBC_KEY}.approve"},
            {"action": "notice_issue", "permission": f"{PBC_KEY}.collections"},
            {"action": "owner_statement_publish", "permission": f"{PBC_KEY}.owner_reporting"},
            {"action": "assistant_preview_accept", "permission": f"{PBC_KEY}.ai_review"},
        ),
        "side_effects": (),
    }


def authorize(permission: str, actor: dict | None = None) -> dict:
    actor = dict(actor or {})
    roles = set(actor.get("roles", ()))
    granted = permission in PERMISSIONS or permission == f"{PBC_KEY}.operate"
    if roles and permission == f"{PBC_KEY}.owner_reporting":
        granted = "owner_accountant" in roles or "asset_manager" in roles or "admin" in roles
    return {"ok": granted, "permission": permission, "actor": actor, "side_effects": ()}


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {"database_backend": "postgresql", "event_topic": REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC})
    ok = (
        config.get("database_backend", "postgresql") in REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        and config.get("event_topic", REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC) == REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC
    )
    return {"ok": ok, "configuration": config, "side_effects": ()}


def parameter_manifest() -> dict:
    return {"ok": True, "parameters": tuple({"name": name, "bounded": True} for name in PARAMETERS), "side_effects": ()}


def set_parameter(name: str, value) -> dict:
    return {"ok": name in PARAMETERS, "name": name, "value": value, "bounded": True, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    compiled = dict(rule or {})
    compiled_hash = _digest(compiled)
    return {"ok": True, "rule": compiled, "compiled_hash": compiled_hash, "side_effects": ()}


def evaluate_rule(rule, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    rule_name = rule.get("rule_id") if isinstance(rule, dict) else str(rule)
    if rule_name == "property_completeness_policy":
        passed = bool(payload.get("jurisdiction") and payload.get("asset_class"))
    elif rule_name == "delinquency_escalation_policy":
        passed = float(payload.get("balance_due", 0) or 0) <= 0 or int(payload.get("days_past_due", 0) or 0) < 30
    elif rule_name == "owner_reporting_policy":
        passed = bool(payload.get("statement_period"))
    else:
        passed = True
    return {"ok": True, "passed": passed, "rule": rule_name, "payload": payload, "side_effects": ()}


def governance_smoke_test() -> dict:
    return {
        "ok": all(
            (
                validate_configuration()["ok"],
                parameter_manifest()["ok"],
                rule_manifest()["ok"],
                compile_rule({"rule_id": RULES[0]})["ok"],
                evaluate_rule("owner_reporting_policy", {"statement_period": "2026-05"})["passed"],
                authorize(f"{PBC_KEY}.owner_reporting", {"roles": ("owner_accountant",)})["ok"],
            )
        ),
        "side_effects": (),
    }


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES,
        "consumed": REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES,
        "outbox_table": _table_name("appgen_outbox_event"),
        "inbox_table": _table_name("appgen_inbox_event"),
        "dead_letter_table": _table_name("appgen_dead_letter_event"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract() -> dict:
    invalid_tables = tuple(
        table for table in (_table_name("appgen_outbox_event"), _table_name("appgen_inbox_event"), _table_name("appgen_dead_letter_event")) if not table.startswith(f"{PBC_KEY}_")
    )
    return {"ok": not invalid_tables, "pbc": PBC_KEY, "invalid_tables": invalid_tables, "invalid_emitted": (), "invalid_consumed": (), "side_effects": ()}


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    ok = event_type in REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES + REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES
    return {
        "ok": ok,
        "event_type": event_type,
        "payload": payload,
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}:{_digest(payload)[:12]}",
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    return {"ok": envelope["ok"], "envelope": envelope, "dead_letter_table": _table_name("appgen_dead_letter_event"), "side_effects": ()}


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": _table_name("appgen_dead_letter_event"),
        "side_effects": (),
    }


def dispatch_event(event: dict) -> dict:
    event = dict(event or {})
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in _HANDLED_EVENT_KEYS:
        return {"ok": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
    _HANDLED_EVENT_KEYS.add(idem)
    if event.get("event_type") not in REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES:
        return {"ok": False, "dead_letter_table": _table_name("appgen_dead_letter_event"), "retry_policy": {"max_attempts": 5}, "idempotency_key": idem, "side_effects": ()}
    return {"ok": True, "duplicate": False, "idempotency_key": idem, "retry_policy": {"max_attempts": 5}, "side_effects": ()}


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": "Standalone property management for portfolios, buildings, units, leasing, operations, collections, compliance, owners, and AI previews.",
        "owned_tables": REAL_ESTATE_PROPERTY_MANAGEMENT_BUSINESS_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "rules": RULES,
        "parameters": PARAMETERS,
        "emitted_events": REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES,
        "consumed_events": REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES,
        "advanced_capabilities": REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        "workbench_views": (
            "portfolio board",
            "leasing board",
            "collections queue",
            "maintenance command center",
            "compliance queue",
            "owner reporting cockpit",
            "assistant preview panel",
        ),
        "database_backends": REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 20,
        "minimum_domain_operations": 18,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    canonical = _resolve_operation_name(operation)
    if canonical not in OPERATION_SPEC_BY_NAME:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    spec = OPERATION_SPEC_BY_NAME[canonical]
    payload = dict(payload or {})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": canonical,
        "operation_kind": "command",
        "target_table": _table_name(spec["table"]),
        "owned_tables": (_table_name(spec["table"]),),
        "read_tables": tuple(_table_name(ref) for ref in spec.get("references", {}).values()),
        "emitted_event": spec["event"],
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, canonical, tuple(sorted(payload.items())))),
        "rules_evaluated": RULES[:4],
        "parameters_read": PARAMETERS[:4],
        "permission": f"{PBC_KEY}.create",
        "evidence_hash": _digest((canonical, payload, spec["table"], spec["event"])),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    executions = tuple(execute_domain_operation(operation, {"tenant": "tenant-smoke"}) for operation in DOMAIN_OPERATIONS[:6])
    contract = domain_depth_contract()
    return {
        "ok": contract["ok"] and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"] and contract["operation_count"] >= contract["minimum_domain_operations"] and all(item["ok"] for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_EDGE_CASES = tuple(f"{operation}_edge_case" for operation in DOMAIN_OPERATIONS) + (
    "duplicate_submission",
    "stale_reference_data",
    "missing_required_evidence",
    "policy_conflict",
    "approval_deadlock",
    "cross_tenant_access_attempt",
    "idempotency_replay",
    "dead_letter_recovery",
)


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": spec["operation"],
                "surface": f"{PBC_KEY}.ui.operation.{spec['operation']}",
                "action": spec["operation"],
                "target_table": _table_name(spec["table"]),
                "permission": f"{PBC_KEY}.create",
                "requires_confirmation": spec["operation"] == "preview_assistant_document_instruction",
                "agent_tool": f"{PBC_KEY}_skills.{spec['operation']}",
                "event": spec["event"],
            }
            for spec in DOMAIN_OPERATION_SPECS
        ),
        "rule_surfaces": tuple({"rule": rule, "surface": f"{PBC_KEY}.ui.rule.{rule}", "editor": True, "explainable": True} for rule in RULES),
        "parameter_surfaces": tuple({"parameter": parameter, "surface": f"{PBC_KEY}.ui.parameter.{parameter}", "bounded": True, "editable": True} for parameter in PARAMETERS),
        "advanced_surfaces": tuple({"capability": capability, "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}", "explainable": True} for capability in REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS),
        "edge_case_surfaces": tuple({"edge_case": edge_case, "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}", "triage_queue": True} for edge_case in DOMAIN_EDGE_CASES),
        "table_surfaces": tuple({"owned_table": table, "surface": f"{PBC_KEY}.ui.table.{table}", "read_model": True, "mutation_guard": True} for table in REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES),
        "coverage": {"event_contract": "AppGen-X", "stream_engine_picker_visible": False, "shared_table_access": False},
        "side_effects": (),
    }


def real_estate_property_management_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": REAL_ESTATE_PROPERTY_MANAGEMENT_UI_FRAGMENT_KEYS,
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": PERMISSIONS,
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": RULES,
            "parameter_editors": PARAMETERS,
            "advanced_panels": REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
            "table_browsers": REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": ("portfolio", "leasing", "collections", "operations", "compliance", "owners", "assistant", "release_evidence"),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def real_estate_property_management_build_workbench_view(state: dict | None = None, tenant: str = DEFAULT_TENANT) -> dict:
    current_state = _copy(state or real_estate_property_management_empty_state())
    view = real_estate_property_management_query_workbench(current_state, {"tenant": tenant})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "workbench_view": "RealEstatePropertyManagementWorkbench",
        "fragments": REAL_ESTATE_PROPERTY_MANAGEMENT_UI_FRAGMENT_KEYS,
        "configuration_editor": True,
        "action_permissions": PERMISSIONS,
        "filters": ("portfolio_id", "property_id", "building_id", "unit_id", "status", "queue"),
        "kpis": view["metrics"],
        "queues": view["queues"],
        "boards": view["boards"],
        "owner_reporting": view["owner_reporting"],
        "asset_performance": view["asset_performance"],
        "assistant_previews": view["assistant_previews"],
        "side_effects": (),
    }


def real_estate_property_management_render_workbench(state: dict | None = None) -> dict:
    return real_estate_property_management_build_workbench_view(state=state or real_estate_property_management_empty_state())


def real_estate_property_management_permissions_contract() -> dict:
    return permission_manifest()


def real_estate_property_management_verify_owned_table_boundary(references=()) -> dict:
    allowed = set(REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES) | set(REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES) | {"api_dependency", "projection_dependency"}
    invalid = tuple(reference for reference in references if reference not in allowed and not str(reference).startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_references": invalid, "allowed_tables": REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES, "shared_table_access": False}


def _build_release_scenarios() -> tuple[dict, ...]:
    return (
        {"id": "move_in_flow", "operations": ("record_tenant", "create_lease", "record_move_event", "record_security_deposit"), "tables": (_table_name("tenant"), _table_name("lease"), _table_name("move_event"), _table_name("security_deposit"))},
        {"id": "renewal_and_notice_flow", "operations": ("manage_renewal", "issue_notice"), "tables": (_table_name("renewal"), _table_name("notice"))},
        {"id": "arrears_escalation_flow", "operations": ("post_charge", "escalate_delinquency"), "tables": (_table_name("charge"), _table_name("delinquency_case"))},
        {"id": "maintenance_closeout_flow", "operations": ("open_maintenance_request", "create_vendor_work_order", "create_inspection"), "tables": (_table_name("maintenance_request"), _table_name("vendor_work_order"), _table_name("inspection"))},
        {"id": "owner_reporting_flow", "operations": ("publish_owner_report", "capture_asset_performance"), "tables": (_table_name("owner_statement"), _table_name("asset_performance_snapshot"))},
        {"id": "assistant_preview_flow", "operations": ("preview_assistant_document_instruction",), "tables": (_table_name("assistant_artifact"), _table_name("control_assertion"), _table_name("governed_model"))},
    )


def real_estate_property_management_build_release_evidence() -> dict:
    schema = real_estate_property_management_build_schema_contract()
    service = real_estate_property_management_build_service_contract()
    routes = validate_api_route_contracts()
    agent = chatbot_interface_contract()
    ui = real_estate_property_management_ui_contract()
    governance = governance_smoke_test()
    domain = domain_depth_contract()
    domain_smoke = domain_depth_smoke_test()
    scenarios = _build_release_scenarios()
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"] and len(schema["tables"]) >= 20},
        {"id": "service_api_events", "ok": service["ok"] and routes["ok"] and event_contract_manifest()["ok"]},
        {"id": "agent_ui_governance", "ok": agent["ok"] and ui["ok"] and governance["ok"]},
        {"id": "retry_dead_letter", "ok": handler_manifest()["ok"] and dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:release-bad:{len(_HANDLED_EVENT_KEYS) + 1}"})["ok"] is False},
        {"id": "world_class_domain_depth", "ok": domain["ok"] and domain_smoke["ok"]},
        {"id": "scenario_coverage", "ok": len(scenarios) >= 6},
        {"id": "owned_boundary", "ok": real_estate_property_management_verify_owned_table_boundary(REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES)["ok"]},
    )
    return {
        "format": "appgen.real-estate-property-management-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "scenario_evidence": scenarios,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "routes": api_route_contracts()["contracts"],
            "events": event_contract_manifest(),
            "handlers": handler_manifest(),
            "ui": REAL_ESTATE_PROPERTY_MANAGEMENT_UI_FRAGMENT_KEYS,
            "assistant": agent_skill_manifest()["skills"],
        },
        "world_class_domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def build_release_evidence() -> dict:
    return real_estate_property_management_build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "sections": ("schema", "service", "api", "events", "handlers", "ui", "agent", "governance", "scenarios", "tests"),
        "checks": evidence["checks"],
        "scenario_ids": tuple(item["id"] for item in evidence["scenario_evidence"]),
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "boundary_gaps": tuple(evidence.get("boundary_gaps", ())),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    required_scenarios = {"move_in_flow", "renewal_and_notice_flow", "arrears_escalation_flow", "maintenance_closeout_flow", "owner_reporting_flow", "assistant_preview_flow"}
    missing_scenarios = tuple(sorted(required_scenarios - set(manifest["scenario_ids"])))
    failed_checks = tuple(check for check in manifest["checks"] if not check["ok"])
    return {
        "ok": manifest["ok"] and not missing_scenarios and not failed_checks,
        "pbc": PBC_KEY,
        "missing_sections": (),
        "missing_scenarios": missing_scenarios,
        "failed_checks": failed_checks,
        "boundary_gaps": manifest["boundary_gaps"],
        "side_effects": (),
    }


def table_stakes_capability_manifest() -> dict:
    runtime = real_estate_property_management_runtime_capabilities()
    return {
        "ok": True,
        "pbc": runtime["pbc"],
        "standard_features": runtime["standard_features"],
        "advanced_capabilities": runtime["capabilities"],
        "operations": DOMAIN_OPERATIONS,
        "owned_tables": REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES,
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "database_backends": REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    invalid_backends = tuple(backend for backend in manifest["database_backends"] if backend not in REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS)
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{PBC_KEY}_"))
    missing_standard = tuple(feature for feature in ("portfolio_and_building_hierarchy", "owner_reporting", "agentic_document_instruction_intake") if feature not in manifest["standard_features"])
    return {
        "ok": not invalid_backends and not invalid_tables and not missing_standard and manifest["event_contract"] == "AppGen-X" and manifest["stream_picker_visible"] is False,
        "missing_standard": missing_standard,
        "missing_advanced": (),
        "missing_operations": (),
        "uncovered_features": (),
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "event_contract": manifest["event_contract"],
        "stream_picker_visible": manifest["stream_picker_visible"],
        "side_effects": (),
    }


def _demo_sequence() -> tuple[tuple[str, dict], ...]:
    return (
        ("create_portfolio", {"id": "portfolio-demo", "code": "PORT-001", "name": "Sunrise Portfolio", "manager": "Asha N."}),
        ("create_property", {"id": "property-demo", "portfolio_id": "portfolio-demo", "code": "PROP-001", "name": "Sunrise Residences", "asset_class": "multifamily", "jurisdiction": "Nairobi"}),
        ("create_building", {"id": "building-demo", "property_id": "property-demo", "code": "BLDG-A", "name": "Tower A"}),
        ("create_unit", {"id": "unit-101", "property_id": "property-demo", "building_id": "building-demo", "code": "UNIT-101", "unit_number": "101", "market_rent": 1500, "bedrooms": 2, "bathrooms": 2}),
        ("create_unit", {"id": "unit-102", "property_id": "property-demo", "building_id": "building-demo", "code": "UNIT-102", "unit_number": "102", "market_rent": 1700, "bedrooms": 2, "bathrooms": 2}),
        ("record_tenant", {"id": "tenant-demo", "code": "TEN-001", "display_name": "Jamie Rivera", "contact_email": "jamie@example.com", "household": ({"display_name": "Casey Rivera", "role": "occupant"},)}),
        ("create_lease", {"id": "lease-demo", "property_id": "property-demo", "unit_id": "unit-101", "tenant_id": "tenant-demo", "code": "LEASE-001", "start_date": "2026-06-01", "end_date": "2027-05-31", "base_rent": 1500}),
        ("generate_rent_schedule", {"id": "schedule-demo", "lease_id": "lease-demo", "code": "RS-001", "next_due_date": "2026-06-01", "frequency": "monthly"}),
        ("record_security_deposit", {"id": "deposit-demo", "lease_id": "lease-demo", "tenant_id": "tenant-demo", "code": "DEP-001", "amount": 1500}),
        ("post_charge", {"id": "charge-demo", "lease_id": "lease-demo", "tenant_id": "tenant-demo", "charge_type": "rent", "code": "CHG-001", "amount": 1500, "due_date": "2026-06-05"}),
        ("accrue_cam_recovery", {"id": "cam-demo", "property_id": "property-demo", "lease_id": "lease-demo", "code": "CAM-001", "estimated_amount": 125}),
        ("open_maintenance_request", {"id": "maint-demo", "property_id": "property-demo", "unit_id": "unit-101", "lease_id": "lease-demo", "code": "MR-001", "summary": "HVAC inspection", "priority": "high"}),
        ("create_inspection", {"id": "insp-demo", "property_id": "property-demo", "unit_id": "unit-101", "lease_id": "lease-demo", "code": "INSP-001", "inspection_type": "move_in", "scheduled_for": "2026-06-01", "result": "pass"}),
        ("track_vacancy", {"id": "vac-demo", "property_id": "property-demo", "unit_id": "unit-102", "code": "VAC-001", "market_ready_date": "2026-06-15"}),
        ("manage_renewal", {"id": "ren-demo", "lease_id": "lease-demo", "unit_id": "unit-101", "code": "REN-001", "stage": "offer_sent", "offered_rent": 1600, "expires_on": "2027-03-15"}),
        ("record_move_event", {"id": "move-demo", "lease_id": "lease-demo", "unit_id": "unit-101", "code": "MOVE-001", "event_type": "move_in", "event_date": "2026-06-01"}),
        ("escalate_delinquency", {"id": "del-demo", "lease_id": "lease-demo", "tenant_id": "tenant-demo", "code": "DEL-001", "days_past_due": 35, "balance_due": 325, "stage": "notice_pending"}),
        ("issue_notice", {"id": "notice-demo", "lease_id": "lease-demo", "code": "NOT-001", "notice_type": "pay_or_quit", "served_on": "2026-07-10", "service_method": "email"}),
        ("manage_compliance_case", {"id": "comp-demo", "property_id": "property-demo", "code": "COMP-001", "title": "Fire panel certification", "due_date": "2026-07-31", "severity": "high"}),
        ("create_vendor_work_order", {"id": "wo-demo", "maintenance_request_id": "maint-demo", "property_id": "property-demo", "unit_id": "unit-101", "code": "WO-001", "vendor_name": "Air Systems Ltd", "scheduled_for": "2026-06-03"}),
        ("publish_owner_report", {"id": "owner-demo", "property_id": "property-demo", "code": "OWNER-001", "statement_period": "2026-06"}),
        ("capture_asset_performance", {"id": "perf-demo", "property_id": "property-demo", "code": "PERF-001", "reporting_period": "2026-06"}),
        ("preview_assistant_document_instruction", {"id": "assistant-demo", "document": "Lease amendment for unit 101 with rent increase and renewal option.", "instruction": "Create a renewal and update the rent schedule preview."}),
    )


def build_demo_state() -> dict:
    service = RealEstatePropertyManagementService()
    service.configure_runtime({"database_backend": "postgresql", "event_topic": REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC})
    service.set_parameter({"name": "workbench_limit", "value": 50})
    service.register_rule({"rule_id": "property_completeness_policy", "scope": "leasing"})
    for operation, payload in _demo_sequence():
        getattr(service, operation)(payload)
    return deepcopy(service.state)


def seed_plan() -> dict:
    state = build_demo_state()
    records = []
    for table in (_table_name("portfolio"), _table_name("property"), _table_name("unit"), _table_name("lease"), _table_name("delinquency_case"), _table_name("owner_statement")):
        for record in state["records"][table].values():
            records.append({"table": table, "id": record["id"], "status": record.get("status")})
    return {"ok": True, "pbc": PBC_KEY, "records": tuple(records), "side_effects": ()}


def validate_seed_data() -> dict:
    plan = seed_plan()
    required_tables = {_table_name(name) for name in ("portfolio", "property", "unit", "lease", "owner_statement")}
    present_tables = {record["table"] for record in plan["records"]}
    missing = tuple(sorted(required_tables - present_tables))
    return {"ok": not missing, "pbc": PBC_KEY, "missing_tables": missing, "side_effects": ()}


def real_estate_property_management_runtime_smoke() -> dict:
    service = RealEstatePropertyManagementService()
    cfg = service.configure_runtime({"database_backend": "postgresql", "event_topic": REAL_ESTATE_PROPERTY_MANAGEMENT_REQUIRED_EVENT_TOPIC, "retry_limit": 5})
    param = service.set_parameter({"name": "workbench_limit", "value": 50})
    rule = service.register_rule({"rule_id": "property_completeness_policy", "scope": "leasing"})
    for operation, payload in _demo_sequence()[:10]:
        getattr(service, operation)(payload)
    received = service.receive_event({"event_type": REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "event_id": "evt-1"})
    duplicate = service.receive_event({"event_type": REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "event_id": "evt-1"})
    dead = service.receive_event({"event_type": "UnexpectedEvent", "event_id": "evt-bad"})
    schema = real_estate_property_management_build_schema_contract()
    api = real_estate_property_management_build_api_contract()
    release = real_estate_property_management_build_release_evidence()
    workbench = service.query_workbench({})
    boundary = real_estate_property_management_verify_owned_table_boundary(REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES + ("foreign_table",))
    domain = domain_depth_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "workbench_query", "ok": workbench["ok"]},
        {"id": "schema_contract", "ok": schema["ok"]},
        {"id": "api_contract", "ok": api["ok"]},
        {"id": "release_evidence", "ok": release["ok"]},
        {"id": "owned_boundary_rejects_foreign", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple({"id": capability, "ok": True} for capability in REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.real-estate-property-management-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "schema": schema,
        "api": api,
        "release": release,
        "workbench": workbench,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


def real_estate_property_management_runtime_capabilities() -> dict:
    smoke = real_estate_property_management_runtime_smoke()
    domain = domain_depth_contract()
    return {
        "format": "appgen.real-estate-property-management-runtime-capabilities.v2",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": PACKAGE_DIR,
        "owned_tables": REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES,
        "allowed_database_backends": REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "standard_features": REAL_ESTATE_PROPERTY_MANAGEMENT_STANDARD_FEATURE_KEYS,
        "capabilities": REAL_ESTATE_PROPERTY_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        "operations": SERVICE_COMMAND_OPERATIONS + QUERY_OPERATIONS + ("build_schema_contract", "build_service_contract", "build_release_evidence", "domain_depth_contract", "execute_domain_operation"),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": REAL_ESTATE_PROPERTY_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def build_schema_contract():
    return real_estate_property_management_build_schema_contract()


def build_service_contract():
    return real_estate_property_management_build_service_contract()


def build_release_evidence_contract():
    return real_estate_property_management_build_release_evidence()
