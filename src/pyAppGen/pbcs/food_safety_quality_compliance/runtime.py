"""Executable runtime contract for the food_safety_quality_compliance PBC."""

from __future__ import annotations

from .slice_app import ALLOWED_DATABASE_BACKENDS
from .slice_app import COMMAND_METHODS
from .slice_app import CONSUMED_EVENT_TYPES
from .slice_app import EMITTED_EVENT_TYPES
from .slice_app import EVENT_CONTRACT
from .slice_app import OWNED_TABLES
from .slice_app import PBC_KEY
from .slice_app import QUERY_METHODS
from .slice_app import REQUIRED_EVENT_TOPIC
from .slice_app import build_api_contract
from .slice_app import build_release_evidence
from .slice_app import build_schema_contract
from .slice_app import build_service_contract
from .slice_app import build_workbench_view
from .slice_app import configure_runtime
from .slice_app import create_haccp_plan
from .slice_app import document_instruction_plan
from .slice_app import domain_depth_contract
from .slice_app import empty_state
from .slice_app import execute_domain_operation
from .slice_app import query_workbench
from .slice_app import receive_event
from .slice_app import register_rule
from .slice_app import register_schema_extension
from .slice_app import run_slice_smoke
from .slice_app import runtime_capabilities
from .slice_app import set_parameter
from .slice_app import verify_owned_table_boundary

FOOD_SAFETY_QUALITY_COMPLIANCE_OWNED_TABLES = OWNED_TABLES
FOOD_SAFETY_QUALITY_COMPLIANCE_RUNTIME_TABLES = OWNED_TABLES
FOOD_SAFETY_QUALITY_COMPLIANCE_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
FOOD_SAFETY_QUALITY_COMPLIANCE_REQUIRED_EVENT_TOPIC = REQUIRED_EVENT_TOPIC
FOOD_SAFETY_QUALITY_COMPLIANCE_EMITTED_EVENT_TYPES = EMITTED_EVENT_TYPES
FOOD_SAFETY_QUALITY_COMPLIANCE_CONSUMED_EVENT_TYPES = CONSUMED_EVENT_TYPES
FOOD_SAFETY_QUALITY_COMPLIANCE_STANDARD_FEATURE_KEYS = runtime_capabilities()["standard_features"]
FOOD_SAFETY_QUALITY_COMPLIANCE_RUNTIME_CAPABILITY_KEYS = runtime_capabilities()["capabilities"]
FOOD_SAFETY_QUALITY_COMPLIANCE_UI_FRAGMENT_KEYS = ("FoodSafetyQualityComplianceWorkbench", "FoodSafetyQualityComplianceDetail", "FoodSafetyQualityComplianceAssistantPanel")
FOOD_SAFETY_QUALITY_COMPLIANCE_BUSINESS_TABLES = OWNED_TABLES[:-3]


def food_safety_quality_compliance_empty_state() -> dict:
    return empty_state()


def food_safety_quality_compliance_configure_runtime(state: dict, config: dict) -> dict:
    return configure_runtime(state, config)


def food_safety_quality_compliance_set_parameter(state: dict, name: str, value) -> dict:
    return set_parameter(state, {"name": name, "value": value})


def food_safety_quality_compliance_register_rule(state: dict, rule: dict) -> dict:
    return register_rule(state, rule)


def food_safety_quality_compliance_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    return register_schema_extension(state, {"table_name": table, "field_map": fields, "tenant": "system"})


def food_safety_quality_compliance_receive_event(state: dict, event: dict) -> dict:
    return receive_event(state, event)


def food_safety_quality_compliance_command_haccp_plan(state: dict, payload: dict) -> dict:
    return create_haccp_plan(state, payload)


def food_safety_quality_compliance_query_workbench(state: dict, filters: dict | None = None) -> dict:
    return query_workbench(state, filters)


def food_safety_quality_compliance_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    workbench = query_workbench(state, payload or {})
    score = max(0.0, min(1.0, 0.5 + 0.05 * sum(workbench["metrics"].values())))
    return {
        "ok": True,
        "score": round(score, 4),
        "explanations": ("haccp_version_pinned", "projection_boundary_enforced", "assistant_confirmation_required"),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def food_safety_quality_compliance_parse_document_instruction(document: str, instruction: str) -> dict:
    return document_instruction_plan(document, instruction)


def food_safety_quality_compliance_build_schema_contract() -> dict:
    return build_schema_contract()


def food_safety_quality_compliance_build_service_contract() -> dict:
    return build_service_contract()


def food_safety_quality_compliance_build_api_contract() -> dict:
    return build_api_contract()


def food_safety_quality_compliance_build_release_evidence() -> dict:
    return build_release_evidence()


def food_safety_quality_compliance_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.create",
            f"{PBC_KEY}.update",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
        ),
        "roles": ("operator", "quality_manager", "supplier_quality_lead", "recall_coordinator", "auditor", "admin"),
        "side_effects": (),
    }


def food_safety_quality_compliance_build_workbench_view(tenant: str = "default") -> dict:
    return build_workbench_view(empty_state(), {"tenant": tenant})


def food_safety_quality_compliance_verify_owned_table_boundary(references=()) -> dict:
    return verify_owned_table_boundary(tuple(references))


def food_safety_quality_compliance_runtime_capabilities() -> dict:
    runtime = runtime_capabilities()
    runtime["smoke"] = food_safety_quality_compliance_runtime_smoke()
    runtime["command_methods"] = COMMAND_METHODS
    runtime["query_methods"] = QUERY_METHODS
    runtime["event_contract"] = EVENT_CONTRACT
    return runtime


def food_safety_quality_compliance_runtime_smoke() -> dict:
    smoke = run_slice_smoke()
    checks = smoke["checks"] + (
        {"id": "schema_contract", "ok": build_schema_contract()["ok"]},
        {"id": "service_contract", "ok": build_service_contract()["ok"]},
        {"id": "api_contract", "ok": build_api_contract()["ok"]},
        {"id": "release_evidence", "ok": build_release_evidence()["ok"]},
        {"id": "domain_depth", "ok": domain_depth_contract()["ok"]},
    )
    return {
        "format": "appgen.food-safety-quality-compliance-runtime-smoke.v2",
        "ok": smoke["ok"] and all(check["ok"] for check in checks),
        "checks": checks,
        "slice_smoke": smoke,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


food_safety_quality_compliance_execute_domain_operation = execute_domain_operation


from .food_control import improve1_food_control_contract as food_safety_quality_compliance_improve1_food_control_contract

_food_safety_quality_compliance_base_build_release_evidence = food_safety_quality_compliance_build_release_evidence
_food_safety_quality_compliance_base_runtime_capabilities = food_safety_quality_compliance_runtime_capabilities

def food_safety_quality_compliance_build_release_evidence() -> dict:
    evidence = _food_safety_quality_compliance_base_build_release_evidence()
    control = food_safety_quality_compliance_improve1_food_control_contract()
    checks = tuple(evidence.get('checks', ())) + ({'id': 'improve1_food_control', 'ok': control['ok']},)
    generated = dict(evidence.get('generated_artifacts', {}))
    generated['food_control'] = {'capability_count': control['capability_count'], 'owned_tables': control['owned_tables'], 'event_contract': control['event_contract'], 'required_event_topic': control['required_event_topic']}
    return {**evidence, 'ok': evidence.get('ok') is True and control['ok'], 'checks': checks, 'generated_artifacts': generated, 'food_control': control, 'blocking_gaps': tuple(evidence.get('blocking_gaps', ())) + tuple(control.get('blocking_gaps', ())), 'side_effects': ()}

def food_safety_quality_compliance_runtime_capabilities() -> dict:
    runtime = _food_safety_quality_compliance_base_runtime_capabilities()
    control = food_safety_quality_compliance_improve1_food_control_contract()
    operations = tuple(runtime.get('operations', ())) + ('improve1_food_control_contract',)
    return {**runtime, 'ok': runtime.get('ok') is True and control['ok'], 'operations': operations, 'food_control': control, 'improve1_capabilities': tuple(item['slug'] for item in control['capabilities']), 'owned_tables': tuple(dict.fromkeys(tuple(runtime.get('owned_tables', ())) + tuple(control['owned_tables']))), 'allowed_database_backends': control['allowed_database_backends'], 'event_contract': control['event_contract'], 'stream_engine_picker_visible': False, 'side_effects': ()}
