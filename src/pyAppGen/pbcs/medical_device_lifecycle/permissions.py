PBC_KEY = 'medical_device_lifecycle'
PERMISSIONS = ('medical_device_lifecycle.read',
 'medical_device_lifecycle.create',
 'medical_device_lifecycle.update',
 'medical_device_lifecycle.approve',
 'medical_device_lifecycle.admin')
ACTION_PERMISSIONS = {
    'view_workbench': 'medical_device_lifecycle.read',
    'register_device': 'medical_device_lifecycle.create',
    'assign_device': 'medical_device_lifecycle.update',
    'record_calibration': 'medical_device_lifecycle.approve',
    'record_maintenance': 'medical_device_lifecycle.approve',
    'launch_recall': 'medical_device_lifecycle.admin',
    'attach_regulatory_evidence': 'medical_device_lifecycle.approve',
    'preview_assistant_change': 'medical_device_lifecycle.read',
}

def permission_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'permissions': PERMISSIONS,
        'roles': ('operator', 'approver', 'auditor', 'biomed_admin'),
        'action_permissions': ACTION_PERMISSIONS,
        'side_effects': (),
    }

def authorize(permission, actor=None):
    return {'ok': permission in PERMISSIONS or permission == f'{PBC_KEY}.operate', 'permission': permission, 'actor': dict(actor or {}), 'side_effects': ()}

def smoke_test():
    manifest = permission_manifest()
    return {
        'ok': manifest['ok'] and bool(manifest['action_permissions']) and authorize(PERMISSIONS[0])['ok'],
        'side_effects': (),
    }
