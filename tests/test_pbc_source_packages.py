from importlib import import_module

from pyAppGen.pbc import (
    PBC_CATALOG,
    pbc_implementation_release_audit,
    pbc_source_artifact_release_audit,
    pbc_source_runtime_test_coverage_audit,
    pbc_specification_release_audit,
)


def test_every_builtin_pbc_has_its_own_source_package_directory():
    for key in PBC_CATALOG:
        module = import_module(f"pyAppGen.pbcs.{key}")
        contract = module.implementation_contract()

        assert module.PBC_KEY == key
        assert contract["pbc"] == key
        assert contract["implementation_directory"] == f"src/pyAppGen/pbcs/{key}"
        assert contract["owns_code"] is True
        assert contract["side_effect_free"] is True
        assert module.register_pbc()["pbc"] == key
        assert module.register_pbc()["standard_features"] == contract["standard_features"]
        assert module.register_pbc()["advanced_capabilities"] == contract["advanced_runtime"]["capabilities"]
        catalog_snapshot = dict(PBC_CATALOG)
        registration = module.registration_plan()
        assert registration["ok"] is True
        assert registration["decision"] == "approved"
        assert key in registration["catalog_patch"]
        assert PBC_CATALOG == catalog_snapshot


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
    assert {
        check["id"]
        for check in audit["checks"]
        if check["id"].endswith(":specification_completeness")
    } == {f"{key}:specification_completeness" for key in PBC_CATALOG}
    assert {
        check["id"]
        for check in audit["checks"]
        if check["id"].endswith(":table_stakes_evidence")
    } == {f"{key}:table_stakes_evidence" for key in PBC_CATALOG}
    for check in audit["checks"]:
        if check["id"].endswith(":source_artifacts_materialized"):
            assert check["ok"] is True
            assert not check["source_artifacts"]["blocking_gaps"]
            assert any(
                item["id"] == "manifest_capability_surface_materialized" and item["ok"]
                for item in check["source_artifacts"]["checks"]
            )
        if check["id"].endswith(":source_package_directory"):
            assert check["ok"] is True
        if check["id"].endswith(":table_stakes_evidence"):
            assert check["ok"] is True
            assert not check["table_stakes"]["blocking_gaps"]
        if check["id"].endswith(":advanced_runtime"):
            assert check["ok"] is True
            assert not check["advanced_runtime"]["blocking_gaps"]
            assert check["advanced_runtime"]["operations"]
            assert check["advanced_runtime"]["capabilities"]


def test_every_builtin_pbc_has_materialized_source_artifacts():
    audit = pbc_source_artifact_release_audit(tuple(PBC_CATALOG))

    assert audit["format"] == "appgen.pbc-source-artifact-release-audit.v1"
    assert audit["ok"] is True
    assert audit["pbc_count"] == len(PBC_CATALOG)
    assert not audit["blocking_gaps"]
    for contract in audit["contracts"]:
        assert contract["directory"] == f"src/pyAppGen/pbcs/{contract['pbc']}"
        assert {
            file["artifact"]
            for file in contract["files"]
            if file["exists"]
        } == set(audit["required_artifacts"])
        assert any(
            check["id"] == "manifest_capability_surface_materialized" and check["ok"]
            for check in contract["checks"]
        )
        assert not contract["blocking_gaps"]


def test_every_builtin_pbc_has_comprehensive_package_specification():
    audit = pbc_specification_release_audit(tuple(PBC_CATALOG))

    assert audit["ok"] is True
    assert audit["pbc_count"] == len(PBC_CATALOG)
    assert not audit["blocking_gaps"]
    for contract in audit["contracts"]:
        assert contract["path"].endswith(f"{contract['pbc']}/SPECIFICATION.md")
        assert contract["word_count"] >= audit["minimum_words"]
        assert not contract["missing_concepts"]
        assert not contract["restricted_legacy_references"]


def test_every_builtin_pbc_has_focused_source_runtime_test_coverage():
    audit = pbc_source_runtime_test_coverage_audit(tuple(PBC_CATALOG))

    assert audit["format"] == "appgen.pbc-source-runtime-test-coverage-audit.v1"
    assert audit["ok"] is True
    assert audit["pbc_count"] == len(PBC_CATALOG)
    assert not audit["blocking_gaps"]
    for contract in audit["contracts"]:
        assert contract["path"] == f"tests/test_pbc_{contract['pbc']}_runtime.py"
        assert contract["test_function_count"] >= 2
        assert not contract["blocking_gaps"]


def test_each_builtin_pbc_passes_release_audit_independently():
    for key in PBC_CATALOG:
        audit = pbc_implementation_release_audit((key,))

        assert audit["ok"] is True, key
        assert not audit["blocking_gaps"], key
        assert {check["id"] for check in audit["checks"] if not check["ok"]} == set()
        assert f"{key}:source_package_schema_service_release" in {
            check["id"] for check in audit["checks"]
        }
