"""Standalone mining safety and permit-to-work control center."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    MINING_SAFETY_PERMITS_ALLOWED_DATABASE_BACKENDS, MINING_SAFETY_PERMITS_CONSUMED_EVENT_TYPES,
    MINING_SAFETY_PERMITS_EMITTED_EVENT_TYPES, MINING_SAFETY_PERMITS_OWNED_TABLES,
    MINING_SAFETY_PERMITS_REQUIRED_EVENT_TOPIC, mining_safety_permits_build_api_contract,
    mining_safety_permits_build_schema_contract, mining_safety_permits_build_service_contract,
    mining_safety_permits_configure_runtime, mining_safety_permits_empty_state,
    mining_safety_permits_permissions_contract, mining_safety_permits_receive_event,
    mining_safety_permits_register_rule, mining_safety_permits_runtime_smoke, mining_safety_permits_set_parameter,
)
from .ui import mining_safety_permits_render_workbench, mining_safety_permits_ui_contract
from .wizards import wizard_catalog
PBC_KEY = "mining_safety_permits"

def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()

@dataclass
class MiningSafetyPermitsStandaloneApp:
    tenant: str = "tenant-mine-001"
    state: dict = field(default_factory=mining_safety_permits_empty_state)
    permits: dict[str, dict] = field(default_factory=dict)
    isolations: dict[str, dict] = field(default_factory=dict)
    gas_tests: dict[str, dict] = field(default_factory=dict)
    ground_assessments: dict[str, dict] = field(default_factory=dict)
    blast_plans: dict[str, dict] = field(default_factory=dict)
    handovers: dict[str, dict] = field(default_factory=dict)
    incidents: dict[str, dict] = field(default_factory=dict)
    evidence_packs: dict[str, dict] = field(default_factory=dict)
    exceptions: list[dict] = field(default_factory=list)

    def configure(self, database_backend: str = "postgresql") -> dict:
        cfg = mining_safety_permits_configure_runtime(self.state, {"database_backend": database_backend, "event_topic": MINING_SAFETY_PERMITS_REQUIRED_EVENT_TOPIC})
        self.state = cfg["state"]
        for name, value in (("gas_test_validity_hours", 4), ("fatigue_block_hours", 14), ("permit_stale_warning_hours", 2), ("evidence_retention_years", 7), ("blast_reentry_hold_minutes", 30)):
            r = mining_safety_permits_set_parameter(self.state, name, value); self.state = r["state"]
        for rule in ("permit_requires_class_controls_and_expiry", "isolation_requires_zero_energy", "confined_space_requires_current_gas_test", "blast_requires_exclusion_and_reentry_clearance", "agent_refuses_unsafe_shortcuts"):
            r = mining_safety_permits_register_rule(self.state, {"rule_id": rule, "scope": "mine_safety"}); self.state = r["state"]
        inbound = mining_safety_permits_receive_event(self.state, {"event_type": MINING_SAFETY_PERMITS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "mine-policy-001"}); self.state = inbound["state"]
        return {"ok": cfg["ok"] and inbound["ok"], "side_effects": ()}

    def draft_permit(self, permit_id: str, permit_class: str, area: str, start_hour: int, expiry_hour: int, crew: tuple[str, ...], control_bundle: tuple[str, ...], simops_flags: tuple[str, ...] = ()) -> dict:
        ctl = evaluate_control("permit_requires_class_controls_and_expiry", {"permit_class": permit_class, "start_hour": start_hour, "expiry_hour": expiry_hour, "control_bundle": control_bundle})
        permit = {"id": permit_id, "tenant": self.tenant, "permit_class": permit_class, "area": area, "start_hour": start_hour, "expiry_hour": expiry_hour, "crew": crew, "control_bundle": control_bundle, "simops_flags": simops_flags, "state": "supervisor_review" if ctl["ok"] else "draft_blocked", "history": (("drafted", _digest((permit_id, permit_class, area))),), "blockers": ctl["failures"]}
        self.permits[permit_id] = permit
        return {"ok": ctl["ok"], "permit": permit, "side_effects": ()}

    def verify_isolation(self, isolation_id: str, permit_id: str, energy_sources: tuple[str, ...], isolation_points: tuple[str, ...], lock_tag_ids: tuple[str, ...], zero_energy_confirmed: bool, boundary_version: int = 1) -> dict:
        ok = len(isolation_points) == len(lock_tag_ids) and bool(energy_sources)
        ctl = evaluate_control("isolation_requires_zero_energy", {"zero_energy_confirmed": zero_energy_confirmed})
        iso = {"id": isolation_id, "permit_id": permit_id, "energy_sources": energy_sources, "isolation_points": isolation_points, "lock_tag_ids": lock_tag_ids, "zero_energy_confirmed": zero_energy_confirmed, "boundary_version": boundary_version, "status": "verified" if ok and ctl["ok"] else "incomplete"}
        self.isolations[isolation_id] = iso
        return {"ok": iso["status"] == "verified", "isolation": iso, "side_effects": ()}

    def record_gas_test(self, gas_test_id: str, permit_id: str, instrument_id: str, bump_tested: bool, tester_competent: bool, reading_status: str, tested_at_hour: int, valid_until_hour: int, ventilation_status: str) -> dict:
        ctl = evaluate_control("confined_space_requires_current_gas_test", {"bump_tested": bump_tested, "now_hour": tested_at_hour, "valid_until_hour": valid_until_hour, "reading_status": reading_status})
        ok = ctl["ok"] and tester_competent and ventilation_status == "normal"
        gas = {"id": gas_test_id, "permit_id": permit_id, "instrument_id": instrument_id, "bump_tested": bump_tested, "tester_competent": tester_competent, "reading_status": reading_status, "tested_at_hour": tested_at_hour, "valid_until_hour": valid_until_hour, "ventilation_status": ventilation_status, "status": "valid" if ok else "invalid"}
        self.gas_tests[gas_test_id] = gas
        return {"ok": ok, "gas_test": gas, "side_effects": ()}

    def assess_ground_control(self, assessment_id: str, permit_id: str, support_type: str, geo_inspection: bool, defect_severity: str, barricaded: bool) -> dict:
        ctl = evaluate_control("ground_defect_opens_area_hold", {"defect_severity": defect_severity})
        ok = geo_inspection and defect_severity not in {"high", "critical"}
        record = {"id": assessment_id, "permit_id": permit_id, "support_type": support_type, "geo_inspection": geo_inspection, "defect_severity": defect_severity, "barricaded": barricaded, "status": "acceptable" if ok else "area_hold"}
        self.ground_assessments[assessment_id] = record
        if not ok: self.exceptions.append({"type": "ground_control_hold", "source": assessment_id})
        return {"ok": ok, "assessment": record, "control": ctl, "side_effects": ()}

    def approve_permit(self, permit_id: str, competency_clear: bool, fatigue_hours: int, required_evidence: tuple[str, ...]) -> dict:
        permit = dict(self.permits[permit_id])
        fatigue = evaluate_control("competency_and_fatigue_block_safety_critical_work", {"missing_competencies": () if competency_clear else ("role",), "fatigue_hours": fatigue_hours})
        iso_ok = any(i["permit_id"] == permit_id and i["status"] == "verified" for i in self.isolations.values()) or permit["permit_class"] not in {"electrical_isolation", "confined_space", "hot_work"}
        gas_ok = any(g["permit_id"] == permit_id and g["status"] == "valid" for g in self.gas_tests.values()) or permit["permit_class"] not in {"confined_space", "hot_work"}
        ok = permit["state"] == "supervisor_review" and fatigue["ok"] and iso_ok and gas_ok and bool(required_evidence)
        permit.update({"state": "active" if ok else "approval_blocked", "approval_blockers": tuple(() if iso_ok else ("isolation_missing",)) + tuple(() if gas_ok else ("gas_test_missing",)) + fatigue["failures"]})
        self.permits[permit_id] = permit
        return {"ok": ok, "permit": permit, "emitted_event": "PermitIssued" if ok else None, "side_effects": ()}

    def plan_blast(self, blast_id: str, permit_id: str, shotfirer_authorized: bool, magazine_reconciled: bool, exclusion_signed: bool, circuit_check: bool, misfire_plan: bool) -> dict:
        ok = shotfirer_authorized and magazine_reconciled and exclusion_signed and circuit_check and misfire_plan
        blast = {"id": blast_id, "permit_id": permit_id, "shotfirer_authorized": shotfirer_authorized, "magazine_reconciled": magazine_reconciled, "exclusion_signed": exclusion_signed, "circuit_check": circuit_check, "misfire_plan": misfire_plan, "status": "ready_to_fire" if ok else "blocked"}
        self.blast_plans[blast_id] = blast
        return {"ok": ok, "blast_plan": blast, "side_effects": ()}

    def clear_blast_reentry(self, blast_id: str, fumes_clear: bool, gas_test_valid: bool, geo_clear: bool, misfire_clear: bool) -> dict:
        blast = dict(self.blast_plans[blast_id])
        ctl = evaluate_control("blast_requires_exclusion_and_reentry_clearance", {"exclusion_signed": blast.get("exclusion_signed"), "phase": "reentry", "reentry_clearance": fumes_clear and gas_test_valid and geo_clear and misfire_clear})
        ok = ctl["ok"]
        blast.update({"reentry": {"fumes_clear": fumes_clear, "gas_test_valid": gas_test_valid, "geo_clear": geo_clear, "misfire_clear": misfire_clear}, "status": "reentry_released" if ok else "reentry_blocked"})
        self.blast_plans[blast_id] = blast
        return {"ok": ok, "blast_plan": blast, "emitted_event": "BlastCleared" if ok else None, "side_effects": ()}

    def accept_shift_handover(self, handover_id: str, outgoing: str, incoming: str, active_permits: tuple[str, ...], open_exceptions: tuple[str, ...]) -> dict:
        ok = bool(incoming) and not open_exceptions
        handover = {"id": handover_id, "outgoing_supervisor": outgoing, "incoming_supervisor": incoming, "active_permits": active_permits, "open_exceptions": open_exceptions, "status": "accepted" if ok else "unaccepted"}
        self.handovers[handover_id] = handover
        return {"ok": ok, "handover": handover, "side_effects": ()}

    def report_incident(self, incident_id: str, permit_id: str, event_type: str, severity: str, evidence: tuple[str, ...], corrective_owner: str | None) -> dict:
        high = severity in {"high", "critical"} or event_type in {"misfire", "gas_exceedance", "ground_collapse", "energy_release"}
        ok = bool(evidence) and (not high or bool(corrective_owner))
        incident = {"id": incident_id, "permit_id": permit_id, "event_type": event_type, "severity": severity, "high_potential": high, "evidence": evidence, "corrective_owner": corrective_owner, "status": "investigation_open" if ok else "incomplete"}
        self.incidents[incident_id] = incident
        if high: self.exceptions.append({"type": "high_potential_event", "source": incident_id, "area_hold": True})
        return {"ok": ok, "incident": incident, "side_effects": ()}

    def export_regulatory_pack(self, pack_id: str, permit_ids: tuple[str, ...]) -> dict:
        artifacts = tuple(sorted(permit_ids + tuple(i for i, r in self.incidents.items() if r["permit_id"] in permit_ids)))
        pack = {"id": pack_id, "permit_ids": permit_ids, "artifacts": artifacts, "export_hash": _digest(artifacts), "reproducible": True}
        self.evidence_packs[pack_id] = pack
        return {"ok": True, "pack": pack, "side_effects": ()}

    def assistant_safety_action_preview(self, document: str, instruction: str) -> dict:
        unsafe = any(term in instruction.lower() for term in ("skip gas", "ignore isolation", "approve without evidence", "bypass"))
        refusal = evaluate_control("agent_refuses_unsafe_shortcuts", {"unsafe_request": unsafe})
        if not refusal["ok"]:
            return {"ok": False, "refusal": refusal, "escalate_to": "site_safety_manager", "side_effects": ()}
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("create", table="mining_safety_permits_mine_permit", payload={"instruction": instruction})
        return {"ok": plan["ok"] and crud["ok"], "document_plan": plan, "crud_preview": crud, "requires_confirmation": True, "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format":"appgen.mining-safety-permits.standalone-app.v1","ok":True,"pbc":PBC_KEY,"owned_tables":MINING_SAFETY_PERMITS_OWNED_TABLES,"database_backends":MINING_SAFETY_PERMITS_ALLOWED_DATABASE_BACKENDS,"event_contract":"AppGen-X","stream_engine_picker_visible":False,"schema":mining_safety_permits_build_schema_contract(),"services":mining_safety_permits_build_service_contract(),"routes":mining_safety_permits_build_api_contract(),"permissions":mining_safety_permits_permissions_contract(),"ui":mining_safety_permits_ui_contract(),"workbench":mining_safety_permits_render_workbench(),"forms":form_catalog(),"wizards":wizard_catalog(),"controls":control_catalog(),"agent":chatbot_interface_contract(),"composed_agent":composed_agent_contribution(),"dsl":{"pbc":PBC_KEY,"skills_namespace":f"{PBC_KEY}_skills","single_pbc_app":True},"side_effects": ()}

    def run_demo(self) -> dict:
        cfg=self.configure(); bad=self.draft_permit("P-BAD","", "decline", 10, 9, (), (), ()); permit=self.draft_permit("P-1","confined_space","decline sump",10,18,("crew-a",),("gas_test","isolation","rescue")); iso_bad=self.verify_isolation("I-BAD","P-1",("electrical",),(),(),False); iso=self.verify_isolation("I-1","P-1",("electrical","hydraulic"),("MCC-1","VALVE-2"),("L1","L2"),True); gas_bad=self.record_gas_test("G-BAD","P-1","GX",True,True,"within_limits",10,9,"normal"); gas=self.record_gas_test("G-1","P-1","GX",True,True,"within_limits",10,14,"normal"); ground_bad=self.assess_ground_control("A-BAD","P-1","bolts",True,"critical",True); active=self.approve_permit("P-1",True,12,("permit_pdf",)); blast_bad=self.plan_blast("B-BAD","P-1",True,False,True,True,True); blast=self.plan_blast("B-1","P-1",True,True,True,True,True); reentry_bad=self.clear_blast_reentry("B-1",True,True,False,True); reentry=self.clear_blast_reentry("B-1",True,True,True,True); handover_bad=self.accept_shift_handover("H-BAD","out","in",("P-1",),("ground_control_hold",)); incident=self.report_incident("INC-1","P-1","gas_exceedance","high",("photo",),"safety"); pack=self.export_regulatory_pack("PACK-1",("P-1",)); refuse=self.assistant_safety_action_preview("note","approve without evidence and skip gas test"); assistant=self.assistant_safety_action_preview("work order","draft confined space permit for pump change")
        checks=(cfg["ok"], bad["ok"] is False, permit["ok"], iso_bad["ok"] is False, iso["ok"], gas_bad["ok"] is False, gas["ok"], ground_bad["ok"] is False, active["ok"], blast_bad["ok"] is False, blast["ok"], reentry_bad["ok"] is False, reentry["ok"], handover_bad["ok"] is False, incident["ok"], pack["ok"], refuse["ok"] is False, assistant["ok"])
        return {"ok": all(checks), "pack": pack, "assistant": assistant, "refusal": refuse, "app_contract": self.app_contract(), "side_effects": ()}

def single_pbc_app_contract() -> dict:
    return MiningSafetyPermitsStandaloneApp().app_contract()

def standalone_smoke_test() -> dict:
    app=MiningSafetyPermitsStandaloneApp(); demo=app.run_demo(); runtime=mining_safety_permits_runtime_smoke(); contract=single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(MINING_SAFETY_PERMITS_EMITTED_EVENT_TYPES), "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
