"""Package-local capability assurance for the privacy_consent_governance PBC."""
from .manifest import PBC_MANIFEST
from .runtime import PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS, privacy_consent_governance_runtime_capabilities

PBC_KEY = 'privacy_consent_governance'
STANDARD_FEATURE_OPERATION_COVERAGE = {'data_subject_profile_management': ('command_data_subject_profile',),
 'privacy_consent_governance_workflow': ('command_data_subject_profile',),
 'privacy_consent_governance_analytics': ('command_data_subject_profile',),
 'configuration_schema': ('command_data_subject_profile',),
 'rule_engine': ('command_data_subject_profile',),
 'parameter_engine': ('command_data_subject_profile',),
 'owned_schema_migrations_models': ('command_data_subject_profile',),
 'appgen_x_outbox_inbox_eventing': ('command_data_subject_profile',),
 'idempotent_handlers': ('command_data_subject_profile',),
 'retry_dead_letter_evidence': ('command_data_subject_profile',),
 'permissions': ('command_data_subject_profile',),
 'seed_data': ('command_data_subject_profile',),
 'workbench': ('command_data_subject_profile',),
 'agentic_document_instruction_intake': ('command_data_subject_profile',),
 'governed_datastore_crud': ('command_data_subject_profile',)}
ADVANCED_CAPABILITY_OPERATION_COVERAGE = {'privacy_consent_governance_event_sourced_operational_history': ('run_advanced_assessment',),
 'privacy_consent_governance_multi_tenant_policy_isolation': ('run_advanced_assessment',),
 'privacy_consent_governance_schema_evolution_resilience': ('run_advanced_assessment',),
 'privacy_consent_governance_autonomous_anomaly_detection': ('run_advanced_assessment',),
 'privacy_consent_governance_semantic_document_instruction_understanding': ('run_advanced_assessment',),
 'privacy_consent_governance_predictive_risk_scoring': ('run_advanced_assessment',),
 'privacy_consent_governance_counterfactual_scenario_simulation': ('run_advanced_assessment',),
 'privacy_consent_governance_cryptographic_audit_proofs': ('run_advanced_assessment',),
 'privacy_consent_governance_continuous_control_testing': ('run_advanced_assessment',),
 'privacy_consent_governance_carbon_and_sustainability_awareness': ('run_advanced_assessment',),
 'privacy_consent_governance_cross_pbc_event_federation': ('run_advanced_assessment',),
 'privacy_consent_governance_governed_ai_agent_execution': ('run_advanced_assessment',)}


def _missing_coverage(features, coverage, operations):
    gaps = []
    for feature in features:
        required_operations = coverage.get(feature, ())
        missing_operations = tuple(operation for operation in required_operations if operation not in operations)
        if missing_operations:
            gaps.append({'feature': feature, 'required_operations': required_operations, 'missing_operations': missing_operations})
    return tuple(gaps)


def table_stakes_capability_manifest():
    runtime = privacy_consent_governance_runtime_capabilities()
    return {'ok': runtime['ok'], 'pbc': PBC_KEY, 'standard_features': PBC_MANIFEST['standard_features'], 'advanced_capabilities': PBC_MANIFEST['advanced_capabilities'], 'runtime_operations': tuple(runtime['operations']), 'owned_tables': tuple(runtime['owned_tables']), 'event_contract': 'AppGen-X', 'stream_picker_visible': False, 'stream_engine_picker_visible': False, 'allowed_database_backends': PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS, 'side_effects': ()}


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
    runtime = privacy_consent_governance_runtime_capabilities()
    return {'ok': coverage['ok'] and runtime['ok'], 'coverage': coverage, 'runtime': runtime, 'side_effects': ()}
