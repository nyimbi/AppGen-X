"""Executable pre-trade trade order intake slice for trading operations."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib

PBC_KEY = 'capital_markets_trading_ops'
EVENT_CONTRACT = 'AppGen-X'

BASE_REQUIRED_FIELDS = (
    'instrument_id',
    'trading_account',
    'desk',
    'trader',
    'book',
    'broker',
    'venue',
    'settlement_model',
    'regulatory_classification',
    'side',
    'quantity',
    'submitted_at',
)

BOOKING_PROFILE_REQUIRED_FIELDS = {
    'equity': ('limit_price',),
    'fixed_income': ('price', 'principal_amount'),
    'fx': ('buy_currency', 'sell_currency', 'currency_pair'),
    'listed_derivative': ('contract_code', 'expiry_month'),
}

DEFAULT_ALLOWED_SETTLEMENT_MODELS = ('DVP', 'FOP', 'CCP')
DEFAULT_DUPLICATE_WINDOW_MINUTES = 15
DEFAULT_MAX_QUANTITY = 250000.0
DEFAULT_RISK_THRESHOLD = 10000000.0
DEFAULT_MATERIALITY_THRESHOLD = 1000000.0
OPEN_ORDER_STATUSES = ('draft', 'validated', 'risk_passed', 'release_blocked', 'routed', 'partially_filled')


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _as_tuple(value) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(sorted(value))
    return (value,)


def _number(value) -> float | None:
    if value in (None, ''):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _missing(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (tuple, list, set, dict)):
        return len(value) == 0
    return False


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if normalized.endswith('Z'):
        normalized = normalized[:-1] + '+00:00'
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _signature(payload: dict) -> str:
    signature_fields = (
        payload.get('tenant', 'default'),
        payload.get('instrument_id'),
        payload.get('trading_account'),
        payload.get('book'),
        payload.get('broker'),
        payload.get('venue'),
        payload.get('side'),
        payload.get('quantity'),
        payload.get('limit_price'),
    )
    return _digest(signature_fields)


def _ruleset_value(rules: dict, name: str, default):
    rule = rules.get('trade_order_policy', rules)
    if isinstance(rule, dict) and name in rule:
        return rule[name]
    return rules.get(name, default)


def required_fields_for_profile(product_type: str) -> tuple[str, ...]:
    profile = (product_type or 'equity').strip().lower()
    return BASE_REQUIRED_FIELDS + BOOKING_PROFILE_REQUIRED_FIELDS.get(profile, ())


def evaluate_trade_order_intake(payload: dict | None, existing_records=(), parameters=None, rules=None) -> dict:
    payload = dict(payload or {})
    parameters = dict(parameters or {})
    rules = dict(rules or {})

    product_type = str(payload.get('product_type', 'equity')).strip().lower() or 'equity'
    required_fields = required_fields_for_profile(product_type)
    missing_fields = tuple(field for field in required_fields if _missing(payload.get(field)))
    invalid_fields = []

    side = str(payload.get('side', '')).strip().upper()
    if side and side not in ('BUY', 'SELL'):
        invalid_fields.append('side')

    quantity = _number(payload.get('quantity'))
    if quantity is None or quantity <= 0:
        invalid_fields.append('quantity')

    price = _number(payload.get('limit_price'))
    if product_type == 'equity' and (price is None or price <= 0):
        invalid_fields.append('limit_price')

    settlement_model = str(payload.get('settlement_model', '')).strip().upper()
    allowed_settlement_models = tuple(
        str(model).strip().upper()
        for model in _as_tuple(_ruleset_value(rules, 'allowed_settlement_models', DEFAULT_ALLOWED_SETTLEMENT_MODELS))
        if str(model).strip()
    ) or DEFAULT_ALLOWED_SETTLEMENT_MODELS

    reference_data_failures = []
    if settlement_model and settlement_model not in allowed_settlement_models:
        reference_data_failures.append(
            {
                'gate': 'settlement_model_allowed',
                'reason': 'unsupported_settlement_model',
                'value': settlement_model,
                'allowed_values': allowed_settlement_models,
            }
        )

    submitted_at = _parse_timestamp(payload.get('submitted_at'))
    if payload.get('submitted_at') and submitted_at is None:
        reference_data_failures.append(
            {'gate': 'submitted_at_format', 'reason': 'invalid_timestamp', 'value': payload.get('submitted_at')}
        )

    notional = _number(payload.get('notional'))
    if notional is None and quantity is not None and price is not None:
        notional = round(quantity * price, 2)

    risk_threshold = _number(parameters.get('risk_threshold')) or DEFAULT_RISK_THRESHOLD
    materiality_threshold = _number(parameters.get('materiality_threshold')) or DEFAULT_MATERIALITY_THRESHOLD
    max_quantity = _number(_ruleset_value(rules, 'max_quantity', DEFAULT_MAX_QUANTITY)) or DEFAULT_MAX_QUANTITY
    duplicate_window_minutes = int(
        _number(_ruleset_value(rules, 'duplicate_window_minutes', DEFAULT_DUPLICATE_WINDOW_MINUTES))
        or DEFAULT_DUPLICATE_WINDOW_MINUTES
    )

    restricted_books = {
        str(value).strip()
        for value in _as_tuple(_ruleset_value(rules, 'restricted_books', ()))
        if str(value).strip()
    }
    blocked_counterparties = {
        str(value).strip()
        for value in _as_tuple(_ruleset_value(rules, 'blocked_counterparties', ()))
        if str(value).strip()
    }

    duplicate_matches = []
    signature = _signature(payload)
    for record in existing_records:
        record_payload = dict(record.get('payload', record))
        if record.get('status') not in OPEN_ORDER_STATUSES:
            continue
        if signature != record.get('trade_order_signature', _signature(record_payload)):
            continue
        record_submitted_at = _parse_timestamp(record_payload.get('submitted_at'))
        if submitted_at and record_submitted_at:
            gap_seconds = abs((submitted_at - record_submitted_at).total_seconds())
            if gap_seconds > duplicate_window_minutes * 60:
                continue
        duplicate_matches.append({'id': record.get('id'), 'status': record.get('status')})

    risk_gate_failures = []
    if quantity is not None and quantity > max_quantity:
        risk_gate_failures.append(
            {
                'gate': 'quantity_threshold',
                'reason': 'quantity_exceeds_policy',
                'value': quantity,
                'threshold': max_quantity,
            }
        )

    if notional is not None and notional > risk_threshold:
        risk_gate_failures.append(
            {
                'gate': 'risk_threshold',
                'reason': 'notional_exceeds_policy',
                'value': notional,
                'threshold': risk_threshold,
            }
        )

    book = str(payload.get('book', '')).strip()
    if book and book in restricted_books:
        risk_gate_failures.append(
            {'gate': 'restricted_book', 'reason': 'book_is_restricted', 'value': book}
        )

    broker = str(payload.get('broker', '')).strip()
    counterparty = str(payload.get('counterparty', broker)).strip()
    if counterparty and counterparty in blocked_counterparties:
        risk_gate_failures.append(
            {
                'gate': 'blocked_counterparty',
                'reason': 'counterparty_is_blocked',
                'value': counterparty,
            }
        )

    if duplicate_matches:
        risk_gate_failures.append(
            {
                'gate': 'duplicate_instruction_window',
                'reason': 'duplicate_instruction_detected',
                'matches': tuple(duplicate_matches),
                'window_minutes': duplicate_window_minutes,
            }
        )

    requires_four_eyes = bool(notional is not None and notional >= materiality_threshold)
    approval_state = str(payload.get('approval_state', 'pending')).strip().lower()
    if requires_four_eyes and approval_state != 'approved':
        risk_gate_failures.append(
            {
                'gate': 'four_eyes_approval',
                'reason': 'approval_required_before_release',
                'approval_state': approval_state or 'pending',
                'threshold': materiality_threshold,
            }
        )

    reference_data_ok = not missing_fields and not invalid_fields and not reference_data_failures
    risk_ok = reference_data_ok and not risk_gate_failures

    if not reference_data_ok:
        lifecycle_state = 'draft'
        status = 'release_blocked'
        status_badge = 'Draft'
    elif risk_ok:
        lifecycle_state = 'risk_passed'
        status = 'risk_passed'
        status_badge = 'Risk Passed'
    else:
        lifecycle_state = 'validated'
        status = 'release_blocked'
        status_badge = 'Release Blocked'

    actionable_remediation = tuple(
        [f'Populate missing field: {field}' for field in missing_fields]
        + [f'Correct invalid field: {field}' for field in invalid_fields]
        + [f'Resolve reference-data gate: {item["gate"]}' for item in reference_data_failures]
        + [f'Clear risk gate: {item["gate"]}' for item in risk_gate_failures]
    )

    return {
        'ok': True,
        'product_type': product_type,
        'required_fields': required_fields,
        'missing_fields': missing_fields,
        'invalid_fields': tuple(invalid_fields),
        'reference_data_failures': tuple(reference_data_failures),
        'risk_gate_failures': tuple(risk_gate_failures),
        'reference_data_ok': reference_data_ok,
        'risk_ok': risk_ok,
        'release_ready': risk_ok,
        'lifecycle_state': lifecycle_state,
        'status': status,
        'status_badge': status_badge,
        'notional': notional,
        'requires_four_eyes_approval': requires_four_eyes,
        'approval_state': approval_state or 'pending',
        'trade_order_signature': signature,
        'duplicate_matches': tuple(duplicate_matches),
        'actionable_remediation': actionable_remediation,
        'workbench_queue': 'ready_for_release' if risk_ok else 'trade_order_exceptions',
        'event_contract': EVENT_CONTRACT,
        'stream_engine_picker_visible': False,
        'shared_table_access': False,
        'side_effects': (),
    }


def build_trade_order_record(payload: dict | None, validation: dict, record_id: str, version: int = 1) -> dict:
    payload = dict(payload or {})
    return {
        'id': record_id,
        'tenant': payload.get('tenant', 'default'),
        'status': validation['status'],
        'status_badge': validation['status_badge'],
        'lifecycle_state': validation['lifecycle_state'],
        'version': version,
        'trade_order_signature': validation['trade_order_signature'],
        'payload': payload,
        'validation': validation,
        'actionable_remediation': validation['actionable_remediation'],
        'workbench_queue': validation['workbench_queue'],
        'release_ready': validation['release_ready'],
    }


def build_trade_order_summary(records) -> dict:
    records = tuple(records)
    blocked = tuple(record for record in records if record.get('status') == 'release_blocked')
    ready = tuple(record for record in records if record.get('status') == 'risk_passed')
    draft = tuple(record for record in records if record.get('lifecycle_state') == 'draft')
    return {
        'total_records': len(records),
        'blocked_orders': len(blocked),
        'ready_for_release': len(ready),
        'draft_orders': len(draft),
        'top_blocked_order_ids': tuple(record['id'] for record in blocked[:5]),
    }
