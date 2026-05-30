"""Standalone executable app harness for the permitting_licensing_inspections PBC."""
from __future__ import annotations

from copy import deepcopy

from . import agent
from . import release_evidence
from . import routes
from . import seed_data
from . import ui
from .permissions import authorize_permission, permission_manifest
from .runtime import (
    permitting_licensing_inspections_add_plan_set,
    permitting_licensing_inspections_approve_review_task,
    permitting_licensing_inspections_build_release_evidence,
    permitting_licensing_inspections_capture_pre_application,
    permitting_licensing_inspections_command_application,
    permitting_licensing_inspections_configure_runtime,
    permitting_licensing_inspections_create_inspection,
    permitting_licensing_inspections_empty_state,
    permitting_licensing_inspections_evaluate_renewal,
    permitting_licensing_inspections_query_workbench,
    permitting_licensing_inspections_receive_event,
    permitting_licensing_inspections_record_permit,
    permitting_licensing_inspections_record_violation,
    permitting_licensing_inspections_register_rule,
    permitting_licensing_inspections_register_schema_extension,
    permitting_licensing_inspections_review_license,
    permitting_licensing_inspections_set_parameter,
    permitting_licensing_inspections_simulate_fee_assessment,
)

DEFAULT_GRANTED_PERMISSIONS = permission_manifest()['permissions']


class PermittingLicensingInspectionsStandaloneApp:
    """In-memory one-PBC application harness backed by package-local runtime code."""

    def __init__(
        self,
        *,
        configuration: dict | None = None,
        parameter_overrides: dict | None = None,
        additional_rules: tuple[dict, ...] = (),
        seed_demo: bool = True,
    ) -> None:
        self._seed_demo = seed_demo
        self._configuration_override = dict(configuration or {})
        self._parameter_overrides = dict(parameter_overrides or {})
        self._additional_rules = tuple(dict(rule) for rule in additional_rules)
        self._state = permitting_licensing_inspections_empty_state()
        self.bootstrap()

    @property
    def state(self) -> dict:
        return self.state_snapshot()

    def state_snapshot(self) -> dict:
        return deepcopy(self._state)

    def bootstrap(self) -> dict:
        bundle = seed_data.bootstrap_seed_bundle()
        configuration = {**bundle['configuration'], **self._configuration_override}
        state = permitting_licensing_inspections_empty_state()
        state = permitting_licensing_inspections_configure_runtime(state, configuration)['state']
        for name, value in {**bundle['parameters'], **self._parameter_overrides}.items():
            state = permitting_licensing_inspections_set_parameter(state, name, value)['state']
        for rule in bundle['rules'] + self._additional_rules:
            state = permitting_licensing_inspections_register_rule(state, rule)['state']
        if self._seed_demo:
            for step in bundle['steps']:
                state = self.execute_action(step['operation'], step['payload'], state=state)['state']
        self._state = state
        return self.state_snapshot()

    def execute_action(self, action: str, payload: dict | None = None, *, state: dict | None = None) -> dict:
        current_state = self._state if state is None else state
        supplied = dict(payload or {})
        if action == 'configure_runtime':
            result = permitting_licensing_inspections_configure_runtime(current_state, supplied)
        elif action == 'set_parameter':
            result = permitting_licensing_inspections_set_parameter(current_state, supplied['name'], supplied['value'])
        elif action == 'register_rule':
            result = permitting_licensing_inspections_register_rule(current_state, supplied)
        elif action == 'register_schema_extension':
            result = permitting_licensing_inspections_register_schema_extension(current_state, supplied['table'], supplied['fields'])
        elif action == 'receive_event':
            result = permitting_licensing_inspections_receive_event(current_state, supplied)
        elif action == 'capture_pre_application':
            result = permitting_licensing_inspections_capture_pre_application(current_state, supplied)
        elif action == 'command_application':
            result = permitting_licensing_inspections_command_application(current_state, supplied)
        elif action == 'add_plan_set':
            result = permitting_licensing_inspections_add_plan_set(current_state, supplied)
        elif action == 'approve_review_task':
            result = permitting_licensing_inspections_approve_review_task(current_state, supplied)
        elif action == 'simulate_fee_assessment':
            result = permitting_licensing_inspections_simulate_fee_assessment(current_state, supplied)
        elif action == 'record_permit':
            result = permitting_licensing_inspections_record_permit(current_state, supplied)
        elif action == 'review_license':
            result = permitting_licensing_inspections_review_license(current_state, supplied)
        elif action == 'create_inspection':
            result = permitting_licensing_inspections_create_inspection(current_state, supplied)
        elif action == 'record_violation':
            result = permitting_licensing_inspections_record_violation(current_state, supplied)
        elif action == 'evaluate_renewal':
            result = permitting_licensing_inspections_evaluate_renewal(current_state, supplied)
        elif action == 'query_workbench':
            result = permitting_licensing_inspections_query_workbench(current_state, supplied)
        else:
            raise ValueError(f'Unsupported standalone action: {action}')
        if state is None and 'state' in result:
            self._state = result['state']
        return result

    def load_demo_workspace(self, *, tenant: str = 'tenant_demo') -> dict:
        app = PermittingLicensingInspectionsStandaloneApp(
            configuration=self._configuration_override,
            parameter_overrides=self._parameter_overrides,
            additional_rules=self._additional_rules,
            seed_demo=True,
        )
        self._state = app.state
        rendered = self.render_shell(tenant=tenant)
        return {'ok': rendered['ok'], 'tenant': tenant, 'rendered': rendered, 'side_effects': ()}

    def ui_manifest(self) -> dict:
        return ui.permitting_licensing_inspections_ui_contract()

    def route_manifest(self) -> dict:
        return routes.api_route_contracts()

    def release_manifest(self) -> dict:
        return release_evidence.build_release_evidence()

    def agent_manifest(self) -> dict:
        return agent.composed_agent_contribution()

    def document_plan(self, document: str = '', instruction: str = '') -> dict:
        return agent.document_instruction_plan(document=document, instruction=instruction)

    def crud_plan(self, action: str = 'read', table: str | None = None, payload: dict | None = None) -> dict:
        return agent.datastore_crud_plan(action=action, table=table, payload=payload)

    def workbench(self, *, tenant: str = 'tenant_demo', granted_permissions: tuple[str, ...] = DEFAULT_GRANTED_PERMISSIONS) -> dict:
        return ui.permitting_licensing_inspections_render_workbench(self._state, tenant=tenant, principal_permissions=granted_permissions)

    def render_shell(self, *, tenant: str = 'tenant_demo', granted_permissions: tuple[str, ...] = DEFAULT_GRANTED_PERMISSIONS) -> dict:
        return ui.permitting_licensing_inspections_render_standalone_app(self._state, tenant=tenant, principal_permissions=granted_permissions)

    def dispatch_route(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        *,
        granted_permissions: tuple[str, ...] = DEFAULT_GRANTED_PERMISSIONS,
    ) -> dict:
        resolved = routes.resolve_route(method, path)
        if not resolved['handled']:
            return {**resolved, 'ok': False, 'side_effects': ()}
        permission = resolved['route']['permission']
        permission_check = authorize_permission(permission, granted_permissions)
        if not permission_check['allowed']:
            return {
                'ok': False,
                'handled': False,
                'reason': 'forbidden',
                'route': resolved['route'],
                'required_permission': permission,
                'granted_permissions': tuple(granted_permissions),
                'side_effects': (),
            }
        dispatched = routes.dispatch_route(method, path, payload or {}, state=self._state)
        if dispatched['ok'] and dispatched['result']['result'].get('state') is not None:
            self._state = dispatched['result']['result']['state']
        return {
            'ok': dispatched['ok'],
            'handled': True,
            'route': resolved['route'],
            'permission_check': permission_check,
            'result': dispatched['result'],
            'side_effects': (),
        }


def create_standalone_app(**kwargs) -> PermittingLicensingInspectionsStandaloneApp:
    return PermittingLicensingInspectionsStandaloneApp(**kwargs)


def smoke_test() -> dict:
    app = PermittingLicensingInspectionsStandaloneApp()
    shell = app.render_shell()
    route = app.dispatch_route('GET', '/permitting-licensing-inspections-workbench', {'tenant': 'tenant_demo'})
    return {
        'ok': shell['ok']
        and route['ok']
        and app.release_manifest()['ok']
        and app.agent_manifest()['ok'],
        'shell': shell,
        'route': route,
        'release': app.release_manifest(),
        'agent': app.agent_manifest(),
        'runtime_release': permitting_licensing_inspections_build_release_evidence(),
        'side_effects': (),
    }
