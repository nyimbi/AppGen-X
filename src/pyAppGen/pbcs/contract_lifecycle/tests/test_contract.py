from pyAppGen.pbcs.contract_lifecycle import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.contract_lifecycle.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.contract_lifecycle.application import (
    ContractLifecycleService,
    empty_state,
    release_scenario,
)
from pyAppGen.pbcs.contract_lifecycle.config import (
    compile_rule,
    evaluate_rule,
    governance_smoke_test,
    parameter_manifest,
    rule_manifest,
)
from pyAppGen.pbcs.contract_lifecycle.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.contract_lifecycle.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.contract_lifecycle.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.contract_lifecycle.routes import api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.contract_lifecycle.schema_contract import build_schema_contract
from pyAppGen.pbcs.contract_lifecycle.service_contract import build_service_contract
from pyAppGen.pbcs.contract_lifecycle.services import service_operation_contracts
from pyAppGen.pbcs.contract_lifecycle.ui import contract_lifecycle_render_workbench, contract_lifecycle_ui_contract


def _intake_payload():
    return {
        "tenant": "tenant-test",
        "code": "CLM-TST-1",
        "request_purpose": "enterprise services agreement",
        "contract_type": "MSA",
        "jurisdiction": "UK",
        "counterparty_name": "Acme Telecom",
        "value_amount": 525000,
        "currency": "USD",
        "term_months": 24,
        "owner": "legal.ops",
        "source_documents": ("msa.docx", "schedule-a.docx"),
        "parties": (
            {"role": "supplier", "legal_name": "Acme Telecom Ltd", "authority_state": "verified"},
            {"role": "buyer", "legal_name": "Northwind Plc", "authority_state": "verified"},
        ),
    }


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    service = build_service_contract()
    release = build_release_evidence()
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()

    assert schema["ok"] is True
    assert len(schema["owned_tables"]) >= 20
    assert service["ok"] is True
    assert "intake_contract" in service["command_methods"]
    assert release["ok"] is True
    assert readiness["ok"] is True
    assert validation["ok"] is True


def test_manifest_and_event_contract():
    implementation = implementation_contract()
    event_manifest = event_contract_manifest()
    event_validation = validate_event_contract()

    assert implementation["pbc"] == "contract_lifecycle"
    assert implementation["advanced_runtime"]["ok"] is True
    assert event_manifest["ok"] is True
    assert "IdentityVerified" in event_manifest["consumed"]
    assert event_validation["ok"] is True


def test_end_to_end_contract_lifecycle_flow_is_executable():
    service = ContractLifecycleService()
    intake = service.intake_contract(_intake_payload())
    contract_id = intake["contract"]["contract_id"]

    classify = service.classify_contract(
        {
            "contract_id": contract_id,
            "taxonomy_version": "2026.1",
            "category": "technology_services",
            "data_sensitivity": "high",
            "controlling_language": "en",
        }
    )
    service.create_authoring_workspace(
        {"contract_id": contract_id, "template_code": "msa-global-v3", "workspace_owner": "legal.ops"}
    )
    service.select_clause(
        {
            "contract_id": contract_id,
            "clause_family": "data_processing",
            "variant_code": "dp-standard",
            "fallback_tier": "tier_1",
        }
    )
    service.negotiate_redline(
        {
            "contract_id": contract_id,
            "changed_clause": "liability_cap",
            "materiality_score": 0.7,
            "sender": "counterparty_counsel",
            "receiver": "internal_legal",
        }
    )
    service.receive_event(
        {
            "event_type": "SupplierQualified",
            "event_id": "evt-supplier",
            "supplier_name": "Acme Telecom",
            "qualified": True,
        }
    )
    risk = service.score_contract_risk({"contract_id": contract_id})
    approvals = service.route_approval(
        {"contract_id": contract_id, "auto_approve": True, "requires_security_review": True}
    )
    service.receive_event(
        {
            "event_type": "IdentityVerified",
            "event_id": "evt-id",
            "contract_id": contract_id,
            "signer_name": "Aisha Grant",
            "verified": True,
        }
    )
    signature = service.capture_signature(
        {
            "contract_id": contract_id,
            "signer_name": "Aisha Grant",
            "signer_title": "Chief Commercial Officer",
            "authority_evidence": "board-resolution-42",
            "identity_verified": True,
        }
    )
    obligation = service.activate_obligation(
        {
            "contract_id": contract_id,
            "obligation_code": "INSURANCE_CERT",
            "owner": "vendor.management",
            "due_date": "2026-08-01",
            "evidence_required": True,
        }
    )
    performance = service.record_obligation_performance(
        {
            "contract_id": contract_id,
            "obligation_id": obligation["rows"][0]["id"],
            "performed_by": "vendor.management",
            "evidence_uri": "s3://evidence/insurance-cert.pdf",
            "reviewed": True,
        }
    )
    renewal = service.schedule_renewal(
        {"contract_id": contract_id, "renewal_decision": "renegotiate", "notice_days": 60}
    )
    amendment = service.execute_amendment(
        {
            "contract_id": contract_id,
            "effective_date": "2026-09-01",
            "change_summary": "Adjust pricing annex",
        }
    )
    compliance = service.run_compliance_check({"contract_id": contract_id})
    workbench = service.build_workbench_view()

    assert intake["ok"] is True
    assert classify["ok"] is True
    assert risk["contract"]["risk_score"] >= 0.0
    assert approvals["contract"]["status"] == "approved"
    assert signature["contract"]["status"] == "active"
    assert performance["ok"] is True
    assert renewal["emitted_event"] == "RenewalScheduled"
    assert amendment["contract"]["status"] == "amended"
    assert compliance["check_result"] == "pass"
    assert workbench["metrics"]["contracts_total"] == 1


def test_signature_and_mutation_guards_are_enforced():
    service = ContractLifecycleService()
    intake = service.intake_contract(_intake_payload())
    contract_id = intake["contract"]["contract_id"]

    unsigned = service.capture_signature(
        {
            "contract_id": contract_id,
            "signer_name": "Aisha Grant",
            "authority_evidence": "board-resolution-42",
            "identity_verified": True,
        }
    )
    foreign_plan = datastore_crud_plan("update", table="foreign_table")
    instruction_plan = document_instruction_plan(
        "Please prepare a renewal reminder and update the obligation owner.",
        "update renewal notice and obligation workflow",
    )

    assert unsigned["ok"] is False
    assert unsigned["reason"] == "approval_required_before_signature"
    assert foreign_plan["ok"] is False
    assert instruction_plan["ok"] is True
    assert instruction_plan["requires_human_confirmation"] is True
    assert all(table.startswith("contract_lifecycle_") for table in instruction_plan["candidate_tables"])


def test_routes_ui_configuration_and_release_surface_are_coherent():
    routes = api_route_contracts()
    route_validation = validate_api_route_contracts()
    ui_contract = contract_lifecycle_ui_contract()
    workbench = contract_lifecycle_render_workbench(empty_state())
    scenario = release_scenario()
    route_dispatch = dispatch_route("/contract-lifecycle-workbench", {"limit": 3}, method="GET")

    assert routes["ok"] is True
    assert route_validation["ok"] is True
    assert ui_contract["ok"] is True
    assert len(ui_contract["forms"]) >= 5
    assert len(ui_contract["wizards"]) >= 3
    assert len(ui_contract["controls"]) >= 4
    assert workbench["ok"] is True
    assert scenario["ok"] is True
    assert route_dispatch["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    compiled = compile_rule(rule_manifest()["rules"][0])
    evaluated = evaluate_rule(compiled, {"risk_score": 0.2, "value_amount": 1000})
    governance = governance_smoke_test()
    handler = handler_manifest()
    handled = dispatch_event({"event_type": "CustomerUpdated", "event_id": "evt-1", "customer_name": "Northwind"})
    duplicate = dispatch_event({"event_type": "CustomerUpdated", "event_id": "evt-1", "customer_name": "Northwind"}, handled["state"])
    rejected = dispatch_event({"event_type": "Unexpected", "event_id": "evt-2"}, duplicate["state"])

    assert compiled["ok"] is True
    assert evaluated["allowed"] is True
    assert governance["ok"] is True
    assert parameter_manifest()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    handler = handler_manifest()
    handled = dispatch_event({"event_type": "CustomerUpdated", "event_id": "evt-handler-1", "customer_name": "Northwind"})
    duplicate = dispatch_event({"event_type": "CustomerUpdated", "event_id": "evt-handler-1", "customer_name": "Northwind"}, handled["state"])
    rejected = dispatch_event({"event_type": "Unexpected", "event_id": "evt-handler-2"}, duplicate["state"])
    assert handler["ok"] is True
    assert handled["ok"] is True
    assert duplicate["duplicate"] is True
    assert rejected["ok"] is False
    assert rejected["dead_letter_table"].endswith("dead_letter_event")


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "contract_lifecycle"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert service_operation_contracts()["operation_contract"]


def test_agent_surfaces_are_side_effect_free():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert composed_agent_contribution()["ok"] is True
