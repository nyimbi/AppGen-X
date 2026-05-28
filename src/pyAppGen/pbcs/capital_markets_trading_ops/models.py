"""Package-local models for the trade-order intake slice."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .runtime import capital_markets_trading_ops_build_schema_contract


@dataclass(frozen=True)
class TradeOrderFormModel:
    tenant: str
    instrument_id: str
    product_type: str
    trading_account: str
    desk: str
    trader: str
    book: str
    broker: str
    venue: str
    settlement_model: str
    regulatory_classification: str
    side: str
    quantity: float
    submitted_at: str
    limit_price: float | None = None
    approval_state: str = 'pending'
    counterparty: str | None = None
    notional: float | None = None

    def to_payload(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class TradeOrderRecordModel:
    id: str
    tenant: str
    status: str
    lifecycle_state: str
    status_badge: str
    workbench_queue: str
    release_ready: bool
    trade_order_signature: str
    version: int = 1
    actionable_remediation: tuple[str, ...] = field(default_factory=tuple)
    payload: dict = field(default_factory=dict)
    validation: dict = field(default_factory=dict)

    @classmethod
    def from_runtime_record(cls, record: dict) -> 'TradeOrderRecordModel':
        return cls(
            id=record['id'],
            tenant=record['tenant'],
            status=record['status'],
            lifecycle_state=record['lifecycle_state'],
            status_badge=record['status_badge'],
            workbench_queue=record['workbench_queue'],
            release_ready=bool(record['release_ready']),
            trade_order_signature=record['trade_order_signature'],
            version=record.get('version', 1),
            actionable_remediation=tuple(record.get('actionable_remediation', ())),
            payload=dict(record.get('payload', {})),
            validation=dict(record.get('validation', {})),
        )

def model_contracts():
    return capital_markets_trading_ops_build_schema_contract()['models']
