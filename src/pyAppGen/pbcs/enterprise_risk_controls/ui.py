"""UI contract for the enterprise_risk_controls PBC."""

from __future__ import annotations

from .controls import enterprise_risk_controls_control_catalog
from .events import CONSUMED
from .events import EMITTED
from .forms import enterprise_risk_controls_form_catalog
from .runtime import ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS
from .runtime import ENTERPRISE_RISK_CONTROLS_OWNED_TABLES
from .runtime import ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC
from .runtime import ENTERPRISE_RISK_CONTROLS_RUNTIME_TABLES
from .wizards import enterprise_risk_controls_wizard_catalog

ENTERPRISE_RISK_CONTROLS_UI_FRAGMENT_KEYS = (
    "EnterpriseRiskControlsWorkbench",
    "RiskRegisterConsole",
    "RiskAssessmentStudio",
    "ControlLibraryStudio",
    "ControlTestingBoard",
    "AttestationConsole",
    "RemediationTracker",
    "AssurancePacketRoom",
    "RiskCommitteeCockpit",
    "IndicatorHeatmap",
    "PolicyRuleStudio",
    "ParameterConsole",
    "ConfigurationPanel",
    "EventingMonitor",
    "AssistantPreviewWorkbench",
    "RiskWizardLauncher",
    "RiskControlCenter",
)


def enterprise_risk_controls_ui_contract() -> dict:
    from .permissions import permission_manifest

    forms = enterprise_risk_controls_form_catalog()
    wizards = enterprise_risk_controls_wizard_catalog()
    controls = enterprise_risk_controls_control_catalog()
    action_permissions = permission_manifest()["action_permissions"]
    return {
        "format": "appgen.enterprise-risk-controls-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": "enterprise_risk_controls",
        "implementation_directory": "src/pyAppGen/pbcs/enterprise_risk_controls",
        "fragments": ENTERPRISE_RISK_CONTROLS_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/enterprise_risk_controls",
            "/workbench/pbcs/enterprise_risk_controls/risks",
            "/workbench/pbcs/enterprise_risk_controls/assessments",
            "/workbench/pbcs/enterprise_risk_controls/controls",
            "/workbench/pbcs/enterprise_risk_controls/testing",
            "/workbench/pbcs/enterprise_risk_controls/attestations",
            "/workbench/pbcs/enterprise_risk_controls/remediation",
            "/workbench/pbcs/enterprise_risk_controls/assurance",
            "/workbench/pbcs/enterprise_risk_controls/rules",
            "/workbench/pbcs/enterprise_risk_controls/parameters",
            "/workbench/pbcs/enterprise_risk_controls/configuration",
            "/workbench/pbcs/enterprise_risk_controls/eventing",
            "/workbench/pbcs/enterprise_risk_controls/assistant",
            "/workbench/pbcs/enterprise_risk_controls/control-center",
        ),
        "panels": (
            {
                "key": "risk_register",
                "fragment": "RiskRegisterConsole",
                "binds_to": ("risk_register", "risk_taxonomy"),
                "commands": ("register_risk",),
            },
            {
                "key": "assessments",
                "fragment": "RiskAssessmentStudio",
                "binds_to": ("risk_assessment", "risk_indicator_observation", "risk_appetite_statement"),
                "commands": ("assess_inherent_risk",),
            },
            {
                "key": "controls",
                "fragment": "ControlLibraryStudio",
                "binds_to": ("control_library", "control_objective", "control_test", "control_attestation"),
                "commands": ("define_control", "schedule_control_test", "record_attestation"),
            },
            {
                "key": "remediation",
                "fragment": "RemediationTracker",
                "binds_to": ("control_exception", "remediation_issue", "remediation_action"),
                "commands": ("open_remediation",),
            },
            {
                "key": "assurance",
                "fragment": "AssurancePacketRoom",
                "binds_to": ("audit_evidence_packet", "risk_committee_packet"),
                "commands": ("generate_assurance_packet",),
            },
            {
                "key": "governance",
                "fragment": "PolicyRuleStudio",
                "binds_to": ("risk_policy_rule", "risk_runtime_parameter", "risk_schema_extension"),
                "commands": ("review_rules", "review_parameters"),
            },
            {
                "key": "assistant",
                "fragment": "AssistantPreviewWorkbench",
                "binds_to": ("risk_register", "control_library", "remediation_issue", "audit_evidence_packet"),
                "commands": ("query_enterprise_risk_controls_assistant_preview",),
            },
            {
                "key": "control_center",
                "fragment": "RiskControlCenter",
                "binds_to": ("risk_appetite_statement", "audit_evidence_packet", "appgen_dead_letter_event"),
                "commands": ("query_enterprise_risk_controls_controls", "review_release_evidence"),
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
                "default_appetite_model",
                "default_heatmap_view",
                "default_attestation_window_days",
                "evidence_hash_algorithm",
            ),
            "allowed_database_backends": ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "high_risk_threshold",
                "appetite_breach_margin",
                "kri_staleness_hours",
                "attestation_window_days",
                "critical_remediation_sla_days",
                "evidence_retention_days",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": (
                "risk_intake",
                "risk_appetite",
                "indicator_quality",
                "evidence",
                "attestation",
                "release_gate",
            ),
            "required_fields": ("rule_id", "scope", "condition"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": EMITTED,
            "consumes": CONSUMED,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "workbench_binding_evidence": {
            "owned_tables": ENTERPRISE_RISK_CONTROLS_OWNED_TABLES,
            "runtime_tables": ENTERPRISE_RISK_CONTROLS_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "form_ids": forms["form_ids"],
            "wizard_ids": wizards["wizard_ids"],
            "control_ids": controls["control_ids"],
        },
    }


def enterprise_risk_controls_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = enterprise_risk_controls_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action for action, required in contract["action_permissions"].items() if required in permissions
    )
    records = tuple(
        record for record in state.get("records", {}).values() if record.get("tenant", tenant) == tenant
    )
    cards = (
        {"key": "registered_risks", "value": len(records), "fragment": "RiskRegisterConsole"},
        {"key": "forms", "value": len(contract["forms"]), "fragment": "AssistantPreviewWorkbench"},
        {"key": "wizards", "value": len(contract["wizards"]), "fragment": "RiskWizardLauncher"},
        {"key": "controls", "value": len(contract["controls"]), "fragment": "RiskControlCenter"},
        {"key": "outbox_events", "value": len(state.get("outbox", ())), "fragment": "EventingMonitor"},
        {"key": "dead_letters", "value": len(state.get("dead_letter", ())), "fragment": "EventingMonitor"},
    )
    return {
        "format": "appgen.enterprise-risk-controls-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/enterprise_risk_controls",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok", True)),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "binding_evidence": contract["workbench_binding_evidence"],
    }


def smoke_test() -> dict:
    contract = enterprise_risk_controls_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = enterprise_risk_controls_render_workbench(
        {
            "configuration": {"ok": True},
            "records": {},
            "rules": {},
            "parameters": {},
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
        },
        tenant="smoke",
        principal_permissions=permissions,
    )
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(rendered.get("cards"))
        and bool(contract.get("action_permissions"))
        and bool(contract.get("configuration_editor"))
        and contract["configuration_editor"].get("stream_engine_picker_visible") is False
        and bool(contract.get("parameter_editor"))
        and bool(contract.get("rule_editor"))
        and bool(contract.get("event_surfaces"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls")),
        "contract": contract,
        "rendered": rendered,
        "side_effects": (),
    }
