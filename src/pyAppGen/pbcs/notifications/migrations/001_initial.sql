CREATE SCHEMA IF NOT EXISTS notifications;

CREATE TABLE notifications_notification_template (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  template_id VARCHAR(255) NOT NULL,
  message_type VARCHAR(255) NOT NULL,
  locale VARCHAR(64) NOT NULL,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  required_variables TEXT NOT NULL,
  status VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (template_id)
);

CREATE TABLE notifications_template_locale_variant (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  variant_id VARCHAR(255) NOT NULL,
  template_id VARCHAR(255) NOT NULL,
  locale VARCHAR(64) NOT NULL,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  status VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (template_id) REFERENCES notifications_notification_template(template_id)
);

CREATE TABLE notifications_delivery_channel (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  channel_id VARCHAR(255) NOT NULL,
  channel_type VARCHAR(64) NOT NULL,
  provider VARCHAR(255) NOT NULL,
  health_score DECIMAL(12, 6) NOT NULL,
  cost_score DECIMAL(12, 6) NOT NULL,
  status VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (channel_id)
);

CREATE TABLE notifications_notification_recipient (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  recipient_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  preferred_channels TEXT NOT NULL,
  locale VARCHAR(64) NOT NULL,
  opt_in BOOLEAN NOT NULL,
  status VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_preference_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  opt_in BOOLEAN NOT NULL,
  preferred_channels TEXT NOT NULL,
  locale VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_consent_ledger (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  consent_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  source_event_type VARCHAR(255) NOT NULL,
  opt_in BOOLEAN NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_delivery_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255),
  campaign_id VARCHAR(255),
  scheduled_for VARCHAR(255) NOT NULL,
  quiet_hours_enforced BOOLEAN NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_throttle_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  window_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) NOT NULL,
  message_count INTEGER NOT NULL,
  max_messages INTEGER NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_provider_route (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  route_id VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) NOT NULL,
  channel_id VARCHAR(255) NOT NULL,
  provider VARCHAR(255) NOT NULL,
  channel_type VARCHAR(64) NOT NULL,
  route_score DECIMAL(12, 6) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_message_delivery (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  template_id VARCHAR(255) NOT NULL,
  channel_id VARCHAR(255) NOT NULL,
  message_type VARCHAR(64) NOT NULL,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  delivery_risk DECIMAL(12, 6) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (delivery_id),
  FOREIGN KEY (template_id) REFERENCES notifications_notification_template(template_id),
  FOREIGN KEY (channel_id) REFERENCES notifications_delivery_channel(channel_id)
);

CREATE TABLE notifications_delivery_attempt (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  attempt_id VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) NOT NULL,
  provider VARCHAR(255) NOT NULL,
  provider_status VARCHAR(255) NOT NULL,
  attempt_number INTEGER NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  FOREIGN KEY (delivery_id) REFERENCES notifications_message_delivery(delivery_id)
);

CREATE TABLE notifications_retry_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  retry_id VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  retry_limit INTEGER NOT NULL,
  next_action VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_delivery_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) NOT NULL,
  provider_status VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  FOREIGN KEY (delivery_id) REFERENCES notifications_message_delivery(delivery_id)
);

CREATE TABLE notifications_bounce_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  bounce_id VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) NOT NULL,
  bounce_type VARCHAR(64) NOT NULL,
  provider_status VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  FOREIGN KEY (delivery_id) REFERENCES notifications_message_delivery(delivery_id)
);

CREATE TABLE notifications_notification_campaign (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  campaign_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  message_type VARCHAR(64) NOT NULL,
  scheduled_for VARCHAR(255) NOT NULL,
  locale VARCHAR(64) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  UNIQUE (campaign_id)
);

CREATE TABLE notifications_campaign_dispatch (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  dispatch_id VARCHAR(255) NOT NULL,
  campaign_id VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) NOT NULL,
  channel_id VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  FOREIGN KEY (campaign_id) REFERENCES notifications_notification_campaign(campaign_id),
  FOREIGN KEY (delivery_id) REFERENCES notifications_message_delivery(delivery_id)
);

CREATE TABLE notifications_transactional_notification (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  transactional_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  template_id VARCHAR(255) NOT NULL,
  delivery_id VARCHAR(255) NOT NULL,
  message_type VARCHAR(64) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  FOREIGN KEY (delivery_id) REFERENCES notifications_message_delivery(delivery_id)
);

CREATE TABLE notifications_notification_audit_log (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  audit_id VARCHAR(255) NOT NULL,
  operation VARCHAR(255) NOT NULL,
  payload_hash VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_deliverability_analytics (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  analytics_id VARCHAR(255) NOT NULL,
  delivery_count INTEGER NOT NULL,
  delivered_count INTEGER NOT NULL,
  failed_count INTEGER NOT NULL,
  bounce_count INTEGER NOT NULL,
  success_rate DECIMAL(12, 6) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_notification_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  consent_policy TEXT NOT NULL,
  delivery_policy TEXT NOT NULL,
  throttle_policy TEXT NOT NULL,
  routing_policy TEXT NOT NULL,
  schedule_policy TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_notification_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value DECIMAL(18, 6) NOT NULL,
  lower_bound DECIMAL(18, 6) NOT NULL,
  upper_bound DECIMAL(18, 6) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_notification_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(64) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit INTEGER NOT NULL,
  supported_locales TEXT NOT NULL,
  supported_channels TEXT NOT NULL,
  quiet_hours TEXT NOT NULL,
  stream_engine_picker_visible BOOLEAN NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE notifications_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE notifications_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  reason TEXT NOT NULL,
  status VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
