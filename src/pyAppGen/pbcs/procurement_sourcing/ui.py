"""UI contract for the Procurement and Strategic Sourcing PBC."""

from __future__ import annotations

from .runtime import PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS
from .runtime import PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES
from .runtime import PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES
from .runtime import PROCUREMENT_SOURCING_OWNED_TABLES
from .runtime import PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC
from .runtime import procurement_sourcing_permissions_contract


PROCUREMENT_SOURCING_UI_FRAGMENT_KEYS = (
    "ProcurementSourcingWorkbench",
    "RequisitionIntakeConsole",
    "ApprovalRoutingBoard",
    "BudgetPolicyCheckPanel",
    "SupplierReferenceConsole",
    "RfqCreationBoard",
    "SupplierInvitationPanel",
    "BidCaptureConsole",
    "BidNormalizationView",
    "SupplierScoringBoard",
    "AwardRecommendationConsole",
    "ContractCreationConsole",
    "ContractRenewalMonitor",
    "PurchaseOrderConsole",
    "SupplierRiskPanel",
    "SpendAnalyticsView",
    "ProcurementRuleStudio",
    "ProcurementParameterConsole",
    "ProcurementConfigurationPanel",
)


def procurement_sourcing_ui_contract() -> dict:
    return {
        "format": "appgen.procurement-sourcing-ui-contract.v1",
        "ok": True,
        "pbc": "procurement_sourcing",
        "implementation_directory": "src/pyAppGen/pbcs/procurement_sourcing",
        "fragments": PROCUREMENT_SOURCING_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/procurement_sourcing",
            "/workbench/pbcs/procurement_sourcing/requisitions",
            "/workbench/pbcs/procurement_sourcing/approvals",
            "/workbench/pbcs/procurement_sourcing/budget-policy",
            "/workbench/pbcs/procurement_sourcing/suppliers",
            "/workbench/pbcs/procurement_sourcing/rfqs",
            "/workbench/pbcs/procurement_sourcing/invitations",
            "/workbench/pbcs/procurement_sourcing/bids",
            "/workbench/pbcs/procurement_sourcing/scoring",
            "/workbench/pbcs/procurement_sourcing/awards",
            "/workbench/pbcs/procurement_sourcing/contracts",
            "/workbench/pbcs/procurement_sourcing/renewals",
            "/workbench/pbcs/procurement_sourcing/purchase-orders",
            "/workbench/pbcs/procurement_sourcing/risk",
            "/workbench/pbcs/procurement_sourcing/spend",
            "/workbench/pbcs/procurement_sourcing/rules",
            "/workbench/pbcs/procurement_sourcing/parameters",
            "/workbench/pbcs/procurement_sourcing/configuration",
        ),
        "panels": (
            {
                "key": "requisition",
                "fragment": "RequisitionIntakeConsole",
                "binds_to": ("requisition", "approval", "budget_policy"),
                "commands": ("create_requisition", "approve_requisition", "screen_policy"),
            },
            {
                "key": "sourcing",
                "fragment": "RfqCreationBoard",
                "binds_to": ("rfq", "supplier", "bid"),
                "commands": ("create_rfq", "capture_bid", "score_suppliers", "select_supplier"),
            },
            {
                "key": "contracting",
                "fragment": "ContractCreationConsole",
                "binds_to": ("award", "contract", "purchase_order", "outbox"),
                "commands": ("create_contract", "issue_purchase_order", "route_purchase_order"),
            },
            {
                "key": "risk",
                "fragment": "SupplierRiskPanel",
                "binds_to": ("supplier_identity", "supplier_risk", "compliance_proof"),
                "commands": ("verify_supplier_identity", "generate_supplier_compliance_proof", "run_control_tests"),
            },
            {
                "key": "governance",
                "fragment": "ProcurementRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": procurement_sourcing_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "allowed_categories"),
            "allowed_database_backends": PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "approval_limit",
                "minimum_bid_count",
                "supplier_risk_threshold",
                "price_variance_tolerance",
                "renewal_horizon_days",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("sourcing", "approval", "budget", "supplier_risk", "award", "contract", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES,
            "consumes": PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES, "shared_table_access": False},
    }


def procurement_sourcing_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = procurement_sourcing_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    requisitions = tuple(req for req in state["requisitions"].values() if req["tenant"] == tenant)
    rfqs = tuple(rfq for rfq in state["rfqs"].values() if rfq["tenant"] == tenant)
    contracts = tuple(contract_record for contract_record in state["contracts"].values() if contract_record["tenant"] == tenant)
    purchase_orders = tuple(po for po in state["purchase_orders"].values() if po["tenant"] == tenant)
    cards = (
        {"key": "requisitions", "value": len(requisitions), "fragment": "RequisitionIntakeConsole"},
        {"key": "rfqs", "value": len(rfqs), "fragment": "RfqCreationBoard"},
        {"key": "contracts", "value": len(contracts), "fragment": "ContractCreationConsole"},
        {"key": "purchase_orders", "value": len(purchase_orders), "fragment": "PurchaseOrderConsole"},
        {"key": "po_amount", "value": round(sum(po["amount"] for po in purchase_orders), 2), "fragment": "SpendAnalyticsView"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "ProcurementRuleStudio"},
    )
    return {
        "format": "appgen.procurement-sourcing-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/procurement_sourcing",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES,
            "outbox_table": "procurement_sourcing_appgen_outbox_event",
            "inbox_table": "procurement_sourcing_appgen_inbox_event",
            "dead_letter_table": "procurement_sourcing_dead_letter_event",
        },
    }
