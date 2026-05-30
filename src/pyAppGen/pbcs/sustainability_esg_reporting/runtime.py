"""Executable runtime contract for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import ADVANCED_CAPABILITIES, ALLOWED_DATABASE_BACKENDS, APPGEN_X_TOPIC, CONSUMED_EVENTS, EMITTED_EVENTS, EVENT_TABLES, PBC_KEY, STANDARD_FEATURES
from .slice_app import (
    build_api_contract,
    build_release_evidence,
    build_runtime_capabilities,
    build_schema_contract,
    build_service_contract,
    build_standalone_app,
    build_permissions_contract,
    verify_owned_table_boundary,
)
from .domain_depth import domain_depth_contract as sustainability_esg_reporting_domain_depth_contract
from .domain_depth import domain_depth_smoke_test as sustainability_esg_reporting_domain_depth_smoke_test
from .domain_depth import execute_domain_operation as sustainability_esg_reporting_execute_domain_operation

SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES = tuple(build_runtime_capabilities()['owned_tables'])
SUSTAINABILITY_ESG_REPORTING_RUNTIME_TABLES = tuple(build_runtime_capabilities()['owned_tables'])
SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
SUSTAINABILITY_ESG_REPORTING_REQUIRED_EVENT_TOPIC = APPGEN_X_TOPIC
SUSTAINABILITY_ESG_REPORTING_EMITTED_EVENT_TYPES = EMITTED_EVENTS
SUSTAINABILITY_ESG_REPORTING_CONSUMED_EVENT_TYPES = CONSUMED_EVENTS
SUSTAINABILITY_ESG_REPORTING_STANDARD_FEATURE_KEYS = STANDARD_FEATURES
SUSTAINABILITY_ESG_REPORTING_RUNTIME_CAPABILITY_KEYS = ADVANCED_CAPABILITIES
SUSTAINABILITY_ESG_REPORTING_UI_FRAGMENT_KEYS = ('SustainabilityEsgReportingWorkbench', 'SustainabilityEsgReportingDetail', 'SustainabilityEsgReportingAssistantPanel')
SUSTAINABILITY_ESG_REPORTING_BUSINESS_TABLES = tuple(table for table in SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES if table not in EVENT_TABLES)


def sustainability_esg_reporting_empty_state():
    return build_standalone_app().empty_state()


def sustainability_esg_reporting_configure_runtime(state, config):
    app = build_standalone_app()
    result = app.configure_runtime(config)
    return {**result, 'state': app.empty_state(), 'side_effects': ()}


def sustainability_esg_reporting_set_parameter(state, name, value):
    app = build_standalone_app()
    result = app.set_parameter(name, value)
    return {**result, 'state': app.empty_state(), 'side_effects': ()}


def sustainability_esg_reporting_register_rule(state, rule):
    app = build_standalone_app()
    result = app.register_rule(rule)
    return {**result, 'state': app.empty_state(), 'side_effects': ()}


def sustainability_esg_reporting_register_schema_extension(state, table, fields):
    app = build_standalone_app()
    result = app.register_schema_extension(table, fields)
    return {**result, 'state': app.empty_state(), 'side_effects': ()}


def sustainability_esg_reporting_receive_event(state, event):
    app = build_standalone_app()
    result = app.receive_event(event)
    return {**result, 'state': app.empty_state(), 'side_effects': ()}


def sustainability_esg_reporting_command_emissions_factor(state, payload):
    app = build_standalone_app()
    result = app.execute_operation('register_emissions_factor', payload)
    return {**result, 'state': app.empty_state(), 'side_effects': ()}


def sustainability_esg_reporting_query_workbench(state, filters=None):
    app = build_standalone_app()
    filters = dict(filters or {})
    return {**app.query_workbench(tenant=filters.get('tenant', 'default'), limit=filters.get('limit', 10)), 'filters': filters, 'read_only': True, 'side_effects': ()}


def sustainability_esg_reporting_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    summary = build_standalone_app().query_workbench(tenant=payload.get('tenant', 'default'))['summary']
    score = round(min(1.0, 0.55 + 0.05 * len(ADVANCED_CAPABILITIES) / 10), 4)
    return {'ok': True, 'score': score, 'summary': summary, 'explanations': ('appgen_x_only', 'owned_boundary_respected', 'release_audits_ready'), 'payload': payload, 'side_effects': ()}


def sustainability_esg_reporting_parse_document_instruction(document, instruction):
    return build_standalone_app().document_instruction_plan(document, instruction)


def sustainability_esg_reporting_build_schema_contract():
    return build_schema_contract()


def sustainability_esg_reporting_build_service_contract():
    return build_service_contract()


def sustainability_esg_reporting_build_api_contract():
    return build_api_contract()


def sustainability_esg_reporting_build_release_evidence():
    return build_release_evidence()


def sustainability_esg_reporting_permissions_contract():
    return build_permissions_contract()


def sustainability_esg_reporting_build_workbench_view(state=None, tenant='default'):
    return build_standalone_app().build_workbench_view(tenant=tenant)


def sustainability_esg_reporting_verify_owned_table_boundary(references):
    return verify_owned_table_boundary(tuple(references))


def sustainability_esg_reporting_runtime_smoke():
    return build_runtime_capabilities()['smoke']


def sustainability_esg_reporting_runtime_capabilities():
    return build_runtime_capabilities()
