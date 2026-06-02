"""Standalone one-PBC application surface for chemical_batch_compliance."""

from __future__ import annotations

from . import routes
from . import ui
from .runtime import CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC
from .services import ChemicalBatchComplianceService
from .services import service_operation_manifest
from .slice_app import build_workbench_view

PBC_KEY = "chemical_batch_compliance"
EVENT_CONTRACT = "AppGen-X"

DEFAULT_PRINCIPAL_PERMISSIONS = (
    "chemical_batch_compliance.read",
    "chemical_batch_compliance.create",
    "chemical_batch_compliance.update",
    "chemical_batch_compliance.approve",
    "chemical_batch_compliance.admin",
)


def _default_configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        "retry_limit": 5,
        "default_policy": "cgmp_change_control",
        "agent_confirmation_required": True,
        "stream_engine_picker_visible": False,
    }


def standalone_app_manifest() -> dict:
    service = ChemicalBatchComplianceService()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app": ui.chemical_batch_compliance_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service_operation_manifest(),
        "configuration": _default_configuration(),
        "side_effects": (),
    }


class ChemicalBatchComplianceStandaloneApp:
    """Package-local app that can run chemical compliance with this PBC alone."""

    def __init__(self, state: dict | None = None) -> None:
        self.service = ChemicalBatchComplianceService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, route: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(route, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant-demo") -> dict:
        configured = self.service.configure_runtime(_default_configuration())
        self.service.set_parameter({"name": "misweigh_alert_pct", "value": 1.0, "tenant": tenant})
        self.service.set_parameter({"name": "workbench_limit", "value": 100, "tenant": tenant})
        rule = self.service.register_rule(
            {
                "tenant": tenant,
                "rule_id": "formula_effectivity_rule",
                "scope": "formula_release",
                "threshold_json": {"max_missing_gates": 0},
            }
        )
        self.service.receive_event(
            {
                "event_type": "PolicyChanged",
                "tenant": tenant,
                "idempotency_key": f"{tenant}:policy-bootstrap",
                "payload": {"policy": "cgmp_change_control"},
            }
        )
        return {
            "ok": configured["ok"] and rule["ok"],
            "tenant": tenant,
            "configuration": configured,
            "rule": rule,
            "state": self.state,
            "side_effects": (),
        }

    def load_demo_workspace(self, *, tenant: str = "tenant-demo") -> dict:
        bootstrapped = self.bootstrap(tenant=tenant)
        sds = self.dispatch(
            "POST /sds-documents",
            {
                "tenant": tenant,
                "material_code": "SOLV-100",
                "revision": "8",
                "issue_date": "2026-01-01",
                "expiration_date": "2027-01-01",
                "jurisdictions": ("US", "EU"),
                "hazard_summary": {"signal_word": "Danger", "flash_point_c": 18},
                "exposure_controls": ("nitrile_gloves", "local_exhaust"),
                "approved": True,
            },
        )
        material = self.dispatch(
            "POST /hazardous-materials",
            {
                "tenant": tenant,
                "material_code": "SOLV-100",
                "ghs_classification": ("Flammable liquid, category 2",),
                "storage_class": "flammable_liquid_cabinet",
                "approved_sources": ("Vendor A",),
                "ppe_requirements": ("gloves", "goggles", "local_exhaust"),
                "label_profile": {"signal_word": "Danger", "pictograms": ("flame",)},
            },
        )
        formula = self.dispatch(
            "POST /chemical-formulas",
            {
                "tenant": tenant,
                "formula_code": "CBR-77",
                "revision": "A",
                "product_name": "Catalyst Blend 77",
                "target_concentration": {"assay_pct": 98.5, "density_g_ml": 0.91},
                "composition_window": {"solvent_pct_min": 30, "solvent_pct_max": 32},
                "approved_substitutes": (
                    {
                        "material_code": "SOLV-100-ALT",
                        "approved_supplier": "Vendor B",
                        "equivalence_basis": "matched impurity profile",
                    },
                ),
                "required_sds_ids": (sds["result"]["result"]["record"]["id"],),
                "required_hazard_material_ids": (material["result"]["result"]["record"]["id"],),
                "required_permits": ("hot_work",),
                "equipment_classes": ("reactor_train_a",),
                "approvals": {"technical": True, "quality": True, "ehs": True},
                "effectivity_start": "2026-01-02",
                "process_steps": (
                    {"step_code": "charge", "critical": True, "parameter": "weight"},
                    {"step_code": "react", "critical": True, "parameter": "temperature"},
                    {"step_code": "filter", "critical": False, "parameter": "clarity"},
                ),
            },
        )
        formula_id = formula["result"]["result"]["record"]["id"]
        released = self.service.release_formula_revision(
            {"id": formula_id, "tenant": tenant, "released_by": "quality-board"}
        )
        batch = self.dispatch(
            "POST /batch-records",
            {
                "tenant": tenant,
                "batch_number": "BATCH-1001",
                "formula_id": formula_id,
                "equipment_profile": {
                    "line_clearance": True,
                    "cleaning_release": True,
                    "calibration_current": True,
                },
                "permits_confirmed": ("hot_work",),
                "step_executions": (
                    {"step_code": "charge", "status": "complete", "operator": "op-1"},
                    {"step_code": "react", "status": "complete", "operator": "op-2"},
                    {"step_code": "filter", "status": "complete", "operator": "op-1"},
                ),
                "dispense_log": (
                    {"material_code": "SOLV-100", "target_qty": 100.0, "actual_qty": 100.4, "container_id": "DRUM-1"},
                ),
                "parameter_log": (
                    {"parameter_name": "temperature", "value": 42, "band": "advisory", "instrument_id": "TEMP-1"},
                ),
                "sampling_plan": (
                    {"sample_point": "react_end", "required_tests": ("assay",), "status": "collected"},
                ),
            },
        )
        batch_id = batch["result"]["result"]["record"]["id"]
        quality = self.service.record_quality_test(
            {
                "tenant": tenant,
                "batch_id": batch_id,
                "sample_point": "react_end",
                "test_name": "assay",
                "specification": {"min": 98.0, "max": 101.0},
                "result_value": 97.5,
                "result_status": "fail",
            }
        )
        instruction = self.service.create_document_instruction(
            {
                "tenant": tenant,
                "document": "Formula Code: CBR-77\nRevision: B\nSolvent Range: 31-33",
                "instruction": "Update the formula revision and prepare a regulatory label update.",
                "artifact_key": "uploaded-formula-change",
            }
        )
        submission = self.dispatch(
            "POST /regulatory-submissions",
            {
                "tenant": tenant,
                "dossier_number": "EPA-2026-001",
                "jurisdiction": "US",
                "submission_type": "label_update",
                "product_code": "CBR-77",
                "source_record_ids": (formula_id, batch_id, sds["result"]["result"]["record"]["id"]),
                "commitment_actions": ("send revised workplace label",),
            },
        )
        workbench = self.render_workbench(tenant=tenant)
        return {
            "ok": all(
                item["ok"]
                for item in (bootstrapped, sds, material, formula, released, batch, quality, instruction, submission, workbench)
            )
            and quality["result"]["hold"] is not None,
            "tenant": tenant,
            "formula_id": formula_id,
            "batch_id": batch_id,
            "workbench": workbench,
            "quality": quality,
            "submission": submission,
            "agent_instruction": instruction,
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str = "tenant-demo", principal_permissions: tuple[str, ...] | None = None) -> dict:
        del principal_permissions
        return build_workbench_view(self.state, tenant=tenant)

    def release_snapshot(self) -> dict:
        from .runtime import chemical_batch_compliance_build_release_evidence
        from .runtime import chemical_batch_compliance_runtime_smoke

        smoke = chemical_batch_compliance_runtime_smoke()
        evidence = chemical_batch_compliance_build_release_evidence(smoke["state"])
        return {
            "ok": smoke["ok"] and evidence["ok"],
            "runtime_smoke_ok": smoke["ok"],
            "evidence": evidence,
            "side_effects": (),
        }


def standalone_route_contracts() -> dict:
    routes_tuple = (
        "GET /chemical-batch-compliance/app",
        "GET /chemical-batch-compliance/forms",
        "GET /chemical-batch-compliance/wizards",
        "GET /chemical-batch-compliance/controls",
        "POST /chemical-batch-compliance/formula-release/run",
        "POST /chemical-batch-compliance/batch-execution/run",
        "POST /chemical-batch-compliance/quality-hold/run",
        "POST /chemical-batch-compliance/regulatory-dossier/run",
        "POST /chemical-batch-compliance/agent/preview",
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "routes": routes_tuple,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def single_pbc_app_contract() -> dict:
    app = ChemicalBatchComplianceStandaloneApp()
    demo = app.load_demo_workspace()
    ui_contract = ui.chemical_batch_compliance_ui_contract()
    route_contracts = standalone_route_contracts()
    release_snapshot = app.release_snapshot()
    return {
        "ok": demo["ok"] and ui_contract["ok"] and route_contracts["ok"] and release_snapshot["ok"],
        "pbc": PBC_KEY,
        "app_name": "Chemical Batch Compliance Workbench",
        "owned_tables": tuple(app.state["tables"].keys()),
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": EVENT_CONTRACT,
        "forms": ui_contract["full_capability_surface"]["forms"],
        "wizards": ui_contract["full_capability_surface"]["wizards"],
        "controls": ui_contract["full_capability_surface"]["controls"],
        "routes": route_contracts,
        "simulation": demo,
        "dsl_exposure": {
            "pbc": PBC_KEY,
            "models": tuple(app.state["tables"].keys()),
            "routes": route_contracts["routes"],
            "agent_skill_namespace": f"{PBC_KEY}_skills",
            "ui_fragments": (
                "ChemicalBatchComplianceWorkbench",
                "FormulaReleaseWorkbench",
                "BatchExecutionWorkbench",
                "QualityHoldWorkbench",
                "RegulatoryDossierWorkbench",
            ),
        },
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def standalone_smoke_test() -> dict:
    contract = single_pbc_app_contract()
    return {
        "ok": contract["ok"] and not contract["stream_engine_picker_visible"],
        "app": contract,
        "side_effects": (),
    }


def workbench_smoke_test() -> dict:
    app = ChemicalBatchComplianceStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench()
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["summary"]["open_holds"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
