from pyAppGen.pbc import FEDERATED_IAM_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import federated_iam_approve_privileged_access
from pyAppGen.pbc import federated_iam_assign_role
from pyAppGen.pbc import federated_iam_build_workbench_view
from pyAppGen.pbc import federated_iam_configure_runtime
from pyAppGen.pbc import federated_iam_empty_state
from pyAppGen.pbc import federated_iam_evaluate_policy
from pyAppGen.pbc import federated_iam_grant_token
from pyAppGen.pbc import federated_iam_link_identity
from pyAppGen.pbc import federated_iam_provision_tenant
from pyAppGen.pbc import federated_iam_register_identity_provider
from pyAppGen.pbc import federated_iam_register_principal
from pyAppGen.pbc import federated_iam_register_rule
from pyAppGen.pbc import federated_iam_render_workbench
from pyAppGen.pbc import federated_iam_runtime_capabilities
from pyAppGen.pbc import federated_iam_runtime_smoke
from pyAppGen.pbc import federated_iam_set_parameter
from pyAppGen.pbc import federated_iam_ui_contract
from pyAppGen.pbc import federated_iam_verify_credential
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_federated_iam_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = federated_iam_runtime_capabilities()
    smoke = federated_iam_runtime_smoke()

    assert runtime["format"] == "appgen.federated-iam-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/federated_iam"
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(FEDERATED_IAM_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("federated_iam")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "IamConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(FEDERATED_IAM_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("federated_iam",))["ok"] is True
    assert pbc_implemented_capability_audit(("federated_iam",))["ok"] is True


def test_federated_iam_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = federated_iam_empty_state()
    state = federated_iam_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.identity.events",
            "retry_limit": 3,
            "allowed_regions": ("US",),
            "allowed_provider_types": ("oidc", "saml", "did_vc"),
            "allowed_principal_types": ("user", "service_account"),
            "allowed_grant_types": ("authorization_code", "client_credentials"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = federated_iam_set_parameter(state, "minimum_trust_score", 0.8)["state"]
    state = federated_iam_set_parameter(state, "session_risk_threshold", 0.6)["state"]
    state = federated_iam_set_parameter(state, "token_ttl_minutes", 60)["state"]
    state = federated_iam_set_parameter(state, "privileged_access_ttl_minutes", 30)["state"]
    state = federated_iam_set_parameter(state, "step_up_threshold", 0.7)["state"]
    state = federated_iam_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "access",
            "allowed_regions": ("US",),
            "allowed_roles": ("catalog_admin", "auditor"),
            "required_claims": ("email", "tenant"),
            "deny_actions": ("delete_tenant",),
            "privileged_actions": ("rotate_key",),
            "status": "active",
        },
    )["state"]

    tenant = federated_iam_provision_tenant(state, {"tenant_id": "tenant_ops", "name": "Ops", "region": "US", "status": "active"})
    state = tenant["state"]
    assert tenant["tenant"]["status"] == "active"

    principal = federated_iam_register_principal(
        state,
        {"principal_id": "principal_ops", "tenant": "tenant_ops", "principal_type": "user", "display_name": "Ada Admin", "status": "active"},
    )
    state = principal["state"]
    assert principal["principal"]["status"] == "active"

    provider = federated_iam_register_identity_provider(
        state,
        {"provider_id": "provider_ops", "tenant": "tenant_ops", "provider_type": "oidc", "issuer": "https://idp.example", "status": "active"},
    )
    state = provider["state"]
    assert provider["provider"]["status"] == "active"

    identity = federated_iam_link_identity(
        state,
        {"identity_id": "identity_ops", "tenant": "tenant_ops", "principal_id": "principal_ops", "provider_id": "provider_ops", "subject": "ada", "claims": {"email": "ada@example.com", "tenant": "tenant_ops"}, "trust_score": 0.92},
    )
    state = identity["state"]
    assert identity["identity"]["status"] == "linked"

    credential = federated_iam_verify_credential(
        state,
        {"verification_id": "verify_ops", "tenant": "tenant_ops", "principal_id": "principal_ops", "credential_type": "did_vc", "issuer": "trusted_registry", "status": "active", "confidence": 0.94},
    )
    state = credential["state"]
    assert credential["credential"]["verified"] is True

    role = federated_iam_assign_role(
        state,
        {"assignment_id": "role_ops", "tenant": "tenant_ops", "principal_id": "principal_ops", "role": "catalog_admin", "scope": "product_catalog_pim", "status": "active"},
    )
    state = role["state"]
    assert role["role_assignment"]["status"] == "active"

    decision = federated_iam_evaluate_policy(
        state,
        {"decision_id": "decision_ops", "tenant": "tenant_ops", "principal_id": "principal_ops", "action": "publish_product", "resource": "product_catalog_pim", "context": {"region": "US", "risk": 0.2}},
    )
    state = decision["state"]
    assert decision["policy_decision"]["decision"] == "allow"

    token = federated_iam_grant_token(
        state,
        {"grant_id": "grant_ops", "tenant": "tenant_ops", "principal_id": "principal_ops", "grant_type": "authorization_code", "audience": "product_catalog_pim", "scopes": ("product_catalog_pim.publish",)},
    )
    state = token["state"]
    assert token["token_grant"]["status"] == "granted"
    assert token["handoffs"] == ("gateway_token_projection", "audit_access_projection", "principal_session_projection")

    privileged = federated_iam_approve_privileged_access(
        state,
        {"request_id": "priv_ops", "tenant": "tenant_ops", "principal_id": "principal_ops", "action": "rotate_key", "resource": "tenant_ops", "risk": 0.4, "approved_by": "security_admin"},
    )
    state = privileged["state"]
    assert privileged["privileged_access"]["status"] == "approved"
    assert state["outbox"][-1]["idempotency_key"] == "federated_iam:PrivilegedAccessApproved:iam_evt_000009"

    workbench = federated_iam_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["principal_count"] == 1
    assert workbench["provider_count"] == 1
    assert workbench["identity_count"] == 1
    assert workbench["active_role_count"] == 1
    assert workbench["policy_decision_count"] == 1
    assert workbench["allowed_decision_count"] == 1
    assert workbench["token_grant_count"] == 1
    assert workbench["privileged_access_count"] == 1

    ui_contract = federated_iam_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "minimum_trust_score" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = federated_iam_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "federated_iam.tenant",
            "federated_iam.principal",
            "federated_iam.policy",
            "federated_iam.token",
            "federated_iam.privileged",
            "federated_iam.configure",
            "federated_iam.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 9
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
