"""Focused contract tests for inventory_positioning."""

from __future__ import annotations

from .. import implementation_contract
from .. import package_discovery_plan
from .. import package_metadata_manifest
from .. import register_pbc
from .. import registration_plan
from .. import validate_package_metadata
from ..agent import smoke_test as agent_smoke_test
from ..capability_assurance import smoke_test as capability_smoke_test
from ..events import EVENT_CONTRACT
from ..events import smoke_test as event_smoke_test
from ..manifest import PBC_MANIFEST
from ..models import smoke_test as model_smoke_test
from ..permissions import smoke_test as permission_smoke_test
from ..release_evidence import RELEASE_EVIDENCE
from ..release_evidence import release_readiness_manifest
from ..release_evidence import smoke_test as release_smoke_test
from ..release_evidence import validate_release_evidence
from ..routes import smoke_test as route_smoke_test
from ..schema_contract import SCHEMA_CONTRACT
from ..schema_contract import smoke_test as schema_smoke_test
from ..seed_data import smoke_test as seed_smoke_test
from ..service_contract import SERVICE_CONTRACT
from ..services import smoke_test as service_smoke_test
from ..standalone import smoke_test as standalone_smoke_test
from ..ui import smoke_test as ui_smoke_test


def test_generated_schema_service_and_release_evidence() -> None:
    assert SCHEMA_CONTRACT["pbc"] == "inventory_positioning"
    assert SCHEMA_CONTRACT["ok"] is True
    assert SCHEMA_CONTRACT["owned_tables"]
    assert schema_smoke_test()["ok"] is True
    assert model_smoke_test()["ok"] is True
    assert SERVICE_CONTRACT["pbc"] == "inventory_positioning"
    assert SERVICE_CONTRACT["ok"] is True
    assert SERVICE_CONTRACT["eventing"]["dead_letter_table"] == "inventory_positioning_dead_letter_event"
    assert RELEASE_EVIDENCE["pbc"] == "inventory_positioning"
    assert RELEASE_EVIDENCE["ok"] is True
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()
    assert readiness["ok"] is True
    assert validation["ok"] is True
    assert not validation["missing_sections"]
    assert not validation["failed_checks"]
    assert not validation["boundary_gaps"]


def test_manifest_and_event_contract() -> None:
    assert PBC_MANIFEST["pbc"] == "inventory_positioning"
    assert PBC_MANIFEST["standard_features"]
    assert PBC_MANIFEST["advanced_capabilities"]
    assert EVENT_CONTRACT["contract"] == "appgen_event_contract"
    assert EVENT_CONTRACT["outbox_table"] == "inventory_positioning_appgen_outbox_event"
    assert EVENT_CONTRACT["inbox_table"] == "inventory_positioning_appgen_inbox_event"
    smoke = event_smoke_test()
    assert smoke["ok"] is True
    assert smoke["emitted"]["table"] == EVENT_CONTRACT["outbox_table"]
    assert smoke["consumed"]["dead_letter_table"] == "inventory_positioning_dead_letter_event"


def test_registration_plan_is_side_effect_free() -> None:
    assert register_pbc()["pbc"] == "inventory_positioning"
    plan = registration_plan()
    metadata = package_metadata_manifest()
    metadata_validation = validate_package_metadata()
    discovery = package_discovery_plan()
    assert plan["ok"] is True
    assert metadata["ok"] is True
    assert metadata_validation["ok"] is True
    assert discovery["ok"] is True
    assert metadata["event_contract"] == "AppGen-X"
    assert metadata["stream_engine_picker_visible"] is False


def test_package_surfaces_are_executable() -> None:
    contract = implementation_contract()
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["permissions_contract"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert contract["agent_contract"]["ok"] is True
    assert contract["standalone_contract"]["ok"] is True
    assert service_smoke_test()["ok"] is True
    assert route_smoke_test()["ok"] is True
    assert ui_smoke_test()["ok"] is True
    assert permission_smoke_test()["ok"] is True
    assert seed_smoke_test()["ok"] is True
    assert release_smoke_test()["ok"] is True
    assert agent_smoke_test()["ok"] is True
    assert standalone_smoke_test()["ok"] is True
    assert capability_smoke_test()["ok"] is True
