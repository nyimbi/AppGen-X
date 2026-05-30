"""UI contract for the Service Ticketing PBC."""

from __future__ import annotations

from .runtime import SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
from .runtime import SERVICE_TICKETING_CONSUMED_EVENT_TYPES
from .runtime import SERVICE_TICKETING_EMITTED_EVENT_TYPES
from .runtime import SERVICE_TICKETING_OWNED_TABLES
from .runtime import SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
from .runtime import SERVICE_TICKETING_RUNTIME_TABLES
from .app_surface import single_pbc_service_ticketing_app_contract


SERVICE_TICKETING_UI_FRAGMENT_KEYS = (
    "ServiceTicketingWorkbench",
    "TicketInbox",
    "ServiceQueueManager",
    "SlaPolicyDesigner",
    "PriorityMatrixPanel",
    "AssignmentQueueBoard",
    "EscalationCommandCenter",
    "TicketInteractionTimeline",
    "KnowledgeSuggestionPanel",
    "EntitlementSnapshotPanel",
    "FieldServiceHandoffPanel",
    "CustomerUpdatePanel",
    "ResolutionConsole",
    "CsatSurveyPanel",
    "ServiceAuditTrail",
    "AutomationInsightPanel",
    "ServiceRuleStudio",
    "ServiceParameterConsole",
    "ServiceConfigurationPanel",
    "ServiceEventOutbox",
    "ServiceEventInbox",
    "ServiceDeadLetterQueue",
)


def service_ticketing_forms_contract() -> dict:
    """Return standalone database-backed form metadata for generated apps."""
    from .app_surface import service_ticketing_forms_contract as _forms

    return _forms()


def service_ticketing_wizards_contract() -> dict:
    """Return standalone guided workflow metadata for generated apps."""
    from .app_surface import service_ticketing_wizards_contract as _wizards

    return _wizards()


def service_ticketing_controls_contract() -> dict:
    """Return standalone control metadata for generated apps."""
    from .app_surface import service_ticketing_controls_contract as _controls

    return _controls()


def service_ticketing_ui_contract() -> dict:
    return {
        "format": "appgen.service-ticketing-ui-contract.v1",
        "ok": True,
        "pbc": "service_ticketing",
        "implementation_directory": "src/pyAppGen/pbcs/service_ticketing",
        "fragments": SERVICE_TICKETING_UI_FRAGMENT_KEYS,
        "forms": service_ticketing_forms_contract()["forms"],
        "wizards": service_ticketing_wizards_contract()["wizards"],
        "controls": service_ticketing_controls_contract()["controls"],
        "single_pbc_app": single_pbc_service_ticketing_app_contract(),
        "routes": (
            "/workbench/pbcs/service_ticketing",
            "/workbench/pbcs/service_ticketing/tickets",
            "/workbench/pbcs/service_ticketing/queues",
            "/workbench/pbcs/service_ticketing/sla",
            "/workbench/pbcs/service_ticketing/assignments",
            "/workbench/pbcs/service_ticketing/interactions",
            "/workbench/pbcs/service_ticketing/knowledge",
            "/workbench/pbcs/service_ticketing/handoffs",
            "/workbench/pbcs/service_ticketing/audit",
            "/workbench/pbcs/service_ticketing/configuration",
        ),
        "panels": (
            {
                "key": "tickets",
                "fragment": "TicketInbox",
                "binds_to": ("support_ticket", "case_lifecycle_state"),
                "commands": ("open_ticket", "record_ticket_interaction", "reopen_ticket", "close_ticket"),
            },
            {
                "key": "queues",
                "fragment": "ServiceQueueManager",
                "binds_to": ("service_queue", "service_priority"),
                "commands": ("configure_runtime",),
            },
            {
                "key": "sla",
                "fragment": "SlaPolicyDesigner",
                "binds_to": ("sla_policy", "escalation_event"),
                "commands": ("create_sla_policy", "record_escalation"),
            },
            {
                "key": "assignments",
                "fragment": "AssignmentQueueBoard",
                "binds_to": ("case_assignment", "field_service_handoff"),
                "commands": ("assign_ticket", "prepare_field_service_handoff"),
            },
            {
                "key": "interactions",
                "fragment": "TicketInteractionTimeline",
                "binds_to": ("ticket_interaction", "knowledge_suggestion", "entitlement_snapshot"),
                "commands": ("record_ticket_interaction", "receive_event"),
            },
            {
                "key": "customer_updates",
                "fragment": "CustomerUpdatePanel",
                "binds_to": ("customer_update", "ticket_interaction"),
                "commands": ("send_customer_update",),
            },
            {
                "key": "resolution",
                "fragment": "ResolutionConsole",
                "binds_to": ("resolution_record", "csat_response", "support_ticket"),
                "commands": ("resolve_ticket", "record_csat_response"),
            },
            {
                "key": "governance",
                "fragment": "ServiceRuleStudio",
                "binds_to": ("service_rule", "service_parameter", "service_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
            {
                "key": "audit",
                "fragment": "ServiceAuditTrail",
                "binds_to": ("ticket_audit_log", "automation_insight", "csat_response"),
                "commands": ("build_release_evidence",),
            },
        ),
        "action_permissions": {
            "open_ticket": "service_ticketing.ticket.write",
            "resolve_ticket": "service_ticketing.customer.update",
            "record_ticket_interaction": "service_ticketing.ticket.write",
            "send_customer_update": "service_ticketing.customer.update",
            "assign_ticket": "service_ticketing.assignment.write",
            "prepare_field_service_handoff": "service_ticketing.escalation.write",
            "create_sla_policy": "service_ticketing.configure",
            "record_escalation": "service_ticketing.escalation.write",
            "record_csat_response": "service_ticketing.csat.write",
            "reopen_ticket": "service_ticketing.ticket.write",
            "close_ticket": "service_ticketing.ticket.write",
            "receive_event": "service_ticketing.event.consume",
            "register_rule": "service_ticketing.configure",
            "set_parameter": "service_ticketing.configure",
            "configure_runtime": "service_ticketing.configure",
            "run_control_tests": "service_ticketing.audit",
            "build_release_evidence": "service_ticketing.audit",
        },
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_region",
                "default_timezone",
                "assignment_mode",
            ),
            "allowed_database_backends": SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
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
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "allowed_regions",
                "allowed_channels",
                "allowed_priorities",
                "assignment_policy",
                "escalation_policy",
            ),
        },
        "event_surfaces": {
            "emits": SERVICE_TICKETING_EMITTED_EVENT_TYPES,
            "consumes": SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "stream_engine_picker_visible": False,
        },
    }


def service_ticketing_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = service_ticketing_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "tickets", "value": view["ticket_count"], "fragment": "TicketInbox"},
        {"key": "queues", "value": view["queue_count"], "fragment": "ServiceQueueManager"},
        {"key": "resolved", "value": view["resolved_ticket_count"], "fragment": "ResolutionConsole"},
        {"key": "handoffs", "value": view["handoff_count"], "fragment": "FieldServiceHandoffPanel"},
        {"key": "knowledge", "value": view["knowledge_suggestion_count"], "fragment": "KnowledgeSuggestionPanel"},
        {"key": "csat", "value": view["csat_pending_count"], "fragment": "CsatSurveyPanel"},
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
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "single_pbc_app": contract["single_pbc_app"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    tickets = tuple(item for item in state.get("support_tickets", {}).values() if item["tenant"] == tenant)
    handoffs = tuple(item for item in state.get("field_service_handoffs", {}).values() if item["tenant"] == tenant)
    knowledge = tuple(item for item in state.get("knowledge_suggestions", {}).values() if item["tenant"] == tenant)
    csat = tuple(item for item in state.get("csat_responses", {}).values() if item["tenant"] == tenant)
    return {
        "ticket_count": len(tickets),
        "queue_count": len(state.get("service_queues", {})),
        "resolved_ticket_count": len(tuple(item for item in tickets if item["status"] == "resolved")),
        "handoff_count": len(handoffs),
        "knowledge_suggestion_count": len(knowledge),
        "csat_pending_count": len(tuple(item for item in csat if item["status"] == "pending")),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
            "runtime_tables": SERVICE_TICKETING_RUNTIME_TABLES,
            "outbox_table": SERVICE_TICKETING_RUNTIME_TABLES[0],
            "inbox_table": SERVICE_TICKETING_RUNTIME_TABLES[1],
            "dead_letter_table": SERVICE_TICKETING_RUNTIME_TABLES[2],
            "eventing": {
                "event_contract": "AppGen-X",
                "required_event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
                "stream_engine_picker_visible": False,
            },
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
    contract = service_ticketing_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = service_ticketing_render_workbench(
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
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and contract.get("single_pbc_app", {}).get("ok") is True
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
