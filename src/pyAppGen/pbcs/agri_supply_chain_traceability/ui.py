"""Workbench and standalone UI contracts for agri_supply_chain_traceability."""
from __future__ import annotations

from . import permissions
from . import routes
from . import runtime
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract


PBC_KEY = 'agri_supply_chain_traceability'
RELEASE_GATE_ACTION = 'assess_release_readiness'
AGRI_SUPPLY_CHAIN_TRACEABILITY_UI_FRAGMENT_KEYS = (
    'AgriSupplyChainTraceabilityWorkbench',
    'AgriSupplyChainTraceabilityDetail',
    'AgriSupplyChainTraceabilityAssistantPanel',
    'AgriSupplyChainTraceabilityReleaseGatePanel',
)
AGRI_SUPPLY_CHAIN_TRACEABILITY_FORM_KEYS = (
    'farm_lot_intake_form',
    'input_batch_application_form',
    'certification_scope_form',
    'storage_exception_form',
    'release_gate_review_form',
)
AGRI_SUPPLY_CHAIN_TRACEABILITY_WIZARD_KEYS = (
    'receiving_intake_wizard',
    'release_readiness_wizard',
    'recall_drill_wizard',
)
AGRI_SUPPLY_CHAIN_TRACEABILITY_CONTROL_KEYS = (
    'tenant_scope_picker',
    'lineage_timeline',
    'document_dropzone',
    'release_gate_banner',
    'exception_queue',
    'compliance_badges',
)


def agri_supply_chain_traceability_form_catalog() -> tuple[dict, ...]:
    return (
        {'key': 'farm_lot_intake_form', 'title': 'Farm lot intake', 'binds_to': 'farm_lot', 'required_fields': ('id', 'tenant', 'site_id', 'commodity', 'season')},
        {'key': 'input_batch_application_form', 'title': 'Input application', 'binds_to': 'input_batch', 'required_fields': ('id', 'tenant', 'farm_lot_id', 'supplier', 'applied_at')},
        {'key': 'certification_scope_form', 'title': 'Certification scope', 'binds_to': 'certification', 'required_fields': ('id', 'tenant', 'covered_farm_lot_ids', 'covered_commodities', 'valid_from', 'valid_to')},
        {'key': 'storage_exception_form', 'title': 'Storage exception', 'binds_to': 'storage_event', 'required_fields': ('id', 'tenant', 'subject_ids', 'farm_lot_id', 'status')},
        {'key': 'release_gate_review_form', 'title': 'Release gate review', 'binds_to': 'release_assessment', 'required_fields': ('candidate_id', 'farm_lot_id', 'commodity', 'shipment_date')},
    )


def agri_supply_chain_traceability_wizard_catalog() -> tuple[dict, ...]:
    return (
        {'key': 'receiving_intake_wizard', 'steps': ('farm_lot', 'input_batch', 'certification', 'provenance_proof'), 'outcome': 'receiving_ready'},
        {'key': 'release_readiness_wizard', 'steps': ('storage_review', 'transport_review', 'recall_check', 'release_decision'), 'outcome': 'release_assessment'},
        {'key': 'recall_drill_wizard', 'steps': ('suspect_batch', 'lineage_expansion', 'notification_scope', 'evidence_pack'), 'outcome': 'recall_drill_pack'},
    )


def agri_supply_chain_traceability_control_catalog() -> tuple[dict, ...]:
    return (
        {'key': 'tenant_scope_picker', 'type': 'selector', 'binds_to': 'tenant'},
        {'key': 'lineage_timeline', 'type': 'timeline', 'binds_to': 'records'},
        {'key': 'document_dropzone', 'type': 'upload', 'binds_to': 'assistant.document_plans'},
        {'key': 'release_gate_banner', 'type': 'banner', 'binds_to': 'release_assessments'},
        {'key': 'exception_queue', 'type': 'table', 'binds_to': 'exception_records'},
        {'key': 'compliance_badges', 'type': 'badge_group', 'binds_to': 'certification_coverage'},
    )


def agri_supply_chain_traceability_standalone_app_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'app_id': 'agri_supply_chain_traceability_one_pbc_app',
        'workbench_route': '/workbench/pbcs/agri_supply_chain_traceability',
        'navigation': (
            {'key': 'overview', 'route': '/workbench/pbcs/agri_supply_chain_traceability/overview'},
            {'key': 'trace', 'route': '/workbench/pbcs/agri_supply_chain_traceability/trace'},
            {'key': 'receiving', 'route': '/workbench/pbcs/agri_supply_chain_traceability/receiving'},
            {'key': 'release', 'route': '/workbench/pbcs/agri_supply_chain_traceability/release'},
            {'key': 'compliance', 'route': '/workbench/pbcs/agri_supply_chain_traceability/compliance'},
        ),
        'forms': AGRI_SUPPLY_CHAIN_TRACEABILITY_FORM_KEYS,
        'wizards': AGRI_SUPPLY_CHAIN_TRACEABILITY_WIZARD_KEYS,
        'controls': AGRI_SUPPLY_CHAIN_TRACEABILITY_CONTROL_KEYS,
        'single_agent_namespace': 'agri_supply_chain_traceability_skills',
        'side_effects': (),
    }


def agri_supply_chain_traceability_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    standalone = agri_supply_chain_traceability_standalone_app_contract()
    route_contracts = routes.api_route_contracts()
    permissions_manifest = permissions.permission_manifest()
    return {
        'format': 'appgen.agri-supply-chain-traceability-ui-contract.v2',
        'ok': True,
        'pbc': PBC_KEY,
        'implementation_directory': 'src/pyAppGen/pbcs/agri_supply_chain_traceability',
        'fragments': AGRI_SUPPLY_CHAIN_TRACEABILITY_UI_FRAGMENT_KEYS,
        'routes': tuple(item['route'] for item in route_contracts['contracts']) + tuple(item['route'] for item in standalone['navigation']) + ('/workbench/pbcs/agri_supply_chain_traceability',),
        'panels': (
            {'key': 'overview', 'fragment': 'AgriSupplyChainTraceabilityWorkbench', 'binds_to': ('farm_lot', 'input_batch', 'certification'), 'commands': ('command_farm_lot', 'record_input_batch', 'record_certification')},
            {'key': 'operations', 'fragment': 'AgriSupplyChainTraceabilityDetail', 'binds_to': ('storage_event', 'transport_leg', 'provenance_proof'), 'commands': ('record_storage_event', 'record_transport_leg', 'record_provenance_proof')},
            {'key': 'release_gate', 'fragment': 'AgriSupplyChainTraceabilityReleaseGatePanel', 'binds_to': ('release_assessment', 'recall_link'), 'commands': ('assess_release_readiness', 'record_recall_link')},
            {'key': 'assistant', 'fragment': 'AgriSupplyChainTraceabilityAssistantPanel', 'binds_to': ('document_instruction_plan', 'datastore_crud_plan'), 'commands': ('parse_document_instruction',)},
        ),
        'forms': agri_supply_chain_traceability_form_catalog(),
        'wizards': agri_supply_chain_traceability_wizard_catalog(),
        'controls': agri_supply_chain_traceability_control_catalog(),
        'standalone_app': standalone,
        'action_permissions': permissions_manifest,
        'configuration_editor': {
            'required_fields': ('database_backend', 'event_topic', 'retry_limit', 'release_gate_enabled', 'default_commodity', 'workbench_limit'),
            'allowed_database_backends': runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_ALLOWED_DATABASE_BACKENDS,
            'required_event_topic': runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC,
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
            'user_eventing_choice': False,
        },
        'parameter_editor': {
            'numeric_parameters': ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'),
            'bounded_supported_parameters': True,
        },
        'rule_editor': {
            'rule_types': ('farm_lot_policy', 'input_batch_policy', 'certification_policy', 'release_gate_policy'),
            'required_fields': ('rule_id', 'tenant', 'scope', 'status'),
            'compiled_evidence_required': True,
        },
        'event_surfaces': {
            'emits': runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES,
            'consumes': runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_CONSUMED_EVENT_TYPES,
            'outbox_status': 'visible',
            'inbox_status': 'visible',
            'dead_letter_status': 'visible',
        },
        'binding_evidence': {
            'owned_tables': runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES,
            'runtime_tables': runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_RUNTIME_TABLES,
            'shared_table_access': False,
            'event_contract': 'AppGen-X',
            'required_event_topic': runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC,
        },
        'full_capability_surface': {
            'operation_actions': DOMAIN_OPERATIONS + ('record_input_batch', RELEASE_GATE_ACTION),
            'rule_editors': DOMAIN_RULES,
            'parameter_editors': DOMAIN_PARAMETERS,
            'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES,
            'table_browsers': DOMAIN_OWNED_TABLES,
            'edge_case_queues': DOMAIN_EDGE_CASES + ('release_gate_blocked', 'cold_chain_breach'),
            'agent_tools': ('agri_supply_chain_traceability_skills.document_intake', 'agri_supply_chain_traceability_skills.release_gate_review', 'agri_supply_chain_traceability_skills.recall_investigation'),
            'navigation_sections': ('overview', 'operations', 'release_gate', 'traceability_graph', 'compliance', 'release_evidence'),
            'release_gate': {
                'action': RELEASE_GATE_ACTION,
                'required_evidence': ('farm_lot', 'input_batch', 'provenance_proof', 'certification', 'storage_event', 'transport_leg', 'recall_link'),
                'decision_states': ('approved', 'blocked'),
                'blocker_classes': ('provenance', 'certification', 'storage', 'transport', 'recall', 'quality_hold'),
            },
            'coverage': surface['coverage'],
        },
        'side_effects': (),
    }


def _count(records: tuple[dict, ...], entity_type: str) -> int:
    return sum(1 for record in records if record.get('entity_type') == entity_type)


def _release_queue(assessments: tuple[dict, ...]) -> tuple[dict, ...]:
    return tuple(
        {
            'candidate_id': assessment['candidate']['candidate_id'],
            'release_status': assessment['release_status'],
            'blocker_count': len(assessment['blockers']),
            'recommended_actions': assessment['recommended_actions'],
        }
        for assessment in assessments
    )


def agri_supply_chain_traceability_render_workbench(state: dict | None = None, *, tenant: str = 'default', principal_permissions: tuple[str, ...] | None = None) -> dict:
    active_state = state or runtime.agri_supply_chain_traceability_empty_state()
    workbench_data = runtime.agri_supply_chain_traceability_query_workbench(active_state, {'tenant': tenant})
    records = tuple(workbench_data['records'])
    assessments = tuple(workbench_data['release_assessments'])
    shell = agri_supply_chain_traceability_standalone_app_contract()
    permissions_value = principal_permissions or tuple(permissions.permission_manifest()['permissions'])
    latest_assessment = assessments[-1] if assessments else None
    cards = (
        {'key': 'farm_lots', 'label': 'Farm lots', 'value': _count(records, 'farm_lot')},
        {'key': 'input_batches', 'label': 'Input batches', 'value': _count(records, 'input_batch')},
        {'key': 'certifications', 'label': 'Certifications', 'value': _count(records, 'certification')},
        {'key': 'release_decisions', 'label': 'Release decisions', 'value': len(assessments)},
    )
    release_gate_panel = {
        'action': RELEASE_GATE_ACTION,
        'required_evidence': ('farm_lot', 'input_batch', 'provenance_proof', 'certification', 'storage_event', 'transport_leg', 'recall_link'),
        'decision_states': ('approved', 'blocked', 'not_run'),
        **(latest_assessment['panel'] if latest_assessment else {
            'ok': True,
            'release_status': 'not_run',
            'passed_checks': (),
            'blockers': (),
            'recommended_actions': (),
        }),
    }
    workbench = {
        'cards': cards,
        'release_queue': _release_queue(assessments),
        'recent_records': tuple(
            {
                'id': record['id'],
                'entity_type': record['entity_type'],
                'status': record['status'],
                'tenant': record['tenant'],
            }
            for record in records[-6:]
        ),
        'release_gate_panel': release_gate_panel,
        'allowed_actions': tuple(sorted(set(ui_action for ui_action in agri_supply_chain_traceability_ui_contract()['full_capability_surface']['operation_actions']))),
        'table_browsers': DOMAIN_OWNED_TABLES,
    }
    return {
        'ok': workbench_data['ok'],
        'pbc': PBC_KEY,
        'tenant': tenant,
        'route': '/workbench/pbcs/agri_supply_chain_traceability',
        'shell': shell,
        'workbench': workbench,
        'forms': agri_supply_chain_traceability_form_catalog(),
        'wizards': agri_supply_chain_traceability_wizard_catalog(),
        'controls': agri_supply_chain_traceability_control_catalog(),
        'operation_actions': agri_supply_chain_traceability_ui_contract()['full_capability_surface']['operation_actions'],
        'table_browsers': DOMAIN_OWNED_TABLES,
        'release_gate_panel': release_gate_panel,
        'principal_permissions': permissions_value,
        'side_effects': (),
    }


def agri_supply_chain_traceability_render_standalone_app(state: dict | None = None, *, tenant: str = 'default', principal_permissions: tuple[str, ...] | None = None) -> dict:
    return agri_supply_chain_traceability_render_workbench(state, tenant=tenant, principal_permissions=principal_permissions)


def smoke_test() -> dict:
    rendered = agri_supply_chain_traceability_render_workbench()
    contract = agri_supply_chain_traceability_ui_contract()
    return {
        'ok': contract['ok'] and rendered['ok'] and bool(contract['forms']) and bool(contract['wizards']) and bool(contract['controls']),
        'contract': contract,
        'rendered': rendered,
        'side_effects': (),
    }
