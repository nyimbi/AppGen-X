from .standalone import real_estate_property_management_ui_contract, real_estate_property_management_render_workbench


def smoke_test():
    rendered = real_estate_property_management_render_workbench()
    return {'ok': real_estate_property_management_ui_contract()['ok'] and rendered['ok'] and 'queues' in rendered, 'side_effects': ()}
