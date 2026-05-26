"""Generated PBC packages expose executable schema, service, and release evidence."""

import importlib
import importlib.util
import py_compile
import sys

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import generate_app_from_schema
from pyAppGen.pbc import pbc_composition_dsl
from pyAppGen.pbc import pbc_generation_smoke_audit


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

        assert schema_payload["ok"] is True
        assert schema_payload["pbc"] == key
        assert schema_payload["owned_tables"]
        assert service_payload["ok"] is True
        assert service_payload["pbc"] == key
        assert service_payload.get("shared_table_access") is False
        assert release_payload["ok"] is True
        assert release_payload["pbc"] == key
        sys.path.insert(0, str(output_dir))
        try:
            generated_test = importlib.import_module(f"pbcs.{key}.tests.test_contract")
            generated_test.test_generated_schema_service_and_release_evidence()
            generated_test.test_manifest_and_event_contract()
        finally:
            sys.path.remove(str(output_dir))
            for module_name in (
                f"pbcs.{key}.tests.test_contract",
                f"pbcs.{key}.tests",
                f"pbcs.{key}",
                "pbcs",
            ):
                sys.modules.pop(module_name, None)

    smoke = pbc_generation_smoke_audit(selected)
    directory_check = next(check for check in smoke["checks"] if check["id"] == "generated_pbc_directories")
    assert smoke["ok"] is True
    assert not directory_check["missing"]
    assert "schema_contract.py" in directory_check["required_artifacts"]
    assert "service_contract.py" in directory_check["required_artifacts"]
    assert "release_evidence.py" in directory_check["required_artifacts"]


def _load_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module
