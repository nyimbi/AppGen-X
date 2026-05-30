"""UI contract for the nonprofit_program_impact PBC."""

from __future__ import annotations

from .controls import nonprofit_program_impact_control_catalog
from .forms import nonprofit_program_impact_form_catalog
from .runtime import NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS
from .runtime import NONPROFIT_PROGRAM_IMPACT_CONSUMED_EVENT_TYPES
from .runtime import NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES
from .runtime import NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC
from .runtime import NONPROFIT_PROGRAM_IMPACT_RUNTIME_TABLES
from .wizards import nonprofit_program_impact_wizard_catalog


PBC_KEY = "nonprofit_program_impact"
NONPROFIT_PROGRAM_IMPACT_UI_FRAGMENT_KEYS = (
    "NonprofitProgramImpactWorkbench",
    "ProgramPortfolioWorkbench",
    "TheoryOfChangeStudio",
    "BeneficiaryImpactTimeline",
    "ServiceDeliveryConsole",
    "OutcomeEvidenceBoard",
    "DonorReportReviewWorkspace",
    "ImpactControlCenter",
    "ImpactWizardLauncher",
    "NonprofitProgramImpactAssistantPanel",
)
_ACTION_PERMISSIONS = {
    "create_program": "nonprofit_program_impact.create",
    "enroll_beneficiary": "nonprofit_program_impact.create",
    "record_service_episode": "nonprofit_program_impact.update",
    "record_outcome_observation": "nonprofit_program_impact.update",
    "freeze_donor_report": "nonprofit_program_impact.approve",
    "run_control_center": "nonprofit_program_impact.admin",
    "assistant_preview": "nonprofit_program_impact.admin",
}


def _sample_state() -> dict:
    return {
        "programs": {
            "PROGRAM-001": {
                "program_id": "PROGRAM-001",
                "tenant": "tenant-smoke",
                "name": "Youth Skills Acceleration",
                "theory_of_change_ready": True,
                "status": "active",
            }
        },
        "beneficiaries": {
            "BEN-001": {
                "beneficiary_id": "BEN-001",
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "status": "enrolled",
            }
        },
        "service_episodes": {
            "EP-001": {
                "episode_id": "EP-001",
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "beneficiary_id": "BEN-001",
                "dosage_completion_ratio": 1.0,
            }
        },
        "outcomes": {
            "OUT-001": {
                "outcome_id": "OUT-001",
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "beneficiary_id": "BEN-001",
                "attainment_ratio": 1.0,
                "status": "on_track",
            }
        },
        "donor_reports": {
            "REPORT-001": {
                "report_id": "REPORT-001",
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "status": "frozen",
            }
        },
        "safeguarding_incidents": {},
        "configuration": {"database_backend": "postgresql", "event_topic": NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC},
        "parameters": {"quality_score_floor": 0.65},
    }


def nonprofit_program_impact_ui_contract() -> dict:
    """Return workbench metadata for the one-PBC nonprofit impact app."""
    forms = nonprofit_program_impact_form_catalog()
    wizards = nonprofit_program_impact_wizard_catalog()
    controls = nonprofit_program_impact_control_catalog()
    return {
        "format": "appgen.nonprofit-program-impact-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/nonprofit_program_impact",
        "fragments": NONPROFIT_PROGRAM_IMPACT_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/nonprofit_program_impact",
            "/workbench/pbcs/nonprofit_program_impact/programs",
            "/workbench/pbcs/nonprofit_program_impact/beneficiaries",
            "/workbench/pbcs/nonprofit_program_impact/service-delivery",
            "/workbench/pbcs/nonprofit_program_impact/outcomes",
            "/workbench/pbcs/nonprofit_program_impact/donor-reports",
            "/workbench/pbcs/nonprofit_program_impact/assistant",
            "/workbench/pbcs/nonprofit_program_impact/controls",
        ),
        "panels": (
            {
                "key": "program_design",
                "fragment": "TheoryOfChangeStudio",
                "binds_to": ("program", "nonprofit_program_impact_policy_rule"),
                "commands": ("create_program",),
            },
            {
                "key": "beneficiary_timeline",
                "fragment": "BeneficiaryImpactTimeline",
                "binds_to": ("beneficiary", "service_episode", "impact_evidence"),
                "commands": ("enroll_beneficiary", "record_service_episode", "record_outcome_observation"),
            },
            {
                "key": "outcome_evidence",
                "fragment": "OutcomeEvidenceBoard",
                "binds_to": ("outcome_measure", "impact_evidence"),
                "commands": ("record_outcome_observation",),
            },
            {
                "key": "donor_reporting",
                "fragment": "DonorReportReviewWorkspace",
                "binds_to": ("donor_report", "outcome_measure"),
                "commands": ("freeze_donor_report",),
            },
            {
                "key": "assistant",
                "fragment": "NonprofitProgramImpactAssistantPanel",
                "binds_to": ("program", "beneficiary", "service_episode", "outcome_measure", "impact_evidence", "donor_report"),
                "commands": ("assistant_preview",),
            },
            {
                "key": "controls",
                "fragment": "ImpactControlCenter",
                "binds_to": ("nonprofit_program_impact_control_assertion", "donor_report", "impact_evidence"),
                "commands": ("run_control_center",),
            },
        ),
        "action_permissions": _ACTION_PERMISSIONS,
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "quality_score_floor",
                "workbench_limit",
            ),
            "allowed_database_backends": NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "quality_score_floor",
                "materiality_threshold",
                "approval_sla_hours",
                "risk_threshold",
                "forecast_horizon_days",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("program_approval", "eligibility_and_consent", "donor_report_freeze"),
            "required_fields": ("rule_id", "rule_type", "status"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": (
                "NonprofitProgramImpactCreated",
                "NonprofitProgramImpactUpdated",
                "NonprofitProgramImpactApproved",
                "NonprofitProgramImpactExceptionOpened",
            ),
            "consumes": NONPROFIT_PROGRAM_IMPACT_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "workbench_binding_evidence": {
            "owned_tables": NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES,
            "runtime_tables": NONPROFIT_PROGRAM_IMPACT_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "form_ids": forms["form_ids"],
            "wizard_ids": wizards["wizard_ids"],
            "control_ids": controls["control_ids"],
        },
    }


def nonprofit_program_impact_render_workbench(state=None, *, tenant: str = "tenant-smoke", principal_permissions: tuple[str, ...] = ()) -> dict:
    """Render high-level workbench cards for the nonprofit impact slice."""
    contract = nonprofit_program_impact_ui_contract()
    source_state = dict(state or _sample_state())
    permissions = set(principal_permissions or tuple(dict.fromkeys(contract["action_permissions"].values())))
    visible_actions = tuple(
        action
        for action, required in contract["action_permissions"].items()
        if required in permissions
    )
    programs = tuple(item for item in source_state.get("programs", {}).values() if item.get("tenant") == tenant)
    beneficiaries = tuple(item for item in source_state.get("beneficiaries", {}).values() if item.get("tenant") == tenant)
    service_episodes = tuple(item for item in source_state.get("service_episodes", {}).values() if item.get("tenant") == tenant)
    outcomes = tuple(item for item in source_state.get("outcomes", {}).values() if item.get("tenant") == tenant)
    donor_reports = tuple(item for item in source_state.get("donor_reports", {}).values() if item.get("tenant") == tenant)
    safeguarding_incidents = tuple(item for item in source_state.get("safeguarding_incidents", {}).values() if item.get("tenant") == tenant)
    cards = (
        {"key": "active_programs", "value": len(tuple(program for program in programs if program.get("status") == "active")), "fragment": "ProgramPortfolioWorkbench"},
        {"key": "beneficiaries_enrolled", "value": len(tuple(item for item in beneficiaries if item.get("status") == "enrolled")), "fragment": "BeneficiaryImpactTimeline"},
        {
            "key": "service_completion_ratio",
            "value": round(sum(item.get("dosage_completion_ratio", 0.0) for item in service_episodes) / len(service_episodes), 4) if service_episodes else 0.0,
            "fragment": "ServiceDeliveryConsole",
        },
        {
            "key": "outcomes_on_track",
            "value": len(tuple(item for item in outcomes if item.get("status") == "on_track")),
            "fragment": "OutcomeEvidenceBoard",
        },
        {
            "key": "frozen_reports",
            "value": len(tuple(item for item in donor_reports if item.get("status") == "frozen")),
            "fragment": "DonorReportReviewWorkspace",
        },
        {
            "key": "open_safeguarding_incidents",
            "value": len(tuple(item for item in safeguarding_incidents if item.get("status") != "closed")),
            "fragment": "ImpactControlCenter",
        },
    )
    return {
        "format": "appgen.nonprofit-program-impact-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/nonprofit_program_impact",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "queues": {
            "programs_requiring_design_review": tuple(program["program_id"] for program in programs if not program.get("theory_of_change_ready", False)),
            "beneficiaries_requiring_follow_up": tuple(item["beneficiary_id"] for item in beneficiaries if item.get("status") != "enrolled"),
            "reports_waiting_for_freeze": tuple(item["report_id"] for item in donor_reports if item.get("status") != "frozen"),
        },
        "metrics": {
            "program_count": len(programs),
            "beneficiary_count": len(beneficiaries),
            "service_episode_count": len(service_episodes),
            "outcome_count": len(outcomes),
            "donor_report_count": len(donor_reports),
        },
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "binding_evidence": contract["workbench_binding_evidence"],
    }


def smoke_test() -> dict:
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = nonprofit_program_impact_ui_contract()
    rendered = nonprofit_program_impact_render_workbench(_sample_state())
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(rendered.get("cards"))
        and bool(contract.get("action_permissions"))
        and bool(contract.get("configuration_editor"))
        and contract.get("configuration_editor", {}).get("stream_engine_picker_visible") is False
        and bool(contract.get("parameter_editor"))
        and bool(contract.get("rule_editor"))
        and bool(contract.get("event_surfaces"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls")),
        "manifest": {"fragments": contract.get("fragments", ())},
        "rendered": rendered,
        "side_effects": (),
    }
