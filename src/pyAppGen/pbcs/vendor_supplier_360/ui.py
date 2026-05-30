"""UI fragments for the vendor_supplier_360 PBC."""
PBC_KEY = 'vendor_supplier_360'
from .app_surface import single_pbc_vendor_supplier_360_app_contract
UI_FRAGMENTS = ('VendorSupplier360Workbench', 'VendorSupplier360Detail', 'VendorSupplier360AssistantPanel')


def vendor_supplier_360_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('vendor_supplier_360.read', 'vendor_supplier_360.create', 'vendor_supplier_360.update', 'vendor_supplier_360.approve', 'vendor_supplier_360.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def vendor_supplier_360_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('vendor_supplier_360.read', 'vendor_supplier_360.create', 'vendor_supplier_360.update', 'vendor_supplier_360.approve', 'vendor_supplier_360.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': vendor_supplier_360_ui_contract()['ok'] and vendor_supplier_360_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as vendor_supplier_360_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as vendor_supplier_360_domain_capability_surface_contract

_BASE_VENDOR_SUPPLIER_360_UI_CONTRACT = vendor_supplier_360_ui_contract
_BASE_VENDOR_SUPPLIER_360_RENDER_WORKBENCH = vendor_supplier_360_render_workbench


def vendor_supplier_360_forms_contract():
    from .app_surface import vendor_supplier_360_forms_contract as _forms
    return _forms()

def vendor_supplier_360_wizards_contract():
    from .app_surface import vendor_supplier_360_wizards_contract as _wizards
    return _wizards()

def vendor_supplier_360_controls_contract():
    from .app_surface import vendor_supplier_360_controls_contract as _controls
    return _controls()


def vendor_supplier_360_ui_contract():
    base = dict(_BASE_VENDOR_SUPPLIER_360_UI_CONTRACT())
    full = vendor_supplier_360_ui_capability_surface_contract()
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
        'navigation_sections': full['navigation_sections'], 'forms': vendor_supplier_360_forms_contract()['forms'], 'wizards': vendor_supplier_360_wizards_contract()['wizards'], 'controls': vendor_supplier_360_controls_contract()['controls'], 'single_pbc_app': single_pbc_vendor_supplier_360_app_contract(),
    }


def vendor_supplier_360_render_workbench(state=None):
    base = dict(_BASE_VENDOR_SUPPLIER_360_RENDER_WORKBENCH(state=state))
    full = vendor_supplier_360_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'panels': tuple(dict.fromkeys(tuple(base.get('panels', ())) + full['navigation_sections'])),
        'operation_actions': full['operation_actions'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'agent_tools': full['agent_tools'], 'forms': vendor_supplier_360_forms_contract()['forms'], 'wizards': vendor_supplier_360_wizards_contract()['wizards'], 'controls': vendor_supplier_360_controls_contract()['controls'], 'single_pbc_app': single_pbc_vendor_supplier_360_app_contract(),
    }


def standalone_ui_smoke_test():
    contract = vendor_supplier_360_ui_contract()
    rendered = vendor_supplier_360_render_workbench()
    return {'ok': contract['ok'] and rendered['ok'] and bool(contract['forms']) and bool(contract['wizards']) and bool(contract['controls']) and contract['single_pbc_app']['ok'], 'contract': contract, 'rendered': rendered, 'side_effects': ()}
