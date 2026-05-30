"""Owned model metadata and standalone store for the utility_outage_restoration PBC."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import UTC, datetime

from .runtime import utility_outage_restoration_build_schema_contract

PBC_KEY = 'utility_outage_restoration'
COMMON_COLUMNS = 'row_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, tenant TEXT NOT NULL, outage_id TEXT, status TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL'
EVENT_COLUMNS = 'row_id INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT NOT NULL, event_type TEXT NOT NULL, payload TEXT NOT NULL, idempotency_key TEXT NOT NULL, created_at TEXT NOT NULL'
STANDALONE_TABLE_DEFINITIONS = (
    {'key': 'utility_outage_restoration_network_asset_projection', 'kind': 'projection', 'description': 'Projected feeder, breaker, recloser, switch, transformer, lateral, and service point topology used by outage triage.'},
    {'key': 'utility_outage_restoration_trouble_call', 'kind': 'operational', 'description': 'Inbound trouble calls, AMI pings, field reports, and SCADA detections clustered into outage incidents.'},
    {'key': 'utility_outage_restoration_oms_event', 'kind': 'operational', 'description': 'Package-local OMS work items and dispatch events produced inside the standalone outage slice.'},
    {'key': 'utility_outage_restoration_outage_incident', 'kind': 'core', 'description': 'Owned outage lifecycle including nested outage lineage, storm mode, and restoration state.'},
    {'key': 'utility_outage_restoration_device_interruption', 'kind': 'core', 'description': 'Projected feeder, breaker, recloser, transformer, and service-point interruptions.'},
    {'key': 'utility_outage_restoration_switching_step', 'kind': 'core', 'description': 'Switching plans, clearance hold points, and restoration sequencing.'},
    {'key': 'utility_outage_restoration_safety_isolation', 'kind': 'safety', 'description': 'Lockout, tagging, grounding, and hazard isolation evidence.'},
    {'key': 'utility_outage_restoration_damage_assessment', 'kind': 'assessment', 'description': 'Field assessments for poles, wire, transformer, vegetation, flood, and fire damage.'},
    {'key': 'utility_outage_restoration_crew_assignment', 'kind': 'core', 'description': 'Crew dispatch, staging, ETA, skills, and mutual-aid-aware work assignments.'},
    {'key': 'utility_outage_restoration_restoration_estimate', 'kind': 'core', 'description': 'ETR revisions with confidence, assumptions, and communication approval state.'},
    {'key': 'utility_outage_restoration_customer_impact', 'kind': 'core', 'description': 'Customer counts, critical customer queues, life-support flags, and notification obligations.'},
    {'key': 'utility_outage_restoration_customer_notification', 'kind': 'communication', 'description': 'Outbound notifications for outage confirmation, ETR updates, and restoration verification.'},
    {'key': 'utility_outage_restoration_mutual_aid_request', 'kind': 'operations', 'description': 'Mutual aid requests, staging details, ETA, and incident allocation.'},
    {'key': 'utility_outage_restoration_restoration_verification', 'kind': 'verification', 'description': 'Service restoration checks, field sign-off, nested outage detection, and closure evidence.'},
    {'key': 'utility_outage_restoration_reliability_metric', 'kind': 'core', 'description': 'Regulatory indices such as SAIDI, SAIFI, CAIDI, and major event day classification.'},
    {'key': 'utility_outage_restoration_governed_assistance_session', 'kind': 'governance', 'description': 'Governed AI assistance plans and operator confirmations for package-local operations.'},
    {'key': 'utility_outage_restoration_appgen_outbox_event', 'kind': 'eventing', 'description': 'AppGen-X outbox events for the standalone slice.'},
    {'key': 'utility_outage_restoration_appgen_inbox_event', 'kind': 'eventing', 'description': 'AppGen-X inbox events accepted by the standalone slice.'},
    {'key': 'utility_outage_restoration_appgen_dead_letter_event', 'kind': 'eventing', 'description': 'Dead-letter evidence for unsupported or failed inbound events.'},
)
STANDALONE_TABLE_KEYS = tuple(item['key'] for item in STANDALONE_TABLE_DEFINITIONS)
CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
EMITTED_EVENT_TYPES = (
    'UtilityOutageRestorationCreated',
    'UtilityOutageRestorationUpdated',
    'UtilityOutageRestorationApproved',
    'UtilityOutageRestorationExceptionOpened',
    'UtilityOutageRestorationCrewDispatched',
    'UtilityOutageRestorationNotificationQueued',
    'UtilityOutageRestorationVerified',
)


def _utcnow() -> str:
    return datetime.now(tz=UTC).isoformat()


def _json_dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def _json_loads(value: str | bytes | None) -> dict:
    if not value:
        return {}
    return json.loads(value)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def model_contracts():
    return utility_outage_restoration_build_schema_contract()['models']


def standalone_model_contract() -> dict:
    table_contracts = tuple(
        {
            'key': item['key'],
            'kind': item['kind'],
            'description': item['description'],
            'storage': 'sqlite_dev_harness',
            'columns': ('record_id', 'tenant', 'outage_id', 'status', 'payload', 'created_at', 'updated_at') if 'event' not in item['key'] else ('event_id', 'event_type', 'payload', 'idempotency_key', 'created_at'),
        }
        for item in STANDALONE_TABLE_DEFINITIONS
    )
    return {
        'format': 'appgen.utility-outage-restoration-standalone-model-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'table_keys': STANDALONE_TABLE_KEYS,
        'tables': table_contracts,
        'database': 'sqlite',
        'deployment_boundary': ('postgresql', 'mysql', 'mariadb'),
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


class UtilityOutageRestorationStandaloneStore:
    """SQLite-backed package-local outage restoration harness."""

    def __init__(self, database_path: str = ':memory:'):
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def close(self) -> None:
        self.connection.close()

    def _create_schema(self) -> None:
        event_tables = {
            'utility_outage_restoration_appgen_outbox_event',
            'utility_outage_restoration_appgen_inbox_event',
            'utility_outage_restoration_appgen_dead_letter_event',
        }
        cursor = self.connection.cursor()
        for table in STANDALONE_TABLE_KEYS:
            columns = EVENT_COLUMNS if table in event_tables else COMMON_COLUMNS
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} ({columns})')
        self.connection.commit()

    def _insert(self, table: str, *, record_id: str, tenant: str, outage_id: str | None, status: str, payload: dict) -> dict:
        now = _utcnow()
        row = {
            'record_id': record_id,
            'tenant': tenant,
            'outage_id': outage_id,
            'status': status,
            'payload': payload,
            'created_at': now,
            'updated_at': now,
        }
        self.connection.execute(
            f'INSERT INTO {table} (record_id, tenant, outage_id, status, payload, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (record_id, tenant, outage_id, status, _json_dumps(payload), now, now),
        )
        self.connection.commit()
        return row

    def _record_event(self, table: str, *, event_type: str, payload: dict, idempotency_key: str | None = None) -> dict:
        now = _utcnow()
        event = {
            'event_id': _digest((table, event_type, payload, now)),
            'event_type': event_type,
            'payload': payload,
            'idempotency_key': idempotency_key or _digest((event_type, payload)),
            'created_at': now,
        }
        self.connection.execute(
            f'INSERT INTO {table} (event_id, event_type, payload, idempotency_key, created_at) VALUES (?, ?, ?, ?, ?)',
            (event['event_id'], event_type, _json_dumps(payload), event['idempotency_key'], now),
        )
        self.connection.commit()
        return event

    def _rows(self, table: str, *, tenant: str | None = None, outage_id: str | None = None) -> tuple[dict, ...]:
        query = f'SELECT * FROM {table}'
        params: list[str] = []
        clauses = []
        if tenant is not None:
            clauses.append('tenant = ?')
            params.append(tenant)
        if outage_id is not None:
            clauses.append('outage_id = ?')
            params.append(outage_id)
        if clauses:
            query += ' WHERE ' + ' AND '.join(clauses)
        query += ' ORDER BY row_id'
        rows = self.connection.execute(query, tuple(params)).fetchall()
        return tuple(
            {
                'record_id': row['record_id'],
                'tenant': row['tenant'],
                'outage_id': row['outage_id'],
                'status': row['status'],
                'payload': _json_loads(row['payload']),
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            for row in rows
        )

    def _event_rows(self, table: str) -> tuple[dict, ...]:
        rows = self.connection.execute(f'SELECT * FROM {table} ORDER BY row_id').fetchall()
        return tuple(
            {
                'event_id': row['event_id'],
                'event_type': row['event_type'],
                'payload': _json_loads(row['payload']),
                'idempotency_key': row['idempotency_key'],
                'created_at': row['created_at'],
            }
            for row in rows
        )

    def get_outage(self, outage_id: str) -> dict | None:
        row = self.connection.execute(
            'SELECT * FROM utility_outage_restoration_outage_incident WHERE record_id = ? ORDER BY row_id DESC LIMIT 1',
            (outage_id,),
        ).fetchone()
        if row is None:
            return None
        return {
            'record_id': row['record_id'],
            'tenant': row['tenant'],
            'outage_id': row['outage_id'],
            'status': row['status'],
            'payload': _json_loads(row['payload']),
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
        }

    def list_outages(self, tenant: str) -> tuple[dict, ...]:
        return self._rows('utility_outage_restoration_outage_incident', tenant=tenant)

    def register_network_asset_projection(self, payload: dict) -> dict:
        supplied = dict(payload)
        projection_id = supplied.get('projection_id') or supplied.get('asset_id') or 'asset-projection-1'
        tenant = supplied.get('tenant', 'default')
        record = self._insert(
            'utility_outage_restoration_network_asset_projection',
            record_id=projection_id,
            tenant=tenant,
            outage_id=supplied.get('outage_id'),
            status='projected',
            payload={
                'asset_id': supplied.get('asset_id', projection_id),
                'asset_type': supplied.get('asset_type', 'feeder_segment'),
                'device_hierarchy': supplied.get('device_hierarchy', ('feeder', 'breaker', 'recloser', 'switch', 'transformer', 'service_point')),
                'service_points': tuple(supplied.get('service_points', ())),
                'critical_customers': tuple(supplied.get('critical_customers', ())),
                'source_system': supplied.get('source_system', 'network_projection'),
            },
        )
        self._record_event('utility_outage_restoration_appgen_outbox_event', event_type=EMITTED_EVENT_TYPES[0], payload={'projection_id': projection_id, 'tenant': tenant})
        return {'ok': True, 'projection': record, 'side_effects': ()}

    def create_outage_incident(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied.get('outage_id') or supplied.get('incident_number') or 'outage-1'
        tenant = supplied.get('tenant', 'default')
        critical_customers = tuple(supplied.get('critical_customers', ()))
        incident_payload = {
            'incident_number': supplied.get('incident_number', outage_id),
            'service_area': supplied.get('service_area', 'north-grid'),
            'parent_outage_id': supplied.get('parent_outage_id'),
            'storm_mode_active': bool(supplied.get('storm_mode_active', False)),
            'reported_channels': tuple(supplied.get('reported_channels', ('trouble_call',))),
            'network_asset_model': tuple(supplied.get('network_asset_model', ())),
            'critical_customers': critical_customers,
            'life_support_customer_count': supplied.get('life_support_customer_count', len([item for item in critical_customers if item.get('life_support')])),
            'priority_sites': tuple(supplied.get('priority_sites', ())),
            'status_reason': supplied.get('status_reason', 'reported'),
        }
        record = self._insert(
            'utility_outage_restoration_outage_incident',
            record_id=outage_id,
            tenant=tenant,
            outage_id=outage_id,
            status=supplied.get('status', 'reported'),
            payload=incident_payload,
        )
        customer_impact = self._insert(
            'utility_outage_restoration_customer_impact',
            record_id=f'impact-{outage_id}',
            tenant=tenant,
            outage_id=outage_id,
            status='calculated',
            payload={
                'affected_customer_count': supplied.get('affected_customer_count', len(tuple(supplied.get('service_points', ()))) or max(1, len(critical_customers))),
                'critical_customer_count': len(critical_customers),
                'critical_customers': critical_customers,
                'priority_required': bool(critical_customers),
            },
        )
        oms_event = self._insert(
            'utility_outage_restoration_oms_event',
            record_id=f'oms-{outage_id}',
            tenant=tenant,
            outage_id=outage_id,
            status='open',
            payload={'event_type': 'outage_created', 'incident_number': incident_payload['incident_number']},
        )
        self._record_event('utility_outage_restoration_appgen_outbox_event', event_type=EMITTED_EVENT_TYPES[0], payload={'outage_id': outage_id, 'tenant': tenant, 'status': record['status']})
        return {'ok': True, 'outage': record, 'customer_impact': customer_impact, 'oms_event': oms_event, 'side_effects': ()}

    def record_trouble_call(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        call_id = supplied.get('call_id') or _digest((outage_id, supplied.get('caller_name'), supplied.get('service_point')))
        record = self._insert(
            'utility_outage_restoration_trouble_call',
            record_id=call_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status='received',
            payload={
                'caller_name': supplied.get('caller_name', 'unknown caller'),
                'service_point': supplied.get('service_point', 'unknown-service-point'),
                'channel': supplied.get('channel', 'voice'),
                'critical_customer': bool(supplied.get('critical_customer', False)),
                'notes': supplied.get('notes', ''),
            },
        )
        self._record_event('utility_outage_restoration_appgen_outbox_event', event_type=EMITTED_EVENT_TYPES[1], payload={'outage_id': outage_id, 'call_id': call_id, 'tenant': outage['tenant']})
        return {'ok': True, 'trouble_call': record, 'side_effects': ()}

    def create_oms_event(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        event_id = supplied.get('event_id') or _digest((outage_id, supplied.get('event_type'), supplied.get('command')))
        record = self._insert(
            'utility_outage_restoration_oms_event',
            record_id=event_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status=supplied.get('status', 'created'),
            payload={
                'event_type': supplied.get('event_type', 'oms_dispatch_created'),
                'command': supplied.get('command', 'dispatch'),
                'priority': supplied.get('priority', 'high'),
                'governed': bool(supplied.get('governed', True)),
            },
        )
        return {'ok': True, 'oms_event': record, 'side_effects': ()}

    def create_device_interruption(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        interruption_id = supplied.get('interruption_id') or supplied.get('device_id') or f'device-{outage_id}'
        record = self._insert(
            'utility_outage_restoration_device_interruption',
            record_id=interruption_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status=supplied.get('status', 'suspected_fault_segment'),
            payload={
                'device_id': supplied.get('device_id', interruption_id),
                'device_type': supplied.get('device_type', 'breaker'),
                'upstream_device_id': supplied.get('upstream_device_id'),
                'downstream_device_ids': tuple(supplied.get('downstream_device_ids', ())),
                'service_points': tuple(supplied.get('service_points', ())),
                'lockout': bool(supplied.get('lockout', True)),
            },
        )
        return {'ok': True, 'device_interruption': record, 'side_effects': ()}

    def dispatch_crew(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        dispatch_id = supplied.get('dispatch_id') or supplied.get('crew_id') or f'crew-{outage_id}'
        record = self._insert(
            'utility_outage_restoration_crew_assignment',
            record_id=dispatch_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status=supplied.get('status', 'assigned'),
            payload={
                'crew_id': supplied.get('crew_id', dispatch_id),
                'crew_type': supplied.get('crew_type', 'line'),
                'skills': tuple(supplied.get('skills', ('switching', 'distribution'))),
                'eta_minutes': supplied.get('eta_minutes', 45),
                'staging_area': supplied.get('staging_area', 'north-yard'),
                'mutual_aid': bool(supplied.get('mutual_aid', False)),
            },
        )
        self._record_event('utility_outage_restoration_appgen_outbox_event', event_type='UtilityOutageRestorationCrewDispatched', payload={'outage_id': outage_id, 'dispatch_id': dispatch_id, 'tenant': outage['tenant']})
        return {'ok': True, 'crew_assignment': record, 'side_effects': ()}

    def author_switching_plan(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        step_id = supplied.get('step_id') or _digest((outage_id, supplied.get('plan_id'), supplied.get('sequence', 1)))
        record = self._insert(
            'utility_outage_restoration_switching_step',
            record_id=step_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status=supplied.get('status', 'planned'),
            payload={
                'plan_id': supplied.get('plan_id', f'plan-{outage_id}'),
                'sequence': supplied.get('sequence', 1),
                'device_id': supplied.get('device_id', 'switch-1'),
                'action': supplied.get('action', 'open_switch'),
                'hold_point': bool(supplied.get('hold_point', True)),
                'authority': supplied.get('authority', 'control_center'),
                'clearance_required': bool(supplied.get('clearance_required', True)),
            },
        )
        return {'ok': True, 'switching_step': record, 'side_effects': ()}

    def isolate_safety(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        isolation_id = supplied.get('isolation_id') or _digest((outage_id, supplied.get('hazard_type'), supplied.get('device_id')))
        record = self._insert(
            'utility_outage_restoration_safety_isolation',
            record_id=isolation_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status=supplied.get('status', 'active'),
            payload={
                'hazard_type': supplied.get('hazard_type', 'downed_wire'),
                'device_id': supplied.get('device_id', 'switch-1'),
                'grounding_applied': bool(supplied.get('grounding_applied', True)),
                'clearance_owner': supplied.get('clearance_owner', 'field_supervisor'),
                'blocked_commands': tuple(supplied.get('blocked_commands', ('close_switch',))),
            },
        )
        return {'ok': True, 'safety_isolation': record, 'side_effects': ()}

    def record_damage_assessment(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        assessment_id = supplied.get('assessment_id') or _digest((outage_id, supplied.get('asset_id'), supplied.get('severity')))
        record = self._insert(
            'utility_outage_restoration_damage_assessment',
            record_id=assessment_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status='assessed',
            payload={
                'asset_id': supplied.get('asset_id', 'pole-1'),
                'severity': supplied.get('severity', 3),
                'hazard_type': supplied.get('hazard_type', 'vegetation'),
                'repair_recommendation': supplied.get('repair_recommendation', 'replace_span'),
                'materials_required': tuple(supplied.get('materials_required', ('wire', 'fuse'))),
            },
        )
        return {'ok': True, 'damage_assessment': record, 'side_effects': ()}

    def calculate_etr(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        crew_eta = supplied.get('crew_eta_minutes', 45)
        switching_steps = supplied.get('switching_steps_remaining', len(self._rows('utility_outage_restoration_switching_step', outage_id=outage_id)))
        damage_records = len(self._rows('utility_outage_restoration_damage_assessment', outage_id=outage_id))
        critical_count = len(tuple(outage['payload'].get('critical_customers', ())))
        nested_count = len(tuple(item for item in self._rows('utility_outage_restoration_outage_incident', tenant=outage['tenant']) if item['payload'].get('parent_outage_id') == outage_id))
        minutes = max(30, crew_eta + switching_steps * 20 + damage_records * 35 + critical_count * 10 + nested_count * 15)
        estimate_id = supplied.get('estimate_id') or f'etr-{outage_id}-{minutes}'
        payload_record = {
            'minutes_to_restore': minutes,
            'confidence': round(min(0.98, 0.55 + (1 / (1 + damage_records + nested_count))), 2),
            'assumptions': ('crew_dispatched', 'switching_authorized', 'materials_available'),
            'revision_reason': supplied.get('revision_reason', 'initial_assessment'),
        }
        record = self._insert(
            'utility_outage_restoration_restoration_estimate',
            record_id=estimate_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status='draft' if supplied.get('approval_required', True) else 'approved',
            payload=payload_record,
        )
        return {'ok': True, 'restoration_estimate': record, 'minutes_to_restore': minutes, 'side_effects': ()}

    def open_nested_outage(self, payload: dict) -> dict:
        supplied = dict(payload)
        parent_outage_id = supplied['parent_outage_id']
        parent = self.get_outage(parent_outage_id)
        if parent is None:
            return {'ok': False, 'reason': 'unknown_parent_outage', 'parent_outage_id': parent_outage_id, 'side_effects': ()}
        nested_payload = dict(supplied)
        nested_payload.setdefault('outage_id', supplied.get('outage_id', f'{parent_outage_id}-nested'))
        nested_payload['tenant'] = parent['tenant']
        nested_payload['parent_outage_id'] = parent_outage_id
        nested_payload.setdefault('status', 'nested_active')
        nested_payload.setdefault('status_reason', 'remaining_transformer_or_service_outage')
        result = self.create_outage_incident(nested_payload)
        return {'ok': result['ok'], 'nested_outage': result.get('outage'), 'side_effects': ()}

    def send_customer_notification(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        notification_id = supplied.get('notification_id') or _digest((outage_id, supplied.get('channel'), supplied.get('milestone')))
        record = self._insert(
            'utility_outage_restoration_customer_notification',
            record_id=notification_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status='queued',
            payload={
                'channel': supplied.get('channel', 'sms'),
                'milestone': supplied.get('milestone', 'etr_update'),
                'audience': supplied.get('audience', 'affected_customers'),
                'message': supplied.get('message', 'Restoration is in progress.'),
                'critical_customer_priority': bool(supplied.get('critical_customer_priority', False)),
            },
        )
        self._record_event('utility_outage_restoration_appgen_outbox_event', event_type='UtilityOutageRestorationNotificationQueued', payload={'outage_id': outage_id, 'notification_id': notification_id, 'tenant': outage['tenant']})
        return {'ok': True, 'notification': record, 'side_effects': ()}

    def request_mutual_aid(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        request_id = supplied.get('request_id') or _digest((outage_id, supplied.get('crew_type'), supplied.get('quantity')))
        record = self._insert(
            'utility_outage_restoration_mutual_aid_request',
            record_id=request_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status=supplied.get('status', 'requested'),
            payload={
                'crew_type': supplied.get('crew_type', 'line'),
                'quantity': supplied.get('quantity', 2),
                'eta_hours': supplied.get('eta_hours', 6),
                'staging_area': supplied.get('staging_area', 'north-yard'),
                'lodging_confirmed': bool(supplied.get('lodging_confirmed', True)),
            },
        )
        return {'ok': True, 'mutual_aid_request': record, 'side_effects': ()}

    def create_governed_assistance_session(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied.get('outage_id')
        tenant = supplied.get('tenant') or (self.get_outage(outage_id)['tenant'] if outage_id and self.get_outage(outage_id) else 'default')
        session_id = supplied.get('session_id') or _digest((outage_id, supplied.get('goal'), supplied.get('operator')))
        record = self._insert(
            'utility_outage_restoration_governed_assistance_session',
            record_id=session_id,
            tenant=tenant,
            outage_id=outage_id,
            status='planned',
            payload={
                'goal': supplied.get('goal', 'Recommend outage restoration sequence'),
                'operator': supplied.get('operator', 'dispatcher'),
                'requires_confirmation': True,
                'allowed_tables': supplied.get('allowed_tables', STANDALONE_TABLE_KEYS[:6]),
                'blocked_actions': ('delete_outage', 'mutate_foreign_asset_tables'),
            },
        )
        return {'ok': True, 'assistance_session': record, 'side_effects': ()}

    def verify_restoration(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        verification_id = supplied.get('verification_id') or f'verify-{outage_id}'
        nested_remaining = len(tuple(item for item in self._rows('utility_outage_restoration_outage_incident', tenant=outage['tenant']) if item['payload'].get('parent_outage_id') == outage_id and item['status'] != 'verified'))
        record = self._insert(
            'utility_outage_restoration_restoration_verification',
            record_id=verification_id,
            tenant=outage['tenant'],
            outage_id=outage_id,
            status='verified' if nested_remaining == 0 else 'partial_restore',
            payload={
                'verified_by': supplied.get('verified_by', 'field_supervisor'),
                'service_confirmed': True,
                'nested_outages_remaining': nested_remaining,
                'meter_ping_success': bool(supplied.get('meter_ping_success', True)),
                'customer_callbacks_clear': bool(supplied.get('customer_callbacks_clear', True)),
            },
        )
        metric = self.compute_regulatory_indices(outage['tenant'])
        self._record_event('utility_outage_restoration_appgen_outbox_event', event_type='UtilityOutageRestorationVerified', payload={'outage_id': outage_id, 'tenant': outage['tenant'], 'status': record['status']})
        return {'ok': True, 'verification': record, 'regulatory_index_snapshot': metric['metric'], 'side_effects': ()}

    def compute_regulatory_indices(self, tenant: str) -> dict:
        outages = self.list_outages(tenant)
        impacts = self._rows('utility_outage_restoration_customer_impact', tenant=tenant)
        estimates = self._rows('utility_outage_restoration_restoration_estimate', tenant=tenant)
        impacted_customers = sum(item['payload'].get('affected_customer_count', 0) for item in impacts)
        sustained_interruptions = max(1, len(outages))
        total_minutes = sum(item['payload'].get('minutes_to_restore', 0) for item in estimates)
        saidi = round(total_minutes / max(1, impacted_customers), 4)
        saifi = round(impacted_customers / max(1, sustained_interruptions * max(1, impacted_customers // max(1, len(outages)) or 1)), 4)
        caidi = round(total_minutes / max(1, sustained_interruptions), 4)
        metric_id = f'reg-{tenant}-{len(outages)}-{len(estimates)}'
        record = self._insert(
            'utility_outage_restoration_reliability_metric',
            record_id=metric_id,
            tenant=tenant,
            outage_id=None,
            status='calculated',
            payload={
                'saidi': saidi,
                'saifi': saifi,
                'caidi': caidi,
                'major_event_day': any(outage['payload'].get('storm_mode_active') for outage in outages),
                'outage_count': len(outages),
            },
        )
        return {'ok': True, 'metric': record, 'side_effects': ()}

    def activate_storm_mode(self, payload: dict) -> dict:
        supplied = dict(payload)
        outage_id = supplied['outage_id']
        outage = self.get_outage(outage_id)
        if outage is None:
            return {'ok': False, 'reason': 'unknown_outage', 'outage_id': outage_id, 'side_effects': ()}
        oms = self.create_oms_event({'outage_id': outage_id, 'event_type': 'storm_mode_activated', 'command': 'storm_mode', 'priority': 'critical'})
        session = self.create_governed_assistance_session({'outage_id': outage_id, 'tenant': outage['tenant'], 'goal': 'Coordinate storm mode restoration sequencing'})
        return {'ok': True, 'storm_mode_active': True, 'oms_event': oms.get('oms_event'), 'assistance_session': session.get('assistance_session'), 'side_effects': ()}

    def receive_event(self, event: dict) -> dict:
        supplied = dict(event)
        event_type = supplied.get('event_type', 'UnknownEvent')
        if event_type not in CONSUMED_EVENT_TYPES:
            dead = self._record_event(
                'utility_outage_restoration_appgen_dead_letter_event',
                event_type=event_type,
                payload={'event': supplied, 'reason': 'unsupported_event_type'},
                idempotency_key=supplied.get('idempotency_key'),
            )
            return {'ok': False, 'dead_letter': dead, 'side_effects': ()}
        inbox = self._record_event(
            'utility_outage_restoration_appgen_inbox_event',
            event_type=event_type,
            payload=supplied,
            idempotency_key=supplied.get('idempotency_key'),
        )
        return {'ok': True, 'inbox_event': inbox, 'side_effects': ()}

    def build_timeline(self, outage_id: str) -> dict:
        timeline = []
        for table, label in (
            ('utility_outage_restoration_trouble_call', 'trouble_call'),
            ('utility_outage_restoration_oms_event', 'oms_event'),
            ('utility_outage_restoration_switching_step', 'switching_step'),
            ('utility_outage_restoration_safety_isolation', 'safety_isolation'),
            ('utility_outage_restoration_damage_assessment', 'damage_assessment'),
            ('utility_outage_restoration_crew_assignment', 'crew_assignment'),
            ('utility_outage_restoration_restoration_estimate', 'restoration_estimate'),
            ('utility_outage_restoration_customer_notification', 'customer_notification'),
            ('utility_outage_restoration_restoration_verification', 'restoration_verification'),
        ):
            for item in self._rows(table, outage_id=outage_id):
                timeline.append({'kind': label, 'record_id': item['record_id'], 'status': item['status'], 'created_at': item['created_at']})
        timeline.sort(key=lambda item: item['created_at'])
        return {'ok': True, 'outage_id': outage_id, 'timeline': tuple(timeline), 'event_count': len(timeline), 'side_effects': ()}

    def build_workbench(self, tenant: str) -> dict:
        outages = self.list_outages(tenant)
        impacts = self._rows('utility_outage_restoration_customer_impact', tenant=tenant)
        crews = self._rows('utility_outage_restoration_crew_assignment', tenant=tenant)
        switching = self._rows('utility_outage_restoration_switching_step', tenant=tenant)
        isolations = self._rows('utility_outage_restoration_safety_isolation', tenant=tenant)
        assessments = self._rows('utility_outage_restoration_damage_assessment', tenant=tenant)
        notifications = self._rows('utility_outage_restoration_customer_notification', tenant=tenant)
        mutual_aid = self._rows('utility_outage_restoration_mutual_aid_request', tenant=tenant)
        verifications = self._rows('utility_outage_restoration_restoration_verification', tenant=tenant)
        storm_mode_active = any(item['payload'].get('storm_mode_active') for item in outages)
        critical_queue = tuple(
            {
                'outage_id': item['outage_id'],
                'critical_customer_count': item['payload'].get('critical_customer_count', 0),
                'priority_required': item['payload'].get('priority_required', False),
            }
            for item in impacts
            if item['payload'].get('critical_customer_count', 0) > 0
        )
        return {
            'ok': True,
            'tenant': tenant,
            'outage_count': len(outages),
            'active_outage_count': len(tuple(item for item in outages if item['status'] not in ('verified', 'closed'))),
            'nested_outage_count': len(tuple(item for item in outages if item['payload'].get('parent_outage_id'))),
            'crew_dispatch_count': len(crews),
            'switching_plan_count': len(switching),
            'active_isolation_count': len(tuple(item for item in isolations if item['status'] == 'active')),
            'damage_assessment_count': len(assessments),
            'notification_count': len(notifications),
            'mutual_aid_request_count': len(mutual_aid),
            'verification_count': len(verifications),
            'storm_mode_active': storm_mode_active,
            'critical_customer_queue': critical_queue,
            'outbox_count': len(self._event_rows('utility_outage_restoration_appgen_outbox_event')),
            'inbox_count': len(self._event_rows('utility_outage_restoration_appgen_inbox_event')),
            'dead_letter_count': len(self._event_rows('utility_outage_restoration_appgen_dead_letter_event')),
            'routes': (
                '/app/utility-outage-restoration/outages',
                '/app/utility-outage-restoration/trouble-calls',
                '/app/utility-outage-restoration/crew-dispatch',
                '/app/utility-outage-restoration/workbench',
            ),
            'side_effects': (),
        }


def standalone_store_smoke_test() -> dict:
    store = UtilityOutageRestorationStandaloneStore()
    try:
        projection = store.register_network_asset_projection({
            'projection_id': 'asset-smoke',
            'tenant': 'tenant-smoke',
            'asset_id': 'feeder-17',
            'service_points': ('svc-1', 'svc-2'),
            'critical_customers': ({'customer_id': 'hospital-1', 'life_support': True},),
        })
        outage = store.create_outage_incident({
            'outage_id': 'outage-smoke',
            'tenant': 'tenant-smoke',
            'incident_number': 'OMS-1001',
            'service_points': ('svc-1', 'svc-2'),
            'critical_customers': ({'customer_id': 'hospital-1', 'life_support': True},),
            'storm_mode_active': True,
        })
        trouble = store.record_trouble_call({'outage_id': 'outage-smoke', 'caller_name': 'A. Customer', 'service_point': 'svc-1', 'critical_customer': True})
        interruption = store.create_device_interruption({'outage_id': 'outage-smoke', 'device_id': 'breaker-17', 'downstream_device_ids': ('xf-1',)})
        crew = store.dispatch_crew({'outage_id': 'outage-smoke', 'crew_id': 'crew-7', 'eta_minutes': 35})
        switching = store.author_switching_plan({'outage_id': 'outage-smoke', 'plan_id': 'plan-smoke', 'sequence': 1, 'device_id': 'switch-9'})
        safety = store.isolate_safety({'outage_id': 'outage-smoke', 'hazard_type': 'downed_wire', 'device_id': 'switch-9'})
        assessment = store.record_damage_assessment({'outage_id': 'outage-smoke', 'asset_id': 'pole-9', 'severity': 4})
        etr = store.calculate_etr({'outage_id': 'outage-smoke', 'crew_eta_minutes': 35})
        nested = store.open_nested_outage({'parent_outage_id': 'outage-smoke', 'outage_id': 'outage-smoke-nested', 'incident_number': 'OMS-1001-N'})
        notification = store.send_customer_notification({'outage_id': 'outage-smoke', 'channel': 'sms', 'critical_customer_priority': True})
        mutual_aid = store.request_mutual_aid({'outage_id': 'outage-smoke', 'quantity': 2, 'crew_type': 'tree'})
        storm = store.activate_storm_mode({'outage_id': 'outage-smoke'})
        verification = store.verify_restoration({'outage_id': 'outage-smoke'})
        regulatory = store.compute_regulatory_indices('tenant-smoke')
        timeline = store.build_timeline('outage-smoke')
        workbench = store.build_workbench('tenant-smoke')
        inbound = store.receive_event({'event_type': 'PolicyChanged', 'idempotency_key': 'policy-smoke', 'policy_id': 'storm-mode'})
        dead = store.receive_event({'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
        checks = (projection, outage, trouble, interruption, crew, switching, safety, assessment, etr, nested, notification, mutual_aid, storm, verification, regulatory, timeline, workbench, inbound)
        return {
            'ok': all(item['ok'] for item in checks)
            and dead['ok'] is False
            and workbench['critical_customer_queue']
            and workbench['storm_mode_active'] is True
            and workbench['nested_outage_count'] >= 1
            and timeline['event_count'] >= 6,
            'projection': projection,
            'outage': outage,
            'trouble': trouble,
            'crew': crew,
            'etr': etr,
            'storm': storm,
            'verification': verification,
            'regulatory': regulatory,
            'timeline': timeline,
            'workbench': workbench,
            'dead_letter': dead,
            'side_effects': (),
        }
    finally:
        store.close()
