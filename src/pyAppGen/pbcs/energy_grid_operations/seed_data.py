"""Seed and demo workspace data for the standalone energy_grid_operations package."""

from __future__ import annotations

from .runtime import DEFAULT_CONFIGURATION, PARAMETER_DEFINITIONS, PBC_KEY, RULE_DEFINITIONS


def demo_workspace_seed(tenant: str = "tenant_demo") -> dict:
    return {
        "configuration": dict(DEFAULT_CONFIGURATION),
        "parameters": tuple({"name": item["name"], "value": item["default"], "tenant": tenant} for item in PARAMETER_DEFINITIONS),
        "rules": tuple(
            {
                "rule_id": item["rule_id"],
                "tenant": tenant,
                "scope": item["scope"],
                "required_fields": item["required_fields"],
                "required_approver_role": item["required_approver_role"],
                "policy_version": DEFAULT_CONFIGURATION["default_policy_version"],
            }
            for item in RULE_DEFINITIONS
        ),
        "records": (
            {
                "route": "POST /grid-assets",
                "payload": {
                    "asset_id": f"asset_{tenant}",
                    "tenant": tenant,
                    "asset_type": "breaker",
                    "asset_name": "North Feeder Breaker",
                    "voltage_kv": 33,
                    "substation_id": f"sub_{tenant}",
                    "feeder_id": f"feeder_{tenant}",
                    "normal_state": "closed",
                    "phases": ("A", "B", "C"),
                    "gis_reference": f"gis://{tenant}/breaker-1",
                    "scada_points": (f"SCADA-{tenant}-BRK",),
                },
            },
            {
                "route": "POST /load-forecasts",
                "payload": {
                    "forecast_id": f"forecast_{tenant}",
                    "tenant": tenant,
                    "feeder_id": f"feeder_{tenant}",
                    "forecast_mw": 28.5,
                    "peak_mw": 31.2,
                    "confidence": 0.84,
                    "weather_scenario": "storm_watch",
                },
            },
            {
                "route": "record_grid_topology",
                "payload": {
                    "topology_id": f"topology_{tenant}",
                    "tenant": tenant,
                    "feeder_id": f"feeder_{tenant}",
                    "source_asset_id": f"asset_{tenant}",
                    "energized_sections": ("section_a", "section_b", "section_c"),
                    "normally_open_ties": ("tie_11",),
                    "backfeed_paths": ("tie_11->feeder_backup",),
                    "phase_map": {"section_a": "ABC", "section_b": "ABC"},
                },
            },
            {
                "route": "create_reliability_constraint",
                "payload": {
                    "constraint_id": f"constraint_{tenant}",
                    "tenant": tenant,
                    "constraint_type": "thermal",
                    "scope_id": f"feeder_{tenant}",
                    "severity": "medium",
                    "limit_value": 55.0,
                },
            },
            {
                "route": "POST /switching-orders",
                "payload": {
                    "switching_order_id": f"switch_{tenant}",
                    "tenant": tenant,
                    "feeder_id": f"feeder_{tenant}",
                    "substation_id": f"sub_{tenant}",
                    "clearance_id": f"clr_{tenant}",
                    "requested_by": "dispatcher",
                    "steps": (
                        {"sequence": 1, "action": "open", "target": f"asset_{tenant}", "hold_point": True, "description": "Open breaker"},
                        {"sequence": 2, "action": "verify", "target": f"asset_{tenant}", "description": "Verify isolation"},
                    ),
                },
            },
            {
                "route": "POST /dispatch-instructions",
                "payload": {
                    "dispatch_instruction_id": f"dispatch_{tenant}",
                    "tenant": tenant,
                    "objective_type": "restoration_support",
                    "feeder_id": f"feeder_{tenant}",
                    "target_asset_id": f"asset_{tenant}",
                    "expected_load_shift_mw": 4.5,
                    "telemetry_freshness_seconds": 90,
                    "rollback_conditions": ("restore_normal_after_restoration",),
                },
            },
            {
                "route": "POST /outage-events",
                "payload": {
                    "outage_event_id": f"outage_{tenant}",
                    "tenant": tenant,
                    "feeder_id": f"feeder_{tenant}",
                    "substation_id": f"sub_{tenant}",
                    "cause": "tree_contact",
                    "affected_customers": 1800,
                },
            },
            {
                "route": "create_energy_grid_operations_control_assertion",
                "payload": {
                    "assertion_id": f"assertion_{tenant}",
                    "tenant": tenant,
                    "control_name": "switching_clearance_evidence",
                    "scope_id": f"switch_{tenant}",
                    "assertion_status": "satisfied",
                    "evidence_summary": "Clearance and hold point reviewed by control room supervisor.",
                },
            },
            {
                "route": "record_energy_grid_operations_governed_model",
                "payload": {
                    "model_id": f"model_{tenant}",
                    "tenant": tenant,
                    "model_kind": "restoration_priority_ranker",
                    "approval_scope": "decision_support_only",
                    "training_boundary": "owned_outage_and_switching_history",
                    "deployment_status": "shadow",
                },
            },
        ),
    }


def seed_plan(tenant: str = "tenant_demo") -> dict:
    seed = demo_workspace_seed(tenant=tenant)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "configuration": seed["configuration"],
        "parameters": seed["parameters"],
        "rules": seed["rules"],
        "records": seed["records"],
        "side_effects": (),
    }


def validate_seed_data(tenant: str = "tenant_demo") -> dict:
    seed = demo_workspace_seed(tenant=tenant)
    asset_ids = {
        item["payload"]["asset_id"]
        for item in seed["records"]
        if item["route"] == "POST /grid-assets"
    }
    topology_sources = {
        item["payload"]["source_asset_id"]
        for item in seed["records"]
        if item["route"] == "record_grid_topology"
    }
    return {
        "ok": bool(asset_ids) and topology_sources.issubset(asset_ids),
        "pbc": PBC_KEY,
        "missing_asset_references": tuple(sorted(topology_sources - asset_ids)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": seed_plan()["ok"] and validate_seed_data()["ok"],
        "side_effects": (),
    }
