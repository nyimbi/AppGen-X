"""Repository and read-model contract for the standalone transportation_management package."""

from __future__ import annotations

from .runtime import TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import TRANSPORTATION_MANAGEMENT_OWNED_TABLES
from .runtime import TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .runtime import transportation_management_build_workbench_view


FORM_BINDINGS = (
    {
        "form": "shipment_creation_form",
        "owned_table": "shipment",
        "repository_method": "shipment_console",
        "writes": ("shipment", "shipment_line", "shipment_package", "shipment_party"),
    },
    {
        "form": "carrier_registration_form",
        "owned_table": "carrier",
        "repository_method": "carrier_console",
        "writes": ("carrier", "carrier_service_level", "carrier_lane", "carrier_identity"),
    },
    {
        "form": "route_planning_form",
        "owned_table": "freight_route",
        "repository_method": "route_console",
        "writes": ("freight_route", "route_stop", "route_leg", "carbon_distance_metric"),
    },
    {
        "form": "dispatch_tracking_form",
        "owned_table": "dispatch_confirmation",
        "repository_method": "tracking_console",
        "writes": ("dispatch_confirmation", "tracking_event", "eta_snapshot"),
    },
    {
        "form": "delivery_proof_form",
        "owned_table": "delivery_proof",
        "repository_method": "tracking_console",
        "writes": ("inbound_arrival", "delivery_proof", "transportation_delivery_proof_hash"),
    },
    {
        "form": "transportation_governance_form",
        "owned_table": "transportation_rule",
        "repository_method": "governance_console",
        "writes": ("transportation_rule", "transportation_parameter", "transportation_configuration", "transportation_schema_extension"),
    },
)
READ_MODELS = (
    {"key": "shipment", "repository_method": "shipment_console"},
    {"key": "carrier", "repository_method": "carrier_console"},
    {"key": "route", "repository_method": "route_console"},
    {"key": "tracking", "repository_method": "tracking_console"},
    {"key": "governance", "repository_method": "governance_console"},
)


def transportation_management_repository_contract() -> dict:
    """Return the repository surface that backs standalone forms and workbench views."""
    return {
        "format": "appgen.transportation-management-repository-contract.v1",
        "ok": bool(FORM_BINDINGS) and bool(READ_MODELS),
        "pbc": "transportation_management",
        "database_backends": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
        "form_bindings": FORM_BINDINGS,
        "read_models": READ_MODELS,
        "shared_table_access": False,
        "side_effects": (),
    }


class TransportationManagementRepository:
    """Repository facade over package-local transportation runtime state."""

    def __init__(self, state: dict):
        self.state = state

    def shipment_console(self, tenant: str) -> dict:
        shipments = tuple(item for item in self.state.get("shipments", {}).values() if item.get("tenant") == tenant)
        return {
            "shipment_count": len(shipments),
            "dispatched_count": len(tuple(item for item in shipments if item.get("status") == "dispatched")),
            "delivered_count": len(tuple(item for item in shipments if item.get("status") == "delivered")),
            "shipments": shipments,
        }

    def carrier_console(self, tenant: str) -> dict:
        carriers = tuple(item for item in self.state.get("carriers", {}).values() if item.get("tenant") == tenant)
        return {
            "carrier_count": len(carriers),
            "active_count": len(tuple(item for item in carriers if item.get("status") == "active")),
            "carriers": carriers,
        }

    def route_console(self, tenant: str) -> dict:
        routes = tuple(item for item in self.state.get("routes", {}).values() if item.get("tenant") == tenant)
        return {
            "route_count": len(routes),
            "estimated_cost": round(sum(item.get("estimated_cost", 0) for item in routes), 2),
            "estimated_carbon": round(sum(item.get("estimated_carbon", 0) for item in routes), 2),
            "routes": routes,
        }

    def tracking_console(self, tenant: str) -> dict:
        tracking = tuple(item for item in self.state.get("tracking_events", {}).values() if item.get("tenant") == tenant)
        shipments = tuple(item for item in self.state.get("shipments", {}).values() if item.get("tenant") == tenant)
        return {
            "tracking_event_count": len(tracking),
            "arrived_count": len(tuple(item for item in shipments if item.get("status") == "arrived")),
            "delivered_count": len(tuple(item for item in shipments if item.get("status") == "delivered")),
            "tracking_events": tracking,
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
            "database_backends": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "side_effects": (),
        }

    def read_model(self, tenant: str) -> dict:
        workbench = transportation_management_build_workbench_view(self.state, tenant=tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "shipment": self.shipment_console(tenant),
            "carrier": self.carrier_console(tenant),
            "route": self.route_console(tenant),
            "tracking": self.tracking_console(tenant),
            "governance": self.governance_console(tenant),
            "workbench": workbench,
            "side_effects": (),
        }


repository_contract = transportation_management_repository_contract


def smoke_test() -> dict:
    """Exercise the repository contract and read models without external I/O."""
    state = {
        "shipments": {"ship_demo": {"tenant": "tenant_demo", "shipment_id": "ship_demo", "status": "delivered"}},
        "carriers": {"carrier_demo": {"tenant": "tenant_demo", "carrier_id": "carrier_demo", "status": "active"}},
        "routes": {"route_demo": {"tenant": "tenant_demo", "route_id": "route_demo", "estimated_cost": 1000, "estimated_carbon": 50}},
        "tracking_events": {"track_demo": {"tenant": "tenant_demo", "event_id": "track_demo", "shipment_id": "ship_demo"}},
        "rules": {"rule_demo": {"tenant": "tenant_demo"}},
        "parameters": {"workbench_limit": 50},
        "configuration": {"ok": True, "event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC},
        "inbox": (),
        "outbox": (),
        "dead_letter": (),
        "dead_letters": (),
    }
    repository = TransportationManagementRepository(state)
    read_model = repository.read_model("tenant_demo")
    binding = repository.form_binding_plan("route_planning_form")
    contract = transportation_management_repository_contract()
    return {
        "ok": contract["ok"]
        and read_model["shipment"]["shipment_count"] == 1
        and read_model["route"]["estimated_cost"] == 1000
        and read_model["workbench"]["shipment_count"] == 1
        and binding["ok"],
        "contract": contract,
        "read_model": read_model,
        "binding": binding,
        "side_effects": (),
    }
