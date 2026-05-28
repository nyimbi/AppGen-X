"""Executable sealing, proof, and disclosure logic for the audit_ledger PBC."""

from __future__ import annotations

import hashlib
import json
from typing import Any


CANONICALIZATION_PROFILE = "appgen.audit-ledger.canonical-json.v1"
REQUIRED_EVENT_FIELDS = (
    "audit_id",
    "tenant",
    "source_pbc",
    "aggregate_id",
    "actor",
    "action",
    "classification",
    "payload",
)
MINIMAL_DISCLOSURE_FIELDS = (
    "audit_id",
    "tenant",
    "source_pbc",
    "aggregate_id",
    "sequence",
    "classification",
    "payload_hash",
    "event_hash",
)
SENSITIVE_DISCLOSURE_FIELDS = {
    "payload",
    "canonical_payload",
    "signature",
    "signature_algorithm",
    "correction_reason",
    "correction_authority",
}
IMMUTABLE_CORRECTION_FIELDS = frozenset(
    {
        "audit_id",
        "tenant",
        "source_pbc",
        "aggregate_id",
        "sequence",
        "previous_hash",
        "event_hash",
        "payload_hash",
        "signature",
        "sealed",
    }
)


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if isinstance(value, set):
        return [_normalize(item) for item in sorted(value, key=lambda item: json.dumps(_normalize(item), sort_keys=True, default=str))]
    return value


def canonicalize_payload(payload: dict | None, *, disclosed_fields: tuple[str, ...] | None = None) -> dict:
    """Canonicalize a payload deterministically for stable hashing and proof views."""
    data = dict(payload or {})
    if disclosed_fields is not None:
        allowed = set(disclosed_fields)
        data = {key: value for key, value in data.items() if key in allowed}
    normalized = _normalize(data)
    serialized = json.dumps(normalized, sort_keys=True, separators=(",", ":"), default=str)
    return {
        "ok": True,
        "profile": CANONICALIZATION_PROFILE,
        "normalized": normalized,
        "serialized": serialized,
        "side_effects": (),
    }


def payload_digest(payload: dict | None, *, disclosed_fields: tuple[str, ...] | None = None) -> dict:
    """Return a deterministic digest for a canonicalized payload view."""
    canonical = canonicalize_payload(payload, disclosed_fields=disclosed_fields)
    digest = hashlib.sha256(canonical["serialized"].encode("utf-8")).hexdigest()
    return {
        "ok": True,
        "profile": canonical["profile"],
        "canonical_payload": canonical["normalized"],
        "serialized": canonical["serialized"],
        "hash": digest,
        "side_effects": (),
    }


def _correction_metadata(audit_event: dict) -> dict | None:
    correction_of = audit_event.get("correction_of")
    if not correction_of:
        return None
    corrected_fields = tuple(sorted(set(audit_event.get("corrected_fields", ()))))
    reason = audit_event.get("correction_reason")
    authority = audit_event.get("correction_authority")
    allowed_fields = tuple(field for field in corrected_fields if field not in IMMUTABLE_CORRECTION_FIELDS)
    immutable_attempts = tuple(field for field in corrected_fields if field in IMMUTABLE_CORRECTION_FIELDS)
    valid = bool(reason and authority and allowed_fields and not immutable_attempts)
    return {
        "correction_of": correction_of,
        "corrected_fields": allowed_fields,
        "reason": reason,
        "authority": authority,
        "immutable_field_attempts": immutable_attempts,
        "verified": valid,
    }


def plan_correction_event(original_event: dict, corrected_fields: dict, *, reason: str, authority: str) -> dict:
    """Plan an immutable correction that links to a prior sealed event."""
    original_audit_id = original_event.get("audit_id")
    candidate_fields = tuple(sorted(corrected_fields))
    correction = _correction_metadata(
        {
            "correction_of": original_audit_id,
            "corrected_fields": candidate_fields,
            "correction_reason": reason,
            "correction_authority": authority,
        }
    )
    if not original_audit_id:
        return {"ok": False, "reason": "unknown_original_event", "side_effects": ()}
    if correction is None or correction["verified"] is not True:
        return {
            "ok": False,
            "reason": "invalid_correction_metadata",
            "original_audit_id": original_audit_id,
            "correction": correction,
            "side_effects": (),
        }
    return {
        "ok": True,
        "original_audit_id": original_audit_id,
        "correction": correction,
        "corrected_values": {key: corrected_fields[key] for key in correction["corrected_fields"]},
        "side_effects": (),
    }


def build_evidence_envelope(
    audit_event: dict,
    *,
    sequence: int,
    previous_hash: str,
    allowed_classifications: tuple[str, ...] = (),
) -> dict:
    """Validate and enrich a sealable audit-event envelope."""
    missing_fields = tuple(sorted(field for field in REQUIRED_EVENT_FIELDS if field not in audit_event))
    classification = audit_event.get("classification")
    classification_allowed = not allowed_classifications or classification in set(allowed_classifications)
    payload_proof = payload_digest(audit_event.get("payload"))
    occurred_at = audit_event.get("occurred_at") or audit_event.get("recorded_at") or f"recorded-sequence-{sequence:06d}"
    timestamp_basis = audit_event.get("timestamp_basis") or ("occurred_at" if audit_event.get("occurred_at") else "recorded_at")
    derived_fields = []
    if "occurred_at" not in audit_event and "recorded_at" not in audit_event:
        derived_fields.append("occurred_at")
    if "timestamp_basis" not in audit_event:
        derived_fields.append("timestamp_basis")
    causality = dict(audit_event.get("causality") or {})
    if not causality:
        derived_fields.append("causality")
    causality.setdefault("correlation_id", audit_event.get("correlation_id") or f"{audit_event.get('source_pbc', 'unknown')}:{audit_event.get('aggregate_id', 'unknown')}")
    causality.setdefault("caused_by", audit_event.get("caused_by") or audit_event.get("correction_of") or previous_hash)
    causality.setdefault("trace_id", audit_event.get("trace_id") or f"{audit_event.get('tenant', 'unknown')}:{audit_event.get('audit_id', 'unknown')}")
    correction = _correction_metadata(audit_event)
    if correction is not None and "correction_of" in audit_event:
        derived_fields.append("correction")
    inadmissibility_reasons = []
    if missing_fields:
        inadmissibility_reasons.append("missing_required_fields")
    if not classification_allowed:
        inadmissibility_reasons.append("classification_not_allowed")
    if correction is not None and correction["verified"] is not True:
        inadmissibility_reasons.append("invalid_correction_metadata")
    admissible = not inadmissibility_reasons
    envelope = {
        "audit_id": audit_event.get("audit_id"),
        "tenant": audit_event.get("tenant"),
        "source_pbc": audit_event.get("source_pbc"),
        "aggregate_id": audit_event.get("aggregate_id"),
        "actor": audit_event.get("actor"),
        "action": audit_event.get("action"),
        "classification": classification,
        "timestamp_basis": timestamp_basis,
        "occurred_at": occurred_at,
        "payload_hash": payload_proof["hash"],
        "canonicalization_profile": payload_proof["profile"],
        "canonical_payload": payload_proof["canonical_payload"],
        "causality": causality,
        "previous_hash": previous_hash,
        "sequence": sequence,
        "correction": correction,
    }
    return {
        "ok": admissible,
        "envelope": envelope,
        "missing_fields": missing_fields,
        "classification_allowed": classification_allowed,
        "admissible": admissible,
        "inadmissibility_reasons": tuple(inadmissibility_reasons),
        "derived_fields": tuple(derived_fields),
        "payload_proof": payload_proof,
        "side_effects": (),
    }


def seal_audit_event(
    audit_event: dict,
    *,
    sequence: int,
    previous_hash: str,
    allowed_classifications: tuple[str, ...] = (),
    signature_algorithm: str = "dilithium3_simulated",
) -> dict:
    """Seal a validated event using canonical payload hashing and deterministic signatures."""
    envelope = build_evidence_envelope(
        audit_event,
        sequence=sequence,
        previous_hash=previous_hash,
        allowed_classifications=allowed_classifications,
    )
    if envelope["ok"] is not True:
        return {
            "ok": False,
            "reason": "inadmissible_evidence_envelope",
            "envelope": envelope,
            "side_effects": (),
        }
    event_hash_payload = {
        "audit_id": envelope["envelope"]["audit_id"],
        "tenant": envelope["envelope"]["tenant"],
        "sequence": sequence,
        "previous_hash": previous_hash,
        "payload_hash": envelope["envelope"]["payload_hash"],
        "occurred_at": envelope["envelope"]["occurred_at"],
        "actor": envelope["envelope"]["actor"],
        "action": envelope["envelope"]["action"],
        "classification": envelope["envelope"]["classification"],
        "causality": envelope["envelope"]["causality"],
        "correction": envelope["envelope"]["correction"],
    }
    event_hash = hashlib.sha256(json.dumps(_normalize(event_hash_payload), sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()
    signature = f"sig_{event_hash[:16]}"
    sealed_event = {
        **audit_event,
        **envelope["envelope"],
        "payload": audit_event.get("payload", {}),
        "payload_hash": envelope["payload_proof"]["hash"],
        "event_hash": event_hash,
        "signature": signature,
        "signature_algorithm": signature_algorithm,
        "sealed": True,
        "admissibility": {
            "admissible": True,
            "derived_fields": envelope["derived_fields"],
            "inadmissibility_reasons": envelope["inadmissibility_reasons"],
        },
    }
    return {
        "ok": True,
        "sealed_event": sealed_event,
        "envelope": envelope,
        "proof": {
            "sequence": sequence,
            "previous_hash": previous_hash,
            "payload_hash": sealed_event["payload_hash"],
            "event_hash": event_hash,
            "signature": signature,
            "signature_algorithm": signature_algorithm,
        },
        "side_effects": (),
    }


def sequence_integrity_proof(events: tuple[dict, ...] | list[dict], *, tenant: str) -> dict:
    """Build a per-tenant chain proof over sealed events."""
    tenant_events = [event for event in events if event.get("tenant") == tenant]
    sorted_events = sorted(tenant_events, key=lambda item: (int(item.get("sequence", 0)), str(item.get("audit_id", ""))))
    if not sorted_events:
        return {
            "ok": False,
            "tenant": tenant,
            "reason": "no_events",
            "sequence_range": (),
            "side_effects": (),
        }
    expected_sequence = 1
    previous_hash = "genesis"
    seen_sequences = set()
    gaps = []
    duplicate_sequences = []
    tampered = []
    non_monotonic_timestamps = []
    invalid_payload_digests = []
    inadmissible_events = []
    correction_links = []
    previous_timestamp = None
    for event in sorted_events:
        sequence = int(event.get("sequence", 0))
        while sequence > expected_sequence:
            gaps.append(expected_sequence)
            expected_sequence += 1
        if sequence in seen_sequences:
            duplicate_sequences.append(event.get("audit_id"))
        seen_sequences.add(sequence)
        if sequence != expected_sequence:
            gaps.append(sequence)
        expected_signature = f"sig_{str(event.get('event_hash', ''))[:16]}"
        digest = payload_digest(event.get("payload"))
        if digest["hash"] != event.get("payload_hash"):
            invalid_payload_digests.append(event.get("audit_id"))
        admissibility = event.get("admissibility", {})
        if not admissibility.get("admissible", False):
            inadmissible_events.append(event.get("audit_id"))
        if event.get("previous_hash") != previous_hash or event.get("signature") != expected_signature:
            tampered.append(event.get("audit_id"))
        timestamp = str(event.get("occurred_at"))
        if previous_timestamp is not None and timestamp < previous_timestamp:
            non_monotonic_timestamps.append(event.get("audit_id"))
        previous_timestamp = timestamp
        previous_hash = str(event.get("event_hash"))
        expected_sequence = max(expected_sequence, sequence + 1)
        correction = event.get("correction") or {}
        if correction.get("correction_of"):
            correction_links.append((correction["correction_of"], event.get("audit_id")))
    proof_hash = hashlib.sha256(
        json.dumps(
            {
                "tenant": tenant,
                "event_ids": [event.get("audit_id") for event in sorted_events],
                "previous_hash": previous_hash,
                "gaps": gaps,
                "duplicate_sequences": duplicate_sequences,
                "tampered": tampered,
                "inadmissible_events": inadmissible_events,
            },
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
    ).hexdigest()
    return {
        "ok": not gaps and not duplicate_sequences and not tampered and not non_monotonic_timestamps and not invalid_payload_digests and not inadmissible_events,
        "tenant": tenant,
        "link_count": len(sorted_events),
        "sequence_range": (sorted_events[0]["sequence"], sorted_events[-1]["sequence"]),
        "gaps": tuple(gaps),
        "duplicate_sequences": tuple(duplicate_sequences),
        "tampered": tuple(tampered),
        "non_monotonic_timestamps": tuple(non_monotonic_timestamps),
        "invalid_payload_digests": tuple(invalid_payload_digests),
        "inadmissible_events": tuple(inadmissible_events),
        "genesis_anchor_ok": sorted_events[0].get("previous_hash") == "genesis",
        "correction_links": tuple(correction_links),
        "proof_hash": proof_hash,
        "side_effects": (),
    }


def plan_disclosure_minimization(
    events: tuple[dict, ...] | list[dict],
    *,
    classification: str,
    requested_fields: tuple[str, ...],
    purpose: str,
    approval_required: bool,
) -> dict:
    """Build a minimized disclosure plan for a forensic export."""
    materialized = tuple(event for event in events if event.get("classification") == classification)
    available_fields = tuple(sorted({field for event in materialized for field in event}))
    requested = tuple(dict.fromkeys(requested_fields))
    selected = tuple(
        field
        for field in dict.fromkeys(MINIMAL_DISCLOSURE_FIELDS + requested)
        if field in available_fields or field in MINIMAL_DISCLOSURE_FIELDS
    )
    withheld = tuple(field for field in available_fields if field not in selected)
    verifier_instructions = (
        "Verify the payload hash against the canonical payload profile.",
        "Verify the event hash and sequence proof before accepting the bundle.",
        "Treat withheld sensitive fields as intentionally minimized disclosure.",
    )
    proof_coverage = {
        "event_count": len(materialized),
        "sequence_range": (
            min((event.get("sequence", 0) for event in materialized), default=0),
            max((event.get("sequence", 0) for event in materialized), default=0),
        ),
        "source_pbcs": tuple(sorted({event.get("source_pbc") for event in materialized if event.get("source_pbc")})),
        "correction_pairs": tuple(
            (
                (event.get("correction") or {}).get("correction_of"),
                event.get("audit_id"),
            )
            for event in materialized
            if (event.get("correction") or {}).get("correction_of")
        ),
    }
    risk_flags = tuple(
        flag
        for flag, enabled in (
            ("sensitive_payload_requested", any(field in SENSITIVE_DISCLOSURE_FIELDS for field in requested)),
            ("regulated_approval_required", approval_required),
            ("empty_result_set", not materialized),
        )
        if enabled
    )
    return {
        "ok": bool(materialized) and bool(selected),
        "purpose": purpose,
        "classification": classification,
        "selected_fields": selected,
        "requested_fields": requested,
        "withheld_fields": withheld,
        "approval_required": approval_required,
        "risk_flags": risk_flags,
        "proof_coverage": proof_coverage,
        "verifier_instructions": verifier_instructions,
        "side_effects": (),
    }


def build_notarization_bundle(
    state: dict,
    *,
    tenant: str,
    boundary_ok: bool,
    boundary_violations: tuple[str, ...] = (),
) -> dict:
    """Summarize release-time proof coverage for the tenant's owned ledger slice."""
    proof = sequence_integrity_proof(tuple(state.get("audit_events", {}).values()), tenant=tenant)
    configuration_digest = payload_digest(state.get("configuration", {}))
    rules_digest = payload_digest(state.get("rules", {}))
    bundle_hash = hashlib.sha256(
        json.dumps(
            {
                "tenant": tenant,
                "proof_hash": proof.get("proof_hash"),
                "configuration_digest": configuration_digest["hash"],
                "rules_digest": rules_digest["hash"],
                "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
                "boundary_violations": boundary_violations,
            },
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
    ).hexdigest()
    return {
        "ok": proof.get("ok") is True and boundary_ok and not boundary_violations,
        "tenant": tenant,
        "bundle_id": f"notarization:{tenant}:{bundle_hash[:16]}",
        "proof_hash": proof.get("proof_hash"),
        "chain_link_count": proof.get("link_count", 0),
        "configuration_digest": configuration_digest["hash"],
        "rules_digest": rules_digest["hash"],
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "release_blocking_count": len(
            tuple(
                item
                for item in state.get("control_assertions", {}).values()
                if item.get("release_blocking")
            )
        ),
        "boundary_ok": boundary_ok,
        "boundary_violations": boundary_violations,
        "proof": proof,
        "side_effects": (),
    }


def audit_ledger_proof_slice_release_evidence() -> dict:
    """Return release evidence for the executable sealing/proof slice."""
    return {
        "ok": True,
        "implemented_backlog_items": (
            "evidence_envelope_completeness_gate",
            "per_tenant_sequence_integrity_proof",
            "canonical_payload_digest_strategy",
            "disclosure_minimization_planner",
            "release_evidence_notarization_bundle",
            "immutable_audit_correction_pattern",
        ),
        "standard_domain_surfaces": (
            "audit_event_sealing",
            "signature_chain_verification",
            "forensic_export_minimization",
            "correction_lineage",
        ),
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "canonicalization_profile": CANONICALIZATION_PROFILE,
        "side_effects": (),
    }
