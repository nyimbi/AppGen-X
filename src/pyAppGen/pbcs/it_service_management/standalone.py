"""Standalone one-PBC application surface for it_service_management."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from .agent import chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from .controls import control_catalog, evaluate_control
from .forms import form_catalog
from .runtime import (
    IT_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    IT_SERVICE_MANAGEMENT_CONSUMED_EVENT_TYPES,
    IT_SERVICE_MANAGEMENT_EMITTED_EVENT_TYPES,
    IT_SERVICE_MANAGEMENT_OWNED_TABLES,
    IT_SERVICE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    it_service_management_build_api_contract,
    it_service_management_build_schema_contract,
    it_service_management_build_service_contract,
    it_service_management_configure_runtime,
    it_service_management_empty_state,
    it_service_management_permissions_contract,
    it_service_management_receive_event,
    it_service_management_register_rule,
    it_service_management_runtime_smoke,
    it_service_management_set_parameter,
)
from .ui import it_service_management_render_workbench, it_service_management_ui_contract
from .wizards import wizard_catalog

PBC_KEY = "it_service_management"


def _digest(value: Any) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


@dataclass
class ItServiceManagementStandaloneApp:
    """Executable ITSM application that can run with this PBC alone."""

    tenant: str = "tenant-itsm-001"
    state: dict = field(default_factory=it_service_management_empty_state)
    incidents: dict[str, dict] = field(default_factory=dict)
    service_requests: dict[str, dict] = field(default_factory=dict)
    changes: dict[str, dict] = field(default_factory=dict)
    problems: dict[str, dict] = field(default_factory=dict)
    configuration_items: dict[str, dict] = field(default_factory=dict)
    sla_clocks: dict[str, dict] = field(default_factory=dict)
    knowledge_articles: dict[str, dict] = field(default_factory=dict)

    def configure(self, database_backend: str = "postgresql") -> dict:
        configured = it_service_management_configure_runtime(
            self.state,
            {"database_backend": database_backend, "event_topic": IT_SERVICE_MANAGEMENT_REQUIRED_EVENT_TOPIC},
        )
        self.state = configured["state"]
        for name, value in (
            ("p1_ack_minutes", 15),
            ("p1_restore_minutes", 240),
            ("catalog_auto_close_hours", 72),
            ("normal_change_min_approvals", 2),
            ("ci_verification_max_days", 90),
            ("recurrence_window_days", 30),
        ):
            result = it_service_management_set_parameter(self.state, name, value)
            self.state = result["state"]
        for rule in (
            {"rule_id": "priority_matrix_required", "scope": "incident", "effect": "derive_priority"},
            {"rule_id": "no_silent_handoff", "scope": "incident", "effect": "require_acceptance"},
            {"rule_id": "backout_required", "scope": "change", "effect": "block_without_backout"},
            {"rule_id": "sod_blocks_access", "scope": "request", "effect": "block_conflict"},
            {"rule_id": "ci_owner_required", "scope": "cmdb", "effect": "block_incomplete_ci"},
        ):
            registered = it_service_management_register_rule(self.state, rule)
            self.state = registered["state"]
        received = it_service_management_receive_event(
            self.state,
            {"event_type": IT_SERVICE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "itsm-policy-001"},
        )
        self.state = received["state"]
        return {"ok": configured["ok"] and received["ok"], "side_effects": ()}

    def derive_priority(self, impact: str, urgency: str, revenue_exposure: float = 0, regulated: bool = False) -> dict:
        ranks = {"low": 1, "medium": 2, "high": 3, "enterprise": 4}
        score = ranks.get(impact, 1) + ranks.get(urgency, 1) + (1 if revenue_exposure >= 100000 else 0) + (1 if regulated else 0)
        priority = "P1" if score >= 7 else "P2" if score >= 5 else "P3" if score >= 3 else "P4"
        return {
            "ok": True,
            "priority": priority,
            "response_minutes": {"P1": 15, "P2": 30, "P3": 240, "P4": 1440}[priority],
            "communication_cadence_minutes": {"P1": 30, "P2": 60, "P3": 240, "P4": 1440}[priority],
            "explanation": (impact, urgency, revenue_exposure, regulated),
            "side_effects": (),
        }

    def open_incident(self, incident_id: str, **payload: Any) -> dict:
        priority = self.derive_priority(
            payload.get("impact", "medium"),
            payload.get("urgency", "medium"),
            payload.get("revenue_exposure", 0),
            payload.get("regulated", False),
        )
        incident = {
            "id": incident_id,
            "tenant": self.tenant,
            "business_service": payload.get("business_service", "digital-workplace"),
            "configuration_item": payload.get("configuration_item"),
            "symptom_signature": payload.get("symptom_signature", "unknown"),
            "priority": priority["priority"],
            "status": "open",
            "major": False,
            "timeline": (("opened", payload.get("actor", "service-desk")),),
            "duplicates": (),
            "evidence_frozen": False,
        }
        self.incidents[incident_id] = incident
        self.start_sla_clock(f"SLA-{incident_id}", incident_id, priority["priority"], "customer_sla")
        return {"ok": True, "incident": incident, "priority": priority, "side_effects": ()}

    def declare_major_incident(self, incident_id: str, commander: str, affected_services: tuple[str, ...], exit_criteria: tuple[str, ...]) -> dict:
        incident = dict(self.incidents[incident_id])
        control = evaluate_control(
            "incident_priority_matrix_control",
            {"impact": "enterprise", "urgency": "high", "affected_services": affected_services, "severity": "major"},
        )
        if not commander or not exit_criteria or not control["ok"]:
            return {"ok": False, "reason": "major_incident_governance_incomplete", "control": control, "side_effects": ()}
        incident.update(
            {
                "major": True,
                "commander": commander,
                "severity": "major",
                "affected_services": affected_services,
                "bridge": f"bridge://{incident_id}",
                "exit_criteria": exit_criteria,
                "timeline": incident["timeline"] + (("major_declared", commander),),
            }
        )
        self.incidents[incident_id] = incident
        return {"ok": True, "incident": incident, "emitted_event": "ItServiceManagementExceptionOpened", "side_effects": ()}

    def correlate_duplicate_incident(self, parent_id: str, child_id: str, preserve_distinct: bool = False) -> dict:
        parent = dict(self.incidents[parent_id])
        child = dict(self.incidents[child_id])
        if preserve_distinct:
            child["related_parent"] = parent_id
            child["merge_status"] = "preserved_distinct"
            self.incidents[child_id] = child
            return {"ok": True, "parent": parent, "child": child, "side_effects": ()}
        parent["duplicates"] = parent.get("duplicates", ()) + (child_id,)
        child["merge_status"] = "rolled_up"
        child["status"] = "child_symptom"
        child["timeline"] = child.get("timeline", ()) + (("rolled_up_to", parent_id),)
        self.incidents[parent_id] = parent
        self.incidents[child_id] = child
        return {"ok": True, "parent": parent, "child": child, "side_effects": ()}

    def freeze_incident_evidence(self, incident_id: str, actor: str) -> dict:
        incident = dict(self.incidents[incident_id])
        incident["evidence_frozen"] = True
        incident["timeline"] = incident["timeline"] + (("evidence_frozen", actor),)
        self.incidents[incident_id] = incident
        return {"ok": True, "incident": incident, "side_effects": ()}

    def start_sla_clock(self, clock_id: str, record_id: str, priority: str, commitment_type: str) -> dict:
        minutes = {"P1": (15, 240, 60, 480), "P2": (30, 480, 120, 960), "P3": (240, 1440, 480, 2880), "P4": (1440, 10080, 2880, 20160)}[priority]
        clock = {
            "id": clock_id,
            "record_id": record_id,
            "commitment_type": commitment_type,
            "acknowledgement_due_minutes": minutes[0],
            "restoration_due_minutes": minutes[1],
            "workaround_due_minutes": minutes[2],
            "resolution_due_minutes": minutes[3],
            "pause_reason": None,
            "breaches": (),
        }
        self.sla_clocks[clock_id] = clock
        return {"ok": True, "sla_clock": clock, "side_effects": ()}

    def pause_sla_clock(self, clock_id: str, reason: str, approved_by: str) -> dict:
        allowed = {"waiting_on_requester", "vendor_pending", "cab_review_pending", "implementation_window", "emergency_freeze_review"}
        clock = dict(self.sla_clocks[clock_id])
        if reason not in allowed or not approved_by:
            return {"ok": False, "reason": "invalid_pause", "side_effects": ()}
        clock["pause_reason"] = reason
        clock["pause_approved_by"] = approved_by
        self.sla_clocks[clock_id] = clock
        return {"ok": True, "sla_clock": clock, "side_effects": ()}

    def create_catalog_request(self, request_id: str, catalog_item: str, requester: str, entitled: bool, tasks: tuple[str, ...]) -> dict:
        request = {
            "id": request_id,
            "catalog_item": catalog_item,
            "requester": requester,
            "entitled": entitled,
            "tasks": tuple({"name": task, "status": "open"} for task in tasks),
            "status": "in_fulfillment" if entitled and tasks else "blocked",
            "confirmation_required": True,
        }
        self.service_requests[request_id] = request
        return {"ok": request["status"] == "in_fulfillment", "request": request, "side_effects": ()}

    def validate_access_request(self, request_id: str, identity: str, target_system: str, access_level: str, manager_approved: bool, owner_approved: bool, sod_conflicts: tuple[str, ...], expiry_date: str | None) -> dict:
        blocked = bool(sod_conflicts) or not manager_approved or not owner_approved or not expiry_date
        request = {
            "id": request_id,
            "identity": identity,
            "target_system": target_system,
            "access_level": access_level,
            "sod_conflicts": sod_conflicts,
            "expiry_date": expiry_date,
            "status": "approved" if not blocked else "blocked",
        }
        self.service_requests[request_id] = request
        return {"ok": not blocked, "request": request, "side_effects": ()}

    def confirm_request_closure(self, request_id: str, confirmed: bool, auto_close_elapsed_hours: int = 0) -> dict:
        request = dict(self.service_requests[request_id])
        request["status"] = "closed" if confirmed or auto_close_elapsed_hours >= 72 else "pending_requester_confirmation"
        self.service_requests[request_id] = request
        return {"ok": request["status"] == "closed", "request": request, "side_effects": ()}

    def register_configuration_item(self, ci_id: str, relationships: tuple[tuple[str, str], ...] = (), **payload: Any) -> dict:
        required = ("technical_owner", "service_owner", "support_group", "criticality")
        missing = tuple(item for item in required if not payload.get(item))
        ci = {
            "id": ci_id,
            "ci_type": payload.get("ci_type", "application"),
            "relationships": relationships,
            "technical_owner": payload.get("technical_owner"),
            "service_owner": payload.get("service_owner"),
            "support_group": payload.get("support_group"),
            "criticality": payload.get("criticality"),
            "last_verified_days_ago": payload.get("last_verified_days_ago", 0),
            "drift_status": "stale" if payload.get("last_verified_days_ago", 0) > 90 else "current",
        }
        self.configuration_items[ci_id] = ci
        return {"ok": not missing and ci["drift_status"] == "current", "configuration_item": ci, "missing": missing, "side_effects": ()}

    def preview_change_impact(self, affected_cis: tuple[str, ...]) -> dict:
        support_groups = []
        dependent_services = []
        for ci_id in affected_cis:
            ci = self.configuration_items[ci_id]
            support_groups.append(ci["support_group"])
            dependent_services.extend(target for relation, target in ci["relationships"] if relation in {"provides", "supports", "depends_on"})
        return {
            "ok": True,
            "affected_cis": affected_cis,
            "dependent_services": tuple(dict.fromkeys(dependent_services)),
            "support_groups_to_notify": tuple(dict.fromkeys(support_groups)),
            "monitoring_signals": ("error_rate", "latency", "availability", "business_transaction_volume"),
            "side_effects": (),
        }

    def submit_change(self, change_id: str, change_class: str, affected_cis: tuple[str, ...], window_allowed: bool, backout_plan: dict, approvals: int = 0, emergency_review_due: bool = False) -> dict:
        impact = self.preview_change_impact(affected_cis)
        risk = len(impact["dependent_services"]) + len(affected_cis) + (2 if change_class == "emergency" else 0)
        complete_backout = all(backout_plan.get(item) for item in ("validation_steps", "success_criteria", "rollback_owner", "backout_triggers"))
        required_approvals = 0 if change_class == "standard" else 1 if change_class == "emergency" else 2
        status = "approved" if window_allowed and complete_backout and approvals >= required_approvals else "blocked"
        change = {
            "id": change_id,
            "change_class": change_class,
            "affected_cis": affected_cis,
            "risk_score": risk,
            "impact_preview": impact,
            "status": status,
            "post_implementation_review_due": emergency_review_due or risk >= 4,
        }
        self.changes[change_id] = change
        return {"ok": status == "approved", "change": change, "side_effects": ()}

    def record_post_implementation_review(self, change_id: str, outcome: str, unexpected_impact: bool, remediation: tuple[str, ...]) -> dict:
        change = dict(self.changes[change_id])
        change["pir"] = {"outcome": outcome, "unexpected_impact": unexpected_impact, "remediation": remediation}
        change["post_implementation_review_due"] = False
        self.changes[change_id] = change
        return {"ok": True, "change": change, "side_effects": ()}

    def create_problem_from_recurrence(self, problem_id: str, symptom_signature: str, rca_template: str) -> dict:
        related = tuple(incident["id"] for incident in self.incidents.values() if incident.get("symptom_signature") == symptom_signature)
        problem = {
            "id": problem_id,
            "linked_incidents": related,
            "rca_template": rca_template,
            "hypotheses": (),
            "validated_causes": (),
            "status": "investigating" if len(related) >= 2 else "candidate",
            "recurrence_score": len(related),
        }
        self.problems[problem_id] = problem
        return {"ok": len(related) >= 2, "problem": problem, "side_effects": ()}

    def publish_known_error(self, article_id: str, problem_id: str, workaround_steps: tuple[str, ...], visibility: str) -> dict:
        problem = dict(self.problems[problem_id])
        if not workaround_steps or visibility not in {"internal", "customer_safe", "both"}:
            return {"ok": False, "reason": "invalid_known_error", "side_effects": ()}
        article = {
            "id": article_id,
            "problem_id": problem_id,
            "workaround_steps": workaround_steps,
            "visibility": visibility,
            "status": "approved",
        }
        problem["known_error_article"] = article_id
        self.problems[problem_id] = problem
        self.knowledge_articles[article_id] = article
        return {"ok": True, "article": article, "problem": problem, "side_effects": ()}

    def assistant_instruction_preview(self, document: str, instruction: str) -> dict:
        plan = document_instruction_plan(document, instruction)
        crud = datastore_crud_plan("update", table="it_service_management_it_incident", payload={"instruction": instruction})
        return {
            "ok": plan["ok"] and crud["ok"],
            "document_plan": plan,
            "crud_preview": crud,
            "requires_confirmation": True,
            "side_effects": (),
        }

    def app_contract(self) -> dict:
        return {
            "format": "appgen.it-service-management.standalone-app.v1",
            "ok": True,
            "pbc": PBC_KEY,
            "owned_tables": IT_SERVICE_MANAGEMENT_OWNED_TABLES,
            "database_backends": IT_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "schema": it_service_management_build_schema_contract(),
            "services": it_service_management_build_service_contract(),
            "routes": it_service_management_build_api_contract(),
            "permissions": it_service_management_permissions_contract(),
            "ui": it_service_management_ui_contract(),
            "workbench": it_service_management_render_workbench(),
            "forms": form_catalog(),
            "wizards": wizard_catalog(),
            "controls": control_catalog(),
            "agent": chatbot_interface_contract(),
            "composed_agent": composed_agent_contribution(),
            "dsl": {"pbc": PBC_KEY, "skills_namespace": f"{PBC_KEY}_skills", "single_pbc_app": True},
            "side_effects": (),
        }

    def run_demo(self) -> dict:
        cfg = self.configure()
        ci_app = self.register_configuration_item(
            "CI-CHECKOUT",
            relationships=(("provides", "checkout"), ("depends_on", "identity")),
            technical_owner="platform-sre",
            service_owner="commerce-owner",
            support_group="sre-primary",
            criticality="tier-0",
        )
        ci_stale = self.register_configuration_item("CI-STALE", technical_owner="ops", service_owner="ops", support_group="ops", criticality="tier-2", last_verified_days_ago=120)
        inc1 = self.open_incident("INC-001", impact="enterprise", urgency="high", revenue_exposure=250000, regulated=True, business_service="checkout", configuration_item="CI-CHECKOUT", symptom_signature="checkout-500")
        inc2 = self.open_incident("INC-002", impact="high", urgency="high", business_service="checkout", configuration_item="CI-CHECKOUT", symptom_signature="checkout-500")
        major = self.declare_major_incident("INC-001", "commander-1", ("checkout", "payment"), ("error_rate_normal", "orders_recovered"))
        duplicate = self.correlate_duplicate_incident("INC-001", "INC-002")
        frozen = self.freeze_incident_evidence("INC-001", "incident-reviewer")
        pause = self.pause_sla_clock("SLA-INC-001", "vendor_pending", "support-manager")
        request = self.create_catalog_request("REQ-001", "laptop_refresh", "user-1", True, ("asset_pick", "ship", "verify"))
        access_block = self.validate_access_request("REQ-SEC", "user-2", "erp", "admin", True, True, ("ap_posting_and_bank_admin",), "2026-06-30")
        closed = self.confirm_request_closure("REQ-001", False, auto_close_elapsed_hours=72)
        change_blocked = self.submit_change("CHG-BAD", "normal", ("CI-CHECKOUT",), True, {"validation_steps": ("smoke",)}, approvals=2)
        change = self.submit_change(
            "CHG-001",
            "normal",
            ("CI-CHECKOUT",),
            True,
            {"validation_steps": ("health",), "success_criteria": "orders stable", "rollback_owner": "sre-primary", "backout_triggers": ("error spike",)},
            approvals=2,
        )
        pir = self.record_post_implementation_review("CHG-001", "successful", False, ())
        problem = self.create_problem_from_recurrence("PRB-001", "checkout-500", "five_whys")
        article = self.publish_known_error("KA-001", "PRB-001", ("route traffic to warm pool",), "both")
        assistant = self.assistant_instruction_preview("incident bridge notes", "update incident with workaround and customer update")
        checks = (
            cfg["ok"], ci_app["ok"], ci_stale["ok"] is False, inc1["ok"], inc2["ok"], major["ok"], duplicate["ok"],
            frozen["ok"], pause["ok"], request["ok"], access_block["ok"] is False, closed["ok"],
            change_blocked["ok"] is False, change["ok"], pir["ok"], problem["ok"], article["ok"], assistant["ok"],
        )
        return {
            "ok": all(checks),
            "major_incident": major,
            "duplicate_rollup": duplicate,
            "stale_ci": ci_stale,
            "blocked_access": access_block,
            "blocked_change": change_blocked,
            "problem": problem,
            "known_error": article,
            "assistant": assistant,
            "app_contract": self.app_contract(),
            "side_effects": (),
        }


def single_pbc_app_contract() -> dict:
    return ItServiceManagementStandaloneApp().app_contract()


def standalone_smoke_test() -> dict:
    app = ItServiceManagementStandaloneApp()
    demo = app.run_demo()
    runtime = it_service_management_runtime_smoke()
    contract = single_pbc_app_contract()
    return {
        "ok": demo["ok"] and runtime["ok"] and contract["ok"] and bool(IT_SERVICE_MANAGEMENT_EMITTED_EVENT_TYPES) and contract["stream_engine_picker_visible"] is False,
        "demo": demo,
        "runtime": runtime,
        "contract": contract,
        "side_effects": (),
    }
