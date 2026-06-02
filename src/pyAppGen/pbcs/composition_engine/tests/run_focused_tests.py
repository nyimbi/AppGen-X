"""Fallback focused test runner for composition_engine when pytest is unavailable."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
import inspect
import sys
import traceback

TEST_MODULES = (
    "pyAppGen.pbcs.composition_engine.tests.test_contract",
    "pyAppGen.pbcs.composition_engine.tests.test_runtime_capabilities",
    "pyAppGen.pbcs.composition_engine.tests.test_orchestration_app",
    "pyAppGen.pbcs.composition_engine.tests.test_repository",
    "pyAppGen.pbcs.composition_engine.tests.test_standalone",
    "tests.test_pbc_composition_engine_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def main() -> int:
    repo_root = _repo_root()
    tests_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(tests_dir))
    sys.path.insert(1, str(repo_root / "src"))
    sys.path.insert(2, str(repo_root))

    executed = 0
    failures: list[tuple[str, str]] = []

    for module_name in TEST_MODULES:
        module = import_module(module_name)
        for name, fn in sorted(inspect.getmembers(module, inspect.isfunction)):
            if not name.startswith("test_"):
                continue
            qualified = f"{module_name}.{name}"
            try:
                fn()
                executed += 1
                print(f"PASS {qualified}")
            except Exception:
                failures.append((qualified, traceback.format_exc()))
                print(f"FAIL {qualified}")

    print(f"executed={executed} failures={len(failures)}")
    if failures:
        for qualified, stack in failures:
            print(f"--- {qualified} ---")
            print(stack)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
