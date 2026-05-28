import re
from pathlib import Path

from pyAppGen.pbc import PBC_CATALOG


def test_each_pbc_has_50_domain_specific_improvement_proposals():
    root = Path("src/pyAppGen/pbcs")
    missing = []
    malformed = []
    for key in sorted(PBC_CATALOG):
        path = root / key / "improve1.md"
        if not path.is_file():
            missing.append(key)
            continue
        text = path.read_text(encoding="utf-8")
        sections = re.findall(r"^### \d+\. ", text, flags=re.MULTILINE)
        if (
            len(sections) != 50
            or text.count("**Justification:**") != 50
            or text.count("**Improvement:**") != 50
            or f"`{key}`" not in text
            or "## Current Domain Evidence Used" not in text
        ):
            malformed.append((key, len(sections)))
    assert missing == []
    assert malformed == []
