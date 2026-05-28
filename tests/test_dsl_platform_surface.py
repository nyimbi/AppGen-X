from pyAppGen.dsl import dsl_antlr_integrity_report
from pyAppGen.dsl import lint_dsl
from pyAppGen.dsl import schema_from_dsl


def test_dsl_accepts_pbc_composition_operations_security_surface() -> None:
    source = """
    app EnterpriseCore { targets: web, mobile, desktop }
    table Journal { id: int pk; status: string required search }
    flow PostJournal { draft -> posted }
    rule PostingPolicy for Journal {
      status in draft, posted
      status == posted -> AuditReview
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
    version Release2026 { semver: "1.0.0"; compatibility: backward }
    operation CloseBooks {
      draft -> reviewed
      reviewed -> posted
      owner: finance_ops
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
    assert report["summary"]["platform_blocks"] == 7

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
    assert dsl_antlr_integrity_report()["ok"] is True
