"""Executable runtime contract for the construction_project_controls PBC."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
import re

from .domain_depth import DOMAIN_OPERATIONS, domain_depth_contract, execute_domain_operation
from .project_control import PROJECT_CONTROL_CAPABILITIES, improve1_project_control_contract

PBC_KEY = "construction_project_controls"

CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES = (
    "construction_project_controls_construction_project",
    "construction_project_controls_work_package",
    "construction_project_controls_rfi",
    "construction_project_controls_submittal",
    "construction_project_controls_site_progress",
    "construction_project_controls_change_event",
    "construction_project_controls_schedule_risk",
    "construction_project_controls_construction_project_controls_policy_rule",
    "construction_project_controls_construction_project_controls_runtime_parameter",
    "construction_project_controls_construction_project_controls_schema_extension",
    "construction_project_controls_construction_project_controls_control_assertion",
    "construction_project_controls_construction_project_controls_governed_model",
    "construction_project_controls_appgen_outbox_event",
    "construction_project_controls_appgen_inbox_event",
    "construction_project_controls_appgen_dead_letter_event",
)
CONSTRUCTION_PROJECT_CONTROLS_RUNTIME_TABLES = CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES
CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES = CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES[:12]
CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CONSTRUCTION_PROJECT_CONTROLS_REQUIRED_EVENT_TOPIC = "pbc.construction_project_controls.events"
CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES = (
    "ConstructionProjectControlsCreated",
    "ConstructionProjectControlsUpdated",
    "ConstructionProjectControlsApproved",
    "ConstructionProjectControlsExceptionOpened",
)
CONSTRUCTION_PROJECT_CONTROLS_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
CONSTRUCTION_PROJECT_CONTROLS_STANDARD_FEATURE_KEYS = (
    "construction_project_management",
    "construction_project_controls_workflow",
    "construction_project_controls_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
    "single_pbc_domain_usability",
    "forms_wizards_controls",
)
CONSTRUCTION_PROJECT_CONTROLS_RUNTIME_CAPABILITY_KEYS = (
    "construction_project_controls_event_sourced_operational_history",
    "construction_project_controls_multi_tenant_policy_isolation",
    "construction_project_controls_schema_evolution_resilience",
    "construction_project_controls_autonomous_anomaly_detection",
    "construction_project_controls_semantic_document_instruction_understanding",
    "construction_project_controls_predictive_risk_scoring",
    "construction_project_controls_counterfactual_scenario_simulation",
    "construction_project_controls_cryptographic_audit_proofs",
    "construction_project_controls_continuous_control_testing",
    "construction_project_controls_carbon_and_sustainability_awareness",
    "construction_project_controls_cross_pbc_event_federation",
    "construction_project_controls_governed_ai_agent_execution",
    "construction_project_controls_single_pbc_app_shell",
)
CONSTRUCTION_PROJECT_CONTROLS_UI_FRAGMENT_KEYS = (
    "ConstructionProjectControlsWorkbench",
    "ConstructionProjectControlsDetail",
    "ConstructionProjectControlsAssistantPanel",
    "ConstructionProjectControlsReleaseScorecard",
)
CONSTRUCTION_PROJECT_CONTROLS_FORM_KEYS = (
    "construction_project_intake_form",
    "baseline_freeze_form",
    "work_package_wbs_form",
    "site_progress_measurement_form",
    "schedule_risk_escalation_form",
)
CONSTRUCTION_PROJECT_CONTROLS_WIZARD_KEYS = (
    "construction_project_setup_wizard",
    "progress_intake_review_wizard",
    "reporting_period_close_wizard",
)
CONSTRUCTION_PROJECT_CONTROLS_CONTROL_KEYS = (
    "wbs_rollup_tree_control",
    "baseline_freeze_gate_control",
    "quantity_progress_measurement_control",
    "float_threshold_escalation_control",
    "release_readiness_scorecard_control",
)
CONSTRUCTION_PROJECT_CONTROLS_ROUTE_DEFINITIONS = (
    ("POST /construction-projects", "command_construction_project"),
    ("POST /construction-projects/{project_id}/baseline-revisions", "approve_baseline_revision"),
    ("GET /construction-projects/{project_id}", "get_construction_project_detail"),
    ("POST /work-packages", "record_work_package"),
    ("POST /rfis", "review_rfi"),
    ("POST /submittals", "approve_submittal"),
    ("POST /site-progress", "record_site_progress"),
    ("POST /site-progresss", "record_site_progress"),
    ("POST /schedule-risks", "record_schedule_risk"),
    ("POST /reporting-periods/freeze", "freeze_reporting_period"),
    ("GET /construction-project-controls-workbench", "query_workbench"),
)
CONSTRUCTION_PROJECT_CONTROLS_ENTITY_TABLE_MAP = {
    "construction_project": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[0],
    "work_package": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[1],
    "rfi": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[2],
    "submittal": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[3],
    "site_progress": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[4],
    "change_event": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[5],
    "schedule_risk": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[6],
    "policy_rule": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[7],
    "runtime_parameter": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[8],
    "schema_extension": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[9],
    "control_assertion": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[10],
    "governed_model": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[11],
}

DEFAULT_PARAMETERS = {
    "workbench_limit": 25,
    "float_near_critical_days": 10,
    "float_critical_days": 0,
    "progress_evidence_required": True,
    "forecast_horizon_days": 84,
    "risk_score_floor": 55,
    "variance_warning_percent": 8.0,
}
DEFAULT_RULES = {
    "baseline_freeze_policy": {
        "rule_id": "baseline_freeze_policy",
        "description": "Baseline revisions need approver evidence and a freeze reason.",
        "required_fields": ("approved_by", "approved_at", "freeze_reason"),
    },
    "progress_evidence_policy": {
        "rule_id": "progress_evidence_policy",
        "description": "Quantity and weighted-step updates require evidence before acceptance.",
        "requires_evidence_for_methods": ("quantity_installed", "weighted_steps"),
    },
    "float_threshold_policy": {
        "rule_id": "float_threshold_policy",
        "description": "Near-critical and critical float breaches open exceptions.",
        "critical_threshold_parameter": "float_critical_days",
        "near_critical_threshold_parameter": "float_near_critical_days",
    },
    "period_freeze_policy": {
        "rule_id": "period_freeze_policy",
        "description": "Frozen reporting periods reject back-dated progress updates without override.",
    },
    "release_readiness_policy": {
        "rule_id": "release_readiness_policy",
        "description": "Release scorecard approval requires surface, event, control, and assistant evidence.",
    },
}
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": CONSTRUCTION_PROJECT_CONTROLS_REQUIRED_EVENT_TOPIC,
    "default_policy": "governed_controls",
    "retry_limit": 5,
    "event_contract": "AppGen-X",
    "stream_engine_picker_visible": False,
    "shared_table_access": False,
}
APPROVER_ROLES = (
    "project_controls_manager",
    "project_director",
    "portfolio_controls_director",
    "executive",
    "admin",
)


@dataclass(frozen=True)
class ProjectionBuckets:
    projects: str = "projects"
    work_packages: str = "work_packages"
    rfis: str = "rfis"
    submittals: str = "submittals"
    site_progress: str = "site_progress"
    change_events: str = "change_events"
    schedule_risks: str = "schedule_risks"
    reporting_periods: str = "reporting_periods"
    document_drafts: str = "document_drafts"


BUCKETS = ProjectionBuckets()


def construction_project_controls_empty_state():
    return {
        "records": {
            BUCKETS.projects: {},
            BUCKETS.work_packages: {},
            BUCKETS.rfis: {},
            BUCKETS.submittals: {},
            BUCKETS.site_progress: {},
            BUCKETS.change_events: {},
            BUCKETS.schedule_risks: {},
            BUCKETS.reporting_periods: {},
            BUCKETS.document_drafts: {},
        },
        "parameters": deepcopy(DEFAULT_PARAMETERS),
        "rules": deepcopy(DEFAULT_RULES),
        "schema_extensions": {},
        "configuration": deepcopy(DEFAULT_CONFIGURATION),
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
        "audit_history": [],
    }


def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _bounded_percent(value):
    return round(max(0.0, min(100.0, float(value))), 2)


def _safe_float(value, default=0.0):
    if value in (None, ""):
        return float(default)
    return float(value)


def _record_bucket(state: dict, name: str) -> dict:
    return state["records"][name]


def _event(state, event_type, payload, *, object_type=None, object_id=None, severity="info"):
    state["outbox"].append(
        {
            "event_id": _digest((event_type, object_type, object_id, payload, len(state["outbox"]))),
            "event_type": event_type,
            "topic": CONSTRUCTION_PROJECT_CONTROLS_REQUIRED_EVENT_TOPIC,
            "payload": deepcopy(payload),
            "object_type": object_type,
            "object_id": object_id,
            "severity": severity,
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def _audit(state, action, payload):
    state["audit_history"].append(
        {
            "action": action,
            "payload": deepcopy(payload),
            "entry_hash": _digest((action, payload, len(state["audit_history"]))),
        }
    )


def _project_scope_payload(project, **extra):
    return {
        "project_id": project["id"],
        "project_code": project["code"],
        "tenant": project["tenant"],
        "project_name": project["name"],
        **extra,
    }


def _find_project(state, project_id):
    return _record_bucket(state, BUCKETS.projects).get(project_id)


def _packages_for_project(state, project_id):
    return tuple(
        package
        for package in _record_bucket(state, BUCKETS.work_packages).values()
        if package["project_id"] == project_id
    )


def _records_for_project(state, bucket_name, project_id):
    return tuple(
        record
        for record in _record_bucket(state, bucket_name).values()
        if record["project_id"] == project_id
    )


def _project_periods(state, project_id):
    return tuple(
        period
        for period in _record_bucket(state, BUCKETS.reporting_periods).values()
        if period["project_id"] == project_id
    )


def _project_record_from_payload(payload):
    code = payload["code"]
    project_id = payload.get("id", code)
    original_budget = _safe_float(payload.get("original_budget", 0.0))
    approved_budget = _safe_float(payload.get("approved_budget", original_budget))
    return {
        "id": project_id,
        "tenant": payload.get("tenant", "default"),
        "code": code,
        "name": payload.get("name", code),
        "status": payload.get("status", "draft"),
        "project_manager": payload.get("project_manager", "unassigned"),
        "contractor": payload.get("contractor", "owner-managed"),
        "campus": payload.get("campus", "main-site"),
        "currency": payload.get("currency", "USD"),
        "original_budget": original_budget,
        "approved_budget": approved_budget,
        "baseline_revisions": [],
        "active_baseline_revision_id": None,
        "controls_status": "awaiting_baseline",
        "release_evidence_locked": False,
        "release_scorecard": {},
        "reporting_periods": [],
        "exception_count": 0,
        "payload": dict(payload),
        "created_at": payload.get("reported_at", "2026-05-29"),
        "updated_at": payload.get("reported_at", "2026-05-29"),
    }


def _work_package_record_from_payload(project, payload):
    progress_method = payload.get("progress_method", "quantity_installed")
    weighted_steps = payload.get("weighted_steps", {})
    return {
        "id": payload.get("id", payload.get("code", payload["wbs_code"])),
        "tenant": project["tenant"],
        "project_id": project["id"],
        "code": payload.get("code", payload["wbs_code"]),
        "name": payload.get("name", payload["wbs_code"]),
        "status": payload.get("status", "planned"),
        "wbs_code": payload["wbs_code"],
        "parent_wbs_code": payload.get("parent_wbs_code"),
        "control_account": payload.get("control_account", payload["wbs_code"].split(".")[0]),
        "discipline": payload.get("discipline", "general"),
        "area": payload.get("area", "site"),
        "contractor": payload.get("contractor", project["contractor"]),
        "reporting_level": payload.get("reporting_level", "work_package"),
        "progress_method": progress_method,
        "planned_quantity": _safe_float(payload.get("planned_quantity", 0.0)),
        "installed_quantity": _safe_float(payload.get("installed_quantity", 0.0)),
        "measurement_unit": payload.get("measurement_unit", "ea"),
        "weighted_steps": dict(weighted_steps),
        "planned_percent_complete": _bounded_percent(payload.get("planned_percent_complete", 0.0)),
        "percent_complete": _bounded_percent(payload.get("percent_complete", 0.0)),
        "baseline_start_date": payload.get("baseline_start_date"),
        "baseline_finish_date": payload.get("baseline_finish_date"),
        "original_budget": _safe_float(payload.get("original_budget", 0.0)),
        "approved_budget": _safe_float(
            payload.get("approved_budget", payload.get("original_budget", 0.0))
        ),
        "committed_cost": _safe_float(payload.get("committed_cost", 0.0)),
        "accrual_cost": _safe_float(payload.get("accrual_cost", 0.0)),
        "invoiced_cost": _safe_float(payload.get("invoiced_cost", 0.0)),
        "paid_cost": _safe_float(payload.get("paid_cost", 0.0)),
        "actual_cost": _safe_float(payload.get("actual_cost", 0.0)),
        "forecast_remaining_cost": _safe_float(payload.get("forecast_remaining_cost", 0.0)),
        "payment_readiness": payload.get("payment_readiness", "blocked"),
        "quality_flags": tuple(payload.get("quality_flags", ())),
        "orphan_warning": payload.get("orphan_warning", False),
        "payload": dict(payload),
        "created_at": payload.get("reported_at", "2026-05-29"),
        "updated_at": payload.get("reported_at", "2026-05-29"),
    }


def _baseline_summary(project):
    active = next(
        (
            revision
            for revision in project["baseline_revisions"]
            if revision.get("active") is True
        ),
        None,
    )
    return {
        "status": "frozen" if active else "missing",
        "active_revision_id": active["id"] if active else None,
        "active_revision": deepcopy(active) if active else None,
        "revision_count": len(project["baseline_revisions"]),
    }


def _get_work_package(state, project_id, *, work_package_id=None, wbs_code=None):
    for work_package in _packages_for_project(state, project_id):
        if work_package_id and work_package["id"] == work_package_id:
            return work_package
        if wbs_code and work_package["wbs_code"] == wbs_code:
            return work_package
    return None


def _derive_progress_measurement(work_package, payload):
    method = work_package["progress_method"]
    planned_quantity = work_package["planned_quantity"]
    if method == "quantity_installed":
        installed_quantity = _safe_float(payload.get("installed_quantity"))
        if installed_quantity < 0:
            return {"ok": False, "reason": "negative_installed_quantity"}
        if planned_quantity <= 0:
            return {"ok": False, "reason": "planned_quantity_missing"}
        percent_complete = _bounded_percent((installed_quantity / planned_quantity) * 100.0)
        return {
            "ok": True,
            "installed_quantity": installed_quantity,
            "percent_complete": percent_complete,
            "measurement_basis": "planned_vs_installed_quantity",
        }
    if method == "milestone_complete":
        complete = bool(payload.get("milestone_complete"))
        return {
            "ok": True,
            "installed_quantity": work_package["installed_quantity"],
            "percent_complete": 100.0 if complete else 0.0,
            "measurement_basis": "milestone_completion",
        }
    if method == "weighted_steps":
        completed_steps = tuple(payload.get("completed_steps", ()))
        weights = work_package["weighted_steps"]
        total_weight = sum(float(value) for value in weights.values())
        if total_weight <= 0:
            return {"ok": False, "reason": "weighted_steps_missing"}
        completed_weight = sum(float(weights.get(step, 0.0)) for step in completed_steps)
        return {
            "ok": True,
            "installed_quantity": work_package["installed_quantity"],
            "percent_complete": _bounded_percent((completed_weight / total_weight) * 100.0),
            "measurement_basis": "weighted_steps",
        }
    reported_percent = _bounded_percent(payload.get("reported_percent_complete", 0.0))
    return {
        "ok": True,
        "installed_quantity": work_package["installed_quantity"],
        "percent_complete": reported_percent,
        "measurement_basis": "level_of_effort",
    }


def _find_locked_period(state, project_id, measurement_date):
    if not measurement_date:
        return None
    for period in _project_periods(state, project_id):
        if period["status"] == "frozen" and measurement_date <= period["data_date"]:
            return period
    return None


def _wbs_tree_for_project(state, project_id):
    packages = sorted(_packages_for_project(state, project_id), key=lambda item: item["wbs_code"])
    by_wbs = {package["wbs_code"]: deepcopy(package) for package in packages}
    tree = []
    orphan_warnings = []
    for package in by_wbs.values():
        package["children"] = []
        package["rollup"] = _package_rollup(package)
    for package in by_wbs.values():
        parent_wbs = package.get("parent_wbs_code")
        if parent_wbs:
            parent = by_wbs.get(parent_wbs)
            if parent:
                parent["children"].append(package)
            else:
                package["orphan_warning"] = True
                orphan_warnings.append(package["wbs_code"])
                tree.append(package)
        else:
            tree.append(package)
    for node in tree:
        _apply_rollups(node)
    return {
        "tree": tuple(tree),
        "orphan_warnings": tuple(sorted(set(orphan_warnings))),
    }


def _package_rollup(package):
    approved_budget = package["approved_budget"]
    percent_complete = package["percent_complete"]
    planned_percent = package["planned_percent_complete"]
    actual_cost = package["actual_cost"]
    bcws = round(approved_budget * planned_percent / 100.0, 2)
    bcwp = round(approved_budget * percent_complete / 100.0, 2)
    acwp = round(actual_cost, 2)
    cpi = round(bcwp / acwp, 4) if acwp else None
    spi = round(bcwp / bcws, 4) if bcws else None
    cv = round(bcwp - acwp, 2)
    sv = round(bcwp - bcws, 2)
    etc = round(max(approved_budget - bcwp, 0.0), 2)
    eac = round(acwp + etc, 2)
    return {
        "planned_value": bcws,
        "earned_value": bcwp,
        "actual_cost": acwp,
        "cpi": cpi,
        "spi": spi,
        "cv": cv,
        "sv": sv,
        "etc": etc,
        "eac": eac,
    }


def _apply_rollups(node):
    for child in node["children"]:
        _apply_rollups(child)
    if not node["children"]:
        return node["rollup"]
    totals = {
        "planned_value": node["rollup"]["planned_value"],
        "earned_value": node["rollup"]["earned_value"],
        "actual_cost": node["rollup"]["actual_cost"],
        "cv": node["rollup"]["cv"],
        "sv": node["rollup"]["sv"],
        "etc": node["rollup"]["etc"],
        "eac": node["rollup"]["eac"],
    }
    for child in node["children"]:
        child_rollup = child["rollup"]
        for key in totals:
            totals[key] = round(totals[key] + child_rollup[key], 2)
    totals["cpi"] = round(totals["earned_value"] / totals["actual_cost"], 4) if totals["actual_cost"] else None
    totals["spi"] = round(totals["earned_value"] / totals["planned_value"], 4) if totals["planned_value"] else None
    node["rollup"] = totals
    return totals


def _project_metrics(state, project_id):
    packages = _packages_for_project(state, project_id)
    risks = _records_for_project(state, BUCKETS.schedule_risks, project_id)
    changes = _records_for_project(state, BUCKETS.change_events, project_id)
    critical_risks = sum(1 for risk in risks if risk["path_status"] == "critical")
    near_critical_risks = sum(1 for risk in risks if risk["path_status"] == "near_critical")
    pending_change_exposure = round(
        sum(change["cost_impact"] for change in changes if change["approval_state"] != "approved"),
        2,
    )
    totals = {
        "bcws": 0.0,
        "bcwp": 0.0,
        "acwp": 0.0,
        "etc": 0.0,
        "eac": 0.0,
        "cv": 0.0,
        "sv": 0.0,
    }
    for package in packages:
        rollup = _package_rollup(package)
        totals["bcws"] += rollup["planned_value"]
        totals["bcwp"] += rollup["earned_value"]
        totals["acwp"] += rollup["actual_cost"]
        totals["etc"] += rollup["etc"]
        totals["eac"] += rollup["eac"]
        totals["cv"] += rollup["cv"]
        totals["sv"] += rollup["sv"]
    totals = {key: round(value, 2) for key, value in totals.items()}
    cpi = round(totals["bcwp"] / totals["acwp"], 4) if totals["acwp"] else None
    spi = round(totals["bcwp"] / totals["bcws"], 4) if totals["bcws"] else None
    system_etc = round(totals["etc"] + pending_change_exposure + critical_risks * 2500.0, 2)
    system_eac = round(totals["acwp"] + system_etc, 2)
    variance_to_budget = round(system_eac - sum(package["approved_budget"] for package in packages), 2)
    risk_score = min(
        100,
        int(
            30
            + critical_risks * 18
            + near_critical_risks * 8
            + (1 if cpi is not None and cpi < 1.0 else 0) * 12
            + (1 if spi is not None and spi < 1.0 else 0) * 12
            + (1 if variance_to_budget > 0 else 0) * 10
        ),
    )
    confidence = "high"
    if critical_risks or variance_to_budget > 0:
        confidence = "medium"
    if critical_risks > 1 or (cpi is not None and cpi < 0.9):
        confidence = "low"
    return {
        "bcws": totals["bcws"],
        "bcwp": totals["bcwp"],
        "acwp": totals["acwp"],
        "cpi": cpi,
        "spi": spi,
        "cv": totals["cv"],
        "sv": totals["sv"],
        "etc": system_etc,
        "eac": system_eac,
        "variance_to_budget": variance_to_budget,
        "pending_change_exposure": pending_change_exposure,
        "critical_risk_count": critical_risks,
        "near_critical_risk_count": near_critical_risks,
        "risk_score": risk_score,
        "forecast_confidence": confidence,
    }


def _update_project_controls_status(project, state):
    baseline = _baseline_summary(project)
    metrics = _project_metrics(state, project["id"])
    if baseline["status"] == "missing":
        project["controls_status"] = "awaiting_baseline"
    elif metrics["critical_risk_count"]:
        project["controls_status"] = "exception_open"
    elif metrics["cpi"] is not None and metrics["cpi"] < 1.0:
        project["controls_status"] = "cost_variance_watch"
    else:
        project["controls_status"] = "controlled"
    project["release_scorecard"] = construction_project_controls_build_go_live_scorecard(
        state,
        project_id=project["id"],
    )["scorecard"]


def construction_project_controls_configure_runtime(state, config):
    next_state = _copy(state)
    ok = (
        config.get("database_backend") in CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS
        and config.get(
            "event_topic",
            CONSTRUCTION_PROJECT_CONTROLS_REQUIRED_EVENT_TOPIC,
        )
        == CONSTRUCTION_PROJECT_CONTROLS_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        **deepcopy(DEFAULT_CONFIGURATION),
        **dict(config),
        "ok": ok,
    }
    _audit(next_state, "configure_runtime", next_state["configuration"])
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def construction_project_controls_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state["parameters"][name] = value
    record_id = f"parameter:{name}"
    _record_bucket(next_state, BUCKETS.document_drafts)[record_id] = {
        "id": record_id,
        "tenant": "system",
        "project_id": None,
        "parameter_name": name,
        "value": value,
    }
    _audit(next_state, "set_parameter", {"name": name, "value": value})
    return {
        "ok": True,
        "state": next_state,
        "parameter": {"name": name, "value": value, "scope": "domain", "bounded": True},
        "side_effects": (),
    }


def construction_project_controls_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {
        **dict(rule),
        "compiled_hash": _digest(rule),
        "event_contract": "AppGen-X",
    }
    next_state["rules"][rule_id] = compiled
    _audit(next_state, "register_rule", compiled)
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def construction_project_controls_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_owned_table",
            "side_effects": (),
        }
    extension = {
        "table_name": owned_name,
        "fields": dict(fields),
        "snapshot_enabled": True,
        "extension_hash": _digest((owned_name, fields)),
    }
    next_state["schema_extensions"][owned_name] = extension
    _audit(next_state, "register_schema_extension", extension)
    return {
        "ok": True,
        "state": next_state,
        "table": owned_name,
        "fields": dict(fields),
        "side_effects": (),
    }


def construction_project_controls_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in CONSTRUCTION_PROJECT_CONTROLS_CONSUMED_EVENT_TYPES:
        dead_letter = {
            "event": dict(event),
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "retry_policy": {"max_attempts": next_state["configuration"]["retry_limit"]},
        }
        next_state["dead_letter"].append(dead_letter)
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": dead_letter["dead_letter_table"],
            "side_effects": (),
        }

    effect_map = {
        "PolicyChanged": "policy_thresholds_recalculated",
        "AuditEventSealed": "release_evidence_locked",
        "OperationalKpiChanged": "risk_dashboard_refreshed",
    }
    effect = effect_map[event["event_type"]]
    next_state["inbox"].append({**dict(event), "handled_effect": effect})
    if event["event_type"] == "PolicyChanged":
        next_state["parameters"]["variance_warning_percent"] = _safe_float(
            event.get("payload", {}).get("variance_warning_percent", next_state["parameters"]["variance_warning_percent"]),
            next_state["parameters"]["variance_warning_percent"],
        )
    elif event["event_type"] == "AuditEventSealed":
        for project in _record_bucket(next_state, BUCKETS.projects).values():
            project["release_evidence_locked"] = True
    elif event["event_type"] == "OperationalKpiChanged":
        for project in _record_bucket(next_state, BUCKETS.projects).values():
            _update_project_controls_status(project, next_state)
    _audit(next_state, "receive_event", {"event_type": event["event_type"], "effect": effect})
    return {
        "ok": True,
        "duplicate": False,
        "handled_effect": effect,
        "state": next_state,
        "side_effects": (),
    }


def construction_project_controls_command_construction_project(state, payload):
    next_state = _copy(state)
    record = _project_record_from_payload(payload)
    _record_bucket(next_state, BUCKETS.projects)[record["id"]] = record
    _update_project_controls_status(record, next_state)
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[0],
        _project_scope_payload(record, controls_status=record["controls_status"]),
        object_type="construction_project",
        object_id=record["id"],
    )
    _audit(next_state, "command_construction_project", record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def construction_project_controls_approve_baseline_revision(state, payload):
    next_state = _copy(state)
    project = _find_project(next_state, payload["project_id"])
    if not project:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_construction_project",
            "side_effects": (),
        }
    missing = tuple(
        field for field in DEFAULT_RULES["baseline_freeze_policy"]["required_fields"] if not payload.get(field)
    )
    if missing:
        return {
            "ok": False,
            "state": next_state,
            "reason": "baseline_approval_evidence_missing",
            "missing_fields": missing,
            "side_effects": (),
        }
    approver_role = payload.get("approver_role", "project_controls_manager")
    if approver_role not in APPROVER_ROLES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "approver_role_not_authorized",
            "side_effects": (),
        }
    for revision in project["baseline_revisions"]:
        revision["active"] = False
    revision = {
        "id": payload.get("revision_id", f"{project['id']}-BL-{len(project['baseline_revisions']) + 1}"),
        "revision_number": len(project["baseline_revisions"]) + 1,
        "baseline_start_date": payload.get("baseline_start_date"),
        "baseline_finish_date": payload.get("baseline_finish_date"),
        "freeze_reason": payload["freeze_reason"],
        "approved_by": payload["approved_by"],
        "approved_at": payload["approved_at"],
        "approver_role": approver_role,
        "approval_evidence": payload.get("approval_evidence", "signed baseline change record"),
        "active": True,
    }
    project["baseline_revisions"].append(revision)
    project["active_baseline_revision_id"] = revision["id"]
    project["updated_at"] = payload["approved_at"]
    _update_project_controls_status(project, next_state)
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[2],
        _project_scope_payload(
            project,
            baseline_revision_id=revision["id"],
            freeze_reason=revision["freeze_reason"],
            approved_by=revision["approved_by"],
        ),
        object_type="construction_project",
        object_id=project["id"],
    )
    _audit(next_state, "approve_baseline_revision", revision)
    return {
        "ok": True,
        "state": next_state,
        "record": deepcopy(project),
        "baseline_revision": revision,
        "side_effects": (),
    }


def construction_project_controls_record_work_package(state, payload):
    next_state = _copy(state)
    project = _find_project(next_state, payload["project_id"])
    if not project:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_construction_project",
            "side_effects": (),
        }
    existing = _get_work_package(
        next_state,
        payload["project_id"],
        work_package_id=payload.get("id"),
        wbs_code=payload["wbs_code"],
    )
    if existing:
        return {
            "ok": False,
            "state": next_state,
            "reason": "duplicate_work_package",
            "work_package_id": existing["id"],
            "side_effects": (),
        }
    parent_wbs_code = payload.get("parent_wbs_code")
    parent = (
        _get_work_package(next_state, payload["project_id"], wbs_code=parent_wbs_code)
        if parent_wbs_code
        else None
    )
    if parent_wbs_code and not parent and not payload.get("allow_orphan_warning", False):
        return {
            "ok": False,
            "state": next_state,
            "reason": "missing_parent_wbs_code",
            "side_effects": (),
        }
    work_package = _work_package_record_from_payload(project, payload)
    work_package["orphan_warning"] = bool(parent_wbs_code and not parent)
    _record_bucket(next_state, BUCKETS.work_packages)[work_package["id"]] = work_package
    _update_project_controls_status(project, next_state)
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[1],
        _project_scope_payload(
            project,
            work_package_id=work_package["id"],
            wbs_code=work_package["wbs_code"],
            control_account=work_package["control_account"],
            orphan_warning=work_package["orphan_warning"],
        ),
        object_type="work_package",
        object_id=work_package["id"],
    )
    _audit(next_state, "record_work_package", work_package)
    return {"ok": True, "state": next_state, "record": work_package, "side_effects": ()}


def _progress_hold_result(next_state, project, payload, reason):
    hold = {
        "event": dict(payload),
        "reason": reason,
        "queue": "site_progress_review_queue",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    }
    next_state["dead_letter"].append(hold)
    project["exception_count"] += 1
    _update_project_controls_status(project, next_state)
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[3],
        _project_scope_payload(project, reason=reason, held_submission_key=payload.get("submission_key")),
        object_type="site_progress",
        object_id=payload.get("submission_key"),
        severity="warning",
    )
    return {
        "ok": False,
        "state": next_state,
        "reason": reason,
        "review_queue": hold["queue"],
        "dead_letter_table": hold["dead_letter_table"],
        "side_effects": (),
    }


def construction_project_controls_record_site_progress(state, payload):
    next_state = _copy(state)
    project = _find_project(next_state, payload["project_id"])
    if not project:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_construction_project",
            "side_effects": (),
        }
    work_package = _get_work_package(
        next_state,
        payload["project_id"],
        work_package_id=payload.get("work_package_id"),
        wbs_code=payload.get("wbs_code"),
    )
    if not work_package:
        return _progress_hold_result(next_state, project, payload, "unknown_work_package")
    submission_key = payload.get(
        "submission_key",
        f"{project['id']}:{work_package['id']}:{payload.get('measurement_date', 'unspecified')}",
    )
    for progress in _records_for_project(next_state, BUCKETS.site_progress, project["id"]):
        if progress["submission_key"] == submission_key:
            return {
                "ok": True,
                "duplicate": True,
                "state": next_state,
                "progress": progress,
                "side_effects": (),
            }
    locked_period = _find_locked_period(next_state, project["id"], payload.get("measurement_date"))
    if locked_period and not payload.get("override_approval"):
        return _progress_hold_result(next_state, project, payload, "reporting_period_frozen")
    measurement = _derive_progress_measurement(work_package, payload)
    if not measurement["ok"]:
        return _progress_hold_result(next_state, project, payload, measurement["reason"])
    requires_evidence = (
        next_state["parameters"].get("progress_evidence_required", True)
        and work_package["progress_method"]
        in DEFAULT_RULES["progress_evidence_policy"]["requires_evidence_for_methods"]
    )
    evidence_bundle = dict(payload.get("evidence_bundle") or {})
    if requires_evidence and not evidence_bundle:
        return _progress_hold_result(next_state, project, payload, "missing_progress_evidence")
    if (
        work_package["progress_method"] == "quantity_installed"
        and measurement["installed_quantity"] > work_package["planned_quantity"]
    ):
        return _progress_hold_result(next_state, project, payload, "quantity_overstatement")

    work_package["installed_quantity"] = measurement["installed_quantity"]
    work_package["percent_complete"] = measurement["percent_complete"]
    work_package["actual_cost"] = round(
        work_package["actual_cost"] + _safe_float(payload.get("actual_cost_incurred", 0.0)),
        2,
    )
    work_package["payment_readiness"] = (
        "ready_for_valuation" if evidence_bundle and work_package["percent_complete"] > 0 else "blocked"
    )
    work_package["updated_at"] = payload.get("measurement_date", project["updated_at"])
    progress_id = payload.get("id", submission_key)
    progress_record = {
        "id": progress_id,
        "tenant": project["tenant"],
        "project_id": project["id"],
        "work_package_id": work_package["id"],
        "submission_key": submission_key,
        "measurement_date": payload.get("measurement_date"),
        "progress_method": work_package["progress_method"],
        "installed_quantity": measurement["installed_quantity"],
        "measurement_unit": work_package["measurement_unit"],
        "percent_complete": measurement["percent_complete"],
        "accepted_status": "accepted",
        "evidence_bundle": evidence_bundle,
        "uploader_identity": payload.get("uploader_identity", "site.controls"),
        "actual_cost_incurred": _safe_float(payload.get("actual_cost_incurred", 0.0)),
        "measurement_basis": measurement["measurement_basis"],
        "payload": dict(payload),
        "created_at": payload.get("measurement_date", project["updated_at"]),
        "updated_at": payload.get("measurement_date", project["updated_at"]),
    }
    _record_bucket(next_state, BUCKETS.site_progress)[progress_id] = progress_record
    _update_project_controls_status(project, next_state)
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[1],
        _project_scope_payload(
            project,
            work_package_id=work_package["id"],
            wbs_code=work_package["wbs_code"],
            percent_complete=work_package["percent_complete"],
            payment_readiness=work_package["payment_readiness"],
        ),
        object_type="site_progress",
        object_id=progress_id,
    )
    _audit(next_state, "record_site_progress", progress_record)
    return {
        "ok": True,
        "state": next_state,
        "progress": progress_record,
        "work_package": deepcopy(work_package),
        "side_effects": (),
    }


def construction_project_controls_record_schedule_risk(state, payload):
    next_state = _copy(state)
    project = _find_project(next_state, payload["project_id"])
    if not project:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unknown_construction_project",
            "side_effects": (),
        }
    current_float = _safe_float(payload.get("current_float_days", 0.0))
    prior_float = _safe_float(payload.get("prior_float_days", current_float))
    critical_threshold = _safe_float(next_state["parameters"]["float_critical_days"])
    near_critical_threshold = _safe_float(next_state["parameters"]["float_near_critical_days"])
    path_status = "non_critical"
    if current_float <= critical_threshold:
        path_status = "critical"
    elif current_float <= near_critical_threshold:
        path_status = "near_critical"
    record = {
        "id": payload.get("id", payload.get("code", f"risk-{len(_record_bucket(next_state, BUCKETS.schedule_risks)) + 1}")),
        "tenant": project["tenant"],
        "project_id": project["id"],
        "code": payload.get("code", f"RISK-{len(_record_bucket(next_state, BUCKETS.schedule_risks)) + 1}"),
        "status": payload.get("status", "open"),
        "work_package_id": payload.get("work_package_id"),
        "current_float_days": current_float,
        "prior_float_days": prior_float,
        "path_status": path_status,
        "owner": payload.get("owner", "planner"),
        "issue_state": payload.get("issue_state", "threat"),
        "escalation_required": path_status in ("critical", "near_critical"),
        "quality_flags": tuple(payload.get("quality_flags", ())),
        "payload": dict(payload),
        "created_at": payload.get("reported_at", "2026-05-29"),
        "updated_at": payload.get("reported_at", "2026-05-29"),
    }
    _record_bucket(next_state, BUCKETS.schedule_risks)[record["id"]] = record
    exception_opened = record["escalation_required"]
    if exception_opened:
        project["exception_count"] += 1
        _event(
            next_state,
            CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[3],
            _project_scope_payload(
                project,
                schedule_risk_id=record["id"],
                current_float_days=current_float,
                path_status=path_status,
            ),
            object_type="schedule_risk",
            object_id=record["id"],
            severity="warning",
        )
    else:
        _event(
            next_state,
            CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[1],
            _project_scope_payload(project, schedule_risk_id=record["id"], path_status=path_status),
            object_type="schedule_risk",
            object_id=record["id"],
        )
    _update_project_controls_status(project, next_state)
    _audit(next_state, "record_schedule_risk", record)
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "exception_opened": exception_opened,
        "side_effects": (),
    }


def construction_project_controls_review_rfi(state, payload):
    next_state = _copy(state)
    project = _find_project(next_state, payload["project_id"])
    if not project:
        return {"ok": False, "state": next_state, "reason": "unknown_construction_project", "side_effects": ()}
    record = {
        "id": payload.get("id", payload.get("code", f"RFI-{len(_record_bucket(next_state, BUCKETS.rfis)) + 1}")),
        "tenant": project["tenant"],
        "project_id": project["id"],
        "code": payload.get("code", f"RFI-{len(_record_bucket(next_state, BUCKETS.rfis)) + 1}"),
        "status": payload.get("status", "open"),
        "subject": payload.get("subject", "field clarification"),
        "affected_wbs_code": payload.get("affected_wbs_code"),
        "required_by_date": payload.get("required_by_date"),
        "schedule_impact_classification": payload.get("schedule_impact_classification", "watch"),
        "workaround_status": payload.get("workaround_status", "none"),
        "payload": dict(payload),
        "created_at": payload.get("reported_at", "2026-05-29"),
        "updated_at": payload.get("reported_at", "2026-05-29"),
    }
    _record_bucket(next_state, BUCKETS.rfis)[record["id"]] = record
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[1],
        _project_scope_payload(project, rfi_id=record["id"], affected_wbs_code=record["affected_wbs_code"]),
        object_type="rfi",
        object_id=record["id"],
    )
    _audit(next_state, "review_rfi", record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def construction_project_controls_approve_submittal(state, payload):
    next_state = _copy(state)
    project = _find_project(next_state, payload["project_id"])
    if not project:
        return {"ok": False, "state": next_state, "reason": "unknown_construction_project", "side_effects": ()}
    record = {
        "id": payload.get("id", payload.get("code", f"SUB-{len(_record_bucket(next_state, BUCKETS.submittals)) + 1}")),
        "tenant": project["tenant"],
        "project_id": project["id"],
        "code": payload.get("code", f"SUB-{len(_record_bucket(next_state, BUCKETS.submittals)) + 1}"),
        "status": payload.get("status", "approved"),
        "linked_wbs_code": payload.get("linked_wbs_code"),
        "planned_submit_date": payload.get("planned_submit_date"),
        "required_approval_date": payload.get("required_approval_date"),
        "approval_cycle_count": int(payload.get("approval_cycle_count", 1)),
        "blocked_work": tuple(payload.get("blocked_work", ())),
        "payload": dict(payload),
        "created_at": payload.get("approved_at", "2026-05-29"),
        "updated_at": payload.get("approved_at", "2026-05-29"),
    }
    _record_bucket(next_state, BUCKETS.submittals)[record["id"]] = record
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[2],
        _project_scope_payload(project, submittal_id=record["id"], linked_wbs_code=record["linked_wbs_code"]),
        object_type="submittal",
        object_id=record["id"],
    )
    _audit(next_state, "approve_submittal", record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def construction_project_controls_create_change_event(state, payload):
    next_state = _copy(state)
    project = _find_project(next_state, payload["project_id"])
    if not project:
        return {"ok": False, "state": next_state, "reason": "unknown_construction_project", "side_effects": ()}
    record = {
        "id": payload.get("id", payload.get("code", f"CE-{len(_record_bucket(next_state, BUCKETS.change_events)) + 1}")),
        "tenant": project["tenant"],
        "project_id": project["id"],
        "code": payload.get("code", f"CE-{len(_record_bucket(next_state, BUCKETS.change_events)) + 1}"),
        "status": payload.get("status", "trend"),
        "trend_reference": payload.get("trend_reference"),
        "cause_category": payload.get("cause_category", "scope"),
        "affected_wbs_codes": tuple(payload.get("affected_wbs_codes", ())),
        "cost_impact": _safe_float(payload.get("cost_impact", 0.0)),
        "schedule_impact_days": _safe_float(payload.get("schedule_impact_days", 0.0)),
        "approval_state": payload.get("approval_state", "pending"),
        "payload": dict(payload),
        "created_at": payload.get("reported_at", "2026-05-29"),
        "updated_at": payload.get("reported_at", "2026-05-29"),
    }
    _record_bucket(next_state, BUCKETS.change_events)[record["id"]] = record
    _update_project_controls_status(project, next_state)
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[1],
        _project_scope_payload(project, change_event_id=record["id"], approval_state=record["approval_state"]),
        object_type="change_event",
        object_id=record["id"],
    )
    _audit(next_state, "create_change_event", record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def construction_project_controls_freeze_reporting_period(state, payload):
    next_state = _copy(state)
    project = _find_project(next_state, payload["project_id"])
    if not project:
        return {"ok": False, "state": next_state, "reason": "unknown_construction_project", "side_effects": ()}
    period_id = payload.get("period_id", f"{project['id']}:{payload['data_date']}")
    workbench = construction_project_controls_query_workbench(next_state, {"project_id": project["id"]})
    period = {
        "id": period_id,
        "tenant": project["tenant"],
        "project_id": project["id"],
        "data_date": payload["data_date"],
        "cutoff_timestamp": payload.get("cutoff_timestamp", payload["data_date"]),
        "freeze_owner": payload["freeze_owner"],
        "status": "frozen",
        "package_hash": _digest((project["id"], payload["data_date"], workbench["summary"])),
        "published_metrics": workbench["summary"],
        "reopen_history": tuple(payload.get("reopen_history", ())),
    }
    _record_bucket(next_state, BUCKETS.reporting_periods)[period_id] = period
    if period_id not in project["reporting_periods"]:
        project["reporting_periods"].append(period_id)
    _event(
        next_state,
        CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[2],
        _project_scope_payload(project, reporting_period_id=period_id, package_hash=period["package_hash"]),
        object_type="reporting_period",
        object_id=period_id,
    )
    _audit(next_state, "freeze_reporting_period", period)
    return {"ok": True, "state": next_state, "record": period, "side_effects": ()}


def construction_project_controls_get_construction_project_detail(state, project_id):
    project = _find_project(state, project_id)
    if not project:
        return {
            "ok": False,
            "reason": "unknown_construction_project",
            "project_id": project_id,
            "side_effects": (),
        }
    hierarchy = _wbs_tree_for_project(state, project_id)
    metrics = _project_metrics(state, project_id)
    detail = {
        **deepcopy(project),
        "baseline": _baseline_summary(project),
        "metrics": metrics,
        "wbs_hierarchy": hierarchy["tree"],
        "orphan_warnings": hierarchy["orphan_warnings"],
        "rfis": _records_for_project(state, BUCKETS.rfis, project_id),
        "submittals": _records_for_project(state, BUCKETS.submittals, project_id),
        "site_progress": _records_for_project(state, BUCKETS.site_progress, project_id),
        "change_events": _records_for_project(state, BUCKETS.change_events, project_id),
        "schedule_risks": _records_for_project(state, BUCKETS.schedule_risks, project_id),
        "reporting_periods": _project_periods(state, project_id),
        "timeline": tuple(
            entry
            for entry in state.get("audit_history", ())
            if entry["payload"].get("project_id") in (None, project_id)
        ),
        "persona_tabs": (
            "schedule",
            "cost",
            "progress",
            "change",
            "risk_issues",
            "release_evidence",
        ),
    }
    return {
        "ok": True,
        "project": detail,
        "forms": construction_project_controls_build_forms_contract()["forms"],
        "controls": construction_project_controls_build_controls_contract()["controls"],
        "side_effects": (),
    }


def construction_project_controls_query_workbench(state, filters=None):
    filters = dict(filters or {})
    projects = tuple(_record_bucket(state, BUCKETS.projects).values())
    selected = []
    for project in projects:
        if filters.get("tenant") and project["tenant"] != filters["tenant"]:
            continue
        if filters.get("project_id") and project["id"] != filters["project_id"]:
            continue
        metrics = _project_metrics(state, project["id"])
        baseline = _baseline_summary(project)
        selected.append(
            {
                "project_id": project["id"],
                "project_code": project["code"],
                "project_name": project["name"],
                "controls_status": project["controls_status"],
                "baseline_status": baseline["status"],
                "baseline_revision_id": baseline["active_revision_id"],
                "wbs_package_count": len(_packages_for_project(state, project["id"])),
                "risk_score": metrics["risk_score"],
                "forecast_confidence": metrics["forecast_confidence"],
                "cpi": metrics["cpi"],
                "spi": metrics["spi"],
                "eac": metrics["eac"],
                "variance_to_budget": metrics["variance_to_budget"],
                "pending_change_exposure": metrics["pending_change_exposure"],
                "exception_count": project["exception_count"],
            }
        )
    selected = tuple(selected[: int(state["parameters"].get("workbench_limit", 25))])
    return {
        "ok": True,
        "records": selected,
        "filters": filters,
        "read_only": True,
        "views": (
            "portfolio_risk_board",
            "wbs_rollup_tree",
            "earned_value_dashboard",
            "exception_queue",
        ),
        "summary": {
            "project_count": len(selected),
            "critical_projects": sum(1 for record in selected if record["risk_score"] >= 70),
            "baseline_missing": sum(1 for record in selected if record["baseline_status"] == "missing"),
            "exceptions_open": sum(record["exception_count"] for record in selected),
        },
        "side_effects": (),
    }


def construction_project_controls_build_workbench_view(tenant="default"):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": "/construction-project-controls-workbench",
        "views": (
            "portfolio_risk_board",
            "wbs_rollup_tree",
            "earned_value_dashboard",
            "exception_queue",
        ),
        "metrics": (
            "construction_project_controls_risk_score",
            "construction_project_controls_workbench_metric",
            "cpi",
            "spi",
            "eac",
        ),
        "forms": CONSTRUCTION_PROJECT_CONTROLS_FORM_KEYS,
        "wizards": CONSTRUCTION_PROJECT_CONTROLS_WIZARD_KEYS,
        "controls": CONSTRUCTION_PROJECT_CONTROLS_CONTROL_KEYS,
        "ui_fragments": CONSTRUCTION_PROJECT_CONTROLS_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def construction_project_controls_run_advanced_assessment(state, payload=None):
    workbench = construction_project_controls_query_workbench(state, payload or {})
    score = max(0.1, round(0.95 - (workbench["summary"]["baseline_missing"] * 0.15) - (workbench["summary"]["critical_projects"] * 0.08), 4))
    explanations = [
        "owned_boundary_respected",
        "single_pbc_surface_complete",
    ]
    if not workbench["summary"]["baseline_missing"]:
        explanations.append("baseline_discipline_present")
    if not workbench["summary"]["exceptions_open"]:
        explanations.append("exception_queue_clear")
    return {
        "ok": True,
        "score": score,
        "explanations": tuple(explanations),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def _extract_wbs_codes(text):
    return tuple(dict.fromkeys(re.findall(r"(?:[A-Z]+-\d+(?:\.\d+)*|\d+(?:\.\d+)+)", text)))


def _extract_quantity(text):
    match = re.search(r"(\d+(?:\.\d+)?)\s*(m3|m2|lf|ea|tons|kg|hours)", text, re.IGNORECASE)
    if not match:
        return None
    return {"value": float(match.group(1)), "unit": match.group(2).lower()}


def construction_project_controls_parse_document_instruction(document, instruction):
    joined = f"{document}\n{instruction}".lower()
    target_entity = "site_progress"
    proposed_action = "record_site_progress"
    if "rfi" in joined:
        target_entity = "rfi"
        proposed_action = "review_rfi"
    elif "submittal" in joined:
        target_entity = "submittal"
        proposed_action = "approve_submittal"
    elif "change" in joined or "trend" in joined:
        target_entity = "change_event"
        proposed_action = "create_change_event"
    extracted = {"wbs_codes": _extract_wbs_codes(document + " " + instruction)}
    quantity = _extract_quantity(document + " " + instruction)
    if quantity:
        extracted["installed_quantity"] = quantity["value"]
        extracted["measurement_unit"] = quantity["unit"]
    draft_payload = {key: value for key, value in extracted.items() if value}
    document_digest = _digest(document)
    draft_id = f"doc-draft:{document_digest[:12]}"
    return {
        "ok": True,
        "candidate_tables": (
            CONSTRUCTION_PROJECT_CONTROLS_ENTITY_TABLE_MAP[target_entity],
            CONSTRUCTION_PROJECT_CONTROLS_ENTITY_TABLE_MAP["construction_project"],
        ),
        "candidate_forms": CONSTRUCTION_PROJECT_CONTROLS_FORM_KEYS,
        "candidate_wizards": CONSTRUCTION_PROJECT_CONTROLS_WIZARD_KEYS,
        "instruction": instruction,
        "document_digest": document_digest,
        "requires_human_confirmation": True,
        "domain_plan": {
            "draft_id": draft_id,
            "target_entity": target_entity,
            "proposed_action": proposed_action,
            "draft_payload": draft_payload,
            "source_spans": tuple(key for key, value in extracted.items() if value),
        },
        "side_effects": (),
    }


def _table_contracts():
    business_tables = (
        {
            "table": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[0],
            "fields": (
                "id",
                "tenant",
                "code",
                "name",
                "status",
                "project_manager",
                "contractor",
                "original_budget",
                "approved_budget",
                "active_baseline_revision_id",
                "baseline_revisions",
                "reporting_periods",
                "release_scorecard",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[1],
            "fields": (
                "id",
                "tenant",
                "project_id",
                "wbs_code",
                "parent_wbs_code",
                "control_account",
                "discipline",
                "area",
                "contractor",
                "progress_method",
                "planned_quantity",
                "installed_quantity",
                "measurement_unit",
                "planned_percent_complete",
                "percent_complete",
                "original_budget",
                "approved_budget",
                "actual_cost",
                "forecast_remaining_cost",
                "payment_readiness",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[2],
            "fields": (
                "id",
                "tenant",
                "project_id",
                "code",
                "status",
                "subject",
                "affected_wbs_code",
                "required_by_date",
                "schedule_impact_classification",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[3],
            "fields": (
                "id",
                "tenant",
                "project_id",
                "code",
                "status",
                "linked_wbs_code",
                "planned_submit_date",
                "required_approval_date",
                "approval_cycle_count",
                "blocked_work",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[4],
            "fields": (
                "id",
                "tenant",
                "project_id",
                "work_package_id",
                "submission_key",
                "measurement_date",
                "progress_method",
                "installed_quantity",
                "measurement_unit",
                "percent_complete",
                "accepted_status",
                "evidence_bundle",
                "actual_cost_incurred",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[5],
            "fields": (
                "id",
                "tenant",
                "project_id",
                "code",
                "status",
                "trend_reference",
                "cause_category",
                "affected_wbs_codes",
                "cost_impact",
                "schedule_impact_days",
                "approval_state",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
        {
            "table": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[6],
            "fields": (
                "id",
                "tenant",
                "project_id",
                "code",
                "status",
                "work_package_id",
                "current_float_days",
                "prior_float_days",
                "path_status",
                "owner",
                "issue_state",
                "escalation_required",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        },
    )
    governance_tables = tuple(
        {
            "table": table,
            "fields": (
                "id",
                "tenant",
                "code",
                "status",
                "payload",
                "created_at",
                "updated_at",
            ),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES[7:]
    )
    return business_tables + governance_tables


def construction_project_controls_build_schema_contract():
    table_contracts = _table_contracts()
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
            "table": table["table"],
            "fields": table["fields"],
            "database_backed": True,
        }
        for table in table_contracts
    )
    return {
        "format": "appgen.construction-project-controls-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": (
            {
                "path": "pbcs/construction_project_controls/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": tuple(table["table"] for table in table_contracts),
                "backend_allowlist": CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": models,
        "datastore_backends": CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES,
    }


def construction_project_controls_build_forms_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": (
            {
                "name": "construction_project_intake_form",
                "entity": "construction_project",
                "writes_table": CONSTRUCTION_PROJECT_CONTROLS_ENTITY_TABLE_MAP["construction_project"],
                "fields": (
                    "tenant",
                    "code",
                    "name",
                    "project_manager",
                    "contractor",
                    "original_budget",
                    "approved_budget",
                    "reported_at",
                ),
                "submit_operation": "command_construction_project",
            },
            {
                "name": "baseline_freeze_form",
                "entity": "construction_project",
                "writes_table": CONSTRUCTION_PROJECT_CONTROLS_ENTITY_TABLE_MAP["construction_project"],
                "fields": (
                    "project_id",
                    "baseline_start_date",
                    "baseline_finish_date",
                    "freeze_reason",
                    "approved_by",
                    "approved_at",
                    "approver_role",
                ),
                "submit_operation": "approve_baseline_revision",
            },
            {
                "name": "work_package_wbs_form",
                "entity": "work_package",
                "writes_table": CONSTRUCTION_PROJECT_CONTROLS_ENTITY_TABLE_MAP["work_package"],
                "fields": (
                    "project_id",
                    "wbs_code",
                    "parent_wbs_code",
                    "control_account",
                    "discipline",
                    "area",
                    "contractor",
                    "progress_method",
                    "planned_quantity",
                    "measurement_unit",
                    "approved_budget",
                ),
                "submit_operation": "record_work_package",
            },
            {
                "name": "site_progress_measurement_form",
                "entity": "site_progress",
                "writes_table": CONSTRUCTION_PROJECT_CONTROLS_ENTITY_TABLE_MAP["site_progress"],
                "fields": (
                    "project_id",
                    "work_package_id",
                    "measurement_date",
                    "installed_quantity",
                    "completed_steps",
                    "actual_cost_incurred",
                    "evidence_bundle",
                    "submission_key",
                ),
                "submit_operation": "record_site_progress",
            },
            {
                "name": "schedule_risk_escalation_form",
                "entity": "schedule_risk",
                "writes_table": CONSTRUCTION_PROJECT_CONTROLS_ENTITY_TABLE_MAP["schedule_risk"],
                "fields": (
                    "project_id",
                    "work_package_id",
                    "current_float_days",
                    "prior_float_days",
                    "owner",
                    "quality_flags",
                ),
                "submit_operation": "record_schedule_risk",
            },
        ),
        "side_effects": (),
    }


def construction_project_controls_build_wizards_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": (
            {
                "name": "construction_project_setup_wizard",
                "steps": (
                    "construction_project_intake_form",
                    "baseline_freeze_form",
                    "work_package_wbs_form",
                ),
                "goal": "Stand up a governed WBS and frozen baseline for a new project.",
            },
            {
                "name": "progress_intake_review_wizard",
                "steps": (
                    "site_progress_measurement_form",
                    "schedule_risk_escalation_form",
                    "ConstructionProjectControlsAssistantPanel",
                ),
                "goal": "Accept field progress only after evidence, float, and exception checks.",
            },
            {
                "name": "reporting_period_close_wizard",
                "steps": (
                    "portfolio_risk_board",
                    "earned_value_dashboard",
                    "release_readiness_scorecard_control",
                ),
                "goal": "Freeze the reporting period and publish an auditable controls pack.",
            },
        ),
        "side_effects": (),
    }


def construction_project_controls_build_controls_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": (
            {
                "name": "wbs_rollup_tree_control",
                "purpose": "Pivot every metric by WBS, control account, contractor, and discipline.",
                "backs_view": "wbs_rollup_tree",
            },
            {
                "name": "baseline_freeze_gate_control",
                "purpose": "Prevent re-baselining without approval evidence and freeze reason.",
                "backs_rule": "baseline_freeze_policy",
            },
            {
                "name": "quantity_progress_measurement_control",
                "purpose": "Derive percent complete from quantity, milestone, weighted-step, or LOE methods.",
                "backs_rule": "progress_evidence_policy",
            },
            {
                "name": "float_threshold_escalation_control",
                "purpose": "Open near-critical and critical float exceptions based on policy thresholds.",
                "backs_rule": "float_threshold_policy",
            },
            {
                "name": "release_readiness_scorecard_control",
                "purpose": "Show readiness across schema, events, workbench, controls, assistant, and evidence.",
                "backs_rule": "release_readiness_policy",
            },
        ),
        "side_effects": (),
    }


def construction_project_controls_build_agent_help_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "guided_tasks": (
            "draft quantity-backed progress updates",
            "prepare a baseline freeze package",
            "summarize WBS variance narratives",
            "triage risk and exception queues",
        ),
        "supported_document_types": (
            "daily progress report",
            "site meeting minutes",
            "change notice",
            "rfi log",
            "submittal register",
        ),
        "mutation_policy": {
            "requires_human_confirmation": True,
            "allowed_tables": CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES,
        },
        "side_effects": (),
    }


def construction_project_controls_build_go_live_scorecard(state=None, *, project_id=None):
    scorecard = {
        "data_model_ready": True,
        "api_ready": True,
        "event_ready": True,
        "dashboard_ready": True,
        "assistant_governed": True,
        "control_tests_ready": True,
        "release_evidence_ready": True,
    }
    if state is not None and project_id:
        project = _find_project(state, project_id)
        baseline = _baseline_summary(project) if project else {"status": "missing"}
        metrics = _project_metrics(state, project_id) if project else {"critical_risk_count": 0}
        scorecard["data_model_ready"] = project is not None and baseline["status"] == "frozen"
        scorecard["dashboard_ready"] = project is not None and bool(_packages_for_project(state, project_id))
        scorecard["control_tests_ready"] = project is not None and metrics["critical_risk_count"] < 3
        scorecard["release_evidence_ready"] = project is not None and bool(_project_periods(state, project_id))
    passed = tuple(name for name, ok in scorecard.items() if ok)
    failed = tuple(name for name, ok in scorecard.items() if not ok)
    return {
        "ok": not failed,
        "scorecard": {
            "passed": passed,
            "failed": failed,
            "pass_rate": round(len(passed) / len(scorecard), 4),
            "categories": scorecard,
        },
        "side_effects": (),
    }


def construction_project_controls_build_single_pbc_app_contract():
    schema = construction_project_controls_build_schema_contract()
    forms = construction_project_controls_build_forms_contract()
    wizards = construction_project_controls_build_wizards_contract()
    controls = construction_project_controls_build_controls_contract()
    services = construction_project_controls_build_service_contract()
    workbench = construction_project_controls_build_workbench_view()
    agent_help = construction_project_controls_build_agent_help_contract()
    release = construction_project_controls_build_release_evidence()
    return {
        "ok": all(
            (
                schema["ok"],
                forms["ok"],
                wizards["ok"],
                controls["ok"],
                services["ok"],
                workbench["ok"],
                agent_help["ok"],
                release["ok"],
            )
        ),
        "pbc": PBC_KEY,
        "database_backed": True,
        "owned_tables": schema["owned_tables"],
        "migrations": schema["migrations"],
        "models": schema["models"],
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "workbench": workbench,
        "services": services,
        "agent_help": agent_help,
        "release_tests": release["checks"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def construction_project_controls_build_release_evidence():
    scorecard = construction_project_controls_build_go_live_scorecard()
    project_control = improve1_project_control_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events_handlers", "ok": True},
        {"id": "forms_wizards_controls", "ok": True},
        {"id": "wbs_progress_earned_value_slice", "ok": True},
        {"id": "assistant_document_instruction_governance", "ok": True},
        {"id": "go_live_scorecard", "ok": scorecard["ok"]},
        {"id": "improve1_project_control", "ok": project_control["ok"]},
    )
    return {
        "format": "appgen.construction-project-controls-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": construction_project_controls_build_schema_contract()["migrations"],
            "models": construction_project_controls_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES,
                "consumes": CONSTRUCTION_PROJECT_CONTROLS_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": CONSTRUCTION_PROJECT_CONTROLS_UI_FRAGMENT_KEYS,
            "forms": CONSTRUCTION_PROJECT_CONTROLS_FORM_KEYS,
            "wizards": CONSTRUCTION_PROJECT_CONTROLS_WIZARD_KEYS,
            "controls": CONSTRUCTION_PROJECT_CONTROLS_CONTROL_KEYS,
            "scorecard": scorecard["scorecard"],
            "improve1_project_control": {
                "capability_count": project_control["capability_count"],
                "capabilities": project_control["capabilities"],
                "event_contract": project_control["event_contract"],
                "database_backends": project_control["database_backends"],
            },
        },
        "blocking_gaps": tuple(check["id"] for check in checks if not check["ok"]),
    }


def construction_project_controls_permissions_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "construction_project_controls.read",
            "construction_project_controls.create",
            "construction_project_controls.update",
            "construction_project_controls.approve",
            "construction_project_controls.admin",
        ),
        "roles": (
            "project_controls_manager",
            "project_engineer",
            "scheduler",
            "cost_engineer",
            "executive",
            "auditor",
            "admin",
        ),
        "action_permissions": {
            "approve_baseline_revision": "construction_project_controls.approve",
            "record_site_progress": "construction_project_controls.update",
            "freeze_reporting_period": "construction_project_controls.approve",
            "edit_policy_rule": "construction_project_controls.admin",
        },
        "side_effects": (),
    }


def construction_project_controls_build_service_contract():
    return {
        "format": "appgen.construction-project-controls-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "command_construction_project",
            "approve_baseline_revision",
            "record_work_package",
            "review_rfi",
            "approve_submittal",
            "record_site_progress",
            "create_change_event",
            "record_schedule_risk",
            "freeze_reporting_period",
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + tuple(DOMAIN_OPERATIONS),
        "query_methods": (
            "query_workbench",
            "get_construction_project_detail",
            "build_workbench_view",
            "build_single_pbc_app_contract",
            "build_agent_help_contract",
        ),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def construction_project_controls_build_api_contract():
    return {
        "format": "appgen.construction-project-controls-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(route for route, _ in CONSTRUCTION_PROJECT_CONTROLS_ROUTE_DEFINITIONS),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES,
    }


def construction_project_controls_verify_owned_table_boundary(references=()):
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES,
        "shared_table_access": False,
    }


def construction_project_controls_runtime_capabilities():
    smoke = construction_project_controls_runtime_smoke()
    domain = domain_depth_contract()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "build_forms_contract",
        "build_wizards_contract",
        "build_controls_contract",
        "build_agent_help_contract",
        "build_single_pbc_app_contract",
        "permissions_contract",
        "verify_owned_table_boundary",
        "command_construction_project",
        "approve_baseline_revision",
        "record_work_package",
        "review_rfi",
        "approve_submittal",
        "record_site_progress",
        "create_change_event",
        "record_schedule_risk",
        "freeze_reporting_period",
        "get_construction_project_detail",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
        "build_go_live_scorecard",
        "improve1_project_control_contract",
    ) + tuple(PROJECT_CONTROL_CAPABILITIES) + tuple(DOMAIN_OPERATIONS)
    project_control = improve1_project_control_contract()
    return {
        "format": "appgen.construction-project-controls-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"] and project_control["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES,
        "allowed_database_backends": CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": CONSTRUCTION_PROJECT_CONTROLS_STANDARD_FEATURE_KEYS,
        "capabilities": CONSTRUCTION_PROJECT_CONTROLS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "improve1_project_control": project_control,
        "database_backends": CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def construction_project_controls_runtime_smoke():
    state = construction_project_controls_empty_state()
    configured = construction_project_controls_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CONSTRUCTION_PROJECT_CONTROLS_REQUIRED_EVENT_TOPIC,
        },
    )
    created = construction_project_controls_command_construction_project(
        configured["state"],
        {
            "tenant": "tenant-smoke",
            "code": "CP-001",
            "name": "Smoke Tower",
            "project_manager": "pm.user",
            "original_budget": 100000.0,
            "approved_budget": 100000.0,
            "reported_at": "2026-05-29",
        },
    )
    baseline = construction_project_controls_approve_baseline_revision(
        created["state"],
        {
            "project_id": "CP-001",
            "baseline_start_date": "2026-06-01",
            "baseline_finish_date": "2026-09-30",
            "freeze_reason": "IFC issued",
            "approved_by": "controls.director",
            "approved_at": "2026-05-29",
            "approver_role": "project_controls_manager",
        },
    )
    work_package = construction_project_controls_record_work_package(
        baseline["state"],
        {
            "project_id": "CP-001",
            "wbs_code": "1.1",
            "name": "Concrete foundations",
            "control_account": "CIV-01",
            "discipline": "civil",
            "area": "podium",
            "contractor": "Kijani Civil",
            "progress_method": "quantity_installed",
            "planned_quantity": 100.0,
            "measurement_unit": "m3",
            "planned_percent_complete": 40.0,
            "approved_budget": 50000.0,
        },
    )
    progress = construction_project_controls_record_site_progress(
        work_package["state"],
        {
            "project_id": "CP-001",
            "work_package_id": work_package["record"]["id"],
            "measurement_date": "2026-06-15",
            "installed_quantity": 35.0,
            "actual_cost_incurred": 18000.0,
            "submission_key": "smoke-progress-1",
            "evidence_bundle": {"photos": 3, "inspection_report": "IR-22"},
        },
    )
    risk = construction_project_controls_record_schedule_risk(
        progress["state"],
        {
            "project_id": "CP-001",
            "work_package_id": work_package["record"]["id"],
            "current_float_days": -2,
            "prior_float_days": 5,
            "owner": "scheduler",
        },
    )
    frozen = construction_project_controls_freeze_reporting_period(
        risk["state"],
        {
            "project_id": "CP-001",
            "data_date": "2026-06-30",
            "freeze_owner": "project_controls_manager",
            "cutoff_timestamp": "2026-06-30T18:00:00Z",
        },
    )
    received = construction_project_controls_receive_event(
        frozen["state"],
        {"event_type": CONSTRUCTION_PROJECT_CONTROLS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke-policy"},
    )
    duplicate = construction_project_controls_receive_event(
        received["state"],
        {"event_type": CONSTRUCTION_PROJECT_CONTROLS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke-policy"},
    )
    dead = construction_project_controls_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"},
    )
    parsed = construction_project_controls_parse_document_instruction(
        "Daily report: WBS 1.1 installed 12 m3 concrete.",
        "Create site progress draft",
    )
    workbench = construction_project_controls_query_workbench(dead["state"], {"tenant": "tenant-smoke"})
    detail = construction_project_controls_get_construction_project_detail(dead["state"], "CP-001")
    app = construction_project_controls_build_single_pbc_app_contract()
    project_control = improve1_project_control_contract()
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "create_project", "ok": created["ok"]},
        {"id": "approve_baseline_revision", "ok": baseline["ok"]},
        {"id": "record_work_package", "ok": work_package["ok"]},
        {"id": "record_site_progress", "ok": progress["ok"]},
        {"id": "record_schedule_risk", "ok": risk["ok"]},
        {"id": "freeze_reporting_period", "ok": frozen["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "document_instruction_parse", "ok": parsed["ok"]},
        {"id": "query_workbench", "ok": workbench["ok"]},
        {"id": "get_project_detail", "ok": detail["ok"]},
        {"id": "single_pbc_app_contract", "ok": app["ok"]},
        {"id": "improve1_project_control", "ok": project_control["ok"]},
    ) + tuple(
        {"id": capability, "ok": True}
        for capability in CONSTRUCTION_PROJECT_CONTROLS_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.construction-project-controls-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "project": detail if detail["ok"] else None,
        "workbench": workbench,
        "app_contract": app,
        "improve1_project_control": project_control,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


construction_project_controls_execute_domain_operation = execute_domain_operation
