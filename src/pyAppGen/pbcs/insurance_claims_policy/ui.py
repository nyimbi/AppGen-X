"""UI contract for the insurance_claims_policy PBC."""

from __future__ import annotations

from .permissions import PERMISSIONS
from .standalone import InsuranceClaimsPolicyStandaloneApp
from .standalone import standalone_manifest

PBC_KEY = "insurance_claims_policy"
UI_FRAGMENTS = (
    "InsuranceClaimsPolicyWorkbench",
    "PolicyIssuanceReadinessBoard",
    "CoverageReasoningWorkbench",
    "ClaimFnolTriagePanel",
    "ReserveAuthorityConsole",
    "SettlementAuthorityRoom",
    "FraudRecoveryHub",
    "InsuranceClaimsPolicyAssistantPanel",
    "InsuranceClaimsPolicyReleasePanel",
)

ACTION_PERMISSIONS = {
    "configure_runtime": "insurance_claims_policy.admin",
    "create_policy": "insurance_claims_policy.create",
    "update_policy": "insurance_claims_policy.update",
    "approve_coverage": "insurance_claims_policy.approve",
    "approve_reserve": "insurance_claims_policy.approve",
    "approve_settlement": "insurance_claims_policy.approve",
    "review_fraud": "insurance_claims_policy.approve",
    "view_workbench": "insurance_claims_policy.read",
}

FORMS = (
    {"id": "policy_intake_form", "binds_to": "insurance_policy", "fields": ("policy_number", "product_code", "policy_state", "premium_status")},
    {"id": "claim_fnol_form", "binds_to": "claim_record", "fields": ("claim_number", "loss_date", "severity_band", "claim_stage")},
    {"id": "reserve_review_form", "binds_to": "claim_reserve", "fields": ("reserve_type", "recommended_amount", "approved_amount", "adequacy_band")},
    {"id": "settlement_offer_form", "binds_to": "settlement_offer", "fields": ("offer_amount", "negotiation_status", "authority_required", "expires_at")},
)

WIZARDS = (
    {"id": "policy_to_claim_wizard", "steps": ("capture_policy", "bind_coverages", "collect_fnol", "determine_coverage")},
    {"id": "reserve_to_settlement_wizard", "steps": ("set_reserve", "score_fraud", "adjudicate_claim", "create_settlement_offer", "execute_payment")},
    {"id": "recovery_wizard", "steps": ("identify_third_party", "record_recovery", "track_deadlines", "close_recovery")},
)

CONTROLS = (
    {"id": "coverage_reasoning_control", "type": "decision_panel", "targets": ("coverage_determination", "policy_coverage", "claim_document")},
    {"id": "fraud_escalation_control", "type": "threshold_slider", "targets": ("fraud_indicator", "claim_exception_case")},
    {"id": "reserve_authority_control", "type": "approval_matrix", "targets": ("claim_reserve", "reserve_change", "settlement_offer")},
    {"id": "release_evidence_control", "type": "status_board", "targets": ("insurance_control_assertion", "insurance_governed_model")},
)


def insurance_claims_policy_standalone_app_contract() -> dict:
    manifest = standalone_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "app_id": "insurance_claims_policy_one_pbc_app",
        "fragments": UI_FRAGMENTS,
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "workflows": manifest["workflows"],
        "side_effects": (),
    }


def insurance_claims_policy_ui_contract() -> dict:
    return {
        "format": "appgen.insurance-claims-policy-ui-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/insurance_claims_policy",
        "fragments": UI_FRAGMENTS,
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "routes": (
            "/workbench/pbcs/insurance_claims_policy",
            "/workbench/pbcs/insurance_claims_policy/policies",
            "/workbench/pbcs/insurance_claims_policy/claims",
            "/workbench/pbcs/insurance_claims_policy/coverage",
            "/workbench/pbcs/insurance_claims_policy/reserves",
            "/workbench/pbcs/insurance_claims_policy/fraud",
            "/workbench/pbcs/insurance_claims_policy/settlement",
            "/workbench/pbcs/insurance_claims_policy/recovery",
            "/workbench/pbcs/insurance_claims_policy/release",
        ),
        "panels": (
            {"key": "issuance", "fragment": "PolicyIssuanceReadinessBoard", "commands": ("create_insurance_policy", "register_policy_holder", "define_policy_coverage", "record_endorsement")},
            {"key": "claims", "fragment": "ClaimFnolTriagePanel", "commands": ("open_claim", "record_loss_event", "attach_claim_document", "determine_coverage")},
            {"key": "reserves", "fragment": "ReserveAuthorityConsole", "commands": ("set_claim_reserve", "record_reserve_change")},
            {"key": "settlement", "fragment": "SettlementAuthorityRoom", "commands": ("adjudicate_claim", "create_settlement_offer", "execute_settlement_payment")},
            {"key": "fraud_and_recovery", "fragment": "FraudRecoveryHub", "commands": ("score_fraud_indicator", "record_subrogation_recovery", "resolve_claim_exception")},
            {"key": "release", "fragment": "InsuranceClaimsPolicyReleasePanel", "commands": ("release_snapshot",)},
        ),
        "action_permissions": ACTION_PERMISSIONS,
        "available_permissions": PERMISSIONS,
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_policy_form", "tenant_isolation_mode", "workbench_limit"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
        },
        "parameter_editor": {"numeric_parameters": ("reserve_review_threshold", "settlement_authority_limit", "fraud_score_threshold", "premium_grace_days", "claim_sla_days", "workbench_limit")},
        "rule_editor": {"rule_types": ("coverage", "reserve", "settlement", "fraud", "billing", "subrogation"), "compiled_evidence_required": True},
        "side_effects": (),
    }


def insurance_claims_policy_render_workbench(state: dict | None = None, *, tenant: str = "default", principal_permissions: tuple[str, ...] | None = None) -> dict:
    app = InsuranceClaimsPolicyStandaloneApp(state=state)
    workbench = app.workbench(tenant=tenant, permissions=principal_permissions or PERMISSIONS)
    contract = insurance_claims_policy_ui_contract()
    allowed = set(principal_permissions or PERMISSIONS)
    visible_actions = tuple(action for action, permission in ACTION_PERMISSIONS.items() if permission in allowed)
    return {
        "format": "appgen.insurance-claims-policy-workbench-render.v1",
        "ok": workbench["ok"],
        "tenant": tenant,
        "route": "/workbench/pbcs/insurance_claims_policy",
        "fragments": contract["fragments"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "workbench": workbench,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in ACTION_PERMISSIONS if action not in visible_actions),
        "shell": {
            "app_id": "insurance_claims_policy_one_pbc_app",
            "title": "Insurance Claims Policy Command Center",
            "sections": ("issuance", "claims", "coverage", "reserves", "settlement", "fraud", "recovery", "release"),
        },
        "side_effects": (),
    }


def insurance_claims_policy_render_standalone_app(state: dict | None = None, *, tenant: str = "default", principal_permissions: tuple[str, ...] | None = None) -> dict:
    return insurance_claims_policy_render_workbench(state, tenant=tenant, principal_permissions=principal_permissions)


def smoke_test() -> dict:
    app = InsuranceClaimsPolicyStandaloneApp()
    app.load_demo_workspace(tenant="tenant_demo")
    contract = insurance_claims_policy_ui_contract()
    rendered = insurance_claims_policy_render_workbench(app.state, tenant="tenant_demo", principal_permissions=PERMISSIONS)
    standalone = insurance_claims_policy_standalone_app_contract()
    return {
        "ok": contract["ok"] and rendered["ok"] and standalone["ok"] and bool(contract["forms"]) and bool(contract["wizards"]) and bool(contract["controls"]),
        "contract": contract,
        "rendered": rendered,
        "standalone": standalone,
        "side_effects": (),
    }
