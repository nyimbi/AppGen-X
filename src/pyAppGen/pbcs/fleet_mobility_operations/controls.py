"""Continuous controls for fleet mobility operations."""
from __future__ import annotations
PBC_KEY = "fleet_mobility_operations"
CONTROLS = (
    {"key": "dispatch_readiness_control", "asserts": "vehicle has registration, fuel/SOC, fresh telematics, no open maintenance or safety blockers", "blocks": ("route_assignment","dispatch")},
    {"key": "driver_rest_overlap_control", "asserts": "driver assignments do not overlap and satisfy rest windows", "blocks": ("assignment_approval",)},
    {"key": "credential_expiry_control", "asserts": "license, endorsements, medical, and training evidence are current", "blocks": ("driver_handoff","assignment_approval")},
    {"key": "telematics_quarantine_control", "asserts": "device messages are known, sane, ordered, and idempotent", "blocks": ("projection_update",)},
    {"key": "route_eta_drift_control", "asserts": "material ETA drift emits route reprojection and exception evidence", "blocks": ("silent_delay",)},
    {"key": "maintenance_horizon_control", "asserts": "near-due services and parts/bay constraints block risky dispatch", "blocks": ("dispatch","long_route_assignment")},
    {"key": "fuel_fraud_control", "asserts": "fuel transactions reconcile to odometer, geofence, card, and idle patterns", "blocks": ("fuel_expense_close",)},
    {"key": "ev_energy_fit_control", "asserts": "state of charge and charger window fit route energy demand", "blocks": ("ev_dispatch",)},
    {"key": "incident_lifecycle_control", "asserts": "breakdown, crash, and compliance incidents move through opened, contained, reassigned, closed", "blocks": ("incident_close","readiness_restore")},
    {"key": "agent_preview_control", "asserts": "assistant replans remain preview-only, owned-table scoped, and confirmation gated", "blocks": ("unconfirmed_mutation","foreign_table_access")},
)
def control_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROLS, "side_effects": ()}
def evaluate_control(control_key: str, context: dict | None = None) -> dict:
    context = dict(context or {})
    control = next((c for c in CONTROLS if c["key"] == control_key), None)
    if control is None:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    failures = tuple(item for item in context.get("failures", ()) if item in control["blocks"] or item == control_key)
    return {"ok": not failures, "control": control, "failures": failures, "blocked_actions": control["blocks"] if failures else (), "side_effects": ()}
def smoke_test() -> dict:
    return {"ok": len(CONTROLS) >= 10 and evaluate_control("dispatch_readiness_control")["ok"], "side_effects": ()}
