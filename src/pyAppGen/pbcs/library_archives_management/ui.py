"""UI contract for the Library and Archives Management PBC."""

from __future__ import annotations

from .controls import library_archives_management_control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .forms import library_archives_management_form_catalog
from .runtime import LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import LIBRARY_ARCHIVES_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .runtime import library_archives_management_permissions_contract
from .wizards import library_archives_management_wizard_catalog

PBC_KEY = "library_archives_management"
REQUIRED_DOMAIN_AREAS = (
    "accessioning",
    "cataloging",
    "authority control",
    "circulation/loans",
    "holds",
    "acquisitions",
    "preservation",
    "digitization",
    "rights/access restrictions",
    "finding aids",
    "reading-room requests",
    "deaccessioning",
    "provenance",
    "conservation",
    "audits",
    "assistant CRUD previews",
)

LIBRARY_ARCHIVES_MANAGEMENT_UI_FRAGMENT_KEYS = (
    "LibraryArchivesManagementWorkbench",
    "LibraryArchivesManagementDetail",
    "LibraryArchivesManagementAssistantPanel",
    "LibraryArchivesManagementAccessionBoard",
    "LibraryArchivesManagementCatalogStudio",
    "LibraryArchivesManagementFindingAidStudio",
    "LibraryArchivesManagementReadingRoomDesk",
    "LibraryArchivesManagementPreservationConsole",
    "LibraryArchivesManagementControlCenter",
    "LibraryArchivesManagementStandaloneWorkbench",
)



def library_archives_management_ui_contract() -> dict:
    """Return the package-local UI contract with form, wizard, and control surfaces."""
    surface = domain_capability_surface_contract()
    forms = library_archives_management_form_catalog()
    wizards = library_archives_management_wizard_catalog()
    controls = library_archives_management_control_catalog()
    permissions = library_archives_management_permissions_contract()
    return {
        "format": "appgen.library-archives-management-ui-contract.v1",
        "ok": surface["ok"] and forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "fragments": LIBRARY_ARCHIVES_MANAGEMENT_UI_FRAGMENT_KEYS,
        "forms": forms["form_ids"],
        "wizards": wizards["wizard_ids"],
        "controls": controls["control_ids"],
        "routes": (
            f"/workbench/pbcs/{PBC_KEY}",
            f"/workbench/pbcs/{PBC_KEY}/accessions",
            f"/workbench/pbcs/{PBC_KEY}/catalog",
            f"/workbench/pbcs/{PBC_KEY}/authority",
            f"/workbench/pbcs/{PBC_KEY}/finding-aids",
            f"/workbench/pbcs/{PBC_KEY}/circulation",
            f"/workbench/pbcs/{PBC_KEY}/reading-room",
            f"/workbench/pbcs/{PBC_KEY}/preservation",
            f"/workbench/pbcs/{PBC_KEY}/digitization",
            f"/workbench/pbcs/{PBC_KEY}/rights",
            f"/workbench/pbcs/{PBC_KEY}/deaccession",
            f"/workbench/pbcs/{PBC_KEY}/audits",
            f"/workbench/pbcs/{PBC_KEY}/assistant-preview",
            f"/workbench/pbcs/{PBC_KEY}/standalone",
        ),
        "panels": (
            {
                "key": "accession_processing",
                "fragment": "LibraryArchivesManagementAccessionBoard",
                "binds_to": (
                    "library_archives_management_archive_request",
                    "library_archives_management_collection_item",
                    "library_archives_management_rights_statement",
                ),
                "commands": (
                    "record_archive_request",
                    "create_collection_item",
                    "simulate_rights_statement",
                ),
            },
            {
                "key": "catalog_and_finding_aids",
                "fragment": "LibraryArchivesManagementCatalogStudio",
                "binds_to": (
                    "library_archives_management_catalog_record",
                    "library_archives_management_collection_item",
                ),
                "commands": (
                    "record_catalog_record",
                    "review_library_archives_management_policy_rule",
                ),
            },
            {
                "key": "reading_room_access",
                "fragment": "LibraryArchivesManagementReadingRoomDesk",
                "binds_to": (
                    "library_archives_management_circulation_loan",
                    "library_archives_management_rights_statement",
                    "library_archives_management_archive_request",
                ),
                "commands": (
                    "review_circulation_loan",
                    "simulate_rights_statement",
                ),
            },
            {
                "key": "preservation_and_digitization",
                "fragment": "LibraryArchivesManagementPreservationConsole",
                "binds_to": (
                    "library_archives_management_preservation_action",
                    "library_archives_management_digitization_job",
                    "library_archives_management_rights_statement",
                ),
                "commands": (
                    "create_preservation_action",
                    "approve_digitization_job",
                    "simulate_rights_statement",
                ),
            },
            {
                "key": "controls",
                "fragment": "LibraryArchivesManagementControlCenter",
                "binds_to": (
                    "library_archives_management_library_archives_management_control_assertion",
                    "library_archives_management_appgen_outbox_event",
                    "library_archives_management_appgen_dead_letter_event",
                ),
                "commands": (
                    "build_release_evidence",
                    "verify_owned_table_boundary",
                    "run_advanced_assessment",
                ),
            },
        ),
        "action_permissions": permissions["permissions"],
        "configuration_editor": {
            "required_fields": (
                "LIBRARY_ARCHIVES_MANAGEMENT_DATABASE_URL",
                "LIBRARY_ARCHIVES_MANAGEMENT_EVENT_TOPIC",
                "LIBRARY_ARCHIVES_MANAGEMENT_RETRY_LIMIT",
                "LIBRARY_ARCHIVES_MANAGEMENT_DEFAULT_POLICY",
            ),
            "allowed_database_backends": LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": LIBRARY_ARCHIVES_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "accessions",
                "catalog",
                "authority",
                "circulation",
                "reading_room",
                "preservation",
                "digitization",
                "rights",
                "deaccession",
                "assistant_preview",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
            "required_domain_areas": REQUIRED_DOMAIN_AREAS,
        },
        "coverage": {
            "forms": forms["domain_areas"],
            "wizards": wizards["domain_areas"],
            "controls": controls["domain_areas"],
        },
        "side_effects": (),
    }



def library_archives_management_render_workbench() -> dict:
    """Return a lightweight standalone workbench description."""
    ui = library_archives_management_ui_contract()
    return {
        "ok": ui["ok"],
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}/standalone",
        "fragments": ui["fragments"],
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "supported_domain_areas": REQUIRED_DOMAIN_AREAS,
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise the package-local UI contract and workbench rendering."""
    contract = library_archives_management_ui_contract()
    rendered = library_archives_management_render_workbench()
    return {
        "ok": contract["ok"] and rendered["ok"],
        "contract": contract,
        "rendered": rendered,
        "side_effects": (),
    }
