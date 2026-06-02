"""Shared standalone blueprint for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from dataclasses import dataclass

PBC_KEY = "sustainability_esg_reporting"
PACKAGE_PATH = "src/pyAppGen/pbcs/sustainability_esg_reporting"
APPGEN_X_TOPIC = f"pbc.{PBC_KEY}.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
UI_FRAGMENTS = (
    "SustainabilityEsgReportingWorkbench",
    "SustainabilityEsgReportingDetail",
    "SustainabilityEsgReportingAssistantPanel",
)
PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
    f"{PBC_KEY}.operate",
)
RELEASE_ARTIFACTS = (
    "__init__.py",
    "agent.py",
    "capability_assurance.py",
    "manifest.py",
    "runtime.py",
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
    "tests/test_contract.py",
)
RULE_DEFINITIONS = (
    {
        "rule_id": "materiality_policy",
        "scope": "materiality",
        "condition": "materiality_threshold_met",
        "description": "Only material metrics and disclosures may progress to filing.",
    },
    {
        "rule_id": "emissions_factor_policy",
        "scope": "carbon",
        "condition": "factor_is_current_and_regionally_valid",
        "description": "Calculations must use current factors for the declared geography and year.",
    },
    {
        "rule_id": "scope_boundary_policy",
        "scope": "boundary",
        "condition": "facility_is_within_approved_scope_boundary",
        "description": "Facilities and suppliers must map to the approved reporting boundary.",
    },
    {
        "rule_id": "renewable_claim_policy",
        "scope": "energy",
        "condition": "certificate_is_retired_before_market_claim",
        "description": "Market-based Scope 2 claims require retired renewable instruments.",
    },
    {
        "rule_id": "assurance_policy",
        "scope": "assurance",
        "condition": "assurance_evidence_and_controls_complete",
        "description": "Disclosure publication requires evidence, controls, and exception review.",
    },
    {
        "rule_id": "target_tracking_policy",
        "scope": "targets",
        "condition": "target_progress_has_latest_actuals",
        "description": "Targets must be tracked with current progress and variance evidence.",
    },
    {
        "rule_id": "disclosure_policy",
        "scope": "disclosure",
        "condition": "board_pack_and_regulator_filing_are_consistent",
        "description": "Board packs and regulator filings must tie out to the same disclosure packet.",
    },
    {
        "rule_id": "data_quality_policy",
        "scope": "quality",
        "condition": "quality_score_is_above_floor",
        "description": "Low-quality records require remediation or approved restatement handling.",
    },
)
PARAMETER_DEFINITIONS = (
    {"key": "quality_score_floor", "scope": "quality", "default": 0.92, "minimum": 0.0, "maximum": 1.0},
    {"key": "target_warning_percent", "scope": "targets", "default": 0.1, "minimum": 0.0, "maximum": 1.0},
    {"key": "factor_expiry_days", "scope": "carbon", "default": 365, "minimum": 30, "maximum": 1825},
    {"key": "assurance_sample_rate", "scope": "assurance", "default": 0.2, "minimum": 0.05, "maximum": 1.0},
    {"key": "materiality_threshold", "scope": "materiality", "default": 0.5, "minimum": 0.0, "maximum": 1.0},
    {"key": "workbench_limit", "scope": "ui", "default": 25, "minimum": 5, "maximum": 100},
    {"key": "certificate_vintage_window_days", "scope": "energy", "default": 450, "minimum": 30, "maximum": 1825},
    {"key": "scenario_shock_limit", "scope": "scenario", "default": 0.35, "minimum": 0.0, "maximum": 1.0},
)
EMITTED_EVENTS = (
    "EsgMetricDefined",
    "MaterialityAssessmentApproved",
    "FacilityProfileRegistered",
    "ActivityDataCaptured",
    "EmissionsCalculated",
    "RenewableInstrumentRecorded",
    "EnvironmentalMetricRecorded",
    "SocialMetricRecorded",
    "GovernanceMetricRecorded",
    "SupplierEsgInputIngested",
    "TargetProgressMeasured",
    "DisclosurePacketBuilt",
    "AssuranceEvidenceAttached",
    "AssuranceExceptionOpened",
    "ClimateScenarioSimulated",
    "BoardPackPrepared",
    "RegulatorFilingSubmitted",
)
CONSUMED_EVENTS = (
    "SupplierQualified",
    "EnergyUsageRecorded",
    "TravelBooked",
    "AssetPlacedInService",
    "PolicyChanged",
    "ShipmentDelivered",
)
STANDARD_FEATURES = (
    "reporting_framework_management",
    "materiality_assessment_workflow",
    "facility_and_activity_data_capture",
    "scope_1_2_3_calculations",
    "renewable_instrument_governance",
    "water_waste_social_governance_metrics",
    "supplier_esg_intake",
    "controls_and_assurance_evidence",
    "restatements_and_targets",
    "scenario_analysis",
    "board_pack_and_regulator_filing_generation",
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
    "forms_wizards_controls",
    "governed_document_instruction_crud_previews",
    "configuration_workbench",
    "continuous_release_assurance",
)
ADVANCED_CAPABILITIES = (
    "carbon_calculation_lineage",
    "supplier_esg_confidence_scoring",
    "renewable_claim_eligibility_checks",
    "water_and_waste_materiality_linking",
    "social_and_governance_metric_evidence_packaging",
    "assurance_anomaly_detection",
    "framework_semantic_mapping",
    "restatement_impact_replay",
    "climate_scenario_transition_risk_simulation",
    "board_pack_drafting",
    "regulator_filing_packager",
    "cryptographic_disclosure_proof",
    "governed_ai_document_mutation_preview",
    "governed_ai_instruction_mutation_preview",
)
NAVIGATION_SECTIONS = (
    "command_center",
    "materiality_and_frameworks",
    "facility_and_activity_data",
    "emissions_and_energy",
    "environmental_metrics",
    "social_and_governance",
    "supplier_network",
    "targets_and_restatements",
    "assurance_and_controls",
    "board_and_regulator",
    "governed_ai",
    "release_evidence",
)


@dataclass(frozen=True)
class TableBlueprint:
    logical_name: str
    description: str
    anchor_field: str | None = None
    anchor_table: str | None = None
    title_hint: str = "title"


BUSINESS_TABLE_BLUEPRINTS = (
    TableBlueprint("esg_metric", "Governed ESG metric ontology with units, ownership, and reporting semantics."),
    TableBlueprint("materiality_assessment", "Double materiality assessments with stakeholder evidence and thresholds."),
    TableBlueprint("reporting_framework_mapping", "Mappings from ESG metrics to framework disclosure requirements.", "metric_id", "esg_metric"),
    TableBlueprint("facility_profile", "Facility and legal entity profile used for operational and reporting boundaries."),
    TableBlueprint("activity_data_record", "Measured or estimated facility, travel, supplier, and product activity data.", "facility_id", "facility_profile"),
    TableBlueprint("emissions_factor", "Approved emissions factors with geography, year, methodology, and expiry.", "metric_id", "esg_metric"),
    TableBlueprint("emissions_calculation", "Scope 1, 2, and 3 carbon calculations with lineage and uncertainty.", "activity_record_id", "activity_data_record"),
    TableBlueprint("scope_boundary", "Operational and equity-share reporting scope boundaries.", "facility_id", "facility_profile"),
    TableBlueprint("renewable_instrument", "Energy attribute certificates and renewable contracts for Scope 2 claims.", "facility_id", "facility_profile"),
    TableBlueprint("water_metric_record", "Water withdrawal, discharge, reuse, and stress-area reporting metrics.", "facility_id", "facility_profile"),
    TableBlueprint("waste_metric_record", "Waste generation, diversion, and hazardous material metrics.", "facility_id", "facility_profile"),
    TableBlueprint("social_metric_record", "Workforce, safety, diversity, training, and human rights metrics.", "metric_id", "esg_metric"),
    TableBlueprint("governance_metric_record", "Governance oversight, policy adoption, ethics, and incident metrics.", "metric_id", "esg_metric"),
    TableBlueprint("supplier_esg_input", "Supplier-provided ESG disclosures, quality scores, and remediation responses.", "metric_id", "esg_metric"),
    TableBlueprint("assurance_control", "Continuous controls and sampling controls over ESG reporting processes.", "metric_id", "esg_metric"),
    TableBlueprint("assurance_evidence", "Evidence room assets with chain-of-custody and sampling metadata.", "metric_id", "esg_metric"),
    TableBlueprint("assurance_exception", "Assurance findings with remediation, retest, and residual risk tracking.", "metric_id", "esg_metric"),
    TableBlueprint("restatement_record", "Period restatements with reason, impact analysis, and approval history.", "metric_id", "esg_metric"),
    TableBlueprint("sustainability_target", "Targets, baselines, target years, and financing or control dependencies.", "metric_id", "esg_metric"),
    TableBlueprint("target_progress", "Periodic progress measurements, variance, and warning posture.", "target_id", "sustainability_target"),
    TableBlueprint("climate_scenario", "Transition and physical climate scenarios with assumptions and stress outputs.", "metric_id", "esg_metric"),
    TableBlueprint("data_quality_check", "Data completeness, reconciliation, and tie-out quality checks.", "metric_id", "esg_metric"),
    TableBlueprint("disclosure_packet", "Disclosure assembly artifact spanning frameworks, evidence, and approvals.", "metric_id", "esg_metric"),
    TableBlueprint("board_pack", "Board reporting pack derived from approved disclosure packets.", "disclosure_packet_id", "disclosure_packet"),
    TableBlueprint("regulator_filing", "Regulator filing package assembled from disclosure packets and evidence.", "disclosure_packet_id", "disclosure_packet"),
    TableBlueprint("governed_document", "Governed AI document previews and approved mutations.", "metric_id", "esg_metric"),
    TableBlueprint("governed_instruction", "Governed AI instruction previews and approved execution plans.", "document_id", "governed_document"),
    TableBlueprint("policy_rule", "Compiled and explainable ESG policy rules."),
    TableBlueprint("runtime_parameter", "Bounded runtime parameters controlling thresholds, limits, and sampling."),
    TableBlueprint("schema_extension", "Owned schema extension registrations for package-local evolution."),
    TableBlueprint("control_assertion", "Control assertions and release gates for the package."),
    TableBlueprint("governed_model", "Governed AI model metadata used for approved assistance."),
)
BUSINESS_TABLES = tuple(f"{PBC_KEY}_{item.logical_name}" for item in BUSINESS_TABLE_BLUEPRINTS)
EVENT_TABLES = (
    f"{PBC_KEY}_appgen_outbox_event",
    f"{PBC_KEY}_appgen_inbox_event",
    f"{PBC_KEY}_appgen_dead_letter_event",
)
RUNTIME_TABLES = BUSINESS_TABLES + EVENT_TABLES

OPERATION_BLUEPRINTS = (
    {"name": "define_esg_metric", "table": "esg_metric", "event": "EsgMetricDefined", "kind": "record"},
    {"name": "assess_materiality", "table": "materiality_assessment", "event": "MaterialityAssessmentApproved", "kind": "record"},
    {"name": "register_facility_profile", "table": "facility_profile", "event": "FacilityProfileRegistered", "kind": "record"},
    {"name": "capture_activity_data", "table": "activity_data_record", "event": "ActivityDataCaptured", "kind": "record"},
    {"name": "register_emissions_factor", "table": "emissions_factor", "event": "EmissionsFactorRegistered", "kind": "record"},
    {"name": "calculate_scope1_emissions", "table": "emissions_calculation", "event": "EmissionsCalculated", "kind": "calculation"},
    {"name": "calculate_scope2_emissions", "table": "emissions_calculation", "event": "EmissionsCalculated", "kind": "calculation"},
    {"name": "calculate_scope3_emissions", "table": "emissions_calculation", "event": "EmissionsCalculated", "kind": "calculation"},
    {"name": "record_renewable_instrument", "table": "renewable_instrument", "event": "RenewableInstrumentRecorded", "kind": "record"},
    {"name": "record_water_metric", "table": "water_metric_record", "event": "EnvironmentalMetricRecorded", "kind": "metric"},
    {"name": "record_waste_metric", "table": "waste_metric_record", "event": "EnvironmentalMetricRecorded", "kind": "metric"},
    {"name": "record_social_metric", "table": "social_metric_record", "event": "SocialMetricRecorded", "kind": "metric"},
    {"name": "record_governance_metric", "table": "governance_metric_record", "event": "GovernanceMetricRecorded", "kind": "metric"},
    {"name": "ingest_supplier_esg_input", "table": "supplier_esg_input", "event": "SupplierEsgInputIngested", "kind": "record"},
    {"name": "define_scope_boundary", "table": "scope_boundary", "event": "ScopeBoundaryDefined", "kind": "record"},
    {"name": "create_sustainability_target", "table": "sustainability_target", "event": "SustainabilityTargetCreated", "kind": "record"},
    {"name": "measure_target_progress", "table": "target_progress", "event": "TargetProgressMeasured", "kind": "progress"},
    {"name": "map_reporting_framework", "table": "reporting_framework_mapping", "event": "FrameworkMappingUpdated", "kind": "record"},
    {"name": "build_disclosure_packet", "table": "disclosure_packet", "event": "DisclosurePacketBuilt", "kind": "packet"},
    {"name": "attach_assurance_evidence", "table": "assurance_evidence", "event": "AssuranceEvidenceAttached", "kind": "record"},
    {"name": "run_assurance_control_test", "table": "assurance_control", "event": "AssuranceControlTested", "kind": "control"},
    {"name": "open_assurance_exception", "table": "assurance_exception", "event": "AssuranceExceptionOpened", "kind": "record"},
    {"name": "record_restatement", "table": "restatement_record", "event": "RestatementRecorded", "kind": "record"},
    {"name": "simulate_climate_scenario", "table": "climate_scenario", "event": "ClimateScenarioSimulated", "kind": "scenario"},
    {"name": "run_data_quality_check", "table": "data_quality_check", "event": "DataQualityCheckRun", "kind": "quality"},
    {"name": "prepare_board_pack", "table": "board_pack", "event": "BoardPackPrepared", "kind": "packet"},
    {"name": "file_regulator_filing", "table": "regulator_filing", "event": "RegulatorFilingSubmitted", "kind": "packet"},
    {"name": "compile_esg_rule", "table": "policy_rule", "event": "EsgRuleCompiled", "kind": "rule"},
    {"name": "preview_governed_document_change", "table": "governed_document", "event": "GovernedDocumentPreviewed", "kind": "preview"},
    {"name": "preview_governed_instruction_change", "table": "governed_instruction", "event": "GovernedInstructionPreviewed", "kind": "preview"},
)
DOMAIN_OPERATIONS = tuple(item["name"] for item in OPERATION_BLUEPRINTS)
OPERATION_INDEX = {item["name"]: item for item in OPERATION_BLUEPRINTS}

ROUTE_DEFINITIONS = (
    {"method": "POST", "path": "/metrics", "operation": "define_esg_metric"},
    {"method": "POST", "path": "/materiality-assessments", "operation": "assess_materiality"},
    {"method": "POST", "path": "/facilities", "operation": "register_facility_profile"},
    {"method": "POST", "path": "/activity-data", "operation": "capture_activity_data"},
    {"method": "POST", "path": "/emissions-factors", "operation": "register_emissions_factor"},
    {"method": "POST", "path": "/emissions-calculations/scope1", "operation": "calculate_scope1_emissions"},
    {"method": "POST", "path": "/emissions-calculations/scope2", "operation": "calculate_scope2_emissions"},
    {"method": "POST", "path": "/emissions-calculations/scope3", "operation": "calculate_scope3_emissions"},
    {"method": "POST", "path": "/renewable-instruments", "operation": "record_renewable_instrument"},
    {"method": "POST", "path": "/targets", "operation": "create_sustainability_target"},
    {"method": "POST", "path": "/disclosure-packets", "operation": "build_disclosure_packet"},
    {"method": "POST", "path": "/board-packs", "operation": "prepare_board_pack"},
    {"method": "POST", "path": "/regulator-filings", "operation": "file_regulator_filing"},
    {"method": "POST", "path": "/agent/document-plan", "operation": "preview_governed_document_change"},
    {"method": "POST", "path": "/agent/crud-plan", "operation": "preview_governed_instruction_change"},
    {"method": "GET", "path": "/sustainability-esg-reporting-workbench", "operation": "query_workbench"},
)
FORM_DEFINITIONS = (
    {"id": "esg_metric_intake", "title": "ESG metric intake", "operation": "define_esg_metric", "fields": ("tenant", "code", "metric_name", "category", "framework", "unit", "materiality_score")},
    {"id": "facility_activity_capture", "title": "Facility activity capture", "operation": "capture_activity_data", "fields": ("tenant", "facility_id", "activity_type", "period", "quantity", "unit", "source_type")},
    {"id": "renewable_claim_form", "title": "Renewable claim eligibility", "operation": "record_renewable_instrument", "fields": ("tenant", "facility_id", "certificate_type", "registry", "vintage_year", "retired")},
    {"id": "disclosure_packet_form", "title": "Disclosure packet builder", "operation": "build_disclosure_packet", "fields": ("tenant", "metric_id", "report_type", "period", "frameworks", "approval_owner")},
    {"id": "regulator_filing_form", "title": "Regulator filing", "operation": "file_regulator_filing", "fields": ("tenant", "disclosure_packet_id", "regulator", "jurisdiction", "filing_deadline")},
)
WIZARD_DEFINITIONS = (
    {"id": "double_materiality", "title": "Double materiality assessment", "steps": ("stakeholders", "impact_scoring", "financial_scoring", "approval")},
    {"id": "scope_coverage", "title": "Scope coverage wizard", "steps": ("boundary", "facilities", "activity_data", "factor_selection", "quality_gate")},
    {"id": "disclosure_and_board_pack", "title": "Disclosure and board-pack wizard", "steps": ("tie_out", "evidence", "assurance", "board_pack", "regulator_filing")},
    {"id": "restatement_and_replay", "title": "Restatement replay wizard", "steps": ("root_cause", "prior_period_impact", "approval", "republication")},
)
CONTROL_DEFINITIONS = (
    {"id": "policy_rule_editor", "type": "rule-editor", "targets": tuple(item["rule_id"] for item in RULE_DEFINITIONS)},
    {"id": "runtime_parameter_editor", "type": "parameter-editor", "targets": tuple(item["key"] for item in PARAMETER_DEFINITIONS)},
    {"id": "assurance_control_console", "type": "control-console", "targets": ("run_assurance_control_test", "open_assurance_exception")},
    {"id": "agent_mutation_guard", "type": "approval-guard", "targets": ("preview_governed_document_change", "preview_governed_instruction_change")},
    {"id": "event_replay_console", "type": "event-console", "targets": EVENT_TABLES},
)


def owned_table(logical_name: str) -> str:
    return logical_name if logical_name.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{logical_name}"


def business_table_for_operation(operation: str) -> str:
    spec = OPERATION_INDEX[operation]
    return owned_table(spec["table"])


def table_blueprint_by_table(table: str) -> TableBlueprint | None:
    logical_name = table.removeprefix(f"{PBC_KEY}_")
    for item in BUSINESS_TABLE_BLUEPRINTS:
        if item.logical_name == logical_name:
            return item
    return None
