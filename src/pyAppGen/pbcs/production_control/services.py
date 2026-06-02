"""Command service layer for the production_control PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .runtime import production_control_build_api_contract
from .runtime import production_control_build_service_contract

PBC_KEY = "production_control"


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
        "idempotency_key": route.get("idempotency_key"),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }


OPERATION_CONTRACTS = tuple(_route_to_contract(route) for route in production_control_build_api_contract()["routes"])


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = production_control_build_service_contract()
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


class ProductionControlService:
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
            result.update({"command": operation_name, "read_only": False, "outbox_table": EVENT_CONTRACT["outbox_table"], "emits": (plan.get("emitted_event"),) if plan.get("emitted_event") else ()})
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
        "service_class": ProductionControlService.__name__,
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
    service = ProductionControlService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = service.execute_operation(operation, {"smoke": True}) if operation else {"ok": False}
    return {"ok": manifest["ok"] and result.get("ok") is True, "manifest": manifest, "result": result, "side_effects": ()}



def standalone_service_operation_contracts():
    contracts=(
        {'operation':'seed_demo_workspace','operation_kind':'command','method':'POST','path':'/app/production-control/demo-workspace','table':'production_control_production_configuration','wizard':'ShopFloorPacketIntakeWizard','permission':'production_control.configure'},
        {'operation':'build_workbench','operation_kind':'query','method':'GET','path':'/app/production-control/workbench','table':'production_control_production_order','wizard':None,'permission':'production_control.read'},
        {'operation':'create_production_order','operation_kind':'command','method':'POST','path':'/app/production-control/orders','table':'production_control_production_order','wizard':'ShopFloorPacketIntakeWizard','permission':'production_control.execute'},
        {'operation':'confirm_operation','operation_kind':'command','method':'POST','path':'/app/production-control/operations/confirm','table':'production_control_operation_confirmation','wizard':'OperationExecutionWizard','permission':'production_control.execute'},
        {'operation':'generate_completion_proof','operation_kind':'command','method':'POST','path':'/app/production-control/proofs','table':'production_control_completion_proof','wizard':'ProductionCompletionWizard','permission':'production_control.audit'},
    )
    return {'format':'appgen.production-control-standalone-service.v1','ok':all(i['table'].startswith('production_control_') for i in contracts),'pbc':'production_control','contracts':contracts,'operations':tuple(i['operation'] for i in contracts),'command_operations':tuple(i['operation'] for i in contracts if i['operation_kind']=='command'),'query_operations':tuple(i['operation'] for i in contracts if i['operation_kind']=='query'),'side_effects':()}

class ProductionControlStandaloneService:
    def __init__(self,repository=None,database_path=':memory:'):
        if repository is None:
            from .repository import ProductionControlStandaloneRepository
            repository=ProductionControlStandaloneRepository(database_path=database_path)
        self.repository=repository
    def close(self): self.repository.close()
    def seed_demo_workspace(self,tenant='tenant_demo'): return self.repository.seed_demo_workspace(tenant=tenant)
    def build_workbench(self,tenant='tenant_demo'): return self.repository.build_workbench(tenant)
    def create_production_order(self,tenant,order): return self.repository.create_production_order(tenant,order)
    def confirm_operation(self,tenant,step_id,**kw): return self.repository.confirm_operation(tenant,step_id,**kw)
    def generate_completion_proof(self,tenant,order_id,disclosure=('order_id','item','completed_qty')): return self.repository.generate_completion_proof(tenant,order_id,tuple(disclosure))
