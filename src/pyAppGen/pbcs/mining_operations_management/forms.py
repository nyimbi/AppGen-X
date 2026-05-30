"""Package-local forms for the Mining Operations Management workbench."""

from __future__ import annotations


PBC_KEY = "mining_operations_management"

MINING_OPERATIONS_MANAGEMENT_FORM_DEFINITIONS = (
    {
        "form_id": "mine_plan_hierarchy_intake",
        "title": "Mine plan hierarchy intake",
        "route": "POST /app/mining-operations-management/forms/mine-plan-hierarchy-intake",
        "operation": "create_mine_plan",
        "permission": "mining_operations_management.create",
        "record_id_field": "plan_id",
        "projection": "mine_plans",
        "target_table": "mining_operations_management_mine_plan",
        "owned_tables": (
            "mining_operations_management_mine_plan",
            "mining_operations_management_pit_block",
        ),
        "improvement_refs": (1, 2, 5, 6),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "plan_id", "type": "string", "required": True},
            {"name": "plan_period", "type": "string", "required": True},
            {
                "name": "mining_method",
                "type": "enum",
                "required": True,
                "choices": ("open_pit", "underground", "hybrid"),
            },
            {"name": "pit_phase", "type": "string", "required": True},
            {"name": "pushback", "type": "string", "required": False},
            {"name": "bench_or_stope", "type": "string", "required": True},
            {"name": "planned_tonnes", "type": "number", "required": True},
            {"name": "planned_grade", "type": "number", "required": True},
            {
                "name": "ore_destination",
                "type": "enum",
                "required": True,
                "choices": ("crusher", "rom_pad", "stockpile", "waste_dump"),
            },
        ),
    },
    {
        "form_id": "blast_readiness_packet",
        "title": "Blast readiness packet",
        "route": "POST /app/mining-operations-management/forms/blast-readiness-packet",
        "operation": "record_pit_block",
        "permission": "mining_operations_management.update",
        "record_id_field": "blast_packet_id",
        "projection": "blast_packets",
        "target_table": "mining_operations_management_pit_block",
        "owned_tables": (
            "mining_operations_management_pit_block",
            "mining_operations_management_mining_operations_management_control_assertion",
        ),
        "improvement_refs": (3, 4, 20, 21, 22),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "blast_packet_id", "type": "string", "required": True},
            {"name": "plan_id", "type": "string", "required": True},
            {"name": "pit_location_id", "type": "string", "required": True},
            {"name": "hole_count", "type": "number", "required": True},
            {"name": "powder_factor", "type": "number", "required": True},
            {"name": "clearance_confirmed", "type": "boolean", "required": True},
            {
                "name": "re_entry_status",
                "type": "enum",
                "required": True,
                "choices": ("hold", "released", "misfire_review"),
            },
            {
                "name": "geotech_risk",
                "type": "enum",
                "required": True,
                "choices": ("low", "medium", "high"),
            },
        ),
    },
    {
        "form_id": "shift_target_board",
        "title": "Shift target board",
        "route": "POST /app/mining-operations-management/forms/shift-target-board",
        "operation": "review_extraction_shift",
        "permission": "mining_operations_management.update",
        "record_id_field": "shift_id",
        "projection": "shift_targets",
        "target_table": "mining_operations_management_extraction_shift",
        "owned_tables": (
            "mining_operations_management_extraction_shift",
            "mining_operations_management_mine_plan",
        ),
        "improvement_refs": (6, 15, 24, 26),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "shift_id", "type": "string", "required": True},
            {"name": "plan_id", "type": "string", "required": True},
            {"name": "shift_name", "type": "enum", "required": True, "choices": ("day", "night")},
            {"name": "target_ore_tonnes", "type": "number", "required": True},
            {"name": "target_waste_tonnes", "type": "number", "required": True},
            {"name": "target_truck_loads", "type": "number", "required": True},
            {"name": "critical_constraint", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "fleet_capability_card",
        "title": "Fleet capability card",
        "route": "POST /app/mining-operations-management/forms/fleet-capability-card",
        "operation": "simulate_fleet_asset",
        "permission": "mining_operations_management.update",
        "record_id_field": "fleet_asset_id",
        "projection": "fleet_assets",
        "target_table": "mining_operations_management_fleet_asset",
        "owned_tables": (
            "mining_operations_management_fleet_asset",
            "mining_operations_management_mining_operations_management_runtime_parameter",
        ),
        "improvement_refs": (8, 9, 23),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "fleet_asset_id", "type": "string", "required": True},
            {
                "name": "equipment_class",
                "type": "enum",
                "required": True,
                "choices": ("truck", "loader", "drill", "dozer"),
            },
            {"name": "payload_band", "type": "string", "required": True},
            {"name": "approved_areas", "type": "list", "required": True},
            {
                "name": "availability_state",
                "type": "enum",
                "required": True,
                "choices": ("available", "maintenance", "breakdown", "inspection_hold"),
            },
            {
                "name": "fuel_type",
                "type": "enum",
                "required": True,
                "choices": ("diesel", "electric", "hybrid"),
            },
        ),
    },
    {
        "form_id": "dispatch_assignment",
        "title": "Dispatch assignment",
        "route": "POST /app/mining-operations-management/forms/dispatch-assignment",
        "operation": "approve_haulage_cycle",
        "permission": "mining_operations_management.approve",
        "record_id_field": "dispatch_id",
        "projection": "dispatch_assignments",
        "target_table": "mining_operations_management_haulage_cycle",
        "owned_tables": (
            "mining_operations_management_haulage_cycle",
            "mining_operations_management_fleet_asset",
        ),
        "improvement_refs": (7, 8, 16, 23),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "dispatch_id", "type": "string", "required": True},
            {"name": "shift_id", "type": "string", "required": True},
            {"name": "fleet_asset_id", "type": "string", "required": True},
            {"name": "mining_area", "type": "string", "required": True},
            {
                "name": "route_status",
                "type": "enum",
                "required": True,
                "choices": ("open", "restricted", "closed"),
            },
            {
                "name": "material_destination",
                "type": "enum",
                "required": True,
                "choices": ("crusher", "rom_pad", "stockpile", "waste_dump"),
            },
            {"name": "queue_length", "type": "number", "required": False},
        ),
    },
    {
        "form_id": "ore_boundary_decision",
        "title": "Ore boundary decision",
        "route": "POST /app/mining-operations-management/forms/ore-boundary-decision",
        "operation": "create_ore_quality",
        "permission": "mining_operations_management.approve",
        "record_id_field": "boundary_decision_id",
        "projection": "ore_boundary_decisions",
        "target_table": "mining_operations_management_ore_quality",
        "owned_tables": (
            "mining_operations_management_ore_quality",
            "mining_operations_management_stockpile",
        ),
        "improvement_refs": (10, 11, 12, 18),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "boundary_decision_id", "type": "string", "required": True},
            {"name": "dig_block_id", "type": "string", "required": True},
            {"name": "grade_band", "type": "string", "required": True},
            {"name": "destination_changed", "type": "boolean", "required": True},
            {"name": "approved_by", "type": "string", "required": False},
            {"name": "assay_reference", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "stockpile_movement",
        "title": "Stockpile movement",
        "route": "POST /app/mining-operations-management/forms/stockpile-movement",
        "operation": "record_stockpile",
        "permission": "mining_operations_management.update",
        "record_id_field": "movement_id",
        "projection": "stockpile_movements",
        "target_table": "mining_operations_management_stockpile",
        "owned_tables": (
            "mining_operations_management_stockpile",
            "mining_operations_management_ore_quality",
        ),
        "improvement_refs": (13, 14, 15, 17, 19),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "movement_id", "type": "string", "required": True},
            {"name": "stockpile_id", "type": "string", "required": True},
            {
                "name": "movement_type",
                "type": "enum",
                "required": True,
                "choices": ("build", "top_up", "reclaim", "survey_adjustment"),
            },
            {"name": "tonnes_delta", "type": "number", "required": True},
            {"name": "estimated_grade", "type": "number", "required": True},
            {"name": "source_reference", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "geotech_conditional_access",
        "title": "Geotech conditional access",
        "route": "POST /app/mining-operations-management/forms/geotech-conditional-access",
        "operation": "review_mining_operations_management_policy_rule",
        "permission": "mining_operations_management.approve",
        "record_id_field": "access_id",
        "projection": "geotech_access_zones",
        "target_table": "mining_operations_management_mining_operations_management_policy_rule",
        "owned_tables": (
            "mining_operations_management_mining_operations_management_policy_rule",
            "mining_operations_management_pit_block",
        ),
        "improvement_refs": (20, 21, 22),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "access_id", "type": "string", "required": True},
            {"name": "area_id", "type": "string", "required": True},
            {
                "name": "access_state",
                "type": "enum",
                "required": True,
                "choices": ("clear", "conditional", "blocked"),
            },
            {"name": "allowed_equipment", "type": "list", "required": False},
            {"name": "monitoring_source", "type": "string", "required": False},
            {"name": "review_due_shift", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "shift_handover_note",
        "title": "Shift handover note",
        "route": "POST /app/mining-operations-management/forms/shift-handover-note",
        "operation": "create_mining_operations_management_control_assertion",
        "permission": "mining_operations_management.update",
        "record_id_field": "handover_id",
        "projection": "shift_handovers",
        "target_table": "mining_operations_management_mining_operations_management_control_assertion",
        "owned_tables": (
            "mining_operations_management_mining_operations_management_control_assertion",
            "mining_operations_management_extraction_shift",
        ),
        "improvement_refs": (24, 25, 26),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "handover_id", "type": "string", "required": True},
            {"name": "shift_id", "type": "string", "required": True},
            {"name": "delay_code", "type": "string", "required": False},
            {"name": "open_issues", "type": "list", "required": False},
            {
                "name": "plant_feed_risk",
                "type": "enum",
                "required": True,
                "choices": ("low", "medium", "high"),
            },
            {"name": "status", "type": "enum", "required": True, "choices": ("open", "closed")},
        ),
    },
)


def mining_operations_management_form_catalog() -> dict:
    forms = tuple(MINING_OPERATIONS_MANAGEMENT_FORM_DEFINITIONS)
    return {
        "format": "appgen.mining-operations-management-form-catalog.v1",
        "ok": bool(forms),
        "pbc": PBC_KEY,
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def mining_operations_management_get_form(form_id: str) -> dict:
    form = next(
        (item for item in MINING_OPERATIONS_MANAGEMENT_FORM_DEFINITIONS if item["form_id"] == form_id),
        None,
    )
    return {
        "ok": form is not None,
        "pbc": PBC_KEY,
        "form": form,
        "side_effects": (),
    }


def mining_operations_management_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    form = mining_operations_management_get_form(form_id).get("form")
    if form is None:
        return {
            "ok": False,
            "accepted": False,
            "reason": "unknown_form",
            "form_id": form_id,
            "side_effects": (),
        }

    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and supplied.get(field["name"]) in {None, "", ()}
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum"
        and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    invalid_lists = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "list"
        and supplied.get(field["name"]) is not None
        and not isinstance(supplied.get(field["name"]), (list, tuple))
    )
    return {
        "ok": not missing and not invalid_choices and not invalid_lists,
        "accepted": not missing and not invalid_choices and not invalid_lists,
        "pbc": PBC_KEY,
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "invalid_lists": invalid_lists,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = mining_operations_management_form_catalog()
    validation = mining_operations_management_validate_form_payload(
        "dispatch_assignment",
        {
            "tenant": "tenant-smoke",
            "dispatch_id": "dispatch_smoke",
            "shift_id": "shift_smoke",
            "fleet_asset_id": "truck_smoke",
            "mining_area": "PB-05",
            "route_status": "open",
            "material_destination": "crusher",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
