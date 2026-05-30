"""Executable domain behavior tests for the procurement_sourcing PBC."""

from __future__ import annotations

import pytest

from .. import runtime
from .. import ui
from ..services import StatefulProcurementSourcingService
from ..services import runtime_service_manifest
from ..services import service_operation_manifest


TENANT = "tenant_proc"
ITEM_ID = "sku-100"


def _configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
        "retry_limit": 2,
        "default_currency": "USD",
        "allowed_categories": ("direct_materials", "maintenance"),
        "workbench_limit": 100,
    }


def _prepared_service(*, po: bool = False) -> StatefulProcurementSourcingService:
    service = StatefulProcurementSourcingService()
    service.configure_runtime(_configuration())
    service.set_parameter({"name": "approval_limit", "value": 5000.0})
    service.set_parameter({"name": "minimum_bid_count", "value": 2})
    service.set_parameter({"name": "supplier_risk_threshold", "value": 0.4})
    service.set_parameter({"name": "price_variance_tolerance", "value": 0.1})
    service.register_rule(
        {
            "rule_id": "rule_direct_materials",
            "tenant": TENANT,
            "scope": "sourcing",
            "category": "direct_materials",
            "preferred_suppliers": ("supplier-a",),
            "restricted_suppliers": ("supplier-blocked",),
            "score_weights": {"price": 0.45, "lead_time": 0.2, "risk": 0.2, "quality": 0.15},
            "allow_split_award": True,
            "status": "active",
        }
    )
    service.register_schema_extension({"table": "procurement_sourcing_rfq", "fields": {"sustainability_payload": "jsonb"}})
    service.create_requisition(
        {
            "requisition_id": "req-001",
            "tenant": TENANT,
            "legal_entity": "entity-alpha",
            "category": "direct_materials",
            "item_id": ITEM_ID,
            "quantity": 100.0,
            "estimated_amount": 3200.0,
            "currency": "USD",
            "cost_center": "operations",
            "requested_by": "planner-1",
        }
    )
    service.approve_requisition({"requisition_id": "req-001", "approver": "manager-1"})
    service.create_rfq({"rfq_id": "rfq-001", "requisition_id": "req-001", "suppliers": ("supplier-a", "supplier-b")})
    service.capture_bid(
        {
            "rfq_id": "rfq-001",
            "bid": {
                "supplier_id": "supplier-a",
                "price": 3000.0,
                "lead_time_days": 8,
                "risk": 0.12,
                "quality": 0.94,
                "carbon": 120,
                "identity": {"did": "did:appgen:supplier-a", "issuer": "trusted_registry", "status": "active"},
            },
        }
    )
    service.capture_bid(
        {
            "rfq_id": "rfq-001",
            "bid": {
                "supplier_id": "supplier-b",
                "price": 2850.0,
                "lead_time_days": 12,
                "risk": 0.18,
                "quality": 0.9,
                "carbon": 80,
                "identity": {"did": "did:appgen:supplier-b", "issuer": "trusted_registry", "status": "active"},
            },
        }
    )
    service.select_supplier({"rfq_id": "rfq-001", "award_id": "award-001"})
    service.create_contract({"contract_id": "contract-001", "award_id": "award-001", "term_months": 12})
    if po:
        service.issue_purchase_order({"po_id": "po-001", "contract_id": "contract-001", "quantity": 100.0, "amount": 3000.0})
    return service


def test_procurement_source_to_order_lifecycle_is_runtime_backed() -> None:
    service = _prepared_service(po=True)

    workbench = service.build_workbench_view({"tenant": TENANT})
    assert workbench["requisition_count"] == 1
    assert workbench["rfq_count"] == 1
    assert workbench["contract_count"] == 1
    assert workbench["po_count"] == 1
    assert workbench["po_amount"] == 3000.0
    assert workbench["event_contract"] == "AppGen-X"

    assert service.state["requisitions"]["req-001"]["status"] == "approved"
    assert service.state["rfqs"]["rfq-001"]["graph_degree"] == 4
    assert len(service.state["bids"]["rfq-001"]) == 2
    assert service.state["awards"]["award-001"]["supplier_id"] == "supplier-a"
    assert service.state["contracts"]["contract-001"]["status"] == "active"
    assert service.state["purchase_orders"]["po-001"]["status"] == "issued"

    event_types = tuple(event["event_type"] for event in service.state["events"])
    assert event_types == (
        "PurchaseRequisitionCreated",
        "PurchaseRequisitionApproved",
        "RfqCreated",
        "SupplierSelected",
        "VendorContractCreated",
        "PurchaseOrderIssued",
    )
    assert all(event["idempotency_key"].startswith("procurement_sourcing:") for event in service.state["outbox"])


def test_procurement_scoring_policy_po_route_proof_and_ui_are_bound() -> None:
    service = _prepared_service(po=True)

    scores = service.score_suppliers({"rfq_id": "rfq-001"})
    policy = service.screen_policy({"po_id": "po-001", "restricted_suppliers": ("supplier-blocked",)})
    route = service.route_purchase_order(
        {
            "po_id": "po-001",
            "rails": (
                {"route": "supplier_api", "available": False, "latency": 1},
                {"route": "outbox", "available": True, "latency": 3},
            ),
        }
    )
    proof = service.generate_supplier_compliance_proof({"supplier_id": "supplier-a", "disclosure": ("supplier_id", "risk")})
    permissions = tuple(sorted(set(ui.procurement_sourcing_ui_contract()["action_permissions"].values())))
    rendered = ui.procurement_sourcing_render_workbench(service.state, tenant=TENANT, principal_permissions=permissions)

    assert scores["scores"][0]["supplier_id"] == "supplier-a"
    assert scores["scores"][0]["award_confidence"] >= 0.8
    assert policy["decision"] == "clear"
    assert route["route"] == "outbox" and route["failover_used"] is True
    assert proof["proof"].startswith("zk_supplier_")
    assert proof["public_claims"] == {"supplier_id": "supplier-a", "risk": 0.12}
    assert rendered["ok"] is True
    assert "ProcurementSourcingWorkbench" in rendered["fragments"]
    assert "source_to_contract_wizard" in {wizard["key"] for wizard in rendered["wizards"]}
    assert "supplier_bid_form" in {form["key"] for form in rendered["forms"]}
    assert rendered["event_outbox_count"] == 6
    assert rendered["binding_evidence"]["outbox_table"] == "procurement_sourcing_appgen_outbox_event"
    assert rendered["binding_evidence"]["shared_table_access"] is False


def test_procurement_advanced_sourcing_intelligence_and_governance_are_executable() -> None:
    service = _prepared_service(po=True)
    state = service.state
    scores = runtime.procurement_sourcing_score_suppliers(state, "rfq-001")["scores"]

    carbon = runtime.procurement_sourcing_schedule_carbon_aware_sourcing(scores)
    optimization = runtime.procurement_sourcing_optimize_award(scores, quantity=100.0)
    mechanism = runtime.procurement_sourcing_allocate_rfq_award(scores, quantity=100.0)
    anomaly = runtime.procurement_sourcing_detect_bid_anomaly(state, "rfq-001")
    stochastic = runtime.procurement_sourcing_model_stochastic_supply_exposure(price_path=(3100.0, 3000.0, 2850.0), volatility=0.07)
    forecast = runtime.procurement_sourcing_forecast_price_lead_time((3000.0, 2900.0, 2850.0), (10.0, 9.0, 8.0))
    simulation = runtime.procurement_sourcing_simulate_sourcing_strategy(state, "rfq-001", proposed_risk_weight=0.4)
    parsed = runtime.procurement_sourcing_parse_document("requisition req_77 category direct_materials amount 2500 supplier supplier_a")
    risk = runtime.procurement_sourcing_score_supplier_risk({"late_rate": 0.03, "quality_escape": 0.02, "financial_risk": 0.06})
    federation = runtime.procurement_sourcing_federate_procurement_view(state, "po-001", systems=("ap", "inventory", "manufacturing"))
    identity = runtime.procurement_sourcing_verify_supplier_identity(state["bids"]["rfq-001"][0]["identity"])
    resilience = runtime.procurement_sourcing_run_resilience_drill(state, "supplier_route_timeout")
    crypto = runtime.procurement_sourcing_rotate_crypto_epoch(state, "dilithium3_simulated")
    controls = runtime.procurement_sourcing_run_control_tests(state)
    model = runtime.procurement_sourcing_register_governed_model(
        "supplier_risk",
        {"features": ("price", "lead_time", "risk"), "auc": 0.9, "drift_score": 0.04},
    )

    assert carbon["supplier_id"] == "supplier-b"
    assert optimization["supplier_id"] == "supplier-a"
    assert mechanism["ok"] is True and mechanism["clearing_bid"] > 0
    assert anomaly["entropy"] >= 0
    assert stochastic["tail_risk"] > stochastic["expected_exposure"]
    assert forecast["price_trend"] < 0 and forecast["lead_time_trend"] < 0
    assert simulation["selected_supplier"] in {"supplier-a", "supplier-b"}
    assert parsed["ok"] is True and parsed["amount"] == 2500.0
    assert risk["decision"] == "monitor"
    assert federation["systems"] == ("ap", "inventory", "manufacturing")
    assert identity["ok"] is True
    assert resilience["mode"] == "degraded_supplier_route"
    assert crypto["epoch"] == 2
    assert controls["ok"] is True and controls["hash_chain_valid"] is True
    assert model["ok"] is True and model["governance"]["explainability_required"] is True


def test_procurement_event_handlers_retry_dead_letter_service_and_boundary_guards() -> None:
    service = _prepared_service()

    processed = service.receive_event(
        {
            "event_id": "shortage-evt-001",
            "event_type": "MaterialShortageDetected",
            "payload": {"tenant": TENANT, "shortage_id": "shortage-001", "item_id": ITEM_ID, "quantity": 100.0},
        }
    )
    duplicate = service.receive_event(
        {
            "event_id": "shortage-evt-001",
            "event_type": "MaterialShortageDetected",
            "payload": {"tenant": TENANT, "shortage_id": "shortage-001", "item_id": ITEM_ID, "quantity": 100.0},
        }
    )
    retrying = service.receive_event({"event_id": "bad-evt-001", "event_type": "UnknownProcurementEvent", "payload": {"tenant": TENANT}})
    dead_letter = service.receive_event({"event_id": "bad-evt-001", "event_type": "UnknownProcurementEvent", "payload": {"tenant": TENANT}})

    assert processed["handler"]["status"] == "processed"
    assert service.state["material_shortage_projections"]["shortage-001"]["quantity"] == 100.0
    assert duplicate["duplicate"] is True
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert service.state["dead_letters"][-1]["reason"] == "unsupported_or_failed_procurement_event"

    runtime_manifest = runtime_service_manifest()
    generated_manifest = service_operation_manifest()
    assert runtime_manifest["ok"] is True
    assert runtime_manifest["service_class"] == "StatefulProcurementSourcingService"
    assert runtime_manifest["event_contract"] == "AppGen-X"
    assert generated_manifest["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in generated_manifest["operation_contracts"])

    boundary = runtime.procurement_sourcing_verify_owned_table_boundary(
        ("procurement_sourcing_purchase_order", "MaterialShortageDetected", "GET /identity/policies", "foreign_procurement_table")
    )
    assert boundary["ok"] is False
    assert boundary["violations"] == ("foreign_procurement_table",)

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        service.configure_runtime({**_configuration(), "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="stream-engine picker"):
        service.configure_runtime({**_configuration(), "stream_engine_picker": "user_choice"})
