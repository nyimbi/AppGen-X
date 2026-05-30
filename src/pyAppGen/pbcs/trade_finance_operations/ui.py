"""UI contract for trade_finance_operations."""

from __future__ import annotations

from .controls import trade_finance_operations_control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .forms import trade_finance_operations_form_contracts
from .runtime import TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS
from .runtime import TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES
from .runtime import TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES
from .runtime import TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC
from .runtime import trade_finance_operations_build_case_detail
from .runtime import trade_finance_operations_build_workbench_view
from .runtime import trade_finance_operations_empty_state
from .wizards import trade_finance_operations_wizard_contracts
from .permissions import permission_manifest

PBC_KEY = "trade_finance_operations"
TRADE_FINANCE_OPERATIONS_UI_FRAGMENT_KEYS = (
    "TradeFinanceOperationsWorkbench",
    "TradeFinanceOperationsDetail",
    "TradeFinanceOperationsAssistantPanel",
)


def trade_finance_operations_ui_contract() -> dict:
    forms = trade_finance_operations_form_contracts()
    wizards = trade_finance_operations_wizard_contracts()
    controls = trade_finance_operations_control_catalog()
    permissions = permission_manifest()
    surface = domain_capability_surface_contract()
    return {
        "format": "appgen.trade-finance-operations-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"] and surface["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/trade_finance_operations",
        "fragments": TRADE_FINANCE_OPERATIONS_UI_FRAGMENT_KEYS,
        "forms": tuple(item["key"] for item in forms["contracts"]),
        "wizards": tuple(item["key"] for item in wizards["contracts"]),
        "controls": tuple(item["key"] for item in controls["contracts"]),
        "routes": (
            "/workbench/pbcs/trade_finance_operations",
            "/workbench/pbcs/trade_finance_operations/issuance",
            "/workbench/pbcs/trade_finance_operations/presentations",
            "/workbench/pbcs/trade_finance_operations/sanctions-holds",
            "/workbench/pbcs/trade_finance_operations/discrepancies",
            "/workbench/pbcs/trade_finance_operations/limits-collateral",
            "/workbench/pbcs/trade_finance_operations/settlements",
            "/workbench/pbcs/trade_finance_operations/release-evidence",
        ),
        "panels": (
            {"key": "issuance", "fragment": "TradeFinanceOperationsWorkbench", "binds_to": ("trade_finance_operations_letter_of_credit", "trade_finance_operations_bank_guarantee"), "commands": ("issue_letter_of_credit", "issue_bank_guarantee", "reserve_limit_exposure")},
            {"key": "document_examination", "fragment": "TradeFinanceOperationsDetail", "binds_to": ("trade_finance_operations_trade_document", "trade_finance_operations_discrepancy_case", "trade_finance_operations_sanctions_check"), "commands": ("record_shipment_documents", "run_sanctions_screening", "examine_document_package")},
            {"key": "settlement", "fragment": "TradeFinanceOperationsDetail", "binds_to": ("trade_finance_operations_fee_accrual", "trade_finance_operations_trade_settlement", "trade_finance_operations_swift_message_evidence"), "commands": ("assess_case_fees", "settle_trade_case", "generate_swift_message_evidence")},
            {"key": "assistant", "fragment": "TradeFinanceOperationsAssistantPanel", "binds_to": ("trade_finance_operations_trade_finance_operations_governed_model",), "commands": ("parse_document_instruction", "run_advanced_assessment", "build_release_evidence_pack")},
        ),
        "action_permissions": permissions["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_policy"),
            "allowed_database_backends": TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "visible_event_contracts": ("AppGen-X",),
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "supported_parameters": DOMAIN_PARAMETERS,
            "numeric_parameters": DOMAIN_PARAMETERS,
        },
        "rule_editor": {
            "rule_types": DOMAIN_RULES,
            "required_fields": ("rule_id", "scope", "status"),
            "compiled_evidence_fields": ("compiled_hash", "compiled"),
        },
        "event_surfaces": {
            "emits": TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES,
            "consumes": TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": DOMAIN_OWNED_TABLES,
            "shared_table_access": False,
        },
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": ("overview", "operations", "edge_case_triage", "advanced_intelligence", "release_evidence"),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def trade_finance_operations_render_workbench(
    state: dict | None = None,
    *,
    tenant: str = "default",
    principal_permissions: tuple[str, ...] = (
        "trade_finance_operations.read",
        "trade_finance_operations.create",
        "trade_finance_operations.update",
        "trade_finance_operations.approve",
        "trade_finance_operations.admin",
    ),
) -> dict:
    contract = trade_finance_operations_ui_contract()
    view = trade_finance_operations_build_workbench_view(tenant=tenant, state=state or trade_finance_operations_empty_state())
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action for action, required in contract["action_permissions"].items() if required in permissions
    )
    return {
        "format": "appgen.trade-finance-operations-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/trade_finance_operations",
        "fragments": contract["fragments"],
        "cards": view["cards"],
        "queues": view["queues"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "forms": trade_finance_operations_form_contracts()["contracts"],
        "wizards": trade_finance_operations_wizard_contracts()["contracts"],
        "controls": trade_finance_operations_control_catalog()["contracts"],
        "binding_evidence": contract["binding_evidence"],
        "side_effects": (),
    }


def trade_finance_operations_render_case_detail(case_id: str = "TFO-SAMPLE", state: dict | None = None) -> dict:
    detail = trade_finance_operations_build_case_detail(case_id=case_id, state=state)
    return {
        "format": "appgen.trade-finance-operations-detail-render.v1",
        "ok": detail["ok"],
        "case_id": case_id,
        "detail": detail,
        "side_effects": (),
    }


def smoke_test() -> dict:
    contract = trade_finance_operations_ui_contract()
    rendered = trade_finance_operations_render_workbench()
    detail = trade_finance_operations_render_case_detail()
    return {
        "ok": contract["ok"] and rendered["ok"] and detail["ok"],
        "contract": contract,
        "rendered": rendered,
        "detail": detail,
        "side_effects": (),
    }
