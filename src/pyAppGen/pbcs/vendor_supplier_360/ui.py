"""UI fragments for the vendor_supplier_360 PBC."""
PBC_KEY = 'vendor_supplier_360'
UI_FRAGMENTS = ('VendorSupplier360Workbench', 'VendorSupplier360Detail', 'VendorSupplier360AssistantPanel')


def vendor_supplier_360_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('vendor_supplier_360.read', 'vendor_supplier_360.create', 'vendor_supplier_360.update', 'vendor_supplier_360.approve', 'vendor_supplier_360.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def vendor_supplier_360_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('vendor_supplier_360.read', 'vendor_supplier_360.create', 'vendor_supplier_360.update', 'vendor_supplier_360.approve', 'vendor_supplier_360.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': vendor_supplier_360_ui_contract()['ok'] and vendor_supplier_360_render_workbench()['ok'], 'side_effects': ()}
