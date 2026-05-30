"""Workbench UI surface for real estate property management."""
from .standalone import real_estate_property_management_ui_contract as _real_estate_property_management_ui_contract
from .standalone import real_estate_property_management_render_workbench as _real_estate_property_management_render_workbench


def real_estate_property_management_ui_contract():
    contract = _real_estate_property_management_ui_contract()
    contract['configuration_editor'] = True
    contract['stream_engine_picker_visible'] = False
    contract.setdefault('action_permissions', ('real_estate_property_management.read', 'real_estate_property_management.create', 'real_estate_property_management.update', 'real_estate_property_management.approve', 'real_estate_property_management.admin'))
    return contract


def real_estate_property_management_render_workbench():
    return _real_estate_property_management_render_workbench()


def smoke_test():
    rendered = real_estate_property_management_render_workbench()
    return {'ok': real_estate_property_management_ui_contract()['ok'] and rendered['ok'] and 'queues' in rendered, 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': real_estate_property_management_ui_contract()['action_permissions'], 'side_effects': ()}
