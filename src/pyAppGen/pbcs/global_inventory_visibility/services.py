"""Command service layer for the global_inventory_visibility PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.global_inventory_visibility.events', 'inbox_topic': 'pbc.global_inventory_visibility.inbox', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'dead_letter_table': 'global_inventory_visibility_appgen_dead_letter_event', 'emitted': ({'event_type': 'AvailabilityProjected', 'schema': 'global_inventory_visibility.availability_projected.emitted.v1', 'topic': 'pbc.global_inventory_visibility.events', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InventoryPoolChanged', 'schema': 'global_inventory_visibility.inventory_pool_changed.emitted.v1', 'topic': 'pbc.global_inventory_visibility.events', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'GoodsReceiptPosted', 'schema': 'global_inventory_visibility.goods_receipt_posted.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'global_inventory_visibility.shipment_delivered.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InventoryAllocated', 'schema': 'global_inventory_visibility.inventory_allocated.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'global_inventory_visibility_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'global_inventory_visibility_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'query_global_availability', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/global-availability', 'permission': 'global_inventory_visibility.query.1', 'owned_tables': (), 'read_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_pool_rules', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/global_inventory_visibility/pool-rules', 'permission': 'global_inventory_visibility.command.2', 'owned_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'read_tables': (), 'emitted_event': 'InventoryPoolChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_supply_nodes', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/supply-nodes', 'permission': 'global_inventory_visibility.query.3', 'owned_tables': (), 'read_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'global_inventory_visibility',
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
        'pbc': 'global_inventory_visibility',
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


class GlobalInventoryVisibilityService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'global_inventory_visibility',
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

    def query_global_availability(self, payload=None):
        return self._query('query_global_availability', payload or {})

    def command_pool_rules(self, payload=None):
        return self._command('command_pool_rules', payload or {})

    def query_supply_nodes(self, payload=None):
        return self._query('query_supply_nodes', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = GlobalInventoryVisibilityService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'global_inventory_visibility',
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
    service = GlobalInventoryVisibilityService()
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



def standalone_service_operation_contracts():
    """Return repository-backed standalone service operations for one-PBC apps."""
    contracts = (
        {"operation": "seed_demo_workspace", "operation_kind": "command", "method": "POST", "path": "/app/global-inventory-visibility/demo-workspace", "table": "global_inventory_visibility_inventory_configuration", "wizard": "AvailabilityProjectionWizard", "permission": "global_inventory_visibility.configure"},
        {"operation": "build_workbench", "operation_kind": "query", "method": "GET", "path": "/app/global-inventory-visibility/workbench", "table": "global_inventory_visibility_inventory_projection", "wizard": None, "permission": "global_inventory_visibility.read"},
        {"operation": "build_pool_read_model", "operation_kind": "query", "method": "GET", "path": "/app/global-inventory-visibility/pools/detail", "table": "global_inventory_visibility_inventory_pool", "wizard": None, "permission": "global_inventory_visibility.read"},
        {"operation": "register_inventory_pool", "operation_kind": "command", "method": "POST", "path": "/app/global-inventory-visibility/pools", "table": "global_inventory_visibility_inventory_pool", "wizard": "AvailabilityProjectionWizard", "permission": "global_inventory_visibility.configure"},
        {"operation": "generate_pool_proof", "operation_kind": "command", "method": "POST", "path": "/app/global-inventory-visibility/proofs", "table": "global_inventory_visibility_inventory_control_assertion", "wizard": "ReservationControlWizard", "permission": "global_inventory_visibility.audit"},
        {"operation": "build_release_read_model", "operation_kind": "query", "method": "GET", "path": "/app/global-inventory-visibility/release-evidence", "table": "global_inventory_visibility_inventory_control_assertion", "wizard": None, "permission": "global_inventory_visibility.audit"},
    )
    return {
        "format": "appgen.global-inventory-visibility-standalone-service.v1",
        "ok": all(item["table"].startswith("global_inventory_visibility_") for item in contracts),
        "pbc": "global_inventory_visibility",
        "contracts": contracts,
        "operations": tuple(item["operation"] for item in contracts),
        "command_operations": tuple(item["operation"] for item in contracts if item["operation_kind"] == "command"),
        "query_operations": tuple(item["operation"] for item in contracts if item["operation_kind"] == "query"),
        "side_effects": (),
    }


class GlobalInventoryVisibilityStandaloneService:
    """Repository-backed command/query surface for standalone package apps."""

    def __init__(self, repository=None, database_path=":memory:"):
        if repository is None:
            from .repository import GlobalInventoryVisibilityRepository

            repository = GlobalInventoryVisibilityRepository(database_path=database_path)
        self.repository = repository

    def close(self):
        self.repository.close()

    def seed_demo_workspace(self, tenant="tenant_demo"):
        return self.repository.seed_demo_workspace(tenant=tenant)

    def build_workbench(self, tenant="tenant_demo"):
        return self.repository.build_workbench(tenant)

    def build_pool_read_model(self, pool_id, tenant=None):
        return self.repository.build_pool_read_model(pool_id=pool_id, tenant=tenant)

    def register_inventory_pool(self, pool):
        return self.repository.register_inventory_pool(pool)

    def generate_pool_proof(self, pool_id, disclosure=("available_to_promise", "capable_to_promise", "freshness_score")):
        return self.repository.generate_pool_proof(pool_id=pool_id, disclosure=tuple(disclosure))

    def build_release_read_model(self, tenant="tenant_demo"):
        return self.repository.build_release_read_model(tenant)

    def run_document_instruction(self, document, instructions, tenant="tenant_demo"):
        from . import agent

        plan = agent.document_instruction_plan(document, instructions)
        return {
            "ok": plan["ok"],
            "tenant": tenant,
            "plan": plan,
            "requires_confirmation": True,
            "side_effects": (),
        }
