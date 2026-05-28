"""Standalone one-PBC application surface for the DOM package."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from . import agent
from . import runtime
from . import ui


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
            "workbench",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench"),
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

    def __init__(self, *, tenant: str = "default", state: dict[str, Any] | None = None) -> None:
        self.tenant = tenant
        self.state = _ensure_state(state or runtime.dom_empty_state())

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)

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
        return rendered


def standalone_smoke_test() -> dict[str, Any]:
    app = DomStandaloneApplication(tenant="tenant_alpha")
    app.configure()
    app.register_defaults()
    app.upsert_customer_projection(
        {
            "tenant": "tenant_alpha",
            "customer_id": "cust_100",
            "status": "active",
            "risk": 0.08,
        }
    )
    app.capture_order(
        {
            "tenant": "tenant_alpha",
            "order_id": "order_100",
            "customer_id": "cust_100",
            "channel": "web",
            "destination": "BOS",
            "service_level": "standard",
            "currency": "USD",
            "lines": (
                {"line_id": "line_1", "item_id": "sku_100", "quantity": 2, "unit_price": 125},
                {"line_id": "line_2", "item_id": "sku_200", "quantity": 1, "unit_price": 80},
            ),
        }
    )
    app.apply_tax_projection("order_100", {"calculation_id": "tax_100", "tax_total": 33.0, "status": "calculated"})
    app.screen_fraud("order_100", signals={"ip_risk": 0.05, "velocity": 0.08, "customer_risk": 0.08})
    verification = app.verify_order("order_100")
    app.price_order("order_100")
    allocation = app.apply_inventory_allocation(
        "order_100",
        (
            {"allocation_id": "alloc_100", "item_id": "sku_100", "quantity": 2, "node_id": "node_east", "confidence": 0.93},
            {"allocation_id": "alloc_101", "item_id": "sku_200", "quantity": 1, "node_id": "node_west", "confidence": 0.88},
        ),
    )
    plan = app.create_fulfillment_plan("order_100")
    route = app.route_fulfillment("order_100")
    shipped = app.confirm_order_shipped("order_100", shipment_id="ship_100")
    workbench = app.workbench(tenant="tenant_alpha")
    document = app.document_intake(
        "Order order_100 customer cust_100 channel web amount 330 lines sku_100 x2 @125 and sku_200 x1 @80",
        "create the order and prepare the verification workbench",
    )
    return {
        "ok": verification["ok"]
        and allocation["ok"]
        and plan["ok"]
        and route["ok"]
        and shipped["ok"]
        and workbench["ok"]
        and document["ok"],
        "manifest": standalone_manifest(),
        "state": app.snapshot(),
        "workbench": workbench,
        "document": document["plan"],
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
