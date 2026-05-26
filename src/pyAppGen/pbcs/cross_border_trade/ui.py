"""UI contract for the Cross Border Trade PBC."""

from __future__ import annotations

from .runtime import CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC
from .runtime import cross_border_trade_build_workbench_view
from .runtime import cross_border_trade_permissions_contract


CROSS_BORDER_TRADE_UI_FRAGMENT_KEYS = (
    "CrossBorderTradeWorkbench",
    "HSClassificationConsole",
    "LandedCostQuoteWorkbench",
    "ExportControlScreeningPanel",
    "CustomsDeclarationConsole",
    "BrokerSubmissionBoard",
    "TradeDocumentEvidencePanel",
    "TradeTopologyGraph",
    "DutyTaxExposurePanel",
    "TradeExceptionResolutionBoard",
    "TradeRuleStudio",
    "TradeParameterConsole",
    "TradeConfigurationPanel",
    "TradeEventingMonitor",
    "TradeDeadLetterQueue",
)


def cross_border_trade_ui_contract() -> dict:
    return {
        "format": "appgen.cross-border-trade-ui-contract.v1",
        "ok": True,
        "pbc": "cross_border_trade",
        "implementation_directory": "src/pyAppGen/pbcs/cross_border_trade",
        "fragments": CROSS_BORDER_TRADE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/cross_border_trade",
            "/workbench/pbcs/cross_border_trade/classifications",
            "/workbench/pbcs/cross_border_trade/landed-cost",
            "/workbench/pbcs/cross_border_trade/export-controls",
            "/workbench/pbcs/cross_border_trade/declarations",
            "/workbench/pbcs/cross_border_trade/brokers",
            "/workbench/pbcs/cross_border_trade/documents",
            "/workbench/pbcs/cross_border_trade/topology",
            "/workbench/pbcs/cross_border_trade/exposure",
            "/workbench/pbcs/cross_border_trade/exceptions",
            "/workbench/pbcs/cross_border_trade/rules",
            "/workbench/pbcs/cross_border_trade/parameters",
            "/workbench/pbcs/cross_border_trade/configuration",
            "/workbench/pbcs/cross_border_trade/eventing",
        ),
        "panels": (
            {
                "key": "classifications",
                "fragment": "HSClassificationConsole",
                "binds_to": ("hs_classification", "country_of_origin", "classification_evidence"),
                "commands": ("classify_product",),
            },
            {
                "key": "landed_cost",
                "fragment": "LandedCostQuoteWorkbench",
                "binds_to": ("landed_cost_quote", "duty", "tax", "fees", "incoterm"),
                "commands": ("quote_landed_cost",),
            },
            {
                "key": "export_controls",
                "fragment": "ExportControlScreeningPanel",
                "binds_to": ("export_control_check", "restricted_party_screen", "license_requirement"),
                "commands": ("screen_export_control",),
            },
            {
                "key": "declarations",
                "fragment": "CustomsDeclarationConsole",
                "binds_to": ("customs_declaration", "broker_submission", "documents"),
                "commands": ("file_customs_declaration",),
            },
            {
                "key": "eventing",
                "fragment": "TradeEventingMonitor",
                "binds_to": ("inbox", "outbox", "dead_letter", "idempotency_key"),
                "commands": ("receive_event",),
            },
            {
                "key": "governance",
                "fragment": "TradeRuleStudio",
                "binds_to": ("configuration_evidence", "rule_evidence", "parameter_evidence"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": cross_border_trade_permissions_contract(),
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "supported_countries",
                "supported_incoterms",
            ),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "required_event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "classification_confidence_threshold",
                "restricted_party_review_threshold",
                "duty_variance_tolerance",
                "de_minimis_value",
                "broker_latency_weight",
                "broker_cost_weight",
                "broker_compliance_weight",
                "carbon_weight",
                "forecast_horizon_days",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": (
                "classification_policy",
                "landed_cost_policy",
                "export_control_policy",
                "declaration_policy",
                "release_gate",
            ),
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "classification_policy",
                "landed_cost_policy",
                "export_control_policy",
                "declaration_policy",
            ),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": ("HSClassified", "LandedCostQuoted", "ExportControlCleared", "CustomsDeclarationFiled"),
            "consumes": ("InventoryReserved", "OrderPlaced", "PaymentCaptured", "ShipmentDispatched"),
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def cross_border_trade_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = cross_border_trade_ui_contract()
    snapshot = cross_border_trade_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    cards = (
        {
            "key": "classifications",
            "value": snapshot["classification_count"],
            "fragment": "HSClassificationConsole",
        },
        {
            "key": "landed_cost_quotes",
            "value": snapshot["quote_count"],
            "fragment": "LandedCostQuoteWorkbench",
        },
        {
            "key": "export_controls",
            "value": snapshot["export_control_count"],
            "fragment": "ExportControlScreeningPanel",
        },
        {
            "key": "declarations",
            "value": snapshot["declaration_count"],
            "fragment": "CustomsDeclarationConsole",
        },
        {
            "key": "dead_letters",
            "value": snapshot["dead_letter_count"],
            "fragment": "TradeDeadLetterQueue",
        },
        {
            "key": "rules",
            "value": snapshot["rule_count"],
            "fragment": "TradeRuleStudio",
        },
    )
    return {
        "format": "appgen.cross-border-trade-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/cross_border_trade",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action for action in contract["action_permissions"] if action not in visible_actions
        ),
        "configuration_bound": snapshot["configuration_bound"],
        "configuration_hash": snapshot["configuration_hash"],
        "rules_bound": snapshot["rules_bound"],
        "rule_evidence": snapshot["rule_evidence"],
        "parameters_bound": snapshot["parameters_bound"],
        "event_outbox_count": snapshot["outbox_count"],
        "event_inbox_count": snapshot["inbox_count"],
        "dead_letter_count": snapshot["dead_letter_count"],
        "owned_tables": snapshot["owned_tables"],
    }
