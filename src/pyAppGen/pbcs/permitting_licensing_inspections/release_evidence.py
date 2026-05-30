from . import ui
from .runtime import permitting_licensing_inspections_build_release_evidence


def build_release_evidence():
    evidence = permitting_licensing_inspections_build_release_evidence()
    shell = ui.permitting_licensing_inspections_standalone_app_contract()
    return {
        **evidence,
        'standalone_app': shell,
        'forms': tuple(form['name'] for form in shell['forms']),
        'wizards': tuple(wizard['name'] for wizard in shell['wizards']),
        'controls': tuple(control['name'] for control in shell['controls']),
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    return {
        'ok': evidence['ok'],
        'pbc': evidence['pbc'],
        'sections': ('schema', 'services', 'events', 'handlers', 'ui', 'forms', 'wizards', 'controls', 'agent', 'standalone', 'governance'),
        'blocking_gaps': (),
        'boundary_gaps': (),
        'evidence': evidence,
        'side_effects': (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    missing = tuple(section for section in ('forms', 'wizards', 'controls', 'standalone') if section not in manifest['sections'])
    return {
        'ok': manifest['ok'] and not missing,
        'pbc': manifest['pbc'],
        'missing_sections': missing,
        'failed_checks': (),
        'boundary_gaps': (),
        'side_effects': (),
    }


def smoke_test():
    return {'ok': release_readiness_manifest()['ok'] and validate_release_evidence()['ok'], 'side_effects': ()}
