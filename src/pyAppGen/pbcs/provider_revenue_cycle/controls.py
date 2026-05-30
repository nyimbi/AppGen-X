"""Package-local controls and assistant mutation previews for provider_revenue_cycle."""

from __future__ import annotations

from .runtime import PBC_KEY
from .runtime import provider_revenue_cycle_build_workbench_view
from .runtime import provider_revenue_cycle_verify_owned_table_boundary

CONTROL_DEFINITIONS = (
    {
        "control_id": "registration_readiness_gate",
        "label": "Block claim progression when registration evidence is incomplete",
        "severity": "high",
        "owned_tables": ("provider_revenue_cycle_patient_account",),
    },
    {
        "control_id": "claim_scrub_fatal_gate",
        "label": "Prevent submission for fatal scrub edits",
        "severity": "critical",
        "owned_tables": ("provider_revenue_cycle_claim_batch",),
    },
    {
        "control_id": "patient_protection_hold",
        "label": "Prevent collections on assistance or dispute holds",
        "severity": "high",
        "owned_tables": ("provider_revenue_cycle_collection_account",),
    },
    {
        "control_id": "refund_duplicate_guard",
        "label": "Reject duplicate refund and credit attempts",
        "severity": "high",
        "owned_tables": ("provider_revenue_cycle_payment_posting",),
    },
    {
        "control_id": "close_reconciliation_gate",
        "label": "Require zero unresolved variance before close",
        "severity": "critical",
        "owned_tables": ("provider_revenue_cycle_collection_account",),
    },
    {
        "control_id": "assistant_boundary_guardrail",
        "label": "Allow assistant previews only for owned-table CRUD previews",
        "severity": "critical",
        "owned_tables": ("provider_revenue_cycle_provider_revenue_cycle_control_assertion",),
    },
)
_CRUD_ACTIONS = {"create", "read", "update", "delete"}


def provider_revenue_cycle_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    normalized_action = str(action or "read").lower()
    candidate_table = str(table or "")
    payload_dict = dict(payload or {})
    boundary = provider_revenue_cycle_verify_owned_table_boundary((f"{candidate_table}_table",))
    ok = normalized_action in _CRUD_ACTIONS and candidate_table.startswith(f"{PBC_KEY}_") and boundary["ok"]
    return {
        "ok": ok,
        "action": normalized_action,
        "table": candidate_table,
        "payload_keys": tuple(sorted(payload_dict)),
        "boundary_ok": boundary["ok"],
        "requires_confirmation": normalized_action != "read",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def provider_revenue_cycle_control_center(state: dict | None = None, *, tenant: str = "default") -> dict:
    workbench = provider_revenue_cycle_build_workbench_view(state=state, tenant=tenant)
    registration_queue = next(queue for queue in workbench["queues"] if queue["queue"] == "registration_deficiencies")
    denial_queue = next(queue for queue in workbench["queues"] if queue["queue"] == "denials_and_underpayments")
    return {
        "ok": workbench["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "controls": CONTROL_DEFINITIONS,
        "assistant_guardrails": provider_revenue_cycle_mutation_preview(
            "update",
            "provider_revenue_cycle_provider_revenue_cycle_control_assertion",
            {"tenant": tenant},
        ),
        "runtime_invariants": {
            "registration_queue_visible": registration_queue["severity"] == "high",
            "denial_queue_visible": denial_queue["severity"] == "critical",
            "fixed_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        "workbench": workbench,
        "side_effects": (),
    }


def provider_revenue_cycle_control_catalog() -> dict:
    control_ids = tuple(control["control_id"] for control in CONTROL_DEFINITIONS)
    return {
        "ok": bool(CONTROL_DEFINITIONS),
        "pbc": PBC_KEY,
        "controls": CONTROL_DEFINITIONS,
        "control_ids": control_ids,
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = provider_revenue_cycle_control_catalog()
    preview = provider_revenue_cycle_mutation_preview("create", "provider_revenue_cycle_patient_account", {"account_id": "acct"})
    center = provider_revenue_cycle_control_center()
    return {
        "ok": catalog["ok"] and preview["ok"] and center["ok"],
        "side_effects": (),
    }
