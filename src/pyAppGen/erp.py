"""Package-level ERP starter templates for AppGen.

The generated ERP workbench is useful after app generation.  This module makes
the same ERP starting point available before generation as reusable DSL input.
"""

from __future__ import annotations


ERP_MODULES: dict[str, dict] = {
    "chart_of_accounts": {
        "label": "Chart of Accounts",
        "domain": "finance",
        "tables": {
            "ledger_account": (
                "id: int pk",
                "code: string required unique search",
                "name: string required search",
                "account_type: string required",
                "active: bool default true",
            ),
            "accounting_period": (
                "id: int pk",
                "name: string required unique search",
                "starts_on: date required",
                "ends_on: date required",
                "status: string required",
            ),
        },
        "workflows": ("account_approval",),
        "reports": ("chart_of_accounts",),
    },
    "general_ledger": {
        "label": "General Ledger",
        "domain": "finance",
        "tables": {
            "journal_entry": (
                "id: int pk",
                "entry_no: string required unique search",
                "posting_date: date required",
                "memo: text",
                "status: string required",
            ),
            "journal_line": (
                "id: int pk",
                "journal_entry_id: int required -> journal_entry.id [many-to-one]",
                "ledger_account_id: int required -> ledger_account.id [many-to-one]",
                "debit_amount: decimal default 0",
                "credit_amount: decimal default 0",
            ),
            "ledger_account": (
                "id: int pk",
                "code: string required unique search",
                "name: string required search",
            ),
        },
        "workflows": ("journal_posting",),
        "reports": ("trial_balance", "general_ledger"),
    },
    "accounts_receivable": {
        "label": "Accounts Receivable",
        "domain": "finance",
        "tables": {
            "customer": (
                "id: int pk",
                "name: string required search",
                "email: email search",
                "tax_number: string",
            ),
            "ar_invoice": (
                "id: int pk",
                "customer_id: int required -> customer.id [many-to-one]",
                "invoice_no: string required unique search",
                "invoice_date: date required",
                "total_amount: decimal required",
                "status: string required",
            ),
            "ar_payment": (
                "id: int pk",
                "ar_invoice_id: int required -> ar_invoice.id [many-to-one]",
                "payment_date: date required",
                "amount: decimal required",
                "reference: string search",
            ),
        },
        "workflows": ("receivable_collection",),
        "reports": ("aged_receivables",),
    },
    "accounts_payable": {
        "label": "Accounts Payable",
        "domain": "finance",
        "tables": {
            "vendor": (
                "id: int pk",
                "name: string required search",
                "email: email search",
                "tax_number: string",
            ),
            "ap_bill": (
                "id: int pk",
                "vendor_id: int required -> vendor.id [many-to-one]",
                "bill_no: string required unique search",
                "bill_date: date required",
                "total_amount: decimal required",
                "status: string required",
            ),
            "ap_payment": (
                "id: int pk",
                "ap_bill_id: int required -> ap_bill.id [many-to-one]",
                "payment_date: date required",
                "amount: decimal required",
                "reference: string search",
            ),
        },
        "workflows": ("payable_approval",),
        "reports": ("aged_payables",),
    },
    "invoicing": {
        "label": "Invoicing",
        "domain": "commerce",
        "tables": {
            "customer": (
                "id: int pk",
                "name: string required search",
                "email: email search",
            ),
            "product": (
                "id: int pk",
                "sku: string required unique search",
                "name: string required search",
                "unit_price: decimal required",
            ),
            "invoice": (
                "id: int pk",
                "customer_id: int required -> customer.id [many-to-one]",
                "invoice_no: string required unique search",
                "invoice_date: date required",
                "status: string required",
            ),
            "invoice_line": (
                "id: int pk",
                "invoice_id: int required -> invoice.id [many-to-one]",
                "product_id: int required -> product.id [many-to-one]",
                "quantity: decimal required",
                "unit_price: decimal required",
            ),
        },
        "workflows": ("invoice_approval",),
        "reports": ("invoice_register", "sales_by_customer"),
    },
    "inventory": {
        "label": "Inventory",
        "domain": "operations",
        "tables": {
            "item": (
                "id: int pk",
                "sku: string required unique search",
                "name: string required search",
                "reorder_point: int default 0",
            ),
            "warehouse": (
                "id: int pk",
                "code: string required unique search",
                "name: string required search",
            ),
            "stock_movement": (
                "id: int pk",
                "item_id: int required -> item.id [many-to-one]",
                "warehouse_id: int required -> warehouse.id [many-to-one]",
                "movement_date: date required",
                "quantity: decimal required",
                "movement_type: string required",
            ),
        },
        "workflows": ("stock_adjustment",),
        "reports": ("inventory_valuation", "stock_card"),
    },
    "human_resources": {
        "label": "Human Resources",
        "domain": "people",
        "tables": {
            "department": (
                "id: int pk",
                "code: string required unique search",
                "name: string required search",
            ),
            "employee": (
                "id: int pk",
                "department_id: int -> department.id [many-to-one]",
                "employee_no: string required unique search",
                "full_name: string required search",
                "email: email search",
                "hire_date: date required",
            ),
        },
        "workflows": ("employee_onboarding",),
        "reports": ("headcount",),
    },
    "payroll": {
        "label": "Payroll",
        "domain": "people",
        "tables": {
            "employee": (
                "id: int pk",
                "employee_no: string required unique search",
                "full_name: string required search",
            ),
            "payroll_run": (
                "id: int pk",
                "period_name: string required search",
                "pay_date: date required",
                "status: string required",
            ),
            "payslip": (
                "id: int pk",
                "payroll_run_id: int required -> payroll_run.id [many-to-one]",
                "employee_id: int required -> employee.id [many-to-one]",
                "gross_pay: decimal required",
                "net_pay: decimal required",
            ),
        },
        "workflows": ("payroll_approval",),
        "reports": ("payroll_summary",),
    },
    "reporting": {
        "label": "Reporting",
        "domain": "governance",
        "tables": {
            "report_definition": (
                "id: int pk",
                "name: string required unique search",
                "subject_area: string required search",
                "output_format: string required",
            ),
            "report_run": (
                "id: int pk",
                "report_definition_id: int required -> report_definition.id [many-to-one]",
                "requested_at: datetime required",
                "status: string required",
            ),
        },
        "workflows": ("report_publication",),
        "reports": ("report_catalog",),
    },
}

ERP_STACKS = {
    "finance_core": (
        "chart_of_accounts",
        "general_ledger",
        "accounts_receivable",
        "accounts_payable",
        "invoicing",
        "reporting",
    ),
    "distribution_core": (
        "inventory",
        "invoicing",
        "accounts_receivable",
        "reporting",
    ),
    "people_core": ("human_resources", "payroll", "reporting"),
    "full_erp": tuple(ERP_MODULES),
}

ERP_ALIASES = {
    "ledger": "general_ledger",
    "general-ledger": "general_ledger",
    "ar": "accounts_receivable",
    "ap": "accounts_payable",
    "invoice": "invoicing",
    "hr": "human_resources",
}


def normalize_erp_module(name: str) -> str:
    """Return the canonical ERP module name for a user-provided module."""
    key = str(name or "").strip().lower().replace(" ", "_").replace("-", "_")
    key = ERP_ALIASES.get(key.replace("_", "-"), ERP_ALIASES.get(key, key))
    if key not in ERP_MODULES:
        raise KeyError(f"Unknown ERP module: {name}")
    return key


def erp_template_catalog() -> dict:
    """Return the package-level ERP template catalog."""
    return {
        "format": "appgen.erp-template-catalog.v1",
        "modules": tuple(
            {
                "module": module,
                "label": spec["label"],
                "domain": spec["domain"],
                "tables": tuple(spec["tables"]),
                "workflows": tuple(spec["workflows"]),
                "reports": tuple(spec["reports"]),
                "command": f"appgen --erp-template {module}",
            }
            for module, spec in ERP_MODULES.items()
        ),
        "stacks": ERP_STACKS,
        "ok": {
            "general_ledger",
            "accounts_payable",
            "accounts_receivable",
            "invoicing",
            "inventory",
            "human_resources",
            "reporting",
        }
        <= set(ERP_MODULES),
    }


def _module_table_blocks(module: str) -> tuple[str, ...]:
    spec = ERP_MODULES[normalize_erp_module(module)]
    blocks = []
    for table, fields in spec["tables"].items():
        body = "\n".join(f"  {field}" for field in fields)
        blocks.append(f"table {table} {{\n{body}\n}}")
    return tuple(blocks)


def erp_module_dsl(module: str, *, app_name: str | None = None) -> str:
    """Render a self-contained AppGen DSL starter for one ERP module."""
    canonical = normalize_erp_module(module)
    name = app_name or f"{canonical.title().replace('_', '')}App"
    blocks = [f"app {name} {{ targets: web, pwa, mobile, desktop }}"]
    blocks.extend(_module_table_blocks(canonical))
    for workflow in ERP_MODULES[canonical]["workflows"]:
        blocks.append(f"flow {workflow} {{\n  draft -> review\n  review -> approved\n}}")
    return "\n\n".join(blocks) + "\n"


def normalize_erp_stack(name: str) -> str:
    """Return the canonical ERP stack name."""
    key = str(name or "").strip().lower().replace(" ", "_").replace("-", "_")
    if key not in ERP_STACKS:
        raise KeyError(f"Unknown ERP stack: {name}")
    return key


def erp_starter_manifest(
    stack: str = "finance_core",
    *,
    app_name: str = "ERPStarter",
) -> dict:
    """Return a reviewable multi-module ERP starter manifest."""
    stack_name = normalize_erp_stack(stack)
    modules = ERP_STACKS[stack_name]
    dsl_blocks = [f"app {app_name} {{ targets: web, pwa, mobile, desktop }}"]
    seen_tables = set()
    workflows = []
    reports = []
    for module in modules:
        for block in _module_table_blocks(module):
            table_name = block.split()[1]
            if table_name in seen_tables:
                continue
            seen_tables.add(table_name)
            dsl_blocks.append(block)
        workflows.extend(ERP_MODULES[module]["workflows"])
        reports.extend(ERP_MODULES[module]["reports"])
    for workflow in dict.fromkeys(workflows):
        dsl_blocks.append(
            f"flow {workflow} {{\n  draft -> review\n  review -> approved\n}}"
        )
    return {
        "format": "appgen.erp-starter.v1",
        "stack": stack_name,
        "app_name": app_name,
        "modules": modules,
        "tables": tuple(sorted(seen_tables)),
        "workflows": tuple(dict.fromkeys(workflows)),
        "reports": tuple(dict.fromkeys(reports)),
        "dsl": "\n\n".join(dsl_blocks) + "\n",
        "command": (
            f"appgen --dsl {stack_name}.appgen --writedir "
            f"apps/{app_name.lower()}"
        ),
    }


def erp_generation_smoke_audit(stack: str = "finance_core") -> dict:
    """Generate and compile an ERP starter app from package-level DSL."""
    import json
    import py_compile
    import tempfile
    from pathlib import Path

    from .gen import generate_app_from_schema
    from .schema import load_schema

    starter = erp_starter_manifest(stack, app_name="ERPGenerationSmoke")
    stack_name = starter["stack"]
    required_tables_by_stack = {
        "finance_core": (
            "ledger_account",
            "journal_entry",
            "journal_line",
            "customer",
            "ar_invoice",
            "ap_bill",
            "invoice",
            "invoice_line",
            "report_definition",
        ),
        "distribution_core": (
            "item",
            "warehouse",
            "stock_movement",
            "customer",
            "invoice",
            "invoice_line",
            "ar_invoice",
            "report_definition",
        ),
        "people_core": (
            "department",
            "employee",
            "payroll_run",
            "payslip",
            "report_definition",
        ),
        "full_erp": tuple(
            sorted({table for module in ERP_MODULES.values() for table in module["tables"]})
        ),
    }
    required_tables = required_tables_by_stack[stack_name]
    required_artifacts = (
        "app/models.py",
        "app/views.py",
        "app/erp_templates.py",
        "app/finance_ops.py",
        "app/reports.py",
        "app/report_delivery.py",
        "app/templates/appgen_erp_templates.html",
        "app/static/appgen.webmanifest",
        "native/appgen_native.py",
        "native/mobile/app.py",
        "native/mobile/pyproject.toml",
        "native/desktop/app.py",
        "native/desktop/pyproject.toml",
    )
    compile_artifacts = (
        "app/models.py",
        "app/views.py",
        "app/erp_templates.py",
        "app/finance_ops.py",
        "app/reports.py",
        "app/report_delivery.py",
        "native/appgen_native.py",
        "native/mobile/app.py",
        "native/desktop/app.py",
    )

    with tempfile.TemporaryDirectory(prefix="appgen-erp-smoke-") as tmp:
        project_dir = Path(tmp)
        dsl_path = project_dir / f"{stack_name}.appgen"
        dsl_path.write_text(starter["dsl"], encoding="utf-8")
        schema = load_schema(dsl_path, source_type="dsl")
        output_dir = project_dir / "app"
        generate_app_from_schema(schema, output_dir)

        schema_tables = tuple(sorted(table.name for table in schema.tables))
        missing_tables = tuple(
            table for table in required_tables if table not in schema_tables
        )
        missing_artifacts = tuple(
            artifact for artifact in required_artifacts if not (project_dir / artifact).exists()
        )
        compiled = []
        compile_failures = []
        for artifact in compile_artifacts:
            path = project_dir / artifact
            if not path.exists():
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"artifact": artifact, "error": str(exc)})
            else:
                compiled.append(artifact)

        manifest = json.loads((output_dir / "appgen.json").read_text(encoding="utf-8"))
        manifest_tables = tuple(sorted(table["name"] for table in manifest["tables"]))
        manifest_missing = tuple(
            table for table in required_tables if table not in manifest_tables
        )

    checks = (
        {
            "id": "starter_dsl_parse",
            "ok": not missing_tables,
            "required_tables": required_tables,
            "schema_tables": schema_tables,
            "missing": missing_tables,
        },
        {
            "id": "generated_artifacts",
            "ok": not missing_artifacts,
            "required_artifacts": required_artifacts,
            "missing": missing_artifacts,
        },
        {
            "id": "generated_python_compiles",
            "ok": not compile_failures and set(compiled) == set(compile_artifacts),
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "manifest_table_coverage",
            "ok": not manifest_missing,
            "manifest_tables": manifest_tables,
            "missing": manifest_missing,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.erp-generation-smoke-audit.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "stack": stack_name,
        "starter": {
            "format": starter["format"],
            "modules": starter["modules"],
            "tables": starter["tables"],
            "workflows": starter["workflows"],
            "reports": starter["reports"],
        },
        "schema_tables": schema_tables,
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def erp_template_release_audit() -> dict:
    """Return package-level release evidence for ERP starter templates."""
    catalog = erp_template_catalog()
    required = (
        "chart_of_accounts",
        "general_ledger",
        "accounts_receivable",
        "accounts_payable",
        "invoicing",
        "inventory",
        "human_resources",
        "payroll",
        "reporting",
    )
    module_names = {module["module"] for module in catalog["modules"]}
    finance = erp_starter_manifest("finance_core")
    generation_smoke = erp_generation_smoke_audit("finance_core")
    gates = (
        {
            "id": "required_modules",
            "ok": set(required) <= module_names,
            "required": required,
        },
        {
            "id": "finance_stack",
            "ok": {"ledger_account", "journal_entry", "invoice", "ap_bill", "ar_invoice"}
            <= set(finance["tables"]),
            "tables": finance["tables"],
        },
        {
            "id": "dsl_export",
            "ok": "app ERPStarter" in finance["dsl"]
            and "table ledger_account" in finance["dsl"],
        },
        {
            "id": "generation_command",
            "ok": finance["command"].startswith("appgen --dsl "),
        },
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.erp-template-release-audit.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "catalog": catalog,
        "starter": finance,
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }
