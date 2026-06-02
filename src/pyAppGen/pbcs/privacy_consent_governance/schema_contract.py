"""Generated owned schema evidence for the privacy_consent_governance PBC."""

from __future__ import annotations

from .models import MODELS, OWNED_TABLES, TABLE_DEFINITIONS, database_model_contract

PBC_KEY = 'privacy_consent_governance'
SCHEMA_CONTRACT = {
    'format': 'appgen.privacy-consent-governance-owned-schema-contract.v2',
    'ok': True,
    'pbc': PBC_KEY,
    'tables': TABLE_DEFINITIONS,
    'migrations': ('migrations/001_initial.sql',),
    'models': MODELS,
    'database_backends': ('postgresql', 'mysql', 'mariadb'),
    'datastore_backends': ('postgresql', 'mysql', 'mariadb'),
    'shared_table_access': False,
    'owned_tables': OWNED_TABLES,
    'model_contract': database_model_contract(),
}


def build_schema_contract() -> dict:
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract() -> dict:
    contract = build_schema_contract()
    owned_tables = tuple(contract.get('owned_tables', ()))
    model_tables = tuple(model['table'] for model in contract.get('models', ()))
    allowed_backends = {'postgresql', 'mysql', 'mariadb'}
    invalid_backends = tuple(backend for backend in contract.get('database_backends', ()) if backend not in allowed_backends)
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f'{PBC_KEY}_'))
    return {
        'ok': contract.get('ok') is True
        and bool(owned_tables)
        and bool(contract.get('migrations'))
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and contract.get('shared_table_access') is False,
        'pbc': PBC_KEY,
        'owned_tables': owned_tables,
        'model_tables': model_tables,
        'migration_paths': tuple(contract.get('migrations', ())),
        'invalid_tables': invalid_tables,
        'missing_models': missing_models,
        'invalid_backends': invalid_backends,
        'side_effects': (),
    }


def smoke_test() -> dict:
    return validate_schema_contract()
