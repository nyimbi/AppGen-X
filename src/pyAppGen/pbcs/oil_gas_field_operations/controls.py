"""Package-local controls for the Oil and Gas Field Operations workbench."""

from __future__ import annotations

from pathlib import Path

from .forms import oil_gas_field_operations_form_catalog
from .runtime import oil_gas_field_operations_runtime_smoke
from .runtime import oil_gas_field_operations_verify_owned_table_boundary
from .wizards import oil_gas_field_operations_wizard_catalog


OIL_GAS_FIELD_OPERATIONS_CONTROLS = (
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Confirms docs, runtime smoke, and package-local app surfaces are present.",
        "permission": "oil_gas_field_operations.admin",
    },
    {
        "control_id": "production_balance_guardrail",
        "title": "Production balance guardrail",
        "description": "Flags deferred production, invalid tests, or missing dispositions before allocation close.",
        "permission": "oil_gas_field_operations.approve",
    },
    {
        "control_id": "integrity_followup",
        "title": "Integrity follow-up",
        "description": "Escalates wells with high integrity risk or unresolved barrier issues.",
        "permission": "oil_gas_field_operations.update",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Keeps assistant actions preview-only and inside oil_gas_field_operations owned tables.",
        "permission": "oil_gas_field_operations.read",
    },
    {
        "control_id": "ticket_reconciliation",
        "title": "Ticket reconciliation",
        "description": "Ensures high-severity tickets and reportable HSE events stay visible on the workbench.",
        "permission": "oil_gas_field_operations.read",
    },
)


def _default_state() -> dict:
    return {
        "wells": {},
        "production_records": {},
        "field_tickets": {},
        "workover_packs": {},
        "hse_events": {},
    }


def oil_gas_field_operations_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(OIL_GAS_FIELD_OPERATIONS_CONTROLS),
        "pbc": "oil_gas_field_operations",
        "controls": OIL_GAS_FIELD_OPERATIONS_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in OIL_GAS_FIELD_OPERATIONS_CONTROLS),
        "side_effects": (),
    }


def oil_gas_field_operations_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a mutation would stay inside the package-owned boundary."""
    normalized = str(action).lower()
    boundary = oil_gas_field_operations_verify_owned_table_boundary((table,))
    requires_confirmation = normalized != "read"
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": "oil_gas_field_operations",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": requires_confirmation,
        "boundary": boundary,
        "side_effects": (),
    }


def oil_gas_field_operations_control_center(state: dict | None = None) -> dict:
    """Return executable control evidence for release and operator workflows."""
    source_state = _default_state() | dict(state or {})
    runtime = oil_gas_field_operations_runtime_smoke()
    forms = oil_gas_field_operations_form_catalog()
    wizards = oil_gas_field_operations_wizard_catalog()
    docs_present = {
        name: (Path(__file__).resolve().parent / name).exists()
        for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md")
    }
    accepted_boundary = oil_gas_field_operations_verify_owned_table_boundary(("oil_gas_field_operations_well",))
    rejected_boundary = oil_gas_field_operations_verify_owned_table_boundary(("foreign_table",))

    production_records = tuple(source_state.get("production_records", {}).values())
    field_tickets = tuple(source_state.get("field_tickets", {}).values())
    wells = tuple(source_state.get("wells", {}).values())
    hse_events = tuple(source_state.get("hse_events", {}).values())

    production_balance_guardrail = {
        "allocation_ready_records": sum(1 for item in production_records if item.get("production_test_state") == "allocation_approved"),
        "records_missing_disposition": sum(1 for item in production_records if not item.get("gas_disposition") or not item.get("oil_disposition")),
        "records_with_deferred_oil": sum(1 for item in production_records if float(item.get("deferred_oil_bbl", 0.0)) > 0.0),
    }
    integrity_followup = {
        "high_risk_wells": sum(1 for item in wells if item.get("integrity_risk") == "high"),
        "watch_wells": sum(1 for item in wells if item.get("integrity_risk") == "watch"),
        "workover_candidates": sum(1 for item in source_state.get("workover_packs", {}).values() if item.get("status") == "ready"),
    }
    ticket_reconciliation = {
        "open_high_severity_tickets": sum(
            1
            for item in field_tickets
            if item.get("severity") in {"high", "critical"} and item.get("status", "open") == "open"
        ),
        "reportable_hse_events": sum(1 for item in hse_events if item.get("reportable")),
    }
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
    }
    return {
        "ok": runtime["ok"] and forms["ok"] and wizards["ok"] and all(docs_present.values()) and assistant_guardrails["boundary_ok"],
        "pbc": "oil_gas_field_operations",
        "controls": oil_gas_field_operations_control_catalog()["controls"],
        "runtime": runtime,
        "forms": forms,
        "wizards": wizards,
        "docs_present": docs_present,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "production_balance_guardrail": production_balance_guardrail,
        "integrity_followup": integrity_followup,
        "ticket_reconciliation": ticket_reconciliation,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the control center with representative state."""
    preview = oil_gas_field_operations_mutation_preview("update", "oil_gas_field_operations_field_ticket", {"ticket_id": "FT-7"})
    control_center = oil_gas_field_operations_control_center(
        {
            "wells": {"WELL-7H": {"well_id": "WELL-7H", "integrity_risk": "watch"}},
            "production_records": {
                "WELL-7H:2026-05-29": {
                    "well_id": "WELL-7H",
                    "production_test_state": "allocation_approved",
                    "oil_disposition": "sold",
                    "gas_disposition": "sales",
                    "deferred_oil_bbl": 12.0,
                }
            },
        }
    )
    return {
        "ok": preview["ok"] and control_center["ok"],
        "preview": preview,
        "control_center": control_center,
        "side_effects": (),
    }
