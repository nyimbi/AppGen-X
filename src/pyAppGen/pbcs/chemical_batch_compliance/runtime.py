"""Executable runtime contract for the chemical_batch_compliance PBC."""

from __future__ import annotations

from .slice_app import ALLOWED_DATABASE_BACKENDS as CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS
from .slice_app import BUSINESS_TABLES as CHEMICAL_BATCH_COMPLIANCE_BUSINESS_TABLES
from .slice_app import COMMAND_METHODS
from .slice_app import CONSUMED_EVENT_TYPES as CHEMICAL_BATCH_COMPLIANCE_CONSUMED_EVENT_TYPES
from .slice_app import EMITTED_EVENT_TYPES as CHEMICAL_BATCH_COMPLIANCE_EMITTED_EVENT_TYPES
from .slice_app import EVENT_TABLES
from .slice_app import OWNED_TABLES as CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES
from .slice_app import PBC_KEY
from .slice_app import QUERY_METHODS
from .slice_app import REQUIRED_EVENT_TOPIC as CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC
from .slice_app import RUNTIME_CAPABILITY_KEYS as CHEMICAL_BATCH_COMPLIANCE_RUNTIME_CAPABILITY_KEYS
from .slice_app import STANDARD_FEATURE_KEYS as CHEMICAL_BATCH_COMPLIANCE_STANDARD_FEATURE_KEYS
from .slice_app import UI_FRAGMENT_KEYS as CHEMICAL_BATCH_COMPLIANCE_UI_FRAGMENT_KEYS
from .slice_app import build_api_contract
from .slice_app import build_app_surface
from .slice_app import build_release_evidence
from .slice_app import build_schema_contract
from .slice_app import build_service_contract
from .slice_app import build_workbench_view
from .slice_app import configure_runtime
from .slice_app import create_document_instruction
from .slice_app import create_formula_revision
from .slice_app import create_regulatory_submission
from .slice_app import delete_document_instruction
from .slice_app import empty_state as chemical_batch_compliance_empty_state
from .slice_app import parse_document_instruction
from .slice_app import permissions_contract as chemical_batch_compliance_permissions_contract
from .slice_app import query_batch_detail
from .slice_app import query_document_instruction
from .slice_app import query_formula_detail
from .slice_app import query_workbench
from .slice_app import receive_event
from .slice_app import record_batch
from .slice_app import record_quality_test
from .slice_app import register_hazardous_material
from .slice_app import register_rule_definition
from .slice_app import register_schema_extension_definition
from .slice_app import release_formula_revision
from .slice_app import resolve_compliance_hold
from .slice_app import run_advanced_assessment
from .slice_app import run_slice_smoke
from .slice_app import set_parameter_value
from .slice_app import upsert_control_assertion
from .slice_app import update_document_instruction
from .slice_app import verify_owned_table_boundary
from .slice_app import review_sds_document

CHEMICAL_BATCH_COMPLIANCE_RUNTIME_TABLES = CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES


def chemical_batch_compliance_configure_runtime(state: dict, config: dict) -> dict:
    return configure_runtime(state, config)


def chemical_batch_compliance_set_parameter(state: dict, name: str, value, tenant: str = "default") -> dict:
    return set_parameter_value(state, name, value, tenant=tenant)


def chemical_batch_compliance_register_rule(state: dict, rule: dict, tenant: str = "default") -> dict:
    return register_rule_definition(state, rule, tenant=tenant)


def chemical_batch_compliance_register_schema_extension(
    state: dict,
    table: str,
    fields: dict,
    tenant: str = "default",
    rationale: str = "",
) -> dict:
    return register_schema_extension_definition(state, table, fields, tenant=tenant, rationale=rationale)


def chemical_batch_compliance_receive_event(state: dict, event: dict) -> dict:
    return receive_event(state, event)


def chemical_batch_compliance_create_formula_revision(state: dict, payload: dict) -> dict:
    return create_formula_revision(state, payload)


def chemical_batch_compliance_release_formula_revision(state: dict, payload: dict) -> dict:
    return release_formula_revision(state, payload)


def chemical_batch_compliance_review_sds_document(state: dict, payload: dict) -> dict:
    return review_sds_document(state, payload)


def chemical_batch_compliance_register_hazardous_material(state: dict, payload: dict) -> dict:
    return register_hazardous_material(state, payload)


def chemical_batch_compliance_record_batch(state: dict, payload: dict) -> dict:
    return record_batch(state, payload)


def chemical_batch_compliance_record_quality_test(state: dict, payload: dict) -> dict:
    return record_quality_test(state, payload)


def chemical_batch_compliance_place_compliance_hold(state: dict, payload: dict) -> dict:
    from .slice_app import place_compliance_hold

    return place_compliance_hold(state, payload)


def chemical_batch_compliance_resolve_compliance_hold(state: dict, payload: dict) -> dict:
    return resolve_compliance_hold(state, payload)


def chemical_batch_compliance_create_regulatory_submission(state: dict, payload: dict) -> dict:
    return create_regulatory_submission(state, payload)


def chemical_batch_compliance_upsert_control_assertion(state: dict, payload: dict) -> dict:
    return upsert_control_assertion(state, payload)


def chemical_batch_compliance_create_document_instruction(state: dict, payload: dict) -> dict:
    return create_document_instruction(state, payload)


def chemical_batch_compliance_update_document_instruction(state: dict, payload: dict) -> dict:
    return update_document_instruction(state, payload)


def chemical_batch_compliance_delete_document_instruction(state: dict, payload: dict) -> dict:
    return delete_document_instruction(state, payload)


def chemical_batch_compliance_query_formula_detail(state: dict, formula_id: str) -> dict:
    return query_formula_detail(state, formula_id)


def chemical_batch_compliance_query_batch_detail(state: dict, batch_id: str) -> dict:
    return query_batch_detail(state, batch_id)


def chemical_batch_compliance_query_document_instruction(state: dict, record_id: str) -> dict:
    return query_document_instruction(state, record_id)


def chemical_batch_compliance_query_workbench(state: dict, filters: dict | None = None) -> dict:
    return query_workbench(state, filters)


def chemical_batch_compliance_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    return run_advanced_assessment(state, payload)


def chemical_batch_compliance_parse_document_instruction(document: str, instruction: str) -> dict:
    return parse_document_instruction(document, instruction)


def chemical_batch_compliance_build_schema_contract() -> dict:
    return build_schema_contract()


def chemical_batch_compliance_build_service_contract() -> dict:
    return build_service_contract()


def chemical_batch_compliance_build_api_contract() -> dict:
    return build_api_contract()


def chemical_batch_compliance_build_release_evidence(state: dict | None = None) -> dict:
    return build_release_evidence(state)


def chemical_batch_compliance_build_workbench_view(tenant: str = "default", state: dict | None = None) -> dict:
    return build_workbench_view(state, tenant=tenant)


def chemical_batch_compliance_build_app_surface(tenant: str = "default", state: dict | None = None) -> dict:
    return build_app_surface(state, tenant=tenant)


def chemical_batch_compliance_verify_owned_table_boundary(references=()) -> dict:
    return verify_owned_table_boundary(tuple(references))


def chemical_batch_compliance_runtime_capabilities() -> dict:
    smoke = chemical_batch_compliance_runtime_smoke()
    operations = COMMAND_METHODS + QUERY_METHODS + (
        "build_schema_contract",
        "build_service_contract",
    )
    return {
        "format": "appgen.chemical-batch-compliance-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES,
        "business_tables": CHEMICAL_BATCH_COMPLIANCE_BUSINESS_TABLES,
        "runtime_tables": CHEMICAL_BATCH_COMPLIANCE_RUNTIME_TABLES,
        "allowed_database_backends": CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "standard_features": CHEMICAL_BATCH_COMPLIANCE_STANDARD_FEATURE_KEYS,
        "capabilities": CHEMICAL_BATCH_COMPLIANCE_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "command_methods": COMMAND_METHODS,
        "query_methods": QUERY_METHODS,
        "smoke": smoke,
        "database_backends": CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "ui_fragments": CHEMICAL_BATCH_COMPLIANCE_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def chemical_batch_compliance_runtime_smoke() -> dict:
    smoke = run_slice_smoke()
    checks = smoke["checks"] + (
        {
            "id": "owned_boundary_accepts_owned_tables",
            "ok": chemical_batch_compliance_verify_owned_table_boundary(
                CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES + EVENT_TABLES
            )["ok"],
        },
        {
            "id": "owned_boundary_rejects_foreign_table",
            "ok": chemical_batch_compliance_verify_owned_table_boundary(("foreign_table",))["ok"] is False,
        },
    )
    return {
        "format": "appgen.chemical-batch-compliance-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "slice_smoke": smoke,
        "state": smoke["state"],
    }
