"""Service layer for the sports_venue_event_operations PBC."""

from __future__ import annotations

from .domain_depth import (
    DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS,
    DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES,
    execute_domain_operation as execute_domain_depth_operation,
)
from .runtime import SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC
from .standalone import SportsVenueEventOperationsStandaloneApp, standalone_manifest


PBC_KEY = "sports_venue_event_operations"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
    "event_topic": SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC,
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "command_venue_event",
            "configure_runtime",
            "set_parameter",
            "register_rule",
        )
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = ("query_workbench",)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES
STANDALONE_ROUTE_SPECS = (
    {"operation": "configure", "method": "POST", "path": "/app/sports-venue-event-operations/configure", "table": f"{PBC_KEY}_sports_venue_event_operations_runtime_parameter", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "register_defaults", "method": "POST", "path": "/app/sports-venue-event-operations/defaults", "table": f"{PBC_KEY}_sports_venue_event_operations_policy_rule", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "upsert_venue_layout", "method": "POST", "path": "/app/sports-venue-event-operations/venue-layouts", "table": f"{PBC_KEY}_venue", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "plan_zone_seating", "method": "POST", "path": "/app/sports-venue-event-operations/seat-plans", "table": f"{PBC_KEY}_ticketing_coordination", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "schedule_event", "method": "POST", "path": "/app/sports-venue-event-operations/events", "table": f"{PBC_KEY}_event_calendar", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "plan_ingress_egress", "method": "POST", "path": "/app/sports-venue-event-operations/ingress-egress", "table": f"{PBC_KEY}_ingress_plan", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "assign_staffing", "method": "POST", "path": "/app/sports-venue-event-operations/staffing", "table": f"{PBC_KEY}_staffing_plan", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "plan_concessions", "method": "POST", "path": "/app/sports-venue-event-operations/concessions", "table": f"{PBC_KEY}_concession_plan", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "coordinate_ticketing", "method": "POST", "path": "/app/sports-venue-event-operations/ticketing", "table": f"{PBC_KEY}_ticketing_coordination", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "issue_credential", "method": "POST", "path": "/app/sports-venue-event-operations/credentials", "table": f"{PBC_KEY}_credential", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "update_security_posture", "method": "POST", "path": "/app/sports-venue-event-operations/security", "table": f"{PBC_KEY}_security_plan", "operation_kind": "command", "wizard": "IncidentCommandWizard"},
    {"operation": "record_crowd_snapshot", "method": "POST", "path": "/app/sports-venue-event-operations/crowd", "table": f"{PBC_KEY}_crowd_observation", "operation_kind": "command", "wizard": "IncidentCommandWizard"},
    {"operation": "open_incident", "method": "POST", "path": "/app/sports-venue-event-operations/incidents", "table": f"{PBC_KEY}_incident", "operation_kind": "command", "wizard": "IncidentCommandWizard"},
    {"operation": "manage_weather_delay", "method": "POST", "path": "/app/sports-venue-event-operations/weather-delays", "table": f"{PBC_KEY}_weather_delay", "operation_kind": "command", "wizard": "WeatherDelayResponseWizard"},
    {"operation": "confirm_production_ready", "method": "POST", "path": "/app/sports-venue-event-operations/production", "table": f"{PBC_KEY}_production_readiness", "operation_kind": "command", "wizard": "BroadcastAndSponsorReadinessWizard"},
    {"operation": "activate_sponsor", "method": "POST", "path": "/app/sports-venue-event-operations/sponsors", "table": f"{PBC_KEY}_sponsor_activation", "operation_kind": "command", "wizard": "BroadcastAndSponsorReadinessWizard"},
    {"operation": "complete_turnover", "method": "POST", "path": "/app/sports-venue-event-operations/turnovers", "table": f"{PBC_KEY}_cleaning_turnover", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "log_accessibility_request", "method": "POST", "path": "/app/sports-venue-event-operations/accessibility", "table": f"{PBC_KEY}_accessibility_case", "operation_kind": "command", "wizard": "AccessibilityAssistanceWizard"},
    {"operation": "register_lost_and_found", "method": "POST", "path": "/app/sports-venue-event-operations/lost-found", "table": f"{PBC_KEY}_lost_found_item", "operation_kind": "command", "wizard": "IncidentCommandWizard"},
    {"operation": "start_emergency_operation", "method": "POST", "path": "/app/sports-venue-event-operations/emergency", "table": f"{PBC_KEY}_emergency_operation", "operation_kind": "command", "wizard": "IncidentCommandWizard"},
    {"operation": "record_attendance_and_revenue", "method": "POST", "path": "/app/sports-venue-event-operations/analytics", "table": f"{PBC_KEY}_revenue_attendance_snapshot", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "document_intake", "method": "POST", "path": "/app/sports-venue-event-operations/document-intake", "table": f"{PBC_KEY}_sports_venue_event_operations_governed_model", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "crud_mutation_plan", "method": "POST", "path": "/app/sports-venue-event-operations/crud-plan", "table": f"{PBC_KEY}_sports_venue_event_operations_control_assertion", "operation_kind": "command", "wizard": "EventCommandSetupWizard"},
    {"operation": "build_workbench", "method": "GET", "path": "/app/sports-venue-event-operations/workbench", "table": f"{PBC_KEY}_event_calendar", "operation_kind": "query", "wizard": "EventCommandSetupWizard"},
    {"operation": "get_event_snapshot", "method": "GET", "path": "/app/sports-venue-event-operations/events/{event_id}", "table": f"{PBC_KEY}_event_calendar", "operation_kind": "query", "wizard": "EventCommandSetupWizard"},
)


def _operation_contract(name, kind):
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES[:2] if kind == "command" else (),
        "read_tables": OWNED_TABLES[:2] if kind == "query" else (),
        "emitted_event": (
            "SportsVenueEventOperationsCreated",
            "SportsVenueEventOperationsUpdated",
            "SportsVenueEventOperationsApproved",
            "SportsVenueEventOperationsExceptionOpened",
        )[0]
        if kind == "command"
        else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class SportsVenueEventOperationsService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {
                "ok": plan["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": {
                    "operation": name,
                    "operation_kind": "command",
                    "owned_tables": plan.get("owned_tables", ()),
                    "read_tables": (),
                    "emitted_event": plan.get("emitted_event"),
                    "transaction_boundary": "owned_datastore_plus_outbox",
                },
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }
        contract = _operation_contract(name, "command")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def _query(self, name, payload):
        contract = _operation_contract(name, "query")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }


class SportsVenueEventOperationsStandaloneService:
    def __init__(self, tenant: str = "default") -> None:
        self.app = SportsVenueEventOperationsStandaloneApp(tenant=tenant)

    def configure(self, payload=None):
        return self.app.configure(payload)

    def register_defaults(self, payload=None):
        return self.app.register_defaults()

    def upsert_venue_layout(self, payload=None):
        return self.app.upsert_venue_layout(payload or {})

    def plan_zone_seating(self, payload=None):
        data = dict(payload or {})
        return self.app.plan_zone_seating(data["event_id"], data)

    def schedule_event(self, payload=None):
        return self.app.schedule_event(payload or {})

    def plan_ingress_egress(self, payload=None):
        data = dict(payload or {})
        return self.app.plan_ingress_egress(data["event_id"], data)

    def assign_staffing(self, payload=None):
        data = dict(payload or {})
        return self.app.assign_staffing(data["event_id"], data)

    def plan_concessions(self, payload=None):
        data = dict(payload or {})
        return self.app.plan_concessions(data["event_id"], data)

    def coordinate_ticketing(self, payload=None):
        data = dict(payload or {})
        return self.app.coordinate_ticketing(data["event_id"], data)

    def issue_credential(self, payload=None):
        data = dict(payload or {})
        return self.app.issue_credential(data["event_id"], data)

    def update_security_posture(self, payload=None):
        data = dict(payload or {})
        return self.app.update_security_posture(data["event_id"], data)

    def record_crowd_snapshot(self, payload=None):
        data = dict(payload or {})
        return self.app.record_crowd_snapshot(data["event_id"], data)

    def open_incident(self, payload=None):
        data = dict(payload or {})
        return self.app.open_incident(data["event_id"], data)

    def manage_weather_delay(self, payload=None):
        data = dict(payload or {})
        return self.app.manage_weather_delay(data["event_id"], data)

    def confirm_production_ready(self, payload=None):
        data = dict(payload or {})
        return self.app.confirm_production_ready(data["event_id"], data)

    def activate_sponsor(self, payload=None):
        data = dict(payload or {})
        return self.app.activate_sponsor(data["event_id"], data)

    def complete_turnover(self, payload=None):
        data = dict(payload or {})
        return self.app.complete_turnover(data["event_id"], data)

    def log_accessibility_request(self, payload=None):
        data = dict(payload or {})
        return self.app.log_accessibility_request(data["event_id"], data)

    def register_lost_and_found(self, payload=None):
        data = dict(payload or {})
        return self.app.register_lost_and_found(data["event_id"], data)

    def start_emergency_operation(self, payload=None):
        data = dict(payload or {})
        return self.app.start_emergency_operation(data["event_id"], data)

    def record_attendance_and_revenue(self, payload=None):
        data = dict(payload or {})
        return self.app.record_attendance_and_revenue(data["event_id"], data)

    def document_intake(self, payload=None):
        data = dict(payload or {})
        return self.app.document_intake(data.get("document"), data.get("instruction"))

    def crud_mutation_plan(self, payload=None):
        data = dict(payload or {})
        return self.app.crud_mutation_plan(data.get("action", "read"), data.get("table"), data.get("payload"))

    def build_workbench(self, payload=None):
        data = dict(payload or {})
        return self.app.build_workbench(data.get("tenant"), data.get("event_id"), data.get("role", "operator"))

    def get_event_snapshot(self, payload=None):
        data = dict(payload or {})
        return self.app.get_event_snapshot(data["event_id"])

    def close(self):
        self.app.close()


def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "SportsVenueEventOperationsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def standalone_service_manifest():
    manifest = standalone_manifest()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "SportsVenueEventOperationsStandaloneService",
        "service_methods": manifest["service_methods"],
        "event_contract": manifest["event_contract"],
        "event_topic": manifest["event_topic"],
        "docs": manifest["docs"],
        "allowed_backends": manifest["allowed_backends"],
        "side_effects": (),
    }


def standalone_service_operation_contracts():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": STANDALONE_ROUTE_SPECS,
        "side_effects": (),
    }


def smoke_test():
    service = SportsVenueEventOperationsService()
    command = getattr(service, COMMAND_OPERATIONS[0])({"tenant": "tenant-smoke"})
    query = getattr(service, QUERY_OPERATIONS[0])({"tenant": "tenant-smoke"})
    standalone = SportsVenueEventOperationsStandaloneService(tenant="tenant_smoke")
    try:
        scheduled = standalone.schedule_event({"event_id": "event_smoke", "venue_id": "venue_smoke"})
        workbench = standalone.build_workbench({"event_id": "event_smoke"})
        return {
            "ok": command["ok"] and query["ok"] and scheduled["ok"] and workbench["ok"] and service_operation_contracts()["ok"],
            "command": command,
            "query": query,
            "standalone": workbench,
            "side_effects": (),
        }
    finally:
        standalone.close()
