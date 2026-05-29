"""Standalone application surface for the revenue_recognition PBC."""

from __future__ import annotations

from .runtime import (
    PBC_KEY,
    REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS,
    REVENUE_RECOGNITION_BUSINESS_TABLES,
    REVENUE_RECOGNITION_OWNED_TABLES,
    REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC,
    REVENUE_RECOGNITION_RUNTIME_CAPABILITY_KEYS,
    REVENUE_RECOGNITION_STANDARD_FEATURE_KEYS,
    revenue_recognition_build_api_contract,
    revenue_recognition_build_schema_contract,
    revenue_recognition_build_service_contract,
    revenue_recognition_build_workbench_view,
    revenue_recognition_parse_document_instruction,
    revenue_recognition_runtime_capabilities,
)

REVENUE_RECOGNITION_FORMS = (
    {
        "id": "revenue_contract_form",
        "title": "Revenue Contract Intake",
        "fields": ("tenant", "code", "customer_account", "contract_date", "currency", "transaction_price", "accounting_standard"),
        "submit_operation": "command_revenue_contract",
        "target_table": "revenue_recognition_revenue_contract",
    },
    {
        "id": "performance_obligation_form",
        "title": "Performance Obligation Identification",
        "fields": ("revenue_contract_id", "obligation_code", "distinct_good_or_service", "satisfaction_pattern", "ssp_basis"),
        "submit_operation": "identify_obligations",
        "target_table": "revenue_recognition_performance_obligation",
    },
    {
        "id": "allocation_form",
        "title": "Transaction Price Allocation",
        "fields": ("revenue_contract_id", "allocation_basis", "variable_consideration", "constraint_applied", "residual_method_reason"),
        "submit_operation": "allocate_transaction_price",
        "target_table": "revenue_recognition_transaction_price_allocation",
    },
    {
        "id": "satisfaction_event_form",
        "title": "Obligation Satisfaction Event",
        "fields": ("performance_obligation_id", "satisfaction_date", "measure", "evidence_uri", "recognition_amount"),
        "submit_operation": "record_satisfaction_event",
        "target_table": "revenue_recognition_revenue_event",
    },
    {
        "id": "revenue_schedule_form",
        "title": "Revenue Schedule",
        "fields": ("revenue_contract_id", "schedule_method", "start_date", "end_date", "periodicity", "hold_policy"),
        "submit_operation": "generate_revenue_schedule",
        "target_table": "revenue_recognition_revenue_schedule",
    },
    {
        "id": "close_disclosure_form",
        "title": "Close and Disclosure Evidence",
        "fields": ("period", "materiality_threshold", "disclosure_precision", "control_owner", "evidence_packet"),
        "submit_operation": "run_close_readiness_check",
        "target_table": "revenue_recognition_compliance_evidence",
    },
)

REVENUE_RECOGNITION_WIZARDS = (
    {
        "id": "asc606_ifrs15_contract_wizard",
        "title": "ASC 606 / IFRS 15 Contract Wizard",
        "steps": ("contract_scope", "obligations", "transaction_price", "allocation", "recognition_plan"),
        "terminal_operation": "generate_revenue_schedule",
    },
    {
        "id": "modification_assessment_wizard",
        "title": "Contract Modification Assessment",
        "steps": ("change_capture", "distinctness_assessment", "prospective_or_cumulative", "reallocation", "disclosure"),
        "terminal_operation": "process_contract_modification",
    },
    {
        "id": "continuous_close_wizard",
        "title": "Continuous Revenue Close Wizard",
        "steps": ("holds", "satisfaction_evidence", "journal_preview", "control_assertions", "disclosure_packet"),
        "terminal_operation": "run_close_readiness_check",
    },
)

REVENUE_RECOGNITION_CONTROLS = (
    {"id": "five_step_policy_gate", "title": "Five-Step Recognition Gate", "protects": "command_revenue_contract", "type": "policy_check"},
    {"id": "ssp_allocation_control", "title": "Standalone Selling Price Allocation Control", "protects": "allocate_transaction_price", "type": "calculation_review"},
    {"id": "variable_consideration_constraint", "title": "Variable Consideration Constraint", "protects": "estimate_variable_consideration", "type": "probability_guard"},
    {"id": "revenue_hold_release_control", "title": "Revenue Hold Release Control", "protects": "apply_revenue_hold", "type": "approval_gate"},
    {"id": "close_readiness_assertion", "title": "Close Readiness Assertion", "protects": "run_close_readiness_check", "type": "continuous_control"},
    {"id": "dead_letter_replay_console", "title": "Dead Letter Replay Console", "protects": "receive_event", "type": "ops_control"},
)


def revenue_recognition_forms_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": REVENUE_RECOGNITION_FORMS,
        "covered_operations": tuple(form["submit_operation"] for form in REVENUE_RECOGNITION_FORMS),
        "owned_tables": REVENUE_RECOGNITION_OWNED_TABLES,
        "writes_foreign_tables": False,
    }


def revenue_recognition_wizards_contract() -> dict:
    terminals = tuple(wizard["terminal_operation"] for wizard in REVENUE_RECOGNITION_WIZARDS)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": REVENUE_RECOGNITION_WIZARDS,
        "terminal_operations": terminals,
        "supports_five_step_model": "generate_revenue_schedule" in terminals,
        "supports_modifications_and_close": "process_contract_modification" in terminals and "run_close_readiness_check" in terminals,
    }


def revenue_recognition_controls_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": REVENUE_RECOGNITION_CONTROLS,
        "control_ids": tuple(control["id"] for control in REVENUE_RECOGNITION_CONTROLS),
        "database_backends": REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS,
        "event_topic": REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
    }


def standalone_seed_bundle() -> tuple[dict, ...]:
    return (
        {"table": "revenue_recognition_revenue_contract", "code": "REV-DEMO-SUBSCRIPTION", "status": "active", "payload": {"transaction_price": 120000, "currency": "USD", "standard": "ASC606"}},
        {"table": "revenue_recognition_performance_obligation", "code": "REV-DEMO-PO-SERVICE", "status": "identified", "payload": {"satisfaction_pattern": "over_time", "ssp": 90000}},
        {"table": "revenue_recognition_transaction_price_allocation", "code": "REV-DEMO-ALLOC", "status": "approved", "payload": {"method": "relative_ssp", "constraint_applied": True}},
        {"table": "revenue_recognition_revenue_schedule", "code": "REV-DEMO-SCHEDULE", "status": "open", "payload": {"periodicity": "monthly", "recognized_to_date": 0}},
        {"table": "revenue_recognition_recognition_policy", "code": "REV-DEMO-POLICY", "status": "compiled", "payload": {"policy": "five_step_recognition"}},
    )


def single_pbc_revenue_recognition_app_contract(state=None) -> dict:
    schema = revenue_recognition_build_schema_contract()
    service = revenue_recognition_build_service_contract()
    api = revenue_recognition_build_api_contract()
    runtime = revenue_recognition_runtime_capabilities()
    workbench = revenue_recognition_build_workbench_view(state=state)
    forms = revenue_recognition_forms_contract()
    wizards = revenue_recognition_wizards_contract()
    controls = revenue_recognition_controls_contract()
    return {
        "ok": all(item["ok"] for item in (schema, service, api, runtime, workbench, forms, wizards, controls))
        and len(standalone_seed_bundle()) >= 5,
        "pbc": PBC_KEY,
        "application_mode": "single_pbc_standalone",
        "owned_tables": runtime["owned_tables"],
        "schema": schema,
        "service": service,
        "api": api,
        "workbench": workbench,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "seed_data": standalone_seed_bundle(),
        "standard_features": REVENUE_RECOGNITION_STANDARD_FEATURE_KEYS,
        "advanced_capabilities": REVENUE_RECOGNITION_RUNTIME_CAPABILITY_KEYS,
        "dependency_boundary": {
            "writes_foreign_tables": False,
            "cross_pbc_dependencies": ("api", "event", "projection"),
            "event_contract": "AppGen-X",
        },
    }


def document_instruction_revenue_recognition_plan(document: str, instructions: str) -> dict:
    text = f"{document}\n{instructions}".lower()
    plan = revenue_recognition_parse_document_instruction(document, instructions)
    if "modification" in text:
        candidate_tables = ("revenue_recognition_contract_modification", "revenue_recognition_transaction_price_allocation")
    elif "schedule" in text or "recognize" in text:
        candidate_tables = ("revenue_recognition_revenue_schedule", "revenue_recognition_revenue_event")
    elif "hold" in text or "exception" in text:
        candidate_tables = ("revenue_recognition_compliance_evidence", "revenue_recognition_revenue_event")
    else:
        candidate_tables = tuple(plan.get("candidate_tables", REVENUE_RECOGNITION_BUSINESS_TABLES[:3]))
    return {
        **plan,
        "ok": plan["ok"] and all(table in REVENUE_RECOGNITION_OWNED_TABLES for table in candidate_tables),
        "candidate_tables": candidate_tables,
        "single_pbc_ready": True,
        "assistant_surface": "RevenueRecognitionAssistantPanel",
        "allowed_mutation_boundary": REVENUE_RECOGNITION_OWNED_TABLES,
    }


def standalone_route_contracts() -> tuple[dict, ...]:
    app_routes = (
        {"method": "GET", "path": "/revenue-recognition/app", "operation": "single_pbc_revenue_recognition_app_contract"},
        {"method": "GET", "path": "/revenue-recognition/forms", "operation": "revenue_recognition_forms_contract"},
        {"method": "GET", "path": "/revenue-recognition/wizards", "operation": "revenue_recognition_wizards_contract"},
        {"method": "GET", "path": "/revenue-recognition/controls", "operation": "revenue_recognition_controls_contract"},
    )
    return tuple(
        {
            **route,
            "pbc": PBC_KEY,
            "required_permission": "revenue_recognition.read",
            "idempotency_key": f"{PBC_KEY}:{route['method']}:{route['path']}",
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for route in app_routes
    )


def app_surface_smoke_test() -> dict:
    app = single_pbc_revenue_recognition_app_contract()
    instruction = document_instruction_revenue_recognition_plan(
        "Customer contract modification adds variable usage consideration and a revenue hold.",
        "create modification assessment, update allocation, and prepare close evidence",
    )
    route_paths = tuple(route["path"] for route in standalone_route_contracts())
    return {
        "ok": app["ok"] and instruction["ok"] and "/revenue-recognition/app" in route_paths,
        "app": app,
        "instruction": instruction,
        "route_paths": route_paths,
    }
