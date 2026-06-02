"""Standalone executable app harness for the enterprise_pim PBC."""

from __future__ import annotations

from copy import deepcopy

from . import agent
from . import release_evidence
from . import routes
from . import seed_data
from . import ui
from .permissions import authorize_permission
from .permissions import permission_manifest
from .runtime import enterprise_pim_accept_dependency_schema
from .runtime import enterprise_pim_approve_validation_workflow
from .runtime import enterprise_pim_build_release_evidence
from .runtime import enterprise_pim_configure_runtime
from .runtime import enterprise_pim_create_attribute_group
from .runtime import enterprise_pim_create_product_relationship
from .runtime import enterprise_pim_create_taxonomy
from .runtime import enterprise_pim_define_attribute
from .runtime import enterprise_pim_define_product_bundle
from .runtime import enterprise_pim_define_variant_family
from .runtime import enterprise_pim_empty_state
from .runtime import enterprise_pim_open_pim_exception
from .runtime import enterprise_pim_publish_master_data
from .runtime import enterprise_pim_receive_event
from .runtime import enterprise_pim_register_attribute_validation_rule
from .runtime import enterprise_pim_register_attribute_value_option
from .runtime import enterprise_pim_register_locale_fallback_rule
from .runtime import enterprise_pim_register_rule
from .runtime import enterprise_pim_resolve_pim_exception
from .runtime import enterprise_pim_set_parameter
from .runtime import enterprise_pim_start_validation_workflow
from .runtime import enterprise_pim_upsert_localized_content
from .runtime import enterprise_pim_upsert_translation_memory


DEFAULT_GRANTED_PERMISSIONS = permission_manifest()["permissions"]


def _normalized_seed_steps():
    bootstrap = seed_data.bootstrap_seed_bundle()
    return bootstrap["steps"]


class EnterprisePimStandaloneApp:
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
        self._state = enterprise_pim_empty_state()
        self.bootstrap()

    @property
    def state(self) -> dict:
        return self.state_snapshot()

    def state_snapshot(self) -> dict:
        return deepcopy(self._state)

    def bootstrap(self) -> dict:
        bootstrap = seed_data.bootstrap_seed_bundle()
        configuration = {**bootstrap["configuration"], **self._configuration_override}
        state = enterprise_pim_empty_state()
        state = enterprise_pim_configure_runtime(state, configuration)["state"]
        for name, value in {**bootstrap["parameters"], **self._parameter_overrides}.items():
            state = enterprise_pim_set_parameter(state, name, value)["state"]
        for rule in bootstrap["rules"] + self._additional_rules:
            state = enterprise_pim_register_rule(state, rule)["state"]
        for dependency in bootstrap["dependency_schemas"]:
            state = enterprise_pim_accept_dependency_schema(
                state,
                dependency["dependency"],
                dependency["contract"],
            )["state"]
        if self._seed_demo:
            for step in bootstrap["steps"]:
                state = self.execute_domain_action(step["operation"], step["payload"], state=state)["state"]
        self._state = state
        return self.state_snapshot()

    def execute_domain_action(self, action: str, payload: dict | None = None, *, state: dict | None = None) -> dict:
        current_state = self._state if state is None else state
        supplied = dict(payload or {})
        if action == "create_taxonomy":
            result = enterprise_pim_create_taxonomy(current_state, supplied)
        elif action == "define_attribute":
            result = enterprise_pim_define_attribute(current_state, supplied)
        elif action == "create_attribute_group":
            result = enterprise_pim_create_attribute_group(current_state, supplied)
        elif action == "register_attribute_value_option":
            result = enterprise_pim_register_attribute_value_option(current_state, supplied)
        elif action == "register_attribute_validation_rule":
            result = enterprise_pim_register_attribute_validation_rule(current_state, supplied)
        elif action == "upsert_localized_content":
            result = enterprise_pim_upsert_localized_content(current_state, supplied)
        elif action == "upsert_translation_memory":
            result = enterprise_pim_upsert_translation_memory(current_state, supplied)
        elif action == "register_locale_fallback_rule":
            result = enterprise_pim_register_locale_fallback_rule(current_state, supplied)
        elif action == "start_validation_workflow":
            result = enterprise_pim_start_validation_workflow(current_state, supplied)
        elif action == "approve_validation_workflow":
            result = enterprise_pim_approve_validation_workflow(current_state, supplied["workflow_id"], approver=supplied["approver"])
        elif action == "accept_dependency_schema":
            result = enterprise_pim_accept_dependency_schema(current_state, supplied["dependency"], supplied["contract"])
        elif action == "receive_event":
            result = enterprise_pim_receive_event(current_state, supplied["event"], simulate_failure=bool(supplied.get("simulate_failure")))
        elif action == "publish_master_data":
            result = enterprise_pim_publish_master_data(current_state, supplied["taxonomy_id"], channels=tuple(supplied["channels"]))
        elif action == "create_product_relationship":
            result = enterprise_pim_create_product_relationship(current_state, supplied)
        elif action == "define_product_bundle":
            result = enterprise_pim_define_product_bundle(current_state, supplied)
        elif action == "define_variant_family":
            result = enterprise_pim_define_variant_family(current_state, supplied)
        elif action == "open_pim_exception":
            result = enterprise_pim_open_pim_exception(current_state, supplied)
        elif action == "resolve_pim_exception":
            result = enterprise_pim_resolve_pim_exception(current_state, supplied)
        else:
            raise ValueError(f"Unsupported standalone action: {action}")
        if state is None and "state" in result:
            self._state = result["state"]
        return result

    def ui_manifest(self) -> dict:
        contract = ui.enterprise_pim_ui_contract()
        return {
            **contract,
            "workbench": ui.enterprise_pim_render_workbench(
                self._state,
                tenant="tenant_demo",
                principal_permissions=DEFAULT_GRANTED_PERMISSIONS,
            ),
        }

    def route_manifest(self) -> dict:
        return routes.api_route_contracts()

    def release_manifest(self) -> dict:
        return release_evidence.build_release_evidence()

    def agent_manifest(self) -> dict:
        return agent.composed_agent_contribution()

    def document_plan(self, document: str = "", instructions: str = "") -> dict:
        return agent.document_instruction_plan(document=document, instructions=instructions)

    def crud_plan(self, action: str = "read", table: str | None = None, payload: dict | None = None) -> dict:
        return agent.datastore_crud_plan(action=action, table=table, payload=payload)

    def workbench(self, *, tenant: str = "tenant_demo", granted_permissions: tuple[str, ...] = DEFAULT_GRANTED_PERMISSIONS) -> dict:
        return ui.enterprise_pim_render_workbench(self._state, tenant=tenant, principal_permissions=granted_permissions)

    def dispatch_route(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        *,
        granted_permissions: tuple[str, ...] = DEFAULT_GRANTED_PERMISSIONS,
    ) -> dict:
        resolved = routes.resolve_route(method, path)
        if not resolved["handled"]:
            return {**resolved, "ok": False, "side_effects": ()}
        permission = resolved["route"]["permission"]
        permission_check = authorize_permission(permission, granted_permissions)
        if not permission_check["allowed"]:
            return {
                "ok": False,
                "handled": False,
                "reason": "forbidden",
                "route": resolved["route"],
                "required_permission": permission,
                "granted_permissions": tuple(granted_permissions),
                "side_effects": (),
            }
        normalized_payload = _normalize_route_payload(resolved["route"]["handler"], payload or {}, resolved["path_params"])
        dispatched = routes.dispatch_route(method, path, normalized_payload, state=self._state)
        if dispatched["ok"] and dispatched["result"].get("state") is not None:
            self._state = dispatched["result"]["state"]
        return {
            "ok": dispatched["ok"],
            "handled": True,
            "route": resolved["route"],
            "path_params": resolved["path_params"],
            "permission_check": permission_check,
            "result": dispatched["result"],
            "side_effects": (),
        }


def _normalize_route_payload(handler: str, payload: dict, path_params: dict) -> dict:
    normalized = dict(payload)
    if handler == "command_validation_workflows_id_approve" and "workflow_id" not in normalized:
        normalized["workflow_id"] = path_params.get("id")
    if handler == "command_pim_exception_resolutions" and "exception_id" not in normalized:
        normalized["exception_id"] = path_params.get("id")
    return normalized


def create_standalone_app(**kwargs) -> EnterprisePimStandaloneApp:
    return EnterprisePimStandaloneApp(**kwargs)


def smoke_test() -> dict:
    app = EnterprisePimStandaloneApp()
    workbench = app.workbench()
    route = app.dispatch_route(
        "GET",
        "/api/pbc/enterprise_pim/pim-workbench",
        {"tenant": "tenant_demo"},
    )
    runtime_release = enterprise_pim_build_release_evidence()
    return {
        "ok": workbench["ok"]
        and route["ok"]
        and app.agent_manifest()["ok"]
        and runtime_release["ok"]
        and bool(_normalized_seed_steps()),
        "workbench": workbench,
        "route": route,
        "agent": app.agent_manifest(),
        "runtime_release": runtime_release,
        "side_effects": (),
    }
