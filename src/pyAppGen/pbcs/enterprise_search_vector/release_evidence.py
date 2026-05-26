"""Generated release evidence for the enterprise_search_vector PBC."""

import importlib.util
from pathlib import Path


RELEASE_EVIDENCE = {'format': 'appgen.enterprise-search-vector-release-evidence.v1', 'ok': True, 'pbc': 'enterprise_search_vector', 'checks': ({'id': 'owned_schema_depth', 'ok': True}, {'id': 'migration_per_owned_table', 'ok': True}, {'id': 'model_per_owned_table', 'ok': True}, {'id': 'service_contract_depth', 'ok': True}, {'id': 'generated_runtime_artifacts', 'ok': True}, {'id': 'appgen_event_contract_only', 'ok': True}, {'id': 'backend_allowlist', 'ok': True}, {'id': 'runtime_event_tables_owned', 'ok': True}, {'id': 'no_shared_table_access', 'ok': True}, {'id': 'permissions_cover_release_queries', 'ok': True}), 'blocking_gaps': (), 'schema': {'format': 'appgen.enterprise-search-vector-owned-schema-contract.v1', 'ok': True, 'pbc': 'enterprise_search_vector', 'owned_tables': ('search_index', 'embedding_job', 'vector_document', 'query_trace', 'enterprise_search_vector_appgen_outbox_event', 'enterprise_search_vector_appgen_inbox_event', 'enterprise_search_vector_dead_letter_event'), 'business_tables': ('search_index', 'embedding_job', 'vector_document', 'query_trace'), 'runtime_tables': ('enterprise_search_vector_appgen_outbox_event', 'enterprise_search_vector_appgen_inbox_event', 'enterprise_search_vector_dead_letter_event'), 'tables': ({'table': 'search_index', 'schema': 'enterprise_search_vector', 'pbc': 'enterprise_search_vector', 'owned': True, 'migration': 'pbcs/enterprise_search_vector/migrations/001_search_index.sql', 'model': 'pbcs/enterprise_search_vector/models/SearchIndex.py', 'fields': ({'name': 'id', 'type': 'uuid', 'required': True}, {'name': 'tenant', 'type': 'text', 'required': True}, {'name': 'created_at', 'type': 'timestamp', 'required': True}, {'name': 'updated_at', 'type': 'timestamp', 'required': True}, {'name': 'index_id', 'type': 'text', 'required': True}, {'name': 'source', 'type': 'text', 'required': True}, {'name': 'locale', 'type': 'text', 'required': True}, {'name': 'status', 'type': 'text', 'required': True}), 'relationships': ()}, {'table': 'embedding_job', 'schema': 'enterprise_search_vector', 'pbc': 'enterprise_search_vector', 'owned': True, 'migration': 'pbcs/enterprise_search_vector/migrations/002_embedding_job.sql', 'model': 'pbcs/enterprise_search_vector/models/EmbeddingJob.py', 'fields': ({'name': 'id', 'type': 'uuid', 'required': True}, {'name': 'tenant', 'type': 'text', 'required': True}, {'name': 'created_at', 'type': 'timestamp', 'required': True}, {'name': 'updated_at', 'type': 'timestamp', 'required': True}, {'name': 'job_id', 'type': 'text', 'required': True}, {'name': 'index_id', 'type': 'text', 'required': True}, {'name': 'document_ids', 'type': 'jsonb', 'required': True}, {'name': 'status', 'type': 'text', 'required': True}), 'relationships': ({'type': 'owned_reference', 'from': 'embedding_job', 'to': 'search_index', 'field': 'index_id'},)}, {'table': 'vector_document', 'schema': 'enterprise_search_vector', 'pbc': 'enterprise_search_vector', 'owned': True, 'migration': 'pbcs/enterprise_search_vector/migrations/003_vector_document.sql', 'model': 'pbcs/enterprise_search_vector/models/VectorDocument.py', 'fields': ({'name': 'id', 'type': 'uuid', 'required': True}, {'name': 'tenant', 'type': 'text', 'required': True}, {'name': 'created_at', 'type': 'timestamp', 'required': True}, {'name': 'updated_at', 'type': 'timestamp', 'required': True}, {'name': 'document_id', 'type': 'text', 'required': True}, {'name': 'index_id', 'type': 'text', 'required': True}, {'name': 'body', 'type': 'text', 'required': True}, {'name': 'embedding', 'type': 'jsonb', 'required': False}, {'name': 'acl', 'type': 'jsonb', 'required': True}), 'relationships': ({'type': 'owned_reference', 'from': 'vector_document', 'to': 'search_index', 'field': 'index_id'},)}, {'table': 'query_trace', 'schema': 'enterprise_search_vector', 'pbc': 'enterprise_search_vector', 'owned': True, 'migration': 'pbcs/enterprise_search_vector/migrations/004_query_trace.sql', 'model': 'pbcs/enterprise_search_vector/models/QueryTrace.py', 'fields': ({'name': 'id', 'type': 'uuid', 'required': True}, {'name': 'tenant', 'type': 'text', 'required': True}, {'name': 'created_at', 'type': 'timestamp', 'required': True}, {'name': 'updated_at', 'type': 'timestamp', 'required': True}, {'name': 'query_id', 'type': 'text', 'required': True}, {'name': 'query_text', 'type': 'text', 'required': True}, {'name': 'principal_permissions', 'type': 'jsonb', 'required': True}, {'name': 'results', 'type': 'jsonb', 'required': True}), 'relationships': ({'type': 'acl_projection', 'from': 'query_trace', 'to': 'vector_document', 'via': 'result_document_ids'},)}, {'table': 'enterprise_search_vector_appgen_outbox_event', 'schema': 'enterprise_search_vector', 'pbc': 'enterprise_search_vector', 'owned': True, 'migration': 'pbcs/enterprise_search_vector/migrations/005_enterprise_search_vector_appgen_outbox_event.sql', 'model': 'pbcs/enterprise_search_vector/models/EnterpriseSearchVectorAppgenOutboxEvent.py', 'fields': ({'name': 'id', 'type': 'uuid', 'required': True}, {'name': 'tenant', 'type': 'text', 'required': True}, {'name': 'created_at', 'type': 'timestamp', 'required': True}, {'name': 'updated_at', 'type': 'timestamp', 'required': True}, {'name': 'event_type', 'type': 'text', 'required': True}, {'name': 'payload', 'type': 'jsonb', 'required': True}, {'name': 'idempotency_key', 'type': 'text', 'required': True}), 'relationships': ({'type': 'event_contract', 'to': 'AppGen-X', 'topic': 'appgen.enterprise_search_vector.events'},)}, {'table': 'enterprise_search_vector_appgen_inbox_event', 'schema': 'enterprise_search_vector', 'pbc': 'enterprise_search_vector', 'owned': True, 'migration': 'pbcs/enterprise_search_vector/migrations/006_enterprise_search_vector_appgen_inbox_event.sql', 'model': 'pbcs/enterprise_search_vector/models/EnterpriseSearchVectorAppgenInboxEvent.py', 'fields': ({'name': 'id', 'type': 'uuid', 'required': True}, {'name': 'tenant', 'type': 'text', 'required': True}, {'name': 'created_at', 'type': 'timestamp', 'required': True}, {'name': 'updated_at', 'type': 'timestamp', 'required': True}, {'name': 'event_type', 'type': 'text', 'required': True}, {'name': 'payload', 'type': 'jsonb', 'required': True}, {'name': 'attempts', 'type': 'integer', 'required': True}), 'relationships': ({'type': 'event_contract', 'to': 'AppGen-X', 'topic': 'appgen.enterprise_search_vector.events'},)}, {'table': 'enterprise_search_vector_dead_letter_event', 'schema': 'enterprise_search_vector', 'pbc': 'enterprise_search_vector', 'owned': True, 'migration': 'pbcs/enterprise_search_vector/migrations/007_enterprise_search_vector_dead_letter_event.sql', 'model': 'pbcs/enterprise_search_vector/models/EnterpriseSearchVectorDeadLetterEvent.py', 'fields': ({'name': 'id', 'type': 'uuid', 'required': True}, {'name': 'tenant', 'type': 'text', 'required': True}, {'name': 'created_at', 'type': 'timestamp', 'required': True}, {'name': 'updated_at', 'type': 'timestamp', 'required': True}, {'name': 'event_type', 'type': 'text', 'required': True}, {'name': 'payload', 'type': 'jsonb', 'required': True}, {'name': 'reason', 'type': 'text', 'required': True}), 'relationships': ({'type': 'event_contract', 'to': 'AppGen-X', 'topic': 'appgen.enterprise_search_vector.events'},)}), 'migrations': ('pbcs/enterprise_search_vector/migrations/001_search_index.sql', 'pbcs/enterprise_search_vector/migrations/002_embedding_job.sql', 'pbcs/enterprise_search_vector/migrations/003_vector_document.sql', 'pbcs/enterprise_search_vector/migrations/004_query_trace.sql', 'pbcs/enterprise_search_vector/migrations/005_enterprise_search_vector_appgen_outbox_event.sql', 'pbcs/enterprise_search_vector/migrations/006_enterprise_search_vector_appgen_inbox_event.sql', 'pbcs/enterprise_search_vector/migrations/007_enterprise_search_vector_dead_letter_event.sql'), 'models': ('pbcs/enterprise_search_vector/models/SearchIndex.py', 'pbcs/enterprise_search_vector/models/EmbeddingJob.py', 'pbcs/enterprise_search_vector/models/VectorDocument.py', 'pbcs/enterprise_search_vector/models/QueryTrace.py', 'pbcs/enterprise_search_vector/models/EnterpriseSearchVectorAppgenOutboxEvent.py', 'pbcs/enterprise_search_vector/models/EnterpriseSearchVectorAppgenInboxEvent.py', 'pbcs/enterprise_search_vector/models/EnterpriseSearchVectorDeadLetterEvent.py'), 'database_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'tenant_isolation': {'field': 'tenant', 'required': True}, 'schema_extensions': {'allowed': True, 'owned_tables_only': True}, 'declared_dependencies': {'apis': ('POST /indexes', 'POST /indexes/{id}/refresh', 'POST /embeddings', 'POST /search', 'POST /query-feedback', 'GET /query-traces'), 'events': ('ProductPublished', 'CustomerUpdated', 'AuditEventSealed'), 'shared_tables': ()}}, 'service': {'format': 'appgen.enterprise-search-vector-service-contract.v1', 'ok': True, 'pbc': 'enterprise_search_vector', 'transaction_boundary': 'enterprise_search_vector_owned_datastore_plus_appgen_outbox', 'command_methods': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'create_index', 'ingest_document', 'run_embedding_job', 'refresh_index', 'query', 'record_feedback', 'build_workbench_view', 'verify_owned_table_boundary', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'simulate_counterfactual_ranking', 'forecast_index_freshness', 'remediate_search_quality', 'screen_search_policy', 'run_relevance_controls', 'generate_index_proof', 'federate_search_sources'), 'query_methods': ('build_api_contract', 'permissions_contract', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence'), 'mutates_only': ('search_index', 'embedding_job', 'vector_document', 'query_trace', 'enterprise_search_vector_appgen_outbox_event', 'enterprise_search_vector_appgen_inbox_event', 'enterprise_search_vector_dead_letter_event'), 'external_dependencies': {'apis': ('POST /indexes', 'POST /indexes/{id}/refresh', 'POST /embeddings', 'POST /search', 'POST /query-feedback', 'GET /query-traces'), 'events': ('ProductPublished', 'CustomerUpdated', 'AuditEventSealed'), 'shared_tables': ()}, 'eventing': {'contract': 'AppGen-X', 'topic': 'appgen.enterprise_search_vector.events', 'outbox_table': 'enterprise_search_vector_appgen_outbox_event', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'dead_letter_table': 'enterprise_search_vector_dead_letter_event', 'idempotency_required': True}, 'idempotent_handlers': ('receive_event',), 'retry_dead_letter_evidence': {'retry_limit_field': 'retry_limit', 'dead_letter_table': 'enterprise_search_vector_dead_letter_event'}, 'generated_artifacts': {'services': ('pbcs/enterprise_search_vector/services/search_service.py',), 'routes': ('pbcs/enterprise_search_vector/routes/search_routes.py',), 'events': ('pbcs/enterprise_search_vector/events/search_events.py',), 'handlers': ('pbcs/enterprise_search_vector/handlers/search_handlers.py',), 'ui': ('pbcs/enterprise_search_vector/ui/workbench.py',)}, 'shared_table_access': False}, 'api': {'format': 'appgen.enterprise-search-vector-api-contract.v1', 'ok': True, 'routes': ('POST /indexes', 'POST /indexes/{id}/refresh', 'POST /embeddings', 'POST /search', 'POST /query-feedback', 'GET /query-traces'), 'shared_table_access': False, 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'database_backends': ('postgresql', 'mysql', 'mariadb'), 'emits': ('SearchIndexUpdated', 'DiscoveryInsightGenerated'), 'consumes': ('ProductPublished', 'CustomerUpdated', 'AuditEventSealed'), 'owned_tables': ('search_index', 'embedding_job', 'vector_document', 'query_trace')}, 'permissions': {'format': 'appgen.enterprise-search-vector-permissions.v1', 'ok': True, 'permissions': ('enterprise_search_vector.index.write', 'enterprise_search_vector.document.write', 'enterprise_search_vector.query', 'enterprise_search_vector.event.consume', 'enterprise_search_vector.configure', 'enterprise_search_vector.audit'), 'action_permissions': {'create_index': 'enterprise_search_vector.index.write', 'refresh_index': 'enterprise_search_vector.index.write', 'run_embedding_job': 'enterprise_search_vector.document.write', 'ingest_document': 'enterprise_search_vector.document.write', 'query': 'enterprise_search_vector.query', 'record_feedback': 'enterprise_search_vector.query', 'receive_event': 'enterprise_search_vector.event.consume', 'register_rule': 'enterprise_search_vector.configure', 'register_schema_extension': 'enterprise_search_vector.configure', 'set_parameter': 'enterprise_search_vector.configure', 'configure_runtime': 'enterprise_search_vector.configure', 'build_workbench_view': 'enterprise_search_vector.audit', 'verify_owned_table_boundary': 'enterprise_search_vector.audit', 'build_schema_contract': 'enterprise_search_vector.audit', 'build_service_contract': 'enterprise_search_vector.audit', 'build_release_evidence': 'enterprise_search_vector.audit'}}}


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
    evidence.setdefault('pbc', 'enterprise_search_vector')
    return evidence


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
        'pbc': 'enterprise_search_vector',
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
        'pbc': 'enterprise_search_vector',
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
