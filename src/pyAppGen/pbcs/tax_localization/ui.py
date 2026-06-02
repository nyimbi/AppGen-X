"""UI contract for the Tax Localization PBC."""

from __future__ import annotations

from .app_surface import single_pbc_tax_localization_contract
from .controls import tax_localization_control_catalog
from .forms import tax_localization_form_catalog
from .runtime import TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS
from .runtime import TAX_LOCALIZATION_CONSUMED_EVENT_TYPES
from .runtime import TAX_LOCALIZATION_EMITTED_EVENT_TYPES
from .runtime import TAX_LOCALIZATION_OWNED_TABLES
from .runtime import TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC
from .runtime import tax_localization_permissions_contract
from .wizards import tax_localization_wizard_catalog


TAX_LOCALIZATION_UI_FRAGMENT_KEYS = (
    "TaxLocalizationWorkbench",
    "JurisdictionMasterConsole",
    "TaxRuleAuthoringStudio",
    "ProductTaxabilityClassifier",
    "TaxQuoteWorkbench",
    "InvoiceTaxRecordingView",
    "FilingPreparationConsole",
    "ExemptionCertificatePanel",
    "CrossBorderDutiesPanel",
    "AuthorityChannelMonitor",
    "TaxReconciliationBoard",
    "DigitalTaxDocumentView",
    "TaxRiskPanel",
    "TaxGovernanceRuleStudio",
    "TaxParameterConsole",
    "TaxConfigurationPanel",
    "TaxAssistantPreviewPanel",
    "TaxWizardLauncher",
    "TaxControlCenter",
)


def tax_localization_ui_contract() -> dict:
    forms = tax_localization_form_catalog()
    wizards = tax_localization_wizard_catalog()
    controls = tax_localization_control_catalog()
    action_permissions = tax_localization_permissions_contract()["action_permissions"]
    return {
        "format": "appgen.tax-localization-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": "tax_localization",
        "implementation_directory": "src/pyAppGen/pbcs/tax_localization",
        "fragments": TAX_LOCALIZATION_UI_FRAGMENT_KEYS,
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "single_pbc_app": single_pbc_tax_localization_contract(),
        "routes": (
            "/workbench/pbcs/tax_localization",
            "/workbench/pbcs/tax_localization/jurisdictions",
            "/workbench/pbcs/tax_localization/tax-rules",
            "/workbench/pbcs/tax_localization/quotes",
            "/workbench/pbcs/tax_localization/invoices",
            "/workbench/pbcs/tax_localization/filings",
            "/workbench/pbcs/tax_localization/exemptions",
            "/workbench/pbcs/tax_localization/reconciliation",
            "/workbench/pbcs/tax_localization/configuration",
            "/workbench/pbcs/tax_localization/assistant",
            "/workbench/pbcs/tax_localization/controls",
        ),
        "panels": (
            {
                "key": "jurisdictions",
                "fragment": "JurisdictionMasterConsole",
                "binds_to": ("tax_jurisdiction", "tax_filing_calendar", "tax_nexus_profile"),
                "commands": ("register_jurisdiction",),
            },
            {
                "key": "rules",
                "fragment": "TaxRuleAuthoringStudio",
                "binds_to": ("tax_rule", "tax_rule_version", "tax_rule_impact_analysis"),
                "commands": ("register_tax_rule", "register_rule", "set_parameter"),
            },
            {
                "key": "calculation",
                "fragment": "TaxQuoteWorkbench",
                "binds_to": ("tax_calculation", "tax_calculation_line", "invoice_tax_record"),
                "commands": ("calculate_tax_quote", "record_invoice_tax"),
            },
            {
                "key": "filing",
                "fragment": "FilingPreparationConsole",
                "binds_to": ("tax_filing", "tax_filing_line", "tax_reconciliation", "tax_remittance_batch"),
                "commands": ("prepare_tax_filing", "reconcile_tax_collected", "route_tax_filing"),
            },
            {
                "key": "assistant",
                "fragment": "TaxAssistantPreviewPanel",
                "binds_to": ("tax_policy_rule", "tax_parameter", "tax_configuration"),
                "commands": ("assistant_preview",),
            },
            {
                "key": "controls",
                "fragment": "TaxControlCenter",
                "binds_to": ("tax_control_assertion", "tax_audit_proof", "tax_notice"),
                "commands": ("run_control_tests", "build_workbench_view"),
            },
        ),
        "action_permissions": action_permissions,
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "tax_quote_precision",
                "filing_reconciliation_tolerance",
                "authority_retry_limit",
                "exemption_expiry_warning_days",
                "nexus_sales_threshold",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("filing", "quote", "exemption", "cross_border", "withholding", "authority_route", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": TAX_LOCALIZATION_EMITTED_EVENT_TYPES,
            "consumes": TAX_LOCALIZATION_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": TAX_LOCALIZATION_OWNED_TABLES,
            "shared_table_access": False,
            "form_ids": forms["form_ids"],
            "wizard_ids": wizards["wizard_ids"],
            "control_ids": controls["control_ids"],
        },
    }


def tax_localization_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = tax_localization_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    jurisdictions = tuple(item for item in state.get("jurisdictions", {}).values() if item.get("tenant") == tenant)
    calculations = tuple(item for item in state.get("calculations", {}).values() if item.get("tenant") == tenant)
    filings = tuple(item for item in state.get("filings", {}).values() if item.get("tenant") == tenant)
    invoice_tax = tuple(item for item in state.get("invoice_tax", {}).values() if item.get("tenant") == tenant)
    cards = (
        {"key": "jurisdictions", "value": len(jurisdictions), "fragment": "JurisdictionMasterConsole"},
        {"key": "calculations", "value": len(calculations), "fragment": "TaxQuoteWorkbench"},
        {"key": "invoice_tax", "value": len(invoice_tax), "fragment": "InvoiceTaxRecordingView"},
        {"key": "filings", "value": len(filings), "fragment": "FilingPreparationConsole"},
        {"key": "forms", "value": len(contract["forms"]), "fragment": "TaxAssistantPreviewPanel"},
        {"key": "wizards", "value": len(contract["wizards"]), "fragment": "TaxWizardLauncher"},
        {"key": "controls", "value": len(contract["controls"]), "fragment": "TaxControlCenter"},
    )
    return {
        "format": "appgen.tax-localization-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/tax_localization",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "single_pbc_app": contract["single_pbc_app"],
        "binding_evidence": contract["binding_evidence"],
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    return _AppGenSmokeState(
        {
            "configuration": _AppGenSmokeState({"ok": True}),
            "rules": _AppGenSmokeState(),
            "parameters": _AppGenSmokeState(),
            "jurisdictions": _AppGenSmokeState(),
            "calculations": _AppGenSmokeState(),
            "invoice_tax": _AppGenSmokeState(),
            "filings": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "dead_letters": (),
        }
    )


def smoke_test():
    contract = tax_localization_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = tax_localization_render_workbench(_appgen_smoke_state(), tenant="smoke", principal_permissions=permissions)
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and contract["configuration_editor"]["stream_engine_picker_visible"] is False
        and contract["binding_evidence"]["shared_table_access"] is False,
        "manifest": {"fragments": contract.get("fragments", ())},
        "contract": contract,
        "rendered": rendered,
        "side_effects": (),
    }
