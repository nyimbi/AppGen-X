"""Standalone renewables asset operations application contract."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    RENEWABLES_ASSET_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    RENEWABLES_ASSET_OPERATIONS_CONSUMED_EVENT_TYPES,
    RENEWABLES_ASSET_OPERATIONS_EMITTED_EVENT_TYPES,
    RENEWABLES_ASSET_OPERATIONS_OWNED_TABLES,
    RENEWABLES_ASSET_OPERATIONS_REQUIRED_EVENT_TOPIC,
    renewables_asset_operations_build_api_contract,
    renewables_asset_operations_build_schema_contract,
    renewables_asset_operations_build_service_contract,
    renewables_asset_operations_configure_runtime,
    renewables_asset_operations_empty_state,
    renewables_asset_operations_permissions_contract,
    renewables_asset_operations_receive_event,
    renewables_asset_operations_register_rule,
    renewables_asset_operations_runtime_smoke,
    renewables_asset_operations_set_parameter,
)
from .ui import renewables_asset_operations_render_workbench, renewables_asset_operations_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "renewables_asset_operations"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class RenewablesAssetOperationsStandaloneApp:
    tenant: str = "tenant-renew-001"
    state: dict = field(default_factory=renewables_asset_operations_empty_state)
    assets: dict[str, dict] = field(default_factory=dict)
    readings: dict[str, dict] = field(default_factory=dict)
    curtailments: dict[str, dict] = field(default_factory=dict)
    availability: dict[str, dict] = field(default_factory=dict)
    ppas: dict[str, dict] = field(default_factory=dict)
    work: dict[str, dict] = field(default_factory=dict)
    performance: dict[str, dict] = field(default_factory=dict)
    inspections: dict[str, dict] = field(default_factory=dict)
    safety: dict[str, dict] = field(default_factory=dict)
    warranty: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend="postgresql"):
        cfg = renewables_asset_operations_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": RENEWABLES_ASSET_OPERATIONS_REQUIRED_EVENT_TOPIC})
        self.state = cfg["state"]
        for name, value in (("meter_tolerance_mwh", 0.5), ("availability_lock_required", True), ("permit_required", True), ("dispatch_shortfall_threshold", 0.0), ("agent_confirmation_required", True)):
            result = renewables_asset_operations_set_parameter(self.state, name, value); self.state = result["state"]
        for rule_id in ("asset_hierarchy_complete", "meter_reconciliation_within_tolerance", "curtailment_has_instruction_evidence", "availability_exclusion_approved", "maintenance_has_safety_permit", "remote_reset_not_allowed_during_lockout", "storage_dispatch_compliant", "agent_mutations_require_confirmation"):
            result = renewables_asset_operations_register_rule(self.state, {"rule_id": rule_id, "scope": "renewables"}); self.state = result["state"]
        inbound = renewables_asset_operations_receive_event(self.state, {"event_type": RENEWABLES_ASSET_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "renew-policy-001"})
        self.state = inbound["state"]
        return {"ok": cfg["ok"] and inbound["ok"], "side_effects": ()}

    def register_asset(self, asset_id, site, technology, grid_node, parent_asset=None, nameplate_mw=0):
        ctl = evaluate_control("asset_hierarchy_complete", {"site": site, "technology": technology, "grid_node": grid_node})
        asset = {"id": asset_id, "tenant": self.tenant, "site": site, "technology": technology, "grid_node": grid_node, "parent_asset": parent_asset, "nameplate_mw": nameplate_mw, "status": "active" if ctl["ok"] else "incomplete", "blockers": ctl["failures"]}
        self.assets[asset_id] = asset
        return {"ok": ctl["ok"], "asset": asset, "side_effects": ()}

    def reconcile_reading(self, reading_id, asset_id, scada_mwh, meter_mwh, tolerance=0.5, source="scada"):
        variance = scada_mwh - meter_mwh
        ctl = evaluate_control("meter_reconciliation_within_tolerance", {"variance": variance, "tolerance": tolerance})
        row = {"id": reading_id, "tenant": self.tenant, "asset_id": asset_id, "source": source, "scada_mwh": scada_mwh, "meter_mwh": meter_mwh, "variance": variance, "status": "approved" if ctl["ok"] else "reconcile_exception", "blockers": ctl["failures"]}
        self.readings[reading_id] = row
        return {"ok": asset_id in self.assets and ctl["ok"], "reading": row, "side_effects": ()}

    def classify_curtailment(self, event_id, asset_id, initiator, mw_requested, mw_delivered, evidence=None, compensable=False):
        ctl = evaluate_control("curtailment_has_instruction_evidence", {"evidence": evidence})
        event = {"id": event_id, "tenant": self.tenant, "asset_id": asset_id, "initiator": initiator, "mw_requested": mw_requested, "mw_delivered": mw_delivered, "recoverable_mw": max(0, mw_requested - mw_delivered), "compensable": compensable, "status": "classified" if ctl["ok"] else "evidence_blocked", "blockers": ctl["failures"]}
        self.curtailments[event_id] = event
        return {"ok": asset_id in self.assets and ctl["ok"], "curtailment": event, "side_effects": ()}

    def lock_availability_pack(self, pack_id, asset_id, technical, contractual, exclusion=False, approved=False):
        ctl = evaluate_control("availability_exclusion_approved", {"exclusion": exclusion, "approved": approved})
        pack = {"id": pack_id, "tenant": self.tenant, "asset_id": asset_id, "technical": technical, "contractual": contractual, "grid_adjusted": min(technical, contractual), "exclusion": exclusion, "locked": ctl["ok"], "blockers": ctl["failures"]}
        self.availability[pack_id] = pack
        return {"ok": asset_id in self.assets and ctl["ok"], "availability": pack, "side_effects": ()}

    def track_ppa_obligation(self, obligation_id, asset_id, guarantee, late=False, waiver=False):
        ctl = evaluate_control("ppa_settlement_deadline_safe", {"late": late, "waiver": waiver})
        row = {"id": obligation_id, "tenant": self.tenant, "asset_id": asset_id, "guarantee": guarantee, "late": late, "status": "on_track" if ctl["ok"] else "late_exception", "blockers": ctl["failures"]}
        self.ppas[obligation_id] = row
        return {"ok": asset_id in self.assets and ctl["ok"], "obligation": row, "side_effects": ()}

    def release_work_order(self, work_id, asset_id, fault, mw_at_risk, permit=False, contractor_expired=False):
        permit_ctl = evaluate_control("maintenance_has_safety_permit", {"permit": permit})
        comp_ctl = evaluate_control("contractor_competency_valid", {"expired": contractor_expired})
        ok = asset_id in self.assets and permit_ctl["ok"] and comp_ctl["ok"]
        row = {"id": work_id, "tenant": self.tenant, "asset_id": asset_id, "fault": fault, "mw_at_risk": mw_at_risk, "criticality": "high" if mw_at_risk >= 5 else "normal", "status": "released" if ok else "blocked", "blockers": permit_ctl["failures"] + comp_ctl["failures"]}
        self.work[work_id] = row
        return {"ok": ok, "work_order": row, "side_effects": ()}

    def enforce_safety_hold(self, hold_id, asset_id, lockout, remote_reset):
        ctl = evaluate_control("remote_reset_not_allowed_during_lockout", {"lockout": lockout, "remote_reset": remote_reset})
        hold = {"id": hold_id, "tenant": self.tenant, "asset_id": asset_id, "lockout": lockout, "remote_reset": remote_reset, "status": "safe" if ctl["ok"] else "unsafe_reset_blocked", "blockers": ctl["failures"]}
        self.safety[hold_id] = hold
        return {"ok": asset_id in self.assets and ctl["ok"], "hold": hold, "side_effects": ()}

    def record_inspection(self, inspection_id, asset_id, template, photos, defects):
        ok = asset_id in self.assets and bool(template) and bool(photos)
        row = {"id": inspection_id, "tenant": self.tenant, "asset_id": asset_id, "template": template, "photos": tuple(photos), "defects": tuple(defects), "follow_on_required": bool(defects), "status": "complete" if ok else "incomplete"}
        self.inspections[inspection_id] = row
        return {"ok": ok, "inspection": row, "side_effects": ()}

    def prepare_warranty_claim(self, claim_id, asset_id, recurrence, threshold, evidence):
        ctl = evaluate_control("warranty_claim_threshold_met", {"recurrence": recurrence, "threshold": threshold})
        ok = asset_id in self.assets and ctl["ok"] and bool(evidence)
        claim = {"id": claim_id, "tenant": self.tenant, "asset_id": asset_id, "recurrence": recurrence, "threshold": threshold, "evidence": evidence, "status": "claim_ready" if ok else "watch", "blockers": ctl["failures"]}
        self.warranty[claim_id] = claim
        return {"ok": ok, "claim": claim, "side_effects": ()}

    def close_performance_rca(self, rca_id, asset_id, expected_mwh, actual_mwh, loss_bucket, recovery_evidence=None):
        ctl = evaluate_control("performance_rca_has_recovery_evidence", {"recovery_evidence": recovery_evidence})
        rca = {"id": rca_id, "tenant": self.tenant, "asset_id": asset_id, "expected_mwh": expected_mwh, "actual_mwh": actual_mwh, "loss_mwh": max(0, expected_mwh - actual_mwh), "loss_bucket": loss_bucket, "status": "closed" if ctl["ok"] else "recovery_unproven", "blockers": ctl["failures"]}
        self.performance[rca_id] = rca
        return {"ok": asset_id in self.assets and ctl["ok"], "rca": rca, "side_effects": ()}

    def review_storage_dispatch(self, review_id, asset_id, delivered, committed, charge_mwh, discharge_mwh):
        ctl = evaluate_control("storage_dispatch_compliant", {"delivered": delivered, "committed": committed})
        rte = round(discharge_mwh / charge_mwh, 3) if charge_mwh else 0
        row = {"id": review_id, "tenant": self.tenant, "asset_id": asset_id, "delivered": delivered, "committed": committed, "round_trip_efficiency": rte, "status": "compliant" if ctl["ok"] else "shortfall", "blockers": ctl["failures"]}
        self.performance[review_id] = row
        return {"ok": asset_id in self.assets and ctl["ok"], "dispatch": row, "side_effects": ()}

    def record_environmental_evidence(self, evidence_id, asset_id, regulated, permit=None):
        ctl = evaluate_control("environmental_permit_attached", {"regulated": regulated, "permit": permit})
        row = {"id": evidence_id, "tenant": self.tenant, "asset_id": asset_id, "regulated": regulated, "permit": permit, "status": "accepted" if ctl["ok"] else "permit_blocked", "blockers": ctl["failures"]}
        self.performance[evidence_id] = row
        return {"ok": asset_id in self.assets and ctl["ok"], "environmental": row, "side_effects": ()}

    def simulate_curtailment_recovery(self, name, curtailed_mwh, recovery_factor):
        return {"ok": True, "mutates_live_records": False, "name": name, "recoverable_mwh": round(curtailed_mwh * recovery_factor, 3), "assumption_hash": _digest((name, curtailed_mwh, recovery_factor)), "side_effects": ()}

    def assistant_operator_action_preview(self, document, instruction, confirmed=False):
        ctl = evaluate_control("agent_mutations_require_confirmation", {"confirmed": confirmed})
        doc = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("update", table="renewables_asset_operations_renewable_asset", payload={"instruction": instruction})
        return {"ok": doc["ok"] and crud["ok"] and ctl["ok"], "document_plan": doc, "crud_preview": crud, "control": ctl, "requires_confirmation": not confirmed, "side_effects": ()}

    def app_contract(self):
        return {"format": "appgen.renewables-asset-operations.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": RENEWABLES_ASSET_OPERATIONS_OWNED_TABLES, "database_backends": RENEWABLES_ASSET_OPERATIONS_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": renewables_asset_operations_build_schema_contract(), "services": renewables_asset_operations_build_service_contract(), "routes": renewables_asset_operations_build_api_contract(), "permissions": renewables_asset_operations_permissions_contract(), "ui": renewables_asset_operations_ui_contract(), "workbench": renewables_asset_operations_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self):
        cfg = self.configure()
        bad_asset = self.register_asset("A0", "Site", None, None)
        asset = self.register_asset("A1", "Site", "solar", "POI-1", nameplate_mw=50)
        bad_read = self.reconcile_reading("G0", "A1", 10, 8, tolerance=0.5)
        read = self.reconcile_reading("G1", "A1", 10, 9.8, tolerance=0.5)
        bad_curt = self.classify_curtailment("C0", "A1", "grid", 20, 10, evidence=None)
        curt = self.classify_curtailment("C1", "A1", "grid", 20, 10, evidence="dispatch")
        bad_avail = self.lock_availability_pack("AV0", "A1", .98, .95, exclusion=True, approved=False)
        avail = self.lock_availability_pack("AV1", "A1", .98, .95, exclusion=True, approved=True)
        bad_ppa = self.track_ppa_obligation("P0", "A1", .95, late=True)
        ppa = self.track_ppa_obligation("P1", "A1", .95, late=True, waiver=True)
        bad_work = self.release_work_order("W0", "A1", "inverter", 8, permit=False)
        work = self.release_work_order("W1", "A1", "inverter", 8, permit=True)
        bad_hold = self.enforce_safety_hold("H0", "A1", lockout=True, remote_reset=True)
        hold = self.enforce_safety_hold("H1", "A1", lockout=True, remote_reset=False)
        insp = self.record_inspection("I1", "A1", "solar walk", ("photo",), ("hotspot",))
        bad_claim = self.prepare_warranty_claim("WC0", "A1", recurrence=1, threshold=2, evidence="faults")
        claim = self.prepare_warranty_claim("WC1", "A1", recurrence=3, threshold=2, evidence="faults")
        bad_rca = self.close_performance_rca("R0", "A1", 100, 80, "soiling")
        rca = self.close_performance_rca("R1", "A1", 100, 80, "soiling", "post clean recovery")
        bad_storage = self.review_storage_dispatch("S0", "A1", delivered=8, committed=10, charge_mwh=12, discharge_mwh=10)
        storage = self.review_storage_dispatch("S1", "A1", delivered=10, committed=10, charge_mwh=12, discharge_mwh=10)
        bad_env = self.record_environmental_evidence("E0", "A1", regulated=True)
        env = self.record_environmental_evidence("E1", "A1", regulated=True, permit="water")
        scenario = self.simulate_curtailment_recovery("grid cap", 100, .85)
        agent_bad = self.assistant_operator_action_preview("ppa", "create obligation", False)
        agent = self.assistant_operator_action_preview("ppa", "create obligation", True)
        checks = (cfg["ok"], bad_asset["ok"] is False, asset["ok"], bad_read["ok"] is False, read["ok"], bad_curt["ok"] is False, curt["ok"], bad_avail["ok"] is False, avail["ok"], bad_ppa["ok"] is False, ppa["ok"], bad_work["ok"] is False, work["ok"], bad_hold["ok"] is False, hold["ok"], insp["ok"], bad_claim["ok"] is False, claim["ok"], bad_rca["ok"] is False, rca["ok"], bad_storage["ok"] is False, storage["ok"], bad_env["ok"] is False, env["ok"], scenario["mutates_live_records"] is False, agent_bad["ok"] is False, agent["ok"])
        return {"ok": all(checks), "app_contract": self.app_contract(), "side_effects": ()}


def single_pbc_app_contract():
    return RenewablesAssetOperationsStandaloneApp().app_contract()


def standalone_smoke_test():
    app = RenewablesAssetOperationsStandaloneApp(); demo = app.run_demo(); runtime = renewables_asset_operations_runtime_smoke(); contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(RENEWABLES_ASSET_OPERATIONS_EMITTED_EVENT_TYPES), "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
