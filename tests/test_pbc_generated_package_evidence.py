"""Generated PBC packages expose executable schema, service, and release evidence."""

import importlib
import importlib.util
import py_compile
import sys

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import generate_app_from_schema
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS
from pyAppGen.pbc import pbc_composition_dsl
from pyAppGen.pbc import pbc_generation_smoke_audit
from pyAppGen.pbc import pbc_release_audit


def test_generated_pbc_packages_include_schema_service_and_release_evidence(tmp_path) -> None:
    selected = ("gl_core", "loyalty_rewards", "enterprise_search_vector")
    schema = schema_from_dsl(
        pbc_composition_dsl(selected, app_name="GeneratedPbcEvidence"),
        source_name="generated-pbc-evidence.appgen",
    )
    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)

    assert (output_dir / "pbcs" / "__init__.py").exists()
    for key in selected:
        pbc_dir = output_dir / "pbcs" / key
        for artifact in (
            "schema_contract.py",
            "service_contract.py",
            "release_evidence.py",
            "agent.py",
            "models.py",
            "services.py",
            "routes.py",
            "events.py",
            "handlers.py",
            "ui.py",
            "tests/__init__.py",
            "tests/test_contract.py",
        ):
            path = pbc_dir / artifact
            assert path.exists(), f"{key} missing {artifact}"
            if path.suffix == ".py":
                py_compile.compile(str(path), doraise=True)

        schema_contract = _load_module(pbc_dir / "schema_contract.py", f"{key}_schema_contract")
        service_contract = _load_module(pbc_dir / "service_contract.py", f"{key}_service_contract")
        release_evidence = _load_module(pbc_dir / "release_evidence.py", f"{key}_release_evidence")

        schema_payload = schema_contract.build_schema_contract()
        service_payload = service_contract.build_service_contract()
        release_payload = release_evidence.build_release_evidence()
        release_manifest = release_evidence.release_readiness_manifest()
        release_validation = release_evidence.validate_release_evidence()
        release_smoke = release_evidence.smoke_test()

        assert schema_payload["ok"] is True
        assert schema_payload["pbc"] == key
        assert schema_payload["owned_tables"]
        assert service_payload["ok"] is True
        assert service_payload["pbc"] == key
        assert service_payload.get("shared_table_access") is False
        assert release_payload["ok"] is True
        assert release_payload["pbc"] == key
        assert release_manifest["ok"] is True
        assert release_validation["ok"] is True
        assert release_smoke["ok"] is True
        assert not release_validation["missing_sections"]
        assert not release_validation["failed_checks"]
        assert not release_validation["boundary_gaps"]
        sys.path.insert(0, str(output_dir))
        try:
            agent = importlib.import_module(f"pbcs.{key}.agent")
            agent_skills = agent.agent_skill_manifest()
            chatbot = agent.chatbot_interface_contract()
            document_plan = agent.document_instruction_plan("uploaded document", "create the relevant record")
            read_plan = agent.datastore_crud_plan("read")
            create_plan = agent.datastore_crud_plan("create", payload={"status": "draft"})
            rejected_foreign = agent.datastore_crud_plan("update", table="foreign_table", payload={"status": "draft"})
            agent_contribution = agent.composed_agent_contribution()
            agent_smoke = agent.smoke_test()
            generated_test = importlib.import_module(f"pbcs.{key}.tests.test_contract")
            assert agent_skills["ok"] is True
            assert chatbot["ok"] is True
            assert document_plan["ok"] is True
            assert read_plan["ok"] is True
            assert create_plan["ok"] is True
            assert rejected_foreign["ok"] is False
            assert agent_contribution["ok"] is True
            assert agent_smoke["ok"] is True
            assert agent_contribution["single_agent_skill_namespace"] == f"{key}_skills"
            assert f"{key}_crud" in agent_contribution["dsl_tools"]
            generated_test.test_generated_schema_service_and_release_evidence()
            generated_test.test_agent_chatbot_skills_are_executable()
            generated_test.test_manifest_and_event_contract()
        finally:
            sys.path.remove(str(output_dir))
            for module_name in (
                f"pbcs.{key}.tests.test_contract",
                f"pbcs.{key}.tests",
                f"pbcs.{key}.agent",
                f"pbcs.{key}",
                "pbcs",
            ):
                sys.modules.pop(module_name, None)

    smoke = pbc_generation_smoke_audit(selected)
    directory_check = next(check for check in smoke["checks"] if check["id"] == "generated_pbc_directories")
    contract_test_check = next(check for check in smoke["checks"] if check["id"] == "generated_pbc_contract_tests")
    assert smoke["ok"] is True
    assert not directory_check["missing"]
    assert "schema_contract.py" in directory_check["required_artifacts"]
    assert "service_contract.py" in directory_check["required_artifacts"]
    assert "release_evidence.py" in directory_check["required_artifacts"]
    assert "agent.py" in directory_check["required_artifacts"]
    assert contract_test_check["ok"] is True
    assert {result["pbc"] for result in contract_test_check["results"]} == set(selected)
    assert all("test_generated_schema_service_and_release_evidence" in result["executed"] for result in contract_test_check["results"])
    assert all("test_agent_chatbot_skills_are_executable" in result["executed"] for result in contract_test_check["results"])


def test_release_audit_runs_generation_smoke_for_every_implemented_pbc() -> None:
    audit = pbc_release_audit()
    generation_gate = next(gate for gate in audit["gates"] if gate["id"] == "generation_smoke")
    contract_test_check = next(
        check for check in audit["generation_smoke"]["checks"] if check["id"] == "generated_pbc_contract_tests"
    )

    assert audit["ok"] is True
    assert generation_gate["ok"] is True
    assert generation_gate["selected_pbcs"] == IMPLEMENTED_PBC_KEYS
    assert audit["generation_smoke"]["selected_pbcs"] == IMPLEMENTED_PBC_KEYS
    assert audit["starter_generation_smoke"]["ok"] is True
    assert len(contract_test_check["results"]) == len(IMPLEMENTED_PBC_KEYS)
    assert {result["pbc"] for result in contract_test_check["results"]} == set(IMPLEMENTED_PBC_KEYS)
    assert all(result["ok"] for result in contract_test_check["results"])


def _load_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module
