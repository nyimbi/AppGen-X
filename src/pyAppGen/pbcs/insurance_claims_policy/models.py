"""Owned model metadata for the insurance_claims_policy PBC."""

from __future__ import annotations

from .domain_depth import DOMAIN_OWNED_TABLES

PBC_KEY = "insurance_claims_policy"
EVENT_TABLES = (
    f"{PBC_KEY}_appgen_outbox_event",
    f"{PBC_KEY}_appgen_inbox_event",
    f"{PBC_KEY}_appgen_dead_letter_event",
)
OWNED_TABLES = tuple(DOMAIN_OWNED_TABLES) + EVENT_TABLES


def _field(name: str, field_type: str, **metadata) -> dict:
    return {"name": name, "type": field_type, **metadata}


def _relationship(field: str, target_logical_table: str, *, cardinality: str = "many-to-one") -> dict:
    target_table = f"{PBC_KEY}_{target_logical_table}"
    return {
        "field": field,
        "target_table": target_table,
        "target_column": "id",
        "cardinality": cardinality,
        "ownership": "same_pbc",
    }


def _domain_fields(*extra_fields: dict) -> tuple[dict, ...]:
    return (
        _field("id", "string", primary_key=True, nullable=False),
        _field("tenant", "string", required=True),
        _field("code", "string", required=True, searchable=True),
        _field("status", "string", required=True, default="draft"),
        _field("version", "integer", required=True, default=1),
        *extra_fields,
        _field("payload", "json", required=False),
        _field("effective_at", "datetime", required=False),
        _field("created_at", "datetime", required=True),
        _field("updated_at", "datetime", required=True),
    )


def _event_fields() -> tuple[dict, ...]:
    return (
        _field("id", "string", primary_key=True, nullable=False),
        _field("tenant", "string", required=True),
        _field("aggregate_id", "string", required=True, searchable=True),
        _field("aggregate_type", "string", required=True),
        _field("event_type", "string", required=True),
        _field("topic", "string", required=True),
        _field("status", "string", required=True, default="pending"),
        _field("attempt_count", "integer", required=True, default=0),
        _field("payload", "json", required=False),
        _field("created_at", "datetime", required=True),
        _field("updated_at", "datetime", required=True),
    )


_TABLE_SPECS = (
    {
        "logical_table": "insurance_policy",
        "fields": _domain_fields(
            _field("policy_number", "string", required=True, searchable=True),
            _field("product_code", "string", required=True),
            _field("policy_state", "string", required=True),
            _field("premium_status", "string", required=True, default="current"),
        ),
        "relationships": (),
    },
    {
        "logical_table": "policy_holder",
        "fields": _domain_fields(
            _field("policy_id", "string", required=True, references=f"{PBC_KEY}_insurance_policy.id"),
            _field("holder_role", "string", required=True),
            _field("party_name", "string", required=True),
            _field("authority_status", "string", required=True, default="verified"),
        ),
        "relationships": (_relationship("policy_id", "insurance_policy"),),
    },
    {
        "logical_table": "policy_coverage",
        "fields": _domain_fields(
            _field("policy_id", "string", required=True, references=f"{PBC_KEY}_insurance_policy.id"),
            _field("coverage_code", "string", required=True),
            _field("peril_code", "string", required=True),
            _field("limit_amount", "decimal", required=True),
            _field("deductible_amount", "decimal", required=True),
        ),
        "relationships": (_relationship("policy_id", "insurance_policy"),),
    },
    {
        "logical_table": "policy_endorsement",
        "fields": _domain_fields(
            _field("policy_id", "string", required=True, references=f"{PBC_KEY}_insurance_policy.id"),
            _field("endorsement_code", "string", required=True),
            _field("requested_change", "string", required=True),
            _field("premium_delta", "decimal", required=True),
        ),
        "relationships": (_relationship("policy_id", "insurance_policy"),),
    },
    {
        "logical_table": "premium_schedule",
        "fields": _domain_fields(
            _field("policy_id", "string", required=True, references=f"{PBC_KEY}_insurance_policy.id"),
            _field("billing_frequency", "string", required=True),
            _field("installment_amount", "decimal", required=True),
            _field("due_date", "datetime", required=True),
        ),
        "relationships": (_relationship("policy_id", "insurance_policy"),),
    },
    {
        "logical_table": "premium_payment",
        "fields": _domain_fields(
            _field("policy_id", "string", required=True, references=f"{PBC_KEY}_insurance_policy.id"),
            _field("schedule_id", "string", required=False, references=f"{PBC_KEY}_premium_schedule.id"),
            _field("amount_paid", "decimal", required=True),
            _field("paid_at", "datetime", required=True),
            _field("payment_status", "string", required=True),
        ),
        "relationships": (
            _relationship("policy_id", "insurance_policy"),
            _relationship("schedule_id", "premium_schedule"),
        ),
    },
    {
        "logical_table": "claim_record",
        "fields": _domain_fields(
            _field("policy_id", "string", required=True, references=f"{PBC_KEY}_insurance_policy.id"),
            _field("claim_number", "string", required=True, searchable=True),
            _field("loss_date", "datetime", required=True),
            _field("severity_band", "string", required=True),
            _field("claim_stage", "string", required=True, default="fnol"),
        ),
        "relationships": (_relationship("policy_id", "insurance_policy"),),
    },
    {
        "logical_table": "loss_event",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("event_type", "string", required=True),
            _field("occurred_at", "datetime", required=True),
            _field("location_code", "string", required=True),
            _field("catastrophe_flag", "boolean", required=True, default=False),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "claimant",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("claimant_role", "string", required=True),
            _field("claimant_name", "string", required=True),
            _field("relationship_to_insured", "string", required=True),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "claim_document",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("document_type", "string", required=True),
            _field("source_channel", "string", required=True),
            _field("received_at", "datetime", required=True),
            _field("verification_status", "string", required=True, default="pending"),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "coverage_determination",
        "fields": _domain_fields(
            _field("policy_id", "string", required=True, references=f"{PBC_KEY}_insurance_policy.id"),
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("decision", "string", required=True),
            _field("covered_amount", "decimal", required=True),
            _field("reasoning_hash", "string", required=True),
        ),
        "relationships": (
            _relationship("policy_id", "insurance_policy"),
            _relationship("claim_id", "claim_record"),
        ),
    },
    {
        "logical_table": "claim_reserve",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("reserve_type", "string", required=True),
            _field("recommended_amount", "decimal", required=True),
            _field("approved_amount", "decimal", required=True),
            _field("adequacy_band", "string", required=True),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "reserve_change",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("reserve_id", "string", required=True, references=f"{PBC_KEY}_claim_reserve.id"),
            _field("delta_amount", "decimal", required=True),
            _field("reason_code", "string", required=True),
            _field("authority_level", "string", required=True),
        ),
        "relationships": (
            _relationship("claim_id", "claim_record"),
            _relationship("reserve_id", "claim_reserve"),
        ),
    },
    {
        "logical_table": "claim_adjudication",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("decision", "string", required=True),
            _field("liability_position", "string", required=True),
            _field("reviewer_role", "string", required=True),
            _field("reviewed_at", "datetime", required=True),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "settlement_offer",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("offer_amount", "decimal", required=True),
            _field("negotiation_status", "string", required=True),
            _field("authority_required", "string", required=True),
            _field("expires_at", "datetime", required=True),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "settlement_payment",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("settlement_offer_id", "string", required=True, references=f"{PBC_KEY}_settlement_offer.id"),
            _field("payee_name", "string", required=True),
            _field("payment_amount", "decimal", required=True),
            _field("payment_status", "string", required=True),
        ),
        "relationships": (
            _relationship("claim_id", "claim_record"),
            _relationship("settlement_offer_id", "settlement_offer"),
        ),
    },
    {
        "logical_table": "subrogation_recovery",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("target_party", "string", required=True),
            _field("recovery_amount", "decimal", required=True),
            _field("recovery_stage", "string", required=True),
            _field("statute_deadline", "datetime", required=True),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "claim_communication",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("channel", "string", required=True),
            _field("recipient_role", "string", required=True),
            _field("response_due_at", "datetime", required=False),
            _field("delivery_status", "string", required=True),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "fraud_indicator",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("signal_type", "string", required=True),
            _field("score", "decimal", required=True),
            _field("disposition", "string", required=True),
            _field("review_status", "string", required=True),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "claim_exception_case",
        "fields": _domain_fields(
            _field("claim_id", "string", required=True, references=f"{PBC_KEY}_claim_record.id"),
            _field("exception_type", "string", required=True),
            _field("severity", "string", required=True),
            _field("queue_name", "string", required=True),
            _field("resolution_status", "string", required=True, default="open"),
        ),
        "relationships": (_relationship("claim_id", "claim_record"),),
    },
    {
        "logical_table": "insurance_policy_rule",
        "fields": _domain_fields(
            _field("rule_scope", "string", required=True),
            _field("rule_type", "string", required=True),
            _field("compiled_hash", "string", required=True),
            _field("activation_status", "string", required=True),
        ),
        "relationships": (),
    },
    {
        "logical_table": "insurance_runtime_parameter",
        "fields": _domain_fields(
            _field("parameter_name", "string", required=True),
            _field("value_type", "string", required=True),
            _field("current_value", "string", required=True),
            _field("bounded", "boolean", required=True, default=True),
        ),
        "relationships": (),
    },
    {
        "logical_table": "insurance_schema_extension",
        "fields": _domain_fields(
            _field("target_table", "string", required=True),
            _field("extension_key", "string", required=True),
            _field("approval_status", "string", required=True),
            _field("extension_payload", "json", required=False),
        ),
        "relationships": (),
    },
    {
        "logical_table": "insurance_control_assertion",
        "fields": _domain_fields(
            _field("control_name", "string", required=True),
            _field("control_status", "string", required=True),
            _field("last_checked_at", "datetime", required=True),
            _field("evidence_ref", "string", required=True),
        ),
        "relationships": (),
    },
    {
        "logical_table": "insurance_governed_model",
        "fields": _domain_fields(
            _field("model_name", "string", required=True),
            _field("model_purpose", "string", required=True),
            _field("model_version", "string", required=True),
            _field("approval_status", "string", required=True),
        ),
        "relationships": (),
    },
    {
        "logical_table": "appgen_outbox_event",
        "fields": _event_fields(),
        "relationships": (),
    },
    {
        "logical_table": "appgen_inbox_event",
        "fields": _event_fields(),
        "relationships": (),
    },
    {
        "logical_table": "appgen_dead_letter_event",
        "fields": _event_fields(),
        "relationships": (),
    },
)


def _model_from_spec(spec: dict) -> dict:
    logical_table = spec["logical_table"]
    owned_table = f"{PBC_KEY}_{logical_table}"
    class_name = "".join(part.capitalize() for part in owned_table.split("_"))
    return {
        "logical_table": logical_table,
        "owned_table": owned_table,
        "class_name": class_name,
        "table": owned_table,
        "fields": spec["fields"],
        "relationships": spec["relationships"],
    }


MODELS = tuple(_model_from_spec(spec) for spec in _TABLE_SPECS)
MODEL_BY_LOGICAL_TABLE = {model["logical_table"]: model for model in MODELS}
MODEL_BY_TABLE = {model["table"]: model for model in MODELS}

OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": f"{PBC_KEY}_",
    "tables": tuple(
        {
            "logical_table": model["logical_table"],
            "owned_table": model["table"],
            "fields": model["fields"],
            "relationships": model["relationships"],
        }
        for model in MODELS
    ),
}


def model_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "schema": OWNED_SCHEMA,
        "models": MODELS,
        "owned_tables": tuple(model["table"] for model in MODELS),
        "event_tables": EVENT_TABLES,
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = model_manifest()
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{PBC_KEY}_"))
    return {
        "ok": manifest["ok"] and len(manifest["owned_tables"]) >= len(DOMAIN_OWNED_TABLES) and not invalid_tables,
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }
