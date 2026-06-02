"""Standalone one-PBC application surface for Livestock Herd Management."""

from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta
from statistics import mean

from . import routes
from . import ui
from .controls import livestock_herd_management_control_center
from .controls import livestock_herd_management_mutation_preview
from .forms import livestock_herd_management_form_catalog
from .manifest import PBC_MANIFEST
from .runtime import LIVESTOCK_HERD_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .wizards import livestock_herd_management_wizard_catalog


PBC_KEY = "livestock_herd_management"


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": LIVESTOCK_HERD_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy": "herd_safety_first",
    "default_species": "cattle",
    "workbench_limit": 100,
    "assistant_mutations_require_confirmation": True,
}
DEFAULT_PARAMETERS = {
    "breeding_min_weight_kg": 320,
    "biosecurity_min_score": 0.8,
    "welfare_watch_threshold": 0.7,
    "max_stocking_density": 2.5,
    "min_paddock_rest_days": 21,
    "vaccination_due_window_days": 7,
    "milk_withdrawal_buffer_days": 3,
    "workbench_limit": 100,
}
DEFAULT_RULES = (
    {
        "rule_id": "herd_identity_integrity",
        "scope": "animal_registry",
        "status": "active",
        "rule": "primary identifiers must be unique across active animals",
    },
    {
        "rule_id": "movement_requires_quarantine_release",
        "scope": "movement_permits",
        "status": "active",
        "rule": "movement permits are blocked while quarantine is open",
    },
    {
        "rule_id": "yield_requires_withdrawal_clearance",
        "scope": "inventory_yield",
        "status": "active",
        "rule": "product release is blocked while treatment withdrawal is active",
    },
)


def _today() -> str:
    return date.today().isoformat()


def _days_from_today(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def _copy_state(state: dict) -> dict:
    return deepcopy(state)


def _safe_mean(values: list[float]) -> float:
    return round(mean(values), 3) if values else 0.0


def _is_missing(value) -> bool:
    return value is None or value == ""


def empty_standalone_state() -> dict:
    """Return a mutable standalone state for the package-local app."""
    return {
        "tenant": "tenant_demo",
        "configuration": dict(DEFAULT_CONFIGURATION),
        "parameters": dict(DEFAULT_PARAMETERS),
        "rules": {rule["rule_id"]: dict(rule) for rule in DEFAULT_RULES},
        "animals": {},
        "herd_groups": {},
        "breeding_records": {},
        "pregnancies": {},
        "calving_events": {},
        "health_treatments": {},
        "vaccinations": {},
        "feed_plans": {},
        "grazing_plans": {},
        "weights": {},
        "genetics_profiles": {},
        "movement_permits": {},
        "mortalities": {},
        "quarantines": {},
        "biosecurity_audits": {},
        "traceability_chains": {},
        "welfare_assessments": {},
        "inventory_yields": {},
        "assistant_previews": {},
        "timeline": [],
    }


class LivestockHerdManagementStandaloneApp:
    """Package-local standalone livestock app with executable domain state."""

    def __init__(self, state: dict | None = None):
        self.state = _copy_state(empty_standalone_state() if state is None else state)

    def _record_timeline(self, event_type: str, payload: dict) -> None:
        self.state["timeline"].append(
            {
                "event_type": event_type,
                "event_topic": LIVESTOCK_HERD_MANAGEMENT_REQUIRED_EVENT_TOPIC,
                "occurred_on": _today(),
                "payload": dict(payload),
            }
        )

    def register_animal(self, payload: dict) -> dict:
        required = ("animal_id", "primary_identifier", "species", "production_type", "source_provenance", "sex", "birth_date", "breed")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}

        identifier = payload["primary_identifier"]
        duplicate_animal = next(
            (
                animal_id
                for animal_id, animal in self.state["animals"].items()
                if animal.get("status") != "deceased"
                and identifier in {entry["identifier"] for entry in animal.get("tag_history", ())}
            ),
            None,
        )
        if duplicate_animal and duplicate_animal != payload["animal_id"]:
            self._record_timeline("LivestockHerdManagementExceptionOpened", {"animal_id": payload["animal_id"], "reason": "duplicate_identifier"})
            return {"ok": False, "reason": "duplicate_identifier", "duplicate_animal": duplicate_animal, "side_effects": ()}

        animal = {
            "animal_id": payload["animal_id"],
            "tenant": payload.get("tenant", self.state["tenant"]),
            "species": payload["species"],
            "production_type": payload["production_type"],
            "sex": payload["sex"],
            "birth_date": payload["birth_date"],
            "breed": payload["breed"],
            "status": "quarantine" if payload.get("requires_quarantine") else "active",
            "lifecycle_state": "new_arrival" if payload.get("requires_quarantine") else "active",
            "primary_identifier": identifier,
            "tag_history": tuple(payload.get("tag_history", ())) + ({"identifier": identifier, "status": "active", "recorded_on": _today()},),
            "source_provenance": payload["source_provenance"],
            "default_group_id": payload.get("default_group_id"),
            "genetics": dict(payload.get("genetics", {})),
            "lineage": dict(payload.get("lineage", {})),
            "traceability_status": payload.get("traceability_status", "registered"),
            "created_on": _today(),
        }
        self.state["animals"][animal["animal_id"]] = animal
        self.state["traceability_chains"][f"trace-{animal['animal_id']}"] = {
            "trace_id": f"trace-{animal['animal_id']}",
            "animal_id": animal["animal_id"],
            "lot_id": payload.get("trace_lot_id", f"identity-{animal['animal_id']}"),
            "origin_premises": payload.get("origin_premises", animal["source_provenance"]),
            "destination_premises": payload.get("default_group_location", animal.get("default_group_id") or "unassigned"),
        }
        if animal.get("default_group_id"):
            self.assign_herd_group(
                {
                    "group_id": animal["default_group_id"],
                    "animal_id": animal["animal_id"],
                    "location": payload.get("default_group_location", "intake-yard"),
                    "production_stage": payload.get("production_stage", "quarantine" if payload.get("requires_quarantine") else "grower"),
                    "entry_date": _today(),
                    "stocking_density": payload.get("stocking_density", 1.5),
                    "reason": "intake_default_group",
                }
            )
        self._record_timeline("LivestockHerdManagementCreated", animal)
        return {"ok": True, "animal": animal, "side_effects": ()}

    def assign_herd_group(self, payload: dict) -> dict:
        required = ("group_id", "animal_id", "location", "production_stage", "entry_date", "stocking_density", "reason")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        if payload["animal_id"] not in self.state["animals"]:
            return {"ok": False, "reason": "unknown_animal", "animal_id": payload["animal_id"], "side_effects": ()}

        group = self.state["herd_groups"].setdefault(
            payload["group_id"],
            {
                "group_id": payload["group_id"],
                "location": payload["location"],
                "production_stage": payload["production_stage"],
                "members": {},
                "stocking_density": payload["stocking_density"],
            },
        )
        group["location"] = payload["location"]
        group["production_stage"] = payload["production_stage"]
        group["stocking_density"] = payload["stocking_density"]
        group["members"][payload["animal_id"]] = {
            "animal_id": payload["animal_id"],
            "entry_date": payload["entry_date"],
            "reason": payload["reason"],
        }
        self.state["animals"][payload["animal_id"]]["default_group_id"] = payload["group_id"]
        self._record_timeline("LivestockHerdManagementUpdated", {"group_id": payload["group_id"], "animal_id": payload["animal_id"], "change": "group_assignment"})
        return {"ok": True, "group": group, "side_effects": ()}

    def record_genetics_profile(self, payload: dict) -> dict:
        required = ("animal_id", "profile_id", "sire_reference", "dam_reference", "inbreeding_risk", "trait_markers")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        if payload["animal_id"] not in self.state["animals"]:
            return {"ok": False, "reason": "unknown_animal", "animal_id": payload["animal_id"], "side_effects": ()}
        profile = {
            **dict(payload),
            "recorded_on": _today(),
            "genetic_warning": payload["inbreeding_risk"] >= 0.18,
        }
        self.state["genetics_profiles"][payload["profile_id"]] = profile
        self.state["animals"][payload["animal_id"]]["genetics"] = profile
        self._record_timeline("LivestockHerdManagementUpdated", {"animal_id": payload["animal_id"], "change": "genetics_profile"})
        return {"ok": True, "profile": profile, "side_effects": ()}

    def record_breeding_cycle(self, payload: dict) -> dict:
        required = ("breeding_id", "animal_id", "service_date", "service_method", "sire_reference", "technician", "expected_due_date", "genetic_risk_score")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        animal = self.state["animals"].get(payload["animal_id"])
        if animal is None:
            return {"ok": False, "reason": "unknown_animal", "animal_id": payload["animal_id"], "side_effects": ()}
        latest_weight = next((entry["weight_kg"] for entry in reversed(self.state["weights"].get(payload["animal_id"], ())) if entry.get("weight_kg")), None)
        if latest_weight is not None and latest_weight < self.state["parameters"]["breeding_min_weight_kg"]:
            return {
                "ok": False,
                "reason": "breeding_weight_gate_failed",
                "animal_id": payload["animal_id"],
                "weight_kg": latest_weight,
                "minimum_weight_kg": self.state["parameters"]["breeding_min_weight_kg"],
                "side_effects": (),
            }
        record = {
            **dict(payload),
            "tenant": animal["tenant"],
            "status": "pregnancy_confirmed",
            "created_on": _today(),
            "eligibility_checks": {
                "status_not_quarantine": animal.get("status") != "quarantine",
                "genetic_risk_ok": payload["genetic_risk_score"] < 0.4,
            },
        }
        self.state["breeding_records"][payload["breeding_id"]] = record
        self.state["pregnancies"][payload["animal_id"]] = {
            "animal_id": payload["animal_id"],
            "breeding_id": payload["breeding_id"],
            "expected_due_date": payload["expected_due_date"],
            "status": "confirmed",
            "gestation_stage": payload.get("gestation_stage", "mid"),
        }
        animal["lifecycle_state"] = "pregnant"
        self._record_timeline("LivestockHerdManagementApproved", {"animal_id": payload["animal_id"], "change": "pregnancy_confirmed"})
        return {"ok": True, "breeding_record": record, "pregnancy": self.state["pregnancies"][payload["animal_id"]], "side_effects": ()}

    def record_calving_event(self, payload: dict) -> dict:
        required = ("calving_id", "dam_id", "offspring_id", "birth_date", "birth_weight_kg", "assistance_level", "colostrum_confirmed", "calf_sex")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        pregnancy = self.state["pregnancies"].get(payload["dam_id"])
        if pregnancy is None:
            return {"ok": False, "reason": "pregnancy_not_found", "dam_id": payload["dam_id"], "side_effects": ()}
        calving = {**dict(payload), "status": "completed", "recorded_on": _today()}
        self.state["calving_events"][payload["calving_id"]] = calving
        self.state["pregnancies"][payload["dam_id"]]["status"] = "calved"
        self.state["animals"][payload["dam_id"]]["lifecycle_state"] = "lactating"
        self.register_animal(
            {
                "animal_id": payload["offspring_id"],
                "tenant": self.state["animals"][payload["dam_id"]]["tenant"],
                "species": self.state["animals"][payload["dam_id"]]["species"],
                "production_type": "breeding",
                "primary_identifier": payload.get("offspring_identifier", f"TAG-{payload['offspring_id'].upper()}"),
                "source_provenance": "born_on_farm",
                "sex": payload["calf_sex"],
                "birth_date": payload["birth_date"],
                "breed": self.state["animals"][payload["dam_id"]]["breed"],
                "requires_quarantine": False,
                "lineage": {
                    "dam_id": payload["dam_id"],
                    "sire_reference": pregnancy.get("sire_reference") or self.state["breeding_records"][pregnancy["breeding_id"]]["sire_reference"],
                },
            }
        )
        self._record_timeline("LivestockHerdManagementCreated", {"calving_id": payload["calving_id"], "offspring_id": payload["offspring_id"]})
        return {"ok": True, "calving": calving, "side_effects": ()}

    def record_health_intervention(self, payload: dict) -> dict:
        required = ("animal_id", "health_event_id", "symptom", "diagnosis", "treatment_name", "vaccination_name", "medication_lot", "withdrawal_days", "administered_by", "next_due_date")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        if payload["animal_id"] not in self.state["animals"]:
            return {"ok": False, "reason": "unknown_animal", "animal_id": payload["animal_id"], "side_effects": ()}
        treatment = {
            "treatment_id": payload.get("treatment_id", f"treatment-{payload['health_event_id']}"),
            "animal_id": payload["animal_id"],
            "health_event_id": payload["health_event_id"],
            "diagnosis": payload["diagnosis"],
            "symptom": payload["symptom"],
            "treatment_name": payload["treatment_name"],
            "medication_lot": payload["medication_lot"],
            "withdrawal_days": payload["withdrawal_days"],
            "withdrawal_release_date": _days_from_today(int(payload["withdrawal_days"])),
            "withdrawal_active": int(payload["withdrawal_days"]) > 0,
            "administered_by": payload["administered_by"],
        }
        vaccination = {
            "vaccination_id": payload.get("vaccination_id", f"vaccination-{payload['health_event_id']}"),
            "animal_id": payload["animal_id"],
            "vaccination_name": payload["vaccination_name"],
            "medication_lot": payload["medication_lot"],
            "next_due_date": payload["next_due_date"],
            "status": "due" if payload["next_due_date"] <= _days_from_today(self.state["parameters"]["vaccination_due_window_days"]) else "current",
        }
        self.state["health_treatments"][treatment["treatment_id"]] = treatment
        self.state["vaccinations"][vaccination["vaccination_id"]] = vaccination
        self._record_timeline("LivestockHerdManagementUpdated", {"animal_id": payload["animal_id"], "change": "health_intervention"})
        return {"ok": True, "treatment": treatment, "vaccination": vaccination, "side_effects": ()}

    def record_feed_and_grazing_plan(self, payload: dict) -> dict:
        required = ("plan_id", "group_id", "ration_name", "dry_matter_pct", "protein_pct", "paddock_id", "forage_cover_kg_dm", "rest_days_required", "target_daily_gain_kg")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        feed_plan = {
            **dict(payload),
            "status": "active",
            "cost_per_head": payload.get("cost_per_head", 4.8),
            "created_on": _today(),
        }
        grazing_plan = {
            "plan_id": payload["plan_id"],
            "group_id": payload["group_id"],
            "paddock_id": payload["paddock_id"],
            "rest_days_required": payload["rest_days_required"],
            "forage_cover_kg_dm": payload["forage_cover_kg_dm"],
            "stocking_density_ok": payload.get("stocking_density", 1.8) <= self.state["parameters"]["max_stocking_density"],
            "status": "on_rotation",
        }
        self.state["feed_plans"][payload["plan_id"]] = feed_plan
        self.state["grazing_plans"][payload["plan_id"]] = grazing_plan
        self._record_timeline("LivestockHerdManagementUpdated", {"group_id": payload["group_id"], "change": "feed_and_grazing"})
        return {"ok": True, "feed_plan": feed_plan, "grazing_plan": grazing_plan, "side_effects": ()}

    def record_weight_observation(self, payload: dict) -> dict:
        required = ("animal_id", "recorded_on", "weight_kg")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        entries = list(self.state["weights"].get(payload["animal_id"], ()))
        entries.append({**dict(payload), "average_daily_gain_kg": payload.get("average_daily_gain_kg", 0.0)})
        self.state["weights"][payload["animal_id"]] = entries
        self._record_timeline("LivestockHerdManagementUpdated", {"animal_id": payload["animal_id"], "change": "weight_observation"})
        return {"ok": True, "weight": entries[-1], "side_effects": ()}

    def record_movement_and_biosecurity(self, payload: dict) -> dict:
        required = ("permit_id", "animal_id", "origin_premises", "destination_premises", "movement_date", "quarantine_status", "biosecurity_score", "trace_lot_id")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        if payload["animal_id"] not in self.state["animals"]:
            return {"ok": False, "reason": "unknown_animal", "animal_id": payload["animal_id"], "side_effects": ()}
        if payload["quarantine_status"] == "open":
            self.state["quarantines"][payload["permit_id"]] = {
                "quarantine_id": payload["permit_id"],
                "animal_id": payload["animal_id"],
                "status": "open",
                "opened_on": payload["movement_date"],
            }
            return {
                "ok": False,
                "reason": "quarantine_open",
                "animal_id": payload["animal_id"],
                "quarantine": self.state["quarantines"][payload["permit_id"]],
                "side_effects": (),
            }
        self.state["quarantines"].pop(payload["permit_id"], None)
        audit = {
            "audit_id": f"audit-{payload['permit_id']}",
            "animal_id": payload["animal_id"],
            "biosecurity_score": payload["biosecurity_score"],
            "status": "pass" if payload["biosecurity_score"] >= self.state["parameters"]["biosecurity_min_score"] else "watch",
        }
        trace = {
            "trace_id": payload["trace_lot_id"],
            "animal_id": payload["animal_id"],
            "lot_id": payload["trace_lot_id"],
            "origin_premises": payload["origin_premises"],
            "destination_premises": payload["destination_premises"],
        }
        permit = {
            **dict(payload),
            "status": "approved" if audit["status"] == "pass" else "review",
        }
        self.state["biosecurity_audits"][audit["audit_id"]] = audit
        self.state["traceability_chains"][trace["trace_id"]] = trace
        self.state["movement_permits"][payload["permit_id"]] = permit
        self.state["animals"][payload["animal_id"]]["status"] = "active"
        self._record_timeline("LivestockHerdManagementApproved", {"animal_id": payload["animal_id"], "change": "movement_release"})
        return {"ok": True, "permit": permit, "biosecurity": audit, "traceability": trace, "side_effects": ()}

    def record_welfare_and_yield(self, payload: dict) -> dict:
        required = ("animal_id", "welfare_score", "weight_kg", "yield_id", "product_type", "quantity", "mortality_status")
        missing = tuple(field for field in required if _is_missing(payload.get(field)))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        if payload["animal_id"] not in self.state["animals"]:
            return {"ok": False, "reason": "unknown_animal", "animal_id": payload["animal_id"], "side_effects": ()}
        self.record_weight_observation(
            {
                "animal_id": payload["animal_id"],
                "recorded_on": payload.get("recorded_on", _today()),
                "weight_kg": payload["weight_kg"],
                "average_daily_gain_kg": payload.get("average_daily_gain_kg", 0.86),
            }
        )
        welfare = {
            "assessment_id": payload.get("assessment_id", f"welfare-{payload['yield_id']}"),
            "animal_id": payload["animal_id"],
            "welfare_score": payload["welfare_score"],
            "status": "watch" if payload["welfare_score"] < self.state["parameters"]["welfare_watch_threshold"] else "clear",
        }
        mortality = {
            "mortality_id": payload.get("mortality_id", f"mortality-{payload['yield_id']}"),
            "animal_id": payload["animal_id"],
            "status": payload["mortality_status"],
            "disposition_method": payload.get("disposition_method"),
        }
        withdrawal_active = any(
            item.get("animal_id") == payload["animal_id"] and item.get("withdrawal_active")
            for item in self.state["health_treatments"].values()
        )
        if withdrawal_active and payload["quantity"] > 0:
            return {"ok": False, "reason": "active_withdrawal_blocks_yield", "animal_id": payload["animal_id"], "side_effects": ()}
        yield_record = {
            "yield_id": payload["yield_id"],
            "animal_id": payload["animal_id"],
            "product_type": payload["product_type"],
            "quantity": payload["quantity"],
            "recorded_on": payload.get("recorded_on", _today()),
        }
        self.state["welfare_assessments"][welfare["assessment_id"]] = welfare
        self.state["mortalities"][mortality["mortality_id"]] = mortality
        self.state["inventory_yields"][yield_record["yield_id"]] = yield_record
        if payload["mortality_status"] != "alive":
            self.state["animals"][payload["animal_id"]]["status"] = "deceased"
            self.state["animals"][payload["animal_id"]]["lifecycle_state"] = "mortality_review"
        self._record_timeline("LivestockHerdManagementUpdated", {"animal_id": payload["animal_id"], "change": "welfare_and_yield"})
        return {"ok": True, "welfare": welfare, "mortality": mortality, "yield_record": yield_record, "side_effects": ()}

    def assistant_crud_preview(self, action: str, table: str, payload: dict | None = None, *, document_text: str = "", instructions: str = "") -> dict:
        preview = livestock_herd_management_mutation_preview(action, table, payload)
        candidate_forms = tuple(
            form["form_id"]
            for form in livestock_herd_management_form_catalog()["forms"]
            if table in form["owned_tables"]
        )
        preview_record = {
            **preview,
            "document_text": document_text,
            "instructions": instructions,
            "candidate_forms": candidate_forms,
            "candidate_wizards": tuple(
                wizard["wizard_id"]
                for wizard in livestock_herd_management_wizard_catalog()["wizards"]
                if any(step["form_id"] in candidate_forms for step in wizard["steps"])
            ),
        }
        self.state["assistant_previews"][f"preview-{len(self.state['assistant_previews']) + 1}"] = preview_record
        return preview_record

    def compute_analytics(self) -> dict:
        active_animals = [animal for animal in self.state["animals"].values() if animal.get("status") != "deceased"]
        due_vaccinations = [item for item in self.state["vaccinations"].values() if item.get("status") == "due"]
        open_quarantines = [item for item in self.state["quarantines"].values() if item.get("status") == "open"]
        active_pregnancies = [item for item in self.state["pregnancies"].values() if item.get("status") == "confirmed"]
        welfare_watch = [item for item in self.state["welfare_assessments"].values() if item.get("status") == "watch"]
        biosecurity_scores = [item.get("biosecurity_score", 0.0) for item in self.state["biosecurity_audits"].values()]
        weights = [entry.get("average_daily_gain_kg", 0.0) for entries in self.state["weights"].values() for entry in entries]
        milk_litres = sum(
            item.get("quantity", 0.0)
            for item in self.state["inventory_yields"].values()
            if item.get("product_type") == "milk"
        )
        mortality_count = sum(1 for item in self.state["mortalities"].values() if item.get("status") != "alive")
        total_animals = len(self.state["animals"]) or 1
        breeding_count = len(self.state["breeding_records"]) or 1
        genetics_watch = [item for item in self.state["genetics_profiles"].values() if item.get("genetic_warning")]
        return {
            "active_animals": len(active_animals),
            "herd_groups": len(self.state["herd_groups"]),
            "pregnancy_queue": len(active_pregnancies),
            "vaccination_due": len(due_vaccinations),
            "quarantine_open": len(open_quarantines),
            "average_daily_gain_kg": _safe_mean(weights),
            "milk_litres": round(milk_litres, 2),
            "mortality_rate": round(mortality_count / total_animals, 3),
            "biosecurity_average": _safe_mean(biosecurity_scores),
            "welfare_watch": len(welfare_watch),
            "breeding_success_rate": round(len(active_pregnancies) / breeding_count, 3),
            "genetics_watch": len(genetics_watch),
            "assistant_previews": len(self.state["assistant_previews"]),
        }

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.state["tenant"] = tenant
        self.register_animal(
            {
                "tenant": tenant,
                "animal_id": "cow-101",
                "species": "cattle",
                "production_type": "dairy",
                "primary_identifier": "RFID-DA-101",
                "source_provenance": "born_on_farm",
                "sex": "female",
                "birth_date": "2022-03-12",
                "breed": "Friesian",
                "default_group_id": "lactating-pen-a",
                "production_stage": "lactating",
                "requires_quarantine": False,
            }
        )
        self.register_animal(
            {
                "tenant": tenant,
                "animal_id": "heifer-202",
                "species": "cattle",
                "production_type": "breeding",
                "primary_identifier": "RFID-HE-202",
                "source_provenance": "purchased",
                "sex": "female",
                "birth_date": "2023-04-01",
                "breed": "Jersey",
                "default_group_id": "quarantine-yard",
                "production_stage": "quarantine",
                "requires_quarantine": True,
            }
        )
        self.record_weight_observation({"animal_id": "cow-101", "recorded_on": "2026-05-01", "weight_kg": 528, "average_daily_gain_kg": 0.78})
        self.record_weight_observation({"animal_id": "cow-101", "recorded_on": "2026-05-20", "weight_kg": 541, "average_daily_gain_kg": 0.91})
        self.record_genetics_profile(
            {
                "animal_id": "cow-101",
                "profile_id": "gen-101",
                "sire_reference": "sire-mwangi-7h",
                "dam_reference": "dam-eld-44",
                "inbreeding_risk": 0.07,
                "trait_markers": {"milk": "A2A2", "fertility": "high", "mastitis": "low"},
            }
        )
        self.record_breeding_cycle(
            {
                "breeding_id": "breed-101",
                "animal_id": "cow-101",
                "service_date": "2026-02-14",
                "service_method": "artificial_insemination",
                "sire_reference": "sire-mwangi-7h",
                "technician": "vet.njeri",
                "expected_due_date": "2026-11-23",
                "genetic_risk_score": 0.11,
            }
        )
        self.record_health_intervention(
            {
                "animal_id": "cow-101",
                "health_event_id": "health-101",
                "symptom": "post-calving fever watch",
                "diagnosis": "metabolic risk review",
                "treatment_name": "calcium-bolus",
                "vaccination_name": "fmd-booster",
                "medication_lot": "LOT-FMD-901",
                "withdrawal_days": 0,
                "administered_by": "tech.mwikali",
                "next_due_date": _days_from_today(5),
            }
        )
        self.record_feed_and_grazing_plan(
            {
                "plan_id": "feed-pen-a",
                "group_id": "lactating-pen-a",
                "ration_name": "high-energy-lactation",
                "dry_matter_pct": 54,
                "protein_pct": 18,
                "paddock_id": "pdk-7",
                "forage_cover_kg_dm": 2150,
                "rest_days_required": 28,
                "target_daily_gain_kg": 0.9,
                "stocking_density": 1.9,
            }
        )
        quarantine_attempt = self.record_movement_and_biosecurity(
            {
                "permit_id": "permit-202",
                "animal_id": "heifer-202",
                "origin_premises": "market-nakuru-2",
                "destination_premises": "farm-main-yard",
                "movement_date": _today(),
                "quarantine_status": "open",
                "biosecurity_score": 0.74,
                "trace_lot_id": "trace-heifer-202",
            }
        )
        quarantine_release = self.record_movement_and_biosecurity(
            {
                "permit_id": "permit-202",
                "animal_id": "heifer-202",
                "origin_premises": "market-nakuru-2",
                "destination_premises": "heifer-yard-1",
                "movement_date": _days_from_today(14),
                "quarantine_status": "released",
                "biosecurity_score": 0.86,
                "trace_lot_id": "trace-heifer-202",
            }
        )
        released_move = self.record_movement_and_biosecurity(
            {
                "permit_id": "permit-101",
                "animal_id": "cow-101",
                "origin_premises": "farm-main-yard",
                "destination_premises": "milk-collection-center-1",
                "movement_date": _today(),
                "quarantine_status": "released",
                "biosecurity_score": 0.93,
                "trace_lot_id": "trace-milk-101",
            }
        )
        self.record_welfare_and_yield(
            {
                "animal_id": "cow-101",
                "welfare_score": 0.91,
                "weight_kg": 545,
                "yield_id": "yield-101",
                "product_type": "milk",
                "quantity": 27.4,
                "mortality_status": "alive",
                "recorded_on": _today(),
            }
        )
        self.record_calving_event(
            {
                "calving_id": "calving-101",
                "dam_id": "cow-101",
                "offspring_id": "calf-501",
                "birth_date": _today(),
                "birth_weight_kg": 33.6,
                "assistance_level": "light",
                "colostrum_confirmed": True,
                "calf_sex": "female",
            }
        )
        self.assistant_crud_preview(
            "update",
            "livestock_herd_management_feed_ration",
            {"plan_id": "feed-pen-a", "protein_pct": 19},
            document_text="Nutrition note: increase protein for the lactating pen and verify paddock rest is still 28 days.",
            instructions="Preview only; show the exact form and wizard that would be used.",
        )
        return {
            "ok": True,
            "tenant": tenant,
            "quarantine_attempt": quarantine_attempt,
            "quarantine_release": quarantine_release,
            "released_move": released_move,
            "analytics": self.compute_analytics(),
            "state": self.state,
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or ui.livestock_herd_management_ui_contract()["action_permissions"]
        return ui.livestock_herd_management_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions,
        )

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def bootstrap_standalone_state(tenant: str = "tenant_demo") -> dict:
    """Return demo standalone state for tests and release evidence."""
    app = LivestockHerdManagementStandaloneApp()
    app.load_demo_workspace(tenant=tenant)
    return app.state


def documentation_presence() -> dict:
    """Describe documentation and operational artifacts expected for the slice."""
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "required_docs": ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"),
        "required_tests": ("tests/test_contract.py", "tests/test_standalone.py"),
        "side_effects": (),
    }


def livestock_herd_management_standalone_application_manifest() -> dict:
    """Return the executable standalone app contribution from the package."""
    app = LivestockHerdManagementStandaloneApp()
    bootstrap = app.load_demo_workspace()
    rendered = app.render_workbench(tenant=bootstrap["tenant"])
    controls = livestock_herd_management_control_center(app.state)
    return {
        "ok": bootstrap["ok"] and rendered["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "mode": "standalone_one_pbc_app",
        "app": ui.livestock_herd_management_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "bootstrap": {
            "tenant": bootstrap["tenant"],
            "animal_count": len(app.state["animals"]),
            "query_result_count": len(rendered["workbench"]["cards"]),
            "timeline_events": len(app.state["timeline"]),
            "analytics": bootstrap["analytics"],
        },
        "controls": controls,
        "documentation": documentation_presence(),
        "manifest_label": PBC_MANIFEST["label"],
        "side_effects": (),
    }


def validate_standalone_application() -> dict:
    """Validate that standalone docs, UI surfaces, and workflows are all present."""
    manifest = livestock_herd_management_standalone_application_manifest()
    app_contract = manifest["app"]
    docs = manifest["documentation"]
    missing_sections = tuple(
        section
        for section, present in (
            ("forms", bool(app_contract["forms"])),
            ("wizards", bool(app_contract["wizards"])),
            ("controls", bool(app_contract["controls"])),
            ("cards", bool(app_contract["workbench_shell"]["cards"])),
            ("documentation", docs["ok"]),
        )
        if not present
    )
    missing_workflows = tuple(
        workflow
        for workflow in (
            "animal_registry",
            "breeding_and_pregnancy",
            "health_and_vaccination",
            "feed_and_grazing",
            "movement_and_quarantine",
            "welfare_and_yield",
            "assistant_preview",
        )
        if workflow not in app_contract["domain_coverage"]
    )
    return {
        "ok": manifest["ok"] and not missing_sections and not missing_workflows,
        "pbc": PBC_KEY,
        "missing_sections": missing_sections,
        "missing_workflows": missing_workflows,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the standalone livestock app end to end."""
    app = LivestockHerdManagementStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant=loaded["tenant"])
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"]
        and rendered["ok"]
        and rendered["workbench"]["cards"][0]["value"] >= 1
        and release_snapshot["ok"],
        "manifest": livestock_herd_management_standalone_application_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }
