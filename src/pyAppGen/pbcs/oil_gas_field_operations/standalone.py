"""Standalone one-PBC application surface for oil_gas_field_operations."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from . import agent
from . import controls
from . import events
from . import forms
from . import runtime
from . import ui
from . import wizards
from .domain_depth import execute_domain_operation

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.OIL_GAS_FIELD_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy": "field_operations_default",
    "workbench_limit": 100,
}

DEFAULT_PARAMETERS = {
    "workbench_limit": 100,
    "risk_threshold": 0.65,
    "approval_sla_hours": 24,
    "materiality_threshold": 10.0,
    "quality_score_floor": 0.8,
}

DEFAULT_RULES = (
    {
        "rule_id": "oil_gas.production.balance.default",
        "tenant": "default",
        "scope": "allocation",
        "max_deferred_oil_bbl": 25.0,
        "requires_gas_disposition": True,
        "status": "active",
    },
    {
        "rule_id": "oil_gas.workover.readiness.default",
        "tenant": "default",
        "scope": "workover",
        "requires_permit_status": "approved",
        "max_open_hse_events": 0,
        "status": "active",
    },
)


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


class OilGasFieldOperationsStandaloneApp:
    """Executable one-PBC app for route surveillance and workover readiness."""

    def __init__(self, database_path: str = ":memory:") -> None:
        self.database_path = database_path
        self.runtime_state = runtime.oil_gas_field_operations_empty_state()
        configured = runtime.oil_gas_field_operations_configure_runtime(self.runtime_state, DEFAULT_CONFIGURATION)
        self.runtime_state = configured["state"]
        for name, value in DEFAULT_PARAMETERS.items():
            result = runtime.oil_gas_field_operations_set_parameter(self.runtime_state, name, value)
            self.runtime_state = result["state"]
        for rule in DEFAULT_RULES:
            result = runtime.oil_gas_field_operations_register_rule(self.runtime_state, rule)
            self.runtime_state = result["state"]
        self.wells: dict[str, dict[str, Any]] = {}
        self.production_records: dict[str, dict[str, Any]] = {}
        self.field_tickets: dict[str, dict[str, Any]] = {}
        self.workover_packs: dict[str, dict[str, Any]] = {}
        self.hse_events: dict[str, dict[str, Any]] = {}
        self.morning_reviews: dict[str, dict[str, Any]] = {}
        self.operation_log: list[dict[str, Any]] = []

    def _record_domain_operation(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        evidence = execute_domain_operation(operation, payload)
        envelope = events.build_event_envelope(evidence.get("emitted_event", events.EMITTED[0]), payload)
        self.operation_log.append(
            {
                "operation": operation,
                "payload": deepcopy(payload),
                "domain_evidence": evidence,
                "event": envelope,
            }
        )
        return evidence

    def snapshot_state(self) -> dict[str, Any]:
        return {
            "wells": deepcopy(self.wells),
            "production_records": deepcopy(self.production_records),
            "field_tickets": deepcopy(self.field_tickets),
            "workover_packs": deepcopy(self.workover_packs),
            "hse_events": deepcopy(self.hse_events),
            "operation_log": tuple(deepcopy(self.operation_log)),
        }

    def register_well(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        validation = forms.oil_gas_field_operations_validate_form_payload("well_hierarchy_intake", supplied)
        if not validation["ok"]:
            return {"ok": False, "validation": validation, "side_effects": ()}
        well_id = supplied["well_id"]
        command = runtime.oil_gas_field_operations_command_well(self.runtime_state, {"id": well_id, **supplied})
        self.runtime_state = command["state"]
        record = {
            **supplied,
            "id": well_id,
            "status": supplied["lifecycle_state"],
            "workbench_queue": "route_surveillance" if supplied["lifecycle_state"] == "producing" else "non_producing",
        }
        self.wells[well_id] = record
        domain_event = self._record_domain_operation("create_well", supplied)
        return {
            "ok": True,
            "record": record,
            "validation": validation,
            "form": forms.oil_gas_field_operations_get_form("well_hierarchy_intake")["form"],
            "controls": controls.oil_gas_field_operations_mutation_preview("create", "oil_gas_field_operations_well", supplied),
            "agent_help": agent.oil_gas_field_operations_assistant_preview(
                {
                    "document_text": f"Register well {well_id} on route {supplied['route_code']}.",
                    "instructions": "Preview the well creation plan.",
                    "target_entity": "well",
                    "requested_action": "create",
                    "payload": supplied,
                }
            ),
            "domain_event": domain_event,
            "side_effects": (),
        }

    def record_daily_production(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        validation = forms.oil_gas_field_operations_validate_form_payload("daily_production_capture", supplied)
        if not validation["ok"]:
            return {"ok": False, "validation": validation, "side_effects": ()}
        well_id = supplied["well_id"]
        if well_id not in self.wells:
            return {"ok": False, "reason": "unknown_well", "well_id": well_id, "validation": validation, "side_effects": ()}
        record_id = f"{well_id}:{supplied['production_date']}"
        deferred_oil_bbl = round(float(supplied.get("oil_bbl", 0.0)) * (float(supplied.get("downtime_hours", 0.0)) / 24.0), 2)
        queue = "production_ready"
        if supplied["production_test_state"] != "allocation_approved" or deferred_oil_bbl > 25.0:
            queue = "production_surveillance"
        if supplied["measurement_basis"] == "revised":
            queue = "allocation_exceptions"
        record = {
            **supplied,
            "id": record_id,
            "deferred_oil_bbl": deferred_oil_bbl,
            "workbench_queue": queue,
            "status": "allocation_ready" if queue == "production_ready" else "review_required",
        }
        self.production_records[record_id] = record
        self.wells[well_id]["last_production_date"] = supplied["production_date"]
        self.wells[well_id]["latest_queue"] = queue
        domain_event = self._record_domain_operation("record_production_reading", supplied)
        return {
            "ok": True,
            "record": record,
            "validation": validation,
            "form": forms.oil_gas_field_operations_get_form("daily_production_capture")["form"],
            "wizard": wizards.oil_gas_field_operations_plan_wizard(
                "morning_production_review",
                {"well_id": well_id, "production_date": supplied["production_date"]},
            ),
            "controls": controls.oil_gas_field_operations_mutation_preview("create", "oil_gas_field_operations_production_reading", supplied),
            "domain_event": domain_event,
            "side_effects": (),
        }

    def open_field_ticket(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        validation = forms.oil_gas_field_operations_validate_form_payload("field_ticket_triage", supplied)
        if not validation["ok"]:
            return {"ok": False, "validation": validation, "side_effects": ()}
        ticket_id = supplied["ticket_id"]
        queue = "route_attention" if supplied["severity"] in {"high", "critical"} or supplied["requires_shutdown"] else "monitor"
        record = {**supplied, "id": ticket_id, "status": "open", "workbench_queue": queue}
        self.field_tickets[ticket_id] = record
        domain_event = self._record_domain_operation("review_field_ticket", supplied)
        return {
            "ok": True,
            "record": record,
            "validation": validation,
            "form": forms.oil_gas_field_operations_get_form("field_ticket_triage")["form"],
            "controls": controls.oil_gas_field_operations_mutation_preview("create", "oil_gas_field_operations_field_ticket", supplied),
            "domain_event": domain_event,
            "side_effects": (),
        }

    def prepare_workover_readiness_pack(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        validation = forms.oil_gas_field_operations_validate_form_payload("workover_readiness_pack", supplied)
        if not validation["ok"]:
            return {"ok": False, "validation": validation, "side_effects": ()}
        well_id = supplied["well_id"]
        if well_id not in self.wells:
            return {"ok": False, "reason": "unknown_well", "well_id": well_id, "validation": validation, "side_effects": ()}
        latest_production = next(
            (item for item in reversed(list(self.production_records.values())) if item["well_id"] == well_id),
            None,
        )
        related_tickets = [item for item in self.field_tickets.values() if item["well_id"] == well_id and item["status"] == "open"]
        open_reportable_hse = [item for item in self.hse_events.values() if item["well_id"] == well_id and item.get("reportable")]
        status = "ready"
        if supplied["permit_status"] != "approved" or supplied["barrier_risk"] == "high" or open_reportable_hse:
            status = "hold"
        pack = {
            **supplied,
            "id": supplied["plan_id"],
            "status": status,
            "latest_production": latest_production,
            "open_ticket_count": len(related_tickets),
            "open_reportable_hse": len(open_reportable_hse),
        }
        self.workover_packs[pack["id"]] = pack
        domain_event = self._record_domain_operation("approve_workover_plan", supplied)
        return {
            "ok": True,
            "record": pack,
            "validation": validation,
            "form": forms.oil_gas_field_operations_get_form("workover_readiness_pack")["form"],
            "wizard": wizards.oil_gas_field_operations_plan_wizard("workover_readiness", {"well_id": well_id}),
            "controls": controls.oil_gas_field_operations_control_center(self.snapshot_state()),
            "domain_event": domain_event,
            "side_effects": (),
        }

    def log_hse_event(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        validation = forms.oil_gas_field_operations_validate_form_payload("hse_boundary_event", supplied)
        if not validation["ok"]:
            return {"ok": False, "validation": validation, "side_effects": ()}
        record = {
            **supplied,
            "id": supplied["event_id"],
            "status": "escalated" if supplied["reportable"] or supplied["containment_status"] == "escalated" else "monitoring",
        }
        self.hse_events[record["id"]] = record
        domain_event = self._record_domain_operation("simulate_hse_event", supplied)
        return {
            "ok": True,
            "record": record,
            "validation": validation,
            "form": forms.oil_gas_field_operations_get_form("hse_boundary_event")["form"],
            "controls": controls.oil_gas_field_operations_mutation_preview("create", "oil_gas_field_operations_hse_event", supplied),
            "domain_event": domain_event,
            "side_effects": (),
        }

    def morning_production_review(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        validation = forms.oil_gas_field_operations_validate_form_payload("morning_review_request", supplied)
        if not validation["ok"]:
            return {"ok": False, "validation": validation, "side_effects": ()}
        route_filter = supplied.get("route_code")
        minimum_deferred = float(supplied.get("minimum_deferred_oil_bbl", 0.0))
        latest_by_well = {}
        for record in self.production_records.values():
            latest_by_well[record["well_id"]] = record
        findings = []
        for well_id, record in latest_by_well.items():
            well = self.wells.get(well_id, {})
            if route_filter and well.get("route_code") != route_filter:
                continue
            if float(record.get("deferred_oil_bbl", 0.0)) < minimum_deferred and record.get("production_test_state") == "allocation_approved":
                continue
            open_tickets = [item for item in self.field_tickets.values() if item["well_id"] == well_id and item["status"] == "open"]
            findings.append(
                {
                    "well_id": well_id,
                    "route_code": well.get("route_code"),
                    "pad_name": well.get("pad_name"),
                    "deferred_oil_bbl": record.get("deferred_oil_bbl", 0.0),
                    "production_test_state": record.get("production_test_state"),
                    "integrity_risk": well.get("integrity_risk"),
                    "open_ticket_count": len(open_tickets),
                    "latest_queue": record.get("workbench_queue"),
                }
            )
        findings.sort(key=lambda item: (item["deferred_oil_bbl"], item["open_ticket_count"]), reverse=True)
        review_id = f"review_{len(self.morning_reviews) + 1:03d}"
        review = {
            "review_id": review_id,
            "route_code": route_filter,
            "summary": {
                "high_priority_wells": len(findings),
                "invalid_tests": sum(1 for item in findings if item["production_test_state"] != "allocation_approved"),
                "integrity_flags": sum(1 for item in findings if item["integrity_risk"] in {"watch", "high"}),
            },
            "findings": tuple(findings),
        }
        self.morning_reviews[review_id] = review
        return {
            "ok": True,
            "review": review,
            "validation": validation,
            "wizard": wizards.oil_gas_field_operations_plan_wizard(
                "morning_production_review",
                {"well_id": next(iter(self.wells), "preview"), "production_date": next(iter(self.production_records.values()), {}).get("production_date", "preview")},
            ),
            "assistant_preview": agent.oil_gas_field_operations_assistant_preview(supplied),
            "side_effects": (),
        }

    def workbench(self, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        supplied = _copy_payload(filters)
        route_filter = supplied.get("route_code")
        records = []
        latest_by_well = {}
        for record in self.production_records.values():
            latest_by_well[record["well_id"]] = record
        for well_id, well in self.wells.items():
            if route_filter and well.get("route_code") != route_filter:
                continue
            latest = latest_by_well.get(well_id, {})
            tickets = [item for item in self.field_tickets.values() if item["well_id"] == well_id and item["status"] == "open"]
            hse = [item for item in self.hse_events.values() if item["well_id"] == well_id]
            records.append(
                {
                    "id": well_id,
                    "route_code": well.get("route_code"),
                    "pad_name": well.get("pad_name"),
                    "lease_name": well.get("lease_name"),
                    "lifecycle_state": well.get("lifecycle_state"),
                    "lift_type": well.get("lift_type"),
                    "integrity_risk": well.get("integrity_risk"),
                    "latest_queue": latest.get("workbench_queue", well.get("workbench_queue")),
                    "deferred_oil_bbl": latest.get("deferred_oil_bbl", 0.0),
                    "production_test_state": latest.get("production_test_state"),
                    "open_ticket_count": len(tickets),
                    "reportable_hse": sum(1 for item in hse if item.get("reportable")),
                }
            )
        summary = {
            "producing_wells": sum(1 for item in self.wells.values() if item.get("lifecycle_state") == "producing"),
            "surveillance_wells": sum(1 for item in records if item.get("latest_queue") == "production_surveillance"),
            "allocation_exceptions": sum(1 for item in records if item.get("latest_queue") == "allocation_exceptions"),
            "open_field_tickets": sum(1 for item in self.field_tickets.values() if item.get("status") == "open"),
            "ready_workover_packs": sum(1 for item in self.workover_packs.values() if item.get("status") == "ready"),
            "reportable_hse": sum(1 for item in self.hse_events.values() if item.get("reportable")),
        }
        return {
            "ok": True,
            "pbc": "oil_gas_field_operations",
            "route_code": route_filter,
            "summary": summary,
            "records": tuple(sorted(records, key=lambda item: (item["deferred_oil_bbl"], item["open_ticket_count"]), reverse=True)),
            "forms": forms.oil_gas_field_operations_form_catalog()["form_ids"],
            "wizards": wizards.oil_gas_field_operations_wizard_catalog()["wizard_ids"],
            "controls": controls.oil_gas_field_operations_control_catalog()["control_ids"],
            "side_effects": (),
        }

    def close(self) -> None:
        return None


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": "oil_gas_field_operations",
        "app_class": "OilGasFieldOperationsStandaloneApp",
        "implementation_directory": "src/pyAppGen/pbcs/oil_gas_field_operations",
        "service_methods": (
            "register_well",
            "record_daily_production",
            "open_field_ticket",
            "prepare_workover_readiness_pack",
            "log_hse_event",
            "morning_production_review",
            "workbench",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench"),
        "docs": ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"),
        "event_contract": "AppGen-X",
        "event_topic": runtime.OIL_GAS_FIELD_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": runtime.OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    }


def oil_gas_field_operations_standalone_app_contract() -> dict:
    forms_catalog = forms.oil_gas_field_operations_form_catalog()
    wizards_catalog = wizards.oil_gas_field_operations_wizard_catalog()
    controls_catalog = controls.oil_gas_field_operations_control_catalog()
    workbench_blueprint = ui.oil_gas_field_operations_standalone_workbench_blueprint()
    agent_surface = agent.agent_skill_manifest()
    return {
        "format": "appgen.oil-gas-field-operations-standalone-app.v1",
        "ok": all(
            item.get("ok") is True
            for item in (forms_catalog, wizards_catalog, controls_catalog, workbench_blueprint, agent_surface)
        ),
        "pbc": "oil_gas_field_operations",
        "manifest": standalone_manifest(),
        "forms": forms_catalog,
        "wizards": wizards_catalog,
        "controls": controls_catalog,
        "ui": workbench_blueprint,
        "agent": agent_surface,
        "side_effects": (),
    }


def oil_gas_field_operations_bootstrap_standalone_app(database_path: str = ":memory:") -> dict:
    app = OilGasFieldOperationsStandaloneApp(database_path=database_path)
    return {
        "ok": True,
        "pbc": "oil_gas_field_operations",
        "app": app,
        "contract": oil_gas_field_operations_standalone_app_contract(),
        "side_effects": (),
    }


def documentation_presence() -> dict:
    base = Path(__file__).resolve().parent
    docs = {name: (base / name).exists() for name in standalone_manifest()["docs"]}
    return {"ok": all(docs.values()), "docs": docs, "side_effects": ()}


def oil_gas_field_operations_standalone_app_smoke() -> dict:
    bundle = oil_gas_field_operations_bootstrap_standalone_app()
    app = bundle["app"]
    try:
        well = app.register_well(
            {
                "tenant": "tenant-smoke",
                "well_id": "OG-7H",
                "field_name": "North Basin",
                "area_name": "Area-1",
                "pad_name": "Pad-A",
                "lease_name": "Lease-77",
                "route_code": "ROUTE-7",
                "wellbore": "7H",
                "completion": "Wolfcamp A",
                "interval_name": "Upper",
                "lifecycle_state": "producing",
                "lift_type": "esp",
                "integrity_risk": "watch",
            }
        )
        production = app.record_daily_production(
            {
                "well_id": "OG-7H",
                "production_date": "2026-05-29",
                "oil_bbl": 160.0,
                "gas_mcf": 780.0,
                "water_bbl": 95.0,
                "injected_water_bbl": 0.0,
                "gas_disposition": "sales",
                "oil_disposition": "sold",
                "measurement_basis": "allocated",
                "production_test_state": "allocation_approved",
                "downtime_hours": 2.0,
                "revision_reason": "separator_test_finalized",
            }
        )
        ticket = app.open_field_ticket(
            {
                "ticket_id": "FT-7",
                "well_id": "OG-7H",
                "ticket_type": "integrity",
                "severity": "high",
                "deferred_oil_bbl": 18.0,
                "root_cause": "annulus pressure increase",
                "requires_shutdown": False,
                "route_code": "ROUTE-7",
            }
        )
        workover = app.prepare_workover_readiness_pack(
            {
                "plan_id": "WO-7",
                "well_id": "OG-7H",
                "candidate_reason": "repeat annulus pressure and ESP instability",
                "expected_recovery_bopd": 60.0,
                "permit_status": "approved",
                "barrier_risk": "watch",
                "lift_failure_mode": "current_imbalance",
            }
        )
        hse = app.log_hse_event(
            {
                "event_id": "HSE-7",
                "well_id": "OG-7H",
                "event_classification": "release",
                "reportable": False,
                "spill_bbl": 0.5,
                "containment_status": "contained",
                "ignition_risk": False,
                "people_affected": 0,
            }
        )
        review = app.morning_production_review(
            {
                "route_code": "ROUTE-7",
                "minimum_deferred_oil_bbl": 5.0,
                "document_text": "Prepare ROUTE-7 morning production review.",
                "instructions": "Read only.",
                "target_entity": "production_reading",
                "requested_action": "read",
            }
        )
        workbench = app.workbench({"route_code": "ROUTE-7"})
        rendered = ui.oil_gas_field_operations_render_standalone_workbench(workbench)
        docs = documentation_presence()
        return {
            "ok": bundle["contract"]["ok"] and well["ok"] and production["ok"] and ticket["ok"] and workover["ok"] and hse["ok"] and review["ok"] and workbench["ok"] and rendered["ok"] and docs["ok"],
            "contract": bundle["contract"],
            "well": well,
            "production": production,
            "ticket": ticket,
            "workover": workover,
            "hse": hse,
            "review": review,
            "workbench": workbench,
            "rendered": rendered,
            "docs": docs,
            "side_effects": (),
        }
    finally:
        app.close()
