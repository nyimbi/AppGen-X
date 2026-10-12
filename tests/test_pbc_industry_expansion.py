from pyAppGen.pbc import (
    PBC_CATALOG,
    PBC_INDUSTRY_EXPANSION_CANDIDATES,
    PBC_INDUSTRY_EXPANSION_OVERLAP_DECISIONS,
    _pbc_descriptor,
)


def test_industry_expansion_candidates_are_registered_without_key_overlap():
    assert len(PBC_INDUSTRY_EXPANSION_CANDIDATES) == 80
    assert len(set(PBC_INDUSTRY_EXPANSION_CANDIDATES)) == 80
    assert set(PBC_INDUSTRY_EXPANSION_CANDIDATES) <= set(PBC_CATALOG)
    for key in PBC_INDUSTRY_EXPANSION_CANDIDATES:
        decision = PBC_INDUSTRY_EXPANSION_OVERLAP_DECISIONS[key]
        assert decision['decision'] == 'create_new_pbc'
        # Read the descriptor, not the catalog literal. The literal's
        # tables/emits/consumes were a second copy of the package's surface and
        # had rotted in 16 of 144 rows; the descriptor reads the package, so it
        # is the only statement of the surface that can be trusted.
        descriptor = _pbc_descriptor(key, PBC_CATALOG[key])
        assert descriptor['tables']
        assert descriptor['apis']
        assert descriptor['emits']
        assert descriptor['consumes']
        assert descriptor['standard_features']
        assert descriptor['advanced_capabilities']


def test_industry_expansion_adjacent_domains_are_explained():
    adjacent = {key: value for key, value in PBC_INDUSTRY_EXPANSION_OVERLAP_DECISIONS.items() if value['adjacent_existing_pbc']}
    assert adjacent
    assert all(value['rationale'] for value in adjacent.values())
