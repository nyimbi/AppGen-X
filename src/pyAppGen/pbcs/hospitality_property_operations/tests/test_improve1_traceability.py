"""Traceability checks for the improve1 implementation matrix."""

from pathlib import Path


def test_improve1_traceability_matrix_maps_all_features():
    pbc_dir = Path(__file__).resolve().parents[1]
    improve = (pbc_dir / "improve1.md").read_text()
    matrix = (pbc_dir / "IMPROVE1_TRACEABILITY.md").read_text()
    feature_count = sum(1 for line in improve.splitlines() if line.startswith("### "))
    rows = [line for line in matrix.splitlines() if line.startswith("| ") and not line.startswith("| #") and not line.startswith("|---")]
    assert feature_count == 50
    assert len(rows) == feature_count
    for heading in ("code artifact + model", "UI surface", "service/API", "test", "evidence"):
        assert heading in matrix
    for expected in range(1, 51):
        assert f"| {expected} |" in matrix
