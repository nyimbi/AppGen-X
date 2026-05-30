"""One-PBC app wrapper for the energy_trading_risk domain."""

from __future__ import annotations

from .agent import assistant_help_manifest
from .agent import build_operator_guidance
from .controls import energy_trading_risk_control_catalog
from .forms import energy_trading_risk_form_catalog
from .repository import EnergyTradingRiskRepository
from .routes import ROUTES
from .services import EnergyTradingRiskService
from .services import service_operation_manifest
from .runtime import energy_trading_risk_empty_state
from .ui import energy_trading_risk_single_pbc_app_ui_contract
from .wizards import energy_trading_risk_wizard_catalog


class EnergyTradingRiskApp:
    """Executable single-PBC app for trade capture and daily risk review."""

    def __init__(self, database_path: str = ":memory:"):
        self.repository = EnergyTradingRiskRepository(database_path=database_path)
        self.applied_migrations = self.repository.apply_migrations()
        self.service = EnergyTradingRiskService()
        self._hydrate_service_state()

    def close(self) -> None:
        self.repository.close()

    def _hydrate_service_state(self, tenant: str | None = None) -> None:
        state = energy_trading_risk_empty_state()
        state["energy_contracts"] = {record["id"]: record for record in self.repository.list_energy_contracts(tenant=tenant, limit=500)}
        state["trade_positions"] = {record["id"]: record for record in self.repository.list_trade_positions(tenant=tenant, limit=500)}
        state["nominations"] = {record["id"]: record for record in self.repository.list_nominations(tenant=tenant, limit=500)}
        state["schedules"] = {record["id"]: record for record in self.repository.list_schedules(tenant=tenant, limit=500)}
        state["settlements"] = {record["id"]: record for record in self.repository.list_settlements(tenant=tenant, limit=500)}
        state["market_price_curves"] = {record["id"]: record for record in self.repository.list_market_price_curves(tenant=tenant, limit=500)}
        state["exposure_limits"] = {record["id"]: record for record in self.repository.list_exposure_limits(tenant=tenant, limit=500)}
        self.service.state = state

    def register_energy_contract(self, payload: dict) -> dict:
        tenant = payload.get("tenant")
        self._hydrate_service_state(tenant=tenant)
        result = self.service.command_energy_contract(payload)
        self.repository.save_energy_contract(result["record"], result.get("events_emitted", ()))
        return result

    def configure_exposure_limit(self, payload: dict) -> dict:
        tenant = payload.get("tenant")
        self._hydrate_service_state(tenant=tenant)
        result = self.service.command_exposure_limit(payload)
        self.repository.save_exposure_limit(result["record"], result.get("events_emitted", ()))
        return result

    def publish_market_price_curve(self, payload: dict) -> dict:
        tenant = payload.get("tenant")
        self._hydrate_service_state(tenant=tenant)
        result = self.service.command_market_price_curve(payload)
        self.repository.save_market_price_curve(result["record"], result.get("events_emitted", ()))
        return result

    def capture_trade_position(self, payload: dict) -> dict:
        tenant = payload.get("tenant")
        self._hydrate_service_state(tenant=tenant)
        result = self.service.command_trade_position(payload)
        self.repository.save_trade_position(result["record"], result.get("events_emitted", ()))
        return {
            **result,
            "form": self.service.trade_capture_form()["form"],
            "wizard": self.service.energy_risk_wizard({"wizard_id": "trade_capture_release"})["wizard"],
            "controls": self.service.energy_risk_controls()["controls"],
            "agent_help": build_operator_guidance(record=result["record"]),
        }

    def submit_nomination(self, payload: dict) -> dict:
        tenant = payload.get("tenant")
        self._hydrate_service_state(tenant=tenant)
        result = self.service.command_nomination(payload)
        self.repository.save_nomination(result["record"], result.get("events_emitted", ()))
        return {
            **result,
            "wizard": self.service.energy_risk_wizard({"wizard_id": "nomination_exception_recovery"})["wizard"],
            "controls": self.service.energy_risk_controls()["controls"],
            "agent_help": build_operator_guidance(record=result["record"]),
        }

    def approve_schedule(self, payload: dict) -> dict:
        tenant = payload.get("tenant")
        self._hydrate_service_state(tenant=tenant)
        result = self.service.command_schedule(payload)
        self.repository.save_schedule(result["record"], result.get("events_emitted", ()))
        return result

    def record_settlement(self, payload: dict) -> dict:
        tenant = payload.get("tenant")
        self._hydrate_service_state(tenant=tenant)
        result = self.service.command_settlement(payload)
        self.repository.save_settlement(result["record"], result.get("events_emitted", ()))
        return result

    def workbench(self, filters=None) -> dict:
        filters = dict(filters or {})
        self._hydrate_service_state(tenant=filters.get("tenant"))
        result = self.service.query_workbench(filters)
        return {
            **result,
            "controls": energy_trading_risk_control_catalog(),
            "forms": energy_trading_risk_form_catalog(),
            "wizards": energy_trading_risk_wizard_catalog(),
            "agent_help": build_operator_guidance(workbench=result),
        }

    def app_contract(self) -> dict:
        self._hydrate_service_state()
        return {
            "ok": True,
            "app": energy_trading_risk_single_pbc_app_ui_contract(),
            "forms": energy_trading_risk_form_catalog(),
            "wizards": energy_trading_risk_wizard_catalog(),
            "controls": energy_trading_risk_control_catalog(),
            "agent_help": assistant_help_manifest(),
            "database": self.repository.database_manifest(),
            "services": service_operation_manifest(),
            "routes": ROUTES,
            "migrations_applied": self.applied_migrations,
            "side_effects": (),
        }
