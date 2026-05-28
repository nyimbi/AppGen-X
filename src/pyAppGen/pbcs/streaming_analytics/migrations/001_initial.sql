CREATE SCHEMA IF NOT EXISTS streaming_analytics;

CREATE TABLE streaming_analytics_metric_stream (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  stream_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  metric_field VARCHAR(255) NOT NULL,
  aggregation VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_aggregation_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  window_id VARCHAR(255) PRIMARY KEY NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  window_minutes VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (stream_id) REFERENCES streaming_analytics_metric_stream(stream_id)
);

CREATE TABLE streaming_analytics_kpi_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  event_count INTEGER NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (stream_id) REFERENCES streaming_analytics_metric_stream(stream_id)
);

CREATE TABLE streaming_analytics_dashboard_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  stream_ids VARCHAR(255) NOT NULL,
  snapshot_count INTEGER NOT NULL,
  latest_values VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (stream_ids) REFERENCES streaming_analytics_metric_stream(stream_id)
);

CREATE TABLE streaming_analytics_metric_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  values VARCHAR(255) NOT NULL,
  quality_score DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_ingestion_checkpoint (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  checkpoint_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source VARCHAR(255) NOT NULL,
  last_event_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_data_quality_result (
  tenant VARCHAR(255) NOT NULL,
  quality_result_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  quality_score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_replay_job (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  replay_job_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source VARCHAR(255) NOT NULL,
  from_event_id VARCHAR(255) NOT NULL,
  to_event_id VARCHAR(255) NOT NULL,
  batch_limit VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_watermark_state (
  tenant VARCHAR(255) NOT NULL,
  watermark_id VARCHAR(255) PRIMARY KEY NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  watermark_seconds VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_retention_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  retention_days VARCHAR(255) NOT NULL,
  eligible_event_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_threshold_alert (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  alert_id VARCHAR(255) PRIMARY KEY NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  snapshot_value VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_metric_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  forecast_id VARCHAR(255) PRIMARY KEY NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  horizon_minutes VARCHAR(255) NOT NULL,
  base_value VARCHAR(255) NOT NULL,
  forecast_value VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_operational_risk_score (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_id VARCHAR(255) PRIMARY KEY NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  risk_band VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_metric_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  resolution VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_window_recomputation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  recomputation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  window_id VARCHAR(255) NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  event_count INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_kpi_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) PRIMARY KEY NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  control_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_kpi_snapshot_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  snapshot_hash VARCHAR(255) NOT NULL,
  event_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_metric_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  metric_field VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  policy_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_analytics_audit_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  audit_id VARCHAR(255) PRIMARY KEY NOT NULL,
  action VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  payload TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_analytics_federation_view (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  view_id VARCHAR(255) PRIMARY KEY NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  metric_field VARCHAR(255) NOT NULL,
  latest_value VARCHAR(255) NOT NULL,
  projection_sources VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE streaming_analytics_analytics_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  model_type VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  training_boundary VARCHAR(255) NOT NULL,
  governance_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
