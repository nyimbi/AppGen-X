from .standalone import PBC_KEY, _HANDLED_EVENT_KEYS, handler_manifest, dispatch_event


def smoke_test():
    base_key = len(_HANDLED_EVENT_KEYS) + 1
    first = dispatch_event({'event_type': handler_manifest()['consumes'][0], 'idempotency_key': f'{PBC_KEY}:smoke:{base_key}'})
    second = dispatch_event({'event_type': handler_manifest()['consumes'][0], 'idempotency_key': f'{PBC_KEY}:smoke:{base_key}'})
    failed = dispatch_event({'event_type': 'Unexpected', 'idempotency_key': f'{PBC_KEY}:bad:{base_key}'})
    return {'ok': first['ok'] and second['duplicate'] and failed['dead_letter_table'].endswith('dead_letter_event'), 'side_effects': ()}
