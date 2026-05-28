from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS
import importlib

NEW_ENTERPRISE_PBC_KEYS = (
    'contract_lifecycle', 'vendor_supplier_360', 'enterprise_risk_controls', 'planning_budgeting_forecasting',
    'revenue_recognition', 'expense_management', 'travel_management', 'grant_fund_accounting',
    'project_portfolio_management', 'professional_services_automation', 'field_service_management',
    'customer_success_management', 'case_knowledge_management', 'privacy_consent_governance',
    'data_product_catalog', 'master_data_governance', 'sustainability_esg_reporting',
    'facilities_space_management', 'legal_matter_management', 'insurance_claims_policy',
)


def test_new_enterprise_pbcs_have_world_class_domain_depth_contracts():
    assert set(NEW_ENTERPRISE_PBC_KEYS) <= set(IMPLEMENTED_PBC_KEYS)
    for key in NEW_ENTERPRISE_PBC_KEYS:
        package = importlib.import_module(f'pyAppGen.pbcs.{key}')
        runtime = getattr(package, f'{key}_runtime_capabilities')()
        domain = runtime['world_class_domain_depth']
        assert runtime['ok'] is True, key
        assert domain['ok'] is True, key
        assert len(domain['owned_tables']) >= 20, key
        assert domain['operation_count'] >= 15, key
        assert len(domain['rules']) >= 6, key
        assert len(domain['parameters']) >= 6, key
        assert len(domain['advanced_capabilities']) >= 6, key
        assert domain['event_contract'] == 'AppGen-X', key
        assert domain['stream_engine_picker_visible'] is False, key
        assert domain['shared_table_access'] is False, key
        assert all(table.startswith(f'{key}_') for table in domain['owned_tables']), key


def test_new_enterprise_pbc_domain_operations_are_executable_and_owned():
    for key in NEW_ENTERPRISE_PBC_KEYS:
        package = importlib.import_module(f'pyAppGen.pbcs.{key}')
        runtime = getattr(package, f'{key}_runtime_capabilities')()
        operation = runtime['world_class_domain_depth']['operations'][0]
        result = getattr(package, f'{key}_execute_domain_operation')(operation, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
        service_module = importlib.import_module(f'pyAppGen.pbcs.{key}.services')
        service_manifest = service_module.service_operation_manifest()
        service = getattr(service_module, service_manifest['service_class'])()
        service_result = getattr(service, operation)({'tenant': 'tenant-smoke', 'code': 'SMOKE'})
        assert result['ok'] is True, key
        assert result['target_table'].startswith(f'{key}_'), key
        assert result['event_contract'] == 'AppGen-X', key
        assert result['shared_table_access'] is False, key
        assert service_result['ok'] is True, key
        assert service_result['operation_contract']['owned_tables'][0].startswith(f'{key}_'), key
        assert service_result['emits'], key


def test_new_enterprise_pbc_specs_are_not_generic_stubs():
    for key in NEW_ENTERPRISE_PBC_KEYS:
        text = open(f'src/pyAppGen/pbcs/{key}/SPECIFICATION.md', encoding='utf-8').read()
        assert len(text.split()) >= 1200, key
        assert 'Executable Domain Operations' in text, key
        assert 'Advanced Capabilities' in text, key
        assert 'AI Agent and Skills' in text, key
        assert 'Release Evidence and Tests' in text, key
        assert text.count('- `') >= 45, key


def test_new_enterprise_pbc_ui_surfaces_every_domain_capability():
    for key in NEW_ENTERPRISE_PBC_KEYS:
        domain_module = importlib.import_module(f'pyAppGen.pbcs.{key}.domain_depth')
        ui_module = importlib.import_module(f'pyAppGen.pbcs.{key}.ui')
        domain = domain_module.domain_capability_surface_contract()
        ui = getattr(ui_module, f'{key}_ui_contract')()
        workbench = getattr(ui_module, f'{key}_render_workbench')()
        full = ui['full_capability_surface']

        assert domain['ok'] is True, key
        assert ui['ok'] is True, key
        assert workbench['ok'] is True, key
        assert set(full['operation_actions']) == set(domain_module.DOMAIN_OPERATIONS), key
        assert set(full['rule_editors']) == set(domain_module.DOMAIN_RULES), key
        assert set(full['parameter_editors']) == set(domain_module.DOMAIN_PARAMETERS), key
        assert set(full['advanced_panels']) == set(domain_module.DOMAIN_ADVANCED_CAPABILITIES), key
        assert set(full['table_browsers']) == set(domain_module.DOMAIN_OWNED_TABLES), key
        assert set(workbench['operation_actions']) == set(domain_module.DOMAIN_OPERATIONS), key
        assert set(workbench['table_browsers']) == set(domain_module.DOMAIN_OWNED_TABLES), key
        assert len(full['edge_case_queues']) >= len(domain_module.DOMAIN_OPERATIONS), key
        assert len(full['agent_tools']) == len(domain_module.DOMAIN_OPERATIONS), key
        assert 'edge_case_triage' in full['navigation_sections'], key
        assert 'advanced_intelligence' in full['navigation_sections'], key
        assert full['coverage']['event_contract'] == 'AppGen-X', key
        assert full['coverage']['stream_engine_picker_visible'] is False, key
        assert full['coverage']['shared_table_access'] is False, key
