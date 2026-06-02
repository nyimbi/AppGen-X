"""Focused standalone one-PBC tests for construction_contracts_commercials."""

from pathlib import Path

from .. import agent, models, release_evidence, routes, services, standalone, ui


def _contract_payload():
    return {
        "tenant": "tenant_test",
        "contract_code": "CCC-ST-TEST-001",
        "title": "Standalone Test Contract",
        "contract_value": 125000.0,
        "pricing_basis": "lump_sum",
        "jurisdiction": "KE",
        "schedule_of_values": (
            {"line_code": "SOV-01", "work_package": "Envelope", "original_value": 70000.0},
            {"line_code": "SOV-02", "work_package": "Services", "original_value": 55000.0},
        ),
    }


def test_standalone_store_executes_core_commercial_flow():
    store = models.ConstructionContractsCommercialsStandaloneStore()
    try:
        contract = store.create_contract(_contract_payload())
        pay_application = store.record_pay_application(
            {
                "contract_code": "CCC-ST-TEST-001",
                "application_number": "APP-ST-001",
                "period_start": "2026-05-01",
                "period_end": "2026-05-30",
                "attachments": ("payapp.pdf", "photos.zip"),
                "lines": (
                    {"line_code": "SOV-01", "current_claimed": 25000.0, "evidence_refs": ("inspection-001",)},
                ),
            }
        )
        waiver = store.create_lien_waiver(
            {
                "contract_code": "CCC-ST-TEST-001",
                "pay_application_id": pay_application["record"]["id"],
                "waiver_number": "LW-ST-001",
                "covered_amount": 25000.0,
                "signed_date": "2026-05-30",
            }
        )
        certified = store.certify_pay_application({"pay_application_id": pay_application["record"]["id"]})
        claim = store.register_commercial_claim(
            {
                "contract_code": "CCC-ST-TEST-001",
                "claim_number": "CL-ST-001",
                "claim_type": "delay",
                "event_date": "2026-05-01",
                "notice_date": "2026-05-20",
                "claimed_amount": 15000.0,
            }
        )
        workbench = store.build_workbench("tenant_test")
        certificate = store.build_payment_certificate({"pay_application_id": pay_application["record"]["id"]})
        assert all(item["ok"] is True for item in (contract, pay_application, waiver, certified, claim, workbench, certificate))
        assert certified["record"]["certified_amount"] == 22500.0
        assert claim["record"]["time_bar_status"] == "late"
        assert workbench["result"]["metrics"]["contract_count"] == 1
        assert certificate["certificate"]["net_due"] == 22500.0
    finally:
        store.close()


def test_standalone_service_routes_ui_agent_and_release_surface():
    service = services.ConstructionContractsCommercialsStandaloneService()
    try:
        create = routes.dispatch_standalone_route(
            "POST",
            "/app/construction-contracts-commercials/contracts",
            _contract_payload(),
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            "GET",
            "/app/construction-contracts-commercials/workbench",
            {"tenant": "tenant_test"},
            service=service,
        )
        rendered = ui.construction_contracts_commercials_render_standalone_workbench(workbench["result"]["result"])
        document_plan = agent.document_instruction_plan(
            "pay application certificate",
            "create pay application and waiver review plan",
        )
        crud_plan = agent.datastore_crud_plan(
            "create",
            "construction_contracts_commercials_pay_application",
            {"contract_code": "CCC-ST-TEST-001"},
        )
        app_contract = standalone.construction_contracts_commercials_standalone_app_contract()
        smoke = standalone.construction_contracts_commercials_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert create["ok"] is True
        assert workbench["ok"] is True
        assert rendered["ok"] is True
        assert document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert app_contract["ok"] is True
        assert smoke["ok"] is True
        assert evidence["documentation"]["ok"] is True
        assert evidence["standalone_app"]["ok"] is True
    finally:
        service.close()


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md", "standalone.py"):
        assert (base / name).exists() is True
