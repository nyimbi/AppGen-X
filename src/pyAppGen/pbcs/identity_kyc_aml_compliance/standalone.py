"""Standalone smoke and audit entrypoints for the identity KYC / AML slice."""

from __future__ import annotations

from . import implementation_contract, smoke_test
from .capability_assurance import validate_table_stakes_capability_coverage
from .release_evidence import validate_release_evidence
from .runtime import identity_kyc_aml_compliance_build_workbench_view, identity_kyc_aml_compliance_empty_state


def standalone_contract():
    return {
        "ok": implementation_contract()["boundary_contract"]["ok"],
        "implementation_contract": implementation_contract(),
        "capability_assurance": validate_table_stakes_capability_coverage(),
        "release_validation": validate_release_evidence(),
        "side_effects": (),
    }


def standalone_smoke():
    state = identity_kyc_aml_compliance_empty_state()
    workbench = identity_kyc_aml_compliance_build_workbench_view(state, tenant="standalone")
    package_smoke = smoke_test()
    audit = standalone_contract()
    return {
        "ok": package_smoke["ok"] and audit["ok"] and workbench["ok"],
        "package_smoke": package_smoke,
        "audit": audit,
        "workbench": workbench,
        "side_effects": (),
    }
