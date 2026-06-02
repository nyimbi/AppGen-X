"""Package-local forms for the Professional Services Automation workbench."""

from __future__ import annotations


PROFESSIONAL_SERVICES_AUTOMATION_FORM_DEFINITIONS = (
    {
        "form_id": "engagement_intake",
        "title": "Open engagement",
        "route": "POST /engagements",
        "operation": "create_engagement",
        "permission": "professional_services_automation.create",
        "owned_tables": (
            "professional_services_automation_engagement",
            "professional_services_automation_statement_of_work",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "engagement_id", "type": "string", "required": True},
            {"name": "client_name", "type": "string", "required": True},
            {
                "name": "engagement_archetype",
                "type": "enum",
                "required": True,
                "choices": (
                    "fixed_price_implementation",
                    "time_and_materials_advisory",
                    "managed_service",
                    "retainer",
                ),
            },
            {"name": "start_date", "type": "date", "required": True},
            {"name": "delivery_manager", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "sow_semantic_intake",
        "title": "Parse SOW",
        "route": "POST /statements-of-work",
        "operation": "register_statement_of_work",
        "permission": "professional_services_automation.create",
        "owned_tables": (
            "professional_services_automation_statement_of_work",
            "professional_services_automation_engagement_exception_case",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "engagement_id", "type": "string", "required": True},
            {"name": "sow_id", "type": "string", "required": True},
            {"name": "document_text", "type": "text", "required": True},
            {"name": "assumptions_present", "type": "boolean", "required": True},
            {"name": "requires_change_control", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "staffing_request",
        "title": "Staffing request",
        "route": "POST /staffing",
        "operation": "open_staffing_request",
        "permission": "professional_services_automation.update",
        "owned_tables": (
            "professional_services_automation_staffing_request",
            "professional_services_automation_consultant_skill_profile",
            "professional_services_automation_staffing_assignment",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "engagement_id", "type": "string", "required": True},
            {"name": "request_id", "type": "string", "required": True},
            {"name": "role_code", "type": "string", "required": True},
            {"name": "start_week", "type": "string", "required": True},
            {"name": "allocation_percent", "type": "integer", "required": True},
            {"name": "required_skills", "type": "list", "required": True},
        ),
    },
    {
        "form_id": "time_and_expense_review",
        "title": "Time and expense review",
        "route": "GET /services-automation-workbench",
        "operation": "capture_time_entry",
        "permission": "professional_services_automation.update",
        "owned_tables": (
            "professional_services_automation_time_entry",
            "professional_services_automation_expense_link",
            "professional_services_automation_billing_readiness_check",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "engagement_id", "type": "string", "required": True},
            {"name": "time_entry_id", "type": "string", "required": True},
            {"name": "billable_hours", "type": "number", "required": True},
            {"name": "narrative", "type": "text", "required": True},
            {"name": "expense_approved", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "billing_readiness_gate",
        "title": "Billing readiness gate",
        "route": "POST /billing-milestones",
        "operation": "run_billing_readiness",
        "permission": "professional_services_automation.approve",
        "owned_tables": (
            "professional_services_automation_billing_schedule",
            "professional_services_automation_billing_readiness_check",
            "professional_services_automation_client_acceptance",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "engagement_id", "type": "string", "required": True},
            {"name": "billing_schedule_id", "type": "string", "required": True},
            {"name": "approved_time_complete", "type": "boolean", "required": True},
            {"name": "accepted_deliverables_complete", "type": "boolean", "required": True},
            {"name": "open_scope_exceptions", "type": "integer", "required": True},
        ),
    },
    {
        "form_id": "document_instruction_preview",
        "title": "Assistant document preview",
        "route": "GET /services-automation-workbench",
        "operation": "parse_document_instruction",
        "permission": "professional_services_automation.read",
        "owned_tables": (
            "professional_services_automation_statement_of_work",
            "professional_services_automation_psa_policy_rule",
            "professional_services_automation_psa_runtime_parameter",
        ),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instruction", "type": "text", "required": True},
            {
                "name": "requested_action",
                "type": "enum",
                "required": True,
                "choices": ("create", "read", "update", "delete"),
            },
            {
                "name": "target_entity",
                "type": "enum",
                "required": True,
                "choices": (
                    "statement_of_work",
                    "staffing_request",
                    "psa_policy_rule",
                    "psa_runtime_parameter",
                ),
            },
        ),
    },
)



def professional_services_automation_form_catalog() -> dict:
    """Return the package-local workbench form registry."""
    forms = tuple(PROFESSIONAL_SERVICES_AUTOMATION_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "professional_services_automation",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }



def professional_services_automation_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next(
        (item for item in PROFESSIONAL_SERVICES_AUTOMATION_FORM_DEFINITIONS if item["form_id"] == form_id),
        None,
    )
    return {
        "ok": form is not None,
        "pbc": "professional_services_automation",
        "form": form,
        "side_effects": (),
    }



def professional_services_automation_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a form payload against required fields and enum choices."""
    form = professional_services_automation_get_form(form_id).get("form")
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
        "pbc": "professional_services_automation",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise one happy-path form validation."""
    catalog = professional_services_automation_form_catalog()
    validation = professional_services_automation_validate_form_payload(
        "document_instruction_preview",
        {
            "document_text": "Client requested additional data migration support.",
            "instruction": "Preview the change-control impact and staffing updates.",
            "requested_action": "update",
            "target_entity": "statement_of_work",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
