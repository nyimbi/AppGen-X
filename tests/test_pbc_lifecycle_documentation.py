from pyAppGen.pbc import PBC_LIFECYCLE_DOCUMENTATION_APIS
from pyAppGen.pbc import PBC_LIFECYCLE_DOCUMENTATION_ARTIFACTS
from pyAppGen.pbc import PBC_LIFECYCLE_DOCUMENTATION_TOPICS
from pyAppGen.pbc import pbc_lifecycle_documentation_audit
from pyAppGen.pbc import pbc_release_audit


def test_pbc_lifecycle_documentation_covers_build_test_package_register_compose():
    audit = pbc_lifecycle_documentation_audit()

    assert audit["format"] == "appgen.pbc-lifecycle-documentation-audit.v1"
    assert audit["ok"] is True
    assert not audit["blocking_gaps"]
    assert audit["required_topics"] == PBC_LIFECYCLE_DOCUMENTATION_TOPICS
    assert audit["required_apis"] == PBC_LIFECYCLE_DOCUMENTATION_APIS
    assert audit["required_artifacts"] == PBC_LIFECYCLE_DOCUMENTATION_ARTIFACTS
    assert {document["path"] for document in audit["documents"]} >= {
        "README.md",
        "docs/pbc-specification.md",
        "docs/composable-pbc-apps.md",
        "docs/kafka-alternatives.md",
    }


def test_pbc_release_audit_requires_lifecycle_documentation():
    audit = pbc_release_audit()
    package_gate = next(gate for gate in audit["gates"] if gate["id"] == "pbc_package_loader")

    assert audit["ok"] is True
    assert package_gate["ok"] is True
    assert package_gate["lifecycle_docs"]["ok"] is True
    assert audit["lifecycle_documentation"]["ok"] is True
