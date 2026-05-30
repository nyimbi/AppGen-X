"""UI contracts for the permitting_licensing_inspections PBC."""
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
from .runtime import (
    PBC_KEY,
    PERMITTING_LICENSING_INSPECTIONS_UI_FRAGMENT_KEYS,
    permitting_licensing_inspections_build_controls_contract,
    permitting_licensing_inspections_build_forms_contract,
    permitting_licensing_inspections_build_wizards_contract,
    permitting_licensing_inspections_build_workbench_view,
    permitting_licensing_inspections_empty_state,
)


def permitting_licensing_inspections_ui_contract():
    surface = domain_capability_surface_contract()
    forms = permitting_licensing_inspections_build_forms_contract()
    wizards = permitting_licensing_inspections_build_wizards_contract()
    controls = permitting_licensing_inspections_build_controls_contract()
    workbench = permitting_licensing_inspections_build_workbench_view()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'fragments': PERMITTING_LICENSING_INSPECTIONS_UI_FRAGMENT_KEYS,
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'action_permissions': (
            'permitting_licensing_inspections.read',
            'permitting_licensing_inspections.create',
            'permitting_licensing_inspections.update',
            'permitting_licensing_inspections.approve',
            'permitting_licensing_inspections.admin',
        ),
        'forms': forms['forms'],
        'wizards': wizards['wizards'],
        'controls': controls['controls'],
        'workbench': workbench,
        'persona_tabs': (
            'intake',
            'plan_review',
            'issuance',
            'inspections',
            'renewals',
            'enforcement',
            'release_evidence',
        ),
        'full_capability_surface': {
            'operation_actions': DOMAIN_OPERATIONS,
            'rule_editors': DOMAIN_RULES,
            'parameter_editors': DOMAIN_PARAMETERS,
            'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES,
            'table_browsers': DOMAIN_OWNED_TABLES,
            'edge_case_queues': DOMAIN_EDGE_CASES,
            'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS),
            'navigation_sections': (
                'overview',
                'forms',
                'wizards',
                'controls',
                'timeline',
                'release_evidence',
            ),
            'coverage': surface['coverage'],
        },
        'side_effects': (),
    }


def permitting_licensing_inspections_render_workbench(state=None, *, tenant='tenant_demo', principal_permissions=()):
    current_state = state or permitting_licensing_inspections_empty_state()
    ui = permitting_licensing_inspections_ui_contract()
    workbench = permitting_licensing_inspections_build_workbench_view(tenant=tenant, state=current_state)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'route': '/permitting-licensing-inspections-workbench',
        'tenant': tenant,
        'views': workbench['views'],
        'cards': workbench['cards'],
        'lanes': workbench['lanes'],
        'forms': tuple(form['name'] for form in ui['forms']),
        'wizards': tuple(wizard['name'] for wizard in ui['wizards']),
        'controls': tuple(control['name'] for control in ui['controls']),
        'permissions': tuple(principal_permissions),
        'table_browsers': ui['full_capability_surface']['table_browsers'],
        'release_scorecard': workbench['release_scorecard'],
        'side_effects': (),
    }


def permitting_licensing_inspections_standalone_app_contract():
    ui = permitting_licensing_inspections_ui_contract()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'app_id': f'{PBC_KEY}_one_pbc_app',
        'title': 'Permitting Licensing and Inspections One-PBC App',
        'navigation': (
            {'label': 'Workbench', 'route': '/permitting-licensing-inspections-workbench'},
            {'label': 'Release Scorecard', 'route': '/permitting-licensing-inspections-workbench#release'},
            {'label': 'Citizen Intake', 'route': '/permitting-licensing-inspections-workbench#intake'},
        ),
        'forms': ui['forms'],
        'wizards': ui['wizards'],
        'controls': ui['controls'],
        'fragments': ui['fragments'],
        'side_effects': (),
    }


def permitting_licensing_inspections_render_standalone_app(state=None, *, tenant='tenant_demo', principal_permissions=()):
    rendered = permitting_licensing_inspections_render_workbench(state, tenant=tenant, principal_permissions=principal_permissions)
    return {
        'ok': rendered['ok'],
        'pbc': PBC_KEY,
        'shell': permitting_licensing_inspections_standalone_app_contract(),
        'workbench': rendered,
        'release_summary': rendered['release_scorecard'],
        'side_effects': (),
    }


def smoke_test():
    state = permitting_licensing_inspections_empty_state()
    return {
        'ok': permitting_licensing_inspections_ui_contract()['ok']
        and permitting_licensing_inspections_render_workbench(state)['ok']
        and permitting_licensing_inspections_standalone_app_contract()['ok']
        and permitting_licensing_inspections_render_standalone_app(state)['ok'],
        'side_effects': (),
    }
