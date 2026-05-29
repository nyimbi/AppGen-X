"""Generated release evidence for the eam PBC."""

import importlib.util
from pathlib import Path

from .app_surface import app_surface_smoke_test, single_pbc_eam_app_contract


RELEASE_EVIDENCE = {'format': 'appgen.eam-release-evidence.v1', 'ok': True, 'checks': ({'id': 'owned_schema_depth', 'ok': True}, {'id': 'migration_per_owned_table', 'ok': True}, {'id': 'service_command_depth', 'ok': True}, {'id': 'api_event_contract', 'ok': True}, {'id': 'permissions_cover_commands', 'ok': True}, {'id': 'backend_allowlist', 'ok': True}, {'id': 'no_shared_table_access', 'ok': True}, {'id': 'ui_workbench_evidence', 'ok': True}), 'schema': {'format': 'appgen.eam-owned-schema-contract.v1', 'ok': True, 'tables': ({'table': 'equipment', 'fields': ('tenant', 'equipment_id', 'site', 'asset_tag', 'criticality', 'location', 'parent_equipment_id', 'warranty_until', 'status'), 'primary_key': ('equipment_id', 'parent_equipment_id'), 'owned_by': 'eam'}, {'table': 'maintenance_plan', 'fields': ('tenant', 'plan_id', 'equipment_id', 'strategy', 'interval_days', 'meter_threshold', 'condition_threshold', 'status'), 'primary_key': ('plan_id', 'equipment_id'), 'owned_by': 'eam'}, {'table': 'work_order', 'fields': ('tenant', 'work_order_id', 'equipment_id', 'plan_id', 'work_type', 'priority', 'risk_score', 'status'), 'primary_key': ('work_order_id', 'equipment_id'), 'owned_by': 'eam'}, {'table': 'spare_part_usage', 'fields': ('tenant', 'usage_id', 'work_order_id', 'part_number', 'quantity', 'unit_cost', 'cost'), 'primary_key': ('usage_id', 'work_order_id'), 'owned_by': 'eam'}, {'table': 'condition_reading', 'fields': ('tenant', 'reading_id', 'equipment_id', 'sensor', 'value', 'unit', 'risk_score', 'alarm'), 'primary_key': ('reading_id', 'equipment_id'), 'owned_by': 'eam'}, {'table': 'meter_reading', 'fields': ('tenant', 'meter_id', 'equipment_id', 'meter_name', 'value', 'unit', 'triggered_plans'), 'primary_key': ('meter_id', 'equipment_id'), 'owned_by': 'eam'}, {'table': 'failure_event', 'fields': ('tenant', 'failure_event_id', 'equipment_id', 'failure_code', 'downtime_hours', 'severity', 'recorded_at'), 'primary_key': ('failure_event_id', 'equipment_id'), 'owned_by': 'eam'}, {'table': 'maintenance_schedule', 'fields': ('tenant', 'schedule_id', 'work_order_id', 'technician', 'scheduled_start', 'scheduled_end', 'carbon_score', 'status'), 'primary_key': ('schedule_id', 'work_order_id'), 'owned_by': 'eam'}, {'table': 'service_vendor_event', 'fields': ('tenant', 'vendor_event_id', 'work_order_id', 'vendor_id', 'sla_state', 'warranty_recovery', 'status'), 'primary_key': ('vendor_event_id', 'work_order_id'), 'owned_by': 'eam'}, {'table': 'safety_permit', 'fields': ('tenant', 'permit_id', 'equipment_id', 'permit_type', 'risk_score', 'approved_by', 'status'), 'primary_key': ('permit_id', 'equipment_id'), 'owned_by': 'eam'}, {'table': 'maintenance_rule', 'fields': ('tenant', 'rule_id', 'rule_type', 'status', 'eligible_work_types', 'allowed_sites', 'compiled_hash'), 'primary_key': ('rule_id',), 'owned_by': 'eam'}, {'table': 'maintenance_parameter', 'fields': ('tenant', 'parameter_id', 'name', 'value', 'bounds', 'compiled_hash'), 'primary_key': ('parameter_id',), 'owned_by': 'eam'}, {'table': 'maintenance_configuration', 'fields': ('tenant', 'configuration_id', 'database_backend', 'event_topic', 'retry_limit', 'default_timezone'), 'primary_key': ('configuration_id',), 'owned_by': 'eam'}, {'table': 'maintenance_outbox', 'fields': ('tenant', 'event_id', 'event_type', 'topic', 'idempotency_key', 'audit_hash'), 'primary_key': ('event_id',), 'owned_by': 'eam'}, {'table': 'maintenance_inbox', 'fields': ('tenant', 'event_id', 'event_type', 'idempotency_key', 'attempts', 'status'), 'primary_key': ('event_id',), 'owned_by': 'eam'}, {'table': 'maintenance_dead_letter', 'fields': ('tenant', 'event_id', 'event_type', 'idempotency_key', 'attempts', 'reason'), 'primary_key': ('event_id',), 'owned_by': 'eam'}), 'relationships': ({'from': 'maintenance_plan.equipment_id', 'to': 'equipment.equipment_id', 'type': 'owned_plan'}, {'from': 'work_order.equipment_id', 'to': 'equipment.equipment_id', 'type': 'owned_execution'}, {'from': 'work_order.plan_id', 'to': 'maintenance_plan.plan_id', 'type': 'owned_trigger'}, {'from': 'condition_reading.equipment_id', 'to': 'equipment.equipment_id', 'type': 'owned_reading'}, {'from': 'meter_reading.equipment_id', 'to': 'equipment.equipment_id', 'type': 'owned_reading'}, {'from': 'safety_permit.equipment_id', 'to': 'equipment.equipment_id', 'type': 'owned_safety'}, {'from': 'spare_part_usage.work_order_id', 'to': 'work_order.work_order_id', 'type': 'owned_consumption'}, {'from': 'maintenance_schedule.work_order_id', 'to': 'work_order.work_order_id', 'type': 'owned_schedule'}, {'from': 'service_vendor_event.work_order_id', 'to': 'work_order.work_order_id', 'type': 'owned_vendor_flow'}), 'migrations': ({'path': 'pbcs/eam/migrations/001_equipment.sql', 'operation': 'create_owned_table', 'table': 'equipment', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/002_maintenance_plan.sql', 'operation': 'create_owned_table', 'table': 'maintenance_plan', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/003_work_order.sql', 'operation': 'create_owned_table', 'table': 'work_order', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/004_spare_part_usage.sql', 'operation': 'create_owned_table', 'table': 'spare_part_usage', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/005_condition_reading.sql', 'operation': 'create_owned_table', 'table': 'condition_reading', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/006_meter_reading.sql', 'operation': 'create_owned_table', 'table': 'meter_reading', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/007_failure_event.sql', 'operation': 'create_owned_table', 'table': 'failure_event', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/008_maintenance_schedule.sql', 'operation': 'create_owned_table', 'table': 'maintenance_schedule', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/009_service_vendor_event.sql', 'operation': 'create_owned_table', 'table': 'service_vendor_event', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/010_safety_permit.sql', 'operation': 'create_owned_table', 'table': 'safety_permit', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/011_maintenance_rule.sql', 'operation': 'create_owned_table', 'table': 'maintenance_rule', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/012_maintenance_parameter.sql', 'operation': 'create_owned_table', 'table': 'maintenance_parameter', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/013_maintenance_configuration.sql', 'operation': 'create_owned_table', 'table': 'maintenance_configuration', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/014_maintenance_outbox.sql', 'operation': 'create_owned_table', 'table': 'maintenance_outbox', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/015_maintenance_inbox.sql', 'operation': 'create_owned_table', 'table': 'maintenance_inbox', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/eam/migrations/016_maintenance_dead_letter.sql', 'operation': 'create_owned_table', 'table': 'maintenance_dead_letter', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}), 'models': ({'class_name': 'Equipment', 'table': 'equipment', 'fields': ('tenant', 'equipment_id', 'site', 'asset_tag', 'criticality', 'location', 'parent_equipment_id', 'warranty_until', 'status')}, {'class_name': 'MaintenancePlan', 'table': 'maintenance_plan', 'fields': ('tenant', 'plan_id', 'equipment_id', 'strategy', 'interval_days', 'meter_threshold', 'condition_threshold', 'status')}, {'class_name': 'WorkOrder', 'table': 'work_order', 'fields': ('tenant', 'work_order_id', 'equipment_id', 'plan_id', 'work_type', 'priority', 'risk_score', 'status')}, {'class_name': 'SparePartUsage', 'table': 'spare_part_usage', 'fields': ('tenant', 'usage_id', 'work_order_id', 'part_number', 'quantity', 'unit_cost', 'cost')}, {'class_name': 'ConditionReading', 'table': 'condition_reading', 'fields': ('tenant', 'reading_id', 'equipment_id', 'sensor', 'value', 'unit', 'risk_score', 'alarm')}, {'class_name': 'MeterReading', 'table': 'meter_reading', 'fields': ('tenant', 'meter_id', 'equipment_id', 'meter_name', 'value', 'unit', 'triggered_plans')}, {'class_name': 'FailureEvent', 'table': 'failure_event', 'fields': ('tenant', 'failure_event_id', 'equipment_id', 'failure_code', 'downtime_hours', 'severity', 'recorded_at')}, {'class_name': 'MaintenanceSchedule', 'table': 'maintenance_schedule', 'fields': ('tenant', 'schedule_id', 'work_order_id', 'technician', 'scheduled_start', 'scheduled_end', 'carbon_score', 'status')}, {'class_name': 'ServiceVendorEvent', 'table': 'service_vendor_event', 'fields': ('tenant', 'vendor_event_id', 'work_order_id', 'vendor_id', 'sla_state', 'warranty_recovery', 'status')}, {'class_name': 'SafetyPermit', 'table': 'safety_permit', 'fields': ('tenant', 'permit_id', 'equipment_id', 'permit_type', 'risk_score', 'approved_by', 'status')}, {'class_name': 'MaintenanceRule', 'table': 'maintenance_rule', 'fields': ('tenant', 'rule_id', 'rule_type', 'status', 'eligible_work_types', 'allowed_sites', 'compiled_hash')}, {'class_name': 'MaintenanceParameter', 'table': 'maintenance_parameter', 'fields': ('tenant', 'parameter_id', 'name', 'value', 'bounds', 'compiled_hash')}, {'class_name': 'MaintenanceConfiguration', 'table': 'maintenance_configuration', 'fields': ('tenant', 'configuration_id', 'database_backend', 'event_topic', 'retry_limit', 'default_timezone')}, {'class_name': 'MaintenanceOutbox', 'table': 'maintenance_outbox', 'fields': ('tenant', 'event_id', 'event_type', 'topic', 'idempotency_key', 'audit_hash')}, {'class_name': 'MaintenanceInbox', 'table': 'maintenance_inbox', 'fields': ('tenant', 'event_id', 'event_type', 'idempotency_key', 'attempts', 'status')}, {'class_name': 'MaintenanceDeadLetter', 'table': 'maintenance_dead_letter', 'fields': ('tenant', 'event_id', 'event_type', 'idempotency_key', 'attempts', 'reason')}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False}, 'service': {'format': 'appgen.eam-service-contract.v1', 'ok': True, 'transaction_boundary': 'eam_owned_datastore_plus_appgen_outbox', 'command_methods': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'register_equipment', 'create_maintenance_plan', 'record_condition_reading', 'record_meter_reading', 'create_safety_permit', 'create_work_order', 'schedule_work_order', 'issue_spare_part', 'complete_work_order', 'run_control_tests', 'register_governed_model'), 'query_methods': ('build_workbench_view', 'simulate_strategy', 'forecast_failures', 'parse_maintenance_instruction', 'score_maintenance_risk', 'recommend_exception_resolution', 'route_maintenance', 'generate_compliance_proof', 'screen_policy', 'federate_maintenance_view', 'verify_equipment_identity', 'run_resilience_drill', 'schedule_carbon_aware_maintenance', 'optimize_maintenance_schedule', 'allocate_labor_and_spares', 'detect_failure_anomaly', 'model_stochastic_maintenance_exposure', 'verify_owned_table_boundary'), 'mutates_only': ('equipment', 'maintenance_plan', 'work_order', 'spare_part_usage', 'condition_reading', 'meter_reading', 'failure_event', 'maintenance_schedule', 'service_vendor_event', 'safety_permit', 'maintenance_rule', 'maintenance_parameter', 'maintenance_configuration', 'maintenance_outbox', 'maintenance_inbox', 'maintenance_dead_letter'), 'external_dependencies': {'apis': ('GET /production/orders/{id}', 'GET /quality/nonconformances/{id}', 'GET /inventory/spares/{id}', 'GET /procurement/vendors/{id}', 'POST /audit/maintenance-events'), 'events': ('DowntimeCaptured', 'NonConformanceRaised', 'InventoryReservationConfirmed', 'PurchaseOrderAcknowledged', 'AssetLifecycleUpdated'), 'api_projections': ('production_uptime_projection', 'quality_reliability_projection', 'inventory_spares_projection', 'procurement_vendor_projection', 'asset_lifecycle_projection'), 'shared_tables': ()}}, 'api': {'format': 'appgen.eam-api-contract.v1', 'ok': True, 'pbc': 'eam', 'owned_tables': ('equipment', 'maintenance_plan', 'work_order', 'spare_part_usage', 'condition_reading', 'meter_reading', 'failure_event', 'maintenance_schedule', 'service_vendor_event', 'safety_permit', 'maintenance_rule', 'maintenance_parameter', 'maintenance_configuration', 'maintenance_outbox', 'maintenance_inbox', 'maintenance_dead_letter'), 'database_backends': ('postgresql', 'mysql', 'mariadb'), 'event_contract': 'AppGen-X', 'required_event_topic': 'appgen.maintenance.events', 'shared_table_access': False, 'stream_engine_picker_visible': False, 'routes': ('POST /equipment', 'POST /maintenance-plans', 'POST /work-orders', 'POST /work-orders/{id}/schedule', 'POST /work-orders/{id}/complete', 'POST /condition-readings', 'POST /meter-readings', 'POST /spare-usage', 'POST /safety-permits', 'GET /maintenance-workbench', 'POST /maintenance-rules', 'POST /maintenance-parameters', 'POST /maintenance-configuration'), 'route_definitions': ({'method': 'POST', 'path': '/equipment', 'command': 'register_equipment'}, {'method': 'POST', 'path': '/maintenance-plans', 'command': 'create_maintenance_plan'}, {'method': 'POST', 'path': '/work-orders', 'command': 'create_work_order'}, {'method': 'POST', 'path': '/work-orders/{id}/schedule', 'command': 'schedule_work_order'}, {'method': 'POST', 'path': '/work-orders/{id}/complete', 'command': 'complete_work_order'}, {'method': 'POST', 'path': '/condition-readings', 'command': 'record_condition_reading'}, {'method': 'POST', 'path': '/meter-readings', 'command': 'record_meter_reading'}, {'method': 'POST', 'path': '/spare-usage', 'command': 'issue_spare_part'}, {'method': 'POST', 'path': '/safety-permits', 'command': 'create_safety_permit'}, {'method': 'GET', 'path': '/maintenance-workbench', 'query': 'build_workbench_view'}, {'method': 'POST', 'path': '/maintenance-rules', 'command': 'register_rule'}, {'method': 'POST', 'path': '/maintenance-parameters', 'command': 'set_parameter'}, {'method': 'POST', 'path': '/maintenance-configuration', 'command': 'configure_runtime'}), 'events': {'emits': ('EquipmentRegistered', 'MaintenancePlanReleased', 'ConditionReadingRecorded', 'MeterReadingRecorded', 'SafetyPermitApproved', 'WorkOrderCreated', 'WorkOrderScheduled', 'SparePartUsed', 'MaintenanceCompleted', 'VendorPerformanceUpdated'), 'consumes': ('DowntimeCaptured', 'NonConformanceRaised', 'InventoryReservationConfirmed', 'PurchaseOrderAcknowledged', 'AssetLifecycleUpdated')}, 'dependencies': {'apis': ('production_uptime_projection', 'quality_reliability_projection', 'inventory_spares_projection', 'procurement_vendor_projection', 'asset_lifecycle_projection', 'GET /production/orders/{id}', 'GET /quality/nonconformances/{id}', 'GET /inventory/spares/{id}', 'GET /procurement/vendors/{id}', 'POST /audit/maintenance-events'), 'projections': ('production_uptime_projection', 'quality_reliability_projection', 'inventory_spares_projection', 'procurement_vendor_projection', 'asset_lifecycle_projection')}, 'permissions': ('eam.read', 'eam.equipment', 'eam.plan', 'eam.execute', 'eam.safety', 'eam.configure', 'eam.audit'), 'configuration': ('EAM_DATABASE_URL', 'EAM_EVENT_TOPIC', 'EAM_RETRY_LIMIT', 'EAM_DEFAULT_TIMEZONE'), 'idempotent_handlers': {'key_pattern': 'eam:<EventType>:<event_id>', 'inbox_table': 'maintenance_inbox', 'dead_letter_table': 'maintenance_dead_letter', 'outbox_table': 'maintenance_outbox'}}, 'permissions': {'format': 'appgen.eam-permissions.v1', 'ok': True, 'pbc': 'eam', 'permissions': ('eam.read', 'eam.equipment', 'eam.plan', 'eam.execute', 'eam.safety', 'eam.configure', 'eam.audit'), 'action_permissions': {'register_equipment': 'eam.equipment', 'create_maintenance_plan': 'eam.plan', 'record_condition_reading': 'eam.execute', 'record_meter_reading': 'eam.execute', 'create_safety_permit': 'eam.safety', 'create_work_order': 'eam.execute', 'schedule_work_order': 'eam.execute', 'issue_spare_part': 'eam.execute', 'complete_work_order': 'eam.execute', 'register_rule': 'eam.configure', 'set_parameter': 'eam.configure', 'configure_runtime': 'eam.configure', 'receive_event': 'eam.execute', 'run_control_tests': 'eam.audit'}, 'rbac_tables': ('maintenance_rule', 'maintenance_parameter', 'maintenance_configuration')}, 'ui': {'fragments': ('MaintenanceWorkbench', 'EquipmentRegistry', 'AssetHierarchyMap', 'MaintenancePlanConsole', 'ConditionMonitoringPanel', 'WorkOrderBoard', 'MaintenanceScheduler', 'SpareUsageConsole', 'SafetyPermitConsole', 'ReliabilityDashboard', 'VendorServicePanel', 'MaintenanceRuleStudio', 'MaintenanceParameterConsole', 'MaintenanceConfigurationPanel'), 'stream_engine_picker_visible': False}, 'blocking_gaps': (), 'pbc': 'eam'}


def _load_sibling_module(module_name):
    """Load a sibling generated module when this file is imported directly."""
    path = Path(__file__).with_name(f'{module_name}.py')
    spec = importlib.util.spec_from_file_location(f'_pbc_release_{module_name}', path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(module_name)
    spec.loader.exec_module(module)
    return module


def _build_schema_contract():
    try:
        from .schema_contract import build_schema_contract
    except ImportError:
        return _load_sibling_module('schema_contract').build_schema_contract()
    return build_schema_contract()


def _build_service_contract():
    try:
        from .service_contract import build_service_contract
    except ImportError:
        return _load_sibling_module('service_contract').build_service_contract()
    return build_service_contract()


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    evidence = dict(RELEASE_EVIDENCE)
    evidence.setdefault('schema', _build_schema_contract())
    evidence.setdefault('service', _build_service_contract())
    evidence.setdefault('pbc', 'eam')
    app_surface = app_surface_smoke_test()
    standalone = single_pbc_eam_app_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'standalone_app_surface', 'ok': app_surface['ok']},
        {'id': 'standalone_forms_wizards_controls', 'ok': standalone['forms']['ok'] and standalone['wizards']['ok'] and standalone['controls']['ok']},
        {'id': 'improve1_coverage', 'ok': len(standalone['forms']['covered_improve1_items']) == 50 and len(standalone['controls']['covered_improve1_items']) == 50},
        {'id': 'end_to_end_maintenance_execution_proof', 'ok': standalone['end_to_end_proof']['ok']},
    )
    return {
        **evidence,
        'ok': evidence.get('ok') is True and all(check['ok'] for check in checks),
        'checks': checks,
        'standalone_app': standalone,
        'standalone_app_smoke': app_surface,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
    }


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ('schema', 'service', 'api', 'permissions', 'ui', 'events')
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get('checks', ()))
    return {
        'ok': evidence.get('ok') is True and bool(checks),
        'pbc': 'eam',
        'format': evidence.get('format'),
        'sections': sections,
        'checks': checks,
        'blocking_gaps': tuple(evidence.get('blocking_gaps', ())),
        'required_sections': ('schema', 'service'),
        'side_effects': (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest['required_sections'] if section not in manifest['sections'])
    failed_checks = tuple(check for check in manifest['checks'] if check.get('ok') is not True)
    schema = evidence.get('schema', {}) if isinstance(evidence.get('schema'), dict) else {}
    service = evidence.get('service', {}) if isinstance(evidence.get('service'), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ('schema_shared_table_access', schema.get('shared_table_access') is not False),
            ('service_shared_table_access', service.get('shared_table_access') is True),
            ('service_missing_command_methods', not bool(service.get('command_methods'))),
        )
        if failed
    )
    return {
        'ok': manifest['ok']
        and evidence.get('pbc') == manifest['pbc']
        and not manifest['blocking_gaps']
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        'pbc': 'eam',
        'manifest': manifest,
        'missing_sections': missing_sections,
        'failed_checks': failed_checks,
        'boundary_gaps': boundary_gaps,
        'side_effects': (),
    }


def smoke_test():
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        'ok': validation['ok'] and evidence.get('ok') is True,
        'validation': validation,
        'evidence': evidence,
        'side_effects': (),
    }
