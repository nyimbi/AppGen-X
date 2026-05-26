from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS
from pyAppGen.pbc import PBC_SPECIFICATION_TRACEABILITY_FIELDS
from pyAppGen.pbc import pbc_release_audit
from pyAppGen.pbc import pbc_specification_contract
from pyAppGen.pbc import pbc_specification_release_audit


def test_every_pbc_specification_traces_manifest_surface() -> None:
    audit = pbc_specification_release_audit(IMPLEMENTED_PBC_KEYS)

    assert audit["ok"] is True
    assert not audit["blocking_gaps"]
    for contract in audit["contracts"]:
        traceability = contract["manifest_traceability"]
        assert traceability["ok"] is True
        assert traceability["appendix_present"] is True
        assert {field["field"] for field in traceability["fields"]} == set(PBC_SPECIFICATION_TRACEABILITY_FIELDS)
        assert not traceability["blocking_gaps"]


def test_traceability_covers_high_risk_spec_surfaces() -> None:
    gl_core = pbc_specification_contract("gl_core")
    returns = pbc_specification_contract("returns_reverse_logistics")

    assert gl_core["ok"] is True
    assert all(not field["missing"] for field in gl_core["manifest_traceability"]["fields"])
    assert returns["ok"] is True
    assert all(not field["missing"] for field in returns["manifest_traceability"]["fields"])


def test_release_audit_requires_specification_manifest_traceability() -> None:
    release = pbc_release_audit()

    assert release["ok"] is True
    assert release["specification_audit"]["ok"] is True
    assert all(contract["manifest_traceability"]["ok"] for contract in release["specification_audit"]["contracts"])
