"""Executable runtime contract for the environment_health_safety PBC."""

from __future__ import annotations

from . import standalone

PBC_KEY = standalone.PBC_KEY
ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES = standalone.OWNED_TABLES
ENVIRONMENT_HEALTH_SAFETY_RUNTIME_TABLES = standalone.OWNED_TABLES
ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS = standalone.ALLOWED_DATABASE_BACKENDS
ENVIRONMENT_HEALTH_SAFETY_REQUIRED_EVENT_TOPIC = standalone.REQUIRED_EVENT_TOPIC
ENVIRONMENT_HEALTH_SAFETY_EMITTED_EVENT_TYPES = standalone.EMITTED_EVENT_TYPES
ENVIRONMENT_HEALTH_SAFETY_CONSUMED_EVENT_TYPES = standalone.CONSUMED_EVENT_TYPES
ENVIRONMENT_HEALTH_SAFETY_STANDARD_FEATURE_KEYS = standalone.STANDARD_FEATURE_KEYS
ENVIRONMENT_HEALTH_SAFETY_RUNTIME_CAPABILITY_KEYS = standalone.ADVANCED_CAPABILITY_KEYS
ENVIRONMENT_HEALTH_SAFETY_UI_FRAGMENT_KEYS = standalone.UI_FRAGMENT_KEYS
ENVIRONMENT_HEALTH_SAFETY_BUSINESS_TABLES = standalone.BUSINESS_TABLES


def environment_health_safety_empty_state() -> dict:
    return standalone.empty_state()


def environment_health_safety_configure_runtime(state: dict, config: dict) -> dict:
    return standalone.configure_runtime(state, config)


def environment_health_safety_set_parameter(state: dict, name: str, value) -> dict:
    return standalone.set_parameter(state, name, value)


def environment_health_safety_register_rule(state: dict, rule: dict) -> dict:
    return standalone.register_rule(state, rule)


def environment_health_safety_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    return standalone.register_schema_extension(state, table, fields)


def environment_health_safety_receive_event(state: dict, event: dict) -> dict:
    return standalone.handle_consumed_event(state, event)


def environment_health_safety_command_ehs_incident(state: dict, payload: dict) -> dict:
    return standalone.create_ehs_incident(state, payload)


def environment_health_safety_query_workbench(state: dict, filters: dict | None = None) -> dict:
    return standalone.query_workbench(state, filters)


def environment_health_safety_run_dynamic_risk_assessment(state: dict, payload: dict) -> dict:
    return standalone.run_dynamic_risk_assessment(state, payload)


def environment_health_safety_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    return standalone.run_advanced_assessment(state, payload)


def environment_health_safety_parse_document_instruction(document: str, instruction: str) -> dict:
    return standalone.build_document_instruction_plan(document, instruction)


def environment_health_safety_build_schema_contract() -> dict:
    return standalone.build_schema_contract()


def environment_health_safety_build_service_contract() -> dict:
    return standalone.build_service_contract()


def environment_health_safety_build_api_contract() -> dict:
    return standalone.build_api_contract()


def environment_health_safety_build_release_evidence() -> dict:
    return standalone.build_release_evidence()


def environment_health_safety_permissions_contract() -> dict:
    return standalone.build_permission_manifest()


def environment_health_safety_build_workbench_view(tenant: str = "default", state: dict | None = None) -> dict:
    return standalone.query_workbench(state or standalone.seed_state(), {"tenant": tenant})


def environment_health_safety_verify_owned_table_boundary(references=()) -> dict:
    return standalone.verify_owned_table_boundary(tuple(references))


def environment_health_safety_runtime_capabilities() -> dict:
    return standalone.runtime_capabilities()


def environment_health_safety_runtime_smoke() -> dict:
    return standalone.smoke_test()


environment_health_safety_execute_domain_operation = standalone.execute_domain_operation
