"""Executable improve1 controls for the Sustainability ESG Reporting PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS,
    SUSTAINABILITY_ESG_REPORTING_CONSUMED_EVENT_TYPES,
    SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES,
    SUSTAINABILITY_ESG_REPORTING_REQUIRED_EVENT_TOPIC,
    SUSTAINABILITY_ESG_REPORTING_RUNTIME_TABLES,
)

PBC_KEY = "sustainability_esg_reporting"
EVENT_CONTRACT = "AppGen-X"
ESG_ALLOWED_DATABASE_BACKENDS = SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS
ESG_REQUIRED_EVENT_TOPIC = SUSTAINABILITY_ESG_REPORTING_REQUIRED_EVENT_TOPIC
ESG_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in ESG_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in ESG_CAPABILITIES}
ESG_OWNED_TABLES = tuple(
    dict.fromkeys(
        SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES
        + SUSTAINABILITY_ESG_REPORTING_RUNTIME_TABLES
        + tuple(f"sustainability_esg_reporting_{capability.slug}_control" for capability in ESG_CAPABILITIES)
    )
)
ESG_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        SUSTAINABILITY_ESG_REPORTING_CONSUMED_EVENT_TYPES
        + (
            "SupplierQualified",
            "ShipmentDelivered",
            "EnergyUsageRecorded",
            "TravelBooked",
            "AssetPlacedInService",
            "PolicyChanged",
            "FacilityProfileChanged",
            "WorkforceMetricPublished",
            "ProcurementSpendClassified",
            "FinanceClosePeriodLocked",
            "CertificateRegistryUpdated",
            "RegulatoryFrameworkChanged",
            "AssuranceRequestReceived",
            "AuditEventSealed",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "reporting_period",
    "framework_version",
    "boundary_id",
    "metric_id",
    "owner_id",
    "evidence_references",
    "policy_version",
)
_FIELD_ROWS = """
1|metric_ontology_id,metric_category,materiality_topic,unit_of_measure,framework_requirement,assurance_level,duplicate_conflict_check
2|source_registry_id,source_type,expected_cadence,data_owner,collection_method,evidence_requirement,quality_profile
3|activity_record_id,completeness_score,missing_interval,estimation_method,estimation_confidence,gap_reason,replacement_policy
4|factor_governance_id,factor_source,jurisdiction,vintage_year,unit_basis,uncertainty_range,expiry_exception
5|factor_selection_id,candidate_factor_set,matching_rule,rejected_factor_set,conversion_logic,uncertainty_impact,policy_justification
6|unit_validation_id,source_unit,normalized_unit,conversion_factor,dimension_family,rounding_rule,invalid_unit_quarantine
7|scope_boundary_id,legal_entity_id,facility_projection_id,ownership_percentage,operational_control,consolidation_method,exclusion_rationale
8|scope1_coverage_id,stationary_combustion,mobile_combustion,fugitive_emissions,process_emissions,refrigerant_gwp_version,coverage_gap
9|scope2_dual_method_id,location_based_factor,market_based_factor,certificate_record,residual_mix_factor,grid_region,retirement_check
10|scope3_matrix_id,scope3_category,category_owner,supplier_dependency,materiality_status,assurance_level,exclusion_rationale
11|supplier_confidence_id,supplier_projection_id,methodology_quality,boundary_quality,data_vintage,discrepancy_score,acceptance_decision
12|supplier_remediation_id,requested_evidence,due_date,communication_thread,escalation_path,temporary_estimate,closure_proof
13|carbon_attribution_id,allocation_object_type,allocation_object_projection,basis,denominator,confidence,double_counting_safeguard
14|carbon_ledger_id,activity_hash,factor_version_hash,boundary_version_hash,adjustment_hash,disclosure_reference,immutable_lineage_hash
15|uncertainty_propagation_id,activity_uncertainty,factor_uncertainty,allocation_uncertainty,total_confidence_band,top_contributor,disclosure_note
16|quality_rule_id,rule_type,affected_metric,severity,failed_value,remediation_owner,disclosure_block
17|duplicate_detection_id,source_identity,activity_period,facility_projection,supplier_projection,evidence_hash,resolution_decision
18|target_taxonomy_id,target_type,baseline_value,baseline_year,science_alignment_evidence,interim_milestone,adjustment_policy
19|target_decomposition_id,operational_reduction,structural_change,factor_update,methodology_change,offset_contribution,real_reduction_flag
20|decarbonization_initiative_id,expected_abatement,cost,initiative_owner,timeline,risk,achieved_abatement
21|reduction_simulation_id,changed_assumption_set,factor_change_set,supplier_shift,cost_per_unit_reduced,target_impact,implementation_risk
22|climate_scenario_id,scenario_family,temperature_pathway,transition_assumption,physical_hazard_set,time_horizon,adaptation_action
23|hazard_exposure_id,facility_or_asset_projection,geospatial_confidence,hazard_type,severity,time_horizon,business_impact
24|transition_risk_id,carbon_price_scenario,policy_assumption,sector_exposure,cost_sensitivity,stranded_asset_indicator,opportunity_value
25|framework_mapping_id,framework_topic,disclosure_requirement,metric_mapping,narrative_requirement,evidence_requirement,gap_status
26|regulatory_change_id,old_framework_version,new_framework_version,changed_requirement,affected_metric_set,assurance_need,deadline
27|disclosure_packet_id,report_type,included_metric_set,narrative_section_set,evidence_link_set,approval_workflow,publication_state
28|tie_out_check_id,packet_total,carbon_ledger_total,target_progress_total,prior_disclosure_total,inconsistency_reason,remediation_required
29|evidence_room_id,evidence_type,source_document,control_assertion,sample_population,reviewer,chain_of_custody_hash
30|assurance_exception_id,finding_category,affected_disclosure,materiality,root_cause,retest_result,closure_proof
31|exception_case_id,exception_type,affected_metric_or_target,owner,due_date,escalation,recurrence_flag
32|offset_governance_id,project_type,registry,serial_number,vintage,additionality,retirement_status
33|certificate_governance_id,certificate_type,registry,generation_period,consumption_period,geography,scope2_claim_eligibility
34|social_metric_id,population_boundary,protected_aggregation_threshold,evidence_requirement,privacy_control,workforce_projection,survey_or_estimate_flag
35|governance_metric_id,policy_link,accountable_body,control_assertion,incident_relationship,training_evidence,narrative_requirement
36|biodiversity_water_waste_id,domain_template,unit_of_measure,boundary_rule,quality_check,disclosure_mapping,materiality_link
37|materiality_assessment_id,stakeholder_group,impact_materiality,financial_materiality,scoring_threshold,approval_state,effective_period
38|stakeholder_approval_id,role_map,approval_matrix,review_cycle,signoff_responsibility,separation_of_duties,waiver_evidence
39|policy_studio_id,policy_template,conflict_detection,impact_simulation,approval_workflow,historical_replay,activation_state
40|parameter_simulation_id,parameter_key,proposed_value,affected_metric_set,affected_packet_set,exception_volume_delta,approval_preview
41|continuous_control_id,control_objective,population,automated_test,sample_result,failure_evidence,retest_date
42|disclosure_proof_id,metric_hash_set,activity_hash_set,factor_hash_set,boundary_hash_set,approval_signature,privacy_preserving_channel
43|audit_reconstruction_id,replay_timestamp,activity_snapshot,factor_snapshot,boundary_snapshot,policy_snapshot,version_lineage_hash
44|anomaly_detection_id,domain_category,baseline_comparison,severity,explanation,root_cause,exception_link
45|governed_model_id,model_purpose,training_data_reference,evaluation_metric,drift_check,bias_fairness_review,rollback_plan
46|agent_skill_id,skill_type,typed_preview,rbac_check,human_confirmation,audit_evidence,crud_reversibility
47|document_ingestion_id,document_type,extracted_record_set,citation_set,confidence,validation_error_set,reversible_mutation_preview
48|boundary_proof_id,external_domain,declared_api_or_event,projection_reference,model_reference,agent_skill_reference,foreign_table_scan
49|role_workbench_id,role_name,view_name,command_set,agent_skill_set,permission_set,capability_visibility
50|release_matrix_id,capability_number,owned_table_set,command_set,route_descriptor,event_contract,release_evidence_check
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    2: ("EnergyUsageRecorded", "ShipmentDelivered"),
    7: ("FacilityProfileChanged", "AssetPlacedInService"),
    10: ("SupplierQualified", "ProcurementSpendClassified"),
    11: ("SupplierQualified",),
    12: ("SupplierQualified",),
    13: ("ShipmentDelivered", "ProcurementSpendClassified"),
    23: ("FacilityProfileChanged", "AssetPlacedInService"),
    26: ("RegulatoryFrameworkChanged", "PolicyChanged"),
    29: ("AssuranceRequestReceived",),
    34: ("WorkforceMetricPublished",),
    40: ("PolicyChanged",),
    43: ("AuditEventSealed", "FinanceClosePeriodLocked"),
    48: ("SupplierQualified", "ShipmentDelivered", "EnergyUsageRecorded", "TravelBooked", "AssetPlacedInService"),
}
_CARBON_ACCOUNTING_FEATURES = (3, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 21, 32, 33, 42, 43, 48, 50)
_DISCLOSURE_ASSURANCE_FEATURES = (1, 16, 25, 26, 27, 28, 29, 30, 31, 38, 41, 42, 43, 49, 50)
_TARGET_RISK_FEATURES = (18, 19, 20, 21, 22, 23, 24, 37, 39, 40, 44, 45, 50)
_SUPPLIER_SOCIAL_GOV_FEATURES = (2, 11, 12, 34, 35, 36, 37, 38, 46, 47, 48, 49, 50)
_AGENT_FEATURES = (5, 12, 21, 25, 26, 39, 40, 44, 45, 46, 47, 49, 50)
_HUMAN_CONFIRMATION_FEATURES = (3, 4, 5, 11, 12, 18, 20, 21, 24, 26, 27, 30, 32, 33, 38, 39, 40, 42, 46, 47, 50)
_APPROVAL_REQUIRED_FEATURES = (4, 7, 18, 20, 24, 26, 27, 30, 32, 33, 38, 39, 40, 42, 50)
_NON_MUTATING_FEATURES = (5, 15, 19, 21, 22, 23, 24, 26, 28, 37, 39, 40, 42, 43, 44, 45, 48, 50)
_PROJECTION_ONLY_FEATURES = (7, 10, 11, 13, 23, 34, 35, 43, 48)


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
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"sustainability_esg_reporting_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"SustainabilityEsgReporting{_camel(capability.slug)}Panel",
        "route": f"POST /sustainability-esg-reporting/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in ESG_CAPABILITIES}


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
        "event_topic": ESG_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "carbon_accounting_evidence_complete": True,
        "disclosure_assurance_evidence_complete": True,
        "target_risk_evidence_complete": True,
        "supplier_social_governance_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned ESG model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if number in _CARBON_ACCOUNTING_FEATURES and payload.get("carbon_accounting_evidence_complete") is not True:
        findings.append("carbon accounting evidence is required for activity completeness, factors, conversions, scopes, supplier categories, attribution, ledger lineage, uncertainty, duplicate prevention, simulations, offsets, certificates, disclosure proofs, audit reconstruction, boundary proof, and release evidence")
    if number in _DISCLOSURE_ASSURANCE_FEATURES and payload.get("disclosure_assurance_evidence_complete") is not True:
        findings.append("disclosure and assurance evidence is required for metric ontology, quality rules, framework mapping, regulatory impact, packets, tie-outs, evidence room, exceptions, stakeholder approvals, continuous controls, proof packets, audit reconstruction, workbenches, and release matrix")
    if number in _TARGET_RISK_FEATURES and payload.get("target_risk_evidence_complete") is not True:
        findings.append("target and climate risk evidence is required for targets, progress decomposition, decarbonization initiatives, scenarios, hazard exposure, transition risk, materiality, policy, parameter simulation, anomaly detection, governed models, and release matrix")
    if number in _SUPPLIER_SOCIAL_GOV_FEATURES and payload.get("supplier_social_governance_evidence_complete") is not True:
        findings.append("supplier, social, governance, document, agent, and role-workbench evidence is required for source registries, supplier confidence/remediation, social metrics, governance metrics, biodiversity/water/waste, materiality, stakeholder governance, agent skills, ingestion, boundary proof, and UI coverage")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("ESG estimates, factor overrides, supplier acceptance, target commitments, simulations, disclosure packets, assurance exceptions, offsets, certificates, approvals, policies, parameters, proofs, and agent CRUD require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("material ESG reporting changes require separated approval for factors, boundaries, targets, initiatives, transition assumptions, regulatory changes, disclosure publication, assurance closure, offsets, certificates, stakeholder approvals, policy activation, parameter changes, proofs, and release gates")
    if number in _AGENT_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("sustainability assistant skills must cite evidence, provide typed reversible previews, enforce RBAC, and block direct CRUD without approval")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("factor explanations, uncertainty propagation, progress decomposition, scenario analysis, risk sensitivity, impact analysis, tie-outs, materiality, policy, parameter, proof, reconstruction, anomaly, model, boundary, and release checks must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("external suppliers, shipments, energy, travel, assets, workforce, finance, and procurement context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != ESG_REQUIRED_EVENT_TOPIC:
        findings.append("sustainability ESG eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in ESG_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary sustainability ESG datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("sustainability ESG controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_sustainability_esg_reporting_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in ESG_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in ESG_DECLARED_DEPENDENCIES)
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
        "required_event_topic": ESG_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": ESG_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "configurable_rules_parameters": True,
        "agent_assisted": True,
        "side_effect_free": True,
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "slug": resolved.slug,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "evidence": evidence,
        "payload_digest": _digest(candidate)[:20],
        "side_effects": (),
    }


def improve1_sustainability_esg_reporting_control_contract() -> dict[str, Any]:
    results = tuple(evaluate_sustainability_esg_reporting_control(capability) for capability in ESG_CAPABILITIES)
    blocking_gaps = tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {
        "format": "appgen.sustainability_esg_reporting.improve1-control-contract.v1",
        "ok": len(results) == 50 and all(item["ok"] for item in results),
        "pbc": PBC_KEY,
        "capability_count": len(results),
        "capabilities": results,
        "owned_tables": ESG_OWNED_TABLES,
        "allowed_database_backends": ESG_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": ESG_REQUIRED_EVENT_TOPIC,
        "declared_dependencies": ESG_DECLARED_DEPENDENCIES,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking_gaps,
        "side_effects": (),
    }


SUSTAINABILITY_ESG_REPORTING_CONTROL_FUNCTIONS = (
    "evaluate_sustainability_esg_reporting_control",
    "improve1_sustainability_esg_reporting_control_contract",
    "sample_payload_for",
)
