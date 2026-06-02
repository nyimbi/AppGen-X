"""Focused standalone tests for the master_data_governance one-PBC slice."""
from pathlib import Path

from pyAppGen.pbcs.master_data_governance import agent
from pyAppGen.pbcs.master_data_governance import release_evidence
from pyAppGen.pbcs.master_data_governance import routes
from pyAppGen.pbcs.master_data_governance import ui
from pyAppGen.pbcs.master_data_governance.standalone import GOLDEN_TABLE
from pyAppGen.pbcs.master_data_governance.standalone import MasterDataGovernanceStandaloneService
from pyAppGen.pbcs.master_data_governance.standalone import build_standalone_app



def test_standalone_service_runs_core_master_data_governance_flow():
    service = MasterDataGovernanceStandaloneService()
    try:
        domain = service.register_domain({
            "tenant": "tenant_test",
            "domain_code": "SUPPLIER_PARTY",
            "label": "Supplier Party",
            "steward": "steward.supplier",
            "matching_strategy": "exact_then_probabilistic",
            "survivorship_policy": "trusted_source_then_manual_review",
        })
        source_a = service.ingest_source_record({
            "tenant": "tenant_test",
            "domain_code": "SUPPLIER_PARTY",
            "source_system": "procurement",
            "source_record_id": "proc-001",
            "entity_key": "SUP-1",
            "attributes": {"name": "Northwind Supply", "tax_id": "KE123"},
        })
        source_b = service.ingest_source_record({
            "tenant": "tenant_test",
            "domain_code": "SUPPLIER_PARTY",
            "source_system": "erp",
            "source_record_id": "erp-001",
            "entity_key": "SUP-1",
            "attributes": {"name": "Northwind Supply Ltd", "tax_id": "KE123"},
        })
        match_candidate = service.create_match_candidate({
            "tenant": "tenant_test",
            "domain_code": "SUPPLIER_PARTY",
            "candidate_code": "MATCH-SUP-1",
            "left_record_code": "PROC-001",
            "right_record_code": "ERP-001",
            "confidence": 0.97,
            "explanation": "same tax id",
        })
        merge = service.approve_merge_decision({
            "tenant": "tenant_test",
            "decision_code": "MERGE-SUP-1",
            "candidate_code": "MATCH-SUP-1",
            "winning_record_code": "PROC-001",
            "losing_record_code": "ERP-001",
            "decision": "approved",
            "approved_by": "steward.supplier",
        })
        survivorship = service.define_survivorship_rule({
            "tenant": "tenant_test",
            "rule_code": "SURV-SUP-1",
            "domain_code": "SUPPLIER_PARTY",
            "attribute_name": "tax_id",
            "precedence": ("trusted_source", "manual_review"),
            "fallback": "manual_review",
            "explanation": "tax id is authoritative from procurement",
        })
        golden = service.publish_golden_record({
            "tenant": "tenant_test",
            "golden_code": "GOLD-SUP-1",
            "domain_code": "SUPPLIER_PARTY",
            "business_key": "SUP-1",
            "winning_record_code": "PROC-001",
            "published_by": "steward.supplier",
            "attributes": {"name": "Northwind Supply", "tax_id": "KE123"},
        })
        quality_rule = service.define_data_quality_rule({
            "tenant": "tenant_test",
            "rule_code": "DQ-SUP-1",
            "domain_code": "SUPPLIER_PARTY",
            "metric": "tax_id_completeness",
            "threshold": 1.0,
            "severity": "high",
            "owner": "quality.team",
        })
        remediation = service.queue_remediation_issue({
            "tenant": "tenant_test",
            "issue_code": "ISSUE-SUP-1",
            "domain_code": "SUPPLIER_PARTY",
            "queue": "supplier_quality",
            "severity": "medium",
            "record_code": "ERP-001",
            "remediation_owner": "quality.team",
        })
        hierarchy = service.upsert_hierarchy_node({
            "tenant": "tenant_test",
            "node_code": "NODE-SUP-ROOT",
            "domain_code": "SUPPLIER_PARTY",
            "parent_code": None,
            "label": "Suppliers",
            "node_type": "root",
        })
        reference = service.register_reference_data({
            "tenant": "tenant_test",
            "value_code": "REF-SUP-CLASS-A",
            "domain_code": "SUPPLIER_PARTY",
            "set_name": "supplier_class",
            "label": "Class A",
            "status": "active",
        })
        policy = service.approve_policy({
            "tenant": "tenant_test",
            "approval_code": "POLICY-SUP-1",
            "policy_name": "supplier_publish_gate",
            "status": "pending",
            "approved_by": "governance.board",
            "rationale": "pending final release review",
        })
        audit = service.record_audit_proof({
            "tenant": "tenant_test",
            "proof_code": "PROOF-SUP-1",
            "artifact_type": "golden_record_release",
            "artifact_code": "GOLD-SUP-1",
            "proof_hash": "sha256:supplier-proof",
            "attested_by": "audit.bot",
        })
        workbench = service.query_workbench({"tenant": "tenant_test"})
        rendered = ui.master_data_governance_render_workbench(workbench["result"])
        assert all(
            item["ok"] is True
            for item in (
                domain,
                source_a,
                source_b,
                match_candidate,
                merge,
                survivorship,
                golden,
                quality_rule,
                remediation,
                hierarchy,
                reference,
                policy,
                audit,
                workbench,
                rendered,
            )
        )
        assert workbench["result"]["summary"]["golden_records"] == 1
        assert workbench["result"]["summary"]["match_queue"] == 1
        assert workbench["result"]["summary"]["remediation_open"] == 1
        assert rendered["binding_evidence"]["event_contract"] == "AppGen-X"
    finally:
        service.close()



def test_routes_agent_and_release_surface_expose_standalone_app():
    service = MasterDataGovernanceStandaloneService()
    try:
        seed = routes.dispatch_route("POST", "/app/master-data-governance/seed-bundle", {"tenant": "tenant_route"}, service=service)
        workbench = routes.dispatch_route("GET", "/app/master-data-governance/workbench", {"tenant": "tenant_route"}, service=service)
        golden_plan = agent.document_instruction_plan(
            "golden record publication checklist",
            "publish the golden supplier record, capture lineage, and record audit proof",
        )
        crud_plan = agent.datastore_crud_plan("create", GOLDEN_TABLE, {"golden_code": "GOLD-ROUTE"})
        release = release_evidence.build_release_evidence()
        assert seed["ok"] is True
        assert workbench["ok"] is True
        assert golden_plan["ok"] is True
        assert any("golden-records" in route for route in golden_plan["route_candidates"])
        assert crud_plan["ok"] is True
        assert release["ok"] is True
        assert release["standalone_app"]["ok"] is True
        assert release["generation_smoke"]["ok"] is True
    finally:
        service.close()



def test_package_local_release_artifacts_exist():
    base = Path(__file__).resolve().parent.parent
    for name in ("SPECIFICATION.md", "RELEASE_EVIDENCE.md", "standalone.py"):
        assert (base / name).exists() is True



def test_standalone_app_wrapper_renders_after_seed_load():
    app = build_standalone_app()
    try:
        seeded = app.load_seed_bundle("tenant_app")
        rendered = app.render_workbench("tenant_app")
        assert seeded["ok"] is True
        assert rendered["ok"] is True
        assert rendered["summary_cards"]
    finally:
        app.close()
