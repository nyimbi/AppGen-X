"""Generated contract smoke tests for returns_reverse_logistics."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'returns_reverse_logistics'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    assert len(SCHEMA_CONTRACT['owned_tables']) >= 35
    assert all(table.startswith('returns_reverse_logistics_') for table in SCHEMA_CONTRACT['owned_tables'])
    assert any(
        field['name'] == 'return_id'
        for table in SCHEMA_CONTRACT['tables']
        if table['owned_table'] == 'returns_reverse_logistics_return_authorization'
        for field in table['fields']
    )
    assert any(
        field['name'] == 'expected_recovery_rate'
        for table in SCHEMA_CONTRACT['tables']
        if table['owned_table'] == 'returns_reverse_logistics_inspection_grade'
        for field in table['fields']
    )
    assert any(
        field['name'] == 'idempotency_key'
        for table in SCHEMA_CONTRACT['tables']
        if table['owned_table'] == 'returns_reverse_logistics_outbox_event'
        for field in table['fields']
    )
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert not model_smoke['manifest']['thin_models']
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'returns_reverse_logistics'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'returns_reverse_logistics'
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

    assert PBC_MANIFEST['pbc'] == 'returns_reverse_logistics'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('returns_reverse_logistics_')
    assert EVENT_CONTRACT['inbox_table'].startswith('returns_reverse_logistics_')
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

    assert register_pbc()['pbc'] == 'returns_reverse_logistics'
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
    assert smoke['first_result']['dead_letter_table'].startswith('returns_reverse_logistics_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']


def test_returns_lifecycle_covers_receipt_disposition_resolution_claims_and_exceptions():
    from .. import runtime

    state = runtime.returns_reverse_logistics_empty_state()
    state = runtime.returns_reverse_logistics_configure_runtime(state, {
        "database_backend": "postgresql",
        "event_topic": runtime.RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "default_currency": "USD",
        "supported_carriers": ("parcel_green",),
        "supported_dispositions": ("restock", "refurbish", "scrap"),
        "workbench_limit": 100,
    })["state"]
    for name, value in (
        ("eligibility_window_days", 30),
        ("fraud_threshold", 0.8),
        ("recovery_floor", 0.3),
        ("carrier_handoff_hours", 24),
        ("carbon_weight", 0.2),
        ("route_switch_threshold", 0.1),
        ("forecast_horizon_days", 14),
        ("anomaly_zscore_threshold", 2.5),
        ("workbench_limit", 100),
    ):
        state = runtime.returns_reverse_logistics_set_parameter(state, name, value)["state"]
    state = runtime.returns_reverse_logistics_register_rule(state, {
        "rule_id": "rule_returns",
        "tenant": "tenant_returns",
        "scope": "return_policy",
        "status": "active",
        "eligibility_policy": {"max_days_since_shipment": 30, "blocked_reasons": (), "minimum_payment_capture_ratio": 1.0},
        "label_policy": {"preferred_carriers": ("parcel_green",), "max_cost": 15.0},
        "inspection_policy": {"restock_min": 0.85, "refurbish_min": 0.55},
        "credit_policy": {"restock_factor": 0.9, "refurbish_factor": 0.65, "scrap_factor": 0.25},
    })["state"]
    state = runtime.returns_reverse_logistics_receive_event(state, {
        "event_id": "evt_order_returns",
        "event_type": "OrderShipped",
        "idempotency_key": "order_returns:v1",
        "payload": {
            "tenant": "tenant_returns",
            "order_id": "order_returns",
            "payment_id": "pay_returns",
            "customer_id": "cust_returns",
            "shipped_at": "2026-05-20",
            "days_since_shipped": 4,
            "return_window_days": 30,
            "final_sale": False,
            "items": ({"sku": "sku_returns", "quantity": 1, "unit_price": 80.0},),
        },
    })["state"]
    state = runtime.returns_reverse_logistics_receive_event(state, {
        "event_id": "evt_payment_returns",
        "event_type": "PaymentCaptured",
        "idempotency_key": "payment_returns:v1",
        "payload": {
            "tenant": "tenant_returns",
            "payment_id": "pay_returns",
            "order_id": "order_returns",
            "captured_amount": 80.0,
            "currency": "USD",
            "ledger_account": "refund_liability",
        },
    })["state"]
    authorized = runtime.returns_reverse_logistics_authorize_return(state, {
        "return_id": "ret_returns",
        "rma": "RMA-RETURNS",
        "tenant": "tenant_returns",
        "order_id": "order_returns",
        "payment_id": "pay_returns",
        "customer_id": "cust_returns",
        "reason": "damaged",
        "requested_at": "2026-05-24",
        "days_since_shipped": 4,
        "items": ({"sku": "sku_returns", "quantity": 1},),
    })
    state = authorized["state"]
    state = runtime.returns_reverse_logistics_create_return_label(state, {
        "label_id": "lbl_returns",
        "return_id": "ret_returns",
        "tenant": "tenant_returns",
        "origin": "Nairobi",
        "destination": "Mombasa",
        "package_weight_kg": 1.0,
    })["state"]
    receipt = runtime.returns_reverse_logistics_record_return_receipt(state, {
        "receipt_id": "rcpt_returns",
        "return_id": "ret_returns",
        "tenant": "tenant_returns",
        "received_at": "2026-05-25T10:00:00Z",
        "receiving_site": "returns_dc",
        "package_condition": "intact",
    })
    state = receipt["state"]
    state = runtime.returns_reverse_logistics_record_inspection_grade(state, {
        "inspection_id": "insp_returns",
        "return_id": "ret_returns",
        "tenant": "tenant_returns",
        "condition_score": 0.93,
        "completeness_score": 1.0,
        "packaging_intact": True,
        "notes": "ready",
    })["state"]
    disposition = runtime.returns_reverse_logistics_resolve_disposition(
        state,
        "ret_returns",
        destination_site="restock_dc",
    )
    state = disposition["state"]
    state = runtime.returns_reverse_logistics_issue_credit_adjustment(state, {
        "adjustment_id": "adj_returns",
        "return_id": "ret_returns",
        "tenant": "tenant_returns",
    })["state"]
    resolution = runtime.returns_reverse_logistics_register_exchange_resolution(
        state,
        "ret_returns",
        resolution_mode="refund",
    )
    state = resolution["state"]
    claim = runtime.returns_reverse_logistics_open_carrier_claim(
        state,
        "ret_returns",
        claim_reason="late_scan",
    )
    state = claim["state"]
    exception = runtime.returns_reverse_logistics_open_exception_case(
        state,
        "ret_returns",
        exception_type="carrier_timeout",
        severity="medium",
        owner="ops",
    )

    assert authorized["return_authorization"]["status"] == "authorized"
    assert receipt["receipt"]["received_status"] == "received"
    assert disposition["disposition"]["status"] == "resolved"
    assert "ret_returns" in state["restocking_orders"]
    assert resolution["resolution"]["resolution_mode"] == "refund"
    assert claim["carrier_claim"]["status"] == "open"
    assert exception["exception_case"]["resolution"] == "failover_carrier_selection"
