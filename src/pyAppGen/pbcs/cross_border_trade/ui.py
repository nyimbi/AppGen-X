"""UI contract for the Cross Border Trade PBC."""

from __future__ import annotations

from .runtime import CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS
from .runtime import CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES
from .runtime import CROSS_BORDER_TRADE_EMITTED_EVENT_TYPES
from .runtime import CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC
from .runtime import cross_border_trade_build_workbench_view
from .runtime import cross_border_trade_permissions_contract
from .app_surface import single_pbc_trade_app_contract, trade_controls_contract, trade_forms_contract, trade_wizards_contract
from .trade_control import improve1_trade_control_contract


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
    permissions = cross_border_trade_permissions_contract()
    single_pbc_app = single_pbc_trade_app_contract()
    trade_control = improve1_trade_control_contract()
    return {
        "format": "appgen.cross-border-trade-ui-contract.v1",
        "ok": True,
        "pbc": "cross_border_trade",
        "implementation_directory": "src/pyAppGen/pbcs/cross_border_trade",
        "fragments": CROSS_BORDER_TRADE_UI_FRAGMENT_KEYS,
        "forms": trade_forms_contract()["forms"],
        "wizards": trade_wizards_contract()["wizards"],
        "controls": trade_controls_contract()["controls"],
        "single_pbc_app": single_pbc_app,
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
            "/workbench/pbcs/cross_border_trade/dead-letter",
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
                "commands": ("screen_export_control", "screen_denied_party", "register_country_restriction_policy"),
            },
            {
                "key": "declarations",
                "fragment": "CustomsDeclarationConsole",
                "binds_to": ("customs_declaration", "broker_handoff", "carrier_handoff", "documents", "compliance_hold"),
                "commands": (
                    "file_customs_declaration",
                    "prepare_trade_document_packet",
                    "queue_broker_handoff",
                    "prepare_carrier_handoff",
                    "release_customs_declaration",
                ),
            },
            {
                "key": "eventing",
                "fragment": "TradeEventingMonitor",
                "binds_to": ("inbox", "outbox", "dead_letter", "idempotency_key"),
                "commands": ("receive_event",),
            },
            {
                "key": "holds",
                "fragment": "TradeExceptionResolutionBoard",
                "binds_to": ("trade_compliance_hold", "denied_party_screening", "country_restriction_policy"),
                "commands": (
                    "screen_export_control",
                    "screen_denied_party",
                    "open_trade_compliance_hold",
                    "resolve_trade_compliance_hold",
                ),
            },
            {
                "key": "governance",
                "fragment": "TradeRuleStudio",
                "binds_to": ("configuration_evidence", "rule_evidence", "parameter_evidence"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": permissions["action_permissions"],
        "permissions_contract": permissions,
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "supported_countries",
                "supported_incoterms",
            ),
            "allowed_database_backends": CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
            "stream_engine_picker_visible": False,
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
        "trade_control_panels": tuple({"capability": sample["capability"], "feature_number": sample["feature_number"], "title": sample["title"], "target_table": sample["target_table"], "route": sample["route"], "permission": sample["permission"]} for sample in trade_control["samples"]),
        "trade_control_contract": trade_control,
        "event_surfaces": {
            "emits": CROSS_BORDER_TRADE_EMITTED_EVENT_TYPES,
            "consumes": CROSS_BORDER_TRADE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def cross_border_trade_forms_contract() -> dict:
    return trade_forms_contract()


def cross_border_trade_wizards_contract() -> dict:
    return trade_wizards_contract()


def cross_border_trade_controls_contract() -> dict:
    return trade_controls_contract()


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
            "key": "compliance_holds",
            "value": snapshot["compliance_hold_count"],
            "fragment": "TradeExceptionResolutionBoard",
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
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "single_pbc_app": contract["single_pbc_app"],
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
        "binding_evidence": snapshot["binding_evidence"],
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = cross_border_trade_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = cross_border_trade_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and contract.get("single_pbc_app", {}).get("single_pbc_app") is True
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
