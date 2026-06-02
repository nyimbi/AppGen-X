import re

from pyAppGen.pbcs.defense_readiness_logistics.defense_app import workflow_contracts
from pyAppGen.pbcs.defense_readiness_logistics.models import load_migration_sql, model_contracts
from pyAppGen.pbcs.defense_readiness_logistics.routes import ROUTE_DEFINITIONS
from pyAppGen.pbcs.defense_readiness_logistics.services import service_operation_manifest


_CREATE_TABLE_RE = re.compile(r"CREATE TABLE\s+(\S+)\s*\((.*?)\);", re.DOTALL)


def _migration_columns(sql_text: str) -> dict[str, tuple[str, ...]]:
    tables = {}
    for table_name, body in _CREATE_TABLE_RE.findall(sql_text):
        columns = []
        for raw_line in body.splitlines():
            line = raw_line.strip().rstrip(",")
            if not line:
                continue
            columns.append(line.split()[0])
        tables[table_name] = tuple(columns)
    return tables


def test_model_contracts_align_with_migration_columns():
    migration_columns = _migration_columns(load_migration_sql())

    for spec in model_contracts():
        assert spec["table"] in migration_columns
        assert migration_columns[spec["table"]] == spec["fields"]


def test_route_bindings_resolve_to_service_operations():
    manifest = service_operation_manifest()
    operations = set(manifest["command_operations"]) | set(manifest["query_operations"])

    assert all(binding["operation"] in operations for binding in ROUTE_DEFINITIONS)


def test_workflow_contracts_reference_service_backed_steps():
    operations = set(service_operation_manifest()["command_operations"])
    workflows = workflow_contracts()["workflows"]

    assert workflows
    for workflow in workflows:
        assert set(workflow["steps"]).issubset(operations)
