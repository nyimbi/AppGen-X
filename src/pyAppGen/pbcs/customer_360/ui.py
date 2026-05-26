"""UI contract for the Customer 360 PBC."""

from __future__ import annotations


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
        "action_permissions": {
            "create_profile": "customer_360.profile",
            "link_identity": "customer_360.profile",
            "open_merge_case": "customer_360.merge",
            "resolve_merge_case": "customer_360.merge",
            "record_consent": "customer_360.consent",
            "set_preference": "customer_360.consent",
            "capture_touchpoint": "customer_360.engage",
            "ingest_engagement_event": "customer_360.engage",
            "register_rule": "customer_360.configure",
            "set_parameter": "customer_360.configure",
            "configure_runtime": "customer_360.configure",
            "run_control_tests": "customer_360.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "identity_match_threshold",
                "churn_risk_threshold",
                "engagement_decay_days",
                "minimum_consent_confidence",
                "timeline_limit",
                "retention_days",
            ),
        },
        "rule_editor": {
            "rule_types": ("privacy", "identity", "preference", "engagement", "segment", "merge"),
            "required_fields": ("rule_id", "tenant", "rule_type", "allowed_channels", "required_consents", "status"),
        },
        "event_surfaces": {
            "emits": ("CustomerUpdated", "CustomerIdentityLinked", "PreferenceChanged", "ConsentRecorded", "TouchpointCaptured", "CustomerSegmentUpdated"),
            "consumes": ("InvoiceIssued", "PaymentCaptured", "OrderVerified", "ServiceTicketClosed", "LoyaltyRewardEarned", "CandidateHired"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
    visible_actions = tuple(action for action, required_permission in action_permissions.items() if required_permission in permissions)
    profiles = tuple(profile for profile in state["profiles"].values() if profile["tenant"] == tenant)
    identities = tuple(identity for identity in state["identities"].values() if identity["tenant"] == tenant)
    consents = tuple(consent for consent in state["consents"].values() if consent["tenant"] == tenant)
    engagements = tuple(event for event in state["engagements"].values() if event["tenant"] == tenant)
    cards = (
        {"key": "profiles", "value": len(profiles), "fragment": "CustomerProfileRegistry"},
        {"key": "identities", "value": len(identities), "fragment": "IdentityResolutionPanel"},
        {"key": "effective_consents", "value": len(tuple(consent for consent in consents if consent["effective"])), "fragment": "ConsentPreferenceCenter"},
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
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
    }
