"""Command service layer for the product_catalog_pim PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.product_catalog_pim.events', 'inbox_topic': 'pbc.product_catalog_pim.inbox', 'outbox_table': 'product_catalog_pim_appgen_outbox_event', 'inbox_table': 'product_catalog_pim_appgen_inbox_event', 'dead_letter_table': 'product_catalog_pim_appgen_dead_letter_event', 'emitted': ({'event_type': 'ProductClassified', 'schema': 'product_catalog_pim.product_classified.emitted.v1', 'topic': 'pbc.product_catalog_pim.events', 'outbox_table': 'product_catalog_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ProductPublished', 'schema': 'product_catalog_pim.product_published.emitted.v1', 'topic': 'pbc.product_catalog_pim.events', 'outbox_table': 'product_catalog_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ForecastUpdated', 'schema': 'product_catalog_pim.forecast_updated.emitted.v1', 'topic': 'pbc.product_catalog_pim.events', 'outbox_table': 'product_catalog_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'TaxCalculated', 'schema': 'product_catalog_pim.tax_calculated.consumed.v1', 'topic': 'pbc.product_catalog_pim.inbox', 'inbox_table': 'product_catalog_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')},), 'retry_policy': {'name': 'product_catalog_pim_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'product_catalog_pim_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_products', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/product_catalog_pim/products', 'permission': 'product_catalog_pim.command.1', 'owned_tables': ('product_catalog_pim_product', 'product_catalog_pim_product_price', 'product_catalog_pim_product_media', 'product_catalog_pim_product_attribute'), 'read_tables': (), 'emitted_event': 'ProductClassified', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_product_read_models', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/product_catalog_pim/product-read-models', 'permission': 'product_catalog_pim.query.2', 'owned_tables': (), 'read_tables': ('product_catalog_pim_product', 'product_catalog_pim_product_price', 'product_catalog_pim_product_media', 'product_catalog_pim_product_attribute'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_prices', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/product_catalog_pim/prices', 'permission': 'product_catalog_pim.command.3', 'owned_tables': ('product_catalog_pim_product', 'product_catalog_pim_product_price', 'product_catalog_pim_product_media', 'product_catalog_pim_product_attribute'), 'read_tables': (), 'emitted_event': 'ForecastUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'product_catalog_pim',
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
        'pbc': 'product_catalog_pim',
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


class ProductCatalogPimService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'product_catalog_pim',
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

    def command_products(self, payload=None):
        return self._command('command_products', payload or {})

    def query_product_read_models(self, payload=None):
        return self._query('query_product_read_models', payload or {})

    def command_prices(self, payload=None):
        return self._command('command_prices', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ProductCatalogPimService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'product_catalog_pim',
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
    service = ProductCatalogPimService()
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
    contracts = (
        {'operation': 'configure_runtime', 'operation_kind': 'command', 'method': 'PUT', 'path': '/app/product-catalog-pim/configuration', 'table': 'product_catalog_pim_product_configuration', 'wizard': 'ProductLaunchIntakeWizard', 'permission': 'product_catalog_pim.configure'},
        {'operation': 'set_parameter', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/parameters', 'table': 'product_catalog_pim_product_parameter', 'wizard': None, 'permission': 'product_catalog_pim.configure'},
        {'operation': 'register_rule', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/rules', 'table': 'product_catalog_pim_product_rule', 'wizard': None, 'permission': 'product_catalog_pim.configure'},
        {'operation': 'receive_event', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/events/inbox', 'table': 'product_catalog_pim_appgen_inbox_event', 'wizard': None, 'permission': 'product_catalog_pim.event'},
        {'operation': 'seed_demo_workspace', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/demo-workspace', 'table': 'product_catalog_pim_product_configuration', 'wizard': 'ProductLaunchIntakeWizard', 'permission': 'product_catalog_pim.configure'},
        {'operation': 'build_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/app/product-catalog-pim/workbench', 'table': 'product_catalog_pim_product', 'wizard': None, 'permission': 'product_catalog_pim.read'},
        {'operation': 'create_product_family', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/families', 'table': 'product_catalog_pim_product_family', 'wizard': 'ProductLaunchIntakeWizard', 'permission': 'product_catalog_pim.product'},
        {'operation': 'register_product', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/products', 'table': 'product_catalog_pim_product', 'wizard': 'ProductLaunchIntakeWizard', 'permission': 'product_catalog_pim.product'},
        {'operation': 'define_attribute_schema', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/attribute-schemas', 'table': 'product_catalog_pim_product_attribute_schema', 'wizard': 'ProductLaunchIntakeWizard', 'permission': 'product_catalog_pim.product'},
        {'operation': 'set_product_attribute', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/attributes', 'table': 'product_catalog_pim_product_attribute', 'wizard': 'ProductEnrichmentWizard', 'permission': 'product_catalog_pim.enrich'},
        {'operation': 'add_localized_content', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/content', 'table': 'product_catalog_pim_product_locale_content', 'wizard': 'ProductEnrichmentWizard', 'permission': 'product_catalog_pim.enrich'},
        {'operation': 'attach_product_media', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/media', 'table': 'product_catalog_pim_product_media', 'wizard': 'ProductEnrichmentWizard', 'permission': 'product_catalog_pim.enrich'},
        {'operation': 'add_price_metadata', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/prices', 'table': 'product_catalog_pim_product_price', 'wizard': 'SellabilityReadinessWizard', 'permission': 'product_catalog_pim.publish'},
        {'operation': 'add_compliance_claim', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/compliance-claims', 'table': 'product_catalog_pim_product_compliance_claim', 'wizard': 'SellabilityReadinessWizard', 'permission': 'product_catalog_pim.enrich'},
        {'operation': 'publish_product', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/publications', 'table': 'product_catalog_pim_catalog_publication', 'wizard': 'CatalogPublicationWizard', 'permission': 'product_catalog_pim.publish'},
        {'operation': 'generate_publication_proof', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/publication-proofs', 'table': 'product_catalog_pim_product_publication_proof', 'wizard': 'CatalogPublicationWizard', 'permission': 'product_catalog_pim.audit'},
        {'operation': 'run_control_tests', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/controls', 'table': 'product_catalog_pim_product_control_assertion', 'wizard': None, 'permission': 'product_catalog_pim.audit'},
        {'operation': 'run_agent_skill', 'operation_kind': 'command', 'method': 'POST', 'path': '/app/product-catalog-pim/agent-sessions', 'table': 'product_catalog_pim_agent_session', 'wizard': None, 'permission': 'product_catalog_pim.read'},
    )
    return {
        'format': 'appgen.product-catalog-pim-standalone-service.v1',
        'ok': all(item['table'].startswith('product_catalog_pim_') for item in contracts),
        'pbc': 'product_catalog_pim',
        'contracts': contracts,
        'operations': tuple(item['operation'] for item in contracts),
        'command_operations': tuple(item['operation'] for item in contracts if item['operation_kind'] == 'command'),
        'query_operations': tuple(item['operation'] for item in contracts if item['operation_kind'] == 'query'),
        'side_effects': (),
    }


class ProductCatalogPimStandaloneService:
    def __init__(self, repository=None, database_path=':memory:'):
        if repository is None:
            from .repository import ProductCatalogPimStandaloneRepository
            repository = ProductCatalogPimStandaloneRepository(database_path=database_path)
        self.repository = repository

    def close(self):
        self.repository.close()

    def configure_runtime(self, tenant, configuration):
        return self.repository.configure_runtime(tenant, configuration)

    def set_parameter(self, tenant, name, value):
        return self.repository.set_parameter(tenant, name, value)

    def register_rule(self, tenant, rule):
        return self.repository.register_rule(tenant, rule)

    def receive_event(self, tenant, event):
        return self.repository.receive_event(tenant, event)

    def seed_demo_workspace(self, tenant='tenant_demo'):
        return self.repository.seed_demo_workspace(tenant=tenant)

    def build_workbench(self, tenant='tenant_demo'):
        return self.repository.build_workbench(tenant)

    def create_product_family(self, tenant, family):
        return self.repository.create_product_family(tenant, family)

    def register_product(self, tenant, product):
        return self.repository.register_product(tenant, product)

    def define_attribute_schema(self, tenant, schema):
        return self.repository.define_attribute_schema(tenant, schema)

    def set_product_attribute(self, tenant, product_id, name, value):
        return self.repository.set_product_attribute(tenant, product_id, name, value)

    def add_localized_content(self, tenant, content):
        return self.repository.add_localized_content(tenant, content)

    def attach_product_media(self, tenant, media):
        return self.repository.attach_product_media(tenant, media)

    def add_price_metadata(self, tenant, price):
        return self.repository.add_price_metadata(tenant, price)

    def add_compliance_claim(self, tenant, claim):
        return self.repository.add_compliance_claim(tenant, claim)

    def publish_product(self, tenant, product_id, channels, locales, published_by='catalog_manager_1'):
        return self.repository.publish_product(tenant, product_id, tuple(channels), tuple(locales), published_by)

    def generate_publication_proof(self, tenant, product_id, disclosure=('product_id', 'sku', 'lifecycle_state', 'completeness')):
        return self.repository.generate_publication_proof(tenant, product_id, tuple(disclosure))

    def run_control_tests(self, tenant):
        return self.repository.run_control_tests(tenant)

    def run_agent_skill(self, tenant, skill, payload):
        return self.repository.run_agent_skill(tenant, skill, payload)
