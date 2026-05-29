from .agent import datastore_crud_plan, document_instruction_plan
from .permissions import permission_manifest
from .runtime import banking_core_accounts_build_release_evidence
from .workflows import workflow_manifest


def build_release_evidence():
    return banking_core_accounts_build_release_evidence()


def release_readiness_manifest():
    evidence = build_release_evidence()
    workflows = workflow_manifest()
    permissions = permission_manifest()
    assistant_preview = document_instruction_plan(
        "customer onboarding pack", "open account for verified customer"
    )
    crud_preview = datastore_crud_plan("update")
    return {
        "ok": evidence["ok"] and workflows["ok"] and permissions["ok"] and assistant_preview["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "forms",
            "wizards",
            "controls",
            "workflows",
            "permissions",
            "single_pbc_app",
            "agent",
            "assistant_document_planning",
            "governance",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "workflow_manifest": workflows,
        "permissions_manifest": permissions,
        "assistant_preview": assistant_preview,
        "crud_preview": crud_preview,
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"]
        and not manifest["blocking_gaps"]
        and "single_pbc_app" in manifest["sections"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if not check["ok"]),
        "workflow_gaps": () if manifest["workflow_manifest"]["workflow_ids"] else ("workflow_manifest",),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],
        "side_effects": (),
    }
