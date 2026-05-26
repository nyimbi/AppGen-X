"""UI contract for the Customer 360 PBC."""

from __future__ import annotations

from .runtime import CUSTOMER_360_ALLOWED_DATABASE_BACKENDS
from .runtime import CUSTOMER_360_CONSUMED_EVENT_TYPES
from .runtime import CUSTOMER_360_EMITTED_EVENT_TYPES
from .runtime import CUSTOMER_360_OWNED_TABLES
from .runtime import CUSTOMER_360_REQUIRED_EVENT_TOPIC
from .runtime import CUSTOMER_360_REQUIRED_RULE_FIELDS
from .runtime import CUSTOMER_360_SUPPORTED_CONFIGURATION_FIELDS
from .runtime import CUSTOMER_360_SUPPORTED_PARAMETER_KEYS
from .runtime import customer_360_permissions_contract

CUSTOMER_360_UI_FRAGMENT_KEYS = (
    "Customer360Workbench",
    "CustomerProfileRegistry",
    "IdentityResolutionPanel",
    "ConsentPreferenceCenter",
    "TouchpointCaptureConsole",
    "EngagementTimeline",
    "RelationshipGraph",
    "ProfileMergeReview",
    "SegmentProjectionDashboard",
    "CustomerRuleStudio",
    "CustomerParameterConsole",
    "CustomerConfigurationPanel",
)


def customer_360_ui_contract() -> dict:
    return {
        "format": "appgen.customer-360-ui-contract.v1",
        "ok": True,
        "pbc": "customer_360",
        "implementation_directory": "src/pyAppGen/pbcs/customer_360",
        "fragments": CUSTOMER_360_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/customer_360",
            "/workbench/pbcs/customer_360/profiles",
            "/workbench/pbcs/customer_360/identities",
            "/workbench/pbcs/customer_360/consents",
            "/workbench/pbcs/customer_360/preferences",
            "/workbench/pbcs/customer_360/touchpoints",
            "/workbench/pbcs/customer_360/timeline",
            "/workbench/pbcs/customer_360/relationships",
            "/workbench/pbcs/customer_360/merge-review",
            "/workbench/pbcs/customer_360/segments",
            "/workbench/pbcs/customer_360/rules",
            "/workbench/pbcs/customer_360/parameters",
            "/workbench/pbcs/customer_360/configuration",
        ),
        "panels": (
            {
                "key": "profile_registry",
                "fragment": "CustomerProfileRegistry",
                "binds_to": ("customer_profile", "customer_identity", "customer_relationship"),
                "commands": ("create_profile", "link_identity", "open_merge_case", "resolve_merge_case"),
            },
            {
                "key": "consent_preferences",
                "fragment": "ConsentPreferenceCenter",
                "binds_to": ("consent_record", "communication_preference", "outbox"),
                "commands": ("record_consent", "set_preference", "screen_privacy_policy"),
            },
            {
                "key": "engagement",
                "fragment": "EngagementTimeline",
                "binds_to": ("touchpoint", "engagement_event", "customer_timeline", "customer_segment_projection"),
                "commands": ("capture_touchpoint", "ingest_engagement_event", "build_timeline"),
            },
            {
                "key": "governance_studio",
                "fragment": "CustomerRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": customer_360_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": CUSTOMER_360_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": CUSTOMER_360_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
            "visible_event_contracts": ("AppGen-X",),
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": CUSTOMER_360_SUPPORTED_PARAMETER_KEYS,
            "supported_parameters": CUSTOMER_360_SUPPORTED_PARAMETER_KEYS,
        },
        "rule_editor": {
            "rule_types": ("privacy", "identity", "preference", "engagement", "segment", "merge"),
            "required_fields": CUSTOMER_360_REQUIRED_RULE_FIELDS,
            "compiled_evidence_fields": ("compiled_hash", "compiled_evidence"),
        },
        "event_surfaces": {
            "emits": CUSTOMER_360_EMITTED_EVENT_TYPES,
            "consumes": CUSTOMER_360_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": CUSTOMER_360_OWNED_TABLES,
            "outbox_table": "customer_360_appgen_outbox_event",
            "inbox_table": "customer_360_appgen_inbox_event",
            "dead_letter_table": "customer_360_dead_letter_event",
            "shared_table_access": False,
        },
    }


def customer_360_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = customer_360_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    profiles = tuple(profile for profile in state["profiles"].values() if profile["tenant"] == tenant)
    identities = tuple(identity for identity in state["identities"].values() if identity["tenant"] == tenant)
    consents = tuple(consent for consent in state["consents"].values() if consent["tenant"] == tenant)
    engagements = tuple(event for event in state["engagements"].values() if event["tenant"] == tenant)
    configuration = state["configuration"]
    rule_ids = tuple(sorted(state["rules"]))
    parameter_names = tuple(sorted(state["parameters"]))
    cards = (
        {"key": "profiles", "value": len(profiles), "fragment": "CustomerProfileRegistry"},
        {"key": "identities", "value": len(identities), "fragment": "IdentityResolutionPanel"},
        {
            "key": "effective_consents",
            "value": len(tuple(consent for consent in consents if consent["effective"])),
            "fragment": "ConsentPreferenceCenter",
        },
        {"key": "engagements", "value": len(engagements), "fragment": "EngagementTimeline"},
        {"key": "customer_value", "value": round(sum(event.get("value", 0) for event in engagements), 2), "fragment": "SegmentProjectionDashboard"},
        {"key": "outbox", "value": len(state["outbox"]), "fragment": "EngagementTimeline"},
    )
    return {
        "format": "appgen.customer-360-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/customer_360",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(configuration.get("ok")),
        "rules_bound": rule_ids,
        "parameters_bound": parameter_names,
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": CUSTOMER_360_OWNED_TABLES,
            "outbox_table": "customer_360_appgen_outbox_event",
            "inbox_table": "customer_360_appgen_inbox_event",
            "dead_letter_table": "customer_360_dead_letter_event",
            "configuration": {
                "bound": bool(configuration.get("ok")),
                "database_backend": configuration.get("database_backend"),
                "event_contract": configuration.get("event_contract"),
                "event_topic": configuration.get("event_topic"),
                "visible_event_contracts": configuration.get("visible_event_contracts", ()),
                "stream_engine_picker_visible": configuration.get("stream_engine_picker_visible"),
                "user_selectable_event_contract": configuration.get("user_selectable_event_contract"),
                "supported_fields": configuration.get(
                    "supported_configuration_fields",
                    CUSTOMER_360_SUPPORTED_CONFIGURATION_FIELDS,
                ),
            },
            "rules": tuple(
                {
                    "rule_id": rule_id,
                    "compiled_hash": state["rules"][rule_id].get("compiled_hash"),
                    "required_fields": state["rules"][rule_id].get("compiled_evidence", {}).get("required_fields", ()),
                }
                for rule_id in rule_ids
            ),
            "parameters": {
                "supported": CUSTOMER_360_SUPPORTED_PARAMETER_KEYS,
                "active": parameter_names,
            },
        },
        "event_outbox_count": len(state["outbox"]),
    }
