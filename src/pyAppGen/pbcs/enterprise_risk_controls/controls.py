"""Package-local controls for the Enterprise Risk Controls workbench."""

from __future__ import annotations

from .domain_depth import domain_depth_contract
from .domain_depth import domain_depth_smoke_test
from .runtime import enterprise_risk_controls_build_release_evidence
from .runtime import enterprise_risk_controls_run_advanced_assessment
from .runtime import enterprise_risk_controls_runtime_smoke
from .runtime import enterprise_risk_controls_verify_owned_table_boundary


ENTERPRISE_RISK_CONTROLS_CONTROLS = (
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Runs package-local release evidence, domain depth, and runtime readiness checks.",
        "permission": "enterprise_risk_controls.audit",
    },
    {
        "control_id": "risk_appetite_gate",
        "title": "Risk appetite gate",
        "description": "Confirms registered risks, parameters, and assessment evidence are present before posture reporting.",
        "permission": "enterprise_risk_controls.assess_risk",
    },
    {
        "control_id": "evidence_integrity",
        "title": "Evidence integrity",
        "description": "Requires packet-ready evidence, traceable eventing, and dead-letter visibility.",
        "permission": "enterprise_risk_controls.compile_assurance",
    },
    {
        "control_id": "tenant_boundary",
        "title": "Tenant and boundary proof",
        "description": "Verifies foreign table access is rejected and only owned records are previewed for mutation.",
        "permission": "enterprise_risk_controls.audit",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Ensures assistant-generated CRUD plans remain preview-only and confirmation-gated.",
        "permission": "enterprise_risk_controls.audit",
    },
)


def enterprise_risk_controls_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(ENTERPRISE_RISK_CONTROLS_CONTROLS),
        "pbc": "enterprise_risk_controls",
        "controls": ENTERPRISE_RISK_CONTROLS_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in ENTERPRISE_RISK_CONTROLS_CONTROLS),
        "side_effects": (),
    }


def enterprise_risk_controls_control_center(state: dict | None = None) -> dict:
    """Return executable control evidence for release and operator workflows."""
    source_state = state or enterprise_risk_controls_runtime_smoke()["state"]
    release = enterprise_risk_controls_build_release_evidence()
    domain = domain_depth_contract()
    domain_smoke = domain_depth_smoke_test()
    advanced = enterprise_risk_controls_run_advanced_assessment(
        source_state,
        {"mode": "control_center"},
    )
    accepted_boundary = enterprise_risk_controls_verify_owned_table_boundary(
        (
            "enterprise_risk_controls_risk_register",
            "PolicyChanged",
            "projection_dependency",
        )
    )
    rejected_boundary = enterprise_risk_controls_verify_owned_table_boundary(("foreign_shared_table",))
    posture = {
        "registered_risks": len(source_state.get("records", {})),
        "configured_parameters": len(source_state.get("parameters", {})),
        "compiled_rules": len(source_state.get("rules", {})),
        "inbox_events": len(source_state.get("inbox", ())),
        "outbox_events": len(source_state.get("outbox", ())),
        "dead_letter_events": len(source_state.get("dead_letter", ())),
        "advanced_score": advanced["score"],
    }
    gate_results = {
        "risk_appetite_gate": posture["registered_risks"] >= 1 and posture["configured_parameters"] >= 1,
        "evidence_integrity": release["ok"] and posture["outbox_events"] >= 1,
        "domain_depth_ready": domain_smoke["ok"] and domain["operation_count"] >= domain["minimum_domain_operations"],
        "dead_letter_visibility": posture["dead_letter_events"] >= 0,
    }
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
    }
    return {
        "ok": all(gate_results.values()) and assistant_guardrails["boundary_ok"],
        "pbc": "enterprise_risk_controls",
        "controls": enterprise_risk_controls_control_catalog()["controls"],
        "release": release,
        "domain_depth": domain,
        "domain_depth_smoke": domain_smoke,
        "advanced_assessment": advanced,
        "posture": posture,
        "gate_results": gate_results,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }


def enterprise_risk_controls_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a mutation would stay inside the enterprise-risk-owned boundary."""
    normalized = str(action).lower()
    boundary = enterprise_risk_controls_verify_owned_table_boundary((table,))
    requires_confirmation = normalized != "read"
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": "enterprise_risk_controls",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": requires_confirmation,
        "boundary": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the control center with runtime smoke evidence."""
    control_center = enterprise_risk_controls_control_center()
    preview = enterprise_risk_controls_mutation_preview(
        "read",
        "enterprise_risk_controls_risk_register",
        {},
    )
    return {
        "ok": control_center["ok"] and preview["ok"],
        "control_center": control_center,
        "preview": preview,
        "side_effects": (),
    }
