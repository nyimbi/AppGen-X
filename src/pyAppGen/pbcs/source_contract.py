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
