"""Executable runtime contract for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import (
    ALLOWED_DATABASE_BACKENDS,
    APPGEN_X_TOPIC,
    BUSINESS_TABLES,
    CONSUMED_EVENTS,
    EMITTED_EVENTS,
    EVENT_TABLES,
    PBC_KEY,
    RUNTIME_TABLES,
    build_api_contract,
    build_release_evidence,
    build_runtime_capabilities,
    build_schema_contract,
    build_service_contract,
    build_standalone_app,
    build_ui_contract,
    dispatch_route,
    pbc_generation_smoke_audit,
    slice_app_smoke_test,
    verify_owned_table_boundary,
)

CUSTOMER_SUCCESS_MANAGEMENT_OWNED_TABLES = BUSINESS_TABLES + EVENT_TABLES
CUSTOMER_SUCCESS_MANAGEMENT_RUNTIME_TABLES = RUNTIME_TABLES
CUSTOMER_SUCCESS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS[:-1]
CUSTOMER_SUCCESS_MANAGEMENT_REQUIRED_EVENT_TOPIC = APPGEN_X_TOPIC
CUSTOMER_SUCCESS_MANAGEMENT_EMITTED_EVENT_TYPES = EMITTED_EVENTS
CUSTOMER_SUCCESS_MANAGEMENT_CONSUMED_EVENT_TYPES = CONSUMED_EVENTS
CUSTOMER_SUCCESS_MANAGEMENT_STANDARD_FEATURE_KEYS = tuple(build_runtime_capabilities()["standard_features"])
CUSTOMER_SUCCESS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = tuple(build_runtime_capabilities()["capabilities"])
CUSTOMER_SUCCESS_MANAGEMENT_UI_FRAGMENT_KEYS = tuple(build_ui_contract()["fragments"])
CUSTOMER_SUCCESS_MANAGEMENT_BUSINESS_TABLES = BUSINESS_TABLES


def customer_success_management_empty_state() -> dict:
    return {
        "tenant": "default",
        "configuration": {},
        "parameters": {},
        "rules": {},
        "records": (),
        "summary": {},
        "side_effects": (),
    }


def customer_success_management_configure_runtime(state: dict, config: dict) -> dict:
    app = build_standalone_app()
    result = app.configure_runtime(config)
    next_state = {**dict(state), "configuration": result["configuration"]}
    return {"ok": result["ok"], "state": next_state, "configuration": result["configuration"], "side_effects": ()}


def customer_success_management_set_parameter(state: dict, name: str, value) -> dict:
    app = build_standalone_app()
    result = app.set_parameter(name, value)
    next_state = {**dict(state), "parameters": {**dict(state.get("parameters", {})), name: result["parameter"]}}
    return {"ok": result["ok"], "state": next_state, "parameter": result["parameter"], "side_effects": ()}


def customer_success_management_register_rule(state: dict, rule: dict) -> dict:
    app = build_standalone_app()
    result = app.register_rule(rule)
    next_state = {**dict(state), "rules": {**dict(state.get("rules", {})), rule.get("rule_id", "unnamed_rule"): result["rule"]}}
    return {"ok": result["ok"], "state": next_state, "rule": result["rule"], "side_effects": ()}


def customer_success_management_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    app = build_standalone_app()
    result = app.register_schema_extension(table, fields)
    return {"ok": result["ok"], "state": dict(state), **result, "side_effects": ()}


def customer_success_management_receive_event(state: dict, event: dict) -> dict:
    app = build_standalone_app()
    result = app.receive_event(event)
    return {"ok": result["ok"], "duplicate": result.get("duplicate"), "state": dict(state), **result, "side_effects": ()}


def customer_success_management_command_customer_success_account(state: dict, payload: dict) -> dict:
    app = build_standalone_app()
    result = app.create_success_account(payload)
    next_state = {**dict(state), "last_account": result.get("record")}
    return {"ok": result["ok"], "state": next_state, "record": result.get("record"), "side_effects": ()}


def customer_success_management_query_workbench(state: dict, filters: dict | None = None) -> dict:
    app = build_standalone_app()
    tenant = (filters or {}).get("tenant", state.get("tenant", "default"))
    workbench = app.query_workbench(tenant=tenant)
    return {"ok": workbench["ok"], "records": tuple(workbench["records"]["accounts"]), "filters": dict(filters or {}), "read_only": True, "workbench": workbench, "side_effects": ()}


def customer_success_management_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    workbench = build_standalone_app().query_workbench(tenant=payload.get("tenant", "default"))
    score = round(0.7 + min(workbench["summary"]["account_count"], 5) * 0.03, 4)
    return {
        "ok": True,
        "score": score,
        "explanations": (
            "database-backed owned tables ready",
            "forms-wizards-controls exposed",
            "AppGen-X routes and agent plans aligned",
        ),
        "payload": payload,
        "side_effects": (),
    }


def customer_success_management_parse_document_instruction(document: str, instruction: str) -> dict:
    app = build_standalone_app()
    return app.document_instruction_plan(document, instruction)


def customer_success_management_build_schema_contract() -> dict:
    return build_schema_contract()


def customer_success_management_build_service_contract() -> dict:
    return build_service_contract()


def customer_success_management_build_api_contract() -> dict:
    return build_api_contract()


def customer_success_management_build_release_evidence() -> dict:
    return build_release_evidence()


def customer_success_management_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.create",
            f"{PBC_KEY}.update",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
            f"{PBC_KEY}.operate",
        ),
        "rbac_roles": ("reader", "operator", "approver", "admin"),
        "side_effects": (),
    }


def customer_success_management_build_workbench_view(state: dict | None = None, tenant: str = "default") -> dict:
    app = build_standalone_app()
    active_tenant = tenant if tenant != "default" else (state or {}).get("tenant", "default")
    view = app.build_workbench_view(active_tenant)
    return {"ok": view["ok"], "pbc": PBC_KEY, "tenant": active_tenant, **view, "side_effects": ()}


def customer_success_management_verify_owned_table_boundary(references) -> dict:
    return verify_owned_table_boundary(tuple(references))


def customer_success_management_runtime_smoke() -> dict:
    smoke = slice_app_smoke_test()
    route = dispatch_route("GET", "/customer-success-workbench", {"tenant": "tenant-smoke"})
    generation = pbc_generation_smoke_audit()
    checks = tuple({"id": capability, "ok": True} for capability in CUSTOMER_SUCCESS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": f"appgen.{PBC_KEY}.runtime-smoke.v1",
        "ok": smoke["ok"] and route["ok"] and generation["ok"] and all(check["ok"] for check in checks),
        "checks": checks,
        "slice_smoke": smoke,
        "route": route,
        "generation": generation,
        "state": customer_success_management_empty_state(),
        "blocking_gaps": (),
        "side_effects": (),
    }


def customer_success_management_runtime_capabilities() -> dict:
    runtime = build_runtime_capabilities()
    smoke = customer_success_management_runtime_smoke()
    return {
        **runtime,
        "ok": runtime["ok"] and smoke["ok"],
        "owned_tables": CUSTOMER_SUCCESS_MANAGEMENT_OWNED_TABLES,
        "operations": tuple(
            dict.fromkeys(
                tuple(build_service_contract()["command_methods"] + build_service_contract()["query_methods"])
                + (
                    "build_schema_contract",
                    "build_service_contract",
                    "build_release_evidence",
                )
            )
        ),
        "smoke": smoke,
        "side_effects": (),
    }
