"""Standalone one-PBC app for the land_real_estate_development package."""

from __future__ import annotations

from copy import deepcopy
import hashlib

from .agent import OWNED_TABLES, chatbot_interface_contract

PBC_KEY = "land_real_estate_development"
APP_PATH_PREFIX = "/app/land-real-estate-development"
OWNED_BUSINESS_TABLES = OWNED_TABLES[:7]

FORM_TABLE_MAP = {
    "land_control_intake_form": OWNED_BUSINESS_TABLES[6],
    "parcel_constraints_form": OWNED_BUSINESS_TABLES[0],
    "zoning_entitlement_form": OWNED_BUSINESS_TABLES[1],
    "feasibility_pro_forma_form": OWNED_BUSINESS_TABLES[3],
    "permit_handoff_form": OWNED_BUSINESS_TABLES[4],
}

ROUTE_DEFINITIONS = (
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/projects",
        "operation": "create_project",
        "owned_table": None,
        "projection": "standalone_project_board",
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/parcels",
        "operation": "register_parcel",
        "owned_table": OWNED_BUSINESS_TABLES[0],
        "projection": None,
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/acquisitions",
        "operation": "record_land_acquisition",
        "owned_table": OWNED_BUSINESS_TABLES[6],
        "projection": None,
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/zoning-cases",
        "operation": "record_zoning_case",
        "owned_table": OWNED_BUSINESS_TABLES[1],
        "projection": None,
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/entitlements",
        "operation": "submit_entitlement",
        "owned_table": OWNED_BUSINESS_TABLES[2],
        "projection": None,
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/permits",
        "operation": "submit_permit_application",
        "owned_table": OWNED_BUSINESS_TABLES[4],
        "projection": None,
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/site-plans",
        "operation": "record_site_plan",
        "owned_table": OWNED_BUSINESS_TABLES[5],
        "projection": None,
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/feasibility-models",
        "operation": "run_feasibility",
        "owned_table": OWNED_BUSINESS_TABLES[3],
        "projection": None,
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/approvals",
        "operation": "record_approval",
        "owned_table": OWNED_BUSINESS_TABLES[5],
        "projection": "approval_register",
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/handoffs/sales",
        "operation": "prepare_sales_handoff",
        "owned_table": OWNED_BUSINESS_TABLES[5],
        "projection": "sales_handoff",
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/handoffs/lease",
        "operation": "prepare_lease_handoff",
        "owned_table": OWNED_BUSINESS_TABLES[5],
        "projection": "lease_handoff",
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/assistant/document-preview",
        "operation": "preview_document_instruction",
        "owned_table": None,
        "projection": "assistant_preview",
    },
    {
        "method": "POST",
        "path": f"{APP_PATH_PREFIX}/assistant/crud-preview",
        "operation": "preview_datastore_crud",
        "owned_table": None,
        "projection": "assistant_preview",
    },
    {
        "method": "GET",
        "path": f"{APP_PATH_PREFIX}/projects/{{project_id}}",
        "operation": "get_project_detail",
        "owned_table": None,
        "projection": "project_detail",
    },
    {
        "method": "GET",
        "path": f"{APP_PATH_PREFIX}/workbench",
        "operation": "build_workbench",
        "owned_table": None,
        "projection": "workbench",
    },
)

CONTROL_KEYS = (
    "land_control_threshold_control",
    "environmental_constraint_control",
    "utility_availability_control",
    "residual_land_value_control",
    "construction_release_control",
    "assistant_mutation_preview_control",
)
WIZARD_KEYS = (
    "land_control_and_diligence_wizard",
    "entitlement_and_permitting_wizard",
    "feasibility_and_ic_wizard",
)
FORM_KEYS = tuple(FORM_TABLE_MAP)
REQUIRED_APPROVAL_TYPES = (
    "acquisition",
    "zoning",
    "entitlement",
    "permit",
    "environmental",
    "utility",
    "site_plan",
)
CONTROLLED_STATUSES = {"controlled", "under_option", "exclusive"}
APPROVED_STATUSES = {"approved", "issued", "recorded", "ready", "complete"}
ZONING_OK_STATUSES = {"approved", "by_right", "complete"}
ENVIRONMENTALLY_CLEAR_STATUSES = {"phase_i_clear", "cleared_with_mitigation", "monitor_only"}
UTILITY_NAMES = ("water", "sewer", "power", "telecom")


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _safe_float(value, default=0.0) -> float:
    if value in (None, ""):
        return float(default)
    return float(value)


def _safe_int(value, default=0) -> int:
    if value in (None, ""):
        return int(default)
    return int(value)


def _bounded_percent(value) -> float:
    return round(max(0.0, min(100.0, _safe_float(value))), 2)


def _normalize_utilities(raw: dict | None) -> dict:
    raw = dict(raw or {})
    normalized = {}
    for name in UTILITY_NAMES:
        utility = dict(raw.get(name, {}))
        available = utility.get("available")
        status = utility.get("status")
        if available is None:
            available = status in {"available", "confirmed", "issued"}
        normalized[name] = {
            "provider": utility.get("provider", f"{name.title()} Utility"),
            "available": bool(available),
            "status": status or ("available" if available else "unconfirmed"),
            "capacity": _safe_float(utility.get("capacity"), 0.0),
        }
    return normalized


def _all_utilities_available(parcel: dict) -> bool:
    return all(parcel["utilities"][name]["available"] for name in UTILITY_NAMES)


def _route_for_table(table: str) -> tuple[str, ...]:
    return tuple(
        f"{route['method']} {route['path']}"
        for route in ROUTE_DEFINITIONS
        if route.get("owned_table") == table
    )


def land_real_estate_development_build_forms_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": (
            {
                "name": "land_control_intake_form",
                "entity": "land_option",
                "writes_table": FORM_TABLE_MAP["land_control_intake_form"],
                "fields": (
                    "project_id",
                    "parcel_id",
                    "agreement_type",
                    "control_status",
                    "purchase_price",
                    "deposit_at_risk",
                    "days_to_expiry",
                    "contingency_clear",
                ),
                "submit_operation": "record_land_acquisition",
            },
            {
                "name": "parcel_constraints_form",
                "entity": "land_parcel",
                "writes_table": FORM_TABLE_MAP["parcel_constraints_form"],
                "fields": (
                    "project_id",
                    "parcel_id",
                    "apn",
                    "acreage",
                    "environmental_status",
                    "wetlands_pct",
                    "floodplain_pct",
                    "easement_burden_pct",
                    "utilities",
                ),
                "submit_operation": "register_parcel",
            },
            {
                "name": "zoning_entitlement_form",
                "entity": "zoning_case",
                "writes_table": FORM_TABLE_MAP["zoning_entitlement_form"],
                "fields": (
                    "project_id",
                    "zoning_case_id",
                    "district",
                    "requested_use",
                    "requested_units",
                    "by_right_units",
                    "discretionary",
                    "hearings_remaining",
                ),
                "submit_operation": "record_zoning_case",
            },
            {
                "name": "feasibility_pro_forma_form",
                "entity": "feasibility_model",
                "writes_table": FORM_TABLE_MAP["feasibility_pro_forma_form"],
                "fields": (
                    "project_id",
                    "feasibility_id",
                    "planned_units",
                    "gross_revenue",
                    "vertical_cost",
                    "infrastructure_cost",
                    "soft_cost",
                    "financing_cost",
                    "contingency",
                    "developer_margin_pct",
                ),
                "submit_operation": "run_feasibility",
            },
            {
                "name": "permit_handoff_form",
                "entity": "permit_application",
                "writes_table": FORM_TABLE_MAP["permit_handoff_form"],
                "fields": (
                    "project_id",
                    "permit_id",
                    "permit_type",
                    "status",
                    "blocking_comments",
                    "will_serve_status",
                    "utility_commitment_expires_in_days",
                ),
                "submit_operation": "submit_permit_application",
            },
        ),
        "side_effects": (),
    }


def land_real_estate_development_build_wizards_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": (
            {
                "name": "land_control_and_diligence_wizard",
                "steps": (
                    "land_control_intake_form",
                    "parcel_constraints_form",
                    "assistant_document_preview",
                ),
                "goal": "Prove site control, parcel quality, easements, and environmental diligence before advancing.",
            },
            {
                "name": "entitlement_and_permitting_wizard",
                "steps": (
                    "zoning_entitlement_form",
                    "permit_handoff_form",
                    "LandRealEstateDevelopmentEntitlementCockpit",
                ),
                "goal": "Sequence zoning, entitlement, utility, and permit readiness through agency approvals.",
            },
            {
                "name": "feasibility_and_ic_wizard",
                "steps": (
                    "feasibility_pro_forma_form",
                    "LandRealEstateDevelopmentFeasibilityCockpit",
                    "LandRealEstateDevelopmentHandoffCockpit",
                ),
                "goal": "Take a site from pro forma and risk controls into construction and sales or lease handoff.",
            },
        ),
        "side_effects": (),
    }


def land_real_estate_development_build_controls_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": (
            {
                "name": "land_control_threshold_control",
                "purpose": "Block advancement until the site clears the governed control threshold and option clocks are visible.",
                "backs_rule": "assemblage_minimum_control_threshold",
            },
            {
                "name": "environmental_constraint_control",
                "purpose": "Hold feasibility or construction readiness when contamination, wetlands, floodplain, or remediation issues remain unresolved.",
                "backs_rule": "environmental_clearance_required",
            },
            {
                "name": "utility_availability_control",
                "purpose": "Require water, sewer, power, telecom, and will-serve evidence before construction release.",
                "backs_rule": "utility_commitment_required",
            },
            {
                "name": "residual_land_value_control",
                "purpose": "Expose residual land value, seller price gap, and pro forma drift before approval.",
                "backs_rule": "supportable_land_value_floor",
            },
            {
                "name": "construction_release_control",
                "purpose": "Gate construction, sales, and lease handoffs on approvals, site plan, and unresolved conditions.",
                "backs_rule": "construction_release_gate",
            },
            {
                "name": "assistant_mutation_preview_control",
                "purpose": "Keep assistant document and CRUD actions in preview mode with owned-table routing only.",
                "backs_rule": "assistant_preview_requires_confirmation",
            },
        ),
        "side_effects": (),
    }


def land_real_estate_development_standalone_workbench_blueprint() -> dict:
    forms = land_real_estate_development_build_forms_contract()
    wizards = land_real_estate_development_build_wizards_contract()
    controls = land_real_estate_development_build_controls_contract()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "route": f"{APP_PATH_PREFIX}/workbench",
        "fragments": (
            "LandRealEstateDevelopmentWorkbench",
            "LandRealEstateDevelopmentParcelCockpit",
            "LandRealEstateDevelopmentEntitlementCockpit",
            "LandRealEstateDevelopmentFeasibilityCockpit",
            "LandRealEstateDevelopmentHandoffCockpit",
            "LandRealEstateDevelopmentAssistantPanel",
        ),
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "cockpit_lanes": (
            "site_control",
            "entitlement_pipeline",
            "feasibility_pro_forma",
            "construction_readiness",
            "sales_lease_handoff",
            "assistant_previews",
        ),
        "side_effects": (),
    }


def land_real_estate_development_render_standalone_workbench(workbench: dict) -> dict:
    projects = tuple(workbench.get("projects", ()))
    at_risk = tuple(project["project_id"] for project in projects if project["risk"]["blockers"])
    return {
        "ok": workbench.get("ok") is True,
        "pbc": PBC_KEY,
        "route": f"{APP_PATH_PREFIX}/workbench",
        "summary_cards": (
            {"name": "projects", "value": workbench.get("project_count", 0)},
            {"name": "parcels", "value": workbench.get("parcel_count", 0)},
            {"name": "construction_ready", "value": workbench.get("construction_ready_count", 0)},
            {"name": "handoff_ready", "value": workbench.get("handoff_ready_count", 0)},
        ),
        "at_risk_projects": at_risk,
        "cockpits": workbench.get("cockpits", {}),
        "side_effects": (),
    }


def _empty_state() -> dict:
    return {
        "projects": {},
        "parcels": {},
        "acquisitions": {},
        "zoning_cases": {},
        "entitlements": {},
        "permits": {},
        "site_plans": {},
        "feasibility_models": {},
        "approvals": {},
        "handoffs": {},
        "assistant_previews": {},
        "outbox": [],
        "audit_history": [],
    }


class LandRealEstateDevelopmentStandaloneStore:
    """In-memory standalone app store for package-local land development flows."""

    def __init__(self, database_path: str = ":memory:") -> None:
        self.database_path = database_path
        self.state = _empty_state()
        self.closed = False

    def close(self) -> None:
        self.closed = True

    def _project(self, project_id: str) -> dict:
        project = self.state["projects"].get(project_id)
        if project is None:
            raise KeyError(project_id)
        return project

    def _records_for_project(self, bucket_name: str, project_id: str) -> tuple[dict, ...]:
        return tuple(
            record
            for record in self.state[bucket_name].values()
            if record.get("project_id") == project_id
        )

    def _emit(self, event_type: str, payload: dict) -> None:
        self.state["outbox"].append(
            {
                "event_id": _digest((event_type, payload, len(self.state["outbox"]))),
                "event_type": event_type,
                "topic": f"pbc.{PBC_KEY}.events",
                "payload": deepcopy(payload),
                "event_contract": "AppGen-X",
            }
        )

    def _audit(self, action: str, payload: dict) -> None:
        self.state["audit_history"].append(
            {
                "action": action,
                "payload": deepcopy(payload),
                "entry_hash": _digest((action, payload, len(self.state["audit_history"]))),
            }
        )

    def create_project(self, payload: dict) -> dict:
        project_id = payload.get("project_id") or payload.get("id") or payload.get("code")
        if not project_id:
            return {"ok": False, "reason": "project_id_required", "side_effects": ()}
        project = {
            "id": project_id,
            "project_id": project_id,
            "tenant": payload.get("tenant", "default"),
            "name": payload.get("name", project_id.replace("-", " ").title()),
            "market_mode": payload.get("market_mode", "for_sale"),
            "asset_strategy": payload.get("asset_strategy", "mixed_use"),
            "seller_price_expectation": _safe_float(payload.get("seller_price_expectation"), 0.0),
            "control_threshold_pct": _bounded_percent(payload.get("control_threshold_pct", 80.0)),
            "target_density_per_net_acre": _safe_float(payload.get("target_density_per_net_acre"), 18.0),
            "status": payload.get("status", "screening"),
        }
        self.state["projects"][project_id] = project
        self._audit("create_project", project)
        self._emit("LandRealEstateDevelopmentCreated", project)
        return {"ok": True, "project": deepcopy(project), "side_effects": ()}

    def register_parcel(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        parcel_id = payload.get("parcel_id") or payload.get("id") or payload.get("apn")
        if not parcel_id:
            return {"ok": False, "reason": "parcel_id_required", "side_effects": ()}
        acreage = _safe_float(payload.get("acreage"), 0.0)
        wetlands_pct = _bounded_percent(payload.get("wetlands_pct", 0.0))
        floodplain_pct = _bounded_percent(payload.get("floodplain_pct", 0.0))
        environmental_constrained_pct = _bounded_percent(
            payload.get("environmental_constrained_pct", wetlands_pct + floodplain_pct)
        )
        easement_burden_pct = _bounded_percent(payload.get("easement_burden_pct", 0.0))
        utilities = _normalize_utilities(payload.get("utilities"))
        net_buildable = round(
            acreage * max(0.0, 1.0 - ((environmental_constrained_pct + easement_burden_pct) / 100.0)),
            3,
        )
        parcel = {
            "id": parcel_id,
            "project_id": project_id,
            "tenant": self.state["projects"][project_id]["tenant"],
            "apn": payload.get("apn", parcel_id),
            "acreage": acreage,
            "gross_acres": acreage,
            "net_buildable_acres": net_buildable,
            "district": payload.get("district", "unzoned"),
            "environmental_status": payload.get("environmental_status", "phase_i_clear"),
            "wetlands_pct": wetlands_pct,
            "floodplain_pct": floodplain_pct,
            "environmental_constrained_pct": environmental_constrained_pct,
            "easement_burden_pct": easement_burden_pct,
            "utilities": utilities,
            "survey_status": payload.get("survey_status", "current"),
        }
        risk_flags = []
        if parcel["environmental_status"] not in ENVIRONMENTALLY_CLEAR_STATUSES:
            risk_flags.append("environmental_clearance_required")
        if not _all_utilities_available(parcel):
            risk_flags.append("utility_gap")
        if easement_burden_pct >= 20.0:
            risk_flags.append("easement_pressure")
        parcel["risk_flags"] = tuple(risk_flags)
        self.state["parcels"][parcel_id] = parcel
        self._audit("register_parcel", parcel)
        self._emit("LandRealEstateDevelopmentUpdated", parcel)
        return {"ok": True, "parcel": deepcopy(parcel), "side_effects": ()}

    def record_land_acquisition(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        parcel_id = payload.get("parcel_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        if parcel_id and parcel_id not in self.state["parcels"]:
            return {"ok": False, "reason": "unknown_parcel", "side_effects": ()}
        acquisition_id = payload.get("acquisition_id") or payload.get("id") or f"{project_id}:{parcel_id or 'site'}"
        acquisition = {
            "id": acquisition_id,
            "project_id": project_id,
            "parcel_id": parcel_id,
            "agreement_type": payload.get("agreement_type", "option"),
            "control_status": payload.get("control_status", "under_option"),
            "purchase_price": _safe_float(payload.get("purchase_price"), 0.0),
            "deposit_at_risk": _safe_float(payload.get("deposit_at_risk"), 0.0),
            "days_to_expiry": _safe_int(payload.get("days_to_expiry"), 0),
            "contingency_clear": bool(payload.get("contingency_clear", False)),
            "notice_window_days": _safe_int(payload.get("notice_window_days"), 5),
        }
        flags = []
        if acquisition["days_to_expiry"] and acquisition["days_to_expiry"] <= 21:
            flags.append("option_expiry_near")
        if not acquisition["contingency_clear"]:
            flags.append("diligence_open")
        if acquisition["control_status"] not in CONTROLLED_STATUSES:
            flags.append("control_unsecured")
        acquisition["risk_flags"] = tuple(flags)
        self.state["acquisitions"][acquisition_id] = acquisition
        self._audit("record_land_acquisition", acquisition)
        self._emit("LandRealEstateDevelopmentUpdated", acquisition)
        if flags:
            self._emit("LandRealEstateDevelopmentExceptionOpened", acquisition)
        return {"ok": True, "acquisition": deepcopy(acquisition), "side_effects": ()}

    def record_zoning_case(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        zoning_case_id = payload.get("zoning_case_id") or payload.get("id") or f"{project_id}:zoning"
        requested_units = _safe_int(payload.get("requested_units"), 0)
        by_right_units = _safe_int(payload.get("by_right_units"), requested_units)
        zoning_case = {
            "id": zoning_case_id,
            "project_id": project_id,
            "district": payload.get("district", "mixed_use"),
            "overlay": payload.get("overlay", ""),
            "requested_use": payload.get("requested_use", "mixed_use"),
            "requested_units": requested_units,
            "by_right_units": by_right_units,
            "discretionary": bool(payload.get("discretionary", requested_units > by_right_units)),
            "hearings_remaining": _safe_int(payload.get("hearings_remaining"), 0),
            "status": payload.get("status", "in_review"),
        }
        zoning_case["risk_flags"] = tuple(
            flag
            for flag, condition in (
                ("discretionary_relief", zoning_case["discretionary"]),
                ("hearing_cycles_open", zoning_case["hearings_remaining"] > 0),
                ("density_reduction", requested_units > by_right_units),
            )
            if condition
        )
        self.state["zoning_cases"][zoning_case_id] = zoning_case
        self._audit("record_zoning_case", zoning_case)
        self._emit("LandRealEstateDevelopmentUpdated", zoning_case)
        return {"ok": True, "zoning_case": deepcopy(zoning_case), "side_effects": ()}

    def submit_entitlement(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        entitlement_id = payload.get("entitlement_id") or payload.get("id") or f"{project_id}:entitlement"
        entitlement = {
            "id": entitlement_id,
            "project_id": project_id,
            "zoning_case_id": payload.get("zoning_case_id"),
            "entitlement_type": payload.get("entitlement_type", "site_plan"),
            "status": payload.get("status", "in_review"),
            "dependencies": tuple(payload.get("dependencies", ())),
            "unresolved_conditions": _safe_int(payload.get("unresolved_conditions"), 0),
            "community_opposition": payload.get("community_opposition", "moderate"),
            "appeal_window_open": bool(payload.get("appeal_window_open", False)),
        }
        self.state["entitlements"][entitlement_id] = entitlement
        self._audit("submit_entitlement", entitlement)
        self._emit("LandRealEstateDevelopmentUpdated", entitlement)
        if entitlement["unresolved_conditions"] > 0 or entitlement["appeal_window_open"]:
            self._emit("LandRealEstateDevelopmentExceptionOpened", entitlement)
        return {"ok": True, "entitlement": deepcopy(entitlement), "side_effects": ()}

    def submit_permit_application(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        permit_id = payload.get("permit_id") or payload.get("id") or f"{project_id}:permit"
        permit = {
            "id": permit_id,
            "project_id": project_id,
            "permit_type": payload.get("permit_type", "grading"),
            "status": payload.get("status", "in_review"),
            "agency": payload.get("agency", "planning_department"),
            "blocking_comments": _safe_int(payload.get("blocking_comments"), 0),
            "resubmittal_required": bool(payload.get("resubmittal_required", False)),
            "will_serve_status": payload.get("will_serve_status", "pending"),
            "utility_commitment_expires_in_days": _safe_int(
                payload.get("utility_commitment_expires_in_days"), 0
            ),
        }
        self.state["permits"][permit_id] = permit
        self._audit("submit_permit_application", permit)
        self._emit("LandRealEstateDevelopmentUpdated", permit)
        if permit["blocking_comments"] > 0 or permit["resubmittal_required"]:
            self._emit("LandRealEstateDevelopmentExceptionOpened", permit)
        return {"ok": True, "permit": deepcopy(permit), "side_effects": ()}

    def record_site_plan(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        site_plan_id = payload.get("site_plan_id") or payload.get("id") or f"{project_id}:site-plan"
        site_plan = {
            "id": site_plan_id,
            "project_id": project_id,
            "approved": bool(payload.get("approved", False)),
            "open_space_pct": _bounded_percent(payload.get("open_space_pct", 0.0)),
            "parking_ratio": _safe_float(payload.get("parking_ratio"), 0.0),
            "dedication_acres": _safe_float(payload.get("dedication_acres"), 0.0),
            "offsite_improvements": tuple(payload.get("offsite_improvements", ())),
            "phase_release": payload.get("phase_release", "phase_1"),
        }
        self.state["site_plans"][site_plan_id] = site_plan
        self._audit("record_site_plan", site_plan)
        self._emit("LandRealEstateDevelopmentUpdated", site_plan)
        return {"ok": True, "site_plan": deepcopy(site_plan), "side_effects": ()}

    def run_feasibility(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        project = self._project(project_id)
        parcels = self._records_for_project("parcels", project_id)
        gross_acres = round(sum(parcel["gross_acres"] for parcel in parcels), 3)
        net_buildable_acres = round(sum(parcel["net_buildable_acres"] for parcel in parcels), 3)
        planned_units = _safe_int(
            payload.get("planned_units"),
            round(net_buildable_acres * project["target_density_per_net_acre"]),
        )
        gross_revenue = _safe_float(
            payload.get("gross_revenue"),
            planned_units * _safe_float(payload.get("average_sales_price"), 0.0),
        )
        vertical_cost = _safe_float(payload.get("vertical_cost"), 0.0)
        infrastructure_cost = _safe_float(payload.get("infrastructure_cost"), 0.0)
        soft_cost = _safe_float(payload.get("soft_cost"), 0.0)
        financing_cost = _safe_float(payload.get("financing_cost"), 0.0)
        contingency = _safe_float(payload.get("contingency"), 0.0)
        developer_margin_pct = _bounded_percent(payload.get("developer_margin_pct", 15.0))
        developer_margin_amount = round(gross_revenue * developer_margin_pct / 100.0, 2)
        supportable_land_value = round(
            gross_revenue
            - vertical_cost
            - infrastructure_cost
            - soft_cost
            - financing_cost
            - contingency
            - developer_margin_amount,
            2,
        )
        seller_gap = round(supportable_land_value - project["seller_price_expectation"], 2)
        environmental_hits = sum(
            1 for parcel in parcels if parcel["environmental_status"] not in ENVIRONMENTALLY_CLEAR_STATUSES
        )
        utility_hits = sum(1 for parcel in parcels if not _all_utilities_available(parcel))
        easement_pressure = sum(1 for parcel in parcels if parcel["easement_burden_pct"] >= 20.0)
        risk_score = round(
            max(
                0.0,
                min(
                    100.0,
                    78.0
                    - environmental_hits * 12.0
                    - utility_hits * 9.0
                    - easement_pressure * 4.0
                    - (8.0 if seller_gap < 0 else 0.0),
                ),
            ),
            2,
        )
        feasibility_id = payload.get("feasibility_id") or payload.get("id") or f"{project_id}:feasibility"
        feasibility = {
            "id": feasibility_id,
            "project_id": project_id,
            "gross_acres": gross_acres,
            "net_buildable_acres": net_buildable_acres,
            "planned_units": planned_units,
            "pro_forma": {
                "gross_revenue": round(gross_revenue, 2),
                "vertical_cost": round(vertical_cost, 2),
                "infrastructure_cost": round(infrastructure_cost, 2),
                "soft_cost": round(soft_cost, 2),
                "financing_cost": round(financing_cost, 2),
                "contingency": round(contingency, 2),
                "developer_margin_amount": developer_margin_amount,
                "supportable_land_value": supportable_land_value,
                "seller_price_expectation": round(project["seller_price_expectation"], 2),
                "seller_gap": seller_gap,
            },
            "risk_score": risk_score,
            "viable": bool(net_buildable_acres > 0 and risk_score >= 55.0 and seller_gap >= 0.0),
            "sensitivity_flags": tuple(
                flag
                for flag, condition in (
                    ("seller_price_above_residual", seller_gap < 0.0),
                    ("environmental_drag", environmental_hits > 0),
                    ("utility_upgrade_risk", utility_hits > 0),
                    ("buildable_area_pressure", easement_pressure > 0),
                )
                if condition
            ),
        }
        self.state["feasibility_models"][feasibility_id] = feasibility
        self._audit("run_feasibility", feasibility)
        self._emit("LandRealEstateDevelopmentUpdated", feasibility)
        if not feasibility["viable"]:
            self._emit("LandRealEstateDevelopmentExceptionOpened", feasibility)
        return {"ok": True, "feasibility": deepcopy(feasibility), "side_effects": ()}

    def record_approval(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        approval_id = payload.get("approval_id") or payload.get("id") or _digest(payload)[:16]
        approval = {
            "id": approval_id,
            "project_id": project_id,
            "approval_type": payload.get("approval_type", "permit"),
            "status": payload.get("status", "approved"),
            "approved_by": payload.get("approved_by", "system"),
            "conditions": tuple(payload.get("conditions", ())),
            "expires_in_days": _safe_int(payload.get("expires_in_days"), 0),
        }
        self.state["approvals"][approval_id] = approval
        self._audit("record_approval", approval)
        event_type = (
            "LandRealEstateDevelopmentApproved"
            if approval["status"] in APPROVED_STATUSES and not approval["conditions"]
            else "LandRealEstateDevelopmentUpdated"
        )
        self._emit(event_type, approval)
        return {"ok": True, "approval": deepcopy(approval), "side_effects": ()}

    def assess_construction_readiness(self, project_id: str) -> dict:
        project = self._project(project_id)
        parcels = self._records_for_project("parcels", project_id)
        acquisitions = self._records_for_project("acquisitions", project_id)
        zoning_cases = self._records_for_project("zoning_cases", project_id)
        entitlements = self._records_for_project("entitlements", project_id)
        permits = self._records_for_project("permits", project_id)
        site_plans = self._records_for_project("site_plans", project_id)
        approvals = self._records_for_project("approvals", project_id)
        total_acres = sum(parcel["gross_acres"] for parcel in parcels)
        controlled_acres = sum(
            self.state["parcels"][acquisition["parcel_id"]]["gross_acres"]
            for acquisition in acquisitions
            if acquisition.get("parcel_id") in self.state["parcels"]
            and acquisition["control_status"] in CONTROLLED_STATUSES
        )
        control_pct = round((controlled_acres / total_acres) * 100.0, 2) if total_acres else 0.0
        approved_types = {
            approval["approval_type"]
            for approval in approvals
            if approval["status"] in APPROVED_STATUSES and not approval["conditions"]
        }
        feasibility_models = self._records_for_project("feasibility_models", project_id)
        latest_feasibility = feasibility_models[-1] if feasibility_models else None
        controls = (
            {
                "name": "land_control_threshold_control",
                "ok": bool(total_acres and control_pct >= project["control_threshold_pct"]),
                "detail": {"controlled_pct": control_pct, "threshold_pct": project["control_threshold_pct"]},
            },
            {
                "name": "environmental_constraint_control",
                "ok": bool(parcels) and all(
                    parcel["environmental_status"] in ENVIRONMENTALLY_CLEAR_STATUSES for parcel in parcels
                ),
                "detail": {"affected_parcels": tuple(parcel["id"] for parcel in parcels if parcel["environmental_status"] not in ENVIRONMENTALLY_CLEAR_STATUSES)},
            },
            {
                "name": "utility_availability_control",
                "ok": bool(parcels) and all(_all_utilities_available(parcel) for parcel in parcels),
                "detail": {"affected_parcels": tuple(parcel["id"] for parcel in parcels if not _all_utilities_available(parcel))},
            },
            {
                "name": "residual_land_value_control",
                "ok": latest_feasibility is not None and latest_feasibility["viable"],
                "detail": deepcopy(latest_feasibility["pro_forma"]) if latest_feasibility else {"seller_gap": None},
            },
            {
                "name": "construction_release_control",
                "ok": bool(zoning_cases)
                and all(case["status"] in ZONING_OK_STATUSES for case in zoning_cases)
                and bool(entitlements)
                and all(
                    item["status"] in APPROVED_STATUSES and item["unresolved_conditions"] == 0
                    for item in entitlements
                )
                and bool(permits)
                and all(
                    permit["status"] in APPROVED_STATUSES
                    and permit["blocking_comments"] == 0
                    and permit["will_serve_status"] in {"confirmed", "issued", "available"}
                    for permit in permits
                )
                and any(plan["approved"] for plan in site_plans)
                and set(REQUIRED_APPROVAL_TYPES).issubset(approved_types),
                "detail": {"approved_types": tuple(sorted(approved_types)), "required_types": REQUIRED_APPROVAL_TYPES},
            },
        )
        blockers = tuple(control["name"] for control in controls if control["ok"] is not True)
        return {
            "ok": True,
            "project_id": project_id,
            "ready": not blockers,
            "control_pct": control_pct,
            "controls": controls,
            "blockers": blockers,
            "side_effects": (),
        }

    def prepare_sales_handoff(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        readiness = self.assess_construction_readiness(project_id)
        release_checks = {
            "map_recorded": bool(payload.get("map_recorded", False)),
            "disclosures_ready": bool(payload.get("disclosures_ready", False)),
            "pricing_basis_locked": bool(payload.get("pricing_basis_locked", False)),
            "hoa_ready": bool(payload.get("hoa_ready", False)),
            "model_approvals_complete": bool(payload.get("model_approvals_complete", False)),
        }
        blockers = tuple(name for name, ok in release_checks.items() if not ok)
        handoff_id = payload.get("handoff_id") or f"{project_id}:sales"
        handoff = {
            "id": handoff_id,
            "project_id": project_id,
            "handoff_type": "sales",
            "status": "ready" if readiness["ready"] and not blockers else "blocked",
            "construction_readiness": readiness,
            "release_checks": release_checks,
            "blockers": readiness["blockers"] + blockers,
        }
        self.state["handoffs"][handoff_id] = handoff
        self._audit("prepare_sales_handoff", handoff)
        self._emit(
            "LandRealEstateDevelopmentApproved"
            if handoff["status"] == "ready"
            else "LandRealEstateDevelopmentExceptionOpened",
            handoff,
        )
        return {"ok": True, "handoff": deepcopy(handoff), "side_effects": ()}

    def prepare_lease_handoff(self, payload: dict) -> dict:
        project_id = payload.get("project_id")
        if not project_id or project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        readiness = self.assess_construction_readiness(project_id)
        release_checks = {
            "tco_received": bool(payload.get("tco_received", False)),
            "common_area_ready": bool(payload.get("common_area_ready", False)),
            "turnover_units_ready": _safe_int(payload.get("turnover_units_ready"), 0) > 0,
            "operating_budget_locked": bool(payload.get("operating_budget_locked", False)),
            "lease_constraints_reviewed": bool(payload.get("lease_constraints_reviewed", False)),
        }
        blockers = tuple(name for name, ok in release_checks.items() if not ok)
        handoff_id = payload.get("handoff_id") or f"{project_id}:lease"
        handoff = {
            "id": handoff_id,
            "project_id": project_id,
            "handoff_type": "lease",
            "status": "ready" if readiness["ready"] and not blockers else "blocked",
            "construction_readiness": readiness,
            "release_checks": release_checks,
            "blockers": readiness["blockers"] + blockers,
        }
        self.state["handoffs"][handoff_id] = handoff
        self._audit("prepare_lease_handoff", handoff)
        self._emit(
            "LandRealEstateDevelopmentApproved"
            if handoff["status"] == "ready"
            else "LandRealEstateDevelopmentExceptionOpened",
            handoff,
        )
        return {"ok": True, "handoff": deepcopy(handoff), "side_effects": ()}

    def preview_document_instruction(self, document: str, instruction: str) -> dict:
        text = f"{document} {instruction}".lower()
        keyword_map = (
            (("parcel", "apn", "survey", "easement", "wetland"), OWNED_BUSINESS_TABLES[0]),
            (("zoning", "district", "hearing"), OWNED_BUSINESS_TABLES[1]),
            (("entitlement", "plat", "approval", "conditional use"), OWNED_BUSINESS_TABLES[2]),
            (("feasibility", "pro forma", "residual", "land value"), OWNED_BUSINESS_TABLES[3]),
            (("permit", "resubmittal", "will-serve"), OWNED_BUSINESS_TABLES[4]),
            (("milestone", "construction", "handoff", "lease", "sales"), OWNED_BUSINESS_TABLES[5]),
            (("option", "purchase agreement", "escrow", "site control"), OWNED_BUSINESS_TABLES[6]),
        )
        candidate_tables = tuple(
            table
            for keywords, table in keyword_map
            if any(keyword in text for keyword in keywords)
        ) or (OWNED_BUSINESS_TABLES[0], OWNED_BUSINESS_TABLES[1], OWNED_BUSINESS_TABLES[3])
        action = "update" if any(word in text for word in ("update", "revise", "amend")) else "create"
        preview = {
            "preview_id": _digest((document, instruction))[:16],
            "document_digest": _digest(document),
            "instruction": instruction,
            "candidate_tables": candidate_tables,
            "wizard_candidates": tuple(
                wizard["name"]
                for wizard in land_real_estate_development_build_wizards_contract()["wizards"]
                if any(
                    keyword in text
                    for keyword in ("parcel", "permit", "entitlement", "feasibility", "handoff")
                )
            ) or WIZARD_KEYS,
            "crud_preview": {
                "operation": action,
                "route_candidates": tuple(_route_for_table(table) for table in candidate_tables),
                "requires_human_confirmation": True,
                "event_contract": "AppGen-X",
            },
        }
        self.state["assistant_previews"][preview["preview_id"]] = preview
        self._audit("preview_document_instruction", preview)
        return {"ok": True, "preview": deepcopy(preview), "side_effects": ()}

    def preview_datastore_crud(self, action: str, table: str | None = None, payload: dict | None = None) -> dict:
        target = table or OWNED_BUSINESS_TABLES[0]
        if target not in OWNED_BUSINESS_TABLES:
            return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
        preview_id = _digest((action, target, payload or {}))[:16]
        preview = {
            "preview_id": preview_id,
            "action": action,
            "table": target,
            "payload": deepcopy(payload or {}),
            "route_candidates": _route_for_table(target),
            "requires_confirmation": action in {"create", "update", "delete"},
            "event_contract": "AppGen-X",
        }
        self.state["assistant_previews"][preview_id] = preview
        self._audit("preview_datastore_crud", preview)
        return {"ok": True, "preview": deepcopy(preview), "side_effects": ()}

    def get_project_detail(self, project_id: str) -> dict:
        if project_id not in self.state["projects"]:
            return {"ok": False, "reason": "unknown_project", "side_effects": ()}
        readiness = self.assess_construction_readiness(project_id)
        handoffs = self._records_for_project("handoffs", project_id)
        return {
            "ok": True,
            "project": deepcopy(self.state["projects"][project_id]),
            "parcels": deepcopy(self._records_for_project("parcels", project_id)),
            "acquisitions": deepcopy(self._records_for_project("acquisitions", project_id)),
            "zoning_cases": deepcopy(self._records_for_project("zoning_cases", project_id)),
            "entitlements": deepcopy(self._records_for_project("entitlements", project_id)),
            "permits": deepcopy(self._records_for_project("permits", project_id)),
            "site_plans": deepcopy(self._records_for_project("site_plans", project_id)),
            "feasibility": deepcopy(self._records_for_project("feasibility_models", project_id)),
            "approvals": deepcopy(self._records_for_project("approvals", project_id)),
            "handoffs": deepcopy(handoffs),
            "construction_readiness": readiness,
            "assistant_preview_count": len(self.state["assistant_previews"]),
            "side_effects": (),
        }

    def build_workbench(self, tenant: str = "default") -> dict:
        projects = []
        for project in self.state["projects"].values():
            if project["tenant"] != tenant:
                continue
            readiness = self.assess_construction_readiness(project["project_id"])
            feasibility_models = self._records_for_project("feasibility_models", project["project_id"])
            latest_feasibility = feasibility_models[-1] if feasibility_models else None
            handoffs = self._records_for_project("handoffs", project["project_id"])
            projects.append(
                {
                    "project_id": project["project_id"],
                    "project_name": project["name"],
                    "control_pct": readiness["control_pct"],
                    "risk": {
                        "score": latest_feasibility["risk_score"] if latest_feasibility else 0.0,
                        "blockers": readiness["blockers"],
                    },
                    "construction_ready": readiness["ready"],
                    "handoff_ready": any(handoff["status"] == "ready" for handoff in handoffs),
                }
            )
        project_count = len(projects)
        parcel_count = sum(1 for parcel in self.state["parcels"].values() if parcel["tenant"] == tenant)
        construction_ready_count = sum(1 for project in projects if project["construction_ready"])
        handoff_ready_count = sum(1 for project in projects if project["handoff_ready"])
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "tenant": tenant,
            "project_count": project_count,
            "parcel_count": parcel_count,
            "construction_ready_count": construction_ready_count,
            "handoff_ready_count": handoff_ready_count,
            "projects": tuple(projects),
            "cockpits": {
                "parcel": {"rows": parcel_count},
                "entitlement": {"open_submittals": sum(1 for row in self.state["entitlements"].values() if row["status"] not in APPROVED_STATUSES)},
                "feasibility": {"latest_models": len(self.state["feasibility_models"])},
                "handoff": {"ready": handoff_ready_count},
                "assistant": {"previews": len(self.state["assistant_previews"])},
            },
            "outbox_count": len(self.state["outbox"]),
            "side_effects": (),
        }


def standalone_model_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "store_class": "LandRealEstateDevelopmentStandaloneStore",
        "database_path_modes": (":memory:", "sqlite-path-like-string"),
        "owned_tables": OWNED_BUSINESS_TABLES,
        "local_projections": (
            "standalone_project_board",
            "project_detail",
            "sales_handoff",
            "lease_handoff",
            "assistant_preview",
        ),
        "side_effects": (),
    }


def standalone_service_operation_contracts() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "LandRealEstateDevelopmentStandaloneService",
        "command_methods": (
            "create_project",
            "register_parcel",
            "record_land_acquisition",
            "record_zoning_case",
            "submit_entitlement",
            "submit_permit_application",
            "record_site_plan",
            "run_feasibility",
            "record_approval",
            "prepare_sales_handoff",
            "prepare_lease_handoff",
            "preview_document_instruction",
            "preview_datastore_crud",
        ),
        "query_methods": ("get_project_detail", "build_workbench"),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def standalone_route_contracts() -> dict:
    contracts = tuple(
        {
            "method": route["method"],
            "path": route["path"],
            "operation": route["operation"],
            "owned_table": route["owned_table"],
            "projection": route["projection"],
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
        }
        for route in ROUTE_DEFINITIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "side_effects": ()}


class LandRealEstateDevelopmentStandaloneService:
    """Service facade over the standalone store."""

    def __init__(self, store: LandRealEstateDevelopmentStandaloneStore | None = None) -> None:
        self.store = store or LandRealEstateDevelopmentStandaloneStore()

    def close(self) -> None:
        self.store.close()

    def create_project(self, payload: dict | None = None) -> dict:
        return self.store.create_project(dict(payload or {}))

    def register_parcel(self, payload: dict | None = None) -> dict:
        return self.store.register_parcel(dict(payload or {}))

    def record_land_acquisition(self, payload: dict | None = None) -> dict:
        return self.store.record_land_acquisition(dict(payload or {}))

    def record_zoning_case(self, payload: dict | None = None) -> dict:
        return self.store.record_zoning_case(dict(payload or {}))

    def submit_entitlement(self, payload: dict | None = None) -> dict:
        return self.store.submit_entitlement(dict(payload or {}))

    def submit_permit_application(self, payload: dict | None = None) -> dict:
        return self.store.submit_permit_application(dict(payload or {}))

    def record_site_plan(self, payload: dict | None = None) -> dict:
        return self.store.record_site_plan(dict(payload or {}))

    def run_feasibility(self, payload: dict | None = None) -> dict:
        return self.store.run_feasibility(dict(payload or {}))

    def record_approval(self, payload: dict | None = None) -> dict:
        return self.store.record_approval(dict(payload or {}))

    def prepare_sales_handoff(self, payload: dict | None = None) -> dict:
        return self.store.prepare_sales_handoff(dict(payload or {}))

    def prepare_lease_handoff(self, payload: dict | None = None) -> dict:
        return self.store.prepare_lease_handoff(dict(payload or {}))

    def preview_document_instruction(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        return self.store.preview_document_instruction(
            payload.get("document", ""),
            payload.get("instruction", ""),
        )

    def preview_datastore_crud(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        return self.store.preview_datastore_crud(
            payload.get("action", "create"),
            payload.get("table"),
            payload.get("payload"),
        )

    def get_project_detail(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        return self.store.get_project_detail(str(payload.get("project_id")))

    def build_workbench(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        return self.store.build_workbench(payload.get("tenant", "default"))


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict | None = None,
    *,
    service: LandRealEstateDevelopmentStandaloneService | None = None,
) -> dict:
    own_service = service or LandRealEstateDevelopmentStandaloneService()
    close_after = service is None
    payload = dict(payload or {})
    try:
        if method == "GET" and path.startswith(f"{APP_PATH_PREFIX}/projects/"):
            payload.setdefault("project_id", path.rsplit("/", 1)[-1])
            result = own_service.get_project_detail(payload)
            operation = "get_project_detail"
        else:
            matches = [
                route
                for route in ROUTE_DEFINITIONS
                if route["method"] == method and route["path"] == path
            ]
            if not matches:
                return {"ok": False, "reason": "route_not_found", "route": f"{method} {path}", "side_effects": ()}
            route = matches[0]
            operation = route["operation"]
            result = getattr(own_service, operation)(payload)
        return {
            "ok": result.get("ok") is True,
            "route": f"{method} {path}",
            "operation": operation,
            "result": result,
            "side_effects": (),
        }
    finally:
        if close_after:
            own_service.close()


def land_real_estate_development_standalone_app_contract() -> dict:
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = land_real_estate_development_standalone_workbench_blueprint()
    assistant = chatbot_interface_contract()
    return {
        "ok": all(item.get("ok") is True for item in (models, services, routes, ui, assistant)),
        "format": "appgen.land-real-estate-development-standalone-app.v1",
        "pbc": PBC_KEY,
        "models": models,
        "services": services,
        "routes": routes,
        "ui": ui,
        "assistant": assistant,
        "side_effects": (),
    }


def land_real_estate_development_bootstrap_standalone_app(
    database_path: str = ":memory:",
) -> dict:
    store = LandRealEstateDevelopmentStandaloneStore(database_path=database_path)
    service = LandRealEstateDevelopmentStandaloneService(store)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "store": store,
        "service": service,
        "contract": land_real_estate_development_standalone_app_contract(),
        "side_effects": (),
    }


def land_real_estate_development_standalone_app_smoke() -> dict:
    bundle = land_real_estate_development_bootstrap_standalone_app()
    service = bundle["service"]
    try:
        create = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/projects",
            {
                "project_id": "oak-meadow",
                "tenant": "tenant-smoke",
                "name": "Oak Meadow",
                "seller_price_expectation": 6000000,
                "control_threshold_pct": 75,
                "target_density_per_net_acre": 22,
            },
            service=service,
        )
        parcel = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/parcels",
            {
                "project_id": "oak-meadow",
                "parcel_id": "parcel-a",
                "apn": "01-001-100",
                "acreage": 22.5,
                "district": "MU-45",
                "environmental_status": "phase_i_clear",
                "wetlands_pct": 4.0,
                "easement_burden_pct": 6.0,
                "utilities": {
                    "water": {"available": True, "capacity": 220},
                    "sewer": {"available": True, "capacity": 210},
                    "power": {"available": True, "capacity": 240},
                    "telecom": {"available": True, "capacity": 180},
                },
            },
            service=service,
        )
        acquisition = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/acquisitions",
            {
                "project_id": "oak-meadow",
                "parcel_id": "parcel-a",
                "agreement_type": "purchase_and_sale",
                "control_status": "controlled",
                "purchase_price": 11000000,
                "deposit_at_risk": 450000,
                "days_to_expiry": 45,
                "contingency_clear": True,
            },
            service=service,
        )
        zoning = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/zoning-cases",
            {
                "project_id": "oak-meadow",
                "zoning_case_id": "zone-1",
                "district": "MU-45",
                "requested_use": "mixed_use_residential",
                "requested_units": 360,
                "by_right_units": 360,
                "status": "approved",
            },
            service=service,
        )
        entitlement = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/entitlements",
            {
                "project_id": "oak-meadow",
                "entitlement_id": "ent-1",
                "zoning_case_id": "zone-1",
                "entitlement_type": "tentative_map",
                "status": "approved",
                "unresolved_conditions": 0,
                "community_opposition": "low",
            },
            service=service,
        )
        permit = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/permits",
            {
                "project_id": "oak-meadow",
                "permit_id": "permit-1",
                "permit_type": "grading",
                "status": "issued",
                "blocking_comments": 0,
                "will_serve_status": "issued",
                "utility_commitment_expires_in_days": 120,
            },
            service=service,
        )
        site_plan = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/site-plans",
            {
                "project_id": "oak-meadow",
                "site_plan_id": "site-1",
                "approved": True,
                "open_space_pct": 18,
                "parking_ratio": 1.8,
                "offsite_improvements": ("frontage_lane", "sewer_stub"),
            },
            service=service,
        )
        feasibility = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/feasibility-models",
            {
                "project_id": "oak-meadow",
                "feasibility_id": "fm-1",
                "planned_units": 360,
                "gross_revenue": 142000000,
                "vertical_cost": 82000000,
                "infrastructure_cost": 12000000,
                "soft_cost": 9500000,
                "financing_cost": 7200000,
                "contingency": 4600000,
                "developer_margin_pct": 14,
            },
            service=service,
        )
        approvals = tuple(
            dispatch_standalone_route(
                "POST",
                f"{APP_PATH_PREFIX}/approvals",
                {
                    "project_id": "oak-meadow",
                    "approval_id": f"approval-{approval_type}",
                    "approval_type": approval_type,
                    "status": "approved",
                    "approved_by": "approver-smoke",
                },
                service=service,
            )
            for approval_type in REQUIRED_APPROVAL_TYPES
        )
        workbench = dispatch_standalone_route(
            "GET",
            f"{APP_PATH_PREFIX}/workbench",
            {"tenant": "tenant-smoke"},
            service=service,
        )
        detail = dispatch_standalone_route(
            "GET",
            f"{APP_PATH_PREFIX}/projects/oak-meadow",
            {},
            service=service,
        )
        rendered = land_real_estate_development_render_standalone_workbench(workbench["result"])
        sales = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/handoffs/sales",
            {
                "project_id": "oak-meadow",
                "map_recorded": True,
                "disclosures_ready": True,
                "pricing_basis_locked": True,
                "hoa_ready": True,
                "model_approvals_complete": True,
            },
            service=service,
        )
        lease = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/handoffs/lease",
            {
                "project_id": "oak-meadow",
                "tco_received": True,
                "common_area_ready": True,
                "turnover_units_ready": 120,
                "operating_budget_locked": True,
                "lease_constraints_reviewed": True,
            },
            service=service,
        )
        document_preview = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/assistant/document-preview",
            {
                "document": "Phase I ESA, tentative map packet, and utility will-serve letters",
                "instruction": "Create parcel and permit updates for Oak Meadow",
            },
            service=service,
        )
        crud_preview = dispatch_standalone_route(
            "POST",
            f"{APP_PATH_PREFIX}/assistant/crud-preview",
            {
                "action": "update",
                "table": OWNED_BUSINESS_TABLES[4],
                "payload": {"project_id": "oak-meadow", "permit_id": "permit-1"},
            },
            service=service,
        )
        return {
            "ok": bundle["contract"]["ok"]
            and create["ok"]
            and parcel["ok"]
            and acquisition["ok"]
            and zoning["ok"]
            and entitlement["ok"]
            and permit["ok"]
            and site_plan["ok"]
            and feasibility["ok"]
            and all(item["ok"] for item in approvals)
            and workbench["ok"]
            and detail["ok"]
            and rendered["ok"]
            and sales["ok"]
            and sales["result"]["handoff"]["status"] == "ready"
            and lease["ok"]
            and lease["result"]["handoff"]["status"] == "ready"
            and document_preview["ok"]
            and crud_preview["ok"],
            "contract": bundle["contract"],
            "workbench": workbench,
            "detail": detail,
            "sales": sales,
            "lease": lease,
            "document_preview": document_preview,
            "crud_preview": crud_preview,
            "side_effects": (),
        }
    finally:
        service.close()
