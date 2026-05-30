"""Service layer for the utility_outage_restoration PBC."""
from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, execute_domain_operation
from .models import UtilityOutageRestorationStandaloneStore, standalone_model_contract, standalone_store_smoke_test

PBC_KEY = 'utility_outage_restoration'
EVENT_CONTRACT = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
    'event_contract': 'AppGen-X',
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            'command_outage_incident',
            'configure_runtime',
            'set_parameter',
            'register_rule',
            'register_schema_extension',
            'receive_event',
            'run_advanced_assessment',
            'parse_document_instruction',
        )
        + tuple(DOMAIN_OPERATIONS)
    )
)
QUERY_OPERATIONS = ('query_workbench', 'build_workbench_view')
OWNED_TABLES = DOMAIN_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    return {
        'operation': name,
        'operation_kind': kind,
        'owned_tables': OWNED_TABLES[:2] if kind == 'command' else (),
        'read_tables': OWNED_TABLES[:2] if kind == 'query' else (),
        'emitted_event': 'UtilityOutageRestorationCreated' if kind == 'command' else None,
        'transaction_boundary': 'owned_datastore_plus_outbox' if kind == 'command' else 'read_only_projection',
    }


class UtilityOutageRestorationService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name in DOMAIN_OPERATIONS:
            plan = execute_domain_operation(name, payload)
            return {
                'ok': plan['ok'],
                'operation': name,
                'operation_kind': 'command',
                'read_only': False,
                'payload': dict(payload),
                'operation_contract': {
                    'operation': name,
                    'operation_kind': 'command',
                    'owned_tables': plan.get('owned_tables', ()),
                    'read_tables': (),
                    'emitted_event': plan.get('emitted_event'),
                    'transaction_boundary': 'owned_datastore_plus_outbox',
                },
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (plan.get('emitted_event'),),
                'transaction_boundary': 'owned_datastore_plus_outbox',
                'domain_depth': plan,
                'side_effects': (),
            }
        contract = _operation_contract(name, 'command')
        return {
            'ok': True,
            'operation': name,
            'operation_kind': 'command',
            'read_only': False,
            'payload': dict(payload),
            'operation_contract': contract,
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (contract['emitted_event'],),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'side_effects': (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        contract = _operation_contract(name, 'query')
        return {
            'ok': True,
            'operation': name,
            'operation_kind': 'query',
            'read_only': True,
            'payload': dict(payload),
            'operation_contract': contract,
            'outbox_table': None,
            'emits': (),
            'side_effects': (),
        }


def service_operation_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'service_class': 'UtilityOutageRestorationService',
        'command_operations': COMMAND_OPERATIONS,
        'query_operations': QUERY_OPERATIONS,
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, 'command') for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, 'query') for name in QUERY_OPERATIONS)
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'operation_contract': contracts[0], 'side_effects': ()}


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = 'query' if operation in manifest['query_operations'] else 'command'
    return {'ok': operation in manifest['query_operations'] + manifest['command_operations'], 'operation': operation, 'operation_kind': kind, 'payload': dict(payload or {}), 'side_effects': ()}


STANDALONE_OPERATION_CONTRACTS = (
    {'operation': 'register_network_asset_projection', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/network-assets', 'handler': 'register_network_asset_projection', 'permission': 'utility_outage_restoration.update', 'table': 'utility_outage_restoration_network_asset_projection', 'form': 'UtilityNetworkAssetProjectionForm', 'wizard': 'OutageTriageWizard'},
    {'operation': 'create_outage_incident', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/outages', 'handler': 'create_outage_incident', 'permission': 'utility_outage_restoration.create', 'table': 'utility_outage_restoration_outage_incident', 'form': 'UtilityOutageIncidentForm', 'wizard': 'OutageTriageWizard'},
    {'operation': 'record_trouble_call', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/trouble-calls', 'handler': 'record_trouble_call', 'permission': 'utility_outage_restoration.create', 'table': 'utility_outage_restoration_trouble_call', 'form': 'UtilityTroubleCallForm', 'wizard': 'OutageTriageWizard'},
    {'operation': 'create_oms_event', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/oms-events', 'handler': 'create_oms_event', 'permission': 'utility_outage_restoration.update', 'table': 'utility_outage_restoration_oms_event', 'form': 'UtilityOmsEventForm', 'wizard': 'CrewDispatchWizard'},
    {'operation': 'create_device_interruption', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/device-interruptions', 'handler': 'create_device_interruption', 'permission': 'utility_outage_restoration.update', 'table': 'utility_outage_restoration_device_interruption', 'form': 'UtilityDeviceInterruptionForm', 'wizard': 'OutageTriageWizard'},
    {'operation': 'dispatch_crew', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/crew-dispatch', 'handler': 'dispatch_crew', 'permission': 'utility_outage_restoration.update', 'table': 'utility_outage_restoration_crew_assignment', 'form': 'UtilityCrewDispatchForm', 'wizard': 'CrewDispatchWizard'},
    {'operation': 'author_switching_plan', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/switching-plan', 'handler': 'author_switching_plan', 'permission': 'utility_outage_restoration.approve', 'table': 'utility_outage_restoration_switching_step', 'form': 'UtilitySwitchingPlanForm', 'wizard': 'SwitchingRestorationWizard'},
    {'operation': 'isolate_safety', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/safety-isolations', 'handler': 'isolate_safety', 'permission': 'utility_outage_restoration.approve', 'table': 'utility_outage_restoration_safety_isolation', 'form': 'UtilitySafetyIsolationForm', 'wizard': 'SwitchingRestorationWizard'},
    {'operation': 'record_damage_assessment', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/damage-assessments', 'handler': 'record_damage_assessment', 'permission': 'utility_outage_restoration.update', 'table': 'utility_outage_restoration_damage_assessment', 'form': 'UtilityDamageAssessmentForm', 'wizard': 'StormModeCoordinationWizard'},
    {'operation': 'calculate_etr', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/etr', 'handler': 'calculate_etr', 'permission': 'utility_outage_restoration.update', 'table': 'utility_outage_restoration_restoration_estimate', 'form': 'UtilityRestorationEstimateForm', 'wizard': 'SwitchingRestorationWizard'},
    {'operation': 'open_nested_outage', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/nested-outages', 'handler': 'open_nested_outage', 'permission': 'utility_outage_restoration.create', 'table': 'utility_outage_restoration_outage_incident', 'form': 'UtilityNestedOutageForm', 'wizard': 'OutageTriageWizard'},
    {'operation': 'send_customer_notification', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/customer-notifications', 'handler': 'send_customer_notification', 'permission': 'utility_outage_restoration.update', 'table': 'utility_outage_restoration_customer_notification', 'form': 'UtilityCustomerNotificationForm', 'wizard': 'StormModeCoordinationWizard'},
    {'operation': 'request_mutual_aid', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/mutual-aid', 'handler': 'request_mutual_aid', 'permission': 'utility_outage_restoration.approve', 'table': 'utility_outage_restoration_mutual_aid_request', 'form': 'UtilityMutualAidRequestForm', 'wizard': 'StormModeCoordinationWizard'},
    {'operation': 'create_governed_assistance_session', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/governed-assistance', 'handler': 'create_governed_assistance_session', 'permission': 'utility_outage_restoration.approve', 'table': 'utility_outage_restoration_governed_assistance_session', 'form': 'UtilityGovernedAssistanceForm', 'wizard': 'GovernedAssistanceWizard'},
    {'operation': 'activate_storm_mode', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/storm-mode', 'handler': 'activate_storm_mode', 'permission': 'utility_outage_restoration.approve', 'table': 'utility_outage_restoration_oms_event', 'form': 'UtilityStormModeActivationForm', 'wizard': 'StormModeCoordinationWizard'},
    {'operation': 'verify_restoration', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/restoration-verification', 'handler': 'verify_restoration', 'permission': 'utility_outage_restoration.approve', 'table': 'utility_outage_restoration_restoration_verification', 'form': 'UtilityRestorationVerificationForm', 'wizard': 'SwitchingRestorationWizard'},
    {'operation': 'receive_event', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/utility-outage-restoration/events/inbox', 'handler': 'receive_event', 'permission': 'utility_outage_restoration.admin', 'table': 'utility_outage_restoration_appgen_inbox_event', 'form': 'UtilityEventInboxForm', 'wizard': 'GovernedAssistanceWizard'},
    {'operation': 'list_outages', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/utility-outage-restoration/outages', 'handler': 'list_outages', 'permission': 'utility_outage_restoration.read', 'table': 'utility_outage_restoration_outage_incident', 'form': None, 'wizard': None},
    {'operation': 'build_timeline', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/utility-outage-restoration/timeline', 'handler': 'build_timeline', 'permission': 'utility_outage_restoration.read', 'table': 'utility_outage_restoration_oms_event', 'form': None, 'wizard': None},
    {'operation': 'build_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/utility-outage-restoration/workbench', 'handler': 'build_workbench', 'permission': 'utility_outage_restoration.read', 'table': 'utility_outage_restoration_outage_incident', 'form': None, 'wizard': None},
    {'operation': 'compute_regulatory_indices', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/utility-outage-restoration/regulatory-indices', 'handler': 'compute_regulatory_indices', 'permission': 'utility_outage_restoration.read', 'table': 'utility_outage_restoration_reliability_metric', 'form': None, 'wizard': None},
)


def standalone_service_operation_contracts() -> dict:
    return {
        'format': 'appgen.utility-outage-restoration-standalone-service-contract.v1',
        'ok': bool(STANDALONE_OPERATION_CONTRACTS),
        'pbc': PBC_KEY,
        'store_contract': standalone_model_contract(),
        'operations': tuple(item['operation'] for item in STANDALONE_OPERATION_CONTRACTS),
        'command_operations': tuple(item['operation'] for item in STANDALONE_OPERATION_CONTRACTS if item['operation_kind'] == 'command'),
        'query_operations': tuple(item['operation'] for item in STANDALONE_OPERATION_CONTRACTS if item['operation_kind'] == 'query'),
        'contracts': STANDALONE_OPERATION_CONTRACTS,
        'side_effects': (),
    }


class UtilityOutageRestorationStandaloneService:
    def __init__(self, store: UtilityOutageRestorationStandaloneStore | None = None):
        self.store = store or UtilityOutageRestorationStandaloneStore()

    def close(self) -> None:
        self.store.close()

    def _wrap(self, operation: str, result: dict) -> dict:
        contract = next(item for item in STANDALONE_OPERATION_CONTRACTS if item['operation'] == operation)
        return {
            'ok': result.get('ok') is True,
            'operation': operation,
            'operation_kind': contract['operation_kind'],
            'route': {'method': contract['method'], 'path': contract['path']},
            'permission': contract['permission'],
            'table': contract['table'],
            'result': result,
            'side_effects': (),
        }

    def register_network_asset_projection(self, payload: dict | None = None) -> dict:
        return self._wrap('register_network_asset_projection', self.store.register_network_asset_projection(payload or {}))

    def create_outage_incident(self, payload: dict | None = None) -> dict:
        return self._wrap('create_outage_incident', self.store.create_outage_incident(payload or {}))

    def record_trouble_call(self, payload: dict | None = None) -> dict:
        return self._wrap('record_trouble_call', self.store.record_trouble_call(payload or {}))

    def create_oms_event(self, payload: dict | None = None) -> dict:
        return self._wrap('create_oms_event', self.store.create_oms_event(payload or {}))

    def create_device_interruption(self, payload: dict | None = None) -> dict:
        return self._wrap('create_device_interruption', self.store.create_device_interruption(payload or {}))

    def dispatch_crew(self, payload: dict | None = None) -> dict:
        return self._wrap('dispatch_crew', self.store.dispatch_crew(payload or {}))

    def author_switching_plan(self, payload: dict | None = None) -> dict:
        return self._wrap('author_switching_plan', self.store.author_switching_plan(payload or {}))

    def isolate_safety(self, payload: dict | None = None) -> dict:
        return self._wrap('isolate_safety', self.store.isolate_safety(payload or {}))

    def record_damage_assessment(self, payload: dict | None = None) -> dict:
        return self._wrap('record_damage_assessment', self.store.record_damage_assessment(payload or {}))

    def calculate_etr(self, payload: dict | None = None) -> dict:
        return self._wrap('calculate_etr', self.store.calculate_etr(payload or {}))

    def open_nested_outage(self, payload: dict | None = None) -> dict:
        return self._wrap('open_nested_outage', self.store.open_nested_outage(payload or {}))

    def send_customer_notification(self, payload: dict | None = None) -> dict:
        return self._wrap('send_customer_notification', self.store.send_customer_notification(payload or {}))

    def request_mutual_aid(self, payload: dict | None = None) -> dict:
        return self._wrap('request_mutual_aid', self.store.request_mutual_aid(payload or {}))

    def create_governed_assistance_session(self, payload: dict | None = None) -> dict:
        return self._wrap('create_governed_assistance_session', self.store.create_governed_assistance_session(payload or {}))

    def activate_storm_mode(self, payload: dict | None = None) -> dict:
        return self._wrap('activate_storm_mode', self.store.activate_storm_mode(payload or {}))

    def verify_restoration(self, payload: dict | None = None) -> dict:
        return self._wrap('verify_restoration', self.store.verify_restoration(payload or {}))

    def receive_event(self, payload: dict | None = None) -> dict:
        return self._wrap('receive_event', self.store.receive_event(payload or {}))

    def list_outages(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap('list_outages', {'ok': True, 'outages': self.store.list_outages(supplied.get('tenant', 'default')), 'side_effects': ()})

    def build_timeline(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap('build_timeline', self.store.build_timeline(supplied.get('outage_id', '')))

    def build_workbench(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap('build_workbench', self.store.build_workbench(supplied.get('tenant', 'default')))

    def compute_regulatory_indices(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap('compute_regulatory_indices', self.store.compute_regulatory_indices(supplied.get('tenant', 'default')))


def standalone_service_smoke_test() -> dict:
    service = UtilityOutageRestorationStandaloneService()
    try:
        projection = service.register_network_asset_projection({'projection_id': 'asset-service', 'tenant': 'tenant-service', 'asset_id': 'feeder-17'})
        outage = service.create_outage_incident({'outage_id': 'outage-service', 'tenant': 'tenant-service', 'incident_number': 'OMS-SVC-1', 'critical_customers': ({'customer_id': 'hospital-1'},)})
        crew = service.dispatch_crew({'outage_id': 'outage-service', 'crew_id': 'crew-17', 'eta_minutes': 25})
        switching = service.author_switching_plan({'outage_id': 'outage-service', 'plan_id': 'switch-svc', 'device_id': 'switch-17'})
        etr = service.calculate_etr({'outage_id': 'outage-service', 'crew_eta_minutes': 25})
        workbench = service.build_workbench({'tenant': 'tenant-service'})
        regulatory = service.compute_regulatory_indices({'tenant': 'tenant-service'})
        return {
            'ok': projection['ok'] and outage['ok'] and crew['ok'] and switching['ok'] and etr['ok'] and workbench['ok'] and regulatory['ok'] and standalone_store_smoke_test()['ok'],
            'projection': projection,
            'outage': outage,
            'workbench': workbench,
            'regulatory': regulatory,
            'side_effects': (),
        }
    finally:
        service.close()


def smoke_test():
    service = UtilityOutageRestorationService()
    command = getattr(service, COMMAND_OPERATIONS[0])({'tenant': 'tenant-smoke'})
    query = getattr(service, QUERY_OPERATIONS[0])({'tenant': 'tenant-smoke'})
    return {'ok': command['ok'] and query['ok'] and service_operation_contracts()['ok'], 'command': command, 'query': query, 'side_effects': ()}
