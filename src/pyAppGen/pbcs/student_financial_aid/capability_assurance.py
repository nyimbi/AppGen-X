from __future__ import annotations

from .runtime import (
    STUDENT_FINANCIAL_AID_ALLOWED_DATABASE_BACKENDS,
    STUDENT_FINANCIAL_AID_RUNTIME_CAPABILITY_KEYS,
    STUDENT_FINANCIAL_AID_STANDARD_FEATURE_KEYS,
    STUDENT_FINANCIAL_AID_REQUIRED_EVENT_TOPIC,
    student_financial_aid_runtime_capabilities,
    student_financial_aid_runtime_smoke,
)


def table_stakes_capability_manifest() -> dict:
    runtime = student_financial_aid_runtime_capabilities()
    return {
        'ok': runtime['ok'],
        'pbc': runtime['pbc'],
        'standard_features': runtime['standard_features'],
        'advanced_capabilities': runtime['capabilities'],
        'operations': runtime['operations'],
        'event_contract': 'AppGen-X',
        'stream_picker_visible': False,
        'side_effects': (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    missing_standard = tuple(feature for feature in STUDENT_FINANCIAL_AID_STANDARD_FEATURE_KEYS if feature not in manifest['standard_features'])
    missing_advanced = tuple(feature for feature in STUDENT_FINANCIAL_AID_RUNTIME_CAPABILITY_KEYS if feature not in manifest['advanced_capabilities'])
    required_operations = {'configure_runtime', 'set_parameter', 'register_rule', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence'}
    missing_operations = tuple(sorted(required_operations - set(manifest['operations'])))
    invalid_backends = tuple(backend for backend in STUDENT_FINANCIAL_AID_ALLOWED_DATABASE_BACKENDS if backend not in ('postgresql', 'mysql', 'mariadb'))
    uncovered_features = tuple(feature for feature in ('owned_schema_migrations_models', 'service_api_route_contracts', 'appgen_event_contract', 'idempotent_handlers', 'retry_dead_letter_policy', 'ui_workbench', 'permissions_rbac', 'configuration_schema', 'rule_engine', 'parameter_engine', 'seed_data') if feature == 'service_api_route_contracts' and 'award_packaging' not in manifest['standard_features'])
    return {
        'ok': not missing_standard and not missing_advanced and not missing_operations and not uncovered_features and not invalid_backends,
        'pbc': manifest['pbc'],
        'missing_standard': missing_standard,
        'missing_advanced': missing_advanced,
        'missing_operations': missing_operations,
        'uncovered_features': uncovered_features,
        'invalid_tables': (),
        'invalid_backends': invalid_backends,
        'event_contract': manifest['event_contract'],
        'event_topic': STUDENT_FINANCIAL_AID_REQUIRED_EVENT_TOPIC,
        'stream_picker_visible': manifest['stream_picker_visible'],
        'side_effects': (),
    }


def smoke_test() -> dict:
    manifest = table_stakes_capability_manifest()
    validation = validate_table_stakes_capability_coverage()
    runtime_smoke = student_financial_aid_runtime_smoke()
    return {
        'ok': manifest['ok'] and validation['ok'] and runtime_smoke['ok'],
        'manifest': manifest,
        'validation': validation,
        'runtime_smoke': runtime_smoke,
        'side_effects': (),
    }
