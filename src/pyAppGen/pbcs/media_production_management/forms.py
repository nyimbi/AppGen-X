"""Role-specific forms for the media_production_management PBC."""
from __future__ import annotations

PBC_KEY = "media_production_management"


def form_catalog() -> dict:
    forms = (
        {
            "id": "development_package_intake",
            "title": "Development Package Intake",
            "owned_table": "media_production_management_production",
            "fields": (
                "tenant", "project_code", "format", "script_draft", "creative_package_uri",
                "attachments", "financing_status", "greenlight_target", "executive_owner",
            ),
            "validations": ("script draft required", "financing status required", "tenant scoped"),
        },
        {
            "id": "budget_top_sheet_revision",
            "title": "Budget Top Sheet Revision",
            "owned_table": "media_production_management_budget_line",
            "fields": (
                "phase", "account_group", "approved_baseline", "forecast_amount", "change_reason",
                "contingency_draw", "currency", "approval_role",
            ),
            "validations": ("locked baseline preserved", "change reason required", "approval threshold enforced"),
        },
        {
            "id": "cast_crew_engagement_packet",
            "title": "Cast And Crew Engagement Packet",
            "owned_table": "media_production_management_crew_booking",
            "fields": (
                "person_name", "engagement_type", "union_status", "rate_card", "availability_window",
                "travel_class", "work_guarantee", "deal_memo_source",
            ),
            "validations": ("cast fields separated from crew", "source document cited", "availability checked"),
        },
        {
            "id": "location_package",
            "title": "Location Package",
            "owned_table": "media_production_management_location_permit",
            "fields": (
                "jurisdiction", "site_owner", "permit_id", "curfew", "police_fire_requirements",
                "parking_plan", "insurance_evidence", "contingency_location",
            ),
            "validations": ("permit evidence required", "curfew parsed", "insurance verified"),
        },
        {
            "id": "shoot_day_release",
            "title": "Shoot Day Release",
            "owned_table": "media_production_management_shoot_day",
            "fields": (
                "shoot_date", "unit", "scene_blocks", "call_sheet_status", "safety_plan",
                "transport_status", "equipment_status", "weather_review", "nearest_hospital",
            ),
            "validations": ("readiness gate passed", "call sheet approved", "high risk safety plan attached"),
        },
        {
            "id": "daily_production_report",
            "title": "Daily Production Report",
            "owned_table": "media_production_management_shoot_day",
            "fields": (
                "actual_first_call", "first_shot", "meal_break", "wrap_time", "pages_completed",
                "scenes_completed", "delay_reasons", "incidents", "overtime_hours",
            ),
            "validations": ("planned actual variance calculated", "incidents triaged", "labor penalties evaluated"),
        },
        {
            "id": "post_vfx_finishing_board",
            "title": "Post, VFX, And Finishing Board",
            "owned_table": "media_production_management_post_production_task",
            "fields": (
                "milestone", "dependency", "owner", "vendor", "shot_code", "turnover_package",
                "version", "approval_state", "due_date",
            ),
            "validations": ("dependencies complete", "turnover package complete", "approval trail preserved"),
        },
        {
            "id": "deliverables_qc_matrix",
            "title": "Deliverables QC Matrix",
            "owned_table": "media_production_management_delivery_asset",
            "fields": (
                "platform", "territory", "language", "audio_layout", "caption_set", "metadata_packet",
                "checksum", "qc_result", "shipment_state", "archive_bundle",
            ),
            "validations": ("platform spec matched", "checksum required", "qc failure routed"),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def form_for(form_id: str) -> dict:
    for form in form_catalog()["forms"]:
        if form["id"] == form_id:
            return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "form_id": form_id, "side_effects": ()}


def smoke_test() -> dict:
    catalog = form_catalog()
    return {
        "ok": catalog["ok"] and len(catalog["forms"]) >= 8 and form_for("shoot_day_release")["ok"],
        "side_effects": (),
    }
