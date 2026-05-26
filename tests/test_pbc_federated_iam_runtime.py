import pytest

from pyAppGen.pbcs.federated_iam import FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.federated_iam import FEDERATED_IAM_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.federated_iam import FEDERATED_IAM_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.federated_iam import FEDERATED_IAM_OWNED_TABLES
from pyAppGen.pbcs.federated_iam import FEDERATED_IAM_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.federated_iam import FEDERATED_IAM_RUNTIME_TABLES
from pyAppGen.pbcs.federated_iam import federated_iam_build_api_contract
from pyAppGen.pbcs.federated_iam import federated_iam_build_release_evidence
from pyAppGen.pbcs.federated_iam import federated_iam_build_schema_contract
from pyAppGen.pbcs.federated_iam import federated_iam_build_service_contract
from pyAppGen.pbcs.federated_iam import federated_iam_permissions_contract
from pyAppGen.pbcs.federated_iam import federated_iam_ui_contract
from pyAppGen.pbcs.federated_iam import implementation_contract as package_implementation_contract
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
from pyAppGen.pbc import federated_iam_receive_event
from pyAppGen.pbc import federated_iam_register_identity_provider
from pyAppGen.pbc import federated_iam_register_principal
from pyAppGen.pbc import federated_iam_register_rule
from pyAppGen.pbc import federated_iam_register_schema_extension
from pyAppGen.pbc import federated_iam_render_workbench
from pyAppGen.pbc import federated_iam_runtime_capabilities
from pyAppGen.pbc import federated_iam_runtime_smoke
from pyAppGen.pbc import federated_iam_set_parameter
from pyAppGen.pbc import federated_iam_verify_owned_table_boundary
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
    assert runtime["owned_tables"] == FEDERATED_IAM_OWNED_TABLES
    assert runtime["runtime_tables"] == FEDERATED_IAM_RUNTIME_TABLES
    assert runtime["required_event_topic"] == FEDERATED_IAM_REQUIRED_EVENT_TOPIC
    assert runtime["allowed_database_backends"] == FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert {"build_schema_contract", "build_service_contract", "build_release_evidence", "run_control_tests"} <= set(runtime["operations"])
    assert smoke["ok"] is True
    assert set(FEDERATED_IAM_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("federated_iam")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == FEDERATED_IAM_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["runtime_tables"] == FEDERATED_IAM_RUNTIME_TABLES
    assert contract["source_package"]["required_event_topic"] == FEDERATED_IAM_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == FEDERATED_IAM_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == FEDERATED_IAM_EMITTED_EVENT_TYPES
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "federated_iam.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "IamConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(FEDERATED_IAM_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("federated_iam",))["ok"] is True
    assert pbc_implemented_capability_audit(("federated_iam",))["ok"] is True
    package_contract = package_implementation_contract()
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True

    api = federated_iam_build_api_contract()
    permissions = federated_iam_permissions_contract()
    assert api["format"] == "appgen.federated-iam-api-contract.v1"
    assert api["owned_tables"] == FEDERATED_IAM_OWNED_TABLES
    assert api["runtime_tables"] == FEDERATED_IAM_RUNTIME_TABLES
    assert api["database_backends"] == FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == FEDERATED_IAM_EMITTED_EVENT_TYPES
    assert api["consumes"] == FEDERATED_IAM_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert api["required_event_topic"] == FEDERATED_IAM_REQUIRED_EVENT_TOPIC
    assert api["dependencies"]["shared_tables"] == ()
    assert api["rules_parameters_configuration"] == ("register_rule", "set_parameter", "configure_runtime")
    assert {route["route"] for route in api["routes"]} >= {
        "PUT /iam/configuration",
        "POST /iam/parameters",
        "POST /iam/rules",
        "POST /principals",
        "POST /iam/events/inbox",
        "GET /iam-workbench",
        "GET /iam/schema-contract",
        "GET /iam/service-contract",
        "GET /iam/release-evidence",
    }
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["grant_token"] == "federated_iam.token"
    assert permissions["action_permissions"]["build_schema_contract"] == "federated_iam.audit"
    assert permissions["action_permissions"]["build_service_contract"] == "federated_iam.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "federated_iam.audit"


def test_federated_iam_package_schema_service_release_and_ui_contracts() -> None:
    schema = federated_iam_build_schema_contract()
    service = federated_iam_build_service_contract()
    release = federated_iam_build_release_evidence()
    api = federated_iam_build_api_contract()
    ui = federated_iam_ui_contract()

    assert schema["format"] == "appgen.federated-iam-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(FEDERATED_IAM_OWNED_TABLES)
    assert len(schema["migrations"]) == len(FEDERATED_IAM_OWNED_TABLES)
    assert tuple(item["table"] for item in schema["runtime_tables"]) == FEDERATED_IAM_RUNTIME_TABLES
    assert schema["datastore_backends"] == FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
    assert schema["required_event_topic"] == FEDERATED_IAM_REQUIRED_EVENT_TOPIC
    assert schema["shared_table_access"] is False

    assert service["format"] == "appgen.federated-iam-service-contract.v1"
    assert service["ok"] is True
    assert service["transaction_boundary"] == "federated_iam_owned_datastore_plus_appgen_outbox"
    assert "receive_event" in service["idempotent_handlers"]
    assert service["retry_dead_letter_evidence"]["dead_letter_table"] == FEDERATED_IAM_RUNTIME_TABLES[2]
    assert service["eventing"]["contract"] == "AppGen-X"
    assert service["external_dependencies"]["shared_tables"] == ()
    assert service["rules_parameters_configuration"] == ("register_rule", "set_parameter", "configure_runtime")

    assert ui["binding_evidence"]["runtime_tables"] == FEDERATED_IAM_RUNTIME_TABLES
    assert ui["binding_evidence"]["event_contract"] == "AppGen-X"
    assert ui["binding_evidence"]["required_event_topic"] == FEDERATED_IAM_REQUIRED_EVENT_TOPIC
    assert ui["binding_evidence"]["shared_table_access"] is False

    assert any(route["command"] == "configure_runtime" for route in api["routes"])
    assert any(route["command"] == "set_parameter" for route in api["routes"])
    assert any(route["command"] == "register_rule" for route in api["routes"])
    assert any(route["command"] == "receive_event" for route in api["routes"])
    assert any(route.get("query") == "build_schema_contract" for route in api["routes"])
    assert any(route.get("query") == "build_service_contract" for route in api["routes"])
    assert any(route.get("query") == "build_release_evidence" for route in api["routes"])
    assert all(route["event_contract"] == "AppGen-X" for route in api["routes"])
    assert all(route["shared_table_access"] is False for route in api["routes"])

    assert release["format"] == "appgen.federated-iam-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert release["schema"]["format"] == schema["format"]
    assert release["service"]["format"] == service["format"]
    assert release["api"]["required_event_topic"] == FEDERATED_IAM_REQUIRED_EVENT_TOPIC
    assert release["ui"]["binding_evidence"]["runtime_tables"] == FEDERATED_IAM_RUNTIME_TABLES
    assert release["workbench"]["binding_evidence"]["outbox_table"] == FEDERATED_IAM_RUNTIME_TABLES[0]
    assert release["boundary"]["declared_dependencies"]["shared_tables"] == ()


def test_federated_iam_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = federated_iam_empty_state()
    state = federated_iam_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
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
    extension = federated_iam_register_schema_extension(state, "principal_identity", {"device_trust_payload": "jsonb", "assurance_payload": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["principal_identity"]["assurance_payload"] == "jsonb"
    role_event = federated_iam_receive_event(
        state,
        {"event_id": "evt_role_ops", "event_type": "RoleChanged", "payload": {"tenant": "tenant_ops", "role_id": "role_ops", "role": "catalog_admin"}},
    )
    state = role_event["state"]
    assert role_event["handler"]["status"] == "processed"
    duplicate = federated_iam_receive_event(
        state,
        {"event_id": "evt_role_ops", "event_type": "RoleChanged", "payload": {"tenant": "tenant_ops", "role_id": "role_ops", "role": "catalog_admin"}},
    )
    assert duplicate["duplicate"] is True

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
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["outbox_count"] == 9
    assert workbench["inbox_count"] == 1
    assert workbench["retry_evidence_count"] == 0
    assert workbench["binding_evidence"]["owned_tables"] == FEDERATED_IAM_OWNED_TABLES
    assert workbench["binding_evidence"]["runtime_tables"] == FEDERATED_IAM_RUNTIME_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["ui_bindings"]["rbac"]["receive_event"] == "federated_iam.event"
    assert workbench["binding_evidence"]["rules"] == ("rule_ops",)
    assert workbench["binding_evidence"]["parameters"] == (
        "minimum_trust_score",
        "privileged_access_ttl_minutes",
        "session_risk_threshold",
        "step_up_threshold",
        "token_ttl_minutes",
    )

    ui_contract = federated_iam_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == FEDERATED_IAM_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == FEDERATED_IAM_OWNED_TABLES
    assert ui_contract["binding_evidence"]["runtime_tables"] == FEDERATED_IAM_RUNTIME_TABLES
    assert ui_contract["binding_evidence"]["event_contract"] == "AppGen-X"
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
            "federated_iam.event",
            "federated_iam.configure",
            "federated_iam.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 9
    assert rendered["inbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == FEDERATED_IAM_OWNED_TABLES
    assert rendered["binding_evidence"]["configuration"] == workbench["binding_evidence"]["configuration"]
    assert rendered["binding_evidence"]["rules"] == workbench["binding_evidence"]["rules"]
    assert rendered["binding_evidence"]["parameters"] == workbench["binding_evidence"]["parameters"]
    assert rendered["binding_evidence"]["ui_bindings"] == {
        "configuration_fragment": "IamConfigurationPanel",
        "rule_fragment": "IamRuleStudio",
        "parameter_fragment": "IamParameterConsole",
        "outbox_table": FEDERATED_IAM_RUNTIME_TABLES[0],
        "inbox_table": FEDERATED_IAM_RUNTIME_TABLES[1],
        "dead_letter_table": FEDERATED_IAM_RUNTIME_TABLES[2],
        "rbac": ui_contract["action_permissions"],
    }

    boundary = federated_iam_verify_owned_table_boundary(
        ("principal", "RoleChanged", "gateway_token_projection", "POST /audit/access-events", FEDERATED_IAM_RUNTIME_TABLES[0])
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = federated_iam_verify_owned_table_boundary(("customer_360",))
    assert violation["ok"] is False
    assert violation["violations"] == ("customer_360",)


def test_federated_iam_rejects_unsupported_database_backends_eventing_and_boundaries() -> None:
    state = federated_iam_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        federated_iam_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        federated_iam_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Federated IAM parameter"):
        federated_iam_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        federated_iam_register_schema_extension(state, "customer_360", {"principal_ref": "jsonb"})

    configured = federated_iam_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": FEDERATED_IAM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "allowed_regions": ("US",),
            "allowed_provider_types": ("oidc",),
            "allowed_principal_types": ("user",),
            "allowed_grant_types": ("authorization_code",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    retrying = federated_iam_receive_event(
        configured,
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    dead_letter = federated_iam_receive_event(
        retrying["state"],
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1
    assert len(dead_letter["state"]["retry_evidence"]) == 2
