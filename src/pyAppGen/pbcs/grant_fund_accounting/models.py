"""Owned model metadata for the grant_fund_accounting PBC, derived from the runtime builder."""

from .runtime import grant_fund_accounting_build_schema_contract as _build_schema_contract

PBC_KEY = 'grant_fund_accounting'
_PREFIX = f"{PBC_KEY}_"
_SCHEMA = _build_schema_contract()

# `OWNED_SCHEMA` keeps the logical/physical shape `model_manifest` reads; the
# tables come from the runtime builder, so the model evidence cannot drift from
# the schema evidence.
OWNED_SCHEMA = {
    'schema': PBC_KEY,
    'table_prefix': _PREFIX,
    'tables': tuple(
        {
            'logical_table': table['table'][len(_PREFIX):] if table['table'].startswith(_PREFIX) else table['table'],
            'owned_table': table['table'],
            'fields': table['fields'],
            'relationships': table.get('relationships', ()),
        }
        for table in _SCHEMA['tables']
    ),
}
MODELS = _SCHEMA['models']

def model_manifest():
    schema_tables = tuple(table['owned_table'] for table in OWNED_SCHEMA.get('tables', ()))
    model_tables = tuple(model['table'] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f'{PBC_KEY}_'))
    relationship_targets = tuple(rel.get('target_table') for table in OWNED_SCHEMA.get('tables', ()) for rel in table.get('relationships', ()) if rel.get('target_table'))
    cross_pbc_relationships = tuple(target for target in relationship_targets if not target.startswith(f'{PBC_KEY}_'))
    return {'ok': bool(schema_tables) and bool(model_tables) and not missing_models and not external_models and not cross_pbc_relationships, 'pbc': PBC_KEY, 'schema_tables': schema_tables, 'model_tables': model_tables, 'missing_models': missing_models, 'external_models': external_models, 'cross_pbc_relationships': cross_pbc_relationships, 'relationship_targets': relationship_targets, 'side_effects': ()}


def instantiate_model(table_name, values=None):
    model = next((item for item in MODELS if item['table'] == table_name), None)
    if model is None:
        return {'ok': False, 'reason': 'unknown_model', 'table': table_name, 'side_effects': ()}
    supplied = dict(values or {})
    fields = tuple(field['name'] if isinstance(field, dict) else field for field in model.get('fields', ()))
    return {'ok': table_name.startswith(f'{PBC_KEY}_') and bool(fields), 'pbc': PBC_KEY, 'model': model['class_name'], 'table': table_name, 'fields': fields, 'payload': {field: supplied.get(field) for field in fields}, 'side_effects': ()}


def smoke_test():
    manifest = model_manifest()
    first_table = manifest['model_tables'][0] if manifest['model_tables'] else None
    instance = instantiate_model(first_table, {'id': 1}) if first_table else {'ok': False}
    return {'ok': manifest['ok'] and instance.get('ok') is True, 'manifest': manifest, 'instance': instance, 'side_effects': ()}
