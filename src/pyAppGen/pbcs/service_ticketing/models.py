"""Owned model metadata for the service_ticketing PBC."""

PBC_KEY = 'service_ticketing'
OWNED_SCHEMA = {'schema': 'service_ticketing', 'table_prefix': 'service_ticketing_', 'tables': ({'logical_table': 'support_ticket', 'owned_table': 'service_ticketing_support_ticket', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'sla_policy', 'owned_table': 'service_ticketing_sla_policy', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'support_ticket_id', 'type': 'integer', 'required': True, 'references': 'service_ticketing_support_ticket.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'case_assignment', 'owned_table': 'service_ticketing_case_assignment', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'support_ticket_id', 'type': 'integer', 'required': True, 'references': 'service_ticketing_support_ticket.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'escalation_event', 'owned_table': 'service_ticketing_escalation_event', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'support_ticket_id', 'type': 'integer', 'required': True, 'references': 'service_ticketing_support_ticket.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': ({'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'}, {'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'}, {'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'}), 'allowed_external_access': 'apis_events_or_projections_only'}
MODELS = ({'class_name': 'ServiceTicketingSupportTicket', 'table': 'service_ticketing_support_ticket', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'ServiceTicketingSlaPolicy', 'table': 'service_ticketing_sla_policy', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'support_ticket_id', 'type': 'integer', 'required': True, 'references': 'service_ticketing_support_ticket.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'ServiceTicketingCaseAssignment', 'table': 'service_ticketing_case_assignment', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'support_ticket_id', 'type': 'integer', 'required': True, 'references': 'service_ticketing_support_ticket.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'ServiceTicketingEscalationEvent', 'table': 'service_ticketing_escalation_event', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'support_ticket_id', 'type': 'integer', 'required': True, 'references': 'service_ticketing_support_ticket.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'support_ticket_id', 'target_table': 'service_ticketing_support_ticket', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)})


def model_manifest():
    """Return executable owned model/table alignment evidence."""
    schema_tables = tuple(table['owned_table'] for table in OWNED_SCHEMA.get('tables', ()))
    model_tables = tuple(model['table'] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f'{PBC_KEY}_'))
    relationship_targets = tuple(
        relationship.get('target_table')
        for table in OWNED_SCHEMA.get('tables', ())
        for relationship in table.get('relationships', ())
        if relationship.get('target_table')
    )
    cross_pbc_relationships = tuple(
        target for target in relationship_targets if not target.startswith(f'{PBC_KEY}_')
    )
    return {
        'ok': bool(schema_tables)
        and bool(model_tables)
        and not missing_models
        and not external_models
        and not cross_pbc_relationships,
        'pbc': PBC_KEY,
        'schema_tables': schema_tables,
        'model_tables': model_tables,
        'missing_models': missing_models,
        'external_models': external_models,
        'cross_pbc_relationships': cross_pbc_relationships,
        'relationship_targets': relationship_targets,
        'side_effects': (),
    }


def instantiate_model(table_name, values=None):
    """Create a side-effect-free model payload for validation and tests."""
    model = next((item for item in MODELS if item['table'] == table_name), None)
    if model is None:
        return {'ok': False, 'reason': 'unknown_model', 'table': table_name, 'side_effects': ()}
    supplied = dict(values or {})
    fields = tuple(field['name'] for field in model.get('fields', ()))
    payload = {field: supplied.get(field) for field in fields}
    return {
        'ok': table_name.startswith(f'{PBC_KEY}_') and bool(fields),
        'pbc': PBC_KEY,
        'model': model['class_name'],
        'table': table_name,
        'fields': fields,
        'payload': payload,
        'side_effects': (),
    }


def smoke_test():
    """Exercise model alignment and model payload creation."""
    manifest = model_manifest()
    first_table = manifest['model_tables'][0] if manifest['model_tables'] else None
    instance = instantiate_model(first_table, {'id': 1}) if first_table else {'ok': False}
    return {
        'ok': manifest['ok'] and instance.get('ok') is True,
        'manifest': manifest,
        'instance': instance,
        'side_effects': (),
    }
