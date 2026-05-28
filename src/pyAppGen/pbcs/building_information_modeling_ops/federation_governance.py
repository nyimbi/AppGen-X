"""Executable BIM federation governance slice for model-version operations."""
from __future__ import annotations

from copy import deepcopy
import hashlib

PBC_KEY = "building_information_modeling_ops"

DISCIPLINES = (
    "architectural",
    "structural",
    "mechanical",
    "electrical",
    "plumbing",
    "fire_protection",
    "civil",
    "interiors",
)
ISSUE_PURPOSES = ("wip", "shared", "construction", "record", "handover")
FEDERATION_ELIGIBLE_PURPOSES = ISSUE_PURPOSES[1:]
APPROVAL_STATES = ("draft", "reviewed", "approved", "rejected")

DOWNSTREAM_ACTIONS = {
    "wip": (),
    "shared": ("review_clash_issue", "create_model_review"),
    "construction": (
        "review_clash_issue",
        "create_model_review",
        "approve_asset_object",
        "simulate_handover_package",
    ),
    "record": (
        "create_model_review",
        "approve_asset_object",
        "simulate_handover_package",
        "record_digital_twin_link",
    ),
    "handover": (
        "approve_asset_object",
        "simulate_handover_package",
        "record_digital_twin_link",
    ),
}

DEFAULT_POLICY = {
    "coordinate_tolerance_mm": 25.0,
    "rotation_tolerance_degrees": 0.5,
    "allowed_federation_issue_purposes": FEDERATION_ELIGIBLE_PURPOSES,
}


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["handled_event_ids"] = set(state.get("handled_event_ids", set()))
    return copied


def _point(payload: dict, key: str) -> dict | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be a mapping with x/y/z")
    normalized = {}
    for axis in ("x", "y", "z"):
        if axis not in value:
            raise ValueError(f"{key}.{axis} is required")
        normalized[axis] = float(value[axis])
    return normalized


def _spatial_coverage(value) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _max_axis_delta(left: dict | None, right: dict | None) -> float | None:
    if left is None or right is None:
        return None
    return max(abs(left[axis] - right[axis]) for axis in ("x", "y", "z"))


def _validation_summary(
    payload: dict,
    project_coordinates: dict,
    policy: dict,
) -> dict:
    tolerance_mm = float(policy["coordinate_tolerance_mm"])
    rotation_tolerance = float(policy["rotation_tolerance_degrees"])
    issues: list[str] = []

    declared_basis = str(payload["coordinate_basis"]).strip().lower()
    if declared_basis != project_coordinates["coordinate_basis"]:
        issues.append("coordinate_basis_mismatch")

    survey_delta = _max_axis_delta(
        _point(payload, "survey_point"),
        project_coordinates["survey_point"],
    )
    if survey_delta is None:
        issues.append("survey_point_missing")
    elif survey_delta > tolerance_mm:
        issues.append("survey_point_out_of_tolerance")

    base_point_delta = _max_axis_delta(
        _point(payload, "project_base_point"),
        project_coordinates["project_base_point"],
    )
    if base_point_delta is None:
        issues.append("project_base_point_missing")
    elif base_point_delta > tolerance_mm:
        issues.append("project_base_point_out_of_tolerance")

    true_north_delta = abs(
        float(payload["true_north_degrees"]) - float(project_coordinates["true_north_degrees"])
    )
    if true_north_delta > rotation_tolerance:
        issues.append("true_north_out_of_tolerance")

    if str(payload["elevation_datum"]).strip().lower() != project_coordinates["elevation_datum"]:
        issues.append("elevation_datum_mismatch")

    unit_scale_delta = abs(float(payload["unit_scale"]) - float(project_coordinates["unit_scale"]))
    if unit_scale_delta > 0:
        issues.append("unit_scale_mismatch")

    return {
        "ok": not issues,
        "issues": tuple(issues),
        "tolerance_mm": tolerance_mm,
        "rotation_tolerance_degrees": rotation_tolerance,
        "project_coordinate_basis": project_coordinates["coordinate_basis"],
        "deviations": {
            "survey_point_mm": survey_delta,
            "project_base_point_mm": base_point_delta,
            "true_north_degrees": round(true_north_delta, 6),
            "unit_scale": round(unit_scale_delta, 6),
        },
    }


def _package_eligibility(package: dict, policy: dict) -> dict:
    allowed_purposes = tuple(policy["allowed_federation_issue_purposes"])
    approved = package["approval_state"] == "approved"
    purpose_allowed = package["issue_purpose"] in allowed_purposes
    coordinates_ok = package["coordinate_validation"]["ok"]
    eligible = approved and purpose_allowed and coordinates_ok
    blockers = []
    if not approved:
        blockers.append("approval_required")
    if not purpose_allowed:
        blockers.append("issue_purpose_not_publishable")
    if not coordinates_ok:
        blockers.extend(package["coordinate_validation"]["issues"])
    return {
        "eligible": eligible,
        "allowed_issue_purposes": allowed_purposes,
        "allowed_downstream_actions": DOWNSTREAM_ACTIONS[package["issue_purpose"]],
        "blockers": tuple(dict.fromkeys(blockers)),
    }


def _calculate_kpis(state: dict) -> dict:
    packages = tuple(state["model_packages"].values())
    federations = tuple(state["federations"].values())
    return {
        "active_federations": sum(1 for item in federations if item["status"] == "active"),
        "approved_model_packages": sum(1 for item in packages if item["approval_state"] == "approved"),
        "blocked_model_packages": sum(
            1 for item in packages if not item["federation_eligibility"]["eligible"]
        ),
        "coordinate_failures": sum(
            1 for item in packages if not item["coordinate_validation"]["ok"]
        ),
        "discipline_coverage": tuple(
            sorted({item["discipline"] for item in packages if item["approval_state"] == "approved"})
        ),
    }


def _rebuild_federations(state: dict) -> dict:
    next_state = _copy(state)
    rebuilt = {}
    for federation_id, federation in sorted(next_state["federations"].items()):
        blockers = []
        contributors = []
        for version_id in federation["version_ids"]:
            package = next_state["model_packages"].get(version_id)
            if package is None:
                blockers.append(f"missing:{version_id}")
                continue
            if not package["federation_eligibility"]["eligible"]:
                blockers.append(f"ineligible:{version_id}")
            contributors.append(
                {
                    "version_id": version_id,
                    "discipline": package["discipline"],
                    "approval_state": package["approval_state"],
                    "checksum": package["checksum"],
                }
            )
        rebuilt[federation_id] = {
            **federation,
            "contributors": tuple(contributors),
            "status": "blocked" if blockers else "active",
            "blocked_version_ids": tuple(sorted(item.split(":", 1)[1] for item in blockers)),
        }
    next_state["federations"] = rebuilt
    next_state["kpis"] = _calculate_kpis(next_state)
    return next_state


def federation_governance_empty_state() -> dict:
    return {
        "project_coordinates": None,
        "policy": dict(DEFAULT_POLICY),
        "model_packages": {},
        "federations": {},
        "release_evidence_seals": {},
        "inbound_traces": [],
        "handled_event_ids": set(),
        "kpis": {
            "active_federations": 0,
            "approved_model_packages": 0,
            "blocked_model_packages": 0,
            "coordinate_failures": 0,
            "discipline_coverage": (),
        },
    }


def configure_project_coordinates(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    required = (
        "coordinate_basis",
        "survey_point",
        "project_base_point",
        "true_north_degrees",
        "elevation_datum",
        "unit_scale",
    )
    missing = tuple(name for name in required if payload.get(name) is None)
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_fields", "missing_fields": missing}

    next_state["project_coordinates"] = {
        "coordinate_basis": str(payload["coordinate_basis"]).strip().lower(),
        "survey_point": _point(payload, "survey_point"),
        "project_base_point": _point(payload, "project_base_point"),
        "true_north_degrees": float(payload["true_north_degrees"]),
        "elevation_datum": str(payload["elevation_datum"]).strip().lower(),
        "unit_scale": float(payload["unit_scale"]),
    }
    next_state["policy"] = {
        "coordinate_tolerance_mm": float(
            payload.get("coordinate_tolerance_mm", DEFAULT_POLICY["coordinate_tolerance_mm"])
        ),
        "rotation_tolerance_degrees": float(
            payload.get(
                "rotation_tolerance_degrees",
                DEFAULT_POLICY["rotation_tolerance_degrees"],
            )
        ),
        "allowed_federation_issue_purposes": tuple(
            payload.get(
                "allowed_federation_issue_purposes",
                DEFAULT_POLICY["allowed_federation_issue_purposes"],
            )
        ),
    }
    next_state = _rebuild_federations(next_state)
    return {
        "ok": True,
        "state": next_state,
        "project_coordinates": dict(next_state["project_coordinates"]),
        "policy": dict(next_state["policy"]),
        "event_type": "BuildingInformationModelingOpsUpdated",
        "event_payload": {
            "action": "project_coordinates_configured",
            "coordinate_basis": next_state["project_coordinates"]["coordinate_basis"],
        },
    }


def register_model_package(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    if next_state["project_coordinates"] is None:
        return {
            "ok": False,
            "state": next_state,
            "reason": "project_coordinates_not_configured",
        }

    required = (
        "version_id",
        "discipline",
        "authoring_party",
        "coordinate_basis",
        "survey_point",
        "project_base_point",
        "true_north_degrees",
        "elevation_datum",
        "unit_scale",
        "issue_purpose",
        "spatial_coverage",
        "lod_target",
        "checksum",
    )
    missing = tuple(name for name in required if payload.get(name) in (None, "", (), []))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_fields", "missing_fields": missing}

    discipline = str(payload["discipline"]).strip().lower()
    if discipline not in DISCIPLINES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unsupported_discipline",
            "discipline": discipline,
        }

    issue_purpose = str(payload["issue_purpose"]).strip().lower()
    if issue_purpose not in ISSUE_PURPOSES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unsupported_issue_purpose",
            "issue_purpose": issue_purpose,
        }

    approval_state = str(payload.get("approval_state", "draft")).strip().lower()
    if approval_state not in APPROVAL_STATES:
        return {
            "ok": False,
            "state": next_state,
            "reason": "unsupported_approval_state",
            "approval_state": approval_state,
        }

    coordinate_validation = _validation_summary(
        payload,
        next_state["project_coordinates"],
        next_state["policy"],
    )
    package = {
        "model_id": str(payload.get("model_id", payload["version_id"])).strip(),
        "version_id": str(payload["version_id"]).strip(),
        "discipline": discipline,
        "authoring_party": str(payload["authoring_party"]).strip(),
        "coordinate_basis": str(payload["coordinate_basis"]).strip().lower(),
        "survey_point": _point(payload, "survey_point"),
        "project_base_point": _point(payload, "project_base_point"),
        "true_north_degrees": float(payload["true_north_degrees"]),
        "elevation_datum": str(payload["elevation_datum"]).strip().lower(),
        "unit_scale": float(payload["unit_scale"]),
        "issue_purpose": issue_purpose,
        "spatial_coverage": _spatial_coverage(payload["spatial_coverage"]),
        "lod_target": str(payload["lod_target"]).strip(),
        "approval_state": approval_state,
        "checksum": str(payload["checksum"]).strip(),
        "coordinate_validation": coordinate_validation,
    }
    package["federation_eligibility"] = _package_eligibility(package, next_state["policy"])
    next_state["model_packages"][package["version_id"]] = package
    next_state = _rebuild_federations(next_state)
    event_type = (
        "BuildingInformationModelingOpsUpdated"
        if payload["version_id"] in state.get("model_packages", {})
        else "BuildingInformationModelingOpsCreated"
    )
    return {
        "ok": True,
        "state": next_state,
        "package": package,
        "event_type": event_type,
        "event_payload": {
            "action": "model_package_registered",
            "version_id": package["version_id"],
            "discipline": package["discipline"],
            "approval_state": package["approval_state"],
            "issue_purpose": package["issue_purpose"],
        },
    }


def assemble_federation(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    federation_id = str(payload.get("federation_id", "")).strip()
    version_ids = tuple(str(item).strip() for item in payload.get("version_ids", ()))
    intended_use = str(payload.get("intended_use", "coordination")).strip().lower()
    if not federation_id or not version_ids:
        return {
            "ok": False,
            "state": next_state,
            "reason": "missing_federation_identity",
        }

    blockers = []
    contributors = []
    coordinate_bases = set()
    elevation_datums = set()
    unit_scales = set()
    discipline_map: dict[str, list[str]] = {}

    if len(set(version_ids)) != len(version_ids):
        blockers.append("duplicate_version_ids")

    for version_id in version_ids:
        package = next_state["model_packages"].get(version_id)
        if package is None:
            blockers.append(f"missing:{version_id}")
            continue
        if not package["federation_eligibility"]["eligible"]:
            blockers.extend(
                f"{version_id}:{reason}"
                for reason in package["federation_eligibility"]["blockers"]
            )
        coordinate_bases.add(package["coordinate_basis"])
        elevation_datums.add(package["elevation_datum"])
        unit_scales.add(package["unit_scale"])
        discipline_map.setdefault(package["discipline"], []).append(version_id)
        contributors.append(
            {
                "version_id": package["version_id"],
                "discipline": package["discipline"],
                "approval_state": package["approval_state"],
                "issue_purpose": package["issue_purpose"],
                "checksum": package["checksum"],
            }
        )

    if len(coordinate_bases) > 1:
        blockers.append("mixed_coordinate_bases")
    if len(elevation_datums) > 1:
        blockers.append("mixed_elevation_datums")
    if len(unit_scales) > 1:
        blockers.append("mixed_unit_scales")

    if blockers:
        return {
            "ok": False,
            "state": next_state,
            "reason": "federation_blocked",
            "blockers": tuple(dict.fromkeys(blockers)),
            "event_type": "BuildingInformationModelingOpsExceptionOpened",
            "event_payload": {
                "action": "federation_assembly_blocked",
                "federation_id": federation_id,
                "version_ids": version_ids,
                "blockers": tuple(dict.fromkeys(blockers)),
            },
        }

    federation = {
        "federation_id": federation_id,
        "intended_use": intended_use,
        "version_ids": version_ids,
        "contributors": tuple(sorted(contributors, key=lambda item: item["version_id"])),
        "discipline_map": tuple(
            (discipline, tuple(sorted(ids)))
            for discipline, ids in sorted(discipline_map.items())
        ),
        "coordinate_basis": next_state["project_coordinates"]["coordinate_basis"],
        "status": "active",
        "blocked_version_ids": (),
        "lineage_hash": _digest((federation_id, version_ids, contributors)),
    }
    next_state["federations"][federation_id] = federation
    next_state = _rebuild_federations(next_state)
    return {
        "ok": True,
        "state": next_state,
        "federation": next_state["federations"][federation_id],
        "event_type": "BuildingInformationModelingOpsApproved",
        "event_payload": {
            "action": "federation_assembled",
            "federation_id": federation_id,
            "version_ids": version_ids,
            "intended_use": intended_use,
        },
    }


def federation_workbench_projection(state: dict) -> dict:
    packages = tuple(sorted(state["model_packages"].values(), key=lambda item: item["version_id"]))
    blocked_packages = tuple(
        {
            "version_id": item["version_id"],
            "discipline": item["discipline"],
            "blockers": item["federation_eligibility"]["blockers"],
        }
        for item in packages
        if not item["federation_eligibility"]["eligible"]
    )
    active_federations = tuple(
        sorted(state["federations"].values(), key=lambda item: item["federation_id"])
    )
    return {
        "ok": True,
        "project_coordinates": deepcopy(state["project_coordinates"]),
        "policy": dict(state["policy"]),
        "kpis": dict(state["kpis"]),
        "active_federations": active_federations,
        "blocked_packages": blocked_packages,
        "discipline_summary": tuple(
            {
                "discipline": discipline,
                "count": sum(1 for item in packages if item["discipline"] == discipline),
                "approved_count": sum(
                    1
                    for item in packages
                    if item["discipline"] == discipline and item["approval_state"] == "approved"
                ),
            }
            for discipline in DISCIPLINES
            if any(item["discipline"] == discipline for item in packages)
        ),
        "inbound_traces": tuple(state["inbound_traces"]),
    }


def build_federation_release_evidence(state: dict, federation_id: str) -> dict:
    federation = state["federations"].get(federation_id)
    if federation is None:
        return {"ok": False, "reason": "unknown_federation", "federation_id": federation_id}
    contributors = tuple(
        {
            "version_id": item["version_id"],
            "discipline": item["discipline"],
            "approval_state": item["approval_state"],
            "checksum": item["checksum"],
        }
        for item in federation["contributors"]
    )
    return {
        "ok": True,
        "federation_id": federation_id,
        "coordinate_basis": federation["coordinate_basis"],
        "contributors": contributors,
        "validation_summary": {
            "all_approved": all(item["approval_state"] == "approved" for item in contributors),
            "package_count": len(contributors),
        },
        "sealed": federation_id in state["release_evidence_seals"],
        "lineage_hash": federation["lineage_hash"],
    }


def apply_inbound_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    handled_id = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if handled_id in next_state["handled_event_ids"]:
        return {
            "ok": True,
            "duplicate": True,
            "state": next_state,
            "trace": {
                "event_type": event.get("event_type"),
                "handled_id": handled_id,
                "result": "duplicate_ignored",
            },
        }

    next_state["handled_event_ids"].add(handled_id)
    payload = dict(event.get("payload") or {})
    event_type = event.get("event_type")

    if event_type == "PolicyChanged":
        next_state["policy"] = {
            **next_state["policy"],
            **{
                key: value
                for key, value in payload.items()
                if key
                in {
                    "coordinate_tolerance_mm",
                    "rotation_tolerance_degrees",
                    "allowed_federation_issue_purposes",
                }
            },
        }
        for version_id, package in list(next_state["model_packages"].items()):
            refreshed = dict(package)
            refreshed["coordinate_validation"] = _validation_summary(
                refreshed,
                next_state["project_coordinates"],
                next_state["policy"],
            )
            refreshed["federation_eligibility"] = _package_eligibility(
                refreshed,
                next_state["policy"],
            )
            next_state["model_packages"][version_id] = refreshed
        next_state = _rebuild_federations(next_state)
        trace = {
            "event_type": event_type,
            "handled_id": handled_id,
            "result": "policy_revalidated",
            "affected_versions": tuple(sorted(next_state["model_packages"])),
        }
    elif event_type == "OperationalKpiChanged":
        next_state["kpis"] = _calculate_kpis(next_state)
        trace = {
            "event_type": event_type,
            "handled_id": handled_id,
            "result": "kpis_refreshed",
            "kpis": dict(next_state["kpis"]),
        }
    elif event_type == "AuditEventSealed":
        target = payload.get("federation_id")
        if target in next_state["federations"]:
            evidence = build_federation_release_evidence(next_state, target)
            next_state["release_evidence_seals"][target] = {
                "sealed_by": payload.get("sealed_by", "system"),
                "lineage_hash": evidence["lineage_hash"],
            }
            trace = {
                "event_type": event_type,
                "handled_id": handled_id,
                "result": "release_evidence_sealed",
                "federation_id": target,
            }
        else:
            trace = {
                "event_type": event_type,
                "handled_id": handled_id,
                "result": "seal_skipped_unknown_federation",
                "federation_id": target,
            }
    else:
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "trace": {
                "event_type": event_type,
                "handled_id": handled_id,
                "result": "unsupported_event",
            },
        }

    next_state["inbound_traces"].append(trace)
    return {"ok": True, "duplicate": False, "state": next_state, "trace": trace}
