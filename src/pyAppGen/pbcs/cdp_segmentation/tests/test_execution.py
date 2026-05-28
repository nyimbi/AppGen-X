"""Execution-focused tests for the cdp_segmentation PBC slice."""

from __future__ import annotations

from .. import agent
from .. import handlers
from .. import routes
from .. import services
from .. import ui
from ..release_evidence import build_release_evidence
from ..runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
from ..runtime import cdp_segmentation_activate_segment
from ..runtime import cdp_segmentation_build_workbench_view
from ..runtime import cdp_segmentation_configure_runtime
from ..runtime import cdp_segmentation_define_segment
from ..runtime import cdp_segmentation_empty_state
from ..runtime import cdp_segmentation_evaluate_segments
from ..runtime import cdp_segmentation_ingest_customer_event
from ..runtime import cdp_segmentation_set_parameter


def _configured_state():
    state = cdp_segmentation_empty_state()
    state = cdp_segmentation_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US",),
            "supported_event_types": ("profile", "payment", "shipment", "engagement"),
            "identity_keys": ("customer_id", "email"),
            "default_timezone": "UTC",
            "activation_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("membership_score_threshold", 0.68),
        ("payment_value_weight", 0.35),
        ("order_recency_weight", 0.25),
        ("engagement_weight", 0.40),
        ("profile_merge_confidence_threshold", 0.85),
        ("consent_risk_threshold", 0.60),
        ("event_freshness_days", 180),
        ("activation_batch_limit", 5000),
        ("max_segments_per_profile", 20),
        ("workbench_limit", 50),
    ):
        state = cdp_segmentation_set_parameter(state, name, value)["state"]
    return state


def test_runtime_slice_tracks_membership_transitions_and_activation_evidence():
    state = _configured_state()
    for event in (
        {
            "event_id": "profile_a",
            "tenant": "tenant_a",
            "customer_id": "cust_a",
            "event_type": "profile",
            "region": "US",
            "properties": {"customer_id": "cust_a", "email": "a@example.com", "opt_in": True},
        },
        {
            "event_id": "payment_a",
            "tenant": "tenant_a",
            "customer_id": "cust_a",
            "event_type": "payment",
            "region": "US",
            "properties": {"amount": 2400.0},
        },
        {
            "event_id": "shipment_a",
            "tenant": "tenant_a",
            "customer_id": "cust_a",
            "event_type": "shipment",
            "region": "US",
            "properties": {"order_id": "ord_a"},
        },
        {
            "event_id": "engagement_a",
            "tenant": "tenant_a",
            "customer_id": "cust_a",
            "event_type": "engagement",
            "region": "US",
            "properties": {"clicks": 8},
        },
    ):
        state = cdp_segmentation_ingest_customer_event(state, event)["state"]
    state = cdp_segmentation_define_segment(
        state,
        {
            "segment_id": "seg_high_value",
            "tenant": "tenant_a",
            "name": "High Value Repeat Buyers",
            "criteria": {"min_payment_value": 1000, "requires_shipment": True, "min_engagement": 0.2},
            "status": "active",
        },
    )["state"]
    evaluated = cdp_segmentation_evaluate_segments(state, "cust_a")
    state = evaluated["state"]
    activated = cdp_segmentation_activate_segment(state, "seg_high_value")
    state = activated["state"]
    membership = next(iter(evaluated["memberships"]))
    assert membership["status"] == "member"
    assert membership["consent_status"] == "active"
    assert state["membership_evaluations"]
    assert state["activation_runs"]
    workbench = cdp_segmentation_build_workbench_view(state, tenant="tenant_a")
    assert workbench["consent_entry_count"] == 1
    assert workbench["top_segments"][0]["member_count"] == 1


def test_service_route_handler_and_agent_surfaces_execute_with_explicit_state():
    service = services.CdpSegmentationService()
    state = _configured_state()
    configured = service.execute_operation(
        "define_segment",
        {
            "state": state,
            "segment_id": "seg_route",
            "tenant": "tenant_a",
            "name": "Consent Ready Buyers",
            "criteria": {"min_payment_value": 0, "requires_shipment": False, "min_engagement": 0.0},
            "status": "active",
        },
    )
    assert configured["ok"] is True
    routed = routes.dispatch_route(
        "POST",
        "/events",
        {
            "state": configured["state"],
            "event_id": "profile_route",
            "tenant": "tenant_a",
            "customer_id": "cust_route",
            "event_type": "profile",
            "region": "US",
            "properties": {"customer_id": "cust_route", "email": "route@example.com", "opt_in": True},
        },
    )
    assert routed["ok"] is True
    handled = handlers.dispatch_event(
        {
            "event_type": "CustomerUpdated",
            "event_id": "evt_handler",
            "payload": {"tenant": "tenant_a", "customer_id": "cust_handler", "email": "handler@example.com", "region": "US", "opt_in": True},
        },
        routed["state"],
    )
    assert handled["handled"] is True
    assert handled["runtime_result"]["ok"] is True
    instruction = agent.document_instruction_plan(
        "Draft a retention audience for opted-in repeat buyers.",
        "Create a segment and prepare the related governance trail.",
    )
    crud = agent.datastore_crud_plan("update", table="cdp_segmentation_segment_definition", payload={"status": "active"})
    assert instruction["suggested_action"] == "define_segment"
    assert crud["preferred_operation"] == "define_segment"


def test_ui_and_release_evidence_cover_docs_and_execution_inventory():
    rendered = ui.cdp_segmentation_render_workbench(
        _configured_state(),
        tenant="tenant_a",
        principal_permissions=tuple(ui.cdp_segmentation_ui_contract()["action_permissions"].values()),
    )
    evidence = build_release_evidence()
    assert rendered["ok"] is True
    assert rendered["forms"]["event_intake"]["submit_action"] == "ingest_customer_event"
    assert rendered["wizards"]["activation_readiness"]["submit_action"] == "allocate_activation"
    assert all(evidence["documentation_inventory"].values())
    assert all(evidence["test_inventory"].values())
