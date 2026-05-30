"""Release evidence wrappers for real estate property management."""
from .standalone import build_release_evidence as _build_release_evidence
from .standalone import release_readiness_manifest as _release_readiness_manifest
from .standalone import validate_release_evidence as _validate_release_evidence


def build_release_evidence():
    return _build_release_evidence()


def release_readiness_manifest():
    manifest = _release_readiness_manifest()
    manifest.setdefault('blocking_gaps', ())
    manifest.setdefault('boundary_gaps', ())
    return manifest


def validate_release_evidence():
    validation = _validate_release_evidence()
    validation.setdefault('blocking_gaps', ())
    validation.setdefault('boundary_gaps', ())
    return validation


def smoke_test():
    validation = validate_release_evidence()
    return {'ok': validation['ok'], 'validation': validation, 'blocking_gaps': validation.get('blocking_gaps', ()), 'boundary_gaps': validation.get('boundary_gaps', ()), 'side_effects': ()}
