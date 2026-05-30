"""Service layer for the hospitality_property_operations PBC."""

from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_EMITTED_EVENTS, workflow_catalog
from .models import HospitalityPropertyOperationsStandaloneStore, OWNED_TABLES, standalone_model_contract

PBC_KEY = "hospitality_property_operations"
EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": "pbc.hospitality_property_operations.events",
    "inbox_topic": "pbc.hospitality_property_operations.inbox",
    "outbox_table": "hospitality_property_operations_appgen_outbox_event",
    "inbox_table": "hospitality_property_operations_appgen_inbox_event",
    "dead_letter_table": "hospitality_property_operations_appgen_dead_letter_event",
    "retry_policy": {"name": "hospitality_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": "hospitality_property_operations_appgen_inbox_event"},
}

OPERATION_CONTRACTS = (
    {
        "operation": "configure_runtime",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/hospitality_property_operations/runtime/configure",
        "permission": "hospitality_property_operations.admin",
        "owned_tables": (),
        "read_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_room_inventory",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/hospitality_property_operations/room-inventorys",
        "permission": "hospitality_property_operations.update",
        "owned_tables": ("hospitality_property_operations_room_inventory",),
        "read_tables": (),
        "emitted_event": DOMAIN_EMITTED_EVENTS[0],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_reservation",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/hospitality_property_operations/reservations",
        "permission": "hospitality_property_operations.create",
        "owned_tables": ("hospitality_property_operations_reservation",),
        "read_tables": (),
        "emitted_event": DOMAIN_EMITTED_EVENTS[1],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_guest_stay",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/hospitality_property_operations/guest-stays",
        "permission": "hospitality_property_operations.update",
        "owned_tables": ("hospitality_property_operations_guest_stay", "hospitality_property_operations_room_inventory"),
        "read_tables": (),
        "emitted_event": DOMAIN_EMITTED_EVENTS[2],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_housekeeping_task",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/hospitality_property_operations/housekeeping-tasks",
        "permission": "hospitality_property_operations.update",
        "owned_tables": ("hospitality_property_operations_housekeeping_task",),
        "read_tables": (),
        "emitted_event": DOMAIN_EMITTED_EVENTS[3],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_guest_request",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/hospitality_property_operations/guest-requests",
        "permission": "hospitality_property_operations.update",
        "owned_tables": ("hospitality_property_operations_guest_request",),
        "read_tables": (),
        "emitted_event": DOMAIN_EMITTED_EVENTS[4],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/hospitality_property_operations/workbench",
        "permission": "hospitality_property_operations.read",
        "owned_tables": (),
        "read_tables": (
            "hospitality_property_operations_room_inventory",
            "hospitality_property_operations_reservation",
            "hospitality_property_operations_guest_stay",
            "hospitality_property_operations_housekeeping_task",
            "hospitality_property_operations_guest_request",
            "hospitality_property_operations_occupancy_snapshot",
        ),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
)

STANDALONE_OPERATION_CONTRACTS = (
    {
        "operation": "upsert_room_inventory",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/rooms",
        "handler": "upsert_room_inventory",
        "permission": "hospitality_property_operations.update",
        "table": "hospitality_property_operations_room_inventory",
        "form": "RoomReadinessForm",
        "wizard": "ArrivalTurnaroundWizard",
    },
    {
        "operation": "create_reservation",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/reservations",
        "handler": "create_reservation",
        "permission": "hospitality_property_operations.create",
        "table": "hospitality_property_operations_reservation",
        "form": "ReservationIntakeForm",
        "wizard": "ArrivalTurnaroundWizard",
    },
    {
        "operation": "check_in_guest",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/stays/check-in",
        "handler": "check_in_guest",
        "permission": "hospitality_property_operations.update",
        "table": "hospitality_property_operations_guest_stay",
        "form": "CheckInControl",
        "wizard": "ArrivalTurnaroundWizard",
    },
    {
        "operation": "check_out_guest",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/stays/check-out",
        "handler": "check_out_guest",
        "permission": "hospitality_property_operations.update",
        "table": "hospitality_property_operations_guest_stay",
        "form": "DepartureControl",
        "wizard": "DepartureRecoveryWizard",
    },
    {
        "operation": "move_guest_stay",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/stays/move",
        "handler": "move_guest_stay",
        "permission": "hospitality_property_operations.approve",
        "table": "hospitality_property_operations_guest_stay",
        "form": "RoomMoveForm",
        "wizard": "ServiceRecoveryWizard",
    },
    {
        "operation": "schedule_housekeeping_task",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/housekeeping-tasks",
        "handler": "schedule_housekeeping_task",
        "permission": "hospitality_property_operations.update",
        "table": "hospitality_property_operations_housekeeping_task",
        "form": "HousekeepingDispatchForm",
        "wizard": "ArrivalTurnaroundWizard",
    },
    {
        "operation": "complete_housekeeping_task",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/housekeeping-tasks/complete",
        "handler": "complete_housekeeping_task",
        "permission": "hospitality_property_operations.update",
        "table": "hospitality_property_operations_housekeeping_task",
        "form": "InspectionReleaseControl",
        "wizard": "ArrivalTurnaroundWizard",
    },
    {
        "operation": "record_guest_request",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/guest-requests",
        "handler": "record_guest_request",
        "permission": "hospitality_property_operations.update",
        "table": "hospitality_property_operations_guest_request",
        "form": "GuestRequestForm",
        "wizard": "ServiceRecoveryWizard",
    },
    {
        "operation": "resolve_guest_request",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/guest-requests/resolve",
        "handler": "resolve_guest_request",
        "permission": "hospitality_property_operations.update",
        "table": "hospitality_property_operations_guest_request",
        "form": "GuestRequestResolutionControl",
        "wizard": "ServiceRecoveryWizard",
    },
    {
        "operation": "capture_occupancy_snapshot",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/occupancy-snapshots",
        "handler": "capture_occupancy_snapshot",
        "permission": "hospitality_property_operations.read",
        "table": "hospitality_property_operations_occupancy_snapshot",
        "form": "OccupancySnapshotControl",
        "wizard": "RevenueControlWizard",
    },
    {
        "operation": "publish_rate_plan",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/hospitality-property-operations/rate-plans",
        "handler": "publish_rate_plan",
        "permission": "hospitality_property_operations.approve",
        "table": "hospitality_property_operations_rate_plan",
        "form": "RateFenceForm",
        "wizard": "RevenueControlWizard",
    },
    {
        "operation": "build_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/hospitality-property-operations/workbench",
        "handler": "build_workbench",
        "permission": "hospitality_property_operations.read",
        "table": "hospitality_property_operations_occupancy_snapshot",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "get_room_detail",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/hospitality-property-operations/rooms/detail",
        "handler": "get_room_detail",
        "permission": "hospitality_property_operations.read",
        "table": "hospitality_property_operations_room_inventory",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "build_shift_handover",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/hospitality-property-operations/shift-handover",
        "handler": "build_shift_handover",
        "permission": "hospitality_property_operations.read",
        "table": "hospitality_property_operations_room_inventory",
        "form": None,
        "wizard": None,
    },
)


def _contract_lookup(operation_name: str) -> dict | None:
    return next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)


def service_operation_contracts() -> dict:
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["emitted_event"] for item in command_contracts if item["operation"] != "configure_runtime")
        and all(item["emitted_event"] is None for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def standalone_service_operation_contracts() -> dict:
    return {
        "ok": bool(STANDALONE_OPERATION_CONTRACTS),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in STANDALONE_OPERATION_CONTRACTS),
        "contracts": STANDALONE_OPERATION_CONTRACTS,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    contract = _contract_lookup(operation_name)
    if not contract:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "transaction_boundary": contract["transaction_boundary"],
        "payload_keys": tuple(sorted(supplied)),
        "event_contract": contract["event_contract"],
        "side_effects": (),
    }


class HospitalityPropertyOperationsService:
    """Side-effect-free generated contract facade used by source-package audits."""

    def _execute(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        result = {
            "ok": plan["ok"],
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": plan["operation_kind"],
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if plan["operation_kind"] == "command":
            event_type = plan.get("emitted_event")
            result.update(
                {
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (event_type,) if event_type else (),
                }
            )
        else:
            result.update({"read_only": True, "outbox_table": None, "emits": ()})
        return result

    def configure_runtime(self, payload: dict | None = None) -> dict:
        return self._execute("configure_runtime", payload or {})

    def command_room_inventory(self, payload: dict | None = None) -> dict:
        return self._execute("command_room_inventory", payload or {})

    def command_reservation(self, payload: dict | None = None) -> dict:
        return self._execute("command_reservation", payload or {})

    def command_guest_stay(self, payload: dict | None = None) -> dict:
        return self._execute("command_guest_stay", payload or {})

    def command_housekeeping_task(self, payload: dict | None = None) -> dict:
        return self._execute("command_housekeeping_task", payload or {})

    def command_guest_request(self, payload: dict | None = None) -> dict:
        return self._execute("command_guest_request", payload or {})

    def query_workbench(self, payload: dict | None = None) -> dict:
        return self._execute("query_workbench", payload or {})


class HospitalityPropertyOperationsStandaloneService:
    """Executable sqlite-backed one-PBC app service."""

    def __init__(self, store: HospitalityPropertyOperationsStandaloneStore | None = None) -> None:
        self.store = store or HospitalityPropertyOperationsStandaloneStore()
        self._owns_store = store is None

    def close(self) -> None:
        if self._owns_store:
            self.store.close()

    def upsert_room_inventory(self, payload: dict | None = None) -> dict:
        return self.store.upsert_room_inventory(payload or {})

    def create_reservation(self, payload: dict | None = None) -> dict:
        return self.store.create_reservation(payload or {})

    def check_in_guest(self, payload: dict | None = None) -> dict:
        return self.store.check_in_guest(payload or {})

    def move_guest_stay(self, payload: dict | None = None) -> dict:
        return self.store.move_guest_stay(payload or {})

    def check_out_guest(self, payload: dict | None = None) -> dict:
        return self.store.check_out_guest(payload or {})

    def schedule_housekeeping_task(self, payload: dict | None = None) -> dict:
        return self.store.schedule_housekeeping_task(payload or {})

    def complete_housekeeping_task(self, payload: dict | None = None) -> dict:
        return self.store.complete_housekeeping_task(payload or {})

    def record_guest_request(self, payload: dict | None = None) -> dict:
        return self.store.record_guest_request(payload or {})

    def resolve_guest_request(self, payload: dict | None = None) -> dict:
        return self.store.resolve_guest_request(payload or {})

    def capture_occupancy_snapshot(self, payload: dict | None = None) -> dict:
        return self.store.capture_occupancy_snapshot(payload or {})

    def publish_rate_plan(self, payload: dict | None = None) -> dict:
        return self.store.publish_rate_plan(payload or {})

    def build_workbench(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self.store.build_workbench(supplied.get("tenant", "default"), supplied.get("shift_code", "day"))

    def get_room_detail(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self.store.get_room_detail(supplied["room_id"])

    def build_shift_handover(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self.store.build_shift_handover(supplied.get("tenant", "default"), supplied.get("shift_code", "day"))

    def run_arrival_turnaround_workflow(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        room = self.upsert_room_inventory(supplied["room"])
        reservation = self.create_reservation(supplied["reservation"])
        housekeeping = self.schedule_housekeeping_task(supplied["housekeeping_task"])
        released = self.complete_housekeeping_task({"task_id": housekeeping["task"]["task_id"], "inspector": supplied.get("inspector", "supervisor")})
        stay = self.check_in_guest({"reservation_id": reservation["reservation"]["reservation_id"], "room_id": room["room"]["room_id"]})
        return {
            "ok": room["ok"] and reservation["ok"] and housekeeping["ok"] and released["ok"] and stay["ok"],
            "workflow": "arrival_turnaround",
            "steps": (room, reservation, housekeeping, released, stay),
            "side_effects": (),
        }

    def run_service_recovery_workflow(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        request = self.record_guest_request(supplied["guest_request"])
        move = None
        if supplied.get("move_guest"):
            move = self.move_guest_stay(supplied["move_guest"])
        resolved = self.resolve_guest_request({"request_id": request["request"]["request_id"], "guest_confirmed": supplied.get("guest_confirmed", True)})
        ok = request["ok"] and resolved["ok"] and (move is None or move["ok"])
        return {"ok": ok, "workflow": "service_recovery", "request": request, "move": move, "resolved": resolved, "side_effects": ()}

    def run_revenue_control_workflow(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        snapshot = self.capture_occupancy_snapshot(supplied.get("snapshot"))
        rate_plan = self.publish_rate_plan(supplied.get("rate_plan"))
        handover = self.build_shift_handover({"tenant": supplied.get("tenant", "default"), "shift_code": supplied.get("shift_code", "day")})
        return {
            "ok": snapshot["ok"] and rate_plan["ok"] and handover["ok"],
            "workflow": "revenue_control",
            "snapshot": snapshot,
            "rate_plan": rate_plan,
            "handover": handover,
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    manifest = service_operation_contracts()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "service_class": "HospitalityPropertyOperationsService",
        "operations": manifest["operations"],
        "command_operations": manifest["command_operations"],
        "query_operations": manifest["query_operations"],
        "operation_contracts": manifest["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = service_operation_manifest()
    service = HospitalityPropertyOperationsService()
    operation = manifest["operations"][1]
    result = getattr(service, operation)({"tenant": "tenant_smoke"})
    return {
        "ok": manifest["ok"] and result["ok"] and result["operation_contract"]["ok"],
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }


def standalone_smoke_test() -> dict:
    service = HospitalityPropertyOperationsStandaloneService()
    try:
        room = service.upsert_room_inventory({"room_id": "rm_smoke", "tenant": "tenant_smoke", "room_number": "500"})
        reservation = service.create_reservation(
            {
                "reservation_id": "res_smoke",
                "tenant": "tenant_smoke",
                "reservation_code": "RSV-SMOKE",
                "guest_name": "Standalone Guest",
                "arrival_date": "2026-05-30",
                "departure_date": "2026-05-31",
                "assigned_room_id": "rm_smoke",
            }
        )
        stay = service.check_in_guest({"reservation_id": "res_smoke", "room_id": "rm_smoke"})
        workbench = service.build_workbench({"tenant": "tenant_smoke"})
        return {
            "ok": room["ok"] and reservation["ok"] and stay["ok"] and workbench["ok"],
            "room": room,
            "reservation": reservation,
            "stay": stay,
            "workbench": workbench,
            "model_contract": standalone_model_contract(),
            "workflows": workflow_catalog(),
            "owned_tables": OWNED_TABLES,
            "side_effects": (),
        }
    finally:
        service.close()
