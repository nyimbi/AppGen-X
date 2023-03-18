from typing import List, Dict, Any

from flask_appbuilder import ModelView, MasterDetailView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from utils import snake_to_pascal


def gen_view(table_name: str, columns: Dict[str, Dict[str, Any]], relationships: List[Dict[str, Any]]) -> str:
    model_name = snake_to_pascal(table_name)
    view_name = model_name + 'View'
    result = f"class {view_name}(ModelView):\n"
    result += f"    datamodel = SQLAInterface({model_name})\n"
    result += f"    list_columns = ['{', '.join([column_name for column_name in columns.keys()])}']\n"
    add_columns = [column_name for column_name, column_info in columns.items() if not column_info['primary_key']]
    result += f"    add_columns = ['{', '.join(add_columns)}']\n"
    show_columns = [column_name for column_name, column_info in columns.items() if not column_info['primary_key']]
    result += f"    show_columns = ['{', '.join(show_columns)}']\n"
    result += "\n"
    result += f"class {model_name}DetailView(ModelView):\n"
    result += f"    datamodel = SQLAInterface({model_name})\n"
    result += f"    related_views = [{view_name}]\n"
    result += "\n"

    for relationship in relationships:
        child_table_name = relationship['table2'].name
        child_model_name = snake_to_pascal(child_table_name)
        child_view_name = child_model_name + 'View'
        result += f"class {model_name}{child_model_name}MasterView(MasterDetailView):\n"
        result += f"    datamodel = SQLAInterface({model_name}, {child_model_name})\n"
        result += f"    related_views = [{child_view_name}]\n"
        result += "\n"
    return result

def gen_views(tables: List[Dict[str, Any]]):
    result = ""
    for table in tables:
        table_name = table['table_name']
        columns = table['columns']
        relationships = table['relationships']
        result += gen_view(table_name, columns, relationships)
    return result