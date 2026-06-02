"""Package-local workflow contracts for the standalone aviation slice."""
from __future__ import annotations

from .maintenance_release import build_release_to_service_pack

PBC_KEY = "aviation_maintenance_repair"


def _step(step_id: str, label: str, status: str, detail: str, blockers: tuple[dict, ...] = ()) -> dict:
    return {
        "step_id": step_id,
        "label": label,
        "status": status,
        "detail": detail,
        "blockers": blockers,
    }


def release_to_service_workflow_contract() -> dict:
    return {
        "ok": True,
        "workflow_id": "release_to_service",
        "pbc": PBC_KEY,
        "label": "Release To Service",
        "wizard": "release_to_service_wizard",
        "permission": f"{PBC_KEY}.approve",
        "command_operation": "assess_release_to_service",
        "steps": (
            "select_aircraft",
            "reconcile_components",
            "close_work_cards",
            "resolve_deferred_defects",
            "verify_airworthiness_directives",
            "assign_certifier",
            "final_release_decision",
        ),
        "side_effects": (),
    }


def document_instruction_workflow_contract() -> dict:
    return {
        "ok": True,
        "workflow_id": "document_instruction_planning",
        "pbc": PBC_KEY,
        "label": "Document Instruction Planning",
        "wizard": "document_instruction_wizard",
        "permission": f"{PBC_KEY}.update",
        "command_operation": "plan_document_instruction",
        "steps": (
            "ingest_document",
            "classify_instruction",
            "preview_candidate_mutations",
            "route_for_human_confirmation",
        ),
        "side_effects": (),
    }


def build_release_to_service_workflow(payload: dict) -> dict:
    source = dict(payload or {})
    pack = build_release_to_service_pack(source)
    blocker_codes = {item["code"] for item in pack["blockers"]}
    steps = (
        _step(
            "select_aircraft",
            "Select Aircraft",
            "complete" if pack.get("tail_number") else "blocked",
            "Tail-specific release assessment requires a selected aircraft.",
            tuple(item for item in pack["blockers"] if item["code"] == "missing_aircraft"),
        ),
        _step(
            "reconcile_components",
            "Reconcile Components",
            "complete" if "components_airworthy" in pack["passed_checks"] else "blocked",
            "Every installed or release-critical component must be airworthy and effective.",
            tuple(item for item in pack["blockers"] if item["code"].startswith("component_") or item["code"].startswith("life_limit")),
        ),
        _step(
            "close_work_cards",
            "Close Work Cards",
            "complete" if "work_cards_closed" in pack["passed_checks"] else "blocked",
            "Routine and non-routine work cards must close with the required signoffs.",
            tuple(
                item
                for item in pack["blockers"]
                if item["code"]
                in {
                    "no_work_cards_in_release_pack",
                    "work_card_not_closed",
                    "missing_required_signoff",
                    "duplicate_inspection_missing",
                    "self_inspection_blocked",
                    "technician_not_authorized",
                    "technician_authorization_expired",
                    "controlled_tool_not_returned",
                    "tool_calibration_expired",
                    "consumable_expired",
                    "consumable_mix_life_expired",
                    "open_non_routine_work",
                }
            ),
        ),
        _step(
            "resolve_deferred_defects",
            "Resolve Deferred Defects",
            "complete" if "deferred_defects_within_limits" in pack["passed_checks"] else "blocked",
            "Deferred defects must remain within their approved interval.",
            tuple(item for item in pack["blockers"] if item["code"] == "deferred_defect_expired"),
        ),
        _step(
            "verify_airworthiness_directives",
            "Verify Airworthiness Directives",
            "complete" if "airworthiness_directives_complied" in pack["passed_checks"] else "blocked",
            "Applicable directives require compliance evidence before release.",
            tuple(item for item in pack["blockers"] if item["code"] == "airworthiness_directive_open"),
        ),
        _step(
            "assign_certifier",
            "Assign Certifier",
            "complete" if "human_certifier_present" in pack["passed_checks"] else "blocked",
            "A human certifier with release authorization must review the pack.",
            tuple(item for item in pack["blockers"] if item["code"] == "human_certifier_required"),
        ),
        _step(
            "final_release_decision",
            "Final Release Decision",
            "complete" if pack["ok"] else "blocked",
            "The release gate passes only when every evidence check is satisfied.",
            pack["blockers"],
        ),
    )
    denominator = len(pack["passed_checks"] + pack["pending_checks"]) or 1
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "workflow_id": "release_to_service",
        "status": "release_ready" if pack["ok"] else "blocked",
        "readiness_score": round(len(pack["passed_checks"]) / denominator, 2),
        "next_action": "issue_release" if pack["ok"] else "resolve_blockers",
        "steps": steps,
        "blocking_codes": tuple(sorted(blocker_codes)),
        "release_pack": pack,
        "side_effects": (),
    }


def workflow_catalog() -> dict:
    workflows = (
        release_to_service_workflow_contract(),
        document_instruction_workflow_contract(),
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "workflows": workflows,
        "wizard_ids": tuple(item["wizard"] for item in workflows),
        "side_effects": (),
    }
