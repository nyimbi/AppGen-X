from importlib import import_module

from pyAppGen.pbc import (
    PBC_CATALOG,
    _composition_shared_tables,
    _owned_tables,
    pbc_catalog,
    pbc_composition_plan,
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
            assert any(
                item["id"] == "capability_assurance_materialized" and item["ok"]
                for item in check["source_artifacts"]["checks"]
            )
            assert any(
                item["id"] == "service_route_runtime_surface_materialized" and item["ok"]
                for item in check["source_artifacts"]["checks"]
            )
            service_route_check = next(
                item
                for item in check["source_artifacts"]["checks"]
                if item["id"] == "service_route_runtime_surface_materialized"
            )
            assert service_route_check["ok"] is True
            assert any(
                item["id"] == "handler_runtime_surface_materialized" and item["ok"]
                for item in check["source_artifacts"]["checks"]
            )
            assert any(
                item["id"] == "event_contract_runtime_surface_materialized" and item["ok"]
                for item in check["source_artifacts"]["checks"]
            )
            assert any(
                item["id"] == "governance_hooks_materialized" and item["ok"]
                for item in check["source_artifacts"]["checks"]
            )
            assert any(
                item["id"] == "handler_contract_tests_materialized" and item["ok"]
                for item in check["source_artifacts"]["checks"]
            )
            assert any(
                item["id"] == "release_evidence_materialized" and item["ok"]
                for item in check["source_artifacts"]["checks"]
            )
            assert any(
                item["id"] == "ui_workbench_surface_materialized" and item["ok"]
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
        assert "capability_assurance.py" in audit["required_artifacts"]
        assert any(
            check["id"] == "manifest_capability_surface_materialized" and check["ok"]
            for check in contract["checks"]
        )
        assert any(
            check["id"] == "capability_assurance_materialized" and check["ok"]
            for check in contract["checks"]
        )
        assert any(
            check["id"] == "service_route_runtime_surface_materialized" and check["ok"]
            for check in contract["checks"]
        )
        route_module = import_module(f"pyAppGen.pbcs.{contract['pbc']}.routes")
        route_contract = route_module.api_route_contracts()
        route_validation = route_module.validate_api_route_contracts()
        assert route_contract["ok"] is True
        assert route_validation["ok"] is True
        assert all(item["event_contract"] == "AppGen-X" for item in route_contract["contracts"])
        assert all(item["stream_engine_picker_visible"] is False for item in route_contract["contracts"])
        assert all(item["shared_table_access"] is False for item in route_contract["contracts"])
        assert not route_validation["service_mismatches"]
        assert not route_validation["missing_idempotency"]
        assert not route_validation["invalid_table_scope"]
        assert any(
            check["id"] == "handler_runtime_surface_materialized" and check["ok"]
            for check in contract["checks"]
        )
        release_module = import_module(f"pyAppGen.pbcs.{contract['pbc']}.release_evidence")
        release_manifest = release_module.release_readiness_manifest()
        release_validation = release_module.validate_release_evidence()
        release_smoke = release_module.smoke_test()
        assert release_manifest["ok"] is True
        assert release_validation["ok"] is True
        assert release_smoke["ok"] is True
        assert not release_manifest["blocking_gaps"]
        assert not release_validation["missing_sections"]
        assert not release_validation["failed_checks"]
        assert not release_validation["boundary_gaps"]
        assert not release_smoke["side_effects"]
        event_module = import_module(f"pyAppGen.pbcs.{contract['pbc']}.events")
        event_manifest = event_module.event_contract_manifest()
        event_validation = event_module.validate_event_contract()
        event_smoke = event_module.smoke_test()
        assert event_manifest["ok"] is True
        assert event_validation["ok"] is True
        assert event_smoke["ok"] is True
        assert event_manifest["stream_engine_picker_visible"] is False
        assert event_smoke["emitted"]["table"].startswith(f"{contract['pbc']}_")
        assert event_smoke["consumed"]["table"].startswith(f"{contract['pbc']}_")
        assert event_smoke["emitted"]["retry_policy"]["max_attempts"] >= 3
        assert event_smoke["consumed"]["dead_letter_table"].startswith(f"{contract['pbc']}_")
        assert not event_validation["invalid_tables"]
        assert not event_validation["invalid_emitted"]
        assert not event_validation["invalid_consumed"]
        assert not event_smoke["side_effects"]
        assert any(
            check["id"] == "governance_hooks_materialized" and check["ok"]
            for check in contract["checks"]
        )
        assert any(
            check["id"] == "handler_contract_tests_materialized" and check["ok"]
            for check in contract["checks"]
        )
        assert any(
            check["id"] == "ui_workbench_surface_materialized" and check["ok"]
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


def _package_event_types(key):
    """Return the package's declared emitted and consumed event types.

    Packages publish these either at the package root or in an ``events``
    submodule; both are the package's own declaration, so the test reads
    whichever the package exposes rather than assuming one location.
    """
    package = import_module(f"pyAppGen.pbcs.{key}")
    emitted = getattr(package, f"{key.upper()}_EMITTED_EVENT_TYPES", None)
    consumed = getattr(package, f"{key.upper()}_CONSUMED_EVENT_TYPES", None)
    if emitted is not None and consumed is not None:
        return tuple(emitted), tuple(consumed)
    events = import_module(f"pyAppGen.pbcs.{key}.events")
    return (
        tuple(getattr(events, f"{key.upper()}_EMITTED_EVENT_TYPES")),
        tuple(getattr(events, f"{key.upper()}_CONSUMED_EVENT_TYPES")),
    )


def test_catalog_descriptor_matches_package_for_reference_pbcs():
    """The catalog descriptor must equal the package it describes.

    The catalog is computed from the package, so a mismatch means one of the
    two hand-maintained surfaces has drifted. These three PBCs cover the hard
    cases (richest runtime, flagship advanced ledger, non-key table prefix) and
    are the reference set the rest migrate behind.
    """
    descriptors = {descriptor["pbc"]: descriptor for descriptor in pbc_catalog()}

    for key in ("dam_core", "gl_core", "ar_credit"):
        descriptor = descriptors[key]
        manifest = import_module(f"pyAppGen.pbcs.{key}.manifest").PBC_MANIFEST
        emitted, consumed = _package_event_types(key)

        assert tuple(descriptor["tables"]) == tuple(manifest["tables"]), key
        assert set(descriptor["emits"]) == set(emitted), key
        assert set(descriptor["consumes"]) == set(consumed), key


def _resolve_owned_table(key, table, owned):
    """Resolve a manifest table to the physical table the package owns.

    Exact name first, then a unique suffix match, then the generated
    key-prefixed form. Mirrors ``_owned_table_name`` so the test measures the
    same mapping the generator uses.
    """
    if table in owned:
        return table
    suffixed = tuple(name for name in owned if name.endswith(f"_{table}"))
    if len(suffixed) == 1:
        return suffixed[0]
    return f"{key}_{table}"


def test_manifest_tables_resolve_to_owned_tables_for_every_pbc():
    """Every manifest table must resolve to exactly one owned table.

    A manifest table with no owned-table counterpart is a name the package
    never creates, so generation would emit a table nothing migrates. Packages
    prefix owned tables with their own domain prefix (``ar_credit`` owns
    ``ar_customer`` for a manifest table ``customer``), so resolution is by
    suffix as well as by exact name. Two manifest tables resolving to the same
    physical table would mean two generated tables are one, so the mapping must
    also be injective.
    """
    for key in PBC_CATALOG:
        manifest = import_module(f"pyAppGen.pbcs.{key}.manifest").PBC_MANIFEST
        owned = _owned_tables(key)
        physical_to_logical: dict[str, str] = {}

        for table in manifest.get("tables", ()) or ():
            physical = _resolve_owned_table(key, table, owned)
            assert physical in owned, f"{key}: manifest table {table!r} is not owned"
            assert physical not in physical_to_logical, (
                f"{key}: manifest tables {physical_to_logical.get(physical)!r} and "
                f"{table!r} both resolve to {physical!r}"
            )
            physical_to_logical[physical] = table


def test_no_two_pbcs_claim_the_same_generated_table():
    """No composition of built-in PBCs may share a generated table.

    Generated apps name every owned table ``{pbc}_{logical}``, so two PBCs
    collide only when one key prefixes the other's table name. Every pair is
    checked, because a collision silently merges two owned datastores and
    breaks the platform's one-datastore-per-PBC promise.
    """
    keys = tuple(PBC_CATALOG)
    plan = pbc_composition_plan(keys)

    assert plan["shared_tables"] == ()


def test_shared_table_detector_fires_on_a_prefix_collision():
    """The collision detector must fail on a deliberate prefix collision.

    A gate that has never been watched fail is not evidence. Two synthetic
    services are chosen so that one PBC's key prefixes the other's table name,
    which is the only way generated table names can collide.
    """
    colliding = (
        {"pbc": "gl_core", "tables": ("ledger", "journal_entry")},
        {"pbc": "gl", "tables": ("core_ledger",)},
    )

    assert _composition_shared_tables(colliding) == (
        {"table": "gl_core_ledger", "owners": ("gl", "gl_core")},
    )

    distinct = (
        {"pbc": "gl_core", "tables": ("ledger",)},
        {"pbc": "ar_credit", "tables": ("ledger",)},
    )

    assert _composition_shared_tables(distinct) == ()

