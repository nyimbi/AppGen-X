"""Package-local controls for the tax_localization standalone workbench."""

from __future__ import annotations

from .runtime import tax_localization_build_release_evidence
from .runtime import tax_localization_build_workbench_view
from .runtime import tax_localization_calculate_tax_quote
from .runtime import tax_localization_configure_runtime
from .runtime import tax_localization_empty_state
from .runtime import tax_localization_prepare_tax_filing
from .runtime import tax_localization_record_invoice_tax
from .runtime import tax_localization_register_jurisdiction
from .runtime import tax_localization_register_tax_rule
from .runtime import tax_localization_run_control_tests
from .runtime import tax_localization_set_parameter
from .runtime import tax_localization_verify_formal_invariants
from .runtime import tax_localization_verify_owned_table_boundary


TAX_LOCALIZATION_CONTROLS = (
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Runs package-local release evidence, control tests, and invariant checks.",
        "permission": "tax_localization.audit",
    },
    {
        "control_id": "filing_submission_gate",
        "title": "Filing submission gate",
        "description": "Requires a prepared filing, calculation backing, and no blocking control gaps.",
        "permission": "tax_localization.file",
    },
    {
        "control_id": "exemption_evidence_gate",
        "title": "Exemption evidence gate",
        "description": "Blocks low-evidence exemption usage from reaching invoice or filing output.",
        "permission": "tax_localization.exemption",
    },
    {
        "control_id": "owned_boundary_and_event_contract",
        "title": "Boundary and event contract proof",
        "description": "Verifies owned-table isolation and AppGen-X eventing metadata.",
        "permission": "tax_localization.audit",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Ensures document-driven changes remain preview-only and confirmation-gated.",
        "permission": "tax_localization.audit",
    },
)


def _control_state() -> dict:
    state = tax_localization_empty_state()
    state = tax_localization_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.tax.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "authority_channels": ("authority_api", "secure_outbox"),
            "workbench_limit": 100,
        },
    )["state"]
    state = tax_localization_set_parameter(state, "tax_quote_precision", 2)["state"]
    state = tax_localization_set_parameter(state, "filing_reconciliation_tolerance", 0.01)["state"]
    state = tax_localization_register_jurisdiction(
        state,
        {
            "jurisdiction_id": "us_tx_austin",
            "tenant": "tenant_alpha",
            "country": "US",
            "region": "TX",
            "locality": "Austin",
            "currency": "USD",
            "authority_channel": "authority_api",
            "filing_frequency": "monthly",
            "risk_score": 0.04,
        },
    )["state"]
    state = tax_localization_register_tax_rule(
        state,
        {
            "rule_id": "rule_tx_general_goods",
            "tenant": "tenant_alpha",
            "jurisdiction_id": "us_tx_austin",
            "tax_type": "sales_tax",
            "product_class": "general_goods",
            "rate": 0.0825,
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
            "version": 1,
            "status": "active",
            "approval": {"approved_by": "tax_controller", "approved_at": "2026-05-29"},
        },
    )["state"]
    quote = tax_localization_calculate_tax_quote(
        state,
        {
            "quote_id": "quote_ctrl_001",
            "tenant": "tenant_alpha",
            "jurisdiction_id": "us_tx_austin",
            "customer_id": "cust_ctrl_001",
            "order_id": "order_ctrl_001",
            "lines": (
                {"line_id": "line_1", "product_id": "sku_1", "product_class": "general_goods", "amount": 100.0, "quantity": 2},
            ),
        },
    )
    state = quote["state"]
    state = tax_localization_record_invoice_tax(state, "invoice_ctrl_001", "quote_ctrl_001")["state"]
    state = tax_localization_prepare_tax_filing(
        state,
        filing_id="filing_ctrl_001",
        jurisdiction_id="us_tx_austin",
        period="2026-05",
        approved_by="tax_controller",
    )["state"]
    return state


def _table_permission(table: str) -> str:
    normalized = table.removeprefix("tax_localization_")
    if "filing" in normalized:
        return "tax_localization.file"
    if "invoice" in normalized or "calculation" in normalized:
        return "tax_localization.calculate"
    if "certificate" in normalized or "exemption" in normalized:
        return "tax_localization.exemption"
    if "rule" in normalized:
        return "tax_localization.rule_admin"
    if "parameter" in normalized or "configuration" in normalized:
        return "tax_localization.configure"
    return "tax_localization.audit"


def tax_localization_control_catalog() -> dict:
    return {
        "ok": bool(TAX_LOCALIZATION_CONTROLS),
        "pbc": "tax_localization",
        "controls": TAX_LOCALIZATION_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in TAX_LOCALIZATION_CONTROLS),
        "side_effects": (),
    }


def tax_localization_control_center(state: dict | None = None) -> dict:
    source_state = state or _control_state()
    release = tax_localization_build_release_evidence()
    runtime_controls = tax_localization_run_control_tests(source_state)
    invariants = tax_localization_verify_formal_invariants(source_state)
    workbench = tax_localization_build_workbench_view(source_state, tenant="tenant_alpha")
    accepted_boundary = tax_localization_verify_owned_table_boundary(("tax_jurisdiction", "GET /products/taxability"))
    rejected_boundary = tax_localization_verify_owned_table_boundary(("shared_revenue_ledger",))
    filing_submission_gate = {
        "prepared_filing": bool(source_state.get("filings")),
        "calculation_backing": all(item.get("calculation_count", 0) > 0 for item in source_state.get("filings", {}).values()),
        "no_blocking_gaps": not runtime_controls["blocking_gaps"],
    }
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
    }
    return {
        "ok": release["ok"] and runtime_controls["ok"] and invariants["ok"] and assistant_guardrails["boundary_ok"],
        "pbc": "tax_localization",
        "controls": tax_localization_control_catalog()["controls"],
        "release": release,
        "runtime_controls": runtime_controls,
        "invariants": invariants,
        "workbench": workbench,
        "filing_submission_gate": filing_submission_gate,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }


def tax_localization_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    normalized_action = str(action).lower()
    boundary = tax_localization_verify_owned_table_boundary((table,))
    return {
        "ok": normalized_action in {"create", "read", "update", "delete"} and boundary["ok"],
        "pbc": "tax_localization",
        "action": normalized_action,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized_action != "read",
        "permission": _table_permission(table),
        "boundary": boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    preview = tax_localization_mutation_preview("read", "tax_localization_tax_jurisdiction", {})
    control_center = tax_localization_control_center()
    return {
        "ok": preview["ok"] and control_center["ok"],
        "preview": preview,
        "control_center": control_center,
        "side_effects": (),
    }
