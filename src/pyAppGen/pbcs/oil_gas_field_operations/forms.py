"""Package-local forms for the Oil and Gas Field Operations workbench."""

from __future__ import annotations


OIL_GAS_FIELD_OPERATIONS_FORM_DEFINITIONS = (
    {
        "form_id": "well_hierarchy_intake",
        "title": "Register producing well",
        "route": "POST /wells",
        "operation": "create_well",
        "permission": "oil_gas_field_operations.create",
        "owned_tables": ("oil_gas_field_operations_well",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "well_id", "type": "string", "required": True},
            {"name": "field_name", "type": "string", "required": True},
            {"name": "area_name", "type": "string", "required": True},
            {"name": "pad_name", "type": "string", "required": True},
            {"name": "lease_name", "type": "string", "required": True},
            {"name": "route_code", "type": "string", "required": True},
            {"name": "wellbore", "type": "string", "required": True},
            {"name": "completion", "type": "string", "required": True},
            {"name": "interval_name", "type": "string", "required": True},
            {
                "name": "lifecycle_state",
                "type": "enum",
                "required": True,
                "choices": ("flowback", "producing", "shut_in", "workover", "suspended", "abandoned"),
            },
            {
                "name": "lift_type",
                "type": "enum",
                "required": True,
                "choices": ("rod_pump", "esp", "gas_lift", "plunger", "pcp", "flowing"),
            },
            {
                "name": "integrity_risk",
                "type": "enum",
                "required": True,
                "choices": ("low", "watch", "high"),
            },
        ),
    },
    {
        "form_id": "daily_production_capture",
        "title": "Capture daily production",
        "route": "POST /production-readings",
        "operation": "record_production_reading",
        "permission": "oil_gas_field_operations.create",
        "owned_tables": ("oil_gas_field_operations_production_reading",),
        "fields": (
            {"name": "well_id", "type": "string", "required": True},
            {"name": "production_date", "type": "string", "required": True},
            {"name": "oil_bbl", "type": "number", "required": True},
            {"name": "gas_mcf", "type": "number", "required": True},
            {"name": "water_bbl", "type": "number", "required": True},
            {"name": "injected_water_bbl", "type": "number", "required": False},
            {
                "name": "gas_disposition",
                "type": "enum",
                "required": True,
                "choices": ("sales", "flare", "vent", "fuel", "reinject"),
            },
            {
                "name": "oil_disposition",
                "type": "enum",
                "required": True,
                "choices": ("sold", "stock", "trucked", "transferred"),
            },
            {
                "name": "measurement_basis",
                "type": "enum",
                "required": True,
                "choices": ("gross_test", "allocated", "revised"),
            },
            {
                "name": "production_test_state",
                "type": "enum",
                "required": True,
                "choices": ("planned", "validated", "superseded", "failed", "allocation_approved"),
            },
            {"name": "downtime_hours", "type": "number", "required": True},
            {"name": "revision_reason", "type": "string", "required": False},
        ),
    },
    {
        "form_id": "field_ticket_triage",
        "title": "Open field ticket",
        "route": "POST /field-tickets",
        "operation": "review_field_ticket",
        "permission": "oil_gas_field_operations.update",
        "owned_tables": ("oil_gas_field_operations_field_ticket",),
        "fields": (
            {"name": "ticket_id", "type": "string", "required": True},
            {"name": "well_id", "type": "string", "required": True},
            {
                "name": "ticket_type",
                "type": "enum",
                "required": True,
                "choices": ("downtime", "integrity", "meter", "chemical", "haul_off", "maintenance"),
            },
            {
                "name": "severity",
                "type": "enum",
                "required": True,
                "choices": ("low", "medium", "high", "critical"),
            },
            {"name": "deferred_oil_bbl", "type": "number", "required": True},
            {"name": "root_cause", "type": "string", "required": True},
            {"name": "requires_shutdown", "type": "boolean", "required": True},
            {"name": "route_code", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "workover_readiness_pack",
        "title": "Prepare workover readiness pack",
        "route": "POST /workover-plans",
        "operation": "approve_workover_plan",
        "permission": "oil_gas_field_operations.approve",
        "owned_tables": ("oil_gas_field_operations_workover_plan",),
        "fields": (
            {"name": "plan_id", "type": "string", "required": True},
            {"name": "well_id", "type": "string", "required": True},
            {"name": "candidate_reason", "type": "string", "required": True},
            {"name": "expected_recovery_bopd", "type": "number", "required": True},
            {
                "name": "permit_status",
                "type": "enum",
                "required": True,
                "choices": ("draft", "submitted", "approved", "blocked"),
            },
            {
                "name": "barrier_risk",
                "type": "enum",
                "required": True,
                "choices": ("low", "watch", "high"),
            },
            {"name": "lift_failure_mode", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "hse_boundary_event",
        "title": "Log HSE boundary event",
        "route": "POST /hse-events",
        "operation": "simulate_hse_event",
        "permission": "oil_gas_field_operations.update",
        "owned_tables": ("oil_gas_field_operations_hse_event",),
        "fields": (
            {"name": "event_id", "type": "string", "required": True},
            {"name": "well_id", "type": "string", "required": True},
            {
                "name": "event_classification",
                "type": "enum",
                "required": True,
                "choices": ("spill", "release", "injury", "near_miss", "integrity_breach"),
            },
            {"name": "reportable", "type": "boolean", "required": True},
            {"name": "spill_bbl", "type": "number", "required": True},
            {
                "name": "containment_status",
                "type": "enum",
                "required": True,
                "choices": ("contained", "monitoring", "escalated"),
            },
            {"name": "ignition_risk", "type": "boolean", "required": True},
            {"name": "people_affected", "type": "number", "required": True},
        ),
    },
    {
        "form_id": "morning_review_request",
        "title": "Run morning production review",
        "route": "POST /oil-gas-field-operations/assistant/document-preview",
        "operation": "query_oil_gas_field_operations_assistant_preview",
        "permission": "oil_gas_field_operations.read",
        "owned_tables": (
            "oil_gas_field_operations_well",
            "oil_gas_field_operations_production_reading",
            "oil_gas_field_operations_field_ticket",
            "oil_gas_field_operations_hse_event",
        ),
        "fields": (
            {"name": "route_code", "type": "string", "required": False},
            {"name": "minimum_deferred_oil_bbl", "type": "number", "required": True},
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {
                "name": "target_entity",
                "type": "enum",
                "required": True,
                "choices": ("well", "production_reading", "field_ticket", "workover_plan", "hse_event"),
            },
            {
                "name": "requested_action",
                "type": "enum",
                "required": True,
                "choices": ("create", "read", "update", "delete"),
            },
        ),
    },
)


def oil_gas_field_operations_form_catalog() -> dict:
    """Return the package-local workbench form registry."""
    forms = tuple(OIL_GAS_FIELD_OPERATIONS_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "oil_gas_field_operations",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def oil_gas_field_operations_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next((item for item in OIL_GAS_FIELD_OPERATIONS_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": "oil_gas_field_operations",
        "form": form,
        "side_effects": (),
    }


def oil_gas_field_operations_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a form payload against required fields and enum choices."""
    form = oil_gas_field_operations_get_form(form_id).get("form")
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
        if field.get("required") and supplied.get(field["name"]) in {None, ""}
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
        "pbc": "oil_gas_field_operations",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one happy-path form validation."""
    catalog = oil_gas_field_operations_form_catalog()
    validation = oil_gas_field_operations_validate_form_payload(
        "morning_review_request",
        {
            "route_code": "ROUTE-7",
            "minimum_deferred_oil_bbl": 25.0,
            "document_text": "Review yesterday's pad performance and open exceptions.",
            "instructions": "Prepare a read-only morning production review.",
            "target_entity": "production_reading",
            "requested_action": "read",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
