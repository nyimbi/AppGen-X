"""Owned model metadata and standalone store for the construction_contracts_commercials PBC."""

from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta
from typing import Any

from .core import (
    CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES,
    CONTROLS,
    FORMS,
    PBC_KEY,
    WIZARDS,
    construction_contracts_commercials_approve_variation_order,
    construction_contracts_commercials_build_final_account_packet,
    construction_contracts_commercials_build_payment_certificate,
    construction_contracts_commercials_build_schema_contract,
    construction_contracts_commercials_build_workbench_view,
    construction_contracts_commercials_certify_pay_application,
    construction_contracts_commercials_command_construction_contract,
    construction_contracts_commercials_create_lien_waiver,
    construction_contracts_commercials_empty_state,
    construction_contracts_commercials_generate_cash_flow_forecast,
    construction_contracts_commercials_generate_contractor_scorecard,
    construction_contracts_commercials_progress_contract_lifecycle,
    construction_contracts_commercials_record_pay_application,
    construction_contracts_commercials_record_subcontract_package,
    construction_contracts_commercials_register_commercial_claim,
    construction_contracts_commercials_release_retainage,
    construction_contracts_commercials_review_retainage,
)


def model_contracts():
    return construction_contracts_commercials_build_schema_contract()["models"]


class ConstructionContractsCommercialsStandaloneStore:
    """Minimal package-local store for the standalone construction-commercials slice."""

    def __init__(self, state: dict[str, Any] | None = None):
        self.state = deepcopy(state) if state is not None else construction_contracts_commercials_empty_state()

    def _apply(self, result: dict[str, Any]) -> dict[str, Any]:
        if "state" in result:
            self.state = result["state"]
        return result

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)

    def create_contract(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_command_construction_contract(self.state, dict(payload), actor=actor))

    def progress_contract_lifecycle(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_progress_contract_lifecycle(self.state, dict(payload), actor=actor))

    def record_pay_application(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_record_pay_application(self.state, dict(payload), actor=actor))

    def create_lien_waiver(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_create_lien_waiver(self.state, dict(payload), actor=actor))

    def certify_pay_application(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_certify_pay_application(self.state, dict(payload), actor=actor))

    def review_retainage(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_review_retainage(self.state, dict(payload), actor=actor))

    def release_retainage(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_release_retainage(self.state, dict(payload), actor=actor))

    def approve_variation_order(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_approve_variation_order(self.state, dict(payload), actor=actor))

    def register_commercial_claim(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_register_commercial_claim(self.state, dict(payload), actor=actor))

    def record_subcontract_package(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._apply(construction_contracts_commercials_record_subcontract_package(self.state, dict(payload), actor=actor))

    def build_workbench(self, tenant: str = "default", actor: dict[str, Any] | None = None) -> dict[str, Any]:
        workbench = construction_contracts_commercials_build_workbench_view(self.state, tenant=tenant, actor=actor)
        return {"ok": workbench["ok"], "tenant": tenant, "result": workbench, "side_effects": ()}

    def build_payment_certificate(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return construction_contracts_commercials_build_payment_certificate(self.state, dict(payload), actor=actor)

    def build_final_account_packet(self, payload: dict[str, Any], actor: dict[str, Any] | None = None) -> dict[str, Any]:
        return construction_contracts_commercials_build_final_account_packet(self.state, dict(payload), actor=actor)

    def generate_cash_flow_forecast(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return construction_contracts_commercials_generate_cash_flow_forecast(self.state, payload)

    def generate_contractor_scorecard(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return construction_contracts_commercials_generate_contractor_scorecard(self.state, payload)

    def close(self) -> None:
        return None


def standalone_model_contract() -> dict[str, Any]:
    schema = construction_contracts_commercials_build_schema_contract()
    return {
        "format": "appgen.construction-contracts-commercials-standalone-model-contract.v1",
        "ok": schema["ok"],
        "pbc": PBC_KEY,
        "store_class": "ConstructionContractsCommercialsStandaloneStore",
        "table_keys": CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES,
        "models": schema["models"],
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "schema": schema,
        "side_effects": (),
    }


def standalone_store_smoke_test() -> dict[str, Any]:
    store = ConstructionContractsCommercialsStandaloneStore()
    try:
        contract = store.create_contract(
            {
                "tenant": "tenant-standalone",
                "contract_code": "CCC-STANDALONE-001",
                "title": "Standalone Envelope Package",
                "contract_value": 120000.0,
                "pricing_basis": "lump_sum",
                "jurisdiction": "KE",
                "schedule_of_values": (
                    {"line_code": "SOV-01", "work_package": "Envelope", "original_value": 70000.0},
                    {"line_code": "SOV-02", "work_package": "Roofing", "original_value": 50000.0},
                ),
                "guarantees": (
                    {"type": "performance_bond", "expiry": (date.today() + timedelta(days=21)).isoformat()},
                ),
            }
        )
        package = store.record_subcontract_package(
            {
                "contract_code": "CCC-STANDALONE-001",
                "package_code": "PKG-STANDALONE-001",
                "subcontractor_name": "Summit Build Ltd",
                "contract_value": 25000.0,
                "insurance_status": "compliant",
                "bond_status": "compliant",
            }
        )
        pay_application = store.record_pay_application(
            {
                "contract_code": "CCC-STANDALONE-001",
                "application_number": "APP-STANDALONE-001",
                "period_start": date.today().replace(day=1).isoformat(),
                "period_end": date.today().isoformat(),
                "attachments": ("payapp.pdf", "inspection.zip"),
                "lines": (
                    {"line_code": "SOV-01", "current_claimed": 30000.0, "evidence_refs": ("inspection-001",)},
                ),
            }
        )
        waiver = store.create_lien_waiver(
            {
                "contract_code": "CCC-STANDALONE-001",
                "pay_application_id": pay_application["record"]["id"],
                "waiver_number": "LW-STANDALONE-001",
                "covered_amount": 30000.0,
                "signed_date": date.today().isoformat(),
            }
        )
        certified = store.certify_pay_application({"pay_application_id": pay_application["record"]["id"]})
        workbench = store.build_workbench("tenant-standalone")
        return {
            "ok": standalone_model_contract()["ok"]
            and contract["ok"]
            and package["ok"]
            and pay_application["ok"]
            and waiver["ok"]
            and certified["ok"]
            and workbench["ok"],
            "contract": contract,
            "package": package,
            "pay_application": pay_application,
            "waiver": waiver,
            "certified": certified,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        store.close()
