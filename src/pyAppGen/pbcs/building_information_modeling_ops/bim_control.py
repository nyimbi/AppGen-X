"""BIM operations control primitives for improve1 domain execution.

This module is deterministic and side-effect-free. It turns the BIM operations
improve1 backlog into executable package-local controls for federations,
coordinates, drawings, clashes, quantities, handover, commissioning, digital
twins, approvals, assistant behavior, release evidence, retention, and KPIs.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
import hashlib
import json
from typing import Mapping, Sequence

PBC_KEY = "building_information_modeling_ops"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "building_information_modeling_ops_bim_model",
    "building_information_modeling_ops_model_version",
    "building_information_modeling_ops_clash_issue",
    "building_information_modeling_ops_asset_object",
    "building_information_modeling_ops_handover_package",
    "building_information_modeling_ops_model_review",
    "building_information_modeling_ops_digital_twin_link",
    "building_information_modeling_ops_building_information_modeling_ops_policy_rule",
    "building_information_modeling_ops_building_information_modeling_ops_runtime_parameter",
    "building_information_modeling_ops_building_information_modeling_ops_schema_extension",
    "building_information_modeling_ops_building_information_modeling_ops_control_assertion",
    "building_information_modeling_ops_building_information_modeling_ops_governed_model",
    "building_information_modeling_ops_appgen_outbox_event",
    "building_information_modeling_ops_appgen_inbox_event",
    "building_information_modeling_ops_appgen_dead_letter_event",
)

BIM_CONTROL_CAPABILITIES = (
    "federation_registry_discipline_package_map",
    "shared_coordinates_georeferencing_assurance",
    "model_issue_purpose_governance",
    "drawing_model_revision_linkage",
    "spatial_hierarchy_completeness_controls",
    "quantity_extraction_measurement_snapshots",
    "construction_clash_taxonomy",
    "clash_grouping_duplicate_suppression",
    "model_issue_ledger",
    "approval_matrix_discipline_zone_purpose",
    "partial_publish_staged_release",
    "model_version_delta_evidence",
    "asset_tagging_completeness_uniqueness",
    "structured_handover_data_mapping",
    "space_room_data_integrity",
    "system_zone_membership_governance",
    "location_asset_consistency_validation",
    "drawing_register_dependency_awareness",
    "revision_transmittal_control",
    "construction_work_package_snapshots",
    "field_verification_intake",
    "temporary_works_model_controls",
    "as_built_reconciliation_workflow",
    "handover_readiness_dashboard",
    "om_document_asset_system_linkage",
    "commissioning_prerequisite_tracking",
    "digital_twin_activation_gates",
    "quantity_change_approval_thresholds",
    "naming_classification_policy_enforcement",
    "units_measurement_normalization",
    "model_health_score_factors",
    "external_domain_event_boundary",
    "incoming_event_policy_kpi_handling",
    "heavy_model_metadata_api_boundary",
    "release_evidence_bundle_generator",
    "continuous_bim_control_assertions",
    "assistant_clash_triage_summary",
    "assistant_handover_gap_detection",
    "assistant_revision_impact_brief",
    "federation_operations_workbench",
    "issue_triage_workbench",
    "asset_handover_workbench",
    "approval_evidence_workbench",
    "exception_taxonomy_service_levels",
    "multi_project_tenant_isolation",
    "controlled_handover_schema_extension",
    "carbon_sustainability_traceability",
    "construction_sequence_location_readiness",
    "archive_supersession_retention_governance",
    "operational_kpi_release_confidence_pack",
)


def _tuple(value: object) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, (list, set)):
        return tuple(value)
    return (value,)


def _date(value: object | None) -> date:
    if value is None:
        return date(2026, 5, 30)
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _result(capability: str, table: str, **payload: object) -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "capability": capability,
        "table": table,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
        **payload,
    }


def build_federation_registry(packages: Sequence[Mapping[str, object]]) -> dict:
    required = ("version_id", "discipline", "authoring_party", "coordinate_basis", "issue_purpose", "spatial_coverage", "lod_target", "approval_state", "checksum")
    normalized = []
    blockers = []
    for package in packages:
        package = dict(package)
        missing = tuple(field for field in required if not package.get(field))
        if missing:
            blockers.append({"version_id": package.get("version_id"), "missing": missing})
        normalized.append({field: package.get(field) for field in required})
    by_discipline = {discipline: tuple(item for item in normalized if item.get("discipline") == discipline) for discipline in sorted({item.get("discipline") for item in normalized})}
    return _result("federation_registry_discipline_package_map", OWNED_TABLES[1], packages=tuple(normalized), by_discipline=by_discipline, publish_blockers=tuple(blockers))


def validate_coordinate_assurance(version: Mapping[str, object], baseline: Mapping[str, object], tolerance_mm: float = 25.0, rotation_tolerance: float = 0.5) -> dict:
    version = dict(version or {})
    baseline = dict(baseline or {})
    issues = []
    if version.get("coordinate_basis") != baseline.get("coordinate_basis"):
        issues.append("coordinate_basis_mismatch")
    for point in ("survey_point", "project_base_point"):
        left = dict(version.get(point) or {})
        right = dict(baseline.get(point) or {})
        delta = max((abs(float(left.get(axis, 0)) - float(right.get(axis, 0))) for axis in ("x", "y", "z")), default=0.0)
        if delta > tolerance_mm:
            issues.append(f"{point}_out_of_tolerance")
    if abs(float(version.get("true_north_degrees", 0)) - float(baseline.get("true_north_degrees", 0))) > rotation_tolerance:
        issues.append("true_north_out_of_tolerance")
    if version.get("elevation_datum") != baseline.get("elevation_datum"):
        issues.append("elevation_datum_mismatch")
    if float(version.get("unit_scale", 1)) != float(baseline.get("unit_scale", 1)):
        issues.append("unit_scale_mismatch")
    return _result("shared_coordinates_georeferencing_assurance", OWNED_TABLES[1], coordinate_ok=not issues, issues=tuple(issues), tolerance_mm=tolerance_mm)


def govern_issue_purpose(version: Mapping[str, object], target_purpose: str) -> dict:
    order = ("wip", "shared", "construction", "record", "handover")
    current = str(dict(version or {}).get("issue_purpose", "wip"))
    approved = dict(version or {}).get("approval_state") == "approved"
    allowed = current in order and target_purpose in order and order.index(target_purpose) <= order.index(current) + 1 and approved
    downstream = {
        "wip": (),
        "shared": ("clash_review", "model_review"),
        "construction": ("clash_review", "asset_enrichment", "work_package"),
        "record": ("asset_handover", "as_built_reconciliation"),
        "handover": ("handover_package", "digital_twin_activation"),
    }.get(target_purpose, ())
    return _result("model_issue_purpose_governance", OWNED_TABLES[1], promotion_allowed=allowed, current_purpose=current, target_purpose=target_purpose, downstream_actions=downstream)


def link_drawing_revision(version: Mapping[str, object], drawings: Sequence[Mapping[str, object]]) -> dict:
    version = dict(version or {})
    linked = tuple({**dict(item), "model_version_id": version.get("version_id"), "supersedes": item.get("previous_revision")} for item in drawings)
    blocked = tuple(item for item in linked if item.get("approval_state") != "approved")
    return _result("drawing_model_revision_linkage", OWNED_TABLES[1], revision_matrix=linked, release_blocked=bool(blocked), unapproved_drawings=blocked)


def validate_spatial_hierarchy(records: Sequence[Mapping[str, object]]) -> dict:
    required = ("site", "building", "storey", "zone", "space")
    invalid = tuple({"record_id": item.get("id"), "missing": tuple(field for field in required if not dict(item).get(field))} for item in (dict(r) for r in records) if any(not item.get(field) for field in required))
    complete = len(tuple(records)) - len(invalid)
    return _result("spatial_hierarchy_completeness_controls", OWNED_TABLES[3], invalid_records=invalid, completeness_percent=round(100 * complete / max(1, len(tuple(records))), 2))


def create_quantity_snapshot(version: Mapping[str, object], measurements: Sequence[Mapping[str, object]], exclusions: Sequence[str] = ()) -> dict:
    totals: dict[str, float] = {}
    for item in measurements:
        item = dict(item)
        if item.get("category") in exclusions:
            continue
        unit = str(item.get("unit", "unit"))
        totals[unit] = round(totals.get(unit, 0.0) + float(item.get("quantity", 0)), 4)
    snapshot = {"version_id": dict(version or {}).get("version_id"), "snapshot_id": _digest((version, totals))[:12], "totals": totals, "excluded_categories": tuple(exclusions)}
    return _result("quantity_extraction_measurement_snapshots", OWNED_TABLES[5], snapshot=snapshot, immutable_after_approval=True)


def classify_clash_issue(issue: Mapping[str, object]) -> dict:
    issue = dict(issue or {})
    severity = issue.get("severity", "medium")
    allowed_dispositions = ("accepted", "waived", "redesign", "site_resolution_required") if severity in {"low", "medium"} else ("redesign", "site_resolution_required")
    blocking = severity in {"high", "critical"}
    return _result("construction_clash_taxonomy", OWNED_TABLES[2], clash_type=issue.get("clash_type", "hard_clash"), severity=severity, allowed_dispositions=allowed_dispositions, blocks_release=blocking)


def group_duplicate_clashes(issues: Sequence[Mapping[str, object]]) -> dict:
    groups: dict[str, list[dict]] = {}
    for issue in issues:
        issue = dict(issue)
        key = _digest((issue.get("location"), issue.get("discipline_pair"), issue.get("system"), issue.get("root_condition")))[:10]
        groups.setdefault(key, []).append(issue)
    grouped = tuple({"group_id": key, "instance_count": len(items), "issue_ids": tuple(item.get("issue_id") for item in items)} for key, items in sorted(groups.items()))
    return _result("clash_grouping_duplicate_suppression", OWNED_TABLES[2], groups=grouped, duplicate_reduction=sum(max(0, item["instance_count"] - 1) for item in grouped))


def build_model_issue_ledger(issues: Sequence[Mapping[str, object]]) -> dict:
    ledger = tuple({**dict(item), "ledger_id": _digest((item.get("source"), item.get("issue_id")))[:12], "closure_required": bool(item.get("blocking"))} for item in issues)
    open_blockers = tuple(item for item in ledger if item.get("closure_required") and item.get("status") != "closed")
    return _result("model_issue_ledger", OWNED_TABLES[2], issue_ledger=ledger, release_blocked=bool(open_blockers), open_blockers=open_blockers)


def route_approval_matrix(candidate: Mapping[str, object], policies: Sequence[Mapping[str, object]]) -> dict:
    candidate = dict(candidate or {})
    matched = tuple(dict(policy) for policy in policies if all(candidate.get(k) == policy.get(k) for k in ("discipline", "zone", "issue_purpose") if policy.get(k) is not None))
    approvers = tuple(dict.fromkeys(role for policy in matched for role in _tuple(policy.get("required_roles")))) or ("bim_manager",)
    return _result("approval_matrix_discipline_zone_purpose", OWNED_TABLES[7], required_approvers=approvers, matched_policy_count=len(matched), risk_score=candidate.get("risk_score", 0))


def evaluate_partial_publish(scope: Mapping[str, object], blockers: Sequence[Mapping[str, object]]) -> dict:
    scope = dict(scope or {})
    relevant_blockers = tuple(dict(item) for item in blockers if set(_tuple(item.get("scope"))).intersection(set(_tuple(scope.get("scope_slice")))))
    return _result("partial_publish_staged_release", OWNED_TABLES[1], publish_scope=scope, partial_publish_allowed=not relevant_blockers, blockers=relevant_blockers)


def compare_model_versions(previous: Mapping[str, object], current: Mapping[str, object]) -> dict:
    previous = dict(previous or {})
    current = dict(current or {})
    categories = ("geometry", "objects", "spaces", "assets", "quantities", "issues")
    deltas = tuple({"category": category, "previous": previous.get(category), "current": current.get(category), "changed": previous.get(category) != current.get(category)} for category in categories)
    return _result("model_version_delta_evidence", OWNED_TABLES[1], compared_versions=(previous.get("version_id"), current.get("version_id")), deltas=deltas, signed_summary_hash=_digest(deltas))


def validate_asset_tags(assets: Sequence[Mapping[str, object]], reserved_prefixes: Sequence[str] = ()) -> dict:
    seen: set[str] = set()
    failures = []
    for asset in assets:
        asset = dict(asset)
        tag = str(asset.get("tag", ""))
        if not tag or tag in seen or (reserved_prefixes and not tag.startswith(tuple(reserved_prefixes))):
            failures.append({"asset_id": asset.get("asset_id"), "tag": tag, "reason": "missing_duplicate_or_bad_prefix"})
        seen.add(tag)
    return _result("asset_tagging_completeness_uniqueness", OWNED_TABLES[3], failures=tuple(failures), unique_tag_count=len(seen))


def validate_structured_handover(package: Mapping[str, object]) -> dict:
    required_groups = ("facility", "floor", "space", "system", "component", "type", "contact", "spares", "warranty", "maintenance")
    missing = tuple(group for group in required_groups if not dict(package or {}).get(group))
    return _result("structured_handover_data_mapping", OWNED_TABLES[4], missing_groups=missing, completion_percent=round(100 * (len(required_groups) - len(missing)) / len(required_groups), 2), vendor_neutral_mapping=True)


def check_space_room_integrity(spaces: Sequence[Mapping[str, object]]) -> dict:
    invalid = tuple(dict(item) for item in spaces if not dict(item).get("room_number") or dict(item).get("overlap") or not dict(item).get("operational_classification"))
    return _result("space_room_data_integrity", OWNED_TABLES[5], invalid_spaces=invalid, blocks_handover=bool(invalid))


def govern_system_zone_membership(assets: Sequence[Mapping[str, object]], mandatory_classes: Sequence[str]) -> dict:
    failures = tuple(dict(item) for item in assets if item.get("asset_class") in mandatory_classes and (not item.get("system") or not item.get("zone")))
    return _result("system_zone_membership_governance", OWNED_TABLES[3], missing_membership=failures, required_for_classes=tuple(mandatory_classes))


def validate_location_asset_consistency(assets: Sequence[Mapping[str, object]], approved_locations: Sequence[str]) -> dict:
    approved = set(approved_locations)
    mismatches = tuple(dict(item) for item in assets if item.get("location") not in approved and not item.get("off_model_exception_approved"))
    return _result("location_asset_consistency_validation", OWNED_TABLES[3], mismatches=mismatches, exception_approvals=tuple(item.get("asset_id") for item in assets if item.get("off_model_exception_approved")))


def build_drawing_dependency_register(drawings: Sequence[Mapping[str, object]]) -> dict:
    lagging = tuple(dict(item) for item in drawings if item.get("required") and item.get("revision_state") != item.get("model_revision_state"))
    return _result("drawing_register_dependency_awareness", OWNED_TABLES[5], drawing_register=tuple(dict(item) for item in drawings), lagging_dependencies=lagging, release_blocked=bool(lagging))


def control_revision_transmittals(transmittals: Sequence[Mapping[str, object]]) -> dict:
    current = tuple(dict(item) for item in transmittals if not item.get("superseded_by"))
    acknowledgement_gaps = tuple(dict(item) for item in current if item.get("ack_required") and not item.get("acknowledged_at"))
    return _result("revision_transmittal_control", OWNED_TABLES[4], current_transmittals=current, acknowledgement_gaps=acknowledgement_gaps, superseded_visible=True)


def create_work_package_snapshot(scope: Mapping[str, object], version: Mapping[str, object]) -> dict:
    snapshot = {"snapshot_id": _digest((scope, version))[:12], "scope": dict(scope or {}), "source_version_id": dict(version or {}).get("version_id"), "checksum": _digest((scope, version, "snapshot"))}
    return _result("construction_work_package_snapshots", OWNED_TABLES[4], snapshot=snapshot, immutable=True)


def intake_field_verification(observation: Mapping[str, object]) -> dict:
    observation = dict(observation or {})
    target = "clash_issue" if observation.get("deviation_type") in {"geometry", "access"} else "model_review"
    return _result("field_verification_intake", OWNED_TABLES[2], target_record_type=target, observation_id=observation.get("observation_id"), evidence=tuple(_tuple(observation.get("evidence"))), revision_response_required=True)


def govern_temporary_works_model(model: Mapping[str, object], as_of: object | None = None) -> dict:
    model = dict(model or {})
    expired = _date(model.get("expiry_date")) < _date(as_of)
    return _result("temporary_works_model_controls", OWNED_TABLES[0], temporary=True, expired=expired, excluded_from_handover=True, review_cadence_days=model.get("review_cadence_days", 7))


def reconcile_as_built(planned: Sequence[Mapping[str, object]], installed: Sequence[Mapping[str, object]]) -> dict:
    installed_by_id = {item.get("asset_id"): dict(item) for item in installed}
    deviations = tuple({"asset_id": item.get("asset_id"), "planned": dict(item), "installed": installed_by_id.get(item.get("asset_id"))} for item in planned if installed_by_id.get(item.get("asset_id")) != dict(item))
    critical_open = tuple(item for item in deviations if item["planned"].get("critical"))
    return _result("as_built_reconciliation_workflow", OWNED_TABLES[4], deviations=deviations, record_issue_blocked=bool(critical_open))


def score_handover_readiness(scope: Mapping[str, object], assets: Sequence[Mapping[str, object]], issues: Sequence[Mapping[str, object]], documents: Sequence[Mapping[str, object]]) -> dict:
    total_assets = max(1, len(tuple(assets)))
    complete_assets = sum(1 for item in assets if item.get("complete"))
    open_blockers = sum(1 for issue in issues if issue.get("blocking") and issue.get("status") != "closed")
    linked_docs = sum(1 for doc in documents if doc.get("approved") and doc.get("asset_id"))
    score = max(0, min(100, round((complete_assets / total_assets) * 70 + min(30, linked_docs * 5) - open_blockers * 20, 2)))
    return _result("handover_readiness_dashboard", OWNED_TABLES[4], scope=dict(scope or {}), readiness_score=score, open_blockers=open_blockers)


def validate_om_document_links(documents: Sequence[Mapping[str, object]], assets: Sequence[Mapping[str, object]]) -> dict:
    asset_ids = {item.get("asset_id") for item in assets}
    missing = tuple(asset for asset in asset_ids if not any(doc.get("asset_id") == asset and doc.get("purpose") in {"manual", "certificate", "maintenance_plan"} for doc in documents))
    return _result("om_document_asset_system_linkage", OWNED_TABLES[4], missing_asset_documents=missing, linkage_matrix=tuple(dict(doc) for doc in documents))


def track_commissioning_prerequisites(assets: Sequence[Mapping[str, object]]) -> dict:
    open_items = tuple({"asset_id": asset.get("asset_id"), "open_prerequisites": tuple(item for item in _tuple(asset.get("prerequisites")) if item not in set(_tuple(asset.get("completed_prerequisites"))))} for asset in assets)
    blocking = tuple(item for item in open_items if item["open_prerequisites"])
    return _result("commissioning_prerequisite_tracking", OWNED_TABLES[3], open_items=blocking, handover_blocked=bool(blocking))


def gate_digital_twin_activation(link: Mapping[str, object], inputs: Mapping[str, object]) -> dict:
    required = ("approved_asset_identifiers", "stable_spatial_hierarchy", "accepted_handover_data", "verified_event_mappings")
    missing = tuple(item for item in required if not dict(inputs or {}).get(item))
    return _result("digital_twin_activation_gates", OWNED_TABLES[6], link_id=dict(link or {}).get("link_id"), activation_allowed=not missing, missing_inputs=missing)


def evaluate_quantity_change_thresholds(deltas: Sequence[Mapping[str, object]], thresholds: Mapping[str, object]) -> dict:
    triggered = tuple(dict(item) for item in deltas if abs(float(item.get("delta_percent", 0))) >= float(dict(thresholds or {}).get(item.get("category"), dict(thresholds or {}).get("default", 10))))
    return _result("quantity_change_approval_thresholds", OWNED_TABLES[7], triggered_reviews=triggered, approval_required=bool(triggered))


def enforce_naming_classification_policy(objects: Sequence[Mapping[str, object]], policy: Mapping[str, object]) -> dict:
    prefixes = tuple(dict(policy or {}).get("accepted_prefixes", ()))
    classes = set(_tuple(dict(policy or {}).get("accepted_classes")))
    violations = tuple(dict(item) for item in objects if (prefixes and not str(item.get("name", "")).startswith(prefixes)) or (classes and item.get("classification") not in classes))
    return _result("naming_classification_policy_enforcement", OWNED_TABLES[7], violations=violations, controlled_exceptions_required=bool(violations))


def normalize_units_measurements(measurements: Sequence[Mapping[str, object]], project_units: Mapping[str, object]) -> dict:
    conversions = {("mm", "m"): 0.001, ("cm", "m"): 0.01, ("m", "m"): 1.0, ("ft", "m"): 0.3048}
    target = dict(project_units or {}).get("length", "m")
    normalized = tuple({**dict(item), "normalized_unit": target, "normalized_value": round(float(item.get("value", 0)) * conversions.get((item.get("unit"), target), 1.0), 6)} for item in measurements)
    return _result("units_measurement_normalization", OWNED_TABLES[5], normalized_measurements=normalized, project_units=dict(project_units or {}))


def calculate_model_health_score(factors: Mapping[str, object]) -> dict:
    weights = {"clash_severity": 25, "quantity_variance": 15, "missing_classifications": 15, "site_findings": 15, "handover_completeness": 20, "policy_exceptions": 10}
    penalties = sum(min(weights[key], float(dict(factors or {}).get(key, 0)) * weights[key]) for key in weights if key != "handover_completeness")
    bonus = float(dict(factors or {}).get("handover_completeness", 0)) * weights["handover_completeness"]
    score = max(0, min(100, round(100 - penalties + bonus - weights["handover_completeness"], 2)))
    return _result("model_health_score_factors", OWNED_TABLES[5], health_score=score, factors=dict(factors or {}), weights=weights)


def build_external_event_boundary() -> dict:
    events = ("ModelVersionApproved", "ModelRevisionSuperseded", "ClashMilestoneClosed", "HandoverReadinessChanged", "DigitalTwinActivated", "BimReleaseBundleGenerated")
    return _result("external_domain_event_boundary", OWNED_TABLES[12], events=events, exposes_internal_tables=False, payload_identifiers=("model_id", "version_id", "federation_id", "package_id"))


def handle_incoming_policy_kpi_event(event: Mapping[str, object], affected_records: Sequence[Mapping[str, object]]) -> dict:
    event = dict(event or {})
    actions = {"PolicyChanged": "reevaluate_approval_thresholds", "AuditEventSealed": "seal_audit_artifacts", "OperationalKpiChanged": "refresh_readiness_metrics"}
    return _result("incoming_event_policy_kpi_handling", OWNED_TABLES[13], action=actions.get(event.get("event_type"), "dead_letter"), affected_records=tuple(dict(item) for item in affected_records), idempotency_key=event.get("idempotency_key") or _digest(event))


def build_heavy_model_api_boundary() -> dict:
    routes = ("POST /bim-models", "POST /model-versions/metadata", "POST /clash-issues/import", "POST /asset-objects/enrich", "POST /handover-packages/validate", "POST /model-versions/{version_id}/promotions")
    return _result("heavy_model_metadata_api_boundary", OWNED_TABLES[1], routes=routes, idempotent_commands=tuple(route for route in routes if route.startswith("POST")), retry_profiles=("large_upload", "metadata_update", "approval_promotion"))


def generate_release_evidence_bundle(inputs: Mapping[str, object]) -> dict:
    required = ("model_versions", "drawings", "issues", "approvals", "quantities", "handover_checks")
    missing = tuple(item for item in required if not dict(inputs or {}).get(item))
    bundle = {"bundle_id": _digest(inputs)[:12], "missing": missing, "immutable_timestamp": datetime(2026, 5, 30, 12, 0).isoformat()}
    return _result("release_evidence_bundle_generator", OWNED_TABLES[11], bundle=bundle, release_ready=not missing)


def evaluate_continuous_bim_controls(assertions: Sequence[Mapping[str, object]]) -> dict:
    failures = tuple(dict(item) for item in assertions if item.get("status") != "pass" and not item.get("suppressed_until"))
    return _result("continuous_bim_control_assertions", OWNED_TABLES[10], failures=failures, signoff_allowed=not failures)


def summarize_clash_triage(issues: Sequence[Mapping[str, object]]) -> dict:
    groups: dict[str, list[dict]] = {}
    for issue in issues:
        issue = dict(issue)
        key = f"{issue.get('trade_pair')}:{issue.get('level')}:{issue.get('root_cause')}"
        groups.setdefault(key, []).append(issue)
    brief = tuple({"focus": key, "count": len(items), "citations": tuple(item.get("issue_id") for item in items)} for key, items in sorted(groups.items()))
    return _result("assistant_clash_triage_summary", OWNED_TABLES[2], meeting_brief=brief, requires_review=True)


def detect_handover_gaps(package: Mapping[str, object], assets: Sequence[Mapping[str, object]]) -> dict:
    package_result = validate_structured_handover(package)
    incomplete_assets = tuple(dict(item) for item in assets if not item.get("complete"))
    tasks = tuple({"discipline": item.get("discipline"), "asset_id": item.get("asset_id"), "missing": tuple(_tuple(item.get("missing")))} for item in incomplete_assets)
    return _result("assistant_handover_gap_detection", OWNED_TABLES[4], missing_groups=package_result["missing_groups"], remediation_tasks=tasks, no_completion_claim_without_evidence=True)


def build_revision_impact_brief(previous: Mapping[str, object], current: Mapping[str, object]) -> dict:
    delta = compare_model_versions(previous, current)
    changed = tuple(item for item in delta["deltas"] if item["changed"])
    return _result("assistant_revision_impact_brief", OWNED_TABLES[1], compared_versions=delta["compared_versions"], impact_cards=changed, citations=delta["compared_versions"], requires_approval=True)


def build_federation_operations_workbench(federations: Sequence[Mapping[str, object]]) -> dict:
    rows = tuple({"federation_id": item.get("federation_id"), "status": item.get("status"), "health_score": item.get("health_score"), "pending_blockers": tuple(_tuple(item.get("blockers")))} for item in federations)
    return _result("federation_operations_workbench", OWNED_TABLES[11], rows=rows, empty_state_supported=True, degraded_state_supported=True)


def build_issue_triage_workbench(issues: Sequence[Mapping[str, object]], filters: Mapping[str, object]) -> dict:
    filtered = tuple(dict(item) for item in issues if all(item.get(key) == value for key, value in dict(filters or {}).items()))
    return _result("issue_triage_workbench", OWNED_TABLES[2], filters=dict(filters or {}), visible_issues=filtered, bulk_actions=("assign", "set_due_date", "close_with_evidence"))


def build_asset_handover_workbench(assets: Sequence[Mapping[str, object]], packages: Sequence[Mapping[str, object]]) -> dict:
    readiness = tuple(score_handover_readiness({"package_id": package.get("package_id")}, assets, (), package.get("documents", ())) for package in packages)
    return _result("asset_handover_workbench", OWNED_TABLES[4], asset_count=len(tuple(assets)), package_readiness=readiness, drilldowns=("assets", "documents", "spaces", "commissioning"))


def build_approval_evidence_workbench(candidate: Mapping[str, object]) -> dict:
    prerequisites = ("revision_delta", "unresolved_issues", "quantity_changes", "control_assertions", "required_approvers", "release_bundle")
    visible = tuple(item for item in prerequisites if dict(candidate or {}).get(item) is not None)
    return _result("approval_evidence_workbench", OWNED_TABLES[11], visible_prerequisites=visible, all_prerequisites_visible=len(visible) == len(prerequisites), rationale_capture_required=True)


def classify_exception_service_levels(exceptions: Sequence[Mapping[str, object]], as_of: object | None = None) -> dict:
    today = _date(as_of)
    targets = {"coordination_critical": 2, "construction_critical": 1, "handover_critical": 3, "informational": 10}
    aged = []
    for item in exceptions:
        item = dict(item)
        age = (today - _date(item.get("opened_date"))).days
        target = targets.get(item.get("class"), 5)
        aged.append({**item, "age_days": age, "target_days": target, "sla_breached": age > target})
    return _result("exception_taxonomy_service_levels", OWNED_TABLES[8], exceptions=tuple(aged), escalations=tuple(item for item in aged if item["sla_breached"]))


def enforce_project_tenant_isolation(record: Mapping[str, object], context: Mapping[str, object]) -> dict:
    record = dict(record or {})
    context = dict(context or {})
    allowed = record.get("tenant") == context.get("tenant") and record.get("project_id") == context.get("project_id")
    return _result("multi_project_tenant_isolation", OWNED_TABLES[11], allowed=allowed, cross_tenant_blocked=record.get("tenant") != context.get("tenant"), cross_project_blocked=record.get("project_id") != context.get("project_id"))


def register_handover_schema_extension(extension: Mapping[str, object]) -> dict:
    extension = dict(extension or {})
    required = ("field_name", "asset_classes", "validation_rule", "migration_history", "export_compatibility")
    missing = tuple(field for field in required if not extension.get(field))
    compatible = str(extension.get("table", OWNED_TABLES[3])).startswith(PBC_KEY)
    return _result("controlled_handover_schema_extension", OWNED_TABLES[9], valid=not missing and compatible, missing_fields=missing, compatible_table=compatible)


def trace_carbon_sustainability(metrics: Sequence[Mapping[str, object]]) -> dict:
    linked = tuple(dict(item) for item in metrics if item.get("model_version_id") and item.get("quantity_snapshot_id") and item.get("asset_id"))
    unlinked = tuple(dict(item) for item in metrics if item not in linked)
    return _result("carbon_sustainability_traceability", OWNED_TABLES[5], linked_metrics=linked, unlinked_metrics=unlinked, source_traceability_percent=round(100 * len(linked) / max(1, len(tuple(metrics))), 2))


def check_construction_sequence_readiness(package: Mapping[str, object]) -> dict:
    package = dict(package or {})
    gates = ("predecessor_complete", "access_zone_clear", "temporary_works_ready", "trade_window_confirmed")
    missing = tuple(gate for gate in gates if not package.get(gate))
    return _result("construction_sequence_location_readiness", OWNED_TABLES[5], location_package=package.get("package_id"), readiness_allowed=not missing, missing_gates=missing)


def govern_archive_supersession(record: Mapping[str, object], retention_years: int = 12) -> dict:
    record = dict(record or {})
    archive = {"archive_id": _digest(record)[:12], "current": False, "superseded_by": record.get("superseded_by"), "retain_until": (_date(record.get("approved_date")) + timedelta(days=365 * retention_years)).isoformat()}
    return _result("archive_supersession_retention_governance", OWNED_TABLES[11], archive_record=archive, immutable=True, queryable=True)


def build_operational_kpi_pack(metrics: Mapping[str, object]) -> dict:
    required = ("federation_health", "blocking_clash_burn_down", "asset_data_completeness", "handover_readiness", "approval_latency", "revision_churn", "release_rework_rate")
    missing = tuple(metric for metric in required if metric not in dict(metrics or {}))
    return _result("operational_kpi_release_confidence_pack", OWNED_TABLES[8], kpi_pack=dict(metrics or {}), missing_metrics=missing, release_confidence="high" if not missing else "incomplete")


def improve1_bim_control_contract() -> dict:
    return _result(
        "improve1_bim_control_contract",
        OWNED_TABLES[0],
        capability_count=len(BIM_CONTROL_CAPABILITIES),
        capabilities=BIM_CONTROL_CAPABILITIES,
        owned_tables=OWNED_TABLES,
        ui_surfaces=tuple(f"{PBC_KEY}.ui.bim_control.{capability}" for capability in BIM_CONTROL_CAPABILITIES),
        service_surfaces=tuple(f"{PBC_KEY}.service.bim_control.{capability}" for capability in BIM_CONTROL_CAPABILITIES),
    )
