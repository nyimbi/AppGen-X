"""Model contracts for agri_supply_chain_traceability."""
from __future__ import annotations

from .schema_contract import build_schema_contract


PBC_KEY = 'agri_supply_chain_traceability'
_ENTITY_TABLES = {
    'farm_lot': f'{PBC_KEY}_farm_lot',
    'input_batch': f'{PBC_KEY}_input_batch',
    'certification': f'{PBC_KEY}_certification',
    'storage_event': f'{PBC_KEY}_storage_event',
    'transport_leg': f'{PBC_KEY}_transport_leg',
    'recall_link': f'{PBC_KEY}_recall_link',
    'provenance_proof': f'{PBC_KEY}_provenance_proof',
}
_REQUIRED_FIELDS = {
    'farm_lot': ('id', 'tenant', 'site_id', 'commodity', 'season'),
    'input_batch': ('id', 'tenant', 'farm_lot_id', 'supplier', 'applied_at'),
    'certification': ('id', 'tenant', 'covered_farm_lot_ids', 'valid_from', 'valid_to'),
    'storage_event': ('id', 'tenant', 'subject_ids', 'farm_lot_id', 'status'),
    'transport_leg': ('id', 'tenant', 'subject_ids', 'farm_lot_id', 'seal_state'),
    'recall_link': ('id', 'tenant', 'subject_ids', 'recall_status'),
    'provenance_proof': ('id', 'tenant', 'subject_ids', 'source_farm_lot_ids'),
}
_STATUS_VALUES = {
    'farm_lot': ('active', 'retired'),
    'input_batch': ('recorded', 'superseded'),
    'certification': ('active', 'suspended', 'expired'),
    'storage_event': ('recorded', 'released', 'exception'),
    'transport_leg': ('planned', 'in_transit', 'blocked'),
    'recall_link': ('draft', 'active', 'closed'),
    'provenance_proof': ('verified', 'superseded'),
}


def model_contracts():
    return build_schema_contract()['models']


def model_manifest() -> dict:
    schema = build_schema_contract()
    schema_index = {item['table']: item for item in schema['models']}
    models = tuple(
        {
            'entity_type': entity_type,
            'table': table,
            'fields': schema_index[table]['fields'],
            'required_fields': _REQUIRED_FIELDS[entity_type],
            'allowed_statuses': _STATUS_VALUES[entity_type],
        }
        for entity_type, table in _ENTITY_TABLES.items()
    )
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'models': models,
        'owned_tables': schema['owned_tables'],
        'database_backends': schema['database_backends'],
        'side_effects': (),
    }


def database_model_contract() -> dict:
    schema = build_schema_contract()
    manifest = model_manifest()
    return {
        'ok': manifest['ok'],
        'pbc': PBC_KEY,
        'database_backends': schema['database_backends'],
        'models': manifest['models'],
        'migrations': schema['migrations'],
        'shared_table_access': False,
        'side_effects': (),
    }


def model_for_entity(entity_type: str) -> dict | None:
    for model in model_manifest()['models']:
        if model['entity_type'] == entity_type:
            return model
    return None


def smoke_test() -> dict:
    manifest = model_manifest()
    return {
        'ok': manifest['ok'] and database_model_contract()['ok'] and model_for_entity('farm_lot')['table'] == f'{PBC_KEY}_farm_lot',
        'manifest': manifest,
        'side_effects': (),
    }
