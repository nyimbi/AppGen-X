from pyAppGen.dsl import dsl_antlr_integrity_report
from pyAppGen.dsl import lint_dsl
from pyAppGen.dsl import schema_from_dsl


def test_dsl_accepts_pbc_composition_operations_security_surface() -> None:
    source = """
    app EnterpriseCore { targets: web, mobile, desktop }
    table Customer { id: int pk; name: string required search }
    table Journal {
      id: int pk
      status: string required search
      customer_id: int -> Customer.id [many-to-one]
      unique journal_customer_status (customer_id, status)
      lookup customer_name (customer.name)
      fk journal_customer_fk (customer_id) -> Customer.id
    }
    view JournalForm for Journal {
      Main: status, customer.name
      @ customer.name TextBox 0 1 6 1
      on Save -> PostJournal
    }
    flow PostJournal {
      participant FinanceOps
      draft -> posted
      human Review assigned FinanceOps -> reviewed
      timer reviewed "P2D" -> escalated
      compensate posted -> ReverseJournal
    }
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
      resource gl_core cpu "500m"
      env gl_core DATABASE_URL
      secret gl_core OPENAI_API_KEY
    }
    version Release2026 { semver: "1.0.0"; compatibility: backward }
    operation CloseBooks {
      draft -> reviewed
      reviewed -> posted
      human Review assigned FinanceOps -> reviewed
      compensate posted -> ReverseJournal
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
      skill reconcile JournalPosted -> CloseBooks
      Journal: read
      on Alert -> CloseBooks
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
    assert [statement.verb for statement in service_deploy.statements] == ["resource", "env", "secret"]
    journal = schema.table("Journal")
    assert [directive.verb for directive in journal.directives] == ["unique", "lookup", "fk"]
    assert schema.views[0].fields == ("status", "customer.name")
    assert schema.views[0].components[0].field == "customer.name"
    assert [directive.verb for directive in schema.flows[0].directives] == [
        "participant",
        "human",
        "timer",
        "compensate",
    ]
    assert schema.agents[0].competencies[0].verb == "skill"
    assert schema.agents[0].permissions[0].resource == "Journal"
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


def test_dsl_rejects_invalid_table_directives_and_lookup_paths() -> None:
    source = """
    app BadLookups { targets: web }
    table Customer { id: int pk; name: string }
    table Invoice {
      id: int pk
      customer_id: int -> Customer.id
      lookup bad_customer (customer.missing_name)
      index bad_index (missing_field)
      fk bad_fk (customer_id) -> Customer.missing_id
    }
    view InvoiceForm for Invoice {
      Main: customer.missing_name
      @ customer.missing_name TextBox 0 0 6 1
    }
    """

    report = lint_dsl(source)
    assert report["ok"] is False
    assert any("Unknown table directive field: Invoice.lookup.customer.missing_name" in error for error in report["errors"])
    assert any("Unknown table directive field: Invoice.index.missing_field" in error for error in report["errors"])
    assert any("Unknown table directive target: Invoice.fk.Customer.missing_id" in error for error in report["errors"])
    assert any("Unresolved lookup path: InvoiceForm.customer.missing_name" in error for error in report["errors"])
