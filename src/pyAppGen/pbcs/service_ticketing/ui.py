"""UI contract for the Service Ticketing PBC."""

from __future__ import annotations

from .runtime import SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
from .runtime import SERVICE_TICKETING_OWNED_TABLES


SERVICE_TICKETING_UI_FRAGMENT_KEYS = (
    "ServiceTicketingWorkbench",
    "TicketInbox",
    "CustomerContextPanel",
    "SlaPolicyDesigner",
    "AssignmentQueueBoard",
    "EscalationCommandCenter",
    "ResolutionConsole",
    "NextBestResponsePanel",
    "PreferenceProjectionPanel",
    "ServiceRuleStudio",
    "ServiceParameterConsole",
    "ServiceConfigurationPanel",
    "ServiceEventOutbox",
    "ServiceDeadLetterQueue",
)


def service_ticketing_ui_contract() -> dict:
    return {
        "format": "appgen.service-ticketing-ui-contract.v1",
        "ok": True,
        "pbc": "service_ticketing",
        "implementation_directory": "src/pyAppGen/pbcs/service_ticketing",
        "fragments": SERVICE_TICKETING_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/service_ticketing",
            "/workbench/pbcs/service_ticketing/tickets",
            "/workbench/pbcs/service_ticketing/sla",
            "/workbench/pbcs/service_ticketing/assignments",
            "/workbench/pbcs/service_ticketing/escalations",
            "/workbench/pbcs/service_ticketing/configuration",
        ),
        "panels": (
            {"key": "tickets", "fragment": "TicketInbox", "binds_to": ("support_ticket",), "commands": ("open_ticket", "resolve_ticket")},
            {"key": "sla", "fragment": "SlaPolicyDesigner", "binds_to": ("sla_policy", "escalation_event"), "commands": ("create_sla_policy", "record_escalation")},
            {"key": "assignments", "fragment": "AssignmentQueueBoard", "binds_to": ("case_assignment",), "commands": ("assign_ticket",)},
            {"key": "governance", "fragment": "ServiceRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "action_permissions": {
            "open_ticket": "service_ticketing.ticket.write",
            "resolve_ticket": "service_ticketing.ticket.write",
            "assign_ticket": "service_ticketing.assignment.write",
            "create_sla_policy": "service_ticketing.configure",
            "record_escalation": "service_ticketing.escalation.write",
            "receive_event": "service_ticketing.event.consume",
            "register_rule": "service_ticketing.configure",
            "set_parameter": "service_ticketing.configure",
            "configure_runtime": "service_ticketing.configure",
            "run_control_tests": "service_ticketing.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_region", "default_timezone", "assignment_mode"),
            "allowed_database_backends": SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "sla_breach_risk_threshold",
                "auto_escalation_threshold",
                "sentiment_risk_weight",
                "priority_weight",
                "customer_tier_weight",
                "queue_load_weight",
                "first_response_minutes",
                "resolution_target_hours",
                "max_open_cases_per_owner",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("assignment", "escalation", "sla", "channel", "priority"),
            "required_fields": ("rule_id", "tenant", "scope", "status", "allowed_regions", "allowed_channels", "allowed_priorities", "assignment_policy", "escalation_policy"),
        },
        "event_surfaces": {
            "emits": ("SupportCaseOpened", "SlaBreached", "CustomerUpdated"),
            "consumes": ("CustomerUpdated", "PreferenceChanged"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def service_ticketing_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = service_ticketing_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "tickets", "value": view["ticket_count"], "fragment": "TicketInbox"},
        {"key": "open", "value": view["open_ticket_count"], "fragment": "TicketInbox"},
        {"key": "resolved", "value": view["resolved_ticket_count"], "fragment": "ResolutionConsole"},
        {"key": "escalations", "value": view["escalation_count"], "fragment": "EscalationCommandCenter"},
        {"key": "outbox", "value": view["outbox_count"], "fragment": "ServiceEventOutbox"},
        {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "ServiceDeadLetterQueue"},
    )
    return {
        "format": "appgen.service-ticketing-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/service_ticketing",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    tickets = tuple(item for item in state.get("support_tickets", {}).values() if item["tenant"] == tenant)
    escalations = tuple(item for item in state.get("escalation_events", {}).values() if item["tenant"] == tenant)
    return {
        "ticket_count": len(tickets),
        "open_ticket_count": len(tuple(item for item in tickets if item["status"] in {"open", "assigned", "escalated"})),
        "resolved_ticket_count": len(tuple(item for item in tickets if item["status"] == "resolved")),
        "escalation_count": len(escalations),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        },
    }
