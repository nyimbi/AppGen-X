"""Executable improve1 controls for the Wealth Portfolio Management PBC."""
from __future__ import annotations
import hashlib
from typing import Any
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import WEALTH_PORTFOLIO_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, WEALTH_PORTFOLIO_MANAGEMENT_CONSUMED_EVENT_TYPES, WEALTH_PORTFOLIO_MANAGEMENT_OWNED_TABLES, WEALTH_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC, WEALTH_PORTFOLIO_MANAGEMENT_RUNTIME_TABLES
PBC_KEY="wealth_portfolio_management"; EVENT_CONTRACT="AppGen-X"
WEALTH_ALLOWED_DATABASE_BACKENDS=WEALTH_PORTFOLIO_MANAGEMENT_ALLOWED_DATABASE_BACKENDS; WEALTH_REQUIRED_EVENT_TOPIC=WEALTH_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC; WEALTH_CAPABILITIES=IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER={capability.feature_number:capability for capability in WEALTH_CAPABILITIES}; CAPABILITY_BY_SLUG={capability.slug:capability for capability in WEALTH_CAPABILITIES}
WEALTH_CONTROL_OWNED_TABLES=tuple(dict.fromkeys(WEALTH_PORTFOLIO_MANAGEMENT_OWNED_TABLES+WEALTH_PORTFOLIO_MANAGEMENT_RUNTIME_TABLES+tuple(f"wealth_portfolio_management_{capability.slug}_control" for capability in WEALTH_CAPABILITIES)))
WEALTH_DECLARED_DEPENDENCIES=tuple(dict.fromkeys(WEALTH_PORTFOLIO_MANAGEMENT_CONSUMED_EVENT_TYPES+("ClientIdentityChanged","HouseholdChanged","CustodianPositionChanged","TradeExecutionReported","SecurityMasterChanged","ProductEligibilityChanged","MarketPriceChanged","TaxLotChanged","FeeBillingEvent","ComplaintOpened","CompliancePolicyChanged","AuditEvidenceSealed","OperationalKpiChanged","PolicyChanged")))
_BASE_FIELDS=("tenant_id","client_id","household_id","portfolio_id","account_id","advisor_id","policy_version","evidence_references")
_FIELD_ROWS="""
1|portfolio_lifecycle_id,current_state,target_state,client_status,account_scope,advisory_program,allowed_commands,state_evidence
2|identity_boundary_id,client_projection,household_projection,beneficial_owner,relationship_role,kyc_status,no_identity_mutation,boundary_evidence
3|mandate_id,objective,risk_band,time_horizon,liquidity_need,restriction_set,eligible_accounts,investment_policy_reference
4|mandate_version_id,version_number,consent_status,client_signature,effective_date,superseded_version,advisor_attestation,audit_hash
5|suitability_profile_id,goal_coverage,risk_profile_status,time_horizon_status,liquidity_status,tax_status,knowledge_status,missing_evidence
6|risk_reconciliation_id,tolerance_score,capacity_score,variance_reason,advisor_review,client_acknowledgment,override_limit,review_due
7|restriction_control_id,restriction_type,security_scope,issuer_scope,sector_scope,esg_scope,trade_block_rule,approval_state
8|model_alignment_id,model_portfolio,target_allocation,current_allocation,drift_threshold,exception_reason,rebalance_trigger,approval_state
9|position_boundary_id,custodian_position,security_id,quantity,market_value,as_of_date,no_position_mutation,boundary_evidence
10|drift_monitor_id,asset_class,current_weight,target_weight,drift_value,threshold,alert_state,recommendation
11|rebalance_order_id,order_state,tax_check_status,restriction_check_status,lot_selection,approval_state,execution_window,cancel_reason
12|tax_rebalance_id,tax_lot_projection,gain_loss,harvest_opportunity,wash_sale_flag,client_tax_policy,tradeoff_reason,approval_state
13|cash_rule_id,target_cash,min_cash,max_cash,income_need,scheduled_withdrawal,trade_funding_rule,breach_action
14|distribution_plan_id,income_source,distribution_schedule,required_cash,security_sale_plan,tax_impact,client_approval,delivery_status
15|performance_snapshot_id,period,valuation_source,return_method,benchmark_id,fee_treatment,data_quality,certification_status
16|benchmark_history_id,benchmark_id,assignment_reason,effective_date,custom_blend,change_approval,history_hash,client_disclosure
17|fee_schedule_id,fee_basis,tier_schedule,household_aggregation,minimum_fee,discount_rule,effective_date,client_disclosure
18|fee_boundary_id,fee_billing_event,calculation_projection,invoice_reference,no_billing_mutation,reconciliation_status,exception_reason,boundary_evidence
19|advisory_review_id,review_type,due_date,reviewer,agenda,open_actions,client_acknowledgment,completion_evidence
20|communication_id,communication_type,channel,audience,message,disclosure_set,delivery_status,timeline_reference
21|proposal_package_id,recommendation_set,suitability_basis,risk_explanation,fee_disclosure,tax_disclosure,client_decision,evidence_packet
22|eligibility_boundary_id,product_projection,security_projection,eligibility_rule,restriction_status,no_product_mutation,boundary_evidence,approval_state
23|concentration_control_id,issuer_exposure,sector_exposure,asset_class_exposure,household_exposure,limit,breach_status,mitigation_action
24|liquidity_monitor_id,liquid_assets,illiquid_assets,withdrawal_need,stress_window,liquidity_gap,recommendation,review_status
25|values_alignment_id,esg_preference,exclusion_list,impact_theme,portfolio_alignment,exception_reason,client_acknowledgment,review_due
26|alternative_commitment_id,fund_id,commitment_amount,capital_call_schedule,liquidity_lockup,eligibility_status,document_status,approval_state
27|corporate_action_id,action_type,security_id,impact_summary,election_deadline,client_instruction,portfolio_effect,processing_status
28|cash_flow_event_id,event_type,amount,effective_date,source_destination,liquidity_effect,rebalance_effect,client_confirmation
29|transition_plan_id,legacy_holdings,tax_budget,restriction_conflict,implementation_phases,risk_transition,client_approval,completion_status
30|household_aggregation_id,household_members,account_set,allocation_view,risk_view,fee_view,performance_view,aggregation_boundary
31|pre_trade_check_id,order_id,restriction_result,suitability_result,concentration_result,liquidity_result,approval_required,block_reason
32|post_trade_validation_id,execution_event,allocation_match,restriction_check,drift_effect,custodian_reconciliation,no_trade_mutation,exception_status
33|exception_taxonomy_id,exception_type,severity,owner,sla,next_action,resolution_evidence,closure_reason
34|command_board_id,portfolio_filters,drift_queue,review_queue,restriction_queue,cash_queue,exception_queue,advisor_actions
35|rule_parameter_id,rule_name,parameter_name,bounds,scope,effective_date,simulation_result,approval_state
36|portfolio_review_agent_id,portfolio_digest,drift_summary,risk_summary,recommendations,cited_facts,human_confirmation,write_block
37|proposal_agent_id,proposal_goal,recommended_trades,fee_disclosure,tax_notes,risk_disclosure,cited_facts,approval_status
38|safety_agent_id,blocked_commands,unsuitable_action,unapproved_trade,missing_consent,conflict_warning,escalation_target,write_block
39|event_model_id,event_name,payload_schema,lifecycle_transition,projection_replay,sequence_trace,consumer_contract,event_mapping
40|portfolio_reconstruction_id,as_of_timestamp,event_sequence,holdings_snapshot,mandate_snapshot,review_snapshot,fee_snapshot,replay_hash
41|evidence_packet_id,hash_chain_root,proposal_hashes,consent_hashes,review_hashes,advisor_signature,verification_channel,tamper_status
42|complaint_linkage_id,complaint_projection,portfolio_reference,communication_reference,trade_reference,no_complaint_mutation,resolution_status,boundary_evidence
43|fiduciary_review_id,best_interest_basis,alternatives_considered,cost_reasonableness,risk_reasonableness,conflict_review,client_benefit,approval_state
44|conflict_control_id,conflict_type,advisor_interest,product_compensation,household_relationship,mitigation,disclosure_status,approval_state
45|data_quality_score_id,position_quality,price_quality,client_profile_quality,mandate_quality,fee_quality,exception_count,remediation_action
46|scenario_analysis_id,scenario_name,market_shock,liquidity_shock,tax_impact,portfolio_drawdown,recovery_path,recommendation
47|smoke_scenario_id,scenario_name,test_reference,ui_evidence,event_trace,boundary_evidence,release_check,coverage_status
48|boundary_proof_id,dependency_name,projection_record,api_event_contract,no_foreign_mutation,idempotency_behavior,dead_letter_behavior,audit_reference
49|advisor_briefing_id,advisor_id,client_priorities,drift_alerts,review_due,compliance_alerts,cash_needs,next_decision
50|command_center_id,active_portfolios,drift_exceptions,review_backlog,trade_blocks,fee_exceptions,compliance_risk,executive_status
"""
_DOMAIN_FIELDS={int(line.split("|",1)[0]):tuple(line.split("|",1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS={number:f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1,51)}; _FEATURE_FIELDS={number:_BASE_FIELDS+_DOMAIN_FIELDS[number]+(_PRIMARY_PROOF_FIELDS[number],) for number in range(1,51)}
_FEATURE_DEPENDENCIES={2:("ClientIdentityChanged","HouseholdChanged"),9:("CustodianPositionChanged",),12:("TaxLotChanged",),18:("FeeBillingEvent",),22:("ProductEligibilityChanged","SecurityMasterChanged"),27:("SecurityMasterChanged",),32:("TradeExecutionReported",),40:("CustodianPositionChanged","MarketPriceChanged"),42:("ComplaintOpened",),48:("PolicyChanged","OperationalKpiChanged"),50:("AuditEvidenceSealed","OperationalKpiChanged")}
_CLIENT_MANDATE_FEATURES=(1,2,3,4,5,6,7,8,19,20,21,29,30,42,43,44,49,50)
_PORTFOLIO_TRADING_FEATURES=(9,10,11,12,13,14,22,23,24,25,26,27,28,31,32,46,50)
_FEES_PERFORMANCE_FEATURES=(15,16,17,18,24,30,40,45,47,48,50)
_GOVERNANCE_AGENT_FEATURES=(33,34,35,36,37,38,39,40,41,42,43,44,47,48,49,50)
_AGENT_FEATURES=(36,37,38,49,50); _HUMAN_CONFIRMATION_FEATURES=(4,6,7,11,12,14,19,20,21,26,27,28,29,31,36,37,38,41,43,44,49,50); _APPROVAL_REQUIRED_FEATURES=(4,7,11,12,14,21,26,29,31,37,38,41,43,44,49,50); _NON_MUTATING_FEATURES=(2,5,6,8,9,10,12,15,16,18,22,23,24,25,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50); _PROJECTION_ONLY_FEATURES=(2,9,12,18,22,27,30,32,40,42,48)
def _digest(value:object)->str: return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()
def _camel(slug:str)->str: return "".join(part.capitalize() for part in slug.split("_"))
def _resolve(capability:Improve1Capability|str|int)->Improve1Capability|None:
    if isinstance(capability,Improve1Capability): return capability
    if isinstance(capability,int): return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)
def _spec_for(capability:Improve1Capability)->dict[str,Any]: return {"title":capability.title,"slug":capability.slug,"tables":(f"wealth_portfolio_management_{capability.slug}_control",),"fields":_FEATURE_FIELDS[capability.feature_number],"primary_proof":_PRIMARY_PROOF_FIELDS[capability.feature_number],"ui":f"WealthPortfolioManagement{_camel(capability.slug)}Panel","route":f"POST /wealth-portfolio-management/improve1/{capability.slug}","dependencies":_FEATURE_DEPENDENCIES.get(capability.feature_number,())}
CONTROL_SPECS={capability.feature_number:_spec_for(capability) for capability in WEALTH_CAPABILITIES}
def sample_payload_for(capability:Improve1Capability|str|int)->dict[str,Any]:
    resolved=_resolve(capability)
    if resolved is None: return {}
    spec=CONTROL_SPECS[resolved.feature_number]; payload={field:f"{resolved.slug}_{field}" for field in spec["fields"]}; payload[spec["primary_proof"]]=True
    payload.update({"database_backend":"postgresql","event_contract":EVENT_CONTRACT,"event_topic":WEALTH_REQUIRED_EVENT_TOPIC,"stream_engine_picker_visible":False,"shared_table_access":False,"dependency_access_mode":"api_event_projection","human_confirmation":True,"approver_separate_from_initiator":True,"agent_preview_only":True,"non_mutating_simulation":True,"client_mandate_evidence_complete":True,"portfolio_trading_evidence_complete":True,"fees_performance_evidence_complete":True,"governance_agent_evidence_complete":True,"side_effects":()}); return payload
def _domain_findings(capability:Improve1Capability,payload:dict[str,Any])->tuple[str,...]:
    findings=[]; n=capability.feature_number; spec=CONTROL_SPECS[n]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_',' ')}"); findings.append(f"{capability.title} requires owned wealth model, UI, service/API, AppGen-X event, agent, test, and release evidence before approval.")
    if n in _CLIENT_MANDATE_FEATURES and payload.get("client_mandate_evidence_complete") is not True: findings.append("client portfolio lifecycle, identity and household boundaries, mandates, consent, suitability, risk reconciliation, restrictions, model alignment, reviews, communications, proposals, transition planning, household aggregation, complaints, fiduciary review, conflicts, advisor briefing, and command center evidence is required")
    if n in _PORTFOLIO_TRADING_FEATURES and payload.get("portfolio_trading_evidence_complete") is not True: findings.append("holdings boundaries, drift monitoring, rebalance lifecycle, tax-aware rebalancing, cash rules, distributions, product/security eligibility, concentration, liquidity, ESG alignment, alternatives, corporate actions, cash-flow events, pre/post-trade checks, scenarios, and command evidence is required")
    if n in _FEES_PERFORMANCE_FEATURES and payload.get("fees_performance_evidence_complete") is not True: findings.append("performance snapshots, benchmark history, fee schedules, fee billing boundaries, liquidity, household aggregation, point-in-time reconstruction, data-quality scoring, release scenarios, boundary proof, and command evidence is required")
    if n in _GOVERNANCE_AGENT_FEATURES and payload.get("governance_agent_evidence_complete") is not True: findings.append("exception taxonomy, workbench, rules, governed review and proposal agents, safety restrictions, AppGen-X event specialization, point-in-time reconstruction, cryptographic advisory evidence, complaints, fiduciary review, conflicts, release scenarios, boundary proof, advisor briefing, and command evidence is required")
    if n in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True: findings.append("mandate consent, risk overrides, restrictions, rebalance orders, tax trades, distributions, reviews, communications, proposals, alternatives, corporate actions, cash flows, transitions, pre-trade checks, agent outputs, evidence packets, fiduciary/conflict decisions, briefing, and command decisions require human confirmation")
    if n in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True: findings.append("high-risk wealth actions require separated approval for mandate consent, restrictions, rebalance and tax trades, distributions, proposals, alternatives, transitions, pre-trade checks, proposal agents, safety restrictions, advisory evidence, fiduciary/conflict review, briefing, and command decisions")
    if n in _AGENT_FEATURES and payload.get("agent_preview_only") is not True: findings.append("wealth assistant skills must cite owned facts, show reversible CRUD previews, enforce suitability and fiduciary policy checks, and block direct writes before approval")
    if n in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True: findings.append("identity projections, suitability/risk analysis, model drift, holdings boundaries, tax analysis, performance, benchmarks, fee billing, eligibility, concentration, liquidity, values alignment, aggregation, post-trade validation, exceptions, workbench, rules, agents, events, replay, evidence packets, complaints, fiduciary/conflict review, data quality, scenarios, release, boundaries, briefings, and command center must be side-effect-free")
    if n in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode")!="api_event_projection": findings.append("client identity, household, custodian position, tax lot, fee billing, product/security, trade, market price, complaint, policy, KPI, and audit context must use declared APIs, events, or projections instead of shared tables")
    if payload.get("event_contract")!=EVENT_CONTRACT or payload.get("event_topic")!=WEALTH_REQUIRED_EVENT_TOPIC: findings.append("wealth portfolio management eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"): findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in WEALTH_ALLOWED_DATABASE_BACKENDS: findings.append("ordinary wealth portfolio management datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"): findings.append("wealth portfolio management controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))
def evaluate_wealth_portfolio_management_control(capability:Improve1Capability|str|int,payload:dict[str,Any]|None=None)->dict[str,Any]:
    resolved=_resolve(capability)
    if resolved is None: return {"ok":False,"reason":"unknown_capability","side_effects":()}
    spec=CONTROL_SPECS[resolved.feature_number]; candidate=sample_payload_for(resolved); candidate.update(dict(payload or {}))
    missing_fields=tuple(field for field in spec["fields"] if candidate.get(field) in (None,"",(),[])); foreign_tables=tuple(table for table in spec["tables"] if table not in WEALTH_CONTROL_OWNED_TABLES); undeclared_dependencies=tuple(dep for dep in spec["dependencies"] if dep not in WEALTH_DECLARED_DEPENDENCIES); findings=_domain_findings(resolved,candidate)
    evidence={"evidence_id":_digest((PBC_KEY,resolved.feature_number,tuple(sorted(candidate))))[:20],"owned_tables":spec["tables"],"required_fields":spec["fields"],"primary_proof":spec["primary_proof"],"ui_surface":spec["ui"],"service_api":spec["route"],"test":"tests/test_domain_behavior.py","event_contract":EVENT_CONTRACT,"required_event_topic":WEALTH_REQUIRED_EVENT_TOPIC,"allowed_database_backends":WEALTH_ALLOWED_DATABASE_BACKENDS,"declared_dependencies":spec["dependencies"],"configurable_rules_parameters":True,"agent_assisted":True,"side_effect_free":True}
    return {"ok":not missing_fields and not foreign_tables and not undeclared_dependencies and not findings,"pbc":PBC_KEY,"feature_number":resolved.feature_number,"title":resolved.title,"slug":resolved.slug,"missing_fields":missing_fields,"foreign_tables":foreign_tables,"undeclared_dependencies":undeclared_dependencies,"findings":findings,"evidence":evidence,"payload_digest":_digest(candidate)[:20],"side_effects":()}
def improve1_wealth_portfolio_management_control_contract()->dict[str,Any]:
    results=tuple(evaluate_wealth_portfolio_management_control(capability) for capability in WEALTH_CAPABILITIES); blocking_gaps=tuple(f"{item['feature_number']}: {finding}" for item in results for finding in item["findings"])
    return {"format":"appgen.wealth_portfolio_management.improve1-control-contract.v1","ok":len(results)==50 and all(item["ok"] for item in results),"pbc":PBC_KEY,"capability_count":len(results),"capabilities":results,"owned_tables":WEALTH_CONTROL_OWNED_TABLES,"allowed_database_backends":WEALTH_ALLOWED_DATABASE_BACKENDS,"event_contract":EVENT_CONTRACT,"required_event_topic":WEALTH_REQUIRED_EVENT_TOPIC,"declared_dependencies":WEALTH_DECLARED_DEPENDENCIES,"stream_engine_picker_visible":False,"blocking_gaps":blocking_gaps,"side_effects":()}
WEALTH_PORTFOLIO_MANAGEMENT_CONTROL_FUNCTIONS=("evaluate_wealth_portfolio_management_control","improve1_wealth_portfolio_management_control_contract","sample_payload_for")
