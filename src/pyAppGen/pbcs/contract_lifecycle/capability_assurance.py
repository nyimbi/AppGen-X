"""Package-local capability assurance for the contract_lifecycle PBC."""
from .manifest import PBC_MANIFEST
from .runtime import CONTRACT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS, contract_lifecycle_runtime_capabilities

PBC_KEY = 'contract_lifecycle'
STANDARD_FEATURE_OPERATION_COVERAGE = {
    'contract_record_management': ('intake_contract', 'classify_contract'),
    'contract_lifecycle_workflow': ('create_authoring_workspace', 'negotiate_redline', 'route_approval'),
    'contract_lifecycle_analytics': ('query_workbench', 'build_workbench_view', 'score_contract_risk'),
    'configuration_schema': ('configure_runtime',),
    'rule_engine': ('compile_contract_rule', 'register_rule'),
    'parameter_engine': ('set_parameter',),
    'owned_schema_migrations_models': ('build_schema_contract',),
    'appgen_x_outbox_inbox_eventing': ('receive_event',),
    'idempotent_handlers': ('receive_event',),
    'retry_dead_letter_evidence': ('receive_event',),
    'permissions': ('build_service_contract',),
    'seed_data': ('build_release_evidence',),
    'workbench': ('query_workbench', 'build_workbench_view'),
    'agentic_document_instruction_intake': ('parse_document_instruction',),
    'governed_datastore_crud': ('intake_contract', 'activate_obligation', 'schedule_renewal'),
    'ai_agent_task_assistance': ('parse_document_instruction',),
    'configuration_workbench': ('configure_runtime', 'build_workbench_view'),
    'continuous_release_assurance': ('build_release_evidence',),
}
ADVANCED_CAPABILITY_OPERATION_COVERAGE = {'contract_lifecycle_event_sourced_operational_history': ('run_advanced_assessment',),
 'contract_lifecycle_multi_tenant_policy_isolation': ('run_advanced_assessment',),
 'contract_lifecycle_schema_evolution_resilience': ('run_advanced_assessment',),
 'contract_lifecycle_autonomous_anomaly_detection': ('run_advanced_assessment',),
 'contract_lifecycle_semantic_document_instruction_understanding': ('run_advanced_assessment',),
 'contract_lifecycle_predictive_risk_scoring': ('run_advanced_assessment',),
 'contract_lifecycle_counterfactual_scenario_simulation': ('run_advanced_assessment',),
 'contract_lifecycle_cryptographic_audit_proofs': ('run_advanced_assessment',),
 'contract_lifecycle_continuous_control_testing': ('run_advanced_assessment',),
 'contract_lifecycle_carbon_and_sustainability_awareness': ('run_advanced_assessment',),
 'contract_lifecycle_cross_pbc_event_federation': ('run_advanced_assessment',),
 'contract_lifecycle_governed_ai_agent_execution': ('run_advanced_assessment',)}


def _missing_coverage(features, coverage, operations):
    gaps = []
    for feature in features:
        required_operations = coverage.get(feature, ())
        missing_operations = tuple(operation for operation in required_operations if operation not in operations)
        if missing_operations:
            gaps.append({'feature': feature, 'required_operations': required_operations, 'missing_operations': missing_operations})
    return tuple(gaps)


def table_stakes_capability_manifest():
    runtime = contract_lifecycle_runtime_capabilities()
    return {'ok': runtime['ok'], 'pbc': PBC_KEY, 'standard_features': PBC_MANIFEST['standard_features'], 'advanced_capabilities': PBC_MANIFEST['advanced_capabilities'], 'runtime_operations': tuple(runtime['operations']), 'owned_tables': tuple(runtime['owned_tables']), 'event_contract': 'AppGen-X', 'stream_picker_visible': False, 'stream_engine_picker_visible': False, 'allowed_database_backends': CONTRACT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS, 'side_effects': ()}


def validate_table_stakes_capability_coverage():
    manifest = table_stakes_capability_manifest()
    operations = set(manifest['runtime_operations'])
    invalid_backends = tuple(backend for backend in (PBC_MANIFEST['datastore_backend'],) if backend not in manifest['allowed_database_backends'])
    invalid_tables = tuple(table for table in manifest['owned_tables'] if not table.startswith(f'{PBC_KEY}_'))
    missing_standard = _missing_coverage(manifest['standard_features'], STANDARD_FEATURE_OPERATION_COVERAGE, operations)
    missing_advanced = _missing_coverage(manifest['advanced_capabilities'], ADVANCED_CAPABILITY_OPERATION_COVERAGE, operations)
    return {'ok': manifest['ok'] and not invalid_backends and not invalid_tables and not missing_standard and not missing_advanced, 'manifest': manifest, 'covered_standard': tuple(feature for feature in manifest['standard_features'] if feature not in {gap['feature'] for gap in missing_standard}), 'covered_advanced': tuple(feature for feature in manifest['advanced_capabilities'] if feature not in {gap['feature'] for gap in missing_advanced}), 'missing_standard': missing_standard, 'missing_advanced': missing_advanced, 'missing_operations': tuple(sorted({operation for gap in missing_standard + missing_advanced for operation in gap['missing_operations']})), 'uncovered_features': (), 'invalid_tables': invalid_tables, 'invalid_backends': invalid_backends, 'event_contract': 'AppGen-X', 'stream_picker_visible': False, 'stream_engine_picker_visible': False, 'side_effects': ()}


def smoke_test():
    coverage = validate_table_stakes_capability_coverage()
    runtime = contract_lifecycle_runtime_capabilities()
    return {'ok': coverage['ok'] and runtime['ok'], 'coverage': coverage, 'runtime': runtime, 'side_effects': ()}
