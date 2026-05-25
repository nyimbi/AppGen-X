from pyAppGen.pbc import AP_AUTOMATION_STANDARD_FEATURE_KEYS
from pyAppGen.pbc import AR_CREDIT_STANDARD_FEATURE_KEYS
from pyAppGen.pbc import GL_CORE_STANDARD_FEATURE_KEYS
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_implemented_pbcs_gate_standard_and_advanced_capability_coverage() -> None:
    audit = pbc_implemented_capability_audit()

    assert audit["ok"] is True
    assert audit["implemented_pbcs"] == IMPLEMENTED_PBC_KEYS
    assert not audit["blocking_gaps"]
    assert {
        check["id"]
        for check in audit["checks"]
        if check["id"].endswith(":standard_table_stakes")
    } == {f"{key}:standard_table_stakes" for key in IMPLEMENTED_PBC_KEYS}
    assert {
        check["id"]
        for check in audit["checks"]
        if check["id"].endswith(":advanced_runtime_complete")
    } == {f"{key}:advanced_runtime_complete" for key in IMPLEMENTED_PBC_KEYS}


def test_implemented_pbc_contracts_expose_standard_feature_inventories() -> None:
    expected = {
        "gl_core": set(GL_CORE_STANDARD_FEATURE_KEYS),
        "ap_automation": set(AP_AUTOMATION_STANDARD_FEATURE_KEYS),
        "ar_credit": set(AR_CREDIT_STANDARD_FEATURE_KEYS),
    }

    for key, standard_features in expected.items():
        contract = pbc_implementation_contract(key)
        runtime_features = set(contract["advanced_runtime"]["standard_features"])
        source_features = set(contract["source_package"]["standard_features"])

        assert standard_features <= runtime_features
        assert runtime_features == source_features
        assert len(runtime_features) >= 18
        assert pbc_implementation_release_audit((key,))["ok"] is True
