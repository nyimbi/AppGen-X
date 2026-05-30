from .standalone import table_stakes_capability_manifest, validate_table_stakes_capability_coverage


def smoke_test():
    validation = validate_table_stakes_capability_coverage()
    return {'ok': validation['ok'], 'validation': validation, 'side_effects': ()}
