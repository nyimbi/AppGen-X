"""Executable schema contract for the bank_payments_clearing PBC."""

from __future__ import annotations

from pathlib import Path

from .runtime import (
    BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS,
    BANK_PAYMENTS_CLEARING_OWNED_TABLES,
)


PBC_KEY = "bank_payments_clearing"
PACKAGE_DIR = Path(__file__).resolve().parent
_GENERIC_FIELDS = (
    "id",
    "tenant",
    "code",
    "status",
    "version",
    "payload",
    "created_at",
    "updated_at",
)
_TABLE_FIELDS = {
    "bank_payments_clearing_payment_instruction": (
        "instruction_id",
        "tenant",
        "rail",
        "participant_bank_id",
        "amount",
        "currency",
        "state",
        "external_reference",
        "screening_evidence",
        "liquidity_evidence",
        "batch_id",
        "created_at",
        "updated_at",
    ),
    "bank_payments_clearing_clearing_batch": (
        "batch_id",
        "tenant",
        "rail",
        "participant_bank_id",
        "state",
        "item_count",
        "total_amount",
        "hash_total",
        "cutoff_context",
        "finalization_lock",
        "created_at",
        "updated_at",
    ),
    "bank_payments_clearing_settlement_file": (
        "file_id",
        "tenant",
        "batch_id",
        "sequence",
        "rail",
        "state",
        "control_total",
        "item_hash",
        "checksum",
        "signature",
        "transmission_status",
        "created_at",
        "updated_at",
    ),
    "bank_payments_clearing_return_item": (
        "return_id",
        "tenant",
        "instruction_id",
        "reason_code",
        "repair_eligible",
        "return_deadline_days",
        "financial_impact",
        "state",
        "notification_required",
        "created_at",
        "updated_at",
    ),
    "bank_payments_clearing_exception_case": (
        "exception_id",
        "tenant",
        "exception_type",
        "object_id",
        "findings",
        "severity",
        "owner_queue",
        "state",
        "closure_requires_evidence",
        "created_at",
        "updated_at",
    ),
    "bank_payments_clearing_bank_reconciliation": (
        "reconciliation_id",
        "tenant",
        "match_count",
        "fee_count",
        "exception_count",
        "matches",
        "fees",
        "exceptions",
        "state",
        "created_at",
        "updated_at",
    ),
    "bank_payments_clearing_participant_bank": (
        "participant_bank_id",
        "tenant",
        "routing_identifier",
        "supported_rails",
        "active_windows",
        "status",
        "audit_hash",
        "created_at",
        "updated_at",
    ),
    "bank_payments_clearing_appgen_outbox_event": (
        "event_id",
        "event_type",
        "topic",
        "contract",
        "payload",
        "idempotency_key",
        "created_at",
    ),
    "bank_payments_clearing_appgen_inbox_event": (
        "event_id",
        "event_type",
        "topic",
        "payload",
        "idempotency_key",
        "received_at",
    ),
    "bank_payments_clearing_appgen_dead_letter_event": (
        "event_id",
        "event_type",
        "topic",
        "payload",
        "idempotency_key",
        "retry_policy",
        "failed_at",
    ),
}


def _camelize(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


def _table_contract(table: str) -> dict:
    fields = _TABLE_FIELDS.get(table, _GENERIC_FIELDS)
    primary_key = ("id",)
    for candidate in (
        "instruction_id",
        "batch_id",
        "file_id",
        "return_id",
        "exception_id",
        "reconciliation_id",
        "participant_bank_id",
        "event_id",
    ):
        if candidate in fields:
            primary_key = (candidate,)
            break
    return {
        "table": table,
        "fields": fields,
        "primary_key": primary_key,
        "owned_by": PBC_KEY,
        "shared_table_access": False,
    }


def build_schema_contract() -> dict:
    tables = tuple(_table_contract(table) for table in BANK_PAYMENTS_CLEARING_OWNED_TABLES)
    models = tuple(
        {
            "class_name": _camelize(table),
            "table": table,
            "fields": next(item["fields"] for item in tables if item["table"] == table),
            "module": "models.py",
        }
        for table in BANK_PAYMENTS_CLEARING_OWNED_TABLES
    )
    return {
        "format": "appgen.bank-payments-clearing-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/bank_payments_clearing",
        "tables": tables,
        "models": models,
        "migrations": (
            {
                "path": "src/pyAppGen/pbcs/bank_payments_clearing/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": BANK_PAYMENTS_CLEARING_OWNED_TABLES,
                "backend_allowlist": BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "model_module": "src/pyAppGen/pbcs/bank_payments_clearing/models.py",
        "database_backends": BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": BANK_PAYMENTS_CLEARING_OWNED_TABLES,
        "side_effects": (),
    }


SCHEMA_CONTRACT = build_schema_contract()


def validate_schema_contract() -> dict:
    schema = build_schema_contract()
    invalid_tables = tuple(
        table["table"]
        for table in schema["tables"]
        if not table["table"].startswith(f"{PBC_KEY}_")
    )
    missing_artifacts = tuple(
        artifact
        for artifact in (
            PACKAGE_DIR / "migrations/001_initial.sql",
            PACKAGE_DIR / "models.py",
        )
        if not artifact.exists()
    )
    invalid_backends = tuple(
        backend
        for backend in schema["database_backends"]
        if backend not in {"postgresql", "mysql", "mariadb"}
    )
    return {
        "ok": schema["ok"]
        and not invalid_tables
        and not missing_artifacts
        and not invalid_backends
        and schema["shared_table_access"] is False,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "missing_artifacts": tuple(str(path) for path in missing_artifacts),
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_schema_contract()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
