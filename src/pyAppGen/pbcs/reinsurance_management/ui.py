"""UI and standalone app surfaces for the reinsurance_management PBC."""

from __future__ import annotations

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_FORMS,
    DOMAIN_OPERATIONS,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    DOMAIN_WIZARDS,
    DOMAIN_WORKBENCH_VIEWS,
    domain_capability_surface_contract,
)
from .runtime import (
    PBC_KEY,
    REINSURANCE_MANAGEMENT_BUSINESS_TABLES,
    REINSURANCE_MANAGEMENT_PERMISSION_SET,
    reinsurance_management_build_workbench_view,
)


def reinsurance_management_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'fragments': (
            'ReinsuranceManagementWorkbench',
            'ReinsuranceManagementTreatyWizard',
            'ReinsuranceManagementRecoveryConsole',
            'ReinsuranceManagementAssistantPanel',
        ),
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'action_permissions': {
            'read': REINSURANCE_MANAGEMENT_PERMISSION_SET[0],
            'create': REINSURANCE_MANAGEMENT_PERMISSION_SET[1],
            'update': REINSURANCE_MANAGEMENT_PERMISSION_SET[2],
            'approve': REINSURANCE_MANAGEMENT_PERMISSION_SET[3],
            'admin': REINSURANCE_MANAGEMENT_PERMISSION_SET[4],
        },
        'full_capability_surface': {
            'operation_actions': DOMAIN_OPERATIONS,
            'rule_editors': DOMAIN_RULES,
            'parameter_editors': DOMAIN_PARAMETERS,
            'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES,
            'table_browsers': REINSURANCE_MANAGEMENT_BUSINESS_TABLES,
            'edge_case_queues': DOMAIN_EDGE_CASES,
            'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS),
            'navigation_sections': ('overview', 'treaty_programs', 'recoveries', 'cat_room', 'settlement_ops', 'assistant_preview', 'release_evidence'),
            'coverage': surface['coverage'],
            'forms': DOMAIN_FORMS,
            'wizards': DOMAIN_WIZARDS,
            'workbench_views': DOMAIN_WORKBENCH_VIEWS,
            'filters': ('treaty_type', 'counterparty', 'peril', 'aging_bucket', 'statement_period', 'status'),
        },
        'side_effects': (),
    }


def _workbench_controls() -> tuple[dict, ...]:
    return (
        {'id': 'launch_treaty_onboarding', 'label': 'New Treaty Wizard', 'wizard': 'treaty_onboarding'},
        {'id': 'launch_cat_event', 'label': 'Open Cat Event Room', 'wizard': 'cat_event_response'},
        {'id': 'launch_cash_call', 'label': 'Prepare Cash Call', 'wizard': 'cash_call_collection'},
        {'id': 'launch_commutation', 'label': 'Run Commutation Case', 'wizard': 'commutation_negotiation'},
    )


def reinsurance_management_render_workbench(
    state: dict | None = None,
    *,
    tenant: str = 'default',
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    base = reinsurance_management_build_workbench_view(state, tenant=tenant)
    permissions = principal_permissions or tuple(reinsurance_management_ui_contract()['action_permissions'].values())
    queues = {
        'aged_recoverables': [item for item in base['boards']['recoverables'] if item.get('aging_bucket') in {'61_90', '90_plus'}],
        'cat_events': [item for item in base['boards']['events'] if item.get('status') == 'open'],
        'cash_calls': [item for item in base['boards']['cash_calls'] if item.get('status') in {'issued', 'scheduled'}],
    }
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'tenant': tenant,
        'permissions': permissions,
        'workbench': {
            **base,
            'controls': _workbench_controls(),
            'queues': queues,
            'assistant_panel': {
                'title': 'Document and Instruction Preview',
                'preview_required_for_mutations': True,
                'supported_entities': ('treaty', 'bordereau', 'claim recovery', 'statement', 'cash call', 'retrocession'),
            },
        },
        'side_effects': (),
    }


def reinsurance_management_standalone_app_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'app_shell': {
            'name': 'Reinsurance Management Standalone',
            'mount_path': f'/apps/{PBC_KEY}',
            'navigation': ('Dashboard', 'Treaties', 'Placements', 'Recoverables', 'Cat Room', 'Statements', 'Assistant'),
            'workbench_route': '/api/pbc/reinsurance_management/workbench',
        },
        'side_effects': (),
    }


def reinsurance_management_render_standalone_app(
    state: dict | None = None,
    *,
    tenant: str = 'default',
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'app': reinsurance_management_standalone_app_contract(),
        'workbench': reinsurance_management_render_workbench(
            state,
            tenant=tenant,
            principal_permissions=principal_permissions,
        )['workbench'],
        'side_effects': (),
    }


def smoke_test() -> dict:
    rendered = reinsurance_management_render_workbench(None, tenant='tenant-smoke')
    return {
        'ok': reinsurance_management_ui_contract()['ok'] and reinsurance_management_render_standalone_app(None, tenant='tenant-smoke')['ok'] and bool(rendered['workbench']['controls']),
        'side_effects': (),
    }
