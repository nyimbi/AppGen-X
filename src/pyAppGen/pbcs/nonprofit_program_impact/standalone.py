"""Standalone one-PBC application surface for the nonprofit_program_impact package."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import agent
from . import controls
from . import ui
from .forms import nonprofit_program_impact_form_catalog
from .wizards import nonprofit_program_impact_wizard_catalog


PBC_KEY = "nonprofit_program_impact"
DEFAULT_EVENT_TOPIC = "pbc.nonprofit_program_impact.events"

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": DEFAULT_EVENT_TOPIC,
    "retry_limit": 3,
    "quality_score_floor": 0.65,
    "workbench_limit": 100,
}

DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.65,
    "materiality_threshold": 0.1,
    "approval_sla_hours": 72,
    "risk_threshold": 0.4,
    "forecast_horizon_days": 180,
    "workbench_limit": 100,
}

DEFAULT_RULES = (
    {
        "rule_id": "nonprofit_program_impact.program.default",
        "rule_type": "program_approval",
        "requires_theory_of_change": True,
        "requires_targets": True,
        "requires_geography": True,
        "status": "active",
    },
    {
        "rule_id": "nonprofit_program_impact.beneficiary.default",
        "rule_type": "eligibility_and_consent",
        "minimum_vulnerability_score": 40,
        "accepted_consent_statuses": ("consented", "guardian_consented"),
        "status": "active",
    },
    {
        "rule_id": "nonprofit_program_impact.reporting.default",
        "rule_type": "donor_report_freeze",
        "quality_score_floor": 0.65,
        "accepted_attribution_policies": ("direct", "proportional", "co_funded"),
        "status": "active",
    },
)


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


def _score_evidence(label: str | None) -> float:
    mapping = {
        "weak": 0.45,
        "moderate": 0.7,
        "strong": 0.9,
        "draft": 0.5,
        "verified": 0.85,
    }
    return mapping.get(str(label or "moderate"), 0.6)


def _sequence_id(prefix: str, existing: dict[str, Any]) -> str:
    return f"{prefix}-{len(existing) + 1:03d}"


def _append_outbox(state: dict[str, Any], event_type: str, payload: dict[str, Any]) -> None:
    state["outbox"] = tuple(state.get("outbox", ())) + ({"event_type": event_type, "payload": deepcopy(payload)},)


class NonprofitProgramImpactStandaloneService:
    """In-memory standalone service for nonprofit program design, delivery, and reporting."""

    def __init__(self) -> None:
        self.state: dict[str, Any] = {
            "configuration": {},
            "parameters": {},
            "rules": {},
            "programs": {},
            "beneficiaries": {},
            "service_episodes": {},
            "outcomes": {},
            "evidence_packs": {},
            "donor_reports": {},
            "safeguarding_incidents": {},
            "outbox": (),
        }
        self.configure()
        self.register_defaults()

    def close(self) -> None:
        """Release local resources."""
        return None

    def export_state(self) -> dict[str, Any]:
        """Return a deep copy of the in-memory standalone state."""
        return deepcopy(self.state)

    def configure(self, config: dict[str, Any] | None = None) -> dict:
        supplied = _copy_payload(config)
        self.state["configuration"] = {**DEFAULT_CONFIGURATION, **supplied}
        return {
            "ok": self.state["configuration"]["database_backend"] in {"postgresql", "mysql", "mariadb"},
            "configuration": deepcopy(self.state["configuration"]),
            "side_effects": (),
        }

    def register_defaults(self) -> dict:
        self.state["parameters"] = deepcopy(DEFAULT_PARAMETERS)
        self.state["rules"] = {rule["rule_id"]: deepcopy(rule) for rule in DEFAULT_RULES}
        return {
            "ok": True,
            "parameters": deepcopy(self.state["parameters"]),
            "rules": deepcopy(self.state["rules"]),
            "side_effects": (),
        }

    def create_program(self, payload: dict[str, Any]) -> dict:
        data = _copy_payload(payload)
        program_id = data.get("program_id") or _sequence_id("PROGRAM", self.state["programs"])
        theory_of_change = deepcopy(data.get("theory_of_change") or {})
        missing_toc = tuple(
            key
            for key in ("activities", "outputs", "short_term_outcomes", "long_term_impact")
            if not theory_of_change.get(key)
        )
        targets = tuple(deepcopy(data.get("targets") or ()))
        record = {
            "program_id": program_id,
            "tenant": data.get("tenant", "default"),
            "name": data.get("name", program_id),
            "theory_model": data.get("theory_model", "direct_service"),
            "target_population": data.get("target_population", "community"),
            "primary_geography": data.get("primary_geography", "unknown"),
            "measurement_horizon": data.get("measurement_horizon", "annual"),
            "funding_type": data.get("funding_type", "restricted"),
            "baseline_year": data.get("baseline_year", 2026),
            "theory_of_change": theory_of_change,
            "theory_of_change_ready": not missing_toc,
            "targets": targets,
            "eligible_geographies": tuple(data.get("eligible_geographies") or (data.get("primary_geography", "unknown"),)),
            "minimum_vulnerability_score": int(data.get("minimum_vulnerability_score", 40)),
            "approval_ready": not missing_toc and bool(targets),
            "status": data.get("status", "active"),
        }
        self.state["programs"][program_id] = record
        _append_outbox(self.state, "NonprofitProgramImpactCreated", {"program_id": program_id, "tenant": record["tenant"]})
        return {
            "ok": True,
            "record": deepcopy(record),
            "blocking_gaps": missing_toc,
            "side_effects": (),
        }

    def enroll_beneficiary(self, payload: dict[str, Any]) -> dict:
        data = _copy_payload(payload)
        program_id = data["program_id"]
        program = self.state["programs"].get(program_id)
        if program is None:
            return {"ok": False, "reason": "unknown_program", "program_id": program_id, "side_effects": ()}

        beneficiary_id = data.get("beneficiary_id") or _sequence_id("BEN", self.state["beneficiaries"])
        geography_ok = data.get("geography") in set(program.get("eligible_geographies", ()))
        vulnerability_ok = int(data.get("vulnerability_score", 0)) >= int(program.get("minimum_vulnerability_score", 0))
        consent_ready = data.get("consent_status") in {"consented", "guardian_consented"}
        eligibility_passed = geography_ok and vulnerability_ok
        record = {
            "beneficiary_id": beneficiary_id,
            "tenant": data.get("tenant", program["tenant"]),
            "program_id": program_id,
            "beneficiary_type": data.get("beneficiary_type", "person"),
            "age_band": data.get("age_band", "youth"),
            "geography": data.get("geography"),
            "vulnerability_score": int(data.get("vulnerability_score", 0)),
            "consent_status": data.get("consent_status", "pending"),
            "consent_ready": consent_ready,
            "eligibility_passed": eligibility_passed,
            "cohort_key": data.get("cohort_key", f"{program_id}:core"),
            "status": "enrolled" if eligibility_passed and consent_ready else "blocked",
        }
        self.state["beneficiaries"][beneficiary_id] = record
        _append_outbox(self.state, "NonprofitProgramImpactUpdated", {"beneficiary_id": beneficiary_id, "program_id": program_id})
        return {
            "ok": eligibility_passed and consent_ready,
            "record": deepcopy(record),
            "blocking_gaps": tuple(
                gap
                for gap, failed in (
                    ("geography_not_eligible", not geography_ok),
                    ("vulnerability_threshold_not_met", not vulnerability_ok),
                    ("consent_not_usable", not consent_ready),
                )
                if failed
            ),
            "side_effects": (),
        }

    def record_service_episode(self, payload: dict[str, Any]) -> dict:
        data = _copy_payload(payload)
        episode_id = data.get("episode_id") or _sequence_id("EP", self.state["service_episodes"])
        program = self.state["programs"].get(data.get("program_id"))
        beneficiary = self.state["beneficiaries"].get(data.get("beneficiary_id"))
        if program is None or beneficiary is None:
            return {"ok": False, "reason": "missing_program_or_beneficiary", "side_effects": ()}

        planned_dosage = max(int(data.get("planned_dosage", 0)), 1)
        delivered_dosage = max(int(data.get("delivered_dosage", 0)), 0)
        ratio = round(delivered_dosage / planned_dosage, 4)
        fidelity_status = data.get("fidelity_status", "on_model")
        safeguarding_flag = data.get("safeguarding_flag", "clear")
        record = {
            "episode_id": episode_id,
            "tenant": beneficiary["tenant"],
            "program_id": data["program_id"],
            "beneficiary_id": data["beneficiary_id"],
            "service_type": data.get("service_type", "mentoring"),
            "delivery_channel": data.get("delivery_channel", "in_person"),
            "planned_dosage": planned_dosage,
            "delivered_dosage": delivered_dosage,
            "dosage_completion_ratio": ratio,
            "fidelity_status": fidelity_status,
            "referral_status": data.get("referral_status", "not_required"),
            "safeguarding_flag": safeguarding_flag,
            "status": "completed" if ratio >= 1.0 and fidelity_status != "at_risk" else "follow_up_required",
        }
        self.state["service_episodes"][episode_id] = record
        if safeguarding_flag in {"needs_follow_up", "incident_opened"}:
            incident_id = _sequence_id("SAFE", self.state["safeguarding_incidents"])
            self.state["safeguarding_incidents"][incident_id] = {
                "incident_id": incident_id,
                "tenant": beneficiary["tenant"],
                "beneficiary_id": data["beneficiary_id"],
                "episode_id": episode_id,
                "status": "open",
                "severity": "high" if safeguarding_flag == "incident_opened" else "medium",
            }
        _append_outbox(self.state, "NonprofitProgramImpactUpdated", {"episode_id": episode_id, "program_id": data["program_id"]})
        return {
            "ok": beneficiary["eligibility_passed"] and beneficiary["consent_ready"],
            "record": deepcopy(record),
            "side_effects": (),
        }

    def record_outcome_observation(self, payload: dict[str, Any]) -> dict:
        data = _copy_payload(payload)
        outcome_id = data.get("outcome_id") or _sequence_id("OUT", self.state["outcomes"])
        baseline_value = int(data.get("baseline_value", 0))
        target_value = max(int(data.get("target_value", 0)), 1)
        actual_value = int(data.get("actual_value", 0))
        attainment_ratio = round(actual_value / target_value, 4)
        evidence_quality_score = _score_evidence(data.get("evidence_quality", "moderate"))
        record = {
            "outcome_id": outcome_id,
            "tenant": data.get("tenant", "default"),
            "program_id": data["program_id"],
            "beneficiary_id": data["beneficiary_id"],
            "indicator_key": data.get("indicator_key", "indicator.unknown"),
            "measurement_window": data.get("measurement_window", "90_day"),
            "baseline_value": baseline_value,
            "target_value": target_value,
            "actual_value": actual_value,
            "delta": actual_value - baseline_value,
            "attainment_ratio": attainment_ratio,
            "evidence_quality": data.get("evidence_quality", "moderate"),
            "evidence_quality_score": evidence_quality_score,
            "status": "on_track" if attainment_ratio >= 1 else "at_risk",
            "supporting_episode_id": data.get("supporting_episode_id"),
        }
        self.state["outcomes"][outcome_id] = record
        _append_outbox(self.state, "NonprofitProgramImpactApproved", {"outcome_id": outcome_id, "program_id": data["program_id"]})
        return {
            "ok": evidence_quality_score >= self.state["parameters"]["quality_score_floor"],
            "record": deepcopy(record),
            "side_effects": (),
        }

    def create_evidence_pack(self, payload: dict[str, Any]) -> dict:
        data = _copy_payload(payload)
        evidence_id = data.get("evidence_id") or _sequence_id("EVID", self.state["evidence_packs"])
        quality_score = round(
            (_score_evidence(data.get("source_strength", "moderate")) + _score_evidence(data.get("verification_status", "verified"))) / 2,
            4,
        )
        record = {
            "evidence_id": evidence_id,
            "tenant": data.get("tenant", "default"),
            "program_id": data["program_id"],
            "beneficiary_id": data.get("beneficiary_id"),
            "outcome_id": data.get("outcome_id"),
            "source_strength": data.get("source_strength", "moderate"),
            "verification_status": data.get("verification_status", "verified"),
            "confidentiality": data.get("confidentiality", "internal"),
            "quality_score": quality_score,
            "story_use_allowed": data.get("story_use_allowed", True),
        }
        self.state["evidence_packs"][evidence_id] = record
        _append_outbox(self.state, "NonprofitProgramImpactUpdated", {"evidence_id": evidence_id, "program_id": data["program_id"]})
        return {
            "ok": quality_score >= self.state["parameters"]["quality_score_floor"],
            "record": deepcopy(record),
            "side_effects": (),
        }

    def freeze_donor_report(self, payload: dict[str, Any]) -> dict:
        data = _copy_payload(payload)
        report_id = data.get("report_id") or _sequence_id("REPORT", self.state["donor_reports"])
        program_id = data["program_id"]
        outcomes = tuple(outcome for outcome in self.state["outcomes"].values() if outcome["program_id"] == program_id)
        evidence = tuple(pack for pack in self.state["evidence_packs"].values() if pack["program_id"] == program_id)
        quality_gate_passed = bool(outcomes) and bool(evidence) and min(
            tuple(outcome["evidence_quality_score"] for outcome in outcomes)
            + tuple(pack["quality_score"] for pack in evidence)
        ) >= self.state["parameters"]["quality_score_floor"]
        status = "frozen" if data.get("report_status", "review") == "frozen" and quality_gate_passed else "review"
        record = {
            "report_id": report_id,
            "tenant": data.get("tenant", "default"),
            "program_id": program_id,
            "reporting_period": data.get("reporting_period", "2026-Q2"),
            "attribution_policy": data.get("attribution_policy", "direct"),
            "freeze_reason": data.get("freeze_reason", "quarter close"),
            "status": status,
            "quality_gate_passed": quality_gate_passed,
            "indicator_snapshot": {
                "outcome_count": len(outcomes),
                "evidence_count": len(evidence),
                "average_attainment": round(sum(item["attainment_ratio"] for item in outcomes) / len(outcomes), 4) if outcomes else 0.0,
            },
        }
        self.state["donor_reports"][report_id] = record
        _append_outbox(self.state, "NonprofitProgramImpactApproved", {"report_id": report_id, "program_id": program_id})
        return {
            "ok": status == "frozen",
            "record": deepcopy(record),
            "side_effects": (),
        }

    def build_workbench(self, tenant: str = "default") -> dict:
        programs = tuple(item for item in self.state["programs"].values() if item["tenant"] == tenant)
        beneficiaries = tuple(item for item in self.state["beneficiaries"].values() if item["tenant"] == tenant)
        service_episodes = tuple(item for item in self.state["service_episodes"].values() if item["tenant"] == tenant)
        outcomes = tuple(item for item in self.state["outcomes"].values() if item["tenant"] == tenant)
        donor_reports = tuple(item for item in self.state["donor_reports"].values() if item["tenant"] == tenant)
        safeguarding_incidents = tuple(item for item in self.state["safeguarding_incidents"].values() if item["tenant"] == tenant)
        metrics = {
            "active_programs": len(tuple(program for program in programs if program["status"] == "active")),
            "enrolled_beneficiaries": len(tuple(beneficiary for beneficiary in beneficiaries if beneficiary["status"] == "enrolled")),
            "service_completion_ratio": round(
                sum(item["dosage_completion_ratio"] for item in service_episodes) / len(service_episodes), 4
            ) if service_episodes else 0.0,
            "outcome_attainment_rate": round(
                sum(item["attainment_ratio"] for item in outcomes) / len(outcomes), 4
            ) if outcomes else 0.0,
            "frozen_reports": len(tuple(report for report in donor_reports if report["status"] == "frozen")),
            "open_safeguarding_incidents": len(tuple(item for item in safeguarding_incidents if item["status"] != "closed")),
        }
        return {
            "ok": True,
            "tenant": tenant,
            "metrics": metrics,
            "queues": {
                "programs_requiring_design_review": tuple(program["program_id"] for program in programs if not program["theory_of_change_ready"]),
                "beneficiaries_requiring_follow_up": tuple(item["beneficiary_id"] for item in beneficiaries if item["status"] != "enrolled"),
                "reports_waiting_for_freeze": tuple(item["report_id"] for item in donor_reports if item["status"] != "frozen"),
            },
            "side_effects": (),
        }

    def build_beneficiary_timeline(self, beneficiary_id: str) -> dict:
        beneficiary = self.state["beneficiaries"].get(beneficiary_id)
        if beneficiary is None:
            return {"ok": False, "reason": "unknown_beneficiary", "beneficiary_id": beneficiary_id, "side_effects": ()}

        entries = []
        entries.append({"stage": "enrollment", "record_id": beneficiary_id, "status": beneficiary["status"]})
        for episode in self.state["service_episodes"].values():
            if episode["beneficiary_id"] == beneficiary_id:
                entries.append({"stage": "service", "record_id": episode["episode_id"], "status": episode["status"]})
        for outcome in self.state["outcomes"].values():
            if outcome["beneficiary_id"] == beneficiary_id:
                entries.append({"stage": "outcome", "record_id": outcome["outcome_id"], "status": outcome["status"]})
        for evidence in self.state["evidence_packs"].values():
            if evidence.get("beneficiary_id") == beneficiary_id:
                entries.append({"stage": "evidence", "record_id": evidence["evidence_id"], "status": evidence["verification_status"]})
        return {
            "ok": True,
            "beneficiary_id": beneficiary_id,
            "event_count": len(entries),
            "entries": tuple(entries),
            "side_effects": (),
        }


def nonprofit_program_impact_standalone_app_contract() -> dict:
    """Return the composed standalone-app surface for this one-PBC package."""
    forms = nonprofit_program_impact_form_catalog()
    wizards = nonprofit_program_impact_wizard_catalog()
    control_catalog = controls.nonprofit_program_impact_control_catalog()
    ui_contract = ui.nonprofit_program_impact_ui_contract()
    assistant = agent.composed_agent_contribution()
    return {
        "format": "appgen.nonprofit-program-impact-standalone-app.v1",
        "ok": all(item.get("ok") is True for item in (forms, wizards, control_catalog, ui_contract, assistant)),
        "pbc": PBC_KEY,
        "app_class": "NonprofitProgramImpactStandaloneService",
        "implementation_directory": "src/pyAppGen/pbcs/nonprofit_program_impact",
        "service_methods": (
            "configure",
            "register_defaults",
            "create_program",
            "enroll_beneficiary",
            "record_service_episode",
            "record_outcome_observation",
            "create_evidence_pack",
            "freeze_donor_report",
            "build_workbench",
            "build_beneficiary_timeline",
            "export_state",
        ),
        "forms": forms,
        "wizards": wizards,
        "controls": control_catalog,
        "ui": ui_contract,
        "agent": assistant,
        "side_effects": (),
    }


def nonprofit_program_impact_bootstrap_standalone_app() -> dict:
    """Create a live standalone service for local package use."""
    service = NonprofitProgramImpactStandaloneService()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service": service,
        "contract": nonprofit_program_impact_standalone_app_contract(),
        "side_effects": (),
    }


def nonprofit_program_impact_standalone_app_smoke() -> dict:
    """Exercise the standalone app through a domain-deep happy path."""
    bundle = nonprofit_program_impact_bootstrap_standalone_app()
    service = bundle["service"]
    try:
        program = service.create_program(
            {
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "name": "Youth Skills Acceleration",
                "theory_model": "direct_service",
                "target_population": "Out-of-school youth",
                "primary_geography": "Nairobi",
                "eligible_geographies": ("Nairobi",),
                "measurement_horizon": "annual",
                "funding_type": "restricted",
                "baseline_year": 2026,
                "minimum_vulnerability_score": 40,
                "targets": ({"indicator_key": "employment_placement", "target_value": 70},),
                "theory_of_change": {
                    "activities": ("mentorship", "job-readiness training"),
                    "outputs": ("training sessions completed",),
                    "short_term_outcomes": ("improved employability",),
                    "long_term_impact": ("stable income",),
                },
            }
        )
        beneficiary = service.enroll_beneficiary(
            {
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "beneficiary_id": "BEN-001",
                "beneficiary_type": "person",
                "age_band": "youth",
                "geography": "Nairobi",
                "vulnerability_score": 65,
                "consent_status": "consented",
            }
        )
        episode = service.record_service_episode(
            {
                "program_id": "PROGRAM-001",
                "beneficiary_id": "BEN-001",
                "episode_id": "EP-001",
                "service_type": "mentoring",
                "delivery_channel": "hybrid",
                "planned_dosage": 8,
                "delivered_dosage": 8,
                "fidelity_status": "on_model",
                "safeguarding_flag": "clear",
            }
        )
        outcome = service.record_outcome_observation(
            {
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "beneficiary_id": "BEN-001",
                "outcome_id": "OUT-001",
                "indicator_key": "employment_placement",
                "measurement_window": "90_day",
                "baseline_value": 0,
                "target_value": 1,
                "actual_value": 1,
                "evidence_quality": "strong",
                "supporting_episode_id": "EP-001",
            }
        )
        evidence = service.create_evidence_pack(
            {
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "beneficiary_id": "BEN-001",
                "outcome_id": "OUT-001",
                "evidence_id": "EVID-001",
                "source_strength": "strong",
                "verification_status": "verified",
                "confidentiality": "internal",
                "story_use_allowed": True,
            }
        )
        donor_report = service.freeze_donor_report(
            {
                "tenant": "tenant-smoke",
                "program_id": "PROGRAM-001",
                "report_id": "REPORT-001",
                "reporting_period": "2026-Q2",
                "attribution_policy": "direct",
                "freeze_reason": "Quarter close review complete",
                "report_status": "frozen",
            }
        )
        workbench = service.build_workbench("tenant-smoke")
        timeline = service.build_beneficiary_timeline("BEN-001")
        state = service.export_state()
        ui_contract = ui.nonprofit_program_impact_ui_contract()
        permissions = tuple(dict.fromkeys(ui_contract["action_permissions"].values()))
        rendered = ui.nonprofit_program_impact_render_workbench(
            state,
            tenant="tenant-smoke",
            principal_permissions=permissions,
        )
        control_center = controls.nonprofit_program_impact_control_center(state)
        return {
            "ok": all(
                item["ok"] is True
                for item in (
                    bundle,
                    program,
                    beneficiary,
                    episode,
                    outcome,
                    evidence,
                    donor_report,
                    workbench,
                    timeline,
                    rendered,
                    control_center,
                )
            ),
            "contract": bundle["contract"],
            "program": program,
            "beneficiary": beneficiary,
            "episode": episode,
            "outcome": outcome,
            "evidence": evidence,
            "donor_report": donor_report,
            "workbench": workbench,
            "timeline": timeline,
            "rendered": rendered,
            "controls": control_center,
            "state": state,
            "side_effects": (),
        }
    finally:
        service.close()
