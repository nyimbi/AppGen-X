"""Package-local forms for the Livestock Herd Management standalone slice."""

from __future__ import annotations


PBC_KEY = "livestock_herd_management"


def _is_missing(value) -> bool:
    return value is None or value == ""


LIVESTOCK_HERD_MANAGEMENT_FORM_DEFINITIONS = (
    {
        "form_id": "animal_registry_intake",
        "title": "Register animal",
        "route": "POST /animals",
        "operation": "register_animal",
        "permission": f"{PBC_KEY}.create",
        "owned_tables": ("livestock_herd_management_animal", "livestock_herd_management_herd_group"),
        "domains": ("animal_registry", "genetics", "traceability", "quarantine"),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "animal_id", "type": "string", "required": True},
            {"name": "species", "type": "enum", "required": True, "choices": ("cattle", "goat", "sheep", "swine", "poultry")},
            {"name": "production_type", "type": "enum", "required": True, "choices": ("dairy", "beef", "breeding", "layer", "broiler")},
            {"name": "primary_identifier", "type": "string", "required": True},
            {"name": "source_provenance", "type": "enum", "required": True, "choices": ("born_on_farm", "purchased", "leased", "transfer_in", "imported")},
            {"name": "sex", "type": "enum", "required": True, "choices": ("female", "male")},
            {"name": "birth_date", "type": "date", "required": True},
            {"name": "breed", "type": "string", "required": True},
            {"name": "default_group_id", "type": "string", "required": False},
            {"name": "requires_quarantine", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "herd_group_assignment",
        "title": "Assign herd group",
        "route": "POST /herd-groups",
        "operation": "assign_herd_group",
        "permission": f"{PBC_KEY}.update",
        "owned_tables": ("livestock_herd_management_herd_group",),
        "domains": ("herd_groups", "grazing", "traceability"),
        "fields": (
            {"name": "group_id", "type": "string", "required": True},
            {"name": "animal_id", "type": "string", "required": True},
            {"name": "location", "type": "string", "required": True},
            {"name": "production_stage", "type": "enum", "required": True, "choices": ("heifer", "lactating", "dry", "grower", "quarantine")},
            {"name": "entry_date", "type": "date", "required": True},
            {"name": "stocking_density", "type": "number", "required": True},
            {"name": "reason", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "breeding_cycle",
        "title": "Record breeding and pregnancy",
        "route": "POST /breeding-records",
        "operation": "record_breeding_cycle",
        "permission": f"{PBC_KEY}.update",
        "owned_tables": ("livestock_herd_management_breeding_record",),
        "domains": ("breeding", "pregnancy", "genetics"),
        "fields": (
            {"name": "breeding_id", "type": "string", "required": True},
            {"name": "animal_id", "type": "string", "required": True},
            {"name": "service_date", "type": "date", "required": True},
            {"name": "service_method", "type": "enum", "required": True, "choices": ("artificial_insemination", "natural_service", "embryo_transfer")},
            {"name": "sire_reference", "type": "string", "required": True},
            {"name": "technician", "type": "string", "required": True},
            {"name": "expected_due_date", "type": "date", "required": True},
            {"name": "genetic_risk_score", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "calving_and_offspring",
        "title": "Record calving",
        "route": "POST /animals/calving-events",
        "operation": "record_calving_event",
        "permission": f"{PBC_KEY}.update",
        "owned_tables": ("livestock_herd_management_animal", "livestock_herd_management_breeding_record"),
        "domains": ("pregnancy", "calving", "traceability", "welfare"),
        "fields": (
            {"name": "calving_id", "type": "string", "required": True},
            {"name": "dam_id", "type": "string", "required": True},
            {"name": "offspring_id", "type": "string", "required": True},
            {"name": "birth_date", "type": "date", "required": True},
            {"name": "birth_weight_kg", "type": "number", "required": True},
            {"name": "assistance_level", "type": "enum", "required": True, "choices": ("none", "light", "veterinary")},
            {"name": "colostrum_confirmed", "type": "boolean", "required": True},
            {"name": "calf_sex", "type": "enum", "required": True, "choices": ("female", "male")},
        ),
    },
    {
        "form_id": "health_treatment_and_vaccination",
        "title": "Health treatment and vaccination",
        "route": "POST /health-events",
        "operation": "record_health_intervention",
        "permission": f"{PBC_KEY}.update",
        "owned_tables": ("livestock_herd_management_health_event", "livestock_herd_management_treatment"),
        "domains": ("health", "treatments", "vaccinations", "withdrawal"),
        "fields": (
            {"name": "animal_id", "type": "string", "required": True},
            {"name": "health_event_id", "type": "string", "required": True},
            {"name": "symptom", "type": "string", "required": True},
            {"name": "diagnosis", "type": "string", "required": True},
            {"name": "treatment_name", "type": "string", "required": True},
            {"name": "vaccination_name", "type": "string", "required": True},
            {"name": "medication_lot", "type": "string", "required": True},
            {"name": "withdrawal_days", "type": "number", "required": True},
            {"name": "administered_by", "type": "string", "required": True},
            {"name": "next_due_date", "type": "date", "required": True},
        ),
    },
    {
        "form_id": "feed_and_grazing_plan",
        "title": "Feed and grazing plan",
        "route": "POST /feed-rations",
        "operation": "record_feed_and_grazing_plan",
        "permission": f"{PBC_KEY}.update",
        "owned_tables": ("livestock_herd_management_feed_ration", "livestock_herd_management_herd_group"),
        "domains": ("feed", "grazing", "paddocks", "weights", "yield"),
        "fields": (
            {"name": "plan_id", "type": "string", "required": True},
            {"name": "group_id", "type": "string", "required": True},
            {"name": "ration_name", "type": "string", "required": True},
            {"name": "dry_matter_pct", "type": "number", "required": True},
            {"name": "protein_pct", "type": "number", "required": True},
            {"name": "paddock_id", "type": "string", "required": True},
            {"name": "forage_cover_kg_dm", "type": "number", "required": True},
            {"name": "rest_days_required", "type": "number", "required": True},
            {"name": "target_daily_gain_kg", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "movement_biosecurity_and_quarantine",
        "title": "Movement, quarantine, and biosecurity",
        "route": "POST /movement-permits",
        "operation": "record_movement_and_biosecurity",
        "permission": f"{PBC_KEY}.approve",
        "owned_tables": ("livestock_herd_management_movement_permit", "livestock_herd_management_health_event"),
        "domains": ("movement_permits", "quarantine", "biosecurity", "traceability"),
        "fields": (
            {"name": "permit_id", "type": "string", "required": True},
            {"name": "animal_id", "type": "string", "required": True},
            {"name": "origin_premises", "type": "string", "required": True},
            {"name": "destination_premises", "type": "string", "required": True},
            {"name": "movement_date", "type": "date", "required": True},
            {"name": "quarantine_status", "type": "enum", "required": True, "choices": ("none", "open", "released")},
            {"name": "biosecurity_score", "type": "number", "required": True},
            {"name": "trace_lot_id", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "welfare_mortality_and_yield",
        "title": "Welfare, mortality, and yield",
        "route": "POST /animals/welfare-yield",
        "operation": "record_welfare_and_yield",
        "permission": f"{PBC_KEY}.update",
        "owned_tables": ("livestock_herd_management_animal", "livestock_herd_management_treatment"),
        "domains": ("welfare", "mortality", "inventory", "product_yield", "weights"),
        "fields": (
            {"name": "animal_id", "type": "string", "required": True},
            {"name": "welfare_score", "type": "number", "required": True},
            {"name": "weight_kg", "type": "number", "required": True},
            {"name": "yield_id", "type": "string", "required": True},
            {"name": "product_type", "type": "enum", "required": True, "choices": ("milk", "meat", "wool", "eggs")},
            {"name": "quantity", "type": "number", "required": True},
            {"name": "mortality_status", "type": "enum", "required": True, "choices": ("alive", "mortality_open", "mortality_closed")},
            {"name": "disposition_method", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "assistant_change_preview",
        "title": "Assistant CRUD preview",
        "route": "POST /assistant/livestock-herd-management/preview",
        "operation": "assistant_crud_preview",
        "permission": f"{PBC_KEY}.admin",
        "owned_tables": (
            "livestock_herd_management_animal",
            "livestock_herd_management_herd_group",
            "livestock_herd_management_health_event",
            "livestock_herd_management_breeding_record",
            "livestock_herd_management_feed_ration",
            "livestock_herd_management_movement_permit",
            "livestock_herd_management_treatment",
        ),
        "domains": ("assistant", "crud_preview", "governance"),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {"name": "target_table", "type": "enum", "required": True, "choices": (
                "livestock_herd_management_animal",
                "livestock_herd_management_herd_group",
                "livestock_herd_management_health_event",
                "livestock_herd_management_breeding_record",
                "livestock_herd_management_feed_ration",
                "livestock_herd_management_movement_permit",
                "livestock_herd_management_treatment",
            )},
            {"name": "requested_action", "type": "enum", "required": True, "choices": ("create", "read", "update", "delete")},
        ),
    },
)


def livestock_herd_management_form_catalog() -> dict:
    """Return the package-local standalone form registry."""
    forms = tuple(LIVESTOCK_HERD_MANAGEMENT_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": PBC_KEY,
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def livestock_herd_management_get_form(form_id: str) -> dict:
    """Return one livestock form definition by identifier."""
    form = next((item for item in LIVESTOCK_HERD_MANAGEMENT_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": PBC_KEY,
        "form": form,
        "side_effects": (),
    }


def livestock_herd_management_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate required fields and enum choices for a standalone livestock form."""
    form = livestock_herd_management_get_form(form_id).get("form")
    if form is None:
        return {"ok": False, "accepted": False, "reason": "unknown_form", "form_id": form_id, "side_effects": ()}

    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and _is_missing(supplied.get(field["name"]))
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum"
        and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    return {
        "ok": not missing and not invalid_choices,
        "accepted": not missing and not invalid_choices,
        "pbc": PBC_KEY,
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one happy-path assistant preview validation."""
    catalog = livestock_herd_management_form_catalog()
    validation = livestock_herd_management_validate_form_payload(
        "assistant_change_preview",
        {
            "document_text": "Vaccination memo: booster due for cohort A and update milk withdrawal queue.",
            "instructions": "Preview updates only; do not mutate production records.",
            "target_table": "livestock_herd_management_treatment",
            "requested_action": "update",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
