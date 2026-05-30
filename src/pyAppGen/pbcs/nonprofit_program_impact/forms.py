"""Package-local forms for the Nonprofit Program Impact standalone workbench."""

from __future__ import annotations


PBC_KEY = "nonprofit_program_impact"


NONPROFIT_PROGRAM_IMPACT_FORM_DEFINITIONS = (
    {
        "form_id": "program_portfolio_setup",
        "title": "Program portfolio setup",
        "route": "POST /app/nonprofit-program-impact/programs",
        "operation": "create_program",
        "permission": "nonprofit_program_impact.create",
        "owned_tables": (
            "nonprofit_program_impact_program",
            "nonprofit_program_impact_nonprofit_program_impact_policy_rule",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "program_id", "type": "string", "required": True},
            {"name": "name", "type": "string", "required": True},
            {"name": "theory_model", "type": "enum", "required": True, "choices": ("direct_service", "community_systems", "advocacy", "cash_assistance")},
            {"name": "target_population", "type": "string", "required": True},
            {"name": "primary_geography", "type": "string", "required": True},
            {"name": "measurement_horizon", "type": "enum", "required": True, "choices": ("90_day", "annual", "multi_year")},
            {"name": "funding_type", "type": "enum", "required": True, "choices": ("restricted", "unrestricted", "co_funded")},
            {"name": "baseline_year", "type": "integer", "required": True},
        ),
    },
    {
        "form_id": "beneficiary_enrollment",
        "title": "Beneficiary enrollment",
        "route": "POST /app/nonprofit-program-impact/beneficiaries",
        "operation": "enroll_beneficiary",
        "permission": "nonprofit_program_impact.create",
        "owned_tables": (
            "nonprofit_program_impact_beneficiary",
            "nonprofit_program_impact_program",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "program_id", "type": "string", "required": True},
            {"name": "beneficiary_id", "type": "string", "required": True},
            {"name": "beneficiary_type", "type": "enum", "required": True, "choices": ("person", "household", "caregiver_child_pair", "group", "institution")},
            {"name": "age_band", "type": "enum", "required": True, "choices": ("child", "youth", "adult", "older_adult")},
            {"name": "geography", "type": "string", "required": True},
            {"name": "vulnerability_score", "type": "integer", "required": True},
            {"name": "consent_status", "type": "enum", "required": True, "choices": ("consented", "guardian_consented", "pending", "withdrawn")},
        ),
    },
    {
        "form_id": "service_delivery_capture",
        "title": "Service delivery capture",
        "route": "POST /app/nonprofit-program-impact/service-episodes",
        "operation": "record_service_episode",
        "permission": "nonprofit_program_impact.update",
        "owned_tables": (
            "nonprofit_program_impact_service_episode",
            "nonprofit_program_impact_beneficiary",
        ),
        "fields": (
            {"name": "program_id", "type": "string", "required": True},
            {"name": "beneficiary_id", "type": "string", "required": True},
            {"name": "episode_id", "type": "string", "required": True},
            {"name": "service_type", "type": "enum", "required": True, "choices": ("counseling", "training", "cash_transfer", "referral", "mentoring", "community_outreach")},
            {"name": "delivery_channel", "type": "enum", "required": True, "choices": ("in_person", "remote", "hybrid", "partner_referral")},
            {"name": "planned_dosage", "type": "integer", "required": True},
            {"name": "delivered_dosage", "type": "integer", "required": True},
            {"name": "fidelity_status", "type": "enum", "required": True, "choices": ("on_model", "adapted", "at_risk")},
            {"name": "safeguarding_flag", "type": "enum", "required": True, "choices": ("clear", "needs_follow_up", "incident_opened")},
        ),
    },
    {
        "form_id": "outcome_follow_up",
        "title": "Outcome follow-up",
        "route": "POST /app/nonprofit-program-impact/outcomes",
        "operation": "record_outcome_observation",
        "permission": "nonprofit_program_impact.update",
        "owned_tables": (
            "nonprofit_program_impact_outcome_measure",
            "nonprofit_program_impact_impact_evidence",
        ),
        "fields": (
            {"name": "program_id", "type": "string", "required": True},
            {"name": "beneficiary_id", "type": "string", "required": True},
            {"name": "outcome_id", "type": "string", "required": True},
            {"name": "indicator_key", "type": "string", "required": True},
            {"name": "measurement_window", "type": "enum", "required": True, "choices": ("baseline", "30_day", "90_day", "annual")},
            {"name": "baseline_value", "type": "integer", "required": True},
            {"name": "target_value", "type": "integer", "required": True},
            {"name": "actual_value", "type": "integer", "required": True},
            {"name": "evidence_quality", "type": "enum", "required": True, "choices": ("weak", "moderate", "strong")},
        ),
    },
    {
        "form_id": "donor_report_freeze",
        "title": "Donor report freeze",
        "route": "POST /app/nonprofit-program-impact/donor-reports",
        "operation": "freeze_donor_report",
        "permission": "nonprofit_program_impact.approve",
        "owned_tables": (
            "nonprofit_program_impact_donor_report",
            "nonprofit_program_impact_outcome_measure",
        ),
        "fields": (
            {"name": "report_id", "type": "string", "required": True},
            {"name": "program_id", "type": "string", "required": True},
            {"name": "reporting_period", "type": "string", "required": True},
            {"name": "attribution_policy", "type": "enum", "required": True, "choices": ("direct", "proportional", "co_funded")},
            {"name": "freeze_reason", "type": "string", "required": True},
            {"name": "report_status", "type": "enum", "required": True, "choices": ("draft", "review", "frozen")},
        ),
    },
    {
        "form_id": "assistant_document_intake",
        "title": "Assistant document intake",
        "route": "POST /app/nonprofit-program-impact/assistant-preview",
        "operation": "assistant_preview",
        "permission": "nonprofit_program_impact.admin",
        "owned_tables": (
            "nonprofit_program_impact_program",
            "nonprofit_program_impact_beneficiary",
            "nonprofit_program_impact_service_episode",
            "nonprofit_program_impact_outcome_measure",
            "nonprofit_program_impact_impact_evidence",
            "nonprofit_program_impact_donor_report",
        ),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {"name": "target_entity", "type": "enum", "required": True, "choices": ("program", "beneficiary", "service_episode", "outcome_measure", "impact_evidence", "donor_report")},
            {"name": "requested_action", "type": "enum", "required": True, "choices": ("create", "read", "update", "delete")},
        ),
    },
)


def nonprofit_program_impact_form_catalog() -> dict:
    """Return the package-local workbench form registry."""
    forms = tuple(NONPROFIT_PROGRAM_IMPACT_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": PBC_KEY,
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def nonprofit_program_impact_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next((item for item in NONPROFIT_PROGRAM_IMPACT_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": PBC_KEY,
        "form": form,
        "side_effects": (),
    }


def nonprofit_program_impact_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a workbench payload against required fields, enums, and integer fields."""
    form = nonprofit_program_impact_get_form(form_id).get("form")
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
    invalid_integers = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "integer"
        and supplied.get(field["name"]) is not None
        and not isinstance(supplied.get(field["name"]), int)
    )
    return {
        "ok": not missing and not invalid_choices and not invalid_integers,
        "accepted": not missing and not invalid_choices and not invalid_integers,
        "pbc": PBC_KEY,
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "invalid_integers": invalid_integers,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one happy-path form validation."""
    catalog = nonprofit_program_impact_form_catalog()
    validation = nonprofit_program_impact_validate_form_payload(
        "assistant_document_intake",
        {
            "document_text": "Proposal narrative: six-month youth mentorship program in Nairobi.",
            "instructions": "Create a bounded preview for the program record.",
            "target_entity": "program",
            "requested_action": "create",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
