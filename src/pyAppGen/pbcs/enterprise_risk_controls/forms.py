"""Package-local forms for the Enterprise Risk Controls workbench."""

from __future__ import annotations


ENTERPRISE_RISK_CONTROLS_FORM_DEFINITIONS = (
    {
        "form_id": "risk_registration",
        "title": "Register enterprise risk",
        "route": "POST /api/pbc/enterprise_risk_controls/risks",
        "operation": "register_risk",
        "permission": "enterprise_risk_controls.register_risk",
        "owned_tables": (
            "enterprise_risk_controls_risk_register",
            "enterprise_risk_controls_risk_taxonomy",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "risk_code", "type": "string", "required": True},
            {
                "name": "category",
                "type": "enum",
                "required": True,
                "choices": (
                    "strategic",
                    "financial",
                    "operational",
                    "technology",
                    "compliance",
                    "cyber",
                ),
            },
            {"name": "risk_statement", "type": "text", "required": True},
            {"name": "owner", "type": "string", "required": True},
            {"name": "appetite_linkage", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "risk_assessment",
        "title": "Assess inherent and residual risk",
        "route": "POST /api/pbc/enterprise_risk_controls/risk-assessments",
        "operation": "assess_inherent_risk",
        "permission": "enterprise_risk_controls.assess_risk",
        "owned_tables": (
            "enterprise_risk_controls_risk_assessment",
            "enterprise_risk_controls_risk_indicator_observation",
        ),
        "fields": (
            {"name": "risk_code", "type": "string", "required": True},
            {
                "name": "assessment_basis",
                "type": "enum",
                "required": True,
                "choices": ("inherent", "residual", "target"),
            },
            {"name": "likelihood", "type": "integer", "required": True},
            {"name": "impact", "type": "integer", "required": True},
            {"name": "velocity", "type": "integer", "required": True},
            {"name": "confidence", "type": "integer", "required": True},
        ),
    },
    {
        "form_id": "control_definition",
        "title": "Define control",
        "route": "POST /api/pbc/enterprise_risk_controls/controls",
        "operation": "define_control",
        "permission": "enterprise_risk_controls.manage_controls",
        "owned_tables": (
            "enterprise_risk_controls_control_library",
            "enterprise_risk_controls_control_objective",
        ),
        "fields": (
            {"name": "control_code", "type": "string", "required": True},
            {"name": "risk_code", "type": "string", "required": True},
            {
                "name": "control_type",
                "type": "enum",
                "required": True,
                "choices": ("preventive", "detective", "corrective"),
            },
            {
                "name": "automation_level",
                "type": "enum",
                "required": True,
                "choices": ("manual", "hybrid", "automated"),
            },
            {"name": "owner", "type": "string", "required": True},
            {"name": "evidence_expectation", "type": "text", "required": True},
        ),
    },
    {
        "form_id": "control_test_plan",
        "title": "Schedule control test",
        "route": "POST /api/pbc/enterprise_risk_controls/control-tests",
        "operation": "schedule_control_test",
        "permission": "enterprise_risk_controls.manage_controls",
        "owned_tables": (
            "enterprise_risk_controls_control_test",
            "enterprise_risk_controls_control_test_evidence",
        ),
        "fields": (
            {"name": "control_code", "type": "string", "required": True},
            {"name": "test_period", "type": "string", "required": True},
            {
                "name": "sampling_strategy",
                "type": "enum",
                "required": True,
                "choices": ("full_population", "risk_weighted", "judgmental"),
            },
            {"name": "tester", "type": "string", "required": True},
            {"name": "independence_confirmed", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "attestation_campaign",
        "title": "Record control attestation",
        "route": "POST /api/pbc/enterprise_risk_controls/attestations",
        "operation": "record_attestation",
        "permission": "enterprise_risk_controls.attest_controls",
        "owned_tables": (
            "enterprise_risk_controls_control_attestation",
            "enterprise_risk_controls_control_owner_assignment",
        ),
        "fields": (
            {"name": "control_code", "type": "string", "required": True},
            {"name": "campaign_id", "type": "string", "required": True},
            {"name": "attestor", "type": "string", "required": True},
            {
                "name": "attestation_outcome",
                "type": "enum",
                "required": True,
                "choices": ("certified", "certified_with_exception", "declined"),
            },
            {"name": "legal_acknowledgement", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "remediation_issue",
        "title": "Open remediation",
        "route": "POST /api/pbc/enterprise_risk_controls/remediations",
        "operation": "open_remediation",
        "permission": "enterprise_risk_controls.manage_remediation",
        "owned_tables": (
            "enterprise_risk_controls_remediation_issue",
            "enterprise_risk_controls_remediation_action",
        ),
        "fields": (
            {"name": "issue_code", "type": "string", "required": True},
            {"name": "risk_code", "type": "string", "required": True},
            {"name": "owner", "type": "string", "required": True},
            {
                "name": "severity",
                "type": "enum",
                "required": True,
                "choices": ("low", "moderate", "high", "critical"),
            },
            {"name": "target_due_date", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "assurance_packet",
        "title": "Generate assurance packet",
        "route": "POST /api/pbc/enterprise_risk_controls/assurance-packets",
        "operation": "generate_assurance_packet",
        "permission": "enterprise_risk_controls.compile_assurance",
        "owned_tables": (
            "enterprise_risk_controls_audit_evidence_packet",
            "enterprise_risk_controls_risk_committee_packet",
        ),
        "fields": (
            {"name": "packet_code", "type": "string", "required": True},
            {"name": "scope", "type": "string", "required": True},
            {"name": "control_codes", "type": "list", "required": True},
            {"name": "reviewer", "type": "string", "required": True},
            {"name": "include_hash_manifest", "type": "boolean", "required": True},
        ),
    },
    {
        "form_id": "document_instruction_intake",
        "title": "Assistant document intake",
        "route": "POST /api/pbc/enterprise_risk_controls/assistant/document-preview",
        "operation": "query_enterprise_risk_controls_assistant_preview",
        "permission": "enterprise_risk_controls.audit",
        "owned_tables": (
            "enterprise_risk_controls_risk_policy_rule",
            "enterprise_risk_controls_risk_runtime_parameter",
            "enterprise_risk_controls_risk_schema_extension",
            "enterprise_risk_controls_risk_register",
            "enterprise_risk_controls_control_library",
            "enterprise_risk_controls_remediation_issue",
            "enterprise_risk_controls_audit_evidence_packet",
        ),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {
                "name": "target_entity",
                "type": "enum",
                "required": True,
                "choices": (
                    "risk_register",
                    "risk_policy_rule",
                    "risk_runtime_parameter",
                    "control_library",
                    "control_test",
                    "remediation_issue",
                    "audit_evidence_packet",
                ),
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


def enterprise_risk_controls_form_catalog() -> dict:
    """Return the package-local workbench form registry."""
    forms = tuple(ENTERPRISE_RISK_CONTROLS_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "enterprise_risk_controls",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def enterprise_risk_controls_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next(
        (item for item in ENTERPRISE_RISK_CONTROLS_FORM_DEFINITIONS if item["form_id"] == form_id),
        None,
    )
    return {
        "ok": form is not None,
        "pbc": "enterprise_risk_controls",
        "form": form,
        "side_effects": (),
    }


def enterprise_risk_controls_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a form payload against required fields and enum choices."""
    form = enterprise_risk_controls_get_form(form_id).get("form")
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
        "pbc": "enterprise_risk_controls",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one happy-path form validation."""
    catalog = enterprise_risk_controls_form_catalog()
    validation = enterprise_risk_controls_validate_form_payload(
        "document_instruction_intake",
        {
            "document_text": "Raise the remediation SLA for critical control issues.",
            "instructions": "Update the remediation parameter for critical issues.",
            "target_entity": "risk_runtime_parameter",
            "requested_action": "update",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
