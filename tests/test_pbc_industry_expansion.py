from pyAppGen.pbc import PBC_CATALOG, PBC_INDUSTRY_EXPANSION_CANDIDATES, PBC_INDUSTRY_EXPANSION_OVERLAP_DECISIONS


def test_industry_expansion_candidates_are_registered_without_key_overlap():
    assert len(PBC_INDUSTRY_EXPANSION_CANDIDATES) == 80
    assert len(set(PBC_INDUSTRY_EXPANSION_CANDIDATES)) == 80
    assert set(PBC_INDUSTRY_EXPANSION_CANDIDATES) <= set(PBC_CATALOG)
    for key in PBC_INDUSTRY_EXPANSION_CANDIDATES:
        decision = PBC_INDUSTRY_EXPANSION_OVERLAP_DECISIONS[key]
        assert decision['decision'] == 'create_new_pbc'
        assert PBC_CATALOG[key]['tables']
        assert PBC_CATALOG[key]['apis']
        assert PBC_CATALOG[key]['emits']
        assert PBC_CATALOG[key]['consumes']
        assert PBC_CATALOG[key]['standard_features']
        assert PBC_CATALOG[key]['advanced_capabilities']


def test_industry_expansion_adjacent_domains_are_explained():
    adjacent = {key: value for key, value in PBC_INDUSTRY_EXPANSION_OVERLAP_DECISIONS.items() if value['adjacent_existing_pbc']}
    assert adjacent
    assert all(value['rationale'] for value in adjacent.values())
