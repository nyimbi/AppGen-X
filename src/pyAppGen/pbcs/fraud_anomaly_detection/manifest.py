"""Manifest for the Fraud Anomaly Detection PBC."""

from .runtime import FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES
from .runtime import FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES
from .runtime import FRAUD_ANOMALY_DETECTION_OWNED_TABLES
from .runtime import FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS
from .runtime import FRAUD_ANOMALY_DETECTION_STANDARD_FEATURE_KEYS
from .runtime import FRAUD_ANOMALY_DETECTION_SUPPORTED_CONFIGURATION_FIELDS


PBC_KEY = 'fraud_anomaly_detection'

PBC_MANIFEST = {
    'pbc': 'fraud_anomaly_detection',
    'label': 'Anomalous Activity and Fraud Detection',
    'mesh': 'intelligence',
    'description': (
        'Behavior baselines, identity graph risk, anomaly scores, fraud rules, '
        'decision explanations, loss exposure, analyst queues, and operational '
        'risk flags for checkout, payment, and access-policy activity.'
    ),
    'datastore_backend': 'postgresql',
    'tables': FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
    'apis': (
        'POST /risk-events',
        'POST /fraud-checks',
        'GET /risk-cases',
        'GET /risk-workbench',
        'POST /fraud-rules',
        'POST /risk-signals/{id}/score',
        'POST /risk-cases',
        'POST /fraud-configuration',
        'POST /fraud-parameters',
    ),
    'emits': FRAUD_ANOMALY_DETECTION_EMITTED_EVENT_TYPES,
    'consumes': FRAUD_ANOMALY_DETECTION_CONSUMED_EVENT_TYPES,
    'template': None,
    'ui_fragments': (
        'FraudAnomalyDetectionWorkbench',
        'RiskSignalMonitor',
        'AnomalyScoreBoard',
        'FraudRuleStudio',
        'RiskCaseConsole',
        'IdentityLinkAnalysisPanel',
        'BehaviorBaselinePanel',
        'DeviceFingerprintPanel',
        'NetworkIndicatorPanel',
        'VelocityWindowPanel',
        'DecisionExplanationConsole',
        'LossExposurePanel',
        'AnalystQueueConsole',
        'FraudParameterConsole',
        'FraudConfigurationPanel',
        'RiskEventInbox',
        'RiskEventOutbox',
        'RiskDeadLetterQueue',
    ),
    'permissions': (
        'fraud_anomaly_detection.read',
        'fraud_anomaly_detection.event.write',
        'fraud_anomaly_detection.anomaly_score.write',
        'fraud_anomaly_detection.fraud_rule.write',
        'fraud_anomaly_detection.risk_case.write',
        'fraud_anomaly_detection.event.consume',
        'fraud_anomaly_detection.configure',
        'fraud_anomaly_detection.audit',
    ),
    'configuration': FRAUD_ANOMALY_DETECTION_SUPPORTED_CONFIGURATION_FIELDS,
    'capabilities': tuple(f'fraud_anomaly_detection.{table}' for table in FRAUD_ANOMALY_DETECTION_OWNED_TABLES),
    'standard_features': FRAUD_ANOMALY_DETECTION_STANDARD_FEATURE_KEYS,
    'workflows': (
        'configure_runtime',
        'set_parameter',
        'register_rule',
        'register_schema_extension',
        'register_fraud_rule',
        'ingest_risk_signal',
        'score_anomaly',
        'open_risk_case',
        'receive_event',
        'build_workbench_view',
    ),
    'analytics': (
        'risk_precision',
        'risk_recall',
        'case_open_rate',
        'false_positive_rate',
        'decision_latency',
        'loss_exposure',
        'drift_score',
        'identity_link_density',
        'velocity_alert_rate',
        'fraud_risk_scored_throughput',
        'risk_case_opened_throughput',
    ),
    'advanced_capabilities': FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS,
    'migrations': ('migrations/001_initial.sql',),
    'seed_data': ('seed_data.py',),
    'tests': ('tests/test_contract.py',),
    'docs': ('SPECIFICATION.md', 'RELEASE_EVIDENCE.md'),
}
