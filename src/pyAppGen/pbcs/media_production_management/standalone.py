"""Standalone one-PBC application for media_production_management."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    MEDIA_PRODUCTION_MANAGEMENT_CONSUMED_EVENT_TYPES,
    MEDIA_PRODUCTION_MANAGEMENT_EMITTED_EVENT_TYPES,
    MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES,
    MEDIA_PRODUCTION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    media_production_management_build_api_contract,
    media_production_management_build_schema_contract,
    media_production_management_build_service_contract,
    media_production_management_configure_runtime,
    media_production_management_empty_state,
    media_production_management_permissions_contract,
    media_production_management_receive_event,
    media_production_management_register_rule,
    media_production_management_runtime_smoke,
    media_production_management_set_parameter,
)
from .ui import media_production_management_render_workbench, media_production_management_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "media_production_management"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class MediaProductionManagementStandaloneApp:
    tenant: str = "tenant-media-001"
    state: dict = field(default_factory=media_production_management_empty_state)
    productions: dict[str, dict] = field(default_factory=dict)
    budgets: dict[str, dict] = field(default_factory=dict)
    engagements: dict[str, dict] = field(default_factory=dict)
    locations: dict[str, dict] = field(default_factory=dict)
    shoot_days: dict[str, dict] = field(default_factory=dict)
    call_sheets: dict[str, dict] = field(default_factory=dict)
    daily_reports: dict[str, dict] = field(default_factory=dict)
    dailies: dict[str, dict] = field(default_factory=dict)
    post_tasks: dict[str, dict] = field(default_factory=dict)
    rights: dict[str, dict] = field(default_factory=dict)
    deliverables: dict[str, dict] = field(default_factory=dict)
    exceptions: list[dict] = field(default_factory=list)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = media_production_management_configure_runtime(
            self.state,
            {"database_backend": database_backend, "event_topic": MEDIA_PRODUCTION_MANAGEMENT_REQUIRED_EVENT_TOPIC},
        )
        self.state = configured["state"]
        for name, value in (
            ("readiness_release_threshold", 90),
            ("budget_revision_approval_percent", 5),
            ("labor_turnaround_hours", 10),
            ("qc_reissue_sla_hours", 48),
            ("dailies_missing_media_escalation_hours", 12),
            ("agent_confidence_threshold", 0.82),
        ):
            result = media_production_management_set_parameter(self.state, name, value)
            self.state = result["state"]
        for rule in (
            {"rule_id": "greenlight_requires_script_finance_and_approval", "scope": "development"},
            {"rule_id": "call_sheet_requires_readiness_gate", "scope": "shoot_day"},
            {"rule_id": "high_risk_scene_requires_safety_plan", "scope": "safety"},
            {"rule_id": "dailies_missing_media_blocks_editorial_handoff", "scope": "dailies"},
            {"rule_id": "rights_and_qc_before_delivery", "scope": "delivery"},
        ):
            registered = media_production_management_register_rule(self.state, rule)
            self.state = registered["state"]
        inbound = media_production_management_receive_event(
            self.state,
            {"event_type": MEDIA_PRODUCTION_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "media-policy-001"},
        )
        self.state = inbound["state"]
        return {"ok": configured["ok"] and inbound["ok"], "side_effects": ()}

    def create_development_package(
        self,
        production_id: str,
        title: str,
        format: str,
        script_draft: str | None,
        creative_package_uri: str | None,
        attachments: tuple[str, ...],
        financing_status: str,
    ) -> dict:
        blockers = []
        if not script_draft:
            blockers.append("script_draft_missing")
        if not creative_package_uri:
            blockers.append("creative_package_missing")
        if financing_status not in {"exploratory", "soft-circled", "committed"}:
            blockers.append("invalid_financing_status")
        production = {
            "id": production_id,
            "tenant": self.tenant,
            "title": title,
            "format": format,
            "script_draft": script_draft,
            "creative_package_uri": creative_package_uri,
            "attachments": attachments,
            "financing_status": financing_status,
            "lifecycle_state": "development" if not blockers else "blocked_development",
            "version_hash": _digest((title, script_draft, creative_package_uri, attachments)),
            "blockers": tuple(blockers),
        }
        self.productions[production_id] = production
        return {"ok": not blockers, "production": production, "side_effects": ()}

    def greenlight_production(self, production_id: str, approval_complete: bool, target_release_window: str) -> dict:
        production = dict(self.productions[production_id])
        control = evaluate_control(
            "greenlight_requires_script_finance_and_approval",
            {
                "script_locked": bool(production.get("script_draft")),
                "financing_status": "committed" if production.get("financing_status") == "committed" else production.get("financing_status"),
                "approval_complete": approval_complete,
            },
        )
        production.update(
            {
                "target_release_window": target_release_window,
                "greenlight_control": control,
                "lifecycle_state": "greenlit" if control["ok"] else "greenlight_blocked",
            }
        )
        self.productions[production_id] = production
        return {"ok": control["ok"], "production": production, "emitted_event": "ProductionGreenlit" if control["ok"] else None, "side_effects": ()}

    def approve_budget_revision(
        self,
        budget_id: str,
        production_id: str,
        phase: str,
        approved_baseline: float,
        forecast_amount: float,
        contingency_draw: float,
        change_reason: str | None,
        approver_role: str,
    ) -> dict:
        variance = forecast_amount - approved_baseline
        variance_percent = abs(variance) / approved_baseline * 100 if approved_baseline else 100
        approval_required = variance_percent >= 5 or contingency_draw > 0
        ok = bool(change_reason) and (not approval_required or approver_role in {"line_producer", "studio_finance", "executive_producer"})
        budget = {
            "id": budget_id,
            "production_id": production_id,
            "phase": phase,
            "approved_baseline": approved_baseline,
            "forecast_amount": forecast_amount,
            "variance": round(variance, 2),
            "variance_percent": round(variance_percent, 2),
            "contingency_draw": contingency_draw,
            "change_reason": change_reason,
            "approval_required": approval_required,
            "approver_role": approver_role,
            "status": "approved_revision" if ok else "blocked_revision",
        }
        self.budgets[budget_id] = budget
        return {"ok": ok, "budget": budget, "side_effects": ()}

    def register_engagement_packet(
        self,
        engagement_id: str,
        production_id: str,
        person_name: str,
        engagement_type: str,
        union_status: str,
        rate_card: str | None,
        availability_window: tuple[int, int],
        deal_memo_source: str | None,
        work_guarantee_days: int = 0,
    ) -> dict:
        blockers = []
        if engagement_type not in {"principal_cast", "background", "crew", "vendor"}:
            blockers.append("invalid_engagement_type")
        if not rate_card:
            blockers.append("rate_card_missing")
        if not deal_memo_source:
            blockers.append("deal_memo_source_missing")
        if availability_window[0] >= availability_window[1]:
            blockers.append("invalid_availability")
        engagement = {
            "id": engagement_id,
            "production_id": production_id,
            "person_name": person_name,
            "engagement_type": engagement_type,
            "union_status": union_status,
            "rate_card": rate_card,
            "availability_window": availability_window,
            "deal_memo_source": deal_memo_source,
            "work_guarantee_days": work_guarantee_days,
            "status": "confirmed" if not blockers else "incomplete_packet",
            "blockers": tuple(blockers),
        }
        self.engagements[engagement_id] = engagement
        return {"ok": not blockers, "engagement": engagement, "side_effects": ()}

    def approve_location_package(
        self,
        location_id: str,
        production_id: str,
        jurisdiction: str,
        permit_id: str | None,
        curfew_hour: int,
        insurance_evidence: str | None,
        contingency_location: str | None,
    ) -> dict:
        blockers = []
        if not permit_id:
            blockers.append("permit_missing")
        if not insurance_evidence:
            blockers.append("insurance_evidence_missing")
        if not 0 <= curfew_hour <= 24:
            blockers.append("invalid_curfew")
        location = {
            "id": location_id,
            "production_id": production_id,
            "jurisdiction": jurisdiction,
            "permit_id": permit_id,
            "curfew_hour": curfew_hour,
            "insurance_evidence": insurance_evidence,
            "contingency_location": contingency_location,
            "status": "ready" if not blockers else "blocked",
            "blockers": tuple(blockers),
        }
        self.locations[location_id] = location
        return {"ok": not blockers, "location": location, "side_effects": ()}

    def build_shoot_day_readiness(
        self,
        shoot_day_id: str,
        production_id: str,
        scene_blocks: tuple[str, ...],
        cast_engagement_ids: tuple[str, ...],
        crew_engagement_ids: tuple[str, ...],
        location_id: str,
        equipment_ready: bool,
        transport_ready: bool,
        weather_review_complete: bool,
        risk_class: str = "standard",
        safety_plan: str | None = None,
    ) -> dict:
        blocking_gaps = []
        location = self.locations.get(location_id, {})
        if location.get("status") != "ready":
            blocking_gaps.append("location_not_ready")
        for engagement_id in cast_engagement_ids + crew_engagement_ids:
            if self.engagements.get(engagement_id, {}).get("status") != "confirmed":
                blocking_gaps.append(f"engagement_not_confirmed:{engagement_id}")
        if not equipment_ready:
            blocking_gaps.append("equipment_not_ready")
        if not transport_ready:
            blocking_gaps.append("transport_not_ready")
        if not weather_review_complete:
            blocking_gaps.append("weather_review_missing")
        safety = evaluate_control("high_risk_scene_requires_safety_plan", {"risk_class": risk_class, "safety_plan": safety_plan})
        blocking_gaps.extend(safety["failures"])
        score = max(0, 100 - 15 * len(blocking_gaps))
        day = {
            "id": shoot_day_id,
            "production_id": production_id,
            "scene_blocks": scene_blocks,
            "cast_engagement_ids": cast_engagement_ids,
            "crew_engagement_ids": crew_engagement_ids,
            "location_id": location_id,
            "equipment_ready": equipment_ready,
            "transport_ready": transport_ready,
            "weather_review_complete": weather_review_complete,
            "risk_class": risk_class,
            "safety_plan": safety_plan,
            "readiness_score": score,
            "blocking_gaps": tuple(blocking_gaps),
            "status": "ready_for_call_sheet" if not blocking_gaps and score >= 90 else "blocked",
        }
        self.shoot_days[shoot_day_id] = day
        return {"ok": day["status"] == "ready_for_call_sheet", "shoot_day": day, "side_effects": ()}

    def issue_call_sheet(
        self,
        call_sheet_id: str,
        shoot_day_id: str,
        nearest_hospital: str,
        weather: str,
        parking_plan: str,
        emergency_contacts: tuple[str, ...],
    ) -> dict:
        day = self.shoot_days[shoot_day_id]
        control = evaluate_control("call_sheet_requires_readiness_gate", {"blocking_gaps": day["blocking_gaps"]})
        ok = control["ok"] and bool(nearest_hospital) and bool(emergency_contacts)
        call_sheet = {
            "id": call_sheet_id,
            "shoot_day_id": shoot_day_id,
            "version": len([c for c in self.call_sheets.values() if c["shoot_day_id"] == shoot_day_id]) + 1,
            "nearest_hospital": nearest_hospital,
            "weather": weather,
            "parking_plan": parking_plan,
            "emergency_contacts": emergency_contacts,
            "status": "issued" if ok else "blocked",
            "supersedes": tuple(c["id"] for c in self.call_sheets.values() if c["shoot_day_id"] == shoot_day_id),
        }
        self.call_sheets[call_sheet_id] = call_sheet
        return {"ok": ok, "call_sheet": call_sheet, "emitted_event": "CallSheetIssued" if ok else None, "side_effects": ()}

    def capture_daily_production_report(
        self,
        report_id: str,
        shoot_day_id: str,
        first_call: int,
        first_shot: int,
        meal_break: int,
        wrap_time: int,
        pages_completed: float,
        planned_pages: float,
        delay_reasons: tuple[str, ...] = (),
        incidents: tuple[str, ...] = (),
    ) -> dict:
        overtime_hours = max(0, wrap_time - first_call - 12)
        meal_penalty = meal_break - first_call > 6
        page_variance = round(pages_completed - planned_pages, 2)
        report = {
            "id": report_id,
            "shoot_day_id": shoot_day_id,
            "first_call": first_call,
            "first_shot": first_shot,
            "meal_break": meal_break,
            "wrap_time": wrap_time,
            "pages_completed": pages_completed,
            "planned_pages": planned_pages,
            "page_variance": page_variance,
            "overtime_hours": overtime_hours,
            "meal_penalty": meal_penalty,
            "delay_reasons": delay_reasons,
            "incidents": incidents,
            "status": "reported",
        }
        self.daily_reports[report_id] = report
        if incidents:
            self.exceptions.append({"type": "safety_or_production_incident", "owner": "production_office", "source": report_id})
        return {"ok": True, "report": report, "side_effects": ()}

    def ingest_dailies(
        self,
        dailies_id: str,
        shoot_day_id: str,
        expected_cards: int,
        received_cards: int,
        checksum_verified: bool,
        sync_complete: bool,
        continuity_notes: tuple[str, ...] = (),
    ) -> dict:
        missing_cards = max(0, expected_cards - received_cards)
        ok = missing_cards == 0 and checksum_verified and sync_complete
        record = {
            "id": dailies_id,
            "shoot_day_id": shoot_day_id,
            "expected_cards": expected_cards,
            "received_cards": received_cards,
            "missing_cards": missing_cards,
            "checksum_verified": checksum_verified,
            "sync_complete": sync_complete,
            "continuity_notes": continuity_notes,
            "status": "editorial_ready" if ok else "blocked_dailies",
        }
        self.dailies[dailies_id] = record
        if not ok:
            self.exceptions.append({"type": "dailies_missing_or_unverified", "owner": "digital_imaging", "source": dailies_id})
        return {"ok": ok, "dailies": record, "side_effects": ()}

    def create_post_task(
        self,
        task_id: str,
        production_id: str,
        milestone: str,
        owner: str,
        dependency_ids: tuple[str, ...],
        vendor: str | None = None,
        shot_code: str | None = None,
        turnover_package_complete: bool = True,
    ) -> dict:
        dependency_missing = [dep for dep in dependency_ids if dep not in self.post_tasks and dep not in self.dailies]
        is_vfx = milestone in {"vfx_turnover", "vfx_final", "plate_delivery"}
        ok = not dependency_missing and (not is_vfx or turnover_package_complete)
        task = {
            "id": task_id,
            "production_id": production_id,
            "milestone": milestone,
            "owner": owner,
            "dependency_ids": dependency_ids,
            "vendor": vendor,
            "shot_code": shot_code,
            "turnover_package_complete": turnover_package_complete,
            "status": "ready" if ok else "blocked",
            "dependency_missing": tuple(dependency_missing),
        }
        self.post_tasks[task_id] = task
        return {"ok": ok, "post_task": task, "side_effects": ()}

    def register_rights_clearance(
        self,
        clearance_id: str,
        production_id: str,
        asset_type: str,
        territory: str,
        expiry: str | None,
        cleared: bool,
        evidence_uri: str | None,
    ) -> dict:
        ok = cleared and bool(evidence_uri)
        clearance = {
            "id": clearance_id,
            "production_id": production_id,
            "asset_type": asset_type,
            "territory": territory,
            "expiry": expiry,
            "cleared": cleared,
            "evidence_uri": evidence_uri,
            "status": "cleared" if ok else "blocked_clearance",
        }
        self.rights[clearance_id] = clearance
        return {"ok": ok, "clearance": clearance, "side_effects": ()}

    def assemble_deliverable(
        self,
        deliverable_id: str,
        production_id: str,
        platform: str,
        territory: str,
        language: str,
        audio_layout: str,
        caption_set: str | None,
        checksum: str | None,
        qc_result: str,
        rights_ids: tuple[str, ...],
        owner: str | None = None,
    ) -> dict:
        uncleared = [rid for rid in rights_ids if self.rights.get(rid, {}).get("status") != "cleared"]
        rights_control = evaluate_control("rights_clearance_blocks_delivery", {"uncleared_rights": len(uncleared)})
        qc_control = evaluate_control("qc_rejection_routes_to_owner", {"qc_result": qc_result, "owner": owner})
        ok = not uncleared and bool(caption_set) and bool(checksum) and qc_result == "passed" and qc_control["ok"]
        deliverable = {
            "id": deliverable_id,
            "production_id": production_id,
            "platform": platform,
            "territory": territory,
            "language": language,
            "audio_layout": audio_layout,
            "caption_set": caption_set,
            "checksum": checksum,
            "qc_result": qc_result,
            "rights_ids": rights_ids,
            "uncleared_rights": tuple(uncleared),
            "owner": owner,
            "status": "delivered" if ok else "blocked_delivery",
            "controls": (rights_control, qc_control),
        }
        self.deliverables[deliverable_id] = deliverable
        if not ok:
            self.exceptions.append({"type": "delivery_blocked", "owner": owner or "delivery_manager", "source": deliverable_id})
        return {"ok": ok, "deliverable": deliverable, "emitted_event": "PackageDelivered" if ok else None, "side_effects": ()}

    def simulate_schedule_budget_risk(self, production_id: str) -> dict:
        budget_risk = sum(1 for b in self.budgets.values() if b["production_id"] == production_id and b["variance"] > 0) * 0.12
        readiness_risk = sum(1 for d in self.shoot_days.values() if d["production_id"] == production_id and d["status"] != "ready_for_call_sheet") * 0.15
        post_risk = sum(1 for t in self.post_tasks.values() if t["production_id"] == production_id and t["status"] == "blocked") * 0.11
        delivery_risk = sum(1 for d in self.deliverables.values() if d["production_id"] == production_id and d["status"] != "delivered") * 0.14
        score = min(1.0, round(0.18 + budget_risk + readiness_risk + post_risk + delivery_risk, 3))
        return {
            "ok": True,
            "production_id": production_id,
            "mutates_live_records": False,
            "risk_score": score,
            "drivers": {
                "budget_risk": round(budget_risk, 3),
                "readiness_risk": round(readiness_risk, 3),
                "post_risk": round(post_risk, 3),
                "delivery_risk": round(delivery_risk, 3),
            },
            "side_effects": (),
        }

    def assistant_media_action_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan(
            "update",
            table="media_production_management_production",
            payload={"instruction": instruction, "source_digest": _digest(document)},
        )
        return {
            "ok": plan["ok"] and crud["ok"],
            "document_plan": plan,
            "crud_preview": crud,
            "requires_confirmation": True,
            "source_citations_required": True,
            "affected_events": ("ProductionUpdated", "ProductionExceptionOpened"),
            "side_effects": (),
        }

    def app_contract(self) -> dict:
        return {
            "format": "appgen.media-production-management.standalone-app.v1",
            "ok": True,
            "pbc": PBC_KEY,
            "owned_tables": MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES,
            "database_backends": MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "schema": media_production_management_build_schema_contract(),
            "services": media_production_management_build_service_contract(),
            "routes": media_production_management_build_api_contract(),
            "permissions": media_production_management_permissions_contract(),
            "ui": media_production_management_ui_contract(),
            "workbench": media_production_management_render_workbench(),
            "forms": form_catalog(),
            "wizards": wizard_catalog(),
            "controls": control_catalog(),
            "agent": chatbot_interface_contract(),
            "composed_agent": composed_agent_contribution(),
            "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True},
            "side_effects": (),
        }

    def run_demo(self) -> dict:
        cfg = self.configure()
        dev_bad = self.create_development_package("PROD-BAD", "Unready Pilot", "episodic", None, None, (), "unknown")
        dev = self.create_development_package("PROD-001", "Harbor Lights", "feature", "draft-04", "s3://creative/deck.pdf", ("director", "lead"), "committed")
        greenlight = self.greenlight_production("PROD-001", True, "2027-Q2")
        budget_bad = self.approve_budget_revision("BUD-BAD", "PROD-001", "shoot", 1000000, 1200000, 0, None, "coordinator")
        budget = self.approve_budget_revision("BUD-001", "PROD-001", "shoot", 1000000, 1060000, 10000, "weather cover and night premium", "studio_finance")
        cast = self.register_engagement_packet("ENG-CAST", "PROD-001", "Lead Actor", "principal_cast", "SAG", "rate-card-a", (1, 30), "deal-memo-001", 10)
        crew = self.register_engagement_packet("ENG-CREW", "PROD-001", "Gaffer", "crew", "IATSE", "rate-card-b", (1, 30), "deal-memo-002", 0)
        location_bad = self.approve_location_package("LOC-BAD", "PROD-001", "Mombasa", None, 22, None, None)
        location = self.approve_location_package("LOC-001", "PROD-001", "Mombasa", "PERMIT-1", 22, "insurance-cert", "warehouse cover")
        blocked_day = self.build_shoot_day_readiness("DAY-BAD", "PROD-001", ("12",), ("ENG-CAST",), ("ENG-CREW",), "LOC-001", True, True, True, "stunts", None)
        ready_day = self.build_shoot_day_readiness("DAY-001", "PROD-001", ("12", "14"), ("ENG-CAST",), ("ENG-CREW",), "LOC-001", True, True, True, "stunts", "stunt coordinator plan")
        call_sheet = self.issue_call_sheet("CALL-001", "DAY-001", "County Hospital", "clear", "north lot", ("AD", "Medic"))
        daily = self.capture_daily_production_report("DPR-001", "DAY-001", 6, 8, 12, 20, 4.5, 5.0, ("weather hold",), ())
        dailies_bad = self.ingest_dailies("DAILIES-BAD", "DAY-001", 4, 3, True, False)
        dailies = self.ingest_dailies("DAILIES-001", "DAY-001", 4, 4, True, True, ("pickup insert scene 14",))
        post_bad = self.create_post_task("POST-BAD", "PROD-001", "vfx_turnover", "vfx_producer", ("DAILIES-001",), "Vendor A", "SEQ010_SH020", False)
        post = self.create_post_task("POST-001", "PROD-001", "picture_lock", "editor", ("DAILIES-001",))
        rights_bad = self.register_rights_clearance("RIGHTS-BAD", "PROD-001", "music_cue", "worldwide", "2028-01-01", False, None)
        rights = self.register_rights_clearance("RIGHTS-001", "PROD-001", "location_release", "worldwide", None, True, "vault://release/location")
        delivery_bad = self.assemble_deliverable("DEL-BAD", "PROD-001", "streamer-a", "US", "en", "5.1", "captions-v1", "abc", "failed", ("RIGHTS-BAD",), None)
        delivery = self.assemble_deliverable("DEL-001", "PROD-001", "streamer-a", "US", "en", "5.1", "captions-v1", "checksum-001", "passed", ("RIGHTS-001",), "delivery_manager")
        risk = self.simulate_schedule_budget_risk("PROD-001")
        assistant = self.assistant_media_action_preview("call sheet pdf text", "revise call time and update transport notes")
        checks = (
            cfg["ok"],
            dev_bad["ok"] is False,
            dev["ok"],
            greenlight["ok"],
            budget_bad["ok"] is False,
            budget["ok"],
            cast["ok"],
            crew["ok"],
            location_bad["ok"] is False,
            location["ok"],
            blocked_day["ok"] is False,
            ready_day["ok"],
            call_sheet["ok"],
            daily["ok"],
            dailies_bad["ok"] is False,
            dailies["ok"],
            post_bad["ok"] is False,
            post["ok"],
            rights_bad["ok"] is False,
            rights["ok"],
            delivery_bad["ok"] is False,
            delivery["ok"],
            risk["ok"] and risk["mutates_live_records"] is False,
            assistant["ok"],
        )
        return {
            "ok": all(checks),
            "development_gap": dev_bad,
            "budget_gap": budget_bad,
            "location_gap": location_bad,
            "blocked_shoot_day": blocked_day,
            "dailies_gap": dailies_bad,
            "post_gap": post_bad,
            "rights_gap": rights_bad,
            "delivery_gap": delivery_bad,
            "risk": risk,
            "assistant": assistant,
            "app_contract": self.app_contract(),
            "side_effects": (),
        }


def single_pbc_app_contract() -> dict:
    return MediaProductionManagementStandaloneApp().app_contract()


def standalone_smoke_test() -> dict:
    app = MediaProductionManagementStandaloneApp()
    demo = app.run_demo()
    runtime = media_production_management_runtime_smoke()
    contract = single_pbc_app_contract()
    return {
        "ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(MEDIA_PRODUCTION_MANAGEMENT_EMITTED_EVENT_TYPES) and contract["stream_engine_picker_visible"] is False,
        "demo": demo,
        "runtime": runtime,
        "contract": contract,
        "side_effects": (),
    }
