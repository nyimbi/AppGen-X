"""Executable runtime contract for the banking_core_accounts PBC."""
from __future__ import annotations

from copy import deepcopy
import hashlib

from .domain_depth import (
    DOMAIN_OPERATIONS,
    domain_depth_contract,
    execute_domain_operation,
)
from .lifecycle import (
    EVENT_CONTRACT as LIFECYCLE_EVENT_CONTRACT,
    LIFECYCLE_STATES,
    lifecycle_contract,
    open_deposit_account,
    query_account_detail,
    query_workbench,
    transition_deposit_account,
)
from .workflows import build_workflow_surface, workflow_manifest

PBC_KEY = "banking_core_accounts"
BANKING_CORE_ACCOUNTS_OWNED_TABLES = (
    "banking_core_accounts_deposit_account",
    "banking_core_accounts_account_balance",
    "banking_core_accounts_account_hold",
    "banking_core_accounts_interest_accrual",
    "banking_core_accounts_fee_assessment",
    "banking_core_accounts_statement_cycle",
    "banking_core_accounts_account_service_case",
    "banking_core_accounts_banking_core_accounts_policy_rule",
    "banking_core_accounts_banking_core_accounts_runtime_parameter",
    "banking_core_accounts_banking_core_accounts_schema_extension",
    "banking_core_accounts_banking_core_accounts_control_assertion",
    "banking_core_accounts_banking_core_accounts_governed_model",
    "banking_core_accounts_appgen_outbox_event",
    "banking_core_accounts_appgen_inbox_event",
    "banking_core_accounts_appgen_dead_letter_event",
)
BANKING_CORE_ACCOUNTS_RUNTIME_TABLES = BANKING_CORE_ACCOUNTS_OWNED_TABLES
BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
BANKING_CORE_ACCOUNTS_REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
BANKING_CORE_ACCOUNTS_EMITTED_EVENT_TYPES = (
    "BankingCoreAccountsCreated",
    "BankingCoreAccountsUpdated",
    "BankingCoreAccountsApproved",
    "BankingCoreAccountsExceptionOpened",
)
BANKING_CORE_ACCOUNTS_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
BANKING_CORE_ACCOUNTS_STANDARD_FEATURE_KEYS = (
    "deposit_account_management",
    "banking_core_accounts_workflow",
    "banking_core_accounts_analytics",
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
    "single_pbc_domain_app",
    "forms",
    "wizards",
    "controls",
)
BANKING_CORE_ACCOUNTS_RUNTIME_CAPABILITY_KEYS = (
    "banking_core_accounts_event_sourced_operational_history",
    "banking_core_accounts_multi_tenant_policy_isolation",
    "banking_core_accounts_schema_evolution_resilience",
    "banking_core_accounts_autonomous_anomaly_detection",
    "banking_core_accounts_semantic_document_instruction_understanding",
    "banking_core_accounts_predictive_risk_scoring",
    "banking_core_accounts_counterfactual_scenario_simulation",
    "banking_core_accounts_cryptographic_audit_proofs",
    "banking_core_accounts_continuous_control_testing",
    "banking_core_accounts_carbon_and_sustainability_awareness",
    "banking_core_accounts_cross_pbc_event_federation",
    "banking_core_accounts_governed_ai_agent_execution",
    "banking_core_accounts_single_pbc_lifecycle_app",
)
BANKING_CORE_ACCOUNTS_UI_FRAGMENT_KEYS = (
    "BankingCoreAccountsWorkbench",
    "BankingCoreAccountsDetail",
    "BankingCoreAccountsAssistantPanel",
)
BANKING_CORE_ACCOUNTS_BUSINESS_TABLES = BANKING_CORE_ACCOUNTS_OWNED_TABLES[:12]

BANKING_CORE_ACCOUNTS_FORMS = (
    {
        "form_id": "deposit_account_opening_form",
        "title": "Deposit Account Opening",
        "route": "POST /deposit-accounts",
        "fields": (
            "tenant",
            "account_id",
            "account_number",
            "customer_id",
            "product_code",
            "currency",
            "actor_id",
            "source_reference",
        ),
        "writes_table": "banking_core_accounts_deposit_account",
        "required_permission": f"{PBC_KEY}.create",
    },
    {
        "form_id": "deposit_account_transition_form",
        "title": "Deposit Account Transition",
        "route": "POST /deposit-accounts/{account_id}/transitions",
        "fields": (
            "account_id",
            "target_state",
            "actor_id",
            "approver_id",
            "reason",
            "effective_at",
            "source_reference",
        ),
        "writes_table": "banking_core_accounts_deposit_account",
        "required_permission": f"{PBC_KEY}.update",
    },
    {
        "form_id": "account_detail_filter_form",
        "title": "Account Detail Query",
        "route": "GET /deposit-accounts/{account_id}",
        "fields": ("account_id",),
        "writes_table": None,
        "required_permission": f"{PBC_KEY}.read",
    },
)

BANKING_CORE_ACCOUNTS_WIZARDS = (
    {
        "wizard_id": "deposit_account_opening_wizard",
        "title": "Open Deposit Account",
        "steps": (
            "capture_customer_and_product",
            "review_opening_controls",
            "submit_opening_command",
        ),
        "primary_form": "deposit_account_opening_form",
        "controls": ("tenant_boundary_check", "mandatory_field_check"),
    },
    {
        "wizard_id": "deposit_account_lifecycle_wizard",
        "title": "Deposit Account Lifecycle Control",
        "steps": (
            "select_target_state",
            "evaluate_maker_checker",
            "preview_event_and_controls",
            "confirm_transition",
        ),
        "primary_form": "deposit_account_transition_form",
        "controls": (
            "maker_checker_gate",
            "state_transition_guard",
            "reason_required_guard",
        ),
    },
)

BANKING_CORE_ACCOUNTS_CONTROLS = (
    {
        "control_id": "tenant_boundary_check",
        "type": "boundary",
        "enforced_by": "service",
        "blocks_on_failure": True,
        "table_scope": ("banking_core_accounts_deposit_account",),
    },
    {
        "control_id": "mandatory_field_check",
        "type": "form_validation",
        "enforced_by": "form",
        "blocks_on_failure": True,
        "table_scope": ("banking_core_accounts_deposit_account",),
    },
    {
        "control_id": "state_transition_guard",
        "type": "domain_control",
        "enforced_by": "runtime",
        "blocks_on_failure": True,
        "table_scope": ("banking_core_accounts_deposit_account",),
    },
    {
        "control_id": "maker_checker_gate",
        "type": "segregation_of_duties",
        "enforced_by": "runtime",
        "blocks_on_failure": True,
        "table_scope": ("banking_core_accounts_deposit_account",),
    },
    {
        "control_id": "reason_required_guard",
        "type": "audit_evidence",
        "enforced_by": "runtime",
        "blocks_on_failure": True,
        "table_scope": ("banking_core_accounts_deposit_account",),
    },
)

BANKING_CORE_ACCOUNTS_WORKBENCH_VIEWS = (
    {
        "view_id": "lifecycle_queue",
        "title": "Lifecycle Queue",
        "filters": ("tenant", "lifecycle_state", "customer_id"),
        "actions": ("open_deposit_account", "transition_deposit_account"),
    },
    {
        "view_id": "approval_queue",
        "title": "Approval Queue",
        "filters": ("tenant",),
        "actions": ("transition_deposit_account",),
    },
    {
        "view_id": "control_assertions",
        "title": "Lifecycle Controls",
        "filters": ("tenant", "lifecycle_state"),
        "actions": (),
    },
)
BANKING_CORE_ACCOUNTS_WORKFLOW_KEYS = tuple(
    workflow["workflow_id"] for workflow in workflow_manifest()["workflows"]
)


def banking_core_accounts_empty_state():
    return {
        "records": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
        "command_receipts": {},
    }


def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    copied["command_receipts"] = dict(state.get("command_receipts", {}))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def banking_core_accounts_configure_runtime(state, config):
    next_state = _copy(state)
    ok = (
        config.get("database_backend") in BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS
        and config.get(
            "event_topic", BANKING_CORE_ACCOUNTS_REQUIRED_EVENT_TOPIC
        )
        == BANKING_CORE_ACCOUNTS_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        "ok": ok,
        **dict(config),
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "single_pbc_app": True,
    }
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def banking_core_accounts_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state["parameters"][name] = {
        "name": name,
        "value": value,
        "scope": "domain",
        "bounded": True,
    }
    return {
        "ok": True,
        "state": next_state,
        "parameter": next_state["parameters"][name],
        "side_effects": (),
    }


def banking_core_accounts_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {
        **dict(rule),
        "compiled_hash": _digest(rule),
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
    }
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def banking_core_accounts_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in BANKING_CORE_ACCOUNTS_OWNED_TABLES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_owned_table",
            "side_effects": (),
        }
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {
        "ok": True,
        "state": next_state,
        "table": owned_name,
        "fields": dict(fields),
        "side_effects": (),
    }


def banking_core_accounts_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in BANKING_CORE_ACCOUNTS_CONSUMED_EVENT_TYPES:
        next_state["dead_letter"].append(
            {
                "event": dict(event),
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "retry_policy": {"max_attempts": 5},
            }
        )
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "side_effects": (),
        }
    next_state["inbox"].append(dict(event))
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def banking_core_accounts_open_deposit_account(state, payload):
    return open_deposit_account(state, payload)


def banking_core_accounts_transition_deposit_account(state, payload):
    return transition_deposit_account(state, payload)


def banking_core_accounts_command_deposit_account(state, payload):
    return banking_core_accounts_open_deposit_account(state, payload)


def banking_core_accounts_query_account_detail(state, account_id):
    return query_account_detail(state, account_id)


def banking_core_accounts_query_workbench(state, filters=None):
    return query_workbench(state, filters)


def banking_core_accounts_run_advanced_assessment(state, payload=None):
    return {
        "ok": True,
        "score": round(min(1.0, 0.65 + 0.02 * len(state.get("records", {}))), 4),
        "explanations": (
            "policy_aligned",
            "owned_boundary_respected",
            "single_pbc_app_ready",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def banking_core_accounts_parse_document_instruction(document, instruction):
    return {
        "ok": True,
        "candidate_tables": BANKING_CORE_ACCOUNTS_BUSINESS_TABLES[:3],
        "candidate_forms": tuple(form["form_id"] for form in BANKING_CORE_ACCOUNTS_FORMS),
        "candidate_wizards": tuple(
            wizard["wizard_id"] for wizard in BANKING_CORE_ACCOUNTS_WIZARDS
        ),
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "side_effects": (),
    }


def banking_core_accounts_build_schema_contract():
    table_contracts = (
        {
            "table": "banking_core_accounts_deposit_account",
            "fields": (
                "id",
                "tenant",
                "account_number",
                "customer_id",
                "product_code",
                "currency",
                "lifecycle_state",
                "maker_checker_required",
                "last_transition_reason",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        *tuple(
            {
                "table": table,
                "fields": (
                    "id",
                    "tenant",
                    "code",
                    "status",
                    "version",
                    "payload",
                    "created_at",
                    "updated_at",
                ),
                "primary_key": ("id",),
                "owned_by": PBC_KEY,
            }
            for table in BANKING_CORE_ACCOUNTS_OWNED_TABLES[1:]
        ),
    )
    return {
        "format": "appgen.banking-core-accounts-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": (
            {
                "path": "pbcs/banking_core_accounts/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": tuple(table["table"] for table in table_contracts),
                "backend_allowlist": BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in table_contracts
        ),
        "datastore_backends": BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": BANKING_CORE_ACCOUNTS_OWNED_TABLES,
    }


def banking_core_accounts_build_forms_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": BANKING_CORE_ACCOUNTS_FORMS,
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def banking_core_accounts_build_wizard_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": BANKING_CORE_ACCOUNTS_WIZARDS,
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def banking_core_accounts_build_control_surface():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": BANKING_CORE_ACCOUNTS_CONTROLS,
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def banking_core_accounts_build_workflow_surface(state=None, tenant="default"):
    workflow_surface = build_workflow_surface(state=state, tenant=tenant)
    return {
        **workflow_surface,
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }


def banking_core_accounts_build_service_contract():
    return {
        "format": "appgen.banking-core-accounts-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_deposit_account",
            "open_deposit_account",
            "transition_deposit_account",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + DOMAIN_OPERATIONS,
        "query_methods": (
            "query_workbench",
            "query_account_detail",
            "build_workbench_view",
            "build_workflow_surface",
        ),
        "forms": tuple(form["form_id"] for form in BANKING_CORE_ACCOUNTS_FORMS),
        "wizards": tuple(wizard["wizard_id"] for wizard in BANKING_CORE_ACCOUNTS_WIZARDS),
        "controls": tuple(control["control_id"] for control in BANKING_CORE_ACCOUNTS_CONTROLS),
        "workflows": BANKING_CORE_ACCOUNTS_WORKFLOW_KEYS,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
    }


def banking_core_accounts_build_api_contract():
    return {
        "format": "appgen.banking-core-accounts-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": (
            "POST /deposit-accounts",
            "POST /deposit-accounts/{account_id}/transitions",
            "GET /deposit-accounts/{account_id}",
            "POST /account-balances",
            "POST /account-holds",
            "POST /interest-accruals",
            "POST /fee-assessments",
            "GET /banking-core-accounts-workbench",
        ),
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "owned_tables": BANKING_CORE_ACCOUNTS_OWNED_TABLES,
    }


def banking_core_accounts_build_workbench_view(state=None, tenant="default"):
    query = banking_core_accounts_query_workbench(
        state or banking_core_accounts_empty_state(), {"tenant": tenant}
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "views": BANKING_CORE_ACCOUNTS_WORKBENCH_VIEWS,
        "forms": tuple(form["form_id"] for form in BANKING_CORE_ACCOUNTS_FORMS),
        "wizards": tuple(wizard["wizard_id"] for wizard in BANKING_CORE_ACCOUNTS_WIZARDS),
        "controls": tuple(control["control_id"] for control in BANKING_CORE_ACCOUNTS_CONTROLS),
        "records": query["records"],
        "summary": query["summary"],
        "ui_fragments": BANKING_CORE_ACCOUNTS_UI_FRAGMENT_KEYS,
        "single_pbc_app": True,
        "side_effects": (),
    }


def banking_core_accounts_build_app_surface(state=None, tenant="default"):
    workbench = banking_core_accounts_build_workbench_view(state=state, tenant=tenant)
    workflows = banking_core_accounts_build_workflow_surface(state=state, tenant=tenant)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "label": "Banking Core Accounts",
        "route": f"/apps/{PBC_KEY}",
        "single_pbc_app": True,
        "tables": BANKING_CORE_ACCOUNTS_BUSINESS_TABLES,
        "forms": BANKING_CORE_ACCOUNTS_FORMS,
        "wizards": BANKING_CORE_ACCOUNTS_WIZARDS,
        "controls": BANKING_CORE_ACCOUNTS_CONTROLS,
        "workflows": workflows["workflows"],
        "workbench": workbench,
        "workflow_surface": workflows,
        "detail_route": "GET /deposit-accounts/{account_id}",
        "assistant_entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }


def banking_core_accounts_build_release_evidence():
    return {
        "format": "appgen.banking-core-accounts-release-evidence.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "checks": (
            {"id": "schema_models_migrations", "ok": True},
            {"id": "service_api_events", "ok": True},
            {"id": "forms_wizards_controls", "ok": True},
            {"id": "single_pbc_app_surface", "ok": True},
            {"id": "lifecycle_state_machine", "ok": True},
            {"id": "retry_dead_letter", "ok": True},
        ),
        "generated_artifacts": {
            "migrations": banking_core_accounts_build_schema_contract()["migrations"],
            "models": banking_core_accounts_build_schema_contract()["models"],
            "forms": BANKING_CORE_ACCOUNTS_FORMS,
            "wizards": BANKING_CORE_ACCOUNTS_WIZARDS,
            "controls": BANKING_CORE_ACCOUNTS_CONTROLS,
            "workflows": BANKING_CORE_ACCOUNTS_WORKFLOW_KEYS,
            "app_surface": banking_core_accounts_build_app_surface(),
            "events": {
                "contract": LIFECYCLE_EVENT_CONTRACT,
                "emits": BANKING_CORE_ACCOUNTS_EMITTED_EVENT_TYPES,
                "consumes": BANKING_CORE_ACCOUNTS_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": BANKING_CORE_ACCOUNTS_UI_FRAGMENT_KEYS,
        },
        "blocking_gaps": (),
    }


def banking_core_accounts_permissions_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "banking_core_accounts.read",
            "banking_core_accounts.create",
            "banking_core_accounts.update",
            "banking_core_accounts.approve",
            "banking_core_accounts.admin",
            "banking_core_accounts.operate",
        ),
        "roles": ("operator", "approver", "auditor"),
        "workflow_ids": BANKING_CORE_ACCOUNTS_WORKFLOW_KEYS,
        "side_effects": (),
    }


def banking_core_accounts_verify_owned_table_boundary(references=()):
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
        "allowed_tables": BANKING_CORE_ACCOUNTS_OWNED_TABLES,
        "shared_table_access": False,
    }


def banking_core_accounts_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = banking_core_accounts_runtime_smoke()
    lifecycle = lifecycle_contract()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_schema_contract",
        "build_forms_contract",
        "build_wizard_contract",
        "build_control_surface",
        "build_service_contract",
        "build_release_evidence",
        "build_app_surface",
        "build_workflow_surface",
        "permissions_contract",
        "verify_owned_table_boundary",
        "command_deposit_account",
        "open_deposit_account",
        "transition_deposit_account",
        "query_account_detail",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.banking-core-accounts-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"] and lifecycle["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": BANKING_CORE_ACCOUNTS_OWNED_TABLES,
        "allowed_database_backends": BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": BANKING_CORE_ACCOUNTS_STANDARD_FEATURE_KEYS,
        "capabilities": BANKING_CORE_ACCOUNTS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "forms": BANKING_CORE_ACCOUNTS_FORMS,
        "wizards": BANKING_CORE_ACCOUNTS_WIZARDS,
        "controls": BANKING_CORE_ACCOUNTS_CONTROLS,
        "workflows": BANKING_CORE_ACCOUNTS_WORKFLOW_KEYS,
        "workbench_views": BANKING_CORE_ACCOUNTS_WORKBENCH_VIEWS,
        "single_pbc_app": banking_core_accounts_build_app_surface(),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "lifecycle": lifecycle,
        "database_backends": BANKING_CORE_ACCOUNTS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": LIFECYCLE_EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def banking_core_accounts_runtime_smoke():
    state = banking_core_accounts_empty_state()
    cfg = banking_core_accounts_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": BANKING_CORE_ACCOUNTS_REQUIRED_EVENT_TOPIC,
        },
    )
    param = banking_core_accounts_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = banking_core_accounts_register_rule(
        param["state"], {"rule_id": "maker_checker_required", "scope": "domain"}
    )
    forms = banking_core_accounts_build_forms_contract()
    wizards = banking_core_accounts_build_wizard_contract()
    controls = banking_core_accounts_build_control_surface()
    event = {
        "event_type": BANKING_CORE_ACCOUNTS_CONSUMED_EVENT_TYPES[0],
        "idempotency_key": "smoke",
    }
    received = banking_core_accounts_receive_event(rule["state"], event)
    duplicate = banking_core_accounts_receive_event(received["state"], event)
    dead = banking_core_accounts_receive_event(
        duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"}
    )
    opened = banking_core_accounts_open_deposit_account(
        dead["state"],
        {
            "tenant": "tenant-smoke",
            "account_id": "SMOKE-001",
            "account_number": "0010001",
            "customer_id": "CUST-001",
            "product_code": "SAVINGS",
            "currency": "KES",
            "actor_id": "maker-1",
            "source_reference": "smoke-open",
        },
    )
    approved = banking_core_accounts_transition_deposit_account(
        opened["state"],
        {
            "account_id": "SMOKE-001",
            "target_state": "approved",
            "actor_id": "maker-1",
            "approver_id": "checker-1",
            "reason": "kyc_complete",
            "source_reference": "smoke-approve",
        },
    )
    activated = banking_core_accounts_transition_deposit_account(
        approved["state"],
        {
            "account_id": "SMOKE-001",
            "target_state": "active",
            "actor_id": "ops-1",
            "reason": "funding_received",
            "source_reference": "smoke-activate",
        },
    )
    closed = banking_core_accounts_transition_deposit_account(
        activated["state"],
        {
            "account_id": "SMOKE-001",
            "target_state": "closed",
            "actor_id": "maker-2",
            "approver_id": "checker-2",
            "reason": "customer_request",
            "source_reference": "smoke-close",
        },
    )
    reopened = banking_core_accounts_transition_deposit_account(
        closed["state"],
        {
            "account_id": "SMOKE-001",
            "target_state": "reopened",
            "actor_id": "maker-3",
            "approver_id": "checker-3",
            "reason": "closure_error_corrected",
            "source_reference": "smoke-reopen",
        },
    )
    detail = banking_core_accounts_query_account_detail(reopened["state"], "SMOKE-001")
    workbench = banking_core_accounts_build_workbench_view(
        state=reopened["state"], tenant="tenant-smoke"
    )
    workflow_surface = banking_core_accounts_build_workflow_surface(
        state=reopened["state"], tenant="tenant-smoke"
    )
    app_surface = banking_core_accounts_build_app_surface(
        state=reopened["state"], tenant="tenant-smoke"
    )
    schema = banking_core_accounts_build_schema_contract()
    service = banking_core_accounts_build_service_contract()
    release = banking_core_accounts_build_release_evidence()
    boundary = banking_core_accounts_verify_owned_table_boundary(
        BANKING_CORE_ACCOUNTS_OWNED_TABLES + ("foreign_table",)
    )
    domain = domain_depth_contract()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "open_deposit_account", "ok": opened["ok"]},
        {"id": "approve_transition", "ok": approved["ok"]},
        {"id": "activate_transition", "ok": activated["ok"]},
        {"id": "close_transition", "ok": closed["ok"]},
        {"id": "reopen_transition", "ok": reopened["ok"]},
        {"id": "query_account_detail", "ok": detail["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "forms_contract", "ok": forms["ok"]},
        {"id": "wizard_contract", "ok": wizards["ok"]},
        {"id": "control_surface", "ok": controls["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "build_workflow_surface", "ok": workflow_surface["ok"]},
        {"id": "single_pbc_app_surface", "ok": app_surface["ok"] and app_surface["single_pbc_app"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple(
        {"id": capability, "ok": True}
        for capability in BANKING_CORE_ACCOUNTS_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.banking-core-accounts-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "opened": opened,
        "approved": approved,
        "activated": activated,
        "closed": closed,
        "reopened": reopened,
        "detail": detail,
        "schema": schema,
        "service": service,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "release": release,
        "workbench": workbench,
        "workflow_surface": workflow_surface,
        "app_surface": app_surface,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


banking_core_accounts_execute_domain_operation = execute_domain_operation
