"""Standalone executable app harness for the enterprise_pim PBC."""

from __future__ import annotations

from copy import deepcopy

from . import agent
from . import routes
from . import services
from . import ui
from .permissions import authorize_permission
from .permissions import permission_manifest
from .runtime import enterprise_pim_accept_dependency_schema
from .runtime import enterprise_pim_add_variant_member
from .runtime import enterprise_pim_approve_validation_workflow
from .runtime import enterprise_pim_assign_assortment
from .runtime import enterprise_pim_assign_data_steward
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
from .seed_data import bootstrap_seed_bundle


DEFAULT_GRANTED_PERMISSIONS = permission_manifest()["permissions"]
HANDLER_ACTIONS = {
    "command_product_taxonomies": "create_taxonomy",
    "command_product_attributes": "define_attribute",
    "command_attribute_groups": "create_attribute_group",
    "command_attribute_options": "register_attribute_value_option",
    "command_attribute_validation_rules": "register_attribute_validation_rule",
    "command_localized_content": "upsert_localized_content",
    "command_translation_memory": "upsert_translation_memory",
    "command_locale_fallbacks": "register_locale_fallback_rule",
    "command_validation_workflows": "start_validation_workflow",
    "command_validation_workflows_id_approve": "approve_validation_workflow",
    "command_dependency_schemas": "accept_dependency_schema",
    "command_pim_events": "receive_event",
    "command_pim_publications": "publish_master_data",
    "command_product_relationships": "create_product_relationship",
    "command_product_bundles": "define_product_bundle",
    "command_variant_families": "define_variant_family",
    "command_variant_members": "add_variant_member",
    "command_assortments": "assign_assortment",
    "command_data_stewards": "assign_data_steward",
    "command_pim_exceptions": "open_pim_exception",
    "command_pim_exception_resolutions": "resolve_pim_exception",
    "query_pim_workbench": "build_workbench_view",
}
FORMS = (
    {
        "key": "runtime_configuration",
        "title": "Runtime Configuration",
        "action": "configure_runtime",
        "required_fields": ("database_backend", "event_topic", "retry_limit", "default_locale", "allowed_locales"),
    },
    {
        "key": "taxonomy_definition",
        "title": "Taxonomy Definition",
        "action": "create_taxonomy",
        "required_fields": ("tenant", "taxonomy_id", "code", "name", "localized_names"),
    },
    {
        "key": "attribute_definition",
        "title": "Attribute Definition",
        "action": "define_attribute",
        "required_fields": ("tenant", "attribute_id", "taxonomy_id", "name", "data_type", "required"),
    },
    {
        "key": "localized_content_entry",
        "title": "Localized Content",
        "action": "upsert_localized_content",
        "required_fields": ("tenant", "content_id", "entity_id", "entity_type", "locale", "title", "description"),
    },
    {
        "key": "dependency_schema_registration",
        "title": "Dependency Schema Registration",
        "action": "accept_dependency_schema",
        "required_fields": ("dependency", "contract"),
    },
    {
        "key": "publication_readiness",
        "title": "Publication Readiness",
        "action": "publish_master_data",
        "required_fields": ("taxonomy_id", "channels"),
    },
)
WIZARDS = (
    {
        "key": "taxonomy_onboarding",
        "title": "Taxonomy Onboarding",
        "steps": ("configure_runtime", "create_taxonomy", "define_attribute", "create_attribute_group"),
    },
    {
        "key": "localization_readiness",
        "title": "Localization Readiness",
        "steps": ("upsert_localized_content", "upsert_translation_memory", "register_locale_fallback_rule"),
    },
    {
        "key": "publication_gate",
        "title": "Publication Gate",
        "steps": ("accept_dependency_schema", "receive_event", "start_validation_workflow", "approve_validation_workflow", "publish_master_data"),
    },
    {
        "key": "exception_resolution",
        "title": "Exception Resolution",
        "steps": ("open_pim_exception", "resolve_pim_exception"),
    },
)
CONTROLS = (
    {"key": "taxonomy_status_board", "binds_to": "product_taxonomy"},
    {"key": "attribute_quality_ledger", "binds_to": "attribute_quality_signal"},
    {"key": "workflow_lane_board", "binds_to": "validation_workflow"},
    {"key": "dependency_projection_queue", "binds_to": "dependency_projection"},
    {"key": "outbox_delivery_monitor", "binds_to": "outbox"},
    {"key": "release_evidence_console", "binds_to": "release_evidence"},
)


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
        self._configuration_override = dict(configuration or {})
        self._parameter_overrides = dict(parameter_overrides or {})
        self._additional_rules = tuple(dict(rule) for rule in additional_rules)
        self._seed_demo = seed_demo
        self._state = enterprise_pim_empty_state()
        self.bootstrap()

    def state_snapshot(self) -> dict:
        return deepcopy(self._state)

    def bootstrap(self) -> dict:
        bundle = bootstrap_seed_bundle()
        state = enterprise_pim_empty_state()
        state = enterprise_pim_configure_runtime(state, {**bundle["configuration"], **self._configuration_override})["state"]
        for name, value in {**bundle["parameters"], **self._parameter_overrides}.items():
            state = enterprise_pim_set_parameter(state, name, value)["state"]
        for rule in bundle["rules"] + self._additional_rules:
            state = enterprise_pim_register_rule(state, rule)["state"]
        for dependency in bundle["dependency_schemas"]:
            state = enterprise_pim_accept_dependency_schema(state, dependency["dependency"], dependency["contract"])["state"]
        if self._seed_demo:
            for step in bundle["steps"]:
                state = self.execute_action(step["operation"], step["payload"], state=state)["state"]
        self._state = state
        return self.state_snapshot()

    def execute_action(self, action: str, payload: dict | None = None, *, state: dict | None = None) -> dict:
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
        elif action == "add_variant_member":
            result = enterprise_pim_add_variant_member(current_state, supplied)
        elif action == "assign_assortment":
            result = enterprise_pim_assign_assortment(current_state, supplied)
        elif action == "assign_data_steward":
            result = enterprise_pim_assign_data_steward(current_state, supplied)
        elif action == "open_pim_exception":
            result = enterprise_pim_open_pim_exception(current_state, supplied)
        elif action == "resolve_pim_exception":
            result = enterprise_pim_resolve_pim_exception(current_state, supplied)
        elif action == "build_workbench_view":
            result = {
                "ok": True,
                "state": current_state,
                "workbench": ui.enterprise_pim_render_workbench(
                    current_state,
                    tenant=supplied.get("tenant", "tenant_demo"),
                    principal_permissions=tuple(supplied.get("granted_permissions", DEFAULT_GRANTED_PERMISSIONS)),
                ),
            }
        else:
            raise ValueError(f"Unsupported standalone action: {action}")
        if state is None and "state" in result:
            self._state = result["state"]
        return result

    def describe_ui(self) -> dict:
        contract = ui.enterprise_pim_ui_contract()
        return {
            **contract,
            "forms": FORMS,
            "wizards": WIZARDS,
            "controls": CONTROLS,
            "workbench": self.workbench(),
        }

    def workbench(self, *, tenant: str = "tenant_demo", granted_permissions: tuple[str, ...] = DEFAULT_GRANTED_PERMISSIONS) -> dict:
        rendered = ui.enterprise_pim_render_workbench(self._state, tenant=tenant, principal_permissions=granted_permissions)
        return {
            **rendered,
            "forms": FORMS,
            "wizards": WIZARDS,
            "controls": CONTROLS,
        }

    def release_manifest(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()

    def route_manifest(self) -> dict:
        return routes.api_route_contracts()

    def service_manifest(self) -> dict:
        return services.service_operation_contracts()

    def agent_manifest(self) -> dict:
        return agent.composed_agent_contribution()

    def document_plan(self, document: str = "", instructions: str = "") -> dict:
        return agent.document_instruction_plan(document=document, instructions=instructions)

    def crud_plan(self, action: str = "read", table: str | None = None, payload: dict | None = None) -> dict:
        return agent.datastore_crud_plan(action=action, table=table, payload=payload)

    def resolve_route(self, method: str, path: str) -> dict:
        for route in routes.ROUTES:
            if route["method"] != method:
                continue
            params = _match_route(route["path"], path)
            if params is not None:
                return {"handled": True, "route": route, "path_params": params}
        return {"handled": False, "route": None, "path_params": {}}

    def dispatch_route(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        *,
        granted_permissions: tuple[str, ...] = DEFAULT_GRANTED_PERMISSIONS,
    ) -> dict:
        resolved = self.resolve_route(method, path)
        if not resolved["handled"]:
            return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
        route = resolved["route"]
        payload_data = {**resolved["path_params"], **dict(payload or {})}
        action_name = HANDLER_ACTIONS.get(route["handler"])
        required_permission = permission_manifest()["action_permissions"].get(action_name, route["permission"])
        permission_check = authorize_permission(required_permission, granted_permissions)
        if not permission_check["allowed"]:
            return {
                "ok": False,
                "handled": False,
                "reason": "forbidden",
                "route": route,
                "required_permission": required_permission,
                "granted_permissions": tuple(granted_permissions),
                "side_effects": (),
            }
        if action_name == "approve_validation_workflow" and "workflow_id" not in payload_data:
            payload_data["workflow_id"] = payload_data["id"]
        if action_name == "resolve_pim_exception" and "exception_id" not in payload_data:
            payload_data["exception_id"] = payload_data["id"]
        result = self.execute_action(action_name, payload_data)
        return {
            "ok": result.get("ok") is True,
            "handled": True,
            "route": route,
            "path_params": resolved["path_params"],
            "permission_check": permission_check,
            "result": result,
            "side_effects": (),
        }


def _match_route(template: str, path: str) -> dict | None:
    template_parts = tuple(part for part in template.strip("/").split("/") if part)
    path_parts = tuple(part for part in path.strip("/").split("/") if part)
    if len(template_parts) != len(path_parts):
        return None
    params = {}
    for expected, actual in zip(template_parts, path_parts):
        if expected.startswith("{") and expected.endswith("}"):
            params[expected[1:-1]] = actual
            continue
        if expected != actual:
            return None
    return params


def create_standalone_app(**kwargs) -> EnterprisePimStandaloneApp:
    return EnterprisePimStandaloneApp(**kwargs)


def smoke_test() -> dict:
    app = EnterprisePimStandaloneApp()
    route = app.dispatch_route("GET", "/api/pbc/enterprise_pim/pim-workbench", {"tenant": "tenant_demo"})
    ui_manifest = app.describe_ui()
    agent_manifest = app.agent_manifest()
    service_manifest = app.service_manifest()
    return {
        "ok": route["ok"]
        and ui_manifest["ok"]
        and agent_manifest["ok"]
        and service_manifest["ok"]
        and bool(ui_manifest["forms"])
        and bool(ui_manifest["wizards"])
        and bool(ui_manifest["controls"]),
        "route": route,
        "ui": ui_manifest,
        "agent": agent_manifest,
        "service": service_manifest,
        "side_effects": (),
    }
