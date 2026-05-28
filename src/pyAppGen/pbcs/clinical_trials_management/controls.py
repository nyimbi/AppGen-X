"""Package-local controls for the Clinical Trials Management workbench."""

from __future__ import annotations

from .runtime import clinical_trials_management_assess_lock_readiness
from .runtime import clinical_trials_management_build_release_evidence
from .runtime import clinical_trials_management_empty_state
from .runtime import clinical_trials_management_run_control_tests
from .runtime import clinical_trials_management_runtime_smoke
from .runtime import clinical_trials_management_verify_formal_invariants
from .runtime import clinical_trials_management_verify_owned_table_boundary


CLINICAL_TRIALS_MANAGEMENT_CONTROLS = (
    {
        "control_id": "eligibility_and_consent_gate",
        "title": "Eligibility and consent gate",
        "description": "Prevents enrollment or visit work when eligibility evidence or current consent is missing.",
        "permission": "clinical_trials_management.audit",
    },
    {
        "control_id": "site_activation_gate",
        "title": "Site activation gate",
        "description": "Requires ethics approval, contract execution, training, and delegation evidence before activation.",
        "permission": "clinical_trials_management.audit",
    },
    {
        "control_id": "safety_reporting_sla",
        "title": "Safety reporting SLA",
        "description": "Flags serious adverse events that miss reporting clocks or unresolved follow-up evidence.",
        "permission": "clinical_trials_management.safety_review",
    },
    {
        "control_id": "data_lock_readiness",
        "title": "Data lock readiness",
        "description": "Summarizes open queries, findings, consent mismatches, and visit blockers before lock.",
        "permission": "clinical_trials_management.lock_review",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Ensures document-driven CRUD previews stay package-owned, preview-only, and confirmation-gated.",
        "permission": "clinical_trials_management.audit",
    },
)


def clinical_trials_management_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(CLINICAL_TRIALS_MANAGEMENT_CONTROLS),
        "pbc": "clinical_trials_management",
        "controls": CLINICAL_TRIALS_MANAGEMENT_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in CLINICAL_TRIALS_MANAGEMENT_CONTROLS),
        "side_effects": (),
    }


def clinical_trials_management_control_center(state: dict | None = None) -> dict:
    """Return executable control evidence for release and trial-operations workflows."""
    source_state = state
    if source_state is None:
        source_state = clinical_trials_management_runtime_smoke()["state"]
    if not source_state:
        source_state = clinical_trials_management_empty_state()

    release = clinical_trials_management_build_release_evidence()
    runtime_controls = clinical_trials_management_run_control_tests(source_state)
    invariants = clinical_trials_management_verify_formal_invariants(source_state)
    lock_readiness = clinical_trials_management_assess_lock_readiness(source_state)
    accepted_boundary = clinical_trials_management_verify_owned_table_boundary(("trial_protocol", "study_site", "monitoring_finding"))
    rejected_boundary = clinical_trials_management_verify_owned_table_boundary(("ehr_patient_projection",))
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
    }
    return {
        "ok": runtime_controls["ok"] and invariants["ok"] and release["ok"] and assistant_guardrails["boundary_ok"],
        "pbc": "clinical_trials_management",
        "controls": clinical_trials_management_control_catalog()["controls"],
        "release": release,
        "runtime_controls": runtime_controls,
        "invariants": invariants,
        "lock_readiness": lock_readiness,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }


def clinical_trials_management_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a mutation stays inside the clinical trials owned boundary."""
    normalized = str(action).lower()
    boundary = clinical_trials_management_verify_owned_table_boundary((table,))
    requires_confirmation = normalized != "read"
    regulatory_facing = table == "clinical_trials_management_adverse_event"
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": "clinical_trials_management",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": requires_confirmation,
        "citation_required": regulatory_facing,
        "boundary": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the control center with runtime smoke evidence."""
    preview = clinical_trials_management_mutation_preview("update", "clinical_trials_management_trial_protocol", {"status": "active"})
    control_center = clinical_trials_management_control_center(clinical_trials_management_runtime_smoke()["state"])
    return {
        "ok": preview["ok"] and control_center["ok"],
        "preview": preview,
        "control_center": control_center,
        "side_effects": (),
    }
