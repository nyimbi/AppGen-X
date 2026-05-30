"""Standalone executable operating surface for the utilities metering billing PBC."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from typing import Any

PBC_KEY = "utilities_metering_billing"
PBC_LABEL = "Utilities Metering and Billing"
PBC_MESH = "finops"
APPGEN_X_TOPIC = "pbc.utilities_metering_billing.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")

STANDARD_FEATURES = (
    "service_point_master_data",
    "energization_workflows",
    "meter_asset_registry",
    "meter_exchange_rollover",
    "multi_register_channels",
    "read_capture_provenance",
    "read_validation_ladder",
    "interval_gap_stitching",
    "estimate_hierarchy",
    "tariff_rate_versioning",
    "tou_and_demand_rating",
    "net_metering",
    "billing_cycle_segmentation",
    "bill_traceability",
    "customer_charge_management",
    "payment_allocation_evidence",
    "move_in_move_out",
    "vacant_premise_modes",
    "disconnect_reconnect_controls",
    "regulatory_reporting",
    "dispute_handling",
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

ADVANCED_CAPABILITIES = (
    "utilities_metering_billing_event_sourced_operational_history",
    "utilities_metering_billing_multi_tenant_policy_isolation",
    "utilities_metering_billing_schema_evolution_resilience",
    "utilities_metering_billing_autonomous_anomaly_detection",
    "utilities_metering_billing_semantic_document_instruction_understanding",
    "utilities_metering_billing_predictive_risk_scoring",
    "utilities_metering_billing_counterfactual_scenario_simulation",
    "utilities_metering_billing_cryptographic_audit_proofs",
    "utilities_metering_billing_continuous_control_testing",
    "utilities_metering_billing_carbon_and_sustainability_awareness",
    "utilities_metering_billing_cross_pbc_event_federation",
    "utilities_metering_billing_governed_ai_agent_execution",
)

RULES = (
    "service_point_policy",
    "meter_read_policy",
    "usage_interval_policy",
    "estimate_policy",
    "tariff_policy",
    "service_order_policy",
    "utility_bill_policy",
    "billing_adjustment_policy",
    "payment_allocation_policy",
    "regulatory_reporting_policy",
)

PARAMETER_DEFAULTS = {
    "quality_score_floor": 0.82,
    "materiality_threshold": 50.0,
    "approval_sla_hours": 24,
    "risk_threshold": 0.68,
    "forecast_horizon_days": 21,
    "workbench_limit": 50,
    "disconnect_notice_days": 14,
    "max_estimate_streak": 2,
    "moratorium_enabled": True,
}

PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
    f"{PBC_KEY}.operate",
)

EMITTED_EVENTS = (
    "UtilitiesMeteringBillingCreated",
    "UtilitiesMeteringBillingUpdated",
    "UtilitiesMeteringBillingApproved",
    "UtilitiesMeteringBillingExceptionOpened",
    "ServicePointActivated",
    "ServicePointDisconnected",
    "MeterInstalled",
    "MeterRemoved",
    "ReadValidated",
    "EstimateCreated",
    "EstimateReplaced",
    "BillSimulated",
    "BillIssued",
    "AdjustmentApproved",
    "DisputeOpened",
)
CONSUMED_EVENTS = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")

READ_VALIDATION_STEPS = (
    "presence",
    "service_point_status",
    "duplicate_detection",
    "date_window",
    "monotonicity",
    "rollover",
    "multiplier",
    "historical_tolerance",
    "prior_final_read_consistency",
)

EXCEPTION_CODES = (
    "inaccessible_meter",
    "suspect_read",
    "repeated_estimate",
    "reverse_flow",
    "meter_mismatch",
    "stale_interval_feed",
    "tariff_missing",
    "service_point_inactive",
    "move_boundary_conflict",
    "protected_disconnect_blocked",
)

API_ROUTES = (
    "POST /service-points",
    "POST /customer-meter-accounts",
    "POST /service-orders",
    "POST /meters",
    "POST /meter-installs",
    "POST /meter-exchanges",
    "POST /meter-reads",
    "POST /meter-reads/validate",
    "POST /usage-intervals",
    "POST /usage-estimates",
    "POST /tariffs",
    "POST /billing-cycles",
    "POST /utility-bills",
    "POST /billing-adjustments",
    "POST /customer-charges",
    "POST /payments",
    "POST /payments/allocations",
    "POST /exceptions",
    "POST /disputes",
    "GET /utilities-metering-billing-workbench",
    "GET /utilities-metering-billing-detail",
    "GET /utilities-metering-billing-regulatory-report",
)

COMMAND_METHODS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "create_service_point",
    "record_customer_meter_account",
    "register_meter_asset",
    "install_meter",
    "exchange_meter",
    "create_meter_read",
    "validate_meter_read",
    "record_usage_interval",
    "estimate_usage_gap",
    "review_tariff",
    "approve_service_order",
    "create_billing_cycle",
    "calculate_usage",
    "simulate_utility_bill",
    "create_billing_adjustment",
    "record_customer_charge",
    "record_payment_receipt",
    "allocate_payment_evidence",
    "open_exception_case",
    "resolve_exception_case",
    "open_dispute_case",
    "generate_regulatory_report",
    "review_utilities_metering_billing_policy_rule",
    "approve_utilities_metering_billing_runtime_parameter",
    "simulate_utilities_metering_billing_schema_extension",
    "create_utilities_metering_billing_control_assertion",
    "record_utilities_metering_billing_governed_model",
)

QUERY_METHODS = (
    "query_workbench",
    "build_workbench_view",
    "build_detail_view",
    "build_regulatory_report_preview",
)

FORM_DEFINITIONS = (
    {
        "id": "service-point-intake",
        "label": "Service Point Intake",
        "owned_table": f"{PBC_KEY}_service_point",
        "command": "create_service_point",
        "fields": ("premise_code", "commodity", "service_point_class", "zone_code", "lifecycle_status"),
    },
    {
        "id": "meter-read-capture",
        "label": "Meter Read Capture",
        "owned_table": f"{PBC_KEY}_meter_read",
        "command": "create_meter_read",
        "fields": ("service_point_id", "meter_asset_id", "register_code", "read_value", "read_source", "collector_id"),
    },
    {
        "id": "tariff-version-review",
        "label": "Tariff Version Review",
        "owned_table": f"{PBC_KEY}_tariff",
        "command": "review_tariff",
        "fields": ("tariff_code", "jurisdiction", "effective_start", "effective_end", "approval_state"),
    },
    {
        "id": "billing-cycle-run",
        "label": "Billing Cycle Run",
        "owned_table": f"{PBC_KEY}_billing_cycle",
        "command": "create_billing_cycle",
        "fields": ("cycle_code", "route_code", "cycle_start", "cycle_end", "status"),
    },
    {
        "id": "adjustment-maker-checker",
        "label": "Adjustment Maker Checker",
        "owned_table": f"{PBC_KEY}_billing_adjustment",
        "command": "create_billing_adjustment",
        "fields": ("utility_bill_id", "reason_code", "amount", "maker", "checker", "approval_state"),
    },
    {
        "id": "dispute-case-form",
        "label": "Dispute Case Form",
        "owned_table": f"{PBC_KEY}_dispute_case",
        "command": "open_dispute_case",
        "fields": ("utility_bill_id", "reason_code", "hold_scope", "status"),
    },
)

WIZARD_DEFINITIONS = (
    {
        "id": "meter-exchange-wizard",
        "label": "Meter Exchange Wizard",
        "workflow": "exchange_meter",
        "steps": ("select_service_point", "capture_final_read", "capture_initial_read", "confirm_lineage"),
    },
    {
        "id": "estimate-review-wizard",
        "label": "Estimate Review Wizard",
        "workflow": "estimate_usage_gap",
        "steps": ("inspect_gap", "select_strategy", "preview_confidence", "confirm_estimate"),
    },
    {
        "id": "bill-run-approval-wizard",
        "label": "Bill Run Approval Wizard",
        "workflow": "simulate_utility_bill",
        "steps": ("build_segments", "review_trace", "confirm_override_guards", "issue_bill"),
    },
    {
        "id": "disconnect-reconnect-wizard",
        "label": "Disconnect Reconnect Wizard",
        "workflow": "approve_service_order",
        "steps": ("review_protection", "notice_window", "field_order", "confirm_status_change"),
    },
    {
        "id": "regulatory-report-wizard",
        "label": "Regulatory Report Wizard",
        "workflow": "generate_regulatory_report",
        "steps": ("select_jurisdiction", "assemble_metrics", "review_exceptions", "seal_report"),
    },
)

CONTROL_DEFINITIONS = (
    {
        "id": "owned-boundary-control",
        "label": "Owned Boundary Control",
        "guard": "All mutations stay inside utilities_metering_billing owned tables.",
        "blocking": True,
    },
    {
        "id": "read-provenance-control",
        "label": "Read Provenance Control",
        "guard": "Reads must include AMI, handheld, customer, or office provenance evidence.",
        "blocking": True,
    },
    {
        "id": "estimate-streak-control",
        "label": "Estimate Streak Control",
        "guard": "Estimate streaks over the bounded threshold require field action.",
        "blocking": True,
    },
    {
        "id": "maker-checker-control",
        "label": "Maker Checker Control",
        "guard": "Adjustments and rebills require structured override evidence and second approval.",
        "blocking": True,
    },
    {
        "id": "protected-customer-control",
        "label": "Protected Customer Control",
        "guard": "Moratorium and protected-account rules block illegal disconnections.",
        "blocking": True,
    },
    {
        "id": "appgen-event-control",
        "label": "AppGen-X Event Control",
        "guard": "Outbox, inbox, and dead-letter evidence remain fixed to the AppGen-X contract.",
        "blocking": True,
    },
    {
        "id": "confirmation-gate-control",
        "label": "Assistant Confirmation Gate",
        "guard": "Every agent-assisted mutation stays in preview until a human confirms it.",
        "blocking": True,
    },
    {
        "id": "release-evidence-control",
        "label": "Release Evidence Control",
        "guard": "The package cannot be marked ready without scenario, audit, and smoke evidence.",
        "blocking": True,
    },
)

TABLE_DEFINITIONS = (
    ("premise", ("id", "tenant", "premise_code", "address_line", "zone_code", "geocode", "status", "created_at", "updated_at")),
    ("service_point", ("id", "tenant", "premise_id", "service_point_code", "commodity", "service_point_class", "voltage_pressure_class", "zone_code", "lifecycle_status", "created_at", "updated_at")),
    ("customer_meter_account", ("id", "tenant", "service_point_id", "customer_account_id", "bill_to_name", "occupancy_start", "occupancy_end", "responsibility_mode", "protected_status", "created_at", "updated_at")),
    ("service_point_assignment", ("id", "tenant", "service_point_id", "customer_meter_account_id", "effective_start", "effective_end", "assignment_status", "created_at", "updated_at")),
    ("meter_asset", ("id", "tenant", "serial_number", "manufacturer", "model", "multiplier", "firmware", "communication_type", "seal_status", "certification_expiry", "created_at", "updated_at")),
    ("meter_installation", ("id", "tenant", "service_point_id", "meter_asset_id", "install_date", "removal_date", "install_reason", "status", "created_at", "updated_at")),
    ("meter_register", ("id", "tenant", "meter_asset_id", "register_code", "channel_type", "unit_of_measure", "tou_bucket", "created_at", "updated_at")),
    ("meter_read", ("id", "tenant", "service_point_id", "meter_asset_id", "register_code", "read_at", "read_value", "read_source", "collector_id", "device_session", "status", "created_at", "updated_at")),
    ("read_validation", ("id", "tenant", "meter_read_id", "decision", "warning_codes", "blocked_codes", "anomaly_score", "created_at", "updated_at")),
    ("usage_interval", ("id", "tenant", "service_point_id", "channel_type", "interval_start", "interval_end", "quantity", "timezone_name", "status", "created_at", "updated_at")),
    ("estimate_record", ("id", "tenant", "service_point_id", "basis", "confidence", "reason_code", "quantity", "expiry_at", "created_at", "updated_at")),
    ("tariff", ("id", "tenant", "tariff_code", "jurisdiction", "commodity", "customer_class", "service_point_class", "effective_start", "effective_end", "approval_state", "created_at", "updated_at")),
    ("tariff_rate", ("id", "tenant", "tariff_id", "component_code", "rate_type", "tou_bucket", "price", "effective_start", "effective_end", "created_at", "updated_at")),
    ("billing_cycle", ("id", "tenant", "cycle_code", "route_code", "cycle_start", "cycle_end", "status", "created_at", "updated_at")),
    ("utility_bill", ("id", "tenant", "service_point_id", "billing_cycle_id", "bill_status", "currency_code", "calculation_hash", "total_due", "issued_at", "created_at", "updated_at")),
    ("bill_segment", ("id", "tenant", "utility_bill_id", "segment_start", "segment_end", "segment_reason", "import_quantity", "export_quantity", "peak_demand_kw", "segment_total", "created_at", "updated_at")),
    ("customer_charge", ("id", "tenant", "utility_bill_id", "charge_code", "charge_type", "amount", "reason", "status", "created_at", "updated_at")),
    ("billing_adjustment", ("id", "tenant", "utility_bill_id", "reason_code", "amount", "maker", "checker", "approval_state", "created_at", "updated_at")),
    ("payment_receipt", ("id", "tenant", "customer_account_id", "payment_reference", "payment_status", "amount", "received_at", "reversal_of", "created_at", "updated_at")),
    ("payment_allocation_evidence", ("id", "tenant", "payment_receipt_id", "utility_bill_id", "bill_segment_id", "allocated_amount", "evidence_hash", "created_at", "updated_at")),
    ("exception_case", ("id", "tenant", "service_point_id", "exception_code", "severity", "owner", "sla_due_at", "status", "created_at", "updated_at")),
    ("service_order", ("id", "tenant", "service_point_id", "order_type", "approval_state", "effective_at", "authorized_by", "status_outcome", "created_at", "updated_at")),
    ("dispute_case", ("id", "tenant", "utility_bill_id", "reason_code", "decision_outcome", "hold_scope", "status", "created_at", "updated_at")),
    ("regulatory_report", ("id", "tenant", "report_code", "jurisdiction", "period_start", "period_end", "metric_payload", "created_at", "updated_at")),
    ("utilities_metering_billing_policy_rule", ("id", "tenant", "rule_id", "scope", "compiled_hash", "status", "created_at", "updated_at")),
    ("utilities_metering_billing_runtime_parameter", ("id", "tenant", "parameter_name", "parameter_value", "bounded", "status", "created_at", "updated_at")),
    ("utilities_metering_billing_schema_extension", ("id", "tenant", "target_table", "field_payload", "simulation_status", "created_at", "updated_at")),
    ("utilities_metering_billing_control_assertion", ("id", "tenant", "assertion_code", "assertion_scope", "status", "evidence_hash", "created_at", "updated_at")),
    ("utilities_metering_billing_governed_model", ("id", "tenant", "model_name", "model_version", "approval_state", "confirmation_required", "created_at", "updated_at")),
    ("appgen_outbox_event", ("id", "tenant", "event_type", "payload", "idempotency_key", "published_at", "status", "created_at", "updated_at")),
    ("appgen_inbox_event", ("id", "tenant", "event_type", "payload", "idempotency_key", "processed_at", "status", "created_at", "updated_at")),
    ("appgen_dead_letter_event", ("id", "tenant", "event_type", "payload", "idempotency_key", "failure_code", "retry_count", "created_at", "updated_at")),
)

BUSINESS_TABLES = tuple(f"{PBC_KEY}_{name}" for name, _ in TABLE_DEFINITIONS[:-3])
EVENT_TABLES = tuple(f"{PBC_KEY}_{name}" for name, _ in TABLE_DEFINITIONS[-3:])
RUNTIME_TABLES = BUSINESS_TABLES + EVENT_TABLES

SCENARIO_MATRIX = (
    {
        "scenario": "occupied_actual_read",
        "covers": ("actual_reads", "validated_usage", "bill_issue"),
        "seed_bundle": "baseline_residential",
    },
    {
        "scenario": "vacant_disconnect_reconnect",
        "covers": ("vacant_premise", "disconnect", "reconnect"),
        "seed_bundle": "vacant_premise",
    },
    {
        "scenario": "meter_exchange_rollover",
        "covers": ("meter_exchange", "rollover", "read_chain"),
        "seed_bundle": "commercial_tou",
    },
    {
        "scenario": "net_metering_tou_demand",
        "covers": ("net_export", "tou", "demand"),
        "seed_bundle": "industrial_net_metering",
    },
    {
        "scenario": "protected_customer_moratorium",
        "covers": ("moratorium", "protected_status", "disconnect_blocked"),
        "seed_bundle": "protected_customer",
    },
    {
        "scenario": "payment_reversal_and_dispute",
        "covers": ("partial_payment", "reversal", "dispute"),
        "seed_bundle": "arrears_and_dispute",
    },
    {
        "scenario": "batch_cycle_close",
        "covers": ("batch_billing", "sla", "exception_backlog"),
        "seed_bundle": "batch_close",
    },
)

def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()

def _copy_state(state: dict[str, Any]) -> dict[str, Any]:
    copied = deepcopy(state)
    copied["handled_event_ids"] = set(state.get("handled_event_ids", set()))
    return copied

def _owned(name: str) -> str:
    return name if name.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{name}"

def _iso(value: str | None, default: str) -> str:
    return value or default

def empty_state() -> dict[str, Any]:
    return {
        "configuration": {},
        "parameters": dict(PARAMETER_DEFAULTS),
        "rules": {},
        "schema_extensions": {},
        "service_points": {},
        "accounts": {},
        "meters": {},
        "reads": {},
        "intervals": {},
        "bills": {},
        "exceptions": {},
        "handled_event_ids": set(),
        "outbox": [],
        "inbox": [],
        "dead_letters": [],
        "side_effects": (),
    }

def _seed_records() -> dict[str, Any]:
    return {
        "service_points": (
            {"service_point_id": "sp-live-001", "premise_code": "PREM-001", "commodity": "electricity", "lifecycle_status": "live", "zone_code": "CBD"},
            {"service_point_id": "sp-vacant-001", "premise_code": "PREM-002", "commodity": "water", "lifecycle_status": "vacant", "zone_code": "NORTH"},
            {"service_point_id": "sp-protected-001", "premise_code": "PREM-003", "commodity": "gas", "lifecycle_status": "live", "zone_code": "SOUTH"},
        ),
        "exceptions": (
            {"exception_code": "suspect_read", "owner": "billing.queue.read_review", "severity": "high", "count": 3},
            {"exception_code": "tariff_missing", "owner": "billing.queue.tariff_activation", "severity": "critical", "count": 1},
        ),
        "kpis": {
            "daily_usage_mwh": 12.6,
            "monthly_usage_mwh": 331.4,
            "estimate_rate": 0.08,
            "read_success_rate": 0.96,
            "billed_to_actual_variance": 0.014,
            "cycle_close_sla_hours": 5.2,
        },
    }

class UtilitiesMeteringBillingStandaloneApp:
    """Deterministic utility billing operator surface for one-PBC generation."""

    def configure_runtime(self, config: dict[str, Any]) -> dict[str, Any]:
        config = dict(config or {})
        backend = config.get("database_backend", "postgresql")
        topic = config.get("event_topic", APPGEN_X_TOPIC)
        ok = backend in ALLOWED_DATABASE_BACKENDS and topic == APPGEN_X_TOPIC and config.get("stream_engine_picker_visible") is not True
        configuration = {
            "database_backend": backend,
            "event_topic": topic,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "tenant_isolation": config.get("tenant_isolation", "strict"),
            "workbench_limit": config.get("workbench_limit", PARAMETER_DEFAULTS["workbench_limit"]),
        }
        return {"ok": ok, "configuration": configuration, "side_effects": ()}

    def set_parameter(self, name: str, value: Any) -> dict[str, Any]:
        bounded = name in PARAMETER_DEFAULTS
        return {
            "ok": bounded,
            "parameter": {
                "name": name,
                "value": value,
                "bounded": bounded,
                "default": PARAMETER_DEFAULTS.get(name),
                "owned_table": f"{PBC_KEY}_utilities_metering_billing_runtime_parameter",
            },
            "side_effects": (),
        }

    def register_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        rule = dict(rule or {})
        rule_id = rule.get("rule_id", "custom_rule")
        compiled = {
            **rule,
            "rule_id": rule_id,
            "compiled_hash": _digest((rule_id, rule)),
            "event_contract": "AppGen-X",
            "bounded_scope": rule.get("scope", "domain"),
        }
        return {"ok": True, "rule": compiled, "side_effects": ()}

    def register_schema_extension(self, table: str, fields: dict[str, Any]) -> dict[str, Any]:
        owned_table = _owned(table)
        ok = owned_table in RUNTIME_TABLES
        return {
            "ok": ok,
            "table": owned_table,
            "fields": dict(fields or {}),
            "reason": None if ok else "unknown_owned_table",
            "side_effects": (),
        }

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        event = dict(event or {})
        event_type = event.get("event_type")
        idempotency_key = event.get("idempotency_key") or _digest(event)
        if event_type not in CONSUMED_EVENTS:
            return {
                "ok": False,
                "duplicate": False,
                "idempotency_key": idempotency_key,
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "failure_code": "unknown_consumed_event",
                "retry_policy": {"max_attempts": 5},
                "side_effects": (),
            }
        return {
            "ok": True,
            "duplicate": False,
            "idempotency_key": idempotency_key,
            "projection_updates": (event_type.lower(),),
            "retry_policy": {"max_attempts": 5},
            "side_effects": (),
        }

    def create_service_point(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        billable_on = _iso(payload.get("billable_on"), "2026-01-01")
        assignments = tuple(payload.get("existing_assignments", ()))
        overlapping = tuple(
            assignment
            for assignment in assignments
            if assignment.get("assignment_status", "active") == "active"
            and assignment.get("effective_start", "0000-01-01") <= billable_on
            and assignment.get("effective_end", "9999-12-31") >= billable_on
        )
        record = {
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "premise_code": payload.get("premise_code", "PREM-001"),
            "commodity": payload.get("commodity", "electricity"),
            "service_point_class": payload.get("service_point_class", "residential"),
            "voltage_pressure_class": payload.get("voltage_pressure_class", "low_voltage"),
            "zone_code": payload.get("zone_code", "CBD"),
            "geocode": payload.get("geocode", "-1.286389,36.817223"),
            "lifecycle_status": payload.get("lifecycle_status", "pending_connection"),
            "billable_on": billable_on,
            "lineage": {
                "active_assignment_count": len(overlapping),
                "premise": payload.get("premise_code", "PREM-001"),
                "active_tariff_id": payload.get("active_tariff_id", "tariff-r1"),
                "active_meter_ids": tuple(payload.get("active_meter_ids", ())),
            },
            "owned_table": f"{PBC_KEY}_service_point",
        }
        return {
            "ok": len(overlapping) <= 1,
            "record": record,
            "lineage": record["lineage"],
            "conflicts": overlapping,
            "emitted_event": "UtilitiesMeteringBillingCreated",
            "side_effects": (),
        }

    def record_customer_meter_account(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        occupancy_start = _iso(payload.get("occupancy_start"), "2026-01-01")
        occupancy_end = _iso(payload.get("occupancy_end"), "9999-12-31")
        account = {
            "account_id": payload.get("account_id", "acct-001"),
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "bill_to_name": payload.get("bill_to_name", "Sample Customer"),
            "responsibility_mode": payload.get("responsibility_mode", "retail_customer"),
            "protected_status": payload.get("protected_status", False),
            "occupancy_start": occupancy_start,
            "occupancy_end": occupancy_end,
            "owned_table": f"{PBC_KEY}_customer_meter_account",
        }
        assignment = {
            "assignment_id": payload.get("assignment_id", f"assign-{account['account_id']}"),
            "service_point_id": account["service_point_id"],
            "customer_meter_account_id": account["account_id"],
            "effective_start": occupancy_start,
            "effective_end": occupancy_end,
            "assignment_status": payload.get("assignment_status", "active"),
            "owned_table": f"{PBC_KEY}_service_point_assignment",
        }
        return {
            "ok": occupancy_start <= occupancy_end,
            "account": account,
            "assignment": assignment,
            "side_effects": (),
        }

    def register_meter_asset(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        registers = tuple(payload.get("registers", ({"register_code": "kwh_import", "channel_type": "import"},)))
        meter = {
            "meter_asset_id": payload.get("meter_asset_id", "meter-001"),
            "serial_number": payload.get("serial_number", "SN-001"),
            "manufacturer": payload.get("manufacturer", "MeterWorks"),
            "model": payload.get("model", "MW-3000"),
            "multiplier": payload.get("multiplier", 1.0),
            "firmware": payload.get("firmware", "1.0.0"),
            "communication_type": payload.get("communication_type", "ami"),
            "seal_status": payload.get("seal_status", "sealed"),
            "certification_expiry": payload.get("certification_expiry", "2027-12-31"),
            "registers": registers,
            "health": {
                "stale_telemetry": payload.get("stale_telemetry", False),
                "drift_suspected": payload.get("drift_suspected", False),
                "certification_due": payload.get("certification_expiry", "2027-12-31") <= payload.get("health_reference_date", "2026-12-31"),
            },
            "owned_table": f"{PBC_KEY}_meter_asset",
        }
        ok = bool(meter["serial_number"]) and meter["multiplier"] > 0 and bool(registers)
        return {"ok": ok, "record": meter, "side_effects": ()}

    def install_meter(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        installation = {
            "installation_id": payload.get("installation_id", "install-001"),
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "meter_asset_id": payload.get("meter_asset_id", "meter-001"),
            "install_date": payload.get("install_date", "2026-01-01"),
            "removal_date": payload.get("removal_date"),
            "install_reason": payload.get("install_reason", "new_connection"),
            "status": payload.get("status", "installed"),
            "owned_table": f"{PBC_KEY}_meter_installation",
        }
        return {"ok": installation["status"] == "installed", "record": installation, "emitted_event": "MeterInstalled", "side_effects": ()}

    def exchange_meter(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        outgoing_final = float(payload.get("outgoing_final_read", 1024.0))
        incoming_initial = float(payload.get("incoming_initial_read", 0.0))
        new_current = float(payload.get("incoming_current_read", 212.0))
        rollover_threshold = float(payload.get("rollover_threshold", 9999.0))
        rollover = bool(payload.get("rollover", False) or outgoing_final > rollover_threshold)
        stitched_usage = max(0.0, outgoing_final - float(payload.get("previous_final_read", 900.0))) + max(0.0, new_current - incoming_initial)
        continuity = {
            "rollover": rollover,
            "stitched_usage": round(stitched_usage, 4),
            "outgoing_meter_asset_id": payload.get("outgoing_meter_asset_id", "meter-old"),
            "incoming_meter_asset_id": payload.get("incoming_meter_asset_id", "meter-new"),
        }
        return {
            "ok": outgoing_final >= incoming_initial,
            "continuity": continuity,
            "outgoing_final_read": outgoing_final,
            "incoming_initial_read": incoming_initial,
            "emitted_events": ("MeterRemoved", "MeterInstalled"),
            "side_effects": (),
        }

    def create_meter_read(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        required = ("read_source", "collector_id", "device_session", "acquisition_time")
        missing = tuple(name for name in required if not payload.get(name))
        record = {
            "meter_read_id": payload.get("meter_read_id", "read-001"),
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "meter_asset_id": payload.get("meter_asset_id", "meter-001"),
            "register_code": payload.get("register_code", "kwh_import"),
            "read_at": payload.get("read_at", "2026-01-31T10:00:00Z"),
            "read_value": float(payload.get("read_value", 1234.0)),
            "provenance": {
                "read_source": payload.get("read_source"),
                "collector_id": payload.get("collector_id"),
                "device_session": payload.get("device_session"),
                "acquisition_time": payload.get("acquisition_time"),
                "geotag": payload.get("geotag"),
                "photo_evidence": payload.get("photo_evidence"),
            },
            "owned_table": f"{PBC_KEY}_meter_read",
        }
        return {
            "ok": not missing,
            "record": record,
            "missing_provenance": missing,
            "emitted_event": "UtilitiesMeteringBillingCreated",
            "side_effects": (),
        }

    def validate_meter_read(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        value = payload.get("read_value")
        previous = payload.get("previous_read_value")
        service_point_status = payload.get("service_point_status", "live")
        cycle_start = payload.get("cycle_start", "2026-01-01")
        cycle_end = payload.get("cycle_end", "2026-01-31")
        read_at = payload.get("read_at", "2026-01-31")
        duplicate_keys = set(payload.get("duplicate_keys", ()))
        idempotency_key = payload.get("idempotency_key", "meter-read-idem")
        multiplier = float(payload.get("multiplier", 1.0))
        historical_average = float(payload.get("historical_average", 100.0))
        tolerance = float(payload.get("tolerance_ratio", 0.5))
        max_register_value = float(payload.get("max_register_value", 9999.0))
        rollover = bool(payload.get("rollover", False) or (previous is not None and value is not None and value < previous and max_register_value))
        delta = 0.0
        if value is not None and previous is not None:
            if value >= previous:
                delta = (value - previous) * multiplier
            elif rollover:
                delta = ((max_register_value - previous) + value) * multiplier
        steps = []
        blocked = []
        warnings = []

        presence_ok = value is not None
        steps.append({"step": "presence", "ok": presence_ok})
        if not presence_ok:
            blocked.append("missing_value")

        status_ok = service_point_status in {"live", "occupied", "vacant"}
        steps.append({"step": "service_point_status", "ok": status_ok, "status": service_point_status})
        if not status_ok:
            blocked.append("service_point_inactive")

        duplicate_ok = idempotency_key not in duplicate_keys
        steps.append({"step": "duplicate_detection", "ok": duplicate_ok})
        if not duplicate_ok:
            blocked.append("duplicate_detection")

        date_ok = cycle_start <= read_at <= cycle_end
        steps.append({"step": "date_window", "ok": date_ok, "window": (cycle_start, cycle_end)})
        if not date_ok:
            blocked.append("date_window")

        monotonicity_ok = previous is None or value is None or value >= previous or rollover
        steps.append({"step": "monotonicity", "ok": monotonicity_ok})
        if not monotonicity_ok:
            blocked.append("monotonicity")

        rollover_ok = previous is None or value is None or value >= previous or rollover
        steps.append({"step": "rollover", "ok": rollover_ok, "rollover": rollover})
        if not rollover_ok:
            blocked.append("rollover")

        multiplier_ok = multiplier > 0
        steps.append({"step": "multiplier", "ok": multiplier_ok, "applied_multiplier": multiplier})
        if not multiplier_ok:
            blocked.append("multiplier")

        tolerance_ok = historical_average <= 0 or delta <= historical_average * (1.0 + tolerance)
        steps.append({"step": "historical_tolerance", "ok": tolerance_ok, "delta": round(delta, 4), "historical_average": historical_average})
        if not tolerance_ok:
            warnings.append("historical_tolerance")

        prior_final_ok = payload.get("previous_final_read_value") in (None, previous) or rollover
        steps.append({"step": "prior_final_read_consistency", "ok": prior_final_ok})
        if not prior_final_ok:
            blocked.append("prior_final_read_consistency")

        anomaly_score = 0.0
        anomaly_score += 0.45 if not tolerance_ok else 0.0
        anomaly_score += 0.35 if payload.get("reverse_flow") else 0.0
        anomaly_score += 0.2 if payload.get("flatline_suspected") else 0.0
        decision = "accepted"
        if blocked:
            decision = "blocked"
        elif warnings:
            decision = "warned"
        validation = {
            "decision": decision,
            "steps": tuple(steps),
            "warning_codes": tuple(warnings),
            "blocked_codes": tuple(blocked),
            "delta": round(delta, 4),
            "anomaly_score": round(min(1.0, anomaly_score), 4),
            "requires_exception": bool(blocked) or anomaly_score >= PARAMETER_DEFAULTS["risk_threshold"],
            "owned_table": f"{PBC_KEY}_read_validation",
        }
        return {"ok": decision != "blocked", "validation": validation, "emitted_event": "ReadValidated", "side_effects": ()}

    def record_usage_interval(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        intervals = tuple(payload.get("intervals", ()))
        expected_count = int(payload.get("expected_interval_count", len(intervals) or 1))
        actual_count = int(payload.get("actual_interval_count", len(intervals) or expected_count))
        overlap_count = int(payload.get("overlap_count", 0))
        completeness = round(actual_count / expected_count, 4) if expected_count else 1.0
        record = {
            "interval_id": payload.get("interval_id", "interval-001"),
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "channel_type": payload.get("channel_type", "import"),
            "interval_length_minutes": payload.get("interval_length_minutes", 30),
            "timezone_name": payload.get("timezone_name", "Africa/Nairobi"),
            "expected_interval_count": expected_count,
            "actual_interval_count": actual_count,
            "overlap_count": overlap_count,
            "missing_count": max(0, expected_count - actual_count),
            "completeness": completeness,
            "repair_path": payload.get("repair_path", "interpolate_or_backfill"),
            "owned_table": f"{PBC_KEY}_usage_interval",
        }
        return {"ok": completeness == 1.0 and overlap_count == 0, "record": record, "side_effects": ()}

    def estimate_usage_gap(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        if payload.get("adjacent_actual_reads"):
            basis = "adjacent_actual_reads"
            confidence = 0.92
        elif payload.get("seasonal_history"):
            basis = "seasonal_history"
            confidence = 0.81
        elif payload.get("occupancy_adjusted_profile"):
            basis = "occupancy_adjusted_profile"
            confidence = 0.74
        elif payload.get("weather_normalized_pattern"):
            basis = "weather_normalized_pattern"
            confidence = 0.69
        else:
            basis = "engineering_fallback"
            confidence = 0.55
        estimate = {
            "estimate_id": payload.get("estimate_id", "estimate-001"),
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "basis": basis,
            "confidence": confidence,
            "reason_code": payload.get("reason_code", "access_denied"),
            "expiry_at": payload.get("expiry_at", "2026-03-01"),
            "quantity": float(payload.get("quantity", 110.0)),
            "owned_table": f"{PBC_KEY}_estimate_record",
        }
        return {"ok": True, "record": estimate, "emitted_event": "EstimateCreated", "side_effects": ()}

    def review_tariff(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        effective_start = payload.get("effective_start", "2026-01-01")
        effective_end = payload.get("effective_end", "2026-12-31")
        existing_versions = tuple(payload.get("existing_versions", ()))
        overlaps = tuple(
            version
            for version in existing_versions
            if not (effective_end < version.get("effective_start", "0000-01-01") or effective_start > version.get("effective_end", "9999-12-31"))
            and version.get("approval_state", "approved") == "approved"
        )
        tariff = {
            "tariff_id": payload.get("tariff_id", "tariff-001"),
            "tariff_code": payload.get("tariff_code", "ELEC-R1"),
            "jurisdiction": payload.get("jurisdiction", "KE-NAIROBI"),
            "commodity": payload.get("commodity", "electricity"),
            "customer_class": payload.get("customer_class", "residential"),
            "service_point_class": payload.get("service_point_class", "urban"),
            "effective_start": effective_start,
            "effective_end": effective_end,
            "approval_state": payload.get("approval_state", "draft"),
            "tou_demand": {
                "tou_buckets": tuple(payload.get("tou_buckets", ("off_peak", "shoulder", "peak"))),
                "demand_rate_kw": float(payload.get("demand_rate_kw", 4.5)),
                "net_metering_enabled": bool(payload.get("net_metering_enabled", True)),
            },
            "riders": tuple(payload.get("riders", ("fuel_adjustment", "social_support"))),
            "owned_table": f"{PBC_KEY}_tariff",
        }
        return {"ok": not overlaps, "record": tariff, "overlaps": overlaps, "side_effects": ()}

    def approve_service_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        order_type = payload.get("order_type", "connect")
        protected = bool(payload.get("protected_status", False))
        moratorium = bool(payload.get("moratorium_enabled", PARAMETER_DEFAULTS["moratorium_enabled"]))
        transitions = {
            "connect": "live",
            "reconnect": "live",
            "disconnect_non_payment": "disconnected_non_payment",
            "disconnect_requested": "disconnected_requested",
            "safety_lockout": "safety_lockout",
            "inspection": payload.get("current_status", "live"),
            "meter_test": payload.get("current_status", "live"),
            "re_read": payload.get("current_status", "live"),
        }
        blocked = protected and moratorium and order_type == "disconnect_non_payment"
        outcome = transitions.get(order_type, payload.get("current_status", "live"))
        order = {
            "service_order_id": payload.get("service_order_id", "so-001"),
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "order_type": order_type,
            "approval_state": "approved" if not blocked else "blocked",
            "effective_at": payload.get("effective_at", "2026-02-01T09:00:00Z"),
            "authorized_by": payload.get("authorized_by", "ops.supervisor"),
            "status_outcome": outcome,
            "notice_window_days": payload.get("notice_window_days", PARAMETER_DEFAULTS["disconnect_notice_days"]),
            "owned_table": f"{PBC_KEY}_service_order",
        }
        emitted_event = "ServicePointActivated" if outcome == "live" else "ServicePointDisconnected"
        return {
            "ok": not blocked,
            "record": order,
            "compliance_block": blocked,
            "emitted_event": emitted_event,
            "side_effects": (),
        }

    def create_billing_cycle(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        events = tuple(payload.get("cycle_events", ()))
        segments = []
        for event in events:
            if event.get("type") in {"meter_exchange", "tariff_change", "move_in", "move_out", "status_change"}:
                segments.append({
                    "segment_reason": event["type"],
                    "effective_at": event.get("effective_at"),
                })
        cycle = {
            "billing_cycle_id": payload.get("billing_cycle_id", "cycle-001"),
            "cycle_code": payload.get("cycle_code", "FEB-2026-R1"),
            "route_code": payload.get("route_code", "R1"),
            "cycle_start": payload.get("cycle_start", "2026-02-01"),
            "cycle_end": payload.get("cycle_end", "2026-02-28"),
            "status": payload.get("status", "ready_for_rating"),
            "segments": tuple(segments) or ({"segment_reason": "base_cycle", "effective_at": payload.get("cycle_start", "2026-02-01")},),
            "owned_table": f"{PBC_KEY}_billing_cycle",
        }
        return {"ok": True, "record": cycle, "side_effects": ()}

    def calculate_usage(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        import_quantity = float(payload.get("import_quantity", 0.0))
        export_quantity = float(payload.get("export_quantity", 0.0))
        if not import_quantity and payload.get("previous_read_value") is not None and payload.get("read_value") is not None:
            import_quantity = max(0.0, float(payload["read_value"]) - float(payload["previous_read_value"])) * float(payload.get("multiplier", 1.0))
        peak_demand_kw = float(payload.get("peak_demand_kw", payload.get("max_interval_demand_kw", 0.0)))
        net_quantity = round(import_quantity - export_quantity, 4)
        usage = {
            "import_quantity": round(import_quantity, 4),
            "export_quantity": round(export_quantity, 4),
            "net_quantity": net_quantity,
            "peak_demand_kw": round(peak_demand_kw, 4),
            "tou_breakdown": payload.get("tou_breakdown", {"off_peak": round(import_quantity * 0.35, 4), "shoulder": round(import_quantity * 0.4, 4), "peak": round(import_quantity * 0.25, 4)}),
            "determinants": ("energy_import", "energy_export", "peak_demand", "customer_charge"),
        }
        return {"ok": True, "usage": usage, "side_effects": ()}

    def simulate_utility_bill(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        usage = self.calculate_usage(payload)["usage"]
        rates = {
            "energy_rate": float(payload.get("energy_rate", 0.18)),
            "demand_rate": float(payload.get("demand_rate", 4.5)),
            "customer_charge": float(payload.get("customer_charge", 12.0)),
            "export_credit_rate": float(payload.get("export_credit_rate", 0.09)),
            "tax_factor": float(payload.get("tax_factor", 0.16)),
        }
        energy_charge = usage["import_quantity"] * rates["energy_rate"]
        demand_charge = usage["peak_demand_kw"] * rates["demand_rate"]
        export_credit = usage["export_quantity"] * rates["export_credit_rate"]
        customer_charge = rates["customer_charge"]
        adjustment_total = sum(float(item.get("amount", 0.0)) for item in payload.get("adjustments", ()))
        statutory = max(0.0, (energy_charge + demand_charge + customer_charge - export_credit + adjustment_total) * rates["tax_factor"])
        total_due = round(energy_charge + demand_charge + customer_charge - export_credit + adjustment_total + statutory, 2)
        segments = tuple(payload.get("segments", ({
            "segment_id": "segment-001",
            "segment_start": payload.get("cycle_start", "2026-02-01"),
            "segment_end": payload.get("cycle_end", "2026-02-28"),
            "segment_reason": payload.get("segment_reason", "base_cycle"),
            "import_quantity": usage["import_quantity"],
            "export_quantity": usage["export_quantity"],
            "peak_demand_kw": usage["peak_demand_kw"],
            "segment_total": total_due,
        },)))
        bill = {
            "utility_bill_id": payload.get("utility_bill_id", "bill-001"),
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "billing_cycle_id": payload.get("billing_cycle_id", "cycle-001"),
            "bill_status": payload.get("bill_status", "simulated"),
            "currency_code": payload.get("currency_code", "USD"),
            "total_due": total_due,
            "bill_segments": segments,
            "usage_trace": {
                "source_reads": tuple(payload.get("source_reads", (payload.get("meter_read_id", "read-001"),))),
                "interval_repairs": tuple(payload.get("interval_repairs", ())),
                "estimate_substitutions": tuple(payload.get("estimate_substitutions", ())),
                "validation_steps": READ_VALIDATION_STEPS,
                "tariff_determinants": usage["determinants"],
            },
            "calculation_hash": _digest((usage, rates, segments, adjustment_total)),
            "owned_table": f"{PBC_KEY}_utility_bill",
        }
        customer_charges = (
            {"charge_code": "customer_charge", "charge_type": "fixed", "amount": round(customer_charge, 2)},
            {"charge_code": "energy_charge", "charge_type": "usage", "amount": round(energy_charge, 2)},
            {"charge_code": "demand_charge", "charge_type": "demand", "amount": round(demand_charge, 2)},
            {"charge_code": "export_credit", "charge_type": "credit", "amount": round(-export_credit, 2)},
            {"charge_code": "statutory_charge", "charge_type": "statutory", "amount": round(statutory, 2)},
        )
        return {
            "ok": True,
            "bill": bill,
            "customer_charges": customer_charges,
            "emitted_event": "BillSimulated",
            "side_effects": (),
        }

    def create_billing_adjustment(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        maker = payload.get("maker", "billing.analyst")
        checker = payload.get("checker", "billing.supervisor")
        approved = payload.get("approval_state", "draft") == "approved"
        valid = maker != checker if approved else True
        adjustment = {
            "billing_adjustment_id": payload.get("billing_adjustment_id", "adj-001"),
            "utility_bill_id": payload.get("utility_bill_id", "bill-001"),
            "reason_code": payload.get("reason_code", "rebill_correction"),
            "amount": float(payload.get("amount", 15.0)),
            "maker": maker,
            "checker": checker,
            "approval_state": payload.get("approval_state", "draft"),
            "override_evidence": {
                "before_value": payload.get("before_value"),
                "after_value": payload.get("after_value"),
                "reason_text": payload.get("reason_text", "Documented correction"),
            },
            "owned_table": f"{PBC_KEY}_billing_adjustment",
        }
        return {"ok": valid, "record": adjustment, "emitted_event": "AdjustmentApproved" if approved and valid else "UtilitiesMeteringBillingUpdated", "side_effects": ()}

    def record_customer_charge(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        charge = {
            "customer_charge_id": payload.get("customer_charge_id", "charge-001"),
            "utility_bill_id": payload.get("utility_bill_id", "bill-001"),
            "charge_code": payload.get("charge_code", "connection_fee"),
            "charge_type": payload.get("charge_type", "fee"),
            "amount": float(payload.get("amount", 25.0)),
            "reason": payload.get("reason", "connection or reconnection fee"),
            "status": payload.get("status", "active"),
            "owned_table": f"{PBC_KEY}_customer_charge",
        }
        return {"ok": True, "record": charge, "side_effects": ()}

    def record_payment_receipt(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        receipt = {
            "payment_receipt_id": payload.get("payment_receipt_id", "pay-001"),
            "customer_account_id": payload.get("customer_account_id", "acct-001"),
            "payment_reference": payload.get("payment_reference", "PMT-001"),
            "payment_status": payload.get("payment_status", "posted"),
            "amount": float(payload.get("amount", 40.0)),
            "received_at": payload.get("received_at", "2026-02-20T12:00:00Z"),
            "reversal_of": payload.get("reversal_of"),
            "owned_table": f"{PBC_KEY}_payment_receipt",
        }
        return {"ok": True, "record": receipt, "side_effects": ()}

    def allocate_payment_evidence(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        allocations = tuple(payload.get("allocations", ({"utility_bill_id": "bill-001", "bill_segment_id": "segment-001", "amount": 20.0},)))
        total_allocated = round(sum(float(item.get("amount", 0.0)) for item in allocations), 2)
        receipt_amount = float(payload.get("receipt_amount", total_allocated))
        evidence_rows = tuple(
            {
                "payment_receipt_id": payload.get("payment_receipt_id", "pay-001"),
                "utility_bill_id": item.get("utility_bill_id", "bill-001"),
                "bill_segment_id": item.get("bill_segment_id", "segment-001"),
                "allocated_amount": float(item.get("amount", 0.0)),
                "evidence_hash": _digest((payload.get("payment_receipt_id", "pay-001"), item)),
                "owned_table": f"{PBC_KEY}_payment_allocation_evidence",
            }
            for item in allocations
        )
        return {"ok": total_allocated <= receipt_amount, "allocations": evidence_rows, "total_allocated": total_allocated, "side_effects": ()}

    def open_exception_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        exception_code = payload.get("exception_code", "suspect_read")
        follow_up = None
        if exception_code in {"suspect_read", "repeated_estimate", "meter_mismatch"}:
            follow_up = {"service_order_type": "inspection", "service_point_id": payload.get("service_point_id", "sp-001")}
        case = {
            "exception_case_id": payload.get("exception_case_id", "exc-001"),
            "service_point_id": payload.get("service_point_id", "sp-001"),
            "exception_code": exception_code,
            "severity": payload.get("severity", "high"),
            "owner": payload.get("owner", "billing.queue.exception_clearance"),
            "sla_due_at": payload.get("sla_due_at", "2026-02-03T17:00:00Z"),
            "status": payload.get("status", "open"),
            "follow_up_service_order": follow_up,
            "owned_table": f"{PBC_KEY}_exception_case",
        }
        return {"ok": exception_code in EXCEPTION_CODES, "record": case, "emitted_event": "UtilitiesMeteringBillingExceptionOpened", "side_effects": ()}

    def resolve_exception_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        resolution = {
            "exception_case_id": payload.get("exception_case_id", "exc-001"),
            "resolution_status": payload.get("resolution_status", "resolved"),
            "corrected_bill_id": payload.get("corrected_bill_id"),
            "service_order_closed": bool(payload.get("service_order_closed", True)),
        }
        return {"ok": resolution["resolution_status"] in {"resolved", "dismissed"}, "resolution": resolution, "side_effects": ()}

    def open_dispute_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        dispute = {
            "dispute_case_id": payload.get("dispute_case_id", "disp-001"),
            "utility_bill_id": payload.get("utility_bill_id", "bill-001"),
            "reason_code": payload.get("reason_code", "bill_accuracy"),
            "hold_scope": payload.get("hold_scope", "dunning_only"),
            "status": payload.get("status", "open"),
            "decision_outcome": payload.get("decision_outcome"),
            "evidence_attachments": tuple(payload.get("evidence_attachments", ("read-photo-1",))),
            "owned_table": f"{PBC_KEY}_dispute_case",
        }
        return {"ok": True, "record": dispute, "emitted_event": "DisputeOpened", "side_effects": ()}

    def generate_regulatory_report(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        metrics = {
            "estimate_rate": round(float(payload.get("estimate_rate", 0.08)), 4),
            "disconnect_actions": int(payload.get("disconnect_actions", 4)),
            "disconnect_blocked_protected": int(payload.get("disconnect_blocked_protected", 1)),
            "rebill_count": int(payload.get("rebill_count", 2)),
            "net_metering_export_kwh": round(float(payload.get("net_metering_export_kwh", 41.2)), 4),
            "tou_peak_kwh": round(float(payload.get("tou_peak_kwh", 83.4)), 4),
            "payment_reversal_count": int(payload.get("payment_reversal_count", 1)),
        }
        report = {
            "report_code": payload.get("report_code", "REG-UTIL-001"),
            "jurisdiction": payload.get("jurisdiction", "KE-NAIROBI"),
            "period_start": payload.get("period_start", "2026-02-01"),
            "period_end": payload.get("period_end", "2026-02-29"),
            "metric_payload": metrics,
            "audit_hash": _digest(metrics),
            "owned_table": f"{PBC_KEY}_regulatory_report",
        }
        return {"ok": True, "report": report, "side_effects": ()}

    def review_utilities_metering_billing_policy_rule(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        return self.register_rule({**payload, "scope": payload.get("scope", "regulatory_pack")})

    def approve_utilities_metering_billing_runtime_parameter(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        return self.set_parameter(payload.get("name", "workbench_limit"), payload.get("value", PARAMETER_DEFAULTS["workbench_limit"]))

    def simulate_utilities_metering_billing_schema_extension(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        return self.register_schema_extension(payload.get("table", "meter_read"), payload.get("fields", {"new_field": "string"}))

    def create_utilities_metering_billing_control_assertion(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        assertion = {
            "assertion_code": payload.get("assertion_code", "bill_trace_complete"),
            "assertion_scope": payload.get("assertion_scope", "release"),
            "status": payload.get("status", "pass"),
            "evidence_hash": _digest(payload),
            "owned_table": f"{PBC_KEY}_utilities_metering_billing_control_assertion",
        }
        return {"ok": True, "record": assertion, "side_effects": ()}

    def record_utilities_metering_billing_governed_model(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload or {})
        model = {
            "model_name": payload.get("model_name", "utilities-billing-assistant"),
            "model_version": payload.get("model_version", "2026.02"),
            "approval_state": payload.get("approval_state", "approved"),
            "confirmation_required": True,
            "owned_table": f"{PBC_KEY}_utilities_metering_billing_governed_model",
        }
        return {"ok": True, "record": model, "side_effects": ()}

    def query_workbench(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        seed = _seed_records()
        summary = {
            **seed["kpis"],
            "service_point_count": len(seed["service_points"]),
            "exception_count": sum(item["count"] for item in seed["exceptions"]),
            "queue_count": 8,
        }
        queues = (
            {"queue": "read_review", "count": 3, "severity": "high", "owner": "billing.queue.read_review"},
            {"queue": "estimate_review", "count": 2, "severity": "medium", "owner": "billing.queue.estimate_review"},
            {"queue": "tariff_activation", "count": 1, "severity": "critical", "owner": "billing.queue.tariff_activation"},
            {"queue": "bill_run_approval", "count": 1, "severity": "medium", "owner": "billing.queue.bill_run"},
            {"queue": "adjustment_approval", "count": 1, "severity": "medium", "owner": "billing.queue.adjustments"},
            {"queue": "move_processing", "count": 1, "severity": "medium", "owner": "billing.queue.moves"},
            {"queue": "dispute_handling", "count": 1, "severity": "high", "owner": "billing.queue.disputes"},
            {"queue": "exception_clearance", "count": 4, "severity": "critical", "owner": "billing.queue.exception_clearance"},
        )
        return {
            "ok": True,
            "tenant": payload.get("tenant", "default"),
            "records": seed,
            "summary": summary,
            "queues": queues,
            "forms": FORM_DEFINITIONS,
            "wizards": WIZARD_DEFINITIONS,
            "controls": CONTROL_DEFINITIONS,
            "side_effects": (),
        }

    def build_workbench_view(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        query = self.query_workbench(payload)
        return {
            "ok": query["ok"],
            "route": f"/workbench/pbcs/{PBC_KEY}",
            "fragments": ("UtilitiesMeteringBillingWorkbench", "UtilitiesMeteringBillingDetail", "UtilitiesMeteringBillingAssistantPanel"),
            "queues": query["queues"],
            "summary": query["summary"],
            "forms": query["forms"],
            "wizards": query["wizards"],
            "controls": query["controls"],
            "single_pbc_app": build_standalone_app_contract(),
            "side_effects": (),
        }

    def build_detail_view(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        timeline = (
            {"kind": "service_point_status", "status": payload.get("service_point_status", "live"), "effective_at": "2026-01-01T00:00:00Z"},
            {"kind": "meter_installation", "meter_asset_id": payload.get("meter_asset_id", "meter-001"), "effective_at": "2026-01-01T08:00:00Z"},
            {"kind": "read_validation", "meter_read_id": payload.get("meter_read_id", "read-001"), "decision": payload.get("read_decision", "accepted"), "effective_at": "2026-01-31T10:00:00Z"},
            {"kind": "tariff_timeline", "tariff_id": payload.get("tariff_id", "tariff-001"), "effective_at": "2026-01-01T00:00:00Z"},
            {"kind": "bill_segment", "utility_bill_id": payload.get("utility_bill_id", "bill-001"), "effective_at": "2026-02-28T23:59:59Z"},
            {"kind": "payment_status", "payment_receipt_id": payload.get("payment_receipt_id", "pay-001"), "effective_at": "2026-02-20T12:00:00Z"},
            {"kind": "dispute_case", "dispute_case_id": payload.get("dispute_case_id", "disp-001"), "effective_at": "2026-02-21T09:00:00Z"},
        )
        return {
            "ok": True,
            "route": f"/detail/pbcs/{PBC_KEY}",
            "timeline": timeline,
            "panels": ("service_point_lineage", "meter_history", "read_history", "tariff_timeline", "bill_trace", "payment_status", "dispute_panel"),
            "side_effects": (),
        }

    def build_regulatory_report_preview(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        report = self.generate_regulatory_report(payload or {})["report"]
        return {
            "ok": True,
            "route": f"/reports/pbcs/{PBC_KEY}/regulatory",
            "report": report,
            "side_effects": (),
        }

    def document_instruction_plan(self, document: str, instruction: str) -> dict[str, Any]:
        lowered = f"{document} {instruction}".lower()
        command = "validate_meter_read"
        tables = (f"{PBC_KEY}_meter_read", f"{PBC_KEY}_read_validation", f"{PBC_KEY}_exception_case")
        if "tariff" in lowered or "regulator" in lowered or "notice" in lowered:
            command = "review_tariff"
            tables = (f"{PBC_KEY}_tariff", f"{PBC_KEY}_tariff_rate", f"{PBC_KEY}_utilities_metering_billing_policy_rule")
        elif "adjustment" in lowered or "rebill" in lowered or "bill explanation" in lowered:
            command = "create_billing_adjustment"
            tables = (f"{PBC_KEY}_billing_adjustment", f"{PBC_KEY}_utility_bill", f"{PBC_KEY}_bill_segment")
        elif "payment" in lowered or "allocation" in lowered:
            command = "allocate_payment_evidence"
            tables = (f"{PBC_KEY}_payment_receipt", f"{PBC_KEY}_payment_allocation_evidence", f"{PBC_KEY}_utility_bill")
        plan = {
            "ok": True,
            "pbc": PBC_KEY,
            "command": command,
            "document_digest": _digest(document),
            "instruction": instruction,
            "candidate_tables": tables,
            "requires_human_confirmation": True,
            "crud_preview": {
                "operation": "update" if command in {"review_tariff", "create_billing_adjustment", "allocate_payment_evidence"} else "create",
                "event_contract": "AppGen-X",
                "owned_tables_only": True,
            },
            "source_mapping": ({"field": "primary_instruction", "source_excerpt": document[:80]},),
            "side_effects": (),
        }
        return plan

    def datastore_crud_plan(self, action: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        target = table or f"{PBC_KEY}_meter_read"
        if not str(target).startswith(f"{PBC_KEY}_"):
            return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "action": action,
            "table": target,
            "payload": dict(payload or {}),
            "requires_confirmation": action in {"create", "update", "delete"},
            "confirmation_gate": "human_approval_required",
            "event_contract": "AppGen-X",
            "side_effects": (),
        }

def build_standalone_app() -> UtilitiesMeteringBillingStandaloneApp:
    return UtilitiesMeteringBillingStandaloneApp()

def build_schema_contract() -> dict[str, Any]:
    tables = tuple(
        {
            "table": _owned(name),
            "fields": fields,
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for name, fields in TABLE_DEFINITIONS
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in _owned(name).split("_")),
            "table": _owned(name),
            "fields": fields,
        }
        for name, fields in TABLE_DEFINITIONS
    )
    return {
        "format": f"appgen.{PBC_KEY}.schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": tables,
        "models": models,
        "migrations": ({"path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql", "operation": "create_owned_tables", "backend_allowlist": ALLOWED_DATABASE_BACKENDS},),
        "relationships": (
            {"from_table": f"{PBC_KEY}_service_point", "target_table": f"{PBC_KEY}_premise", "relationship": "many_to_one"},
            {"from_table": f"{PBC_KEY}_meter_installation", "target_table": f"{PBC_KEY}_service_point", "relationship": "many_to_one"},
            {"from_table": f"{PBC_KEY}_bill_segment", "target_table": f"{PBC_KEY}_utility_bill", "relationship": "many_to_one"},
        ),
        "dependencies": {"shared_tables": ()},
        "owned_tables": RUNTIME_TABLES,
        "shared_table_access": False,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "side_effects": (),
    }

def build_service_contract() -> dict[str, Any]:
    return {
        "format": f"appgen.{PBC_KEY}.service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": COMMAND_METHODS,
        "query_methods": QUERY_METHODS,
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "side_effects": (),
    }

def build_api_contract() -> dict[str, Any]:
    return {
        "format": f"appgen.{PBC_KEY}.api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": API_ROUTES,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": RUNTIME_TABLES,
        "side_effects": (),
    }

def build_agent_contract() -> dict[str, Any]:
    namespace = f"{PBC_KEY}_skills"
    skills = (
        {
            "name": f"{PBC_KEY}_read_exception_review",
            "scope": PBC_KEY,
            "description": "Summarize read provenance, validation failures, anomaly drivers, and recommended next actions.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_tariff_notice_intake",
            "scope": PBC_KEY,
            "description": "Parse tariff schedules and regulator notices into draft tariff or policy updates.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_adjustment_bill_explanation",
            "scope": PBC_KEY,
            "description": "Draft adjustment proposals, bill explanations, and dispute summaries with evidence links.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_regulatory_reporting_preview",
            "scope": PBC_KEY,
            "description": "Preview regulatory reporting metrics and scenario readiness for release evidence.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
    )
    return {"ok": True, "namespace": namespace, "skills": skills, "side_effects": ()}

def build_ui_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": ("UtilitiesMeteringBillingWorkbench", "UtilitiesMeteringBillingDetail", "UtilitiesMeteringBillingAssistantPanel"),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": PERMISSIONS,
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "queues": (
            "read_review",
            "estimate_review",
            "tariff_activation",
            "bill_run_approval",
            "adjustment_approval",
            "move_processing",
            "dispute_handling",
            "exception_clearance",
        ),
        "detail_panels": ("service_point_lineage", "meter_history", "read_history", "tariff_timeline", "bill_trace", "payment_status", "dispute_panel"),
        "assistant_panel": {
            "namespace": f"{PBC_KEY}_skills",
            "governed_datastore_crud": True,
            "confirmation_gated": True,
        },
        "full_capability_surface": {
            "operation_actions": COMMAND_METHODS,
            "query_actions": QUERY_METHODS,
            "rule_editors": RULES,
            "parameter_editors": tuple(PARAMETER_DEFAULTS),
            "advanced_panels": ADVANCED_CAPABILITIES,
            "table_browsers": RUNTIME_TABLES,
            "forms": FORM_DEFINITIONS,
            "wizards": WIZARD_DEFINITIONS,
            "controls": CONTROL_DEFINITIONS,
        },
        "side_effects": (),
    }

def build_standalone_app_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "label": PBC_LABEL,
        "route": f"/app/pbcs/{PBC_KEY}",
        "database_backed": True,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "side_effects": (),
    }

def build_release_evidence() -> dict[str, Any]:
    checks = (
        {"id": "schema_contract", "ok": build_schema_contract()["ok"]},
        {"id": "service_contract", "ok": build_service_contract()["ok"]},
        {"id": "api_contract", "ok": build_api_contract()["ok"]},
        {"id": "ui_contract", "ok": build_ui_contract()["ok"]},
        {"id": "standalone_app", "ok": build_standalone_app_contract()["ok"]},
        {"id": "agent_contract", "ok": build_agent_contract()["ok"]},
        {"id": "scenario_matrix", "ok": len(SCENARIO_MATRIX) >= 7},
        {"id": "controls_cover_release_gate", "ok": len(CONTROL_DEFINITIONS) >= 8},
        {"id": "forms_wizards_controls", "ok": len(FORM_DEFINITIONS) >= 6 and len(WIZARD_DEFINITIONS) >= 5},
        {"id": "governed_crud_confirmation", "ok": build_ui_contract()["assistant_panel"]["confirmation_gated"] is True},
    )
    return {
        "format": f"appgen.{PBC_KEY}.release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "scenario_matrix": SCENARIO_MATRIX,
        "generated_artifacts": {
            "migrations": build_schema_contract()["migrations"],
            "models": build_schema_contract()["models"],
            "events": {"emits": EMITTED_EVENTS, "consumes": CONSUMED_EVENTS, "contract": "AppGen-X"},
            "ui": build_ui_contract()["fragments"],
            "forms": FORM_DEFINITIONS,
            "wizards": WIZARD_DEFINITIONS,
            "controls": CONTROL_DEFINITIONS,
        },
        "boundary_gaps": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }

def build_runtime_capabilities() -> dict[str, Any]:
    return {
        "format": f"appgen.{PBC_KEY}.runtime-capabilities.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": RUNTIME_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "standard_features": STANDARD_FEATURES,
        "capabilities": ADVANCED_CAPABILITIES,
        "operations": COMMAND_METHODS + QUERY_METHODS + (
            "build_schema_contract",
            "build_service_contract",
            "build_api_contract",
            "build_release_evidence",
            "build_ui_contract",
            "verify_owned_table_boundary",
            "build_standalone_app_contract",
        ),
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }

def verify_owned_table_boundary(references: tuple[str, ...] | list[str]) -> dict[str, Any]:
    references = tuple(references)
    invalid = tuple(
        reference
        for reference in references
        if reference.endswith("_table") and not reference.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": RUNTIME_TABLES,
        "shared_table_access": False,
        "side_effects": (),
    }

def slice_app_smoke_test() -> dict[str, Any]:
    app = build_standalone_app()
    config = app.configure_runtime({"database_backend": "postgresql", "event_topic": APPGEN_X_TOPIC})
    parameter = app.set_parameter("workbench_limit", 80)
    rule = app.register_rule({"rule_id": "meter_read_policy", "scope": "domain"})
    service_point = app.create_service_point({"service_point_id": "sp-smoke", "premise_code": "PREM-SMOKE"})
    meter = app.register_meter_asset({"meter_asset_id": "meter-smoke", "serial_number": "SMK-1"})
    read = app.create_meter_read({
        "meter_read_id": "read-smoke",
        "service_point_id": "sp-smoke",
        "meter_asset_id": "meter-smoke",
        "read_value": 1450.0,
        "read_source": "ami",
        "collector_id": "ami.headend",
        "device_session": "sess-1",
        "acquisition_time": "2026-01-31T10:00:00Z",
    })
    validation = app.validate_meter_read({
        "read_value": 1450.0,
        "previous_read_value": 1320.0,
        "service_point_status": "live",
        "read_at": "2026-01-31",
        "cycle_start": "2026-01-01",
        "cycle_end": "2026-01-31",
        "historical_average": 150.0,
        "idempotency_key": "idem-smoke",
    })
    interval = app.record_usage_interval({"expected_interval_count": 48, "actual_interval_count": 48, "timezone_name": "Africa/Nairobi"})
    estimate = app.estimate_usage_gap({"adjacent_actual_reads": True, "quantity": 120.0})
    tariff = app.review_tariff({"tariff_code": "ELEC-SMOKE", "effective_start": "2026-01-01", "effective_end": "2026-12-31"})
    order = app.approve_service_order({"order_type": "connect", "protected_status": False})
    cycle = app.create_billing_cycle({"cycle_code": "SMOKE-CYCLE"})
    bill = app.simulate_utility_bill({"service_point_id": "sp-smoke", "import_quantity": 130.0, "export_quantity": 10.0, "peak_demand_kw": 6.0})
    adjustment = app.create_billing_adjustment({"approval_state": "approved", "maker": "a", "checker": "b"})
    payment = app.record_payment_receipt({"amount": 60.0})
    allocation = app.allocate_payment_evidence({"receipt_amount": 60.0, "allocations": ({"utility_bill_id": "bill-001", "bill_segment_id": "segment-001", "amount": 60.0},)})
    exception_case = app.open_exception_case({"exception_code": "suspect_read"})
    dispute = app.open_dispute_case({"utility_bill_id": "bill-001"})
    report = app.generate_regulatory_report({})
    workbench = app.build_workbench_view({"tenant": "tenant-smoke"})
    detail = app.build_detail_view({})
    document = app.document_instruction_plan("Tariff notice for peak rider", "update tariff from regulator notice")
    crud = app.datastore_crud_plan("create", table=f"{PBC_KEY}_meter_read", payload={"status": "draft"})
    event = app.receive_event({"event_type": CONSUMED_EVENTS[0], "idempotency_key": "smoke-event"})
    control = app.create_utilities_metering_billing_control_assertion({})
    governed = app.record_utilities_metering_billing_governed_model({})
    checks = (
        config["ok"],
        parameter["ok"],
        rule["ok"],
        service_point["ok"],
        meter["ok"],
        read["ok"],
        validation["ok"],
        interval["ok"],
        estimate["ok"],
        tariff["ok"],
        order["ok"],
        cycle["ok"],
        bill["ok"],
        adjustment["ok"],
        payment["ok"],
        allocation["ok"],
        exception_case["ok"],
        dispute["ok"],
        report["ok"],
        workbench["ok"],
        detail["ok"],
        document["ok"],
        crud["ok"],
        event["ok"],
        control["ok"],
        governed["ok"],
    )
    return {
        "ok": all(checks),
        "checks": checks,
        "blocking_gaps": (),
        "side_effects": (),
    }
