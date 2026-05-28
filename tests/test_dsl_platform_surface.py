from pyAppGen.dsl import dsl_antlr_integrity_report
from pyAppGen.dsl import lint_dsl
from pyAppGen.dsl import schema_from_dsl


def test_dsl_accepts_pbc_composition_operations_security_surface() -> None:
    source = """
    app EnterpriseCore { targets: web, mobile, desktop }
    table Journal { id: int pk; status: string required search }
    view JournalForm for Journal {
      Main: status
      on Save -> PostJournal
    }
    flow PostJournal { draft -> posted }
    rule PostingPolicy for Journal {
      status in draft, posted
      status == posted and id > 0 -> AuditReview
    }
    pbc gl_core {
      label: "General Ledger Core"
      mesh: finops
      owns: journal_entry, account
      emits: JournalPosted
      consumes: InvoiceApproved
    }
    composition EnterpriseCoreMesh {
      include pbc gl_core version "1.x"
      require datastore owned_per_pbc
      require eventing appgen_x_outbox
      expose workbench all
      expose assistant FinanceAssistant
      connect gl_core emits JournalPosted -> gl_core consumes InvoiceApproved
    }
    audit ReleaseAudit { evidence: migrations, tests, "security"; gate: release }
    deploy Production { target: kubernetes; strategy: rolling }
    deploy Services {
      runtime: kubernetes
      mesh: mtls
      unit gl_core as microservice
      unit CloseBooks as process
      unit NightlyClose as worker
      scale gl_core min 2 max 10
      health gl_core "/healthz"
      check gl_core readiness "/readyz"
    }
    version Release2026 { semver: "1.0.0"; compatibility: backward }
    operation CloseBooks {
      draft -> reviewed
      reviewed -> posted
      owner: finance_ops
    }
    api JournalsApi {
      GET "/journals" -> PostJournal
      auth: Journal.read
    }
    event JournalPosted {
      publish JournalPosted -> PostJournal
      topic: pbc.gl_core.events
    }
    job NightlyClose {
      daily -> CloseBooks
      retry: 3
    }
    report TrialBalance {
      source: Journal
      export: csv, pdf
    }
    menu MainMenu {
      on Open -> PostJournal
    }
    component StatusBadge {
      on Click -> PostJournal
      prop: status
    }
    package DesktopMobileWeb {
      targets: web, mobile, desktop
      channel: stable
    }
    test JournalSmoke {
      run happy_path -> PostJournal
      assert: ok
    }
    security TenantPolicy {
      Journal: read, create, update
      rbac: enabled
    }
    llm LocalModel { provider: ollama; mode: local; model: qwen3_4b }
    agent FinanceAssistant {
      provider: LocalModel
      goal: "Guide finance work"
      tools: gl_core_skills, schema, forms
    }
    """

    report = lint_dsl(source)
    assert report["ok"] is True
    assert report["summary"]["platform_blocks"] == 8
    assert report["summary"]["enterprise_contracts"] == 8

    schema = schema_from_dsl(source)
    assert {block.kind for block in schema.platform_blocks} == {
        "pbc",
        "composition",
        "audit",
        "deploy",
        "version",
        "operation",
        "security",
    }
    service_deploy = next(block for block in schema.platform_blocks if block.name == "Services")
    assert [unit.pattern for unit in service_deploy.deployment_units] == [
        "microservice",
        "process",
        "worker",
    ]
    assert service_deploy.deployment_scales[0].maximum == 10
    assert service_deploy.deployment_health[1].kind == "readiness"
    assert len(schema.api_contracts) == 1
    assert len(schema.event_contracts) == 1
    assert len(schema.job_contracts) == 1
    assert len(schema.report_contracts) == 1
    assert len(schema.menu_contracts) == 1
    assert len(schema.component_contracts) == 1
    assert len(schema.package_contracts) == 1
    assert len(schema.test_contracts) == 1
    assert schema.views[0].handlers[0].target == "PostJournal"
    assert dsl_antlr_integrity_report()["ok"] is True


def test_dsl_rejects_unknown_enterprise_contract_references() -> None:
    source = """
    app BadEnterprise { targets: web }
    table Journal { id: int pk; status: string }
    api BadApi { GET "/journals" -> MissingOperation }
    package BadPackage { targets: toaster }
    """

    report = lint_dsl(source)
    assert report["ok"] is False
    assert any("Unknown contract target: BadApi.MissingOperation" in error for error in report["errors"])
    assert any("Unknown package target: BadPackage.toaster" in error for error in report["errors"])


def test_dsl_rejects_invalid_deployment_topology() -> None:
    source = """
    app BadDeploy { targets: web }
    table Journal { id: int pk; status: string }
    pbc gl_core { owns: Journal }
    deploy Production {
      unit missing_pbc as microservice
      unit gl_core as spaceship
      scale gl_core min 5 max 2
      health missing_pbc "/healthz"
    }
    """

    report = lint_dsl(source)
    assert report["ok"] is False
    assert any("Unknown deployment unit target: Production.missing_pbc" in error for error in report["errors"])
    assert any("Unknown deployment pattern: Production.spaceship" in error for error in report["errors"])
    assert any("Invalid deployment scale range: Production.gl_core" in error for error in report["errors"])
    assert any("Unknown deployment health target: Production.missing_pbc" in error for error in report["errors"])
