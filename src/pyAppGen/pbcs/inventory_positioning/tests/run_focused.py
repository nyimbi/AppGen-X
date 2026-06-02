"""Run focused inventory_positioning tests without external dependencies."""

from __future__ import annotations

import importlib
import pkgutil
import sys
from pathlib import Path


PACKAGE = "pyAppGen.pbcs.inventory_positioning.tests"


def main() -> int:
    package = importlib.import_module(PACKAGE)
    package_path = Path(package.__file__).parent
    failures: list[str] = []
    executed = 0
    for module_info in pkgutil.iter_modules([str(package_path)]):
        if not module_info.name.startswith("test_"):
            continue
        module = importlib.import_module(f"{PACKAGE}.{module_info.name}")
        for name in sorted(dir(module)):
            if not name.startswith("test_"):
                continue
            candidate = getattr(module, name)
            if callable(candidate):
                executed += 1
                try:
                    candidate()
                except Exception as exc:  # pragma: no cover - runner only
                    failures.append(f"{module_info.name}.{name}: {exc}")
    print(f"executed={executed}")
    if failures:
        print("failures=")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("status=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
