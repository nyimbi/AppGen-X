"""Standalone one-PBC application surface for airline_operations_control."""

from __future__ import annotations

from . import routes
from . import ui
from .runtime import AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION
from .runtime import AIRLINE_OPERATIONS_CONTROL_DEFAULT_PARAMETERS
from .runtime import AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE
from .services import AirlineOperationsControlService


DEFAULT_CONFIGURATION = AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION
DEFAULT_PARAMETERS = AIRLINE_OPERATIONS_CONTROL_DEFAULT_PARAMETERS
DEFAULT_RULE = AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE


def standalone_app_manifest() -> dict:
    service_manifest = AirlineOperationsControlService().query_service_contract({})["result"]
    return {
        "ok": True,
        "pbc": "airline_operations_control",
        "app": ui.airline_operations_control_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service_manifest,
        "side_effects": (),
    }


class AirlineOperationsControlStandaloneApp:
    """Package-local standalone app that owns the airline OCC runtime state."""

    def __init__(self, state: dict | None = None):
        self.service = AirlineOperationsControlService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        self.dispatch("POST", "/api/pbc/airline_operations_control/runtime/configuration", {"configuration": DEFAULT_CONFIGURATION})
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch("POST", "/api/pbc/airline_operations_control/runtime/parameters", {"name": name, "value": value})
        self.dispatch("POST", "/api/pbc/airline_operations_control/runtime/rules", {"rule": {**DEFAULT_RULE, "tenant": tenant}})
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/events/inbox",
            {
                "envelope": {
                    "event_type": "PolicyChanged",
                    "event_id": f"policy-{tenant}",
                    "payload": {"tenant": tenant, "policy_id": "daily-occ", "scope": "network_control"},
                }
            },
        )
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/flight-legs",
            {
                "flight_leg": {
                    "tenant": tenant,
                    "id": "KQ600",
                    "flight_number": "KQ600",
                    "tail_number": "5Y-KZA",
                    "origin": "NBO",
                    "destination": "MBA",
                    "scheduled_departure_at": "2026-05-30T06:00:00+00:00",
                    "scheduled_arrival_at": "2026-05-30T07:00:00+00:00",
                    "actual_off_block_at": "2026-05-30T06:18:00+00:00",
                    "actual_on_block_at": "2026-05-30T07:24:00+00:00",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/flight-legs",
            {
                "flight_leg": {
                    "tenant": tenant,
                    "id": "KQ601",
                    "flight_number": "KQ601",
                    "tail_number": "5Y-KZA",
                    "origin": "MBA",
                    "destination": "KIS",
                    "scheduled_departure_at": "2026-05-30T07:45:00+00:00",
                    "scheduled_arrival_at": "2026-05-30T08:40:00+00:00",
                    "aircraft_type": "narrowbody",
                    "crew_change_required": True,
                    "catering_required": True,
                    "station_type": "outstation",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/aircraft-rotations",
            {
                "rotation": {
                    "tenant": tenant,
                    "rotation_id": "ROT-5Y-KZA",
                    "tail_number": "5Y-KZA",
                    "operating_day": "2026-05-30",
                    "leg_ids": ("KQ600", "KQ601"),
                    "spare_tail_candidates": ("5Y-KZX", "5Y-KZY"),
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/crew-pairings",
            {
                "crew_pairing": {
                    "tenant": tenant,
                    "crew_pairing_id": "CP-600",
                    "remaining_duty_minutes": 52,
                    "legality_state": "legal",
                    "reserve_activation_required": True,
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/disruption-events",
            {
                "disruption_event": {
                    "tenant": tenant,
                    "disruption_event_id": "DIS-600",
                    "event_type": "weather",
                    "severity": "high",
                    "affected_leg_ids": ("KQ601",),
                    "source_lineage": ("metar", "dispatcher_note"),
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/reaccommodation-plans",
            {
                "reaccommodation_plan": {
                    "tenant": tenant,
                    "reaccommodation_plan_id": "REAC-600",
                    "passenger_count": 34,
                    "manual_review_required": True,
                    "blocked_reason": "special_assistance_boundary",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/operations-decisions",
            {
                "operations_decision": {
                    "tenant": tenant,
                    "operations_decision_id": "DEC-600",
                    "decision_type": "tail_swap",
                    "selected_action": "swap_tail",
                    "alternatives": ("delay", "cancel", "ferry"),
                    "approval_state": "approved",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/delay-codes",
            {
                "delay_code": {
                    "tenant": tenant,
                    "delay_code_id": "DLY-600",
                    "primary_code": "93",
                    "contributing_codes": ("11", "41"),
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/airline_operations_control/workflows/recovery",
            {
                "workflow": {
                    "tenant": tenant,
                    "workflow_id": "WF-600",
                    "focus_leg_ids": ("KQ601",),
                    "linked_disruption_id": "DIS-600",
                    "linked_rotation_id": "ROT-5Y-KZA",
                    "selected_decision_id": "DEC-600",
                }
            },
        )
        return {"ok": True, "tenant": tenant, "workbench": self.render_workbench(tenant=tenant), "side_effects": ()}

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(sorted(set(ui.airline_operations_control_ui_contract()["action_permissions"].values())))
        return ui.airline_operations_control_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    app = AirlineOperationsControlStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["cards"][0]["value"] >= 1 and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }
