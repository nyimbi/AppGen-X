"""One-PBC application surface for fraud anomaly detection operations."""

from __future__ import annotations

import hashlib


PBC_KEY = "fraud_anomaly_detection"
OWNED_TABLES = (
    "fraud_anomaly_detection_risk_signal",
    "fraud_anomaly_detection_anomaly_score",
    "fraud_anomaly_detection_fraud_rule",
    "fraud_anomaly_detection_risk_case",
    "fraud_anomaly_detection_identity_link",
    "fraud_anomaly_detection_behavior_baseline",
    "fraud_anomaly_detection_device_fingerprint",
    "fraud_anomaly_detection_network_indicator",
    "fraud_anomaly_detection_velocity_window",
    "fraud_anomaly_detection_decision_explanation",
    "fraud_anomaly_detection_loss_exposure",
    "fraud_anomaly_detection_analyst_queue_item",
    "fraud_anomaly_detection_fraud_parameter",
    "fraud_anomaly_detection_fraud_configuration",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def fraud_anomaly_detection_forms_contract() -> dict:
    """Return database-backed forms for a one-PBC fraud operations app."""
    forms = (
        {"form_id": "risk_signal_intake_form", "writes_table": "fraud_anomaly_detection_risk_signal", "command": "ingest_risk_signal", "fields": ("tenant", "signal_id", "subject_id", "signal_type", "source", "amount", "occurred_at", "payload_hash"), "validations": ("source_supported", "subject_projection_bound", "payload_hash_required", "idempotency_key_required")},
        {"form_id": "anomaly_score_form", "writes_table": "fraud_anomaly_detection_anomaly_score", "command": "score_anomaly", "fields": ("tenant", "score_id", "signal_id", "risk_score", "model_version", "threshold", "decision", "explainability_ref"), "validations": ("risk_score_in_range", "threshold_bound", "model_version_active", "explanation_required")},
        {"form_id": "fraud_rule_form", "writes_table": "fraud_anomaly_detection_fraud_rule", "command": "register_fraud_rule", "fields": ("tenant", "rule_id", "rule_type", "risk_domain", "condition", "action", "status", "effective_at"), "validations": ("rule_compiles_to_hash", "false_positive_simulation_required", "rollback_plan_required")},
        {"form_id": "risk_case_form", "writes_table": "fraud_anomaly_detection_risk_case", "command": "open_risk_case", "fields": ("tenant", "case_id", "subject_id", "score_id", "priority", "case_type", "owner", "status"), "validations": ("priority_supported", "owner_required", "case_deduplication_checked", "sla_started")},
        {"form_id": "identity_link_form", "writes_table": "fraud_anomaly_detection_identity_link", "command": "link_identity", "fields": ("tenant", "link_id", "subject_id", "linked_subject_id", "link_type", "confidence", "evidence_hash", "status"), "validations": ("no_self_link", "confidence_in_range", "evidence_hash_required", "privacy_policy_checked")},
        {"form_id": "behavior_baseline_form", "writes_table": "fraud_anomaly_detection_behavior_baseline", "command": "update_behavior_baseline", "fields": ("tenant", "baseline_id", "subject_id", "metric", "baseline_value", "decay_days", "sample_count", "status"), "validations": ("minimum_sample_count", "decay_policy_bound", "metric_supported")},
        {"form_id": "device_fingerprint_form", "writes_table": "fraud_anomaly_detection_device_fingerprint", "command": "record_device_fingerprint", "fields": ("tenant", "device_id", "subject_id", "fingerprint_hash", "risk_tags", "first_seen", "last_seen", "status"), "validations": ("fingerprint_hash_required", "sensitive_fields_tokenized", "device_reuse_checked")},
        {"form_id": "network_indicator_form", "writes_table": "fraud_anomaly_detection_network_indicator", "command": "record_network_indicator", "fields": ("tenant", "indicator_id", "subject_id", "ip_hash", "asn", "geo_risk", "proxy_signal", "status"), "validations": ("ip_hash_required", "geo_risk_in_range", "proxy_signal_classified")},
        {"form_id": "velocity_window_form", "writes_table": "fraud_anomaly_detection_velocity_window", "command": "calculate_velocity_window", "fields": ("tenant", "window_id", "subject_id", "metric", "count", "window_seconds", "limit", "status"), "validations": ("window_seconds_positive", "limit_declared", "velocity_policy_bound")},
        {"form_id": "decision_explanation_form", "writes_table": "fraud_anomaly_detection_decision_explanation", "command": "explain_decision", "fields": ("tenant", "explanation_id", "score_id", "top_factors", "counterfactual", "appeal_guidance", "audit_hash", "status"), "validations": ("top_factors_required", "counterfactual_safe", "appeal_guidance_required")},
        {"form_id": "loss_exposure_form", "writes_table": "fraud_anomaly_detection_loss_exposure", "command": "project_loss_exposure", "fields": ("tenant", "exposure_id", "case_id", "exposure_amount", "currency", "confidence", "mitigation", "status"), "validations": ("currency_required", "confidence_in_range", "mitigation_required_for_high_loss")},
        {"form_id": "analyst_queue_form", "writes_table": "fraud_anomaly_detection_analyst_queue_item", "command": "enqueue_analyst_case", "fields": ("tenant", "queue_item_id", "case_id", "queue", "priority", "skills_required", "assigned_to", "status"), "validations": ("case_exists", "skills_matched", "priority_queue_policy_checked")},
        {"form_id": "fraud_governance_form", "writes_table": "fraud_anomaly_detection_fraud_configuration", "command": "configure_runtime", "fields": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "scoring_mode", "status"), "validations": ("database_backend_allowed", "event_contract_appgen_x", "stream_picker_hidden", "approval_required")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def fraud_anomaly_detection_wizards_contract() -> dict:
    """Return guided workflows for fraud analysts, risk operations, and policy owners."""
    wizards = (
        {"wizard_id": "risk_signal_triage_wizard", "steps": ("ingest_signal", "deduplicate_subject", "score_anomaly", "explain_decision", "decide_case_open"), "completion_event": "FraudRiskScored"},
        {"wizard_id": "analyst_case_investigation_wizard", "steps": ("open_case", "review_identity_links", "review_device_and_network", "estimate_loss", "record_disposition"), "completion_event": "RiskCaseOpened"},
        {"wizard_id": "identity_graph_risk_wizard", "steps": ("link_subjects", "score_link_confidence", "detect_ring_pattern", "apply_privacy_policy", "publish_link_evidence"), "completion_event": "IdentityRiskLinked"},
        {"wizard_id": "velocity_policy_wizard", "steps": ("select_metric", "calculate_window", "compare_limit", "simulate_threshold", "activate_rule"), "completion_event": "VelocityPolicyActivated"},
        {"wizard_id": "device_network_enrichment_wizard", "steps": ("capture_device", "tokenize_network", "classify_proxy", "update_baseline", "feed_anomaly_score"), "completion_event": "RiskSignalEnriched"},
        {"wizard_id": "false_positive_review_wizard", "steps": ("sample_cases", "review_explanations", "adjust_threshold", "register_rule_change", "monitor_precision"), "completion_event": "FraudRuleTuned"},
        {"wizard_id": "fraud_release_control_wizard", "steps": ("draft_configuration", "simulate_loss_impact", "approve_change", "activate_policy", "monitor_dead_letters"), "completion_event": "FraudPolicyChanged"},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def fraud_anomaly_detection_controls_contract() -> dict:
    """Return fraud controls for precision, privacy, explainability, and operational resilience."""
    controls = (
        {"control_id": "risk_signal_idempotency_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_risk_signal", "fraud_anomaly_detection_anomaly_score")},
        {"control_id": "model_threshold_and_false_positive_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_anomaly_score", "fraud_anomaly_detection_fraud_rule")},
        {"control_id": "case_sla_and_deduplication_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_risk_case", "fraud_anomaly_detection_analyst_queue_item")},
        {"control_id": "identity_privacy_and_link_evidence_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_identity_link", "fraud_anomaly_detection_behavior_baseline")},
        {"control_id": "device_network_tokenization_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_device_fingerprint", "fraud_anomaly_detection_network_indicator")},
        {"control_id": "velocity_window_policy_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_velocity_window", "fraud_anomaly_detection_fraud_parameter")},
        {"control_id": "decision_explainability_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_decision_explanation", "fraud_anomaly_detection_anomaly_score")},
        {"control_id": "loss_exposure_mitigation_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_loss_exposure", "fraud_anomaly_detection_risk_case")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("fraud_anomaly_detection_appgen_outbox_event", "fraud_anomaly_detection_appgen_inbox_event", "fraud_anomaly_detection_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_fraud_anomaly_detection_app_contract() -> dict:
    """Return evidence that this PBC can stand alone as a fraud operations app."""
    forms = fraud_anomaly_detection_forms_contract()["forms"]
    wizards = fraud_anomaly_detection_wizards_contract()["wizards"]
    controls = fraud_anomaly_detection_controls_contract()["controls"]
    return {"ok": bool(forms) and bool(wizards) and bool(controls), "pbc": PBC_KEY, "single_pbc_app": True, "database_backed": True, "allowed_database_backends": ("postgresql", "mysql", "mariadb"), "owned_tables": OWNED_TABLES, "forms": forms, "wizards": wizards, "controls": controls, "workbench": "FraudAnomalyDetectionWorkbench", "assistant_panel": "FraudAnomalyDetectionAgent", "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "side_effects": ()}


def document_instruction_fraud_anomaly_detection_plan(document: str, instructions: str) -> dict:
    """Map fraud documents and instructions to governed CRUD previews."""
    text = f"{document} {instructions}".lower()
    if "case" in text or "investigat" in text or "analyst" in text:
        operation, table = "open_risk_case", "fraud_anomaly_detection_risk_case"
    elif "identity" in text or "link" in text or "ring" in text:
        operation, table = "link_identity", "fraud_anomaly_detection_identity_link"
    elif "device" in text or "fingerprint" in text:
        operation, table = "record_device_fingerprint", "fraud_anomaly_detection_device_fingerprint"
    elif "network" in text or "proxy" in text or "ip" in text:
        operation, table = "record_network_indicator", "fraud_anomaly_detection_network_indicator"
    elif "velocity" in text or "window" in text or "burst" in text:
        operation, table = "calculate_velocity_window", "fraud_anomaly_detection_velocity_window"
    elif "explain" in text or "reason" in text or "appeal" in text:
        operation, table = "explain_decision", "fraud_anomaly_detection_decision_explanation"
    elif "loss" in text or "exposure" in text or "mitigation" in text:
        operation, table = "project_loss_exposure", "fraud_anomaly_detection_loss_exposure"
    elif "queue" in text or "assign" in text or "skill" in text:
        operation, table = "enqueue_analyst_case", "fraud_anomaly_detection_analyst_queue_item"
    elif "rule" in text or "threshold" in text or "policy" in text:
        operation, table = "register_fraud_rule", "fraud_anomaly_detection_fraud_rule"
    elif "score" in text or "anomaly" in text or "risk" in text:
        operation, table = "score_anomaly", "fraud_anomaly_detection_anomaly_score"
    else:
        operation, table = "ingest_risk_signal", "fraud_anomaly_detection_risk_signal"
    return {"ok": True, "pbc": PBC_KEY, "document_digest": _digest(document, instructions), "proposed_operation": operation, "target_table": table, "requires_human_confirmation": True, "crud_datastore_mutation": True, "event_contract": "AppGen-X", "side_effects": ()}


def app_surface_smoke_test() -> dict:
    """Exercise standalone fraud app contracts."""
    app = single_pbc_fraud_anomaly_detection_app_contract()
    case_plan = document_instruction_fraud_anomaly_detection_plan("suspicious checkout", "open analyst case")
    identity_plan = document_instruction_fraud_anomaly_detection_plan("identity ring evidence", "link subjects")
    checks = (app["ok"], len(app["forms"]) >= 13, len(app["wizards"]) >= 7, len(app["controls"]) >= 10, case_plan["target_table"] == "fraud_anomaly_detection_risk_case", identity_plan["target_table"] == "fraud_anomaly_detection_identity_link", all(table.startswith("fraud_anomaly_detection_") for control in app["controls"] for table in control["table_scope"]))
    return {"ok": all(checks), "single_pbc_app": app, "document_plans": (case_plan, identity_plan), "side_effects": ()}
