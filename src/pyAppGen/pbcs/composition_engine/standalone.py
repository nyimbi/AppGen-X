"""Standalone application surface for the Composition Engine PBC."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from . import agent
from . import controls
from . import forms
from . import routes
from . import runtime
from . import ui
from . import wizards
from .config import PARAMETER_SCHEMA
from .config import RULE_TEMPLATE
from .repository import CompositionEngineRepository
from .repository import repository_manifest

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "allowed_targets": ("web", "admin", "mobile"),
    "allowed_layout_modes": ("grid", "flow", "dashboard"),
    "publication_mode": "side_effect_free_plan",
    "default_timezone": "UTC",
    "workbench_limit": 50,
}
DEFAULT_PARAMETERS = {item["key"]: item["default"] for item in PARAMETER_SCHEMA}
DEFAULT_RULE = {
    **RULE_TEMPLATE,
    "rule_id": "composition_engine.workspace_release_gate",
    "required_fragments": ("CompositionWorkbench",),
    "allowed_meshes": ("platform", "relationship", "operations"),
    "route_policy": "balanced",
    "requires_approval": True,
    "severity": "blocking",
    "status": "active",
}


@dataclass(frozen=True)
class _OperationMatch:
    operation: str
    path_parameters: dict[str, str]


class CompositionEngineStandaloneApp:
    """Database-backed standalone app that executes composition workflows."""

    def __init__(self, database_path: str = ":memory:", *, bootstrap: bool = False) -> None:
        self.repository = CompositionEngineRepository(database_path=database_path)
        self.applied_migrations = self.repository.apply_migrations()
        self.state = runtime.composition_engine_empty_state()
        if bootstrap:
            self.bootstrap()
        else:
            self.repository.sync_state(self.state)

    def close(self) -> None:
        self.repository.close()

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict[str, Any]:
        self.state = runtime.composition_engine_configure_runtime(self.state, dict(DEFAULT_CONFIGURATION))["state"]
        for key, value in DEFAULT_PARAMETERS.items():
            self.state = runtime.composition_engine_set_parameter(self.state, key, value)["state"]
        self.state = runtime.composition_engine_register_rule(
            self.state,
            {
                **DEFAULT_RULE,
                "tenant": tenant,
            },
        )["state"]
        self.state = runtime.composition_engine_receive_event(
            self.state,
            {
                "event_id": f"schema-{tenant}",
                "event_type": "SchemaAccepted",
                "payload": {
                    "tenant": tenant,
                    "schema_id": "CustomerProfile",
                    "owner_pbc": "customer_360",
                },
            },
        )["state"]
        self.repository.sync_state(self.state)
        return {
            "ok": True,
            "tenant": tenant,
            "applied_migrations": self.applied_migrations,
            "configuration": dict(self.state["configuration"]),
            "side_effects": (),
        }

    def submit_form(self, form_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        validation = forms.composition_engine_validate_form_payload(form_id, payload)
        if not validation["ok"]:
            return {
                "ok": False,
                "form_id": form_id,
                "validation": validation,
                "reason": "invalid_form_payload",
                "side_effects": (),
            }
        form = forms.composition_engine_get_form(form_id)["form"]
        result = self._execute_operation(form["operation"], payload)
        if result.get("state") is not None:
            self.state = result["state"]
            self.repository.sync_state(self.state)
        return {
            "ok": result.get("ok") is True,
            "form_id": form_id,
            "operation": form["operation"],
            "result": result,
            "side_effects": (),
        }

    def run_wizard(self, wizard_id: str, step_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
        plan = wizards.composition_engine_plan_wizard(wizard_id, context=step_payloads.get("context", {}))
        if not plan["ok"]:
            return {"ok": False, "wizard_id": wizard_id, "plan": plan, "side_effects": ()}
        context = dict(step_payloads.get("context", {}))
        step_results = []
        for step in plan["steps"]:
            step_payload = {**context, **dict(step_payloads.get(step["step_id"], {}))}
            if "workspace_id" not in step_payload and "workspace_id" in context:
                step_payload["workspace_id"] = context["workspace_id"]
            result = self.submit_form(step["form_id"], step_payload)
            if not result["ok"]:
                return {
                    "ok": False,
                    "wizard_id": wizard_id,
                    "plan": plan,
                    "failed_step": step["step_id"],
                    "step_results": tuple(step_results),
                    "result": result,
                    "side_effects": (),
                }
            operation_result = result["result"]
            if step["operation"] == "create_workspace":
                context["workspace_id"] = operation_result["workspace"]["workspace_id"]
            step_results.append({"step_id": step["step_id"], "result": operation_result})
        return {
            "ok": True,
            "wizard_id": wizard_id,
            "workspace_id": context.get("workspace_id"),
            "steps": tuple(step_results),
            "side_effects": (),
        }

    def dispatch(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        matched = self._match_operation(method, path)
        if matched is None:
            return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
        merged_payload = {**payload, **matched.path_parameters}
        if "id" in merged_payload and "workspace_id" not in merged_payload:
            merged_payload["workspace_id"] = merged_payload["id"]
        result = self._execute_operation(matched.operation, merged_payload)
        if result.get("state") is not None:
            self.state = result["state"]
            self.repository.sync_state(self.state)
        return {
            "ok": result.get("ok") is True,
            "handled": True,
            "operation": matched.operation,
            "result": result,
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict[str, Any]:
        permissions = principal_permissions or tuple(sorted(set(ui.composition_engine_ui_contract()["action_permissions"].values())))
        workbench = ui.composition_engine_render_workbench(self.state, tenant=tenant, principal_permissions=permissions)
        return {
            "ok": workbench["ok"],
            "shell": {
                "app_id": "composition_engine_one_pbc_app",
                "route": workbench["route"],
                "database_backed": True,
                "forms": tuple(form["form_id"] for form in forms.composition_engine_form_catalog()["forms"]),
                "wizards": tuple(wizard["wizard_id"] for wizard in wizards.composition_engine_wizard_catalog()["wizards"]),
                "controls": tuple(control["control_id"] for control in controls.composition_engine_control_catalog()["controls"]),
            },
            "workbench": workbench,
            "side_effects": (),
        }

    def assistant_preview(
        self,
        document_text: str,
        instructions: str,
        *,
        action: str = "read",
        target_table: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return agent.assistant_preview(
            document_text,
            instructions,
            action=action,
            table=target_table,
            payload=payload,
        )

    def control_center(self, *, workspace_id: str | None = None) -> dict[str, Any]:
        return controls.composition_engine_control_center(self.state, workspace_id=workspace_id)

    def release_snapshot(self) -> dict[str, Any]:
        from . import release_evidence

        return {
            "ok": True,
            "repository": self.repository.database_manifest(),
            "release_evidence": release_evidence.build_release_evidence(),
            "side_effects": (),
        }

    def _execute_operation(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        if operation == "create_workspace":
            return runtime.composition_engine_create_workspace(
                self.state,
                {
                    "workspace_id": payload["workspace_id"],
                    "tenant": payload["tenant"],
                    "name": payload["name"],
                    "owner": payload["owner"],
                    "target": payload["target"],
                },
            )
        if operation == "select_pbc":
            return runtime.composition_engine_select_pbc(
                self.state,
                payload["workspace_id"],
                {
                    "pbc": payload["pbc"],
                    "mesh": payload["mesh"],
                    "reason": payload["reason"],
                },
            )
        if operation == "register_component":
            component_result = runtime.composition_engine_register_component(
                self.state,
                {
                    "tenant": payload["tenant"],
                    "component_id": payload["component_id"],
                    "pbc": payload["pbc"],
                    "fragment": payload["fragment"],
                    "permissions": tuple(payload["permissions"]),
                    "schemas": tuple(payload["schemas"]),
                },
            )
            next_state = component_result["state"]
            fragment_result = None
            if payload.get("fragment_id") and payload.get("route"):
                fragment_result = runtime.composition_engine_register_ui_fragment(
                    next_state,
                    {
                        "tenant": payload["tenant"],
                        "fragment_id": payload["fragment_id"],
                        "component_id": payload["component_id"],
                        "route": payload["route"],
                        "slots": tuple(payload.get("slots", ("main",))),
                        "events": tuple(payload.get("events", ())),
                    },
                )
                next_state = fragment_result["state"]
            return {
                "ok": component_result["ok"] and (fragment_result is None or fragment_result["ok"]),
                "state": next_state,
                "component": component_result["component"],
                "fragment": fragment_result["fragment"] if fragment_result else None,
            }
        if operation == "bind_layout":
            return runtime.composition_engine_bind_layout(
                self.state,
                {
                    "tenant": payload["tenant"],
                    "binding_id": payload["binding_id"],
                    "workspace_id": payload["workspace_id"],
                    "page": payload["page"],
                    "slot": payload["slot"],
                    "fragment_id": payload["fragment_id"],
                    "projection": payload["projection"],
                },
            )
        if operation == "register_rule":
            return runtime.composition_engine_register_rule(self.state, dict(payload))
        if operation == "assistant_document_preview":
            return runtime.composition_engine_assistant_document_preview(
                payload["document_text"],
                payload["instructions"],
                action=payload.get("requested_action", "read"),
                target_table=payload.get("target_table"),
                payload=payload.get("payload"),
            )
        if operation == "preview_selection_impact":
            return runtime.composition_engine_preview_selection_impact(
                self.state,
                payload["workspace_id"],
                tuple(payload["candidate_pbcs"]),
            )
        if operation == "route_agent_intent":
            return runtime.composition_engine_route_agent_intent(
                payload["intent"],
                context={"workspace_id": payload.get("workspace_id", "")},
            )
        if operation == "release_rehearsal":
            return runtime.composition_engine_release_rehearsal(self.state, payload["workspace_id"])
        if operation == "build_control_center":
            return runtime.composition_engine_build_control_center(self.state, workspace_id=payload["workspace_id"])
        if operation == "build_release_notes":
            return runtime.composition_engine_build_release_notes(self.state, payload["workspace_id"])
        if operation == "build_workbench_view":
            return runtime.composition_engine_build_workbench_view(self.state, tenant=payload["tenant"])
        raise ValueError(f"Unsupported standalone operation: {operation}")

    def _match_operation(self, method: str, path: str) -> _OperationMatch | None:
        route_index = tuple(routes.api_route_contracts()["contracts"])
        for route in route_index:
            if route["method"] != method:
                continue
            pattern = re.sub(r"\{([^}]+)\}", r"(?P<\1>[^/]+)", route["path"])
            match = re.fullmatch(pattern, path)
            if match:
                operation = route.get("operation") or route.get("handler")
                return _OperationMatch(operation=operation, path_parameters=match.groupdict())
        return None


def standalone_app_manifest() -> dict[str, Any]:
    """Return the standalone application contract for composition_engine."""
    return {
        "ok": True,
        "pbc": "composition_engine",
        "repository": repository_manifest(),
        "routes": routes.api_route_contracts()["routes"],
        "ui": ui.composition_engine_ui_contract(),
        "forms": forms.composition_engine_form_catalog()["forms"],
        "wizards": wizards.composition_engine_wizard_catalog()["wizards"],
        "controls": controls.composition_engine_control_catalog()["controls"],
        "assistant": agent.chatbot_interface_contract(),
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    """Exercise the standalone app through bootstrap, forms, wizard, controls, and assistant flows."""
    app = CompositionEngineStandaloneApp(bootstrap=True)
    app.submit_form(
        "workspace_intake",
        {
            "tenant": "tenant_demo",
            "workspace_id": "ws_demo",
            "name": "Customer Ops Console",
            "owner": "ops_user",
            "target": "web",
        },
    )
    app.submit_form(
        "pbc_selection",
        {
            "workspace_id": "ws_demo",
            "pbc": "customer_360",
            "mesh": "relationship",
            "reason": "Customer profile workbench",
        },
    )
    app.submit_form(
        "component_fragment_registration",
        {
            "tenant": "tenant_demo",
            "component_id": "cmp_customer",
            "pbc": "customer_360",
            "fragment": "CompositionWorkbench",
            "permissions": ("composition_engine.compose",),
            "schemas": ("CustomerProfile",),
            "fragment_id": "frag_customer",
            "route": "/customers/ops",
            "slots": ("main",),
            "events": ("CustomerProfile",),
        },
    )
    app.submit_form(
        "layout_binding",
        {
            "tenant": "tenant_demo",
            "binding_id": "bind_customer",
            "workspace_id": "ws_demo",
            "page": "home",
            "slot": "main",
            "fragment_id": "frag_customer",
            "projection": "customer_profile_projection",
        },
    )
    rehearsal = app.submit_form("workspace_governance_review", {"workspace_id": "ws_demo"})
    rendered = app.render_workbench(tenant="tenant_demo")
    assistant_preview = app.assistant_preview(
        "Compose a customer workbench with governed publication.",
        "Preview an update to the workspace only.",
        action="update",
        target_table="composition_engine_composition_workspace",
    )
    repository_summary = app.repository.workspace_summary(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    app.close()
    return {
        "ok": rehearsal["ok"] and rendered["ok"] and assistant_preview["ok"] and repository_summary["workspace_count"] == 1 and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "rehearsal": rehearsal,
        "rendered": rendered,
        "assistant_preview": assistant_preview,
        "repository_summary": repository_summary,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }
