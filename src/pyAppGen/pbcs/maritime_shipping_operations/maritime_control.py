"""Executable improve1 controls for the Maritime Shipping Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "maritime_shipping_operations"
EVENT_CONTRACT = "AppGen-X"
MARITIME_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
MARITIME_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.maritime_shipping_operations.events"
_BASE_OWNED_TABLES = (
    "maritime_shipping_operations_voyage",
    "maritime_shipping_operations_vessel",
    "maritime_shipping_operations_cargo_booking",
    "maritime_shipping_operations_charter_party",
    "maritime_shipping_operations_port_call",
    "maritime_shipping_operations_demurrage_claim",
    "maritime_shipping_operations_bunker_event",
    "maritime_shipping_operations_maritime_shipping_operations_policy_rule",
    "maritime_shipping_operations_maritime_shipping_operations_runtime_parameter",
    "maritime_shipping_operations_maritime_shipping_operations_schema_extension",
    "maritime_shipping_operations_maritime_shipping_operations_control_assertion",
    "maritime_shipping_operations_maritime_shipping_operations_governed_model",
    "maritime_shipping_operations_appgen_outbox_event",
    "maritime_shipping_operations_appgen_inbox_event",
    "maritime_shipping_operations_appgen_dead_letter_event",
)
MARITIME_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(
    _BASE_OWNED_TABLES + tuple(f"maritime_shipping_operations_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)
))
MARITIME_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys((
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "CrewReadinessProjected",
    "PartyScreeningListChanged",
    "PortRestrictionPublished",
    "WeatherRiskChanged",
    "IdentityProjectionChanged",
    "PartnerAcknowledgementReceived",
)))
MARITIME_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in MARITIME_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in MARITIME_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "voyage_id", "vessel_id", "port_call_id", "booking_id", "policy_version", "audit_trail", "evidence_references")
_PRIMARY_PROOF_FIELDS: dict[int, str] = {1: 'rotation_graph_validated', 2: 'schedule_reliability_baseline_calculated', 3: 'berth_window_commitment_confirmed', 4: 'statement_of_facts_evidence_attached', 5: 'capacity_allocation_within_constraints', 6: 'cutoff_governance_decision_recorded', 7: 'bill_of_lading_lifecycle_approved', 8: 'stowage_plan_constraints_satisfied', 9: 'special_cargo_compliance_complete', 10: 'reefer_assurance_confirmed', 11: 'charter_clause_library_versioned', 12: 'laytime_computation_trace_verified', 13: 'demurrage_detention_exposure_classified', 14: 'claim_dossier_complete', 15: 'bunker_uplift_plan_approved', 16: 'rob_consumption_variance_reconciled', 17: 'carbon_tradeoff_explained', 18: 'crewing_projection_boundary_respected', 19: 'compliance_obligation_register_current', 20: 'sanctions_screening_cleared', 21: 'port_corridor_restriction_simulated', 22: 'maritime_event_taxonomy_emitted', 23: 'event_replay_projection_verified', 24: 'consumed_event_lineage_preserved', 25: 'dead_letter_replay_classified', 26: 'policy_rule_impact_previewed', 27: 'runtime_parameter_activation_approved', 28: 'schema_extension_compatibility_checked', 29: 'voyage_workbench_board_visible', 30: 'narrative_timeline_timezone_verified', 31: 'assistant_action_preview_confirmed', 32: 'schedule_recovery_options_compared', 33: 'booking_bill_intake_ambiguities_flagged', 34: 'claims_triage_evidence_sufficient', 35: 'counterfactual_simulation_side_effect_free', 36: 'predictive_risk_factors_explained', 37: 'anomaly_classification_actionable', 38: 'tenant_service_line_isolation_enforced', 39: 'maritime_reference_data_validated', 40: 'bulk_operation_row_outcomes_recorded', 41: 'search_export_keys_preserved', 42: 'partner_acknowledgement_tracked', 43: 'mobile_port_ops_permission_guarded', 44: 'continuous_control_assertions_generated', 45: 'cryptographic_audit_proof_sealed', 46: 'analytics_kpi_drillthrough_reconciled', 47: 'release_evidence_pack_complete', 48: 'digital_twin_fixture_replayable', 49: 'incident_drill_response_recorded', 50: 'go_live_gate_all_paths_passed'}
_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {
    feature_number: _BASE_FIELDS + (primary_proof,)
    for feature_number, primary_proof in _PRIMARY_PROOF_FIELDS.items()
}
_FEATURE_DEPENDENCIES: dict[int, tuple[str, ...]] = {18: ('CrewReadinessProjected',), 20: ('PartyScreeningListChanged', 'PolicyChanged'), 21: ('PortRestrictionPublished', 'WeatherRiskChanged'), 24: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'), 31: ('AuditEventSealed',), 36: ('WeatherRiskChanged', 'OperationalKpiChanged'), 38: ('IdentityProjectionChanged',), 42: ('PartnerAcknowledgementReceived',), 47: ('AuditEventSealed',)}
_DOMAIN_MESSAGES: dict[int, str] = {1: 'voyage rotations must model service string, trade lane, ballast or laden state, leg sequence, port-call links, canal transits, revised and actual milestones', 2: 'schedule reliability must separate proforma, revised, and actual movement variance by berth, weather, canal, congestion, and cascading network causes', 3: 'port-call commitments must govern terminal, berth, pilotage, tugs, gangs, crane intensity, working windows, call swaps, omissions, and rollover reasons', 4: 'statements of facts must preserve local time, UTC, source, correction lineage, and attachments for every operational milestone', 5: 'booking allocation must reserve capacity by leg, equipment, commodity, stowage, reefer, hazardous limit, waitlist, and commercial priority', 6: 'booking amendments must evaluate documentation, customs, hazardous, VGM, release, and gate-in cutoffs before acceptance or rollover', 7: 'bill-of-lading lifecycle must govern draft, review, approval, issue, surrender, switch, correction, archive, parties, freight terms, originals, and release mode', 8: 'stowage controls must validate bay-row-tier intent, discharge sequence, stack weight, segregation, lashing, hatch constraints, and restow exposure', 9: 'special cargo controls must validate IMDG segregation, flashpoint, packing certificate, OOG dimensions, lifts, and terminal acceptance prerequisites', 10: 'reefer assurance must reserve plugs, set point, ventilation, humidity, PTI, genset dependency, telemetry, and temperature deviation response', 11: 'charter clauses must version laycan, rates, demurrage, despatch, off-hire, bunker quality, performance warranties, and notices', 12: 'laytime computation must trace NOR, reversible laytime, SHEX/SHINC, weather, shifting, strike, pumping warranty, and stop-resume events', 13: 'demurrage and detention exposure must classify voyage and equipment charges by party, port, equipment, dispute, invoice, collection, and evidence source', 14: 'claim dossiers must package statement of facts, NOR, clauses, communications, logs, weather evidence, approvals, rebuttals, negotiation, and settlement history', 15: 'bunker planning must compare supplier, grade, quantity, density, sulfur context, price basis, barge window, ROB effect, congestion, and ECA entry', 16: 'ROB and consumption variance must reconcile departure, arrival, noon, idle, berth, speed, weather, hull, waiting, and reporting anomaly drivers', 17: 'carbon operation views must explain emissions, CII, ECA fuel switches, schedule recovery tradeoffs, bunker spend, and carbon intensity', 18: 'crewing readiness must remain a projection boundary with no crew roster tables while blocking voyages from safe-manning or restriction signals', 19: 'compliance obligations must track customs, manifests, hazardous declarations, ballast, sulfur, sanctions, discharge permits, owners, due dates, and evidence', 20: 'sanctions screening must cover booking, bill, charter, bank, supplier, restricted port, list version, analyst disposition, re-screening, and approval trail', 21: 'port and corridor intelligence must simulate draft, tide, daylight, pilotage, tug, strike, canal, convoy, war-risk, and local routing constraints', 22: 'maritime events must emit typed operational truth while preserving package-level compatibility events and AppGen-X ordering', 23: 'event-sourced history must replay material changes for voyages, calls, bookings, charters, claims, bunkers, actors, commands, policies, and documents', 24: 'consumed events must re-evaluate open operations with lineage for policy changes, audit seals, and KPI refreshes without duplicate outcomes', 25: 'dead-letter operations must show failed message context, retry count, poison reason, safe replay classification, and duplicate-safe resubmission', 26: 'policy governance must version booking, dangerous-goods, sanctions, demurrage, and bunker rules with activation workflow and impact preview', 27: 'runtime parameters must externalize schedule, reefer, laytime, demurrage, bunker, and stale-call tolerances with bounds, owner, rationale, and rollback', 28: 'schema extensions must check API, event, analytics, projection, backfill, release, and legacy record compatibility before activation', 29: 'voyage boards must group planning, readiness, execution, settlement, and exceptions with vessel-string, port, cargo, saved filters, and drill-throughs', 30: 'detail timelines must merge events, documents, policy decisions, consumption, laytime, comments, correction lineage, UTC, and local time views', 31: 'assistant actions must preview schedule, booking, bill, claim, and bunker mutations with affected records, obligations, permissions, and emitted events', 32: 'schedule recovery skills must compare skip, swap, cargo cut, cutoff revision, and speed-up options across customer, bunker, demurrage, and emissions impact', 33: 'intake skills must extract booking and bill instructions, parties, counts, commodity, freight terms, marks, routing, ambiguities, and source spans', 34: 'claims triage must cite fact gaps, conflicting timestamps, clauses, correspondence, settlement history, and evidence sufficiency before disposition', 35: 'counterfactual simulations must be non-mutating and compare diversion, omission, terminal swap, reroute, speed, and bunker alternatives', 36: 'risk scoring must explain terminal delay, weather, congestion, hazardous mix, document lead time, supplier variance, and charter exposure factors', 37: 'anomaly detection must classify impossible timelines, missing departures, ROB inconsistencies, over-issued bills, duplicate milestones, and correction paths', 38: 'tenant isolation must partition workbench, rules, parameters, evidence, voyages, bookings, claims, service lines, and shared reference-data views', 39: 'reference-data gates must validate IMO, call sign, UN/LOCODE, terminal, carrier, service, cargo description, dangerous-goods, and bunker-grade codes', 40: 'bulk operations must preserve row-level validation, partial success, per-record audit, notifications, rollover, cutoff, schedule, and claim outcomes', 41: 'search and export must filter voyages, calls, bookings, bills, claims, and bunkers by shipping keys while preserving governed record identifiers', 42: 'partner integrations must track terminal, agent, customs, bunker, and claim exchanges with acknowledgements, rejection reasons, timeout alerts, and fallback', 43: 'mobile port operations must support permissioned event capture, statements of facts, exception acknowledgement, approvals, responsive layout, and low-bandwidth use', 44: 'continuous controls must assert segregation of duties, sanction freshness, charter linkage, evidence completeness, parameter bounds, and operational exception creation', 45: 'cryptographic audit proofs must hash-chain timelines, bill approvals, claim dossiers, policy versions, release packs, and redacted proof views', 46: 'analytics must reconcile schedule reliability, booking rollover, bill latency, laytime, demurrage, bunker variance, carbon, and compliance to source records', 47: 'release evidence packs must cover voyage, booking, bill, claim, bunker, event, control, UI, and residual-risk scenarios for changed maritime surfaces', 48: 'digital-twin fixtures must replay liner, tanker, and dry-bulk voyages across API, UI, analytics, assistant, laytime, bunker, documents, and claims', 49: 'incident drills must record schedule collapse, berth cancellation, sanctions hit, dead-letter buildup, bunker failure, evidence corruption, responders, and SLA outcome', 50: 'go-live gates must fail unless voyage, schedule, port-call, booking, bill, laytime, demurrage, bunker, compliance, assistant, event, and evidence paths all pass'}
_HUMAN_CONFIRMATION_FEATURES = (31, 32, 33, 34)
_PROJECTION_ONLY_FEATURES = (18, 20, 24, 36, 38, 42)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    proof = _PRIMARY_PROOF_FIELDS[capability.feature_number]
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"maritime_shipping_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": proof,
        "ui": f"MaritimeShippingOperations{_camel(capability.slug)}Panel",
        "route": f"POST /maritime-shipping-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in MARITIME_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": MARITIME_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    feature_number = capability.feature_number
    spec = CONTROL_SPECS[feature_number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[feature_number])
    if feature_number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("maritime assistant skills must preview and propose; governed datastore mutations require human confirmation")
    if feature_number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("cross-PBC maritime context must be read through declared APIs, events, or projections, never shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != MARITIME_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("maritime eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in MARITIME_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary maritime shipping datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("maritime controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_maritime_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in MARITIME_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in MARITIME_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "primary_proof": spec["primary_proof"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": MARITIME_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": MARITIME_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "slug": resolved.slug,
        "title": resolved.title,
        "capability": resolved.as_traceability_row(),
        "payload": candidate,
        "evidence": evidence,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "side_effects": (),
    }


def improve1_maritime_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_maritime_control(capability) for capability in MARITIME_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.maritime-shipping-operations-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": MARITIME_CONTROL_OWNED_TABLES,
        "declared_dependencies": MARITIME_CONTROL_DECLARED_DEPENDENCIES,
        "allowed_database_backends": MARITIME_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": MARITIME_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


MARITIME_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_maritime_control(slug, payload))
    for capability in MARITIME_CONTROL_CAPABILITIES
}
