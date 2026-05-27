CREATE SCHEMA IF NOT EXISTS streaming_analytics;

CREATE TABLE streaming_analytics_metric_stream (
  id INTEGER PRIMARY KEY NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  metric_field VARCHAR(255) NOT NULL,
  aggregation VARCHAR(64) NOT NULL,
  region VARCHAR(64) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (stream_id)
);

CREATE TABLE streaming_analytics_aggregation_window (
  id INTEGER PRIMARY KEY NOT NULL,
  window_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  window_minutes INTEGER NOT NULL,
  watermark_seconds INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (window_id),
  FOREIGN KEY (stream_id) REFERENCES streaming_analytics_metric_stream(stream_id)
);

CREATE TABLE streaming_analytics_kpi_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  stream_id VARCHAR(255) NOT NULL,
  value DECIMAL(18, 6) NOT NULL,
  event_count INTEGER NOT NULL,
  confidence DECIMAL(18, 6) NOT NULL,
  forecast_value DECIMAL(18, 6),
  audit_proof VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (snapshot_id),
  FOREIGN KEY (stream_id) REFERENCES streaming_analytics_metric_stream(stream_id)
);

CREATE TABLE streaming_analytics_dashboard_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  projection_id VARCHAR(255) NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  stream_ids TEXT NOT NULL,
  latest_values TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (projection_id)
);

CREATE TABLE streaming_analytics_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  contract VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  retry_policy TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE streaming_analytics_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  handler VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE streaming_analytics_dead_letter_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  handler VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
