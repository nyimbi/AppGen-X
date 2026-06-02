"""Package-local controls for the Nonprofit Program Impact workbench."""

from __future__ import annotations

from . import agent
from .forms import nonprofit_program_impact_form_catalog
from .runtime import nonprofit_program_impact_build_release_evidence
from .runtime import nonprofit_program_impact_runtime_smoke
from .runtime import nonprofit_program_impact_verify_owned_table_boundary
from .wizards import nonprofit_program_impact_wizard_catalog


PBC_KEY = "nonprofit_program_impact"


NONPROFIT_PROGRAM_IMPACT_CONTROLS = (
    {
        "control_id": "theory_of_change_readiness",
        "title": "Theory of change readiness",
        "description": "Confirms each reportable program has a populated results chain, target population, and target window.",
        "permission": "nonprofit_program_impact.approve",
    },
    {
        "control_id": "eligibility_and_consent_gate",
        "title": "Eligibility and consent gate",
        "description": "Requires beneficiary eligibility to pass and consent to be usable before service evidence is counted.",
        "permission": "nonprofit_program_impact.update",
    },
    {
        "control_id": "dosage_and_fidelity_gate",
        "title": "Dosage and fidelity gate",
        "description": "Checks planned-versus-delivered dosage and flags at-risk fidelity for review.",
        "permission": "nonprofit_program_impact.update",
    },
    {
        "control_id": "evidence_quality_floor",
        "title": "Evidence quality floor",
        "description": "Ensures outcome evidence meets the configured quality threshold before donor reporting.",
        "permission": "nonprofit_program_impact.approve",
    },
    {
        "control_id": "donor_report_freeze_gate",
        "title": "Donor report freeze gate",
        "description": "Blocks report freeze when attribution, evidence quality, or period snapshots are incomplete.",
        "permission": "nonprofit_program_impact.approve",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Ensures assistant previews stay inside the nonprofit impact owned boundary and require confirmation before mutation.",
        "permission": "nonprofit_program_impact.admin",
    },
)


def _sample_state() -> dict:
    return {
        "configuration": {"database_backend": "postgresql", "event_topic": "pbc.nonprofit_program_impact.events", "retry_limit": 3},
        "parameters": {"quality_score_floor": 0.65},
        "rules": {"program_policy": {"status": "active"}},
        "programs": {
            "PROGRAM-001": {
                "program_id": "PROGRAM-001",
                "tenant": "tenant-smoke",
                "name": "Youth Skills Acceleration",
                "theory_of_change_ready": True,
                "target_population": "Out-of-school youth",
                "measurement_horizon": "annual",
                "status": "active",
            }
        },
        "beneficiaries": {
            "BEN-001": {
                "beneficiary_id": "BEN-001",
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "eligibility_passed": True,
                "consent_ready": True,
                "status": "enrolled",
            }
        },
        "service_episodes": {
            "EP-001": {
                "episode_id": "EP-001",
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "beneficiary_id": "BEN-001",
                "dosage_completion_ratio": 1.0,
                "fidelity_status": "on_model",
                "safeguarding_flag": "clear",
            }
        },
        "outcomes": {
            "OUT-001": {
                "outcome_id": "OUT-001",
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "beneficiary_id": "BEN-001",
                "attainment_ratio": 1.1,
                "evidence_quality_score": 0.85,
                "status": "on_track",
            }
        },
        "evidence_packs": {
            "EVID-001": {
                "evidence_id": "EVID-001",
                "program_id": "PROGRAM-001",
                "quality_score": 0.82,
                "verification_status": "verified",
            }
        },
        "donor_reports": {
            "REPORT-001": {
                "report_id": "REPORT-001",
                "program_id": "PROGRAM-001",
                "status": "frozen",
                "quality_gate_passed": True,
            }
        },
        "safeguarding_incidents": {},
        "outbox": ({"event_type": "NonprofitProgramImpactCreated"},),
    }


def nonprofit_program_impact_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(NONPROFIT_PROGRAM_IMPACT_CONTROLS),
        "pbc": PBC_KEY,
        "controls": NONPROFIT_PROGRAM_IMPACT_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in NONPROFIT_PROGRAM_IMPACT_CONTROLS),
        "side_effects": (),
    }


def nonprofit_program_impact_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a mutation would stay inside the nonprofit impact owned boundary."""
    normalized = str(action).lower()
    boundary = nonprofit_program_impact_verify_owned_table_boundary((table,))
    target = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    crud = agent.datastore_crud_plan(normalized, target, payload)
    requires_confirmation = normalized != "read"
    return {
        "ok": boundary["ok"] and crud["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": PBC_KEY,
        "action": normalized,
        "table": target,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": requires_confirmation,
        "boundary": boundary,
        "crud": crud,
        "side_effects": (),
    }


def nonprofit_program_impact_control_center(state: dict | None = None) -> dict:
    """Return executable control evidence for release and operator workflows."""
    source_state = dict(state or _sample_state())
    release = nonprofit_program_impact_build_release_evidence()
    runtime = nonprofit_program_impact_runtime_smoke()
    forms = nonprofit_program_impact_form_catalog()
    wizards = nonprofit_program_impact_wizard_catalog()

    programs = tuple(source_state.get("programs", {}).values())
    beneficiaries = tuple(source_state.get("beneficiaries", {}).values())
    service_episodes = tuple(source_state.get("service_episodes", {}).values())
    outcomes = tuple(source_state.get("outcomes", {}).values())
    evidence_packs = tuple(source_state.get("evidence_packs", {}).values())
    donor_reports = tuple(source_state.get("donor_reports", {}).values())
    safeguarding_incidents = tuple(source_state.get("safeguarding_incidents", {}).values())

    theory_of_change_ready = bool(programs) and all(program.get("theory_of_change_ready") for program in programs)
    eligibility_and_consent_ready = bool(beneficiaries) and all(
        beneficiary.get("eligibility_passed") and beneficiary.get("consent_ready")
        for beneficiary in beneficiaries
    )
    dosage_and_fidelity_ready = bool(service_episodes) and all(
        episode.get("dosage_completion_ratio", 0) >= 0.75 and episode.get("fidelity_status") in {"on_model", "adapted"}
        for episode in service_episodes
    )
    quality_scores = tuple(pack.get("quality_score", pack.get("evidence_quality_score", 0.0)) for pack in evidence_packs + outcomes)
    evidence_quality_floor = bool(quality_scores) and min(quality_scores) >= source_state.get("parameters", {}).get("quality_score_floor", 0.65)
    donor_report_freeze_ready = bool(donor_reports) and all(
        report.get("status") == "frozen" and report.get("quality_gate_passed")
        for report in donor_reports
    )
    safeguarding_open = tuple(
        incident for incident in safeguarding_incidents if incident.get("status") != "closed"
    ) + tuple(
        episode for episode in service_episodes if episode.get("safeguarding_flag") in {"needs_follow_up", "incident_opened"}
    )

    accepted_boundary = nonprofit_program_impact_verify_owned_table_boundary(
        ("program", "beneficiary", "service_episode", "outcome_measure", "impact_evidence", "donor_report")
    )
    rejected_boundary = nonprofit_program_impact_verify_owned_table_boundary(("shared_finance_table",))
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
        "preview": nonprofit_program_impact_mutation_preview(
            "update",
            "nonprofit_program_impact_program",
            {"program_id": "PROGRAM-001", "name": "Updated program name"},
        ),
    }
    return {
        "ok": all(
            (
                release["ok"],
                runtime["ok"],
                forms["ok"],
                wizards["ok"],
                theory_of_change_ready,
                eligibility_and_consent_ready,
                dosage_and_fidelity_ready,
                evidence_quality_floor,
                donor_report_freeze_ready,
                assistant_guardrails["boundary_ok"],
            )
        ),
        "pbc": PBC_KEY,
        "controls": nonprofit_program_impact_control_catalog()["controls"],
        "release": release,
        "runtime": runtime,
        "forms": forms,
        "wizards": wizards,
        "readiness": {
            "theory_of_change_ready": theory_of_change_ready,
            "eligibility_and_consent_ready": eligibility_and_consent_ready,
            "dosage_and_fidelity_ready": dosage_and_fidelity_ready,
            "evidence_quality_floor": evidence_quality_floor,
            "donor_report_freeze_ready": donor_report_freeze_ready,
        },
        "metrics": {
            "program_count": len(programs),
            "beneficiary_count": len(beneficiaries),
            "service_episode_count": len(service_episodes),
            "outcome_count": len(outcomes),
            "evidence_pack_count": len(evidence_packs),
            "frozen_report_count": len(tuple(report for report in donor_reports if report.get("status") == "frozen")),
            "open_safeguarding_count": len(safeguarding_open),
        },
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the control center with packaged sample evidence."""
    empty_preview = nonprofit_program_impact_mutation_preview("read", "nonprofit_program_impact_program", {})
    control_center = nonprofit_program_impact_control_center(_sample_state())
    return {
        "ok": empty_preview["ok"] and control_center["ok"],
        "preview": empty_preview,
        "control_center": control_center,
        "side_effects": (),
    }
