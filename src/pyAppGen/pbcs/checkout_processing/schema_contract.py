"""Generated owned schema evidence for the checkout_processing PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.checkout-processing-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'cart', 'owned_table': 'checkout_processing_cart', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'cart_line', 'owned_table': 'checkout_processing_cart_line', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'cart_id', 'type': 'integer', 'required': True, 'references': 'checkout_processing_cart.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'cart_id', 'target_table': 'checkout_processing_cart', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'checkout_session', 'owned_table': 'checkout_processing_checkout_session', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'cart_id', 'type': 'integer', 'required': True, 'references': 'checkout_processing_cart.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'cart_id', 'target_table': 'checkout_processing_cart', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'promotion_redemption', 'owned_table': 'checkout_processing_promotion_redemption', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'cart_id', 'type': 'integer', 'required': True, 'references': 'checkout_processing_cart.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'cart_id', 'target_table': 'checkout_processing_cart', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': ({'from': 'cart_line.cart_id', 'to': 'cart.cart_id', 'type': 'owned_child'}, {'from': 'promotion_redemption.cart_id', 'to': 'cart.cart_id', 'type': 'owned_discount'}, {'from': 'checkout_session.cart_id', 'to': 'cart.cart_id', 'type': 'owned_session'}, {'from': 'checkout_pricing_handoff.session_id', 'to': 'checkout_session.session_id', 'type': 'owned_handoff'}, {'from': 'checkout_tax_handoff.session_id', 'to': 'checkout_session.session_id', 'type': 'owned_handoff'}, {'from': 'checkout_inventory_reservation_handoff.session_id', 'to': 'checkout_session.session_id', 'type': 'owned_handoff'}, {'from': 'checkout_payment_intent_handoff.session_id', 'to': 'checkout_session.session_id', 'type': 'owned_handoff'}, {'from': 'checkout_risk_screen.session_id', 'to': 'checkout_session.session_id', 'type': 'owned_risk'}, {'from': 'checkout_address_validation.cart_id', 'to': 'cart.cart_id', 'type': 'owned_validation'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'CheckoutProcessingCart', 'table': 'checkout_processing_cart', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'CheckoutProcessingCartLine', 'table': 'checkout_processing_cart_line', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'cart_id', 'type': 'integer', 'required': True, 'references': 'checkout_processing_cart.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'cart_id', 'target_table': 'checkout_processing_cart', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'CheckoutProcessingCheckoutSession', 'table': 'checkout_processing_checkout_session', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'cart_id', 'type': 'integer', 'required': True, 'references': 'checkout_processing_cart.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'cart_id', 'target_table': 'checkout_processing_cart', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'CheckoutProcessingPromotionRedemption', 'table': 'checkout_processing_promotion_redemption', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'cart_id', 'type': 'integer', 'required': True, 'references': 'checkout_processing_cart.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'cart_id', 'target_table': 'checkout_processing_cart', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'runtime_tables': ('checkout_processing_appgen_outbox_event', 'checkout_processing_appgen_inbox_event', 'checkout_processing_dead_letter_event'), 'shared_table_access': False, 'pbc': 'checkout_processing', 'owned_tables': ('checkout_processing_cart', 'checkout_processing_cart_line', 'checkout_processing_checkout_session', 'checkout_processing_promotion_redemption'), 'database_backends': ('postgresql',)}


def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract['pbc']
    owned_tables = tuple(contract.get('owned_tables', ()))
    raw_model_tables = tuple(
        model.get('table')
        for model in contract.get('models', ())
        if isinstance(model, dict) and model.get('table')
    )
    model_tables = tuple(
        table if table.startswith(f'{pbc}_') else f'{pbc}_{table}'
        for table in raw_model_tables
    )
    migration_paths = tuple(contract.get('migrations', ()))
    allowed_backends = {'postgresql', 'mysql', 'mariadb'}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f'{pbc}_'))
    missing_models = tuple(table for table in owned_tables if model_tables and table not in model_tables)
    invalid_backends = tuple(
        backend for backend in contract.get('database_backends', ()) if backend not in allowed_backends
    )
    return {
        'ok': contract.get('ok') is True
        and bool(owned_tables)
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and contract.get('shared_table_access') is False,
        'pbc': pbc,
        'owned_tables': owned_tables,
        'raw_model_tables': raw_model_tables,
        'model_tables': model_tables,
        'migration_paths': migration_paths,
        'invalid_tables': invalid_tables,
        'missing_models': missing_models,
        'invalid_backends': invalid_backends,
        'side_effects': (),
    }


def smoke_test():
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
