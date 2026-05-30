from .controls import media_rights_content_monetization_control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .forms import media_rights_content_monetization_form_catalog
from .wizards import media_rights_content_monetization_wizard_catalog

PBC_KEY = 'media_rights_content_monetization'


def media_rights_content_monetization_ui_contract():
    surface = domain_capability_surface_contract()
    forms = media_rights_content_monetization_form_catalog()
    wizards = media_rights_content_monetization_wizard_catalog()
    controls = media_rights_content_monetization_control_catalog()
    return {
        'ok': surface['ok'] and forms['ok'] and wizards['ok'] and controls['ok'],
        'pbc': PBC_KEY,
        'fragments': (
            'MediaRightsContentMonetizationWorkbench',
            'MediaRightsContentMonetizationDetail',
            'MediaRightsContentMonetizationAssistantPanel',
        ),
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'action_permissions': (
            'media_rights_content_monetization.read',
            'media_rights_content_monetization.create',
            'media_rights_content_monetization.update',
            'media_rights_content_monetization.approve',
            'media_rights_content_monetization.admin',
        ),
        'forms': forms['forms'],
        'wizards': wizards['wizards'],
        'controls': controls['controls'],
        'standalone_views': (
            'availability_calendar',
            'conflict_resolution_queue',
            'royalty_waterfall_preview',
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
                'operations',
                'edge_case_triage',
                'advanced_intelligence',
                'release_evidence',
                'standalone_application',
            ),
            'coverage': surface['coverage'],
        },
        'side_effects': (),
    }



def media_rights_content_monetization_render_workbench():
    ui = media_rights_content_monetization_ui_contract()
    full = ui['full_capability_surface']
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'route': f'/workbench/pbcs/{PBC_KEY}',
        'operation_actions': full['operation_actions'],
        'table_browsers': full['table_browsers'],
        'form_ids': tuple(form['form_id'] for form in ui['forms']),
        'wizard_ids': tuple(wizard['wizard_id'] for wizard in ui['wizards']),
        'control_ids': tuple(control['control_id'] for control in ui['controls']),
        'side_effects': (),
    }



def media_rights_content_monetization_render_standalone_workbench(workbench: dict | None = None) -> dict:
    """Render a compact standalone-workbench view from package-local workbench data."""
    source = dict(workbench or {})
    metrics = dict(source.get('metrics', {}))
    calendar = tuple(source.get('availability_calendar', ()))
    conflicts = tuple(source.get('conflict_queue', ()))
    return {
        'ok': bool(metrics) or bool(calendar) or bool(conflicts),
        'pbc': PBC_KEY,
        'cards': (
            {'id': 'asset_count', 'value': metrics.get('rights_assets', 0)},
            {'id': 'active_licenses', 'value': metrics.get('active_licenses', 0)},
            {'id': 'open_conflicts', 'value': metrics.get('open_conflicts', 0)},
            {'id': 'approved_usage_records', 'value': metrics.get('approved_usage_records', 0)},
        ),
        'calendar_rows': calendar,
        'conflict_rows': conflicts,
        'side_effects': (),
    }



def smoke_test():
    manifest = media_rights_content_monetization_ui_contract()
    workbench = media_rights_content_monetization_render_workbench()
    rendered = media_rights_content_monetization_render_standalone_workbench(
        {
            'metrics': {'rights_assets': 1, 'active_licenses': 1, 'open_conflicts': 0, 'approved_usage_records': 1},
            'availability_calendar': (
                {'window_id': 'win_001', 'asset_id': 'asset_001', 'availability_state': 'live'},
            ),
            'conflict_queue': (),
        }
    )
    return {
        'ok': manifest['ok'] and workbench['ok'] and rendered['ok'],
        'manifest': {'fragments': manifest['fragments']},
        'rendered': rendered,
        'side_effects': (),
    }
