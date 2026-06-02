"""Executable standalone workflows for insurance underwriting."""

from __future__ import annotations


def underwriting_workflow_catalog() -> dict:
    contracts = (
        {
            "key": "SubmissionIntakeWorkflow",
            "steps": ("create_submission", "build_risk_profile", "review_rating_factor"),
            "route": "POST /app/insurance-underwriting/workflows/intake",
        },
        {
            "key": "QuoteToBindWorkflow",
            "steps": (
                "review_rating_factor",
                "generate_quote",
                "issue_underwriting_decision",
                "assemble_bind_package",
            ),
            "route": "POST /app/insurance-underwriting/workflows/quote-to-bind",
        },
    )
    return {
        "format": "appgen.insurance-underwriting-workflow-catalog.v1",
        "ok": True,
        "pbc": "insurance_underwriting",
        "contracts": contracts,
        "side_effects": (),
    }


def run_submission_intake_workflow(service, payload: dict) -> dict:
    submission = service.create_submission(payload)
    if submission["ok"] is not True:
        return {
            "ok": False,
            "workflow": "SubmissionIntakeWorkflow",
            "submission": submission,
            "side_effects": (),
        }
    risk_profile_payload = {
        "risk_profile_id": payload.get("risk_profile_id", f"{payload['submission_id']}-risk"),
        "submission_id": payload["submission_id"],
        "tenant": payload["tenant"],
        "industry_code": payload.get("industry_code", "GEN"),
        "hazard_factors": payload.get("hazard_factors", ("fire",)),
        "catastrophe_score": payload.get("catastrophe_score", 0.2),
        "prior_loss_count": payload.get("prior_loss_count", len(payload.get("prior_losses", ()))),
    }
    risk = service.build_risk_profile(risk_profile_payload)
    factor = service.review_rating_factor(
        {
            "factor_id": payload.get("factor_id", f"{payload['submission_id']}-base-rate"),
            "submission_id": payload["submission_id"],
            "tenant": payload["tenant"],
            "factor_type": "base_rate",
            "selected_value": payload.get("base_rate", 1.0),
            "weight": 0.35,
            "source": "actuarial_projection",
        }
    )
    return {
        "ok": submission["ok"] and risk["ok"] and factor["ok"],
        "workflow": "SubmissionIntakeWorkflow",
        "steps": (submission, risk, factor),
        "side_effects": (),
    }


def run_quote_to_bind_workflow(service, payload: dict) -> dict:
    quote = service.generate_quote(payload)
    if quote["ok"] is not True:
        return {
            "ok": False,
            "workflow": "QuoteToBindWorkflow",
            "quote": quote,
            "side_effects": (),
        }
    decision = service.issue_underwriting_decision(
        {
            "decision_id": payload.get("decision_id", f"{payload['submission_id']}-decision"),
            "submission_id": payload["submission_id"],
            "quote_id": quote["result"]["quote_id"],
            "tenant": payload["tenant"],
            "authority_level": payload.get("authority_level", "senior"),
            "actor_roles": payload.get("actor_roles", ("approver",)),
            "approved_by": payload.get("approved_by", "underwriter"),
        }
    )
    bind = service.assemble_bind_package(
        {
            "bind_package_id": payload.get("bind_package_id", f"{payload['submission_id']}-bind"),
            "submission_id": payload["submission_id"],
            "quote_id": quote["result"]["quote_id"],
            "tenant": payload["tenant"],
            "subjectivities": payload.get(
                "subjectivities",
                ({"name": "signed_application", "satisfied": True},),
            ),
            "documents": payload.get("documents", ("signed_application",)),
            "payment_confirmed": payload.get("payment_confirmed", True),
        }
    )
    return {
        "ok": quote["ok"] and decision["ok"] and bind["ok"],
        "workflow": "QuoteToBindWorkflow",
        "steps": (quote, decision, bind),
        "side_effects": (),
    }


def workflow_smoke_test(service_factory) -> dict:
    service = service_factory()
    try:
        intake = run_submission_intake_workflow(
            service,
            {
                "submission_id": "smoke-submission",
                "tenant": "tenant-smoke",
                "product_line": "property",
                "applicant_name": "Smoke Manufacturing",
                "jurisdiction": "US-NY",
                "requested_limit": 750000.0,
                "declared_revenue": 1800000.0,
                "exposure_locations": ("Albany",),
                "documents": ("application.pdf",),
                "prior_losses": (),
            },
        )
        bind = run_quote_to_bind_workflow(
            service,
            {
                "submission_id": "smoke-submission",
                "tenant": "tenant-smoke",
                "quote_id": "smoke-submission-quote",
                "approved_by": "chief-underwriter",
                "authority_level": "chief",
            },
        )
        return {
            "ok": underwriting_workflow_catalog()["ok"] and intake["ok"] and bind["ok"],
            "intake": intake,
            "bind": bind,
            "side_effects": (),
        }
    finally:
        service.close()
