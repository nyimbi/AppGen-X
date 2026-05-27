"""Generated contract smoke tests for cdp_segmentation."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'cdp_segmentation'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'cdp_segmentation'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'cdp_segmentation'
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

    assert PBC_MANIFEST['pbc'] == 'cdp_segmentation'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('cdp_segmentation_')
    assert EVENT_CONTRACT['inbox_table'].startswith('cdp_segmentation_')
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

    assert register_pbc()['pbc'] == 'cdp_segmentation'
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
    assert smoke['first_result']['dead_letter_table'].startswith('cdp_segmentation_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']


def test_cdp_advanced_orchestration_tail_is_executable():
    from ..runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
    from ..runtime import cdp_segmentation_allocate_activation
    from ..runtime import cdp_segmentation_configure_runtime
    from ..runtime import cdp_segmentation_define_segment
    from ..runtime import cdp_segmentation_detect_profile_anomaly
    from ..runtime import cdp_segmentation_empty_state
    from ..runtime import cdp_segmentation_evaluate_segments
    from ..runtime import cdp_segmentation_federate_customer_view
    from ..runtime import cdp_segmentation_forecast_audience
    from ..runtime import cdp_segmentation_generate_profile_proof
    from ..runtime import cdp_segmentation_heal_profile_merge
    from ..runtime import cdp_segmentation_ingest_customer_event
    from ..runtime import cdp_segmentation_parse_segment_rule
    from ..runtime import cdp_segmentation_register_governed_model
    from ..runtime import cdp_segmentation_register_rule
    from ..runtime import cdp_segmentation_resolve_audience_exception
    from ..runtime import cdp_segmentation_run_data_quality_controls
    from ..runtime import cdp_segmentation_score_lifecycle_risk
    from ..runtime import cdp_segmentation_screen_consent_policy
    from ..runtime import cdp_segmentation_set_parameter
    from ..runtime import cdp_segmentation_simulate_segment_membership

    state = cdp_segmentation_empty_state()
    state = cdp_segmentation_configure_runtime(
        state,
        {
            'database_backend': 'postgresql',
            'event_topic': CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
            'retry_limit': 3,
            'default_region': 'US',
            'supported_regions': ('US',),
            'supported_event_types': ('profile', 'payment', 'shipment', 'engagement'),
            'identity_keys': ('customer_id', 'email'),
            'default_timezone': 'UTC',
            'activation_mode': 'policy',
            'workbench_limit': 50,
        },
    )['state']
    for name, value in (
        ('membership_score_threshold', 0.6),
        ('profile_merge_confidence_threshold', 0.85),
        ('event_freshness_days', 180),
        ('payment_value_weight', 0.35),
        ('order_recency_weight', 0.25),
        ('engagement_weight', 0.4),
        ('consent_risk_threshold', 0.6),
        ('activation_batch_limit', 5000),
        ('max_segments_per_profile', 20),
        ('workbench_limit', 50),
    ):
        state = cdp_segmentation_set_parameter(state, name, value)['state']
    state = cdp_segmentation_register_rule(
        state,
        {
            'rule_id': 'rule_tail',
            'tenant': 'tenant_tail',
            'scope': 'cdp_segmentation',
            'status': 'active',
            'allowed_event_types': ('profile', 'payment', 'shipment', 'engagement'),
            'allowed_regions': ('US',),
            'segment_policy': {'minimum_score': 0.6, 'required_properties': ('customer_id',)},
            'consent_policy': {'require_opt_in': True, 'restricted_regions': ()},
            'activation_policy': {'destinations': ('notifications', 'pricing')},
        },
    )['state']
    for event in (
        {'event_id': 'profile_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail', 'event_type': 'profile', 'region': 'US', 'properties': {'customer_id': 'cust_tail', 'email': 'tail@example.com', 'opt_in': True}},
        {'event_id': 'payment_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail', 'event_type': 'payment', 'region': 'US', 'properties': {'amount': 2000}},
        {'event_id': 'ship_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail', 'event_type': 'shipment', 'region': 'US', 'properties': {'order_id': 'ord_tail'}},
        {'event_id': 'engage_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail', 'event_type': 'engagement', 'region': 'US', 'properties': {'clicks': 5}},
    ):
        state = cdp_segmentation_ingest_customer_event(state, event)['state']
    state = cdp_segmentation_define_segment(
        state,
        {'segment_id': 'seg_tail', 'tenant': 'tenant_tail', 'name': 'Tail Segment', 'criteria': {'min_payment_value': 1000, 'requires_shipment': True, 'min_engagement': 0.2}, 'status': 'active'},
    )['state']
    state = cdp_segmentation_evaluate_segments(state, 'cust_tail')['state']
    state = cdp_segmentation_parse_segment_rule(state, {'rule_text': 'high value with shipment and engagement', 'tenant': 'tenant_tail', 'segment_id': 'seg_tail'})['state']
    state = cdp_segmentation_simulate_segment_membership(
        state,
        {'simulation_id': 'sim_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail', 'segment_id': 'seg_tail', 'counterfactual_properties': {'amount': 3000, 'clicks': 9}},
    )['state']
    state = cdp_segmentation_forecast_audience(state, {'forecast_id': 'forecast_tail', 'tenant': 'tenant_tail', 'segment_id': 'seg_tail', 'horizon_days': 30})['state']
    state = cdp_segmentation_score_lifecycle_risk(state, {'score_id': 'risk_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail'})['state']
    state = cdp_segmentation_heal_profile_merge(state, {'merge_id': 'merge_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail', 'candidate_customer_id': 'cust_alias', 'confidence': 0.91})['state']
    state = cdp_segmentation_generate_profile_proof(state, {'proof_id': 'proof_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail'})['state']
    state = cdp_segmentation_screen_consent_policy(state, {'screening_id': 'consent_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail', 'activation_destination': 'notifications'})['state']
    state = cdp_segmentation_run_data_quality_controls(state, 'tenant_tail')['state']
    state = cdp_segmentation_federate_customer_view(state, {'view_id': 'view_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail'})['state']
    state = cdp_segmentation_allocate_activation(state, {'allocation_id': 'alloc_tail', 'tenant': 'tenant_tail', 'segment_id': 'seg_tail', 'destination': 'notifications', 'budget': 500})['state']
    state = cdp_segmentation_detect_profile_anomaly(state, {'signal_id': 'anom_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail'})['state']
    state = cdp_segmentation_resolve_audience_exception(state, {'exception_id': 'exception_tail', 'tenant': 'tenant_tail', 'customer_id': 'cust_tail', 'reason': 'identity_conflict', 'resolution': 'accepted_primary_identity'})['state']
    state = cdp_segmentation_register_governed_model(state, {'model_id': 'model_tail', 'tenant': 'tenant_tail', 'model_type': 'lifecycle_risk', 'version': '1.0', 'status': 'approved'})['state']

    assert state['segment_rules']
    assert state['segment_simulations']['sim_tail']['counterfactual_score'] >= state['segment_simulations']['sim_tail']['baseline_score']
    assert state['audience_forecasts']['forecast_tail']['forecast_members'] >= 1
    assert state['lifecycle_risk_scores']['risk_tail']['risk_band'] in {'normal', 'high'}
    assert state['merge_candidates']['merge_tail']['status'] == 'accepted'
    assert state['profile_proofs']['proof_tail']['status'] == 'issued'
    assert state['consent_policy_screenings']['consent_tail']['decision'] == 'allowed'
    assert state['data_quality_findings']
    assert state['cdp_federation_views']['view_tail']['status'] == 'materialized'
    assert state['activation_allocations']['alloc_tail']['status'] == 'allocated'
    assert state['profile_anomaly_signals']['anom_tail']['status'] in {'normal', 'review'}
    assert state['profile_exceptions']['exception_tail']['status'] == 'resolved'
    assert state['cdp_governed_models']['model_tail']['training_data_boundary'] == 'cdp_segmentation_owned_tables'


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
