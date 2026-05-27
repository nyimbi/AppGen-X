"""Command service layer for the enterprise_search_vector PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .runtime import ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES
from .runtime import enterprise_search_vector_build_service_contract


PBC_KEY = "enterprise_search_vector"

_ROUTE_DEFINITIONS = (
    {
        "route": "POST /indexes",
        "operation": "create_index",
        "kind": "command",
        "owned_tables": ("search_index",),
        "permission": "enterprise_search_vector.index.write",
        "emitted_event": "SearchIndexUpdated",
        "idempotency_key": "index_id",
    },
    {
        "route": "POST /indexes/{id}/refresh",
        "operation": "refresh_index",
        "kind": "command",
        "owned_tables": ("search_index", "vector_document"),
        "permission": "enterprise_search_vector.index.write",
        "emitted_event": "SearchIndexUpdated",
        "idempotency_key": "refresh_id",
    },
    {
        "route": "POST /documents",
        "operation": "ingest_document",
        "kind": "command",
        "owned_tables": ("vector_document", "search_index"),
        "permission": "enterprise_search_vector.document.write",
        "emitted_event": "SearchIndexUpdated",
        "idempotency_key": "document_id",
    },
    {
        "route": "POST /embeddings",
        "operation": "run_embedding_job",
        "kind": "command",
        "owned_tables": ("embedding_job", "vector_document", "search_index"),
        "permission": "enterprise_search_vector.document.write",
        "emitted_event": "SearchIndexUpdated",
        "idempotency_key": "job_id",
    },
    {
        "route": "POST /search",
        "operation": "query",
        "kind": "command",
        "owned_tables": ("query_trace", "search_index"),
        "permission": "enterprise_search_vector.query",
        "emitted_event": "DiscoveryInsightGenerated",
        "idempotency_key": "query_id",
    },
    {
        "route": "POST /query-feedback",
        "operation": "record_feedback",
        "kind": "command",
        "owned_tables": ("query_trace", "vector_document", "search_index"),
        "permission": "enterprise_search_vector.query",
        "emitted_event": "SearchIndexUpdated",
        "idempotency_key": "query_id:document_id",
    },
    {
        "route": "POST /ranking-simulations",
        "operation": "simulate_counterfactual_ranking",
        "kind": "command",
        "owned_tables": ("ranking_simulation", "query_trace"),
        "permission": "enterprise_search_vector.intelligence.write",
        "emitted_event": None,
        "idempotency_key": "simulation_id",
    },
    {
        "route": "POST /freshness-forecasts",
        "operation": "forecast_index_freshness",
        "kind": "command",
        "owned_tables": ("freshness_forecast", "search_index", "vector_document"),
        "permission": "enterprise_search_vector.intelligence.write",
        "emitted_event": None,
        "idempotency_key": "forecast_id",
    },
    {
        "route": "POST /quality-remediations",
        "operation": "remediate_search_quality",
        "kind": "command",
        "owned_tables": ("quality_remediation", "vector_document", "search_index"),
        "permission": "enterprise_search_vector.quality.write",
        "emitted_event": "SearchIndexUpdated",
        "idempotency_key": "remediation_id",
    },
    {
        "route": "POST /policy-screenings",
        "operation": "screen_search_policy",
        "kind": "command",
        "owned_tables": ("search_policy_screening",),
        "permission": "enterprise_search_vector.policy.write",
        "emitted_event": None,
        "idempotency_key": "screening_id",
    },
    {
        "route": "POST /relevance-controls",
        "operation": "run_relevance_controls",
        "kind": "command",
        "owned_tables": ("relevance_control_assertion", "query_trace"),
        "permission": "enterprise_search_vector.audit",
        "emitted_event": None,
        "idempotency_key": "assertion_id",
    },
    {
        "route": "POST /index-proofs",
        "operation": "generate_index_proof",
        "kind": "command",
        "owned_tables": ("index_proof", "search_audit_entry", "search_index"),
        "permission": "enterprise_search_vector.audit",
        "emitted_event": None,
        "idempotency_key": "proof_id",
    },
    {
        "route": "POST /federated-source-views",
        "operation": "federate_search_sources",
        "kind": "command",
        "owned_tables": ("federated_search_view", "search_index", "vector_document", "query_trace"),
        "permission": "enterprise_search_vector.intelligence.write",
        "emitted_event": None,
        "idempotency_key": "view_id",
    },
    {
        "route": "POST /query-intent-risks",
        "operation": "score_query_intent_risk",
        "kind": "command",
        "owned_tables": ("query_intent_risk", "query_trace"),
        "permission": "enterprise_search_vector.policy.write",
        "emitted_event": None,
        "idempotency_key": "risk_id",
    },
    {
        "route": "POST /retention-deletions",
        "operation": "record_retention_deletion",
        "kind": "command",
        "owned_tables": ("retention_deletion_record", "search_audit_entry", "vector_document"),
        "permission": "enterprise_search_vector.retention.write",
        "emitted_event": None,
        "idempotency_key": "record_id",
    },
    {
        "route": "POST /governed-models",
        "operation": "register_governed_model",
        "kind": "command",
        "owned_tables": ("search_governed_model",),
        "permission": "enterprise_search_vector.configure",
        "emitted_event": None,
        "idempotency_key": "model_id",
    },
    {
        "route": "POST /enterprise-search-vector/events/inbox",
        "operation": "receive_event",
        "kind": "command",
        "owned_tables": (),
        "permission": "enterprise_search_vector.event.consume",
        "emitted_event": "SearchIndexUpdated",
        "consumed_event": ("ProductPublished", "CustomerUpdated", "AuditEventSealed"),
        "idempotency_key": "event_id",
    },
    {
        "route": "GET /query-traces",
        "operation": "query_traces",
        "kind": "query",
        "owned_tables": ("query_trace",),
        "permission": "enterprise_search_vector.audit",
    },
    {
        "route": "GET /enterprise-search-vector-workbench",
        "operation": "build_workbench_view",
        "kind": "query",
        "owned_tables": ("search_index", "embedding_job", "vector_document", "query_trace"),
        "permission": "enterprise_search_vector.audit",
    },
    {
        "route": "GET /enterprise-search-vector/schema-contract",
        "operation": "build_schema_contract",
        "kind": "query",
        "owned_tables": ("search_index", "embedding_job", "vector_document", "query_trace"),
        "permission": "enterprise_search_vector.audit",
    },
    {
        "route": "GET /enterprise-search-vector/service-contract",
        "operation": "build_service_contract",
        "kind": "query",
        "owned_tables": ("search_index", "embedding_job", "vector_document", "query_trace"),
        "permission": "enterprise_search_vector.audit",
    },
    {
        "route": "GET /enterprise-search-vector/release-evidence",
        "operation": "build_release_evidence",
        "kind": "query",
        "owned_tables": ("search_index", "embedding_job", "vector_document", "query_trace"),
        "permission": "enterprise_search_vector.audit",
    },
)


def _method_path(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, path


def _owned_tables(route: dict) -> tuple[str, ...]:
    return tuple(
        table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        for table in route.get("owned_tables", ())
    )


def _build_operation_contracts() -> tuple[dict, ...]:
    contracts = []
    for route in _ROUTE_DEFINITIONS:
        method, path = _method_path(route["route"])
        is_command = route["kind"] == "command"
        table_scope = _owned_tables(route)
        if is_command and not table_scope and route["operation"] == "receive_event":
            table_scope = (ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[1], ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[2])
        contracts.append(
            {
                "operation": route["operation"],
                "operation_kind": route["kind"],
                "method": method,
                "path": path,
                "permission": route["permission"],
                "owned_tables": table_scope if is_command else (),
                "read_tables": () if is_command else table_scope,
                "emitted_event": route.get("emitted_event") if is_command else None,
                "consumed_event": tuple(route.get("consumed_event", ())),
                "idempotency_key": route.get("idempotency_key"),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _build_operation_contracts()


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = enterprise_search_vector_build_service_contract()
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
    table_scope = contract["owned_tables"] or contract["read_tables"] or tuple(ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES)
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
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
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


class EnterpriseSearchVectorService:
    """Side-effect-free service facade for generated route dispatch."""

    def execute_operation(self, operation_name: str, payload: dict | None = None) -> dict:
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": operation_kind,
            "payload": dict(payload or {}),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if operation_kind == "command":
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (plan.get("emitted_event"),),
                    "consumes": plan.get("consumed_event", ()),
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
        "service_class": EnterpriseSearchVectorService.__name__,
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
    service = EnterpriseSearchVectorService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = service.execute_operation(operation, {"smoke": True}) if operation else {"ok": False}
    return {
        "ok": manifest["ok"] and result.get("ok") is True and result.get("operation_contract", {}).get("ok") is True,
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }
