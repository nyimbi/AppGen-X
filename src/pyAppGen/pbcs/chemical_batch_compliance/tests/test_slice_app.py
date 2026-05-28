from pyAppGen.pbcs.chemical_batch_compliance.routes import ChemicalBatchComplianceService
from pyAppGen.pbcs.chemical_batch_compliance.routes import dispatch_route
from pyAppGen.pbcs.chemical_batch_compliance.runtime import chemical_batch_compliance_runtime_smoke
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import build_app_surface
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import create_formula_revision
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import create_regulatory_submission
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import empty_state
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import query_batch_detail
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import record_batch
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import record_quality_test
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import register_hazardous_material
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import release_formula_revision
from pyAppGen.pbcs.chemical_batch_compliance.slice_app import review_sds_document


def _released_formula_state():
    state = empty_state()
    sds = review_sds_document(
        state,
        {
            "tenant": "tenant-test",
            "material_code": "SOLV-200",
            "revision": "4",
            "issue_date": "2026-01-01",
            "expiration_date": "2027-01-01",
            "approved": True,
        },
    )
    material = register_hazardous_material(
        sds["state"],
        {
            "tenant": "tenant-test",
            "material_code": "SOLV-200",
            "ghs_classification": ("Flammable liquid, category 2",),
            "approved_sources": ("Qualified Vendor",),
        },
    )
    formula = create_formula_revision(
        material["state"],
        {
            "tenant": "tenant-test",
            "formula_code": "FORM-1",
            "revision": "A",
            "product_name": "Blend 1",
            "target_concentration": {"assay_pct": 98.2},
            "composition_window": {"solvent_pct_min": 20, "solvent_pct_max": 25},
            "required_sds_ids": (sds["record"]["id"],),
            "required_hazard_material_ids": (material["record"]["id"],),
            "required_permits": ("hot_work",),
            "approvals": {"technical": True, "quality": True, "ehs": True},
            "effectivity_start": "2026-01-03",
            "process_steps": (
                {"step_code": "charge", "critical": True},
                {"step_code": "react", "critical": True},
            ),
        },
    )
    released = release_formula_revision(formula["state"], {"id": formula["record"]["id"], "tenant": "tenant-test"})
    return released["state"], released["record"]


def test_formula_release_requires_safety_and_approval_gates():
    state = empty_state()
    formula = create_formula_revision(
        state,
        {
            "tenant": "tenant-test",
            "formula_code": "FORM-MISSING",
            "revision": "A",
            "product_name": "Unreleased Blend",
            "target_concentration": {"assay_pct": 90.0},
            "composition_window": {"solvent_pct_min": 10, "solvent_pct_max": 15},
            "effectivity_start": "2026-01-03",
        },
    )
    released = release_formula_revision(formula["state"], {"id": formula["record"]["id"], "tenant": "tenant-test"})
    assert released["ok"] is False
    assert "missing_technical_approval" in released["missing_gates"]
    assert "missing_quality_approval" in released["missing_gates"]
    assert "missing_ehs_approval" in released["missing_gates"]


def test_batch_quality_failure_creates_hold_and_submission_uses_owned_records():
    state, formula = _released_formula_state()
    batch = record_batch(
        state,
        {
            "tenant": "tenant-test",
            "batch_number": "B-2001",
            "formula_id": formula["id"],
            "equipment_profile": {
                "line_clearance": True,
                "cleaning_release": True,
                "calibration_current": True,
            },
            "permits_confirmed": ("hot_work",),
            "step_executions": (
                {"step_code": "charge", "status": "complete"},
                {"step_code": "react", "status": "complete"},
            ),
            "dispense_log": (
                {"material_code": "SOLV-200", "target_qty": 100.0, "actual_qty": 100.0},
            ),
        },
    )
    quality = record_quality_test(
        batch["state"],
        {
            "tenant": "tenant-test",
            "batch_id": batch["record"]["id"],
            "test_name": "assay",
            "specification": {"min": 98.0, "max": 101.0},
            "result_value": 97.0,
            "result_status": "fail",
        },
    )
    detail = query_batch_detail(quality["state"], batch["record"]["id"])
    submission = create_regulatory_submission(
        quality["state"],
        {
            "tenant": "tenant-test",
            "dossier_number": "DOS-1",
            "jurisdiction": "US",
            "submission_type": "label_update",
            "product_code": "FORM-1",
            "source_record_ids": (formula["id"], batch["record"]["id"]),
        },
    )
    assert quality["hold"] is not None
    assert detail["ok"] is True
    assert len(detail["holds"]) == 1
    assert submission["record"]["status"] == "ready_for_submission"


def test_route_dispatch_and_app_surface_are_usable():
    service = ChemicalBatchComplianceService()
    formula = dispatch_route(
        "POST /chemical-formulas",
        {
            "tenant": "tenant-route",
            "formula_code": "ROUTE-1",
            "revision": "A",
            "product_name": "Route Blend",
            "target_concentration": {"assay_pct": 88.0},
            "composition_window": {"solvent_pct_min": 12, "solvent_pct_max": 13},
            "effectivity_start": "2026-01-01",
        },
        service=service,
    )
    workbench = dispatch_route("GET /chemical-batch-compliance-workbench", {"tenant": "tenant-route"}, service=service)
    surface = build_app_surface(service.state, tenant="tenant-route")
    assert formula["ok"] is True
    assert workbench["ok"] is True
    assert len(surface["forms"]) == 4
    assert len(surface["controls"]) == 5


def test_runtime_smoke_covers_end_to_end_slice():
    smoke = chemical_batch_compliance_runtime_smoke()
    assert smoke["ok"] is True
    assert any(check["id"] == "document_instruction_crud" and check["ok"] for check in smoke["slice_smoke"]["checks"])
