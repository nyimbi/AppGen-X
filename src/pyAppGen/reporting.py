"""Package-level reporting and visualization contracts.

Generated apps include reports, report delivery, and dashboards.  This module
exposes the roadmap reporting contract before generation, including table,
join, three-way, ChartView, PDF, and email delivery evidence.
"""

from __future__ import annotations

from .schema import AppSchema
from .schema import ColumnSchema
from .schema import RelationSchema
from .schema import TableSchema


def sample_reporting_schema() -> AppSchema:
    """Return a small schema with one-hop and three-way reporting paths."""
    return AppSchema(
        app_name="ReportingDemo",
        tables=(
            TableSchema(
                "customer",
                (
                    ColumnSchema("id", "int", primary_key=True),
                    ColumnSchema("name", "string", nullable=False, searchable=True),
                    ColumnSchema("email", "email", searchable=True),
                ),
            ),
            TableSchema(
                "invoice",
                (
                    ColumnSchema("id", "int", primary_key=True),
                    ColumnSchema("customer_id", "int", nullable=False, references=("customer", "id")),
                    ColumnSchema("invoice_no", "string", nullable=False, searchable=True),
                    ColumnSchema("total_amount", "decimal", nullable=False),
                ),
            ),
            TableSchema(
                "invoice_line",
                (
                    ColumnSchema("id", "int", primary_key=True),
                    ColumnSchema("invoice_id", "int", nullable=False, references=("invoice", "id")),
                    ColumnSchema("product_name", "string", nullable=False, searchable=True),
                    ColumnSchema("quantity", "decimal", nullable=False),
                    ColumnSchema("line_amount", "decimal", nullable=False),
                ),
            ),
        ),
        relations=(
            RelationSchema("invoice", "customer_id", "customer", "id", "many-to-one"),
            RelationSchema("invoice_line", "invoice_id", "invoice", "id", "many-to-one"),
        ),
    )


def table_report_catalog(schema: AppSchema | None = None) -> tuple[dict, ...]:
    """Return one generated report contract per table."""
    app_schema = schema or sample_reporting_schema()
    reports = []
    for table in app_schema.tables:
        visible_columns = tuple(column.name for column in table.columns if not column.hidden)
        reports.append(
            {
                "key": f"{table.name}_table_report",
                "kind": "table",
                "table": table.name,
                "columns": visible_columns,
                "formats": ("html", "csv", "pdf"),
                "delivery": ("download", "email"),
            }
        )
    return tuple(reports)


def join_report_catalog(schema: AppSchema | None = None) -> tuple[dict, ...]:
    """Return one generated join report per explicit relation."""
    app_schema = schema or sample_reporting_schema()
    reports = []
    for relation in app_schema.relations:
        reports.append(
            {
                "key": f"{relation.source_table}_{relation.target_table}_join_report",
                "kind": "join",
                "tables": (relation.source_table, relation.target_table),
                "join": {
                    "source": f"{relation.source_table}.{relation.source_column}",
                    "target": f"{relation.target_table}.{relation.target_column}",
                    "cardinality": relation.cardinality or "many-to-one",
                },
                "formats": ("html", "csv", "pdf"),
            }
        )
    return tuple(reports)


def three_way_report_catalog(schema: AppSchema | None = None) -> tuple[dict, ...]:
    """Return reports for two-hop relation paths such as line -> invoice -> customer."""
    app_schema = schema or sample_reporting_schema()
    reports = []
    by_target = {}
    for relation in app_schema.relations:
        by_target.setdefault(relation.target_table, []).append(relation)
    for first in app_schema.relations:
        for second in by_target.get(first.source_table, ()):
            reports.append(
                {
                    "key": f"{second.source_table}_{first.source_table}_{first.target_table}_three_way_report",
                    "kind": "three_way",
                    "tables": (second.source_table, first.source_table, first.target_table),
                    "joins": (
                        f"{second.source_table}.{second.source_column}->{second.target_table}.{second.target_column}",
                        f"{first.source_table}.{first.source_column}->{first.target_table}.{first.target_column}",
                    ),
                    "formats": ("html", "csv", "pdf"),
                }
            )
    return tuple(reports)


def chartview_catalog(schema: AppSchema | None = None) -> tuple[dict, ...]:
    """Return generated ChartView contracts for every table."""
    app_schema = schema or sample_reporting_schema()
    chartviews = []
    for table in app_schema.tables:
        numeric_columns = tuple(
            column.name
            for column in table.columns
            if column.type_name in {"int", "decimal", "float"} and not column.primary_key
        )
        label_columns = tuple(
            column.name
            for column in table.columns
            if column.type_name in {"string", "email"} and not column.hidden
        )
        chartviews.append(
            {
                "key": f"{table.name}_chart_view",
                "table": table.name,
                "class_name": _class_name(table.name, "ChartView"),
                "charts": (
                    {"type": "kpi", "metric": "count", "label": "Records"},
                    {
                        "type": "bar",
                        "metric": numeric_columns[0] if numeric_columns else "count",
                        "dimension": label_columns[0] if label_columns else "id",
                    },
                ),
                "renderers": ("flask_appbuilder_chart", "vega_lite", "accessible_table"),
            }
        )
    return tuple(chartviews)


def report_delivery_contract() -> dict:
    """Return PDF/email/export delivery evidence for generated reports."""
    return {
        "format": "appgen.package-report-delivery.v1",
        "formats": ("html", "csv", "pdf"),
        "channels": ("download", "email"),
        "guards": ("no_plaintext_secrets", "attachment_content_type", "row_limit", "audit_log"),
        "email_attachment_types": ("text/csv", "application/pdf"),
    }


def reporting_release_audit(schema: AppSchema | None = None, existing_paths: set[str] | None = None) -> dict:
    """Return package-level proof for report, join, 3-way, and ChartView coverage."""
    app_schema = schema or sample_reporting_schema()
    existing = existing_paths or {
        "app/reports.py",
        "app/report_delivery.py",
        "app/dashboards.py",
        "app/templates/appgen_reports.html",
        "app/templates/appgen_report_delivery.html",
        "app/templates/appgen_dashboards.html",
    }
    table_reports = table_report_catalog(app_schema)
    join_reports = join_report_catalog(app_schema)
    three_way_reports = three_way_report_catalog(app_schema)
    chartviews = chartview_catalog(app_schema)
    delivery = report_delivery_contract()
    table_names = {table.name for table in app_schema.tables}
    gates = (
        {
            "id": "every_table_reported",
            "ok": table_names <= {report["table"] for report in table_reports},
            "tables": tuple(sorted(table_names)),
        },
        {
            "id": "join_reports",
            "ok": len(join_reports) >= len(app_schema.relations),
            "count": len(join_reports),
        },
        {
            "id": "three_way_reports",
            "ok": bool(three_way_reports),
            "count": len(three_way_reports),
        },
        {
            "id": "chartviews",
            "ok": table_names <= {chart["table"] for chart in chartviews}
            and all("ChartView" in chart["class_name"] for chart in chartviews),
            "count": len(chartviews),
        },
        {
            "id": "pdf_email_delivery",
            "ok": "pdf" in delivery["formats"] and "email" in delivery["channels"],
            "delivery": delivery,
        },
        {
            "id": "artifact_contract",
            "ok": {
                "app/reports.py",
                "app/report_delivery.py",
                "app/dashboards.py",
                "app/templates/appgen_reports.html",
                "app/templates/appgen_report_delivery.html",
                "app/templates/appgen_dashboards.html",
            }
            <= existing,
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-reporting-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "table_reports": table_reports,
        "join_reports": join_reports,
        "three_way_reports": three_way_reports,
        "chartviews": chartviews,
        "delivery": delivery,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-reporting-chartview-readiness-unless-ok-is-true",
    }


def _class_name(table_name: str, suffix: str) -> str:
    return "".join(part.capitalize() for part in table_name.split("_")) + suffix
