"""UI contract for the Tax Localization PBC."""

from __future__ import annotations


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
)


def tax_localization_ui_contract() -> dict:
    return {
        "format": "appgen.tax-localization-ui-contract.v1",
        "ok": True,
        "pbc": "tax_localization",
        "implementation_directory": "src/pyAppGen/pbcs/tax_localization",
        "fragments": TAX_LOCALIZATION_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/tax_localization",
            "/workbench/pbcs/tax_localization/jurisdictions",
            "/workbench/pbcs/tax_localization/tax-rules",
            "/workbench/pbcs/tax_localization/product-taxability",
            "/workbench/pbcs/tax_localization/quotes",
            "/workbench/pbcs/tax_localization/invoices",
            "/workbench/pbcs/tax_localization/filings",
            "/workbench/pbcs/tax_localization/exemptions",
            "/workbench/pbcs/tax_localization/cross-border",
            "/workbench/pbcs/tax_localization/authority-channels",
            "/workbench/pbcs/tax_localization/reconciliation",
            "/workbench/pbcs/tax_localization/documents",
            "/workbench/pbcs/tax_localization/risk",
            "/workbench/pbcs/tax_localization/rules",
            "/workbench/pbcs/tax_localization/parameters",
            "/workbench/pbcs/tax_localization/configuration",
        ),
        "panels": (
            {
                "key": "jurisdiction",
                "fragment": "JurisdictionMasterConsole",
                "binds_to": ("jurisdiction", "authority_channel", "filing_calendar"),
                "commands": ("register_jurisdiction", "verify_tax_identity", "score_jurisdiction_risk"),
            },
            {
                "key": "rules",
                "fragment": "TaxRuleAuthoringStudio",
                "binds_to": ("tax_rule", "rule_version", "compiled_expression"),
                "commands": ("register_tax_rule", "compile_regulatory_rule", "simulate_tax_policy_change"),
            },
            {
                "key": "calculation",
                "fragment": "TaxQuoteWorkbench",
                "binds_to": ("calculation", "invoice_tax", "exemption_certificate"),
                "commands": ("classify_product", "calculate_tax_quote", "record_invoice_tax", "validate_exemption_certificate"),
            },
            {
                "key": "filing",
                "fragment": "FilingPreparationConsole",
                "binds_to": ("filing", "reconciliation", "digital_document", "outbox"),
                "commands": ("prepare_tax_filing", "reconcile_tax_collected", "route_tax_filing"),
            },
            {
                "key": "governance",
                "fragment": "TaxGovernanceRuleStudio",
                "binds_to": ("policy_rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": {
            "register_jurisdiction": "tax_localization.jurisdiction",
            "register_tax_rule": "tax_localization.rule_admin",
            "classify_product": "tax_localization.calculate",
            "calculate_tax_quote": "tax_localization.calculate",
            "record_invoice_tax": "tax_localization.invoice",
            "prepare_tax_filing": "tax_localization.file",
            "validate_exemption_certificate": "tax_localization.exemption",
            "reconcile_tax_collected": "tax_localization.reconcile",
            "route_tax_filing": "tax_localization.file",
            "generate_tax_audit_proof": "tax_localization.audit",
            "register_rule": "tax_localization.configure",
            "set_parameter": "tax_localization.configure",
            "configure_runtime": "tax_localization.configure",
            "run_control_tests": "tax_localization.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
        },
        "rule_editor": {
            "rule_types": ("filing", "quote", "exemption", "cross_border", "withholding", "authority_route", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": ("TaxJurisdictionRegistered", "TaxRuleActivated", "TaxCalculated", "InvoiceTaxRecorded", "TaxFilingPrepared"),
            "consumes": ("ProductClassified", "InvoiceIssued", "OrderPriced", "PaymentCollected", "AccessPolicyChanged"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def tax_localization_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = tax_localization_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    jurisdictions = tuple(item for item in state["jurisdictions"].values() if item["tenant"] == tenant)
    calculations = tuple(item for item in state["calculations"].values() if item["tenant"] == tenant)
    filings = tuple(item for item in state["filings"].values() if item["tenant"] == tenant)
    invoice_tax = tuple(item for item in state["invoice_tax"].values() if item["tenant"] == tenant)
    cards = (
        {"key": "jurisdictions", "value": len(jurisdictions), "fragment": "JurisdictionMasterConsole"},
        {"key": "calculations", "value": len(calculations), "fragment": "TaxQuoteWorkbench"},
        {"key": "invoice_tax", "value": len(invoice_tax), "fragment": "InvoiceTaxRecordingView"},
        {"key": "filings", "value": len(filings), "fragment": "FilingPreparationConsole"},
        {"key": "open_liability", "value": round(sum(item["tax_total"] for item in calculations) - sum(item["liability"] for item in filings), 2), "fragment": "TaxReconciliationBoard"},
        {"key": "rules", "value": len(state.get("policy_rules", {})), "fragment": "TaxGovernanceRuleStudio"},
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
        "rules_bound": tuple(sorted(state.get("policy_rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
    }
