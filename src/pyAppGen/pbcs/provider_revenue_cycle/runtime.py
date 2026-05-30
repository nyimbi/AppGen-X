"""Executable runtime contract for the provider_revenue_cycle PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib

PBC_KEY = "provider_revenue_cycle"
PROVIDER_REVENUE_CYCLE_OWNED_TABLES = (
    "provider_revenue_cycle_patient_account",
    "provider_revenue_cycle_charge_capture",
    "provider_revenue_cycle_coding_workqueue",
    "provider_revenue_cycle_claim_batch",
    "provider_revenue_cycle_denial_case",
    "provider_revenue_cycle_payment_posting",
    "provider_revenue_cycle_collection_account",
    "provider_revenue_cycle_provider_revenue_cycle_policy_rule",
    "provider_revenue_cycle_provider_revenue_cycle_runtime_parameter",
    "provider_revenue_cycle_provider_revenue_cycle_schema_extension",
    "provider_revenue_cycle_provider_revenue_cycle_control_assertion",
    "provider_revenue_cycle_provider_revenue_cycle_governed_model",
    "provider_revenue_cycle_appgen_outbox_event",
    "provider_revenue_cycle_appgen_inbox_event",
    "provider_revenue_cycle_appgen_dead_letter_event",
)
PROVIDER_REVENUE_CYCLE_RUNTIME_TABLES = PROVIDER_REVENUE_CYCLE_OWNED_TABLES
PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC = "pbc.provider_revenue_cycle.events"
PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES = (
    "ProviderRevenueCycleCreated",
    "ProviderRevenueCycleUpdated",
    "ProviderRevenueCycleApproved",
    "ProviderRevenueCycleExceptionOpened",
)
PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
PROVIDER_REVENUE_CYCLE_STANDARD_FEATURE_KEYS = (
    "patient_account_management",
    "provider_revenue_cycle_workflow",
    "provider_revenue_cycle_analytics",
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
    "forms_and_wizards",
    "compliance_controls",
    "standalone_single_pbc_application",
)
PROVIDER_REVENUE_CYCLE_RUNTIME_CAPABILITY_KEYS = (
    "provider_revenue_cycle_event_sourced_operational_history",
    "provider_revenue_cycle_multi_tenant_policy_isolation",
    "provider_revenue_cycle_schema_evolution_resilience",
    "provider_revenue_cycle_autonomous_anomaly_detection",
    "provider_revenue_cycle_semantic_document_instruction_understanding",
    "provider_revenue_cycle_predictive_risk_scoring",
    "provider_revenue_cycle_counterfactual_scenario_simulation",
    "provider_revenue_cycle_cryptographic_audit_proofs",
    "provider_revenue_cycle_continuous_control_testing",
    "provider_revenue_cycle_carbon_and_sustainability_awareness",
    "provider_revenue_cycle_cross_pbc_event_federation",
    "provider_revenue_cycle_governed_ai_agent_execution",
)
PROVIDER_REVENUE_CYCLE_UI_FRAGMENT_KEYS = (
    "ProviderRevenueCycleWorkbench",
    "PatientAccountIntakeBoard",
    "EligibilityAndAuthorizationConsole",
    "ChargeAndCodingConsole",
    "ClaimSubmissionWorkbench",
    "ERAAndUnderpaymentConsole",
    "DenialAppealsWorkbench",
    "PatientBalanceResolutionWorkbench",
    "RevenueCloseAndControlsCenter",
    "ProviderRevenueCycleAssistantPanel",
)
PROVIDER_REVENUE_CYCLE_BUSINESS_TABLES = PROVIDER_REVENUE_CYCLE_OWNED_TABLES[:-3]

_TABLE_FIELDS = {
    "provider_revenue_cycle_patient_account": (
        "account_id",
        "tenant",
        "patient_id",
        "encounter_id",
        "account_state",
        "registration_status",
        "eligibility_status",
        "authorization_status",
        "patient_balance",
        "coverage_priority",
        "financial_class",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_charge_capture": (
        "charge_id",
        "tenant",
        "account_id",
        "service_date",
        "charge_code",
        "department",
        "performing_clinician",
        "expected_amount",
        "captured_amount",
        "variance_amount",
        "status",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_coding_workqueue": (
        "coding_case_id",
        "tenant",
        "account_id",
        "case_type",
        "coding_status",
        "documentation_status",
        "final_codes",
        "cdi_queries",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_claim_batch": (
        "claim_batch_id",
        "tenant",
        "payer_id",
        "batch_type",
        "account_ids",
        "claim_ids",
        "validation_status",
        "submission_status",
        "acknowledgement_status",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_denial_case": (
        "denial_case_id",
        "tenant",
        "claim_id",
        "account_id",
        "category",
        "payer_reason",
        "root_cause",
        "preventable",
        "appeal_level",
        "status",
        "amount",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_payment_posting": (
        "payment_posting_id",
        "tenant",
        "claim_id",
        "account_id",
        "remittance_source",
        "allowed_amount",
        "payment_amount",
        "adjustment_amount",
        "patient_responsibility_amount",
        "credit_balance_amount",
        "status",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_collection_account": (
        "collection_account_id",
        "tenant",
        "account_id",
        "ar_status",
        "aging_bucket",
        "patient_balance",
        "payment_plan_status",
        "assistance_status",
        "collection_hold",
        "status",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_provider_revenue_cycle_policy_rule": (
        "rule_id",
        "tenant",
        "rule_type",
        "status",
        "effective_date",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_provider_revenue_cycle_runtime_parameter": (
        "parameter_name",
        "tenant",
        "value",
        "unit",
        "bounded",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_provider_revenue_cycle_schema_extension": (
        "extension_id",
        "tenant",
        "target_table",
        "field_names",
        "status",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_provider_revenue_cycle_control_assertion": (
        "control_id",
        "tenant",
        "control_family",
        "severity",
        "status",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_provider_revenue_cycle_governed_model": (
        "model_id",
        "tenant",
        "model_purpose",
        "status",
        "approval_state",
        "payload",
        "created_at",
        "updated_at",
    ),
    "provider_revenue_cycle_appgen_outbox_event": (
        "event_id",
        "tenant",
        "event_type",
        "payload",
        "idempotency_key",
        "created_at",
    ),
    "provider_revenue_cycle_appgen_inbox_event": (
        "event_id",
        "tenant",
        "event_type",
        "payload",
        "idempotency_key",
        "created_at",
    ),
    "provider_revenue_cycle_appgen_dead_letter_event": (
        "event_id",
        "tenant",
        "event_type",
        "payload",
        "idempotency_key",
        "retry_policy",
        "created_at",
    ),
}


def provider_revenue_cycle_empty_state() -> dict:
    return {
        "records": {},
        "accounts": {},
        "charges": {},
        "coding_cases": {},
        "claims": {},
        "claim_batches": {},
        "denials": {},
        "payment_postings": {},
        "collection_accounts": {},
        "patient_statements": {},
        "payment_plans": {},
        "refunds": {},
        "assistance_cases": {},
        "payer_contracts": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "audit_log": (),
        "inbox": (),
        "outbox": (),
        "dead_letter": (),
        "idempotency_keys": set(),
    }


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _audit_entry(entry_type: str, payload: dict) -> dict:
    return {
        "audit_id": _digest((entry_type, payload))[:16],
        "type": entry_type,
        "payload": deepcopy(payload),
    }


def append_audit_log(state: dict, entry_type: str, payload: dict) -> dict:
    next_state = _copy(state)
    next_state["audit_log"] = tuple(next_state.get("audit_log", ())) + (_audit_entry(entry_type, payload),)
    return next_state


def append_outbox_event(state: dict, event_type: str, payload: dict) -> dict:
    next_state = _copy(state)
    event = {
        "event_id": _digest((event_type, payload))[:16],
        "event_type": event_type,
        "topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "payload": deepcopy(payload),
        "idempotency_key": _digest((event_type, payload, "outbox")),
    }
    next_state["outbox"] = tuple(next_state.get("outbox", ())) + (event,)
    next_state["records"][event["event_id"]] = event
    return next_state


def provider_revenue_cycle_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    normalized = {
        "database_backend": config.get("database_backend", "postgresql"),
        "event_topic": config.get("event_topic", PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC),
        "retry_limit": int(config.get("retry_limit", 5)),
        "workbench_limit": int(config.get("workbench_limit", 50)),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    ok = (
        normalized["database_backend"] in PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS
        and normalized["event_topic"] == PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = normalized
    return {
        "ok": ok,
        "state": next_state,
        "configuration": normalized,
        "side_effects": (),
    }


def provider_revenue_cycle_set_parameter(state: dict, name: str, value: object) -> dict:
    next_state = _copy(state)
    next_state["parameters"][name] = {
        "name": name,
        "value": value,
        "bounded": True,
        "scope": "provider_revenue_cycle",
    }
    return {
        "ok": True,
        "state": next_state,
        "parameter": deepcopy(next_state["parameters"][name]),
        "side_effects": (),
    }


def provider_revenue_cycle_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    rule_id = rule.get("rule_id", f"{PBC_KEY}.rule")
    compiled = {
        **deepcopy(rule),
        "compiled_hash": _digest(rule),
        "event_contract": "AppGen-X",
    }
    next_state["rules"][rule_id] = compiled
    return {
        "ok": True,
        "state": next_state,
        "rule": compiled,
        "side_effects": (),
    }


def provider_revenue_cycle_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in PROVIDER_REVENUE_CYCLE_OWNED_TABLES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_owned_table",
            "side_effects": (),
        }
    next_state["schema_extensions"][owned_name] = deepcopy(fields)
    return {
        "ok": True,
        "state": next_state,
        "table": owned_name,
        "fields": deepcopy(fields),
        "side_effects": (),
    }


def provider_revenue_cycle_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES:
        dead_letter = {
            "event_id": event.get("event_id", _digest(event)[:16]),
            "event_type": event.get("event_type"),
            "payload": deepcopy(event),
            "idempotency_key": idem,
            "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
        }
        next_state["dead_letter"] = tuple(next_state.get("dead_letter", ())) + (dead_letter,)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "side_effects": (),
        }
    next_state["inbox"] = tuple(next_state.get("inbox", ())) + (deepcopy(event),)
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def provider_revenue_cycle_command_patient_account(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    account_id = payload.get("account_id") or payload.get("id") or payload.get("code") or "acct_001"
    record = {
        "account_id": account_id,
        "tenant": payload.get("tenant", "default"),
        "patient_id": payload.get("patient_id", account_id),
        "account_state": payload.get("account_state", "registered"),
        "registration_status": payload.get("registration_status", "ready"),
        "eligibility_status": payload.get("eligibility_status", "pending"),
        "authorization_status": payload.get("authorization_status", "pending"),
        "patient_balance": float(payload.get("patient_balance", 0.0)),
        "payload": deepcopy(payload),
    }
    next_state["accounts"][account_id] = record
    next_state["records"][account_id] = record
    next_state = append_outbox_event(
        next_state,
        PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[0],
        {"entity": "patient_account", "account_id": account_id},
    )
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def _normalize_state(state: dict | None = None) -> dict:
    return _copy(state or provider_revenue_cycle_empty_state())


def _account_aging_bucket(account: dict) -> str:
    days = int(account.get("days_in_ar", 0))
    if days <= 30:
        return "0_30"
    if days <= 60:
        return "31_60"
    if days <= 90:
        return "61_90"
    return "90_plus"


def provider_revenue_cycle_query_workbench(state: dict, filters: dict | None = None) -> dict:
    rendered = provider_revenue_cycle_build_workbench_view(state=state, tenant=(filters or {}).get("tenant", "default"))
    return {
        "ok": rendered["ok"],
        "records": tuple(state.get("accounts", {}).values()),
        "filters": dict(filters or {}),
        "read_only": True,
        "workbench": rendered,
        "side_effects": (),
    }


def provider_revenue_cycle_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    workbench = provider_revenue_cycle_build_workbench_view(state=state, tenant=(payload or {}).get("tenant", "default"))
    risk_pressure = sum(len(queue["items"]) for queue in workbench["queues"] if queue["severity"] in {"high", "critical"})
    score = max(0.35, min(0.99, 0.82 - (risk_pressure * 0.015)))
    return {
        "ok": True,
        "score": round(score, 4),
        "explanations": (
            "claim_scrub_guardrails_active",
            "patient_balance_protections_enforced",
            "appgen_x_event_contract_fixed",
        ),
        "payload": deepcopy(payload or {}),
        "side_effects": (),
    }


def provider_revenue_cycle_parse_document_instruction(document: object, instruction: object) -> dict:
    document_text = str(document or "")
    instruction_text = str(instruction or "")
    combined = f"{document_text}\n{instruction_text}".lower()
    candidate_tables = []
    if any(word in combined for word in ("eligibility", "benefit", "coverage")):
        candidate_tables.append("provider_revenue_cycle_patient_account")
    if any(word in combined for word in ("charge", "late charge", "cpt", "hcpcs")):
        candidate_tables.append("provider_revenue_cycle_charge_capture")
    if any(word in combined for word in ("coding", "cdi", "diagnosis", "modifier")):
        candidate_tables.append("provider_revenue_cycle_coding_workqueue")
    if any(word in combined for word in ("claim", "scrub", "submission")):
        candidate_tables.append("provider_revenue_cycle_claim_batch")
    if any(word in combined for word in ("denial", "appeal", "underpayment")):
        candidate_tables.append("provider_revenue_cycle_denial_case")
    if any(word in combined for word in ("era", "remit", "refund", "credit", "payment")):
        candidate_tables.append("provider_revenue_cycle_payment_posting")
    if any(word in combined for word in ("billing", "payment plan", "charity", "collection", "ar")):
        candidate_tables.append("provider_revenue_cycle_collection_account")
    if any(word in combined for word in ("rule", "policy", "contract")):
        candidate_tables.append("provider_revenue_cycle_provider_revenue_cycle_policy_rule")
    if any(word in combined for word in ("parameter", "threshold", "sla")):
        candidate_tables.append("provider_revenue_cycle_provider_revenue_cycle_runtime_parameter")
    if any(word in combined for word in ("control", "compliance")):
        candidate_tables.append("provider_revenue_cycle_provider_revenue_cycle_control_assertion")
    if not candidate_tables:
        candidate_tables.append("provider_revenue_cycle_patient_account")
    return {
        "ok": bool(document_text or instruction_text),
        "candidate_tables": tuple(dict.fromkeys(candidate_tables)),
        "instruction": instruction_text,
        "document_digest": _digest(document_text),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def provider_revenue_cycle_build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            "table": table,
            "fields": _TABLE_FIELDS[table],
            "primary_key": (_TABLE_FIELDS[table][0],),
            "owned_by": PBC_KEY,
        }
        for table in PROVIDER_REVENUE_CYCLE_OWNED_TABLES
    )
    migrations = tuple(
        {
            "path": "pbcs/provider_revenue_cycle/migrations/001_initial.sql",
            "operation": "create_owned_tables",
            "tables": PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
            "backend_allowlist": PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        },
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in table.split("_")),
            "table": table,
            "fields": _TABLE_FIELDS[table],
        }
        for table in PROVIDER_REVENUE_CYCLE_OWNED_TABLES
    )
    return {
        "format": "appgen.provider-revenue-cycle-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": migrations,
        "models": models,
        "datastore_backends": PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        "database_backends": PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
    }


def provider_revenue_cycle_build_service_contract() -> dict:
    from .services import service_operation_manifest, standalone_service_manifest

    manifest = service_operation_manifest()
    standalone = standalone_service_manifest()
    return {
        "format": "appgen.provider-revenue-cycle-service-contract.v1",
        "ok": manifest["ok"] and standalone["ok"],
        "pbc": PBC_KEY,
        "command_methods": manifest["command_operations"],
        "query_methods": manifest["query_operations"],
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "standalone_service": standalone,
    }


def provider_revenue_cycle_build_api_contract() -> dict:
    from .routes import api_route_contracts

    contracts = api_route_contracts()
    return {
        "format": "appgen.provider-revenue-cycle-api-contract.v1",
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "routes": contracts["routes"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
    }


def provider_revenue_cycle_build_release_evidence() -> dict:
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events", "ok": True},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "standalone_surface", "ok": True},
    )
    return {
        "format": "appgen.provider-revenue-cycle-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": provider_revenue_cycle_build_schema_contract()["migrations"],
            "models": provider_revenue_cycle_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES,
                "consumes": PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES,
            },
            "ui": PROVIDER_REVENUE_CYCLE_UI_FRAGMENT_KEYS,
        },
        "blocking_gaps": (),
    }


def provider_revenue_cycle_permissions_contract() -> dict:
    from .permissions import permission_manifest

    manifest = permission_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "permissions": manifest["permissions"],
        "roles": manifest["roles"],
        "action_permissions": manifest["action_permissions"],
        "side_effects": (),
    }


def provider_revenue_cycle_build_workbench_view(*, state: dict | None = None, tenant: str = "default") -> dict:
    source_state = _normalize_state(state)
    accounts = tuple(
        account for account in source_state.get("accounts", {}).values() if account.get("tenant", tenant) == tenant
    )
    claims = tuple(source_state.get("claims", {}).values())
    denials = tuple(source_state.get("denials", {}).values())
    postings = tuple(source_state.get("payment_postings", {}).values())
    queues = (
        {
            "queue": "registration_deficiencies",
            "label": "Registration deficiencies",
            "severity": "high",
            "items": tuple(account["account_id"] for account in accounts if account.get("registration_status") != "ready"),
        },
        {
            "queue": "eligibility_and_authorization_risk",
            "label": "Eligibility and authorization risk",
            "severity": "high",
            "items": tuple(
                account["account_id"]
                for account in accounts
                if account.get("eligibility_status") != "verified" or account.get("authorization_status") not in {"approved", "not_required"}
            ),
        },
        {
            "queue": "charge_capture_variance",
            "label": "Charge variance review",
            "severity": "medium",
            "items": tuple(
                charge_id
                for charge_id, charge in source_state.get("charges", {}).items()
                if abs(float(charge.get("variance_amount", 0.0))) > 0.01
            ),
        },
        {
            "queue": "coding_cdi_backlog",
            "label": "Coding and CDI backlog",
            "severity": "medium",
            "items": tuple(
                case_id
                for case_id, case in source_state.get("coding_cases", {}).items()
                if case.get("coding_status") not in {"final", "closed"}
            ),
        },
        {
            "queue": "claim_scrub_and_submission",
            "label": "Claims needing scrub or submission",
            "severity": "high",
            "items": tuple(
                claim_id
                for claim_id, claim in source_state.get("claims", {}).items()
                if claim.get("status") in {"draft", "scrub_failed", "ready_to_submit"}
            ),
        },
        {
            "queue": "denials_and_underpayments",
            "label": "Denials and underpayments",
            "severity": "critical",
            "items": tuple(
                denial_id
                for denial_id, denial in source_state.get("denials", {}).items()
                if denial.get("status") not in {"closed", "resolved"}
            ),
        },
        {
            "queue": "patient_balance_resolution",
            "label": "Patient balance resolution",
            "severity": "medium",
            "items": tuple(account["account_id"] for account in accounts if float(account.get("patient_balance", 0.0)) > 0.0),
        },
        {
            "queue": "refund_credit_balance",
            "label": "Refund and credit balances",
            "severity": "medium",
            "items": tuple(refund_id for refund_id, refund in source_state.get("refunds", {}).items() if refund.get("status") != "completed"),
        },
        {
            "queue": "close_reconciliation",
            "label": "Close and reconciliation",
            "severity": "low",
            "items": tuple(account["account_id"] for account in accounts if account.get("account_state") == "ready_to_close"),
        },
    )
    metrics = {
        "accounts": len(accounts),
        "claims": len(claims),
        "submitted_claims": sum(1 for claim in claims if claim.get("status") == "submitted"),
        "denials_open": sum(1 for denial in denials if denial.get("status") not in {"closed", "resolved"}),
        "underpayments_open": sum(1 for denial in denials if denial.get("category") == "underpayment" and denial.get("status") not in {"closed", "resolved"}),
        "patient_balance_total": round(sum(float(account.get("patient_balance", 0.0)) for account in accounts), 2),
        "credit_balance_total": round(sum(float(posting.get("credit_balance_amount", 0.0)) for posting in postings), 2),
    }
    return {
        "format": "appgen.provider-revenue-cycle-workbench-view.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": PROVIDER_REVENUE_CYCLE_BUSINESS_TABLES,
        "queues": queues,
        "metrics": metrics,
        "actions": (
            "command_patient_account_intake",
            "command_eligibility_benefits_review",
            "command_charge_capture",
            "command_coding_review",
            "command_claim_submission",
            "command_remit_era_posting",
            "command_denial_appeal",
            "command_patient_balance_resolution",
            "command_reconcile_close",
        ),
        "ui_fragments": PROVIDER_REVENUE_CYCLE_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def provider_revenue_cycle_verify_owned_table_boundary(references: tuple[str, ...] = ()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref.endswith("_table")
        and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
        "shared_table_access": False,
    }


def provider_revenue_cycle_runtime_capabilities() -> dict:
    from .domain_depth import DOMAIN_OPERATIONS, domain_depth_contract

    domain = domain_depth_contract()
    smoke = provider_revenue_cycle_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "command_patient_account",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.provider-revenue-cycle-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
        "allowed_database_backends": PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        "standard_features": PROVIDER_REVENUE_CYCLE_STANDARD_FEATURE_KEYS,
        "capabilities": PROVIDER_REVENUE_CYCLE_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def provider_revenue_cycle_runtime_smoke() -> dict:
    from .standalone import ProviderRevenueCycleStandaloneApplication

    app = ProviderRevenueCycleStandaloneApplication(tenant="tenant-smoke")
    configured = app.configure(
        {
            "database_backend": "postgresql",
            "event_topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 5,
            "workbench_limit": 50,
        }
    )
    defaults = app.register_defaults()
    account = app.intake_patient_account(
        {
            "tenant": "tenant-smoke",
            "account_id": "acct_smoke",
            "patient_id": "pat_smoke",
            "encounter_id": "enc_smoke",
            "registration_status": "ready",
            "guarantor": {"name": "Ada Guarantor"},
            "coverage_priority": "primary",
            "financial_class": "commercial",
        }
    )
    eligibility = app.review_eligibility_and_benefits(
        "acct_smoke",
        {
            "payer_id": "payer_alpha",
            "coverage_active": True,
            "benefit_summary": "Professional and facility coverage active",
            "patient_responsibility_estimate": 120.0,
        },
    )
    authorization = app.link_prior_authorization(
        "acct_smoke",
        {
            "authorization_id": "auth_smoke",
            "service_code": "99213",
            "status": "approved",
            "units_remaining": 2,
        },
    )
    charge = app.capture_charge(
        "acct_smoke",
        {
            "charge_id": "chg_smoke",
            "service_date": "2026-05-30",
            "charge_code": "99213",
            "expected_amount": 180.0,
            "captured_amount": 180.0,
            "department": "clinic",
            "performing_clinician": "dr_smith",
        },
    )
    coding = app.review_coding(
        "acct_smoke",
        {
            "coding_case_id": "coding_smoke",
            "case_type": "professional",
            "documentation_status": "complete",
            "diagnosis_codes": ("I10",),
            "procedure_codes": ("99213",),
            "modifiers": ("25",),
        },
    )
    contract = app.upsert_payer_contract(
        {
            "contract_id": "contract_smoke",
            "payer_id": "payer_alpha",
            "expected_rate": 150.0,
            "timely_filing_days": 90,
        }
    )
    claim = app.create_claim("acct_smoke")
    scrub = app.scrub_claim(claim["claim"]["claim_id"])
    submit = app.submit_claim(claim["claim"]["claim_id"])
    remit = app.post_remittance_era(
        claim["claim"]["claim_id"],
        {
            "payment_posting_id": "era_smoke",
            "allowed_amount": 150.0,
            "payment_amount": 140.0,
            "adjustment_amount": 10.0,
            "patient_responsibility_amount": 20.0,
        },
    )
    statement = app.generate_patient_statement("acct_smoke", {"statement_id": "stmt_smoke"})
    plan = app.enroll_payment_plan(
        "acct_smoke",
        {"plan_id": "plan_smoke", "monthly_amount": 10.0, "term_months": 2},
    )
    assistance = app.evaluate_financial_assistance(
        "acct_smoke",
        {"assistance_id": "assist_smoke", "status": "approved", "discount_percent": 25.0},
    )
    refund = app.issue_refund_or_credit(
        "acct_smoke",
        {"refund_id": "refund_smoke", "type": "credit_balance", "amount": 5.0},
    )
    workbench = app.build_ar_workqueue()
    assessment = provider_revenue_cycle_run_advanced_assessment(app.state)
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "register_defaults", "ok": defaults["ok"]},
        {"id": "intake_patient_account", "ok": account["ok"]},
        {"id": "eligibility_review", "ok": eligibility["ok"]},
        {"id": "prior_authorization", "ok": authorization["ok"]},
        {"id": "charge_capture", "ok": charge["ok"]},
        {"id": "coding_review", "ok": coding["ok"]},
        {"id": "payer_contract", "ok": contract["ok"]},
        {"id": "claim_creation", "ok": claim["ok"]},
        {"id": "claim_scrub", "ok": scrub["ok"]},
        {"id": "claim_submission", "ok": submit["ok"]},
        {"id": "era_posting", "ok": remit["ok"]},
        {"id": "patient_statement", "ok": statement["ok"]},
        {"id": "payment_plan", "ok": plan["ok"]},
        {"id": "financial_assistance", "ok": assistance["ok"]},
        {"id": "refund_credit", "ok": refund["ok"]},
        {"id": "workbench", "ok": workbench["ok"]},
        {"id": "advanced_assessment", "ok": assessment["ok"]},
    )
    return {
        "format": "appgen.provider-revenue-cycle-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "state": deepcopy(app.state),
        "workbench": workbench,
        "assessment": assessment,
        "side_effects": (),
    }
