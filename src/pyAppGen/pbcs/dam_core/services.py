"""Command service layer for the dam_core PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.dam_core.events', 'inbox_topic': 'pbc.dam_core.inbox', 'outbox_table': 'dam_core_appgen_outbox_event', 'inbox_table': 'dam_core_appgen_inbox_event', 'dead_letter_table': 'dam_core_appgen_dead_letter_event', 'emitted': ({'event_type': 'AssetPublished', 'schema': 'dam_core.asset_published.emitted.v1', 'topic': 'pbc.dam_core.events', 'outbox_table': 'dam_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'RightsPolicyChanged', 'schema': 'dam_core.rights_policy_changed.emitted.v1', 'topic': 'pbc.dam_core.events', 'outbox_table': 'dam_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductPublished', 'schema': 'dam_core.product_published.consumed.v1', 'topic': 'pbc.dam_core.inbox', 'inbox_table': 'dam_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')},), 'retry_policy': {'name': 'dam_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'dam_core_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_assets', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/assets', 'permission': 'dam_core.command.1', 'owned_tables': ('dam_core_asset', 'dam_core_asset_rendition', 'dam_core_rights_policy', 'dam_core_metadata_tag'), 'read_tables': (), 'emitted_event': 'AssetPublished', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_renditions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/renditions', 'permission': 'dam_core.command.2', 'owned_tables': ('dam_core_asset', 'dam_core_asset_rendition', 'dam_core_rights_policy', 'dam_core_metadata_tag'), 'read_tables': (), 'emitted_event': 'RightsPolicyChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_rights', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/dam_core/rights', 'permission': 'dam_core.query.3', 'owned_tables': (), 'read_tables': ('dam_core_asset', 'dam_core_asset_rendition', 'dam_core_rights_policy', 'dam_core_metadata_tag'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})

OPERATION_CONTRACTS = OPERATION_CONTRACTS + (
    {'operation': 'command_collections', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/collections', 'permission': 'dam_core.asset.write', 'owned_tables': ('dam_core_asset_collection',), 'read_tables': (), 'emitted_event': 'AssetCollectionCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_collection_members', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/collection-members', 'permission': 'dam_core.asset.write', 'owned_tables': ('dam_core_asset_collection_member',), 'read_tables': (), 'emitted_event': 'AssetAddedToCollection', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_license_agreements', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/license-agreements', 'permission': 'dam_core.rights.manage', 'owned_tables': ('dam_core_license_agreement',), 'read_tables': (), 'emitted_event': 'LicenseAgreementRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_usage_entitlements', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/usage-entitlements', 'permission': 'dam_core.rights.manage', 'owned_tables': ('dam_core_usage_entitlement',), 'read_tables': (), 'emitted_event': 'UsageEntitlementGranted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_metadata_taxonomies', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/metadata-taxonomies', 'permission': 'dam_core.metadata.write', 'owned_tables': ('dam_core_metadata_taxonomy',), 'read_tables': (), 'emitted_event': 'MetadataTaxonomyRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_metadata_enrichments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/metadata-enrichments', 'permission': 'dam_core.metadata.write', 'owned_tables': ('dam_core_metadata_enrichment',), 'read_tables': (), 'emitted_event': 'MetadataEnriched', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_semantic_annotations', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/semantic-annotations', 'permission': 'dam_core.metadata.write', 'owned_tables': ('dam_core_semantic_annotation',), 'read_tables': (), 'emitted_event': 'SemanticAnnotationAdded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_asset_workflows', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/asset-workflows', 'permission': 'dam_core.workflow', 'owned_tables': ('dam_core_asset_workflow_case', 'dam_core_asset_review_task'), 'read_tables': (), 'emitted_event': 'AssetWorkflowStarted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_review_tasks', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/review-tasks', 'permission': 'dam_core.workflow', 'owned_tables': ('dam_core_asset_review_task',), 'read_tables': (), 'emitted_event': 'AssetReviewTaskCompleted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_asset_exceptions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/asset-exceptions', 'permission': 'dam_core.workflow', 'owned_tables': ('dam_core_asset_exception',), 'read_tables': (), 'emitted_event': 'AssetExceptionOpened', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_exception_resolutions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/exception-resolutions', 'permission': 'dam_core.workflow', 'owned_tables': ('dam_core_asset_exception',), 'read_tables': (), 'emitted_event': 'AssetExceptionResolved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_usage_snapshots', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/usage-snapshots', 'permission': 'dam_core.audit', 'owned_tables': ('dam_core_asset_usage_snapshot',), 'read_tables': (), 'emitted_event': 'AssetUsageSnapshotRecorded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_duplicate_candidates', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/duplicate-candidates', 'permission': 'dam_core.audit', 'owned_tables': ('dam_core_asset_duplicate_candidate',), 'read_tables': (), 'emitted_event': 'AssetDuplicateCandidateDetected', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_asset_lineage', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dam_core/asset-lineage', 'permission': 'dam_core.audit', 'owned_tables': ('dam_core_asset_lineage',), 'read_tables': (), 'emitted_event': 'AssetLineageRecorded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
)


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(item['emitted_event'] for item in command_contracts)
        and all(item['owned_tables'] and not item['read_tables'] for item in command_contracts)
        and all(item['emitted_event'] is None for item in query_contracts)
        and all(item['read_tables'] and not item['owned_tables'] for item in query_contracts),
        'pbc': 'dam_core',
        'operations': operations,
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
        'contracts': OPERATION_CONTRACTS,
        'side_effects': (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item['operation'] == operation_name), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_operation', 'operation': operation_name, 'side_effects': ()}
    supplied = dict(payload or {})
    table_scope = contract['owned_tables'] or contract['read_tables']
    return {
        'ok': bool(table_scope) and contract['event_contract'] == 'AppGen-X',
        'pbc': 'dam_core',
        'operation': operation_name,
        'operation_kind': contract['operation_kind'],
        'route': {'method': contract['method'], 'path': contract['path']},
        'permission': contract['permission'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'payload_keys': tuple(sorted(supplied)),
        'transaction_boundary': contract['transaction_boundary'],
        'event_contract': contract['event_contract'],
        'side_effects': (),
    }


class DamCoreService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'dam_core',
            'operation': operation_name,
            'operation_kind': operation_kind,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'side_effects': (),
        }
        if operation_kind == 'command':
            event_type = plan.get('emitted_event')
            result.update({
                'command': operation_name,
                'read_only': False,
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (event_type,) if event_type else (),
            })
        elif operation_kind == 'query':
            result.update({
                'query': operation_name,
                'read_only': True,
                'outbox_table': None,
                'emits': (),
            })
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_assets(self, payload=None):
        return self._command('command_assets', payload or {})

    def command_renditions(self, payload=None):
        return self._command('command_renditions', payload or {})

    def command_collections(self, payload=None):
        return self._command('command_collections', payload or {})

    def command_collection_members(self, payload=None):
        return self._command('command_collection_members', payload or {})

    def command_license_agreements(self, payload=None):
        return self._command('command_license_agreements', payload or {})

    def command_usage_entitlements(self, payload=None):
        return self._command('command_usage_entitlements', payload or {})

    def command_metadata_taxonomies(self, payload=None):
        return self._command('command_metadata_taxonomies', payload or {})

    def command_metadata_enrichments(self, payload=None):
        return self._command('command_metadata_enrichments', payload or {})

    def command_semantic_annotations(self, payload=None):
        return self._command('command_semantic_annotations', payload or {})

    def command_asset_workflows(self, payload=None):
        return self._command('command_asset_workflows', payload or {})

    def command_review_tasks(self, payload=None):
        return self._command('command_review_tasks', payload or {})

    def command_asset_exceptions(self, payload=None):
        return self._command('command_asset_exceptions', payload or {})

    def command_exception_resolutions(self, payload=None):
        return self._command('command_exception_resolutions', payload or {})

    def command_usage_snapshots(self, payload=None):
        return self._command('command_usage_snapshots', payload or {})

    def command_duplicate_candidates(self, payload=None):
        return self._command('command_duplicate_candidates', payload or {})

    def command_asset_lineage(self, payload=None):
        return self._command('command_asset_lineage', payload or {})

    def query_rights(self, payload=None):
        return self._query('query_rights', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = DamCoreService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'dam_core',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = DamCoreService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok']
        and result.get('ok') is True
        and result.get('operation_contract', {}).get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
