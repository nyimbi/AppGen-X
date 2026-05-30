"""Stateful service layer for the advertising campaign standalone slice."""

from __future__ import annotations

from .agent import campaign_brief_preview
from .agent import document_instruction_plan
from .agent import launch_readiness_preview
from .permissions import ACTION_PERMISSIONS
from .runtime import ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES
from .runtime import advertising_campaign_operations_attempt_launch_campaign
from .runtime import advertising_campaign_operations_build_workbench_view
from .runtime import advertising_campaign_operations_configure_runtime
from .runtime import advertising_campaign_operations_create_campaign_plan
from .runtime import advertising_campaign_operations_empty_state
from .runtime import advertising_campaign_operations_query_workbench
from .runtime import advertising_campaign_operations_receive_event
from .runtime import advertising_campaign_operations_register_rule
from .runtime import advertising_campaign_operations_register_schema_extension
from .runtime import advertising_campaign_operations_review_launch_readiness
from .runtime import advertising_campaign_operations_set_parameter
from .workflows import workflow_catalog

PBC_KEY = "advertising_campaign_operations"
API_PREFIX = f"/api/pbc/{PBC_KEY}"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
SERVICE_CONTRACTS = (
    {
        "operation": "configure_runtime",
        "operation_kind": "command",
        "method": "POST",
        "path": f"{API_PREFIX}/runtime/configuration",
        "permission": ACTION_PERMISSIONS["configure_runtime"],
        "owned_tables": (f"{PBC_KEY}_advertising_campaign_operations_runtime_parameter",),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "set_parameter",
        "operation_kind": "command",
        "method": "POST",
        "path": f"{API_PREFIX}/runtime/parameters",
        "permission": ACTION_PERMISSIONS["set_parameter"],
        "owned_tables": (f"{PBC_KEY}_advertising_campaign_operations_runtime_parameter",),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "register_rule",
        "operation_kind": "command",
        "method": "POST",
        "path": f"{API_PREFIX}/runtime/rules",
        "permission": ACTION_PERMISSIONS["register_rule"],
        "owned_tables": (f"{PBC_KEY}_advertising_campaign_operations_policy_rule",),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "register_schema_extension",
        "operation_kind": "command",
        "method": "POST",
        "path": f"{API_PREFIX}/runtime/schema-extensions",
        "permission": ACTION_PERMISSIONS["register_schema_extension"],
        "owned_tables": (f"{PBC_KEY}_advertising_campaign_operations_schema_extension",),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "receive_event",
        "operation_kind": "command",
        "method": "POST",
        "path": f"{API_PREFIX}/events/inbox",
        "permission": ACTION_PERMISSIONS["receive_event"],
        "owned_tables": (EVENT_CONTRACT["inbox_table"], EVENT_CONTRACT["dead_letter_table"]),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "create_campaign_plan",
        "operation_kind": "command",
        "method": "POST",
        "path": f"{API_PREFIX}/campaign-plans",
        "permission": ACTION_PERMISSIONS["create_campaign_plan"],
        "owned_tables": (f"{PBC_KEY}_ad_campaign", EVENT_CONTRACT["outbox_table"]),
        "read_tables": (),
        "emitted_event": "AdvertisingCampaignOperationsCreated",
    },
    {
        "operation": "attempt_launch_campaign",
        "operation_kind": "command",
        "method": "POST",
        "path": f"{API_PREFIX}/launch-attempts",
        "permission": ACTION_PERMISSIONS["attempt_launch_campaign"],
        "owned_tables": (f"{PBC_KEY}_ad_campaign", EVENT_CONTRACT["outbox_table"]),
        "read_tables": (),
        "emitted_event": (
            "AdvertisingCampaignOperationsApproved",
            "AdvertisingCampaignOperationsExceptionOpened",
        ),
    },
    {
        "operation": "review_launch_readiness",
        "operation_kind": "query",
        "method": "POST",
        "path": f"{API_PREFIX}/launch-reviews",
        "permission": ACTION_PERMISSIONS["review_launch_readiness"],
        "owned_tables": (),
        "read_tables": (f"{PBC_KEY}_ad_campaign",),
        "emitted_event": None,
    },
    {
        "operation": "query_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": f"{API_PREFIX}/workbench",
        "permission": ACTION_PERMISSIONS["query_workbench"],
        "owned_tables": (),
        "read_tables": (
            f"{PBC_KEY}_ad_campaign",
            f"{PBC_KEY}_campaign_budget",
            f"{PBC_KEY}_media_placement",
            f"{PBC_KEY}_creative_asset",
            f"{PBC_KEY}_audience_segment",
        ),
        "emitted_event": None,
    },
    {
        "operation": "document_instruction_plan",
        "operation_kind": "query",
        "method": "POST",
        "path": f"{API_PREFIX}/assistant/document-plans",
        "permission": ACTION_PERMISSIONS["document_instruction_plan"],
        "owned_tables": (),
        "read_tables": ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES[:5],
        "emitted_event": None,
    },
    {
        "operation": "campaign_brief_preview",
        "operation_kind": "query",
        "method": "POST",
        "path": f"{API_PREFIX}/assistant/brief-previews",
        "permission": ACTION_PERMISSIONS["campaign_brief_preview"],
        "owned_tables": (),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "launch_readiness_preview",
        "operation_kind": "query",
        "method": "POST",
        "path": f"{API_PREFIX}/assistant/launch-previews",
        "permission": ACTION_PERMISSIONS["launch_readiness_preview"],
        "owned_tables": (),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "query_release_snapshot",
        "operation_kind": "query",
        "method": "GET",
        "path": f"{API_PREFIX}/release-snapshot",
        "permission": ACTION_PERMISSIONS["query_release_snapshot"],
        "owned_tables": (),
        "read_tables": ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES,
        "emitted_event": None,
    },
    {
        "operation": "query_service_contract",
        "operation_kind": "query",
        "method": "GET",
        "path": f"{API_PREFIX}/service-contract",
        "permission": ACTION_PERMISSIONS["query_service_contract"],
        "owned_tables": (),
        "read_tables": (),
        "emitted_event": None,
    },
)
COMMAND_OPERATIONS = tuple(
    contract["operation"] for contract in SERVICE_CONTRACTS if contract["operation_kind"] == "command"
)
QUERY_OPERATIONS = tuple(
    contract["operation"] for contract in SERVICE_CONTRACTS if contract["operation_kind"] == "query"
)


def _contract_for(operation: str) -> dict:
    contract = next(item for item in SERVICE_CONTRACTS if item["operation"] == operation)
    return {
        **contract,
        "idempotency_key": f"{PBC_KEY}:{operation}" if contract["operation_kind"] == "command" else None,
        "idempotency_required": contract["operation_kind"] == "command",
        "transaction_boundary": "owned_datastore_plus_outbox" if contract["operation_kind"] == "command" else "read_only_projection",
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


class AdvertisingCampaignOperationsService:
    """In-memory service facade that owns the PBC runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or advertising_campaign_operations_empty_state()

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS or name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._invoke(_name, payload or {})
        raise AttributeError(name)

    def _invoke(self, operation: str, payload: dict) -> dict:
        contract = _contract_for(operation)
        if contract["operation_kind"] == "command":
            result = self._invoke_command(operation, payload)
        else:
            result = self._invoke_query(operation, payload)
        return {
            **result,
            "operation": operation,
            "operation_kind": contract["operation_kind"],
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"] if contract["operation_kind"] == "command" else None,
            "emits": ()
            if result.get("emitted_event") is None
            else result["emitted_event"]
            if isinstance(result.get("emitted_event"), tuple)
            else (result["emitted_event"],),
            "transaction_boundary": contract["transaction_boundary"],
        }

    def _invoke_command(self, operation: str, payload: dict) -> dict:
        if operation == "configure_runtime":
            result = advertising_campaign_operations_configure_runtime(self.state, payload.get("configuration") or payload)
        elif operation == "set_parameter":
            result = advertising_campaign_operations_set_parameter(self.state, payload["name"], payload["value"])
        elif operation == "register_rule":
            result = advertising_campaign_operations_register_rule(self.state, payload.get("rule") or payload)
        elif operation == "register_schema_extension":
            result = advertising_campaign_operations_register_schema_extension(self.state, payload["table"], payload.get("fields") or {})
        elif operation == "receive_event":
            result = advertising_campaign_operations_receive_event(self.state, payload.get("envelope") or payload.get("event") or payload)
        elif operation == "create_campaign_plan":
            result = advertising_campaign_operations_create_campaign_plan(self.state, payload.get("campaign") or payload)
        elif operation == "attempt_launch_campaign":
            result = advertising_campaign_operations_attempt_launch_campaign(self.state, payload.get("campaign") or payload)
        else:
            raise AttributeError(operation)
        if "state" in result:
            self.state = result["state"]
        emitted_event = None
        if operation == "create_campaign_plan" and result.get("ok"):
            emitted_event = "AdvertisingCampaignOperationsCreated"
        elif operation == "attempt_launch_campaign":
            emitted_event = "AdvertisingCampaignOperationsApproved" if result.get("ready") else "AdvertisingCampaignOperationsExceptionOpened"
        return {**result, "read_only": False, "emitted_event": emitted_event, "side_effects": ()}

    def _invoke_query(self, operation: str, payload: dict) -> dict:
        if operation == "review_launch_readiness":
            result = advertising_campaign_operations_review_launch_readiness(self.state, payload)
        elif operation == "query_workbench":
            tenant = payload.get("tenant", "default")
            snapshot = advertising_campaign_operations_query_workbench(self.state, {"tenant": tenant})
            view = advertising_campaign_operations_build_workbench_view(tenant=tenant, state=self.state)
            result = {
                "ok": snapshot["ok"] and view["ok"],
                "tenant": tenant,
                "snapshot": snapshot,
                "workbench": view,
                "command_center": snapshot["command_center"],
                "side_effects": (),
            }
        elif operation == "document_instruction_plan":
            result = document_instruction_plan(payload.get("document", ""), payload.get("instruction", ""))
        elif operation == "campaign_brief_preview":
            result = campaign_brief_preview(payload)
        elif operation == "launch_readiness_preview":
            result = launch_readiness_preview(payload)
        elif operation == "query_release_snapshot":
            from .release_evidence import build_release_evidence

            result = build_release_evidence(state=self.state)
        elif operation == "query_service_contract":
            result = service_operation_contracts()
        else:
            raise AttributeError(operation)
        return {**result, "read_only": True, "emitted_event": None, "side_effects": ()}


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "AdvertisingCampaignOperationsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "workflow_catalog": workflow_catalog()["workflows"],
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_contract_for(item["operation"]) for item in SERVICE_CONTRACTS)
    return {
        "format": "appgen.advertising-campaign-operations-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = AdvertisingCampaignOperationsService()
    config_result = service.configure_runtime({"configuration": {"database_backend": "postgresql", "event_topic": "pbc.advertising_campaign_operations.events", "workbench_limit": 50}})
    plan_result = service.create_campaign_plan(
        {
            "tenant": "tenant-smoke",
            "code": "SMOKE",
            "brief": {
                "objective": "Acquire qualified signups",
                "offer": "30 day trial",
                "audience_promise": "Reach in-market buyers",
                "channels": ("search", "social"),
                "primary_kpi": "qualified_signups",
                "guardrails": ("cpa",),
                "launch_dependencies": ("tracking",),
            },
        }
    )
    launch_result = service.attempt_launch_campaign(
        {
            "campaign_id": "SMOKE",
            "readiness": {
                "budget_approved": True,
                "creative_approved": True,
                "audience_ready": True,
                "placements_ready": True,
                "tracking_ready": True,
                "suppliers_eligible": True,
                "policy_compliant": True,
                "dependency_status": {"tracking": True},
            },
        }
    )
    workbench = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": config_result["ok"] and plan_result["ok"] and launch_result["ok"] and workbench["ok"] and service_operation_contracts()["ok"],
        "config": config_result,
        "plan": plan_result,
        "launch": launch_result,
        "workbench": workbench,
        "side_effects": (),
    }
