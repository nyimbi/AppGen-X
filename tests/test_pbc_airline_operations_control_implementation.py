from pyAppGen.pbcs.airline_operations_control.runtime import (
    airline_operations_control_build_workbench_view,
    airline_operations_control_command_flight_leg,
    airline_operations_control_empty_state,
    airline_operations_control_record_aircraft_rotation,
)
from pyAppGen.pbcs.airline_operations_control.services import AirlineOperationsControlService, service_operation_manifest
from pyAppGen.pbcs.airline_operations_control.ui import airline_operations_control_render_workbench


def test_rotation_workbench_flags_broken_turns_from_late_inbound():
    state = airline_operations_control_empty_state()
    inbound = airline_operations_control_command_flight_leg(
        state,
        {
            "tenant": "tenant-aoc",
            "id": "KQ100",
            "flight_number": "KQ100",
            "tail_number": "5Y-KQA",
            "origin": "NBO",
            "destination": "MBA",
            "scheduled_departure_at": "2026-05-28T08:00:00+00:00",
            "scheduled_arrival_at": "2026-05-28T09:00:00+00:00",
            "actual_off_block_at": "2026-05-28T08:18:00+00:00",
            "actual_on_block_at": "2026-05-28T09:24:00+00:00",
        },
    )
    outbound = airline_operations_control_command_flight_leg(
        inbound["state"],
        {
            "tenant": "tenant-aoc",
            "id": "KQ101",
            "flight_number": "KQ101",
            "tail_number": "5Y-KQA",
            "origin": "MBA",
            "destination": "KIS",
            "scheduled_departure_at": "2026-05-28T09:45:00+00:00",
            "scheduled_arrival_at": "2026-05-28T10:40:00+00:00",
            "aircraft_type": "narrowbody",
            "crew_change_required": True,
            "catering_required": True,
            "station_type": "outstation",
        },
    )
    rotation = airline_operations_control_record_aircraft_rotation(
        outbound["state"],
        {
            "tenant": "tenant-aoc",
            "rotation_id": "ROT-5Y-KQA",
            "tail_number": "5Y-KQA",
            "operating_day": "2026-05-28",
            "leg_ids": ("KQ100", "KQ101"),
            "spare_tail_candidates": ("5Y-KQX",),
        },
    )

    workbench = airline_operations_control_build_workbench_view(rotation["state"], tenant="tenant-aoc")

    assert inbound["authoritative_status"] == "arrived"
    assert workbench["workbench"]["metrics"]["broken_turn_count"] == 1
    assert workbench["workbench"]["tail_graphs"][0]["recovery_outlook"] == "degrading"
    assert workbench["workbench"]["turn_watchlist"][0]["outbound_leg_id"] == "KQ101"
    assert workbench["workbench"]["turn_watchlist"][0]["status"] == "impossible"
    assert workbench["workbench"]["attention_queue"][0]["reason"] == "impossible"


def test_leg_timeline_branches_cover_diversion_and_return_to_gate():
    state = airline_operations_control_empty_state()
    diverted = airline_operations_control_command_flight_leg(
        state,
        {
            "tenant": "tenant-aoc",
            "id": "KQ200",
            "flight_number": "KQ200",
            "tail_number": "5Y-KQB",
            "origin": "NBO",
            "destination": "ZNZ",
            "scheduled_departure_at": "2026-05-28T11:00:00+00:00",
            "scheduled_arrival_at": "2026-05-28T12:15:00+00:00",
            "actual_takeoff_at": "2026-05-28T11:22:00+00:00",
            "diverted_at": "2026-05-28T11:58:00+00:00",
            "diverted_to": "DAR",
        },
    )
    returned = airline_operations_control_command_flight_leg(
        diverted["state"],
        {
            "tenant": "tenant-aoc",
            "id": "KQ201",
            "flight_number": "KQ201",
            "tail_number": "5Y-KQB",
            "origin": "DAR",
            "destination": "NBO",
            "scheduled_departure_at": "2026-05-28T13:00:00+00:00",
            "scheduled_arrival_at": "2026-05-28T14:00:00+00:00",
            "actual_off_block_at": "2026-05-28T13:10:00+00:00",
            "returned_to_gate_at": "2026-05-28T13:24:00+00:00",
        },
    )

    assert diverted["record"]["branch"] == "diverted"
    assert diverted["record"]["completion_airport"] == "DAR"
    assert returned["record"]["branch"] == "returned_to_gate"
    assert returned["record"]["authoritative_status"] == "returned_to_gate"
    assert any(item["milestone"] == "returned_to_gate_at" for item in returned["timeline"])


def test_service_and_ui_project_scenario_payloads_into_workbench():
    service = AirlineOperationsControlService()
    workbench = service.query_workbench(
        {
            "tenant": "tenant-aoc",
            "flight_legs": (
                {
                    "tenant": "tenant-aoc",
                    "id": "KQ300",
                    "flight_number": "KQ300",
                    "tail_number": "5Y-KQC",
                    "origin": "NBO",
                    "destination": "KGL",
                    "scheduled_departure_at": "2026-05-28T15:00:00+00:00",
                    "scheduled_arrival_at": "2026-05-28T16:20:00+00:00",
                    "actual_off_block_at": "2026-05-28T15:05:00+00:00",
                    "actual_on_block_at": "2026-05-28T16:30:00+00:00",
                },
                {
                    "tenant": "tenant-aoc",
                    "id": "KQ301",
                    "flight_number": "KQ301",
                    "tail_number": "5Y-KQC",
                    "origin": "KGL",
                    "destination": "NBO",
                    "scheduled_departure_at": "2026-05-28T17:30:00+00:00",
                    "scheduled_arrival_at": "2026-05-28T18:30:00+00:00",
                    "aircraft_type": "regional",
                },
            ),
            "aircraft_rotations": (
                {
                    "tenant": "tenant-aoc",
                    "rotation_id": "ROT-5Y-KQC",
                    "tail_number": "5Y-KQC",
                    "leg_ids": ("KQ300", "KQ301"),
                },
            ),
        }
    )
    rendered = airline_operations_control_render_workbench(
        tenant="tenant-aoc",
        flight_legs=workbench["workbench"]["workbench"]["legs"],
        aircraft_rotations=(
            {
                "tenant": "tenant-aoc",
                "rotation_id": "ROT-5Y-KQC",
                "tail_number": "5Y-KQC",
                "leg_ids": ("KQ300", "KQ301"),
            },
        ),
    )

    assert workbench["workbench"]["workbench"]["metrics"]["flight_leg_count"] == 2
    assert workbench["workbench"]["workbench"]["metrics"]["broken_turn_count"] == 0
    assert rendered["decision_support_panels"] == (
        "canonical_leg_timelines",
        "tail_rotation_continuity",
        "minimum_turn_watchlist",
    )
    assert rendered["turn_watchlist"] == ()


def test_service_contract_and_rotation_command_expose_executable_slice():
    service = AirlineOperationsControlService()
    leg_payloads = (
        {
            "tenant": "tenant-aoc",
            "id": "KQ400",
            "flight_number": "KQ400",
            "tail_number": "5Y-KQD",
            "origin": "NBO",
            "destination": "JRO",
            "scheduled_departure_at": "2026-05-28T19:00:00+00:00",
            "scheduled_arrival_at": "2026-05-28T20:00:00+00:00",
            "actual_on_block_at": "2026-05-28T20:02:00+00:00",
        },
        {
            "tenant": "tenant-aoc",
            "id": "KQ401",
            "flight_number": "KQ401",
            "tail_number": "5Y-KQD",
            "origin": "JRO",
            "destination": "NBO",
            "scheduled_departure_at": "2026-05-28T20:50:00+00:00",
            "scheduled_arrival_at": "2026-05-28T21:50:00+00:00",
            "aircraft_type": "regional",
            "minimum_turn_minutes": 30,
        },
    )

    rotation = service.record_aircraft_rotation(
        {
            "tenant": "tenant-aoc",
            "rotation_id": "ROT-5Y-KQD",
            "tail_number": "5Y-KQD",
            "leg_ids": ("KQ400", "KQ401"),
            "flight_legs": leg_payloads,
        }
    )

    assert "record_aircraft_rotation" in service_operation_manifest()["command_operations"]
    assert rotation["ok"] is True
    assert rotation["rotation_graph"]["rotation_id"] == "ROT-5Y-KQD"
    assert rotation["rotation_graph"]["broken_turn_count"] == 0
    assert rotation["operation_contract"]["emitted_event"] == "AirlineOperationsControlUpdated"
