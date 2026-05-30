from .standalone import (
    PBC_KEY,
    REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES as EMITTED,
    REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES as CONSUMED,
    event_contract_manifest,
    validate_event_contract,
    build_event_envelope,
    event_dispatch_plan,
)


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {'tenant': 'tenant-smoke'})
    consumed = build_event_envelope(CONSUMED[0], {'tenant': 'tenant-smoke'})
    return {'ok': event_contract_manifest()['ok'] and validate_event_contract()['ok'] and emitted['ok'] and consumed['ok'], 'emitted': emitted, 'consumed': consumed, 'side_effects': ()}
