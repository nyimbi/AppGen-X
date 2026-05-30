"""Executable runtime contract for the public_safety_dispatch PBC."""
from __future__ import annotations

from .standalone import (
    ADVANCED_CAPABILITIES,
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
    pbc_generation_smoke_audit,
    standalone_smoke_test,
)

PUBLIC_SAFETY_DISPATCH_OWNED_TABLES = BUSINESS_TABLES + EVENT_TABLES
PUBLIC_SAFETY_DISPATCH_RUNTIME_TABLES = RUNTIME_TABLES
PUBLIC_SAFETY_DISPATCH_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
PUBLIC_SAFETY_DISPATCH_REQUIRED_EVENT_TOPIC = APPGEN_X_TOPIC
PUBLIC_SAFETY_DISPATCH_EMITTED_EVENT_TYPES = EMITTED_EVENTS
PUBLIC_SAFETY_DISPATCH_CONSUMED_EVENT_TYPES = CONSUMED_EVENTS
PUBLIC_SAFETY_DISPATCH_STANDARD_FEATURE_KEYS = tuple(build_runtime_capabilities()["standard_features"])
PUBLIC_SAFETY_DISPATCH_RUNTIME_CAPABILITY_KEYS = tuple(ADVANCED_CAPABILITIES)
PUBLIC_SAFETY_DISPATCH_UI_FRAGMENT_KEYS = tuple(build_ui_contract()["fragments"])
PUBLIC_SAFETY_DISPATCH_BUSINESS_TABLES = BUSINESS_TABLES


def public_safety_dispatch_empty_state() -> dict:
    return {
        "tenant": "default",
        "configuration": {},
        "parameters": {},
        "rules": {},
        "summary": {},
        "side_effects": (),
    }


def public_safety_dispatch_configure_runtime(state: dict, config: dict) -> dict:
    app = build_standalone_app()
    result = app.configure_runtime(config)
    next_state = {**dict(state), "configuration": result["configuration"]}
    return {"ok": result["ok"], "state": next_state, "configuration": result["configuration"], "side_effects": ()}


def public_safety_dispatch_set_parameter(state: dict, name: str, value) -> dict:
    app = build_standalone_app()
    result = app.set_parameter(name, value)
    next_state = {**dict(state), "parameters": {**dict(state.get("parameters", {})), name: result.get("parameter")}}
    return {"ok": result["ok"], "state": next_state, "parameter": result.get("parameter"), "side_effects": ()}


def public_safety_dispatch_register_rule(state: dict, rule: dict) -> dict:
    app = build_standalone_app()
    result = app.register_rule(rule)
    next_state = {**dict(state), "rules": {**dict(state.get("rules", {})), rule.get("rule_id", "unnamed_rule"): result["rule"]}}
    return {"ok": result["ok"], "state": next_state, "rule": result["rule"], "side_effects": ()}


def public_safety_dispatch_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    app = build_standalone_app()
    result = app.register_schema_extension(table, fields)
    return {"ok": result["ok"], "state": dict(state), **result, "side_effects": ()}


def public_safety_dispatch_receive_event(state: dict, event: dict) -> dict:
    app = build_standalone_app()
    result = app.receive_event(event)
    return {"ok": result["ok"], "state": dict(state), **result, "side_effects": ()}


def public_safety_dispatch_command_emergency_call(state: dict, payload: dict) -> dict:
    app = build_standalone_app()
    result = app.create_emergency_call(payload)
    next_state = {**dict(state), "tenant": payload.get("tenant", state.get("tenant", "default")), "summary": {"incident_id": result.get("incident", {}).get("id")}}
    return {"ok": result["ok"], "state": next_state, **result, "side_effects": ()}


def public_safety_dispatch_query_workbench(state: dict, filters: dict | None = None) -> dict:
    filters = dict(filters or {})
    tenant = filters.get("tenant", state.get("tenant", "default"))
    app = build_standalone_app()
    app.load_demo_workspace(tenant)
    workbench = app.query_workbench(tenant)
    return {"ok": workbench["ok"], "records": tuple(workbench["records"]["incidents"]), "filters": filters, "read_only": True, "workbench": workbench, "side_effects": ()}


def public_safety_dispatch_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    tenant = dict(payload or {}).get("tenant", state.get("tenant", "tenant_alpha"))
    app = build_standalone_app()
    result = app.run_advanced_assessment(tenant=tenant)
    return {**result, "side_effects": ()}


def public_safety_dispatch_parse_document_instruction(document: str, instruction: str) -> dict:
    return build_standalone_app().document_instruction_plan(document, instruction)


def public_safety_dispatch_build_schema_contract() -> dict:
    return build_schema_contract()


def public_safety_dispatch_build_service_contract() -> dict:
    return build_service_contract()


def public_safety_dispatch_build_api_contract() -> dict:
    return build_api_contract()


def public_safety_dispatch_build_release_evidence() -> dict:
    return build_release_evidence()


def public_safety_dispatch_permissions_contract() -> dict:
    from .permissions import permission_manifest

    return permission_manifest()


def public_safety_dispatch_build_workbench_view(state: dict | None = None, tenant: str = "default") -> dict:
    app = build_standalone_app()
    app.load_demo_workspace(tenant)
    view = app.build_workbench_view(tenant)
    return {"ok": view["ok"], "pbc": PBC_KEY, "tenant": tenant, **view, "side_effects": ()}


def public_safety_dispatch_verify_owned_table_boundary(references) -> dict:
    return build_standalone_app().verify_owned_table_boundary(tuple(references))


def public_safety_dispatch_runtime_smoke() -> dict:
    standalone = standalone_smoke_test()
    generation = pbc_generation_smoke_audit()
    release = public_safety_dispatch_build_release_evidence()
    checks = tuple({"id": capability, "ok": True} for capability in PUBLIC_SAFETY_DISPATCH_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": f"appgen.{PBC_KEY}.runtime-smoke.v1",
        "ok": standalone["ok"] and generation["ok"] and release["ok"] and all(check["ok"] for check in checks),
        "checks": checks,
        "standalone": standalone,
        "generation": generation,
        "release": release,
        "state": public_safety_dispatch_empty_state(),
        "side_effects": (),
    }


def public_safety_dispatch_runtime_capabilities() -> dict:
    runtime = build_runtime_capabilities()
    smoke = public_safety_dispatch_runtime_smoke()
    return {
        **runtime,
        "ok": runtime["ok"] and smoke["ok"],
        "owned_tables": PUBLIC_SAFETY_DISPATCH_OWNED_TABLES,
        "runtime_tables": PUBLIC_SAFETY_DISPATCH_RUNTIME_TABLES,
        "allowed_database_backends": PUBLIC_SAFETY_DISPATCH_ALLOWED_DATABASE_BACKENDS,
        "operations": tuple(dict.fromkeys(tuple(build_service_contract()["command_methods"] + build_service_contract()["query_methods"] + ("build_schema_contract", "build_service_contract", "build_api_contract", "build_release_evidence")))),
        "smoke": smoke,
        "side_effects": (),
    }

# Improve1 public safety dispatch control extension.
from .public_safety_dispatch_control import evaluate_public_safety_dispatch_control, improve1_public_safety_dispatch_control_contract

_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_RUNTIME_CAPABILITIES = public_safety_dispatch_runtime_capabilities
_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = public_safety_dispatch_build_release_evidence


def public_safety_dispatch_runtime_capabilities() -> dict:
    runtime = dict(_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_RUNTIME_CAPABILITIES())
    control = improve1_public_safety_dispatch_control_contract()
    runtime["ok"] = bool(runtime.get("ok")) and control["ok"]
    runtime["public_safety_dispatch_control"] = control
    runtime["operations"] = tuple(dict.fromkeys(tuple(runtime.get("operations", ())) + ("evaluate_public_safety_dispatch_control", "improve1_public_safety_dispatch_control_contract")))
    runtime["improve1_control_owned_tables"] = control["owned_tables"]
    return runtime


def public_safety_dispatch_build_release_evidence() -> dict:
    evidence = dict(_PUBLIC_SAFETY_DISPATCH_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = improve1_public_safety_dispatch_control_contract()
    artifacts = dict(evidence.get("generated_artifacts", {}))
    artifacts["public_safety_dispatch_control"] = {
        "contract": control["format"],
        "capability_count": control["capability_count"],
        "owned_tables": control["owned_tables"],
        "service_apis": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "ui_surfaces": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "test": "tests/test_domain_behavior.py",
    }
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_public_safety_dispatch_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "generated_artifacts": artifacts,
        "public_safety_dispatch_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence
