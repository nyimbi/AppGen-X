from .runtime import restaurant_operations_build_release_evidence
from .standalone import restaurant_operations_standalone_app_contract, restaurant_operations_standalone_app_smoke


def build_release_evidence():
    evidence = restaurant_operations_build_release_evidence()
    evidence['standalone'] = {
        'contract': restaurant_operations_standalone_app_contract(),
        'smoke': restaurant_operations_standalone_app_smoke(),
    }
    evidence['ok'] = evidence['ok'] and evidence['standalone']['contract']['ok'] and evidence['standalone']['smoke']['ok']
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        'ok': evidence['ok'],
        'pbc': evidence['pbc'],
        'sections': ('schema', 'services', 'events', 'handlers', 'ui', 'agent', 'governance', 'standalone'),
        'blocking_gaps': (),
        'boundary_gaps': (),
        'evidence': evidence,
        'side_effects': (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in ('schema', 'services', 'events', 'handlers', 'ui', 'agent', 'governance', 'standalone') if section not in manifest['sections'])
    return {'ok': manifest['ok'] and not missing_sections, 'pbc': manifest['pbc'], 'missing_sections': missing_sections, 'failed_checks': (), 'boundary_gaps': (), 'side_effects': ()}


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}
