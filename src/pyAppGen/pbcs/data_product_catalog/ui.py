"""UI fragments for the data_product_catalog PBC."""
PBC_KEY = 'data_product_catalog'
UI_FRAGMENTS = ('DataProductCatalogWorkbench', 'DataProductCatalogDetail', 'DataProductCatalogAssistantPanel')


def data_product_catalog_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('data_product_catalog.read', 'data_product_catalog.create', 'data_product_catalog.update', 'data_product_catalog.approve', 'data_product_catalog.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def data_product_catalog_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('data_product_catalog.read', 'data_product_catalog.create', 'data_product_catalog.update', 'data_product_catalog.approve', 'data_product_catalog.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': data_product_catalog_ui_contract()['ok'] and data_product_catalog_render_workbench()['ok'], 'side_effects': ()}
