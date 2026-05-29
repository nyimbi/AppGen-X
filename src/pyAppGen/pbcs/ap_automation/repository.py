"""Database-backed repository contract for the Accounts Payable Automation PBC."""

from __future__ import annotations

from .runtime import AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
from .runtime import AP_AUTOMATION_OWNED_TABLES
from .runtime import ap_automation_build_workbench_view
from .runtime import ap_automation_capture_invoice
from .runtime import ap_automation_configure_runtime
from .runtime import ap_automation_create_payment_batch
from .runtime import ap_automation_empty_state
from .runtime import ap_automation_execute_payment
from .runtime import ap_automation_generate_remittance_advice
from .runtime import ap_automation_issue_purchase_order
from .runtime import ap_automation_onboard_vendor
from .runtime import ap_automation_receive_event
from .runtime import ap_automation_reconcile_vendor_statement
from .runtime import ap_automation_record_goods_receipt
from .runtime import ap_automation_register_rule
from .runtime import ap_automation_register_vendor_tax_profile
from .runtime import ap_automation_schedule_payments
from .runtime import ap_automation_screen_vendor_network
from .runtime import ap_automation_set_parameter
from .runtime import ap_automation_validate_vendor_bank_account


REPOSITORY_BINDINGS = (
    {
        "dataset": "vendor_readiness",
        "root_table": "ap_automation_vendor",
        "supporting_tables": (
            "ap_automation_vendor_bank_account",
            "ap_automation_vendor_tax_profile",
            "ap_automation_vendor_risk_signal",
        ),
        "form_ids": ("vendor_onboarding",),
        "wizard_ids": ("vendor_onboarding_wizard",),
        "control_ids": ("vendor_payment_readiness",),
        "filter_fields": ("tenant", "vendor_id", "approval_status", "screening_status"),
    },
    {
        "dataset": "invoice_capture_queue",
        "root_table": "ap_automation_invoice",
        "supporting_tables": (
            "ap_automation_invoice_line",
            "ap_automation_invoice_capture_artifact",
            "ap_automation_invoice_match_result",
        ),
        "form_ids": ("invoice_capture",),
        "wizard_ids": ("invoice_capture_wizard",),
        "control_ids": ("duplicate_invoice_hold_guard",),
        "filter_fields": ("tenant", "invoice_id", "vendor_id", "payment_status"),
    },
    {
        "dataset": "payment_release",
        "root_table": "ap_automation_payment",
        "supporting_tables": (
            "ap_automation_payment_batch",
            "ap_automation_payment_rail_decision",
            "ap_automation_approval_task",
        ),
        "form_ids": ("payment_batch_release",),
        "wizard_ids": ("payment_release_wizard",),
        "control_ids": ("payment_batch_release_integrity",),
        "filter_fields": ("tenant", "payment_id", "invoice_id", "status"),
    },
    {
        "dataset": "statement_reconciliation",
        "root_table": "ap_automation_vendor_statement",
        "supporting_tables": (
            "ap_automation_invoice",
            "ap_automation_payment",
            "ap_automation_exception_case",
        ),
        "form_ids": ("vendor_statement_reconciliation",),
        "wizard_ids": ("vendor_statement_wizard",),
        "control_ids": ("statement_exception_visibility",),
        "filter_fields": ("tenant", "statement_id", "vendor_id", "status"),
    },
)


class ApAutomationRepository:
    """Owned-table repository facade for database-backed forms and wizards."""

    def contract(self) -> dict:
        return repository_contract()

    def tenant_snapshot(self, state: dict, tenant: str) -> dict:
        vendor_rows = tuple(
            {
                "vendor_id": vendor["vendor_id"],
                "name": vendor["name"],
                "approval_status": vendor["approval_status"],
                "payment_enabled": vendor["payment_enabled"],
                "pending_checks": vendor.get("evidence_pack", {}).get("pending_checks", ()),
            }
            for vendor in state.get("vendors", {}).values()
            if vendor["tenant"] == tenant
        )
        invoice_rows = tuple(
            {
                "invoice_id": invoice["invoice_id"],
                "vendor_id": invoice["vendor_id"],
                "supplier_invoice_number": invoice.get("supplier_invoice_number"),
                "status": invoice["status"],
                "total": invoice["total"],
                "duplicate_review_required": invoice.get("duplicate_review_required", False),
            }
            for invoice in state.get("invoices", {}).values()
            if invoice["tenant"] == tenant
        )
        payment_rows = tuple(
            {
                "payment_id": payment["payment_id"],
                "invoice_id": payment["invoice_id"],
                "status": payment["status"],
                "amount": payment["amount"],
                "hold_reasons": payment.get("hold_reasons", ()),
                "batch_id": payment.get("batch_id"),
            }
            for payment in state.get("payments", {}).values()
            if payment["tenant"] == tenant
        )
        statement_rows = tuple(
            {
                "statement_id": statement["statement_id"],
                "status": statement["status"],
                "exception_count": statement.get("exception_count", 0),
                "reconciled_amount": statement.get("reconciled_amount", 0.0),
            }
            for statement in state.get("vendor_statements", {}).values()
            if statement["tenant"] == tenant
        )
        workbench = ap_automation_build_workbench_view(state, tenant=tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "datasets": {
                "vendor_readiness": vendor_rows,
                "invoice_capture_queue": invoice_rows,
                "payment_release": payment_rows,
                "statement_reconciliation": statement_rows,
            },
            "record_counts": {
                "vendors": len(vendor_rows),
                "invoices": len(invoice_rows),
                "payments": len(payment_rows),
                "statements": len(statement_rows),
            },
            "workbench": workbench,
            "side_effects": (),
        }

    def binding_for_form(self, form_id: str) -> dict:
        binding = next(
            (
                item
                for item in REPOSITORY_BINDINGS
                if form_id in item["form_ids"]
            ),
            None,
        )
        return {
            "ok": binding is not None,
            "form_id": form_id,
            "binding": dict(binding) if binding else None,
            "side_effects": (),
        }

    def persist_plan(self, table: str, payload: dict) -> dict:
        allowed = table in AP_AUTOMATION_OWNED_TABLES
        return {
            "ok": allowed,
            "table": table,
            "payload_keys": tuple(sorted(dict(payload or {}))),
            "database_backends": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
            "statement": "insert_or_update_owned_record" if allowed else "rejected_non_owned_table",
            "side_effects": (),
        }


def repository_contract() -> dict:
    """Return repository evidence for data-bound AP surfaces."""
    return {
        "format": "appgen.ap-automation-repository.v1",
        "ok": bool(REPOSITORY_BINDINGS),
        "pbc": "ap_automation",
        "database_backends": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": AP_AUTOMATION_OWNED_TABLES,
        "datasets": REPOSITORY_BINDINGS,
        "shared_table_access": False,
        "supports": ("forms", "wizards", "controls", "workbench"),
        "side_effects": (),
    }


def build_demo_state(*, include_release: bool = False) -> dict:
    """Build a deterministic AP state for repository-backed form and control smoke tests."""
    state = ap_automation_empty_state()
    state = ap_automation_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.ap.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire", "instant_bank_api"),
            "workbench_limit": 25,
        },
    )["state"]
    for name, value in (
        ("auto_match_threshold", 0.95),
        ("payment_approval_limit", 5000),
        ("discount_capture_floor", 0.01),
        ("vendor_risk_threshold", 0.7),
        ("liquidity_buffer", 250),
        ("workbench_limit", 25),
    ):
        state = ap_automation_set_parameter(state, name, value)["state"]
    state = ap_automation_register_rule(
        state,
        {
            "rule_id": "rule_repository_demo",
            "tenant": "tenant_repo",
            "scope": "invoice_match",
            "requires_three_way_match": True,
            "auto_match_threshold": 0.95,
            "status": "active",
        },
    )["state"]
    state = ap_automation_onboard_vendor(
        state,
        {
            "vendor_id": "vendor_repo",
            "tenant": "tenant_repo",
            "name": "Repository Vendor Ltd",
            "beneficial_owners": ("owner_repo",),
            "terms": {"net_days": 30, "discount_days": 10, "discount_rate": 0.02},
            "risk_signals": {"sanction_hits": 0, "late_delivery_rate": 0.01, "financial_stress": 0.02},
            "activation_requirements": ("approval", "bank_validation", "tax_profile", "screening"),
            "identity": {"did": "did:appgen:vendor-repo", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    state = ap_automation_receive_event(
        state,
        {
            "event_id": "evt_repo_vendor_approved",
            "event_type": "VendorApproved",
            "payload": {"tenant": "tenant_repo", "vendor_id": "vendor_repo", "approved_by": "controller_repo"},
        },
    )["state"]
    state = ap_automation_validate_vendor_bank_account(
        state,
        {
            "vendor_id": "vendor_repo",
            "bank_account_id": "bank_repo",
            "account_number": "123456789012",
            "rail": "ach",
            "verification_method": "independent_callback",
            "verification_reference": "repo-bank-001",
            "verified_by": "analyst_repo",
        },
    )["state"]
    state = ap_automation_register_vendor_tax_profile(
        state,
        {
            "vendor_id": "vendor_repo",
            "tax_profile_id": "tax_repo",
            "jurisdiction": "US-NY",
            "withholding_code": "NONE",
            "certificate_id": "cert-repo",
            "expiry_date": "2027-12-31",
        },
    )["state"]
    state = ap_automation_screen_vendor_network(state, "vendor_repo", sanction_entities=())["state"]
    state = ap_automation_issue_purchase_order(
        state,
        {
            "po_id": "po_repo",
            "tenant": "tenant_repo",
            "vendor_id": "vendor_repo",
            "currency": "USD",
            "lines": ({"sku": "hosting", "quantity": 1, "unit_price": 900, "account": "expense"},),
        },
    )["state"]
    state = ap_automation_record_goods_receipt(
        state,
        {
            "receipt_id": "gr_repo",
            "tenant": "tenant_repo",
            "po_id": "po_repo",
            "lines": ({"sku": "hosting", "quantity": 1},),
        },
    )["state"]
    state = ap_automation_capture_invoice(
        state,
        {
            "invoice_id": "inv_repo",
            "tenant": "tenant_repo",
            "vendor_id": "vendor_repo",
            "po_id": "po_repo",
            "receipt_id": "gr_repo",
            "invoice_date": "2026-05-25",
            "due_date": "2026-06-24",
            "supplier_invoice_number": "REPO-900",
            "currency": "USD",
            "tax": {"jurisdiction": "US-NY", "amount": 72, "rate": 0.08},
            "lines": ({"sku": "hosting", "quantity": 1, "unit_price": 900, "account": "expense"},),
            "artifact": {"channel": "email", "source_document": "repo_invoice.pdf", "confidence": 0.99},
        },
    )["state"]
    state = ap_automation_schedule_payments(
        state,
        tenant="tenant_repo",
        liquidity_forecast=(5000, 4900, 4800),
        risk_limit=0.7,
    )["state"]
    if include_release:
        state = ap_automation_create_payment_batch(
            state,
            {"tenant": "tenant_repo", "payment_ids": ("pay_inv_repo",), "batch_id": "batch_repo_1"},
        )["state"]
        state = ap_automation_execute_payment(
            state,
            "pay_inv_repo",
            rails=(
                {"rail": "instant_bank_api", "cost": 5, "latency": 2, "fx_rate": 1.0, "available": False},
                {"rail": "ach", "cost": 1, "latency": 24, "fx_rate": 1.0, "available": True},
            ),
        )["state"]
        state = ap_automation_generate_remittance_advice(
            state,
            "pay_inv_repo",
            delivery_channel="portal",
        )["state"]
        state = ap_automation_reconcile_vendor_statement(
            state,
            {
                "statement_id": "stmt_repo_1",
                "tenant": "tenant_repo",
                "vendor_id": "vendor_repo",
                "lines": ({"supplier_invoice_number": "REPO-900", "amount": 972.0, "status": "paid"},),
            },
        )["state"]
    return state


def smoke_test() -> dict:
    """Exercise the repository contract and dataset bindings without external I/O."""
    repository = ApAutomationRepository()
    state = build_demo_state(include_release=True)
    snapshot = repository.tenant_snapshot(state, "tenant_repo")
    binding = repository.binding_for_form("payment_batch_release")
    persist = repository.persist_plan("ap_automation_payment", {"payment_id": "pay_inv_repo"})
    return {
        "ok": repository.contract()["ok"] and snapshot["ok"] and binding["ok"] and persist["ok"],
        "contract": repository.contract(),
        "snapshot": snapshot,
        "binding": binding,
        "persist": persist,
        "side_effects": (),
    }
