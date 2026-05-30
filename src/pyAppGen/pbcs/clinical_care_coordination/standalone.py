"""Standalone one-PBC application surface for clinical_care_coordination."""

from __future__ import annotations

from . import release_evidence
from . import routes
from . import ui
from .services import ClinicalCareCoordinationService


DEFAULT_PRINCIPAL_PERMISSIONS = tuple(ui.ACTION_PERMISSIONS)


def standalone_app_manifest() -> dict:
    service_manifest = ClinicalCareCoordinationService().query_service_contract({})["result"]
    return {
        "ok": True,
        "pbc": "clinical_care_coordination",
        "app": ui.clinical_care_coordination_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service_manifest,
        "side_effects": (),
    }


class ClinicalCareCoordinationStandaloneApp:
    """Package-local standalone app that owns care coordination runtime state."""

    def __init__(self, state: dict | None = None):
        self.service = ClinicalCareCoordinationService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, route: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(route, payload, service=self.service)

    def bootstrap(self, *, patient_ref: str = "patient-demo") -> dict:
        plan = self.dispatch(
            "POST /patient-care-plans",
            {
                "patient_ref": patient_ref,
                "problem": "post discharge heart failure transition",
                "goal": "complete follow-up plan",
                "responsible_role": "primary_coordinator",
                "review_cadence_days": 7,
                "state": "active",
                "barriers": ("transportation",),
            },
        )
        team = self.dispatch(
            "POST /care-teams",
            {
                "patient_ref": patient_ref,
                "member_ref": "coordinator-1",
                "role": "primary_coordinator",
                "coverage_start": "2026-01-01",
                "consent_scope": ("care_plan", "referral", "transition"),
                "can_receive_protected_details": True,
            },
        )
        return {
            "ok": plan["ok"] and team["ok"],
            "patient_ref": patient_ref,
            "care_plan_id": plan["result"]["care_plan"]["id"],
            "state": self.state,
            "side_effects": (),
        }

    def load_demo_workspace(self, *, patient_ref: str = "patient-demo") -> dict:
        bootstrapped = self.bootstrap(patient_ref=patient_ref)
        care_plan_id = bootstrapped["care_plan_id"]
        referral = self.dispatch(
            "POST /referrals",
            {
                "patient_ref": patient_ref,
                "specialty": "cardiology",
                "urgency": "urgent",
                "reason": "post discharge medication optimization",
                "expected_turnaround_days": 3,
                "authorization_required": False,
            },
        )
        self.service.receive_referral_result(
            {
                "referral_id": referral["result"]["referral"]["id"],
                "result_document_ref": "doc-demo-referral",
                "summary": "Increase daily monitoring and schedule review.",
            }
        )
        self.dispatch(
            "POST /encounters",
            {
                "patient_ref": patient_ref,
                "occurred_at": "2026-01-02",
                "coordination_actions": (
                    {
                        "action": "patient_outreach",
                        "owner_role": "primary_coordinator",
                        "source_note_span": "discharge-summary:12-19",
                    },
                ),
            },
        )
        self.dispatch(
            "POST /care-gaps",
            {
                "patient_ref": patient_ref,
                "gap_type": "post_discharge_follow_up",
                "severity": "high",
                "guideline_basis": "follow up within seven days",
                "linked_care_plan_id": care_plan_id,
            },
        )
        self.dispatch(
            "POST /transition-plans",
            {
                "patient_ref": patient_ref,
                "discharge_source": "inpatient",
                "receiving_setting": "home",
                "medication_reconciliation_status": "complete",
                "follow_up_appointments": ("cardiology",),
                "patient_instructions": "Daily weights and urgent symptom escalation.",
                "caregiver_confirmation": True,
                "transportation_plan": "family transport confirmed",
            },
        )
        self.dispatch(
            "POST /outcome-measures",
            {
                "care_plan_id": care_plan_id,
                "measure_code": "follow_up_completed",
                "baseline_value": 0,
                "current_value": 1,
                "target_value": 1,
                "source": "standalone_demo",
            },
        )
        return {
            "ok": True,
            "patient_ref": patient_ref,
            "workbench": self.render_workbench(),
            "side_effects": (),
        }

    def render_workbench(self, *, principal_permissions: tuple[str, ...] | None = None) -> dict:
        return ui.clinical_care_coordination_render_workbench(
            self.state,
            principal_permissions=principal_permissions or DEFAULT_PRINCIPAL_PERMISSIONS,
        )

    def release_snapshot(self) -> dict:
        return release_evidence.release_readiness_manifest()


def smoke_test() -> dict:
    app = ClinicalCareCoordinationStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench()
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["queue_counts"]["high_risk_patients"] >= 1 and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }


def workbench_smoke_test() -> dict:
    app = ClinicalCareCoordinationStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench()
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["shell"]["app_id"] == "clinical_care_coordination_one_pbc_app",
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
