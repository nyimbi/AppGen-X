"""Package-local controls for the Livestock Herd Management standalone slice."""

from __future__ import annotations

from .runtime import livestock_herd_management_build_release_evidence
from .runtime import livestock_herd_management_verify_owned_table_boundary


PBC_KEY = "livestock_herd_management"


LIVESTOCK_HERD_MANAGEMENT_CONTROLS = (
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Verifies package-local release evidence, standalone coverage, and documentation presence.",
        "permission": f"{PBC_KEY}.admin",
    },
    {
        "control_id": "biosecurity_gate",
        "title": "Biosecurity gate",
        "description": "Blocks movements for animals with open quarantine or weak biosecurity audit scores.",
        "permission": f"{PBC_KEY}.approve",
    },
    {
        "control_id": "traceability_integrity",
        "title": "Traceability integrity",
        "description": "Requires identity continuity, trace lots, and source provenance for active animals.",
        "permission": f"{PBC_KEY}.read",
    },
    {
        "control_id": "welfare_and_withdrawal",
        "title": "Welfare and withdrawal",
        "description": "Flags unresolved low welfare scores and product releases during active withdrawal windows.",
        "permission": f"{PBC_KEY}.update",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Keeps preview-only CRUD planning within package-owned tables and confirmation gates.",
        "permission": f"{PBC_KEY}.admin",
    },
)


def _default_state() -> dict:
    return {
        "animals": {
            "cow-001": {
                "animal_id": "cow-001",
                "status": "active",
                "primary_identifier": "RFID-001",
                "tag_history": ({"identifier": "RFID-001", "status": "active"},),
                "source_provenance": "born_on_farm",
            }
        },
        "movement_permits": {},
        "quarantines": {},
        "biosecurity_audits": {"audit-001": {"biosecurity_score": 0.96, "status": "pass"}},
        "traceability_chains": {"trace-001": {"animal_id": "cow-001", "lot_id": "lot-milk-001"}},
        "welfare_assessments": {"welfare-001": {"animal_id": "cow-001", "welfare_score": 0.88, "status": "clear"}},
        "health_treatments": {},
        "vaccinations": {},
        "inventory_yields": {},
        "assistant_previews": {},
    }


def livestock_herd_management_control_catalog() -> dict:
    """Return standalone operational controls for livestock workflows."""
    return {
        "ok": bool(LIVESTOCK_HERD_MANAGEMENT_CONTROLS),
        "pbc": PBC_KEY,
        "controls": LIVESTOCK_HERD_MANAGEMENT_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in LIVESTOCK_HERD_MANAGEMENT_CONTROLS),
        "side_effects": (),
    }


def livestock_herd_management_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a livestock mutation stays inside the owned boundary."""
    normalized = str(action).lower()
    boundary = livestock_herd_management_verify_owned_table_boundary((table,))
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": PBC_KEY,
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized != "read",
        "boundary": boundary,
        "preview_only": True,
        "side_effects": (),
    }


def livestock_herd_management_control_center(state: dict | None = None) -> dict:
    """Return executable control evidence for the standalone livestock slice."""
    source_state = dict(_default_state() if state is None else state)
    animals = source_state.get("animals", {})
    quarantines = source_state.get("quarantines", {})
    movements = source_state.get("movement_permits", {})
    biosecurity = source_state.get("biosecurity_audits", {})
    traceability = source_state.get("traceability_chains", {})
    welfare = source_state.get("welfare_assessments", {})
    treatments = source_state.get("health_treatments", {})
    yields = source_state.get("inventory_yields", {})

    active_animal_ids = tuple(animal_id for animal_id, animal in animals.items() if animal.get("status") != "deceased")
    quarantine_blockers = tuple(
        permit_id
        for permit_id, permit in movements.items()
        if permit.get("animal_id") in {item.get("animal_id") for item in quarantines.values() if item.get("status") == "open"}
    )
    low_biosecurity = tuple(
        audit_id for audit_id, audit in biosecurity.items() if audit.get("biosecurity_score", 0.0) < 0.8
    )
    missing_traceability = tuple(
        animal_id
        for animal_id in active_animal_ids
        if animal_id not in {entry.get("animal_id") for entry in traceability.values()}
        or not animals[animal_id].get("tag_history")
        or not animals[animal_id].get("source_provenance")
    )
    welfare_watch = tuple(
        assessment_id for assessment_id, assessment in welfare.items() if assessment.get("welfare_score", 1.0) < 0.7
    )
    withdrawal_violations = tuple(
        yield_id
        for yield_id, yield_record in yields.items()
        if yield_record.get("animal_id") in {
            treatment.get("animal_id")
            for treatment in treatments.values()
            if treatment.get("withdrawal_active")
        }
    )
    assistant_guardrails = livestock_herd_management_mutation_preview(
        "update",
        "livestock_herd_management_animal",
        {"animal_id": "cow-001"},
    )
    rejected_boundary = livestock_herd_management_mutation_preview("update", "foreign_table", {"animal_id": "cow-001"})
    release = livestock_herd_management_build_release_evidence()
    return {
        "ok": not quarantine_blockers and not low_biosecurity and not missing_traceability and not welfare_watch and not withdrawal_violations and assistant_guardrails["ok"] and not rejected_boundary["ok"] and release["ok"],
        "pbc": PBC_KEY,
        "controls": livestock_herd_management_control_catalog()["controls"],
        "release": release,
        "quarantine_blockers": quarantine_blockers,
        "low_biosecurity": low_biosecurity,
        "missing_traceability": missing_traceability,
        "welfare_watch": welfare_watch,
        "withdrawal_violations": withdrawal_violations,
        "assistant_guardrails": assistant_guardrails,
        "rejected_boundary": rejected_boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise control-center evidence and owned-boundary previews."""
    preview = livestock_herd_management_mutation_preview(
        "create",
        "livestock_herd_management_health_event",
        {"health_event_id": "he-001"},
    )
    control_center = livestock_herd_management_control_center()
    return {
        "ok": preview["ok"] and control_center["ok"],
        "preview": preview,
        "control_center": control_center,
        "side_effects": (),
    }
