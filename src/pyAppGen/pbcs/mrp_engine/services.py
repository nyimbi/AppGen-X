"""Command service layer for the mrp_engine PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .runtime import mrp_engine_build_api_contract
from .runtime import mrp_engine_build_service_contract

PBC_KEY = "mrp_engine"


def _route_to_contract(route: dict) -> dict:
    method, path = route["route"].split(" ", 1)
    operation = route.get("command") or route.get("query")
    operation_kind = "command" if route.get("command") else "query"
    owned_tables = tuple(
        table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        for table in route.get("owned_tables", ())
    )
    is_command = operation_kind == "command"
    if is_command and not owned_tables:
        owned_tables = (EVENT_CONTRACT["inbox_table"],)
    idempotency_key = route.get("idempotency_key") or (
        f"{PBC_KEY}:{operation}:idempotency_key" if is_command else None
    )
    return {
        "operation": operation,
        "operation_kind": operation_kind,
        "method": method,
        "path": path,
        "permission": route["requires_permission"],
        "owned_tables": owned_tables if is_command else (),
        "read_tables": () if is_command else owned_tables,
        "emitted_event": (route.get("emits") or (f"{PBC_KEY}.{operation}.executed",))[0] if is_command else None,
        "consumed_event": tuple(route.get("consumes", ())),
        "idempotency_key": idempotency_key,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }


OPERATION_CONTRACTS = tuple(_route_to_contract(route) for route in mrp_engine_build_api_contract()["routes"])


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = mrp_engine_build_service_contract()
    return {
        "ok": runtime_service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] or item["consumed_event"] for item in command_contracts)
        and all(item["read_tables"] for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "runtime_service_contract": runtime_service,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": bool(contract["owned_tables"] or contract["read_tables"] or contract["consumed_event"]),
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_event": contract["consumed_event"],
        "idempotency_key": contract["idempotency_key"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


class MrpEngineService:
    """Side-effect-free generated command facade."""

    def execute_operation(self, operation_name: str, payload: dict | None = None) -> dict:
        plan = operation_plan(operation_name, payload)
        result = {
            "ok": plan["ok"],
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": plan.get("operation_kind"),
            "payload": dict(payload or {}),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if plan.get("operation_kind") == "command":
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (plan.get("emitted_event"),) if plan.get("emitted_event") else (),
                }
            )
        elif plan.get("operation_kind") == "query":
            result.update({"query": operation_name, "read_only": True, "outbox_table": None, "emits": ()})
        return result

    def __getattr__(self, operation_name: str):
        if operation_name in service_operation_contracts()["operations"]:
            return lambda payload=None: self.execute_operation(operation_name, payload or {})
        raise AttributeError(operation_name)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": MrpEngineService.__name__,
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = MrpEngineService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = service.execute_operation(operation, {"smoke": True}) if operation else {"ok": False}
    return {"ok": manifest["ok"] and result.get("ok") is True, "manifest": manifest, "result": result, "side_effects": ()}



def standalone_service_operation_contracts():
    contracts = (
        {'operation': 'seed_demo_workspace', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/mrp-engine/demo-workspace', 'table': 'mrp_engine_mrp_configuration', 'wizard': 'PlanningDocumentIntakeWizard', 'permission': 'mrp_engine.configure'},
        {'operation': 'build_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/mrp-engine/workbench', 'table': 'mrp_engine_planned_order', 'wizard': None, 'permission': 'mrp_engine.read'},
        {'operation': 'register_bom', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/mrp-engine/boms', 'table': 'mrp_engine_bill_of_material', 'wizard': 'PlanningDocumentIntakeWizard', 'permission': 'mrp_engine.master'},
        {'operation': 'create_mrp_run', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/mrp-engine/runs', 'table': 'mrp_engine_mrp_run', 'wizard': 'MrpRunWizard', 'permission': 'mrp_engine.plan'},
        {'operation': 'calculate_material_plan', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/mrp-engine/runs/net', 'table': 'mrp_engine_planned_order', 'wizard': 'NettingAndPeggingWizard', 'permission': 'mrp_engine.plan'},
        {'operation': 'generate_supply_proof', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/mrp-engine/proofs', 'table': 'mrp_engine_supply_availability_proof', 'wizard': 'PlannedOrderReleaseWizard', 'permission': 'mrp_engine.audit'},
    )
    return {'format': 'appgen.mrp-engine-standalone-service.v1', 'ok': all(item['table'].startswith('mrp_engine_') for item in contracts), 'pbc': 'mrp_engine', 'contracts': contracts, 'operations': tuple(item['operation'] for item in contracts), 'command_operations': tuple(item['operation'] for item in contracts if item['operation_kind'] == 'command'), 'query_operations': tuple(item['operation'] for item in contracts if item['operation_kind'] == 'query'), 'side_effects': ()}


class MrpEngineStandaloneService:
    def __init__(self, repository=None, database_path=':memory:'):
        if repository is None:
            from .repository import MrpEngineStandaloneRepository
            repository = MrpEngineStandaloneRepository(database_path=database_path)
        self.repository = repository

    def close(self):
        self.repository.close()

    def seed_demo_workspace(self, tenant='tenant_demo'):
        return self.repository.seed_demo_workspace(tenant=tenant)

    def build_workbench(self, tenant='tenant_demo'):
        return self.repository.build_workbench(tenant)

    def register_bom(self, tenant, bom):
        return self.repository.register_bom(tenant, bom)

    def create_mrp_run(self, tenant, mrp_run):
        return self.repository.create_mrp_run(tenant, mrp_run)

    def calculate_material_plan(self, tenant, run_id):
        return self.repository.calculate_material_plan(tenant, run_id)

    def generate_supply_proof(self, tenant, planned_order_id, disclosure=('planned_order_id', 'item', 'quantity')):
        return self.repository.generate_supply_proof(tenant, planned_order_id, tuple(disclosure))
