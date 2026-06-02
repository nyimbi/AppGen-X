from pyAppGen.pbcs.food_safety_quality_compliance.routes import FoodSafetyQualityComplianceService
from pyAppGen.pbcs.food_safety_quality_compliance.routes import dispatch_route
from pyAppGen.pbcs.food_safety_quality_compliance.runtime import food_safety_quality_compliance_runtime_smoke
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import QUALITY_HOLD_TABLE
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import approve_document_instruction
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import approve_haccp_plan
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import build_app_surface
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import close_nonconformance
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import create_critical_control_point
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import create_document_instruction
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import create_haccp_plan
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import empty_state
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import open_quality_hold
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import query_haccp_plan_detail
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import record_inspection
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import release_quality_hold
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import run_mock_recall
from pyAppGen.pbcs.food_safety_quality_compliance.slice_app import start_recall_event


def _approved_plan_state():
    state = empty_state()
    plan = create_haccp_plan(
        state,
        {
            "tenant": "tenant-test",
            "plan_code": "RTE-CHILL",
            "version": "2",
            "facility_code": "FAC-1",
            "product_scope": ("ready_to_eat_meals",),
            "process_steps": ({"step_code": "cook"}, {"step_code": "chill"}),
            "hazard_analysis": (
                {"hazard_id": "haz-1", "process_step_code": "cook", "requires_ccp": True},
                {"hazard_id": "haz-2", "process_step_code": "chill", "requires_ccp": True},
            ),
            "approvals": {"food_safety": True, "quality": True},
            "effective_from": "2026-01-03",
        },
    )
    failed = approve_haccp_plan(plan["state"], {"tenant": "tenant-test", "id": plan["record"]["id"], "approvals": {"operations": True}})
    assert failed["ok"] is False
    ccp1 = create_critical_control_point(
        plan["state"],
        {
            "tenant": "tenant-test",
            "plan_id": plan["record"]["id"],
            "process_step_code": "cook",
            "hazard_id": "haz-1",
            "limit_min": 74.0,
            "limit_max": 76.0,
            "unit": "celsius",
            "monitoring_method": "probe",
            "monitoring_frequency_minutes": 15,
        },
    )
    ccp2 = create_critical_control_point(
        ccp1["state"],
        {
            "tenant": "tenant-test",
            "plan_id": plan["record"]["id"],
            "process_step_code": "chill",
            "hazard_id": "haz-2",
            "limit_min": 0.0,
            "limit_max": 5.0,
            "unit": "celsius",
            "monitoring_method": "data_logger",
            "monitoring_frequency_minutes": 30,
        },
    )
    approved = approve_haccp_plan(
        ccp2["state"],
        {"tenant": "tenant-test", "id": plan["record"]["id"], "approvals": {"operations": True}, "effective_from": "2026-01-03"},
    )
    return approved["state"], approved["record"]


def test_inspection_pins_haccp_version_and_opens_hold_and_nonconformance():
    state, plan = _approved_plan_state()
    inspection = record_inspection(
        state,
        {
            "tenant": "tenant-test",
            "plan_code": plan["plan_code"],
            "facility_code": plan["facility_code"],
            "area": "cooling-room",
            "checklist": ("temperature",),
            "findings": (
                {
                    "category": "temperature",
                    "severity": "critical",
                    "description": "Rapid chill exceeded safe temperature.",
                    "affected_lots": ("LOT-1",),
                    "process_step_code": "chill",
                    "affected_quantity": 42.0,
                },
            ),
            "inspector": "qa.lead",
        },
    )
    detail = query_haccp_plan_detail(inspection["state"], plan["id"])
    assert inspection["ok"] is True
    assert inspection["record"]["plan_version"] == plan["version"]
    assert inspection["created_hold_ids"]
    assert inspection["created_nonconformance_ids"]
    assert detail["ok"] is True
    assert len(detail["quality_holds"]) == 1


def test_major_nonconformance_cannot_close_without_root_cause_evidence():
    state, _plan = _approved_plan_state()
    inspection = record_inspection(
        state,
        {
            "tenant": "tenant-test",
            "plan_code": "RTE-CHILL",
            "facility_code": "FAC-1",
            "area": "label-room",
            "checklist": ("label",),
            "findings": ({"category": "allergen", "severity": "major", "description": "Undeclared allergen statement missing.", "affected_lots": ("LOT-2",)},),
            "inspector": "qa.lead",
        },
    )
    nc_id = inspection["created_nonconformance_ids"][0]
    failed = close_nonconformance(inspection["state"], {"id": nc_id})
    closed = close_nonconformance(
        inspection["state"],
        {
            "id": nc_id,
            "root_cause_method": "5 whys",
            "confirmed_root_cause": "Label changeover verification skipped.",
            "preventive_action": "Require dual sign-off.",
            "effectiveness_evidence": "Three compliant changeovers observed.",
        },
    )
    assert failed["ok"] is False
    assert closed["ok"] is True


def test_hold_release_requires_disposition_approval_and_quantity_match():
    state, plan = _approved_plan_state()
    hold = open_quality_hold(
        state,
        {
            "tenant": "tenant-test",
            "hold_reason": "Foreign material investigation.",
            "affected_lots": ("LOT-3",),
            "quantity": 10.0,
            "location": "quality-cage",
            "haccp_plan_id": plan["id"],
        },
    )
    failed = release_quality_hold(hold["state"], {"id": hold["record"]["id"], "approved_by": (), "disposition": "rework", "quantity_reconciled": 10.0})
    released = release_quality_hold(hold["state"], {"id": hold["record"]["id"], "approved_by": ("qa.lead",), "disposition": "rework", "quantity_reconciled": 10.0})
    assert failed["ok"] is False
    assert released["ok"] is True
    assert released["record"]["status"] == "released"


def test_recall_analysis_enforces_projection_boundary():
    state, _plan = _approved_plan_state()
    failed = start_recall_event(
        state,
        {"tenant": "tenant-test", "classification": "class_i", "reason": "pathogen", "inventory_table": "inventory.lot"},
    )
    mock = run_mock_recall(
        state,
        {
            "tenant": "tenant-test",
            "classification": "mock_recall",
            "reason": "annual_readiness",
            "genealogy_projection": ({"source_lot": "RAW-1", "finished_lot": "LOT-4", "customers": ("Retailer A",)},),
            "shipment_projection": ({"lot": "LOT-4", "customer": "Retailer A"},),
            "trace_elapsed_minutes": 80,
        },
    )
    assert failed["ok"] is False
    assert mock["ok"] is True
    assert mock["evidence_packet"]["projection_boundary_ok"] is True
    assert mock["evidence_packet"]["mutates_live_state"] is False


def test_governed_agent_preview_requires_citations_and_release_review():
    state = empty_state()
    failed = create_document_instruction(
        state,
        {
            "tenant": "tenant-test",
            "document": "Deviation memo",
            "instruction": "Open hold for LOT-5.",
            "target_table": QUALITY_HOLD_TABLE,
            "action": "create",
        },
    )
    created = create_document_instruction(
        state,
        {
            "tenant": "tenant-test",
            "document": "Deviation memo",
            "instruction": "Open hold for LOT-5.",
            "target_table": QUALITY_HOLD_TABLE,
            "action": "create",
            "citations": ("memo:1",),
        },
    )
    blocked = approve_document_instruction(created["state"], {"id": created["record"]["id"], "approved_by": "qa.lead"})
    approved = approve_document_instruction(created["state"], {"id": created["record"]["id"], "approved_by": "qa.lead", "release_reviewed": True})
    assert failed["ok"] is False
    assert blocked["ok"] is False
    assert approved["ok"] is True


def test_route_dispatch_and_app_surface_are_usable():
    service = FoodSafetyQualityComplianceService()
    plan = dispatch_route(
        "POST /haccp-plans",
        {
            "tenant": "tenant-route",
            "plan_code": "ROUTE-1",
            "version": "1",
            "facility_code": "FAC-1",
            "product_scope": ("meal",),
            "process_steps": ({"step_code": "cook"},),
            "hazard_analysis": ({"hazard_id": "haz-1", "process_step_code": "cook", "requires_ccp": False},),
        },
        service=service,
    )
    workbench = dispatch_route("GET /food-safety-quality-compliance-workbench", {"tenant": "tenant-route"}, service=service)
    surface = build_app_surface(service.state, tenant="tenant-route")
    assert plan["ok"] is True
    assert workbench["ok"] is True
    assert len(surface["forms"]) == 4
    assert len(surface["controls"]) == 5


def test_runtime_smoke_covers_end_to_end_slice():
    smoke = food_safety_quality_compliance_runtime_smoke()
    assert smoke["ok"] is True
    assert any(check["id"] == "document_instruction_crud" and check["ok"] for check in smoke["slice_smoke"]["checks"])
