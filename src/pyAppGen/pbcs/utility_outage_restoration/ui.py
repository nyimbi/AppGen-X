"""UI and standalone workbench contracts for the utility_outage_restoration PBC."""
from __future__ import annotations

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)

PBC_KEY = 'utility_outage_restoration'


def utility_outage_restoration_ui_contract():
    surface = domain_capability_surface_contract()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'fragments': ('UtilityOutageRestorationWorkbench', 'UtilityOutageRestorationDetail', 'UtilityOutageRestorationAssistantPanel'),
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'action_permissions': ('utility_outage_restoration.read', 'utility_outage_restoration.create', 'utility_outage_restoration.update', 'utility_outage_restoration.approve', 'utility_outage_restoration.admin'),
        'full_capability_surface': {
            'operation_actions': DOMAIN_OPERATIONS,
            'rule_editors': DOMAIN_RULES,
            'parameter_editors': DOMAIN_PARAMETERS,
            'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES,
            'table_browsers': DOMAIN_OWNED_TABLES,
            'edge_case_queues': DOMAIN_EDGE_CASES,
            'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS),
            'navigation_sections': ('overview', 'operations', 'edge_case_triage', 'advanced_intelligence', 'release_evidence'),
            'coverage': surface['coverage'],
        },
        'side_effects': (),
    }


def utility_outage_restoration_render_workbench():
    ui = utility_outage_restoration_ui_contract()
    full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}


def utility_outage_restoration_form_contracts() -> dict:
    contracts = (
        {'key': 'UtilityNetworkAssetProjectionForm', 'table': 'utility_outage_restoration_network_asset_projection', 'operation': 'register_network_asset_projection', 'fields': ('projection_id', 'tenant', 'asset_id', 'asset_type', 'service_points', 'critical_customers')},
        {'key': 'UtilityOutageIncidentForm', 'table': 'utility_outage_restoration_outage_incident', 'operation': 'create_outage_incident', 'fields': ('outage_id', 'tenant', 'incident_number', 'service_area', 'critical_customers', 'storm_mode_active')},
        {'key': 'UtilityTroubleCallForm', 'table': 'utility_outage_restoration_trouble_call', 'operation': 'record_trouble_call', 'fields': ('outage_id', 'caller_name', 'service_point', 'channel', 'critical_customer')},
        {'key': 'UtilityOmsEventForm', 'table': 'utility_outage_restoration_oms_event', 'operation': 'create_oms_event', 'fields': ('outage_id', 'event_type', 'command', 'priority')},
        {'key': 'UtilityDeviceInterruptionForm', 'table': 'utility_outage_restoration_device_interruption', 'operation': 'create_device_interruption', 'fields': ('outage_id', 'device_id', 'device_type', 'downstream_device_ids', 'lockout')},
        {'key': 'UtilityCrewDispatchForm', 'table': 'utility_outage_restoration_crew_assignment', 'operation': 'dispatch_crew', 'fields': ('outage_id', 'crew_id', 'crew_type', 'skills', 'eta_minutes', 'staging_area', 'mutual_aid')},
        {'key': 'UtilitySwitchingPlanForm', 'table': 'utility_outage_restoration_switching_step', 'operation': 'author_switching_plan', 'fields': ('outage_id', 'plan_id', 'sequence', 'device_id', 'action', 'hold_point', 'authority')},
        {'key': 'UtilitySafetyIsolationForm', 'table': 'utility_outage_restoration_safety_isolation', 'operation': 'isolate_safety', 'fields': ('outage_id', 'hazard_type', 'device_id', 'grounding_applied', 'clearance_owner')},
        {'key': 'UtilityDamageAssessmentForm', 'table': 'utility_outage_restoration_damage_assessment', 'operation': 'record_damage_assessment', 'fields': ('outage_id', 'asset_id', 'severity', 'hazard_type', 'repair_recommendation')},
        {'key': 'UtilityRestorationEstimateForm', 'table': 'utility_outage_restoration_restoration_estimate', 'operation': 'calculate_etr', 'fields': ('outage_id', 'crew_eta_minutes', 'switching_steps_remaining', 'approval_required', 'revision_reason')},
        {'key': 'UtilityNestedOutageForm', 'table': 'utility_outage_restoration_outage_incident', 'operation': 'open_nested_outage', 'fields': ('parent_outage_id', 'outage_id', 'incident_number', 'status_reason')},
        {'key': 'UtilityCustomerNotificationForm', 'table': 'utility_outage_restoration_customer_notification', 'operation': 'send_customer_notification', 'fields': ('outage_id', 'channel', 'milestone', 'audience', 'message', 'critical_customer_priority')},
        {'key': 'UtilityMutualAidRequestForm', 'table': 'utility_outage_restoration_mutual_aid_request', 'operation': 'request_mutual_aid', 'fields': ('outage_id', 'crew_type', 'quantity', 'eta_hours', 'staging_area', 'lodging_confirmed')},
        {'key': 'UtilityGovernedAssistanceForm', 'table': 'utility_outage_restoration_governed_assistance_session', 'operation': 'create_governed_assistance_session', 'fields': ('outage_id', 'tenant', 'goal', 'operator')},
        {'key': 'UtilityStormModeActivationForm', 'table': 'utility_outage_restoration_oms_event', 'operation': 'activate_storm_mode', 'fields': ('outage_id', 'operator', 'reason')},
        {'key': 'UtilityRestorationVerificationForm', 'table': 'utility_outage_restoration_restoration_verification', 'operation': 'verify_restoration', 'fields': ('outage_id', 'verified_by', 'meter_ping_success', 'customer_callbacks_clear')},
        {'key': 'UtilityEventInboxForm', 'table': 'utility_outage_restoration_appgen_inbox_event', 'operation': 'receive_event', 'fields': ('event_type', 'idempotency_key', 'payload')},
    )
    return {'format': 'appgen.utility-outage-restoration-form-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'side_effects': ()}


def utility_outage_restoration_wizard_contracts() -> dict:
    contracts = (
        {'key': 'OutageTriageWizard', 'steps': ('network_projection', 'incident', 'trouble_call', 'device_interruption'), 'forms': ('UtilityNetworkAssetProjectionForm', 'UtilityOutageIncidentForm', 'UtilityTroubleCallForm', 'UtilityDeviceInterruptionForm'), 'keywords': ('outage', 'trouble call', 'nested', 'critical customer')},
        {'key': 'CrewDispatchWizard', 'steps': ('oms_event', 'crew_dispatch', 'critical_customer_review'), 'forms': ('UtilityOmsEventForm', 'UtilityCrewDispatchForm'), 'keywords': ('crew', 'dispatch', 'staging', 'mutual aid')},
        {'key': 'SwitchingRestorationWizard', 'steps': ('switching_plan', 'safety_isolation', 'etr', 'verification'), 'forms': ('UtilitySwitchingPlanForm', 'UtilitySafetyIsolationForm', 'UtilityRestorationEstimateForm', 'UtilityRestorationVerificationForm'), 'keywords': ('switching', 'isolation', 'etr', 'restore', 'verification')},
        {'key': 'StormModeCoordinationWizard', 'steps': ('damage_assessment', 'mutual_aid', 'notifications'), 'forms': ('UtilityDamageAssessmentForm', 'UtilityMutualAidRequestForm', 'UtilityCustomerNotificationForm', 'UtilityStormModeActivationForm'), 'keywords': ('storm', 'damage', 'mutual aid', 'notification')},
        {'key': 'GovernedAssistanceWizard', 'steps': ('document_review', 'governed_plan', 'confirmation_gate'), 'forms': ('UtilityGovernedAssistanceForm', 'UtilityEventInboxForm'), 'keywords': ('assistant', 'governed', 'document', 'plan', 'crud')},
    )
    return {'format': 'appgen.utility-outage-restoration-wizard-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'side_effects': ()}


def utility_outage_restoration_control_catalog() -> dict:
    contracts = (
        {'key': 'CriticalCustomerQueueControl', 'type': 'queue', 'binds_to': ('utility_outage_restoration_customer_impact', 'utility_outage_restoration_customer_notification')},
        {'key': 'SwitchingSafetyBoardControl', 'type': 'board', 'binds_to': ('utility_outage_restoration_switching_step', 'utility_outage_restoration_safety_isolation')},
        {'key': 'StormModeCommandControl', 'type': 'command_console', 'binds_to': ('utility_outage_restoration_damage_assessment', 'utility_outage_restoration_mutual_aid_request', 'utility_outage_restoration_oms_event')},
        {'key': 'RegulatoryIndexPanelControl', 'type': 'metrics', 'binds_to': ('utility_outage_restoration_reliability_metric',)},
        {'key': 'NotificationDeliveryQueueControl', 'type': 'queue', 'binds_to': ('utility_outage_restoration_customer_notification',)},
        {'key': 'MutualAidBoardControl', 'type': 'board', 'binds_to': ('utility_outage_restoration_mutual_aid_request', 'utility_outage_restoration_crew_assignment')},
        {'key': 'GovernedAssistanceControl', 'type': 'review', 'binds_to': ('utility_outage_restoration_governed_assistance_session',)},
    )
    return {'format': 'appgen.utility-outage-restoration-control-catalog.v1', 'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'side_effects': ()}


def utility_outage_restoration_standalone_workbench_blueprint() -> dict:
    forms = utility_outage_restoration_form_contracts()['contracts']
    wizards = utility_outage_restoration_wizard_contracts()['contracts']
    controls = utility_outage_restoration_control_catalog()['contracts']
    return {
        'format': 'appgen.utility-outage-restoration-standalone-workbench-blueprint.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'route': '/app/utility-outage-restoration/workbench',
        'forms': tuple(item['key'] for item in forms),
        'wizards': tuple(item['key'] for item in wizards),
        'controls': tuple(item['key'] for item in controls),
        'fragments': (
            'UtilityOutageRestorationStandaloneWorkbench',
            'UtilityOutageTriagePanel',
            'UtilityCrewDispatchPanel',
            'UtilitySwitchingSafetyPanel',
            'UtilityStormModePanel',
            'UtilityRegulatoryIndexPanel',
            'UtilityGovernedAssistancePanel',
        ),
        'sections': ('overview', 'critical_customers', 'switching_and_isolation', 'storm_mode', 'notifications', 'regulatory_indices', 'governed_assistance'),
        'side_effects': (),
    }


def utility_outage_restoration_render_standalone_workbench(workbench: dict) -> dict:
    blueprint = utility_outage_restoration_standalone_workbench_blueprint()
    cards = (
        {'key': 'active_outages', 'value': workbench.get('active_outage_count', 0), 'emphasis': 'high'},
        {'key': 'critical_queue', 'value': len(tuple(workbench.get('critical_customer_queue', ()))), 'emphasis': 'high'},
        {'key': 'crew_dispatches', 'value': workbench.get('crew_dispatch_count', 0), 'emphasis': 'medium'},
        {'key': 'switching_steps', 'value': workbench.get('switching_plan_count', 0), 'emphasis': 'medium'},
        {'key': 'storm_mode', 'value': int(bool(workbench.get('storm_mode_active'))), 'emphasis': 'critical'},
        {'key': 'regulatory_snapshots', 'value': workbench.get('verification_count', 0), 'emphasis': 'medium'},
    )
    return {
        'format': 'appgen.utility-outage-restoration-standalone-workbench-render.v1',
        'ok': blueprint['ok'] and workbench.get('ok') is True,
        'pbc': PBC_KEY,
        'route': blueprint['route'],
        'cards': cards,
        'critical_customer_queue': workbench.get('critical_customer_queue', ()),
        'storm_mode_active': workbench.get('storm_mode_active', False),
        'forms': utility_outage_restoration_form_contracts()['contracts'],
        'wizards': utility_outage_restoration_wizard_contracts()['contracts'],
        'controls': utility_outage_restoration_control_catalog()['contracts'],
        'side_effects': (),
    }


def smoke_test():
    return {'ok': utility_outage_restoration_ui_contract()['ok'] and utility_outage_restoration_render_workbench()['ok'], 'side_effects': ()}
