"""UI contract for the policy_administration_insurance PBC."""

from __future__ import annotations

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)
from .runtime import (
    POLICY_ADMINISTRATION_INSURANCE_ALLOWED_DATABASE_BACKENDS,
    POLICY_ADMINISTRATION_INSURANCE_CONSUMED_EVENT_TYPES,
    POLICY_ADMINISTRATION_INSURANCE_EMITTED_EVENT_TYPES,
    POLICY_ADMINISTRATION_INSURANCE_REQUIRED_EVENT_TOPIC,
)

PBC_KEY = "policy_administration_insurance"
POLICY_ADMINISTRATION_INSURANCE_UI_FRAGMENT_KEYS = (
    "PolicyAdministrationInsuranceWorkbench",
    "PolicyAdministrationInsuranceLifecyclePanel",
    "PolicyAdministrationInsuranceCoveragePanel",
    "PolicyAdministrationInsuranceTransactionQueue",
    "PolicyAdministrationInsuranceCompliancePanel",
    "PolicyAdministrationInsuranceDocumentCenter",
    "PolicyAdministrationInsuranceAssistantPanel",
)
POLICY_ADMINISTRATION_INSURANCE_FORM_KEYS = (
    "PolicyIssuanceIntakeForm",
    "CoverageScheduleForm",
    "EndorsementRequestForm",
    "RenewalDecisionForm",
    "CancellationNoticeForm",
    "BillingProjectionForm",
    "PolicyDocumentPackageForm",
    "PolicyEventInboxForm",
)
POLICY_ADMINISTRATION_INSURANCE_WIZARD_KEYS = (
    "PolicyIssuanceWizard",
    "MidTermEndorsementWizard",
    "RenewalDecisionWizard",
    "CancellationReinstatementWizard",
    "PolicyDocumentAssemblyWizard",
)
POLICY_ADMINISTRATION_INSURANCE_CONTROL_KEYS = (
    "PolicyWorkbenchSummaryCards",
    "PolicyLifecycleTimelineControl",
    "CoverageGapControl",
    "NoticeComplianceControl",
    "BillingFreshnessControl",
    "PolicyEventConsole",
)
POLICY_ADMINISTRATION_INSURANCE_ACTION_PERMISSIONS = {
    "query_workbench": f"{PBC_KEY}.read",
    "build_workbench_view": f"{PBC_KEY}.read",
    "command_insurance_policy": f"{PBC_KEY}.create",
    "create_insurance_policy": f"{PBC_KEY}.create",
    "record_coverage_item": f"{PBC_KEY}.update",
    "review_endorsement": f"{PBC_KEY}.update",
    "approve_renewal_notice": f"{PBC_KEY}.approve",
    "simulate_cancellation_event": f"{PBC_KEY}.approve",
    "create_billing_status": f"{PBC_KEY}.update",
    "record_policy_document": f"{PBC_KEY}.update",
    "register_rule": f"{PBC_KEY}.admin",
    "set_parameter": f"{PBC_KEY}.admin",
    "register_schema_extension": f"{PBC_KEY}.admin",
    "run_advanced_assessment": f"{PBC_KEY}.approve",
    "parse_document_instruction": f"{PBC_KEY}.read",
    "receive_event": f"{PBC_KEY}.update",
}


def policy_administration_insurance_form_contracts() -> dict:
    contracts = (
        {
            "key": "PolicyIssuanceIntakeForm",
            "table": "policy_administration_insurance_insurance_policy",
            "operation": "command_insurance_policy",
            "fields": (
                "policy_id",
                "tenant",
                "product_code",
                "insured_name",
                "policy_state",
                "effective_date",
                "expiration_date",
                "billing_plan",
            ),
        },
        {
            "key": "CoverageScheduleForm",
            "table": "policy_administration_insurance_coverage_item",
            "operation": "record_coverage_item",
            "fields": (
                "coverage_item_id",
                "policy_id",
                "coverage_type",
                "covered_object",
                "limit_amount",
                "deductible_amount",
                "effective_date",
                "status",
            ),
        },
        {
            "key": "EndorsementRequestForm",
            "table": "policy_administration_insurance_endorsement",
            "operation": "review_endorsement",
            "fields": (
                "endorsement_id",
                "policy_id",
                "change_type",
                "requested_effective_date",
                "accepted_effective_date",
                "premium_delta",
                "approval_status",
            ),
        },
        {
            "key": "RenewalDecisionForm",
            "table": "policy_administration_insurance_renewal_notice",
            "operation": "approve_renewal_notice",
            "fields": (
                "renewal_notice_id",
                "policy_id",
                "renewal_cycle",
                "review_status",
                "notice_deadline",
                "offered_terms",
                "decision_status",
            ),
        },
        {
            "key": "CancellationNoticeForm",
            "table": "policy_administration_insurance_cancellation_event",
            "operation": "simulate_cancellation_event",
            "fields": (
                "cancellation_event_id",
                "policy_id",
                "reason",
                "initiator",
                "notice_deadline",
                "effective_date",
                "rescission_window",
            ),
        },
        {
            "key": "BillingProjectionForm",
            "table": "policy_administration_insurance_billing_status",
            "operation": "create_billing_status",
            "fields": (
                "billing_status_id",
                "policy_id",
                "account_state",
                "amount_due",
                "delinquency_date",
                "invoice_status",
                "freshness",
            ),
        },
        {
            "key": "PolicyDocumentPackageForm",
            "table": "policy_administration_insurance_policy_document",
            "operation": "record_policy_document",
            "fields": (
                "policy_document_id",
                "policy_id",
                "document_type",
                "template_version",
                "jurisdiction",
                "delivery_status",
                "render_hash",
            ),
        },
        {
            "key": "PolicyEventInboxForm",
            "table": "policy_administration_insurance_appgen_inbox_event",
            "operation": "receive_event",
            "fields": ("event_id", "event_type", "payload", "idempotency_key"),
        },
    )
    return {
        "format": "appgen.policy-administration-insurance-form-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def policy_administration_insurance_wizard_contracts() -> dict:
    contracts = (
        {
            "key": "PolicyIssuanceWizard",
            "steps": (
                "policy_intake",
                "coverage_schedule",
                "billing_projection",
                "document_package",
                "issuance_review",
            ),
            "forms": (
                "PolicyIssuanceIntakeForm",
                "CoverageScheduleForm",
                "BillingProjectionForm",
                "PolicyDocumentPackageForm",
            ),
            "keywords": ("issue", "bind", "new policy", "quote to bind"),
        },
        {
            "key": "MidTermEndorsementWizard",
            "steps": (
                "endorsement_request",
                "coverage_delta",
                "premium_impact",
                "approval_review",
            ),
            "forms": ("EndorsementRequestForm", "CoverageScheduleForm", "BillingProjectionForm"),
            "keywords": ("endorsement", "mid term", "change coverage", "policy change"),
        },
        {
            "key": "RenewalDecisionWizard",
            "steps": (
                "renewal_review",
                "billing_verification",
                "notice_compliance",
                "offer_decision",
            ),
            "forms": ("RenewalDecisionForm", "BillingProjectionForm", "PolicyDocumentPackageForm"),
            "keywords": ("renewal", "non-renewal", "offer terms", "notice"),
        },
        {
            "key": "CancellationReinstatementWizard",
            "steps": (
                "cancellation_request",
                "notice_readiness",
                "billing_cure",
                "decision_review",
            ),
            "forms": ("CancellationNoticeForm", "BillingProjectionForm", "PolicyDocumentPackageForm"),
            "keywords": ("cancel", "nonpayment", "reinstate", "rescission"),
        },
        {
            "key": "PolicyDocumentAssemblyWizard",
            "steps": ("document_review", "package_selection", "delivery_evidence", "assistant_plan"),
            "forms": ("PolicyDocumentPackageForm", "PolicyEventInboxForm"),
            "keywords": ("document", "notice", "certificate", "binder", "delivery"),
        },
    )
    return {
        "format": "appgen.policy-administration-insurance-wizard-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def policy_administration_insurance_control_catalog() -> dict:
    contracts = (
        {
            "key": "PolicyWorkbenchSummaryCards",
            "type": "cards",
            "binds_to": ("active_policies", "open_endorsements", "renewal_queue", "outbox"),
        },
        {
            "key": "PolicyLifecycleTimelineControl",
            "type": "timeline",
            "binds_to": (
                "policy_state",
                "endorsement",
                "renewal_notice",
                "cancellation_event",
                "policy_document",
            ),
        },
        {
            "key": "CoverageGapControl",
            "type": "validation",
            "binds_to": ("coverage_item", "endorsement", "renewal_notice"),
        },
        {
            "key": "NoticeComplianceControl",
            "type": "compliance",
            "binds_to": (
                "renewal_notice",
                "cancellation_event",
                "policy_document",
            ),
        },
        {
            "key": "BillingFreshnessControl",
            "type": "projection_guard",
            "binds_to": ("billing_status", "cancellation_event", "renewal_notice"),
        },
        {
            "key": "PolicyEventConsole",
            "type": "event_console",
            "binds_to": (
                "policy_administration_insurance_appgen_outbox_event",
                "policy_administration_insurance_appgen_inbox_event",
                "policy_administration_insurance_appgen_dead_letter_event",
            ),
        },
    )
    return {
        "format": "appgen.policy-administration-insurance-control-catalog.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "side_effects": (),
    }


def policy_administration_insurance_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "format": "appgen.policy-administration-insurance-ui-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "fragments": POLICY_ADMINISTRATION_INSURANCE_UI_FRAGMENT_KEYS,
        "forms": POLICY_ADMINISTRATION_INSURANCE_FORM_KEYS,
        "wizards": POLICY_ADMINISTRATION_INSURANCE_WIZARD_KEYS,
        "controls": POLICY_ADMINISTRATION_INSURANCE_CONTROL_KEYS,
        "routes": (
            f"/workbench/pbcs/{PBC_KEY}",
            f"/workbench/pbcs/{PBC_KEY}/policies",
            f"/workbench/pbcs/{PBC_KEY}/coverage",
            f"/workbench/pbcs/{PBC_KEY}/endorsements",
            f"/workbench/pbcs/{PBC_KEY}/renewals",
            f"/workbench/pbcs/{PBC_KEY}/cancellations",
            f"/workbench/pbcs/{PBC_KEY}/documents",
            f"/workbench/pbcs/{PBC_KEY}/release-evidence",
        ),
        "panels": (
            {
                "key": "policy_lifecycle",
                "fragment": "PolicyAdministrationInsuranceLifecyclePanel",
                "binds_to": (
                    "insurance_policy",
                    "endorsement",
                    "renewal_notice",
                    "cancellation_event",
                ),
                "commands": (
                    "command_insurance_policy",
                    "review_endorsement",
                    "approve_renewal_notice",
                    "simulate_cancellation_event",
                ),
            },
            {
                "key": "coverage_and_billing",
                "fragment": "PolicyAdministrationInsuranceCoveragePanel",
                "binds_to": ("coverage_item", "billing_status"),
                "commands": ("record_coverage_item", "create_billing_status"),
            },
            {
                "key": "documents_and_compliance",
                "fragment": "PolicyAdministrationInsuranceCompliancePanel",
                "binds_to": ("policy_document", "renewal_notice", "cancellation_event"),
                "commands": ("record_policy_document", "run_advanced_assessment", "parse_document_instruction"),
            },
            {
                "key": "assistant_workspace",
                "fragment": "PolicyAdministrationInsuranceAssistantPanel",
                "binds_to": ("policy_document", "policy_administration_insurance_appgen_inbox_event"),
                "commands": ("parse_document_instruction", "receive_event", "query_workbench"),
            },
        ),
        "action_permissions": POLICY_ADMINISTRATION_INSURANCE_ACTION_PERMISSIONS,
        "configuration_editor": {
            "allowed_database_backends": POLICY_ADMINISTRATION_INSURANCE_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": POLICY_ADMINISTRATION_INSURANCE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "supported_parameters": DOMAIN_PARAMETERS,
            "bounded_parameters": DOMAIN_PARAMETERS,
        },
        "rule_editor": {
            "rule_types": DOMAIN_RULES,
            "required_fields": ("rule_id", "scope", "status"),
            "compiled_evidence_fields": ("compiled_hash",),
        },
        "event_surfaces": {
            "emits": POLICY_ADMINISTRATION_INSURANCE_EMITTED_EVENT_TYPES,
            "consumes": POLICY_ADMINISTRATION_INSURANCE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": DOMAIN_OWNED_TABLES,
            "shared_table_access": False,
            "outbox_table": "policy_administration_insurance_appgen_outbox_event",
            "inbox_table": "policy_administration_insurance_appgen_inbox_event",
            "dead_letter_table": "policy_administration_insurance_appgen_dead_letter_event",
        },
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
                "policy_lifecycle",
                "coverage_and_billing",
                "transactions",
                "documents_and_compliance",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def policy_administration_insurance_render_workbench() -> dict:
    contract = policy_administration_insurance_ui_contract()
    full = contract["full_capability_surface"]
    cards = (
        {"key": "active_policies", "value": 1, "control": "PolicyWorkbenchSummaryCards"},
        {"key": "open_endorsements", "value": 1, "control": "PolicyLifecycleTimelineControl"},
        {"key": "renewal_queue", "value": 1, "control": "NoticeComplianceControl"},
        {"key": "billing_freshness", "value": 1, "control": "BillingFreshnessControl"},
    )
    return {
        "format": "appgen.policy-administration-insurance-workbench-render.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "cards": cards,
        "operation_actions": full["operation_actions"],
        "table_browsers": full["table_browsers"],
        "forms": policy_administration_insurance_form_contracts()["contracts"],
        "wizards": policy_administration_insurance_wizard_contracts()["contracts"],
        "controls": policy_administration_insurance_control_catalog()["contracts"],
        "visible_actions": tuple(contract["action_permissions"]),
        "configuration_bound": True,
        "side_effects": (),
    }


def policy_administration_insurance_standalone_workbench_blueprint() -> dict:
    forms = policy_administration_insurance_form_contracts()
    wizards = policy_administration_insurance_wizard_contracts()
    controls = policy_administration_insurance_control_catalog()
    return {
        "format": "appgen.policy-administration-insurance-standalone-workbench.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "forms": forms["contracts"],
        "wizards": wizards["contracts"],
        "controls": controls["contracts"],
        "focus_queues": (
            "issuance_readiness",
            "endorsement_review",
            "renewal_readiness",
            "cancellation_notice_compliance",
            "document_delivery",
        ),
        "side_effects": (),
    }


def policy_administration_insurance_render_standalone_workbench(summary: dict) -> dict:
    blueprint = policy_administration_insurance_standalone_workbench_blueprint()
    cards = (
        {
            "key": "policies",
            "value": summary.get("policy_count", 0),
            "control": "PolicyWorkbenchSummaryCards",
        },
        {
            "key": "domain_operations",
            "value": summary.get("domain_operation_count", 0),
            "control": "PolicyLifecycleTimelineControl",
        },
        {
            "key": "outbox",
            "value": summary.get("outbox_count", 0),
            "control": "PolicyEventConsole",
        },
        {
            "key": "documents",
            "value": summary.get("document_plan_count", 0),
            "control": "NoticeComplianceControl",
        },
    )
    return {
        "format": "appgen.policy-administration-insurance-standalone-workbench-render.v1",
        "ok": blueprint["ok"],
        "pbc": PBC_KEY,
        "tenant": summary.get("tenant"),
        "cards": cards,
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "summary": dict(summary),
        "side_effects": (),
    }


def smoke_test() -> dict:
    contract = policy_administration_insurance_ui_contract()
    rendered = policy_administration_insurance_render_workbench()
    standalone = policy_administration_insurance_render_standalone_workbench({"tenant": "smoke"})
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract["ok"]
        and rendered["ok"]
        and standalone["ok"]
        and bool(contract["fragments"])
        and bool(contract["forms"])
        and bool(contract["wizards"])
        and bool(contract["controls"])
        and contract["configuration_editor"]["stream_engine_picker_visible"] is False,
        "contract": contract,
        "rendered": rendered,
        "standalone": standalone,
        "side_effects": (),
    }
