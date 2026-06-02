"""Standalone one-PBC app surface for clinical_trials_management."""

from __future__ import annotations

from .agent import chatbot_interface_contract, clinical_trials_management_assistant_preview, composed_agent_contribution
from .controls import clinical_trials_management_control_center
from .forms import clinical_trials_management_form_catalog
from .runtime import (
    CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
    CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    clinical_trials_management_assess_lock_readiness,
    clinical_trials_management_build_release_evidence,
    clinical_trials_management_build_workbench_view,
    clinical_trials_management_command_adverse_event,
    clinical_trials_management_command_consent_record,
    clinical_trials_management_command_monitoring_finding,
    clinical_trials_management_command_study_site,
    clinical_trials_management_command_subject,
    clinical_trials_management_command_trial_protocol,
    clinical_trials_management_command_visit_schedule,
    clinical_trials_management_configure_runtime,
    clinical_trials_management_empty_state,
    clinical_trials_management_receive_event,
    clinical_trials_management_register_governed_model,
    clinical_trials_management_register_rule,
    clinical_trials_management_run_control_tests,
    clinical_trials_management_set_parameter,
    clinical_trials_management_verify_formal_invariants,
)
from .ui import clinical_trials_management_render_workbench, clinical_trials_management_standalone_app_contract
from .wizards import clinical_trials_management_wizard_catalog

PBC_KEY = "clinical_trials_management"
EVENT_CONTRACT = "AppGen-X"


def _default_configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "default_timezone": "UTC",
        "default_jurisdiction": "US",
        "retry_limit": 5,
        "stream_engine_picker_visible": False,
    }


class ClinicalTrialsManagementStandaloneApp:
    """Runs clinical trial operations with package-owned runtime state only."""

    def __init__(self, state: dict | None = None) -> None:
        self.state = state or clinical_trials_management_empty_state()

    def bootstrap(self, *, tenant: str = "tenant-demo") -> dict:
        configured = clinical_trials_management_configure_runtime(self.state, _default_configuration())
        self.state = configured["state"]
        parameter = clinical_trials_management_set_parameter(self.state, "serious_event_reporting_hours", 24)
        self.state = parameter["state"]
        rule = clinical_trials_management_register_rule(
            self.state,
            {
                "tenant": tenant,
                "rule_id": "safety-reporting-sla",
                "rule_type": "safety",
                "scope": "tenant",
                "condition": "serious_event_reporting_hours<=24",
                "status": "active",
                "policy_version": "v1",
                "description": "Serious adverse events must be reported within 24 hours.",
            },
        )
        self.state = rule["state"]
        event = clinical_trials_management_receive_event(
            self.state,
            {"tenant": tenant, "event_type": "PolicyChanged", "idempotency_key": f"{tenant}:policy-bootstrap"},
        )
        self.state = event["state"]
        return {"ok": configured["ok"] and parameter["ok"] and rule["ok"] and event["ok"], "configuration": configured, "parameter": parameter, "rule": rule, "event": event, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant-demo") -> dict:
        bootstrapped = self.bootstrap(tenant=tenant)
        protocol = clinical_trials_management_command_trial_protocol(
            self.state,
            {
                "tenant": tenant,
                "protocol_id": "PROT-DEMO",
                "protocol_code": "PROT-DEMO",
                "title": "Phase II oncology study",
                "phase": "II",
                "version": 2,
                "status": "active",
                "amendment_reason": "Tumor assessment cadence update",
                "countries": ("US", "GB"),
            },
        )
        self.state = protocol["state"]
        site = clinical_trials_management_command_study_site(
            self.state,
            {
                "tenant": tenant,
                "site_id": "SITE-DEMO",
                "protocol_id": "PROT-DEMO",
                "site_number": "001",
                "country": "US",
                "principal_investigator": "Dr. Rivera",
                "ethics_approval": True,
                "contract_executed": True,
                "training_complete": True,
                "delegation_log_ready": True,
                "activation_date": "2026-05-29",
            },
        )
        self.state = site["state"]
        consent = clinical_trials_management_command_consent_record(
            self.state,
            {
                "tenant": tenant,
                "consent_id": "CONS-DEMO",
                "subject_id": "SUBJ-DEMO",
                "protocol_id": "PROT-DEMO",
                "site_id": "SITE-DEMO",
                "consent_version": 2,
                "language": "en",
                "status": "current",
                "signed_on": "2026-05-29",
                "consent_scope": ("main_study", "recontact"),
                "source_document_ref": "tmf://consent/CONS-DEMO",
            },
        )
        self.state = consent["state"]
        subject = clinical_trials_management_command_subject(
            self.state,
            {
                "tenant": tenant,
                "subject_id": "SUBJ-DEMO",
                "protocol_id": "PROT-DEMO",
                "site_id": "SITE-DEMO",
                "screening_number": "SCR-DEMO",
                "eligibility_evidence_complete": True,
                "exclusion_clear": True,
                "consent_id": "CONS-DEMO",
                "enrollment_requested": True,
                "cohort": "C1",
                "arm": "A",
            },
        )
        self.state = subject["state"]
        visit = clinical_trials_management_command_visit_schedule(
            self.state,
            {
                "tenant": tenant,
                "visit_id": "VISIT-DEMO",
                "subject_id": "SUBJ-DEMO",
                "protocol_id": "PROT-DEMO",
                "site_id": "SITE-DEMO",
                "visit_code": "C1D1",
                "visit_type": "baseline",
                "target_day": 1,
                "actual_day": 1,
                "required_procedures": ("labs", "ecg", "tumor_assessment"),
                "completed_procedures": ("labs", "ecg", "tumor_assessment"),
            },
        )
        self.state = visit["state"]
        adverse_event = clinical_trials_management_command_adverse_event(
            self.state,
            {
                "tenant": tenant,
                "adverse_event_id": "AE-DEMO",
                "subject_id": "SUBJ-DEMO",
                "protocol_id": "PROT-DEMO",
                "site_id": "SITE-DEMO",
                "event_term": "Grade 3 neutropenia",
                "seriousness": "serious",
                "grade": "3",
                "expectedness": "expected",
                "relatedness": "possible",
                "reported_within_hours": 8,
                "status": "closed",
            },
        )
        self.state = adverse_event["state"]
        finding = clinical_trials_management_command_monitoring_finding(
            self.state,
            {
                "tenant": tenant,
                "finding_id": "MON-DEMO",
                "protocol_id": "PROT-DEMO",
                "site_id": "SITE-DEMO",
                "subject_id": "SUBJ-DEMO",
                "finding_type": "source_data",
                "severity": "major",
                "owner": "monitor-1",
                "status": "resolved",
            },
        )
        self.state = finding["state"]
        model = clinical_trials_management_register_governed_model(
            self.state,
            {
                "tenant": tenant,
                "model_id": "RBM-DEMO",
                "use_case": "risk_based_monitoring",
                "model_version": "1.0",
                "approval_status": "approved",
                "drift_status": "stable",
            },
        )
        self.state = model["state"]
        assistant = clinical_trials_management_assistant_preview(
            {
                "document_text": "Monitoring memo: consent and source data checked at Site 001.",
                "instructions": "Create a monitoring finding preview only.",
                "target_entity": "monitoring_finding",
                "requested_action": "create",
                "payload": {"finding_id": "MON-PREVIEW"},
            }
        )
        controls = clinical_trials_management_run_control_tests(self.state)
        lock = clinical_trials_management_assess_lock_readiness(self.state, {"requested_by": "standalone"})
        invariants = clinical_trials_management_verify_formal_invariants(self.state)
        workbench = self.render_workbench(tenant=tenant)
        return {
            "ok": all((bootstrapped["ok"], protocol["ok"], site["ok"], consent["ok"], subject["ok"], visit["ok"], adverse_event["ok"], finding["ok"], model["ok"], assistant["ok"], controls["ok"], lock["ready"], invariants["ok"], workbench["ok"])),
            "protocol": protocol,
            "site": site,
            "consent": consent,
            "subject": subject,
            "visit": visit,
            "adverse_event": adverse_event,
            "finding": finding,
            "model": model,
            "assistant": assistant,
            "controls": controls,
            "lock": lock,
            "invariants": invariants,
            "workbench": workbench,
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str = "tenant-demo", principal_permissions: tuple[str, ...] = ()) -> dict:
        return clinical_trials_management_render_workbench(self.state, tenant=tenant, principal_permissions=principal_permissions)

    def release_snapshot(self) -> dict:
        evidence = clinical_trials_management_build_release_evidence()
        controls = clinical_trials_management_run_control_tests(self.state)
        return {"ok": evidence["ok"] and controls["ok"], "evidence": evidence, "controls": controls, "side_effects": ()}


def single_pbc_app_contract() -> dict:
    app = ClinicalTrialsManagementStandaloneApp()
    loaded = app.load_demo_workspace()
    ui = clinical_trials_management_standalone_app_contract()
    release = app.release_snapshot()
    return {
        "ok": loaded["ok"] and ui["ok"] and release["ok"],
        "pbc": PBC_KEY,
        "app_name": "Clinical Trials Management Workbench",
        "owned_tables": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
        "database_backends": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "simulation": loaded,
        "release": release,
        "dsl_exposure": {
            "pbc": PBC_KEY,
            "models": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
            "agent_skill_namespace": f"{PBC_KEY}_skills",
            "ui_fragments": ui["fragments"],
        },
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def standalone_smoke_test() -> dict:
    contract = single_pbc_app_contract()
    return {"ok": contract["ok"] and chatbot_interface_contract()["ok"] and composed_agent_contribution()["ok"] and not contract["stream_engine_picker_visible"], "app": contract, "side_effects": ()}
