"""UI contract for provider_revenue_cycle."""

from __future__ import annotations

from .controls import provider_revenue_cycle_control_catalog
from .forms import provider_revenue_cycle_form_catalog
from .permissions import permission_manifest
from .runtime import PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS
from .runtime import PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES
from .runtime import PROVIDER_REVENUE_CYCLE_OWNED_TABLES
from .runtime import PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC
from .runtime import PROVIDER_REVENUE_CYCLE_RUNTIME_TABLES
from .runtime import PROVIDER_REVENUE_CYCLE_UI_FRAGMENT_KEYS
from .runtime import provider_revenue_cycle_build_workbench_view
from .runtime import provider_revenue_cycle_runtime_smoke
from .wizards import provider_revenue_cycle_wizard_catalog


def provider_revenue_cycle_ui_contract() -> dict:
    forms = provider_revenue_cycle_form_catalog()
    wizards = provider_revenue_cycle_wizard_catalog()
    controls = provider_revenue_cycle_control_catalog()
    permissions = permission_manifest()
    return {
        "format": "appgen.provider-revenue-cycle-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": "provider_revenue_cycle",
        "implementation_directory": "src/pyAppGen/pbcs/provider_revenue_cycle",
        "fragments": PROVIDER_REVENUE_CYCLE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/provider_revenue_cycle",
            "/workbench/pbcs/provider_revenue_cycle/intake",
            "/workbench/pbcs/provider_revenue_cycle/eligibility-and-auth",
            "/workbench/pbcs/provider_revenue_cycle/charge-and-coding",
            "/workbench/pbcs/provider_revenue_cycle/claims",
            "/workbench/pbcs/provider_revenue_cycle/era-and-underpayments",
            "/workbench/pbcs/provider_revenue_cycle/denials",
            "/workbench/pbcs/provider_revenue_cycle/patient-balance",
            "/workbench/pbcs/provider_revenue_cycle/controls",
            "/workbench/pbcs/provider_revenue_cycle/assistant",
        ),
        "panels": (
            {"key": "intake", "fragment": "PatientAccountIntakeBoard", "binds_to": ("patient_account",), "commands": ("command_patient_account_intake",)},
            {"key": "eligibility", "fragment": "EligibilityAndAuthorizationConsole", "binds_to": ("patient_account",), "commands": ("command_eligibility_benefits_review", "command_prior_authorization_link")},
            {"key": "charge_coding", "fragment": "ChargeAndCodingConsole", "binds_to": ("charge_capture", "coding_case"), "commands": ("command_charge_capture", "command_coding_review")},
            {"key": "claims", "fragment": "ClaimSubmissionWorkbench", "binds_to": ("claim_batch",), "commands": ("command_claim_create", "command_claim_scrub", "command_claim_submission")},
            {"key": "era_underpayments", "fragment": "ERAAndUnderpaymentConsole", "binds_to": ("payment_posting", "denial_case"), "commands": ("command_remit_era_posting",)},
            {"key": "denials", "fragment": "DenialAppealsWorkbench", "binds_to": ("denial_case",), "commands": ("command_denial_open", "command_denial_appeal")},
            {"key": "patient_balance", "fragment": "PatientBalanceResolutionWorkbench", "binds_to": ("collection_account",), "commands": ("command_patient_statement_issue", "command_payment_plan_enroll", "command_financial_assistance", "command_refund_credit_issue")},
            {"key": "close_controls", "fragment": "RevenueCloseAndControlsCenter", "binds_to": ("control_assertion",), "commands": ("command_reconcile_close", "query_provider_revenue_cycle_controls")},
            {"key": "assistant", "fragment": "ProviderRevenueCycleAssistantPanel", "binds_to": ("control_assertion",), "commands": ("query_provider_revenue_cycle_assistant_preview",)},
        ),
        "action_permissions": permissions["action_permissions"],
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "workbench_limit"),
            "allowed_database_backends": PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "workbench_limit",
                "materiality_threshold",
                "timely_filing_warning_days",
                "underpayment_variance_threshold",
                "default_payment_plan_term_months",
                "charity_auto_hold_threshold",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": (
                "registration_gate",
                "claim_scrub",
                "payer_contract",
                "denial_appeal",
                "patient_balance_protection",
                "close_gate",
            ),
            "required_fields": ("rule_id", "rule_type", "status"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": ("ProviderRevenueCycleCreated", "ProviderRevenueCycleUpdated", "ProviderRevenueCycleApproved", "ProviderRevenueCycleExceptionOpened"),
            "consumes": PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "workbench_binding_evidence": {
            "owned_tables": PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
            "runtime_tables": PROVIDER_REVENUE_CYCLE_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "form_ids": forms["form_ids"],
            "wizard_ids": wizards["wizard_ids"],
            "control_ids": controls["control_ids"],
        },
    }


def provider_revenue_cycle_render_workbench(state=None, *, tenant: str = "tenant-smoke", principal_permissions: tuple[str, ...] = ()) -> dict:
    contract = provider_revenue_cycle_ui_contract()
    permissions = set(principal_permissions or tuple(dict.fromkeys(contract["action_permissions"].values())))
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    source_state = state or provider_revenue_cycle_runtime_smoke()["state"]
    workbench = provider_revenue_cycle_build_workbench_view(state=source_state, tenant=tenant)
    cards = (
        {"key": "accounts", "value": workbench["metrics"]["accounts"], "fragment": "PatientAccountIntakeBoard"},
        {"key": "claims", "value": workbench["metrics"]["claims"], "fragment": "ClaimSubmissionWorkbench"},
        {"key": "denials_open", "value": workbench["metrics"]["denials_open"], "fragment": "DenialAppealsWorkbench"},
        {"key": "underpayments", "value": workbench["metrics"]["underpayments_open"], "fragment": "ERAAndUnderpaymentConsole"},
        {"key": "patient_balance_total", "value": workbench["metrics"]["patient_balance_total"], "fragment": "PatientBalanceResolutionWorkbench"},
    )
    return {
        "format": "appgen.provider-revenue-cycle-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/provider_revenue_cycle",
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
    contract = provider_revenue_cycle_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = provider_revenue_cycle_render_workbench(
        provider_revenue_cycle_runtime_smoke()["state"],
        tenant="tenant-smoke",
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
