"""Standalone executable slice app for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .blueprint import (
    ADVANCED_CAPABILITIES,
    ALLOWED_DATABASE_BACKENDS,
    APPGEN_X_TOPIC,
    BUSINESS_TABLES,
    BUSINESS_TABLE_BLUEPRINTS,
    CONSUMED_EVENTS,
    CONTROL_DEFINITIONS,
    DOMAIN_OPERATIONS,
    EMITTED_EVENTS,
    EVENT_TABLES,
    FORM_DEFINITIONS,
    NAVIGATION_SECTIONS,
    OPERATION_INDEX,
    PARAMETER_DEFINITIONS,
    PBC_KEY,
    PERMISSIONS,
    RELEASE_ARTIFACTS,
    ROUTE_DEFINITIONS,
    RULE_DEFINITIONS,
    RUNTIME_TABLES,
    STANDARD_FEATURES,
    UI_FRAGMENTS,
    WIZARD_DEFINITIONS,
    business_table_for_operation,
    owned_table,
    table_blueprint_by_table,
)
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, ui_capability_surface_contract

PACKAGE_DIR = Path(__file__).resolve().parent
MIGRATION_PATH = PACKAGE_DIR / 'migrations' / '001_initial.sql'
SPECIFICATION_PATH = PACKAGE_DIR / 'SPECIFICATION.md'


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _dedupe(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _common_fields(anchor_field: str | None = None, anchor_table: str | None = None) -> tuple[dict[str, Any], ...]:
    fields = [
        {'name': 'id', 'type': 'text', 'primary_key': True, 'nullable': False},
        {'name': 'tenant', 'type': 'string', 'required': True},
        {'name': 'code', 'type': 'string', 'required': True, 'searchable': True},
        {'name': 'title', 'type': 'string', 'required': True},
        {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'},
        {'name': 'owner', 'type': 'string', 'required': False},
        {'name': 'period', 'type': 'string', 'required': False},
        {'name': 'score', 'type': 'decimal', 'required': False},
    ]
    if anchor_field:
        field = {'name': anchor_field, 'type': 'text', 'required': False}
        if anchor_table:
            field['references'] = owned_table(anchor_table) + '.id'
        fields.append(field)
    fields.extend(
        [
            {'name': 'version', 'type': 'integer', 'required': True, 'default': 1},
            {'name': 'payload', 'type': 'json', 'required': False},
            {'name': 'created_at', 'type': 'datetime', 'required': True},
            {'name': 'updated_at', 'type': 'datetime', 'required': True},
        ]
    )
    return tuple(fields)


def _event_fields() -> tuple[dict[str, Any], ...]:
    return (
        {'name': 'id', 'type': 'text', 'primary_key': True, 'nullable': False},
        {'name': 'tenant', 'type': 'string', 'required': True},
        {'name': 'event_type', 'type': 'string', 'required': True},
        {'name': 'topic', 'type': 'string', 'required': True},
        {'name': 'status', 'type': 'string', 'required': True},
        {'name': 'idempotency_key', 'type': 'string', 'required': True},
        {'name': 'payload', 'type': 'json', 'required': False},
        {'name': 'retry_count', 'type': 'integer', 'required': True, 'default': 0},
        {'name': 'created_at', 'type': 'datetime', 'required': True},
        {'name': 'updated_at', 'type': 'datetime', 'required': True},
    )


def _model_name(table: str) -> str:
    return ''.join(part.capitalize() for part in table.split('_'))


def build_schema_contract() -> dict[str, Any]:
    tables = []
    models = []
    for blueprint in BUSINESS_TABLE_BLUEPRINTS:
        table = owned_table(blueprint.logical_name)
        fields = _common_fields(blueprint.anchor_field, blueprint.anchor_table)
        relationships = ()
        if blueprint.anchor_field and blueprint.anchor_table:
            relationships = (
                {
                    'field': blueprint.anchor_field,
                    'target_table': owned_table(blueprint.anchor_table),
                    'target_column': 'id',
                    'cardinality': 'many-to-one',
                    'ownership': 'same_pbc',
                },
            )
        tables.append(
            {
                'logical_table': blueprint.logical_name,
                'owned_table': table,
                'description': blueprint.description,
                'fields': fields,
                'relationships': relationships,
            }
        )
        models.append(
            {
                'class_name': _model_name(table),
                'table': table,
                'fields': fields,
                'relationships': relationships,
            }
        )
    for table in EVENT_TABLES:
        fields = _event_fields()
        tables.append(
            {
                'logical_table': table.removeprefix(f'{PBC_KEY}_'),
                'owned_table': table,
                'description': 'AppGen-X event transport table.',
                'fields': fields,
                'relationships': (),
            }
        )
        models.append({'class_name': _model_name(table), 'table': table, 'fields': fields, 'relationships': ()})
    return {
        'format': f'appgen.{PBC_KEY}.owned-schema-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'tables': tuple(tables),
        'migrations': ('migrations/001_initial.sql',),
        'models': tuple(models),
        'datastore_backends': ALLOWED_DATABASE_BACKENDS,
        'database_backends': ALLOWED_DATABASE_BACKENDS,
        'shared_table_access': False,
        'stream_engine_picker_visible': False,
        'owned_tables': tuple(RUNTIME_TABLES),
        'boundary_gaps': (),
        'side_effects': (),
    }


def build_models_contract() -> dict[str, Any]:
    schema = build_schema_contract()
    return {
        'ok': schema['ok'],
        'pbc': PBC_KEY,
        'schema': {'schema': PBC_KEY, 'table_prefix': f'{PBC_KEY}_', 'tables': schema['tables']},
        'models': schema['models'],
        'owned_tables': schema['owned_tables'],
        'side_effects': (),
    }


class SustainabilityEsgReportingSliceApp:
    """One-PBC standalone app with an owned package-local datastore."""

    def __init__(self) -> None:
        self.records = {table: {} for table in RUNTIME_TABLES}
        self.configuration = {
            'database_backend': 'postgresql',
            'event_topic': APPGEN_X_TOPIC,
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
        }
        self.parameters = {item['key']: item['default'] for item in PARAMETER_DEFINITIONS}
        self.rules = {item['rule_id']: dict(item) for item in RULE_DEFINITIONS}
        self.schema_extensions: dict[str, dict[str, Any]] = {}
        self.idempotency_keys: set[str] = set()

    def empty_state(self) -> dict[str, Any]:
        return {
            'configuration': deepcopy(self.configuration),
            'parameters': deepcopy(self.parameters),
            'rules': deepcopy(self.rules),
            'schema_extensions': deepcopy(self.schema_extensions),
            'records': {table: tuple(items.values()) for table, items in self.records.items()},
            'idempotency_keys': tuple(sorted(self.idempotency_keys)),
        }

    def configure_runtime(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        config = dict(config or {})
        backend = config.get('database_backend', self.configuration['database_backend'])
        topic = config.get('event_topic', self.configuration['event_topic'])
        ok = backend in ALLOWED_DATABASE_BACKENDS and topic == APPGEN_X_TOPIC
        self.configuration.update(
            {
                'database_backend': backend,
                'event_topic': topic,
                'event_contract': 'AppGen-X',
                'stream_engine_picker_visible': False,
            }
        )
        return {'ok': ok, 'configuration': deepcopy(self.configuration), 'side_effects': ()}

    def set_parameter(self, name: str, value: Any) -> dict[str, Any]:
        definition = next((item for item in PARAMETER_DEFINITIONS if item['key'] == name), None)
        if definition is None:
            return {'ok': False, 'reason': 'unknown_parameter', 'parameter': name, 'side_effects': ()}
        bounded = definition['minimum'] <= value <= definition['maximum']
        if bounded:
            self.parameters[name] = value
        record = self._insert_record(
            owned_table('runtime_parameter'),
            {
                'tenant': 'system',
                'code': name,
                'title': name.replace('_', ' ').title(),
                'status': 'active' if bounded else 'rejected',
                'score': float(value) if isinstance(value, (int, float)) else None,
                'payload': {'value': value, 'definition': definition, 'bounded': bounded},
            },
        )
        return {'ok': bounded, 'parameter': record, 'side_effects': ()}

    def register_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        if 'stream_engine' in rule or 'stream_engine_picker' in rule:
            return {'ok': False, 'reason': 'stream_engine_picker_disallowed', 'side_effects': ()}
        rule_id = rule.get('rule_id', 'unnamed_rule')
        compiled = {**dict(rule), 'compiled_hash': _digest((rule_id, rule)), 'event_contract': 'AppGen-X'}
        self.rules[rule_id] = compiled
        record = self._insert_record(
            owned_table('policy_rule'),
            {
                'tenant': rule.get('tenant', 'system'),
                'code': rule_id,
                'title': rule_id.replace('_', ' ').title(),
                'status': 'compiled',
                'payload': compiled,
            },
        )
        return {'ok': True, 'rule': record, 'side_effects': ()}

    def register_schema_extension(self, table: str, fields: dict[str, Any]) -> dict[str, Any]:
        full_table = owned_table(table)
        if full_table not in BUSINESS_TABLES:
            return {'ok': False, 'reason': 'unknown_owned_table', 'table': table, 'side_effects': ()}
        self.schema_extensions[full_table] = dict(fields)
        record = self._insert_record(
            owned_table('schema_extension'),
            {
                'tenant': 'system',
                'code': full_table,
                'title': f'Extension for {full_table}',
                'status': 'registered',
                'payload': {'table': full_table, 'fields': dict(fields)},
            },
        )
        return {'ok': True, 'record': record, 'side_effects': ()}

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        idempotency_key = event.get('idempotency_key') or event.get('event_id') or _digest(event)
        if idempotency_key in self.idempotency_keys:
            return {'ok': True, 'duplicate': True, 'idempotency_key': idempotency_key, 'side_effects': ()}
        self.idempotency_keys.add(idempotency_key)
        if event.get('event_type') not in CONSUMED_EVENTS:
            dead = self._append_event(
                EVENT_TABLES[2],
                {
                    'tenant': event.get('tenant', 'system'),
                    'event_type': event.get('event_type', 'Unknown'),
                    'topic': APPGEN_X_TOPIC,
                    'status': 'dead-lettered',
                    'idempotency_key': idempotency_key,
                    'payload': {'event': dict(event), 'retry_policy': {'max_attempts': 5, 'backoff': 'exponential'}},
                },
            )
            return {
                'ok': False,
                'duplicate': False,
                'dead_letter_table': EVENT_TABLES[2],
                'retry_policy': {'max_attempts': 5, 'backoff': 'exponential'},
                'event': dead,
                'side_effects': (),
            }
        inbox = self._append_event(
            EVENT_TABLES[1],
            {
                'tenant': event.get('tenant', 'system'),
                'event_type': event['event_type'],
                'topic': APPGEN_X_TOPIC,
                'status': 'processed',
                'idempotency_key': idempotency_key,
                'payload': dict(event),
            },
        )
        return {'ok': True, 'duplicate': False, 'event': inbox, 'side_effects': ()}

    def operation_contract(self, operation: str) -> dict[str, Any]:
        if operation == 'query_workbench':
            return {
                'operation': operation,
                'operation_kind': 'query',
                'owned_tables': (),
                'read_tables': tuple(BUSINESS_TABLES),
                'emitted_event': None,
                'transaction_boundary': 'read_only_projection',
                'event_contract': 'AppGen-X',
            }
        spec = OPERATION_INDEX[operation]
        return {
            'operation': operation,
            'operation_kind': 'command',
            'owned_tables': (business_table_for_operation(operation),),
            'read_tables': (),
            'emitted_event': spec['event'],
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'event_contract': 'AppGen-X',
        }

    def execute_operation(self, operation: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        if operation not in OPERATION_INDEX:
            return {'ok': False, 'reason': 'unknown_operation', 'operation': operation, 'side_effects': ()}
        spec = OPERATION_INDEX[operation]
        if spec['kind'] == 'rule':
            result = self.register_rule({'rule_id': payload.get('rule_id', payload.get('code', 'compiled_rule')), **payload})
            if not result['ok']:
                return result
            record = result['rule']
            event = self._emit_event(spec['event'], record['tenant'], record['id'], {'rule_id': record['code']})
            return {
                'ok': True,
                'operation': operation,
                'record': record,
                'rows': (record,),
                'event': event,
                'emitted_event': spec['event'],
                'operation_contract': self.operation_contract(operation),
                'side_effects': (),
            }
        materialized = self._materialize_payload(spec, payload)
        record = self._insert_record(business_table_for_operation(operation), materialized)
        event = self._emit_event(spec['event'], record['tenant'], record['id'], {'operation': operation, 'record_id': record['id']})
        response = {
            'ok': True,
            'operation': operation,
            'record': record,
            'rows': (record,),
            'event': event,
            'emitted_event': spec['event'],
            'operation_contract': self.operation_contract(operation),
            'side_effects': (),
        }
        if spec['kind'] == 'calculation':
            response['co2e_total'] = record['payload']['co2e_total']
            response['scope'] = record['payload']['scope']
        if spec['kind'] == 'progress':
            response['progress_percent'] = record['payload']['progress_percent']
        if spec['kind'] == 'scenario':
            response['stressed_emissions'] = record['payload']['stressed_emissions']
        if spec['kind'] == 'packet':
            response['summary'] = record['payload']['summary']
        if spec['kind'] == 'preview':
            response['requires_confirmation'] = True
            response['preview_only'] = True
        return response

    def query_workbench(self, tenant: str = 'default', limit: int = 10) -> dict[str, Any]:
        limit = max(1, min(int(limit), 100))
        recent_packets = self._list_records(owned_table('disclosure_packet'), tenant=tenant, limit=limit)
        open_exceptions = tuple(
            record
            for record in self._list_records(owned_table('assurance_exception'), tenant=tenant, limit=limit)
            if record['status'] != 'resolved'
        )
        summary = {
            'tenant': tenant,
            'metrics_total': len(self._list_records(owned_table('esg_metric'), tenant=tenant)),
            'calculations_total': len(self._list_records(owned_table('emissions_calculation'), tenant=tenant)),
            'open_assurance_exceptions': len(open_exceptions),
            'targets_total': len(self._list_records(owned_table('sustainability_target'), tenant=tenant)),
            'regulator_filings_total': len(self._list_records(owned_table('regulator_filing'), tenant=tenant)),
        }
        return {
            'ok': True,
            'pbc': PBC_KEY,
            'tenant': tenant,
            'view': UI_FRAGMENTS[0],
            'panels': NAVIGATION_SECTIONS,
            'forms': FORM_DEFINITIONS,
            'wizards': WIZARD_DEFINITIONS,
            'controls': CONTROL_DEFINITIONS,
            'summary': summary,
            'recent_disclosure_packets': recent_packets,
            'open_assurance_exceptions': open_exceptions,
            'configuration': deepcopy(self.configuration),
            'action_permissions': PERMISSIONS,
            'side_effects': (),
        }

    def build_workbench_view(self, tenant: str = 'default', limit: int = 10) -> dict[str, Any]:
        return self.query_workbench(tenant=tenant, limit=limit)

    def document_instruction_plan(self, document: str, instruction: str) -> dict[str, Any]:
        lowered = f'{document} {instruction}'.lower()
        candidate_tables = [owned_table('governed_document'), owned_table('governed_instruction'), owned_table('disclosure_packet')]
        if 'renewable' in lowered:
            candidate_tables.append(owned_table('renewable_instrument'))
        if 'water' in lowered:
            candidate_tables.append(owned_table('water_metric_record'))
        if 'waste' in lowered:
            candidate_tables.append(owned_table('waste_metric_record'))
        if 'supplier' in lowered:
            candidate_tables.append(owned_table('supplier_esg_input'))
        if 'board' in lowered:
            candidate_tables.append(owned_table('board_pack'))
        if 'regulator' in lowered or 'filing' in lowered:
            candidate_tables.append(owned_table('regulator_filing'))
        return {
            'ok': True,
            'pbc': PBC_KEY,
            'document_digest': _digest(document),
            'instruction': instruction,
            'candidate_tables': tuple(dict.fromkeys(candidate_tables)),
            'requires_human_confirmation': True,
            'crud_preview': {
                'operation': 'preview',
                'event_contract': 'AppGen-X',
                'mutations': (
                    {'table': owned_table('governed_document'), 'action': 'preview_update'},
                    {'table': owned_table('governed_instruction'), 'action': 'preview_update'},
                ),
            },
            'side_effects': (),
        }

    def datastore_crud_plan(self, action: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        target = owned_table(table or 'governed_document')
        if target not in BUSINESS_TABLES:
            return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
        mutation = action in {'create', 'update', 'delete'}
        preview_only = mutation and target in {owned_table('governed_document'), owned_table('governed_instruction')}
        return {
            'ok': True,
            'pbc': PBC_KEY,
            'action': action,
            'table': target,
            'payload': dict(payload or {}),
            'requires_confirmation': mutation,
            'preview_only': preview_only,
            'event_contract': 'AppGen-X',
            'side_effects': (),
        }

    def dispatch_route(self, path: str, payload: dict[str, Any] | None = None, method: str = 'GET') -> dict[str, Any]:
        route = next((item for item in ROUTE_DEFINITIONS if item['path'] == path and item['method'] == method), None)
        if route is None:
            return {'ok': False, 'reason': 'unknown_route', 'path': path, 'method': method, 'side_effects': ()}
        if route['operation'] == 'query_workbench':
            payload = dict(payload or {})
            return {
                'ok': True,
                'route': route,
                'result': self.query_workbench(tenant=payload.get('tenant', 'default'), limit=payload.get('limit', 10)),
                'side_effects': (),
            }
        if route['operation'] == 'preview_governed_document_change':
            payload = dict(payload or {})
            result = self.document_instruction_plan(payload.get('document', ''), payload.get('instruction', ''))
            return {'ok': result['ok'], 'route': route, 'result': result, 'side_effects': ()}
        if route['operation'] == 'preview_governed_instruction_change':
            payload = dict(payload or {})
            result = self.datastore_crud_plan(payload.get('action', 'update'), table=payload.get('table'), payload=payload.get('payload'))
            return {'ok': result['ok'], 'route': route, 'result': result, 'side_effects': ()}
        result = self.execute_operation(route['operation'], payload)
        return {'ok': result['ok'], 'route': route, 'result': result, 'side_effects': ()}

    def _materialize_payload(self, spec: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        kind = spec['kind']
        status = payload.get('status', 'draft')
        title = payload.get('title') or payload.get('metric_name') or payload.get('activity_type') or spec['name'].replace('_', ' ').title()
        materialized = {
            'tenant': payload.get('tenant', 'default'),
            'code': payload.get('code', _digest((spec['name'], payload))[:10].upper()),
            'title': title,
            'status': status,
            'owner': payload.get('owner', 'sustainability.ops'),
            'period': payload.get('period', payload.get('reporting_period', '2026-Q1')),
            'score': float(payload.get('score', payload.get('materiality_score', 0.0) or 0.0)),
            'payload': dict(payload),
        }
        blueprint = table_blueprint_by_table(business_table_for_operation(spec['name']))
        if blueprint and blueprint.anchor_field:
            anchor_value = payload.get(blueprint.anchor_field) or payload.get(blueprint.anchor_field.removesuffix('_id'))
            materialized[blueprint.anchor_field] = anchor_value
        if kind == 'calculation':
            quantity = float(payload.get('quantity', 0.0))
            factor = float(payload.get('factor_value', 0.0))
            adjustment = float(payload.get('market_adjustment', 1.0))
            if spec['name'] == 'calculate_scope2_emissions':
                location = round(quantity * factor, 4)
                market = round(location * adjustment, 4)
                materialized['payload'].update({'scope': 'scope_2', 'location_based_total': location, 'market_based_total': market, 'co2e_total': market})
            else:
                scope = 'scope_1' if spec['name'] == 'calculate_scope1_emissions' else 'scope_3'
                total = round(quantity * factor * adjustment, 4)
                materialized['payload'].update({'scope': scope, 'co2e_total': total, 'quantity': quantity, 'factor_value': factor})
                materialized['score'] = total
        elif kind == 'progress':
            target = float(payload.get('target_value', 0.0))
            actual = float(payload.get('actual_value', 0.0))
            progress = round(actual / target, 4) if target else 0.0
            materialized['payload'].update({'target_value': target, 'actual_value': actual, 'progress_percent': progress, 'variance': round(actual - target, 4)})
            materialized['score'] = progress
        elif kind == 'scenario':
            baseline = float(payload.get('baseline_emissions', 0.0))
            shock = float(payload.get('shock_percent', 0.0))
            stressed = round(baseline * (1.0 + shock), 4)
            materialized['payload'].update({'baseline_emissions': baseline, 'shock_percent': shock, 'stressed_emissions': stressed})
            materialized['score'] = stressed
            materialized['status'] = payload.get('status', 'simulated')
        elif kind == 'quality':
            completeness = float(payload.get('completeness', 0.0))
            evidence_count = len(tuple(payload.get('evidence', ())))
            quality_score = round(min(1.0, completeness * 0.85 + min(evidence_count, 5) * 0.05), 4)
            materialized['payload'].update({'quality_score': quality_score, 'evidence_count': evidence_count})
            materialized['score'] = quality_score
            materialized['status'] = 'passed' if quality_score >= self.parameters['quality_score_floor'] else 'failed'
        elif kind == 'packet':
            summary = {
                'metrics': len(self.records[owned_table('esg_metric')]),
                'calculations': len(self.records[owned_table('emissions_calculation')]),
                'evidence': len(self.records[owned_table('assurance_evidence')]),
                'exceptions': len(self.records[owned_table('assurance_exception')]),
            }
            materialized['payload'].update({'summary': summary, 'frameworks': tuple(payload.get('frameworks', ('ISSB', 'CSRD', 'GRI'))), 'appgen_topic': APPGEN_X_TOPIC})
            materialized['status'] = payload.get('status', 'draft')
        elif kind == 'metric':
            value = float(payload.get('value', payload.get('quantity', 0.0) or 0.0))
            materialized['payload'].update({'value': value, 'unit': payload.get('unit', 'tbd')})
            materialized['score'] = value
        elif kind == 'control':
            result = payload.get('result', 'pass')
            materialized['payload'].update({'control_result': result, 'sample_size': payload.get('sample_size', 25)})
            materialized['status'] = 'passed' if result == 'pass' else 'failed'
        elif kind == 'preview':
            materialized['status'] = 'preview'
            materialized['payload'].update({'preview_only': True, 'requires_confirmation': True})
        return materialized

    def _append_event(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        record_id = payload.get('id', _digest((table, payload, _utcnow())))
        record = {
            'id': record_id,
            'tenant': payload.get('tenant', 'system'),
            'event_type': payload['event_type'],
            'topic': payload.get('topic', APPGEN_X_TOPIC),
            'status': payload.get('status', 'pending'),
            'idempotency_key': payload['idempotency_key'],
            'payload': dict(payload.get('payload', {})),
            'retry_count': int(payload.get('retry_count', 0)),
            'created_at': _utcnow(),
            'updated_at': _utcnow(),
        }
        self.records[table][record_id] = record
        return record

    def _emit_event(self, event_type: str, tenant: str, record_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._append_event(
            EVENT_TABLES[0],
            {
                'tenant': tenant,
                'event_type': event_type,
                'topic': APPGEN_X_TOPIC,
                'status': 'planned',
                'idempotency_key': _digest((event_type, tenant, record_id, payload)),
                'payload': {'record_id': record_id, **payload},
            },
        )

    def _insert_record(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        blueprint = table_blueprint_by_table(table)
        code = payload.get('code', _digest((table, payload))[:10].upper())
        record_id = payload.get('id', f'{table}:{code.lower()}')
        record = {
            'id': record_id,
            'tenant': payload.get('tenant', 'default'),
            'code': code,
            'title': payload.get('title', blueprint.description if blueprint else table),
            'status': payload.get('status', 'draft'),
            'owner': payload.get('owner', 'sustainability.ops'),
            'period': payload.get('period', '2026-Q1'),
            'score': payload.get('score'),
            'version': int(payload.get('version', 1)),
            'payload': deepcopy(payload.get('payload', {})),
            'created_at': _utcnow(),
            'updated_at': _utcnow(),
        }
        if blueprint and blueprint.anchor_field:
            record[blueprint.anchor_field] = payload.get(blueprint.anchor_field)
        self.records[table][record_id] = record
        return record

    def _list_records(self, table: str, tenant: str | None = None, limit: int | None = None) -> tuple[dict[str, Any], ...]:
        rows = tuple(self.records[table].values())
        if tenant is not None:
            rows = tuple(item for item in rows if item.get('tenant') == tenant)
        rows = tuple(sorted(rows, key=lambda item: item['created_at'], reverse=True))
        if limit is not None:
            rows = rows[: int(limit)]
        return rows


def build_standalone_app() -> SustainabilityEsgReportingSliceApp:
    return SustainabilityEsgReportingSliceApp()


def build_service_contract() -> dict[str, Any]:
    command_methods = _dedupe(
        (
            'configure_runtime',
            'set_parameter',
            'register_rule',
            'register_schema_extension',
            'receive_event',
            'document_instruction_plan',
            'datastore_crud_plan',
        )
        + tuple(DOMAIN_OPERATIONS)
    )
    query_methods = ('query_workbench', 'build_workbench_view')
    return {
        'format': f'appgen.{PBC_KEY}.service-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'command_methods': command_methods,
        'query_methods': query_methods,
        'shared_table_access': False,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'world_class_domain_depth': domain_depth_contract(),
        'side_effects': (),
    }


def build_api_contract() -> dict[str, Any]:
    routes = tuple(
        {
            **route,
            'pbc': PBC_KEY,
            'idempotency_key': f"{PBC_KEY}:{route['method']}:{route['path']}",
            'required_permission': f'{PBC_KEY}.read' if route['method'] == 'GET' else f'{PBC_KEY}.operate',
            'event_contract': 'AppGen-X',
            'shared_table_access': False,
            'stream_engine_picker_visible': False,
        }
        for route in ROUTE_DEFINITIONS
    )
    return {
        'format': f'appgen.{PBC_KEY}.api-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'routes': routes,
        'side_effects': (),
    }


def build_event_contract() -> dict[str, Any]:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'contract': 'AppGen-X',
        'event_topic': APPGEN_X_TOPIC,
        'emitted': EMITTED_EVENTS,
        'consumed': CONSUMED_EVENTS,
        'outbox_table': EVENT_TABLES[0],
        'inbox_table': EVENT_TABLES[1],
        'dead_letter_table': EVENT_TABLES[2],
        'idempotency': 'required',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def build_handler_manifest() -> dict[str, Any]:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'handlers': tuple(
            {
                'event_type': event_type,
                'idempotency_key_template': f'{PBC_KEY}:{event_type}:<event_id>',
                'retry_policy': {'max_attempts': 5, 'backoff': 'exponential'},
                'dead_letter_table': EVENT_TABLES[2],
            }
            for event_type in CONSUMED_EVENTS
        ),
        'side_effects': (),
    }


def build_ui_contract() -> dict[str, Any]:
    surface = ui_capability_surface_contract()
    return {
        'ok': surface['ok'],
        'pbc': PBC_KEY,
        'fragments': UI_FRAGMENTS,
        'workbench_view': UI_FRAGMENTS[0],
        'configuration_editor': True,
        'forms': FORM_DEFINITIONS,
        'wizards': WIZARD_DEFINITIONS,
        'controls': CONTROL_DEFINITIONS,
        'advanced_panels': tuple(surface['advanced_panels']),
        'navigation_sections': tuple(surface['navigation_sections']),
        'action_permissions': tuple(PERMISSIONS),
        'agent_tools': tuple(surface['agent_tools']),
        'stream_engine_picker_visible': False,
        'full_capability_surface': surface,
        'side_effects': (),
    }


def build_agent_contract() -> dict[str, Any]:
    skills = tuple(
        {
            'name': f'{PBC_KEY}_{operation}',
            'scope': PBC_KEY,
            'description': f'{operation.replace("_", " ")} for {PBC_KEY}',
            'requires_confirmation_for_mutation': operation.startswith('preview_governed_') or operation in {'record_restatement', 'file_regulator_filing'},
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        }
        for operation in (
            'guide_user',
            'query_workbench',
            'define_esg_metric',
            'capture_activity_data',
            'calculate_scope1_emissions',
            'calculate_scope2_emissions',
            'calculate_scope3_emissions',
            'build_disclosure_packet',
            'prepare_board_pack',
            'file_regulator_filing',
            'preview_governed_document_change',
            'preview_governed_instruction_change',
        )
    )
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'skills': skills,
        'single_agent_contribution': f'{PBC_KEY}_skills',
        'dsl_tools': (f'{PBC_KEY}_skills', f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'),
        'side_effects': (),
    }


def build_permissions_contract() -> dict[str, Any]:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'permissions': PERMISSIONS,
        'rbac_roles': ('reader', 'operator', 'approver', 'admin'),
        'side_effects': (),
    }


def build_configuration_contract() -> dict[str, Any]:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'database_backends': ALLOWED_DATABASE_BACKENDS,
        'event_topic': APPGEN_X_TOPIC,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'parameter_schema': PARAMETER_DEFINITIONS,
        'rule_schema': RULE_DEFINITIONS,
        'side_effects': (),
    }


def verify_owned_table_boundary(references: tuple[str, ...] | list[str]) -> dict[str, Any]:
    allowed = set(RUNTIME_TABLES) | set(CONSUMED_EVENTS) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {
        'ok': not foreign,
        'foreign_references': foreign,
        'allowed_dependency_modes': ('api', 'event', 'projection'),
        'side_effects': (),
    }


def slice_app_smoke_test() -> dict[str, Any]:
    app = build_standalone_app()
    config = app.configure_runtime({'database_backend': 'postgresql', 'event_topic': APPGEN_X_TOPIC})
    metric = app.execute_operation('define_esg_metric', {'tenant': 'tenant-smoke', 'code': 'METRIC-NET-ZERO', 'metric_name': 'Net Zero CO2e', 'framework': 'ISSB', 'materiality_score': 0.88})
    materiality = app.execute_operation('assess_materiality', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'stakeholders': ('investors', 'communities'), 'materiality_score': 0.91})
    facility = app.execute_operation('register_facility_profile', {'tenant': 'tenant-smoke', 'code': 'FAC-001', 'title': 'Nairobi Plant', 'country': 'KE'})
    activity = app.execute_operation('capture_activity_data', {'tenant': 'tenant-smoke', 'facility_id': facility['record']['id'], 'activity_type': 'diesel', 'quantity': 125.0, 'unit': 'liters'})
    factor = app.execute_operation('register_emissions_factor', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'factor_value': 2.68, 'geography': 'KE', 'year': 2026})
    scope1 = app.execute_operation('calculate_scope1_emissions', {'tenant': 'tenant-smoke', 'activity_record_id': activity['record']['id'], 'quantity': 125.0, 'factor_value': 2.68})
    renewable = app.execute_operation('record_renewable_instrument', {'tenant': 'tenant-smoke', 'facility_id': facility['record']['id'], 'certificate_type': 'I-REC', 'retired': True})
    water = app.execute_operation('record_water_metric', {'tenant': 'tenant-smoke', 'facility_id': facility['record']['id'], 'value': 410.5, 'unit': 'm3'})
    social = app.execute_operation('record_social_metric', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'value': 0.42, 'unit': 'ratio'})
    governance = app.execute_operation('record_governance_metric', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'value': 1.0, 'unit': 'index'})
    supplier = app.execute_operation('ingest_supplier_esg_input', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'supplier_name': 'Acme Steel', 'quality_score': 0.81})
    target = app.execute_operation('create_sustainability_target', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'target_value': 100.0, 'baseline_value': 150.0, 'target_year': 2030})
    progress = app.execute_operation('measure_target_progress', {'tenant': 'tenant-smoke', 'target_id': target['record']['id'], 'target_value': 100.0, 'actual_value': 72.0})
    framework = app.execute_operation('map_reporting_framework', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'frameworks': ('ISSB', 'CSRD', 'GRI')})
    evidence = app.execute_operation('attach_assurance_evidence', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'evidence_uri': 's3://bucket/evidence.pdf'})
    control = app.execute_operation('run_assurance_control_test', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'result': 'pass', 'sample_size': 30})
    exception = app.execute_operation('open_assurance_exception', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'title': 'Supplier evidence gap', 'severity': 'medium'})
    restatement = app.execute_operation('record_restatement', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'reason': 'supplier correction'})
    scenario = app.execute_operation('simulate_climate_scenario', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'baseline_emissions': 200.0, 'shock_percent': 0.15})
    quality = app.execute_operation('run_data_quality_check', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'completeness': 0.97, 'evidence': ('meter.csv', 'invoice.pdf')})
    packet = app.execute_operation('build_disclosure_packet', {'tenant': 'tenant-smoke', 'metric_id': metric['record']['id'], 'frameworks': ('ISSB', 'CSRD'), 'report_type': 'annual'})
    board = app.execute_operation('prepare_board_pack', {'tenant': 'tenant-smoke', 'disclosure_packet_id': packet['record']['id'], 'title': 'Q1 Board Pack'})
    filing = app.execute_operation('file_regulator_filing', {'tenant': 'tenant-smoke', 'disclosure_packet_id': packet['record']['id'], 'regulator': 'SEC', 'jurisdiction': 'US'})
    document = app.document_instruction_plan('Prepare the board pack and regulator filing.', 'preview governed edits for the disclosure narrative')
    crud = app.datastore_crud_plan('update', table=owned_table('governed_document'), payload={'status': 'preview'})
    received = app.receive_event({'event_type': CONSUMED_EVENTS[0], 'event_id': 'evt-1', 'tenant': 'tenant-smoke'})
    duplicate = app.receive_event({'event_type': CONSUMED_EVENTS[0], 'event_id': 'evt-1', 'tenant': 'tenant-smoke'})
    dead = app.receive_event({'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad', 'tenant': 'tenant-smoke'})
    workbench = app.build_workbench_view(tenant='tenant-smoke', limit=5)
    route = app.dispatch_route('/sustainability-esg-reporting-workbench', {'tenant': 'tenant-smoke', 'limit': 5}, method='GET')
    checks = (
        config['ok'],
        metric['ok'],
        materiality['ok'],
        facility['ok'],
        activity['ok'],
        factor['ok'],
        scope1['co2e_total'] > 0,
        renewable['ok'],
        water['ok'],
        social['ok'],
        governance['ok'],
        supplier['ok'],
        target['ok'],
        progress['progress_percent'] > 0,
        framework['ok'],
        evidence['ok'],
        control['ok'],
        exception['ok'],
        restatement['ok'],
        scenario['stressed_emissions'] > 0,
        quality['record']['status'] == 'passed',
        packet['summary']['metrics'] >= 1,
        board['ok'],
        filing['ok'],
        document['ok'],
        crud['ok'],
        received['ok'],
        duplicate['duplicate'] is True,
        dead['ok'] is False,
        workbench['summary']['metrics_total'] >= 1,
        route['ok'],
    )
    return {
        'ok': all(checks),
        'state': app.empty_state(),
        'side_effects': (),
    }


def pbc_source_artifact_contract() -> dict[str, Any]:
    existing = tuple(path for path in RELEASE_ARTIFACTS if (PACKAGE_DIR / path).exists())
    missing = tuple(path for path in RELEASE_ARTIFACTS if path not in existing)
    migration_sql = MIGRATION_PATH.read_text(encoding='utf-8')
    return {
        'ok': not missing and 'CREATE TABLE' in migration_sql,
        'pbc': PBC_KEY,
        'schema_contract': build_schema_contract(),
        'missing_artifacts': missing,
        'migration_path': str(MIGRATION_PATH.relative_to(PACKAGE_DIR)),
        'side_effects': (),
    }


def pbc_package_audit() -> dict[str, Any]:
    from .manifest import PBC_MANIFEST

    schema = build_schema_contract()
    service = build_service_contract()
    return {
        'ok': PBC_MANIFEST['pbc'] == PBC_KEY and schema['ok'] and service['ok'],
        'pbc': PBC_KEY,
        'manifest': PBC_MANIFEST,
        'schema_table_count': len(schema['owned_tables']),
        'service_command_count': len(service['command_methods']),
        'side_effects': (),
    }


def pbc_specification_audit() -> dict[str, Any]:
    specification = SPECIFICATION_PATH.read_text(encoding='utf-8')
    required_terms = (
        'materiality',
        'Scope 1/2/3',
        'renewable',
        'water',
        'waste',
        'social',
        'governance',
        'board packs',
        'regulator filings',
        'AppGen-X',
    )
    missing = tuple(term for term in required_terms if term not in specification)
    return {
        'ok': not missing,
        'pbc': PBC_KEY,
        'missing_terms': missing,
        'side_effects': (),
    }


def pbc_agent_audit() -> dict[str, Any]:
    app = build_standalone_app()
    contract = build_agent_contract()
    document = app.document_instruction_plan('Update the waste and water disclosure.', 'preview the board and regulator narrative changes')
    crud = app.datastore_crud_plan('update', table=owned_table('governed_document'), payload={'status': 'preview'})
    rejected = app.datastore_crud_plan('update', table='foreign_table')
    return {
        'ok': contract['ok'] and document['ok'] and crud['ok'] and rejected['ok'] is False,
        'pbc': PBC_KEY,
        'contract': contract,
        'side_effects': (),
    }


def pbc_implementation_release_audit() -> dict[str, Any]:
    service = build_service_contract()
    api = build_api_contract()
    ui = build_ui_contract()
    events = build_event_contract()
    boundary = verify_owned_table_boundary(tuple(RUNTIME_TABLES) + ('api_dependency',))
    smoke = slice_app_smoke_test()
    checks = (
        {'id': 'service_contract', 'ok': service['ok']},
        {'id': 'api_contract', 'ok': api['ok']},
        {'id': 'ui_surface', 'ok': ui['ok'] and bool(ui['forms']) and bool(ui['wizards']) and bool(ui['controls'])},
        {'id': 'event_contract', 'ok': events['ok'] and events['contract'] == 'AppGen-X'},
        {'id': 'owned_boundary', 'ok': boundary['ok']},
        {'id': 'slice_smoke', 'ok': smoke['ok']},
    )
    return {
        'ok': all(check['ok'] for check in checks),
        'pbc': PBC_KEY,
        'checks': checks,
        'smoke': smoke,
        'side_effects': (),
    }


def pbc_capability_audit() -> dict[str, Any]:
    domain = domain_depth_contract()
    surface = ui_capability_surface_contract()
    return {
        'ok': domain['ok']
        and surface['ok']
        and len(STANDARD_FEATURES) >= 20
        and len(ADVANCED_CAPABILITIES) >= 10
        and bool(FORM_DEFINITIONS)
        and bool(WIZARD_DEFINITIONS)
        and bool(CONTROL_DEFINITIONS),
        'pbc': PBC_KEY,
        'standard_features': STANDARD_FEATURES,
        'advanced_capabilities': ADVANCED_CAPABILITIES,
        'surface': surface,
        'side_effects': (),
    }


def pbc_generation_smoke_audit() -> dict[str, Any]:
    models = build_models_contract()
    api = build_api_contract()
    smoke = slice_app_smoke_test()
    return {
        'ok': models['ok'] and api['ok'] and smoke['ok'],
        'pbc': PBC_KEY,
        'route_count': len(api['routes']),
        'model_count': len(models['models']),
        'smoke': smoke,
        'side_effects': (),
    }


def build_release_evidence() -> dict[str, Any]:
    source = pbc_source_artifact_contract()
    package = pbc_package_audit()
    specification = pbc_specification_audit()
    agent = pbc_agent_audit()
    implementation = pbc_implementation_release_audit()
    capability = pbc_capability_audit()
    generation = pbc_generation_smoke_audit()
    checks = (
        {'id': 'pbc_source_artifact_contract', 'ok': source['ok']},
        {'id': 'pbc_package_audit', 'ok': package['ok']},
        {'id': 'pbc_specification_audit', 'ok': specification['ok']},
        {'id': 'pbc_agent_audit', 'ok': agent['ok']},
        {'id': 'pbc_implementation_release_audit', 'ok': implementation['ok']},
        {'id': 'pbc_capability_audit', 'ok': capability['ok']},
        {'id': 'pbc_generation_smoke_audit', 'ok': generation['ok']},
        {'id': 'owned_table_depth', 'ok': len(BUSINESS_TABLES) >= 24},
        {'id': 'domain_operation_depth', 'ok': len(DOMAIN_OPERATIONS) >= 20},
        {'id': 'forms_wizards_controls_present', 'ok': bool(FORM_DEFINITIONS) and bool(WIZARD_DEFINITIONS) and bool(CONTROL_DEFINITIONS)},
    )
    return {
        'format': f'appgen.{PBC_KEY}.release-evidence.v1',
        'ok': all(check['ok'] for check in checks),
        'pbc': PBC_KEY,
        'checks': checks,
        'blocking_gaps': tuple(check['id'] for check in checks if not check['ok']),
        'boundary_gaps': source['schema_contract'].get('boundary_gaps', ()),
        'audits': {
            'pbc_source_artifact_contract': source,
            'pbc_package_audit': package,
            'pbc_specification_audit': specification,
            'pbc_agent_audit': agent,
            'pbc_implementation_release_audit': implementation,
            'pbc_capability_audit': capability,
            'pbc_generation_smoke_audit': generation,
        },
        'side_effects': (),
    }


def build_runtime_capabilities() -> dict[str, Any]:
    smoke = slice_app_smoke_test()
    service = build_service_contract()
    return {
        'format': f'appgen.{PBC_KEY}.runtime-capabilities.v1',
        'ok': smoke['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': 'src/pyAppGen/pbcs/sustainability_esg_reporting',
        'owned_tables': tuple(RUNTIME_TABLES),
        'allowed_database_backends': ALLOWED_DATABASE_BACKENDS,
        'capabilities': tuple(ADVANCED_CAPABILITIES),
        'standard_features': tuple(STANDARD_FEATURES),
        'operations': _dedupe(tuple(service['command_methods'] + service['query_methods'])),
        'world_class_domain_depth': domain_depth_contract(),
        'domain_depth_smoke': domain_depth_smoke_test(),
        'smoke': smoke,
        'side_effects': (),
    }
