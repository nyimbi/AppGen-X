"""Traceability checks for the improve1 implementation matrix."""

from pathlib import Path
import re


REQUIRED_COLUMNS = (
    "code artifact + model",
    "UI surface",
    "service/API",
    "test",
    "evidence",
)


def _split_row(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def test_improve1_traceability_matrix_maps_all_features():
    pbc_dir = Path(__file__).resolve().parents[1]
    pbcs_root = pbc_dir.parent
    improve = (pbc_dir / "improve1.md").read_text()
    matrix = (pbc_dir / "IMPROVE1_TRACEABILITY.md").read_text()
    features = re.findall(r"^###\s+(\d+)\.\s+(.+)$", improve, re.M)
    rows = [line for line in matrix.splitlines() if line.startswith("| ") and not line.startswith("| #") and not line.startswith("|---")]

    assert len(features) == 50
    assert len(rows) == len(features)
    for heading in REQUIRED_COLUMNS:
        assert heading in matrix

    for index, ((feature_number, feature_title), row) in enumerate(zip(features, rows), start=1):
        cells = _split_row(row)
        assert len(cells) == 7
        assert cells[0] == str(index) == feature_number
        assert cells[1] == feature_title
        for evidence_cell in cells[2:]:
            assert "`missing`" not in evidence_cell
            refs = re.findall(r"`([^`]+)`", evidence_cell)
            assert refs, f"row {index} has no evidence refs in {evidence_cell!r}"
            for ref in refs:
                assert (pbcs_root / ref).exists(), f"row {index} references missing evidence path: {ref}"
