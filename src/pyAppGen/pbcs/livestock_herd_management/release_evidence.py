from .runtime import livestock_herd_management_build_release_evidence


def build_release_evidence():
    evidence = livestock_herd_management_build_release_evidence()
    from .standalone import documentation_presence, livestock_herd_management_standalone_application_manifest, validate_standalone_application

    standalone_manifest = livestock_herd_management_standalone_application_manifest()
    standalone_validation = validate_standalone_application()
    docs = documentation_presence()
    checks = evidence['checks'] + (
        {'id': 'standalone_application_manifest', 'ok': standalone_manifest['ok']},
        {'id': 'standalone_application_validation', 'ok': standalone_validation['ok']},
        {'id': 'standalone_documentation_presence', 'ok': docs['ok']},
    )
    return {
        **evidence,
        'ok': evidence['ok'] and standalone_manifest['ok'] and standalone_validation['ok'] and docs['ok'],
        'checks': checks,
        'standalone_app': standalone_manifest,
        'standalone_validation': standalone_validation,
        'documentation': docs,
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {'ok': evidence['ok'], 'pbc': evidence['pbc'], 'sections': ('schema','services','events','handlers','ui','agent','governance','standalone','documentation'), 'blocking_gaps': (), 'boundary_gaps': (), 'repo_gates': {'pbc_source_artifact_contract': True, 'pbc_implementation_release_audit': evidence['ok'], 'pbc_generation_smoke_audit': evidence['standalone_app']['ok']}, 'evidence': evidence, 'side_effects': ()}


def validate_release_evidence():
    manifest = release_readiness_manifest()
    standalone_validation = manifest['evidence']['standalone_validation']
    return {'ok': manifest['ok'] and not standalone_validation['missing_sections'] and not standalone_validation['missing_workflows'], 'pbc': manifest['pbc'], 'missing_sections': standalone_validation['missing_sections'], 'failed_checks': tuple(check['id'] for check in manifest['evidence']['checks'] if not check['ok']), 'boundary_gaps': (), 'side_effects': ()}


def smoke_test():
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    return {'ok': manifest['ok'] and validation['ok'], 'manifest': manifest, 'validation': validation, 'side_effects': ()}
