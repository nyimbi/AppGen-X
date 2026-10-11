"""Owned schema evidence for the grant_fund_accounting PBC, derived from the runtime builder."""

from .runtime import grant_fund_accounting_build_schema_contract as _build_schema_contract

SCHEMA_CONTRACT = _build_schema_contract()

def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    contract = build_schema_contract()
    pbc = contract['pbc']
    owned_tables = tuple(contract.get('owned_tables', ()))
    model_tables = tuple(model['table'] for model in contract.get('models', ()))
    allowed_backends = {'postgresql', 'mysql', 'mariadb'}
    invalid_backends = tuple(backend for backend in contract.get('database_backends', ()) if backend not in allowed_backends)
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f'{pbc}_'))
    return {'ok': contract.get('ok') is True and bool(owned_tables) and bool(contract.get('migrations')) and not invalid_tables and not missing_models and not invalid_backends and contract.get('shared_table_access') is False, 'pbc': pbc, 'owned_tables': owned_tables, 'model_tables': model_tables, 'migration_paths': tuple(contract.get('migrations', ())), 'invalid_tables': invalid_tables, 'missing_models': missing_models, 'invalid_backends': invalid_backends, 'side_effects': ()}


def smoke_test():
    return validate_schema_contract()
