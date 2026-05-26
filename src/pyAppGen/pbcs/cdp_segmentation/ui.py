"""UI contract for the CDP Segmentation PBC."""

from __future__ import annotations

from .runtime import CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
from .runtime import CDP_SEGMENTATION_OWNED_TABLES


CDP_SEGMENTATION_UI_FRAGMENT_KEYS = (
    "CdpSegmentationWorkbench",
    "CustomerEventStream",
    "ProfilePropertyPanel",
    "SegmentDefinitionBuilder",
    "MembershipEvaluationBoard",
    "ActivationConsole",
    "ConsentPolicyPanel",
    "IdentityStitchingPanel",
    "CdpRuleStudio",
    "CdpParameterConsole",
    "CdpConfigurationPanel",
    "CdpEventOutbox",
    "CdpDeadLetterQueue",
)


def cdp_segmentation_ui_contract() -> dict:
    return {
        "format": "appgen.cdp-segmentation-ui-contract.v1",
        "ok": True,
        "pbc": "cdp_segmentation",
        "implementation_directory": "src/pyAppGen/pbcs/cdp_segmentation",
        "fragments": CDP_SEGMENTATION_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/cdp_segmentation",
            "/workbench/pbcs/cdp_segmentation/events",
            "/workbench/pbcs/cdp_segmentation/profiles",
            "/workbench/pbcs/cdp_segmentation/segments",
            "/workbench/pbcs/cdp_segmentation/memberships",
            "/workbench/pbcs/cdp_segmentation/configuration",
        ),
        "action_permissions": {
            "ingest_customer_event": "cdp_segmentation.event.write",
            "upsert_profile_property": "cdp_segmentation.event.write",
            "define_segment": "cdp_segmentation.segment.write",
            "evaluate_segments": "cdp_segmentation.membership.evaluate",
            "activate_segment": "cdp_segmentation.membership.evaluate",
            "receive_event": "cdp_segmentation.event.consume",
            "register_rule": "cdp_segmentation.configure",
            "set_parameter": "cdp_segmentation.configure",
            "configure_runtime": "cdp_segmentation.configure",
            "run_control_tests": "cdp_segmentation.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_region", "default_timezone", "activation_mode"),
            "allowed_database_backends": CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "membership_score_threshold",
                "profile_merge_confidence_threshold",
                "event_freshness_days",
                "payment_value_weight",
                "order_recency_weight",
                "engagement_weight",
                "consent_risk_threshold",
                "activation_batch_limit",
                "max_segments_per_profile",
                "workbench_limit",
            ),
        },
        "event_surfaces": {
            "emits": ("CustomerSegmentUpdated", "ProfileEnriched"),
            "consumes": ("CustomerUpdated", "PaymentCaptured", "OrderShipped"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def cdp_segmentation_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = cdp_segmentation_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, permission in contract["action_permissions"].items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "events", "value": view["event_count"], "fragment": "CustomerEventStream"},
        {"key": "profiles", "value": view["profile_count"], "fragment": "ProfilePropertyPanel"},
        {"key": "segments", "value": view["segment_count"], "fragment": "SegmentDefinitionBuilder"},
        {"key": "memberships", "value": view["membership_count"], "fragment": "MembershipEvaluationBoard"},
        {"key": "outbox", "value": view["outbox_count"], "fragment": "CdpEventOutbox"},
        {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "CdpDeadLetterQueue"},
    )
    return {
        "format": "appgen.cdp-segmentation-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/cdp_segmentation",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    events = tuple(item for item in state.get("customer_events", {}).values() if item["tenant"] == tenant)
    segments = tuple(item for item in state.get("segment_definitions", {}).values() if item["tenant"] == tenant)
    memberships = tuple(item for item in state.get("segment_memberships", {}).values() if item["tenant"] == tenant)
    profiles = {item["customer_id"] for item in state.get("profile_properties", {}).values() if item["tenant"] == tenant}
    return {
        "event_count": len(events),
        "profile_count": len(profiles),
        "segment_count": len(segments),
        "membership_count": len(memberships),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
        },
    }
