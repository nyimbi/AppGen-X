"""Standalone defense readiness logistics app surface."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256

PBC_KEY = "defense_readiness_logistics"
OWNED_TABLES = (
    "defense_readiness_logistics_unit_readiness",
    "defense_readiness_logistics_mission_asset",
    "defense_readiness_logistics_supply_request",
    "defense_readiness_logistics_maintenance_status",
    "defense_readiness_logistics_deployment_plan",
    "defense_readiness_logistics_readiness_inspection",
    "defense_readiness_logistics_logistics_movement",
    "defense_readiness_logistics_personnel_qualification",
    "defense_readiness_logistics_ammunition_lot",
    "defense_readiness_logistics_fuel_allocation",
    "defense_readiness_logistics_movement_load_plan",
    "defense_readiness_logistics_theater_support_request",
    "defense_readiness_logistics_controlled_item_custody",
    "defense_readiness_logistics_readiness_exception",
)


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def empty_defense_state() -> dict:
    return {
        "units": {},
        "assets": {},
        "maintenance": {},
        "supplies": {},
        "deployment_plans": {},
        "movements": {},
        "movement_load_plans": {},
        "inspections": {},
        "personnel_qualifications": {},
        "ammunition_lots": {},
        "fuel_allocations": {},
        "controlled_item_custody": {},
        "theater_support": {},
        "exceptions": {},
        "outbox": [],
    }


def _copy_state(state: dict) -> dict:
    return deepcopy(state)


def _emit(state: dict, event_type: str, payload: dict) -> None:
    state["outbox"].append(
        {
            "event_type": event_type,
            "event_contract": "AppGen-X",
            "topic": "pbc.defense_readiness_logistics.events",
            "payload": dict(payload),
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def assess_unit_readiness(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    unit_id = payload.get("unit_id") or f"unit-{_digest(payload.get('unit_name', 'unit'))[:8]}"
    mission_set = payload.get("mission_set", "general_deployment")
    blockers = []
    personnel = payload.get("personnel", {})
    supply = payload.get("supply", {})
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
    readiness_state = "deployment_ready" if not blockers and payload.get("commander_approved") else "validated_ready" if not blockers else "degraded"
    record = {
        "id": unit_id,
        "table": "defense_readiness_logistics_unit_readiness",
        "unit_name": payload.get("unit_name", unit_id),
        "mission_set": mission_set,
        "reported_status": payload.get("reported_status", "reported"),
        "validated_status": readiness_state,
        "blockers": tuple(blockers),
        "personnel": dict(personnel),
        "supply": dict(supply),
        "ammo_fill_rate": float(payload.get("ammo_fill_rate", 0.0)),
        "fuel_days": float(payload.get("fuel_days", 0.0)),
        "commander_approved": bool(payload.get("commander_approved", False)),
    }
    next_state["units"][unit_id] = record
    event_type = "DefenseReadinessLogisticsApproved" if readiness_state == "deployment_ready" else "DefenseReadinessLogisticsExceptionOpened" if blockers else "DefenseReadinessLogisticsUpdated"
    _emit(next_state, event_type, {"entity": "unit_readiness", "id": unit_id, "state": readiness_state, "blockers": tuple(blockers)})
    return {"ok": True, "state": next_state, "unit_readiness": record, "side_effects": ()}


def record_mission_asset(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    asset_id = payload.get("asset_id") or f"asset-{_digest((payload.get('serial'), payload.get('asset_type')))[:8]}"
    asset = {
        "id": asset_id,
        "table": "defense_readiness_logistics_mission_asset",
        "unit_id": payload.get("unit_id"),
        "asset_type": payload.get("asset_type"),
        "serial": payload.get("serial"),
        "serviceability": payload.get("serviceability", "serviceable"),
        "available_from": payload.get("available_from"),
        "available_to": payload.get("available_to"),
        "controlled_item": bool(payload.get("controlled_item", False)),
        "lot_or_batch": payload.get("lot_or_batch"),
        "mission_commitments": tuple(payload.get("mission_commitments", ())),
    }
    next_state["assets"][asset_id] = asset
    _emit(next_state, "DefenseReadinessLogisticsUpdated", {"entity": "mission_asset", "id": asset_id})
    return {"ok": True, "state": next_state, "mission_asset": asset, "side_effects": ()}


def project_maintenance_status(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    asset_id = payload.get("asset_id")
    maintenance_id = payload.get("maintenance_id") or f"mx-{_digest((asset_id, payload.get('fault_codes')))[:8]}"
    required_parts = tuple(payload.get("required_parts", ()))
    available_parts = set(payload.get("available_parts", ()))
    deferred_faults = tuple(payload.get("deferred_faults", ()))
    blockers = []
    missing_parts = tuple(part for part in required_parts if part not in available_parts)
    if missing_parts:
        blockers.append("repair_parts_unavailable")
    if payload.get("safety_critical") and deferred_faults:
        blockers.append("safety_critical_deferral")
    if payload.get("projected_return") is None:
        blockers.append("projected_return_missing")
    status = "return_to_service_planned" if not blockers else "maintenance_hold"
    record = {
        "id": maintenance_id,
        "table": "defense_readiness_logistics_maintenance_status",
        "asset_id": asset_id,
        "fault_codes": tuple(payload.get("fault_codes", ())),
        "required_parts": required_parts,
        "missing_parts": missing_parts,
        "deferred_faults": deferred_faults,
        "projected_return": payload.get("projected_return"),
        "confidence": float(payload.get("confidence", 0.0)),
        "readiness_impact": payload.get("readiness_impact", "unknown"),
        "status": status,
        "blockers": tuple(blockers),
    }
    next_state["maintenance"][maintenance_id] = record
    if asset_id and asset_id in next_state["assets"]:
        next_state["assets"][asset_id]["serviceability"] = "serviceable" if not blockers and payload.get("restored") else "maintenance_hold"
    _emit(next_state, "DefenseReadinessLogisticsExceptionOpened" if blockers else "DefenseReadinessLogisticsUpdated", {"entity": "maintenance_status", "id": maintenance_id, "blockers": tuple(blockers)})
    return {"ok": not blockers, "state": next_state, "maintenance_status": record, "side_effects": ()}


def score_supply_readiness(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    request_id = payload.get("request_id") or f"sup-{_digest((payload.get('unit_id'), payload.get('mission_set'), payload.get('demand')))[:8]}"
    demand = dict(payload.get("demand", {}))
    on_hand = dict(payload.get("on_hand", {}))
    in_transit = dict(payload.get("in_transit", {}))
    substitutes = dict(payload.get("approved_substitutes", {}))
    shortages = {}
    for item, required in demand.items():
        available = float(on_hand.get(item, 0)) + float(in_transit.get(item, 0)) + float(substitutes.get(item, 0))
        if available < float(required):
            shortages[item] = {"required": float(required), "available": available, "gap": float(required) - available}
    ammo_lot = payload.get("ammo_lot")
    if ammo_lot and payload.get("ammo_lot_restricted"):
        shortages[f"ammo_lot:{ammo_lot}"] = {"required": 1.0, "available": 0.0, "gap": 1.0}
    fuel_required = float(payload.get("fuel_required", 0.0))
    fuel_available = float(payload.get("fuel_available", 0.0))
    if fuel_available < fuel_required:
        shortages["fuel"] = {"required": fuel_required, "available": fuel_available, "gap": fuel_required - fuel_available}
    score = 1.0 if not demand and not shortages else max(0.0, 1.0 - (len(shortages) / max(1, len(demand) + (1 if fuel_required else 0))))
    record = {
        "id": request_id,
        "table": "defense_readiness_logistics_supply_request",
        "unit_id": payload.get("unit_id"),
        "mission_set": payload.get("mission_set"),
        "demand": demand,
        "on_hand": on_hand,
        "in_transit": in_transit,
        "approved_substitutes": substitutes,
        "shortages": shortages,
        "readiness_score": round(score, 4),
        "status": "filled" if not shortages else "shortage_mitigation_required",
    }
    next_state["supplies"][request_id] = record
    _emit(next_state, "DefenseReadinessLogisticsExceptionOpened" if shortages else "DefenseReadinessLogisticsUpdated", {"entity": "supply_request", "id": request_id, "shortages": tuple(shortages)})
    return {"ok": not shortages, "state": next_state, "supply_readiness": record, "side_effects": ()}


def build_mission_capability(state: dict, payload: dict) -> dict:
    unit_id = payload.get("unit_id")
    mission_set = payload.get("mission_set", "general_deployment")
    unit = state.get("units", {}).get(unit_id)
    assets = tuple(asset for asset in state.get("assets", {}).values() if asset.get("unit_id") == unit_id)
    blockers = list(unit.get("blockers", ())) if unit else ["unit_readiness_missing"]
    if not any(asset.get("serviceability") == "serviceable" for asset in assets):
        blockers.append("serviceable_asset_missing")
    rating = "capable" if not blockers else "partially_capable" if unit and "inspection_evidence_missing" not in blockers else "not_capable"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "unit_id": unit_id,
        "mission_set": mission_set,
        "rating": rating,
        "blockers": tuple(dict.fromkeys(blockers)),
        "source_records": {
            "unit_readiness": unit_id if unit else None,
            "mission_assets": tuple(asset["id"] for asset in assets),
        },
        "side_effects": (),
    }


def validate_deployment_kit(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = tuple(payload.get("required_items", ()))
    packed = set(payload.get("packed_items", ()))
    expiring = tuple(item for item in payload.get("expiration_sensitive_items", ()) if item not in payload.get("replacement_confirmed", ()))
    missing = tuple(item for item in required if item not in packed)
    critical_missing = tuple(item for item in missing if item in set(payload.get("mission_critical_items", required)))
    status = "complete" if not missing and not expiring else "blocked" if critical_missing or expiring else "partial"
    kit = {
        "id": payload.get("kit_id", f"kit-{_digest((required, tuple(sorted(packed))))[:8]}"),
        "table": "defense_readiness_logistics_deployment_plan",
        "required_items": required,
        "packed_items": tuple(sorted(packed)),
        "missing_items": missing,
        "expiration_blockers": expiring,
        "completion_percent": 100.0 if not required else round(100.0 * (len(required) - len(missing)) / len(required), 2),
        "status": status,
    }
    next_state["deployment_plans"][kit["id"]] = kit
    _emit(next_state, "DefenseReadinessLogisticsExceptionOpened" if status == "blocked" else "DefenseReadinessLogisticsUpdated", {"entity": "deployment_kit", "id": kit["id"], "status": status})
    return {"ok": status != "blocked", "state": next_state, "deployment_kit": kit, "side_effects": ()}


def plan_logistics_movement(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    movement_id = payload.get("movement_id") or f"move-{_digest((payload.get('deployment_id'), payload.get('mode'), payload.get('route')))[:8]}"
    mode = payload.get("mode", "convoy")
    blockers = []
    if mode == "convoy" and not payload.get("route_reviewed"):
        blockers.append("route_review_required")
    if mode == "airlift" and float(payload.get("weight", 0.0)) > float(payload.get("aircraft_weight_limit", 0.0)):
        blockers.append("aircraft_weight_limit_exceeded")
    if mode == "sealift" and payload.get("hazardous_cargo") and not payload.get("dangerous_goods_documents"):
        blockers.append("dangerous_goods_documents_missing")
    load_plan = dict(payload.get("load_plan", {}))
    if payload.get("hazardous_cargo") and not load_plan.get("segregation_checked"):
        blockers.append("hazardous_load_segregation_required")
    if payload.get("controlled_items") and not payload.get("custody_chain_verified"):
        blockers.append("controlled_item_custody_missing")
    if payload.get("fuel_required", 0) and float(payload.get("fuel_available", 0.0)) < float(payload.get("fuel_required", 0.0)):
        blockers.append("fuel_plan_gap")
    asset_ids = tuple(payload.get("asset_ids", ()))
    for existing in next_state["movements"].values():
        if existing.get("window") == payload.get("window") and set(existing.get("asset_ids", ())) & set(asset_ids):
            blockers.append("asset_double_booked")
            break
    movement = {
        "id": movement_id,
        "table": "defense_readiness_logistics_logistics_movement",
        "deployment_id": payload.get("deployment_id"),
        "mode": mode,
        "route": payload.get("route"),
        "window": payload.get("window"),
        "asset_ids": asset_ids,
        "status": "released" if not blockers and payload.get("commander_approved") else "blocked" if blockers else "route_reviewed",
        "blockers": tuple(dict.fromkeys(blockers)),
    }
    next_state["movements"][movement_id] = movement
    if load_plan:
        next_state["movement_load_plans"][movement_id] = {
            "id": f"load-{movement_id}",
            "table": "defense_readiness_logistics_movement_load_plan",
            "movement_id": movement_id,
            "load_plan": load_plan,
            "validated": not any(blocker.endswith("required") for blocker in blockers),
        }
    _emit(next_state, "DefenseReadinessLogisticsExceptionOpened" if blockers else "DefenseReadinessLogisticsApproved", {"entity": "logistics_movement", "id": movement_id, "blockers": movement["blockers"]})
    return {"ok": not blockers, "state": next_state, "logistics_movement": movement, "side_effects": ()}


def release_deployment_plan(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    deployment_id = payload.get("deployment_id") or f"dep-{_digest(payload)[:8]}"
    unit_id = payload.get("unit_id")
    kit_id = payload.get("kit_id")
    movement_id = payload.get("movement_id")
    unit = next_state["units"].get(unit_id)
    kit = next_state["deployment_plans"].get(kit_id)
    movement = next_state["movements"].get(movement_id)
    blockers = []
    if not unit or unit.get("validated_status") != "deployment_ready":
        blockers.append("unit_not_deployment_ready")
    if not kit or kit.get("status") != "complete":
        blockers.append("deployment_kit_not_complete")
    if not movement or movement.get("status") != "released":
        blockers.append("movement_not_released")
    blocking_exceptions = tuple(item for item in next_state["exceptions"].values() if item.get("blocks_deployment"))
    if blocking_exceptions:
        blockers.append("open_blocking_exception")
    plan = {
        "id": deployment_id,
        "table": "defense_readiness_logistics_deployment_plan",
        "unit_id": unit_id,
        "kit_id": kit_id,
        "movement_id": movement_id,
        "status": "released" if not blockers else "blocked",
        "blockers": tuple(blockers),
        "approval_evidence": tuple(payload.get("approval_evidence", ())),
    }
    next_state["deployment_plans"][deployment_id] = plan
    _emit(next_state, "DefenseReadinessLogisticsApproved" if not blockers else "DefenseReadinessLogisticsExceptionOpened", {"entity": "deployment_plan", "id": deployment_id, "blockers": tuple(blockers)})
    return {"ok": not blockers, "state": next_state, "deployment_plan": plan, "side_effects": ()}


def build_defense_workbench(state: dict) -> dict:
    units = tuple(state.get("units", {}).values())
    movements = tuple(state.get("movements", {}).values())
    assets = tuple(state.get("assets", {}).values())
    queues = {
        "commander_readiness_board": tuple(unit for unit in units if unit["validated_status"] != "deployment_ready"),
        "maintenance_control": tuple(asset for asset in assets if asset.get("serviceability") != "serviceable"),
        "movement_control": tuple(move for move in movements if move["status"] != "released"),
        "classified_export_review": tuple(unit for unit in units if unit.get("classification_marking") in {"secret", "restricted"}),
        "exception_backlog": tuple(item for item in units + movements if item.get("blockers")),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "queues": queues,
        "queue_counts": {key: len(value) for key, value in queues.items()},
        "side_effects": (),
    }


def forms_contract() -> dict:
    forms = (
        {"form_id": "unit_readiness_assessment_form", "writes_table": "defense_readiness_logistics_unit_readiness", "command": "assess_unit_readiness"},
        {"form_id": "mission_asset_availability_form", "writes_table": "defense_readiness_logistics_mission_asset", "command": "record_mission_asset"},
        {"form_id": "maintenance_projection_form", "writes_table": "defense_readiness_logistics_maintenance_status", "command": "project_maintenance_status"},
        {"form_id": "supply_readiness_form", "writes_table": "defense_readiness_logistics_supply_request", "command": "score_supply_readiness"},
        {"form_id": "deployment_kit_form", "writes_table": "defense_readiness_logistics_deployment_plan", "command": "validate_deployment_kit"},
        {"form_id": "movement_order_form", "writes_table": "defense_readiness_logistics_logistics_movement", "command": "plan_logistics_movement"},
        {"form_id": "deployment_release_form", "writes_table": "defense_readiness_logistics_deployment_plan", "command": "release_deployment_plan"},
        {"form_id": "controlled_item_custody_form", "writes_table": "defense_readiness_logistics_controlled_item_custody", "command": "verify_controlled_item_custody"},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def wizards_contract() -> dict:
    wizards = (
        {"wizard_id": "readiness_validation_wizard", "steps": ("report_readiness", "attach_evidence", "calculate_blockers", "commander_review")},
        {"wizard_id": "mission_capability_wizard", "steps": ("select_mission_set", "roll_up_people_assets_supply", "explain_capability", "open_exceptions")},
        {"wizard_id": "deployment_release_wizard", "steps": ("validate_kit", "validate_movement", "check_fuel_ammo", "release_or_hold")},
        {"wizard_id": "maintenance_recovery_wizard", "steps": ("project_return_to_service", "identify_parts", "review_deferrals", "restore_serviceability")},
        {"wizard_id": "movement_order_wizard", "steps": ("select_mode", "validate_load", "review_route", "approve_release")},
        {"wizard_id": "single_pbc_launch_wizard", "steps": ("configure_database", "load_seed_data", "open_workbench", "invite_roles")},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def controls_contract() -> dict:
    controls = (
        {"control_id": "personnel_certification_gate", "blocks_on_failure": True, "table_scope": ("defense_readiness_logistics_unit_readiness",)},
        {"control_id": "mission_asset_availability_gate", "blocks_on_failure": True, "table_scope": ("defense_readiness_logistics_mission_asset",)},
        {"control_id": "maintenance_serviceability_gate", "blocks_on_failure": True, "table_scope": ("defense_readiness_logistics_maintenance_status",)},
        {"control_id": "supply_ammo_fuel_gate", "blocks_on_failure": True, "table_scope": ("defense_readiness_logistics_supply_request", "defense_readiness_logistics_deployment_plan")},
        {"control_id": "deployment_kit_completeness_gate", "blocks_on_failure": True, "table_scope": ("defense_readiness_logistics_deployment_plan",)},
        {"control_id": "movement_load_route_gate", "blocks_on_failure": True, "table_scope": ("defense_readiness_logistics_logistics_movement",)},
        {"control_id": "classification_redaction_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
        {"control_id": "offline_sync_conflict_gate", "blocks_on_failure": True, "table_scope": ("defense_readiness_logistics_readiness_exception",)},
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
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "workbench": "DefenseReadinessLogisticsWorkbench",
        "assistant_panel": "DefenseReadinessLogisticsAssistantPanel",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_mutation_plan(document: str, instruction: str) -> dict:
    text = f"{document} {instruction}".lower()
    if "movement" in text or "convoy" in text or "airlift" in text:
        operation = "plan_logistics_movement"
        table = "defense_readiness_logistics_logistics_movement"
    elif "kit" in text or "packing" in text:
        operation = "validate_deployment_kit"
        table = "defense_readiness_logistics_deployment_plan"
    elif "maintenance" in text or "fault" in text:
        operation = "project_maintenance_status"
        table = "defense_readiness_logistics_maintenance_status"
    elif "shortage" in text or "supply" in text or "fuel" in text or "ammo" in text:
        operation = "score_supply_readiness"
        table = "defense_readiness_logistics_supply_request"
    elif "asset" in text or "serial" in text:
        operation = "record_mission_asset"
        table = "defense_readiness_logistics_mission_asset"
    else:
        operation = "assess_unit_readiness"
        table = "defense_readiness_logistics_unit_readiness"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "proposed_operation": operation,
        "target_table": table,
        "requires_human_confirmation": True,
        "requires_citations": True,
        "crud_datastore_mutation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def defense_app_smoke_test() -> dict:
    state = empty_defense_state()
    ready = assess_unit_readiness(
        state,
        {
            "unit_id": "unit-1",
            "unit_name": "Alpha",
            "mission_set": "rapid_deployment",
            "personnel": {"available": 12, "required": 10, "certified_roles": 5, "required_certified_roles": 4},
            "serviceable_assets": 4,
            "required_assets": 3,
            "supply": {"critical_fill_rate": 0.95},
            "ammo_fill_rate": 0.9,
            "fuel_days": 3,
            "inspection_evidence": ("inspection-1",),
            "commander_approved": True,
        },
    )
    asset = record_mission_asset(ready["state"], {"unit_id": "unit-1", "asset_type": "vehicle", "serial": "VH-1", "serviceability": "serviceable"})
    capability = build_mission_capability(asset["state"], {"unit_id": "unit-1", "mission_set": "rapid_deployment"})
    kit = validate_deployment_kit(asset["state"], {"required_items": ("med", "comms"), "packed_items": ("med", "comms"), "mission_critical_items": ("med", "comms")})
    movement = plan_logistics_movement(kit["state"], {"deployment_id": "dep-1", "mode": "convoy", "route_reviewed": True, "fuel_required": 100, "fuel_available": 125, "asset_ids": ("asset-a",), "window": "D1", "commander_approved": True})
    released = release_deployment_plan(movement["state"], {"deployment_id": "dep-1", "unit_id": "unit-1", "kit_id": kit["deployment_kit"]["id"], "movement_id": movement["logistics_movement"]["id"], "approval_evidence": ("commander",)})
    workbench = build_defense_workbench(released["state"])
    checks = (
        ready["unit_readiness"]["validated_status"] == "deployment_ready",
        capability["rating"] == "capable",
        kit["ok"],
        movement["ok"],
        released["ok"],
        workbench["ok"],
        single_pbc_app_contract()["ok"],
        document_instruction_mutation_plan("convoy order", "create movement")["target_table"] == "defense_readiness_logistics_logistics_movement",
    )
    return {"ok": all(checks), "state": movement["state"], "workbench": workbench, "single_pbc_app": single_pbc_app_contract(), "side_effects": ()}
