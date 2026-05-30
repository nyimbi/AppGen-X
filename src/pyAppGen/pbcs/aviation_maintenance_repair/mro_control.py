"""Aviation MRO control primitives for improve1 domain execution.

These functions are deterministic, side-effect-free, and package-local. They
model the specialist control decisions behind the 50-item aviation maintenance
repair improve1 backlog without reading shared tables or external systems.
"""
from __future__ import annotations

from datetime import date
import hashlib
from typing import Mapping, Sequence

PBC_KEY = "aviation_maintenance_repair"
EVENT_CONTRACT = "AppGen-X"

MRO_CONTROL_CAPABILITIES = (
    "aircraft_configuration_baseline",
    "aircraft_utilization_synchronization",
    "serialized_component_history",
    "life_limited_part_status",
    "maintenance_program_applicability",
    "work_card_revision_control",
    "non_routine_card_generation",
    "defect_log_governance",
    "mel_cdl_deferment_countdown",
    "airworthiness_directive_planning",
    "service_bulletin_decision_register",
    "engineering_order_governance",
    "maintenance_visit_planning",
    "inspection_campaign_orchestration",
    "duplicate_inspection_enforcement",
    "technician_authorization_matrix",
    "shift_handover_continuity",
    "tooling_calibration_lockout",
    "consumable_life_control",
    "material_readiness_board",
    "parts_traceability_pack",
    "quarantine_flow",
    "rotable_lifecycle_tracking",
    "cannibalization_governance",
    "vendor_repair_station_evidence",
    "inspection_evidence_capture",
    "release_to_service_evidence_pack",
    "deferred_defect_risk_board",
    "repeat_defect_detection",
    "reliability_metrics",
    "deferred_defect_forecast_breach",
    "maintenance_forecast",
    "aog_triage_workbench",
    "line_maintenance_workbench",
    "base_maintenance_control_tower",
    "continuous_release_evidence_generation",
    "domain_event_boundary_catalog",
    "validation_simulation_export_api_boundary",
    "cross_linked_audit_trail",
    "signed_record_correction",
    "technical_document_revision_intake",
    "agent_work_scope_drafting",
    "agent_defect_troubleshooting_evidence",
    "agent_certification_guardrails",
    "reliability_to_planning_feedback",
    "fleet_configuration_drift_dashboard",
    "lease_return_redelivery_readiness",
    "structural_corrosion_campaign_management",
    "pre_close_release_gate",
    "continuous_airworthiness_dashboard",
)


def _as_tuple(value: object) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, (list, set)):
        return tuple(value)
    return (value,)


def _as_date(value: object | None) -> date:
    if value is None:
        return date(2026, 5, 30)
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()[:16]


def _result(capability: str, **payload: object) -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "capability": capability,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
        **payload,
    }


def build_aircraft_configuration_baseline(aircraft: Mapping[str, object], requirements: Sequence[Mapping[str, object]] = ()) -> dict:
    aircraft = dict(aircraft or {})
    option_codes = set(_as_tuple(aircraft.get("option_codes")))
    mod_status = dict(aircraft.get("embodiment_status") or {})
    applicable = []
    suppressed = []
    for requirement in requirements:
        requirement = dict(requirement)
        required_option = requirement.get("option_code")
        required_mod = requirement.get("mod_standard")
        applies = (not required_option or required_option in option_codes) and (not required_mod or mod_status.get(required_mod) == "embodied")
        target = applicable if applies else suppressed
        target.append({**requirement, "effectivity_trace": {"option_code": required_option, "mod_standard": required_mod}})
    return _result(
        "aircraft_configuration_baseline",
        table=f"{PBC_KEY}_aircraft",
        tail_number=aircraft.get("tail_number"),
        baseline={"fleet_subtype": aircraft.get("fleet_subtype"), "option_codes": tuple(sorted(option_codes)), "embodiment_status": mod_status},
        applicable_requirements=tuple(applicable),
        suppressed_requirements=tuple(suppressed),
    )


def synchronize_utilization_timeline(aircraft: Mapping[str, object], utilization_updates: Sequence[Mapping[str, object]]) -> dict:
    aircraft = dict(aircraft or {})
    totals = {"flight_hours": float(aircraft.get("flight_hours", 0)), "flight_cycles": int(aircraft.get("flight_cycles", 0)), "grounded_intervals": 0}
    timeline = []
    for update in utilization_updates:
        update = dict(update)
        totals["flight_hours"] += float(update.get("flight_hours", 0))
        totals["flight_cycles"] += int(update.get("flight_cycles", 0))
        if update.get("status") in {"grounded", "aog", "maintenance"}:
            totals["grounded_intervals"] += 1
        timeline.append({**update, "cumulative_hours": round(totals["flight_hours"], 2), "cumulative_cycles": totals["flight_cycles"]})
    return _result("aircraft_utilization_synchronization", table=f"{PBC_KEY}_aircraft", tail_number=aircraft.get("tail_number"), totals=totals, timeline=tuple(timeline))


def build_serialized_component_history(serial: str, movements: Sequence[Mapping[str, object]]) -> dict:
    ordered = tuple(dict(item) for item in movements)
    current = ordered[-1] if ordered else {}
    carried_defects = tuple(item.get("defect_id") for item in ordered if item.get("defect_id"))
    return _result("serialized_component_history", table=f"{PBC_KEY}_component", serial_number=serial, current_position=current.get("position"), movement_history=ordered, carried_defects=carried_defects)


def calculate_life_limited_part_status(component: Mapping[str, object], as_of: object | None = None) -> dict:
    component = dict(component or {})
    remaining_hours = float(component.get("limit_hours", 0)) - float(component.get("hours_since_new", 0))
    remaining_cycles = int(component.get("limit_cycles", 0)) - int(component.get("cycles_since_new", 0))
    blocked = remaining_hours <= 0 or remaining_cycles <= 0 or component.get("quarantine_state") in {"active", "suspect", "quarantined"}
    alert = remaining_hours <= float(component.get("soft_alert_hours", 50)) or remaining_cycles <= int(component.get("soft_alert_cycles", 25))
    return _result("life_limited_part_status", table=f"{PBC_KEY}_component", component_id=component.get("component_id"), as_of=_as_date(as_of).isoformat(), status="blocked" if blocked else "alert" if alert else "serviceable", remaining_life={"hours": remaining_hours, "cycles": remaining_cycles})


def evaluate_maintenance_program_applicability(program: Mapping[str, object], aircraft: Mapping[str, object]) -> dict:
    program = dict(program or {})
    aircraft = dict(aircraft or {})
    applies = aircraft.get("fleet_subtype") in set(_as_tuple(program.get("fleet_subtypes"))) or aircraft.get("aircraft_type") in set(_as_tuple(program.get("aircraft_types")))
    return _result("maintenance_program_applicability", table=f"{PBC_KEY}_maintenance_visit", applies=applies, revision=program.get("revision"), interval_source=program.get("interval_source"), escalation_reference=program.get("escalation_reference"))


def control_work_card_revision(work_card: Mapping[str, object], source_document: Mapping[str, object]) -> dict:
    card = dict(work_card or {})
    doc = dict(source_document or {})
    stale = bool(card.get("source_revision") and doc.get("revision") and card.get("source_revision") != doc.get("revision"))
    applicable = not card.get("effectivity") or card.get("aircraft_type") in set(_as_tuple(card.get("effectivity")))
    required_roles = tuple(card.get("required_signoff_roles") or ("performer",))
    return _result("work_card_revision_control", table=f"{PBC_KEY}_work_card", work_card_id=card.get("work_card_id"), locked_revision=card.get("source_revision"), current_document_revision=doc.get("revision"), stale_revision=stale, applicable=applicable, required_signoff_roles=required_roles, blocked=stale or not applicable)


def generate_non_routine_card(originating_card: Mapping[str, object], finding: Mapping[str, object]) -> dict:
    finding = dict(finding or {})
    origin = dict(originating_card or {})
    card_id = f"NR-{origin.get('work_card_id', 'CARD')}-{_digest(finding)[:6]}"
    return _result("non_routine_card_generation", table=f"{PBC_KEY}_work_card", work_card_id=card_id, origin_work_card_id=origin.get("work_card_id"), zone=finding.get("zone"), ata=finding.get("ata"), critical_path_impact=bool(finding.get("critical_path")))


def build_defect_log(defect: Mapping[str, object], actions: Sequence[Mapping[str, object]]) -> dict:
    narrative = tuple(dict(item) for item in actions)
    status = "closed" if narrative and narrative[-1].get("action") in {"rectified", "cleared", "closed"} else dict(defect or {}).get("status", "open")
    return _result("defect_log_governance", table=f"{PBC_KEY}_deferred_defect", defect_id=dict(defect or {}).get("defect_id"), status=status, chronology=narrative, has_troubleshooting=any(item.get("action") == "troubleshooting" for item in narrative))


def evaluate_mel_cdl_deferment(defect: Mapping[str, object], utilization_projection: Mapping[str, object], as_of: object | None = None) -> dict:
    defect = dict(defect or {})
    today = _as_date(as_of)
    expiry = _as_date(defect.get("expiry_date")) if defect.get("expiry_date") else today
    days_remaining = (expiry - today).days
    projected_days = int(utilization_projection.get("days_until_next_maintenance", 0))
    breach_before_maintenance = days_remaining < projected_days
    return _result("mel_cdl_deferment_countdown", table=f"{PBC_KEY}_deferred_defect", defect_id=defect.get("defect_id"), category=defect.get("category"), days_remaining=days_remaining, breach_before_maintenance=breach_before_maintenance, required_procedures=tuple(defect.get("operational_procedures") or ()))


def plan_airworthiness_directive_compliance(directive: Mapping[str, object], population: Sequence[Mapping[str, object]]) -> dict:
    directive = dict(directive or {})
    applicable = tuple(dict(item) for item in population if item.get("aircraft_type") in set(_as_tuple(directive.get("aircraft_types"))))
    overdue = tuple(item for item in applicable if int(item.get("days_to_due", 999)) < 0)
    suppressed = bool(directive.get("terminating_action_embodied") or directive.get("amoc_reference"))
    return _result("airworthiness_directive_planning", table=f"{PBC_KEY}_airworthiness_directive", ad_id=directive.get("ad_id"), applicable_population=applicable, overdue_population=overdue, next_due_suppressed=suppressed)


def register_service_bulletin_decision(sb: Mapping[str, object]) -> dict:
    sb = dict(sb or {})
    adopted = sb.get("decision") in {"adopt", "partial_adopt", "mandatory"}
    return _result("service_bulletin_decision_register", table=f"{PBC_KEY}_maintenance_visit", sb_id=sb.get("sb_id"), adopted=adopted, embodiment_strategy=sb.get("embodiment_strategy"), affected_fleet=tuple(sb.get("affected_fleet") or ()), open_exposure=tuple(sb.get("open_exposure") or ()))


def govern_engineering_order(order: Mapping[str, object], target: Mapping[str, object]) -> dict:
    order = dict(order or {})
    target = dict(target or {})
    applicable = not order.get("applicability") or target.get("tail_number") in set(_as_tuple(order.get("applicability"))) or target.get("serial_number") in set(_as_tuple(order.get("applicability")))
    return _result("engineering_order_governance", table=f"{PBC_KEY}_maintenance_visit", engineering_order_id=order.get("engineering_order_id"), applicable=applicable, approval_basis=order.get("approval_basis"), repair_classification=order.get("repair_classification"))


def plan_maintenance_visit(visit: Mapping[str, object], work_cards: Sequence[Mapping[str, object]], material_board: Sequence[Mapping[str, object]] = ()) -> dict:
    cards = tuple(dict(item) for item in work_cards)
    material = tuple(dict(item) for item in material_board)
    blockers = tuple(item for item in material if item.get("status") in {"short", "blocked"})
    critical = tuple(card for card in cards if card.get("critical_path"))
    slipped = tuple(card for card in critical if int(card.get("slip_hours", 0)) > 0)
    return _result("maintenance_visit_planning", table=f"{PBC_KEY}_maintenance_visit", visit_id=dict(visit or {}).get("visit_id"), critical_path=critical, slipped_critical_path=slipped, material_blockers=blockers, release_risk="high" if blockers or slipped else "controlled")


def orchestrate_inspection_campaign(campaign: Mapping[str, object], findings: Sequence[Mapping[str, object]]) -> dict:
    findings = tuple(dict(item) for item in findings)
    open_findings = tuple(item for item in findings if item.get("status") not in {"closed", "accepted"})
    zones = tuple(sorted({item.get("zone") for item in findings if item.get("zone")}))
    return _result("inspection_campaign_orchestration", table=f"{PBC_KEY}_work_card", campaign_id=dict(campaign or {}).get("campaign_id"), zones=zones, open_findings=open_findings, release_blocked=bool(open_findings))


def enforce_duplicate_inspection(work_card: Mapping[str, object]) -> dict:
    card = dict(work_card or {})
    signoffs = tuple(dict(item) for item in _as_tuple(card.get("signoffs")))
    performer = next((item for item in signoffs if item.get("role") == "performer"), {})
    inspector = next((item for item in signoffs if item.get("role") in {"inspector", "duplicate_inspector"}), {})
    self_release = performer and inspector and performer.get("technician_id") == inspector.get("technician_id")
    missing = bool(card.get("duplicate_inspection_required") and not inspector)
    return _result("duplicate_inspection_enforcement", table=f"{PBC_KEY}_work_card", work_card_id=card.get("work_card_id"), valid=not self_release and not missing, self_release_blocked=bool(self_release), duplicate_inspection_missing=missing)


def evaluate_technician_authorization(task: Mapping[str, object], authorizations: Sequence[Mapping[str, object]], as_of: object | None = None) -> dict:
    task = dict(task or {})
    today = _as_date(as_of)
    matches = []
    for auth in authorizations:
        auth = dict(auth)
        if auth.get("technician_id") == task.get("technician_id") and auth.get("aircraft_type") == task.get("aircraft_type") and auth.get("task_family") == task.get("task_family"):
            valid_to = _as_date(auth.get("valid_to")) if auth.get("valid_to") else today
            matches.append({**auth, "valid": valid_to >= today})
    return _result("technician_authorization_matrix", table=f"{PBC_KEY}_work_card", authorized=any(item["valid"] for item in matches), authorization_matches=tuple(matches), task_family=task.get("task_family"))


def build_shift_handover(visit: Mapping[str, object], open_items: Sequence[Mapping[str, object]]) -> dict:
    items = tuple(dict(item) for item in open_items)
    safety = tuple(item for item in items if item.get("safety_critical") or item.get("isolated_system"))
    return _result("shift_handover_continuity", table=f"{PBC_KEY}_maintenance_visit", visit_id=dict(visit or {}).get("visit_id"), open_items=items, safety_critical_items=safety, acknowledgement_required=bool(items))


def evaluate_tooling_lockout(tools: Sequence[Mapping[str, object]], as_of: object | None = None) -> dict:
    today = _as_date(as_of)
    tools = tuple(dict(item) for item in tools)
    blocked = tuple(item for item in tools if not item.get("returned", True) or (item.get("calibration_due") and _as_date(item["calibration_due"]) < today))
    return _result("tooling_calibration_lockout", table=f"{PBC_KEY}_work_card", blocked_tools=blocked, release_blocked=bool(blocked))


def evaluate_consumable_life(consumables: Sequence[Mapping[str, object]], as_of: object | None = None) -> dict:
    today = _as_date(as_of)
    consumables = tuple(dict(item) for item in consumables)
    expired = tuple(item for item in consumables if item.get("expiry") and _as_date(item["expiry"]) < today or item.get("mix_life_expired"))
    return _result("consumable_life_control", table=f"{PBC_KEY}_work_card", expired_consumables=expired, release_blocked=bool(expired))


def build_material_readiness_board(work_cards: Sequence[Mapping[str, object]], part_requests: Sequence[Mapping[str, object]]) -> dict:
    requests = tuple(dict(item) for item in part_requests)
    shortages = tuple(item for item in requests if item.get("status") in {"short", "awaiting_alternate", "blocked"})
    critical_shortages = tuple(item for item in shortages if item.get("work_card_id") in {card.get("work_card_id") for card in work_cards if card.get("critical_path")})
    return _result("material_readiness_board", table=f"{PBC_KEY}_work_card", shortages=shortages, critical_path_shortages=critical_shortages, kit_complete=not shortages)


def validate_parts_traceability_pack(component: Mapping[str, object]) -> dict:
    component = dict(component or {})
    required = ("release_certificate", "serial_number", "source_chain", "life_document")
    missing = tuple(item for item in required if not component.get(item))
    return _result("parts_traceability_pack", table=f"{PBC_KEY}_component", component_id=component.get("component_id"), complete=not missing, missing_evidence=missing, installation_blocked=bool(missing))


def quarantine_part_flow(component: Mapping[str, object], release_request: Mapping[str, object] | None = None) -> dict:
    component = dict(component or {})
    active = component.get("quarantine_state") in {"active", "suspect", "damaged", "unapproved"}
    release_allowed = active and bool(dict(release_request or {}).get("technical_justification")) and bool(dict(release_request or {}).get("authority"))
    return _result("quarantine_flow", table=f"{PBC_KEY}_component", component_id=component.get("component_id"), quarantined=active, release_allowed=release_allowed, installation_blocked=active and not release_allowed)


def track_rotable_lifecycle(rotable: Mapping[str, object], events: Sequence[Mapping[str, object]]) -> dict:
    events = tuple(dict(item) for item in events)
    repair = next((item for item in reversed(events) if item.get("event") in {"repair_dispatched", "vendor_received", "returned_serviceable"}), {})
    repeat_removals = sum(1 for item in events if item.get("event") == "removed") > 1
    return _result("rotable_lifecycle_tracking", table=f"{PBC_KEY}_component", rotable_id=dict(rotable or {}).get("component_id"), current_repair_state=repair.get("event"), repeat_removal_pressure=repeat_removals, lifecycle_events=events)


def govern_cannibalization(action: Mapping[str, object]) -> dict:
    action = dict(action or {})
    restoration_due = bool(action.get("donor_aircraft") and action.get("restoration_due_date"))
    return _result("cannibalization_governance", table=f"{PBC_KEY}_component", donor_aircraft=action.get("donor_aircraft"), recipient_aircraft=action.get("recipient_aircraft"), reversible_record=True, restoration_due=restoration_due, open_donor_exposure=not action.get("restoration_closed"))


def evaluate_vendor_repair_station_work(package: Mapping[str, object]) -> dict:
    package = dict(package or {})
    accepted = bool(package.get("vendor_capability_basis") and package.get("release_document") and package.get("technical_acceptance"))
    return _result("vendor_repair_station_evidence", table=f"{PBC_KEY}_component", repair_order_id=package.get("repair_order_id"), accepted=accepted, closure_blocked=not accepted)


def capture_inspection_evidence(evidence: Mapping[str, object]) -> dict:
    evidence = dict(evidence or {})
    complete = bool(evidence.get("method") and evidence.get("inspector_qualification") and evidence.get("measured_result") and evidence.get("disposition"))
    return _result("inspection_evidence_capture", table=f"{PBC_KEY}_work_card", evidence_id=evidence.get("evidence_id"), complete=complete, media=tuple(evidence.get("media") or ()), disposition=evidence.get("disposition"))


def generate_release_evidence_pack(payload: Mapping[str, object]) -> dict:
    payload = dict(payload or {})
    categories = {
        "signed_cards": tuple(payload.get("signed_cards") or ()),
        "duplicate_inspections": tuple(payload.get("duplicate_inspections") or ()),
        "deferred_defects": tuple(payload.get("deferred_defects") or ()),
        "parts_traceability": tuple(payload.get("parts_traceability") or ()),
        "authorization_checks": tuple(payload.get("authorization_checks") or ()),
    }
    missing = tuple(name for name, values in categories.items() if not values)
    return _result("release_to_service_evidence_pack", table=f"{PBC_KEY}_compliance_release", release_id=payload.get("release_id"), categories=categories, missing_categories=missing, ready=not missing)


def build_defect_risk_board(defects: Sequence[Mapping[str, object]]) -> dict:
    defects = tuple(dict(item) for item in defects)
    ranked = tuple(sorted(defects, key=lambda item: (item.get("mel_category", "D"), -int(item.get("recurrence_count", 0)), int(item.get("days_remaining", 999)))))
    immediate = tuple(item for item in ranked if int(item.get("days_remaining", 999)) <= 2 or int(item.get("recurrence_count", 0)) >= 3)
    return _result("deferred_defect_risk_board", table=f"{PBC_KEY}_deferred_defect", ranked_defects=ranked, immediate_attention=immediate)


def detect_repeat_defect(new_defect: Mapping[str, object], history: Sequence[Mapping[str, object]], threshold_days: int = 30) -> dict:
    new_defect = dict(new_defect or {})
    matches = tuple(dict(item) for item in history if item.get("tail_number") == new_defect.get("tail_number") and item.get("ata") == new_defect.get("ata") and item.get("symptom") == new_defect.get("symptom") and int(item.get("days_since_clearance", 999)) <= threshold_days)
    return _result("repeat_defect_detection", table=f"{PBC_KEY}_deferred_defect", defect_id=new_defect.get("defect_id"), recurrent=bool(matches), related_occurrences=matches)


def compute_reliability_metrics(defects: Sequence[Mapping[str, object]], removals: Sequence[Mapping[str, object]]) -> dict:
    defect_count = len(tuple(defects))
    removal_count = len(tuple(removals))
    by_ata: dict[str, int] = {}
    for item in tuple(defects) + tuple(removals):
        ata = str(dict(item).get("ata", "unknown"))
        by_ata[ata] = by_ata.get(ata, 0) + 1
    top_offenders = tuple(sorted(by_ata.items(), key=lambda item: item[1], reverse=True))
    return _result("reliability_metrics", table=f"{PBC_KEY}_deferred_defect", defect_count=defect_count, unscheduled_removal_count=removal_count, top_offenders=top_offenders)


def forecast_deferred_defect_breach(defect: Mapping[str, object], utilization_projection: Mapping[str, object], as_of: object | None = None) -> dict:
    countdown = evaluate_mel_cdl_deferment(defect, utilization_projection, as_of=as_of)
    options = ("pull_forward_line_check", "assign_base_visit", "clear_defect_before_dispatch") if countdown["breach_before_maintenance"] else ("monitor",)
    return _result("deferred_defect_forecast_breach", table=f"{PBC_KEY}_deferred_defect", forecast_breach_date=dict(defect or {}).get("expiry_date"), breach_before_maintenance=countdown["breach_before_maintenance"], maintenance_options=options)


def build_maintenance_forecast(tasks: Sequence[Mapping[str, object]], utilization: Mapping[str, object]) -> dict:
    utilization = dict(utilization or {})
    forecast = []
    for task in tasks:
        task = dict(task)
        hours_remaining = float(task.get("hour_interval", 0)) - float(utilization.get("projected_hours", 0))
        cycles_remaining = int(task.get("cycle_interval", 0)) - int(utilization.get("projected_cycles", 0))
        driver = "flight_hours" if hours_remaining <= cycles_remaining else "flight_cycles"
        forecast.append({**task, "due_driver": driver, "hours_remaining": hours_remaining, "cycles_remaining": cycles_remaining})
    return _result("maintenance_forecast", table=f"{PBC_KEY}_maintenance_visit", forecast=tuple(forecast), changed_items=tuple(item for item in forecast if item.get("hours_remaining", 999) <= 50 or item.get("cycles_remaining", 999) <= 25))


def build_aog_triage_workbench(event: Mapping[str, object], resources: Mapping[str, object]) -> dict:
    event = dict(event or {})
    resources = dict(resources or {})
    blockers = tuple(name for name in ("authorized_staff", "nearby_parts", "engineering_disposition") if not resources.get(name))
    return _result("aog_triage_workbench", table=f"{PBC_KEY}_deferred_defect", tail_number=event.get("tail_number"), recovery_blockers=blockers, next_decision="resolve_blockers" if blockers else "release_recovery_plan")


def build_line_maintenance_workbench(tail_status: Mapping[str, object]) -> dict:
    status = dict(tail_status or {})
    dispatch_critical = tuple(item for item in _as_tuple(status.get("open_defects")) if dict(item).get("dispatch_critical"))
    return _result("line_maintenance_workbench", table=f"{PBC_KEY}_aircraft", tail_number=status.get("tail_number"), dispatch_critical_defects=dispatch_critical, release_ready=not dispatch_critical and not status.get("release_blockers"))


def build_base_maintenance_control_tower(visits: Sequence[Mapping[str, object]]) -> dict:
    visits = tuple(dict(item) for item in visits)
    drivers = tuple(item for item in visits if item.get("critical_path_slipped") or item.get("material_blockers"))
    return _result("base_maintenance_control_tower", table=f"{PBC_KEY}_maintenance_visit", visits=visits, release_drivers=drivers, dock_count=len({item.get("dock") for item in visits if item.get("dock")}))


def build_event_boundary_catalog() -> dict:
    events = (
        "AircraftGrounded", "WorkCardReleased", "WorkCardSigned", "DefectDeferred", "AirworthinessDirectiveComplied", "ComponentInstalled", "MaintenanceReleaseIssued",
    )
    return _result("domain_event_boundary_catalog", table=f"{PBC_KEY}_appgen_outbox_event", events=events, payload_contracts=tuple({"event_type": event, "contract": EVENT_CONTRACT} for event in events))


def build_api_boundary_expansion() -> dict:
    routes = (
        "POST /aviation-maintenance-repair/applicability:validate",
        "POST /aviation-maintenance-repair/forecast:simulate",
        "GET /aviation-maintenance-repair/release-packs/{id}:export",
        "POST /aviation-maintenance-repair/repeat-defects:lookup",
        "POST /aviation-maintenance-repair/authorizations:precheck",
    )
    return _result("validation_simulation_export_api_boundary", table=f"{PBC_KEY}_compliance_release", routes=routes, mutation_bypass_allowed=False)


def build_cross_linked_audit_trail(events: Sequence[Mapping[str, object]]) -> dict:
    pivots = {"aircraft": {}, "component": {}, "work_card": {}, "certifier": {}}
    for event in events:
        event = dict(event)
        for pivot in pivots:
            key = event.get(pivot) or event.get(f"{pivot}_id")
            if key:
                pivots[pivot].setdefault(key, []).append(event)
    return _result("cross_linked_audit_trail", table=f"{PBC_KEY}_compliance_release", pivots={name: {key: tuple(value) for key, value in records.items()} for name, records in pivots.items()})


def correct_signed_record(record: Mapping[str, object], correction: Mapping[str, object]) -> dict:
    record = dict(record or {})
    correction = dict(correction or {})
    approved = bool(correction.get("requested_by") and correction.get("reason") and correction.get("approved_by"))
    return _result("signed_record_correction", table=f"{PBC_KEY}_work_card", original_record=record, superseding_statement=correction.get("superseding_statement"), approved=approved, original_visible=True)


def ingest_technical_document_revision(document: Mapping[str, object], affected_items: Sequence[Mapping[str, object]]) -> dict:
    document = dict(document or {})
    impacts = tuple({**dict(item), "regeneration_required": dict(item).get("current_revision") != document.get("revision")} for item in affected_items)
    return _result("technical_document_revision_intake", table=f"{PBC_KEY}_work_card", document_type=document.get("document_type"), revision=document.get("revision"), impacted_items=impacts, acknowledgement_required=bool(impacts))


def draft_work_scope_from_planning_package(package: Mapping[str, object]) -> dict:
    package = dict(package or {})
    proposed = []
    for source in ("due_tasks", "open_defects", "ad_sb_exposure", "material_ready_cards"):
        for item in _as_tuple(package.get(source)):
            item = dict(item)
            proposed.append({"source": source, "task_id": item.get("task_id") or item.get("defect_id") or item.get("reference"), "reason": item.get("reason") or source, "planner_decision": "pending"})
    return _result("agent_work_scope_drafting", table=f"{PBC_KEY}_work_card", proposed_scope=tuple(proposed), requires_human_confirmation=True)


def assemble_defect_troubleshooting_evidence(defect: Mapping[str, object], history: Sequence[Mapping[str, object]], references: Sequence[Mapping[str, object]]) -> dict:
    defect = dict(defect or {})
    facts = tuple(dict(item) for item in history if item.get("ata") == defect.get("ata") or item.get("symptom") == defect.get("symptom"))
    approved_refs = tuple(dict(item) for item in references if item.get("approved"))
    return _result("agent_defect_troubleshooting_evidence", table=f"{PBC_KEY}_deferred_defect", defect_id=defect.get("defect_id"), facts=facts, approved_references=approved_refs, unsupported_suggestions=())


def enforce_agent_certification_guardrails(action: Mapping[str, object]) -> dict:
    action = dict(action or {})
    certifying = action.get("action") in {"certify_release", "sign_duplicate_inspection", "issue_crs"}
    return _result("agent_certification_guardrails", table=f"{PBC_KEY}_compliance_release", allowed=not certifying, blocked=certifying, reason="human_certifier_required" if certifying else "assistant_action_limited_to_draft_or_evidence")


def link_reliability_to_planning(finding: Mapping[str, object]) -> dict:
    finding = dict(finding or {})
    actions = []
    if int(finding.get("repeat_count", 0)) >= 3:
        actions.append("raise_repeat_defect_threshold_review")
    if finding.get("ata"):
        actions.append("targeted_inspection_campaign")
    if finding.get("component_family"):
        actions.append("component_strategy_review")
    return _result("reliability_to_planning_feedback", table=f"{PBC_KEY}_maintenance_visit", finding_id=finding.get("finding_id"), planning_actions=tuple(actions))


def build_configuration_drift_dashboard(fleet: Sequence[Mapping[str, object]]) -> dict:
    fleet = tuple(dict(item) for item in fleet)
    baseline = next((item.get("baseline") for item in fleet if item.get("baseline")), None)
    drift = tuple(item for item in fleet if baseline and item.get("configuration") != baseline)
    return _result("fleet_configuration_drift_dashboard", table=f"{PBC_KEY}_aircraft", baseline=baseline, drifted_tails=drift, exposure_count=len(drift))


def build_redelivery_readiness_package(aircraft: Mapping[str, object], records: Mapping[str, object]) -> dict:
    records = dict(records or {})
    required = ("configuration_history", "major_maintenance", "ad_status", "llp_traceability", "repair_status", "open_defects")
    gaps = tuple(item for item in required if not records.get(item))
    return _result("lease_return_redelivery_readiness", table=f"{PBC_KEY}_compliance_release", tail_number=dict(aircraft or {}).get("tail_number"), gap_list=gaps, ready=not gaps)


def manage_structural_corrosion_campaign(campaign: Mapping[str, object], findings: Sequence[Mapping[str, object]]) -> dict:
    findings = tuple(dict(item) for item in findings)
    carry_forward = tuple(item for item in findings if item.get("follow_up_required") or item.get("status") not in {"closed", "accepted"})
    return _result("structural_corrosion_campaign_management", table=f"{PBC_KEY}_maintenance_visit", campaign_id=dict(campaign or {}).get("campaign_id"), carry_forward_items=carry_forward, next_visit_required=bool(carry_forward))


def run_pre_close_release_gate(checks: Mapping[str, object]) -> dict:
    checks = dict(checks or {})
    categories = ("open_work_cards", "outstanding_defects", "overdue_inspections", "missing_tool_returns", "part_traceability_issues", "invalid_signoff_authority")
    failures = tuple(category for category in categories if checks.get(category))
    return _result("pre_close_release_gate", table=f"{PBC_KEY}_compliance_release", failures=failures, release_blocked=bool(failures), checklist={category: not bool(checks.get(category)) for category in categories})


def build_continuous_airworthiness_dashboard(inputs: Mapping[str, object]) -> dict:
    inputs = dict(inputs or {})
    indicators = {
        "ad_compliance_risk": int(inputs.get("open_ad_count", 0)),
        "deferred_defect_exposure": int(inputs.get("open_deferred_defects", 0)),
        "repeat_defect_pressure": int(inputs.get("repeat_defects", 0)),
        "visit_release_confidence": float(inputs.get("release_confidence", 0.0)),
        "tooling_material_readiness": float(inputs.get("readiness", 0.0)),
        "certifier_capacity": int(inputs.get("available_certifiers", 0)),
    }
    high_risk = indicators["ad_compliance_risk"] > 0 or indicators["deferred_defect_exposure"] > 5 or indicators["visit_release_confidence"] < 0.8
    return _result("continuous_airworthiness_dashboard", table=f"{PBC_KEY}_aircraft", indicators=indicators, posture="watch" if high_risk else "controlled", exportable_summary=True)


def improve1_mro_control_contract() -> dict:
    return _result(
        "improve1_mro_control_contract",
        table=f"{PBC_KEY}_compliance_release",
        capability_count=len(MRO_CONTROL_CAPABILITIES),
        capabilities=MRO_CONTROL_CAPABILITIES,
        owned_tables=(
            f"{PBC_KEY}_aircraft",
            f"{PBC_KEY}_component",
            f"{PBC_KEY}_work_card",
            f"{PBC_KEY}_maintenance_visit",
            f"{PBC_KEY}_airworthiness_directive",
            f"{PBC_KEY}_deferred_defect",
            f"{PBC_KEY}_compliance_release",
        ),
        ui_surfaces=tuple(f"{PBC_KEY}.ui.mro_control.{capability}" for capability in MRO_CONTROL_CAPABILITIES),
        service_surfaces=tuple(f"{PBC_KEY}.service.mro_control.{capability}" for capability in MRO_CONTROL_CAPABILITIES),
    )
