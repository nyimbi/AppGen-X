from typing import List, Dict, Any

from flask_appbuilder import ModelView, MasterDetailView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from utils import snake_to_pascal
from headers import VIEW_HEADER, VIEW_FOOTER, VIEW_REG, DOC_HEADER


model_views = []
master_views = []
detail_views = []


def gen_model_view(table_name: str, columns: Dict[str, Dict[str, Any]]) -> str:
    model_name = snake_to_pascal(table_name)
    view_name = model_name + 'View'
    model_views.append(view_name)
    result = f"class {view_name}(ModelView):\n"
    result += f"    datamodel = SQLAInterface({model_name})\n"
    result += f"    list_columns = ['{', '.join([column_name for column_name in columns.keys()])}']\n"
    add_columns = [column_name for column_name, column_info in columns.items() if not column_info['is_primary_key']]
    result += f"    add_columns = ['{', '.join(add_columns)}']\n"
    show_columns = [column_name for column_name, column_info in columns.items() if not column_info['is_primary_key']]
    result += f"    show_columns = ['{', '.join(show_columns)}']\n"
    result += "\n"
    return result



def gen_master_view(table_name: str, columns: Dict[str, Dict[str, Any]], relationships: List[Dict[str, Any]]) -> str:
    result = ""
    model_name = snake_to_pascal(table_name)
    child_views = []
    for relationship in relationships:
        child_table_name = relationship['table2'].name
        child_model_name = snake_to_pascal(child_table_name)
        child_view_name = child_model_name + 'View'
        parent_view_name = f"{model_name}{child_model_name}MasterView"
        master_views.append(parent_view_name)
        col_list =', '.join([column_name for column_name in columns.keys() if not columns[column_name]['is_primary_key']])
        quoted_col_list = ', '.join([f'"{column}"' for column in col_list.split(', ')])
        result += f"class {parent_view_name}(MasterDetailView):\n"
        result += f"    datamodel = SQLAInterface({model_name}, {child_model_name})\n"
        result += f"    related_views = [{child_view_name}]\n"
        result += f"    add_columns = [{quoted_col_list}]\n"
        result += f"    show_columns = [{quoted_col_list}]\n"
        result += f"    edit_columns = [{quoted_col_list}]\n"
        result += f"    add_title = 'Add {model_name} and {child_model_name}'\n"
        result += f"    show_title = 'Show {model_name} and {child_model_name}'\n"
        result += f"    edit_title = 'Edit {model_name} and {child_model_name}'\n"
        result += "\n"
        result += f"    add_title = 'Add {child_model_name} to {model_name}'\n"
        result += f"    show_title = '{child_model_name} in {model_name}'\n"
        result += f"    edit_title = 'Edit {child_model_name} in {model_name}'\n"
        result += "\n"
        result += f"    add_title = 'Add {model_name} and {child_model_name}'\n"
        result += f"    show_title = 'Show {model_name} and {child_model_name}'\n"
        result += f"    edit_title = 'Edit {model_name} and {child_model_name}'\n"
        result += "\n"

    if len(child_views) > 1:
        multiple_view_name = f"{model_name}MultipleView"
        master_views.append(multiple_view_name)
        result += f"class {multiple_view_name}(MultipleView):\n"
        result += f"    views = [{', '.join(child_views)}]\n"
        result += "\n"

    return result


def register_views():
    result = ''
    for view in model_views:
        result += f'appbuilder.add_view(eval({view}), {view}, icon="fa-folder-open-o", category="Setup")\n'

    for view in master_views:
        result += f'appbuilder.add_view(eval({view}), category="Master Detail Models")\n'
    return result


def generate_views(tables: List[Dict[str, Any]]):
    '''
    This generates all the views
    :param tables:
    :return: The vide code
    '''
    result = ""
    result += VIEW_HEADER
    for table in tables:
        table_name = table['table_name']
        columns = table['columns']
        relationships = table['relationships']
        result += gen_model_view(table_name, columns)

    for table in tables:
        table_name = table['table_name']
        columns = table['columns']
        relationships = table['relationships']
        result += gen_master_view(table_name, columns, relationships)

    result += register_views()
    result += VIEW_FOOTER

    with open("views.py", "w") as f:
        f.write(result + '\n\n')

    return result
