"""Standalone publishing editorial operations application contract."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    PUBLISHING_EDITORIAL_OPERATIONS_CONSUMED_EVENT_TYPES,
    PUBLISHING_EDITORIAL_OPERATIONS_EMITTED_EVENT_TYPES,
    PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES,
    PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
    publishing_editorial_operations_build_api_contract,
    publishing_editorial_operations_build_schema_contract,
    publishing_editorial_operations_build_service_contract,
    publishing_editorial_operations_configure_runtime,
    publishing_editorial_operations_empty_state,
    publishing_editorial_operations_permissions_contract,
    publishing_editorial_operations_receive_event,
    publishing_editorial_operations_register_rule,
    publishing_editorial_operations_runtime_smoke,
    publishing_editorial_operations_set_parameter,
)
from .ui import publishing_editorial_operations_render_workbench, publishing_editorial_operations_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "publishing_editorial_operations"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class PublishingEditorialOperationsStandaloneApp:
    tenant: str = "tenant-pub-001"
    state: dict = field(default_factory=publishing_editorial_operations_empty_state)
    proposals: dict[str, dict] = field(default_factory=dict)
    board_decisions: dict[str, dict] = field(default_factory=dict)
    manuscripts: dict[str, dict] = field(default_factory=dict)
    reviews: dict[str, dict] = field(default_factory=dict)
    copyedits: dict[str, dict] = field(default_factory=dict)
    rights: dict[str, dict] = field(default_factory=dict)
    editions: dict[str, dict] = field(default_factory=dict)
    schedules: dict[str, dict] = field(default_factory=dict)
    proofs: dict[str, dict] = field(default_factory=dict)
    distributions: dict[str, dict] = field(default_factory=dict)
    exceptions: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = publishing_editorial_operations_configure_runtime(
            self.state,
            {"database_backend": database_backend, "event_topic": PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC},
        )
        self.state = configured["state"]
        for name, value in (
            ("review_deadline_days", 21),
            ("copyedit_query_sla_days", 7),
            ("proof_round_limit", 3),
            ("release_binder_required", True),
            ("agent_confirmation_required", True),
        ):
            result = publishing_editorial_operations_set_parameter(self.state, name, value)
            self.state = result["state"]
        for rule_id in (
            "acquisition_packet_complete",
            "board_decision_has_quorum",
            "manuscript_package_complete",
            "reviewer_conflict_cleared",
            "rights_collision_absent",
            "production_handoff_complete",
            "release_binder_complete",
            "agent_mutations_require_confirmation",
        ):
            result = publishing_editorial_operations_register_rule(self.state, {"rule_id": rule_id, "scope": "editorial"})
            self.state = result["state"]
        inbound = publishing_editorial_operations_receive_event(
            self.state,
            {"event_type": PUBLISHING_EDITORIAL_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "pub-policy-001"},
        )
        self.state = inbound["state"]
        return {"ok": configured["ok"] and inbound["ok"], "side_effects": ()}

    def capture_acquisition(self, proposal_id: str, packet: str | None, sponsor: str | None, comp_titles: tuple[str, ...], season: str | None) -> dict:
        control = evaluate_control("acquisition_packet_complete", {"packet": packet, "sponsor": sponsor, "comp_titles": comp_titles, "season": season})
        proposal = {"id": proposal_id, "tenant": self.tenant, "packet": packet, "sponsor": sponsor, "comp_titles": tuple(comp_titles), "season": season, "status": "board_ready" if control["ok"] else "intake_blocked", "blockers": control["failures"]}
        self.proposals[proposal_id] = proposal
        return {"ok": control["ok"], "proposal": proposal, "side_effects": ()}

    def record_board_decision(self, decision_id: str, proposal_id: str, decision: str, quorum: bool, conditions: tuple[str, ...] = ()) -> dict:
        control = evaluate_control("board_decision_has_quorum", {"quorum": quorum, "decision": decision, "conditions": conditions})
        ok = proposal_id in self.proposals and decision in {"approved", "conditional", "declined"} and control["ok"]
        row = {"id": decision_id, "tenant": self.tenant, "proposal_id": proposal_id, "decision": decision if ok else "blocked", "conditions": tuple(conditions), "blockers": control["failures"]}
        self.board_decisions[decision_id] = row
        return {"ok": ok, "decision": row, "side_effects": ()}

    def create_manuscript(self, manuscript_id: str, proposal_id: str, missing: tuple[str, ...], waiver: str | None = None) -> dict:
        control = evaluate_control("manuscript_package_complete", {"missing": missing, "waiver": waiver})
        ok = proposal_id in self.proposals and control["ok"]
        manuscript = {"id": manuscript_id, "tenant": self.tenant, "proposal_id": proposal_id, "missing": tuple(missing), "waiver": waiver, "status": "active_edit" if ok else "package_blocked", "blockers": control["failures"]}
        self.manuscripts[manuscript_id] = manuscript
        return {"ok": ok, "manuscript": manuscript, "side_effects": ()}

    def freeze_version(self, manuscript_id: str, frozen_version: str | None, reason: str | None) -> dict:
        control = evaluate_control("version_freeze_recorded", {"frozen_version": frozen_version})
        manuscript = self.manuscripts.get(manuscript_id, {})
        manuscript = {**manuscript, "frozen_version": frozen_version, "freeze_reason": reason, "version_status": "frozen" if control["ok"] else "unfrozen"}
        self.manuscripts[manuscript_id] = manuscript
        return {"ok": manuscript_id in self.manuscripts and control["ok"], "manuscript": manuscript, "side_effects": ()}

    def invite_reviewer(self, review_id: str, manuscript_id: str, review_model: str, conflict: bool, anonymity_rule: str | None) -> dict:
        control = evaluate_control("reviewer_conflict_cleared", {"conflict": conflict, "anonymity_rule": anonymity_rule})
        review = {"id": review_id, "tenant": self.tenant, "manuscript_id": manuscript_id, "review_model": review_model, "conflict": conflict, "anonymity_rule": anonymity_rule, "status": "invited" if control["ok"] else "blocked", "blockers": control["failures"]}
        self.reviews[review_id] = review
        return {"ok": manuscript_id in self.manuscripts and control["ok"], "review": review, "side_effects": ()}

    def approve_decision_bundle(self, bundle_id: str, manuscript_id: str, rationale: str | None, review_synthesis: str | None, revision_points: tuple[str, ...], schedule_impact: str | None) -> dict:
        control = evaluate_control("decision_bundle_complete", {"rationale": rationale, "review_synthesis": review_synthesis, "revision_points": revision_points, "schedule_impact": schedule_impact})
        bundle = {"id": bundle_id, "tenant": self.tenant, "manuscript_id": manuscript_id, "rationale": rationale, "review_synthesis": review_synthesis, "revision_points": tuple(revision_points), "schedule_impact": schedule_impact, "status": "approved" if control["ok"] else "blocked", "blockers": control["failures"]}
        self.board_decisions[bundle_id] = bundle
        return {"ok": manuscript_id in self.manuscripts and control["ok"], "bundle": bundle, "side_effects": ()}

    def manage_copyedit(self, copyedit_id: str, manuscript_id: str, style_sheet: str, critical_open: int, signoff: bool) -> dict:
        control = evaluate_control("critical_queries_resolved", {"critical_open": critical_open})
        copyedit = {"id": copyedit_id, "tenant": self.tenant, "manuscript_id": manuscript_id, "style_sheet": style_sheet, "critical_open": critical_open, "signoff": signoff, "status": "signed_off" if control["ok"] and signoff else "query_blocked", "blockers": control["failures"]}
        self.copyedits[copyedit_id] = copyedit
        return {"ok": manuscript_id in self.manuscripts and control["ok"] and signoff, "copyedit": copyedit, "side_effects": ()}

    def clear_rights(self, rights_id: str, manuscript_id: str, territory: str, language: str, fmt: str, collisions: tuple[str, ...] = ()) -> dict:
        control = evaluate_control("rights_collision_absent", {"collisions": collisions})
        rights = {"id": rights_id, "tenant": self.tenant, "manuscript_id": manuscript_id, "territory": territory, "language": language, "format": fmt, "collisions": tuple(collisions), "status": "cleared" if control["ok"] else "collision", "blockers": control["failures"]}
        self.rights[rights_id] = rights
        return {"ok": manuscript_id in self.manuscripts and control["ok"], "rights": rights, "side_effects": ()}

    def approve_edition(self, edition_id: str, manuscript_id: str, identifiers: tuple[str, ...], accessibility_flags: tuple[str, ...]) -> dict:
        control = evaluate_control("metadata_authority_valid", {"identifiers": identifiers})
        edition = {"id": edition_id, "tenant": self.tenant, "manuscript_id": manuscript_id, "identifiers": tuple(identifiers), "accessibility_flags": tuple(accessibility_flags), "metadata_hash": _digest((identifiers, accessibility_flags)), "status": "metadata_ready" if control["ok"] else "metadata_blocked", "blockers": control["failures"]}
        self.editions[edition_id] = edition
        return {"ok": manuscript_id in self.manuscripts and control["ok"], "edition": edition, "side_effects": ()}

    def assemble_handoff(self, schedule_id: str, edition_id: str, frozen_text: str | None, assets: tuple[str, ...], rights: str | None, specs: str | None, metadata: str | None) -> dict:
        control = evaluate_control("production_handoff_complete", {"frozen_text": frozen_text, "assets": assets, "rights": rights, "specs": specs, "metadata": metadata})
        schedule = {"id": schedule_id, "tenant": self.tenant, "edition_id": edition_id, "frozen_text": frozen_text, "assets": tuple(assets), "rights": rights, "specs": specs, "metadata": metadata, "status": "handoff_ready" if control["ok"] else "handoff_blocked", "blockers": control["failures"]}
        self.schedules[schedule_id] = schedule
        return {"ok": edition_id in self.editions and control["ok"], "schedule": schedule, "side_effects": ()}

    def approve_proof(self, proof_id: str, edition_id: str, unclassified: int, blind: bool = False, redacted: bool = True) -> dict:
        correction_control = evaluate_control("proof_corrections_classified", {"unclassified": unclassified})
        privacy_control = evaluate_control("blind_review_privacy_enforced", {"blind": blind, "redacted": redacted})
        ok = edition_id in self.editions and correction_control["ok"] and privacy_control["ok"]
        proof = {"id": proof_id, "tenant": self.tenant, "edition_id": edition_id, "unclassified": unclassified, "blind": blind, "redacted": redacted, "status": "approved" if ok else "blocked", "blockers": correction_control["failures"] + privacy_control["failures"]}
        self.proofs[proof_id] = proof
        return {"ok": ok, "proof": proof, "side_effects": ()}

    def publish_release_binder(self, binder_id: str, edition_id: str, missing_sections: tuple[str, ...]) -> dict:
        control = evaluate_control("release_binder_complete", {"missing_sections": missing_sections})
        binder = {"id": binder_id, "tenant": self.tenant, "edition_id": edition_id, "sections": ("lineage", "rights", "metadata", "proof", "schedule", "communications", "exceptions"), "missing_sections": tuple(missing_sections), "verdict": "release_ready" if control["ok"] else "not_ready", "blockers": control["failures"]}
        self.distributions[binder_id] = binder
        return {"ok": edition_id in self.editions and control["ok"], "binder": binder, "side_effects": ()}

    def open_exception(self, exception_id: str, exception_class: str, owner: str, evidence: str | None) -> dict:
        ok = bool(exception_class) and bool(owner) and bool(evidence)
        exception = {"id": exception_id, "tenant": self.tenant, "exception_class": exception_class, "owner": owner, "evidence": evidence, "status": "resolved" if ok else "open"}
        self.exceptions[exception_id] = exception
        return {"ok": ok, "exception": exception, "side_effects": ()}

    def simulate_schedule(self, name: str, reviewer_delay_days: int, proof_round_delta: int) -> dict:
        return {"ok": True, "mutates_live_records": False, "name": name, "reviewer_delay_days": reviewer_delay_days, "proof_round_delta": proof_round_delta, "risk_score": min(1.0, 0.2 + reviewer_delay_days / 100 + proof_round_delta / 10), "side_effects": ()}

    def assistant_editorial_action_preview(self, document: str, instruction: str, confirmed: bool = False) -> dict:
        control = evaluate_control("agent_mutations_require_confirmation", {"confirmed": confirmed})
        document_plan = document_instruction_plan(document, instruction)
        crud_preview = datastore_crud_plan("update", table="publishing_editorial_operations_manuscript", payload={"instruction": instruction})
        return {"ok": document_plan["ok"] and crud_preview["ok"] and control["ok"], "document_plan": document_plan, "crud_preview": crud_preview, "control": control, "requires_confirmation": not confirmed, "side_effects": ()}

    def app_contract(self) -> dict:
        return {"format": "appgen.publishing-editorial-operations.standalone-app.v1", "ok": True, "pbc": PBC_KEY, "owned_tables": PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES, "database_backends": PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "schema": publishing_editorial_operations_build_schema_contract(), "services": publishing_editorial_operations_build_service_contract(), "routes": publishing_editorial_operations_build_api_contract(), "permissions": publishing_editorial_operations_permissions_contract(), "ui": publishing_editorial_operations_ui_contract(), "workbench": publishing_editorial_operations_render_workbench(), "forms": form_catalog(), "wizards": wizard_catalog(), "controls": control_catalog(), "agent": chatbot_interface_contract(), "composed_agent": composed_agent_contribution(), "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True}, "side_effects": ()}

    def run_demo(self) -> dict:
        configured = self.configure()
        bad_acq = self.capture_acquisition("A0", "packet", None, (), "Fall")
        acq = self.capture_acquisition("A1", "packet", "editor", ("Comp A",), "Fall")
        bad_board = self.record_board_decision("BD0", "A1", "conditional", True, ())
        board = self.record_board_decision("BD1", "A1", "conditional", True, ("revise sample",))
        bad_ms = self.create_manuscript("M0", "A1", ("author_bio",), None)
        ms = self.create_manuscript("M1", "A1", (), None)
        bad_freeze = self.freeze_version("M1", None, None)
        freeze = self.freeze_version("M1", "proof-v1", "ready for proof")
        bad_review = self.invite_reviewer("R0", "M1", "double_blind", True, "double_blind")
        review = self.invite_reviewer("R1", "M1", "double_blind", False, "double_blind")
        bad_bundle = self.approve_decision_bundle("DB0", "M1", "accept", None, ("revise",), "Fall risk")
        bundle = self.approve_decision_bundle("DB1", "M1", "accept", "strong reviews", ("revise",), "Fall risk")
        bad_copy = self.manage_copyedit("CE0", "M1", "house-v1", 1, True)
        copy = self.manage_copyedit("CE1", "M1", "house-v1", 0, True)
        bad_rights = self.clear_rights("RG0", "M1", "US", "en", "ebook", ("exclusive_audio",))
        rights = self.clear_rights("RG1", "M1", "US", "en", "ebook", ())
        bad_edition = self.approve_edition("E0", "M1", (), ("alt-text",))
        edition = self.approve_edition("E1", "M1", ("ISBN-1",), ("alt-text",))
        bad_handoff = self.assemble_handoff("S0", "E1", "proof-v1", (), "RG1", "trim", "meta")
        handoff = self.assemble_handoff("S1", "E1", "proof-v1", ("cover",), "RG1", "trim", "meta")
        bad_proof = self.approve_proof("P0", "E1", 1)
        proof = self.approve_proof("P1", "E1", 0, blind=True, redacted=True)
        bad_binder = self.publish_release_binder("B0", "E1", ("rights",))
        binder = self.publish_release_binder("B1", "E1", ())
        exception = self.open_exception("X1", "rights_collision", "rights-editor", "resolved")
        scenario = self.simulate_schedule("late review", 14, 1)
        agent_bad = self.assistant_editorial_action_preview("pitch", "create manuscript", False)
        agent = self.assistant_editorial_action_preview("pitch", "create manuscript", True)
        checks = (configured["ok"], bad_acq["ok"] is False, acq["ok"], bad_board["ok"] is False, board["ok"], bad_ms["ok"] is False, ms["ok"], bad_freeze["ok"] is False, freeze["ok"], bad_review["ok"] is False, review["ok"], bad_bundle["ok"] is False, bundle["ok"], bad_copy["ok"] is False, copy["ok"], bad_rights["ok"] is False, rights["ok"], bad_edition["ok"] is False, edition["ok"], bad_handoff["ok"] is False, handoff["ok"], bad_proof["ok"] is False, proof["ok"], bad_binder["ok"] is False, binder["ok"], exception["ok"], scenario["mutates_live_records"] is False, agent_bad["ok"] is False, agent["ok"])
        return {"ok": all(checks), "app_contract": self.app_contract(), "side_effects": ()}


def single_pbc_app_contract() -> dict:
    return PublishingEditorialOperationsStandaloneApp().app_contract()


def standalone_smoke_test() -> dict:
    app = PublishingEditorialOperationsStandaloneApp()
    demo = app.run_demo()
    runtime = publishing_editorial_operations_runtime_smoke()
    contract = single_pbc_app_contract()
    return {"ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(PUBLISHING_EDITORIAL_OPERATIONS_EMITTED_EVENT_TYPES), "demo": demo, "runtime": runtime, "contract": contract, "side_effects": ()}
