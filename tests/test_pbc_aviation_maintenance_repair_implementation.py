from pyAppGen.pbcs.aviation_maintenance_repair import (
    aviation_maintenance_repair_assess_release_to_service,
    aviation_maintenance_repair_build_release_evidence,
    aviation_maintenance_repair_build_service_contract,
    aviation_maintenance_repair_build_workbench_view,
    aviation_maintenance_repair_empty_state,
    aviation_maintenance_repair_query_workbench,
    build_release_to_service_pack,
    evaluate_component_installation,
    evaluate_work_card_closeout,
)
from pyAppGen.pbcs.aviation_maintenance_repair.agent import (
    chatbot_interface_contract,
    document_instruction_plan,
)
from pyAppGen.pbcs.aviation_maintenance_repair.services import (
    AviationMaintenanceRepairService,
    service_operation_manifest,
)
from pyAppGen.pbcs.aviation_maintenance_repair.ui import (
    aviation_maintenance_repair_render_workbench,
    aviation_maintenance_repair_ui_contract,
)


def _release_payload(**overrides):
    payload = {
        "release_id": "RTS-001",
        "as_of": "2026-05-28",
        "aircraft": {"tail_number": "5Y-AXA", "aircraft_type": "B737", "fleet_subtype": "B737-800"},
        "work_cards": (
            {
                "work_card_id": "WC-001",
                "status": "closed",
                "task_family": "line",
                "aircraft_type": "B737",
                "required_signoff_roles": ("performer", "duplicate_inspector"),
                "duplicate_inspection_required": True,
                "signoffs": (
                    {"role": "performer", "technician_id": "tech-a"},
                    {"role": "duplicate_inspector", "technician_id": "tech-b"},
                ),
                "controlled_tools": (
                    {"tool_id": "torque-1", "returned": True, "calibration_due": "2026-12-31"},
                ),
                "consumables": (
                    {"batch_id": "sealant-1", "expiry": "2026-12-31"},
                ),
            },
        ),
        "components": (
            {
                "component_id": "COMP-001",
                "remaining_cycles": 250,
                "remaining_hours": 750,
                "release_certificate": "ARC-001",
                "effectivity_aircraft_types": ("B737",),
            },
        ),
        "airworthiness_directives": ({"ad_id": "AD-001", "status": "complied"},),
        "deferred_defects": ({"defect_id": "MEL-001", "status": "deferred", "expiry_date": "2026-06-15"},),
        "technician_authorizations": (
            {"technician_id": "tech-a", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"},
            {"technician_id": "tech-b", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"},
        ),
        "certifier": {"technician_id": "cert-1", "release_authorization": True},
    }
    payload.update(overrides)
    return payload


def test_release_to_service_pack_accepts_complete_airworthy_evidence():
    pack = build_release_to_service_pack(_release_payload())

    assert pack["ok"] is True
    assert pack["status"] == "release_ready"
    assert pack["blockers"] == ()
    assert set(pack["passed_checks"]) >= {
        "work_cards_closed",
        "duplicate_inspections_complete",
        "technicians_authorized",
        "controlled_tools_valid",
        "consumables_within_life",
        "components_airworthy",
        "deferred_defects_within_limits",
        "airworthiness_directives_complied",
        "human_certifier_present",
    }

    runtime = aviation_maintenance_repair_assess_release_to_service(
        aviation_maintenance_repair_empty_state(),
        _release_payload(),
    )
    assert runtime["ok"] is True
    assert runtime["state"]["outbox"][-1]["event_type"] == "AviationMaintenanceRepairApproved"

    workbench = aviation_maintenance_repair_query_workbench(runtime["state"], {"tail_number": "5Y-AXA"})
    assert workbench["release_queue"][0]["status"] == "release_ready"


def test_release_to_service_pack_blocks_safety_and_authorization_gaps():
    bad_card = {
        **_release_payload()["work_cards"][0],
        "signoffs": ({"role": "performer", "technician_id": "tech-a"}, {"role": "duplicate_inspector", "technician_id": "tech-a"}),
        "controlled_tools": ({"tool_id": "torque-expired", "returned": False, "calibration_due": "2026-01-01"},),
        "consumables": ({"batch_id": "sealant-expired", "expiry": "2026-01-01", "mix_life_expired": True},),
    }
    bad_component = {
        "component_id": "COMP-BLOCK",
        "remaining_cycles": 0,
        "remaining_hours": 0,
        "quarantine_state": "active",
        "effectivity_aircraft_types": ("A320",),
    }
    payload = _release_payload(
        work_cards=(bad_card,),
        components=(bad_component,),
        airworthiness_directives=({"ad_id": "AD-OPEN", "status": "open"},),
        deferred_defects=({"defect_id": "MEL-OLD", "status": "deferred", "expiry_date": "2026-01-01"},),
        certifier={},
    )

    result = aviation_maintenance_repair_assess_release_to_service(
        aviation_maintenance_repair_empty_state(),
        payload,
    )

    codes = {blocker["code"] for blocker in result["release_pack"]["blockers"]}
    assert result["ok"] is False
    assert {
        "self_inspection_blocked",
        "controlled_tool_not_returned",
        "tool_calibration_expired",
        "consumable_expired",
        "consumable_mix_life_expired",
        "life_limit_cycles_exhausted",
        "life_limit_hours_exhausted",
        "component_quarantined",
        "missing_release_certificate",
        "component_not_effective_for_aircraft",
        "deferred_defect_expired",
        "airworthiness_directive_open",
        "human_certifier_required",
    }.issubset(codes)
    assert result["state"]["outbox"][-1]["event_type"] == "AviationMaintenanceRepairExceptionOpened"


def test_component_and_work_card_checks_are_independently_executable():
    component = evaluate_component_installation(
        {"component_id": "COMP-OK", "remaining_cycles": 1, "remaining_hours": 2, "release_certificate": "ARC", "effectivity_tail_numbers": ("5Y-AXA",)},
        {"tail_number": "5Y-AXA"},
        as_of="2026-05-28",
    )
    assert component["ok"] is True

    card = evaluate_work_card_closeout(
        _release_payload()["work_cards"][0],
        _release_payload()["technician_authorizations"],
        as_of="2026-05-28",
    )
    assert card["ok"] is True
    assert card["signed_roles"] == ("duplicate_inspector", "performer")


def test_release_slice_is_exposed_to_service_ui_agent_and_release_evidence():
    service = AviationMaintenanceRepairService()
    preview = service.assess_release_to_service(_release_payload())
    assert preview["ok"] is True
    assert preview["release_pack"]["status"] == "release_ready"

    assert "assess_release_to_service" in service_operation_manifest()["command_operations"]
    assert "assess_release_to_service" in aviation_maintenance_repair_build_service_contract()["command_methods"]
    assert any(check["id"] == "maintenance_release_execution" and check["ok"] for check in aviation_maintenance_repair_build_release_evidence()["checks"])

    ui_contract = aviation_maintenance_repair_ui_contract()
    assert "release_to_service" in ui_contract["full_capability_surface"]["navigation_sections"]
    assert "release_to_service_pack" in aviation_maintenance_repair_render_workbench()["release_panels"]
    assert "release_to_service_pack" in aviation_maintenance_repair_build_workbench_view()["release_panels"]

    chatbot = chatbot_interface_contract()
    assert "release_to_service_evidence_preview" in chatbot["capabilities"]
    instruction = document_instruction_plan("work pack", "prepare release signoff evidence")
    assert instruction["release_to_service_preview"]["human_certifier_required"] is True
    assert instruction["release_to_service_preview"]["assistant_can_certify"] is False

