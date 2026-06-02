"""Package-local controls for the Mining Operations Management workbench."""

from __future__ import annotations

from copy import deepcopy

from .runtime import mining_operations_management_build_release_evidence
from .runtime import mining_operations_management_runtime_smoke
from .runtime import mining_operations_management_verify_owned_table_boundary


PBC_KEY = "mining_operations_management"

MINING_OPERATIONS_MANAGEMENT_CONTROLS = (
    {
        "control_id": "blast_clearance_gate",
        "title": "Blast clearance gate",
        "description": "Blocks blast release when clearance or re-entry conditions remain open.",
        "permission": "mining_operations_management.approve",
    },
    {
        "control_id": "dispatch_boundary_proof",
        "title": "Dispatch boundary proof",
        "description": "Ensures assigned assets only work approved areas and open routes.",
        "permission": "mining_operations_management.approve",
    },
    {
        "control_id": "ore_boundary_governance",
        "title": "Ore boundary governance",
        "description": "Requires approval before destination-changing ore-waste calls take effect.",
        "permission": "mining_operations_management.approve",
    },
    {
        "control_id": "stockpile_genealogy_integrity",
        "title": "Stockpile genealogy integrity",
        "description": "Requires every stockpile movement to retain source lineage and grade evidence.",
        "permission": "mining_operations_management.update",
    },
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Runs package-local release evidence and owned-boundary checks.",
        "permission": "mining_operations_management.admin",
    },
)


def _ensure_state(state: dict | None) -> dict:
    if state is None:
        smoke = mining_operations_management_runtime_smoke()
        return {
            **deepcopy(smoke.get("command", {}).get("state", {}) or {}),
            "mine_plans": {},
            "blast_packets": {},
            "shift_targets": {},
            "fleet_assets": {},
            "dispatch_assignments": {},
            "ore_boundary_decisions": {},
            "stockpile_movements": {},
            "geotech_access_zones": {},
            "shift_handovers": {},
        }
    ensured = deepcopy(dict(state))
    for key in (
        "mine_plans",
        "blast_packets",
        "shift_targets",
        "fleet_assets",
        "dispatch_assignments",
        "ore_boundary_decisions",
        "stockpile_movements",
        "geotech_access_zones",
        "shift_handovers",
    ):
        ensured.setdefault(key, {})
    return ensured


def mining_operations_management_control_catalog() -> dict:
    return {
        "format": "appgen.mining-operations-management-control-catalog.v1",
        "ok": bool(MINING_OPERATIONS_MANAGEMENT_CONTROLS),
        "pbc": PBC_KEY,
        "controls": MINING_OPERATIONS_MANAGEMENT_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in MINING_OPERATIONS_MANAGEMENT_CONTROLS),
        "side_effects": (),
    }


def mining_operations_management_control_center(state: dict | None = None) -> dict:
    current = _ensure_state(state)
    release = mining_operations_management_build_release_evidence()
    accepted_boundary = mining_operations_management_verify_owned_table_boundary(
        (
            "mining_operations_management_mine_plan",
            "mining_operations_management_haulage_cycle",
            "mining_operations_management_stockpile",
        )
    )
    rejected_boundary = mining_operations_management_verify_owned_table_boundary(("foreign_dispatch_table",))

    blast_packets = tuple(current["blast_packets"].values())
    dispatch_assignments = tuple(current["dispatch_assignments"].values())
    fleet_assets = current["fleet_assets"]
    ore_boundary_decisions = tuple(current["ore_boundary_decisions"].values())
    stockpile_movements = tuple(current["stockpile_movements"].values())
    geotech_access_zones = tuple(current["geotech_access_zones"].values())

    pending_clearance = tuple(
        packet["record_id"]
        for packet in blast_packets
        if not packet["payload"].get("clearance_confirmed")
        or packet["payload"].get("re_entry_status") != "released"
    )
    dispatch_violations = []
    for assignment in dispatch_assignments:
        payload = assignment["payload"]
        asset = fleet_assets.get(payload.get("fleet_asset_id"))
        approved_areas = tuple(asset["payload"].get("approved_areas", ())) if asset else ()
        if payload.get("route_status") == "closed":
            dispatch_violations.append(f"{assignment['record_id']}:route_closed")
        if approved_areas and payload.get("mining_area") not in approved_areas:
            dispatch_violations.append(f"{assignment['record_id']}:area_not_approved")
    unapproved_boundary_changes = tuple(
        decision["record_id"]
        for decision in ore_boundary_decisions
        if decision["payload"].get("destination_changed") and not decision["payload"].get("approved_by")
    )
    missing_genealogy = tuple(
        movement["record_id"]
        for movement in stockpile_movements
        if not movement["payload"].get("source_reference")
    )
    blocked_areas = tuple(
        access["record_id"]
        for access in geotech_access_zones
        if access["payload"].get("access_state") == "blocked"
    )

    return {
        "ok": release["ok"]
        and accepted_boundary["ok"]
        and not rejected_boundary["ok"]
        and not pending_clearance
        and not dispatch_violations
        and not unapproved_boundary_changes
        and not missing_genealogy,
        "pbc": PBC_KEY,
        "controls": mining_operations_management_control_catalog()["controls"],
        "release": release,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "blast_clearance": {
            "pending_packet_ids": pending_clearance,
            "released_count": len(blast_packets) - len(pending_clearance),
        },
        "dispatch_boundary": {
            "violations": tuple(dispatch_violations),
            "assignment_count": len(dispatch_assignments),
        },
        "ore_boundary": {
            "unapproved_destination_changes": unapproved_boundary_changes,
            "decision_count": len(ore_boundary_decisions),
        },
        "stockpile_genealogy": {
            "missing_lineage": missing_genealogy,
            "movement_count": len(stockpile_movements),
        },
        "geotech_access": {
            "blocked_areas": blocked_areas,
            "conditional_areas": tuple(
                access["record_id"]
                for access in geotech_access_zones
                if access["payload"].get("access_state") == "conditional"
            ),
        },
        "side_effects": (),
    }


def mining_operations_management_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    normalized = str(action).lower()
    boundary = mining_operations_management_verify_owned_table_boundary((table,))
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": PBC_KEY,
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized != "read",
        "boundary": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    preview = mining_operations_management_mutation_preview(
        "update",
        "mining_operations_management_mine_plan",
        {"plan_id": "plan_smoke"},
    )
    control_center = mining_operations_management_control_center()
    return {
        "ok": preview["ok"] and control_center["accepted_boundary"]["ok"] and not control_center["rejected_boundary"]["ok"],
        "preview": preview,
        "control_center": control_center,
        "side_effects": (),
    }
