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
    contract = procurement_sourcing_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = procurement_sourcing_render_workbench(
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


PROCUREMENT_SOURCING_FORM_KEYS = (
    "requisition_intake_form",
    "rfq_creation_form",
    "supplier_bid_form",
    "award_decision_form",
    "contract_and_po_form",
    "procurement_governance_form",
)
PROCUREMENT_SOURCING_WIZARD_KEYS = (
    "source_to_contract_wizard",
    "emergency_buy_wizard",
    "supplier_onboarding_wizard",
    "contract_to_po_wizard",
)
PROCUREMENT_SOURCING_CONTROL_KEYS = (
    "tenant_scope_picker",
    "category_strategy_selector",
    "supplier_risk_heatmap",
    "bid_comparison_matrix",
    "award_confidence_meter",
    "event_reliability_drawer",
    "assistant_skill_panel",
)


def procurement_sourcing_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "requisition_intake_form",
            "title": "Purchase Requisition Intake",
            "command": "create_requisition",
            "owned_table": "purchase_requisition",
            "fields": ("requisition_id", "tenant", "legal_entity", "category", "item_id", "quantity", "estimated_amount", "currency", "cost_center", "requested_by"),
        },
        {
            "key": "rfq_creation_form",
            "title": "RFQ Creation",
            "command": "create_rfq",
            "owned_table": "rfq",
            "fields": ("rfq_id", "requisition_id", "suppliers", "category", "terms", "due_at"),
        },
        {
            "key": "supplier_bid_form",
            "title": "Supplier Bid Capture",
            "command": "capture_bid",
            "owned_table": "supplier_bid",
            "fields": ("rfq_id", "supplier_id", "price", "lead_time_days", "risk", "quality", "carbon", "identity"),
        },
        {
            "key": "award_decision_form",
            "title": "Award Decision",
            "command": "select_supplier",
            "owned_table": "supplier_award",
            "fields": ("award_id", "rfq_id", "score_weights", "split_award", "approval_note"),
        },
        {
            "key": "contract_and_po_form",
            "title": "Contract and Purchase Order",
            "command": "issue_purchase_order",
            "owned_table": "purchase_order",
            "fields": ("contract_id", "po_id", "quantity", "amount", "currency", "payment_terms"),
        },
        {
            "key": "procurement_governance_form",
            "title": "Procurement Governance",
            "command": "register_rule",
            "owned_table": "procurement_rule",
            "fields": ("rule_id", "tenant", "rule_type", "category", "preferred_suppliers", "restricted_suppliers", "score_weights", "status"),
        },
    )


def procurement_sourcing_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "source_to_contract_wizard",
            "steps": ("requisition_intake_form", "rfq_creation_form", "supplier_bid_form", "award_decision_form", "contract_and_po_form"),
            "goal": "Move a governed requisition through RFQ, scoring, award, contract, and purchase order issuance.",
        },
        {
            "key": "emergency_buy_wizard",
            "steps": ("requisition_intake_form", "procurement_governance_form", "contract_and_po_form"),
            "goal": "Execute urgent buys with approval-limit, supplier-risk, and event-outbox controls still enforced.",
        },
        {
            "key": "supplier_onboarding_wizard",
            "steps": ("supplier_bid_form", "procurement_governance_form"),
            "goal": "Capture supplier identity, qualification, risk, carbon, and policy screening before award eligibility.",
        },
        {
            "key": "contract_to_po_wizard",
            "steps": ("award_decision_form", "contract_and_po_form"),
            "goal": "Convert an award into contract evidence and a tolerance-checked purchase order.",
        },
    )


def procurement_sourcing_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "category_strategy_selector", "type": "selector", "binds_to": "category_strategy"},
        {"key": "supplier_risk_heatmap", "type": "heatmap", "binds_to": "supplier_risk_projection"},
        {"key": "bid_comparison_matrix", "type": "matrix", "binds_to": "supplier_bid"},
        {"key": "award_confidence_meter", "type": "meter", "binds_to": "supplier_award"},
        {"key": "event_reliability_drawer", "type": "drawer", "binds_to": "event_reliability"},
        {"key": "assistant_skill_panel", "type": "assistant", "binds_to": "procurement_sourcing_skills"},
    )


def procurement_sourcing_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "procurement_sourcing",
        "app_id": "procurement_sourcing_one_pbc_app",
        "workbench_route": "/workbench/pbcs/procurement_sourcing",
        "navigation": (
            {"key": "requisitions", "route": "/workbench/pbcs/procurement_sourcing/requisitions"},
            {"key": "sourcing", "route": "/workbench/pbcs/procurement_sourcing/rfqs"},
            {"key": "awards", "route": "/workbench/pbcs/procurement_sourcing/awards"},
            {"key": "contracts", "route": "/workbench/pbcs/procurement_sourcing/contracts"},
            {"key": "purchase_orders", "route": "/workbench/pbcs/procurement_sourcing/purchase-orders"},
            {"key": "governance", "route": "/workbench/pbcs/procurement_sourcing/configuration"},
        ),
        "forms": PROCUREMENT_SOURCING_FORM_KEYS,
        "wizards": PROCUREMENT_SOURCING_WIZARD_KEYS,
        "controls": PROCUREMENT_SOURCING_CONTROL_KEYS,
        "single_agent_namespace": "procurement_sourcing_skills",
        "side_effects": (),
    }


def procurement_sourcing_ui_contract() -> dict:
    shell = procurement_sourcing_standalone_app_contract()
    return {
        "format": "appgen.procurement-sourcing-ui-contract.v1",
        "ok": True,
        "pbc": "procurement_sourcing",
        "implementation_directory": "src/pyAppGen/pbcs/procurement_sourcing",
        "fragments": PROCUREMENT_SOURCING_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in shell["navigation"]) + (shell["workbench_route"],),
        "panels": (
            {"key": "requisition", "fragment": "RequisitionIntakeConsole", "binds_to": ("requisition", "approval", "budget_policy"), "commands": ("create_requisition", "approve_requisition", "screen_policy")},
            {"key": "sourcing", "fragment": "RfqCreationBoard", "binds_to": ("rfq", "supplier", "bid"), "commands": ("create_rfq", "capture_bid", "score_suppliers", "select_supplier")},
            {"key": "contracting", "fragment": "ContractCreationConsole", "binds_to": ("award", "contract", "purchase_order", "outbox"), "commands": ("create_contract", "issue_purchase_order", "route_purchase_order")},
            {"key": "risk", "fragment": "SupplierRiskPanel", "binds_to": ("supplier_identity", "supplier_risk", "compliance_proof"), "commands": ("generate_supplier_compliance_proof", "run_control_tests")},
            {"key": "governance", "fragment": "ProcurementRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "forms": procurement_sourcing_form_catalog(),
        "wizards": procurement_sourcing_wizard_catalog(),
        "controls": procurement_sourcing_control_catalog(),
        "standalone_app": shell,
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
            "numeric_parameters": ("approval_limit", "minimum_bid_count", "supplier_risk_threshold", "price_variance_tolerance", "renewal_horizon_days", "workbench_limit"),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("sourcing", "approval", "budget", "supplier_risk", "award", "contract", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES,
            "consumes": PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES,
            "outbox_table": "procurement_sourcing_appgen_outbox_event",
            "inbox_table": "procurement_sourcing_appgen_inbox_event",
            "dead_letter_table": "procurement_sourcing_dead_letter_event",
            "shared_table_access": False,
            "required_event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
            "rbac_permissions": procurement_sourcing_permissions_contract()["permissions"],
        },
    }


def procurement_sourcing_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = procurement_sourcing_ui_contract()
    shell = procurement_sourcing_standalone_app_contract()
    from .runtime import procurement_sourcing_build_workbench_view

    snapshot = procurement_sourcing_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    return {
        "format": "appgen.procurement-sourcing-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "requisitions", "value": snapshot["requisition_count"], "fragment": "RequisitionIntakeConsole"},
            {"key": "rfqs", "value": snapshot["rfq_count"], "fragment": "RfqCreationBoard"},
            {"key": "contracts", "value": snapshot["contract_count"], "fragment": "ContractCreationConsole"},
            {"key": "purchase_orders", "value": snapshot["po_count"], "fragment": "PurchaseOrderConsole"},
            {"key": "po_amount", "value": snapshot["po_amount"], "fragment": "SpendAnalyticsView"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": snapshot["inbox_count"],
        "dead_letter_count": snapshot["dead_letter_count"],
        "binding_evidence": contract["binding_evidence"],
        "workbench": snapshot,
    }


def procurement_sourcing_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    contract = procurement_sourcing_ui_contract()
    permissions = principal_permissions or tuple(sorted(set(contract["action_permissions"].values())))
    rendered = procurement_sourcing_render_workbench(state, tenant=tenant, principal_permissions=permissions)
    return {
        "ok": rendered["ok"],
        "pbc": "procurement_sourcing",
        "shell": procurement_sourcing_standalone_app_contract(),
        "workbench": rendered,
        "side_effects": (),
    }


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = procurement_sourcing_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = procurement_sourcing_render_workbench(_appgen_smoke_state(), tenant="smoke", principal_permissions=permissions)
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {"rule_types": ("configuration", "parameter", "release_gate"), "required_fields": ("rule_id", "scope", "status")}
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
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {
            "fragments": contract.get("fragments", ()),
            "routes": contract.get("routes", ()),
            "forms": tuple(item["key"] for item in contract.get("forms", ())),
            "wizards": tuple(item["key"] for item in contract.get("wizards", ())),
            "controls": tuple(item["key"] for item in contract.get("controls", ())),
        },
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
