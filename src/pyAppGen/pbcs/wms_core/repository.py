"""Repository and read-model contract for the standalone wms_core package."""

from __future__ import annotations

from .runtime import WMS_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import WMS_CORE_OWNED_TABLES
from .runtime import WMS_CORE_REQUIRED_EVENT_TOPIC
from .runtime import wms_core_build_workbench_view


FORM_BINDINGS = (
    {
        "form": "warehouse_registration_form",
        "owned_table": "warehouse",
        "repository_method": "warehouse_console",
        "writes": ("warehouse", "warehouse_zone", "warehouse_identity"),
    },
    {
        "form": "bin_slotting_form",
        "owned_table": "bin_location",
        "repository_method": "warehouse_console",
        "writes": ("bin_location", "bin_capacity_snapshot", "bin_attribute"),
    },
    {
        "form": "inbound_receipt_form",
        "owned_table": "inbound_receipt",
        "repository_method": "inbound_console",
        "writes": ("inbound_receipt", "inbound_receipt_line", "putaway_task"),
    },
    {
        "form": "pick_wave_release_form",
        "owned_table": "pick_wave",
        "repository_method": "outbound_console",
        "writes": ("pick_wave", "pick_task", "pack_task", "shipment_confirmation"),
    },
    {
        "form": "pack_confirmation_form",
        "owned_table": "pack_task",
        "repository_method": "outbound_console",
        "writes": ("pack_task", "carton", "shipment_label"),
    },
)
READ_MODELS = (
    {"key": "warehouse", "repository_method": "warehouse_console"},
    {"key": "inbound", "repository_method": "inbound_console"},
    {"key": "outbound", "repository_method": "outbound_console"},
    {"key": "governance", "repository_method": "governance_console"},
)


def wms_core_repository_contract() -> dict:
    """Return the repository surface that backs standalone forms and workbench views."""
    return {
        "format": "appgen.wms-core-repository-contract.v1",
        "ok": bool(FORM_BINDINGS) and bool(READ_MODELS),
        "pbc": "wms_core",
        "database_backends": WMS_CORE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
        "owned_tables": WMS_CORE_OWNED_TABLES,
        "form_bindings": FORM_BINDINGS,
        "read_models": READ_MODELS,
        "shared_table_access": False,
        "side_effects": (),
    }


class WmsCoreRepository:
    """Repository facade over the package-local WMS runtime state."""

    def __init__(self, state: dict):
        self.state = state

    def warehouse_console(self, tenant: str) -> dict:
        warehouses = tuple(
            item for item in self.state.get("warehouses", {}).values() if item.get("tenant") == tenant
        )
        bins = tuple(item for item in self.state.get("bins", {}).values() if item.get("tenant") == tenant)
        return {
            "warehouse_count": len(warehouses),
            "bin_count": len(bins),
            "warehouses": warehouses,
            "bins": bins,
        }

    def inbound_console(self, tenant: str) -> dict:
        receipts = tuple(
            item for item in self.state.get("receipts", {}).values() if item.get("tenant") == tenant
        )
        putaway_tasks = tuple(
            item for item in self.state.get("putaway_tasks", {}).values() if item.get("tenant") == tenant
        )
        return {
            "receipt_count": len(receipts),
            "putaway_count": len(putaway_tasks),
            "receipts": receipts,
            "putaway_tasks": putaway_tasks,
        }

    def outbound_console(self, tenant: str) -> dict:
        waves = tuple(item for item in self.state.get("waves", {}).values() if item.get("tenant") == tenant)
        picks = tuple(item for item in self.state.get("picks", {}).values() if item.get("tenant") == tenant)
        packs = tuple(
            item for item in self.state.get("pack_tasks", {}).values() if item.get("tenant") == tenant
        )
        shipments = tuple(
            item for item in self.state.get("shipments", {}).values() if item.get("tenant") == tenant
        )
        return {
            "wave_count": len(waves),
            "pick_count": len(picks),
            "pack_count": len(packs),
            "shipment_count": len(shipments),
            "waves": waves,
            "picks": picks,
            "pack_tasks": packs,
            "shipments": shipments,
        }

    def governance_console(self, tenant: str) -> dict:
        return {
            "tenant": tenant,
            "rule_count": len(self.state.get("rules", {})),
            "parameter_count": len(self.state.get("parameters", {})),
            "configuration_bound": bool(self.state.get("configuration", {}).get("ok")),
            "inbox_count": len(self.state.get("inbox", ())),
            "outbox_count": len(self.state.get("outbox", ())),
            "dead_letter_count": len(
                self.state.get("dead_letter", self.state.get("dead_letters", ()))
            ),
        }

    def form_binding_plan(self, form_key: str) -> dict:
        binding = next((item for item in FORM_BINDINGS if item["form"] == form_key), None)
        return {
            "ok": binding is not None,
            "form": form_key,
            "binding": binding,
            "database_backends": WMS_CORE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "side_effects": (),
        }

    def read_model(self, tenant: str) -> dict:
        workbench = wms_core_build_workbench_view(self.state, tenant=tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "warehouse": self.warehouse_console(tenant),
            "inbound": self.inbound_console(tenant),
            "outbound": self.outbound_console(tenant),
            "governance": self.governance_console(tenant),
            "workbench": workbench,
            "side_effects": (),
        }


repository_contract = wms_core_repository_contract


def smoke_test() -> dict:
    """Exercise the repository contract and read models without external I/O."""
    state = {
        "warehouses": {
            "wh_demo": {"tenant": "tenant_demo", "warehouse_id": "wh_demo", "name": "Demo"},
        },
        "bins": {
            "bin_demo": {
                "tenant": "tenant_demo",
                "bin_id": "bin_demo",
                "warehouse_id": "wh_demo",
                "zone": "fast_pick",
            },
        },
        "receipts": {},
        "putaway_tasks": {},
        "waves": {},
        "picks": {},
        "pack_tasks": {},
        "shipments": {},
        "rules": {"rule_demo": {"tenant": "tenant_demo"}},
        "parameters": {"workbench_limit": 50},
        "configuration": {"ok": True, "event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC},
        "inbox": (),
        "outbox": (),
        "dead_letter": (),
        "dead_letters": (),
    }
    repository = WmsCoreRepository(state)
    read_model = repository.read_model("tenant_demo")
    binding = repository.form_binding_plan("warehouse_registration_form")
    contract = wms_core_repository_contract()
    return {
        "ok": contract["ok"]
        and read_model["warehouse"]["warehouse_count"] == 1
        and read_model["workbench"]["warehouse_count"] == 1
        and binding["ok"],
        "contract": contract,
        "read_model": read_model,
        "binding": binding,
        "side_effects": (),
    }
