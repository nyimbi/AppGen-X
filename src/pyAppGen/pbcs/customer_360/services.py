"""Command service layer for the customer_360 PBC."""

from __future__ import annotations

from .models import Customer360StandaloneStore
from .models import standalone_model_contract

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.customer_360.events', 'inbox_topic': 'pbc.customer_360.inbox', 'outbox_table': 'customer_360_appgen_outbox_event', 'inbox_table': 'customer_360_appgen_inbox_event', 'dead_letter_table': 'customer_360_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomerUpdated', 'schema': 'customer_360.customer_updated.emitted.v1', 'topic': 'pbc.customer_360.events', 'outbox_table': 'customer_360_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PreferenceChanged', 'schema': 'customer_360.preference_changed.emitted.v1', 'topic': 'pbc.customer_360.events', 'outbox_table': 'customer_360_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InvoiceIssued', 'schema': 'customer_360.invoice_issued.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'customer_360.payment_captured.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CandidateHired', 'schema': 'customer_360.candidate_hired.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'customer_360_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'customer_360_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_profiles', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/customer_360/profiles', 'permission': 'customer_360.command.1', 'owned_tables': ('customer_360_customer_profile', 'customer_360_engagement_event', 'customer_360_communication_preference', 'customer_360_touchpoint'), 'read_tables': (), 'emitted_event': 'CustomerUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_touchpoints', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/customer_360/touchpoints', 'permission': 'customer_360.command.2', 'owned_tables': ('customer_360_customer_profile', 'customer_360_engagement_event', 'customer_360_communication_preference', 'customer_360_touchpoint'), 'read_tables': (), 'emitted_event': 'PreferenceChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_customer_timeline', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/customer_360/customer-timeline', 'permission': 'customer_360.query.3', 'owned_tables': (), 'read_tables': ('customer_360_customer_profile', 'customer_360_engagement_event', 'customer_360_communication_preference', 'customer_360_touchpoint'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(item['emitted_event'] for item in command_contracts)
        and all(item['owned_tables'] and not item['read_tables'] for item in command_contracts)
        and all(item['emitted_event'] is None for item in query_contracts)
        and all(item['read_tables'] and not item['owned_tables'] for item in query_contracts),
        'pbc': 'customer_360',
        'operations': operations,
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
        'contracts': OPERATION_CONTRACTS,
        'side_effects': (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item['operation'] == operation_name), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_operation', 'operation': operation_name, 'side_effects': ()}
    supplied = dict(payload or {})
    table_scope = contract['owned_tables'] or contract['read_tables']
    return {
        'ok': bool(table_scope) and contract['event_contract'] == 'AppGen-X',
        'pbc': 'customer_360',
        'operation': operation_name,
        'operation_kind': contract['operation_kind'],
        'route': {'method': contract['method'], 'path': contract['path']},
        'permission': contract['permission'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'payload_keys': tuple(sorted(supplied)),
        'transaction_boundary': contract['transaction_boundary'],
        'event_contract': contract['event_contract'],
        'side_effects': (),
    }


class Customer360Service:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'customer_360',
            'operation': operation_name,
            'operation_kind': operation_kind,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'side_effects': (),
        }
        if operation_kind == 'command':
            event_type = plan.get('emitted_event')
            result.update({
                'command': operation_name,
                'read_only': False,
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (event_type,) if event_type else (),
            })
        elif operation_kind == 'query':
            result.update({
                'query': operation_name,
                'read_only': True,
                'outbox_table': None,
                'emits': (),
            })
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_profiles(self, payload=None):
        return self._command('command_profiles', payload or {})

    def command_touchpoints(self, payload=None):
        return self._command('command_touchpoints', payload or {})

    def query_customer_timeline(self, payload=None):
        return self._query('query_customer_timeline', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = Customer360Service()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'customer_360',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = Customer360Service()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok']
        and result.get('ok') is True
        and result.get('operation_contract', {}).get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }


STANDALONE_OPERATION_CONTRACTS = (
    {
        "operation": "create_profile",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/profiles",
        "handler": "create_profile",
        "permission": "customer_360.profile",
        "table": "customer_360_customer_profile",
        "form": "CustomerProfileIntakeForm",
        "wizard": "CustomerProfileOnboardingWizard",
    },
    {
        "operation": "link_identity",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/identities",
        "handler": "link_identity",
        "permission": "customer_360.profile",
        "table": "customer_360_customer_identity",
        "form": "CustomerIdentityLinkForm",
        "wizard": "CustomerProfileOnboardingWizard",
    },
    {
        "operation": "record_consent",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/consents",
        "handler": "record_consent",
        "permission": "customer_360.consent",
        "table": "customer_360_consent_record",
        "form": "CustomerConsentForm",
        "wizard": "ConsentRecoveryWizard",
    },
    {
        "operation": "set_preference",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/preferences",
        "handler": "set_preference",
        "permission": "customer_360.consent",
        "table": "customer_360_communication_preference",
        "form": "CustomerPreferenceForm",
        "wizard": "ConsentRecoveryWizard",
    },
    {
        "operation": "capture_touchpoint",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/touchpoints",
        "handler": "capture_touchpoint",
        "permission": "customer_360.engage",
        "table": "customer_360_touchpoint",
        "form": "CustomerTouchpointForm",
        "wizard": "CustomerTouchpointWizard",
    },
    {
        "operation": "ingest_engagement_event",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/engagement-events",
        "handler": "ingest_engagement_event",
        "permission": "customer_360.engage",
        "table": "customer_360_engagement_event",
        "form": "CustomerEngagementEventForm",
        "wizard": "CustomerTouchpointWizard",
    },
    {
        "operation": "open_merge_case",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/merge-cases",
        "handler": "open_merge_case",
        "permission": "customer_360.merge",
        "table": "customer_360_profile_merge_case",
        "form": "CustomerMergeReviewForm",
        "wizard": "MergeCaseResolutionWizard",
    },
    {
        "operation": "resolve_merge_case",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/merge-cases/resolve",
        "handler": "resolve_merge_case",
        "permission": "customer_360.merge",
        "table": "customer_360_profile_merge_case",
        "form": "CustomerMergeReviewForm",
        "wizard": "MergeCaseResolutionWizard",
    },
    {
        "operation": "receive_event",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/customer-360/events/inbox",
        "handler": "receive_event",
        "permission": "customer_360.event",
        "table": "customer_360_appgen_inbox_event",
        "form": "CustomerEventInboxForm",
        "wizard": "CustomerDocumentIntakeWizard",
    },
    {
        "operation": "get_profile",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/customer-360/profiles/detail",
        "handler": "get_profile",
        "permission": "customer_360.read",
        "table": "customer_360_customer_profile",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "list_profiles",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/customer-360/profiles",
        "handler": "list_profiles",
        "permission": "customer_360.read",
        "table": "customer_360_customer_profile",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "build_timeline",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/customer-360/timeline",
        "handler": "build_timeline",
        "permission": "customer_360.read",
        "table": "customer_360_engagement_event",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "build_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/customer-360/workbench",
        "handler": "build_workbench",
        "permission": "customer_360.read",
        "table": "customer_360_customer_profile",
        "form": None,
        "wizard": None,
    },
)


def standalone_service_operation_contracts() -> dict:
    return {
        "format": "appgen.customer-360-standalone-service-contract.v1",
        "ok": bool(STANDALONE_OPERATION_CONTRACTS),
        "pbc": "customer_360",
        "store_contract": standalone_model_contract(),
        "operations": tuple(item["operation"] for item in STANDALONE_OPERATION_CONTRACTS),
        "command_operations": tuple(
            item["operation"]
            for item in STANDALONE_OPERATION_CONTRACTS
            if item["operation_kind"] == "command"
        ),
        "query_operations": tuple(
            item["operation"]
            for item in STANDALONE_OPERATION_CONTRACTS
            if item["operation_kind"] == "query"
        ),
        "contracts": STANDALONE_OPERATION_CONTRACTS,
        "side_effects": (),
    }


class Customer360StandaloneService:
    """Executable standalone service backed by the package-local SQLite store."""

    def __init__(self, store: Customer360StandaloneStore | None = None):
        self.store = store or Customer360StandaloneStore()

    def close(self) -> None:
        self.store.close()

    def _wrap(self, operation: str, result: dict) -> dict:
        contract = next(
            item for item in STANDALONE_OPERATION_CONTRACTS if item["operation"] == operation
        )
        return {
            "ok": result.get("ok") is True,
            "operation": operation,
            "operation_kind": contract["operation_kind"],
            "route": {"method": contract["method"], "path": contract["path"]},
            "permission": contract["permission"],
            "table": contract["table"],
            "result": result,
            "side_effects": (),
        }

    def create_profile(self, payload: dict | None = None) -> dict:
        return self._wrap("create_profile", self.store.create_profile(payload or {}))

    def link_identity(self, payload: dict | None = None) -> dict:
        return self._wrap("link_identity", self.store.link_identity(payload or {}))

    def record_consent(self, payload: dict | None = None) -> dict:
        return self._wrap("record_consent", self.store.record_consent(payload or {}))

    def set_preference(self, payload: dict | None = None) -> dict:
        return self._wrap("set_preference", self.store.set_preference(payload or {}))

    def capture_touchpoint(self, payload: dict | None = None) -> dict:
        return self._wrap("capture_touchpoint", self.store.capture_touchpoint(payload or {}))

    def ingest_engagement_event(self, payload: dict | None = None) -> dict:
        return self._wrap("ingest_engagement_event", self.store.ingest_engagement_event(payload or {}))

    def open_merge_case(self, payload: dict | None = None) -> dict:
        return self._wrap("open_merge_case", self.store.open_merge_case(payload or {}))

    def resolve_merge_case(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        result = self.store.resolve_merge_case(
            supplied.get("merge_case_id", ""),
            supplied.get("resolved_by", "standalone_operator"),
        )
        return self._wrap("resolve_merge_case", result)

    def receive_event(self, payload: dict | None = None) -> dict:
        return self._wrap("receive_event", self.store.receive_event(payload or {}))

    def get_profile(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap(
            "get_profile",
            {"ok": True, "profile": self.store.get_profile(supplied.get("profile_id", ""))},
        )

    def list_profiles(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap(
            "list_profiles",
            {"ok": True, "profiles": self.store.list_profiles(supplied.get("tenant", ""))},
        )

    def build_timeline(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("build_timeline", self.store.build_timeline(supplied.get("profile_id", "")))

    def build_workbench(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("build_workbench", self.store.build_workbench(supplied.get("tenant", "")))


def standalone_service_smoke_test() -> dict:
    service = Customer360StandaloneService()
    try:
        create = service.create_profile(
            {
                "profile_id": "cust_service",
                "tenant": "tenant_service",
                "display_name": "Service Smoke",
                "region": "US",
            }
        )
        preference = service.set_preference(
            {
                "preference_id": "pref_service",
                "tenant": "tenant_service",
                "profile_id": "cust_service",
                "channel": "email",
                "topic": "updates",
                "status": "opt_in",
            }
        )
        timeline = service.build_timeline({"profile_id": "cust_service"})
        workbench = service.build_workbench({"tenant": "tenant_service"})
        return {
            "ok": create["ok"] and preference["ok"] and timeline["ok"] and workbench["ok"],
            "service_contract": standalone_service_operation_contracts(),
            "create": create,
            "timeline": timeline,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        service.close()
