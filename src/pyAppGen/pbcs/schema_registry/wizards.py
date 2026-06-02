"""Workflow wizards for the schema_registry standalone PBC."""

from __future__ import annotations

from .forms import schema_registry_form_catalog
from .forms import schema_registry_form_submission_plan


PBC_KEY = "schema_registry"

WIZARD_CATALOG = (
    {
        "key": "subject_onboarding_wizard",
        "title": "Subject Onboarding",
        "goal": "Configure the registry, register a subject, publish its first schema version, and expose it to downstream consumers.",
        "steps": (
            "runtime_configuration_form",
            "subject_registration_form",
            "schema_version_form",
            "consumer_binding_form",
            "projection_publish_form",
        ),
        "required_permissions": (
            "schema_registry.configure",
            "schema_registry.register",
            "schema_registry.publish",
        ),
    },
    {
        "key": "breaking_change_review_wizard",
        "title": "Breaking Change Review",
        "goal": "Simulate a contract change, quantify blast radius, record a governed violation, and route remediation through the assistant.",
        "steps": (
            "compatibility_check_form",
            "violation_triage_form",
            "assistant_intake_form",
        ),
        "required_permissions": (
            "schema_registry.validate",
            "schema_registry.triage",
            "schema_registry.read",
        ),
    },
    {
        "key": "release_gate_wizard",
        "title": "Release Gate Readiness",
        "goal": "Validate payload samples, publish contract projections, and capture the evidence required for a release gate decision.",
        "steps": (
            "payload_validation_form",
            "projection_publish_form",
            "assistant_intake_form",
        ),
        "required_permissions": (
            "schema_registry.validate",
            "schema_registry.publish",
            "schema_registry.audit",
        ),
    },
)


def schema_registry_wizard_catalog() -> tuple[dict, ...]:
    return WIZARD_CATALOG


def schema_registry_wizard_keys() -> tuple[str, ...]:
    return tuple(wizard["key"] for wizard in WIZARD_CATALOG)


def schema_registry_wizard_plan(wizard_key: str, payload: dict | None = None) -> dict:
    wizard = next((item for item in WIZARD_CATALOG if item["key"] == wizard_key), None)
    if wizard is None:
        return {
            "ok": False,
            "pbc": PBC_KEY,
            "wizard_key": wizard_key,
            "reason": "unknown_wizard",
            "side_effects": (),
        }
    supplied = dict(payload or {})
    form_index = {form["key"]: form for form in schema_registry_form_catalog()}
    steps = []
    missing_forms = []
    for step in wizard["steps"]:
        form = form_index.get(step)
        if form is None:
            missing_forms.append(step)
            continue
        step_payload = supplied.get(step, {})
        plan = schema_registry_form_submission_plan(step, step_payload)
        steps.append(
            {
                "form_key": step,
                "title": form["title"],
                "command": form["command"],
                "permission": form["permission"],
                "writes": form["writes"],
                "ready": plan["ok"],
                "missing_fields": plan["missing_fields"],
            }
        )
    return {
        "ok": not missing_forms,
        "pbc": PBC_KEY,
        "wizard_key": wizard_key,
        "title": wizard["title"],
        "goal": wizard["goal"],
        "required_permissions": wizard["required_permissions"],
        "steps": tuple(steps),
        "missing_forms": tuple(missing_forms),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise onboarding and release-gate wizard planning."""
    onboarding = schema_registry_wizard_plan(
        "subject_onboarding_wizard",
        {
            "runtime_configuration_form": {
                "database_backend": "postgresql",
                "event_topic": "appgen.schema.events",
                "retry_limit": 3,
            },
            "subject_registration_form": {
                "subject_id": "subject_smoke",
                "tenant": "tenant_smoke",
                "owner_pbc": "schema_registry",
                "name": "tenant_smoke.order.created",
                "channel": "event",
                "format": "json",
                "namespace": "tenant_smoke.orders",
            },
            "schema_version_form": {
                "version_id": "version_smoke",
                "tenant": "tenant_smoke",
                "subject_id": "subject_smoke",
                "semantic_version": "1.0.0",
                "schema": {"fields": {"order_id": {"type": "string", "required": True}}},
            },
            "consumer_binding_form": {
                "binding_id": "binding_smoke",
                "tenant": "tenant_smoke",
                "subject_id": "subject_smoke",
                "consumer_pbc": "api_gateway_mesh",
                "consumer_type": "projection",
                "min_version": "1.0.0",
            },
            "projection_publish_form": {"subject_id": "subject_smoke", "systems": ("gateway", "audit")},
        },
    )
    release = schema_registry_wizard_plan("release_gate_wizard")
    return {
        "ok": onboarding["ok"] and release["ok"],
        "wizards": WIZARD_CATALOG,
        "onboarding": onboarding,
        "release": release,
        "side_effects": (),
    }
