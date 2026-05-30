"""UI, forms, and workbench contracts for insurance underwriting."""

from __future__ import annotations

from .domain_depth import domain_capability_surface_contract
from .permissions import ACTION_PERMISSIONS, permission_manifest


PBC_KEY = "insurance_underwriting"
UI_FRAGMENT_KEYS = (
    "InsuranceUnderwritingWorkbench",
    "InsuranceUnderwritingDetail",
    "InsuranceUnderwritingAssistantPanel",
    "SubmissionDetailPanel",
    "ReferralQueueBoard",
    "QuoteScenarioDesk",
    "BindReadinessBoard",
    "UnderwriterAssistantPanel",
    "GovernanceStudio",
    "ReleaseEvidencePanel",
)
FORM_KEYS = (
    "SubmissionIntakeForm",
    "RiskProfileForm",
    "RatingWorksheetForm",
    "QuoteScenarioForm",
    "DecisionReviewForm",
    "BindReadinessForm",
    "ExclusionForm",
    "RuleEditorForm",
    "ParameterTuningForm",
    "EventInboxForm",
)
WIZARD_KEYS = (
    "UnderwritingIntakeWizard",
    "QuoteApprovalWizard",
    "BindReadinessWizard",
    "GovernanceTuningWizard",
    "AssistantDocumentIntakeWizard",
)
CONTROL_KEYS = (
    "WorkbenchSummaryCards",
    "ReferralSlaBoard",
    "QuoteScenarioMatrix",
    "SubjectivityChecklist",
    "EventOpsConsole",
)


def insurance_underwriting_form_contracts() -> dict:
    contracts = (
        {"key": "SubmissionIntakeForm", "table": "insurance_underwriting_underwriting_submission", "operation": "create_submission", "fields": ("submission_id", "tenant", "product_line", "applicant_name", "jurisdiction", "requested_limit", "declared_revenue", "effective_date", "exposure_locations", "documents")},
        {"key": "RiskProfileForm", "table": "insurance_underwriting_risk_profile", "operation": "build_risk_profile", "fields": ("risk_profile_id", "submission_id", "industry_code", "hazard_factors", "catastrophe_score", "prior_loss_count", "financial_signals")},
        {"key": "RatingWorksheetForm", "table": "insurance_underwriting_rating_factor", "operation": "review_rating_factor", "fields": ("factor_id", "submission_id", "factor_type", "selected_value", "weight", "source", "override_reason")},
        {"key": "QuoteScenarioForm", "table": "insurance_underwriting_quote", "operation": "generate_quote", "fields": ("quote_id", "submission_id", "scenario_name", "base_rate", "subjectivities", "exclusions")},
        {"key": "DecisionReviewForm", "table": "insurance_underwriting_underwriting_decision", "operation": "issue_underwriting_decision", "fields": ("decision_id", "submission_id", "quote_id", "authority_level", "approved_by", "rationale")},
        {"key": "BindReadinessForm", "table": "insurance_underwriting_bind_package", "operation": "assemble_bind_package", "fields": ("bind_package_id", "submission_id", "quote_id", "subjectivities", "documents", "payment_confirmed")},
        {"key": "ExclusionForm", "table": "insurance_underwriting_exclusion", "operation": "record_exclusion", "fields": ("exclusion_id", "submission_id", "quote_id", "clause_code", "reason", "customer_explanation", "approved_by")},
        {"key": "RuleEditorForm", "table": "insurance_underwriting_insurance_underwriting_policy_rule", "operation": "register_rule", "fields": ("rule_id", "rule_type", "version", "status", "definition")},
        {"key": "ParameterTuningForm", "table": "insurance_underwriting_insurance_underwriting_runtime_parameter", "operation": "set_parameter", "fields": ("parameter_name", "value", "bounded_min", "bounded_max")},
        {"key": "EventInboxForm", "table": "insurance_underwriting_appgen_inbox_event", "operation": "receive_event", "fields": ("event_type", "source_pbc", "payload", "idempotency_key")},
    )
    return {"format": "appgen.insurance-underwriting-form-contract.v1", "ok": True, "pbc": PBC_KEY, "contracts": contracts, "side_effects": ()}


def insurance_underwriting_wizard_contracts() -> dict:
    contracts = (
        {"key": "UnderwritingIntakeWizard", "steps": ("submission", "risk_profile", "rating_factor"), "forms": ("SubmissionIntakeForm", "RiskProfileForm", "RatingWorksheetForm"), "keywords": ("new submission", "intake", "quote")},
        {"key": "QuoteApprovalWizard", "steps": ("rating", "quote", "decision", "exclusion"), "forms": ("RatingWorksheetForm", "QuoteScenarioForm", "DecisionReviewForm", "ExclusionForm"), "keywords": ("quote", "decision", "approve", "decline", "refer")},
        {"key": "BindReadinessWizard", "steps": ("decision", "subjectivities", "bind"), "forms": ("DecisionReviewForm", "BindReadinessForm"), "keywords": ("bind", "subjectivity", "ready to bind")},
        {"key": "GovernanceTuningWizard", "steps": ("rule", "parameter", "control"), "forms": ("RuleEditorForm", "ParameterTuningForm"), "keywords": ("rule", "parameter", "governance")},
        {"key": "AssistantDocumentIntakeWizard", "steps": ("document_review", "fact_extraction", "crud_plan"), "forms": ("EventInboxForm", "SubmissionIntakeForm"), "keywords": ("document", "loss run", "inspection", "application")},
    )
    return {"format": "appgen.insurance-underwriting-wizard-contract.v1", "ok": True, "pbc": PBC_KEY, "contracts": contracts, "side_effects": ()}


def insurance_underwriting_control_catalog() -> dict:
    contracts = (
        {"key": "WorkbenchSummaryCards", "type": "cards", "binds_to": ("submission_count", "referral_queue_count", "quotes_expiring_count", "bind_ready_count")},
        {"key": "ReferralSlaBoard", "type": "queue", "binds_to": ("referrals",)},
        {"key": "QuoteScenarioMatrix", "type": "comparison", "binds_to": ("quotes_expiring", "premium", "rate")},
        {"key": "SubjectivityChecklist", "type": "checklist", "binds_to": ("bind_ready", "subjectivities")},
        {"key": "EventOpsConsole", "type": "event_console", "binds_to": ("outbox_count", "inbox_count", "dead_letter_count")},
    )
    return {"format": "appgen.insurance-underwriting-control-catalog.v1", "ok": True, "pbc": PBC_KEY, "contracts": contracts, "side_effects": ()}


def insurance_underwriting_ui_contract() -> dict:
    permissions = permission_manifest()
    surface = domain_capability_surface_contract()
    return {
        "format": "appgen.insurance-underwriting-ui-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/insurance_underwriting",
        "fragments": UI_FRAGMENT_KEYS,
        "forms": FORM_KEYS,
        "wizards": WIZARD_KEYS,
        "controls": CONTROL_KEYS,
        "routes": (
            "/workbench/pbcs/insurance_underwriting",
            "/workbench/pbcs/insurance_underwriting/submissions",
            "/workbench/pbcs/insurance_underwriting/referrals",
            "/workbench/pbcs/insurance_underwriting/quotes",
            "/workbench/pbcs/insurance_underwriting/bind-readiness",
            "/workbench/pbcs/insurance_underwriting/governance",
            "/workbench/pbcs/insurance_underwriting/release-evidence",
        ),
        "panels": (
            {"key": "submission_intake", "fragment": "SubmissionDetailPanel", "binds_to": ("underwriting_submission", "risk_profile"), "commands": ("create_submission", "build_risk_profile", "run_submission_intake_workflow")},
            {"key": "referrals", "fragment": "ReferralQueueBoard", "binds_to": ("underwriting_submission", "underwriting_decision"), "commands": ("issue_underwriting_decision",)},
            {"key": "quote_scenarios", "fragment": "QuoteScenarioDesk", "binds_to": ("rating_factor", "quote", "exclusion"), "commands": ("review_rating_factor", "generate_quote", "record_exclusion")},
            {"key": "bind_readiness", "fragment": "BindReadinessBoard", "binds_to": ("bind_package",), "commands": ("assemble_bind_package", "run_quote_to_bind_workflow")},
            {"key": "assistant", "fragment": "UnderwriterAssistantPanel", "binds_to": ("underwriting_submission", "quote", "bind_package"), "commands": ("document_instruction_plan", "datastore_crud_plan")},
            {"key": "governance", "fragment": "GovernanceStudio", "binds_to": ("insurance_underwriting_policy_rule", "insurance_underwriting_runtime_parameter"), "commands": ("register_rule", "set_parameter")},
        ),
        "action_permissions": permissions["action_permissions"],
        "configuration_editor": {
            "supported_fields": ("database_backend", "event_topic", "workbench_limit", "appetite_mode", "default_authority_level", "assistant_requires_citations"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "supported_parameters": ("quality_score_floor", "risk_threshold", "quote_validity_days", "auto_bind_limit", "referral_sla_hours", "max_override_delta_pct"),
        },
        "rule_editor": {
            "rule_types": ("completeness", "appetite", "override", "authority", "bind"),
            "required_fields": ("rule_id", "rule_type", "description"),
        },
        "stream_engine_picker_visible": False,
        "full_capability_surface": surface,
        "side_effects": (),
    }


def insurance_underwriting_standalone_workbench_blueprint() -> dict:
    return {
        "format": "appgen.insurance-underwriting-standalone-workbench-blueprint.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "forms": insurance_underwriting_form_contracts()["contracts"],
        "wizards": insurance_underwriting_wizard_contracts()["contracts"],
        "controls": insurance_underwriting_control_catalog()["contracts"],
        "ui": insurance_underwriting_ui_contract(),
        "side_effects": (),
    }


def insurance_underwriting_render_workbench(
    workbench: dict,
    *,
    principal_permissions: tuple[str, ...] = tuple(permission_manifest()["permissions"]),
) -> dict:
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action for action, permission in ACTION_PERMISSIONS.items() if permission in permissions
    )
    cards = (
        {"key": "submissions", "value": workbench.get("submission_count", 0), "fragment": "InsuranceUnderwritingWorkbench"},
        {"key": "referrals", "value": workbench.get("referral_queue_count", 0), "fragment": "ReferralQueueBoard"},
        {"key": "quotes_expiring", "value": workbench.get("quotes_expiring_count", 0), "fragment": "QuoteScenarioDesk"},
        {"key": "bind_ready", "value": workbench.get("bind_ready_count", 0), "fragment": "BindReadinessBoard"},
        {"key": "dead_letters", "value": workbench.get("dead_letter_count", 0), "fragment": "ReleaseEvidencePanel"},
    )
    return {
        "format": "appgen.insurance-underwriting-workbench-render.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "route": "/workbench/pbcs/insurance_underwriting",
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in ACTION_PERMISSIONS if action not in visible_actions),
        "queues": workbench.get("queues", {}),
        "forms": insurance_underwriting_form_contracts()["contracts"],
        "wizards": insurance_underwriting_wizard_contracts()["contracts"],
        "controls": insurance_underwriting_control_catalog()["contracts"],
        "workbench_view": True,
        "side_effects": (),
    }


def insurance_underwriting_render_standalone_workbench(workbench: dict) -> dict:
    return insurance_underwriting_render_workbench(workbench)


def smoke_test() -> dict:
    blueprint = insurance_underwriting_standalone_workbench_blueprint()
    rendered = insurance_underwriting_render_workbench(
        {
            "submission_count": 1,
            "referral_queue_count": 1,
            "quotes_expiring_count": 0,
            "bind_ready_count": 0,
            "dead_letter_count": 0,
            "queues": {"referrals": ("sub-1",)},
        }
    )
    return {"ok": blueprint["ok"] and rendered["ok"] and insurance_underwriting_ui_contract()["ok"], "blueprint": blueprint, "rendered": rendered, "side_effects": ()}
