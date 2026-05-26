"""Command service layer for the personnel_identity PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.personnel_identity.events', 'inbox_topic': 'pbc.personnel_identity.inbox', 'outbox_table': 'personnel_identity_appgen_outbox_event', 'inbox_table': 'personnel_identity_appgen_inbox_event', 'dead_letter_table': 'personnel_identity_appgen_dead_letter_event', 'emitted': ({'event_type': 'DepartmentRegistered', 'schema': 'personnel_identity.department_registered.emitted.v1', 'topic': 'pbc.personnel_identity.events', 'outbox_table': 'personnel_identity_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'EmployeeCreated', 'schema': 'personnel_identity.employee_created.emitted.v1', 'topic': 'pbc.personnel_identity.events', 'outbox_table': 'personnel_identity_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'EmployeeStatusChanged', 'schema': 'personnel_identity.employee_status_changed.emitted.v1', 'topic': 'pbc.personnel_identity.events', 'outbox_table': 'personnel_identity_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'RoleChanged', 'schema': 'personnel_identity.role_changed.emitted.v1', 'topic': 'pbc.personnel_identity.events', 'outbox_table': 'personnel_identity_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'IdentityAttributeChanged', 'schema': 'personnel_identity.identity_attribute_changed.emitted.v1', 'topic': 'pbc.personnel_identity.events', 'outbox_table': 'personnel_identity_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'EmployeeProvisioned', 'schema': 'personnel_identity.employee_provisioned.consumed.v1', 'topic': 'pbc.personnel_identity.inbox', 'inbox_table': 'personnel_identity_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'personnel_identity.access_policy_changed.consumed.v1', 'topic': 'pbc.personnel_identity.inbox', 'inbox_table': 'personnel_identity_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrgUnitChanged', 'schema': 'personnel_identity.org_unit_changed.consumed.v1', 'topic': 'pbc.personnel_identity.inbox', 'inbox_table': 'personnel_identity_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'RoleReviewRequested', 'schema': 'personnel_identity.role_review_requested.consumed.v1', 'topic': 'pbc.personnel_identity.inbox', 'inbox_table': 'personnel_identity_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'personnel_identity_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'personnel_identity_appgen_inbox_event'}}


class PersonnelIdentityService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'personnel_identity',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_personnel_departments(self, payload=None):
        return self._command('command_personnel_departments', payload or {})

    def command_personnel_departments_id_hierarchy(self, payload=None):
        return self._command('command_personnel_departments_id_hierarchy', payload or {})

    def command_personnel_employees(self, payload=None):
        return self._command('command_personnel_employees', payload or {})

    def command_personnel_employees_id_contacts(self, payload=None):
        return self._command('command_personnel_employees_id_contacts', payload or {})

    def command_personnel_employees_id_documents(self, payload=None):
        return self._command('command_personnel_employees_id_documents', payload or {})

    def command_personnel_employees_id_status(self, payload=None):
        return self._command('command_personnel_employees_id_status', payload or {})

    def command_personnel_employees_id_roles(self, payload=None):
        return self._command('command_personnel_employees_id_roles', payload or {})

    def command_personnel_employees_id_attributes(self, payload=None):
        return self._command('command_personnel_employees_id_attributes', payload or {})

    def command_personnel_employees_id_verification(self, payload=None):
        return self._command('command_personnel_employees_id_verification', payload or {})

    def command_personnel_employees_id_proofs(self, payload=None):
        return self._command('command_personnel_employees_id_proofs', payload or {})

    def command_personnel_provisioning_routes(self, payload=None):
        return self._command('command_personnel_provisioning_routes', payload or {})

    def command_personnel_events_inbox(self, payload=None):
        return self._command('command_personnel_events_inbox', payload or {})

    def command_personnel_rules(self, payload=None):
        return self._command('command_personnel_rules', payload or {})

    def command_personnel_parameters(self, payload=None):
        return self._command('command_personnel_parameters', payload or {})

    def command_personnel_configuration(self, payload=None):
        return self._command('command_personnel_configuration', payload or {})

    def query_personnel_org_chart(self, payload=None):
        return self._command('query_personnel_org_chart', payload or {})

    def query_personnel_workbench(self, payload=None):
        return self._command('query_personnel_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = PersonnelIdentityService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'personnel_identity',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = PersonnelIdentityService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
