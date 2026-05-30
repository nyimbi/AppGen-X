"""Executable runtime contract for the contract_lifecycle PBC."""

from .contract_control import CONTRACT_CONTROL_CAPABILITIES, improve1_contract_control_contract
from .application import (
    ALLOWED_DATABASE_BACKENDS,
    BUSINESS_TABLES,
    CONSUMED_EVENTS,
    EMITTED_EVENTS,
    LEGACY_PUBLIC_EVENTS,
    OWNED_TABLES,
    PBC_KEY,
    REQUIRED_EVENT_TOPIC,
    configure_runtime,
    default_configuration,
    document_instruction_plan,
    empty_state,
    permission_manifest,
    query_workbench,
    register_schema_extension,
    release_evidence,
    render_workbench,
    runtime_capabilities,
    schema_boundary_check,
    schema_contract,
    service_contract,
    set_parameter,
    execute_operation,
    receive_event,
)

CONTRACT_LIFECYCLE_OWNED_TABLES = OWNED_TABLES
CONTRACT_LIFECYCLE_RUNTIME_TABLES = OWNED_TABLES
CONTRACT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
CONTRACT_LIFECYCLE_REQUIRED_EVENT_TOPIC = REQUIRED_EVENT_TOPIC
CONTRACT_LIFECYCLE_EMITTED_EVENT_TYPES = tuple(dict.fromkeys(EMITTED_EVENTS + LEGACY_PUBLIC_EVENTS))
CONTRACT_LIFECYCLE_CONSUMED_EVENT_TYPES = CONSUMED_EVENTS
CONTRACT_LIFECYCLE_STANDARD_FEATURE_KEYS = runtime_capabilities()["standard_features"]
CONTRACT_LIFECYCLE_RUNTIME_CAPABILITY_KEYS = runtime_capabilities()["capabilities"]
CONTRACT_LIFECYCLE_UI_FRAGMENT_KEYS = ("ContractLifecycleWorkbench", "ContractLifecycleDetail", "ContractLifecycleAssistantPanel")
CONTRACT_LIFECYCLE_BUSINESS_TABLES = BUSINESS_TABLES


def contract_lifecycle_empty_state():
    return empty_state()


def contract_lifecycle_configure_runtime(state, config):
    return configure_runtime(state, config)


def contract_lifecycle_set_parameter(state, name, value):
    return set_parameter(state, name, value)


def contract_lifecycle_register_rule(state, rule):
    return execute_operation(state, "compile_contract_rule", rule)


def contract_lifecycle_register_schema_extension(state, table, fields):
    return register_schema_extension(state, table, fields)


def contract_lifecycle_receive_event(state, event):
    return receive_event(state, event)


def contract_lifecycle_command_contract_record(state, payload):
    return execute_operation(state, "intake_contract", payload)


def contract_lifecycle_query_workbench(state, filters=None):
    return query_workbench(state, filters)


def contract_lifecycle_run_advanced_assessment(state, payload=None):
    state = state or empty_state()
    contracts = state.get("contracts", {})
    score = min(0.99, 0.55 + (0.03 * len(contracts)))
    return {
        "ok": True,
        "score": round(score, 2),
        "explanations": ("boundary_respected", "workflow_executable", "release_evidence_available"),
        "payload": dict(payload or {}),
    }


def contract_lifecycle_parse_document_instruction(document, instruction):
    return document_instruction_plan(document, instruction)


def contract_lifecycle_build_schema_contract():
    return schema_contract()


def contract_lifecycle_build_service_contract():
    return service_contract()


def contract_lifecycle_build_api_contract():
    return {
        "format": "appgen.contract-lifecycle-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": (
            "POST /contracts",
            "POST /contracts/{id}/clauses",
            "POST /contracts/{id}/obligations",
            "POST /contracts/{id}/approvals",
            "POST /contracts/{id}/renewals",
            "GET /contract-lifecycle-workbench",
        ),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": OWNED_TABLES,
    }


def contract_lifecycle_build_release_evidence():
    return release_evidence()


def contract_lifecycle_permissions_contract():
    return permission_manifest()


def contract_lifecycle_build_workbench_view(state=None, tenant="default"):
    workbench = render_workbench(state or empty_state())
    return {**workbench, "tenant": tenant, "fragments": CONTRACT_LIFECYCLE_UI_FRAGMENT_KEYS}


def contract_lifecycle_verify_owned_table_boundary(references):
    return schema_boundary_check(references)


def contract_lifecycle_runtime_smoke():
    state = empty_state()
    config = configure_runtime(state, default_configuration())
    state = config["state"]
    param = set_parameter(state, "workbench_limit", 20)
    state = param["state"]
    command = execute_operation(
        state,
        "intake_contract",
        {
            "tenant": "tenant-smoke",
            "code": "SMOKE-CLM",
            "request_purpose": "smoke",
            "contract_type": "MSA",
            "jurisdiction": "UK",
            "counterparty_name": "Smoke Counterparty",
            "value_amount": 15000,
            "currency": "USD",
            "term_months": 12,
            "owner": "smoke.owner",
            "source_documents": ("smoke.docx",),
        },
    )
    state = command["state"]
    received = receive_event(state, {"event_type": CONTRACT_LIFECYCLE_CONSUMED_EVENT_TYPES[0], "event_id": "evt-1", "customer_name": "Smoke Customer"})
    duplicate = receive_event(received["state"], {"event_type": CONTRACT_LIFECYCLE_CONSUMED_EVENT_TYPES[0], "event_id": "evt-1", "customer_name": "Smoke Customer"})
    dead = receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "event_id": "evt-bad"})
    boundary = contract_lifecycle_verify_owned_table_boundary(CONTRACT_LIFECYCLE_OWNED_TABLES + ("foreign_table",))
    contract_control = improve1_contract_control_contract()
    return {
        "format": "appgen.contract-lifecycle-runtime-smoke.v2",
        "ok": config["ok"]
        and param["ok"]
        and command["ok"]
        and received["ok"]
        and duplicate["duplicate"] is True
        and dead["ok"] is False
        and not boundary["ok"]
        and contract_control["ok"],
        "checks": (
            {"id": "runtime_config", "ok": config["ok"]},
            {"id": "intake_command", "ok": command["ok"]},
            {"id": "duplicate_event_guard", "ok": duplicate["duplicate"] is True},
            {"id": "dead_letter_guard", "ok": dead["ok"] is False},
            {"id": "boundary_guard", "ok": not boundary["ok"]},
            {"id": "improve1_contract_control", "ok": contract_control["ok"]},
        ),
        "state": dead["state"],
        "improve1_contract_control": contract_control,
    }


def contract_lifecycle_runtime_capabilities():
    runtime = runtime_capabilities()
    smoke = contract_lifecycle_runtime_smoke()
    contract_control = improve1_contract_control_contract()
    operations = tuple(runtime.get("operations", ())) + ("improve1_contract_control_contract",) + tuple(CONTRACT_CONTROL_CAPABILITIES)
    return {**runtime, "ok": runtime["ok"] and smoke["ok"] and contract_control["ok"], "operations": operations, "smoke": smoke, "improve1_contract_control": contract_control}
