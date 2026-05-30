"""Package-local table-stakes capability assurance for real estate property management."""
from .standalone import table_stakes_capability_manifest as _table_stakes_capability_manifest
from .standalone import validate_table_stakes_capability_coverage as _validate_table_stakes_capability_coverage


def table_stakes_capability_manifest():
    manifest = _table_stakes_capability_manifest()
    manifest['event_contract'] = 'AppGen-X'
    manifest['stream_picker_visible'] = False
    manifest['invalid_backends'] = ()
    return manifest


def validate_table_stakes_capability_coverage():
    validation = _validate_table_stakes_capability_coverage()
    validation['event_contract'] = 'AppGen-X'
    validation['stream_picker_visible'] = False
    validation['invalid_backends'] = ()
    return validation


def smoke_test():
    validation = validate_table_stakes_capability_coverage()
    return {'ok': validation['ok'], 'validation': validation, 'event_contract': 'AppGen-X', 'stream_picker_visible': False, 'invalid_backends': (), 'side_effects': ()}
