"""Deterministic standalone seed bundle for hotel_revenue_management."""

from __future__ import annotations

from .config import DOMAIN_RULE_SCHEMA
from .runtime import PBC_KEY


def default_configuration() -> dict:
    return {
        "database_backend": "postgresql",
        "event_topic": "pbc.hotel_revenue_management.events",
        "retry_limit": 5,
        "default_policy": "balanced-revenue-control",
        "workbench_limit": 45,
        "confirmation_required_for_agent_writes": True,
    }


def default_parameter_values() -> dict:
    return {
        "quality_score_floor": 0.78,
        "materiality_threshold": 0.12,
        "approval_sla_hours": 24,
        "risk_threshold": 0.68,
        "forecast_horizon_days": 180,
        "workbench_limit": 45,
    }


def default_rules() -> tuple[dict, ...]:
    return DOMAIN_RULE_SCHEMA


def default_room_types() -> tuple[dict, ...]:
    return (
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "code": "DLX",
            "name": "Deluxe King",
            "physical_rooms": 18,
            "maintenance_holdback": 1,
            "complimentary_allotment": 1,
            "capacity_adults": 2,
            "capacity_children": 1,
            "substitution_targets": ("STE",),
        },
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "code": "STE",
            "name": "Junior Suite",
            "physical_rooms": 8,
            "maintenance_holdback": 0,
            "complimentary_allotment": 0,
            "capacity_adults": 3,
            "capacity_children": 1,
            "substitution_targets": (),
        },
    )


def default_rate_plans() -> tuple[dict, ...]:
    return (
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "room_type_id": "DLX",
            "code": "BAR",
            "base_rate": 189.0,
            "currency": "USD",
            "member_fence": "public",
            "cancellation_policy": "24h-flex",
        },
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "room_type_id": "DLX",
            "code": "MEMBER",
            "parent_rate_plan_id": "BAR",
            "base_rate": 189.0,
            "derived_discount_pct": 10.0,
            "currency": "USD",
            "member_fence": "member",
            "cancellation_policy": "24h-flex",
        },
    )


def default_channel_inventory_commands() -> tuple[dict, ...]:
    return (
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "room_type_id": "DLX",
            "rate_plan_id": "BAR",
            "code": "DIRECT-0601",
            "channel_code": "direct",
            "stay_date": "2026-06-01",
            "allotment": 9,
        },
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "room_type_id": "DLX",
            "rate_plan_id": "BAR",
            "code": "OTA1-0601",
            "channel_code": "ota-1",
            "stay_date": "2026-06-01",
            "allotment": 6,
            "parity_exception_reason": "member_only_discount",
        },
    )


def default_forecasts() -> tuple[dict, ...]:
    return (
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "room_type_id": "DLX",
            "code": "FC-0601",
            "stay_date": "2026-06-01",
            "transient_demand": 10,
            "corporate_demand": 3,
            "group_demand": 2,
            "wholesale_demand": 1,
            "house_use_demand": 0,
            "pickup_baseline": 8,
            "confidence": 0.82,
            "manual_override_rooms": 17,
            "override_reason": "concert weekend",
            "approved_by": "rm-alpha",
        },
    )


def default_overbooking_policies() -> tuple[dict, ...]:
    return (
        {
            "tenant": "tenant_alpha",
            "hotel_id": "hotel_alpha",
            "room_type_id": "DLX",
            "code": "OB-PEAK",
            "forecast_rooms": 17,
            "overbook_limit": 2,
            "date_class": "compression",
            "no_show_rate": 0.05,
            "cancellation_rate": 0.08,
            "arrival_protection_pct": 0.1,
        },
    )


def default_governed_models() -> tuple[dict, ...]:
    return (
        {
            "tenant": "tenant_alpha",
            "code": "YIELD-GOV-1",
            "model_name": "compression-night-advisor",
            "model_version": "1.0.0",
            "model_purpose": "recommend rate and channel controls",
            "approval_policy": "human-confirmed",
            "drift_threshold": 0.15,
            "human_confirmation_required": True,
        },
    )


def seed_plan() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "configuration": default_configuration(),
        "parameters": default_parameter_values(),
        "rules": default_rules(),
        "room_types": default_room_types(),
        "rate_plans": default_rate_plans(),
        "channel_inventory": default_channel_inventory_commands(),
        "forecasts": default_forecasts(),
        "overbooking_policies": default_overbooking_policies(),
        "governed_models": default_governed_models(),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    rate_plan_ids = {item["code"] for item in default_rate_plans()}
    room_type_ids = {item["code"] for item in default_room_types()}
    inventory_ok = all(item["rate_plan_id"] in rate_plan_ids and item["room_type_id"] in room_type_ids for item in default_channel_inventory_commands())
    forecast_ok = all(item["room_type_id"] in room_type_ids for item in default_forecasts())
    policy_ok = all(item["room_type_id"] in room_type_ids for item in default_overbooking_policies())
    return {
        "ok": inventory_ok and forecast_ok and policy_ok,
        "pbc": PBC_KEY,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
