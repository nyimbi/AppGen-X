"""Domain models and schema metadata for the gaming_casino_operations PBC."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


PBC_KEY = "gaming_casino_operations"

PLAYER_PROFILE_TABLE = f"{PBC_KEY}_player_profile"
TABLE_GAME_TABLE = f"{PBC_KEY}_table_game"
SLOT_MACHINE_TABLE = f"{PBC_KEY}_slot_machine"
WAGER_SESSION_TABLE = f"{PBC_KEY}_wager_session"
PAYOUT_TABLE = f"{PBC_KEY}_payout"
RESPONSIBLE_GAMING_CASE_TABLE = f"{PBC_KEY}_responsible_gaming_case"
GAMING_COMPLIANCE_TABLE = f"{PBC_KEY}_gaming_compliance"
POLICY_RULE_TABLE = f"{PBC_KEY}_policy_rule"
RUNTIME_PARAMETER_TABLE = f"{PBC_KEY}_runtime_parameter"
SCHEMA_EXTENSION_TABLE = f"{PBC_KEY}_schema_extension"
CONTROL_ASSERTION_TABLE = f"{PBC_KEY}_control_assertion"
GOVERNED_MODEL_TABLE = f"{PBC_KEY}_governed_model"
OUTBOX_EVENT_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_EVENT_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_EVENT_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"

BUSINESS_TABLES = (
    PLAYER_PROFILE_TABLE,
    TABLE_GAME_TABLE,
    SLOT_MACHINE_TABLE,
    WAGER_SESSION_TABLE,
    PAYOUT_TABLE,
    RESPONSIBLE_GAMING_CASE_TABLE,
    GAMING_COMPLIANCE_TABLE,
    POLICY_RULE_TABLE,
    RUNTIME_PARAMETER_TABLE,
    SCHEMA_EXTENSION_TABLE,
    CONTROL_ASSERTION_TABLE,
    GOVERNED_MODEL_TABLE,
)
EVENT_TABLES = (
    OUTBOX_EVENT_TABLE,
    INBOX_EVENT_TABLE,
    DEAD_LETTER_EVENT_TABLE,
)
OWNED_TABLES = BUSINESS_TABLES + EVENT_TABLES


def _field(name: str, field_type: str, *, required: bool = True) -> dict[str, Any]:
    return {"name": name, "type": field_type, "required": required}


COMMON_FIELDS = (
    _field("id", "text"),
    _field("tenant", "text"),
    _field("created_at", "timestamp"),
    _field("updated_at", "timestamp"),
)

TABLE_DEFINITIONS: dict[str, dict[str, Any]] = {
    PLAYER_PROFILE_TABLE: {
        "class_name": "GamingCasinoOperationsPlayerProfile",
        "description": "Patron enrollment, identity evidence, restrictions, and host context.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("player_number", "text"),
            _field("legal_name", "text"),
            _field("date_of_birth", "text"),
            _field("loyalty_tier", "text"),
            _field("enrollment_status", "text"),
            _field("identity_confidence", "numeric"),
            _field("age_verified", "boolean"),
            _field("restriction_state", "text"),
            _field("property_id", "text"),
            _field("host_id", "text", required=False),
            _field("duplicate_review_state", "text"),
            _field("payload", "json", required=False),
        ),
    },
    TABLE_GAME_TABLE: {
        "class_name": "GamingCasinoOperationsTableGame",
        "description": "Table lifecycle, shift ownership, bankroll, and exception evidence.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("table_number", "text"),
            _field("pit", "text"),
            _field("game_variant", "text"),
            _field("table_status", "text"),
            _field("shift_id", "text"),
            _field("opening_bankroll", "numeric"),
            _field("current_bankroll", "numeric"),
            _field("dealer_id", "text"),
            _field("supervisor_id", "text"),
            _field("dispute_state", "text"),
            _field("payload", "json", required=False),
        ),
    },
    SLOT_MACHINE_TABLE: {
        "class_name": "GamingCasinoOperationsSlotMachine",
        "description": "Slot configuration, outage state, meter evidence, and approvals.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("asset_code", "text"),
            _field("bank_location", "text"),
            _field("denomination", "numeric"),
            _field("paytable_version", "text"),
            _field("progressive_link", "text", required=False),
            _field("operational_state", "text"),
            _field("fault_state", "text"),
            _field("jurisdiction_approval_state", "text"),
            _field("last_meter_reading", "numeric"),
            _field("payload", "json", required=False),
        ),
    },
    WAGER_SESSION_TABLE: {
        "class_name": "GamingCasinoOperationsWagerSession",
        "description": "Unified table and slot session context, ratings, and disputes.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("player_profile_id", "text"),
            _field("asset_kind", "text"),
            _field("asset_id", "text"),
            _field("session_status", "text"),
            _field("rating_status", "text"),
            _field("average_bet", "numeric", required=False),
            _field("theoretical_win", "numeric", required=False),
            _field("dispute_flag", "boolean"),
            _field("started_at", "timestamp"),
            _field("ended_at", "timestamp", required=False),
            _field("payload", "json", required=False),
        ),
    },
    PAYOUT_TABLE: {
        "class_name": "GamingCasinoOperationsPayout",
        "description": "Hand-pay, cage, and jackpot journal with approval evidence.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("payout_number", "text"),
            _field("source_type", "text"),
            _field("source_id", "text"),
            _field("payout_kind", "text"),
            _field("amount", "numeric"),
            _field("currency", "text"),
            _field("approval_state", "text"),
            _field("patron_verification_level", "text"),
            _field("suspicious_activity_flag", "boolean"),
            _field("payload", "json", required=False),
        ),
    },
    RESPONSIBLE_GAMING_CASE_TABLE: {
        "class_name": "GamingCasinoOperationsResponsibleGamingCase",
        "description": "Intervention plans, cooling-off state, and player care evidence.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("case_number", "text"),
            _field("player_profile_id", "text"),
            _field("risk_level", "text"),
            _field("intervention_state", "text"),
            _field("cooling_off_until", "text", required=False),
            _field("owner_id", "text"),
            _field("payload", "json", required=False),
        ),
    },
    GAMING_COMPLIANCE_TABLE: {
        "class_name": "GamingCasinoOperationsComplianceCase",
        "description": "Compliance incidents, surveillance reviews, and case ownership.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("case_number", "text"),
            _field("compliance_type", "text"),
            _field("severity", "text"),
            _field("case_status", "text"),
            _field("jurisdiction", "text"),
            _field("owner_id", "text"),
            _field("payload", "json", required=False),
        ),
    },
    POLICY_RULE_TABLE: {
        "class_name": "GamingCasinoOperationsPolicyRule",
        "description": "Jurisdiction and property rules that govern live floor work.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("rule_id", "text"),
            _field("jurisdiction", "text"),
            _field("scope", "text"),
            _field("rule_status", "text"),
            _field("version", "integer"),
            _field("effective_from", "text"),
            _field("effective_to", "text", required=False),
            _field("payload", "json", required=False),
        ),
    },
    RUNTIME_PARAMETER_TABLE: {
        "class_name": "GamingCasinoOperationsRuntimeParameter",
        "description": "Bounded operational parameters for floor control decisions.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("parameter_name", "text"),
            _field("parameter_value", "json"),
            _field("scope", "text"),
            _field("parameter_status", "text"),
        ),
    },
    SCHEMA_EXTENSION_TABLE: {
        "class_name": "GamingCasinoOperationsSchemaExtension",
        "description": "Package-local schema extension registry.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("table_name", "text"),
            _field("extension_name", "text"),
            _field("extension_status", "text"),
            _field("fields_json", "json"),
        ),
    },
    CONTROL_ASSERTION_TABLE: {
        "class_name": "GamingCasinoOperationsControlAssertion",
        "description": "Continuous control tests and operator attestation records.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("assertion_id", "text"),
            _field("control_name", "text"),
            _field("frequency", "text"),
            _field("assertion_status", "text"),
            _field("owner_id", "text"),
            _field("payload", "json", required=False),
        ),
    },
    GOVERNED_MODEL_TABLE: {
        "class_name": "GamingCasinoOperationsGovernedModel",
        "description": "Governed AI models, approval state, and drift review evidence.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("model_name", "text"),
            _field("model_version", "text"),
            _field("approval_state", "text"),
            _field("drift_state", "text"),
            _field("last_reviewed_at", "text"),
            _field("payload", "json", required=False),
        ),
    },
    OUTBOX_EVENT_TABLE: {
        "class_name": "GamingCasinoOperationsOutboxEvent",
        "description": "AppGen-X outbox evidence for emitted domain events.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("event_type", "text"),
            _field("aggregate_table", "text"),
            _field("aggregate_id", "text"),
            _field("topic", "text"),
            _field("event_status", "text"),
            _field("payload", "json"),
        ),
    },
    INBOX_EVENT_TABLE: {
        "class_name": "GamingCasinoOperationsInboxEvent",
        "description": "AppGen-X inbox evidence for consumed events.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("event_type", "text"),
            _field("aggregate_table", "text", required=False),
            _field("aggregate_id", "text", required=False),
            _field("topic", "text"),
            _field("event_status", "text"),
            _field("payload", "json"),
        ),
    },
    DEAD_LETTER_EVENT_TABLE: {
        "class_name": "GamingCasinoOperationsDeadLetterEvent",
        "description": "Rejected or exhausted AppGen-X event evidence.",
        "primary_key": ("id",),
        "fields": COMMON_FIELDS
        + (
            _field("event_type", "text"),
            _field("aggregate_table", "text", required=False),
            _field("aggregate_id", "text", required=False),
            _field("topic", "text"),
            _field("event_status", "text"),
            _field("payload", "json"),
        ),
    },
}


@dataclass(frozen=True)
class PlayerProfileModel:
    id: str
    tenant: str
    player_number: str
    legal_name: str
    date_of_birth: str
    loyalty_tier: str
    enrollment_status: str
    identity_confidence: float
    age_verified: bool
    restriction_state: str
    property_id: str
    created_at: str
    updated_at: str
    host_id: str | None = None
    duplicate_review_state: str = "not_required"
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TableGameModel:
    id: str
    tenant: str
    table_number: str
    pit: str
    game_variant: str
    table_status: str
    shift_id: str
    opening_bankroll: float
    current_bankroll: float
    dealer_id: str
    supervisor_id: str
    dispute_state: str
    created_at: str
    updated_at: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SlotMachineModel:
    id: str
    tenant: str
    asset_code: str
    bank_location: str
    denomination: float
    paytable_version: str
    operational_state: str
    fault_state: str
    jurisdiction_approval_state: str
    last_meter_reading: float
    created_at: str
    updated_at: str
    progressive_link: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WagerSessionModel:
    id: str
    tenant: str
    player_profile_id: str
    asset_kind: str
    asset_id: str
    session_status: str
    rating_status: str
    dispute_flag: bool
    started_at: str
    created_at: str
    updated_at: str
    average_bet: float | None = None
    theoretical_win: float | None = None
    ended_at: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PayoutModel:
    id: str
    tenant: str
    payout_number: str
    source_type: str
    source_id: str
    payout_kind: str
    amount: float
    currency: str
    approval_state: str
    patron_verification_level: str
    suspicious_activity_flag: bool
    created_at: str
    updated_at: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResponsibleGamingCaseModel:
    id: str
    tenant: str
    case_number: str
    player_profile_id: str
    risk_level: str
    intervention_state: str
    owner_id: str
    created_at: str
    updated_at: str
    cooling_off_until: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ComplianceCaseModel:
    id: str
    tenant: str
    case_number: str
    compliance_type: str
    severity: str
    case_status: str
    jurisdiction: str
    owner_id: str
    created_at: str
    updated_at: str
    payload: dict[str, Any] = field(default_factory=dict)


CORE_MODEL_BUILDERS = {
    PLAYER_PROFILE_TABLE: PlayerProfileModel,
    TABLE_GAME_TABLE: TableGameModel,
    SLOT_MACHINE_TABLE: SlotMachineModel,
    WAGER_SESSION_TABLE: WagerSessionModel,
    PAYOUT_TABLE: PayoutModel,
    RESPONSIBLE_GAMING_CASE_TABLE: ResponsibleGamingCaseModel,
    GAMING_COMPLIANCE_TABLE: ComplianceCaseModel,
}


def _required_field_names(table: str) -> tuple[str, ...]:
    definition = TABLE_DEFINITIONS[table]
    return tuple(field["name"] for field in definition["fields"] if field["required"])


def _base_record(table: str, payload: dict[str, Any]) -> dict[str, Any]:
    definition = TABLE_DEFINITIONS[table]
    missing = tuple(
        name for name in _required_field_names(table) if payload.get(name) is None
    )
    if missing:
        return {"ok": False, "table": table, "missing": missing, "side_effects": ()}
    record = {field["name"]: payload.get(field["name"]) for field in definition["fields"]}
    return {
        "ok": True,
        "table": table,
        "record": record,
        "class_name": definition["class_name"],
        "side_effects": (),
    }


def create_model_record(table: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Create a typed record for an owned table."""
    if table not in TABLE_DEFINITIONS:
        return {"ok": False, "table": table, "reason": "unknown_owned_table", "side_effects": ()}

    base = _base_record(table, payload)
    if base["ok"] is not True:
        return base

    record = base["record"]
    builder = CORE_MODEL_BUILDERS.get(table)
    if builder is None:
        return base
    return {
        **base,
        "record": asdict(builder(**record)),
    }


def model_contracts() -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "table": table,
            "class_name": definition["class_name"],
            "primary_key": definition["primary_key"],
            "fields": definition["fields"],
            "description": definition["description"],
        }
        for table, definition in TABLE_DEFINITIONS.items()
    )


def standalone_model_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "owned_tables": OWNED_TABLES,
        "business_tables": BUSINESS_TABLES,
        "event_tables": EVENT_TABLES,
        "models": model_contracts(),
        "side_effects": (),
    }


def model_alignment_smoke_test() -> dict[str, Any]:
    examples = (
        create_model_record(
            PLAYER_PROFILE_TABLE,
            {
                "id": "player_smoke",
                "tenant": "tenant_smoke",
                "player_number": "P-100",
                "legal_name": "Smoke Patron",
                "date_of_birth": "1990-01-01",
                "loyalty_tier": "standard",
                "enrollment_status": "active",
                "identity_confidence": 0.98,
                "age_verified": True,
                "restriction_state": "clear",
                "property_id": "property-smoke",
                "duplicate_review_state": "not_required",
                "created_at": "2026-05-30T00:00:00Z",
                "updated_at": "2026-05-30T00:00:00Z",
            },
        ),
        create_model_record(
            TABLE_GAME_TABLE,
            {
                "id": "table_smoke",
                "tenant": "tenant_smoke",
                "table_number": "BJ-12",
                "pit": "North",
                "game_variant": "blackjack",
                "table_status": "open",
                "shift_id": "shift-smoke",
                "opening_bankroll": 25000.0,
                "current_bankroll": 25000.0,
                "dealer_id": "dealer-smoke",
                "supervisor_id": "supervisor-smoke",
                "dispute_state": "clear",
                "created_at": "2026-05-30T00:00:00Z",
                "updated_at": "2026-05-30T00:00:00Z",
            },
        ),
    )
    return {
        "ok": all(example["ok"] is True for example in examples),
        "examples": examples,
        "contract": standalone_model_contract(),
        "side_effects": (),
    }
