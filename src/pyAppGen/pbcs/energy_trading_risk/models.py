"""Domain payload models for the energy_trading_risk one-PBC app."""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass

from .runtime import energy_trading_risk_build_schema_contract


@dataclass(frozen=True)
class EnergyTradeCaptureModel:
    tenant: str
    commodity: str
    market_hub: str
    book: str
    trader: str
    strategy: str
    counterparty: str
    side: str
    position_type: str
    delivery_start: str
    delivery_end: str
    delivery_profile: str
    pricing_formula: str
    volume_mwh: float
    fixed_price: float
    submitted_at: str
    approval_state: str = "pending"
    id: str | None = None
    contract_id: str | None = None

    def to_payload(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class NominationSubmissionModel:
    tenant: str
    trade_id: str
    delivery_period: str
    interval_start: str
    interval_end: str
    volume_mwh: float
    submitted_at: str
    operator: str
    id: str | None = None
    reason_code: str | None = None

    def to_payload(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class MarketPriceCurveModel:
    tenant: str
    commodity: str
    market_hub: str
    delivery_period: str
    strip_start: str
    strip_end: str
    curve_price: float
    as_of: str
    source_name: str
    id: str | None = None

    def to_payload(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ExposureLimitModel:
    tenant: str
    commodity: str
    market_hub: str
    book: str
    max_net_exposure_mwh: float
    max_projected_mtm: float
    severity: str
    owner: str
    effective_from: str
    id: str | None = None

    def to_payload(self) -> dict:
        return asdict(self)



def model_contracts() -> dict:
    """Return owned schema models plus package-local payload models."""
    schema = energy_trading_risk_build_schema_contract()
    return {
        "ok": schema["ok"],
        "schema_models": schema["models"],
        "input_models": (
            {
                "class_name": "EnergyTradeCaptureModel",
                "fields": tuple(EnergyTradeCaptureModel.__dataclass_fields__),
            },
            {
                "class_name": "NominationSubmissionModel",
                "fields": tuple(NominationSubmissionModel.__dataclass_fields__),
            },
            {
                "class_name": "MarketPriceCurveModel",
                "fields": tuple(MarketPriceCurveModel.__dataclass_fields__),
            },
            {
                "class_name": "ExposureLimitModel",
                "fields": tuple(ExposureLimitModel.__dataclass_fields__),
            },
        ),
        "models": schema["models"],
        "side_effects": (),
    }
