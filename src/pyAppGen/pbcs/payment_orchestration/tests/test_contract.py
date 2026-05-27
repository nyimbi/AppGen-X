"""Generated contract smoke tests for payment_orchestration."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'payment_orchestration'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'payment_orchestration'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'payment_orchestration'
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

    assert PBC_MANIFEST['pbc'] == 'payment_orchestration'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('payment_orchestration_')
    assert EVENT_CONTRACT['inbox_table'].startswith('payment_orchestration_')
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

    assert register_pbc()['pbc'] == 'payment_orchestration'
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
    assert smoke['first_result']['dead_letter_table'].startswith('payment_orchestration_')
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


def test_payment_lifecycle_covers_authorization_settlement_payout_and_dispute():
    from .. import runtime

    state = runtime.payment_orchestration_empty_state()
    state = runtime.payment_orchestration_configure_runtime(state, {
        "database_backend": "postgresql",
        "event_topic": runtime.PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "default_currency": "USD",
        "supported_currencies": ("USD",),
        "supported_regions": ("US",),
        "supported_methods": ("card",),
        "settlement_windows": ("night",),
        "default_timezone": "UTC",
        "workbench_limit": 100,
    })["state"]
    for name, value in (
        ("authorization_threshold", 0.7),
        ("fraud_review_threshold", 0.7),
        ("capture_amount_tolerance", 0.5),
        ("retry_limit", 3),
        ("gateway_latency_weight", 0.2),
        ("gateway_cost_weight", 0.2),
        ("gateway_auth_weight", 0.5),
        ("settlement_risk_weight", 0.1),
        ("max_capture_attempts", 3),
        ("workbench_limit", 100),
    ):
        state = runtime.payment_orchestration_set_parameter(state, name, value)["state"]
    state = runtime.payment_orchestration_register_rule(state, {
        "rule_id": "rule_card",
        "tenant": "tenant_payment",
        "rule_type": "gateway_routing",
        "allowed_gateways": ("gateway_primary",),
        "allowed_currencies": ("USD",),
        "allowed_regions": ("US",),
        "risk_ceiling": 0.8,
        "capture_policy": "authorize_then_capture",
        "status": "active",
    })["state"]
    state = runtime.payment_orchestration_register_gateway(state, {
        "gateway_id": "gateway_primary",
        "tenant": "tenant_payment",
        "provider": "primarypay",
        "regions": ("US",),
        "currencies": ("USD",),
        "methods": ("card",),
        "latency_ms": 120,
        "fee_bps": 80,
        "authorization_rate": 0.93,
        "settlement_risk": 0.04,
        "capacity": 50,
        "carbon_score": 20,
        "status": "active",
    })["state"]
    state = runtime.payment_orchestration_receive_event(state, {
        "event_id": "checkout_payment_1",
        "event_type": "CheckoutCompleted",
        "payload": {
            "tenant": "tenant_payment",
            "checkout_id": "checkout_payment",
            "customer_id": "customer_payment",
            "amount": 100,
            "currency": "USD",
            "region": "US",
        },
    })["state"]
    state = runtime.payment_orchestration_tokenize_payment_method(state, {
        "token_id": "token_payment",
        "tenant": "tenant_payment",
        "customer_id": "customer_payment",
        "method_type": "card",
        "network": "card_network",
        "issuer_country": "US",
        "vault_ref": "vault://token_payment",
    })["state"]
    state = runtime.payment_orchestration_create_payment_intent(state, {
        "intent_id": "pi_payment",
        "tenant": "tenant_payment",
        "checkout_id": "checkout_payment",
        "customer_id": "customer_payment",
        "amount": 100,
        "currency": "USD",
        "region": "US",
        "token_id": "token_payment",
    })["state"]
    state = runtime.payment_orchestration_route_gateway(state, "pi_payment")["state"]
    state = runtime.payment_orchestration_request_fraud_check(state, "pi_payment")["state"]
    state = runtime.payment_orchestration_receive_event(state, {
        "event_id": "fraud_payment_1",
        "event_type": "FraudRiskScored",
        "payload": {"tenant": "tenant_payment", "intent_id": "pi_payment", "risk_score": 0.1, "decision": "approve"},
    })["state"]

    capture = runtime.payment_orchestration_capture_payment(state, "pi_payment", amount=100)
    state = capture["state"]
    settlement = runtime.payment_orchestration_settle_payment(state, "pi_payment", settlement_reference="batch_payment")
    state = settlement["state"]
    payout = runtime.payment_orchestration_schedule_payout(state, "pi_payment", payout_account="merchant_account")
    state = payout["state"]
    dispute = runtime.payment_orchestration_open_dispute(
        state,
        "pi_payment",
        amount=12,
        reason="customer_query",
        evidence=("delivery_proof",),
    )
    state = dispute["state"]
    resolution = runtime.payment_orchestration_resolve_dispute(
        state,
        dispute["dispute"]["dispute_id"],
        decision="merchant_won",
        resolution_notes="proof accepted",
    )

    assert capture["ok"] is True
    assert settlement["settlement"]["status"] == "settled"
    assert payout["payout"]["status"] == "scheduled"
    assert dispute["dispute"]["status"] == "under_review"
    assert resolution["dispute"]["status"] == "resolved"
    assert state["outbox"][-1]["event_type"] == "PaymentDisputeOpened"
