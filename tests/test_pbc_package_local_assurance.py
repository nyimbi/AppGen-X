from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_package_local_assurance_audit
from pyAppGen.pbc import pbc_package_local_assurance_contract
from pyAppGen.pbc import pbc_release_audit


def test_package_local_assurance_executes_for_every_implemented_pbc() -> None:
    audit = pbc_package_local_assurance_audit()

    assert audit["ok"] is True
    assert audit["pbc_count"] == len(IMPLEMENTED_PBC_KEYS)
    assert not audit["blocking_gaps"]
    assert {contract["pbc"] for contract in audit["contracts"]} == set(IMPLEMENTED_PBC_KEYS)
    assert all(contract["assurance_artifact"].startswith(f"src/pyAppGen/pbcs/{contract['pbc']}/") for contract in audit["contracts"])


def test_package_local_assurance_supports_module_and_runtime_test_modes() -> None:
    financial = pbc_package_local_assurance_contract("gl_core")
    platform = pbc_package_local_assurance_contract("federated_iam")

    assert financial["ok"] is True
    assert financial["evidence"]["mode"] == "capability_assurance"
    assert financial["evidence"]["validation"]["event_contract"] == "AppGen-X"
    assert financial["evidence"]["validation"]["stream_picker_visible"] is False
    assert platform["ok"] is True
    assert platform["evidence"]["mode"] == "runtime_capability_tests"
    assert platform["evidence"]["runtime_capabilities"]["ok"] is True
    assert platform["evidence"]["runtime_smoke"]["ok"] is True


def test_release_and_capability_audits_require_package_local_assurance() -> None:
    capability = pbc_implemented_capability_audit(("gl_core", "federated_iam"))
    release = pbc_release_audit()

    assert capability["ok"] is True
    assert {
        check["id"]
        for check in capability["checks"]
        if check["id"].endswith(":package_local_assurance")
    } == {"gl_core:package_local_assurance", "federated_iam:package_local_assurance"}
    assert release["ok"] is True
    assert release["package_local_assurance"]["ok"] is True
    implementation_gate = next(gate for gate in release["gates"] if gate["id"] == "pbc_implementation_contracts")
    assert implementation_gate["package_local_assurance"]["ok"] is True
