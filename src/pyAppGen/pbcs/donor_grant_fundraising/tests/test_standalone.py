from pyAppGen.pbcs.donor_grant_fundraising.standalone import DonorGrantFundraisingStandaloneApplication, standalone_manifest, standalone_smoke_test


def test_standalone_manifest_declares_one_pbc_operating_shell():
    manifest = standalone_manifest()

    assert manifest["ok"] is True
    assert manifest["app_class"] == "DonorGrantFundraisingStandaloneApplication"
    assert "seed_demo_data" in manifest["service_methods"]
    assert manifest["allowed_backends"] == ("postgresql", "mysql", "mariadb")


def test_standalone_application_bootstraps_defaults_and_operating_records():
    app = DonorGrantFundraisingStandaloneApplication(tenant="tenant_zeta")

    configured = app.configure()
    defaults = app.register_defaults()
    seeds = app.seed_demo_data()
    workbench = app.workbench(tenant="tenant_zeta")

    assert configured["ok"] is True
    assert defaults["ok"] is True
    assert len(defaults["parameters"]) >= 6
    assert seeds["ok"] is True
    assert workbench["ok"] is True
    assert workbench["queue_counts"]["portfolio_next_actions"] == 1


def test_standalone_application_runs_grant_review_budget_and_document_flow():
    app = DonorGrantFundraisingStandaloneApplication(tenant="tenant_zeta")
    app.configure()
    app.register_defaults()
    app.seed_demo_data()

    pledge = app.create_pledge({
        "pledge_id": "pledge-zeta",
        "donor_id": "seed-foundation",
        "campaign_id": "seed-campaign",
        "amount": 12000,
        "installments": ({"amount": 6000}, {"amount": 6000}),
    })
    gift = app.post_gift({
        "gift_id": "gift-zeta",
        "donor_id": "seed-foundation",
        "campaign_id": "seed-campaign",
        "pledge_id": "pledge-zeta",
        "restriction_id": "seed-restriction",
        "purpose_code": "education",
        "amount": 6000,
    })
    grant = app.manage_grant_application({
        "grant_application_id": "grant-zeta",
        "funder_id": "seed-foundation",
        "stage": "submitted",
        "proposal_complete": True,
        "review_signoffs": ("program", "finance"),
        "budget": {"purpose_code": "education", "line_items": ({"amount": 8000}, {"amount": 4000})},
    })
    review = app.manage_review_chain({
        "entity_type": "grant_application",
        "entity_id": "grant-zeta",
        "required_roles": ("program", "finance"),
        "completed_roles": ("program", "finance"),
        "status": "approved",
    })
    validation = app.validate_grant_budget({
        "grant_application_id": "grant-zeta",
        "restriction_id": "seed-restriction",
        "approvals": ("finance",),
        "period": "fy26",
    })
    document = app.document_intake("education grant proposal", "prepare review checklist")
    crud = app.crud_mutation_plan(action_name="create", table="donor_grant_fundraising_acknowledgement", payload={"gift_id": "gift-zeta"})

    assert pledge["ok"] is True
    assert gift["ok"] is True
    assert grant["ok"] is True
    assert review["ok"] is True
    assert validation["budget_validation"]["status"] == "passed"
    assert document["plan"]["domain_plan"]["target_table"] == "donor_grant_fundraising_review_chain"
    assert crud["ok"] is True


def test_standalone_smoke_test_passes():
    assert standalone_smoke_test()["ok"] is True
