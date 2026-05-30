"""Workbench, forms, wizards, and controls for the identity KYC / AML slice."""

from __future__ import annotations

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    DOMAIN_OWNED_TABLES,
    domain_capability_surface_contract,
)
from .runtime import PBC_KEY, identity_kyc_aml_compliance_build_workbench_view


def identity_kyc_aml_compliance_ui_contract():
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "IdentityKycAmlComplianceWorkbench",
            "IdentityKycAmlComplianceDetail",
            "IdentityKycAmlComplianceAssistantPanel",
            "IdentityKycAmlComplianceOnboardingWizard",
            "IdentityKycAmlComplianceReviewPacket",
        ),
        "forms": (
            "KycProfileIntakeForm",
            "IdentityDocumentForm",
            "BeneficialOwnerForm",
            "ScreeningHitResolutionForm",
            "MonitoringAlertTriageForm",
            "RiskChallengeForm",
        ),
        "wizards": (
            {
                "name": "identity_kyc_aml_compliance_onboarding_wizard",
                "steps": (
                    "classification",
                    "document_capture",
                    "screening",
                    "beneficial_ownership",
                    "edd_packet",
                    "approval_gate",
                ),
            },
            {
                "name": "identity_kyc_aml_compliance_rescreening_wizard",
                "steps": (
                    "trigger_reason",
                    "screening_scope",
                    "ownership_refresh",
                    "review_outcome",
                ),
            },
        ),
        "controls": (
            "LifecycleBadge",
            "ScreeningSeverityChip",
            "EddTriggerPill",
            "OwnershipCoverageMeter",
            "RescreeningDueDateControl",
            "AlertSlaIndicator",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "identity_kyc_aml_compliance.read",
            "identity_kyc_aml_compliance.create",
            "identity_kyc_aml_compliance.update",
            "identity_kyc_aml_compliance.approve",
            "identity_kyc_aml_compliance.admin",
            "identity_kyc_aml_compliance.operate",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "onboarding",
                "screening",
                "beneficial_ownership",
                "ongoing_monitoring",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def identity_kyc_aml_compliance_render_workbench(state=None, tenant="default"):
    ui = identity_kyc_aml_compliance_ui_contract()
    workbench = identity_kyc_aml_compliance_build_workbench_view(state=state, tenant=tenant)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "operation_actions": ui["full_capability_surface"]["operation_actions"],
        "table_browsers": ui["full_capability_surface"]["table_browsers"],
        "queues": workbench["queues"],
        "metrics": workbench["metrics"],
        "side_effects": (),
    }


def smoke_test():
    return {"ok": identity_kyc_aml_compliance_ui_contract()["ok"] and identity_kyc_aml_compliance_render_workbench()["ok"], "side_effects": ()}
