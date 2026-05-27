"""UI contract for the CDP Segmentation PBC."""

from __future__ import annotations

from .runtime import CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
from .runtime import CDP_SEGMENTATION_OWNED_TABLES
from .runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
from .runtime import CDP_SEGMENTATION_RUNTIME_TABLES


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
    "CdpSchemaContractExplorer",
    "CdpServiceContractExplorer",
    "CdpReleaseEvidencePanel",
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
            "/workbench/pbcs/cdp_segmentation/schema-contract",
            "/workbench/pbcs/cdp_segmentation/service-contract",
            "/workbench/pbcs/cdp_segmentation/release-evidence",
        ),
        "action_permissions": {
            "ingest_customer_event": "cdp_segmentation.event.write",
            "upsert_profile_property": "cdp_segmentation.event.write",
            "define_segment": "cdp_segmentation.segment.write",
            "evaluate_segments": "cdp_segmentation.membership.evaluate",
            "activate_segment": "cdp_segmentation.membership.evaluate",
            "simulate_segment_membership": "cdp_segmentation.analytics.write",
            "forecast_audience": "cdp_segmentation.analytics.write",
            "resolve_audience_exception": "cdp_segmentation.profile.govern",
            "parse_segment_rule": "cdp_segmentation.segment.write",
            "score_lifecycle_risk": "cdp_segmentation.analytics.write",
            "heal_profile_merge": "cdp_segmentation.profile.govern",
            "generate_profile_proof": "cdp_segmentation.profile.govern",
            "screen_consent_policy": "cdp_segmentation.profile.govern",
            "run_data_quality_controls": "cdp_segmentation.audit",
            "federate_customer_view": "cdp_segmentation.profile.govern",
            "allocate_activation": "cdp_segmentation.membership.evaluate",
            "detect_profile_anomaly": "cdp_segmentation.analytics.write",
            "register_governed_model": "cdp_segmentation.configure",
            "receive_event": "cdp_segmentation.event.consume",
            "register_rule": "cdp_segmentation.configure",
            "set_parameter": "cdp_segmentation.configure",
            "configure_runtime": "cdp_segmentation.configure",
            "run_control_tests": "cdp_segmentation.audit",
            "build_schema_contract": "cdp_segmentation.audit",
            "build_service_contract": "cdp_segmentation.audit",
            "build_release_evidence": "cdp_segmentation.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_region", "default_timezone", "activation_mode"),
            "allowed_database_backends": CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
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
        "rule_editor": {
            "rule_types": ("configuration", "parameter", "release_gate", "domain_policy"),
            "required_fields": ("rule_id", "tenant", "rule_type", "status"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "event_surfaces": {
            "emits": ("CustomerSegmentUpdated", "ProfileEnriched"),
            "consumes": ("CustomerUpdated", "PaymentCaptured", "OrderShipped"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": CDP_SEGMENTATION_OWNED_TABLES,
            "runtime_tables": CDP_SEGMENTATION_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
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
            "runtime_tables": CDP_SEGMENTATION_RUNTIME_TABLES,
            "shared_table_access": False,
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = cdp_segmentation_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = cdp_segmentation_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
