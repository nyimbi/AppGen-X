"""Media Rights and Content Monetization PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .controls import media_rights_content_monetization_control_catalog
from .controls import media_rights_content_monetization_control_center
from .controls import media_rights_content_monetization_mutation_preview
from .forms import media_rights_content_monetization_form_catalog
from .forms import media_rights_content_monetization_get_form
from .forms import media_rights_content_monetization_validate_form_payload
from .release_evidence import build_release_evidence
from .release_evidence import release_readiness_manifest
from .release_evidence import validate_release_evidence
from .runtime import *
from .standalone import MediaRightsContentMonetizationStandaloneApplication
from .standalone import bootstrap_media_rights_content_monetization_standalone_app
from .standalone import media_rights_content_monetization_standalone_app_contract
from .standalone import media_rights_content_monetization_standalone_smoke
from .ui import media_rights_content_monetization_render_standalone_workbench
from .ui import media_rights_content_monetization_render_workbench
from .ui import media_rights_content_monetization_ui_contract
from .wizards import media_rights_content_monetization_plan_wizard
from .wizards import media_rights_content_monetization_wizard_catalog

PBC_KEY = 'media_rights_content_monetization'


def implementation_contract() -> dict:
    runtime = media_rights_content_monetization_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {
        **contract,
        'standard_features': runtime['standard_features'],
        'advanced_runtime': runtime,
        'ui_contract': media_rights_content_monetization_ui_contract(),
        'forms': media_rights_content_monetization_form_catalog(),
        'wizards': media_rights_content_monetization_wizard_catalog(),
        'controls': media_rights_content_monetization_control_catalog(),
        'standalone_app_contract': media_rights_content_monetization_standalone_app_contract(),
        'api_contract': media_rights_content_monetization_build_api_contract(),
        'schema_contract': media_rights_content_monetization_build_schema_contract(),
        'service_contract': media_rights_content_monetization_build_service_contract(),
        'release_evidence_contract': build_release_evidence(),
        'permissions_contract': media_rights_content_monetization_permissions_contract(),
        'owned_tables': MEDIA_RIGHTS_CONTENT_MONETIZATION_OWNED_TABLES,
        'runtime_tables': MEDIA_RIGHTS_CONTENT_MONETIZATION_RUNTIME_TABLES,
        'allowed_database_backends': MEDIA_RIGHTS_CONTENT_MONETIZATION_ALLOWED_DATABASE_BACKENDS,
        'required_event_topic': MEDIA_RIGHTS_CONTENT_MONETIZATION_REQUIRED_EVENT_TOPIC,
        'emits': MEDIA_RIGHTS_CONTENT_MONETIZATION_EMITTED_EVENT_TYPES,
        'consumes': MEDIA_RIGHTS_CONTENT_MONETIZATION_CONSUMED_EVENT_TYPES,
        'boundary_contract': media_rights_content_monetization_verify_owned_table_boundary(MEDIA_RIGHTS_CONTENT_MONETIZATION_OWNED_TABLES + ('api_dependency',)),
    }



def register_pbc() -> dict:
    return dict(PBC_MANIFEST)



def registration_plan(existing_catalog: dict | None = None) -> dict:
    return source_registration_plan(PBC_KEY, register_pbc(), existing_catalog=existing_catalog)



def package_metadata_manifest() -> dict:
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())



def validate_package_metadata() -> dict:
    return validate_source_package_metadata(package_metadata_manifest())



def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
    metadata_validation = validate_package_metadata()
    registration = registration_plan(existing_catalog=existing_catalog)
    return {'format': 'appgen.pbc-source-package-discovery-plan.v1', 'ok': metadata_validation['ok'] and registration['ok'], 'pbc': PBC_KEY, 'metadata_validation': metadata_validation, 'registration': registration, 'side_effects': ()}



def smoke_test() -> dict:
    discovery = package_discovery_plan()
    runtime = media_rights_content_monetization_runtime_smoke()
    standalone = media_rights_content_monetization_standalone_smoke()
    return {
        'ok': discovery['ok'] and runtime['ok'] and standalone['ok'],
        'discovery': discovery,
        'runtime': runtime,
        'standalone': standalone,
        'side_effects': (),
    }
