"""Generated contract smoke tests for subscription_billing."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'subscription_billing'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'subscription_billing'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'subscription_billing'
    assert RELEASE_EVIDENCE['ok'] is True


    release_manifest = release_evidence.release_readiness_manifest()
    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()
    assert release_manifest['ok'] is True
    assert release_validation['ok'] is True
    assert release_smoke['ok'] is True
    assert not release_manifest['blocking_gaps']
    assert not release_validation['missing_sections']
    assert not release_validation['failed_checks']
    assert not release_validation['boundary_gaps']
    assert not release_manifest['side_effects']
    assert not release_validation['side_effects']
    assert not release_smoke['side_effects']


def test_manifest_and_event_contract():
    from .. import events

    assert PBC_MANIFEST['pbc'] == 'subscription_billing'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('subscription_billing_')
    assert EVENT_CONTRACT['inbox_table'].startswith('subscription_billing_')
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    smoke = events.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['stream_engine_picker_visible'] is False
    assert not validation['invalid_tables']
    assert not validation['invalid_emitted']
    assert not validation['invalid_consumed']
    assert smoke['emitted']['table'] == EVENT_CONTRACT['outbox_table']
    assert smoke['consumed']['table'] == EVENT_CONTRACT['inbox_table']
    assert smoke['emitted']['retry_policy']['max_attempts'] >= 3
    assert smoke['consumed']['dead_letter_table'].startswith(PBC_MANIFEST['pbc'] + '_')
    assert not manifest['side_effects']
    assert not validation['side_effects']
    assert not smoke['side_effects']


def test_registration_plan_is_side_effect_free():
    from .. import package_discovery_plan, package_metadata_manifest, register_pbc, registration_plan, validate_package_metadata

    assert register_pbc()['pbc'] == 'subscription_billing'
    plan = registration_plan()
    assert plan['ok'] is True
    assert plan['catalog_patch']
    metadata = package_metadata_manifest()
    metadata_validation = validate_package_metadata()
    discovery = package_discovery_plan()
    assert metadata['ok'] is True
    assert metadata_validation['ok'] is True
    assert discovery['ok'] is True
    assert metadata['stream_engine_picker_visible'] is False
    assert metadata['event_contract'] == 'AppGen-X'
    assert not metadata_validation['missing_entrypoints']
    assert not metadata_validation['missing_publish_artifacts']
    assert not metadata_validation['missing_capability_evidence']
    assert not metadata_validation['invalid']
    assert not discovery['side_effects']


def test_service_and_route_surface_are_executable():
    from .. import routes, services

    service_smoke = services.smoke_test()
    operation_contracts = services.service_operation_contracts()
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    route_smoke = routes.smoke_test()
    assert service_smoke['ok'] is True
    assert operation_contracts['ok'] is True
    assert route_contracts['ok'] is True
    assert route_validation['ok'] is True
    assert route_contracts['contracts']
    assert all(item['permission'] for item in route_contracts['contracts'])
    assert all(item['event_contract'] == 'AppGen-X' for item in route_contracts['contracts'])
    assert all(item['stream_engine_picker_visible'] is False for item in route_contracts['contracts'])
    assert all(item['shared_table_access'] is False for item in route_contracts['contracts'])
    assert not route_validation['service_mismatches']
    assert not route_validation['missing_idempotency']
    assert not route_validation['invalid_table_scope']
    assert service_smoke['result']['operation_contract']['route']['path']
    assert service_smoke['result']['operation_contract']['permission']
    assert service_smoke['result']['operation_contract']['event_contract'] == 'AppGen-X'
    assert service_smoke['result']['operation_contract']['owned_tables'] or service_smoke['result']['operation_contract']['read_tables']
    assert route_smoke['ok'] is True
    assert not service_smoke['side_effects']
    assert not operation_contracts['side_effects']
    assert not route_contracts['side_effects']
    assert not route_validation['side_effects']
    assert not route_smoke['side_effects']


def test_configuration_permissions_and_seed_hooks_are_executable():
    from .. import config, permissions, seed_data

    config_smoke = config.smoke_test()
    governance_smoke = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    assert config_smoke['ok'] is True
    assert governance_smoke['ok'] is True
    assert governance_smoke['parameter']['accepted'] is True
    assert governance_smoke['compiled_rule']['compiled'] is True
    assert governance_smoke['rule_decision']['allowed'] is True
    assert permission_smoke['ok'] is True
    assert seed_smoke['ok'] is True
    assert not config_smoke['side_effects']
    assert not governance_smoke['side_effects']
    assert not permission_smoke['side_effects']
    assert not seed_smoke['side_effects']


def test_ui_workbench_surface_is_executable():
    from .. import ui

    if hasattr(ui, 'smoke_test'):
        smoke = ui.smoke_test()
    else:
        contract = getattr(ui, f"{PBC_MANIFEST['pbc']}_ui_contract")()
        rendered = {
            'ok': contract['ok'],
            'cards': contract.get('panels') or contract.get('fragments'),
            'route': (contract.get('routes') or (None,))[0],
        }
        smoke = {
            'ok': contract['ok'] and bool(contract.get('fragments')) and bool(rendered['cards']),
            'manifest': {'fragments': contract.get('fragments', ())},
            'rendered': rendered,
            'side_effects': (),
        }
    assert smoke['ok'] is True
    assert smoke['manifest']['fragments']
    assert smoke['rendered']['cards']
    assert not smoke['side_effects']


def test_event_handlers_are_idempotent_and_retryable():
    from .. import handlers

    smoke = handlers.smoke_test()
    assert smoke['ok'] is True
    assert smoke['manifest']['handlers']
    assert smoke['first_result']['retry_policy']
    assert smoke['first_result']['dead_letter_table'].startswith('subscription_billing_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']

def test_table_stakes_and_advanced_capability_assurance_is_executable():
    from .. import capability_assurance

    manifest = capability_assurance.table_stakes_capability_manifest()
    validation = capability_assurance.validate_table_stakes_capability_coverage()
    smoke = capability_assurance.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['standard_features']
    assert manifest['advanced_capabilities']
    assert not validation['missing_standard']
    assert not validation['missing_advanced']
    assert not validation['missing_operations']
    assert not validation['uncovered_features']
    assert not validation['invalid_tables']
    assert not validation['invalid_backends']
    assert validation['stream_picker_visible'] is False
    assert validation['event_contract'] == 'AppGen-X'
    assert validation['owned_boundary_rejection']['ok'] is False
    assert validation['owned_boundary_rejection']['violations']
    assert not smoke['side_effects']


def test_subscription_lifecycle_covers_trials_changes_credits_entitlements_and_revenue():
    from .. import runtime

    state = runtime.subscription_billing_empty_state()
    state = runtime.subscription_billing_configure_runtime(state, {
        "database_backend": "postgresql",
        "event_topic": runtime.SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "default_currency": "USD",
        "supported_currencies": ("USD",),
        "supported_regions": ("US",),
        "billing_calendars": ("monthly",),
        "default_timezone": "UTC",
        "invoice_approval_mode": "policy",
        "workbench_limit": 100,
    })["state"]
    for name, value in (
        ("renewal_confidence_threshold", 0.7),
        ("churn_risk_threshold", 0.8),
        ("dunning_risk_threshold", 0.5),
        ("usage_rating_precision", 2),
        ("proration_rounding_precision", 2),
        ("retry_limit", 3),
        ("carbon_batch_window_hours", 8),
        ("discount_guardrail_percent", 25.0),
        ("approval_amount_threshold", 10000.0),
        ("workbench_limit", 100),
    ):
        state = runtime.subscription_billing_set_parameter(state, name, value)["state"]
    state = runtime.subscription_billing_register_rule(state, {
        "rule_id": "rule_subscription",
        "tenant": "tenant_billing",
        "rule_type": "renewal",
        "allowed_plan_families": ("growth",),
        "allowed_currencies": ("USD",),
        "allowed_regions": ("US",),
        "renewal_policy": "auto",
        "invoice_policy": "approve_below_threshold",
        "status": "active",
    })["state"]
    for plan_id, base_price in (("plan_growth", 100.0), ("plan_scale", 175.0)):
        state = runtime.subscription_billing_register_plan(state, {
            "plan_id": plan_id,
            "tenant": "tenant_billing",
            "family": "growth",
            "name": plan_id,
            "currency": "USD",
            "region": "US",
            "billing_period": "monthly",
            "base_price": base_price,
            "usage_rate": 2.0,
            "included_units": 10.0,
            "status": "active",
        })["state"]

    trial = runtime.subscription_billing_start_trial(state, {
        "trial_id": "trial_billing",
        "tenant": "tenant_billing",
        "customer_id": "cust_billing",
        "plan_id": "plan_growth",
        "start_date": "2026-01-01",
        "end_date": "2026-01-15",
        "region": "US",
        "currency": "USD",
    })
    state = trial["state"]
    state = runtime.subscription_billing_create_subscription(state, {
        "subscription_id": "sub_billing",
        "tenant": "tenant_billing",
        "customer_id": "cust_billing",
        "plan_id": "plan_growth",
        "start_date": "2026-01-15",
        "renewal_date": "2026-02-15",
        "region": "US",
        "currency": "USD",
        "seats": 3,
    })["state"]
    state = runtime.subscription_billing_add_subscription_addon(state, {
        "addon_id": "addon_billing",
        "tenant": "tenant_billing",
        "subscription_id": "sub_billing",
        "name": "support",
        "quantity": 1,
        "unit_price": 20.0,
        "effective_date": "2026-01-15",
    })["state"]
    state = runtime.subscription_billing_record_usage(state, {
        "usage_id": "usage_billing",
        "tenant": "tenant_billing",
        "subscription_id": "sub_billing",
        "meter_name": "api_calls",
        "quantity": 30.0,
        "occurred_at": "2026-01-20T00:00:00Z",
    })["state"]
    invoice = runtime.subscription_billing_generate_invoice(state, "sub_billing", period="2026-01")
    state = invoice["state"]
    credit = runtime.subscription_billing_issue_credit_memo(
        state,
        invoice["invoice"]["invoice_id"],
        amount=10.0,
        reason="service_adjustment",
    )
    state = credit["state"]
    payment = runtime.subscription_billing_apply_payment_to_invoice(
        state,
        invoice["invoice"]["invoice_id"],
        payment_event_id="payment_billing",
        amount=invoice["invoice"]["amount"],
    )
    state = payment["state"]
    entitlement = runtime.subscription_billing_grant_entitlement(
        state,
        "sub_billing",
        entitlement_key="support",
        scope="tenant_billing",
    )
    state = entitlement["state"]
    revenue = runtime.subscription_billing_recognize_revenue(
        state,
        invoice["invoice"]["invoice_id"],
        period="2026-01",
    )
    state = revenue["state"]
    changed = runtime.subscription_billing_change_subscription_plan(
        state,
        "sub_billing",
        target_plan_id="plan_scale",
        effective_date="2026-02-01",
        reason="upgrade",
    )
    state = changed["state"]
    exception = runtime.subscription_billing_open_billing_exception(
        state,
        "sub_billing",
        exception_type="usage_spike",
        severity="medium",
        description="usage review",
    )
    state = exception["state"]
    resolved = runtime.subscription_billing_resolve_billing_exception(
        state,
        exception["exception"]["exception_id"],
        resolution="accepted",
    )
    state = resolved["state"]
    cancelled = runtime.subscription_billing_cancel_subscription(
        state,
        "sub_billing",
        effective_date="2026-03-01",
        reason="customer_request",
    )

    assert trial["trial"]["status"] == "active"
    assert credit["credit_memo"]["status"] == "issued"
    assert payment["invoice"]["status"] == "paid"
    assert entitlement["entitlement"]["projection"] == "entitlement_projection"
    assert len(revenue["revenue_schedules"]) == 2
    assert changed["subscription"]["plan_id"] == "plan_scale"
    assert resolved["exception"]["status"] == "resolved"
    assert cancelled["subscription"]["status"] == "cancelled"
