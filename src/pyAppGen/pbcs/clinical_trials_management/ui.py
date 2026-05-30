"""UI contract for the clinical_trials_management PBC."""

from __future__ import annotations

from .controls import clinical_trials_management_control_catalog
from .forms import clinical_trials_management_form_catalog
from .runtime import CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES
from .runtime import CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES
from .runtime import CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .runtime import CLINICAL_TRIALS_MANAGEMENT_RUNTIME_TABLES
from .runtime import clinical_trials_management_build_workbench_view
from .runtime import clinical_trials_management_runtime_smoke
from .wizards import clinical_trials_management_wizard_catalog
from .trial_control import TRIAL_CONTROL_CAPABILITIES
from .trial_control import improve1_trial_control_contract


CLINICAL_TRIALS_MANAGEMENT_UI_FRAGMENT_KEYS = (
    "ClinicalTrialsOperationsWorkbench",
    "ProtocolAmendmentBoard",
    "SiteActivationBoard",
    "ScreeningQueue",
    "ConsentAndVisitConsole",
    "SafetyReportingConsole",
    "MonitoringFindingsConsole",
    "DataLockReadinessBoard",
    "TrialRuleStudio",
    "RuntimeParameterConsole",
    "AssistantPreviewWorkbench",
    "ClinicalTrialWizardLauncher",
    "ClinicalTrialsControlCenter",
)


def clinical_trials_management_ui_contract() -> dict:
    """Return workbench metadata for the one-PBC clinical trials app."""
    from .permissions import permission_manifest

    forms = clinical_trials_management_form_catalog()
    wizards = clinical_trials_management_wizard_catalog()
    controls = clinical_trials_management_control_catalog()
    action_permissions = permission_manifest()["action_permissions"]
    return {
        "format": "appgen.clinical-trials-management-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": "clinical_trials_management",
        "implementation_directory": "src/pyAppGen/pbcs/clinical_trials_management",
        "fragments": CLINICAL_TRIALS_MANAGEMENT_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/clinical_trials_management",
            "/workbench/pbcs/clinical_trials_management/protocols",
            "/workbench/pbcs/clinical_trials_management/sites",
            "/workbench/pbcs/clinical_trials_management/subjects",
            "/workbench/pbcs/clinical_trials_management/consent-and-visits",
            "/workbench/pbcs/clinical_trials_management/safety",
            "/workbench/pbcs/clinical_trials_management/monitoring",
            "/workbench/pbcs/clinical_trials_management/governance",
            "/workbench/pbcs/clinical_trials_management/assistant",
            "/workbench/pbcs/clinical_trials_management/controls",
        ),
        "panels": (
            {
                "key": "protocols",
                "fragment": "ProtocolAmendmentBoard",
                "binds_to": ("trial_protocol", "policy_rule"),
                "commands": ("command_trial_protocols", "command_policy_rules"),
            },
            {
                "key": "site_activation",
                "fragment": "SiteActivationBoard",
                "binds_to": ("study_site", "trial_protocol"),
                "commands": ("command_study_sites",),
            },
            {
                "key": "screening",
                "fragment": "ScreeningQueue",
                "binds_to": ("subject", "consent_record"),
                "commands": ("command_subjects", "command_consent_records"),
            },
            {
                "key": "visits",
                "fragment": "ConsentAndVisitConsole",
                "binds_to": ("consent_record", "visit_schedule"),
                "commands": ("command_visit_schedules",),
            },
            {
                "key": "safety",
                "fragment": "SafetyReportingConsole",
                "binds_to": ("adverse_event",),
                "commands": ("command_adverse_events",),
            },
            {
                "key": "monitoring",
                "fragment": "MonitoringFindingsConsole",
                "binds_to": ("monitoring_finding",),
                "commands": ("command_monitoring_findings",),
            },
            {
                "key": "governance",
                "fragment": "TrialRuleStudio",
                "binds_to": ("policy_rule", "runtime_parameter"),
                "commands": ("command_policy_rules", "command_runtime_parameters"),
            },
            {
                "key": "assistant",
                "fragment": "AssistantPreviewWorkbench",
                "binds_to": ("trial_protocol", "study_site", "subject", "consent_record", "visit_schedule", "adverse_event", "monitoring_finding"),
                "commands": ("query_clinical_trials_management_assistant_preview",),
            },
            {
                "key": "controls",
                "fragment": "ClinicalTrialsControlCenter",
                "binds_to": ("control_assertion", "monitoring_finding", "adverse_event"),
                "commands": ("query_clinical_trials_management_controls", "assess_lock_readiness"),
            },
        ),
        "action_permissions": action_permissions,
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "default_timezone",
                "default_jurisdiction",
                "retry_limit",
            ),
            "allowed_database_backends": CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "screening_window_days",
                "visit_window_grace_days",
                "serious_event_reporting_hours",
                "monitoring_followup_days",
                "reconsent_notice_days",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("protocol_gate", "site_activation", "consent", "eligibility", "safety", "privacy"),
            "required_fields": ("rule_id", "rule_type", "scope", "status", "condition"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": ("ClinicalTrialProtocolRegistered", "ClinicalTrialSiteActivated", "ClinicalTrialSeriousAdverseEventReported"),
            "consumes": CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "trial_control_panels": tuple(f"trial_control_{capability}" for capability in TRIAL_CONTROL_CAPABILITIES),
        "trial_control_contract": improve1_trial_control_contract(),
        "workbench_binding_evidence": {
            "owned_tables": CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
            "runtime_tables": CLINICAL_TRIALS_MANAGEMENT_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "form_ids": forms["form_ids"],
            "wizard_ids": wizards["wizard_ids"],
            "control_ids": controls["control_ids"],
            "trial_control_count": len(TRIAL_CONTROL_CAPABILITIES),
        },
    }


def clinical_trials_management_render_workbench(state=None, *, tenant: str = "tenant-smoke", principal_permissions: tuple[str, ...] = ()) -> dict:
    """Render high-level workbench cards for the clinical trials slice."""
    contract = clinical_trials_management_ui_contract()
    permissions = set(principal_permissions or tuple(dict.fromkeys(contract["action_permissions"].values())))
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    source_state = state or clinical_trials_management_runtime_smoke()["state"]
    workbench = clinical_trials_management_build_workbench_view(tenant, source_state)
    cards = (
        {"key": "active_protocols", "value": workbench["metrics"]["active_protocols"], "fragment": "ProtocolAmendmentBoard"},
        {"key": "active_sites", "value": workbench["metrics"]["active_sites"], "fragment": "SiteActivationBoard"},
        {"key": "enrolled_subjects", "value": workbench["metrics"]["enrolled_subjects"], "fragment": "ScreeningQueue"},
        {"key": "serious_events", "value": workbench["metrics"]["serious_events"], "fragment": "SafetyReportingConsole"},
        {"key": "open_findings", "value": workbench["metrics"]["open_findings"], "fragment": "MonitoringFindingsConsole"},
        {"key": "lock_ready", "value": workbench["metrics"]["lock_ready"], "fragment": "DataLockReadinessBoard"},
    )
    return {
        "format": "appgen.clinical-trials-management-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/clinical_trials_management",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "queues": workbench["queues"],
        "metrics": workbench["metrics"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "binding_evidence": contract["workbench_binding_evidence"],
    }


def smoke_test() -> dict:
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = clinical_trials_management_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = clinical_trials_management_render_workbench(
        clinical_trials_management_runtime_smoke()["state"],
        tenant="tenant-smoke",
        principal_permissions=permissions,
    )
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(contract.get("cards") if "cards" in contract else rendered.get("cards"))
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


def clinical_trials_management_standalone_app_contract() -> dict:
    contract = clinical_trials_management_ui_contract()
    return {
        "ok": contract["ok"] and len(contract["forms"]) >= 10 and len(contract["wizards"]) >= 4 and len(contract["controls"]) >= 5,
        "pbc": "clinical_trials_management",
        "app_id": "clinical_trials_management_one_pbc_app",
        "fragments": contract["fragments"],
        "routes": contract["routes"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "workbench_sections": (
            "protocol_governance",
            "site_activation",
            "subject_screening",
            "consent_and_visits",
            "safety_reporting",
            "monitoring_findings",
            "data_lock_readiness",
            "assistant_preview",
        ),
        "agent_skill_namespace": "clinical_trials_management_skills",
        "configuration_editor": contract["configuration_editor"],
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }
