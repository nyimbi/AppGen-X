CREATE SCHEMA IF NOT EXISTS procurement_sourcing;

CREATE TABLE procurement_sourcing_purchase_requisition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  requisition_id VARCHAR(255) PRIMARY KEY NOT NULL,
  legal_entity VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  estimated_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_purchase_requisition_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  requisition_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  uom VARCHAR(255) NOT NULL,
  required_date TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (requisition_id) REFERENCES procurement_sourcing_purchase_requisition(requisition_id)
);

CREATE TABLE procurement_sourcing_requisition_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_id VARCHAR(255) PRIMARY KEY NOT NULL,
  requisition_id VARCHAR(255) PRIMARY KEY NOT NULL,
  approver VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (requisition_id) REFERENCES procurement_sourcing_purchase_requisition(requisition_id)
);

CREATE TABLE procurement_sourcing_requisition_budget_check (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  budget_check_id VARCHAR(255) PRIMARY KEY NOT NULL,
  requisition_id VARCHAR(255) PRIMARY KEY NOT NULL,
  budget_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_category_strategy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  strategy_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  category VARCHAR(255) NOT NULL,
  preferred_method VARCHAR(255) NOT NULL,
  risk_weight VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_category_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  category VARCHAR(255) NOT NULL,
  approval_limit VARCHAR(255) NOT NULL,
  minimum_bid_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supplier_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supplier_identity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  identity_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  did VARCHAR(255) NOT NULL,
  issuer VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (supplier_id) REFERENCES procurement_sourcing_supplier_profile(supplier_id)
);

CREATE TABLE procurement_sourcing_supplier_site (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  site_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  country VARCHAR(255) NOT NULL,
  lead_time_days VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (supplier_id) REFERENCES procurement_sourcing_supplier_profile(supplier_id)
);

CREATE TABLE procurement_sourcing_supplier_qualification (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  qualification_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  category VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supplier_risk_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  signal_type VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_preferred_supplier_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  preferred_policy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  category VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  priority VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_rfq (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rfq_id VARCHAR(255) PRIMARY KEY NOT NULL,
  requisition_id VARCHAR(255) PRIMARY KEY NOT NULL,
  category VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  released_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (requisition_id) REFERENCES procurement_sourcing_purchase_requisition(requisition_id)
);

CREATE TABLE procurement_sourcing_rfq_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rfq_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rfq_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  target_price VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (rfq_id) REFERENCES procurement_sourcing_rfq(rfq_id)
);

CREATE TABLE procurement_sourcing_supplier_invitation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  invitation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rfq_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  sent_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supplier_bid (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  bid_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rfq_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  price VARCHAR(255) NOT NULL,
  lead_time_days VARCHAR(255) NOT NULL,
  risk VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (rfq_id) REFERENCES procurement_sourcing_rfq(rfq_id)
);

CREATE TABLE procurement_sourcing_supplier_bid_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  bid_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  bid_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rfq_line_id VARCHAR(255) NOT NULL,
  price VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (bid_id) REFERENCES procurement_sourcing_supplier_bid(bid_id)
);

CREATE TABLE procurement_sourcing_bid_normalization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  normalization_id VARCHAR(255) PRIMARY KEY NOT NULL,
  bid_id VARCHAR(255) PRIMARY KEY NOT NULL,
  normalized_price VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supplier_scorecard (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scorecard_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  rfq_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  award_confidence DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supplier_award (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  award_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rfq_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (rfq_id) REFERENCES procurement_sourcing_rfq(rfq_id)
);

CREATE TABLE procurement_sourcing_split_award (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  split_award_id VARCHAR(255) PRIMARY KEY NOT NULL,
  award_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  clearing_bid VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_vendor_contract (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  contract_id VARCHAR(255) PRIMARY KEY NOT NULL,
  award_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  term_months INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (award_id) REFERENCES procurement_sourcing_supplier_award(award_id)
);

CREATE TABLE procurement_sourcing_contract_clause (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  clause_id VARCHAR(255) PRIMARY KEY NOT NULL,
  contract_id VARCHAR(255) PRIMARY KEY NOT NULL,
  clause_type VARCHAR(255) NOT NULL,
  obligation VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (contract_id) REFERENCES procurement_sourcing_vendor_contract(contract_id)
);

CREATE TABLE procurement_sourcing_contract_compliance_obligation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  obligation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  contract_id VARCHAR(255) PRIMARY KEY NOT NULL,
  metric VARCHAR(255) NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_contract_renewal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  renewal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  contract_id VARCHAR(255) PRIMARY KEY NOT NULL,
  renewal_date TIMESTAMP NOT NULL,
  decision VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_purchase_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  po_id VARCHAR(255) PRIMARY KEY NOT NULL,
  contract_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (contract_id) REFERENCES procurement_sourcing_vendor_contract(contract_id)
);

CREATE TABLE procurement_sourcing_purchase_order_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  po_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  po_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item_id VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  price VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (po_id) REFERENCES procurement_sourcing_purchase_order(po_id)
);

CREATE TABLE procurement_sourcing_change_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  change_order_id VARCHAR(255) PRIMARY KEY NOT NULL,
  po_id VARCHAR(255) PRIMARY KEY NOT NULL,
  change_type VARCHAR(255) NOT NULL,
  amount_delta DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_po_tolerance_check (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tolerance_check_id VARCHAR(255) PRIMARY KEY NOT NULL,
  po_id VARCHAR(255) PRIMARY KEY NOT NULL,
  contract_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_payment_terms (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  payment_terms_id VARCHAR(255) PRIMARY KEY NOT NULL,
  contract_id VARCHAR(255) PRIMARY KEY NOT NULL,
  term_code VARCHAR(255) NOT NULL,
  discount_rate DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_material_shortage_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_vendor_performance_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_budget_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supplier_risk_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_contract_compliance_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_access_policy_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_purchase_order_route (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supplier_compliance_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_carbon_sourcing_selection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_award_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_rfq_mechanism_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_bid_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_supply_exposure_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_price_lead_time_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_sourcing_strategy_simulation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_parsed_document (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE procurement_sourcing_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
