"""Executable standalone one-PBC application surface for laboratory_information_management."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any

from .controls import laboratory_information_management_control_catalog
from .forms import laboratory_information_management_form_catalog
from .runtime import LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import LABORATORY_INFORMATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .wizards import laboratory_information_management_wizard_catalog


PBC_KEY = "laboratory_information_management"
EVENT_TOPIC = LABORATORY_INFORMATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
ALLOWED_DATABASE_BACKENDS = LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS

OWNED_TABLES = {
    "sample": "laboratory_information_management_lab_sample",
    "test_order": "laboratory_information_management_test_order",
    "batch_run": "laboratory_information_management_lab_batch",
    "instrument_run": "laboratory_information_management_instrument_run",
    "result": "laboratory_information_management_result",
    "quality_control": "laboratory_information_management_quality_control",
    "chain_of_custody": "laboratory_information_management_chain_custody",
    "policy_rule": "laboratory_information_management_laboratory_information_management_policy_rule",
    "runtime_parameter": "laboratory_information_management_laboratory_information_management_runtime_parameter",
    "governed_model": "laboratory_information_management_laboratory_information_management_governed_model",
}

ENTITY_TO_FORM = {
    "sample": "sample_accessioning",
    "test_order": "test_order_intake",
    "batch_run": "batch_run_execution",
    "result": "result_review_and_release",
    "oos": "oos_investigation",
    "stability_study": "stability_study_scheduler",
    "reagent_inventory": "qc_and_reagent_lot",
    "analyst_competency": "instrument_calibration_console",
    "certificate_of_analysis": "certificate_of_analysis",
}

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": EVENT_TOPIC,
    "retry_limit": 3,
    "default_policy": "cGMP",
    "workbench_limit": 100,
    "assistant_mutations_require_confirmation": True,
}

DEFAULT_PARAMETERS = {
    "identity_confidence_floor": 0.95,
    "critical_result_notification_minutes": 30,
    "result_release_requires_qc": True,
    "stability_pull_warning_days": 2,
    "competency_warning_days": 30,
    "reagent_low_stock_threshold": 10,
}

DEFAULT_RULES = (
    {
        "rule_id": "lims.sample.identity",
        "scope": "sample_accessioning",
        "status": "active",
        "minimum_identity_confidence": 0.95,
        "reject_duplicate_accessions": True,
    },
    {
        "rule_id": "lims.release.qc",
        "scope": "result_release",
        "status": "active",
        "require_qc_pass": True,
        "require_chain_of_custody_intact": True,
        "require_esignature": True,
    },
)

DEFAULT_METHOD = {
    "method_id": "METH-HPLC-ASSAY-V3",
    "name": "Potency assay by HPLC",
    "version": "3.2",
    "sop_id": "SOP-HPLC-017",
    "validation_status": "validated",
    "effective_from": "2026-01-01",
    "instrument_capabilities": ("INST-HPLC-01",),
    "specification_low": 98.0,
    "specification_high": 102.0,
    "critical_high": 105.0,
    "units": "% label claim",
}

DEFAULT_INSTRUMENT = {
    "instrument_id": "INST-HPLC-01",
    "location": "Chemistry Bench 4",
    "status": "available",
    "qualification_state": "qualified",
    "method_capabilities": ("METH-HPLC-ASSAY-V3",),
    "maintenance_due": "2026-12-31",
    "calibration_due": "2026-06-30",
}

DEFAULT_CALIBRATION = {
    "calibration_id": "CAL-HPLC-01",
    "instrument_id": "INST-HPLC-01",
    "method_id": "METH-HPLC-ASSAY-V3",
    "performed_on": "2026-05-01",
    "expires_on": "2026-06-30",
    "result": "pass",
    "drift_percent": 0.3,
}

DEFAULT_QC_LOT = {
    "qc_lot_id": "QC-ASSAY-2026-01",
    "analyte": "assay",
    "expected_low": 99.0,
    "expected_high": 101.0,
    "expiry_date": "2026-12-31",
    "status": "qualified",
}

DEFAULT_REAGENT_LOT = {
    "reagent_lot_id": "REAGENT-MOBILE-PHASE-01",
    "name": "Mobile phase A",
    "expiry_date": "2026-12-31",
    "storage_condition": "ambient",
    "qualification_status": "qualified",
    "quantity_on_hand": 100,
    "reorder_point": 10,
}

DEFAULT_COMPETENCY = {
    "competency_id": "COMP-ADA-HPLC",
    "analyst_id": "analyst_ada",
    "method_id": "METH-HPLC-ASSAY-V3",
    "status": "current",
    "valid_until": "2026-12-31",
    "last_assessed_on": "2026-05-01",
}


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


def _ensure_state(state: dict[str, Any] | None = None) -> dict[str, Any]:
    enriched = dict(state or {})
    defaults: dict[str, Any] = {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "samples": {},
        "accession_index": {},
        "chain_of_custody": {},
        "orders": {},
        "methods": {},
        "instruments": {},
        "calibrations": {},
        "qc_lots": {},
        "reagent_lots": {},
        "analyst_competencies": {},
        "batch_runs": {},
        "results": {},
        "oos_events": {},
        "stability_studies": {},
        "stability_pulls": {},
        "certificates": {},
        "document_previews": {},
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "audit_trail": (),
        "critical_notifications": {},
        "corrections": {},
        "capa": {},
        "sequence": 0,
    }
    for key, default in defaults.items():
        if key not in enriched:
            enriched[key] = deepcopy(default)
    return enriched


def _sequence(state: dict[str, Any], prefix: str) -> tuple[dict[str, Any], str]:
    next_value = int(state.get("sequence", 0)) + 1
    return {**state, "sequence": next_value}, f"{prefix}-{next_value:05d}"


def _timestamp(state: dict[str, Any]) -> str:
    return f"2026-05-30T00:00:{int(state.get('sequence', 0)):02d}Z"


def _hash(payload: Any) -> str:
    return hashlib.sha256(repr(payload).encode("utf-8")).hexdigest()


def _append_event(state: dict[str, Any], event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    event = {
        "event_id": _hash((event_type, payload, len(state.get("outbox", ()))))[:16],
        "event_type": event_type,
        "topic": EVENT_TOPIC,
        "payload": deepcopy(payload),
    }
    return {**state, "outbox": (*tuple(state.get("outbox", ())), event)}


def _append_audit(state: dict[str, Any], action: str, record_type: str, record_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    previous_hash = state.get("audit_trail", ())[-1]["entry_hash"] if state.get("audit_trail") else "GENESIS"
    entry = {
        "audit_id": f"audit-{len(state.get('audit_trail', ())) + 1:05d}",
        "timestamp": _timestamp(state),
        "action": action,
        "record_type": record_type,
        "record_id": record_id,
        "payload": deepcopy(payload),
        "previous_hash": previous_hash,
    }
    entry["entry_hash"] = _hash((entry["timestamp"], action, record_type, record_id, entry["payload"], previous_hash))
    return {**state, "audit_trail": (*tuple(state.get("audit_trail", ())), entry)}


def _set_record(state: dict[str, Any], collection: str, key: str, value: dict[str, Any]) -> dict[str, Any]:
    records = dict(state.get(collection, {}))
    records[key] = deepcopy(value)
    return {**state, collection: records}


def _instrument_ready(state: dict[str, Any], instrument_id: str, method_id: str) -> tuple[bool, tuple[str, ...]]:
    instrument = state.get("instruments", {}).get(instrument_id)
    blockers: list[str] = []
    if instrument is None:
        return False, ("unknown_instrument",)
    if instrument.get("status") != "available":
        blockers.append("instrument_unavailable")
    if instrument.get("qualification_state") != "qualified":
        blockers.append("instrument_unqualified")
    if method_id not in tuple(instrument.get("method_capabilities", ())):
        blockers.append("method_not_supported")
    calibration = next(
        (
            item
            for item in state.get("calibrations", {}).values()
            if item["instrument_id"] == instrument_id and item["method_id"] == method_id
        ),
        None,
    )
    if calibration is None:
        blockers.append("missing_calibration")
    elif calibration.get("result") != "pass":
        blockers.append("calibration_failed")
    return not blockers, tuple(blockers)


def _reagent_ready(state: dict[str, Any], reagent_lot_ids: tuple[str, ...]) -> tuple[bool, tuple[str, ...]]:
    blockers: list[str] = []
    threshold = int(state.get("parameters", {}).get("reagent_low_stock_threshold", DEFAULT_PARAMETERS["reagent_low_stock_threshold"]))
    for reagent_lot_id in reagent_lot_ids:
        lot = state.get("reagent_lots", {}).get(reagent_lot_id)
        if lot is None:
            blockers.append(f"unknown_reagent:{reagent_lot_id}")
            continue
        if lot.get("qualification_status") != "qualified":
            blockers.append(f"reagent_not_qualified:{reagent_lot_id}")
        if int(lot.get("quantity_on_hand", 0)) <= 0:
            blockers.append(f"reagent_depleted:{reagent_lot_id}")
        if int(lot.get("quantity_on_hand", 0)) <= threshold:
            blockers.append(f"reagent_low_stock:{reagent_lot_id}")
    return not blockers or all(item.startswith("reagent_low_stock:") for item in blockers), tuple(blockers)


def _competency_ready(state: dict[str, Any], analyst_id: str, method_id: str) -> tuple[bool, str | None]:
    for competency in state.get("analyst_competencies", {}).values():
        if competency["analyst_id"] == analyst_id and competency["method_id"] == method_id:
            if competency.get("status") == "current":
                return True, None
            return False, "competency_not_current"
    return False, "missing_competency"


def _sample_custody_ok(state: dict[str, Any], sample_id: str) -> bool:
    sample = state.get("samples", {}).get(sample_id)
    return bool(sample) and not sample.get("custody_exception_open", False)


def _result_release_blockers(state: dict[str, Any], result: dict[str, Any]) -> tuple[str, ...]:
    blockers: list[str] = []
    batch = state.get("batch_runs", {}).get(result["batch_run_id"])
    if batch is None:
        blockers.append("missing_batch_run")
    else:
        if batch.get("status") != "reviewed":
            blockers.append("batch_not_reviewed")
        if not batch.get("qc_passed"):
            blockers.append("qc_not_passed")
    if not _sample_custody_ok(state, result["sample_id"]):
        blockers.append("custody_exception_open")
    if result.get("status") in {"oos_hold", "oos_investigation"}:
        blockers.append("oos_unresolved")
    if result.get("technical_review_status") != "approved":
        blockers.append("technical_review_missing")
    return tuple(blockers)


def _extract_citations(document_text: str, keywords: tuple[str, ...]) -> tuple[dict[str, Any], ...]:
    citations: list[dict[str, Any]] = []
    for line_number, line in enumerate(str(document_text).splitlines(), start=1):
        lowered = line.lower()
        if any(keyword in lowered for keyword in keywords):
            citations.append({"line": line_number, "excerpt": line.strip()[:160]})
    if not citations and document_text:
        first_line = str(document_text).splitlines()[0]
        citations.append({"line": 1, "excerpt": first_line[:160]})
    return tuple(citations)


class LaboratoryInformationManagementStandaloneApp:
    """Mutable one-PBC application shell for laboratory operations."""

    def __init__(self, tenant: str = "default") -> None:
        self.tenant = tenant
        self.state = _ensure_state({"tenant": tenant})

    def configure(self, configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        supplied = {**DEFAULT_CONFIGURATION, **_copy_payload(configuration)}
        ok = supplied.get("database_backend") in ALLOWED_DATABASE_BACKENDS and supplied.get("event_topic") == EVENT_TOPIC
        self.state = {**self.state, "configuration": supplied}
        self.state = _append_audit(self.state, "configure", "configuration", "runtime", supplied)
        return {"ok": ok, "configuration": supplied, "state": self.state, "side_effects": ()}

    def register_defaults(self) -> dict[str, Any]:
        self.state = {**self.state, "parameters": dict(DEFAULT_PARAMETERS)}
        self.state = {**self.state, "rules": {rule["rule_id"]: dict(rule) for rule in DEFAULT_RULES}}
        method = self.register_method(DEFAULT_METHOD)
        instrument = self.manage_instrument(DEFAULT_INSTRUMENT)
        calibration = self.record_calibration(DEFAULT_CALIBRATION)
        qc_lot = self.register_qc_lot(DEFAULT_QC_LOT)
        reagent = self.adjust_reagent_inventory(DEFAULT_REAGENT_LOT)
        competency = self.record_analyst_competency(DEFAULT_COMPETENCY)
        return {
            "ok": all(item["ok"] for item in (method, instrument, calibration, qc_lot, reagent, competency)),
            "defaults": {
                "method": method,
                "instrument": instrument,
                "calibration": calibration,
                "qc_lot": qc_lot,
                "reagent": reagent,
                "competency": competency,
            },
            "state": self.state,
            "side_effects": (),
        }

    def register_method(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        method_id = supplied["method_id"]
        record = {
            "method_id": method_id,
            "name": supplied["name"],
            "version": supplied["version"],
            "sop_id": supplied["sop_id"],
            "validation_status": supplied["validation_status"],
            "effective_from": supplied["effective_from"],
            "specification_low": float(supplied["specification_low"]),
            "specification_high": float(supplied["specification_high"]),
            "critical_high": float(supplied.get("critical_high", supplied["specification_high"])),
            "units": supplied.get("units", "units"),
            "instrument_capabilities": tuple(supplied.get("instrument_capabilities", ())),
        }
        self.state = _set_record(self.state, "methods", method_id, record)
        self.state = _append_audit(self.state, "register_method", "method", method_id, record)
        return {"ok": record["validation_status"] == "validated", "method": record, "state": self.state, "side_effects": ()}

    def manage_instrument(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        instrument_id = supplied["instrument_id"]
        record = {
            "instrument_id": instrument_id,
            "location": supplied["location"],
            "status": supplied["status"],
            "qualification_state": supplied["qualification_state"],
            "method_capabilities": tuple(supplied.get("method_capabilities", ())),
            "maintenance_due": supplied.get("maintenance_due"),
            "calibration_due": supplied.get("calibration_due"),
        }
        self.state = _set_record(self.state, "instruments", instrument_id, record)
        self.state = _append_audit(self.state, "manage_instrument", "instrument", instrument_id, record)
        return {"ok": record["qualification_state"] == "qualified", "instrument": record, "state": self.state, "side_effects": ()}

    def record_calibration(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        calibration_id = supplied["calibration_id"]
        record = {
            "calibration_id": calibration_id,
            "instrument_id": supplied["instrument_id"],
            "method_id": supplied["method_id"],
            "performed_on": supplied["performed_on"],
            "expires_on": supplied["expires_on"],
            "result": supplied["result"],
            "drift_percent": float(supplied.get("drift_percent", 0.0)),
        }
        self.state = _set_record(self.state, "calibrations", calibration_id, record)
        self.state = _append_audit(self.state, "record_calibration", "calibration", calibration_id, record)
        return {"ok": record["result"] == "pass", "calibration": record, "state": self.state, "side_effects": ()}

    def register_qc_lot(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        qc_lot_id = supplied["qc_lot_id"]
        record = {
            "qc_lot_id": qc_lot_id,
            "analyte": supplied["analyte"],
            "expected_low": float(supplied["expected_low"]),
            "expected_high": float(supplied["expected_high"]),
            "expiry_date": supplied["expiry_date"],
            "status": supplied.get("status", supplied.get("qualification_status", "qualified")),
        }
        self.state = _set_record(self.state, "qc_lots", qc_lot_id, record)
        self.state = _append_audit(self.state, "register_qc_lot", "qc_lot", qc_lot_id, record)
        return {"ok": record["status"] == "qualified", "qc_lot": record, "state": self.state, "side_effects": ()}

    def adjust_reagent_inventory(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        reagent_lot_id = supplied["reagent_lot_id"]
        previous = self.state.get("reagent_lots", {}).get(reagent_lot_id, {})
        record = {
            "reagent_lot_id": reagent_lot_id,
            "name": supplied.get("name", previous.get("name", reagent_lot_id)),
            "expiry_date": supplied["expiry_date"],
            "storage_condition": supplied.get("storage_condition", previous.get("storage_condition", "ambient")),
            "qualification_status": supplied.get("qualification_status", previous.get("qualification_status", "qualified")),
            "quantity_on_hand": int(supplied.get("quantity_on_hand", previous.get("quantity_on_hand", 0))),
            "reorder_point": int(supplied.get("reorder_point", previous.get("reorder_point", DEFAULT_PARAMETERS["reagent_low_stock_threshold"]))),
        }
        self.state = _set_record(self.state, "reagent_lots", reagent_lot_id, record)
        self.state = _append_audit(self.state, "adjust_reagent_inventory", "reagent_lot", reagent_lot_id, record)
        return {"ok": record["qualification_status"] == "qualified", "reagent_lot": record, "state": self.state, "side_effects": ()}

    def record_analyst_competency(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        competency_id = supplied["competency_id"]
        record = {
            "competency_id": competency_id,
            "analyst_id": supplied["analyst_id"],
            "method_id": supplied["method_id"],
            "status": supplied["status"],
            "valid_until": supplied["valid_until"],
            "last_assessed_on": supplied["last_assessed_on"],
        }
        self.state = _set_record(self.state, "analyst_competencies", competency_id, record)
        self.state = _append_audit(self.state, "record_analyst_competency", "analyst_competency", competency_id, record)
        return {"ok": record["status"] == "current", "competency": record, "state": self.state, "side_effects": ()}

    def accession_sample(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        accession_number = supplied["accession_number"]
        if accession_number in self.state.get("accession_index", {}):
            return {"ok": False, "reason": "duplicate_accession_number", "accession_number": accession_number, "side_effects": ()}
        confidence = float(supplied["identity_confidence"])
        floor = float(self.state.get("parameters", {}).get("identity_confidence_floor", DEFAULT_PARAMETERS["identity_confidence_floor"]))
        if confidence < floor:
            return {"ok": False, "reason": "identity_confidence_below_floor", "accession_number": accession_number, "side_effects": ()}
        record = {
            "tenant": supplied["tenant"],
            "sample_id": supplied["sample_id"],
            "accession_number": accession_number,
            "sample_type": supplied["sample_type"],
            "collected_at": supplied["collected_at"],
            "received_at": supplied["received_at"],
            "collector": supplied["collector"],
            "received_by": supplied["received_by"],
            "container": supplied["container"],
            "preservative": supplied.get("preservative"),
            "identity_confidence": confidence,
            "storage_condition": supplied.get("storage_condition", "ambient"),
            "stability_expiry": supplied.get("stability_expiry", "2026-06-30"),
            "status": "accessioned",
            "custody_exception_open": False,
        }
        self.state = _set_record(self.state, "samples", record["sample_id"], record)
        accession_index = dict(self.state.get("accession_index", {}))
        accession_index[accession_number] = record["sample_id"]
        self.state = {**self.state, "accession_index": accession_index}
        self.state = _append_event(self.state, "LaboratoryInformationManagementCreated", {"sample_id": record["sample_id"], "accession_number": accession_number})
        self.state = _append_audit(self.state, "accession_sample", "sample", record["sample_id"], record)
        return {"ok": True, "sample": record, "state": self.state, "side_effects": ()}

    def record_chain_of_custody(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        sample = self.state.get("samples", {}).get(supplied["sample_id"])
        if sample is None:
            return {"ok": False, "reason": "unknown_sample", "sample_id": supplied["sample_id"], "side_effects": ()}
        self.state, custody_id = _sequence(self.state, "custody")
        record = {
            "custody_id": custody_id,
            "tenant": supplied["tenant"],
            "sample_id": supplied["sample_id"],
            "from_actor": supplied["from_actor"],
            "to_actor": supplied["to_actor"],
            "location": supplied["location"],
            "condition": supplied["condition"],
            "seal_status": supplied["seal_status"],
            "accepted": bool(supplied["accepted"]),
            "exception": supplied.get("exception"),
        }
        self.state = _set_record(self.state, "chain_of_custody", custody_id, record)
        updated_sample = dict(sample)
        updated_sample["custody_exception_open"] = not record["accepted"] or bool(record.get("exception"))
        if updated_sample["custody_exception_open"]:
            updated_sample["status"] = "custody_exception"
        self.state = _set_record(self.state, "samples", sample["sample_id"], updated_sample)
        self.state = _append_audit(self.state, "record_chain_of_custody", "chain_of_custody", custody_id, record)
        return {"ok": True, "custody_event": record, "sample": updated_sample, "state": self.state, "side_effects": ()}

    def place_test_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        if supplied["sample_id"] not in self.state.get("samples", {}):
            return {"ok": False, "reason": "unknown_sample", "sample_id": supplied["sample_id"], "side_effects": ()}
        record = {
            "tenant": supplied["tenant"],
            "order_id": supplied["order_id"],
            "sample_id": supplied["sample_id"],
            "ordered_by": supplied["ordered_by"],
            "priority": supplied["priority"],
            "specimen_type": supplied["specimen_type"],
            "tests": tuple(supplied["tests"]),
            "clinical_context": supplied.get("clinical_context"),
            "billing_context": supplied.get("billing_context"),
            "reflex_eligible": bool(supplied.get("reflex_eligible", False)),
            "status": "queued",
        }
        self.state = _set_record(self.state, "orders", record["order_id"], record)
        self.state = _append_event(self.state, "LaboratoryInformationManagementUpdated", {"order_id": record["order_id"], "sample_id": record["sample_id"]})
        self.state = _append_audit(self.state, "place_test_order", "test_order", record["order_id"], record)
        return {"ok": True, "order": record, "state": self.state, "side_effects": ()}

    def create_batch_run(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        method = self.state.get("methods", {}).get(supplied["method_id"])
        if method is None or method.get("validation_status") != "validated":
            return {"ok": False, "reason": "method_not_validated", "method_id": supplied["method_id"], "side_effects": ()}
        sample_ids = tuple(supplied["sample_ids"])
        unknown_samples = tuple(sample_id for sample_id in sample_ids if sample_id not in self.state.get("samples", {}))
        if unknown_samples:
            return {"ok": False, "reason": "unknown_samples", "sample_ids": unknown_samples, "side_effects": ()}
        instrument_ready, instrument_blockers = _instrument_ready(self.state, supplied["instrument_id"], supplied["method_id"])
        reagent_ready, reagent_blockers = _reagent_ready(self.state, tuple(supplied["reagent_lot_ids"]))
        competency_ready, competency_blocker = _competency_ready(self.state, supplied["analyst_id"], supplied["method_id"])
        blockers = tuple(item for item in instrument_blockers + reagent_blockers + (() if competency_ready else (str(competency_blocker),)) if item)
        record = {
            "tenant": supplied["tenant"],
            "batch_run_id": supplied["batch_run_id"],
            "order_id": supplied["order_id"],
            "sample_ids": sample_ids,
            "method_id": supplied["method_id"],
            "instrument_id": supplied["instrument_id"],
            "analyst_id": supplied["analyst_id"],
            "qc_lot_id": supplied["qc_lot_id"],
            "reagent_lot_ids": tuple(supplied["reagent_lot_ids"]),
            "status": "running" if instrument_ready and reagent_ready and competency_ready else "held",
            "blockers": blockers,
            "qc_passed": None,
            "results": (),
            "reviewed_by": None,
        }
        self.state = _set_record(self.state, "batch_runs", record["batch_run_id"], record)
        self.state = _append_audit(self.state, "create_batch_run", "batch_run", record["batch_run_id"], record)
        return {"ok": record["status"] == "running", "batch_run": record, "state": self.state, "side_effects": ()}

    def record_qc_measurement(self, batch_run_id: str, observed_value: float, reviewer: str) -> dict[str, Any]:
        batch = self.state.get("batch_runs", {}).get(batch_run_id)
        if batch is None:
            return {"ok": False, "reason": "unknown_batch_run", "batch_run_id": batch_run_id, "side_effects": ()}
        lot = self.state.get("qc_lots", {}).get(batch["qc_lot_id"])
        if lot is None:
            return {"ok": False, "reason": "unknown_qc_lot", "batch_run_id": batch_run_id, "side_effects": ()}
        passed = float(lot["expected_low"]) <= float(observed_value) <= float(lot["expected_high"])
        qc_result = {
            "batch_run_id": batch_run_id,
            "qc_lot_id": lot["qc_lot_id"],
            "observed_value": float(observed_value),
            "reviewer": reviewer,
            "passed": passed,
        }
        updated = dict(batch)
        updated["qc_passed"] = passed
        self.state = _set_record(self.state, "batch_runs", batch_run_id, updated)
        self.state = _append_audit(self.state, "record_qc_measurement", "quality_control", batch_run_id, qc_result)
        return {"ok": True, "qc_result": qc_result, "batch_run": updated, "state": self.state, "side_effects": ()}

    def import_result(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        batch = self.state.get("batch_runs", {}).get(supplied["batch_run_id"])
        if batch is None:
            return {"ok": False, "reason": "unknown_batch_run", "batch_run_id": supplied["batch_run_id"], "side_effects": ()}
        if supplied["sample_id"] not in batch["sample_ids"]:
            return {"ok": False, "reason": "sample_not_in_batch", "sample_id": supplied["sample_id"], "side_effects": ()}
        method = self.state.get("methods", {}).get(batch["method_id"])
        value = float(supplied["value"])
        oos = value < float(method["specification_low"]) or value > float(method["specification_high"])
        critical = value >= float(method.get("critical_high", method["specification_high"]))
        record = {
            "result_id": supplied["result_id"],
            "tenant": supplied["tenant"],
            "batch_run_id": supplied["batch_run_id"],
            "sample_id": supplied["sample_id"],
            "order_id": batch["order_id"],
            "analyte": supplied["analyte"],
            "value": value,
            "unit": supplied.get("unit", method.get("units")),
            "specification_low": float(method["specification_low"]),
            "specification_high": float(method["specification_high"]),
            "status": "oos_hold" if oos else "preliminary",
            "technical_review_status": "pending",
            "abnormal_flag": oos,
            "critical_flag": critical,
            "review_comments": (),
            "signatures": (),
        }
        self.state = _set_record(self.state, "results", record["result_id"], record)
        updated_batch = dict(batch)
        updated_batch["results"] = tuple(updated_batch.get("results", ())) + (record["result_id"],)
        self.state = _set_record(self.state, "batch_runs", batch["batch_run_id"], updated_batch)
        if critical:
            notification = {
                "result_id": record["result_id"],
                "status": "pending",
                "recipient": supplied.get("critical_recipient", "on_call_supervisor"),
                "read_back_evidence": None,
            }
            self.state = _set_record(self.state, "critical_notifications", record["result_id"], notification)
        self.state = _append_audit(self.state, "import_result", "result", record["result_id"], record)
        return {"ok": True, "result": record, "state": self.state, "side_effects": ()}

    def review_batch_run(self, batch_run_id: str, reviewer: str) -> dict[str, Any]:
        batch = self.state.get("batch_runs", {}).get(batch_run_id)
        if batch is None:
            return {"ok": False, "reason": "unknown_batch_run", "batch_run_id": batch_run_id, "side_effects": ()}
        blockers = []
        if batch.get("qc_passed") is not True:
            blockers.append("qc_not_passed")
        if not batch.get("results"):
            blockers.append("missing_results")
        updated = dict(batch)
        updated["status"] = "reviewed" if not blockers else "held"
        updated["reviewed_by"] = reviewer
        updated["review_blockers"] = tuple(blockers)
        self.state = _set_record(self.state, "batch_runs", batch_run_id, updated)
        self.state = _append_audit(self.state, "review_batch_run", "batch_run", batch_run_id, updated)
        return {"ok": not blockers, "batch_run": updated, "state": self.state, "side_effects": ()}

    def review_result(self, result_id: str, reviewer: str, comment: str = "") -> dict[str, Any]:
        result = self.state.get("results", {}).get(result_id)
        if result is None:
            return {"ok": False, "reason": "unknown_result", "result_id": result_id, "side_effects": ()}
        updated = dict(result)
        updated["technical_review_status"] = "approved"
        updated["review_comments"] = tuple(updated.get("review_comments", ())) + ({"reviewer": reviewer, "comment": comment or "Technical review complete"},)
        self.state = _set_record(self.state, "results", result_id, updated)
        self.state = _append_audit(self.state, "review_result", "result", result_id, updated)
        return {"ok": True, "result": updated, "state": self.state, "side_effects": ()}

    def open_oos_investigation(self, result_id: str, reason: str, owner: str, capa: str | None = None) -> dict[str, Any]:
        result = self.state.get("results", {}).get(result_id)
        if result is None:
            return {"ok": False, "reason": "unknown_result", "result_id": result_id, "side_effects": ()}
        self.state, oos_id = _sequence(self.state, "oos")
        investigation = {
            "oos_id": oos_id,
            "result_id": result_id,
            "reason": reason,
            "owner": owner,
            "status": "open",
            "capa": capa or "Document root cause and verify corrective action effectiveness.",
        }
        self.state = _set_record(self.state, "oos_events", oos_id, investigation)
        updated = dict(result)
        updated["status"] = "oos_investigation"
        self.state = _set_record(self.state, "results", result_id, updated)
        self.state = _append_event(self.state, "LaboratoryInformationManagementExceptionOpened", {"result_id": result_id, "oos_id": oos_id})
        self.state = _append_audit(self.state, "open_oos_investigation", "oos", oos_id, investigation)
        return {"ok": True, "investigation": investigation, "result": updated, "state": self.state, "side_effects": ()}

    def resolve_oos_investigation(self, result_id: str, disposition: str, approver: str, conclusion: str) -> dict[str, Any]:
        open_investigation = next(
            (item for item in self.state.get("oos_events", {}).values() if item["result_id"] == result_id and item["status"] == "open"),
            None,
        )
        if open_investigation is None:
            return {"ok": False, "reason": "no_open_oos", "result_id": result_id, "side_effects": ()}
        closed = {
            **open_investigation,
            "status": "closed",
            "disposition": disposition,
            "approver": approver,
            "conclusion": conclusion,
        }
        self.state = _set_record(self.state, "oos_events", open_investigation["oos_id"], closed)
        result = dict(self.state["results"][result_id])
        result["status"] = "reviewed_with_exception" if disposition == "report_with_comment" else "invalidated"
        self.state = _set_record(self.state, "results", result_id, result)
        capa_id = f"capa-{closed['oos_id']}"
        self.state = _set_record(
            self.state,
            "capa",
            capa_id,
            {"capa_id": capa_id, "source_oos_id": closed["oos_id"], "owner": approver, "effectiveness_check": "pending"},
        )
        self.state = _append_audit(self.state, "resolve_oos_investigation", "oos", closed["oos_id"], closed)
        return {"ok": True, "investigation": closed, "result": result, "state": self.state, "side_effects": ()}

    def release_result(
        self,
        result_id: str,
        technical_reviewer: str,
        approver: str,
        signature_purpose: str,
        signature_meaning: str,
        release_comment: str = "",
    ) -> dict[str, Any]:
        if result_id not in self.state.get("results", {}):
            return {"ok": False, "reason": "unknown_result", "result_id": result_id, "side_effects": ()}
        self.review_result(result_id, technical_reviewer, release_comment or "Reviewed for release")
        result = dict(self.state["results"][result_id])
        blockers = _result_release_blockers(self.state, result)
        if blockers:
            return {"ok": False, "reason": "release_blocked", "blockers": blockers, "result": result, "side_effects": ()}
        signature = {
            "signed_by": approver,
            "role": "approver",
            "purpose": signature_purpose,
            "meaning": signature_meaning,
            "record_hash": _hash(result),
            "revoked": False,
        }
        result["status"] = "final"
        result["released_by"] = approver
        result["signatures"] = tuple(result.get("signatures", ())) + (signature,)
        if result.get("critical_flag"):
            notification = dict(self.state.get("critical_notifications", {}).get(result_id, {}))
            notification["status"] = "acknowledged"
            notification["read_back_evidence"] = "Read back to ordering provider"
            self.state = _set_record(self.state, "critical_notifications", result_id, notification)
        self.state = _set_record(self.state, "results", result_id, result)
        self.state = _append_event(self.state, "LaboratoryInformationManagementApproved", {"result_id": result_id, "status": "final"})
        self.state = _append_audit(self.state, "release_result", "result", result_id, result)
        return {"ok": True, "result": result, "state": self.state, "side_effects": ()}

    def correct_result(self, result_id: str, corrected_value: float, reason: str, approver: str) -> dict[str, Any]:
        result = self.state.get("results", {}).get(result_id)
        if result is None:
            return {"ok": False, "reason": "unknown_result", "result_id": result_id, "side_effects": ()}
        correction_id = f"corr-{len(self.state.get('corrections', {})) + 1:05d}"
        correction = {
            "correction_id": correction_id,
            "result_id": result_id,
            "original_value": result["value"],
            "corrected_value": float(corrected_value),
            "reason": reason,
            "approver": approver,
        }
        self.state = _set_record(self.state, "corrections", correction_id, correction)
        updated = dict(result)
        updated["status"] = "corrected"
        updated["value"] = float(corrected_value)
        self.state = _set_record(self.state, "results", result_id, updated)
        self.state = _append_event(self.state, "LaboratoryInformationManagementUpdated", {"result_id": result_id, "correction_id": correction_id})
        self.state = _append_audit(self.state, "correct_result", "result", result_id, correction)
        return {"ok": True, "correction": correction, "result": updated, "state": self.state, "side_effects": ()}

    def create_stability_study(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        if supplied["sample_id"] not in self.state.get("samples", {}):
            return {"ok": False, "reason": "unknown_sample", "sample_id": supplied["sample_id"], "side_effects": ()}
        record = {
            "study_id": supplied["study_id"],
            "sample_id": supplied["sample_id"],
            "protocol_id": supplied["protocol_id"],
            "storage_condition": supplied["storage_condition"],
            "timepoints": tuple(supplied["timepoints"]),
            "status": "active",
        }
        self.state = _set_record(self.state, "stability_studies", record["study_id"], record)
        self.state = _append_audit(self.state, "create_stability_study", "stability_study", record["study_id"], record)
        return {"ok": True, "study": record, "state": self.state, "side_effects": ()}

    def schedule_stability_pull(self, study_id: str, timepoint: str, due_on: str) -> dict[str, Any]:
        study = self.state.get("stability_studies", {}).get(study_id)
        if study is None:
            return {"ok": False, "reason": "unknown_study", "study_id": study_id, "side_effects": ()}
        self.state, pull_id = _sequence(self.state, "pull")
        record = {
            "pull_id": pull_id,
            "study_id": study_id,
            "sample_id": study["sample_id"],
            "timepoint": timepoint,
            "due_on": due_on,
            "status": "scheduled",
        }
        self.state = _set_record(self.state, "stability_pulls", pull_id, record)
        self.state = _append_audit(self.state, "schedule_stability_pull", "stability_pull", pull_id, record)
        return {"ok": True, "pull": record, "state": self.state, "side_effects": ()}

    def complete_stability_pull(self, pull_id: str, observed_on: str, result_summary: str) -> dict[str, Any]:
        pull = self.state.get("stability_pulls", {}).get(pull_id)
        if pull is None:
            return {"ok": False, "reason": "unknown_pull", "pull_id": pull_id, "side_effects": ()}
        updated = dict(pull)
        updated["status"] = "completed"
        updated["observed_on"] = observed_on
        updated["result_summary"] = result_summary
        self.state = _set_record(self.state, "stability_pulls", pull_id, updated)
        self.state = _append_audit(self.state, "complete_stability_pull", "stability_pull", pull_id, updated)
        return {"ok": True, "pull": updated, "state": self.state, "side_effects": ()}

    def generate_certificate_of_analysis(self, order_id: str, certificate_id: str, issued_by: str, customer_reference: str | None = None) -> dict[str, Any]:
        order = self.state.get("orders", {}).get(order_id)
        if order is None:
            return {"ok": False, "reason": "unknown_order", "order_id": order_id, "side_effects": ()}
        results = tuple(
            result
            for result in self.state.get("results", {}).values()
            if result["order_id"] == order_id and result["status"] in {"final", "corrected"}
        )
        if not results:
            return {"ok": False, "reason": "no_reportable_results", "order_id": order_id, "side_effects": ()}
        batch = next((item for item in self.state.get("batch_runs", {}).values() if item["order_id"] == order_id), None)
        certificate = {
            "certificate_id": certificate_id,
            "order_id": order_id,
            "sample_id": order["sample_id"],
            "issued_by": issued_by,
            "customer_reference": customer_reference,
            "result_ids": tuple(result["result_id"] for result in results),
            "method_id": batch["method_id"] if batch else None,
            "instrument_id": batch["instrument_id"] if batch else None,
            "qc_lot_id": batch["qc_lot_id"] if batch else None,
            "reagent_lot_ids": batch["reagent_lot_ids"] if batch else (),
            "signatures": tuple(result["signatures"][-1] for result in results if result.get("signatures")),
        }
        self.state = _set_record(self.state, "certificates", certificate_id, certificate)
        self.state = _append_audit(self.state, "generate_certificate_of_analysis", "certificate", certificate_id, certificate)
        return {"ok": True, "certificate": certificate, "state": self.state, "side_effects": ()}

    def document_instruction_preview(
        self,
        document_text: str,
        instructions: str,
        target_entity: str | None = None,
        requested_action: str = "read",
    ) -> dict[str, Any]:
        lowered = f"{document_text}\n{instructions}".lower()
        inferred = target_entity
        if inferred is None:
            if "stability" in lowered:
                inferred = "stability_study"
            elif "coa" in lowered or "certificate" in lowered:
                inferred = "certificate_of_analysis"
            elif "reagent" in lowered:
                inferred = "reagent_inventory"
            elif "competency" in lowered or "analyst" in lowered:
                inferred = "analyst_competency"
            elif "oos" in lowered or "out of spec" in lowered:
                inferred = "oos"
            elif "batch" in lowered or "run" in lowered:
                inferred = "batch_run"
            elif "result" in lowered:
                inferred = "result"
            elif "order" in lowered:
                inferred = "test_order"
            else:
                inferred = "sample"
        table = OWNED_TABLES.get(inferred if inferred != "oos" else "result", OWNED_TABLES["sample"])
        form_catalog = laboratory_information_management_form_catalog()
        wizard_catalog = laboratory_information_management_wizard_catalog()
        form_id = ENTITY_TO_FORM.get(inferred, "assistant_document_preview")
        form = next((item for item in form_catalog["forms"] if item["form_id"] == form_id), form_catalog["forms"][-1])
        keywords = tuple(word for word in (inferred, requested_action, "sample", "order", "result", "qc", "batch", "stability") if word)
        citations = _extract_citations(document_text, keywords)
        wizard_candidates = tuple(
            wizard["wizard_id"]
            for wizard in wizard_catalog["wizards"]
            if any(keyword in lowered for keyword in (wizard["wizard_id"].replace("_", " "), wizard["title"].lower(), inferred.replace("_", " ")))
        )
        preview = {
            "preview_id": f"preview-{len(self.state.get('document_previews', {})) + 1:05d}",
            "target_entity": inferred,
            "action": requested_action,
            "table": table,
            "route": form["route"],
            "form_id": form["form_id"],
            "requires_confirmation": requested_action != "read",
            "citations": citations,
            "wizard_candidates": wizard_candidates or ("assistant_guided_change",),
            "boundary_ok": table.startswith(f"{PBC_KEY}_"),
            "preview_only": True,
        }
        self.state = _set_record(self.state, "document_previews", preview["preview_id"], preview)
        self.state = _append_audit(self.state, "document_instruction_preview", "document_preview", preview["preview_id"], preview)
        return {"ok": preview["boundary_ok"] and bool(preview["citations"]), "preview": preview, "state": self.state, "side_effects": ()}

    def verify_audit_trail(self) -> dict[str, Any]:
        previous_hash = "GENESIS"
        failures = []
        for entry in self.state.get("audit_trail", ()):
            recomputed = _hash((entry["timestamp"], entry["action"], entry["record_type"], entry["record_id"], entry["payload"], previous_hash))
            if entry["previous_hash"] != previous_hash or entry["entry_hash"] != recomputed:
                failures.append(entry["audit_id"])
            previous_hash = entry["entry_hash"]
        return {"ok": not failures, "entry_count": len(self.state.get("audit_trail", ())), "failures": tuple(failures), "side_effects": ()}

    def workbench(self, tenant: str | None = None) -> dict[str, Any]:
        active_tenant = tenant or self.tenant
        samples = tuple(sample for sample in self.state.get("samples", {}).values() if sample["tenant"] == active_tenant)
        orders = tuple(order for order in self.state.get("orders", {}).values() if order["tenant"] == active_tenant)
        batches = tuple(batch for batch in self.state.get("batch_runs", {}).values() if batch["tenant"] == active_tenant)
        results = tuple(result for result in self.state.get("results", {}).values() if result["tenant"] == active_tenant)
        due_pulls = tuple(pull for pull in self.state.get("stability_pulls", {}).values() if pull["status"] == "scheduled")
        low_stock = tuple(lot for lot in self.state.get("reagent_lots", {}).values() if int(lot["quantity_on_hand"]) <= int(lot["reorder_point"]))
        competency_watch = tuple(
            item
            for item in self.state.get("analyst_competencies", {}).values()
            if item["status"] != "current" or item["valid_until"] <= "2026-06-30"
        )
        queue_counts = {
            "accessioning": len(tuple(sample for sample in samples if sample["status"] == "accessioned")),
            "custody_exceptions": len(tuple(sample for sample in samples if sample.get("custody_exception_open"))),
            "pending_runs": len(tuple(batch for batch in batches if batch["status"] in {"running", "held"})),
            "qc_failures": len(tuple(batch for batch in batches if batch.get("qc_passed") is False)),
            "results_review": len(tuple(result for result in results if result["status"] in {"preliminary", "reviewed_with_exception", "oos_hold", "oos_investigation"})),
            "oos_open": len(tuple(event for event in self.state.get("oos_events", {}).values() if event["status"] == "open")),
            "stability_due": len(due_pulls),
            "coa_ready": len(tuple(order for order in orders if any(result["order_id"] == order["order_id"] and result["status"] in {"final", "corrected"} for result in results))),
            "inventory_watch": len(low_stock),
            "competency_watch": len(competency_watch),
        }
        assistant_guardrails = {
            "preview_only": True,
            "requires_confirmation_for_mutation": bool(self.state.get("configuration", {}).get("assistant_mutations_require_confirmation", True)),
            "citations_required": True,
        }
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "tenant": active_tenant,
            "queue_counts": queue_counts,
            "samples": samples,
            "orders": orders,
            "batch_runs": batches,
            "results": results,
            "stability_pulls": due_pulls,
            "reagent_watch": low_stock,
            "competency_watch": competency_watch,
            "forms": laboratory_information_management_form_catalog()["forms"],
            "wizards": laboratory_information_management_wizard_catalog()["wizards"],
            "controls": laboratory_information_management_control_catalog()["controls"],
            "audit": self.verify_audit_trail(),
            "assistant_guardrails": assistant_guardrails,
            "side_effects": (),
        }


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_class": "LaboratoryInformationManagementStandaloneApp",
        "implementation_directory": "src/pyAppGen/pbcs/laboratory_information_management",
        "service_methods": (
            "configure",
            "register_defaults",
            "register_method",
            "manage_instrument",
            "record_calibration",
            "register_qc_lot",
            "adjust_reagent_inventory",
            "record_analyst_competency",
            "accession_sample",
            "record_chain_of_custody",
            "place_test_order",
            "create_batch_run",
            "record_qc_measurement",
            "import_result",
            "review_batch_run",
            "review_result",
            "open_oos_investigation",
            "resolve_oos_investigation",
            "release_result",
            "correct_result",
            "create_stability_study",
            "schedule_stability_pull",
            "complete_stability_pull",
            "generate_certificate_of_analysis",
            "document_instruction_preview",
            "workbench",
            "verify_audit_trail",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench"),
        "docs": ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"),
        "event_contract": "AppGen-X",
        "event_topic": EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": ALLOWED_DATABASE_BACKENDS,
    }


def bootstrap_standalone_app(tenant: str = "default") -> dict[str, Any]:
    app = LaboratoryInformationManagementStandaloneApp(tenant=tenant)
    app.configure()
    app.register_defaults()
    return {"ok": True, "pbc": PBC_KEY, "app": app, "contract": standalone_manifest(), "side_effects": ()}


def documentation_presence() -> dict[str, Any]:
    base = Path(__file__).parent
    artifacts = tuple({"name": name, "exists": (base / name).exists()} for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"))
    missing = tuple(item["name"] for item in artifacts if not item["exists"])
    return {"ok": not missing, "artifacts": artifacts, "missing": missing, "side_effects": ()}


def standalone_smoke_test() -> dict[str, Any]:
    bundle = bootstrap_standalone_app(tenant="tenant_smoke")
    app = bundle["app"]
    accession = app.accession_sample(
        {
            "tenant": "tenant_smoke",
            "sample_id": "SMP-001",
            "accession_number": "ACC-001",
            "sample_type": "retain",
            "collected_at": "2026-05-29T08:00:00Z",
            "received_at": "2026-05-29T09:00:00Z",
            "collector": "nurse_kimani",
            "received_by": "accessioner_jules",
            "container": "amber_vial",
            "identity_confidence": 0.99,
            "storage_condition": "25C",
            "stability_expiry": "2026-08-31",
        }
    )
    custody = app.record_chain_of_custody(
        {
            "tenant": "tenant_smoke",
            "sample_id": "SMP-001",
            "from_actor": "accessioner_jules",
            "to_actor": "analyst_ada",
            "location": "Chemistry Bench 4",
            "condition": "acceptable",
            "seal_status": "intact",
            "accepted": True,
        }
    )
    order = app.place_test_order(
        {
            "tenant": "tenant_smoke",
            "order_id": "ORD-001",
            "sample_id": "SMP-001",
            "ordered_by": "qa_release",
            "priority": "routine",
            "specimen_type": "retain",
            "tests": ("assay",),
            "clinical_context": "release testing",
        }
    )
    batch = app.create_batch_run(
        {
            "tenant": "tenant_smoke",
            "batch_run_id": "RUN-001",
            "order_id": "ORD-001",
            "sample_ids": ("SMP-001",),
            "method_id": DEFAULT_METHOD["method_id"],
            "instrument_id": DEFAULT_INSTRUMENT["instrument_id"],
            "analyst_id": DEFAULT_COMPETENCY["analyst_id"],
            "qc_lot_id": DEFAULT_QC_LOT["qc_lot_id"],
            "reagent_lot_ids": (DEFAULT_REAGENT_LOT["reagent_lot_id"],),
        }
    )
    qc = app.record_qc_measurement("RUN-001", 100.2, "qa_supervisor")
    result = app.import_result(
        {
            "tenant": "tenant_smoke",
            "result_id": "RES-001",
            "batch_run_id": "RUN-001",
            "sample_id": "SMP-001",
            "analyte": "assay",
            "value": 100.5,
            "unit": "% label claim",
        }
    )
    review = app.review_batch_run("RUN-001", "supervisor_maina")
    released = app.release_result(
        "RES-001",
        technical_reviewer="supervisor_maina",
        approver="qp_wanjiru",
        signature_purpose="batch_release",
        signature_meaning="I approve this result for report release.",
    )
    study = app.create_stability_study(
        {
            "study_id": "STAB-001",
            "sample_id": "SMP-001",
            "protocol_id": "PROT-STAB-001",
            "storage_condition": "25C/60RH",
            "timepoints": ("T0", "M1"),
        }
    )
    pull = app.schedule_stability_pull("STAB-001", "M1", "2026-06-30")
    pull_done = app.complete_stability_pull(pull["pull"]["pull_id"], "2026-06-30", "Assay remains within specification.")
    coa = app.generate_certificate_of_analysis("ORD-001", "COA-001", "qp_wanjiru", "BATCH-77")
    preview = app.document_instruction_preview(
        "Sample ACC-001 needs a certificate and reagent reconciliation.\nAnalyst competency renewal due next month.",
        "prepare a create preview for the certificate package",
        requested_action="create",
    )
    workbench = app.workbench("tenant_smoke")
    audit = app.verify_audit_trail()
    return {
        "ok": all(
            item["ok"]
            for item in (
                bundle,
                accession,
                custody,
                order,
                batch,
                qc,
                result,
                review,
                released,
                study,
                pull,
                pull_done,
                coa,
                preview,
                workbench,
                audit,
                documentation_presence(),
            )
        ),
        "manifest": standalone_manifest(),
        "bundle": bundle,
        "accession": accession,
        "batch": batch,
        "released": released,
        "coa": coa,
        "preview": preview,
        "workbench": workbench,
        "audit": audit,
        "side_effects": (),
    }
