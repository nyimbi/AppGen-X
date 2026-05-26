from importlib import import_module

from pyAppGen.pbc import PBC_CATALOG, pbc_implementation_release_audit


def test_every_builtin_pbc_has_its_own_source_package_directory():
    for key in PBC_CATALOG:
        module = import_module(f"pyAppGen.pbcs.{key}")
        contract = module.implementation_contract()

        assert module.PBC_KEY == key
        assert contract["pbc"] == key
        assert contract["implementation_directory"] == f"src/pyAppGen/pbcs/{key}"
        assert contract["owns_code"] is True
        assert contract["side_effect_free"] is True


def test_release_audit_requires_builtin_pbc_source_packages():
    audit = pbc_implementation_release_audit(tuple(PBC_CATALOG))

    assert audit["ok"] is True
    assert {
        check["id"]
        for check in audit["checks"]
        if check["id"].endswith(":source_package_directory")
    } == {f"{key}:source_package_directory" for key in PBC_CATALOG}
    assert {
        check["id"]
        for check in audit["checks"]
        if check["id"].endswith(":source_package_schema_service_release")
    } == {f"{key}:source_package_schema_service_release" for key in PBC_CATALOG}


def test_each_builtin_pbc_passes_release_audit_independently():
    for key in PBC_CATALOG:
        audit = pbc_implementation_release_audit((key,))

        assert audit["ok"] is True, key
        assert not audit["blocking_gaps"], key
        assert {check["id"] for check in audit["checks"] if not check["ok"]} == set()
        assert f"{key}:source_package_schema_service_release" in {
            check["id"] for check in audit["checks"]
        }
