"""Package-local controls for the standalone ar_credit workbench."""

from __future__ import annotations

from .receivables_workflows import ar_credit_build_collections_follow_up
from .runtime import ar_credit_build_release_evidence
from .runtime import ar_credit_build_workbench_view
from .runtime import ar_credit_empty_state
from .runtime import ar_credit_run_control_tests
from .runtime import ar_credit_verify_formal_invariants
from .runtime import ar_credit_verify_owned_table_boundary
from .seed_data import load_demo_state


AR_CREDIT_CONTROLS = (
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Runs runtime release evidence and confirms standalone surface coverage.",
        "permission": "ar_credit.audit",
    },
    {
        "control_id": "invoice_gate",
        "title": "Invoice completeness gate",
        "description": "Confirms invoice issuance keeps customer, tax, obligation, and credit checks intact.",
        "permission": "ar_credit.invoice",
    },
    {
        "control_id": "cash_application_guardrails",
        "title": "Cash application guardrails",
        "description": "Verifies remittance parsing, unapplied-cash fallback, and duplicate receipt protection.",
        "permission": "ar_credit.cash",
    },
    {
        "control_id": "tenant_boundary",
        "title": "Owned-boundary proof",
        "description": "Rejects foreign table references and keeps AppGen-X as the only event contract.",
        "permission": "ar_credit.audit",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Ensures previews stay confirmation-gated and package-owned.",
        "permission": "ar_credit.audit",
    },
)


def ar_credit_control_catalog() -> dict:
    return {
        "ok": bool(AR_CREDIT_CONTROLS),
        "pbc": "ar_credit",
        "controls": AR_CREDIT_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in AR_CREDIT_CONTROLS),
        "side_effects": (),
    }


def ar_credit_control_center(
    state: dict | None = None,
    *,
    tenant: str = "tenant_demo",
    as_of: str = "2026-06-30",
) -> dict:
    source_state = state or load_demo_state(tenant=tenant)["state"]
    release = ar_credit_build_release_evidence()
    runtime_controls = ar_credit_run_control_tests(source_state)
    invariants = ar_credit_verify_formal_invariants(source_state)
    accepted_boundary = ar_credit_verify_owned_table_boundary((
        "ar_customer",
        "ar_invoice",
        "ar_cash_application",
        "CustomerOnboarded",
        "GET /customer_360/customers/{id}/profile",
    ))
    rejected_boundary = ar_credit_verify_owned_table_boundary(("gl_core_journal_entry", "shared_customer_master"))
    workbench = ar_credit_build_workbench_view(source_state, tenant=tenant, as_of=as_of)
    follow_up = ar_credit_build_collections_follow_up(source_state, customer_id=f"cust-{tenant}", as_of=as_of)
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
        "appgen_x_only": release["api"]["event_contract"] == "AppGen-X",
    }
    return {
        "ok": runtime_controls["ok"]
        and invariants["ok"]
        and release["ok"]
        and accepted_boundary["ok"]
        and not rejected_boundary["ok"]
        and workbench["ok"]
        and follow_up["ok"],
        "pbc": "ar_credit",
        "controls": ar_credit_control_catalog()["controls"],
        "release": release,
        "runtime_controls": runtime_controls,
        "invariants": invariants,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "workbench": workbench,
        "follow_up": follow_up,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }


def ar_credit_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    normalized = str(action).lower()
    boundary = ar_credit_verify_owned_table_boundary((table,))
    requires_confirmation = normalized != "read"
    return {
        "ok": normalized in {"create", "read", "update", "delete"} and boundary["ok"],
        "pbc": "ar_credit",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": requires_confirmation,
        "boundary": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    preview = ar_credit_mutation_preview("update", "ar_invoice", {"status": "issued"})
    center = ar_credit_control_center(ar_credit_empty_state() | load_demo_state()["state"])
    return {
        "ok": preview["ok"] and center["ok"],
        "preview": preview,
        "control_center": center,
        "side_effects": (),
    }
