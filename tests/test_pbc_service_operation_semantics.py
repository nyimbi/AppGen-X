import importlib

from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS


def test_pbc_service_facades_separate_commands_from_queries() -> None:
    for key in IMPLEMENTED_PBC_KEYS:
        services = importlib.import_module(f"pyAppGen.pbcs.{key}.services")
        manifest = services.service_operation_manifest()
        service = getattr(services, manifest["service_class"])()

        assert manifest["ok"] is True
        assert manifest["command_operations"]

        command_name = manifest["command_operations"][0]

        command = getattr(service, command_name)({"tenant": "tenant-smoke"})

        assert command["ok"] is True
        assert command["operation_kind"] == "command"
        assert command["read_only"] is False
        assert command["outbox_table"] == services.EVENT_CONTRACT["outbox_table"]
        assert command["emits"] == (command["operation_contract"]["emitted_event"],)
        assert command["operation_contract"]["owned_tables"]
        assert not command["operation_contract"]["read_tables"]

        for query_name in manifest["query_operations"]:
            query = getattr(service, query_name)({"tenant": "tenant-smoke"})

            assert query["ok"] is True
            assert query["operation_kind"] == "query"
            assert query["read_only"] is True
            assert query["outbox_table"] is None
            assert query["emits"] == ()
            assert query["operation_contract"]["emitted_event"] is None
            assert query["operation_contract"]["read_tables"]
            assert not query["operation_contract"]["owned_tables"]


def test_query_enabled_pbc_services_have_read_only_query_facades() -> None:
    query_enabled = ()
    for key in IMPLEMENTED_PBC_KEYS:
        services = importlib.import_module(f"pyAppGen.pbcs.{key}.services")
        manifest = services.service_operation_manifest()
        service = getattr(services, manifest["service_class"])()

        query_enabled += tuple(manifest["query_operations"])
        for query_name in manifest["query_operations"]:
            query = getattr(service, query_name)({"tenant": "tenant-smoke"})

            assert query["ok"] is True
            assert query["operation_kind"] == "query"
            assert query["read_only"] is True
            assert query["outbox_table"] is None
            assert query["emits"] == ()
            assert query["operation_contract"]["emitted_event"] is None
            assert query["operation_contract"]["read_tables"]
            assert not query["operation_contract"]["owned_tables"]

    assert query_enabled


def test_pbc_service_contracts_reject_query_outbox_semantics() -> None:
    for key in IMPLEMENTED_PBC_KEYS:
        services = importlib.import_module(f"pyAppGen.pbcs.{key}.services")
        contracts = services.service_operation_contracts()

        assert contracts["ok"] is True
        for contract in contracts["contracts"]:
            if contract["operation_kind"] == "command":
                assert contract["emitted_event"]
                assert contract["owned_tables"]
                assert not contract["read_tables"]
            else:
                assert contract["operation_kind"] == "query"
                assert contract["emitted_event"] is None
                assert contract["read_tables"]
                assert not contract["owned_tables"]
