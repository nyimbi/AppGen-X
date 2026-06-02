"""One-PBC application surface for order routing optimization."""

from __future__ import annotations

import hashlib

PBC_KEY = "order_routing_optimization"
OWNED_TABLES = (
    "order_routing_optimization_routing_plan",
    "order_routing_optimization_routing_plan_leg",
    "order_routing_optimization_routing_node",
    "order_routing_optimization_routing_node_calendar",
    "order_routing_optimization_routing_node_service",
    "order_routing_optimization_routing_node_capacity",
    "order_routing_optimization_route_candidate",
    "order_routing_optimization_capacity_snapshot",
    "order_routing_optimization_routing_decision",
    "order_routing_optimization_node_reservation",
    "order_routing_optimization_split_shipment",
    "order_routing_optimization_split_shipment_leg",
    "order_routing_optimization_routing_exception",
    "order_routing_optimization_exception_resolution",
    "order_routing_optimization_routing_approval",
    "order_routing_optimization_routing_feedback",
    "order_routing_optimization_routing_rule",
    "order_routing_optimization_routing_parameter",
    "order_routing_optimization_routing_configuration",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def routing_forms_contract() -> dict:
    """Return the forms a single-PBC routing app can render and bind."""
    forms = (
        {
            "form_id": "route_request_intake_form",
            "writes_table": "order_routing_optimization_routing_plan",
            "command": "route_orders",
            "fields": (
                "tenant",
                "order_id",
                "channel",
                "destination_region",
                "requested_units",
                "sku_lines",
                "sla_target_hours",
                "priority_class",
                "ship_complete_preference",
            ),
            "validations": (
                "order_id_required",
                "sku_lines_required",
                "sla_target_required",
                "tenant_scope_required",
            ),
        },
        {
            "form_id": "routing_node_profile_form",
            "writes_table": "order_routing_optimization_routing_node",
            "command": "ingest_capacity_snapshot",
            "fields": (
                "tenant",
                "node_id",
                "node_type",
                "region",
                "timezone",
                "available_to_promise",
                "blackout_windows",
                "service_classes",
            ),
            "validations": (
                "node_region_supported",
                "timezone_required",
                "service_class_required",
                "atp_non_negative",
            ),
        },
        {
            "form_id": "capacity_snapshot_form",
            "writes_table": "order_routing_optimization_capacity_snapshot",
            "command": "ingest_capacity_snapshot",
            "fields": (
                "tenant",
                "snapshot_id",
                "node_id",
                "available_units",
                "reserved_units",
                "forecast_load",
                "cutoff_time",
                "source_event_id",
            ),
            "validations": (
                "node_exists",
                "available_units_non_negative",
                "reserved_units_not_over_capacity",
                "source_event_idempotent",
            ),
        },
        {
            "form_id": "route_candidate_form",
            "writes_table": "order_routing_optimization_route_candidate",
            "command": "upsert_route_candidate",
            "fields": (
                "tenant",
                "candidate_id",
                "order_id",
                "node_id",
                "total_cost",
                "sla_hours",
                "carbon_kg",
                "risk_score",
                "substitution_mode",
            ),
            "validations": (
                "candidate_order_scope_required",
                "cost_sla_carbon_required",
                "node_capacity_projection_required",
                "substitution_allowed_by_rule",
            ),
        },
        {
            "form_id": "split_shipment_policy_form",
            "writes_table": "order_routing_optimization_split_shipment",
            "command": "route_orders",
            "fields": (
                "tenant",
                "order_id",
                "max_split_count",
                "minimum_leg_units",
                "customer_promise_policy",
                "excluded_nodes",
                "approval_threshold",
            ),
            "validations": (
                "max_split_within_parameter_bounds",
                "minimum_leg_units_positive",
                "customer_promise_not_degraded_without_approval",
            ),
        },
        {
            "form_id": "reservation_and_commit_form",
            "writes_table": "order_routing_optimization_node_reservation",
            "command": "reserve_node_capacity",
            "fields": (
                "tenant",
                "decision_id",
                "order_id",
                "node_id",
                "allocated_units",
                "hold_minutes",
                "idempotency_key",
            ),
            "validations": (
                "decision_must_be_screened",
                "capacity_still_available",
                "idempotency_key_required",
                "reservation_hold_within_bounds",
            ),
        },
        {
            "form_id": "routing_exception_resolution_form",
            "writes_table": "order_routing_optimization_exception_resolution",
            "command": "recommend_exception_resolution",
            "fields": (
                "tenant",
                "exception_id",
                "resolution_action",
                "override_reason",
                "approver",
                "customer_impact",
                "control_evidence",
            ),
            "validations": (
                "exception_exists",
                "override_reason_required_for_manual_route",
                "approver_required_for_policy_override",
                "control_evidence_required",
            ),
        },
        {
            "form_id": "routing_governance_form",
            "writes_table": "order_routing_optimization_routing_rule",
            "command": "register_rule",
            "fields": (
                "tenant",
                "rule_id",
                "rule_type",
                "regions",
                "eligible_nodes",
                "capacity_floor",
                "split_policy",
                "substitution_mode",
                "effective_at",
            ),
            "validations": (
                "required_rule_fields_present",
                "rule_compiles_to_hash",
                "impact_simulation_required",
                "rollback_plan_required",
            ),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def routing_wizards_contract() -> dict:
    """Return guided routing workflows for operators and planners."""
    wizards = (
        {
            "wizard_id": "promise_safe_route_wizard",
            "steps": (
                "verify_order_projection",
                "load_availability_tax_transport_inputs",
                "score_candidates_by_cost_sla_capacity_risk_carbon",
                "screen_policy_and_split_rules",
                "reserve_capacity_and_publish_route",
            ),
            "completion_event": "FulfillmentRouteSelected",
        },
        {
            "wizard_id": "capacity_recovery_wizard",
            "steps": (
                "detect_capacity_shortfall",
                "rank_substitute_nodes",
                "simulate_customer_promise_delta",
                "request_or_auto_apply_approval",
                "publish_rebalanced_reservation",
            ),
            "completion_event": "NodeCapacityReserved",
        },
        {
            "wizard_id": "split_shipment_optimization_wizard",
            "steps": (
                "select_split_policy",
                "calculate_leg_costs_and_promises",
                "screen_customer_and_regional_constraints",
                "generate_split_route_plan",
                "capture_customer_impact_evidence",
            ),
            "completion_event": "FulfillmentRouteSelected",
        },
        {
            "wizard_id": "exception_resolution_wizard",
            "steps": (
                "triage_exception_severity",
                "explain_failed_constraints",
                "simulate_recovery_options",
                "capture_override_or_reject_decision",
                "close_exception_with_audit_trace",
            ),
            "completion_event": "RoutingExceptionResolved",
        },
        {
            "wizard_id": "routing_rule_change_wizard",
            "steps": (
                "draft_rule_or_parameter_change",
                "compile_policy_hash",
                "run_counterfactual_open_order_impact",
                "approve_and_activate_change",
                "monitor_post_activation_drift",
            ),
            "completion_event": "RoutingPolicyChanged",
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def routing_controls_contract() -> dict:
    """Return operator and release controls for the routing app."""
    controls = (
        {
            "control_id": "candidate_input_completeness_gate",
            "blocks_on_failure": True,
            "table_scope": (
                "order_routing_optimization_route_candidate",
                "order_routing_optimization_capacity_snapshot",
            ),
        },
        {
            "control_id": "capacity_reservation_idempotency_gate",
            "blocks_on_failure": True,
            "table_scope": ("order_routing_optimization_node_reservation",),
        },
        {
            "control_id": "split_promise_degradation_gate",
            "blocks_on_failure": True,
            "table_scope": (
                "order_routing_optimization_split_shipment",
                "order_routing_optimization_routing_promise",
            ),
        },
        {
            "control_id": "cost_sla_capacity_risk_weight_gate",
            "blocks_on_failure": True,
            "table_scope": (
                "order_routing_optimization_routing_parameter",
                "order_routing_optimization_routing_rule",
            ),
        },
        {
            "control_id": "policy_override_approval_gate",
            "blocks_on_failure": True,
            "table_scope": (
                "order_routing_optimization_routing_approval",
                "order_routing_optimization_exception_resolution",
            ),
        },
        {
            "control_id": "appgen_event_replay_gate",
            "blocks_on_failure": True,
            "table_scope": (
                "order_routing_optimization_appgen_outbox_event",
                "order_routing_optimization_appgen_inbox_event",
                "order_routing_optimization_dead_letter_event",
            ),
        },
        {
            "control_id": "owned_boundary_and_no_shared_tables_gate",
            "blocks_on_failure": True,
            "table_scope": OWNED_TABLES,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_routing_app_contract() -> dict:
    """Return evidence that this PBC can stand alone as a routing application."""
    forms = routing_forms_contract()["forms"]
    wizards = routing_wizards_contract()["wizards"]
    controls = routing_controls_contract()["controls"]
    return {
        "ok": bool(forms) and bool(wizards) and bool(controls),
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
        "owned_tables": OWNED_TABLES,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "workbench": "OrderRoutingWorkbench",
        "assistant_panel": "OrderRoutingOptimizationAgent",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_routing_plan(document: str, instructions: str) -> dict:
    """Map documents and instructions to governed CRUD previews."""
    text = f"{document} {instructions}".lower()
    if "capacity" in text or "atp" in text or "snapshot" in text:
        operation = "ingest_capacity_snapshot"
        table = "order_routing_optimization_capacity_snapshot"
    elif "candidate" in text or "node" in text or "carrier" in text:
        operation = "upsert_route_candidate"
        table = "order_routing_optimization_route_candidate"
    elif "split" in text or "partial" in text:
        operation = "route_orders"
        table = "order_routing_optimization_split_shipment"
    elif "reserve" in text or "commit" in text or "hold" in text:
        operation = "reserve_node_capacity"
        table = "order_routing_optimization_node_reservation"
    elif "exception" in text or "override" in text or "approval" in text:
        operation = "recommend_exception_resolution"
        table = "order_routing_optimization_exception_resolution"
    elif "rule" in text or "parameter" in text or "policy" in text:
        operation = "register_rule"
        table = "order_routing_optimization_routing_rule"
    else:
        operation = "route_orders"
        table = "order_routing_optimization_routing_plan"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document, instructions),
        "proposed_operation": operation,
        "target_table": table,
        "requires_human_confirmation": True,
        "crud_datastore_mutation": operation not in ("build_workbench_view",),
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def app_surface_smoke_test() -> dict:
    """Exercise standalone routing app contracts."""
    app = single_pbc_routing_app_contract()
    capacity_plan = document_instruction_routing_plan("node capacity snapshot", "load ATP")
    split_plan = document_instruction_routing_plan("customer allows partial shipment", "optimize split")
    checks = (
        app["ok"],
        len(app["forms"]) >= 8,
        len(app["wizards"]) >= 5,
        len(app["controls"]) >= 7,
        capacity_plan["target_table"] == "order_routing_optimization_capacity_snapshot",
        split_plan["target_table"] == "order_routing_optimization_split_shipment",
        all(
            table.startswith("order_routing_optimization_")
            for control in app["controls"]
            for table in control["table_scope"]
        ),
    )
    return {
        "ok": all(checks),
        "single_pbc_app": app,
        "document_plans": (capacity_plan, split_plan),
        "side_effects": (),
    }
