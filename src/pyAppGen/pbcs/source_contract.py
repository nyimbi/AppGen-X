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
