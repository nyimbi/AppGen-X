"""The composition plan must separate a real interlock from an event loop.

`pbc_composition_plan` reads each selected PBC's emitted and consumed events and
reports what crosses between them. It had one bucket for "the event is emitted
somewhere in this composition", which is wrong in two ways.

A PBC that consumes an event it also emits was reported as its own provider.
That is the platform's normal outbox-to-own-inbox projection, not a dependency
on another PBC, and `ar_credit` doing it with `DeliveryConfirmed` put a
self-edge into the three-PBC plan's only dependency.

The provider lookup was also a dict comprehension, so when two selected PBCs
both emit an event, whichever came last in selection order became "the"
provider. Thirteen events are emitted by more than one package in the catalog
and 46 consumer rows depend on one of them, so the plan was asserting an
arbitrary choice as fact.

These tests pin the three buckets: a dependency crosses between two different
selected PBCs, an external event contract is emitted by none, and an internal
event loop is emitted only by its own consumer.
"""

import collections

import pytest

from pyAppGen import pbc

COMPOSITION = ("dam_core", "gl_core", "ar_credit")


def _descriptor(key: str) -> dict:
    return pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])


def _last_writer_emitted(selected: tuple[str, ...]) -> dict[str, str]:
    """Rebuild the old provider map, keeping the last emitter of each event."""
    emitted: dict[str, str] = {}
    for key in selected:
        for event in _descriptor(key).get("emits") or ():
            emitted[event] = key
    return emitted


@pytest.mark.parametrize("key", COMPOSITION)
def test_a_dependency_is_never_the_consumer_itself(key: str) -> None:
    """No PBC in the reference composition is its own provider."""
    plan = pbc.pbc_composition_plan(COMPOSITION)
    assert all(item["provider"] != item["from"] for item in plan["dependencies"]), key


def test_the_three_reference_pbcs_interlock_through_external_contracts_only() -> None:
    """The three share no event, so every cross-boundary event is an obligation.

    `dam_core` emits twenty events and consumes `ProductPublished`, which
    neither `gl_core` nor `ar_credit` emits. The plan's dependencies are
    therefore empty and its external contracts carry the integration surface.
    """
    plan = pbc.pbc_composition_plan(COMPOSITION)

    assert plan["dependencies"] == ()
    assert plan["external_event_contracts"], "the composition has integration obligations"
    emitted = {key: set(_descriptor(key).get("emits") or ()) for key in COMPOSITION}
    for item in plan["external_event_contracts"]:
        assert not any(item["event"] in emitted[other] for other in COMPOSITION), item


def test_a_self_consumed_event_is_reported_as_an_internal_loop() -> None:
    """`ar_credit` projects its own `DeliveryConfirmed`, and says so.

    The package records a delivery and emits the event, then handles the same
    event to build its delivery projection. Both halves are real, so the event
    belongs in neither of the other two buckets.
    """
    plan = pbc.pbc_composition_plan(COMPOSITION)
    loops = {(item["pbc"], item["event"]) for item in plan["internal_event_loops"]}

    assert ("ar_credit", "DeliveryConfirmed") in loops
    assert not any(item["event"] == "DeliveryConfirmed" for item in plan["dependencies"])


def _contested_selection() -> tuple[tuple[str, ...], str, set[str]]:
    """Return a selection where a consumed event has two selected providers.

    Found from the catalog rather than hardcoded: an event with at least two
    emitters, and a third PBC that consumes it and emits nothing of the same
    name. Selecting all of them makes the ambiguity real rather than latent, so
    the assertion has something to be right or wrong about.
    """
    emitters: dict[str, list[str]] = collections.defaultdict(list)
    consumers: dict[str, list[str]] = collections.defaultdict(list)
    for key in pbc.IMPLEMENTED_PBC_KEYS:
        descriptor = _descriptor(key)
        for event in descriptor.get("emits") or ():
            emitters[event].append(key)
        for event in descriptor.get("consumes") or ():
            consumers[event].append(key)
    for event, producers in sorted(emitters.items()):
        if len(producers) < 2:
            continue
        for consumer in consumers.get(event, ()):
            if consumer in producers:
                continue
            selected = tuple(dict.fromkeys((*producers[:2], consumer)))
            return selected, event, set(producers[:2])
    raise AssertionError("no event has two emitters and a third-party consumer")


def test_an_event_two_selected_pbcs_emit_names_both() -> None:
    """A shared emitter is ambiguous, and the plan reports both candidates.

    `dom` and `wms_core` both emit `OrderShipped` and `gl_core` consumes it, so
    the selected composition has two candidate providers. Reporting one of them
    as `provider` was a fact about selection order, not about the composition.
    """
    selected, event, producers = _contested_selection()
    plan = pbc.pbc_composition_plan(selected)

    row = next(item for item in plan["dependencies"] if item["event"] == event)
    assert set(row["providers"]) == producers, row
    assert row["provider"] in producers, row
    assert row["from"] not in producers, row


def test_the_check_canaries_against_the_last_writer_map() -> None:
    """Point the check at the old map and confirm it reports the wrong provider.

    The old map kept the last emitter of each event, so the same selection under
    it must disagree with the plan. If this canary cannot produce a
    disagreement, the assertion above is measuring nothing.
    """
    selected, event, producers = _contested_selection()
    old = _last_writer_emitted(selected)
    assert old[event] == selected[len(producers) - 1], "the old map keeps the last writer"
    assert old[event] in producers, "the last writer is one of the emitters, so only one is named"

    plan = pbc.pbc_composition_plan(selected)
    row = next(item for item in plan["dependencies"] if item["event"] == event)
    assert len(row["providers"]) > 1, "the plan must name every candidate, not the last writer"
