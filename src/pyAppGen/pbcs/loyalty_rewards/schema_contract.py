"""Generated owned schema evidence for the loyalty_rewards PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.loyalty-rewards-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'reward_account', 'owned_table': 'loyalty_rewards_reward_account', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'points_ledger', 'owned_table': 'loyalty_rewards_points_ledger', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'reward_account_id', 'type': 'integer', 'required': True, 'references': 'loyalty_rewards_reward_account.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'reward_account_id', 'target_table': 'loyalty_rewards_reward_account', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'earning_rule', 'owned_table': 'loyalty_rewards_earning_rule', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'reward_account_id', 'type': 'integer', 'required': True, 'references': 'loyalty_rewards_reward_account.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'reward_account_id', 'target_table': 'loyalty_rewards_reward_account', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'redemption', 'owned_table': 'loyalty_rewards_redemption', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'reward_account_id', 'type': 'integer', 'required': True, 'references': 'loyalty_rewards_reward_account.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'reward_account_id', 'target_table': 'loyalty_rewards_reward_account', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': ({'from_table': 'points_ledger', 'from_field': 'account_id', 'to_table': 'reward_account', 'to_field': 'account_id', 'type': 'owned_reference'}, {'from_table': 'redemption', 'from_field': 'account_id', 'to_table': 'reward_account', 'to_field': 'account_id', 'type': 'owned_reference'}, {'from_table': 'reward_account', 'from_field': 'tier', 'to_table': 'earning_rule', 'to_field': 'status', 'type': 'runtime_policy_reference'}), 'runtime_tables': ({'table': 'loyalty_rewards_appgen_outbox_event', 'fields': ('event_id', 'event_type', 'tenant', 'payload', 'contract', 'idempotency_key', 'retry_policy', 'audit_hash'), 'event_contract': 'AppGen-X', 'owned_by': 'loyalty_rewards'}, {'table': 'loyalty_rewards_appgen_inbox_event', 'fields': ('event_id', 'event_type', 'payload', 'handler', 'idempotency_key', 'attempts', 'status'), 'event_contract': 'AppGen-X', 'owned_by': 'loyalty_rewards'}, {'table': 'loyalty_rewards_dead_letter_event', 'fields': ('event_id', 'event_type', 'payload', 'handler', 'idempotency_key', 'attempts', 'reason'), 'event_contract': 'AppGen-X', 'owned_by': 'loyalty_rewards'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'LoyaltyRewardsRewardAccount', 'table': 'loyalty_rewards_reward_account', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'LoyaltyRewardsPointsLedger', 'table': 'loyalty_rewards_points_ledger', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'reward_account_id', 'type': 'integer', 'required': True, 'references': 'loyalty_rewards_reward_account.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'reward_account_id', 'target_table': 'loyalty_rewards_reward_account', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'LoyaltyRewardsEarningRule', 'table': 'loyalty_rewards_earning_rule', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'reward_account_id', 'type': 'integer', 'required': True, 'references': 'loyalty_rewards_reward_account.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'reward_account_id', 'target_table': 'loyalty_rewards_reward_account', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'LoyaltyRewardsRedemption', 'table': 'loyalty_rewards_redemption', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'reward_account_id', 'type': 'integer', 'required': True, 'references': 'loyalty_rewards_reward_account.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'reward_account_id', 'target_table': 'loyalty_rewards_reward_account', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'generated_artifacts': {'migrations': ('pbcs/loyalty_rewards/migrations/001_reward_account.sql', 'pbcs/loyalty_rewards/migrations/002_points_ledger.sql', 'pbcs/loyalty_rewards/migrations/003_earning_rule.sql', 'pbcs/loyalty_rewards/migrations/004_redemption.sql'), 'models': ('pyAppGen.pbcs.loyalty_rewards.models.reward_account', 'pyAppGen.pbcs.loyalty_rewards.models.points_ledger', 'pyAppGen.pbcs.loyalty_rewards.models.earning_rule', 'pyAppGen.pbcs.loyalty_rewards.models.redemption')}, 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'pbc': 'loyalty_rewards', 'owned_tables': ('loyalty_rewards_reward_account', 'loyalty_rewards_points_ledger', 'loyalty_rewards_earning_rule', 'loyalty_rewards_redemption'), 'database_backends': ('postgresql',)}


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
