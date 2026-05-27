"""Generated contract smoke tests for service_ticketing."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'service_ticketing'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'service_ticketing'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'service_ticketing'
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

    assert PBC_MANIFEST['pbc'] == 'service_ticketing'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('service_ticketing_')
    assert EVENT_CONTRACT['inbox_table'].startswith('service_ticketing_')
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

    assert register_pbc()['pbc'] == 'service_ticketing'
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
    assert smoke['first_result']['dead_letter_table'].startswith('service_ticketing_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']


def test_service_ticketing_lifecycle_tail_is_executable():
    from ..runtime import SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
    from ..runtime import service_ticketing_assign_ticket
    from ..runtime import service_ticketing_close_ticket
    from ..runtime import service_ticketing_configure_runtime
    from ..runtime import service_ticketing_create_sla_policy
    from ..runtime import service_ticketing_empty_state
    from ..runtime import service_ticketing_open_ticket
    from ..runtime import service_ticketing_prepare_field_service_handoff
    from ..runtime import service_ticketing_record_csat_response
    from ..runtime import service_ticketing_record_ticket_interaction
    from ..runtime import service_ticketing_register_rule
    from ..runtime import service_ticketing_reopen_ticket
    from ..runtime import service_ticketing_resolve_ticket
    from ..runtime import service_ticketing_run_control_tests
    from ..runtime import service_ticketing_send_customer_update
    from ..runtime import service_ticketing_set_parameter

    state = service_ticketing_empty_state()
    state = service_ticketing_configure_runtime(
        state,
        {
            'database_backend': 'postgresql',
            'event_topic': SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
            'retry_limit': 3,
            'default_region': 'US',
            'supported_regions': ('US',),
            'channels': ('email', 'chat', 'portal'),
            'priority_levels': ('low', 'medium', 'high', 'critical'),
            'default_timezone': 'UTC',
            'assignment_mode': 'policy',
            'workbench_limit': 25,
        },
    )['state']
    for name, value in (
        ('sla_breach_risk_threshold', 0.7),
        ('auto_escalation_threshold', 0.95),
        ('sentiment_risk_weight', 0.3),
        ('priority_weight', 0.3),
        ('customer_tier_weight', 0.2),
        ('queue_load_weight', 0.2),
        ('first_response_minutes', 30),
        ('resolution_target_hours', 24),
        ('max_open_cases_per_owner', 25),
        ('workbench_limit', 25),
    ):
        state = service_ticketing_set_parameter(state, name, value)['state']
    state = service_ticketing_register_rule(
        state,
        {
            'rule_id': 'rule_tail',
            'tenant': 'tenant_tail',
            'scope': 'service_ticketing',
            'status': 'active',
            'allowed_regions': ('US',),
            'allowed_channels': ('email', 'chat', 'portal'),
            'allowed_priorities': ('low', 'medium', 'high', 'critical'),
            'assignment_policy': {
                'default_queue': 'tier_2',
                'default_owner': 'agent_tail',
                'skills': ('technical',),
            },
            'escalation_policy': {
                'critical_queue': 'priority_response',
                'breach_owner': 'manager_tail',
            },
        },
    )['state']
    state = service_ticketing_create_sla_policy(
        state,
        {
            'sla_policy_id': 'sla_tail',
            'tenant': 'tenant_tail',
            'name': 'Tail Lifecycle',
            'priority': 'high',
            'first_response_minutes': 30,
            'resolution_target_hours': 12,
            'status': 'active',
        },
    )['state']
    state = service_ticketing_open_ticket(
        state,
        {
            'ticket_id': 'case_tail',
            'tenant': 'tenant_tail',
            'customer_id': 'cust_tail',
            'subject': 'Service issue',
            'description': 'Customer needs a full support lifecycle',
            'channel': 'chat',
            'priority': 'high',
            'region': 'US',
            'sentiment': -0.3,
            'sla_policy_id': 'sla_tail',
        },
    )['state']
    state = service_ticketing_assign_ticket(
        state,
        {
            'assignment_id': 'assign_tail',
            'tenant': 'tenant_tail',
            'ticket_id': 'case_tail',
            'owner': 'agent_tail',
            'queue': 'tier_2',
            'skills': ('technical',),
        },
    )['state']
    interaction = service_ticketing_record_ticket_interaction(
        state,
        {
            'ticket_id': 'case_tail',
            'interaction_type': 'agent_response',
            'actor': 'agent_tail',
            'summary': 'Collected diagnostics and advised next steps',
            'channel': 'chat',
        },
    )
    state = interaction['state']
    update = service_ticketing_send_customer_update(
        state,
        {
            'ticket_id': 'case_tail',
            'update_type': 'progress_notice',
            'message': 'The service team is actively working the case.',
        },
    )
    state = update['state']
    handoff = service_ticketing_prepare_field_service_handoff(
        state,
        {
            'ticket_id': 'case_tail',
            'handoff_reason': 'onsite_check',
            'target_team': 'field_success',
        },
    )
    state = handoff['state']
    state = service_ticketing_resolve_ticket(state, 'case_tail', resolution='Issue resolved after field check')['state']
    survey_id = next(iter(state['csat_responses']))
    csat = service_ticketing_record_csat_response(
        state,
        {
            'survey_id': survey_id,
            'score': 5,
            'comment': 'Professional support and clear updates',
        },
    )
    state = csat['state']
    state = service_ticketing_reopen_ticket(state, {'ticket_id': 'case_tail', 'reason': 'follow_up_question'})['state']
    closed = service_ticketing_close_ticket(
        state,
        {
            'ticket_id': 'case_tail',
            'closure_reason': 'customer_confirmed_complete',
        },
    )
    state = closed['state']
    control = service_ticketing_run_control_tests(state)

    assert interaction['interaction']['interaction_id'] in state['ticket_interactions']
    assert update['customer_update']['update_id'] in state['customer_updates']
    assert handoff['handoff']['handoff_id'] in state['field_service_handoffs']
    assert csat['csat_response']['status'] == 'received'
    assert closed['ticket']['status'] == 'closed'
    assert state['case_lifecycle_states']['case_tail']['stage'] == 'closed'
    assert {'TicketInteractionRecorded', 'CustomerUpdateSent', 'CsatResponseRecorded', 'SupportCaseReopened', 'SupportCaseClosed'} <= {
        item['event_type'] for item in state['outbox']
    }
    assert control['ok'] is True


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
