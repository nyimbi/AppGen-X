"""Executable configuration contract for the mrp_engine PBC."""

PBC_KEY = 'mrp_engine'
CONFIG_SCHEMA = ({'key': 'MRP_ENGINE_DATABASE_URL', 'required': True, 'source': 'environment'}, {'key': 'MRP_ENGINE_EVENT_TOPIC', 'required': True, 'source': 'environment'}, {'key': 'MRP_ENGINE_RETRY_LIMIT', 'required': False, 'source': 'environment'})


def configuration_manifest():
    """Return required configuration keys and validation rules."""
    return {
        'ok': bool(CONFIG_SCHEMA),
        'pbc': PBC_KEY,
        'schema': CONFIG_SCHEMA,
        'required_keys': required_keys(),
        'side_effects': (),
    }


def required_keys():
    """Return configuration keys that must be supplied by an installer."""
    return tuple(item['key'] for item in CONFIG_SCHEMA if item.get('required'))


def validate_configuration(values=None):
    """Validate supplied configuration values without reading process state."""
    supplied = dict(values or {key: 'configured' for key in required_keys()})
    missing = tuple(key for key in required_keys() if not supplied.get(key))
    known = {item['key'] for item in CONFIG_SCHEMA}
    unknown = tuple(sorted(key for key in supplied if key not in known))
    return {
        'ok': not missing and not unknown,
        'pbc': PBC_KEY,
        'missing': missing,
        'unknown': unknown,
        'required_keys': required_keys(),
        'side_effects': (),
    }


def smoke_test():
    """Exercise configuration validation using synthetic values."""
    return validate_configuration()
