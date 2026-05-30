"""Standalone one-PBC application surface for the MRP Engine package."""

from __future__ import annotations

from tempfile import NamedTemporaryFile

from . import agent, ui
from .repository import MrpEngineStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import MrpEngineStandaloneService, standalone_service_operation_contracts


def mrp_engine_standalone_app_contract() -> dict:
    repository = standalone_repository_contract(); services = standalone_service_operation_contracts(); routes = standalone_route_contracts(); workbench = ui.mrp_engine_standalone_workbench_blueprint(); workspace = agent.standalone_agent_workspace_contract()
    return {'format': 'appgen.mrp-engine-standalone-app.v1', 'ok': all(item.get('ok') is True for item in (repository, services, routes, workbench, workspace)), 'pbc': 'mrp_engine', 'repository': repository, 'services': services, 'routes': routes, 'ui': workbench, 'agent': workspace, 'side_effects': ()}


def mrp_engine_bootstrap_standalone_app(database_path=':memory:', *, tenant='tenant_demo', seed_demo=True) -> dict:
    repository = MrpEngineStandaloneRepository(database_path=database_path); service = MrpEngineStandaloneService(repository); seeded = repository.seed_demo_workspace(tenant=tenant) if seed_demo else {'ok': True, 'tenant': tenant}
    return {'ok': seeded['ok'], 'pbc': 'mrp_engine', 'repository': repository, 'service': service, 'seeded': seeded, 'contract': mrp_engine_standalone_app_contract(), 'side_effects': ()}


def mrp_engine_standalone_app_smoke() -> dict:
    bundle = mrp_engine_bootstrap_standalone_app(seed_demo=False); service = bundle['service']
    try:
        seed_route = dispatch_standalone_route('POST', '/app/mrp-engine/demo-workspace', {'tenant': 'tenant_demo'}, service=service)
        workbench = dispatch_standalone_route('GET', '/app/mrp-engine/workbench', {'tenant': 'tenant_demo'}, service=service)
        proof = dispatch_standalone_route('POST', '/app/mrp-engine/proofs', {'tenant': 'tenant_demo', 'planned_order_id': 'po_run_demo_100_component_a', 'disclosure': ('planned_order_id', 'item', 'quantity')}, service=service)
        rendered = ui.mrp_engine_render_standalone_workbench(workbench['result']['result'])
        return {'ok': bundle['contract']['ok'] and seed_route['ok'] and workbench['ok'] and proof['ok'] and rendered['ok'] and standalone_repository_smoke_test()['ok'], 'contract': bundle['contract'], 'seed_route': seed_route, 'workbench': workbench, 'proof': proof, 'rendered': rendered, 'side_effects': ()}
    finally:
        service.close()


def standalone_release_snapshot() -> dict:
    with NamedTemporaryFile(suffix='.sqlite3') as handle:
        app = mrp_engine_bootstrap_standalone_app(database_path=handle.name, seed_demo=True)
        try:
            workbench = app['service'].build_workbench('tenant_demo')
            return {'ok': app['ok'] and workbench['ok'], 'app': app['contract'], 'workbench': workbench, 'read_model': app['repository'].read_model('tenant_demo'), 'side_effects': ()}
        finally:
            app['service'].close()
