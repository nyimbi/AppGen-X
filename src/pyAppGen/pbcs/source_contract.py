"""Shared source-package contract helpers for built-in PBC packages."""

from __future__ import annotations


def source_pbc_package_contract(pbc_key: str, capabilities: tuple[str, ...] = ()) -> dict:
    return {
        "format": "appgen.pbc-source-package.v1",
        "pbc": pbc_key,
        "implementation_directory": f"src/pyAppGen/pbcs/{pbc_key}",
        "owns_code": True,
        "side_effect_free": True,
        "capabilities": tuple(capabilities),
    }


def source_package_metadata(
    pbc_key: str,
    manifest: dict,
    implementation: dict | None = None,
) -> dict:
    """Return executable package identity and discovery metadata."""
    from pyAppGen.pbc import PBC_ALLOWED_DATASTORE_BACKENDS
    from pyAppGen.pbc import PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS

    package = implementation or source_pbc_package_contract(pbc_key)
    artifacts = tuple(PBC_IMPLEMENTATION_REQUIRED_ARTIFACTS)
    return {
        "format": "appgen.pbc-package-metadata.v1",
        "ok": True,
        "pbc": pbc_key,
        "package_name": f"pyAppGen.pbcs.{pbc_key}",
        "version": manifest.get("version", "1.0.0"),
        "label": manifest.get("label"),
        "mesh": manifest.get("mesh"),
        "implementation_directory": package.get("implementation_directory", f"src/pyAppGen/pbcs/{pbc_key}"),
        "entrypoints": {
            "manifest": "PBC_MANIFEST",
            "register": "register_pbc",
            "registration_plan": "registration_plan",
            "implementation_contract": "implementation_contract",
            "package_metadata": "package_metadata_manifest",
            "metadata_validation": "validate_package_metadata",
        },
        "artifacts": artifacts,
        "docs": tuple(manifest.get("docs", ())),
        "tests": tuple(manifest.get("tests", ())),
        "capabilities": tuple(manifest.get("capabilities", ())),
        "standard_features": tuple(manifest.get("standard_features", ())),
        "advanced_capabilities": tuple(manifest.get("advanced_capabilities", ())),
        "datastore_backend": manifest.get("datastore_backend"),
        "allowed_database_backends": PBC_ALLOWED_DATASTORE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "registration_mode": "side_effect_free_plan",
        "side_effects": (),
    }


def validate_source_package_metadata(metadata: dict) -> dict:
    """Validate package metadata without mutating registries or importing runtime state."""
    pbc_key = metadata.get("pbc")
    missing_entrypoints = tuple(
        key
        for key in (
            "manifest",
            "register",
            "registration_plan",
            "implementation_contract",
            "package_metadata",
            "metadata_validation",
        )
        if not metadata.get("entrypoints", {}).get(key)
    )
    missing_publish_artifacts = tuple(
        artifact
        for artifact in ("__init__.py", "manifest.py", "tests/test_contract.py", "RELEASE_EVIDENCE.md")
        if artifact not in tuple(metadata.get("artifacts", ()))
    )
    missing_capability_evidence = tuple(
        field
        for field in ("standard_features", "advanced_capabilities", "capabilities")
        if not metadata.get(field)
    )
    invalid = []
    if metadata.get("implementation_directory") != f"src/pyAppGen/pbcs/{pbc_key}":
        invalid.append("implementation_directory")
    if metadata.get("datastore_backend") not in tuple(metadata.get("allowed_database_backends", ())):
        invalid.append("datastore_backend")
    if metadata.get("event_contract") != "AppGen-X":
        invalid.append("event_contract")
    if metadata.get("stream_engine_picker_visible") is not False:
        invalid.append("stream_engine_picker_visible")
    return {
        "format": "appgen.pbc-package-metadata-validation.v1",
        "ok": not missing_entrypoints
        and not missing_publish_artifacts
        and not missing_capability_evidence
        and not invalid
        and not metadata.get("side_effects"),
        "pbc": pbc_key,
        "missing_entrypoints": missing_entrypoints,
        "missing_publish_artifacts": missing_publish_artifacts,
        "missing_capability_evidence": missing_capability_evidence,
        "invalid": tuple(invalid),
        "side_effects": (),
    }


def source_registration_plan(
    pbc_key: str,
    manifest: dict,
    *,
    existing_catalog: dict[str, dict] | None = None,
) -> dict:
    """Return a side-effect-free registration plan for a source PBC package."""
    from pyAppGen.pbc import PBC_CATALOG
    from pyAppGen.pbc import register_pbc_manifest

    catalog = (
        existing_catalog
        if existing_catalog is not None
        else {key: value for key, value in PBC_CATALOG.items() if key != pbc_key}
    )
    return register_pbc_manifest(dict(manifest), existing_catalog=catalog)
