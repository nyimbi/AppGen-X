"""UI fragments for the data_product_catalog PBC."""
PBC_KEY = 'data_product_catalog'
UI_FRAGMENTS = ('DataProductCatalogWorkbench', 'DataProductCatalogDetail', 'DataProductCatalogAssistantPanel')


def data_product_catalog_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('data_product_catalog.read', 'data_product_catalog.create', 'data_product_catalog.update', 'data_product_catalog.approve', 'data_product_catalog.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def data_product_catalog_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('data_product_catalog.read', 'data_product_catalog.create', 'data_product_catalog.update', 'data_product_catalog.approve', 'data_product_catalog.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': data_product_catalog_ui_contract()['ok'] and data_product_catalog_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as data_product_catalog_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as data_product_catalog_domain_capability_surface_contract

_BASE_DATA_PRODUCT_CATALOG_UI_CONTRACT = data_product_catalog_ui_contract
_BASE_DATA_PRODUCT_CATALOG_RENDER_WORKBENCH = data_product_catalog_render_workbench


def data_product_catalog_ui_contract():
    base = dict(_BASE_DATA_PRODUCT_CATALOG_UI_CONTRACT())
    full = data_product_catalog_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'full_capability_surface': full,
        'operation_actions': full['operation_actions'],
        'rule_editors': full['rule_editors'],
        'parameter_editors': full['parameter_editors'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'navigation_sections': full['navigation_sections'],
    }


def data_product_catalog_render_workbench(state=None):
    base = dict(_BASE_DATA_PRODUCT_CATALOG_RENDER_WORKBENCH(state=state))
    full = data_product_catalog_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'panels': tuple(dict.fromkeys(tuple(base.get('panels', ())) + full['navigation_sections'])),
        'operation_actions': full['operation_actions'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'agent_tools': full['agent_tools'],
    }
