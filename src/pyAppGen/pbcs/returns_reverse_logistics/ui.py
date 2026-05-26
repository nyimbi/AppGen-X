"""UI contract for the Returns and Reverse Logistics PBC."""

from __future__ import annotations

from .runtime import RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
from .runtime import returns_reverse_logistics_build_workbench_view
from .runtime import returns_reverse_logistics_permissions_contract


RETURNS_REVERSE_LOGISTICS_UI_FRAGMENT_KEYS = (
    "ReturnsReverseLogisticsWorkbench",
    "ReturnAuthorizationConsole",
    "EligibilityScreeningPanel",
    "ReturnLabelConsole",
    "CarrierHandoffBoard",
    "InspectionDispositionWorkbench",
    "CreditAdjustmentConsole",
    "RefundLedgerHandoffPanel",
    "FraudSignalPanel",
    "ReverseTopologyGraph",
    "ReturnExceptionResolutionBoard",
    "ReturnRuleStudio",
    "ReturnParameterConsole",
    "ReturnConfigurationPanel",
    "ReturnEventingMonitor",
)


def returns_reverse_logistics_ui_contract() -> dict:
    return {
        "format": "appgen.returns-reverse-logistics-ui-contract.v1",
        "ok": True,
        "pbc": "returns_reverse_logistics",
        "implementation_directory": "src/pyAppGen/pbcs/returns_reverse_logistics",
        "fragments": RETURNS_REVERSE_LOGISTICS_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/returns_reverse_logistics",
            "/workbench/pbcs/returns_reverse_logistics/returns",
            "/workbench/pbcs/returns_reverse_logistics/eligibility",
            "/workbench/pbcs/returns_reverse_logistics/labels",
            "/workbench/pbcs/returns_reverse_logistics/carrier-handoff",
            "/workbench/pbcs/returns_reverse_logistics/inspection",
            "/workbench/pbcs/returns_reverse_logistics/credits",
            "/workbench/pbcs/returns_reverse_logistics/refunds-ledger",
            "/workbench/pbcs/returns_reverse_logistics/fraud",
            "/workbench/pbcs/returns_reverse_logistics/topology",
            "/workbench/pbcs/returns_reverse_logistics/exceptions",
            "/workbench/pbcs/returns_reverse_logistics/rules",
            "/workbench/pbcs/returns_reverse_logistics/parameters",
            "/workbench/pbcs/returns_reverse_logistics/configuration",
            "/workbench/pbcs/returns_reverse_logistics/eventing",
        ),
        "panels": (
            {
                "key": "returns",
                "fragment": "ReturnAuthorizationConsole",
                "binds_to": ("return_authorization", "eligibility", "fraud_assessment"),
                "commands": ("authorize_return",),
            },
            {
                "key": "labels",
                "fragment": "ReturnLabelConsole",
                "binds_to": ("return_label", "carrier_handoff", "carbon_route"),
                "commands": ("create_return_label",),
            },
            {
                "key": "inspection",
                "fragment": "InspectionDispositionWorkbench",
                "binds_to": ("inspection_grade", "disposition", "credit_adjustment", "ledger_handoff"),
                "commands": ("record_inspection_grade", "issue_credit_adjustment"),
            },
            {
                "key": "eventing",
                "fragment": "ReturnEventingMonitor",
                "binds_to": ("inbox", "outbox", "dead_letter", "idempotency_key"),
                "commands": ("receive_event",),
            },
            {
                "key": "governance",
                "fragment": "ReturnRuleStudio",
                "binds_to": ("configuration_evidence", "rule_evidence", "parameter_evidence"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": returns_reverse_logistics_permissions_contract(),
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "supported_carriers",
                "supported_dispositions",
            ),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "required_event_topic": RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "eligibility_window_days",
                "fraud_threshold",
                "recovery_floor",
                "carrier_handoff_hours",
                "carbon_weight",
                "route_switch_threshold",
                "forecast_horizon_days",
                "anomaly_zscore_threshold",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": (
                "return_policy",
                "label_routing",
                "inspection",
                "credit_adjustment",
                "fraud_screen",
                "release_gate",
            ),
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "eligibility_policy",
                "label_policy",
                "inspection_policy",
                "credit_policy",
            ),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": ("ReturnAuthorized", "CreditAdjustmentIssued"),
            "consumes": ("OrderShipped", "PaymentCaptured"),
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def returns_reverse_logistics_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = returns_reverse_logistics_ui_contract()
    snapshot = returns_reverse_logistics_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    cards = (
        {
            "key": "returns",
            "value": snapshot["return_count"],
            "fragment": "ReturnAuthorizationConsole",
        },
        {
            "key": "labels",
            "value": snapshot["label_count"],
            "fragment": "ReturnLabelConsole",
        },
        {
            "key": "inspections",
            "value": snapshot["inspection_count"],
            "fragment": "InspectionDispositionWorkbench",
        },
        {
            "key": "credits",
            "value": snapshot["credit_count"],
            "fragment": "CreditAdjustmentConsole",
        },
        {
            "key": "dead_letters",
            "value": snapshot["dead_letter_count"],
            "fragment": "ReturnEventingMonitor",
        },
        {
            "key": "rules",
            "value": snapshot["rule_count"],
            "fragment": "ReturnRuleStudio",
        },
    )
    return {
        "format": "appgen.returns-reverse-logistics-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/returns_reverse_logistics",
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
    }
