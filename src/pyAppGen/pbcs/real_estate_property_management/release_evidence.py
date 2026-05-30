from .standalone import build_release_evidence, release_readiness_manifest, validate_release_evidence


def smoke_test():
    validation = validate_release_evidence()
    return {'ok': validation['ok'], 'validation': validation, 'side_effects': ()}
