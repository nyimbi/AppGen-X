"""Generated release evidence for the loyalty_rewards PBC."""

import importlib.util
from pathlib import Path


RELEASE_EVIDENCE = {'format': 'appgen.loyalty-rewards-release-evidence.v1', 'ok': True, 'checks': ({'id': 'owned_schema_coverage', 'ok': True}, {'id': 'runtime_appgen_x_tables', 'ok': True}, {'id': 'migration_and_model_artifacts', 'ok': True}, {'id': 'service_route_event_handler_ui_artifacts', 'ok': True}, {'id': 'commands_permissions_configuration', 'ok': True}, {'id': 'idempotent_handlers_retry_dead_letter', 'ok': True}, {'id': 'backend_allowlist_only', 'ok': True}, {'id': 'no_shared_tables_and_appgen_x_only_eventing', 'ok': True}, {'id': 'permissions_cover_release_queries', 'ok': True}), 'schema': {'format': 'appgen.loyalty-rewards-owned-schema-contract.v1', 'ok': True, 'tables': ({'table': 'reward_account', 'fields': ('account_id', 'tenant', 'customer_id', 'currency', 'region', 'tier', 'status', 'balance', 'lifetime_points', 'liability_amount', 'audit_proof'), 'primary_key': ('account_id',), 'owned_by': 'loyalty_rewards'}, {'table': 'points_ledger', 'fields': ('ledger_id', 'account_id', 'tenant', 'entry_type', 'points', 'source', 'source_ref', 'audit_proof'), 'primary_key': ('ledger_id',), 'owned_by': 'loyalty_rewards'}, {'table': 'earning_rule', 'fields': ('earning_rule_id', 'tenant', 'name', 'activity_type', 'points_per_currency_unit', 'tier_multipliers', 'status', 'compiled_hash'), 'primary_key': ('earning_rule_id',), 'owned_by': 'loyalty_rewards'}, {'table': 'redemption', 'fields': ('redemption_id', 'account_id', 'tenant', 'points', 'order_id', 'status', 'monetary_value', 'audit_proof'), 'primary_key': ('redemption_id',), 'owned_by': 'loyalty_rewards'}), 'relationships': ({'from_table': 'points_ledger', 'from_field': 'account_id', 'to_table': 'reward_account', 'to_field': 'account_id', 'type': 'owned_reference'}, {'from_table': 'redemption', 'from_field': 'account_id', 'to_table': 'reward_account', 'to_field': 'account_id', 'type': 'owned_reference'}, {'from_table': 'reward_account', 'from_field': 'tier', 'to_table': 'earning_rule', 'to_field': 'status', 'type': 'runtime_policy_reference'}), 'runtime_tables': ({'table': 'loyalty_rewards_appgen_outbox_event', 'fields': ('event_id', 'event_type', 'tenant', 'payload', 'contract', 'idempotency_key', 'retry_policy', 'audit_hash'), 'event_contract': 'AppGen-X', 'owned_by': 'loyalty_rewards'}, {'table': 'loyalty_rewards_appgen_inbox_event', 'fields': ('event_id', 'event_type', 'payload', 'handler', 'idempotency_key', 'attempts', 'status'), 'event_contract': 'AppGen-X', 'owned_by': 'loyalty_rewards'}, {'table': 'loyalty_rewards_dead_letter_event', 'fields': ('event_id', 'event_type', 'payload', 'handler', 'idempotency_key', 'attempts', 'reason'), 'event_contract': 'AppGen-X', 'owned_by': 'loyalty_rewards'}), 'migrations': ({'path': 'pbcs/loyalty_rewards/migrations/001_reward_account.sql', 'operation': 'create_owned_table', 'table': 'reward_account', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/loyalty_rewards/migrations/002_points_ledger.sql', 'operation': 'create_owned_table', 'table': 'points_ledger', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/loyalty_rewards/migrations/003_earning_rule.sql', 'operation': 'create_owned_table', 'table': 'earning_rule', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/loyalty_rewards/migrations/004_redemption.sql', 'operation': 'create_owned_table', 'table': 'redemption', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}), 'models': ({'class_name': 'RewardAccount', 'table': 'reward_account', 'fields': ('account_id', 'tenant', 'customer_id', 'currency', 'region', 'tier', 'status', 'balance', 'lifetime_points', 'liability_amount', 'audit_proof'), 'module': 'pyAppGen.pbcs.loyalty_rewards.models.reward_account'}, {'class_name': 'PointsLedger', 'table': 'points_ledger', 'fields': ('ledger_id', 'account_id', 'tenant', 'entry_type', 'points', 'source', 'source_ref', 'audit_proof'), 'module': 'pyAppGen.pbcs.loyalty_rewards.models.points_ledger'}, {'class_name': 'EarningRule', 'table': 'earning_rule', 'fields': ('earning_rule_id', 'tenant', 'name', 'activity_type', 'points_per_currency_unit', 'tier_multipliers', 'status', 'compiled_hash'), 'module': 'pyAppGen.pbcs.loyalty_rewards.models.earning_rule'}, {'class_name': 'Redemption', 'table': 'redemption', 'fields': ('redemption_id', 'account_id', 'tenant', 'points', 'order_id', 'status', 'monetary_value', 'audit_proof'), 'module': 'pyAppGen.pbcs.loyalty_rewards.models.redemption'}), 'generated_artifacts': {'migrations': ('pbcs/loyalty_rewards/migrations/001_reward_account.sql', 'pbcs/loyalty_rewards/migrations/002_points_ledger.sql', 'pbcs/loyalty_rewards/migrations/003_earning_rule.sql', 'pbcs/loyalty_rewards/migrations/004_redemption.sql'), 'models': ('pyAppGen.pbcs.loyalty_rewards.models.reward_account', 'pyAppGen.pbcs.loyalty_rewards.models.points_ledger', 'pyAppGen.pbcs.loyalty_rewards.models.earning_rule', 'pyAppGen.pbcs.loyalty_rewards.models.redemption')}, 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False}, 'service': {'format': 'appgen.loyalty-rewards-service-contract.v1', 'ok': True, 'transaction_boundary': 'loyalty_rewards_owned_datastore_plus_appgen_outbox', 'command_methods': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'register_earning_rule', 'enroll_member', 'receive_event', 'issue_points', 'adjust_points', 'create_redemption', 'expire_points', 'verify_owned_table_boundary'), 'query_methods': ('build_workbench_view', 'build_api_contract', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract'), 'mutates_only': ('reward_account', 'points_ledger', 'earning_rule', 'redemption'), 'runtime_tables': ('loyalty_rewards_appgen_outbox_event', 'loyalty_rewards_appgen_inbox_event', 'loyalty_rewards_dead_letter_event'), 'permission_requirements': {'configure_runtime': 'loyalty_rewards.configure', 'set_parameter': 'loyalty_rewards.configure', 'register_rule': 'loyalty_rewards.configure', 'register_schema_extension': 'loyalty_rewards.configure', 'register_earning_rule': 'loyalty_rewards.configure', 'enroll_member': 'loyalty_rewards.account.write', 'receive_event': 'loyalty_rewards.event.consume', 'issue_points': 'loyalty_rewards.points.write', 'adjust_points': 'loyalty_rewards.points.write', 'create_redemption': 'loyalty_rewards.redemption.write', 'expire_points': 'loyalty_rewards.points.write', 'build_schema_contract': 'loyalty_rewards.audit', 'build_service_contract': 'loyalty_rewards.audit', 'build_release_evidence': 'loyalty_rewards.audit', 'verify_owned_table_boundary': 'loyalty_rewards.audit'}, 'configuration_schema': {'required_fields': ('database_backend', 'event_topic', 'retry_limit', 'default_currency', 'supported_currencies', 'supported_regions', 'tier_calendar', 'default_timezone', 'liability_mode', 'workbench_limit'), 'allowed_database_backends': ('postgresql', 'mysql', 'mariadb'), 'event_contract': 'AppGen-X', 'required_event_topic': 'appgen.loyalty_rewards.events', 'stream_engine_picker_visible': False}, 'idempotent_handlers': ({'event_type': 'PaymentCaptured', 'idempotency_key': 'event_id', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'dead_letter_table': 'loyalty_rewards_dead_letter_event', 'retry_limit_source': 'configuration.retry_limit', 'event_contract': 'AppGen-X'}, {'event_type': 'PromotionApplied', 'idempotency_key': 'event_id', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'dead_letter_table': 'loyalty_rewards_dead_letter_event', 'retry_limit_source': 'configuration.retry_limit', 'event_contract': 'AppGen-X'}), 'retry_dead_letter': {'retry_limit_source': 'configuration.retry_limit', 'outbox_table': 'loyalty_rewards_appgen_outbox_event', 'inbox_table': 'loyalty_rewards_appgen_inbox_event', 'dead_letter_table': 'loyalty_rewards_dead_letter_event', 'simulate_failure_supported': True}, 'generated_artifacts': {'services': ({'name': 'configure_runtime', 'path': 'pbcs/loyalty_rewards/services/configure_runtime.py'}, {'name': 'set_parameter', 'path': 'pbcs/loyalty_rewards/services/set_parameter.py'}, {'name': 'register_rule', 'path': 'pbcs/loyalty_rewards/services/register_rule.py'}, {'name': 'register_schema_extension', 'path': 'pbcs/loyalty_rewards/services/register_schema_extension.py'}, {'name': 'register_earning_rule', 'path': 'pbcs/loyalty_rewards/services/register_earning_rule.py'}, {'name': 'enroll_member', 'path': 'pbcs/loyalty_rewards/services/enroll_member.py'}, {'name': 'receive_event', 'path': 'pbcs/loyalty_rewards/services/receive_event.py'}, {'name': 'issue_points', 'path': 'pbcs/loyalty_rewards/services/issue_points.py'}, {'name': 'adjust_points', 'path': 'pbcs/loyalty_rewards/services/adjust_points.py'}, {'name': 'create_redemption', 'path': 'pbcs/loyalty_rewards/services/create_redemption.py'}, {'name': 'expire_points', 'path': 'pbcs/loyalty_rewards/services/expire_points.py'}, {'name': 'verify_owned_table_boundary', 'path': 'pbcs/loyalty_rewards/services/verify_owned_table_boundary.py'}), 'routes': ({'route': 'POST /reward-accounts', 'path': 'pbcs/loyalty_rewards/routes/reward_accounts.py'}, {'route': 'POST /points', 'path': 'pbcs/loyalty_rewards/routes/points.py'}, {'route': 'POST /points/adjustments', 'path': 'pbcs/loyalty_rewards/routes/points_adjustments.py'}, {'route': 'POST /redemptions', 'path': 'pbcs/loyalty_rewards/routes/redemptions.py'}, {'route': 'POST /loyalty-rewards/events/inbox', 'path': 'pbcs/loyalty_rewards/routes/loyalty_rewards_events_inbox.py'}, {'route': 'GET /reward-accounts', 'path': 'pbcs/loyalty_rewards/routes/reward_accounts.py'}, {'route': 'GET /loyalty-rewards/schema-contract', 'path': 'pbcs/loyalty_rewards/routes/loyalty_rewards_schema_contract.py'}, {'route': 'GET /loyalty-rewards/service-contract', 'path': 'pbcs/loyalty_rewards/routes/loyalty_rewards_service_contract.py'}, {'route': 'GET /loyalty-rewards/release-evidence', 'path': 'pbcs/loyalty_rewards/routes/loyalty_rewards_release_evidence.py'}), 'events': ({'direction': 'consumes', 'event_type': 'PaymentCaptured', 'topic': 'appgen.loyalty_rewards.events'}, {'direction': 'consumes', 'event_type': 'PromotionApplied', 'topic': 'appgen.loyalty_rewards.events'}, {'direction': 'emits', 'event_type': 'RewardBalanceChanged', 'topic': 'appgen.loyalty_rewards.events'}, {'direction': 'emits', 'event_type': 'CustomerSegmentUpdated', 'topic': 'appgen.loyalty_rewards.events'}), 'handlers': ({'event_type': 'PaymentCaptured', 'path': 'pbcs/loyalty_rewards/handlers/paymentcaptured.py', 'idempotency_key': 'event_id', 'dead_letter_table': 'loyalty_rewards_dead_letter_event'}, {'event_type': 'PromotionApplied', 'path': 'pbcs/loyalty_rewards/handlers/promotionapplied.py', 'idempotency_key': 'event_id', 'dead_letter_table': 'loyalty_rewards_dead_letter_event'}), 'ui': ({'fragment': 'LoyaltyRewardsWorkbench', 'path': 'pbcs/loyalty_rewards/ui/LoyaltyRewardsWorkbench.tsx'}, {'fragment': 'RewardAccountRegistry', 'path': 'pbcs/loyalty_rewards/ui/RewardAccountRegistry.tsx'}, {'fragment': 'PointsLedgerPanel', 'path': 'pbcs/loyalty_rewards/ui/PointsLedgerPanel.tsx'}, {'fragment': 'EarningRuleStudio', 'path': 'pbcs/loyalty_rewards/ui/EarningRuleStudio.tsx'}, {'fragment': 'RedemptionConsole', 'path': 'pbcs/loyalty_rewards/ui/RedemptionConsole.tsx'}, {'fragment': 'TierQualificationBoard', 'path': 'pbcs/loyalty_rewards/ui/TierQualificationBoard.tsx'}, {'fragment': 'ReferralAndPartnerPanel', 'path': 'pbcs/loyalty_rewards/ui/ReferralAndPartnerPanel.tsx'}, {'fragment': 'ExpirationLiabilityPanel', 'path': 'pbcs/loyalty_rewards/ui/ExpirationLiabilityPanel.tsx'}, {'fragment': 'RewardsFraudReviewQueue', 'path': 'pbcs/loyalty_rewards/ui/RewardsFraudReviewQueue.tsx'}, {'fragment': 'RewardsRuleStudio', 'path': 'pbcs/loyalty_rewards/ui/RewardsRuleStudio.tsx'}, {'fragment': 'RewardsParameterConsole', 'path': 'pbcs/loyalty_rewards/ui/RewardsParameterConsole.tsx'}, {'fragment': 'RewardsConfigurationPanel', 'path': 'pbcs/loyalty_rewards/ui/RewardsConfigurationPanel.tsx'}, {'fragment': 'RewardsEventOutbox', 'path': 'pbcs/loyalty_rewards/ui/RewardsEventOutbox.tsx'}, {'fragment': 'RewardsDeadLetterQueue', 'path': 'pbcs/loyalty_rewards/ui/RewardsDeadLetterQueue.tsx'})}, 'external_dependencies': {'apis': ('payment_projection', 'promotion_projection', 'customer_segment_projection'), 'events': ('PaymentCaptured', 'PromotionApplied'), 'api_projections': ('payment_projection', 'promotion_projection', 'customer_segment_projection'), 'shared_tables': ()}}, 'api': {'format': 'appgen.loyalty-rewards-api-contract.v1', 'ok': True, 'routes': ({'route': 'POST /reward-accounts', 'command': 'enroll_member', 'owned_tables': ('reward_account',), 'emits': (), 'requires_permission': 'loyalty_rewards.account.write', 'idempotency_key': 'account_id'}, {'route': 'POST /points', 'command': 'issue_points', 'owned_tables': ('points_ledger', 'reward_account'), 'emits': ('RewardBalanceChanged', 'CustomerSegmentUpdated'), 'requires_permission': 'loyalty_rewards.points.write', 'idempotency_key': 'ledger_id'}, {'route': 'POST /points/adjustments', 'command': 'adjust_points', 'owned_tables': ('points_ledger', 'reward_account'), 'emits': ('RewardBalanceChanged', 'CustomerSegmentUpdated'), 'requires_permission': 'loyalty_rewards.points.write', 'idempotency_key': 'ledger_id'}, {'route': 'POST /redemptions', 'command': 'create_redemption', 'owned_tables': ('redemption', 'points_ledger', 'reward_account'), 'emits': ('RewardBalanceChanged',), 'requires_permission': 'loyalty_rewards.redemption.write', 'idempotency_key': 'redemption_id'}, {'route': 'POST /loyalty-rewards/events/inbox', 'command': 'receive_event', 'owned_tables': (), 'consumes': ('PaymentCaptured', 'PromotionApplied'), 'requires_permission': 'loyalty_rewards.event.consume', 'idempotency_key': 'event_id'}, {'route': 'GET /reward-accounts', 'query': 'build_workbench_view', 'owned_tables': ('reward_account', 'points_ledger', 'earning_rule', 'redemption'), 'requires_permission': 'loyalty_rewards.audit'}, {'route': 'GET /loyalty-rewards/schema-contract', 'query': 'build_schema_contract', 'owned_tables': ('reward_account', 'points_ledger', 'earning_rule', 'redemption'), 'requires_permission': 'loyalty_rewards.audit'}, {'route': 'GET /loyalty-rewards/service-contract', 'query': 'build_service_contract', 'owned_tables': ('reward_account', 'points_ledger', 'earning_rule', 'redemption'), 'requires_permission': 'loyalty_rewards.audit'}, {'route': 'GET /loyalty-rewards/release-evidence', 'query': 'build_release_evidence', 'owned_tables': ('reward_account', 'points_ledger', 'earning_rule', 'redemption'), 'requires_permission': 'loyalty_rewards.audit'}), 'declared_catalog_routes': ('POST /points', 'POST /redemptions', 'GET /reward-accounts'), 'owned_tables': ('reward_account', 'points_ledger', 'earning_rule', 'redemption'), 'runtime_tables': ('loyalty_rewards_appgen_outbox_event', 'loyalty_rewards_appgen_inbox_event', 'loyalty_rewards_dead_letter_event'), 'emits': ('RewardBalanceChanged', 'CustomerSegmentUpdated'), 'consumes': ('PaymentCaptured', 'PromotionApplied'), 'database_backends': ('postgresql', 'mysql', 'mariadb'), 'permissions': ('loyalty_rewards.account.write', 'loyalty_rewards.audit', 'loyalty_rewards.configure', 'loyalty_rewards.event.consume', 'loyalty_rewards.points.write', 'loyalty_rewards.redemption.write'), 'shared_table_access': False, 'event_contract': 'AppGen-X', 'required_event_topic': 'appgen.loyalty_rewards.events', 'stream_engine_picker_visible': False}, 'permissions': {'format': 'appgen.loyalty-rewards-permissions.v1', 'ok': True, 'permissions': ('loyalty_rewards.account.write', 'loyalty_rewards.points.write', 'loyalty_rewards.redemption.write', 'loyalty_rewards.event.consume', 'loyalty_rewards.configure', 'loyalty_rewards.audit'), 'action_permissions': {'enroll_member': 'loyalty_rewards.account.write', 'issue_points': 'loyalty_rewards.points.write', 'adjust_points': 'loyalty_rewards.points.write', 'expire_points': 'loyalty_rewards.points.write', 'create_redemption': 'loyalty_rewards.redemption.write', 'receive_event': 'loyalty_rewards.event.consume', 'register_earning_rule': 'loyalty_rewards.configure', 'register_rule': 'loyalty_rewards.configure', 'register_schema_extension': 'loyalty_rewards.configure', 'set_parameter': 'loyalty_rewards.configure', 'configure_runtime': 'loyalty_rewards.configure', 'build_api_contract': 'loyalty_rewards.audit', 'build_schema_contract': 'loyalty_rewards.audit', 'build_service_contract': 'loyalty_rewards.audit', 'build_release_evidence': 'loyalty_rewards.audit', 'permissions_contract': 'loyalty_rewards.audit', 'build_workbench_view': 'loyalty_rewards.audit', 'verify_owned_table_boundary': 'loyalty_rewards.audit'}}, 'blocking_gaps': (), 'pbc': 'loyalty_rewards'}


def _load_sibling_module(module_name):
    """Load a sibling generated module when this file is imported directly."""
    path = Path(__file__).with_name(f'{module_name}.py')
    spec = importlib.util.spec_from_file_location(f'_pbc_release_{module_name}', path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(module_name)
    spec.loader.exec_module(module)
    return module


def _build_schema_contract():
    try:
        from .schema_contract import build_schema_contract
    except ImportError:
        return _load_sibling_module('schema_contract').build_schema_contract()
    return build_schema_contract()


def _build_service_contract():
    try:
        from .service_contract import build_service_contract
    except ImportError:
        return _load_sibling_module('service_contract').build_service_contract()
    return build_service_contract()


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    evidence = dict(RELEASE_EVIDENCE)
    evidence.setdefault('schema', _build_schema_contract())
    evidence.setdefault('service', _build_service_contract())
    evidence.setdefault('pbc', 'loyalty_rewards')
    return evidence


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ('schema', 'service', 'api', 'permissions', 'ui', 'events')
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get('checks', ()))
    return {
        'ok': evidence.get('ok') is True and bool(checks),
        'pbc': 'loyalty_rewards',
        'format': evidence.get('format'),
        'sections': sections,
        'checks': checks,
        'blocking_gaps': tuple(evidence.get('blocking_gaps', ())),
        'required_sections': ('schema', 'service'),
        'side_effects': (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest['required_sections'] if section not in manifest['sections'])
    failed_checks = tuple(check for check in manifest['checks'] if check.get('ok') is not True)
    schema = evidence.get('schema', {}) if isinstance(evidence.get('schema'), dict) else {}
    service = evidence.get('service', {}) if isinstance(evidence.get('service'), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ('schema_shared_table_access', schema.get('shared_table_access') is not False),
            ('service_shared_table_access', service.get('shared_table_access') is True),
            ('service_missing_command_methods', not bool(service.get('command_methods'))),
        )
        if failed
    )
    return {
        'ok': manifest['ok']
        and evidence.get('pbc') == manifest['pbc']
        and not manifest['blocking_gaps']
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        'pbc': 'loyalty_rewards',
        'manifest': manifest,
        'missing_sections': missing_sections,
        'failed_checks': failed_checks,
        'boundary_gaps': boundary_gaps,
        'side_effects': (),
    }


def smoke_test():
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        'ok': validation['ok'] and evidence.get('ok') is True,
        'validation': validation,
        'evidence': evidence,
        'side_effects': (),
    }
