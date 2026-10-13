"""No PBC may pad its domain-operation list with numbered placeholders.

`DOMAIN_OPERATIONS` is the capability surface a PBC publishes: the UI turns each
entry into an operation button, the agent exposes it as `<key>_skills.<op>`, and
the edge-case queues and permission strings are built from it one-to-one. A
placeholder therefore is not a harmless extra list item; it manufactures a button
that dispatches to nothing and an agent tool that does not exist.

The placeholders were `operate_<key>_13` .. `operate_<key>_18`, appended to reach
the `>= 15` floor in `tests/test_pbc_enterprise_domain_depth.py`. They also broke
the table mapping: `execute_domain_operation` resolved a target by
`DOMAIN_OWNED_TABLES[index % len(...)]`, so slot 13 pointed at the outbox event
table. The honest packages instead carry an explicit `_OPERATION_TARGETS` map, so
each operation names the table it writes.

This test asserts the property the padding violated, across the whole catalog:
every operation is a real name, and every operation resolves to a table its own
package owns.
"""

import importlib
import re

import pytest

from pyAppGen import pbc

# A placeholder is a numbered suffix, or one of the filler verbs the generator
# used. `create_rating_model_v2` is a legitimate name; `operate_x_13` is not, and
# the distinguishing feature is the trailing integer, not the verb alone.
_PADDING = re.compile(r"_\d+$")
_FILLER = re.compile(r"^(operate|manage|handle|run|process|execute)_.+_\d+$")

# The packages the padding was authored into. The gate runs over the whole
# catalog, but these are the ones a regression would reappear in first.
_PADDED_PBCS = (
    "actuarial_pricing_reserving",
    "advertising_campaign_operations",
    "livestock_herd_management",
    "capital_projects_delivery",
    "defense_readiness_logistics",
    "donor_grant_fundraising",
)


def _domain_module(key: str):
    return importlib.import_module(f"pyAppGen.pbcs.{key}.domain_depth")


def _operations(key: str) -> tuple[str, ...]:
    return tuple(_domain_module(key).DOMAIN_OPERATIONS)


def _placeholder_operations(key: str) -> list[str]:
    return sorted(op for op in _operations(key) if _PADDING.search(op) or _FILLER.match(op))


def _unowned_operation_targets(key: str) -> list[tuple[str, str]]:
    """Operations whose resolved target table the package does not own.

    Resolution is read from the running object, not re-derived: packages spell
    the map three ways (an `_OPERATION_TARGETS` of plain strings, one of
    `(table, event, permission)` tuples, or no map at all with the index-modulo
    fallback). Calling `execute_domain_operation` and reading `target_table`
    reports what the package actually resolves at runtime, so the check cannot
    drift from the code it is checking.
    """
    module = _domain_module(key)
    owned = set(module.DOMAIN_OWNED_TABLES)
    execute = module.execute_domain_operation
    bad: list[tuple[str, str]] = []
    for operation in module.DOMAIN_OPERATIONS:
        result = execute(operation, {"tenant": "tenant-gate"})
        target = result.get("target_table")
        if target not in owned:
            bad.append((operation, target))
    return bad


def test_the_padded_packages_carry_no_placeholder_operations() -> None:
    offenders = {key: _placeholder_operations(key) for key in _PADDED_PBCS}
    offenders = {key: ops for key, ops in offenders.items() if ops}
    assert not offenders, f"placeholder domain operations survived: {offenders}"


def test_no_pbc_declares_a_placeholder_domain_operation() -> None:
    """The property holds across the whole implemented catalog.

    The padding was one templating decision applied to every package at once, so
    it could reappear anywhere the template is reused. Checking all of them costs
    a few seconds and is the only way to know the class is closed.
    """
    offenders = {}
    for key in pbc.IMPLEMENTED_PBC_KEYS:
        try:
            found = _placeholder_operations(key)
        except (ImportError, AttributeError):
            continue
        if found:
            offenders[key] = found
    assert not offenders, f"placeholder domain operations: {offenders}"


def test_every_domain_operation_targets_a_table_its_package_owns() -> None:
    offenders = {}
    for key in pbc.IMPLEMENTED_PBC_KEYS:
        try:
            bad = _unowned_operation_targets(key)
        except (ImportError, AttributeError):
            continue
        if bad:
            offenders[key] = bad
    assert not offenders, f"operations resolving outside the owned set: {offenders}"


@pytest.mark.parametrize("key", _PADDED_PBCS)
def test_a_padded_package_still_meets_the_depth_floor_honestly(key: str) -> None:
    """Removing padding must not drop a package below the published floor.

    `tests/test_pbc_enterprise_domain_depth.py` asserts `operation_count >= 15`
    for its own twenty keys. The padded packages live outside that set, so the
    floor is asserted here for the ones this change touched.
    """
    assert len(_operations(key)) >= 15, key


def test_the_check_canaries_against_a_planted_placeholder() -> None:
    """Point the check at the bug's own shape and confirm it reports it.

    The padding is a numbered suffix. Planting one on a real package must make
    the placeholder check report it; if the canary does not fire, the checks
    above are measuring something that cannot fail.
    """
    key = "actuarial_pricing_reserving"
    module = _domain_module(key)
    planted = tuple(module.DOMAIN_OPERATIONS) + (f"operate_{key}_99",)

    found = sorted(op for op in planted if _PADDING.search(op) or _FILLER.match(op))
    assert found == [f"operate_{key}_99"], "the canary planted nothing the check would see"

    # The shipped package must be clean, or the canary is describing live code.
    assert _placeholder_operations(key) == []
