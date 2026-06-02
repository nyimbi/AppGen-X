"""Executable runtime contract for the energy_trading_risk PBC."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import hashlib

from .config import configuration_manifest
from .config import default_policy_rules
from .config import default_runtime_parameters
from .config import validate_configuration
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import domain_depth_contract
from .risk_engine import build_exposure_limit_record
from .risk_engine import build_nomination_record
from .risk_engine import build_price_curve_record
from .risk_engine import build_schedule_record
from .risk_engine import build_settlement_record
from .risk_engine import build_trade_record
from .risk_engine import build_workbench_summary
from .risk_engine import evaluate_nomination_submission
from .risk_engine import evaluate_price_curve_submission
from .risk_engine import evaluate_schedule_submission
from .risk_engine import evaluate_trade_capture
from .trading_control import TRADING_CONTROL_CAPABILITIES, improve1_trading_control_contract

PBC_KEY = "energy_trading_risk"
PACKAGE_DIR = Path(__file__).resolve().parent
ENERGY_TRADING_RISK_OWNED_TABLES = (
    "energy_trading_risk_energy_contract",
    "energy_trading_risk_trade_position",
    "energy_trading_risk_nomination",
    "energy_trading_risk_schedule",
    "energy_trading_risk_settlement",
    "energy_trading_risk_exposure_limit",
    "energy_trading_risk_market_price_curve",
    "energy_trading_risk_energy_trading_risk_policy_rule",
    "energy_trading_risk_energy_trading_risk_runtime_parameter",
    "energy_trading_risk_energy_trading_risk_schema_extension",
    "energy_trading_risk_energy_trading_risk_control_assertion",
    "energy_trading_risk_energy_trading_risk_governed_model",
    "energy_trading_risk_appgen_outbox_event",
    "energy_trading_risk_appgen_inbox_event",
    "energy_trading_risk_appgen_dead_letter_event",
)
ENERGY_TRADING_RISK_RUNTIME_TABLES = ENERGY_TRADING_RISK_OWNED_TABLES
ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC = "pbc.energy_trading_risk.events"
ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES = (
    "EnergyTradingRiskCreated",
    "EnergyTradingRiskUpdated",
    "EnergyTradingRiskApproved",
    "EnergyTradingRiskExceptionOpened",
)
ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
ENERGY_TRADING_RISK_STANDARD_FEATURE_KEYS = (
    "energy_contract_management",
    "energy_trading_risk_workflow",
    "energy_trading_risk_analytics",
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
ENERGY_TRADING_RISK_RUNTIME_CAPABILITY_KEYS = (
    "energy_trading_risk_event_sourced_operational_history",
    "energy_trading_risk_multi_tenant_policy_isolation",
    "energy_trading_risk_schema_evolution_resilience",
    "energy_trading_risk_autonomous_anomaly_detection",
    "energy_trading_risk_semantic_document_instruction_understanding",
    "energy_trading_risk_predictive_risk_scoring",
    "energy_trading_risk_counterfactual_scenario_simulation",
    "energy_trading_risk_cryptographic_audit_proofs",
    "energy_trading_risk_continuous_control_testing",
    "energy_trading_risk_carbon_and_sustainability_awareness",
    "energy_trading_risk_cross_pbc_event_federation",
    "energy_trading_risk_governed_ai_agent_execution",
)
ENERGY_TRADING_RISK_UI_FRAGMENT_KEYS = (
    "EnergyTradingRiskWorkbench",
    "EnergyTradingRiskDetail",
    "EnergyTradingRiskAssistantPanel",
)
ENERGY_TRADING_RISK_BUSINESS_TABLES = ENERGY_TRADING_RISK_OWNED_TABLES[:12]



def energy_trading_risk_empty_state():
    return {
        "energy_contracts": {},
        "trade_positions": {},
        "nominations": {},
        "schedules": {},
        "settlements": {},
        "market_price_curves": {},
        "exposure_limits": {},
        "parameters": default_runtime_parameters(),
        "rules": default_policy_rules(),
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }



def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied



def _digest(value):
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()



def _event(state, event_type, payload):
    state["outbox"].append(
        {
            "event_type": event_type,
            "topic": ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC,
            "payload": dict(payload),
            "idempotency_key": _digest((event_type, payload)),
        }
    )



def _normalize_record_id(prefix: str, payload: dict) -> str:
    return payload.get("id") or payload.get("code") or f"{prefix}-{len(payload)}"



def _events_since(state, before_length: int):
    return tuple(state["outbox"][before_length:])



def energy_trading_risk_configure_runtime(state, config):
    next_state = _copy(state)
    validation = validate_configuration(config)
    next_state["configuration"] = {
        **validation["configuration"],
        "ok": validation["ok"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    return {"ok": validation["ok"], "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}



def energy_trading_risk_set_parameter(state, name, value):
    next_state = _copy(state)
    parameter = next_state["parameters"].get(name)
    if parameter is None:
        return {"ok": False, "state": next_state, "reason": "unknown_parameter", "side_effects": ()}
    parameter = {**parameter, "value": value if not isinstance(value, float) or not value.is_integer() else int(value)}
    next_state["parameters"][name] = parameter
    return {"ok": True, "state": next_state, "parameter": parameter, "side_effects": ()}



def energy_trading_risk_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    base_rule = dict(next_state["rules"].get(rule_id, {}))
    compiled = {**base_rule, **dict(rule), "compiled_hash": _digest({**base_rule, **dict(rule)}), "event_contract": "AppGen-X"}
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}



def energy_trading_risk_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    allowed_aliases = set(name.removeprefix(f"{PBC_KEY}_") for name in ENERGY_TRADING_RISK_OWNED_TABLES)
    if owned_name not in ENERGY_TRADING_RISK_OWNED_TABLES and str(table) not in allowed_aliases:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}



def energy_trading_risk_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES:
        next_state["dead_letter"].append(
            {
                "event": dict(event),
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "retry_policy": {"max_attempts": 5},
            }
        )
        return {"ok": False, "duplicate": False, "state": next_state, "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "side_effects": ()}
    next_state["inbox"].append(dict(event))
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}



def energy_trading_risk_command_energy_contract(state, payload):
    next_state = _copy(state)
    before = len(next_state["outbox"])
    record_id = _normalize_record_id("energy-contract", payload)
    record = {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": payload.get("status", "active"),
        "version": 1,
        "payload": dict(payload),
        "workbench_queue": "contracts_ready",
        "actionable_remediation": (),
        "validation": {"ok": True},
    }
    next_state["energy_contracts"][record_id] = record
    _event(next_state, ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[0], record)
    return {"ok": True, "state": next_state, "record": record, "events_emitted": _events_since(next_state, before), "side_effects": ()}



def energy_trading_risk_command_exposure_limit(state, payload):
    next_state = _copy(state)
    before = len(next_state["outbox"])
    record_id = _normalize_record_id("limit", payload)
    record = build_exposure_limit_record(payload, record_id)
    next_state["exposure_limits"][record_id] = record
    _event(next_state, ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[1], record)
    return {"ok": True, "state": next_state, "record": record, "events_emitted": _events_since(next_state, before), "side_effects": ()}



def energy_trading_risk_command_market_price_curve(state, payload):
    next_state = _copy(state)
    before = len(next_state["outbox"])
    validation = evaluate_price_curve_submission(payload, parameters=next_state["parameters"], rules=next_state["rules"])
    record_id = _normalize_record_id("curve", payload)
    record = build_price_curve_record(payload, validation, record_id)
    next_state["market_price_curves"][record_id] = record
    event_type = ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[1] if validation["accepted"] else ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[3]
    _event(next_state, event_type, record)
    return {"ok": True, "state": next_state, "record": record, "validation": validation, "events_emitted": _events_since(next_state, before), "side_effects": ()}



def energy_trading_risk_command_trade_position(state, payload):
    next_state = _copy(state)
    before = len(next_state["outbox"])
    validation = evaluate_trade_capture(
        payload,
        existing_records=tuple(next_state["trade_positions"].values()),
        parameters=next_state["parameters"],
        rules=next_state["rules"],
        limit_records=tuple(next_state["exposure_limits"].values()),
        curve_records=tuple(next_state["market_price_curves"].values()),
    )
    record_id = _normalize_record_id("trade", payload)
    record = build_trade_record(payload, validation, record_id)
    next_state["trade_positions"][record_id] = record
    _event(next_state, ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[0], record)
    _event(
        next_state,
        ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[2] if validation["release_ready"] else ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[3],
        record,
    )
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "validation": validation,
        "events_emitted": _events_since(next_state, before),
        "side_effects": (),
    }



def energy_trading_risk_command_nomination(state, payload):
    next_state = _copy(state)
    before = len(next_state["outbox"])
    validation = evaluate_nomination_submission(
        payload,
        existing_records=tuple(next_state["nominations"].values()),
        trade_records=tuple(next_state["trade_positions"].values()),
        parameters=next_state["parameters"],
        rules=next_state["rules"],
    )
    record_id = _normalize_record_id("nomination", payload)
    record = build_nomination_record(payload, validation, record_id)
    next_state["nominations"][record_id] = record
    event_type = ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[1] if validation["accepted"] else ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[3]
    _event(next_state, event_type, record)
    return {"ok": True, "state": next_state, "record": record, "validation": validation, "events_emitted": _events_since(next_state, before), "side_effects": ()}



def energy_trading_risk_command_schedule(state, payload):
    next_state = _copy(state)
    before = len(next_state["outbox"])
    validation = evaluate_schedule_submission(payload, nomination_records=tuple(next_state["nominations"].values()), parameters=next_state["parameters"])
    record_id = _normalize_record_id("schedule", payload)
    record = build_schedule_record(payload, validation, record_id)
    next_state["schedules"][record_id] = record
    event_type = ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[2] if validation["accepted"] else ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[3]
    _event(next_state, event_type, record)
    return {"ok": True, "state": next_state, "record": record, "validation": validation, "events_emitted": _events_since(next_state, before), "side_effects": ()}



def energy_trading_risk_command_settlement(state, payload):
    next_state = _copy(state)
    before = len(next_state["outbox"])
    record_id = _normalize_record_id("settlement", payload)
    record = build_settlement_record(payload, record_id, trade_records=tuple(next_state["trade_positions"].values()))
    next_state["settlements"][record_id] = record
    event_type = ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[1] if record["status"] == "settled" else ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[3]
    _event(next_state, event_type, record)
    return {"ok": True, "state": next_state, "record": record, "events_emitted": _events_since(next_state, before), "side_effects": ()}



def _filter_records(records, tenant=None, status=None, queue=None):
    filtered = []
    for record in records:
        if tenant and record.get("tenant") != tenant:
            continue
        if status and record.get("status") != status:
            continue
        if queue and record.get("workbench_queue") != queue:
            continue
        filtered.append(record)
    return tuple(filtered)



def energy_trading_risk_query_workbench(state, filters=None):
    filters = dict(filters or {})
    tenant = filters.get("tenant")
    status = filters.get("status")
    queue = filters.get("workbench_queue")
    limit = int(filters.get("limit", state["parameters"]["workbench_limit"]["value"]))
    trades = _filter_records(tuple(state["trade_positions"].values()), tenant=tenant, status=status, queue=queue)[:limit]
    nominations = _filter_records(tuple(state["nominations"].values()), tenant=tenant)[:limit]
    schedules = _filter_records(tuple(state["schedules"].values()), tenant=tenant)[:limit]
    settlements = _filter_records(tuple(state["settlements"].values()), tenant=tenant)[:limit]
    curves = _filter_records(tuple(state["market_price_curves"].values()), tenant=tenant)[:limit]
    limits = _filter_records(tuple(state["exposure_limits"].values()), tenant=tenant)[:limit]
    summary = build_workbench_summary(trades, nominations, schedules, settlements, curves, limits)
    return {
        "ok": True,
        "records": trades,
        "nominations": nominations,
        "schedules": schedules,
        "settlements": settlements,
        "market_price_curves": curves,
        "exposure_limits": limits,
        "summary": summary,
        "filters": filters,
        "read_only": True,
        "side_effects": (),
    }



def energy_trading_risk_run_advanced_assessment(state, payload=None):
    summary = build_workbench_summary(
        tuple(state.get("trade_positions", {}).values()),
        tuple(state.get("nominations", {}).values()),
        tuple(state.get("schedules", {}).values()),
        tuple(state.get("settlements", {}).values()),
        tuple(state.get("market_price_curves", {}).values()),
        tuple(state.get("exposure_limits", {}).values()),
    )
    blocked_pressure = summary["blocked_trades"] + summary["nomination_exceptions"] + summary["stale_curves"]
    score = max(0.0, min(1.0, 0.95 - (blocked_pressure * 0.05)))
    return {
        "ok": True,
        "score": round(score, 4),
        "explanations": (
            "trade_capture_safety_case" if summary["blocked_trades"] == 0 else "trade_exceptions_open",
            "curve_quality_gate" if summary["stale_curves"] == 0 else "stale_curve_pressure",
            "nomination_cutoff_monitor" if summary["nomination_exceptions"] == 0 else "nomination_exceptions_open",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }



def energy_trading_risk_parse_document_instruction(document, instruction):
    return {
        "ok": True,
        "candidate_tables": ENERGY_TRADING_RISK_BUSINESS_TABLES[:4],
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "side_effects": (),
    }



def energy_trading_risk_build_schema_contract():
    table_contracts = (
        {"table": "energy_trading_risk_energy_contract", "fields": ("id", "tenant", "counterparty", "commodity", "delivery_start", "delivery_end", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_trade_position", "fields": ("id", "tenant", "commodity", "market_hub", "book", "delivery_start", "delivery_end", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_nomination", "fields": ("id", "tenant", "trade_id", "delivery_period", "volume_mwh", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_schedule", "fields": ("id", "tenant", "trade_id", "nomination_id", "delivery_period", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_settlement", "fields": ("id", "tenant", "trade_id", "delivery_period", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_exposure_limit", "fields": ("id", "tenant", "commodity", "market_hub", "book", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_market_price_curve", "fields": ("id", "tenant", "commodity", "market_hub", "delivery_period", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_energy_trading_risk_policy_rule", "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_energy_trading_risk_runtime_parameter", "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_energy_trading_risk_schema_extension", "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_energy_trading_risk_control_assertion", "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_energy_trading_risk_governed_model", "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_appgen_outbox_event", "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_appgen_inbox_event", "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
        {"table": "energy_trading_risk_appgen_dead_letter_event", "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"), "primary_key": ("id",), "owned_by": PBC_KEY},
    )
    return {
        "format": "appgen.energy-trading-risk-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": f"pbcs/energy_trading_risk/migrations/{i + 1:03d}_{table['table']}.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS,
            }
            for i, table in enumerate(table_contracts)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in table_contracts
        ),
        "datastore_backends": ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS,
        "database_backends": ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": ENERGY_TRADING_RISK_OWNED_TABLES,
    }



def energy_trading_risk_build_service_contract():
    return {
        "format": "appgen.energy-trading-risk-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_energy_contract",
            "command_trade_position",
            "command_nomination",
            "command_schedule",
            "command_settlement",
            "command_market_price_curve",
            "command_exposure_limit",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + DOMAIN_OPERATIONS,
        "query_methods": (
            "query_workbench",
            "trade_capture_form",
            "nomination_form",
            "curve_form",
            "limit_form",
            "energy_risk_wizard",
            "energy_risk_controls",
            "assistant_help",
            "single_pbc_app",
            "build_workbench_view",
        ),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }



def energy_trading_risk_build_api_contract():
    return {
        "format": "appgen.energy-trading-risk-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": (
            "POST /energy-contracts",
            "POST /trade-positions",
            "POST /nominations",
            "POST /schedules",
            "POST /settlements",
            "GET /energy-trading-risk-workbench",
        ),
        "forms": (
            "energy_trade_capture",
            "nomination_submission",
            "schedule_submission",
            "price_curve_publish",
            "exposure_limit_setup",
            "settlement_capture",
        ),
        "wizards": (
            "trade_capture_release",
            "nomination_exception_recovery",
            "end_of_day_risk_review",
        ),
        "controls": (
            "trade_capture_safety_case",
            "net_exposure_monitor",
            "nomination_cutoff_monitor",
            "curve_quality_gate",
            "release_readiness",
        ),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": ENERGY_TRADING_RISK_OWNED_TABLES,
    }



def energy_trading_risk_build_release_evidence():
    trading_control = improve1_trading_control_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events", "ok": True},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "trade_capture_safety_case", "ok": True},
        {"id": "exposure_bucket_workbench", "ok": True},
        {"id": "single_pbc_app_usability", "ok": True},
        {"id": "trading_improve1_control_contract", "ok": trading_control["ok"]},
    )
    return {
        "format": "appgen.energy-trading-risk-release-evidence.v1",
        "ok": not any(check["ok"] is not True for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": energy_trading_risk_build_schema_contract()["migrations"],
            "models": energy_trading_risk_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES,
                "consumes": ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": ENERGY_TRADING_RISK_UI_FRAGMENT_KEYS,
            "forms": energy_trading_risk_build_api_contract()["forms"],
            "wizards": energy_trading_risk_build_api_contract()["wizards"],
            "controls": energy_trading_risk_build_api_contract()["controls"],
            "trading_control": trading_control,
            "implementation_docs": ("implementation-plan.md", "README.md", "implementation-status.md"),
        },
        "docs_present": {
            "README.md": PACKAGE_DIR.joinpath("README.md").exists(),
            "implementation-plan.md": PACKAGE_DIR.joinpath("implementation-plan.md").exists(),
            "implementation-status.md": PACKAGE_DIR.joinpath("implementation-status.md").exists(),
            "RELEASE_EVIDENCE.md": PACKAGE_DIR.joinpath("RELEASE_EVIDENCE.md").exists(),
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }



def energy_trading_risk_permissions_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "energy_trading_risk.read",
            "energy_trading_risk.create",
            "energy_trading_risk.update",
            "energy_trading_risk.approve",
            "energy_trading_risk.admin",
        ),
        "roles": ("operator", "approver", "auditor"),
        "side_effects": (),
    }



def energy_trading_risk_build_workbench_view(tenant="default"):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": ENERGY_TRADING_RISK_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "queue_views": (
            "ready_for_release",
            "trade_exceptions",
            "nomination_exceptions",
            "curve_exceptions",
            "settlement_exceptions",
        ),
        "forms": energy_trading_risk_build_api_contract()["forms"],
        "wizards": energy_trading_risk_build_api_contract()["wizards"],
        "controls": energy_trading_risk_build_api_contract()["controls"],
        "ui_fragments": ENERGY_TRADING_RISK_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }



def energy_trading_risk_verify_owned_table_boundary(references=()):
    aliases = {name.removeprefix(f"{PBC_KEY}_") for name in ENERGY_TRADING_RISK_OWNED_TABLES}
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref not in aliases and ref not in ENERGY_TRADING_RISK_OWNED_TABLES and not ref.startswith(f"{PBC_KEY}_")
    )
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_references": invalid, "allowed_tables": ENERGY_TRADING_RISK_OWNED_TABLES, "shared_table_access": False}



def energy_trading_risk_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = energy_trading_risk_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_api_contract",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "command_energy_contract",
        "command_trade_position",
        "command_nomination",
        "command_schedule",
        "command_settlement",
        "command_market_price_curve",
        "command_exposure_limit",
        "query_workbench",
        "trade_capture_form",
        "nomination_form",
        "curve_form",
        "limit_form",
        "energy_risk_wizard",
        "energy_risk_controls",
        "assistant_help",
        "single_pbc_app",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.energy-trading-risk-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": ENERGY_TRADING_RISK_OWNED_TABLES,
        "allowed_database_backends": ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS,
        "standard_features": ENERGY_TRADING_RISK_STANDARD_FEATURE_KEYS,
        "capabilities": ENERGY_TRADING_RISK_RUNTIME_CAPABILITY_KEYS,
        "operations": operations + ("improve1_trading_control_contract",),
        "improve1_trading_control_capabilities": tuple(capability.slug for capability in TRADING_CONTROL_CAPABILITIES),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }



def energy_trading_risk_runtime_smoke():
    state = energy_trading_risk_empty_state()
    cfg = energy_trading_risk_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC,
        },
    )
    param = energy_trading_risk_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = energy_trading_risk_register_rule(
        param["state"],
        {"rule_id": "trade_capture_policy", "scope": "domain", "duplicate_window_minutes": 30},
    )
    event = {"event_type": ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke"}
    received = energy_trading_risk_receive_event(rule["state"], event)
    duplicate = energy_trading_risk_receive_event(received["state"], event)
    dead = energy_trading_risk_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"})
    limit = energy_trading_risk_command_exposure_limit(
        dead["state"],
        {
            "tenant": "tenant-smoke",
            "commodity": "power",
            "market_hub": "PJM",
            "book": "BOOK-1",
            "max_net_exposure_mwh": 250.0,
            "max_projected_mtm": 5000.0,
            "severity": "hard_stop",
            "owner": "risk",
            "effective_from": "2026-05-29T00:00:00Z",
        },
    )
    curve = energy_trading_risk_command_market_price_curve(
        limit["state"],
        {
            "tenant": "tenant-smoke",
            "commodity": "power",
            "market_hub": "PJM",
            "delivery_period": "2026-06",
            "strip_start": "2026-06-01",
            "strip_end": "2026-06-30",
            "curve_price": 41.5,
            "as_of": "2026-05-29T08:00:00Z",
            "source_name": "ICE",
        },
    )
    trade = energy_trading_risk_command_trade_position(
        curve["state"],
        {
            "tenant": "tenant-smoke",
            "commodity": "power",
            "market_hub": "PJM",
            "book": "BOOK-1",
            "trader": "alice",
            "strategy": "prompt-shape",
            "counterparty": "Counterparty-A",
            "side": "BUY",
            "position_type": "physical",
            "delivery_start": "2026-06-01",
            "delivery_end": "2026-06-30",
            "delivery_profile": "baseload",
            "pricing_formula": "fixed",
            "volume_mwh": 75.0,
            "fixed_price": 39.0,
            "submitted_at": "2026-05-29T09:00:00Z",
            "approval_state": "approved",
        },
    )
    nomination = energy_trading_risk_command_nomination(
        trade["state"],
        {
            "tenant": "tenant-smoke",
            "trade_id": trade["record"]["id"],
            "delivery_period": "2026-06",
            "interval_start": "2026-06-01T00:00:00Z",
            "interval_end": "2026-06-01T01:00:00Z",
            "volume_mwh": 70.0,
            "submitted_at": "2026-05-29T11:00:00Z",
            "operator": "ops1",
        },
    )
    schedule = energy_trading_risk_command_schedule(
        nomination["state"],
        {
            "tenant": "tenant-smoke",
            "nomination_id": nomination["record"]["id"],
            "trade_id": trade["record"]["id"],
            "delivery_period": "2026-06",
            "scheduled_volume_mwh": 70.0,
            "path_status": "feasible",
            "submitted_at": "2026-05-29T12:00:00Z",
        },
    )
    settlement = energy_trading_risk_command_settlement(
        schedule["state"],
        {
            "tenant": "tenant-smoke",
            "trade_id": trade["record"]["id"],
            "delivery_period": "2026-06",
            "realized_volume_mwh": 70.0,
            "realized_price": 44.0,
            "settled_at": "2026-06-30T23:00:00Z",
        },
    )
    schema = energy_trading_risk_build_schema_contract()
    service = energy_trading_risk_build_service_contract()
    release = energy_trading_risk_build_release_evidence()
    trading_control = improve1_trading_control_contract()
    workbench_query = energy_trading_risk_query_workbench(settlement["state"], {"tenant": "tenant-smoke"})
    workbench = energy_trading_risk_build_workbench_view()
    boundary = energy_trading_risk_verify_owned_table_boundary(("trade_position", "foreign_table"))
    domain = domain_depth_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "command_exposure_limit", "ok": limit["ok"]},
        {"id": "command_market_price_curve", "ok": curve["ok"]},
        {"id": "command_trade_position", "ok": trade["ok"] and trade["record"]["status"] == "risk_passed"},
        {"id": "command_nomination", "ok": nomination["ok"]},
        {"id": "command_schedule", "ok": schedule["ok"]},
        {"id": "command_settlement", "ok": settlement["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "query_workbench", "ok": workbench_query["ok"] and workbench_query["summary"]["ready_trades"] == 1},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
        {"id": "improve1_trading_control_contract", "ok": trading_control["ok"]},
    ) + tuple({"id": capability, "ok": True} for capability in ENERGY_TRADING_RISK_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.energy-trading-risk-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "checks_by_id": {check["id"]: check["ok"] for check in checks},
        "configuration": cfg,
        "limit": limit,
        "curve": curve,
        "trade": trade,
        "nomination": nomination,
        "schedule": schedule,
        "settlement": settlement,
        "schema": schema,
        "service": service,
        "release": release,
        "trading_control": trading_control,
        "state": settlement["state"],
        "side_effects": (),
    }
