"""Repository and read-model contract for the standalone procurement_sourcing package."""

from __future__ import annotations

from .runtime import PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS
from .runtime import PROCUREMENT_SOURCING_OWNED_TABLES
from .runtime import PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC
from .runtime import procurement_sourcing_build_workbench_view


FORM_BINDINGS = (
    {
        "form": "requisition_intake_form",
        "owned_table": "purchase_requisition",
        "repository_method": "requisition_console",
        "writes": ("purchase_requisition", "purchase_requisition_line", "requisition_budget_check"),
    },
    {
        "form": "rfq_creation_form",
        "owned_table": "rfq",
        "repository_method": "sourcing_console",
        "writes": ("rfq", "rfq_line", "supplier_invitation"),
    },
    {
        "form": "supplier_bid_form",
        "owned_table": "supplier_bid",
        "repository_method": "sourcing_console",
        "writes": ("supplier_bid", "supplier_bid_line", "bid_normalization"),
    },
    {
        "form": "award_decision_form",
        "owned_table": "supplier_award",
        "repository_method": "award_console",
        "writes": ("supplier_scorecard", "supplier_award", "split_award"),
    },
    {
        "form": "contract_and_po_form",
        "owned_table": "vendor_contract",
        "repository_method": "contracting_console",
        "writes": ("vendor_contract", "contract_clause", "purchase_order", "purchase_order_line"),
    },
    {
        "form": "procurement_governance_form",
        "owned_table": "procurement_rule",
        "repository_method": "governance_console",
        "writes": ("rule", "parameter", "configuration", "schema_extension"),
    },
)
READ_MODELS = (
    {"key": "requisition", "repository_method": "requisition_console"},
    {"key": "sourcing", "repository_method": "sourcing_console"},
    {"key": "award", "repository_method": "award_console"},
    {"key": "contracting", "repository_method": "contracting_console"},
    {"key": "governance", "repository_method": "governance_console"},
)


def procurement_sourcing_repository_contract() -> dict:
    """Return the repository surface that backs standalone forms and workbench views."""
    return {
        "format": "appgen.procurement-sourcing-repository-contract.v1",
        "ok": bool(FORM_BINDINGS) and bool(READ_MODELS),
        "pbc": "procurement_sourcing",
        "database_backends": PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
        "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES,
        "form_bindings": FORM_BINDINGS,
        "read_models": READ_MODELS,
        "shared_table_access": False,
        "side_effects": (),
    }


class ProcurementSourcingRepository:
    """Repository facade over the package-local procurement runtime state."""

    def __init__(self, state: dict):
        self.state = state

    def requisition_console(self, tenant: str) -> dict:
        requisitions = tuple(
            item for item in self.state.get("requisitions", {}).values() if item.get("tenant") == tenant
        )
        approved = tuple(item for item in requisitions if item.get("status") == "approved")
        blocked = tuple(item for item in requisitions if item.get("status") == "policy_blocked")
        return {
            "requisition_count": len(requisitions),
            "approved_count": len(approved),
            "blocked_count": len(blocked),
            "total_estimated_amount": round(sum(item.get("estimated_amount", 0) for item in requisitions), 2),
            "requisitions": requisitions,
        }

    def sourcing_console(self, tenant: str) -> dict:
        rfqs = tuple(item for item in self.state.get("rfqs", {}).values() if item.get("tenant") == tenant)
        rfq_ids = {item.get("rfq_id") for item in rfqs}
        bids = tuple(
            bid
            for rfq_id, rfq_bids in self.state.get("bids", {}).items()
            if rfq_id in rfq_ids
            for bid in rfq_bids
        )
        return {
            "rfq_count": len(rfqs),
            "bid_count": len(bids),
            "open_rfq_count": len(tuple(item for item in rfqs if item.get("status") == "open")),
            "rfqs": rfqs,
            "bids": bids,
        }

    def award_console(self, tenant: str) -> dict:
        awards = tuple(item for item in self.state.get("awards", {}).values() if item.get("tenant") == tenant)
        return {
            "award_count": len(awards),
            "awarded_amount": round(sum(item.get("amount", 0) for item in awards), 2),
            "awards": awards,
        }

    def contracting_console(self, tenant: str) -> dict:
        contracts = tuple(item for item in self.state.get("contracts", {}).values() if item.get("tenant") == tenant)
        purchase_orders = tuple(
            item for item in self.state.get("purchase_orders", {}).values() if item.get("tenant") == tenant
        )
        return {
            "contract_count": len(contracts),
            "purchase_order_count": len(purchase_orders),
            "purchase_order_amount": round(sum(item.get("amount", 0) for item in purchase_orders), 2),
            "contracts": contracts,
            "purchase_orders": purchase_orders,
        }

    def governance_console(self, tenant: str) -> dict:
        return {
            "tenant": tenant,
            "rule_count": len(self.state.get("rules", {})),
            "parameter_count": len(self.state.get("parameters", {})),
            "configuration_bound": bool(self.state.get("configuration", {}).get("ok")),
            "inbox_count": len(self.state.get("inbox", ())),
            "outbox_count": len(self.state.get("outbox", ())),
            "dead_letter_count": len(self.state.get("dead_letter", self.state.get("dead_letters", ()))),
        }

    def form_binding_plan(self, form_key: str) -> dict:
        binding = next((item for item in FORM_BINDINGS if item["form"] == form_key), None)
        return {
            "ok": binding is not None,
            "form": form_key,
            "binding": binding,
            "database_backends": PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "side_effects": (),
        }

    def read_model(self, tenant: str) -> dict:
        workbench = procurement_sourcing_build_workbench_view(self.state, tenant=tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "requisition": self.requisition_console(tenant),
            "sourcing": self.sourcing_console(tenant),
            "award": self.award_console(tenant),
            "contracting": self.contracting_console(tenant),
            "governance": self.governance_console(tenant),
            "workbench": workbench,
            "side_effects": (),
        }


repository_contract = procurement_sourcing_repository_contract


def smoke_test() -> dict:
    """Exercise the repository contract and read models without external I/O."""
    state = {
        "requisitions": {
            "req_demo": {"tenant": "tenant_demo", "requisition_id": "req_demo", "status": "approved", "estimated_amount": 1000},
        },
        "rfqs": {"rfq_demo": {"tenant": "tenant_demo", "rfq_id": "rfq_demo", "status": "open"}},
        "bids": {"rfq_demo": ({"supplier_id": "supplier_demo", "price": 980},)},
        "awards": {"award_demo": {"tenant": "tenant_demo", "award_id": "award_demo", "amount": 980}},
        "contracts": {"contract_demo": {"tenant": "tenant_demo", "contract_id": "contract_demo"}},
        "purchase_orders": {"po_demo": {"tenant": "tenant_demo", "po_id": "po_demo", "amount": 980}},
        "rules": {"rule_demo": {"tenant": "tenant_demo"}},
        "parameters": {"approval_limit": 5000},
        "configuration": {"ok": True, "event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC},
        "inbox": (),
        "outbox": (),
        "dead_letter": (),
        "dead_letters": (),
    }
    repository = ProcurementSourcingRepository(state)
    read_model = repository.read_model("tenant_demo")
    binding = repository.form_binding_plan("requisition_intake_form")
    contract = procurement_sourcing_repository_contract()
    return {
        "ok": contract["ok"]
        and read_model["requisition"]["requisition_count"] == 1
        and read_model["workbench"]["po_amount"] == 980
        and binding["ok"],
        "contract": contract,
        "read_model": read_model,
        "binding": binding,
        "side_effects": (),
    }
