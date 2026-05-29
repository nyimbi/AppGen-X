"""Standalone one-PBC application surface for the Quality Assurance package."""

from __future__ import annotations

from tempfile import NamedTemporaryFile
from typing import Any

from . import agent
from . import seed_data
from . import ui
from .repository import QualityAssuranceStandaloneRepository
from .repository import standalone_repository_contract
from .repository import standalone_repository_smoke_test
from .routes import dispatch_standalone_route
from .routes import standalone_route_contracts
from .services import QualityAssuranceStandaloneService
from .services import standalone_service_operation_contracts


def quality_assurance_standalone_app_contract() -> dict:
    repository = standalone_repository_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    workbench = ui.quality_assurance_standalone_workbench_blueprint()
    workspace = agent.standalone_agent_workspace_contract()
    return {'format': 'appgen.quality-assurance-standalone-app.v1', 'ok': all(item.get('ok') is True for item in (repository, services, routes, workbench, workspace)), 'pbc': 'quality_assurance', 'repository': repository, 'services': services, 'routes': routes, 'ui': workbench, 'agent': workspace, 'side_effects': ()}


def quality_assurance_bootstrap_standalone_app(database_path=':memory:', *, tenant='tenant_demo', seed_demo=True) -> dict:
    repository = QualityAssuranceStandaloneRepository(database_path=database_path)
    service = QualityAssuranceStandaloneService(repository)
    seeded = repository.seed_demo_workspace(tenant=tenant) if seed_demo else {'ok': True, 'tenant': tenant}
    return {'ok': seeded['ok'], 'pbc': 'quality_assurance', 'repository': repository, 'service': service, 'seeded': seeded, 'contract': quality_assurance_standalone_app_contract(), 'side_effects': ()}


def quality_assurance_standalone_app_smoke() -> dict:
    bundle = quality_assurance_bootstrap_standalone_app(seed_demo=False)
    service = bundle['service']
    try:
        seed_route = dispatch_standalone_route('POST', '/app/quality-assurance/demo-workspace', {'tenant': 'tenant_demo'}, service=service)
        workbench = dispatch_standalone_route('GET', '/app/quality-assurance/workbench', {'tenant': 'tenant_demo'}, service=service)
        controls = dispatch_standalone_route('GET', '/app/quality-assurance/controls', {'tenant': 'tenant_demo'}, service=service)
        proof = dispatch_standalone_route('POST', '/app/quality-assurance/proofs', {'tenant': 'tenant_demo', 'result_id': 'result_demo_100', 'disclosure': ('result_id', 'lot_id', 'decision')}, service=service)
        rendered = ui.quality_assurance_render_standalone_workbench(workbench['result']['result'])
        return {'ok': bundle['contract']['ok'] and seed_route['ok'] and workbench['ok'] and controls['ok'] and proof['ok'] and rendered['ok'] and standalone_repository_smoke_test()['ok'], 'contract': bundle['contract'], 'seed_route': seed_route, 'workbench': workbench, 'controls': controls, 'proof': proof, 'rendered': rendered, 'side_effects': ()}
    finally:
        service.close()


def standalone_release_snapshot() -> dict:
    with NamedTemporaryFile(suffix='.sqlite3') as handle:
        app = quality_assurance_bootstrap_standalone_app(database_path=handle.name, seed_demo=True)
        try:
            service = app['service']
            workbench = service.build_workbench('tenant_demo')
            return {'ok': app['ok'] and workbench['ok'], 'app': app['contract'], 'workbench': workbench, 'read_model': app['repository'].read_model('tenant_demo'), 'side_effects': ()}
        finally:
            service.close()
