"""Command and preview service layer for the asset_lifecycle PBC."""

from __future__ import annotations

from .depreciation_engine import build_schedule_version
from .manifest import PBC_MANIFEST
from .runtime import ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC


def _physical_owned_tables() -> tuple[str, ...]:
    tables = []
    for table in PBC_MANIFEST.get("tables", ()):
        if table == "fixed_asset":
            tables.append("asset_lifecycle_fixed_asset")
        elif table.startswith("asset_lifecycle_"):
            tables.append(table)
        else:
            tables.append(f"asset_lifecycle_{table}")
    tables.extend(
        (
            "asset_lifecycle_appgen_outbox_event",
            "asset_lifecycle_appgen_inbox_event",
            "asset_lifecycle_dead_letter_event",
        )
    )
    return tuple(tables)


_SERVICE_TABLES = _physical_owned_tables()
_QUERY_TABLES = tuple(table for table in _SERVICE_TABLES if table != "asset_lifecycle_appgen_outbox_event")

EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
    "inbox_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
    "outbox_table": "asset_lifecycle_appgen_outbox_event",
    "inbox_table": "asset_lifecycle_appgen_inbox_event",
    "dead_letter_table": "asset_lifecycle_dead_letter_event",
    "retry_policy": {"name": "asset_lifecycle_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": "asset_lifecycle_appgen_inbox_event"},
}

_OPERATION_SPECS = (
    ("command_assets", "command", "POST", "/api/pbc/asset_lifecycle/assets", "asset_lifecycle.command.1", "AssetRegistered"),
    (
        "command_assets_asset_id_service",
        "command",
        "POST",
        "/api/pbc/asset_lifecycle/assets/{asset_id}/service",
        "asset_lifecycle.command.2",
        "AssetPlacedInService",
    ),
    (
        "command_assets_asset_id_depreciation_schedules",
        "command",
        "POST",
        "/api/pbc/asset_lifecycle/assets/{asset_id}/depreciation-schedules",
        "asset_lifecycle.command.3",
        "DepreciationCalculated",
    ),
    ("command_depreciation_runs", "command", "POST", "/api/pbc/asset_lifecycle/depreciation-runs", "asset_lifecycle.command.4", "DepreciationCalculated"),
    (
        "command_assets_asset_id_transfers",
        "command",
        "POST",
        "/api/pbc/asset_lifecycle/assets/{asset_id}/transfers",
        "asset_lifecycle.command.5",
        "AssetTransferred",
    ),
    (
        "command_assets_asset_id_revaluations",
        "command",
        "POST",
        "/api/pbc/asset_lifecycle/assets/{asset_id}/revaluations",
        "asset_lifecycle.command.6",
        "AssetRevalued",
    ),
    (
        "command_assets_asset_id_impairments",
        "command",
        "POST",
        "/api/pbc/asset_lifecycle/assets/{asset_id}/impairments",
        "asset_lifecycle.command.7",
        "AssetImpaired",
    ),
    (
        "command_assets_asset_id_maintenance_adjustments",
        "command",
        "POST",
        "/api/pbc/asset_lifecycle/assets/{asset_id}/maintenance-adjustments",
        "asset_lifecycle.command.8",
        "MaintenanceAdjustedAssetLife",
    ),
    (
        "command_assets_asset_id_retirements",
        "command",
        "POST",
        "/api/pbc/asset_lifecycle/assets/{asset_id}/retirements",
        "asset_lifecycle.command.9",
        "AssetRetired",
    ),
    ("command_assets_events_inbox", "command", "POST", "/api/pbc/asset_lifecycle/assets/events/inbox", "asset_lifecycle.command.10", None),
    ("query_assets", "query", "GET", "/api/pbc/asset_lifecycle/assets", "asset_lifecycle.query.11", None),
    (
        "query_assets_asset_id_risk",
        "query",
        "GET",
        "/api/pbc/asset_lifecycle/assets/{asset_id}/risk",
        "asset_lifecycle.query.12",
        None,
    ),
)


def _build_operation_contracts() -> tuple[dict, ...]:
    contracts = []
    for operation, kind, method, path, permission, emitted_event in _OPERATION_SPECS:
        contracts.append(
            {
                "operation": operation,
                "operation_kind": kind,
                "method": method,
                "path": path,
                "permission": permission,
                "owned_tables": _SERVICE_TABLES if kind == "command" else (),
                "read_tables": () if kind == "command" else _QUERY_TABLES,
                "emitted_event": emitted_event,
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _build_operation_contracts()


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item["operation"] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    inbox_commands = {"command_assets_events_inbox"}
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["emitted_event"] for item in command_contracts if item["operation"] not in inbox_commands)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["emitted_event"] is None for item in query_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "asset_lifecycle",
        "operations": operations,
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "scenario_methods": ("preview_depreciation_plan",),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    table_scope = contract["owned_tables"] or contract["read_tables"]
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "asset_lifecycle",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "side_effects": (),
    }


class AssetLifecycleService:
    """Side-effect-free facade for route-bound operations and slice previews."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "asset_lifecycle",
            "operation": operation_name,
            "operation_kind": operation_kind,
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if operation_kind == "command":
            event_type = plan.get("emitted_event")
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (event_type,) if event_type else (),
                }
            )
        elif operation_kind == "query":
            result.update(
                {
                    "query": operation_name,
                    "read_only": True,
                    "outbox_table": None,
                    "emits": (),
                }
            )
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_assets(self, payload=None):
        return self._command("command_assets", payload or {})

    def command_assets_asset_id_service(self, payload=None):
        return self._command("command_assets_asset_id_service", payload or {})

    def command_assets_asset_id_depreciation_schedules(self, payload=None):
        return self._command("command_assets_asset_id_depreciation_schedules", payload or {})

    def command_depreciation_runs(self, payload=None):
        return self._command("command_depreciation_runs", payload or {})

    def command_assets_asset_id_transfers(self, payload=None):
        return self._command("command_assets_asset_id_transfers", payload or {})

    def command_assets_asset_id_revaluations(self, payload=None):
        return self._command("command_assets_asset_id_revaluations", payload or {})

    def command_assets_asset_id_impairments(self, payload=None):
        return self._command("command_assets_asset_id_impairments", payload or {})

    def command_assets_asset_id_maintenance_adjustments(self, payload=None):
        return self._command("command_assets_asset_id_maintenance_adjustments", payload or {})

    def command_assets_asset_id_retirements(self, payload=None):
        return self._command("command_assets_asset_id_retirements", payload or {})

    def command_assets_events_inbox(self, payload=None):
        return self._command("command_assets_events_inbox", payload or {})

    def query_assets(self, payload=None):
        return self._query("query_assets", payload or {})

    def query_assets_asset_id_risk(self, payload=None):
        return self._query("query_assets_asset_id_risk", payload or {})

    def preview_depreciation_plan(self, payload=None):
        """Preview a schedule build or revision using the package-local engine."""
        supplied = dict(payload or {})
        asset = dict(supplied.get("asset") or supplied)
        if not asset.get("asset_id"):
            return {"ok": False, "reason": "missing_asset_id", "side_effects": ()}
        asset.setdefault("status", "in_service")
        asset.setdefault("book", "corporate")
        asset.setdefault("service_date", "2026-01-01")
        asset.setdefault("book_value", asset.get("cost", 0.0))
        asset.setdefault("residual_value", 0.0)
        asset.setdefault("depreciation_months_posted", 0)
        asset.setdefault("next_depreciation_period", asset["service_date"][:7])
        current_schedule = supplied.get("current_schedule") or {}
        preview = build_schedule_version(
            asset,
            method=supplied.get("method", "straight_line"),
            version=int(supplied.get("version") or current_schedule.get("version", asset.get("active_schedule_version", 0)) + 1),
            revision_reason=supplied.get("revision_reason", "preview"),
            effective_period=supplied.get("effective_period") or asset.get("next_depreciation_period"),
            prior_schedule=current_schedule or None,
        )
        return {
            "ok": preview["ok"],
            "pbc": "asset_lifecycle",
            "operation": "preview_depreciation_plan",
            "preview": preview,
            "operation_contract": operation_plan("command_assets_asset_id_depreciation_schedules", {"asset_id": asset["asset_id"]}),
            "side_effects": (),
        }


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = AssetLifecycleService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith("command_") or name.startswith("query_"))
        and callable(getattr(service, name))
    )
    contracts = service_operation_contracts()
    return {
        "ok": bool(operations) and contracts["ok"],
        "pbc": "asset_lifecycle",
        "service_class": service.__class__.__name__,
        "operations": operations,
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "scenario_methods": contracts["scenario_methods"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test():
    """Execute one route-bound service operation through the facade."""
    manifest = service_operation_manifest()
    service = AssetLifecycleService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = getattr(service, operation)({"smoke": True}) if operation else {"ok": False}
    preview = service.preview_depreciation_plan(
        {
            "asset": {
                "asset_id": "asset_smoke",
                "cost": 12000,
                "book_value": 12000,
                "residual_value": 2000,
                "useful_life_months": 60,
                "service_date": "2026-01-01",
            }
        }
    )
    return {
        "ok": manifest["ok"]
        and result.get("ok") is True
        and result.get("operation_contract", {}).get("ok") is True
        and preview.get("ok") is True,
        "manifest": manifest,
        "result": result,
        "preview": preview,
        "side_effects": (),
    }



def standalone_service_operation_contracts():
    contracts=(
        {'operation':'seed_demo_workspace','operation_kind':'command','method':'POST','path':'/app/asset-lifecycle/demo-workspace','table':'asset_lifecycle_asset_configuration','wizard':'AssetCapitalizationWizard','permission':'asset_lifecycle.configure'},
        {'operation':'build_workbench','operation_kind':'query','method':'GET','path':'/app/asset-lifecycle/workbench','table':'asset_lifecycle_fixed_asset','wizard':None,'permission':'asset_lifecycle.read'},
        {'operation':'register_asset','operation_kind':'command','method':'POST','path':'/app/asset-lifecycle/assets','table':'asset_lifecycle_fixed_asset','wizard':'AssetCapitalizationWizard','permission':'asset_lifecycle.register'},
        {'operation':'run_depreciation','operation_kind':'command','method':'POST','path':'/app/asset-lifecycle/depreciation-runs','table':'asset_lifecycle_asset_depreciation_run','wizard':'DepreciationRunWizard','permission':'asset_lifecycle.depreciation'},
        {'operation':'transfer_asset','operation_kind':'command','method':'POST','path':'/app/asset-lifecycle/transfers','table':'asset_lifecycle_asset_transfer','wizard':'AssetTransferWizard','permission':'asset_lifecycle.transfer'},
        {'operation':'generate_asset_audit_proof','operation_kind':'command','method':'POST','path':'/app/asset-lifecycle/audit-proofs','table':'asset_lifecycle_asset_audit_proof','wizard':'AssetAuditProofWizard','permission':'asset_lifecycle.audit'},
    )
    return {'format':'appgen.asset-lifecycle-standalone-service.v1','ok':all(i['table'].startswith('asset_lifecycle_') for i in contracts),'pbc':'asset_lifecycle','contracts':contracts,'operations':tuple(i['operation'] for i in contracts),'command_operations':tuple(i['operation'] for i in contracts if i['operation_kind']=='command'),'query_operations':tuple(i['operation'] for i in contracts if i['operation_kind']=='query'),'side_effects':()}

class AssetLifecycleStandaloneService:
    def __init__(self,repository=None,database_path=':memory:'):
        if repository is None:
            from .repository import AssetLifecycleStandaloneRepository
            repository=AssetLifecycleStandaloneRepository(database_path=database_path)
        self.repository=repository
    def close(self): self.repository.close()
    def seed_demo_workspace(self,tenant='tenant_demo'): return self.repository.seed_demo_workspace(tenant=tenant)
    def build_workbench(self,tenant='tenant_demo'): return self.repository.build_workbench(tenant)
    def register_asset(self,tenant,asset): return self.repository.register_asset(tenant,asset)
    def run_depreciation(self,tenant,run_id,period): return self.repository.run_depreciation(tenant,run_id,period)
    def transfer_asset(self,tenant,asset_id,location,cost_center,approved_by): return self.repository.transfer_asset(tenant,asset_id,location,cost_center,approved_by)
    def generate_asset_audit_proof(self,tenant,asset_id,disclosure=('asset_id','status','book_value','location')): return self.repository.generate_asset_audit_proof(tenant,asset_id,tuple(disclosure))
