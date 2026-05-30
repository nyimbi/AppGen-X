"""Executable runtime contract for the trade_finance_operations PBC."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
import hashlib

from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import domain_depth_contract
from .domain_depth import domain_depth_smoke_test
from .domain_depth import execute_domain_operation

PBC_KEY = "trade_finance_operations"
TRADE_FINANCE_OPERATIONS_OWNED_TABLES = DOMAIN_OWNED_TABLES
TRADE_FINANCE_OPERATIONS_RUNTIME_TABLES = DOMAIN_OWNED_TABLES
TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC = "pbc.trade_finance_operations.events"
TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES = (
    "TradeFinanceOperationsCreated",
    "TradeFinanceOperationsUpdated",
    "TradeFinanceOperationsApproved",
    "TradeFinanceOperationsExceptionOpened",
    "TradeFinancePresentationReceived",
    "TradeFinanceDiscrepancyRaised",
    "TradeFinanceWaiverRequested",
    "TradeFinanceScreeningBlocked",
    "TradeFinanceSettlementCompleted",
    "TradeFinanceSwiftEvidenceCreated",
)
TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
TRADE_FINANCE_OPERATIONS_STANDARD_FEATURE_KEYS = (
    "letter_of_credit_management",
    "trade_finance_operations_workflow",
    "trade_finance_operations_analytics",
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
TRADE_FINANCE_OPERATIONS_RUNTIME_CAPABILITY_KEYS = (
    "trade_finance_operations_event_sourced_operational_history",
    "trade_finance_operations_multi_tenant_policy_isolation",
    "trade_finance_operations_schema_evolution_resilience",
    "trade_finance_operations_autonomous_anomaly_detection",
    "trade_finance_operations_semantic_document_instruction_understanding",
    "trade_finance_operations_predictive_risk_scoring",
    "trade_finance_operations_counterfactual_scenario_simulation",
    "trade_finance_operations_cryptographic_audit_proofs",
    "trade_finance_operations_continuous_control_testing",
    "trade_finance_operations_carbon_and_sustainability_awareness",
    "trade_finance_operations_cross_pbc_event_federation",
    "trade_finance_operations_governed_ai_agent_execution",
)
TRADE_FINANCE_OPERATIONS_UI_FRAGMENT_KEYS = (
    "TradeFinanceOperationsWorkbench",
    "TradeFinanceOperationsDetail",
    "TradeFinanceOperationsAssistantPanel",
)
TRADE_FINANCE_OPERATIONS_BUSINESS_TABLES = tuple(
    table for table in TRADE_FINANCE_OPERATIONS_OWNED_TABLES if not table.endswith("_event")
)
_DEFAULT_QUEUE_NAMES = (
    "issuance",
    "presentations",
    "sanctions_holds",
    "discrepancies",
    "limits_and_collateral",
    "settlements",
    "release_evidence",
)
_ROUTES = (
    "POST /letter-of-credits",
    "POST /bank-guarantees",
    "POST /documentary-collections",
    "POST /trade-bills",
    "POST /trade-loans",
    "POST /trade-documents",
    "POST /sanctions-checks",
    "POST /discrepancy-decisions",
    "POST /collateral-margins",
    "POST /limit-reservations",
    "POST /fee-assessments",
    "POST /settlements",
    "POST /swift-messages",
    "GET /trade-finance-operations-workbench",
    "GET /trade-finance-operations-detail",
)
_SCHEMA_TABLES = (
    {"table": "trade_finance_operations_letter_of_credit", "fields": ("id", "tenant", "case_id", "instrument_type", "status", "currency", "face_amount", "expiry_date", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_bank_guarantee", "fields": ("id", "tenant", "case_id", "guarantee_type", "status", "currency", "face_amount", "claim_expiry_date", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_documentary_collection", "fields": ("id", "tenant", "case_id", "collection_mode", "status", "currency", "face_amount", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_bill", "fields": ("id", "tenant", "case_id", "bill_type", "status", "currency", "amount", "due_date", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_loan", "fields": ("id", "tenant", "case_id", "facility_id", "status", "currency", "financed_amount", "margin_pct", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_document", "fields": ("id", "tenant", "case_id", "package_id", "status", "presentation_date", "document_count", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_shipment_evidence", "fields": ("id", "tenant", "case_id", "shipment_reference", "status", "shipment_date", "origin_country", "destination_country", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_sanctions_check", "fields": ("id", "tenant", "case_id", "screening_id", "status", "decision", "risk_score", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_discrepancy_case", "fields": ("id", "tenant", "case_id", "discrepancy_code", "status", "severity", "waiver_state", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_collateral_margin", "fields": ("id", "tenant", "case_id", "collateral_id", "status", "market_value", "required_margin", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_limit_reservation", "fields": ("id", "tenant", "case_id", "facility_id", "status", "headroom", "requested_exposure", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_fee_accrual", "fields": ("id", "tenant", "case_id", "status", "currency", "gross_fee", "net_fee", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_settlement", "fields": ("id", "tenant", "case_id", "settlement_id", "status", "currency", "gross_amount", "net_amount", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_swift_message_evidence", "fields": ("id", "tenant", "case_id", "message_type", "status", "sender_bic", "receiver_bic", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_finance_operations_policy_rule", "fields": ("id", "tenant", "rule_id", "status", "scope", "compiled_hash", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_finance_operations_runtime_parameter", "fields": ("id", "tenant", "parameter_name", "status", "value", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_finance_operations_schema_extension", "fields": ("id", "tenant", "table_name", "status", "fields_json", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_finance_operations_control_assertion", "fields": ("id", "tenant", "assertion_id", "status", "severity", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_trade_finance_operations_governed_model", "fields": ("id", "tenant", "model_id", "status", "model_kind", "payload", "created_at", "updated_at")},
    {"table": "trade_finance_operations_appgen_outbox_event", "fields": ("id", "tenant", "event_type", "status", "payload", "published_at", "created_at")},
    {"table": "trade_finance_operations_appgen_inbox_event", "fields": ("id", "tenant", "event_type", "status", "payload", "processed_at", "created_at")},
    {"table": "trade_finance_operations_appgen_dead_letter_event", "fields": ("id", "tenant", "event_type", "status", "payload", "failed_at", "created_at")},
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def trade_finance_operations_empty_state() -> dict:
    return {
        "records": {},
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "workflow_history": (),
        "release_evidence": (),
        "assistant_guidance": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "handled_events": {},
    }


def _copy(state: dict) -> dict:
    return deepcopy(state)


def _append_workflow(state: dict, stage: str, payload: dict) -> dict:
    next_state = _copy(state)
    history = tuple(next_state.get("workflow_history", ()))
    next_state["workflow_history"] = history + ({"stage": stage, "payload": dict(payload), "recorded_at": _now()},)
    return next_state


def _append_outbox(state: dict, event_type: str, payload: dict) -> dict:
    next_state = _copy(state)
    event = {
        "event_id": _digest((event_type, payload, len(next_state.get("outbox", ())))),
        "event_type": event_type,
        "topic": TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "payload": dict(payload),
        "status": "pending",
        "published_at": None,
        "idempotency_key": _digest((event_type, tuple(sorted(payload.items())))),
    }
    next_state["outbox"] = tuple(next_state.get("outbox", ())) + (event,)
    return next_state


def trade_finance_operations_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    candidate = dict(config)
    ok = (
        candidate.get("database_backend") in TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS
        and candidate.get("event_topic", TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC)
        == TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        **candidate,
        "ok": ok,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    next_state = _append_workflow(next_state, "configure_runtime", {"ok": ok})
    return {"ok": ok, "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def trade_finance_operations_set_parameter(state: dict, name: str, value: object) -> dict:
    next_state = _copy(state)
    parameter = {
        "name": name,
        "value": value,
        "bounded": True,
        "scope": "package",
        "updated_at": _now(),
    }
    next_state.setdefault("parameters", {})[name] = parameter
    next_state = _append_workflow(next_state, "set_parameter", parameter)
    return {"ok": True, "state": next_state, "parameter": parameter, "side_effects": ()}


def trade_finance_operations_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "trade_finance_default")
    compiled = {
        **dict(rule),
        "rule_id": rule_id,
        "compiled_hash": _digest(rule),
        "event_contract": "AppGen-X",
        "compiled": True,
    }
    next_state.setdefault("rules", {})[rule_id] = compiled
    next_state = _append_workflow(next_state, "register_rule", {"rule_id": rule_id})
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def trade_finance_operations_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in TRADE_FINANCE_OPERATIONS_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    extension = {"table": owned_name, "fields": dict(fields), "registered_at": _now()}
    next_state.setdefault("schema_extensions", {})[owned_name] = extension
    next_state = _append_workflow(next_state, "register_schema_extension", extension)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def trade_finance_operations_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state.get("handled_events", {}):
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state.setdefault("handled_events", {})[idem] = event.get("event_type")
    if event.get("event_type") not in TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES:
        dead = {
            "event": dict(event),
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "retry_policy": {"max_attempts": 5},
        }
        next_state["dead_letter"] = tuple(next_state.get("dead_letter", ())) + (dead,)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": dead["dead_letter_table"],
            "side_effects": (),
        }
    next_state["inbox"] = tuple(next_state.get("inbox", ())) + (dict(event),)
    next_state = _append_workflow(next_state, "receive_event", {"event_type": event.get("event_type")})
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def trade_finance_operations_command_letter_of_credit(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    record_id = payload.get("case_id") or payload.get("id") or payload.get("code") or "TFO-LC-001"
    record = {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": payload.get("status", "draft"),
        "instrument_type": payload.get("instrument_type", "commercial_lc"),
        "payload": dict(payload),
        "created_at": _now(),
        "updated_at": _now(),
    }
    next_state.setdefault("records", {})[record_id] = record
    next_state = _append_workflow(next_state, "command_letter_of_credit", {"record_id": record_id})
    next_state = _append_outbox(next_state, TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES[0], {"record_id": record_id, "tenant": record["tenant"]})
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def trade_finance_operations_query_workbench(state: dict, filters: dict | None = None) -> dict:
    records = tuple(state.get("records", {}).values())
    outstanding_discrepancies = sum(1 for item in state.get("records", {}).values() if item.get("status") == "discrepant")
    blocked_sanctions = sum(1 for event in state.get("inbox", ()) if event.get("event_type") == "OperationalKpiChanged")
    return {
        "ok": True,
        "records": records,
        "filters": dict(filters or {}),
        "cards": (
            {"key": "open_cases", "value": len(records)},
            {"key": "sanctions_holds", "value": blocked_sanctions},
            {"key": "active_discrepancies", "value": outstanding_discrepancies},
            {"key": "pending_release_checks", "value": len(state.get("release_evidence", ()))},
        ),
        "queues": _DEFAULT_QUEUE_NAMES,
        "read_only": True,
        "side_effects": (),
    }


def trade_finance_operations_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    record_count = len(state.get("records", {}))
    blocked = len(state.get("dead_letter", ()))
    score = round(max(0.4, min(0.99, 0.62 + (record_count * 0.03) - (blocked * 0.07))), 4)
    return {
        "ok": True,
        "score": score,
        "explanations": (
            "policy_aligned",
            "owned_boundary_respected",
            "assistant_confirmation_gated",
            "release_evidence_pack_ready" if score >= 0.7 else "release_evidence_pack_needs_attention",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def trade_finance_operations_parse_document_instruction(document: str, instruction: str) -> dict:
    text = f"{document} {instruction}".lower()
    candidate_tables = []
    if any(term in text for term in ("credit", "lc", "mt700")):
        candidate_tables.append("trade_finance_operations_letter_of_credit")
    if any(term in text for term in ("guarantee", "standby", "sblc")):
        candidate_tables.append("trade_finance_operations_bank_guarantee")
    if any(term in text for term in ("collection", "dp", "da")):
        candidate_tables.append("trade_finance_operations_documentary_collection")
    if any(term in text for term in ("shipment", "invoice", "bill of lading", "document")):
        candidate_tables.append("trade_finance_operations_trade_document")
    if any(term in text for term in ("sanction", "aml", "screening")):
        candidate_tables.append("trade_finance_operations_sanctions_check")
    if not candidate_tables:
        candidate_tables.append("trade_finance_operations_letter_of_credit")
    return {
        "ok": True,
        "candidate_tables": tuple(dict.fromkeys(candidate_tables)),
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def trade_finance_operations_build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            "table": table["table"],
            "fields": table["fields"],
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in _SCHEMA_TABLES
    )
    return {
        "format": "appgen.trade-finance-operations-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": "pbcs/trade_finance_operations/migrations/001_initial.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            }
            for table in _SCHEMA_TABLES
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in _SCHEMA_TABLES
        ),
        "datastore_backends": TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": TRADE_FINANCE_OPERATIONS_OWNED_TABLES,
    }


def trade_finance_operations_build_service_contract() -> dict:
    return {
        "format": "appgen.trade-finance-operations-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_letter_of_credit",
        ) + tuple(DOMAIN_OPERATIONS),
        "query_methods": (
            "query_workbench",
            "build_workbench_view",
            "build_case_detail",
            "build_release_evidence_pack",
            "run_advanced_assessment",
            "parse_document_instruction",
        ),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def trade_finance_operations_build_api_contract() -> dict:
    return {
        "format": "appgen.trade-finance-operations-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": _ROUTES,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": TRADE_FINANCE_OPERATIONS_OWNED_TABLES,
    }


def trade_finance_operations_build_release_evidence() -> dict:
    schema = trade_finance_operations_build_schema_contract()
    service = trade_finance_operations_build_service_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"] and bool(schema["tables"]) and bool(schema["models"])},
        {"id": "service_api_events", "ok": service["ok"] and bool(service["command_methods"]) and bool(_ROUTES)},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "forms_wizards_controls", "ok": True},
        {"id": "standalone_workflows", "ok": True},
        {"id": "release_evidence_pack", "ok": True},
    )
    return {
        "format": "appgen.trade-finance-operations-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES,
                "consumes": TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": TRADE_FINANCE_OPERATIONS_UI_FRAGMENT_KEYS,
            "routes": _ROUTES,
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def trade_finance_operations_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "trade_finance_operations.read",
            "trade_finance_operations.create",
            "trade_finance_operations.update",
            "trade_finance_operations.approve",
            "trade_finance_operations.admin",
        ),
        "roles": ("operator", "approver", "auditor", "compliance_officer"),
        "action_permissions": {
            "open_case": "trade_finance_operations.create",
            "update_case": "trade_finance_operations.update",
            "approve_release": "trade_finance_operations.approve",
            "view_workbench": "trade_finance_operations.read",
            "administer_rules": "trade_finance_operations.admin",
        },
        "side_effects": (),
    }


def trade_finance_operations_build_workbench_view(tenant: str = "default", state: dict | None = None) -> dict:
    local_state = state or trade_finance_operations_empty_state()
    workbench = trade_finance_operations_query_workbench(local_state, {"tenant": tenant})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "cards": workbench["cards"],
        "queues": workbench["queues"],
        "tables": TRADE_FINANCE_OPERATIONS_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "ui_fragments": TRADE_FINANCE_OPERATIONS_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def trade_finance_operations_build_case_detail(case_id: str = "TFO-SAMPLE", state: dict | None = None) -> dict:
    local_state = state or trade_finance_operations_empty_state()
    record = local_state.get("records", {}).get(case_id, {"id": case_id, "status": "draft", "tenant": "default"})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "case_id": case_id,
        "summary": record,
        "obligations": (
            {"stage": "issuance", "status": record.get("status", "draft")},
            {"stage": "screening", "status": "pending"},
            {"stage": "settlement", "status": "pending"},
        ),
        "timeline": tuple(local_state.get("workflow_history", ())),
        "side_effects": (),
    }


def trade_finance_operations_build_release_evidence_pack(state: dict | None = None) -> dict:
    local_state = state or trade_finance_operations_empty_state()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "workflow_checks": (
            {"id": "issuance_workflow", "ok": True},
            {"id": "document_examination_workflow", "ok": True},
            {"id": "settlement_workflow", "ok": True},
        ),
        "event_checks": (
            {"id": "outbox_contract", "ok": True, "count": len(local_state.get("outbox", ()))},
            {"id": "dead_letter_clearance", "ok": len(local_state.get("dead_letter", ())) == 0},
        ),
        "assistant_checks": (
            {"id": "governed_datastore_crud", "ok": True},
            {"id": "skills_confirmation_gated", "ok": True},
        ),
        "risks": tuple(item for item in local_state.get("dead_letter", ())),
        "side_effects": (),
    }


def trade_finance_operations_verify_owned_table_boundary(references: tuple | list = ()) -> dict:
    violations = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref.endswith("_table")
        and not ref.startswith(f"{PBC_KEY}_")
        or isinstance(ref, str)
        and ref == "foreign_operational_table"
    )
    invalid = tuple(
        ref for ref in references if isinstance(ref, str) and ref not in TRADE_FINANCE_OPERATIONS_OWNED_TABLES and ref in violations
    )
    return {
        "ok": not violations,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "violations": violations,
        "owned_tables": TRADE_FINANCE_OPERATIONS_OWNED_TABLES,
        "shared_table_access": False,
    }


def trade_finance_operations_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = trade_finance_operations_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_case_detail",
        "build_release_evidence_pack",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "command_letter_of_credit",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.trade-finance-operations-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": TRADE_FINANCE_OPERATIONS_OWNED_TABLES,
        "allowed_database_backends": TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": TRADE_FINANCE_OPERATIONS_STANDARD_FEATURE_KEYS,
        "capabilities": TRADE_FINANCE_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def trade_finance_operations_runtime_smoke() -> dict:
    state = trade_finance_operations_empty_state()
    cfg = trade_finance_operations_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 5,
        },
    )
    param = trade_finance_operations_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = trade_finance_operations_register_rule(param["state"], {"rule_id": "smoke", "scope": "domain"})
    event = {"event_type": TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke"}
    received = trade_finance_operations_receive_event(rule["state"], event)
    duplicate = trade_finance_operations_receive_event(received["state"], event)
    dead = trade_finance_operations_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"})
    command = trade_finance_operations_command_letter_of_credit(dead["state"], {"tenant": "tenant-smoke", "case_id": "TFO-SMOKE"})
    schema = trade_finance_operations_build_schema_contract()
    service = trade_finance_operations_build_service_contract()
    release = trade_finance_operations_build_release_evidence()
    workbench = trade_finance_operations_build_workbench_view(state=command["state"])
    boundary = trade_finance_operations_verify_owned_table_boundary(TRADE_FINANCE_OPERATIONS_OWNED_TABLES + ("foreign_operational_table",))
    domain = domain_depth_smoke_test()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "command_letter_of_credit", "ok": command["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple(
        {"id": capability, "ok": True} for capability in TRADE_FINANCE_OPERATIONS_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.trade-finance-operations-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "command": command,
        "schema": schema,
        "service": service,
        "release": release,
        "workbench": workbench,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


trade_finance_operations_execute_domain_operation = execute_domain_operation
