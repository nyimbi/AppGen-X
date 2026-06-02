"""API route contracts for the asset_lifecycle PBC."""

from __future__ import annotations

from .services import AssetLifecycleService
from .services import service_operation_contracts


def _route_from_operation(contract: dict) -> dict:
    return {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["operation"],
        "permission": contract["permission"],
        "operation": contract["operation"],
        "operation_kind": contract["operation_kind"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "event_contract": contract["event_contract"],
        "transaction_boundary": contract["transaction_boundary"],
        "idempotency_required": contract["operation_kind"] == "command",
        "idempotency_key": (
            f"asset_lifecycle:{contract['operation']}:idempotency_key"
            if contract["operation_kind"] == "command"
            else None
        ),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


API_ROUTE_CONTRACTS = tuple(_route_from_operation(contract) for contract in service_operation_contracts()["contracts"])
ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["handler"],
        "permission": contract["permission"],
    }
    for contract in API_ROUTE_CONTRACTS
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts():
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()["contracts"]
    operation_index = {item["operation"]: item for item in service_contracts}
    contracts = tuple(
        {
            **contract,
            "service_operation": operation_index.get(contract["operation"]),
            "route_id": f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "asset_lifecycle",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts():
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if not item["service_operation"]
        or item["service_operation"]["method"] != item["method"]
        or item["service_operation"]["path"] != item["path"]
        or item["service_operation"]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(
        item["route_id"]
        for item in contracts
        if item["idempotency_required"] and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("asset_lifecycle_")
    )
    return {
        "ok": manifest["ok"]
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        "pbc": "asset_lifecycle",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    service = AssetLifecycleService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test():
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    if not ROUTES:
        return {"ok": False, "reason": "no_routes"}
    first = ROUTES[0]
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True})
    return {
        "ok": validation["ok"] and dispatched["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }


STANDALONE_ROUTES=(
    {'method':'POST','path':'/app/asset-lifecycle/demo-workspace','handler':'seed_demo_workspace'},
    {'method':'GET','path':'/app/asset-lifecycle/workbench','handler':'build_workbench'},
    {'method':'POST','path':'/app/asset-lifecycle/assets','handler':'register_asset'},
    {'method':'POST','path':'/app/asset-lifecycle/depreciation-runs','handler':'run_depreciation'},
    {'method':'POST','path':'/app/asset-lifecycle/transfers','handler':'transfer_asset'},
    {'method':'POST','path':'/app/asset-lifecycle/audit-proofs','handler':'generate_asset_audit_proof'},)

def standalone_route_contracts():
    from .services import standalone_service_operation_contracts
    ops={i['operation']:i for i in standalone_service_operation_contracts()['contracts']}; contracts=tuple({**r,'operation':r['handler'],'service_operation':ops.get(r['handler'])} for r in STANDALONE_ROUTES)
    return {'format':'appgen.asset-lifecycle-standalone-routes.v1','ok':all(i['service_operation'] for i in contracts),'pbc':'asset_lifecycle','routes':tuple(f"{i['method']} {i['path']}" for i in contracts),'contracts':contracts,'side_effects':()}

def dispatch_standalone_route(method,path,payload=None,*,service=None):
    from .services import AssetLifecycleStandaloneService
    route=next((i for i in STANDALONE_ROUTES if i['method']==method and i['path']==path),None)
    if route is None: return {'ok':False,'handled':False,'reason':'route_not_found','side_effects':()}
    own=service is None; service=service or AssetLifecycleStandaloneService(); data=dict(payload or {})
    try:
        if route['handler']=='seed_demo_workspace': result=service.seed_demo_workspace(tenant=data.get('tenant','tenant_demo'))
        elif route['handler']=='build_workbench': result=service.build_workbench(tenant=data.get('tenant','tenant_demo'))
        elif route['handler']=='register_asset': result=service.register_asset(data.get('tenant','tenant_demo'),data)
        elif route['handler']=='run_depreciation': result=service.run_depreciation(data.get('tenant','tenant_demo'),data['run_id'],data['period'])
        elif route['handler']=='transfer_asset': result=service.transfer_asset(data.get('tenant','tenant_demo'),data['asset_id'],data['location'],data['cost_center'],data.get('approved_by','asset_controller'))
        elif route['handler']=='generate_asset_audit_proof': result=service.generate_asset_audit_proof(data.get('tenant','tenant_demo'),data['asset_id'],tuple(data.get('disclosure',('asset_id','status','book_value','location'))))
        else: result={'ok':False,'reason':'handler_not_implemented'}
        return {'ok':result.get('ok') is True,'handled':True,'route':route,'result':{'ok':result.get('ok') is True,'result':result},'side_effects':()}
    finally:
        if own: service.close()
