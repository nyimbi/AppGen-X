"""UI contract for the CDP Segmentation PBC."""

from __future__ import annotations

from .cdp_control import CDP_CONTROL_CAPABILITIES, improve1_cdp_control_contract
from .runtime import CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
from .runtime import CDP_SEGMENTATION_OWNED_TABLES
from .runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
from .runtime import CDP_SEGMENTATION_RUNTIME_TABLES


CDP_SEGMENTATION_UI_FRAGMENT_KEYS = (
    'CdpSegmentationWorkbench',
    'CustomerEventStream',
    'ProfilePropertyPanel',
    'ProfileConsentTimeline',
    'SegmentDefinitionBuilder',
    'MembershipEvaluationBoard',
    'MembershipTransitionLedger',
    'ActivationConsole',
    'ActivationAllocationPlanner',
    'ConsentPolicyPanel',
    'IdentityStitchingPanel',
    'CdpRuleStudio',
    'CdpParameterConsole',
    'CdpConfigurationPanel',
    'DocumentInstructionDesk',
    'SegmentSimulationWizard',
    'ActivationReadinessWizard',
    'WorkbenchControls',
    'CdpEventOutbox',
    'CdpDeadLetterQueue',
    'CdpSchemaContractExplorer',
    'CdpServiceContractExplorer',
    'CdpReleaseEvidencePanel',
)
CDP_SEGMENTATION_FORM_KEYS = (
    'CustomerEventIntakeForm',
    'ProfilePropertyForm',
    'SegmentDefinitionForm',
    'SegmentRuleDocumentForm',
    'ActivationAllocationForm',
)
CDP_SEGMENTATION_WIZARD_KEYS = (
    'SegmentSimulationWizard',
    'ActivationReadinessWizard',
    'AudienceRecoveryWizard',
    'DocumentInstructionWizard',
)
CDP_SEGMENTATION_CONTROL_KEYS = (
    'WorkbenchSummaryCards',
    'TenantSegmentFilters',
    'MembershipTransitionLedgerControl',
    'ConsentGuardrailControl',
    'AgentInstructionPreviewControl',
    'EventingReliabilityConsole',
)


def cdp_segmentation_form_catalog() -> dict:
    forms = (
        {
            'key': 'CustomerEventIntakeForm',
            'route': '/app/cdp-segmentation/events',
            'operation': 'ingest_customer_event',
            'table': 'cdp_segmentation_customer_event',
            'fields': ('event_id', 'tenant', 'customer_id', 'event_type', 'region', 'properties'),
        },
        {
            'key': 'ProfilePropertyForm',
            'route': '/app/cdp-segmentation/profile-properties',
            'operation': 'upsert_profile_property',
            'table': 'cdp_segmentation_profile_property',
            'fields': ('property_id', 'tenant', 'customer_id', 'name', 'value', 'source'),
        },
        {
            'key': 'SegmentDefinitionForm',
            'route': '/app/cdp-segmentation/segments',
            'operation': 'define_segment',
            'table': 'cdp_segmentation_segment_definition',
            'fields': ('segment_id', 'tenant', 'name', 'criteria', 'status'),
        },
        {
            'key': 'SegmentRuleDocumentForm',
            'route': '/app/cdp-segmentation/assistant/document-preview',
            'operation': 'document_instruction_crud_support',
            'table': 'cdp_segmentation_segment_rule',
            'fields': ('document', 'instructions', 'payload'),
        },
        {
            'key': 'ActivationAllocationForm',
            'route': '/app/cdp-segmentation/activation-allocations',
            'operation': 'allocate_activation',
            'table': 'cdp_segmentation_activation_allocation',
            'fields': ('allocation_id', 'tenant', 'segment_id', 'destination', 'budget'),
        },
    )
    return {
        'format': 'appgen.cdp-segmentation-form-catalog.v1',
        'ok': True,
        'pbc': 'cdp_segmentation',
        'forms': forms,
        'form_ids': tuple(item['key'] for item in forms),
        'side_effects': (),
    }


def cdp_segmentation_wizard_catalog() -> dict:
    wizards = (
        {
            'key': 'SegmentSimulationWizard',
            'forms': ('SegmentDefinitionForm', 'CustomerEventIntakeForm'),
            'steps': ('choose_segment', 'choose_customer', 'adjust_counterfactual', 'review_delta'),
            'goal': 'Model how one customer moves into or out of a governed audience before activation.',
        },
        {
            'key': 'ActivationReadinessWizard',
            'forms': ('SegmentDefinitionForm', 'ActivationAllocationForm'),
            'steps': ('screen_consent', 'estimate_audience', 'allocate_budget', 'review_delivery'),
            'goal': 'Check consent, volume, and budget before dispatching one audience activation.',
        },
        {
            'key': 'AudienceRecoveryWizard',
            'forms': ('ProfilePropertyForm', 'SegmentRuleDocumentForm'),
            'steps': ('inspect_profile', 'capture_exception', 'draft_resolution', 'approve_recovery'),
            'goal': 'Recover blocked or inconsistent segment members without leaving cdp_segmentation.',
        },
        {
            'key': 'DocumentInstructionWizard',
            'forms': ('SegmentRuleDocumentForm',),
            'steps': ('summarize_document', 'map_to_owned_table', 'preview_mutation', 'confirm_handoff'),
            'goal': 'Convert operator instructions into governed CRUD previews against owned CDP tables.',
        },
    )
    return {
        'format': 'appgen.cdp-segmentation-wizard-catalog.v1',
        'ok': True,
        'pbc': 'cdp_segmentation',
        'wizards': wizards,
        'wizard_ids': tuple(item['key'] for item in wizards),
        'missing_form_bindings': tuple(
            wizard['key']
            for wizard in wizards
            for form in wizard['forms']
            if form not in cdp_segmentation_form_catalog()['form_ids']
        ),
        'side_effects': (),
    }


def cdp_segmentation_control_catalog() -> dict:
    controls = (
        {'key': 'WorkbenchSummaryCards', 'type': 'cards', 'binds_to': ('events', 'profiles', 'segments', 'memberships')},
        {'key': 'TenantSegmentFilters', 'type': 'filters', 'binds_to': ('tenant', 'segment_status', 'membership_status', 'consent_status')},
        {'key': 'MembershipTransitionLedgerControl', 'type': 'ledger', 'binds_to': ('membership_evaluations',)},
        {'key': 'ConsentGuardrailControl', 'type': 'policy', 'binds_to': ('profile_consents', 'consent_policy_screenings')},
        {'key': 'AgentInstructionPreviewControl', 'type': 'assistant_preview', 'binds_to': ('segment_rule', 'profile_property', 'profile_exception')},
        {'key': 'EventingReliabilityConsole', 'type': 'event_console', 'binds_to': CDP_SEGMENTATION_RUNTIME_TABLES},
    )
    return {
        'format': 'appgen.cdp-segmentation-control-catalog.v1',
        'ok': True,
        'pbc': 'cdp_segmentation',
        'controls': controls,
        'control_ids': tuple(item['key'] for item in controls),
        'side_effects': (),
    }


def cdp_segmentation_standalone_app_contract() -> dict:
    from .standalone import standalone_route_contracts

    route_manifest = standalone_route_contracts()
    return {
        'ok': route_manifest['ok'],
        'pbc': 'cdp_segmentation',
        'app_id': 'cdp_segmentation_one_pbc_app',
        'workbench_route': '/workbench/pbcs/cdp_segmentation',
        'navigation': (
            {'key': 'events', 'route': '/workbench/pbcs/cdp_segmentation/events'},
            {'key': 'profiles', 'route': '/workbench/pbcs/cdp_segmentation/profiles'},
            {'key': 'segments', 'route': '/workbench/pbcs/cdp_segmentation/segments'},
            {'key': 'memberships', 'route': '/workbench/pbcs/cdp_segmentation/memberships'},
            {'key': 'assistant', 'route': '/workbench/pbcs/cdp_segmentation/assistant'},
            {'key': 'release', 'route': '/workbench/pbcs/cdp_segmentation/release-evidence'},
        ),
        'service_routes': route_manifest['routes'],
        'forms': CDP_SEGMENTATION_FORM_KEYS,
        'wizards': CDP_SEGMENTATION_WIZARD_KEYS,
        'controls': CDP_SEGMENTATION_CONTROL_KEYS,
        'single_agent_namespace': 'cdp_segmentation_skills',
        'side_effects': (),
    }


def cdp_segmentation_ui_contract() -> dict:
    forms = cdp_segmentation_form_catalog()
    wizards = cdp_segmentation_wizard_catalog()
    controls = cdp_segmentation_control_catalog()
    return {
        'format': 'appgen.cdp-segmentation-ui-contract.v2',
        'ok': forms['ok'] and wizards['ok'] and controls['ok'],
        'pbc': 'cdp_segmentation',
        'implementation_directory': 'src/pyAppGen/pbcs/cdp_segmentation',
        'fragments': CDP_SEGMENTATION_UI_FRAGMENT_KEYS,
        'routes': (
            '/workbench/pbcs/cdp_segmentation',
            '/workbench/pbcs/cdp_segmentation/events',
            '/workbench/pbcs/cdp_segmentation/profiles',
            '/workbench/pbcs/cdp_segmentation/segments',
            '/workbench/pbcs/cdp_segmentation/memberships',
            '/workbench/pbcs/cdp_segmentation/configuration',
            '/workbench/pbcs/cdp_segmentation/assistant',
            '/workbench/pbcs/cdp_segmentation/controls',
            '/workbench/pbcs/cdp_segmentation/schema-contract',
            '/workbench/pbcs/cdp_segmentation/service-contract',
            '/workbench/pbcs/cdp_segmentation/release-evidence',
        ),
        'action_permissions': {
            'ingest_customer_event': 'cdp_segmentation.event.write',
            'upsert_profile_property': 'cdp_segmentation.event.write',
            'define_segment': 'cdp_segmentation.segment.write',
            'evaluate_segments': 'cdp_segmentation.membership.evaluate',
            'activate_segment': 'cdp_segmentation.membership.evaluate',
            'simulate_segment_membership': 'cdp_segmentation.analytics.write',
            'forecast_audience': 'cdp_segmentation.analytics.write',
            'resolve_audience_exception': 'cdp_segmentation.profile.govern',
            'parse_segment_rule': 'cdp_segmentation.segment.write',
            'score_lifecycle_risk': 'cdp_segmentation.analytics.write',
            'heal_profile_merge': 'cdp_segmentation.profile.govern',
            'generate_profile_proof': 'cdp_segmentation.profile.govern',
            'screen_consent_policy': 'cdp_segmentation.profile.govern',
            'run_data_quality_controls': 'cdp_segmentation.audit',
            'federate_customer_view': 'cdp_segmentation.profile.govern',
            'allocate_activation': 'cdp_segmentation.membership.evaluate',
            'detect_profile_anomaly': 'cdp_segmentation.analytics.write',
            'register_governed_model': 'cdp_segmentation.configure',
            'receive_event': 'cdp_segmentation.event.consume',
            'register_rule': 'cdp_segmentation.configure',
            'set_parameter': 'cdp_segmentation.configure',
            'configure_runtime': 'cdp_segmentation.configure',
            'run_control_tests': 'cdp_segmentation.audit',
            'build_schema_contract': 'cdp_segmentation.audit',
            'build_service_contract': 'cdp_segmentation.audit',
            'build_release_evidence': 'cdp_segmentation.audit',
        },
        'configuration_editor': {
            'required_fields': ('database_backend', 'event_topic', 'retry_limit', 'default_region', 'default_timezone', 'activation_mode'),
            'allowed_database_backends': CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
            'event_contract': 'AppGen-X',
            'required_event_topic': CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
            'stream_engine_picker_visible': False,
        },
        'parameter_editor': {
            'numeric_parameters': (
                'membership_score_threshold',
                'profile_merge_confidence_threshold',
                'event_freshness_days',
                'payment_value_weight',
                'order_recency_weight',
                'engagement_weight',
                'consent_risk_threshold',
                'activation_batch_limit',
                'max_segments_per_profile',
                'workbench_limit',
            ),
        },
        'rule_editor': {
            'rule_types': ('configuration', 'parameter', 'release_gate', 'domain_policy'),
            'required_fields': ('rule_id', 'tenant', 'scope', 'status', 'allowed_event_types', 'allowed_regions', 'segment_policy', 'consent_policy', 'activation_policy'),
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
        },
        'event_surfaces': {
            'emits': ('CustomerSegmentUpdated', 'ProfileEnriched'),
            'consumes': ('CustomerUpdated', 'PaymentCaptured', 'OrderShipped'),
            'outbox_status': 'visible',
            'dead_letter_status': 'visible',
        },
        'forms': {
            'event_intake': {
                'fields': ('event_id', 'tenant', 'customer_id', 'event_type', 'region', 'properties'),
                'submit_action': 'ingest_customer_event',
            },
            'segment_definition': {
                'fields': ('segment_id', 'tenant', 'name', 'criteria', 'status'),
                'submit_action': 'define_segment',
            },
            'document_instruction': {
                'fields': ('document', 'instructions', 'payload'),
                'submit_action': 'parse_segment_rule',
            },
        },
        'wizards': {
            'segment_simulation': {
                'steps': ('choose_segment', 'choose_customer', 'adjust_counterfactual', 'review_delta'),
                'submit_action': 'simulate_segment_membership',
            },
            'activation_readiness': {
                'steps': ('screen_consent', 'estimate_audience', 'allocate_budget', 'review_delivery'),
                'submit_action': 'allocate_activation',
            },
        },
        'controls': {
            'grid_filters': ('tenant', 'segment_status', 'membership_status', 'consent_status'),
            'quick_actions': ('evaluate_segments', 'activate_segment', 'run_data_quality_controls'),
            'document_actions': ('summarize', 'draft_segment', 'draft_profile_update', 'draft_governance_ticket'),
            'assistant_preview_route': '/app/cdp-segmentation/assistant/document-preview',
        },
        'form_catalog': forms['forms'],
        'wizard_catalog': wizards['wizards'],
        'control_catalog': controls['controls'],
        'advanced_panels': CDP_CONTROL_CAPABILITIES,
        'cdp_control_panels': tuple(f'cdp_control_{capability}' for capability in CDP_CONTROL_CAPABILITIES),
        'cdp_control_contract': improve1_cdp_control_contract(),
        'standalone_app': cdp_segmentation_standalone_app_contract(),
        'binding_evidence': {
            'owned_tables': CDP_SEGMENTATION_OWNED_TABLES,
            'runtime_tables': CDP_SEGMENTATION_RUNTIME_TABLES,
            'shared_table_access': False,
            'event_contract': 'AppGen-X',
            'required_event_topic': CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
            'form_ids': forms['form_ids'],
            'wizard_ids': wizards['wizard_ids'],
            'control_ids': controls['control_ids'],
        },
    }


def cdp_segmentation_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = cdp_segmentation_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, permission in contract['action_permissions'].items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {'key': 'events', 'value': view['event_count'], 'fragment': 'CustomerEventStream'},
        {'key': 'profiles', 'value': view['profile_count'], 'fragment': 'ProfilePropertyPanel'},
        {'key': 'segments', 'value': view['segment_count'], 'fragment': 'SegmentDefinitionBuilder'},
        {'key': 'memberships', 'value': view['membership_count'], 'fragment': 'MembershipEvaluationBoard'},
        {'key': 'consent_entries', 'value': view['consent_entry_count'], 'fragment': 'ProfileConsentTimeline'},
        {'key': 'transition_ledger', 'value': len(view['recent_membership_transitions']), 'fragment': 'MembershipTransitionLedger'},
        {'key': 'outbox', 'value': view['outbox_count'], 'fragment': 'CdpEventOutbox'},
        {'key': 'dead_letter', 'value': view['dead_letter_count'], 'fragment': 'CdpDeadLetterQueue'},
    )
    workbench_actions = (
        'ingest_customer_event',
        'define_segment',
        'evaluate_segments',
        'activate_segment',
        'run_data_quality_controls',
        'build_release_evidence',
    )
    return {
        'format': 'appgen.cdp-segmentation-workbench-render.v2',
        'ok': True,
        'tenant': tenant,
        'route': '/workbench/pbcs/cdp_segmentation',
        'fragments': contract['fragments'],
        'cards': cards,
        'navigation': contract['standalone_app']['navigation'],
        'visible_actions': visible_actions,
        'locked_actions': tuple(action for action in workbench_actions if action not in visible_actions),
        'configuration_bound': bool(state.get('configuration', {}).get('ok')),
        'rules_bound': tuple(sorted(state.get('rules', {}))),
        'parameters_bound': tuple(sorted(state.get('parameters', {}))),
        'event_outbox_count': len(state.get('outbox', ())),
        'dead_letter_count': len(state.get('dead_letter', ())),
        'alerts': view['alerts'],
        'top_segments': view['top_segments'],
        'forms': contract['forms'],
        'wizards': contract['wizards'],
        'controls': contract['controls'],
        'binding_evidence': view['binding_evidence'],
        'standalone_app': contract['standalone_app'],
    }


def cdp_segmentation_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
    document: str | None = None,
    instructions: str | None = None,
) -> dict:
    from .agent import document_instruction_crud_support

    shell = cdp_segmentation_standalone_app_contract()
    workbench = cdp_segmentation_render_workbench(
        state,
        tenant=tenant,
        principal_permissions=principal_permissions,
    )
    preview = document_instruction_crud_support(
        document or 'Prepare an audience for high value opted-in customers.',
        instructions or 'Draft the owned-table mutation preview for a new retention segment.',
    )
    return {
        'format': 'appgen.cdp-segmentation-standalone-render.v1',
        'ok': shell['ok'] and workbench['ok'] and preview['ok'],
        'pbc': 'cdp_segmentation',
        'tenant': tenant,
        'route': shell['workbench_route'],
        'shell': shell,
        'workbench': workbench,
        'assistant_preview': preview,
        'side_effects': (),
    }


def _view_counts(state: dict, tenant: str) -> dict:
    from .runtime import cdp_segmentation_build_workbench_view

    view = cdp_segmentation_build_workbench_view(state, tenant=tenant)
    return {
        **view,
        'binding_evidence': {
            'configuration': bool(state.get('configuration', {}).get('ok')),
            'rules': tuple(sorted(state.get('rules', {}))),
            'parameters': tuple(sorted(state.get('parameters', {}))),
            'owned_tables': CDP_SEGMENTATION_OWNED_TABLES,
            'runtime_tables': CDP_SEGMENTATION_RUNTIME_TABLES,
            'shared_table_access': False,
            'event_contract': 'AppGen-X',
        },
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        'configuration': _AppGenSmokeState({'ok': True}),
        'rules': _AppGenSmokeState(),
        'parameters': _AppGenSmokeState(),
        'outbox': (),
        'inbox': (),
        'dead_letter': (),
        'dead_letters': (),
        'events': (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = cdp_segmentation_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get('action_permissions', {}).values()))
    rendered = cdp_segmentation_render_workbench(
        _appgen_smoke_state(),
        tenant='smoke',
        principal_permissions=permissions,
    )
    standalone_render = cdp_segmentation_render_standalone_app(
        _appgen_smoke_state(),
        tenant='smoke',
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get('cards') or contract.get('panels') or contract.get('fragments', ()))
    configuration_editor = contract.get('configuration_editor', {})
    event_surfaces = contract.get('event_surfaces', {})
    rule_editor = contract.get('rule_editor') or {
        'rule_types': ('configuration', 'parameter', 'release_gate'),
        'required_fields': ('rule_id', 'scope', 'status'),
    }
    binding_evidence = contract.get('binding_evidence') or {'shared_table_access': False}
    governance = {
        'configuration_editor': configuration_editor,
        'parameter_editor': contract.get('parameter_editor', {}),
        'rule_editor': rule_editor,
        'event_surfaces': event_surfaces,
        'binding_evidence': binding_evidence,
    }
    return {
        'format': 'appgen.pbc-ui-smoke-test.v1',
        'ok': contract.get('ok') is True
        and rendered.get('ok') is True
        and standalone_render.get('ok') is True
        and bool(contract.get('fragments'))
        and bool(contract.get('routes'))
        and bool(cards)
        and bool(contract.get('action_permissions'))
        and bool(configuration_editor)
        and configuration_editor.get('stream_engine_picker_visible', configuration_editor.get('user_facing_stream_engine_picker', False)) is False
        and bool(contract.get('parameter_editor'))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ('outbox_status' in event_surfaces or 'contract' in event_surfaces)
        and binding_evidence.get('shared_table_access') is not True
        and not binding_evidence.get('shared_tables', ()),
        'manifest': {'fragments': contract.get('fragments', ()), 'routes': contract.get('routes', ())},
        'contract': contract,
        'governance': governance,
        'rendered': rendered,
        'standalone_render': standalone_render,
        'cards': cards,
        'side_effects': (),
    }
