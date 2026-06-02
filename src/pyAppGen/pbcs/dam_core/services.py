"""Command and query service layer for the dam_core PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from . import runtime


_COMMAND_OPERATION_SPECS = (
    {"operation": "command_configure_runtime", "method": "POST", "path": "/api/pbc/dam_core/runtime/configuration", "permission": "dam_core.configure", "owned_tables": ("dam_core_dam_configuration",), "emitted_event": None},
    {"operation": "command_set_parameter", "method": "POST", "path": "/api/pbc/dam_core/runtime/parameters", "permission": "dam_core.configure", "owned_tables": ("dam_core_dam_parameter",), "emitted_event": None},
    {"operation": "command_register_rule", "method": "POST", "path": "/api/pbc/dam_core/runtime/rules", "permission": "dam_core.configure", "owned_tables": ("dam_core_dam_rule",), "emitted_event": None},
    {"operation": "command_receive_event", "method": "POST", "path": "/api/pbc/dam_core/events/inbox", "permission": "dam_core.event.consume", "owned_tables": ("dam_core_appgen_inbox_event", "dam_core_dead_letter_event", "dam_core_product_projection"), "emitted_event": None},
    {"operation": "command_register_asset", "method": "POST", "path": "/api/pbc/dam_core/assets", "permission": "dam_core.asset.write", "owned_tables": ("dam_core_asset", "dam_core_asset_binary", "dam_core_asset_fingerprint", "dam_core_appgen_outbox_event"), "emitted_event": "AssetRegistered"},
    {"operation": "command_create_asset_collection", "method": "POST", "path": "/api/pbc/dam_core/collections", "permission": "dam_core.asset.write", "owned_tables": ("dam_core_asset_collection", "dam_core_appgen_outbox_event"), "emitted_event": "AssetCollectionCreated"},
    {"operation": "command_add_asset_to_collection", "method": "POST", "path": "/api/pbc/dam_core/collection-members", "permission": "dam_core.asset.write", "owned_tables": ("dam_core_asset_collection_member", "dam_core_asset_collection", "dam_core_appgen_outbox_event"), "emitted_event": "AssetAddedToCollection"},
    {"operation": "command_attach_rights_policy", "method": "POST", "path": "/api/pbc/dam_core/rights-policies", "permission": "dam_core.rights.manage", "owned_tables": ("dam_core_rights_policy", "dam_core_appgen_outbox_event"), "emitted_event": "AssetRightsPolicyAttached"},
    {"operation": "command_register_license_agreement", "method": "POST", "path": "/api/pbc/dam_core/license-agreements", "permission": "dam_core.rights.manage", "owned_tables": ("dam_core_license_agreement", "dam_core_appgen_outbox_event"), "emitted_event": "LicenseAgreementRegistered"},
    {"operation": "command_grant_usage_entitlement", "method": "POST", "path": "/api/pbc/dam_core/usage-entitlements", "permission": "dam_core.rights.manage", "owned_tables": ("dam_core_usage_entitlement", "dam_core_appgen_outbox_event"), "emitted_event": "UsageEntitlementGranted"},
    {"operation": "command_register_metadata_taxonomy", "method": "POST", "path": "/api/pbc/dam_core/metadata-taxonomies", "permission": "dam_core.metadata.write", "owned_tables": ("dam_core_metadata_taxonomy", "dam_core_appgen_outbox_event"), "emitted_event": "MetadataTaxonomyRegistered"},
    {"operation": "command_add_metadata_tag", "method": "POST", "path": "/api/pbc/dam_core/tags", "permission": "dam_core.metadata.write", "owned_tables": ("dam_core_metadata_tag", "dam_core_asset", "dam_core_appgen_outbox_event"), "emitted_event": "AssetMetadataTagged"},
    {"operation": "command_enrich_metadata", "method": "POST", "path": "/api/pbc/dam_core/metadata-enrichments", "permission": "dam_core.metadata.write", "owned_tables": ("dam_core_metadata_enrichment", "dam_core_appgen_outbox_event"), "emitted_event": "MetadataEnriched"},
    {"operation": "command_add_semantic_annotation", "method": "POST", "path": "/api/pbc/dam_core/semantic-annotations", "permission": "dam_core.metadata.write", "owned_tables": ("dam_core_semantic_annotation", "dam_core_appgen_outbox_event"), "emitted_event": "SemanticAnnotationAdded"},
    {"operation": "command_request_rendition", "method": "POST", "path": "/api/pbc/dam_core/renditions", "permission": "dam_core.rendition.write", "owned_tables": ("dam_core_asset_rendition", "dam_core_asset", "dam_core_appgen_outbox_event"), "emitted_event": "AssetRenditionRequested"},
    {"operation": "command_complete_rendition", "method": "POST", "path": "/api/pbc/dam_core/renditions/complete", "permission": "dam_core.rendition.write", "owned_tables": ("dam_core_asset_rendition", "dam_core_appgen_outbox_event"), "emitted_event": "AssetRenditionReady"},
    {"operation": "command_start_asset_workflow", "method": "POST", "path": "/api/pbc/dam_core/workflows", "permission": "dam_core.workflow", "owned_tables": ("dam_core_asset_workflow_case", "dam_core_asset_review_task", "dam_core_appgen_outbox_event"), "emitted_event": "AssetWorkflowStarted"},
    {"operation": "command_complete_asset_review_task", "method": "POST", "path": "/api/pbc/dam_core/review-tasks/complete", "permission": "dam_core.workflow", "owned_tables": ("dam_core_asset_review_task", "dam_core_asset_workflow_case", "dam_core_appgen_outbox_event"), "emitted_event": "AssetReviewTaskCompleted"},
    {"operation": "command_open_asset_exception", "method": "POST", "path": "/api/pbc/dam_core/exceptions", "permission": "dam_core.workflow", "owned_tables": ("dam_core_asset_exception", "dam_core_appgen_outbox_event"), "emitted_event": "AssetExceptionOpened"},
    {"operation": "command_resolve_asset_exception_case", "method": "POST", "path": "/api/pbc/dam_core/exceptions/resolve", "permission": "dam_core.workflow", "owned_tables": ("dam_core_asset_exception", "dam_core_appgen_outbox_event"), "emitted_event": "AssetExceptionResolved"},
    {"operation": "command_record_asset_usage_snapshot", "method": "POST", "path": "/api/pbc/dam_core/usage-snapshots", "permission": "dam_core.audit", "owned_tables": ("dam_core_asset_usage_snapshot", "dam_core_appgen_outbox_event"), "emitted_event": "AssetUsageSnapshotRecorded"},
    {"operation": "command_detect_asset_duplicate_candidate", "method": "POST", "path": "/api/pbc/dam_core/duplicate-candidates", "permission": "dam_core.audit", "owned_tables": ("dam_core_asset_duplicate_candidate", "dam_core_appgen_outbox_event"), "emitted_event": "AssetDuplicateCandidateDetected"},
    {"operation": "command_record_asset_lineage", "method": "POST", "path": "/api/pbc/dam_core/lineage", "permission": "dam_core.audit", "owned_tables": ("dam_core_asset_lineage", "dam_core_appgen_outbox_event"), "emitted_event": "AssetLineageRecorded"},
)

_QUERY_OPERATION_SPECS = (
    {"operation": "query_rights", "method": "GET", "path": "/api/pbc/dam_core/rights/decision", "permission": "dam_core.rights.evaluate", "read_tables": ("dam_core_asset", "dam_core_rights_policy")},
    {"operation": "query_workbench", "method": "GET", "path": "/api/pbc/dam_core/workbench", "permission": "dam_core.audit", "read_tables": tuple(f"dam_core_{table}" for table in runtime.DAM_CORE_OWNED_TABLES)},
    {"operation": "query_api_contract", "method": "GET", "path": "/api/pbc/dam_core/api-contract", "permission": "dam_core.audit", "read_tables": tuple(f"dam_core_{table}" for table in runtime.DAM_CORE_OWNED_TABLES)},
    {"operation": "query_schema_contract", "method": "GET", "path": "/api/pbc/dam_core/schema-contract", "permission": "dam_core.audit", "read_tables": tuple(f"dam_core_{table}" for table in runtime.DAM_CORE_OWNED_TABLES)},
    {"operation": "query_service_contract", "method": "GET", "path": "/api/pbc/dam_core/service-contract", "permission": "dam_core.audit", "read_tables": tuple(f"dam_core_{table}" for table in runtime.DAM_CORE_OWNED_TABLES)},
    {"operation": "query_release_evidence", "method": "GET", "path": "/api/pbc/dam_core/release-evidence", "permission": "dam_core.audit", "read_tables": tuple(f"dam_core_{table}" for table in runtime.DAM_CORE_OWNED_TABLES)},
    {"operation": "query_permissions_contract", "method": "GET", "path": "/api/pbc/dam_core/permissions", "permission": "dam_core.audit", "read_tables": ("dam_core_dam_rule", "dam_core_dam_parameter", "dam_core_dam_configuration")},
    {"operation": "query_agent_surface", "method": "GET", "path": "/api/pbc/dam_core/agent", "permission": "dam_core.audit", "read_tables": ("dam_core_asset", "dam_core_appgen_outbox_event", "dam_core_appgen_inbox_event")},
)

OPERATION_CONTRACTS = tuple(
    {
        **spec,
        "operation_kind": "command",
        "read_tables": (),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "idempotency_key": f"dam_core:{spec['operation']}:idempotency_key",
    }
    for spec in _COMMAND_OPERATION_SPECS
) + tuple(
    {
        **spec,
        "operation_kind": "query",
        "owned_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "idempotency_key": None,
    }
    for spec in _QUERY_OPERATION_SPECS
)


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(not item["read_tables"] for item in command_contracts)
        and all(not item["owned_tables"] for item in query_contracts),
        "pbc": "dam_core",
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": True,
        "pbc": "dam_core",
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
        "idempotency_key": contract["idempotency_key"],
        "side_effects": (),
    }


class DamCoreService:
    """Executable package-local service facade over the DAM runtime."""

    def __init__(self, state: dict | None = None):
        self.state = state or runtime.dam_core_empty_state()

    def _command(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        result = self._apply_command(operation_name, payload)
        if "state" in result:
            self.state = result["state"]
        return {
            "ok": result.get("ok") is True,
            "pbc": "dam_core",
            "operation": operation_name,
            "operation_kind": "command",
            "payload": payload,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (plan["emitted_event"],) if plan["emitted_event"] else (),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def _query(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        result = self._apply_query(operation_name, payload)
        return {
            "ok": result.get("ok") is True,
            "pbc": "dam_core",
            "operation": operation_name,
            "operation_kind": "query",
            "payload": payload,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "emits": (),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def _apply_command(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "command_configure_runtime":
            return runtime.dam_core_configure_runtime(self.state, payload["configuration"])
        if operation_name == "command_set_parameter":
            return runtime.dam_core_set_parameter(self.state, payload["name"], payload["value"])
        if operation_name == "command_register_rule":
            return runtime.dam_core_register_rule(self.state, payload["rule"])
        if operation_name == "command_receive_event":
            return runtime.dam_core_receive_event(self.state, payload["envelope"], simulate_failure=payload.get("simulate_failure", False))
        if operation_name == "command_register_asset":
            return runtime.dam_core_register_asset(self.state, payload["asset"])
        if operation_name == "command_create_asset_collection":
            return runtime.dam_core_create_asset_collection(self.state, payload["collection"])
        if operation_name == "command_add_asset_to_collection":
            return runtime.dam_core_add_asset_to_collection(self.state, payload["member"])
        if operation_name == "command_attach_rights_policy":
            return runtime.dam_core_attach_rights_policy(self.state, payload["policy"])
        if operation_name == "command_register_license_agreement":
            return runtime.dam_core_register_license_agreement(self.state, payload["agreement"])
        if operation_name == "command_grant_usage_entitlement":
            return runtime.dam_core_grant_usage_entitlement(self.state, payload["entitlement"])
        if operation_name == "command_register_metadata_taxonomy":
            return runtime.dam_core_register_metadata_taxonomy(self.state, payload["taxonomy"])
        if operation_name == "command_add_metadata_tag":
            return runtime.dam_core_add_metadata_tag(self.state, payload["tag"])
        if operation_name == "command_enrich_metadata":
            return runtime.dam_core_enrich_metadata(self.state, payload["enrichment"])
        if operation_name == "command_add_semantic_annotation":
            return runtime.dam_core_add_semantic_annotation(self.state, payload["annotation"])
        if operation_name == "command_request_rendition":
            return runtime.dam_core_request_rendition(self.state, payload["rendition"])
        if operation_name == "command_complete_rendition":
            return runtime.dam_core_complete_rendition(self.state, payload["rendition_id"], payload["result"])
        if operation_name == "command_start_asset_workflow":
            return runtime.dam_core_start_asset_workflow(self.state, payload["workflow"])
        if operation_name == "command_complete_asset_review_task":
            return runtime.dam_core_complete_asset_review_task(self.state, payload["task_id"], payload["decision"])
        if operation_name == "command_open_asset_exception":
            return runtime.dam_core_open_asset_exception(self.state, payload["exception"])
        if operation_name == "command_resolve_asset_exception_case":
            return runtime.dam_core_resolve_asset_exception_case(self.state, payload["exception_id"], payload["resolution"])
        if operation_name == "command_record_asset_usage_snapshot":
            return runtime.dam_core_record_asset_usage_snapshot(self.state, payload["snapshot"])
        if operation_name == "command_detect_asset_duplicate_candidate":
            return runtime.dam_core_detect_asset_duplicate_candidate(self.state, payload["candidate"])
        if operation_name == "command_record_asset_lineage":
            return runtime.dam_core_record_asset_lineage(self.state, payload["lineage"])
        raise ValueError(f"Unsupported DAM Core command: {operation_name}")

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "query_rights":
            return runtime.dam_core_enforce_rights(self.state, payload["asset_id"], market=payload["market"], use_case=payload.get("use_case", "workbench"))
        if operation_name == "query_workbench":
            return runtime.dam_core_build_workbench_view(self.state, tenant=payload["tenant"])
        if operation_name == "query_api_contract":
            return runtime.dam_core_build_api_contract()
        if operation_name == "query_schema_contract":
            return runtime.dam_core_build_schema_contract()
        if operation_name == "query_service_contract":
            return runtime.dam_core_build_service_contract()
        if operation_name == "query_release_evidence":
            from . import release_evidence

            return release_evidence.build_release_evidence()
        if operation_name == "query_permissions_contract":
            return runtime.dam_core_permissions_contract()
        if operation_name == "query_agent_surface":
            from . import agent

            return agent.composed_agent_contribution()
        raise ValueError(f"Unsupported DAM Core query: {operation_name}")

    def command_configure_runtime(self, payload: dict | None = None) -> dict:
        return self._command("command_configure_runtime", payload)

    def command_set_parameter(self, payload: dict | None = None) -> dict:
        return self._command("command_set_parameter", payload)

    def command_register_rule(self, payload: dict | None = None) -> dict:
        return self._command("command_register_rule", payload)

    def command_receive_event(self, payload: dict | None = None) -> dict:
        return self._command("command_receive_event", payload)

    def command_register_asset(self, payload: dict | None = None) -> dict:
        return self._command("command_register_asset", payload)

    def command_create_asset_collection(self, payload: dict | None = None) -> dict:
        return self._command("command_create_asset_collection", payload)

    def command_add_asset_to_collection(self, payload: dict | None = None) -> dict:
        return self._command("command_add_asset_to_collection", payload)

    def command_attach_rights_policy(self, payload: dict | None = None) -> dict:
        return self._command("command_attach_rights_policy", payload)

    def command_register_license_agreement(self, payload: dict | None = None) -> dict:
        return self._command("command_register_license_agreement", payload)

    def command_grant_usage_entitlement(self, payload: dict | None = None) -> dict:
        return self._command("command_grant_usage_entitlement", payload)

    def command_register_metadata_taxonomy(self, payload: dict | None = None) -> dict:
        return self._command("command_register_metadata_taxonomy", payload)

    def command_add_metadata_tag(self, payload: dict | None = None) -> dict:
        return self._command("command_add_metadata_tag", payload)

    def command_enrich_metadata(self, payload: dict | None = None) -> dict:
        return self._command("command_enrich_metadata", payload)

    def command_add_semantic_annotation(self, payload: dict | None = None) -> dict:
        return self._command("command_add_semantic_annotation", payload)

    def command_request_rendition(self, payload: dict | None = None) -> dict:
        return self._command("command_request_rendition", payload)

    def command_complete_rendition(self, payload: dict | None = None) -> dict:
        return self._command("command_complete_rendition", payload)

    def command_start_asset_workflow(self, payload: dict | None = None) -> dict:
        return self._command("command_start_asset_workflow", payload)

    def command_complete_asset_review_task(self, payload: dict | None = None) -> dict:
        return self._command("command_complete_asset_review_task", payload)

    def command_open_asset_exception(self, payload: dict | None = None) -> dict:
        return self._command("command_open_asset_exception", payload)

    def command_resolve_asset_exception_case(self, payload: dict | None = None) -> dict:
        return self._command("command_resolve_asset_exception_case", payload)

    def command_record_asset_usage_snapshot(self, payload: dict | None = None) -> dict:
        return self._command("command_record_asset_usage_snapshot", payload)

    def command_detect_asset_duplicate_candidate(self, payload: dict | None = None) -> dict:
        return self._command("command_detect_asset_duplicate_candidate", payload)

    def command_record_asset_lineage(self, payload: dict | None = None) -> dict:
        return self._command("command_record_asset_lineage", payload)

    def query_rights(self, payload: dict | None = None) -> dict:
        return self._query("query_rights", payload)

    def query_workbench(self, payload: dict | None = None) -> dict:
        return self._query("query_workbench", payload)

    def query_api_contract(self, payload: dict | None = None) -> dict:
        return self._query("query_api_contract", payload)

    def query_schema_contract(self, payload: dict | None = None) -> dict:
        return self._query("query_schema_contract", payload)

    def query_service_contract(self, payload: dict | None = None) -> dict:
        return self._query("query_service_contract", payload)

    def query_release_evidence(self, payload: dict | None = None) -> dict:
        return self._query("query_release_evidence", payload)

    def query_permissions_contract(self, payload: dict | None = None) -> dict:
        return self._query("query_permissions_contract", payload)

    def query_agent_surface(self, payload: dict | None = None) -> dict:
        return self._query("query_agent_surface", payload)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    service = DamCoreService()
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": "dam_core",
        "service_class": service.__class__.__name__,
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute configuration, one command, and one query through the facade."""
    service = DamCoreService()
    service.command_configure_runtime(
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": runtime.DAM_CORE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_storage_tier": "warm",
                "allowed_mime_types": ("image/jpeg",),
                "rendition_profiles": ("web_large",),
                "rights_default_decision": "review",
                "metadata_taxonomies": ("product",),
                "default_locale": "en-US",
                "workbench_limit": 100,
            }
        }
    )
    service.command_set_parameter({"name": "max_asset_size_mb", "value": 100})
    service.command_set_parameter({"name": "metadata_confidence_floor", "value": 0.6})
    service.command_register_asset(
        {
            "asset": {
                "asset_id": "asset_smoke",
                "tenant": "tenant_smoke",
                "filename": "asset.jpg",
                "mime_type": "image/jpeg",
                "size_mb": 12,
                "storage_uri": "object://dam/smoke/asset.jpg",
                "binary": b"smoke-asset",
                "created_by": "smoke",
            }
        }
    )
    query = service.query_workbench({"tenant": "tenant_smoke"})
    return {
        "ok": service_operation_manifest()["ok"] and query["ok"] and query["result"]["asset_count"] == 1,
        "manifest": service_operation_manifest(),
        "result": query,
        "side_effects": (),
    }
