"""Standalone application contract for the Project Portfolio Management PBC.

The module is intentionally in-memory and side-effect-free so release audits can
prove a single-PBC composed app would have forms, controls, workflows, agent
previews, owned datastore contracts, and executable portfolio governance logic
without requiring external services.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import (
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    PROJECT_PORTFOLIO_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    PROJECT_PORTFOLIO_MANAGEMENT_CONSUMED_EVENT_TYPES,
    PROJECT_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES,
    PROJECT_PORTFOLIO_MANAGEMENT_OWNED_TABLES,
    PROJECT_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    project_portfolio_management_build_api_contract,
    project_portfolio_management_build_schema_contract,
    project_portfolio_management_build_service_contract,
    project_portfolio_management_configure_runtime,
    project_portfolio_management_empty_state,
    project_portfolio_management_permissions_contract,
    project_portfolio_management_receive_event,
    project_portfolio_management_register_rule,
    project_portfolio_management_runtime_smoke,
    project_portfolio_management_set_parameter,
)
from .ui import project_portfolio_management_render_workbench, project_portfolio_management_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "project_portfolio_management"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class ProjectPortfolioManagementStandaloneApp:
    tenant: str = "tenant-ppm-001"
    state: dict = field(default_factory=project_portfolio_management_empty_state)
    items: dict[str, dict] = field(default_factory=dict)
    cases: dict[str, dict] = field(default_factory=dict)
    scores: dict[str, dict] = field(default_factory=dict)
    prioritization_runs: dict[str, dict] = field(default_factory=dict)
    gates: dict[str, dict] = field(default_factory=dict)
    dependencies: dict[str, dict] = field(default_factory=dict)
    resources: dict[str, dict] = field(default_factory=dict)
    benefits: dict[str, dict] = field(default_factory=dict)
    risks: dict[str, dict] = field(default_factory=dict)
    issues: dict[str, dict] = field(default_factory=dict)
    change_requests: dict[str, dict] = field(default_factory=dict)
    financials: dict[str, dict] = field(default_factory=dict)
    exceptions: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = project_portfolio_management_configure_runtime(
            self.state,
            {
                "database_backend": database_backend,
                "event_topic": PROJECT_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC,
                "stream_engine_picker_visible": False,
            },
        )
        self.state = configured["state"]
        for name, value in (
            ("intake_readiness_floor", 70),
            ("risk_appetite_threshold", 0.70),
            ("financial_materiality", 100000),
            ("capacity_conflict_threshold", 1.0),
            ("benefit_confidence_floor", 0.60),
            ("agent_confirmation_required", True),
        ):
            result = project_portfolio_management_set_parameter(self.state, name, value)
            self.state = result["state"]
        for rule_id in (
            "intake_readiness_required",
            "scoring_weights_balanced",
            "prioritization_must_fit_constraints",
            "gate_requires_evidence_and_quorum",
            "resource_capacity_not_exceeded",
            "benefit_claim_requires_attribution",
            "financial_variance_requires_explanation",
            "agent_mutations_require_confirmation",
        ):
            result = project_portfolio_management_register_rule(self.state, {"rule_id": rule_id, "scope": "portfolio"})
            self.state = result["state"]
        inbound = project_portfolio_management_receive_event(
            self.state,
            {"event_type": PROJECT_PORTFOLIO_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "ppm-budget-001"},
        )
        self.state = inbound["state"]
        return {"ok": configured["ok"] and inbound["ok"], "side_effects": ()}

    def intake_item(
        self,
        item_id: str,
        title: str,
        sponsor: str | None,
        archetype: str,
        objectives: tuple[str, ...],
        evidence: tuple[str, ...],
        readiness_score: int,
    ) -> dict:
        control = evaluate_control("intake_readiness_required", {"score": readiness_score})
        ok = bool(title) and bool(sponsor) and bool(objectives) and control["ok"]
        item = {
            "id": item_id,
            "tenant": self.tenant,
            "title": title,
            "sponsor": sponsor,
            "archetype": archetype,
            "objectives": tuple(objectives),
            "evidence": tuple(evidence),
            "readiness_score": readiness_score,
            "state": "case_ready" if ok else "remediation",
            "blockers": control["failures"],
        }
        self.items[item_id] = item
        return {"ok": ok, "item": item, "side_effects": ()}

    def create_business_case(
        self,
        case_id: str,
        item_id: str,
        cost: float,
        benefit: float,
        assumptions: tuple[str, ...],
        expired_assumptions: int = 0,
    ) -> dict:
        control = evaluate_control("business_case_assumptions_current", {"expired_assumptions": expired_assumptions})
        ok = item_id in self.items and cost > 0 and benefit > 0 and control["ok"]
        business_case = {
            "id": case_id,
            "tenant": self.tenant,
            "item_id": item_id,
            "cost": cost,
            "benefit": benefit,
            "assumptions": tuple(assumptions),
            "roi": round((benefit - cost) / cost, 3) if cost else 0,
            "status": "approved" if ok else "blocked",
            "blockers": control["failures"],
        }
        self.cases[case_id] = business_case
        return {"ok": ok, "business_case": business_case, "side_effects": ()}

    def score_item(
        self,
        score_id: str,
        item_id: str,
        strategic_value: float,
        financial_value: float,
        execution_risk: float,
        benefit_confidence: float,
        weights: tuple[float, float, float, float] = (0.40, 0.25, 0.20, 0.15),
    ) -> dict:
        control = evaluate_control("scoring_weights_balanced", {"weights": weights})
        score = round(
            strategic_value * weights[0]
            + financial_value * weights[1]
            + (1 - execution_risk) * weights[2]
            + benefit_confidence * weights[3],
            3,
        )
        row = {
            "id": score_id,
            "tenant": self.tenant,
            "item_id": item_id,
            "strategic_value": strategic_value,
            "financial_value": financial_value,
            "execution_risk": execution_risk,
            "benefit_confidence": benefit_confidence,
            "weights": weights,
            "score": score,
            "model_version": "ppm-score-v1",
            "explanation_hash": _digest((item_id, score, weights)),
        }
        self.scores[score_id] = row
        return {"ok": item_id in self.items and control["ok"], "score": row, "control": control, "side_effects": ()}

    def prioritize(self, run_id: str, item_ids: tuple[str, ...], budget: float, capacity: int) -> dict:
        cost = sum(case["cost"] for case in self.cases.values() if case["item_id"] in item_ids)
        demand = len(item_ids)
        control = evaluate_control(
            "prioritization_must_fit_constraints",
            {"cost": cost, "budget": budget, "demand": demand, "capacity": capacity},
        )
        ranked = tuple(
            sorted(
                item_ids,
                key=lambda item_id: max((score["score"] for score in self.scores.values() if score["item_id"] == item_id), default=0),
                reverse=True,
            )
        )
        selected = ranked if control["ok"] else ranked[: max(0, capacity)]
        run = {
            "id": run_id,
            "tenant": self.tenant,
            "item_ids": tuple(item_ids),
            "budget": budget,
            "capacity": capacity,
            "cost": cost,
            "selected_items": selected,
            "rejected_items": tuple(item_id for item_id in ranked if item_id not in selected),
            "status": "published" if control["ok"] else "scenario_only",
            "constraint_failures": control["failures"],
        }
        self.prioritization_runs[run_id] = run
        return {"ok": control["ok"], "run": run, "side_effects": ()}

    def record_gate(
        self,
        gate_id: str,
        item_id: str,
        gate: str,
        evidence: tuple[str, ...],
        quorum: bool,
        decision: str,
        conditions: tuple[str, ...] = (),
    ) -> dict:
        control = evaluate_control("gate_requires_evidence_and_quorum", {"evidence": evidence, "quorum": quorum})
        ok = item_id in self.items and control["ok"] and decision in {"approved", "conditional", "deferred", "rejected"}
        gate_row = {
            "id": gate_id,
            "tenant": self.tenant,
            "item_id": item_id,
            "gate": gate,
            "decision": decision if ok else "blocked",
            "conditions": tuple(conditions),
            "blockers": control["failures"],
        }
        self.gates[gate_id] = gate_row
        return {"ok": ok, "gate": gate_row, "side_effects": ()}

    def map_dependency(self, dependency_id: str, predecessor_id: str, successor_id: str, risk: float) -> dict:
        ok = predecessor_id in self.items and successor_id in self.items and predecessor_id != successor_id
        dependency = {
            "id": dependency_id,
            "tenant": self.tenant,
            "predecessor_id": predecessor_id,
            "successor_id": successor_id,
            "risk": risk,
            "propagated_exposure": round(risk * 1.2, 3),
            "status": "mapped" if ok else "invalid",
        }
        self.dependencies[dependency_id] = dependency
        return {"ok": ok, "dependency": dependency, "side_effects": ()}

    def assign_resources(self, assignment_id: str, item_id: str, skill: str, demand: int, supply: int) -> dict:
        control = evaluate_control("resource_capacity_not_exceeded", {"demand": demand, "supply": supply})
        row = {
            "id": assignment_id,
            "tenant": self.tenant,
            "item_id": item_id,
            "skill": skill,
            "demand": demand,
            "supply": supply,
            "status": "assigned" if control["ok"] else "conflict",
            "blockers": control["failures"],
        }
        self.resources[assignment_id] = row
        return {"ok": item_id in self.items and control["ok"], "assignment": row, "side_effects": ()}

    def measure_benefit(
        self,
        benefit_id: str,
        item_id: str,
        baseline: float,
        target: float,
        actual: float,
        attribution: str | None,
        confidence: float,
    ) -> dict:
        control = evaluate_control("benefit_claim_requires_attribution", {"attribution": attribution})
        leakage = max(0, target - actual)
        ok = item_id in self.items and control["ok"] and confidence >= 0.60
        benefit = {
            "id": benefit_id,
            "tenant": self.tenant,
            "item_id": item_id,
            "baseline": baseline,
            "target": target,
            "actual": actual,
            "attribution": attribution,
            "confidence": confidence,
            "leakage": leakage,
            "status": "accepted" if ok else "review",
        }
        self.benefits[benefit_id] = benefit
        return {"ok": ok, "benefit": benefit, "side_effects": ()}

    def record_risk(self, risk_id: str, item_id: str, exposure: float, accepted: bool = False) -> dict:
        control = evaluate_control("risk_appetite_breach_requires_acceptance", {"breach": exposure > 0.70, "accepted": accepted})
        risk = {
            "id": risk_id,
            "tenant": self.tenant,
            "item_id": item_id,
            "exposure": exposure,
            "status": "accepted" if control["ok"] else "escalate",
            "blockers": control["failures"],
        }
        self.risks[risk_id] = risk
        return {"ok": item_id in self.items and control["ok"], "risk": risk, "side_effects": ()}

    def open_issue(self, issue_id: str, item_id: str, severity: str, owner: str | None) -> dict:
        ok = item_id in self.items and severity in {"low", "medium", "high", "critical"} and bool(owner)
        issue = {"id": issue_id, "tenant": self.tenant, "item_id": item_id, "severity": severity, "owner": owner, "status": "open" if ok else "blocked"}
        self.issues[issue_id] = issue
        return {"ok": ok, "issue": issue, "side_effects": ()}

    def process_change_request(self, change_id: str, item_id: str, cost_delta: float, benefit_delta: float, approved: bool) -> dict:
        ok = item_id in self.items and approved
        request = {
            "id": change_id,
            "tenant": self.tenant,
            "item_id": item_id,
            "cost_delta": cost_delta,
            "benefit_delta": benefit_delta,
            "portfolio_impact": round(benefit_delta - cost_delta, 2),
            "status": "approved" if ok else "pending_approval",
        }
        self.change_requests[change_id] = request
        return {"ok": ok, "change_request": request, "side_effects": ()}

    def snapshot_financials(
        self,
        snapshot_id: str,
        item_id: str,
        baseline: float,
        forecast: float,
        actual: float,
        explanation: str | None = None,
        materiality: float = 100000,
    ) -> dict:
        variance = forecast - baseline
        control = evaluate_control(
            "financial_variance_requires_explanation",
            {"variance": variance, "materiality": materiality, "explanation": explanation},
        )
        snapshot = {
            "id": snapshot_id,
            "tenant": self.tenant,
            "item_id": item_id,
            "baseline": baseline,
            "forecast": forecast,
            "actual": actual,
            "variance": variance,
            "explanation": explanation,
            "status": "accepted" if control["ok"] else "explanation_required",
        }
        self.financials[snapshot_id] = snapshot
        return {"ok": item_id in self.items and control["ok"], "financial_snapshot": snapshot, "side_effects": ()}

    def resolve_exception(self, exception_id: str, item_id: str, reason: str, approver: str | None) -> dict:
        ok = item_id in self.items and bool(reason) and bool(approver)
        exception = {"id": exception_id, "tenant": self.tenant, "item_id": item_id, "reason": reason, "approver": approver, "status": "resolved" if ok else "open"}
        self.exceptions[exception_id] = exception
        return {"ok": ok, "exception": exception, "side_effects": ()}

    def simulate_scenario(self, name: str, budget_delta: float, capacity_delta: int) -> dict:
        return {
            "ok": True,
            "mutates_live_records": False,
            "name": name,
            "budget_delta": budget_delta,
            "capacity_delta": capacity_delta,
            "items_considered": tuple(self.items),
            "portfolio_digest": _digest((tuple(self.items), tuple(self.cases), budget_delta, capacity_delta)),
            "narrative": "side-effect-free executive scenario",
            "side_effects": (),
        }

    def assistant_portfolio_action_preview(self, document: str, instruction: str, confirmed: bool = False) -> dict:
        control = evaluate_control("agent_mutations_require_confirmation", {"confirmed": confirmed})
        document_plan = document_instruction_plan(document, instruction)
        crud_preview = datastore_crud_plan(
            "update",
            table="project_portfolio_management_portfolio_item",
            payload={"instruction": instruction},
        )
        return {
            "ok": document_plan["ok"] and crud_preview["ok"] and control["ok"],
            "control": control,
            "document_plan": document_plan,
            "crud_preview": crud_preview,
            "requires_confirmation": not confirmed,
            "side_effects": (),
        }

    def app_contract(self) -> dict:
        return {
            "format": "appgen.project-portfolio-management.standalone-app.v1",
            "ok": True,
            "pbc": PBC_KEY,
            "owned_tables": PROJECT_PORTFOLIO_MANAGEMENT_OWNED_TABLES,
            "database_backends": PROJECT_PORTFOLIO_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "schema": project_portfolio_management_build_schema_contract(),
            "services": project_portfolio_management_build_service_contract(),
            "routes": project_portfolio_management_build_api_contract(),
            "permissions": project_portfolio_management_permissions_contract(),
            "ui": project_portfolio_management_ui_contract(),
            "workbench": project_portfolio_management_render_workbench(),
            "forms": form_catalog(),
            "wizards": wizard_catalog(),
            "controls": control_catalog(),
            "agent": chatbot_interface_contract(),
            "composed_agent": composed_agent_contribution(),
            "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True},
            "side_effects": (),
        }

    def run_demo(self) -> dict:
        configured = self.configure()
        weak_intake = self.intake_item("I0", "Incomplete", None, "innovation", (), (), 10)
        item = self.intake_item("I1", "Modernize portfolio governance", "CFO", "platform", ("growth",), ("brief",), 85)
        second_item = self.intake_item("I2", "Resilience uplift", "COO", "risk", ("resilience",), ("risk memo",), 82)
        business_case = self.create_business_case("BC1", "I1", 100000, 250000, ("adoption", "automation"))
        score = self.score_item("S1", "I1", 0.90, 0.80, 0.20, 0.80)
        constrained = self.prioritize("P0", ("I1", "I2"), 50000, 1)
        prioritized = self.prioritize("P1", ("I1",), 200000, 1)
        missing_gate = self.record_gate("G0", "I1", "funding", (), True, "approved")
        gate = self.record_gate("G1", "I1", "funding", ("case",), True, "approved")
        dependency = self.map_dependency("D1", "I1", "I2", 0.30)
        overallocated = self.assign_resources("R0", "I1", "architect", 2, 1)
        assigned = self.assign_resources("R1", "I1", "architect", 1, 1)
        unattributed = self.measure_benefit("B0", "I1", 0, 100, 80, None, 0.80)
        benefit = self.measure_benefit("B1", "I1", 0, 100, 90, "metric", 0.80)
        unaccepted_risk = self.record_risk("RK0", "I1", 0.90, False)
        accepted_risk = self.record_risk("RK1", "I1", 0.90, True)
        issue = self.open_issue("ISS1", "I1", "high", "portfolio-owner")
        change = self.process_change_request("CR1", "I1", 15000, 40000, True)
        unexplained = self.snapshot_financials("F0", "I1", 100000, 250000, 90000, materiality=100000)
        explained = self.snapshot_financials("F1", "I1", 100000, 250000, 90000, "scope expansion", materiality=100000)
        exception = self.resolve_exception("EX1", "I1", "strategic mandate", "cfo")
        scenario = self.simulate_scenario("capital cut", -10000, 0)
        unconfirmed_agent = self.assistant_portfolio_action_preview("case", "update priority", False)
        confirmed_agent = self.assistant_portfolio_action_preview("case", "update priority", True)
        checks = (
            configured["ok"],
            weak_intake["ok"] is False,
            item["ok"],
            second_item["ok"],
            business_case["ok"],
            score["ok"],
            constrained["ok"] is False,
            prioritized["ok"],
            missing_gate["ok"] is False,
            gate["ok"],
            dependency["ok"],
            overallocated["ok"] is False,
            assigned["ok"],
            unattributed["ok"] is False,
            benefit["ok"],
            unaccepted_risk["ok"] is False,
            accepted_risk["ok"],
            issue["ok"],
            change["ok"],
            unexplained["ok"] is False,
            explained["ok"],
            exception["ok"],
            scenario["mutates_live_records"] is False,
            unconfirmed_agent["ok"] is False,
            confirmed_agent["ok"],
        )
        return {"ok": all(checks), "app_contract": self.app_contract(), "side_effects": ()}


def single_pbc_app_contract() -> dict:
    return ProjectPortfolioManagementStandaloneApp().app_contract()


def standalone_smoke_test() -> dict:
    app = ProjectPortfolioManagementStandaloneApp()
    demo = app.run_demo()
    runtime = project_portfolio_management_runtime_smoke()
    contract = single_pbc_app_contract()
    return {
        "ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(PROJECT_PORTFOLIO_MANAGEMENT_EMITTED_EVENT_TYPES),
        "demo": demo,
        "runtime": runtime,
        "contract": contract,
        "side_effects": (),
    }
