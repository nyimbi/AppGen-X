"""Standalone one-PBC application surface for the DOM package."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from . import agent
from . import permissions
from . import runtime
from . import seed_data
from . import ui
from .repository import DomStandaloneRepository


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.DOM_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "allowed_channels": ("web", "marketplace", "edi", "call_center", "store"),
    "allowed_statuses": (
        "draft",
        "captured",
        "held",
        "verified",
        "priced",
        "allocated",
        "planned",
        "backordered",
        "cancelled",
        "shipped",
        "exception",
    ),
    "workbench_limit": 100,
}

DEFAULT_PARAMETERS = {
    "fraud_threshold": 0.7,
    "allocation_confidence_threshold": 0.75,
    "partial_fulfillment_threshold": 0.5,
    "max_split_shipments": 3,
    "service_level_weight": 0.55,
    "distance_weight": 0.25,
    "margin_weight": 0.2,
    "promise_horizon_days": 5,
    "exception_age_threshold_hours": 24,
    "retry_limit": 3,
    "workbench_limit": 100,
}

DEFAULT_RULES = (
    {
        "rule_id": "dom.order_capture.default",
        "tenant": "default",
        "rule_type": "order_orchestration",
        "channels": ("web", "marketplace", "edi", "call_center", "store"),
        "customer_statuses": ("active", "vip"),
        "allow_split": True,
        "preferred_nodes": ("node_east", "node_west", "node_central"),
        "restricted_destinations": ("embargoed_zone",),
        "requires_tax": True,
        "status": "active",
    },
    {
        "rule_id": "dom.compliance.default",
        "tenant": "default",
        "rule_type": "release_gate",
        "scope": "release_gate",
        "status": "active",
        "requires_payment_authorization": False,
        "requires_customer_projection": True,
    },
)


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


def _ensure_state(state: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(state)
    defaults: dict[str, Any] = {
        "orders": {},
        "customers": {},
        "tax": {},
        "fraud": {},
        "allocations": {},
        "fulfillment_plans": {},
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "handled_events": {},
        "retry_evidence": (),
        "holds": {},
        "exceptions": {},
        "backorders": {},
        "substitutions": {},
        "cancellations": {},
        "allocation_sets": {},
        "channel_contexts": {},
        "promises": {},
        "status_history": (),
        "audit_traces": (),
        "documents": (),
        "order_controls": {},
        "shipment_statuses": {},
    }
    for key, default in defaults.items():
        if key not in enriched:
            enriched[key] = deepcopy(default)
    return enriched


def _sequence_id(prefix: str, existing: dict[str, Any] | tuple[Any, ...]) -> str:
    size = len(existing)
    return f"{prefix}_{size + 1:05d}"


def _append_audit_trace(state: dict[str, Any], *, order_id: str | None, action: str, data: dict[str, Any]) -> dict[str, Any]:
    traces = tuple(state.get("audit_traces", ()))
    entry = {
        "trace_id": f"trace_{len(traces) + 1:05d}",
        "order_id": order_id,
        "action": action,
        "data": deepcopy(data),
    }
    return {**state, "audit_traces": (*traces, entry)}


def _append_status(state: dict[str, Any], *, order_id: str, status: str, reason: str) -> dict[str, Any]:
    history = tuple(state.get("status_history", ()))
    entry = {
        "status_id": f"status_{len(history) + 1:05d}",
        "order_id": order_id,
        "status": status,
        "reason": reason,
    }
    return {**state, "status_history": (*history, entry)}


def _service_level_days(service_level: str) -> int:
    normalized = str(service_level or "standard").lower()
    return {"same_day": 0, "next_day": 1, "express": 2, "standard": 4, "economy": 6}.get(normalized, 5)


def _build_promise(order: dict[str, Any], allocation: dict[str, Any] | None = None) -> dict[str, Any]:
    confidence = 0.55
    node_id = None
    if allocation:
        confidence = max(0.2, min(float(allocation.get("confidence", 0.55)), 0.99))
        node_id = allocation.get("node_id")
    promise_days = _service_level_days(order.get("service_level", "standard")) + (0 if confidence >= 0.8 else 2)
    return {
        "promise_id": f"promise_{order['order_id']}",
        "order_id": order["order_id"],
        "promise_days": promise_days,
        "promise_date_hint": f"T+{promise_days}d",
        "atp_confidence": round(confidence, 2),
        "node_id": node_id,
        "status": "promised" if confidence >= 0.5 else "at_risk",
    }


def _blocking_holds(state: dict[str, Any], order_id: str) -> tuple[dict[str, Any], ...]:
    return tuple(
        hold
        for hold in state.get("holds", {}).values()
        if hold["order_id"] == order_id and hold["status"] == "open" and hold.get("blocking", True)
    )


def _record_order_exception(
    state: dict[str, Any],
    *,
    order_id: str,
    exception_type: str,
    reason: str,
    severity: str = "medium",
    blocking: bool = True,
) -> dict[str, Any]:
    exception_id = _sequence_id("exception", state.get("exceptions", {}))
    exception = {
        "exception_id": exception_id,
        "order_id": order_id,
        "type": exception_type,
        "reason": reason,
        "severity": severity,
        "status": "open",
        "blocking": blocking,
    }
    next_state = {
        **state,
        "exceptions": {**state.get("exceptions", {}), exception_id: exception},
    }
    next_state = _append_audit_trace(
        next_state,
        order_id=order_id,
        action="record_exception",
        data={"exception_type": exception_type, "reason": reason, "severity": severity},
    )
    return next_state


def _close_exception(state: dict[str, Any], *, order_id: str, exception_type: str) -> dict[str, Any]:
    exceptions = {}
    for key, value in state.get("exceptions", {}).items():
        if value["order_id"] == order_id and value["type"] == exception_type and value["status"] == "open":
            exceptions[key] = {**value, "status": "closed"}
        else:
            exceptions[key] = value
    return {**state, "exceptions": exceptions}


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": "dom",
        "app_class": "DomStandaloneApplication",
        "implementation_directory": "src/pyAppGen/pbcs/dom",
        "service_methods": (
            "configure",
            "register_defaults",
            "upsert_customer_projection",
            "capture_order",
            "apply_tax_projection",
            "screen_fraud",
            "verify_order",
            "price_order",
            "apply_inventory_allocation",
            "create_fulfillment_plan",
            "route_fulfillment",
            "release_hold",
            "request_cancellation",
            "create_backorder",
            "apply_substitution",
            "record_exception",
            "receive_event",
            "document_intake",
            "crud_mutation_plan",
            "submit_form",
            "run_wizard",
            "execute_control",
            "run_agent_skill",
            "repository_manifest",
            "read_model_snapshot",
            "load_demo_workspace",
            "workbench",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "assistant", "workbench"),
        "repository_class": "DomStandaloneRepository",
        "database_backed_ui": True,
        "local_harness_backend": "sqlite3",
        "docs": (
            "README.md",
            "implementation-plan.md",
            "implementation-status.md",
            "RELEASE_EVIDENCE.md",
        ),
        "event_contract": "AppGen-X",
        "event_topic": runtime.DOM_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": runtime.DOM_ALLOWED_DATABASE_BACKENDS,
    }


class DomStandaloneApplication:
    """Mutable, package-local DOM application shell for one-PBC usage."""

    def __init__(
        self,
        *,
        tenant: str = "default",
        state: dict[str, Any] | None = None,
        repository: DomStandaloneRepository | None = None,
        database_path: str = ":memory:",
    ) -> None:
        self.tenant = tenant
        self.repository = repository or DomStandaloneRepository(database_path=database_path)
        persisted = self.repository.load_state(tenant) if state is None else None
        self.state = _ensure_state(state or persisted or runtime.dom_empty_state())
        self._persist_state()

    def close(self) -> None:
        self.repository.close()

    def _timestamp(self) -> str:
        return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def _persist_state(self) -> None:
        timestamp = self._timestamp()
        self.repository.save_state(self.tenant, self.state, updated_at=timestamp)
        self.repository.sync_read_models(self.tenant, self.state, updated_at=timestamp)

    def snapshot(self) -> dict[str, Any]:
        self._persist_state()
        return deepcopy(self.state)

    def repository_manifest(self) -> dict[str, Any]:
        dashboard = self.repository.activity_dashboard(self.tenant)
        return {**self.repository.repository_manifest(), "dashboard": dashboard}

    def read_model_snapshot(self) -> dict[str, Any]:
        return {
            "ok": True,
            "tenant": self.tenant,
            "orders": self.repository.list_order_read_models(self.tenant, limit=100),
            "exceptions": self.repository.list_exception_read_models(self.tenant, limit=100),
            "dashboard": self.repository.activity_dashboard(self.tenant, limit=10),
        }

    def _effective_permissions(self, granted_permissions: tuple[str, ...] | None) -> tuple[str, ...]:
        if granted_permissions:
            return tuple(granted_permissions)
        return tuple(ui.dom_ui_contract()["binding_evidence"]["rbac_permissions"])

    def _audit_action(self, action: str, payload: dict[str, Any]) -> dict[str, Any]:
        if action == "screen_order_policy":
            return runtime.dom_screen_order_policy(
                self.state,
                payload["order_id"],
                restricted_destinations=tuple(payload.get("restricted_destinations", ("embargoed_zone",))),
            )
        if action == "generate_order_verification_proof":
            return runtime.dom_generate_order_verification_proof(
                self.state,
                payload["order_id"],
                disclosure=tuple(payload.get("disclosure", ("order_id", "status", "total"))),
            )
        if action == "run_control_tests":
            return runtime.dom_run_control_tests(self.state)
        return {"ok": False, "reason": "unknown_audit_action", "action": action}

    def _dispatch_action(self, action: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        if action == "capture_order":
            return self.capture_order(data)
        if action == "upsert_customer_projection":
            return self.upsert_customer_projection(data)
        if action == "apply_tax_projection":
            projection = _copy_payload(data.get("tax_projection")) or data
            return self.apply_tax_projection(data["order_id"], projection)
        if action == "screen_fraud":
            return self.screen_fraud(data["order_id"], signals=_copy_payload(data.get("signals")))
        if action == "verify_order":
            return self.verify_order(data["order_id"])
        if action == "price_order":
            return self.price_order(data["order_id"])
        if action == "apply_inventory_allocation":
            return self.apply_inventory_allocation(data["order_id"], data.get("allocations") or data.get("allocation") or ())
        if action == "create_fulfillment_plan":
            return self.create_fulfillment_plan(data["order_id"])
        if action == "route_fulfillment":
            return self.route_fulfillment(data["order_id"], rails=tuple(data.get("rails", ())) or None)
        if action == "confirm_order_shipped":
            return self.confirm_order_shipped(data["order_id"], shipment_id=data["shipment_id"])
        if action == "release_hold":
            return self.release_hold(
                order_id=data["order_id"],
                hold_id=data["hold_id"],
                released_by=data.get("released_by", "workflow"),
                note=data.get("note", ""),
            )
        if action == "request_cancellation":
            return self.request_cancellation(order_id=data["order_id"], reason=data["reason"], actor=data.get("actor", "user"))
        if action == "create_backorder":
            return self.create_backorder(
                order_id=data["order_id"],
                line_id=data["line_id"],
                quantity=float(data["quantity"]),
                reason=data["reason"],
            )
        if action == "apply_substitution":
            return self.apply_substitution(
                order_id=data["order_id"],
                line_id=data["line_id"],
                substitute_item_id=data["substitute_item_id"],
                reason=data.get("reason", "equivalent_inventory"),
            )
        if action == "record_exception":
            return self.record_exception(
                order_id=data["order_id"],
                exception_type=data.get("exception_type", "manual_review"),
                reason=data.get("reason", "manual review required"),
                severity=data.get("severity", "medium"),
            )
        if action in {"screen_order_policy", "generate_order_verification_proof", "run_control_tests"}:
            return self._audit_action(action, data)
        return {"ok": False, "reason": "unknown_action", "action": action}

    def submit_form(
        self,
        form_key: str,
        payload: dict[str, Any],
        *,
        principal_permissions: tuple[str, ...] | None = None,
    ) -> dict[str, Any]:
        contract = ui.dom_ui_contract()["forms"].get(form_key)
        if contract is None:
            return {"ok": False, "reason": "unknown_form", "form_key": form_key}
        granted = self._effective_permissions(principal_permissions)
        authorization = permissions.authorize(contract["submit_action"], granted)
        if not authorization["allowed"]:
            result = {"ok": False, "reason": "forbidden", "authorization": authorization}
        else:
            result = self._dispatch_action(contract["submit_action"], payload)
        submission_id = _sequence_id("form", self.repository.list_form_submissions(self.tenant, limit=1000))
        self.repository.record_form_submission(
            submission_id=submission_id,
            tenant=self.tenant,
            form_key=form_key,
            action=contract["submit_action"],
            order_id=payload.get("order_id"),
            payload=payload,
            result=result,
            created_at=self._timestamp(),
        )
        return {
            "ok": result.get("ok") is True,
            "form_key": form_key,
            "action": contract["submit_action"],
            "authorization": authorization,
            "result": result,
            "repository": self.repository.activity_dashboard(self.tenant, limit=5),
        }

    def run_wizard(
        self,
        wizard_key: str,
        payload: dict[str, Any],
        *,
        principal_permissions: tuple[str, ...] | None = None,
    ) -> dict[str, Any]:
        contract = ui.dom_ui_contract()["wizards"].get(wizard_key)
        if contract is None:
            return {"ok": False, "reason": "unknown_wizard", "wizard_key": wizard_key}
        granted = set(self._effective_permissions(principal_permissions))
        required_actions = tuple(dict.fromkeys(contract.get("step_actions", {}).values()))
        missing_permissions = tuple(
            action
            for action in required_actions
            if not permissions.authorize(action, tuple(granted))["allowed"]
        )
        steps = []
        order_id = payload.get("order_id") or payload.get("order", {}).get("order_id")
        if missing_permissions:
            result = {"ok": False, "reason": "forbidden", "missing_permissions": missing_permissions}
        elif wizard_key == "order_intake_wizard":
            steps.append({"step": "capture", "action": "capture_order", "result": self.capture_order(_copy_payload(payload["order"]))})
            if steps[-1]["result"].get("ok") and payload.get("tax_projection"):
                steps.append({"step": "tax", "action": "apply_tax_projection", "result": self.apply_tax_projection(order_id, _copy_payload(payload["tax_projection"]))})
            if steps[-1]["result"].get("ok") and payload.get("fraud_signals") is not None:
                steps.append({"step": "fraud", "action": "screen_fraud", "result": self.screen_fraud(order_id, signals=_copy_payload(payload.get("fraud_signals")))})
            if all(step["result"].get("ok") is True for step in steps):
                steps.append({"step": "verify", "action": "verify_order", "result": self.verify_order(order_id)})
            if all(step["result"].get("ok") is True for step in steps):
                steps.append({"step": "price", "action": "price_order", "result": self.price_order(order_id)})
            result = {"ok": all(step["result"].get("ok") is True for step in steps), "order_id": order_id}
        elif wizard_key == "fulfillment_wizard":
            steps.append({"step": "allocation", "action": "apply_inventory_allocation", "result": self.apply_inventory_allocation(order_id, payload.get("allocations") or ())})
            if steps[-1]["result"].get("ok") is True:
                steps.append({"step": "plan", "action": "create_fulfillment_plan", "result": self.create_fulfillment_plan(order_id)})
            if all(step["result"].get("ok") is True for step in steps):
                steps.append({"step": "route", "action": "route_fulfillment", "result": self.route_fulfillment(order_id, rails=tuple(payload.get("rails", ())) or None)})
            if all(step["result"].get("ok") is True for step in steps) and payload.get("shipment_id"):
                steps.append({"step": "ship", "action": "confirm_order_shipped", "result": self.confirm_order_shipped(order_id, shipment_id=payload["shipment_id"])})
            result = {"ok": all(step["result"].get("ok") is True for step in steps), "order_id": order_id}
        else:
            steps.append({"step": "triage", "action": "record_exception", "result": self.record_exception(order_id=payload["order_id"], exception_type=payload.get("exception_type", "manual_review"), reason=payload.get("reason", "wizard triage"), severity=payload.get("severity", "medium"))})
            if payload.get("hold_id"):
                steps.append({"step": "release", "action": "release_hold", "result": self.release_hold(order_id=payload["order_id"], hold_id=payload["hold_id"], released_by=payload.get("released_by", "workflow"), note=payload.get("note", ""))})
            if payload.get("backorder"):
                steps.append({"step": "backorder", "action": "create_backorder", "result": self.create_backorder(order_id=payload["order_id"], line_id=payload["backorder"]["line_id"], quantity=float(payload["backorder"]["quantity"]), reason=payload["backorder"].get("reason", "manual_review"))})
            result = {"ok": all(step["result"].get("ok") is True for step in steps), "order_id": payload["order_id"]}
        workflow_run_id = _sequence_id("workflow", self.repository.list_workflow_runs(self.tenant, limit=1000))
        self.repository.record_workflow_run(
            workflow_run_id=workflow_run_id,
            tenant=self.tenant,
            wizard_key=wizard_key,
            order_id=order_id,
            status="completed" if result.get("ok") else "blocked",
            context=payload,
            steps=tuple(steps),
            result=result,
            created_at=self._timestamp(),
        )
        return {
            "ok": result.get("ok") is True,
            "wizard_key": wizard_key,
            "required_actions": required_actions,
            "steps": tuple(steps),
            "result": result,
            "repository": self.repository.activity_dashboard(self.tenant, limit=5),
        }

    def execute_control(
        self,
        control_key: str,
        payload: dict[str, Any],
        *,
        principal_permissions: tuple[str, ...] | None = None,
    ) -> dict[str, Any]:
        contract = ui.dom_ui_contract()["controls"].get(control_key)
        if contract is None:
            return {"ok": False, "reason": "unknown_control", "control_key": control_key}
        granted = self._effective_permissions(principal_permissions)
        authorization = permissions.authorize(contract["action"], granted)
        result = self._dispatch_action(contract["action"], payload) if authorization["allowed"] else {"ok": False, "reason": "forbidden", "authorization": authorization}
        control_run_id = _sequence_id("control", self.repository.list_control_executions(self.tenant, limit=1000))
        self.repository.record_control_execution(
            control_run_id=control_run_id,
            tenant=self.tenant,
            control_key=control_key,
            action=contract["action"],
            order_id=payload.get("order_id"),
            allowed=authorization["allowed"],
            payload=payload,
            result=result,
            created_at=self._timestamp(),
        )
        return {
            "ok": result.get("ok") is True,
            "control_key": control_key,
            "authorization": authorization,
            "result": result,
            "repository": self.repository.activity_dashboard(self.tenant, limit=5),
        }

    def run_agent_skill(
        self,
        skill_name: str,
        payload: dict[str, Any] | None = None,
        *,
        principal_permissions: tuple[str, ...] | None = None,
    ) -> dict[str, Any]:
        requested = _copy_payload(payload)
        manifest = agent.agent_skill_manifest()
        available = {item["name"] for item in manifest["skills"]}
        if skill_name not in available:
            return {"ok": False, "reason": "unknown_skill", "skill_name": skill_name}
        granted = self._effective_permissions(principal_permissions)
        authorization = permissions.authorize("build_workbench_view", granted)
        if skill_name.endswith("document_instruction_intake"):
            result = agent.document_instruction_plan(requested.get("document"), requested.get("instructions", ""))
        elif skill_name.endswith("governed_create"):
            result = agent.datastore_crud_plan("create", table=requested.get("table", "dom_sales_order"), payload=requested.get("payload"))
        elif skill_name.endswith("governed_update"):
            result = agent.datastore_crud_plan("update", table=requested.get("table", "dom_sales_order"), payload=requested.get("payload"))
        elif skill_name.endswith("governed_delete"):
            result = agent.datastore_crud_plan("delete", table=requested.get("table", "dom_sales_order"), payload=requested.get("payload"))
        elif skill_name.endswith("governed_read"):
            result = agent.datastore_crud_plan("read", table=requested.get("table", "dom_sales_order"), payload=requested.get("payload"))
        elif skill_name.endswith("policy_explanation"):
            result = {
                "ok": True,
                "authorization": permissions.authorize(requested.get("action", "verify_order"), granted),
                "rule_manifest": tuple(config["rule_id"] for config in DEFAULT_RULES),
            }
        elif skill_name.endswith("workbench_navigation"):
            result = self.workbench(tenant=requested.get("tenant", self.tenant), permissions=granted)
        else:
            order_id = requested.get("order_id")
            result = {
                "ok": True,
                "task_guidance": {
                    "order_id": order_id,
                    "available_actions": tuple(ui.dom_ui_contract()["action_permissions"]),
                    "current_order": self.state.get("orders", {}).get(order_id),
                },
            }
        session_id = _sequence_id("agent", self.repository.list_agent_sessions(self.tenant, limit=1000))
        self.repository.record_agent_session(
            session_id=session_id,
            tenant=self.tenant,
            skill_name=skill_name,
            scope=requested.get("scope", "preview"),
            requires_confirmation=result.get("requires_confirmation", requested.get("requires_confirmation", True)),
            payload=requested,
            result={"authorization": authorization, "result": result},
            created_at=self._timestamp(),
        )
        return {
            "ok": result.get("ok") is True,
            "skill_name": skill_name,
            "authorization": authorization,
            "result": result,
            "repository": self.repository.activity_dashboard(self.tenant, limit=5),
        }

    def configure(self, configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = {**DEFAULT_CONFIGURATION, **_copy_payload(configuration)}
        result = runtime.dom_configure_runtime(self.state, candidate)
        self.state = _ensure_state(result["state"])
        self.state = _append_audit_trace(
            self.state,
            order_id=None,
            action="configure_runtime",
            data={"database_backend": candidate["database_backend"], "event_topic": candidate["event_topic"]},
        )
        return {**result, "state": self.snapshot()}

    def register_defaults(self, *, tenant: str | None = None) -> dict[str, Any]:
        active_tenant = tenant or self.tenant
        if not self.state.get("configuration", {}).get("ok"):
            self.configure()
        parameter_results = []
        for key, value in DEFAULT_PARAMETERS.items():
            parameter_results.append(runtime.dom_set_parameter(self.state, key, value))
            self.state = _ensure_state(parameter_results[-1]["state"])
        rule_results = []
        for rule in DEFAULT_RULES:
            rule_results.append(runtime.dom_register_rule(self.state, {**rule, "tenant": active_tenant}))
            self.state = _ensure_state(rule_results[-1]["state"])
        self.state = _append_audit_trace(
            self.state,
            order_id=None,
            action="register_defaults",
            data={"tenant": active_tenant, "parameters": tuple(DEFAULT_PARAMETERS), "rules": tuple(item["rule"]["rule_id"] for item in rule_results)},
        )
        return {
            "ok": all(item["ok"] for item in parameter_results + rule_results),
            "state": self.snapshot(),
            "parameters": tuple(item["parameter"] for item in parameter_results),
            "rules": tuple(item["rule"] for item in rule_results),
        }

    def upsert_customer_projection(self, customer: dict[str, Any]) -> dict[str, Any]:
        candidate = {
            "tenant": customer.get("tenant", self.tenant),
            "customer_id": customer["customer_id"],
            "status": customer.get("status", "active"),
            "risk": customer.get("risk", 0.0),
            "identity": customer.get(
                "identity",
                {
                    "did": f"did:appgen:{customer['customer_id']}",
                    "issuer": "trusted_registry",
                    "status": "active",
                },
            ),
        }
        result = runtime.dom_upsert_customer_projection(self.state, candidate)
        self.state = _ensure_state(result["state"])
        self.state = _append_audit_trace(
            self.state,
            order_id=None,
            action="upsert_customer_projection",
            data={"customer_id": candidate["customer_id"], "status": candidate["status"]},
        )
        return {**result, "state": self.snapshot()}

    def apply_hold(
        self,
        *,
        order_id: str,
        hold_type: str,
        reason: str,
        owner: str = "system",
        blocking: bool = True,
    ) -> dict[str, Any]:
        hold_id = _sequence_id("hold", self.state.get("holds", {}))
        hold = {
            "hold_id": hold_id,
            "order_id": order_id,
            "type": hold_type,
            "reason": reason,
            "owner": owner,
            "blocking": blocking,
            "status": "open",
        }
        self.state = _ensure_state(
            {
                **self.state,
                "holds": {**self.state.get("holds", {}), hold_id: hold},
            }
        )
        if order_id in self.state["orders"]:
            order = {**self.state["orders"][order_id], "status": "held"}
            self.state["orders"][order_id] = order
            self.state = _append_status(self.state, order_id=order_id, status="held", reason=hold_type)
        self.state = _append_audit_trace(
            self.state,
            order_id=order_id,
            action="apply_hold",
            data={"hold_id": hold_id, "hold_type": hold_type, "reason": reason},
        )
        return {"ok": True, "hold": hold, "state": self.snapshot()}

    def release_hold(self, *, order_id: str, hold_id: str, released_by: str, note: str = "") -> dict[str, Any]:
        hold = self.state.get("holds", {}).get(hold_id)
        if not hold or hold["order_id"] != order_id:
            return {"ok": False, "reason": "unknown_hold", "hold_id": hold_id, "state": self.snapshot()}
        released = {**hold, "status": "released", "released_by": released_by, "release_note": note}
        self.state = {**self.state, "holds": {**self.state["holds"], hold_id: released}}
        if order_id in self.state["orders"] and not _blocking_holds(self.state, order_id):
            order = {**self.state["orders"][order_id]}
            if order["status"] == "held":
                order["status"] = "captured"
                self.state["orders"][order_id] = order
                self.state = _append_status(self.state, order_id=order_id, status="captured", reason="hold_released")
        self.state = _append_audit_trace(
            self.state,
            order_id=order_id,
            action="release_hold",
            data={"hold_id": hold_id, "released_by": released_by},
        )
        return {"ok": True, "hold": released, "state": self.snapshot()}

    def capture_order(self, order: dict[str, Any]) -> dict[str, Any]:
        required = {"order_id", "customer_id", "channel", "destination", "service_level", "lines"}
        missing = tuple(sorted(field for field in required if not order.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_fields", "missing": missing, "state": self.snapshot()}
        if not self.state.get("configuration", {}).get("ok"):
            self.configure()
        if not self.state.get("rules"):
            self.register_defaults(tenant=order.get("tenant", self.tenant))
        candidate = {
            "tenant": order.get("tenant", self.tenant),
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "channel": order["channel"],
            "currency": order.get("currency", self.state["configuration"].get("default_currency", "USD")),
            "destination": order["destination"],
            "service_level": order.get("service_level", "standard"),
            "lines": tuple(_copy_payload(line) for line in order["lines"]),
            "source_reference": order.get("source_reference"),
        }
        result = runtime.dom_capture_order(self.state, candidate)
        self.state = _ensure_state(result["state"])
        order_id = candidate["order_id"]
        validation_issues = []
        for line in candidate["lines"]:
            if float(line.get("quantity", 0)) <= 0:
                validation_issues.append({"line_id": line.get("line_id"), "issue": "quantity_must_be_positive"})
            if float(line.get("unit_price", 0)) < 0:
                validation_issues.append({"line_id": line.get("line_id"), "issue": "unit_price_must_be_non_negative"})
        channel_context = {
            "order_id": order_id,
            "channel": candidate["channel"],
            "source_system": order.get("source_system", "standalone"),
            "service_level": candidate["service_level"],
            "cutoff": order.get("cutoff", "17:00"),
            "customer_promise": order.get("customer_promise", "best_effort"),
        }
        promise = _build_promise(self.state["orders"][order_id])
        self.state = {
            **self.state,
            "channel_contexts": {**self.state.get("channel_contexts", {}), order_id: channel_context},
            "promises": {**self.state.get("promises", {}), order_id: promise},
            "order_controls": {
                **self.state.get("order_controls", {}),
                order_id: {"validation_issues": tuple(validation_issues), "documents": ()},
            },
        }
        self.state = _append_status(
            self.state,
            order_id=order_id,
            status=self.state["orders"][order_id]["status"],
            reason="order_captured",
        )
        self.state = _append_audit_trace(
            self.state,
            order_id=order_id,
            action="capture_order",
            data={"channel": candidate["channel"], "line_count": len(candidate["lines"]), "validation_issues": validation_issues},
        )
        if candidate["customer_id"] not in self.state.get("customers", {}):
            self.apply_hold(
                order_id=order_id,
                hold_type="customer_projection_missing",
                reason="customer projection must exist before verification",
            )
        if validation_issues:
            self.apply_hold(
                order_id=order_id,
                hold_type="line_validation",
                reason="line validation issues require remediation",
            )
            self.state = _record_order_exception(
                self.state,
                order_id=order_id,
                exception_type="line_validation",
                reason="line validation issues detected at capture",
                severity="medium",
            )
        return {
            "ok": result["ok"] and not validation_issues,
            "order": self.state["orders"][order_id],
            "promise": promise,
            "channel_context": channel_context,
            "validation_issues": tuple(validation_issues),
            "state": self.snapshot(),
        }

    def apply_tax_projection(self, order_id: str, tax: dict[str, Any]) -> dict[str, Any]:
        result = runtime.dom_apply_tax_projection(self.state, order_id, tax)
        self.state = _ensure_state(result["state"])
        self.state = _close_exception(self.state, order_id=order_id, exception_type="tax_missing")
        self.state = _append_audit_trace(
            self.state,
            order_id=order_id,
            action="apply_tax_projection",
            data={"calculation_id": tax.get("calculation_id"), "tax_total": tax.get("tax_total")},
        )
        return {**result, "state": self.snapshot()}

    def screen_fraud(self, order_id: str, *, signals: dict[str, Any]) -> dict[str, Any]:
        result = runtime.dom_screen_fraud(self.state, order_id, signals=signals)
        self.state = _ensure_state(result["state"])
        if result["decision"] == "review":
            self.apply_hold(
                order_id=order_id,
                hold_type="fraud_review",
                reason="fraud screen requires manual review",
                owner="fraud_ops",
            )
        else:
            self.state = _close_exception(self.state, order_id=order_id, exception_type="fraud_review")
        self.state = _append_audit_trace(
            self.state,
            order_id=order_id,
            action="screen_fraud",
            data={"score": result["score"], "decision": result["decision"]},
        )
        return {**result, "state": self.snapshot()}

    def verify_order(self, order_id: str) -> dict[str, Any]:
        blocking_holds = _blocking_holds(self.state, order_id)
        if blocking_holds:
            self.state = _record_order_exception(
                self.state,
                order_id=order_id,
                exception_type="blocking_hold",
                reason="verification blocked by open hold",
                severity="high",
            )
            return {
                "ok": False,
                "reason": "blocking_hold",
                "holds": tuple(blocking_holds),
                "state": self.snapshot(),
            }
        result = runtime.dom_verify_order(self.state, order_id)
        self.state = _ensure_state(result["state"])
        if result["ok"]:
            self.state = _append_status(self.state, order_id=order_id, status="verified", reason="verification_passed")
        else:
            self.state = _record_order_exception(
                self.state,
                order_id=order_id,
                exception_type="verification_failed",
                reason="verification gates not satisfied",
                severity="high",
            )
        return {**result, "state": self.snapshot()}

    def price_order(self, order_id: str) -> dict[str, Any]:
        result = runtime.dom_price_order(self.state, order_id)
        self.state = _ensure_state(result["state"])
        self.state = _append_status(self.state, order_id=order_id, status="priced", reason="pricing_completed")
        return {**result, "state": self.snapshot()}

    def apply_inventory_allocation(self, order_id: str, allocations: dict[str, Any] | tuple[dict[str, Any], ...]) -> dict[str, Any]:
        allocation_set = tuple(allocations) if isinstance(allocations, tuple) else (allocations,)
        primary = max(allocation_set, key=lambda item: float(item.get("confidence", 0)))
        result = runtime.dom_apply_inventory_allocation(self.state, order_id, primary)
        self.state = _ensure_state(result["state"])
        self.state = {
            **self.state,
            "allocation_sets": {**self.state.get("allocation_sets", {}), order_id: allocation_set},
            "promises": {**self.state.get("promises", {}), order_id: _build_promise(self.state["orders"][order_id], primary)},
        }
        ordered_quantity = sum(float(line["quantity"]) for line in self.state["orders"][order_id]["lines"])
        allocated_quantity = sum(float(item.get("quantity", 0)) for item in allocation_set)
        if allocated_quantity < ordered_quantity:
            remaining = round(ordered_quantity - allocated_quantity, 2)
            first_line = self.state["orders"][order_id]["lines"][0]
            self.create_backorder(
                order_id=order_id,
                line_id=first_line["line_id"],
                quantity=remaining,
                reason="allocation_gap",
            )
        self.state = _append_status(self.state, order_id=order_id, status="allocated", reason="inventory_allocated")
        return {
            **result,
            "allocation_set": allocation_set,
            "state": self.snapshot(),
        }

    def create_fulfillment_plan(self, order_id: str) -> dict[str, Any]:
        result = runtime.dom_create_fulfillment_plan(self.state, order_id)
        self.state = _ensure_state(result["state"])
        allocation_set = tuple(self.state.get("allocation_sets", {}).get(order_id, (self.state["allocations"][order_id],)))
        split_shipments = tuple(
            {
                "split_id": f"split_{order_id}_{index + 1}",
                "plan_id": result["plan"]["plan_id"],
                "node_id": allocation["node_id"],
                "quantity": allocation["quantity"],
                "status": "planned",
            }
            for index, allocation in enumerate(allocation_set)
            if len(allocation_set) > 1
        )
        if split_shipments:
            self.state = {**self.state, "order_controls": {**self.state["order_controls"], order_id: {**self.state["order_controls"].get(order_id, {}), "split_shipments": split_shipments}}}
        self.state = _append_status(self.state, order_id=order_id, status="planned", reason="fulfillment_plan_created")
        return {**result, "split_shipments": split_shipments, "state": self.snapshot()}

    def route_fulfillment(self, order_id: str, *, rails: tuple[dict[str, Any], ...] | None = None) -> dict[str, Any]:
        plan = next(
            (value for value in self.state.get("fulfillment_plans", {}).values() if value["order_id"] == order_id),
            None,
        )
        if not plan:
            return {"ok": False, "reason": "missing_plan", "order_id": order_id, "state": self.snapshot()}
        route = runtime.dom_route_fulfillment(
            plan,
            rails=rails
            or (
                {"route": "warehouse_api", "available": False, "latency": 3},
                {"route": "outbox", "available": True, "latency": 1},
            ),
        )
        self.state = _append_audit_trace(
            self.state,
            order_id=order_id,
            action="route_fulfillment",
            data={"route": route["route"], "failover_used": route["failover_used"]},
        )
        return {**route, "state": self.snapshot()}

    def create_backorder(self, *, order_id: str, line_id: str, quantity: float, reason: str) -> dict[str, Any]:
        backorder_id = _sequence_id("backorder", self.state.get("backorders", {}))
        backorder = {
            "backorder_id": backorder_id,
            "order_id": order_id,
            "line_id": line_id,
            "quantity": quantity,
            "reason": reason,
            "status": "open",
        }
        self.state = {**self.state, "backorders": {**self.state.get("backorders", {}), backorder_id: backorder}}
        self.state = _append_status(self.state, order_id=order_id, status="backordered", reason=reason)
        self.state = _record_order_exception(
            self.state,
            order_id=order_id,
            exception_type="allocation_gap",
            reason="unallocated quantity moved to backorder",
            severity="medium",
        )
        return {"ok": True, "backorder": backorder, "state": self.snapshot()}

    def apply_substitution(
        self,
        *,
        order_id: str,
        line_id: str,
        substitute_item_id: str,
        reason: str = "equivalent_inventory",
    ) -> dict[str, Any]:
        substitution_id = _sequence_id("substitution", self.state.get("substitutions", {}))
        substitution = {
            "substitution_id": substitution_id,
            "order_id": order_id,
            "line_id": line_id,
            "substitute_item_id": substitute_item_id,
            "reason": reason,
            "status": "proposed",
        }
        self.state = {
            **self.state,
            "substitutions": {**self.state.get("substitutions", {}), substitution_id: substitution},
        }
        self.state = _append_audit_trace(
            self.state,
            order_id=order_id,
            action="apply_substitution",
            data={"line_id": line_id, "substitute_item_id": substitute_item_id},
        )
        return {"ok": True, "substitution": substitution, "state": self.snapshot()}

    def request_cancellation(self, *, order_id: str, reason: str, actor: str = "user") -> dict[str, Any]:
        order = self.state["orders"].get(order_id)
        if not order:
            return {"ok": False, "reason": "unknown_order", "order_id": order_id, "state": self.snapshot()}
        cancellation_id = _sequence_id("cancel", self.state.get("cancellations", {}))
        cancellable = order["status"] not in {"shipped"}
        request = {
            "cancellation_id": cancellation_id,
            "order_id": order_id,
            "reason": reason,
            "actor": actor,
            "status": "approved" if cancellable else "pending_manual_review",
        }
        self.state = {
            **self.state,
            "cancellations": {**self.state.get("cancellations", {}), cancellation_id: request},
        }
        if cancellable:
            self.state["orders"][order_id] = {**order, "status": "cancelled"}
            self.state = _append_status(self.state, order_id=order_id, status="cancelled", reason=reason)
        else:
            self.state = _record_order_exception(
                self.state,
                order_id=order_id,
                exception_type="cancellation_conflict",
                reason="order already shipped or in irreversible stage",
                severity="medium",
            )
        self.state = _append_audit_trace(
            self.state,
            order_id=order_id,
            action="request_cancellation",
            data={"reason": reason, "status": request["status"]},
        )
        return {"ok": True, "cancellation": request, "state": self.snapshot()}

    def record_exception(self, *, order_id: str, exception_type: str, reason: str, severity: str = "medium") -> dict[str, Any]:
        self.state = _record_order_exception(
            self.state,
            order_id=order_id,
            exception_type=exception_type,
            reason=reason,
            severity=severity,
        )
        exception = next(
            value
            for value in self.state["exceptions"].values()
            if value["order_id"] == order_id and value["type"] == exception_type and value["status"] == "open"
        )
        return {"ok": True, "exception": exception, "state": self.snapshot()}

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        result = runtime.dom_receive_event(self.state, event)
        self.state = _ensure_state(result["state"])
        self.state = _append_audit_trace(
            self.state,
            order_id=event.get("payload", {}).get("order_id"),
            action="receive_event",
            data={"event_type": event.get("event_type"), "status": result["handler"]["status"]},
        )
        return {**result, "state": self.snapshot()}

    def confirm_order_shipped(self, order_id: str, *, shipment_id: str) -> dict[str, Any]:
        result = runtime.dom_confirm_order_shipped(self.state, order_id, shipment_id=shipment_id)
        self.state = _ensure_state(result["state"])
        self.state = _append_status(self.state, order_id=order_id, status="shipped", reason="shipment_confirmed")
        self.state = _close_exception(self.state, order_id=order_id, exception_type="allocation_gap")
        return {**result, "state": self.snapshot()}

    def document_intake(self, document: str, instructions: str = "") -> dict[str, Any]:
        plan = agent.document_instruction_plan(document, instructions)
        self.state = _ensure_state(
            {**self.state, "documents": (*self.state.get("documents", ()), {"document": document, "instructions": instructions, "plan": plan})}
        )
        return {"ok": plan["ok"], "plan": plan, "state": self.snapshot()}

    def crud_mutation_plan(self, *, action_name: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return agent.datastore_crud_plan(action_name, table=table, payload=payload)

    def workbench(self, *, tenant: str | None = None, permissions: tuple[str, ...] | None = None) -> dict[str, Any]:
        active_tenant = tenant or self.tenant
        permissions = permissions or tuple(ui.dom_ui_contract()["binding_evidence"]["rbac_permissions"])
        rendered = ui.dom_render_workbench(self.state, tenant=active_tenant, principal_permissions=permissions)
        rendered["standalone"] = {
            "holds": tuple(hold for hold in self.state.get("holds", {}).values() if self.state["orders"].get(hold["order_id"], {}).get("tenant") == active_tenant),
            "exceptions": tuple(exc for exc in self.state.get("exceptions", {}).values() if self.state["orders"].get(exc["order_id"], {}).get("tenant") == active_tenant),
            "backorders": tuple(item for item in self.state.get("backorders", {}).values() if self.state["orders"].get(item["order_id"], {}).get("tenant") == active_tenant),
            "cancellations": tuple(item for item in self.state.get("cancellations", {}).values() if self.state["orders"].get(item["order_id"], {}).get("tenant") == active_tenant),
            "substitutions": tuple(item for item in self.state.get("substitutions", {}).values() if self.state["orders"].get(item["order_id"], {}).get("tenant") == active_tenant),
            "audit_traces": tuple(item for item in self.state.get("audit_traces", ()) if item.get("order_id") is None or self.state["orders"].get(item["order_id"], {}).get("tenant") == active_tenant),
        }
        rendered["repository"] = self.repository.activity_dashboard(active_tenant, limit=10)
        rendered["read_models"] = {
            "orders": self.repository.list_order_read_models(active_tenant, limit=50),
            "exceptions": self.repository.list_exception_read_models(active_tenant, limit=50),
        }
        return rendered


    def load_demo_workspace(self, seed_bundle: dict[str, Any] | None = None) -> dict[str, Any]:
        bundle = _copy_payload(seed_bundle) if seed_bundle is not None else seed_data.standalone_seed_bundle()
        active_tenant = bundle.get("tenant", self.tenant)
        if active_tenant != self.tenant:
            self.tenant = active_tenant
            self.state = _ensure_state(self.repository.load_state(active_tenant) or runtime.dom_empty_state())
            self._persist_state()
        granted = tuple(ui.dom_ui_contract()["binding_evidence"]["rbac_permissions"])
        configured = self.configure(bundle.get("configuration"))
        defaults = self.register_defaults(tenant=active_tenant)
        customer_submissions = tuple(
            self.submit_form(
                "customer_projection_form",
                {**customer, "tenant": active_tenant},
                principal_permissions=granted,
            )
            for customer in bundle.get("customers", ())
        )
        order_results = []
        for index, order_bundle in enumerate(bundle.get("orders", ()), start=1):
            order_payload = {**_copy_payload(order_bundle.get("order")), "tenant": active_tenant}
            order_id = order_payload["order_id"]
            if index == 1:
                intake = self.run_wizard(
                    "order_intake_wizard",
                    {
                        "order": order_payload,
                        "tax_projection": _copy_payload(order_bundle.get("tax_projection")),
                        "fraud_signals": _copy_payload(order_bundle.get("fraud_signals")),
                    },
                    principal_permissions=granted,
                )
                fulfillment = self.run_wizard(
                    "fulfillment_wizard",
                    {
                        "order_id": order_id,
                        "allocations": tuple(_copy_payload(item) for item in order_bundle.get("allocations", ())),
                        "rails": tuple(_copy_payload(item) for item in order_bundle.get("rails", ())),
                        "shipment_id": order_bundle.get("shipment_id"),
                    },
                    principal_permissions=granted,
                )
                controls = tuple(
                    self.execute_control(
                        control["control_key"],
                        _copy_payload(control.get("payload")),
                        principal_permissions=granted,
                    )
                    for control in order_bundle.get("controls", ())
                )
                agent_result = self.run_agent_skill(
                    "dom.document_instruction_intake",
                    {
                        "document": order_bundle.get("document", ""),
                        "instructions": order_bundle.get("instructions", ""),
                        "scope": "demo_workspace",
                    },
                    principal_permissions=granted,
                )
                order_results.append(
                    {
                        "order_id": order_id,
                        "mode": "wizard",
                        "intake": intake,
                        "fulfillment": fulfillment,
                        "controls": controls,
                        "agent": agent_result,
                    }
                )
                continue
            capture = self.submit_form(
                "order_capture_form",
                order_payload,
                principal_permissions=granted,
            )
            tax_result = self.apply_tax_projection(order_id, _copy_payload(order_bundle.get("tax_projection")))
            fraud_result = self.screen_fraud(order_id, signals=_copy_payload(order_bundle.get("fraud_signals")))
            exception_result = None
            if order_bundle.get("exception"):
                exception_result = self.submit_form(
                    "exception_resolution_form",
                    {"order_id": order_id, **_copy_payload(order_bundle["exception"])},
                    principal_permissions=granted,
                )
            cancellation_result = None
            if order_bundle.get("cancellation"):
                cancellation_result = self.submit_form(
                    "cancellation_form",
                    {"order_id": order_id, **_copy_payload(order_bundle["cancellation"])},
                    principal_permissions=granted,
                )
            order_results.append(
                {
                    "order_id": order_id,
                    "mode": "form",
                    "capture": capture,
                    "tax": tax_result,
                    "fraud": fraud_result,
                    "exception": exception_result,
                    "cancellation": cancellation_result,
                }
            )
        workbench = self.workbench(tenant=active_tenant, permissions=granted)
        read_models = self.read_model_snapshot()
        repository = self.repository.activity_dashboard(active_tenant, limit=10)
        order_checks = []
        for item in order_results:
            if item["mode"] == "wizard":
                order_checks.append(item["intake"]["ok"] and item["fulfillment"]["ok"] and all(control["ok"] for control in item["controls"]) and item["agent"]["ok"])
            else:
                order_checks.append(
                    item["capture"]["ok"]
                    and item["tax"]["ok"]
                    and item["fraud"]["ok"]
                    and (item["exception"] is None or item["exception"]["ok"])
                    and (item["cancellation"] is None or item["cancellation"]["ok"])
                )
        return {
            "ok": configured["ok"]
            and defaults["ok"]
            and all(item["ok"] for item in customer_submissions)
            and all(order_checks)
            and workbench["ok"]
            and repository["counts"]["forms"] >= 3
            and repository["counts"]["workflows"] >= 2
            and repository["counts"]["controls"] >= 2
            and repository["counts"]["agent_sessions"] >= 1
            and repository["counts"]["orders"] >= 2,
            "tenant": active_tenant,
            "configured": configured,
            "defaults": defaults,
            "customer_submissions": customer_submissions,
            "orders": tuple(order_results),
            "workbench": workbench,
            "repository": repository,
            "read_models": read_models,
        }


def standalone_release_snapshot(seed_bundle: dict[str, Any] | None = None) -> dict[str, Any]:
    bundle = _copy_payload(seed_bundle) if seed_bundle is not None else seed_data.standalone_seed_bundle()
    tenant = bundle.get("tenant", "tenant_demo")
    with NamedTemporaryFile(suffix=".sqlite3") as handle:
        app = DomStandaloneApplication(tenant=tenant, database_path=handle.name)
        loaded = app.load_demo_workspace(seed_bundle=bundle)
        snapshot = app.snapshot()
        read_models = app.read_model_snapshot()
        repository = app.repository_manifest()
        workbench = loaded["workbench"]
        docs = documentation_presence()
        app.close()
    return {
        "ok": loaded["ok"]
        and docs["ok"]
        and len(read_models["orders"]) >= 2
        and repository["dashboard"]["counts"]["orders"] >= 2
        and bool(workbench["forms"])
        and bool(workbench["wizards"])
        and bool(workbench["controls"]),
        "tenant": tenant,
        "loaded": loaded,
        "state": snapshot,
        "read_models": read_models,
        "repository": repository,
        "workbench": workbench,
        "docs": docs,
    }


def standalone_smoke_test() -> dict[str, Any]:
    snapshot = standalone_release_snapshot()
    first_agent_session = (snapshot["repository"]["dashboard"].get("recent_agent_sessions") or [{}])[0]
    return {
        "ok": snapshot["ok"],
        "manifest": standalone_manifest(),
        "state": snapshot["state"],
        "workbench": snapshot["workbench"],
        "document": first_agent_session.get("result", {}),
        "repository": snapshot["repository"],
        "read_models": snapshot["read_models"],
    }


def documentation_presence() -> dict[str, Any]:
    base = Path(__file__).resolve().parent
    docs = tuple(
        {
            "path": name,
            "exists": (base / name).exists(),
        }
        for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md")
    )
    return {
        "ok": all(item["exists"] for item in docs),
        "docs": docs,
    }
