"""Executable standalone app surface for defense_readiness_logistics."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256

from .events import build_event_envelope
from .models import BUSINESS_TABLES, OWNED_TABLES

PBC_KEY = "defense_readiness_logistics"
OWNED_TABLES = OWNED_TABLES
WORKBENCH_ROUTE = f"/workbench/pbcs/{PBC_KEY}"


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def _copy_state(state: dict) -> dict:
    return deepcopy(state)


def _as_tuple(values) -> tuple:
    if values is None:
        return ()
    if isinstance(values, tuple):
        return values
    if isinstance(values, list):
        return tuple(values)
    return (values,)


def _latest_for_unit(records: dict, unit_code: str) -> dict | None:
    for record in reversed(tuple(records.values())):
        if record.get("unit_code") == unit_code:
            return record
    return None


def empty_defense_state() -> dict:
    return {
        "units": {},
        "assets": {},
        "maintenance": {},
        "supplies": {},
        "deployment_kits": {},
        "deployment_plans": {},
        "movements": {},
        "load_plans": {},
        "inspections": {},
        "qualifications": {},
        "ammunition_lots": {},
        "fuel_allocations": {},
        "custody": {},
        "theater_support": {},
        "exceptions": {},
        "outbox": [],
        "timeline": [],
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "inbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _append_timeline(state: dict, fact_type: str, record: dict) -> None:
    state["timeline"].append(
        {
            "fact_type": fact_type,
            "record_id": record["id"],
            "table": record["table"],
            "when": _utcnow(),
            "status": record.get("status") or record.get("readiness_state") or record.get("movement_state"),
        }
    )


def _emit(state: dict, event_type: str, fact_type: str, aggregate_table: str, aggregate_id: str, payload: dict) -> dict:
    envelope = build_event_envelope(
        event_type,
        payload,
        fact_type=fact_type,
        aggregate_table=aggregate_table,
        aggregate_id=aggregate_id,
    )
    state["outbox"].append(envelope)
    return envelope


def _open_exception(
    state: dict,
    *,
    tenant_id: str,
    exception_type: str,
    source_table: str,
    source_id: str,
    blocker_code: str,
    narrative: str,
    owner_role: str = "operations_controller",
    severity: str = "high",
    blocks_deployment: bool = True,
) -> dict:
    exception_id = f"exc-{_digest((source_table, source_id, blocker_code, narrative))[:10]}"
    now = _utcnow()
    record = {
        "id": exception_id,
        "table": f"{PBC_KEY}_readiness_exception",
        "tenant_id": tenant_id,
        "exception_type": exception_type,
        "exception_state": "open",
        "owner_role": owner_role,
        "severity": severity,
        "blocks_deployment": bool(blocks_deployment),
        "source_table": source_table,
        "source_id": source_id,
        "blocker_code": blocker_code,
        "narrative": narrative,
        "opened_at": now,
        "resolved_at": None,
        "created_at": now,
        "updated_at": now,
    }
    state["exceptions"][exception_id] = record
    _append_timeline(state, "readiness_exception_opened", record)
    _emit(
        state,
        "DefenseReadinessLogisticsExceptionOpened",
        "readiness_exception_opened",
        record["table"],
        record["id"],
        {
            "exception_type": exception_type,
            "source_table": source_table,
            "source_id": source_id,
            "blocker_code": blocker_code,
        },
    )
    return record


def assess_unit_readiness(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    unit_code = payload.get("unit_code") or payload.get("unit_id") or payload.get("unit_name", "unit").lower().replace(" ", "-")
    readiness_id = payload.get("unit_id") or f"unit-{_digest((tenant_id, unit_code, payload.get('mission_set', 'general')))[:10]}"
    mission_set = payload.get("mission_set", "general_deployment")
    personnel = dict(payload.get("personnel", {}))
    supply = dict(payload.get("supply", {}))
    blockers = []
    if int(personnel.get("available", 0)) < int(personnel.get("required", 0)):
        blockers.append("personnel_shortfall")
    if int(personnel.get("certified_roles", 0)) < int(personnel.get("required_certified_roles", 0)):
        blockers.append("certification_shortfall")
    if int(payload.get("serviceable_assets", 0)) < int(payload.get("required_assets", 0)):
        blockers.append("asset_outage")
    if float(supply.get("critical_fill_rate", 0.0)) < float(payload.get("minimum_supply_fill_rate", 0.9)):
        blockers.append("supply_deficit")
    if float(payload.get("ammo_fill_rate", 0.0)) < float(payload.get("minimum_ammo_fill_rate", 0.8)):
        blockers.append("ammo_deficit")
    if float(payload.get("fuel_days", 0.0)) < float(payload.get("required_fuel_days", 1.0)):
        blockers.append("fuel_deficit")
    if not payload.get("inspection_evidence"):
        blockers.append("inspection_evidence_missing")
    if payload.get("classification_marking", "restricted") not in {"unclassified", "restricted", "secret", "top_secret"}:
        blockers.append("classification_marking_invalid")

    commander_approved = bool(payload.get("commander_approved", False))
    readiness_state = "deployment_ready" if commander_approved and not blockers else "validated_ready" if not blockers else "degraded"
    validation_state = "approved" if readiness_state == "deployment_ready" else "validated" if not blockers else "blocked"
    now = _utcnow()
    record = {
        "id": readiness_id,
        "table": f"{PBC_KEY}_unit_readiness",
        "tenant_id": tenant_id,
        "formation_id": payload.get("formation_id"),
        "operation_code": payload.get("operation_code"),
        "unit_code": unit_code,
        "unit_name": payload.get("unit_name", unit_code.upper()),
        "mission_set": mission_set,
        "readiness_state": readiness_state,
        "reported_state": payload.get("reported_state", "reported"),
        "validation_state": validation_state,
        "deployment_authorized": int(readiness_state == "deployment_ready"),
        "commander_approved": int(commander_approved),
        "classification_marking": payload.get("classification_marking", "restricted"),
        "personnel_available": int(personnel.get("available", 0)),
        "personnel_required": int(personnel.get("required", 0)),
        "certified_roles_available": int(personnel.get("certified_roles", 0)),
        "certified_roles_required": int(personnel.get("required_certified_roles", 0)),
        "serviceable_assets": int(payload.get("serviceable_assets", 0)),
        "required_assets": int(payload.get("required_assets", 0)),
        "supply_fill_rate": float(supply.get("critical_fill_rate", 0.0)),
        "minimum_supply_fill_rate": float(payload.get("minimum_supply_fill_rate", 0.9)),
        "ammo_fill_rate": float(payload.get("ammo_fill_rate", 0.0)),
        "minimum_ammo_fill_rate": float(payload.get("minimum_ammo_fill_rate", 0.8)),
        "fuel_days": float(payload.get("fuel_days", 0.0)),
        "required_fuel_days": float(payload.get("required_fuel_days", 1.0)),
        "blocker_codes_json": tuple(dict.fromkeys(blockers)),
        "evidence_pack_id": next(iter(payload.get("inspection_evidence", ())), None),
        "narrative": payload.get("narrative"),
        "assessment_at": now,
        "created_at": now,
        "updated_at": now,
    }
    next_state["units"][record["id"]] = record
    _append_timeline(next_state, "unit_readiness_assessed", record)
    event_type = "DefenseReadinessLogisticsApproved" if readiness_state == "deployment_ready" else "DefenseReadinessLogisticsUpdated"
    _emit(
        next_state,
        event_type,
        "unit_readiness_assessed",
        record["table"],
        record["id"],
        {"unit_code": unit_code, "mission_set": mission_set, "blockers": record["blocker_codes_json"]},
    )
    for blocker in record["blocker_codes_json"]:
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="readiness_blocker",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code=blocker,
            narrative=f"{unit_code} blocked by {blocker}",
            owner_role="commander",
            severity="high",
            blocks_deployment=True,
        )
    return {"ok": not blockers, "state": next_state, "unit_readiness": record, "side_effects": ()}


def record_mission_asset(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    unit_code = payload.get("unit_code") or payload.get("unit_id") or "unit-unknown"
    asset_code = payload.get("asset_code") or payload.get("asset_id") or payload.get("serial") or "asset"
    asset_id = payload.get("asset_id") or f"asset-{_digest((tenant_id, unit_code, asset_code))[:10]}"
    serviceability = payload.get("serviceability", payload.get("serviceability_state", "serviceable"))
    now = _utcnow()
    record = {
        "id": asset_id,
        "table": f"{PBC_KEY}_mission_asset",
        "tenant_id": tenant_id,
        "unit_code": unit_code,
        "asset_code": asset_code,
        "asset_type": payload.get("asset_type", "general_asset"),
        "serial_number": payload.get("serial"),
        "lot_batch": payload.get("lot_or_batch"),
        "serviceability_state": serviceability,
        "acceptance_state": payload.get("acceptance_state", "accepted" if serviceability == "serviceable" else "maintenance_hold"),
        "available_from": payload.get("available_from"),
        "available_to": payload.get("available_to"),
        "location_code": payload.get("location_code"),
        "mission_assignment": payload.get("mission_assignment"),
        "controlled_item": int(bool(payload.get("controlled_item", False))),
        "classification_marking": payload.get("classification_marking", "restricted"),
        "discrepancy_codes_json": tuple(payload.get("discrepancy_codes", ())),
        "created_at": now,
        "updated_at": now,
    }
    next_state["assets"][record["id"]] = record
    _append_timeline(next_state, "mission_asset_recorded", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsCreated",
        "mission_asset_recorded",
        record["table"],
        record["id"],
        {"asset_code": asset_code, "unit_code": unit_code, "serviceability_state": serviceability},
    )
    return {"ok": True, "state": next_state, "mission_asset": record, "side_effects": ()}


def create_readiness_inspection(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    unit_code = payload.get("unit_code") or payload.get("unit_id") or "unit-unknown"
    evidence_items = set(payload.get("evidence_items", ()))
    required_evidence = set(payload.get("required_evidence", ("checklist", "signature")))
    missing = tuple(sorted(required_evidence - evidence_items))
    inspection_id = payload.get("inspection_id") or f"insp-{_digest((tenant_id, unit_code, tuple(sorted(evidence_items))))[:10]}"
    state_name = "accepted" if not missing else "blocked"
    now = _utcnow()
    record = {
        "id": inspection_id,
        "table": f"{PBC_KEY}_readiness_inspection",
        "tenant_id": tenant_id,
        "unit_code": unit_code,
        "inspection_type": payload.get("inspection_type", "pre_deployment"),
        "inspection_state": state_name,
        "checklist_score": float(payload.get("checklist_score", 1.0 if not missing else 0.5)),
        "evidence_pack_id": payload.get("evidence_pack_id") or f"pack-{inspection_id}",
        "inspector_name": payload.get("inspector_name", "duty_officer"),
        "signatures_json": tuple(payload.get("signatures", ())),
        "findings_json": tuple(payload.get("findings", ())),
        "corrective_actions_json": tuple(payload.get("corrective_actions", ())),
        "performed_at": payload.get("performed_at", now),
        "created_at": now,
        "updated_at": now,
    }
    next_state["inspections"][record["id"]] = record
    _append_timeline(next_state, "readiness_inspection_recorded", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated" if not missing else "DefenseReadinessLogisticsExceptionOpened",
        "readiness_inspection_recorded",
        record["table"],
        record["id"],
        {"unit_code": unit_code, "missing_evidence": missing},
    )
    if missing:
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="inspection_gap",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code="inspection_evidence_missing",
            narrative=f"Inspection for {unit_code} missing {', '.join(missing)}",
            owner_role="inspection_team",
        )
    return {"ok": not missing, "state": next_state, "readiness_inspection": record, "side_effects": ()}


def verify_personnel_qualification(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    unit_code = payload.get("unit_code") or payload.get("unit_id") or "unit-unknown"
    role_code = payload.get("role_code", "mission_crew")
    record_id = payload.get("qualification_id") or f"qual-{_digest((tenant_id, unit_code, role_code))[:10]}"
    certified = int(payload.get("certified_count", payload.get("certified_roles", 0)))
    required = int(payload.get("required_count", payload.get("required_roles", 0)))
    available = int(payload.get("available_count", payload.get("available", certified)))
    clearance_required = bool(payload.get("clearance_required", False))
    clearance_gap = int(payload.get("clearance_gap", 1 if clearance_required and not payload.get("clearance_met", True) else 0))
    has_gap = certified < required or available < required or clearance_gap > 0
    now = _utcnow()
    record = {
        "id": record_id,
        "table": f"{PBC_KEY}_personnel_qualification",
        "tenant_id": tenant_id,
        "unit_code": unit_code,
        "role_code": role_code,
        "certified_count": certified,
        "required_count": required,
        "available_count": available,
        "clearance_required": int(clearance_required),
        "clearance_gap": clearance_gap,
        "expiry_window_code": payload.get("expiry_window_code"),
        "created_at": now,
        "updated_at": now,
    }
    next_state["qualifications"][record["id"]] = record
    _append_timeline(next_state, "personnel_qualification_verified", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated" if not has_gap else "DefenseReadinessLogisticsExceptionOpened",
        "personnel_qualification_verified",
        record["table"],
        record["id"],
        {"unit_code": unit_code, "role_code": role_code, "qualification_gap": has_gap},
    )
    if has_gap:
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="qualification_gap",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code="certification_shortfall",
            narrative=f"{unit_code} lacks qualified coverage for role {role_code}",
            owner_role="personnel_controller",
        )
    return {"ok": not has_gap, "state": next_state, "personnel_qualification": record, "side_effects": ()}


def project_maintenance_status(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    asset_code = payload.get("asset_code") or payload.get("asset_id") or "asset-unknown"
    maintenance_id = payload.get("maintenance_id") or f"mx-{_digest((tenant_id, asset_code, payload.get('fault_codes', ())))[:10]}"
    required_parts = tuple(payload.get("required_parts", ()))
    available_parts = set(payload.get("available_parts", ()))
    missing_parts = tuple(part for part in required_parts if part not in available_parts)
    deferred_faults = tuple(payload.get("deferred_faults", ()))
    blockers = []
    if missing_parts:
        blockers.append("repair_parts_unavailable")
    if bool(payload.get("safety_critical", False)) and deferred_faults:
        blockers.append("safety_critical_deferral")
    if not payload.get("projected_return"):
        blockers.append("projected_return_missing")
    state_name = "return_to_service_planned" if not blockers else "maintenance_hold"
    now = _utcnow()
    record = {
        "id": maintenance_id,
        "table": f"{PBC_KEY}_maintenance_status",
        "tenant_id": tenant_id,
        "asset_code": asset_code,
        "maintenance_state": state_name,
        "fault_codes_json": tuple(payload.get("fault_codes", ())),
        "required_parts_json": required_parts,
        "available_parts_json": tuple(sorted(available_parts)),
        "missing_parts_json": missing_parts,
        "deferred_faults_json": deferred_faults,
        "safety_critical": int(bool(payload.get("safety_critical", False))),
        "projected_return_at": payload.get("projected_return"),
        "confidence_score": float(payload.get("confidence", 0.0)),
        "readiness_impact": payload.get("readiness_impact", "unknown"),
        "depot_code": payload.get("depot_code"),
        "technician_gap": int(payload.get("technician_gap", 0)),
        "created_at": now,
        "updated_at": now,
    }
    next_state["maintenance"][record["id"]] = record
    for asset in next_state["assets"].values():
        if asset.get("asset_code") == asset_code or asset.get("id") == asset_code:
            asset["serviceability_state"] = "serviceable" if not blockers and payload.get("restored", False) else "maintenance_hold"
            asset["updated_at"] = now
    _append_timeline(next_state, "maintenance_projected", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated" if not blockers else "DefenseReadinessLogisticsExceptionOpened",
        "maintenance_projected",
        record["table"],
        record["id"],
        {"asset_code": asset_code, "blockers": tuple(blockers)},
    )
    for blocker in blockers:
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="maintenance_blocker",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code=blocker,
            narrative=f"Maintenance forecast for {asset_code} blocked by {blocker}",
            owner_role="maintenance_control",
        )
    return {"ok": not blockers, "state": next_state, "maintenance_status": record, "side_effects": ()}


def score_supply_readiness(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    unit_code = payload.get("unit_code") or payload.get("unit_id") or "unit-unknown"
    request_id = payload.get("request_id") or f"sup-{_digest((tenant_id, unit_code, payload.get('mission_set', 'general')))[:10]}"
    demand = dict(payload.get("demand", {}))
    on_hand = dict(payload.get("on_hand", {}))
    in_transit = dict(payload.get("in_transit", {}))
    substitutes = dict(payload.get("approved_substitutes", {}))
    shortages = {}
    for item, required in demand.items():
        available = float(on_hand.get(item, 0.0)) + float(in_transit.get(item, 0.0)) + float(substitutes.get(item, 0.0))
        if available < float(required):
            shortages[item] = {
                "required": float(required),
                "available": round(available, 4),
                "gap": round(float(required) - available, 4),
            }
    ammo_lot_code = payload.get("ammo_lot_code") or payload.get("ammo_lot")
    if ammo_lot_code and payload.get("ammo_lot_restricted", False):
        shortages[f"ammo_lot:{ammo_lot_code}"] = {"required": 1.0, "available": 0.0, "gap": 1.0}
    fuel_required = float(payload.get("fuel_required", 0.0))
    fuel_available = float(payload.get("fuel_available", 0.0))
    if fuel_available < fuel_required:
        shortages["fuel"] = {"required": fuel_required, "available": fuel_available, "gap": round(fuel_required - fuel_available, 4)}
    denominator = max(1, len(demand) + (1 if fuel_required else 0))
    score = max(0.0, 1.0 - (len(shortages) / denominator))
    now = _utcnow()
    record = {
        "id": request_id,
        "table": f"{PBC_KEY}_supply_request",
        "tenant_id": tenant_id,
        "unit_code": unit_code,
        "mission_set": payload.get("mission_set", "general_deployment"),
        "request_state": "filled" if not shortages else "shortage_mitigation_required",
        "criticality": payload.get("criticality", "mission_essential"),
        "demand_json": demand,
        "on_hand_json": on_hand,
        "in_transit_json": in_transit,
        "approved_substitutes_json": substitutes,
        "shortage_json": shortages,
        "readiness_score": round(score, 4),
        "ammo_lot_code": ammo_lot_code,
        "fuel_required": fuel_required,
        "fuel_available": fuel_available,
        "required_by": payload.get("required_by"),
        "created_at": now,
        "updated_at": now,
    }
    next_state["supplies"][record["id"]] = record
    _append_timeline(next_state, "supply_readiness_scored", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated" if not shortages else "DefenseReadinessLogisticsExceptionOpened",
        "supply_readiness_scored",
        record["table"],
        record["id"],
        {"unit_code": unit_code, "shortage_count": len(shortages), "readiness_score": record["readiness_score"]},
    )
    for blocker in shortages:
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="supply_shortage",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code=str(blocker),
            narrative=f"{unit_code} shortage blocks mission support for {blocker}",
            owner_role="supply_control",
        )
    return {"ok": not shortages, "state": next_state, "supply_readiness": record, "side_effects": ()}


def allocate_fuel_reserve(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    unit_code = payload.get("unit_code") or payload.get("unit_id") or "unit-unknown"
    allocation_id = payload.get("allocation_id") or f"fuel-{_digest((tenant_id, unit_code, payload.get('fuel_type', 'jp8')))[:10]}"
    on_hand = float(payload.get("on_hand_quantity", payload.get("fuel_available", 0.0)))
    required = float(payload.get("required_quantity", payload.get("fuel_required", 0.0)))
    reserve = float(payload.get("contingency_reserve", 0.0))
    sufficiency_state = "sufficient" if on_hand >= required + reserve else "gap"
    now = _utcnow()
    record = {
        "id": allocation_id,
        "table": f"{PBC_KEY}_fuel_allocation",
        "tenant_id": tenant_id,
        "unit_code": unit_code,
        "allocation_code": payload.get("allocation_code", allocation_id),
        "fuel_type": payload.get("fuel_type", "jp8"),
        "on_hand_quantity": on_hand,
        "required_quantity": required,
        "contingency_reserve": reserve,
        "refuel_points_json": tuple(payload.get("refuel_points", ())),
        "sufficiency_state": sufficiency_state,
        "created_at": now,
        "updated_at": now,
    }
    next_state["fuel_allocations"][record["id"]] = record
    _append_timeline(next_state, "fuel_allocation_recorded", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated" if sufficiency_state == "sufficient" else "DefenseReadinessLogisticsExceptionOpened",
        "fuel_allocation_recorded",
        record["table"],
        record["id"],
        {"unit_code": unit_code, "sufficiency_state": sufficiency_state},
    )
    if sufficiency_state != "sufficient":
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="fuel_gap",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code="fuel_plan_gap",
            narrative=f"{unit_code} fuel reserve below requirement",
            owner_role="movement_control",
        )
    return {"ok": sufficiency_state == "sufficient", "state": next_state, "fuel_allocation": record, "side_effects": ()}


def validate_deployment_kit(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    required_items = tuple(payload.get("required_items", ()))
    packed_items = tuple(sorted(set(payload.get("packed_items", ()))))
    missing = tuple(item for item in required_items if item not in packed_items)
    mission_critical = set(payload.get("mission_critical_items", required_items))
    critical_missing = tuple(item for item in missing if item in mission_critical)
    replacement_confirmed = set(payload.get("replacement_confirmed", ()))
    expiration_blockers = tuple(item for item in payload.get("expiration_sensitive_items", ()) if item not in replacement_confirmed)
    kit_id = payload.get("kit_id") or f"kit-{_digest((tenant_id, required_items, packed_items))[:10]}"
    status = "complete" if not missing and not expiration_blockers else "blocked" if critical_missing or expiration_blockers else "partial"
    now = _utcnow()
    record = {
        "id": kit_id,
        "table": f"{PBC_KEY}_deployment_plan",
        "tenant_id": tenant_id,
        "unit_code": payload.get("unit_code") or payload.get("unit_id") or "unit-unknown",
        "deployment_code": payload.get("deployment_code", kit_id),
        "mission_set": payload.get("mission_set", "general_deployment"),
        "release_state": status,
        "kit_id": kit_id,
        "movement_id": None,
        "movement_mode": None,
        "departure_window": None,
        "arrival_window": None,
        "approval_evidence_json": tuple(payload.get("approval_evidence", ())),
        "blocker_codes_json": tuple(dict.fromkeys(critical_missing + expiration_blockers)),
        "evidence_pack_id": payload.get("evidence_pack_id"),
        "required_items": required_items,
        "packed_items": packed_items,
        "missing_items": missing,
        "expiration_blockers": expiration_blockers,
        "completion_percent": 100.0 if not required_items else round(100.0 * (len(required_items) - len(missing)) / len(required_items), 2),
        "created_at": now,
        "updated_at": now,
    }
    next_state["deployment_kits"][record["id"]] = record
    _append_timeline(next_state, "deployment_kit_validated", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated" if status == "complete" else "DefenseReadinessLogisticsExceptionOpened",
        "deployment_kit_validated",
        record["table"],
        record["id"],
        {"deployment_code": record["deployment_code"], "status": status, "blockers": record["blocker_codes_json"]},
    )
    for blocker in record["blocker_codes_json"]:
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="deployment_kit_gap",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code=blocker,
            narrative=f"Deployment kit {kit_id} blocked by {blocker}",
            owner_role="supply_control",
        )
    return {"ok": status == "complete", "state": next_state, "deployment_kit": record, "side_effects": ()}


def validate_movement_load_plan(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    movement_id = payload.get("movement_id") or payload.get("movement_code") or "movement-unknown"
    load_plan_id = payload.get("load_plan_id") or f"load-{_digest((tenant_id, movement_id, payload.get('weight_total', 0.0)))[:10]}"
    invalid_reasons = []
    if float(payload.get("weight_total", 0.0)) > float(payload.get("weight_limit", payload.get("weight_total", 0.0))):
        invalid_reasons.append("weight_limit_exceeded")
    if float(payload.get("cube_total", 0.0)) > float(payload.get("cube_limit", payload.get("cube_total", 0.0))):
        invalid_reasons.append("cube_limit_exceeded")
    if int(payload.get("tie_down_points_available", 0)) < int(payload.get("tie_down_points_required", 0)):
        invalid_reasons.append("tie_down_shortfall")
    if payload.get("hazardous_cargo", False) and not payload.get("segregation_checked", False):
        invalid_reasons.append("hazardous_load_segregation_required")
    state_name = "validated" if not invalid_reasons else "blocked"
    now = _utcnow()
    record = {
        "id": load_plan_id,
        "table": f"{PBC_KEY}_movement_load_plan",
        "tenant_id": tenant_id,
        "movement_id": movement_id,
        "weight_total": float(payload.get("weight_total", 0.0)),
        "cube_total": float(payload.get("cube_total", 0.0)),
        "tie_down_points_required": int(payload.get("tie_down_points_required", 0)),
        "tie_down_points_available": int(payload.get("tie_down_points_available", 0)),
        "segregation_checked": int(bool(payload.get("segregation_checked", False))),
        "hazardous_class_json": tuple(payload.get("hazardous_class", ())),
        "validation_state": state_name,
        "invalid_reasons_json": tuple(invalid_reasons),
        "created_at": now,
        "updated_at": now,
    }
    next_state["load_plans"][record["id"]] = record
    _append_timeline(next_state, "movement_load_plan_validated", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated" if not invalid_reasons else "DefenseReadinessLogisticsExceptionOpened",
        "movement_load_plan_validated",
        record["table"],
        record["id"],
        {"movement_id": movement_id, "invalid_reasons": tuple(invalid_reasons)},
    )
    return {"ok": not invalid_reasons, "state": next_state, "movement_load_plan": record, "side_effects": ()}


def verify_controlled_item_custody(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    custody_id = payload.get("custody_id") or f"custody-{_digest((tenant_id, payload.get('movement_id'), payload.get('custody_item_code')))[:10]}"
    acknowledged = bool(payload.get("acknowledged", payload.get("acknowledged_at")))
    blocker_reason = None if acknowledged else "custody_acknowledgement_missing"
    now = _utcnow()
    record = {
        "id": custody_id,
        "table": f"{PBC_KEY}_controlled_item_custody",
        "tenant_id": tenant_id,
        "movement_id": payload.get("movement_id"),
        "custody_item_code": payload.get("custody_item_code", "controlled-device"),
        "custody_state": "verified" if acknowledged else "blocked",
        "assigned_to": payload.get("assigned_to"),
        "transferred_to": payload.get("transferred_to"),
        "acknowledged_at": payload.get("acknowledged_at", now if acknowledged else None),
        "classification_marking": payload.get("classification_marking", "secret"),
        "blocker_reason": blocker_reason,
        "created_at": now,
        "updated_at": now,
    }
    next_state["custody"][record["id"]] = record
    _append_timeline(next_state, "controlled_item_custody_verified", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated" if acknowledged else "DefenseReadinessLogisticsExceptionOpened",
        "controlled_item_custody_verified",
        record["table"],
        record["id"],
        {"movement_id": record["movement_id"], "custody_state": record["custody_state"]},
    )
    if blocker_reason:
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="custody_gap",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code=blocker_reason,
            narrative="Controlled item custody has not been acknowledged",
            owner_role="movement_control",
        )
    return {"ok": acknowledged, "state": next_state, "controlled_item_custody": record, "side_effects": ()}


def request_theater_support(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    request_id = payload.get("support_request_id") or f"support-{_digest((tenant_id, payload.get('operation_code'), payload.get('support_type')))[:10]}"
    support_state = payload.get("support_state", "firm" if payload.get("firm_commitment", False) else "assumed")
    now = _utcnow()
    record = {
        "id": request_id,
        "table": f"{PBC_KEY}_theater_support_request",
        "tenant_id": tenant_id,
        "operation_code": payload.get("operation_code", "operation-unknown"),
        "support_type": payload.get("support_type", "prepositioned_stock"),
        "support_state": support_state,
        "provider_name": payload.get("provider_name"),
        "support_scope": payload.get("support_scope", "mission_support"),
        "firm_commitment": int(bool(payload.get("firm_commitment", False))),
        "assumption_notes": payload.get("assumption_notes"),
        "evidence_ref": payload.get("evidence_ref"),
        "created_at": now,
        "updated_at": now,
    }
    next_state["theater_support"][record["id"]] = record
    _append_timeline(next_state, "theater_support_recorded", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated",
        "theater_support_recorded",
        record["table"],
        record["id"],
        {"operation_code": record["operation_code"], "support_state": support_state},
    )
    return {"ok": True, "state": next_state, "theater_support_request": record, "side_effects": ()}


def triage_readiness_exception(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    exception_id = payload.get("exception_id") or f"exc-{_digest((tenant_id, payload.get('source_table'), payload.get('blocker_code')))[:10]}"
    existing = dict(next_state["exceptions"].get(exception_id, {}))
    now = _utcnow()
    record = {
        "id": exception_id,
        "table": f"{PBC_KEY}_readiness_exception",
        "tenant_id": tenant_id,
        "exception_type": payload.get("exception_type", existing.get("exception_type", "manual_triage")),
        "exception_state": payload.get("exception_state", existing.get("exception_state", "open")),
        "owner_role": payload.get("owner_role", existing.get("owner_role", "operations_controller")),
        "severity": payload.get("severity", existing.get("severity", "medium")),
        "blocks_deployment": int(bool(payload.get("blocks_deployment", existing.get("blocks_deployment", False)))),
        "source_table": payload.get("source_table", existing.get("source_table", f"{PBC_KEY}_unit_readiness")),
        "source_id": payload.get("source_id", existing.get("source_id", "unknown")),
        "blocker_code": payload.get("blocker_code", existing.get("blocker_code", "manual_exception")),
        "narrative": payload.get("narrative", existing.get("narrative")),
        "opened_at": existing.get("opened_at", now),
        "resolved_at": now if payload.get("exception_state") == "resolved" else existing.get("resolved_at"),
        "created_at": existing.get("created_at", now),
        "updated_at": now,
    }
    next_state["exceptions"][record["id"]] = record
    _append_timeline(next_state, "readiness_exception_triaged", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsUpdated",
        "readiness_exception_triaged",
        record["table"],
        record["id"],
        {"exception_state": record["exception_state"], "owner_role": record["owner_role"]},
    )
    return {"ok": True, "state": next_state, "readiness_exception": record, "side_effects": ()}


def plan_logistics_movement(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    movement_id = payload.get("movement_id") or f"move-{_digest((tenant_id, payload.get('deployment_id'), payload.get('mode')))[:10]}"
    mode = payload.get("mode", payload.get("movement_mode", "convoy"))
    load_plan_id = payload.get("load_plan_id")
    custody_id = payload.get("custody_id")
    blockers = []
    if mode == "convoy" and not payload.get("route_reviewed", False):
        blockers.append("route_review_required")
    if mode == "airlift" and float(payload.get("weight_total", payload.get("weight", 0.0))) > float(payload.get("aircraft_weight_limit", 0.0)):
        blockers.append("aircraft_weight_limit_exceeded")
    if mode == "sealift" and payload.get("hazardous_cargo", False) and not payload.get("dangerous_goods_documents", False):
        blockers.append("dangerous_goods_documents_missing")
    if payload.get("fuel_required", 0.0) and float(payload.get("fuel_available", 0.0)) < float(payload.get("fuel_required", 0.0)):
        blockers.append("fuel_plan_gap")
    if payload.get("controlled_items") and not payload.get("custody_chain_verified", False):
        blockers.append("controlled_item_custody_missing")
    if load_plan_id:
        load_plan = next_state["load_plans"].get(load_plan_id)
        if not load_plan or load_plan.get("validation_state") != "validated":
            blockers.append("movement_load_plan_invalid")
    if custody_id:
        custody = next_state["custody"].get(custody_id)
        if not custody or custody.get("custody_state") != "verified":
            blockers.append("controlled_item_custody_missing")
    asset_ids = tuple(payload.get("asset_ids", ()))
    for existing in next_state["movements"].values():
        if existing.get("window_code") == payload.get("window") and set(existing.get("asset_ids_json", ())) & set(asset_ids):
            blockers.append("asset_double_booked")
            break
    movement_state = "released" if payload.get("commander_approved", False) and not blockers else "route_reviewed" if not blockers else "blocked"
    now = _utcnow()
    record = {
        "id": movement_id,
        "table": f"{PBC_KEY}_logistics_movement",
        "tenant_id": tenant_id,
        "deployment_code": payload.get("deployment_id") or payload.get("deployment_code"),
        "movement_state": movement_state,
        "movement_mode": mode,
        "route_code": payload.get("route") or payload.get("route_code"),
        "route_reviewed": int(bool(payload.get("route_reviewed", False))),
        "force_protection_reviewed": int(bool(payload.get("force_protection_reviewed", False))),
        "lift_confirmed": int(bool(payload.get("lift_confirmed", mode != "convoy"))),
        "fuel_required": float(payload.get("fuel_required", 0.0)),
        "fuel_available": float(payload.get("fuel_available", 0.0)),
        "hazardous_cargo": int(bool(payload.get("hazardous_cargo", False))),
        "dangerous_goods_documents": int(bool(payload.get("dangerous_goods_documents", False))),
        "custody_chain_verified": int(bool(payload.get("custody_chain_verified", False))),
        "load_plan_id": load_plan_id,
        "window_code": payload.get("window"),
        "asset_ids_json": asset_ids,
        "blocker_codes_json": tuple(dict.fromkeys(blockers)),
        "released_at": now if movement_state == "released" else None,
        "created_at": now,
        "updated_at": now,
    }
    next_state["movements"][record["id"]] = record
    _append_timeline(next_state, "logistics_movement_planned", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsApproved" if movement_state == "released" else "DefenseReadinessLogisticsUpdated" if not blockers else "DefenseReadinessLogisticsExceptionOpened",
        "logistics_movement_planned",
        record["table"],
        record["id"],
        {"deployment_code": record["deployment_code"], "movement_mode": mode, "blockers": record["blocker_codes_json"]},
    )
    for blocker in record["blocker_codes_json"]:
        _open_exception(
            next_state,
            tenant_id=tenant_id,
            exception_type="movement_blocker",
            source_table=record["table"],
            source_id=record["id"],
            blocker_code=blocker,
            narrative=f"Movement {movement_id} blocked by {blocker}",
            owner_role="movement_control",
        )
    return {"ok": not blockers, "state": next_state, "logistics_movement": record, "side_effects": ()}


def build_mission_capability(state: dict, payload: dict) -> dict:
    unit_code = payload.get("unit_code") or payload.get("unit_id")
    mission_set = payload.get("mission_set", "general_deployment")
    unit = next((item for item in state.get("units", {}).values() if item.get("unit_code") == unit_code), None)
    supply = _latest_for_unit(state.get("supplies", {}), unit_code) if unit_code else None
    fuel = _latest_for_unit(state.get("fuel_allocations", {}), unit_code) if unit_code else None
    inspection = next((item for item in reversed(tuple(state.get("inspections", {}).values())) if item.get("unit_code") == unit_code), None)
    assets = tuple(asset for asset in state.get("assets", {}).values() if asset.get("unit_code") == unit_code)
    blockers = []
    if not unit:
        blockers.append("unit_readiness_missing")
    else:
        blockers.extend(unit.get("blocker_codes_json", ()))
        if unit.get("readiness_state") != "deployment_ready":
            blockers.append("unit_not_deployment_ready")
    if not any(asset.get("serviceability_state") == "serviceable" for asset in assets):
        blockers.append("serviceable_asset_missing")
    if not inspection and not (unit and unit.get("evidence_pack_id")):
        blockers.append("inspection_not_cleared")
    if inspection and inspection.get("inspection_state") != "accepted":
        blockers.append("inspection_not_cleared")
    if supply and supply.get("request_state") != "filled":
        blockers.append("supply_shortfall")
    if fuel and fuel.get("sufficiency_state") != "sufficient":
        blockers.append("fuel_shortfall")
    deduped = tuple(dict.fromkeys(blockers))
    rating = "capable" if not deduped else "partially_capable" if unit and len(deduped) <= 2 else "not_capable"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "unit_code": unit_code,
        "mission_set": mission_set,
        "rating": rating,
        "blockers": deduped,
        "source_records": {
            "unit_readiness": unit.get("id") if unit else None,
            "inspection": inspection.get("id") if inspection else None,
            "mission_assets": tuple(asset["id"] for asset in assets),
            "supply_request": supply.get("id") if supply else None,
            "fuel_allocation": fuel.get("id") if fuel else None,
        },
        "side_effects": (),
    }


def run_readiness_validation_workflow(state: dict, payload: dict) -> dict:
    qualification = verify_personnel_qualification(state, payload.get("qualification", {}))
    inspection = create_readiness_inspection(qualification["state"], payload.get("inspection", {}))
    readiness_payload = dict(payload.get("readiness", {}))
    if inspection["ok"] and not readiness_payload.get("inspection_evidence"):
        readiness_payload["inspection_evidence"] = (inspection["readiness_inspection"]["evidence_pack_id"],)
    readiness = assess_unit_readiness(inspection["state"], readiness_payload)
    workflow = {
        "workflow_id": "readiness_validation_workflow",
        "steps": ("verify_personnel_qualification", "create_readiness_inspection", "assess_unit_readiness"),
        "qualification_ok": qualification["ok"],
        "inspection_ok": inspection["ok"],
        "readiness_ok": readiness["ok"],
    }
    return {"ok": all((qualification["ok"], inspection["ok"], readiness["ok"])), "state": readiness["state"], "workflow": workflow, "unit_readiness": readiness["unit_readiness"], "side_effects": ()}


def run_movement_release_workflow(state: dict, payload: dict) -> dict:
    load_plan = validate_movement_load_plan(state, payload.get("load_plan", {}))
    custody = verify_controlled_item_custody(load_plan["state"], payload.get("custody", {}))
    movement_payload = dict(payload.get("movement", {}))
    if load_plan["ok"]:
        movement_payload.setdefault("load_plan_id", load_plan["movement_load_plan"]["id"])
    if custody["ok"]:
        movement_payload.setdefault("custody_id", custody["controlled_item_custody"]["id"])
        movement_payload.setdefault("custody_chain_verified", True)
    movement = plan_logistics_movement(custody["state"], movement_payload)
    workflow = {
        "workflow_id": "movement_release_workflow",
        "steps": ("validate_movement_load_plan", "verify_controlled_item_custody", "plan_logistics_movement"),
        "load_plan_ok": load_plan["ok"],
        "custody_ok": custody["ok"],
        "movement_ok": movement["ok"],
    }
    return {"ok": all((load_plan["ok"], custody["ok"], movement["ok"])), "state": movement["state"], "workflow": workflow, "logistics_movement": movement["logistics_movement"], "side_effects": ()}


def release_deployment_plan(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    tenant_id = payload.get("tenant_id", "tenant-default")
    unit_code = payload.get("unit_code") or payload.get("unit_id")
    deployment_id = payload.get("deployment_id") or payload.get("deployment_code") or f"dep-{_digest((tenant_id, unit_code, payload.get('kit_id'), payload.get('movement_id')))[:10]}"
    movement_id = payload.get("movement_id")
    kit_id = payload.get("kit_id")
    unit = next((item for item in next_state["units"].values() if item.get("unit_code") == unit_code), None)
    kit = next_state["deployment_kits"].get(kit_id) if kit_id else None
    movement = next_state["movements"].get(movement_id) if movement_id else None
    supply = _latest_for_unit(next_state["supplies"], unit_code) if unit_code else None
    fuel = _latest_for_unit(next_state["fuel_allocations"], unit_code) if unit_code else None
    blockers = []
    if not unit or unit.get("readiness_state") != "deployment_ready":
        blockers.append("unit_not_deployment_ready")
    if not kit or kit.get("release_state") != "complete":
        blockers.append("deployment_kit_not_complete")
    if not movement or movement.get("movement_state") != "released":
        blockers.append("movement_not_released")
    if supply and supply.get("request_state") != "filled":
        blockers.append("supply_not_cleared")
    if fuel and fuel.get("sufficiency_state") != "sufficient":
        blockers.append("fuel_not_cleared")
    if any(exc.get("blocks_deployment") and exc.get("exception_state") == "open" for exc in next_state["exceptions"].values() if exc.get("source_id") in {movement_id, kit_id, unit.get("id") if unit else None}):
        blockers.append("open_blocking_exception")
    now = _utcnow()
    record = {
        "id": deployment_id,
        "table": f"{PBC_KEY}_deployment_plan",
        "tenant_id": tenant_id,
        "unit_code": unit_code or "unit-unknown",
        "deployment_code": deployment_id,
        "mission_set": payload.get("mission_set", unit.get("mission_set") if unit else "general_deployment"),
        "release_state": "released" if not blockers else "blocked",
        "kit_id": kit_id,
        "movement_id": movement_id,
        "movement_mode": movement.get("movement_mode") if movement else None,
        "departure_window": payload.get("departure_window", movement.get("window_code") if movement else None),
        "arrival_window": payload.get("arrival_window"),
        "approval_evidence_json": tuple(payload.get("approval_evidence", ())),
        "blocker_codes_json": tuple(dict.fromkeys(blockers)),
        "evidence_pack_id": payload.get("evidence_pack_id") or f"release-pack-{deployment_id}",
        "created_at": now,
        "updated_at": now,
    }
    next_state["deployment_plans"][record["id"]] = record
    _append_timeline(next_state, "deployment_plan_released", record)
    _emit(
        next_state,
        "DefenseReadinessLogisticsApproved" if not blockers else "DefenseReadinessLogisticsExceptionOpened",
        "deployment_plan_released",
        record["table"],
        record["id"],
        {"deployment_code": deployment_id, "blockers": record["blocker_codes_json"]},
    )
    return {"ok": not blockers, "state": next_state, "deployment_plan": record, "side_effects": ()}


def build_defense_workbench(state: dict) -> dict:
    units = tuple(state.get("units", {}).values())
    maintenance = tuple(state.get("maintenance", {}).values())
    supplies = tuple(state.get("supplies", {}).values())
    movements = tuple(state.get("movements", {}).values())
    exceptions = tuple(exc for exc in state.get("exceptions", {}).values() if exc.get("exception_state") == "open")
    queues = {
        "commander_readiness_board": tuple(unit for unit in units if unit.get("readiness_state") != "deployment_ready"),
        "maintenance_control": tuple(item for item in maintenance if item.get("maintenance_state") != "return_to_service_planned"),
        "supply_readiness": tuple(item for item in supplies if item.get("request_state") != "filled"),
        "movement_control": tuple(item for item in movements if item.get("movement_state") != "released"),
        "classified_export_review": tuple(
            record
            for record in units + tuple(state.get("assets", {}).values()) + tuple(state.get("custody", {}).values())
            if record.get("classification_marking") in {"secret", "top_secret"}
        ),
        "exception_backlog": exceptions,
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": WORKBENCH_ROUTE,
        "queues": queues,
        "queue_counts": {key: len(value) for key, value in queues.items()},
        "owned_tables": BUSINESS_TABLES,
        "side_effects": (),
    }


def workflow_contracts() -> dict:
    workflows = (
        {
            "workflow_id": "readiness_validation_workflow",
            "steps": ("verify_personnel_qualification", "create_readiness_inspection", "assess_unit_readiness"),
            "writes_tables": (
                f"{PBC_KEY}_personnel_qualification",
                f"{PBC_KEY}_readiness_inspection",
                f"{PBC_KEY}_unit_readiness",
            ),
        },
        {
            "workflow_id": "movement_release_workflow",
            "steps": ("validate_movement_load_plan", "verify_controlled_item_custody", "plan_logistics_movement"),
            "writes_tables": (
                f"{PBC_KEY}_movement_load_plan",
                f"{PBC_KEY}_controlled_item_custody",
                f"{PBC_KEY}_logistics_movement",
            ),
        },
        {
            "workflow_id": "deployment_release_workflow",
            "steps": ("score_supply_readiness", "allocate_fuel_reserve", "validate_deployment_kit", "release_deployment_plan"),
            "writes_tables": (
                f"{PBC_KEY}_supply_request",
                f"{PBC_KEY}_fuel_allocation",
                f"{PBC_KEY}_deployment_plan",
            ),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "workflows": workflows, "side_effects": ()}


def forms_contract() -> dict:
    forms = (
        {
            "form_id": "unit_readiness_assessment_form",
            "writes_table": f"{PBC_KEY}_unit_readiness",
            "command": "assess_unit_readiness",
            "field_groups": ("unit_identity", "personnel", "assets", "supply", "ammo", "fuel", "inspection"),
        },
        {
            "form_id": "mission_asset_availability_form",
            "writes_table": f"{PBC_KEY}_mission_asset",
            "command": "record_mission_asset",
            "field_groups": ("identity", "serviceability", "traceability", "availability_window"),
        },
        {
            "form_id": "maintenance_projection_form",
            "writes_table": f"{PBC_KEY}_maintenance_status",
            "command": "project_maintenance_status",
            "field_groups": ("faults", "parts", "projection", "deferred_risk"),
        },
        {
            "form_id": "supply_readiness_form",
            "writes_table": f"{PBC_KEY}_supply_request",
            "command": "score_supply_readiness",
            "field_groups": ("demand", "stock", "substitutes", "fuel_and_ammo"),
        },
        {
            "form_id": "deployment_kit_form",
            "writes_table": f"{PBC_KEY}_deployment_plan",
            "command": "validate_deployment_kit",
            "field_groups": ("kit_manifest", "mission_critical_items", "expiration_controls"),
        },
        {
            "form_id": "movement_order_form",
            "writes_table": f"{PBC_KEY}_logistics_movement",
            "command": "plan_logistics_movement",
            "field_groups": ("mode", "route", "load", "dangerous_goods", "fuel"),
        },
        {
            "form_id": "deployment_release_form",
            "writes_table": f"{PBC_KEY}_deployment_plan",
            "command": "release_deployment_plan",
            "field_groups": ("readiness", "kit", "movement", "release_evidence"),
        },
        {
            "form_id": "controlled_item_custody_form",
            "writes_table": f"{PBC_KEY}_controlled_item_custody",
            "command": "verify_controlled_item_custody",
            "field_groups": ("item_identity", "custody_chain", "acknowledgement", "classification"),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def wizards_contract() -> dict:
    wizards = (
        {"wizard_id": "readiness_validation_wizard", "steps": ("capture_personnel_gaps", "capture_inspection_evidence", "assess_readiness", "commander_review")},
        {"wizard_id": "mission_capability_wizard", "steps": ("select_unit", "roll_up_assets_supply_fuel", "explain_blockers", "open_exceptions")},
        {"wizard_id": "deployment_release_wizard", "steps": ("score_supply", "allocate_fuel", "validate_kit", "release_or_hold")},
        {"wizard_id": "maintenance_recovery_wizard", "steps": ("project_return_to_service", "confirm_parts", "review_deferred_faults", "return_asset")},
        {"wizard_id": "movement_order_wizard", "steps": ("select_mode", "validate_load", "verify_custody", "release_movement")},
        {"wizard_id": "single_pbc_launch_wizard", "steps": ("configure_database", "load_seed_data", "open_workbench", "invite_roles")},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def controls_contract() -> dict:
    controls = (
        {"control_id": "personnel_certification_gate", "blocks_on_failure": True, "table_scope": (f"{PBC_KEY}_personnel_qualification", f"{PBC_KEY}_unit_readiness")},
        {"control_id": "inspection_evidence_pack_gate", "blocks_on_failure": True, "table_scope": (f"{PBC_KEY}_readiness_inspection", f"{PBC_KEY}_unit_readiness")},
        {"control_id": "maintenance_serviceability_gate", "blocks_on_failure": True, "table_scope": (f"{PBC_KEY}_maintenance_status", f"{PBC_KEY}_mission_asset")},
        {"control_id": "supply_ammo_fuel_gate", "blocks_on_failure": True, "table_scope": (f"{PBC_KEY}_supply_request", f"{PBC_KEY}_fuel_allocation", f"{PBC_KEY}_deployment_plan")},
        {"control_id": "deployment_kit_completeness_gate", "blocks_on_failure": True, "table_scope": (f"{PBC_KEY}_deployment_plan",)},
        {"control_id": "movement_load_route_gate", "blocks_on_failure": True, "table_scope": (f"{PBC_KEY}_movement_load_plan", f"{PBC_KEY}_logistics_movement")},
        {"control_id": "controlled_item_custody_gate", "blocks_on_failure": True, "table_scope": (f"{PBC_KEY}_controlled_item_custody", f"{PBC_KEY}_logistics_movement")},
        {"control_id": "classification_redaction_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
        "owned_tables": OWNED_TABLES,
        "workbench_route": WORKBENCH_ROUTE,
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "workflows": workflow_contracts()["workflows"],
        "assistant_panel": "DefenseReadinessLogisticsAssistantPanel",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_mutation_plan(document: str, instruction: str) -> dict:
    text = f"{document} {instruction}".lower()
    ambiguity_flags = []
    citations = []
    if "movement" in text or "convoy" in text or "airlift" in text or "sealift" in text:
        operation = "plan_logistics_movement"
        workflow_id = "movement_release_workflow"
        table = f"{PBC_KEY}_logistics_movement"
        skill_name = f"{PBC_KEY}_extract_movement_order"
        citations = ("movement_message", "route_fragment", "cargo_fragment")
    elif "maintenance" in text or "fault" in text or "serviceability" in text:
        operation = "project_maintenance_status"
        workflow_id = "readiness_validation_workflow"
        table = f"{PBC_KEY}_maintenance_status"
        skill_name = f"{PBC_KEY}_summarize_maintenance_narrative"
        citations = ("maintenance_narrative", "parts_evidence")
    elif "shortage" in text or "supply" in text or "fuel" in text or "ammo" in text:
        operation = "score_supply_readiness"
        workflow_id = "deployment_release_workflow"
        table = f"{PBC_KEY}_supply_request"
        skill_name = f"{PBC_KEY}_propose_shortage_mitigation"
        citations = ("stock_snapshot", "policy_rule", "transit_status")
    elif "inspection" in text or "evidence pack" in text or "checklist" in text:
        operation = "create_readiness_inspection"
        workflow_id = "readiness_validation_workflow"
        table = f"{PBC_KEY}_readiness_inspection"
        skill_name = f"{PBC_KEY}_capture_inspection_evidence"
        citations = ("inspection_checklist", "signatures")
    else:
        operation = "assess_unit_readiness"
        workflow_id = "readiness_validation_workflow"
        table = f"{PBC_KEY}_unit_readiness"
        skill_name = f"{PBC_KEY}_explain_readiness_posture"
        citations = ("readiness_report", "supporting_evidence")
        if "ready" not in text and "readiness" not in text:
            ambiguity_flags.append("domain_intent_inferred")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instruction_digest": _digest(instruction),
        "proposed_operation": operation,
        "workflow_id": workflow_id,
        "target_table": table,
        "skill_name": skill_name,
        "preview_only": True,
        "requires_human_confirmation": True,
        "requires_citations": True,
        "citation_requirements": citations,
        "ambiguity_flags": tuple(ambiguity_flags),
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def defense_app_smoke_test() -> dict:
    state = empty_defense_state()
    readiness = run_readiness_validation_workflow(
        state,
        {
            "qualification": {
                "tenant_id": "tenant-smoke",
                "unit_code": "alpha-1",
                "role_code": "crew-chief",
                "certified_count": 8,
                "required_count": 6,
                "available_count": 8,
            },
            "inspection": {
                "tenant_id": "tenant-smoke",
                "unit_code": "alpha-1",
                "inspection_type": "pre_deployment",
                "evidence_items": ("checklist", "signature", "photo"),
                "signatures": ("cmdr", "inspector"),
            },
            "readiness": {
                "tenant_id": "tenant-smoke",
                "unit_id": "unit-alpha-1",
                "unit_code": "alpha-1",
                "unit_name": "Alpha 1",
                "mission_set": "theater_entry",
                "personnel": {"available": 42, "required": 40, "certified_roles": 9, "required_certified_roles": 8},
                "serviceable_assets": 8,
                "required_assets": 6,
                "supply": {"critical_fill_rate": 0.97},
                "ammo_fill_rate": 0.92,
                "fuel_days": 4,
                "required_fuel_days": 3,
                "commander_approved": True,
                "classification_marking": "restricted",
            },
        },
    )
    asset = record_mission_asset(
        readiness["state"],
        {
            "tenant_id": "tenant-smoke",
            "asset_id": "veh-1",
            "unit_code": "alpha-1",
            "asset_code": "veh-1",
            "asset_type": "vehicle",
            "serial": "VH-001",
            "serviceability": "serviceable",
        },
    )
    maintenance = project_maintenance_status(
        asset["state"],
        {
            "tenant_id": "tenant-smoke",
            "asset_code": "veh-1",
            "fault_codes": ("pmcs",),
            "required_parts": ("filter",),
            "available_parts": ("filter",),
            "projected_return": "D+0",
            "confidence": 0.92,
            "restored": True,
        },
    )
    supply = score_supply_readiness(
        maintenance["state"],
        {
            "tenant_id": "tenant-smoke",
            "unit_code": "alpha-1",
            "mission_set": "theater_entry",
            "demand": {"class_ix": 10, "medical": 4},
            "on_hand": {"class_ix": 10, "medical": 4},
            "fuel_required": 100,
            "fuel_available": 120,
        },
    )
    fuel = allocate_fuel_reserve(
        supply["state"],
        {
            "tenant_id": "tenant-smoke",
            "unit_code": "alpha-1",
            "fuel_required": 100,
            "fuel_available": 140,
            "contingency_reserve": 20,
        },
    )
    kit = validate_deployment_kit(
        fuel["state"],
        {
            "tenant_id": "tenant-smoke",
            "unit_code": "alpha-1",
            "kit_id": "kit-alpha-1",
            "required_items": ("medical", "comms", "tools"),
            "packed_items": ("medical", "comms", "tools"),
            "mission_critical_items": ("medical", "comms"),
        },
    )
    movement = run_movement_release_workflow(
        kit["state"],
        {
            "load_plan": {
                "tenant_id": "tenant-smoke",
                "movement_id": "move-alpha-1",
                "weight_total": 80,
                "weight_limit": 100,
                "cube_total": 40,
                "cube_limit": 50,
                "tie_down_points_required": 8,
                "tie_down_points_available": 8,
                "segregation_checked": True,
            },
            "custody": {
                "tenant_id": "tenant-smoke",
                "movement_id": "move-alpha-1",
                "custody_item_code": "keymat-1",
                "assigned_to": "ops-chief",
                "acknowledged": True,
            },
            "movement": {
                "tenant_id": "tenant-smoke",
                "movement_id": "move-alpha-1",
                "deployment_id": "dep-alpha-1",
                "mode": "convoy",
                "route_reviewed": True,
                "force_protection_reviewed": True,
                "fuel_required": 80,
                "fuel_available": 100,
                "asset_ids": ("veh-1",),
                "window": "D1",
                "commander_approved": True,
                "controlled_items": True,
            },
        },
    )
    release = release_deployment_plan(
        movement["state"],
        {
            "tenant_id": "tenant-smoke",
            "deployment_id": "dep-alpha-1",
            "unit_code": "alpha-1",
            "kit_id": "kit-alpha-1",
            "movement_id": "move-alpha-1",
            "approval_evidence": ("commander_release", "movement_brief", "evidence_bundle"),
        },
    )
    capability = build_mission_capability(release["state"], {"unit_code": "alpha-1", "mission_set": "theater_entry"})
    workbench = build_defense_workbench(release["state"])
    return {
        "ok": all(
            (
                readiness["ok"],
                asset["ok"],
                maintenance["ok"],
                supply["ok"],
                fuel["ok"],
                kit["ok"],
                movement["ok"],
                release["ok"],
                capability["rating"] == "capable",
                workbench["queue_counts"]["commander_readiness_board"] == 0,
            )
        ),
        "state": release["state"],
        "capability": capability,
        "workbench": workbench,
        "single_pbc_app": single_pbc_app_contract(),
        "side_effects": (),
    }
