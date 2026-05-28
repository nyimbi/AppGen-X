from pyAppGen.pbcs.airport_operations_management.agent import (
    gate_assignment_decision_rationale,
)
from pyAppGen.pbcs.airport_operations_management.compatibility import (
    build_gate_assignment_compatibility_matrix,
)
from pyAppGen.pbcs.airport_operations_management.runtime import (
    airport_operations_management_build_release_evidence,
    airport_operations_management_build_workbench_view,
    airport_operations_management_command_gate_assignment,
    airport_operations_management_empty_state,
    airport_operations_management_query_workbench,
)
from pyAppGen.pbcs.airport_operations_management.services import (
    AirportOperationsManagementService,
)
from pyAppGen.pbcs.airport_operations_management.ui import (
    airport_operations_management_render_workbench,
    airport_operations_management_ui_contract,
)


def _stand(
    stand_code,
    *,
    gate_code=None,
    stand_type="contact",
    supported_aircraft_families=("narrowbody",),
    max_wingspan_code="C",
    international_capable=False,
    bussing_supported=False,
    hydrant_fuel=True,
    ground_power=True,
    preconditioned_air=True,
    adjacent_shadow_stands=(),
    active=True,
):
    return {
        "stand_code": stand_code,
        "gate_code": gate_code or stand_code,
        "stand_type": stand_type,
        "supported_aircraft_families": supported_aircraft_families,
        "max_wingspan_code": max_wingspan_code,
        "international_capable": international_capable,
        "bussing_supported": bussing_supported,
        "hydrant_fuel": hydrant_fuel,
        "ground_power": ground_power,
        "preconditioned_air": preconditioned_air,
        "adjacent_shadow_stands": adjacent_shadow_stands,
        "active": active,
    }


def test_gate_assignment_compatibility_matrix_captures_operational_constraints():
    stands = (
        _stand("A1", supported_aircraft_families=("narrowbody",), max_wingspan_code="C"),
        _stand(
            "B7",
            supported_aircraft_families=("widebody",),
            max_wingspan_code="E",
            international_capable=True,
            adjacent_shadow_stands=("B8",),
        ),
        _stand(
            "C12",
            supported_aircraft_families=("widebody",),
            max_wingspan_code="E",
            international_capable=True,
        ),
    )
    matrix = build_gate_assignment_compatibility_matrix(
        {
            "flight_number": "AX512",
            "aircraft_family": "widebody",
            "wingspan_code": "E",
            "operation_type": "international",
            "requires_hydrant_fuel": True,
            "requires_ground_power": True,
            "requires_preconditioned_air": True,
            "requires_contact_stand": True,
        },
        stands=stands,
        occupied_stands=("B8",),
    )

    assert matrix["recommended_option"]["stand_code"] == "C12"
    assert matrix["summary"] == {"usable": 1, "conditional": 0, "blocked": 2}

    assessments = {item["stand_code"]: item for item in matrix["assessments"]}
    assert "aircraft_family_not_supported" in assessments["A1"]["reason_codes"]
    assert "international_arrival_requires_border_capable_stand" in assessments["A1"]["reason_codes"]
    assert "adjacent_shadow_conflict" in assessments["B7"]["reason_codes"]


def test_command_gate_assignment_rejects_remote_stand_without_required_support():
    result = airport_operations_management_command_gate_assignment(
        airport_operations_management_empty_state(),
        {
            "tenant": "station-1",
            "flight_number": "AX102",
            "aircraft_family": "narrowbody",
            "wingspan_code": "C",
            "requires_contact_stand": True,
            "candidate_stands": (
                _stand(
                    "R2",
                    stand_type="remote",
                    supported_aircraft_families=("narrowbody",),
                    max_wingspan_code="C",
                    bussing_supported=False,
                    hydrant_fuel=False,
                    preconditioned_air=False,
                ),
            ),
        },
    )

    assert result["ok"] is False
    assert result["reason"] == "no_compatible_stand"
    assert result["record"]["status"] == "rejected"
    assert result["record"]["compatibility_summary"] == {
        "usable": 0,
        "conditional": 0,
        "blocked": 1,
    }
    assert (
        result["state"]["outbox"][-1]["event_type"]
        == "AirportOperationsManagementExceptionOpened"
    )
    reason_codes = result["record"]["compatibility_matrix"][0]["reason_codes"]
    assert "contact_stand_required" in reason_codes
    assert "remote_stand_missing_bussing_support" in reason_codes


def test_decision_support_surfaces_explain_selected_stand_and_workbench_queue():
    stands = (
        _stand("A4", gate_code="A4", supported_aircraft_families=("narrowbody",)),
        _stand(
            "R5",
            gate_code="R5",
            stand_type="remote",
            supported_aircraft_families=("narrowbody",),
            bussing_supported=True,
            hydrant_fuel=False,
            preconditioned_air=False,
        ),
    )
    request = {
        "tenant": "station-2",
        "flight_number": "AX220",
        "aircraft_family": "narrowbody",
        "wingspan_code": "C",
        "operation_type": "domestic",
        "candidate_stands": stands,
    }

    service = AirportOperationsManagementService()
    plan = service.evaluate_gate_assignment_compatibility(request)
    assert plan["ok"] is True
    assert plan["compatibility_plan"]["recommended_option"]["stand_code"] == "A4"

    rationale = gate_assignment_decision_rationale(request, candidate_stands=stands)
    assert "A4" in rationale["summary"]

    created = airport_operations_management_command_gate_assignment(
        airport_operations_management_empty_state(),
        request,
    )
    workbench = airport_operations_management_query_workbench(
        created["state"], {"tenant": "station-2"}
    )
    assert workbench["decision_queue"][0]["recommended_stand"] == "A4"

    ui_contract = airport_operations_management_ui_contract()
    assert "stand_compatibility_matrix" in ui_contract["full_capability_surface"][
        "decision_support_panels"
    ]
    rendered = airport_operations_management_render_workbench()
    assert rendered["decision_support"]["legend"] == ("usable", "conditional", "blocked")
    assert "compatibility_columns" in airport_operations_management_build_workbench_view()[
        "decision_support"
    ]

    release_evidence = airport_operations_management_build_release_evidence()
    assert any(check["id"] == "gate_stand_compatibility_execution" and check["ok"] for check in release_evidence["checks"])
    assert release_evidence["generated_artifacts"]["decision_support"]["operation"] == "evaluate_gate_assignment_compatibility"
