from pydbml import PyDBML
from typing import Dict, List
from jinja2 import Template
from pathlib import Path

def parse_dbml(dbml_file: str) -> List[dict]:
    parsed = PyDBML(Path(dbml_file))
    tables = []

    for table in parsed.tables:
        table_name = table.name
        columns = {}
        relationships = []

        for column in table.columns:
            column_name = column.name
            column_type = column.type
            nullable = not column.not_null
            unique = column.unique
            primary_key = column.pk

            columns[column_name] = {
                'type': column_type,
                'nullable': nullable,
                'unique': unique,
                'primary_key': primary_key,
            }

        for constraint in table.get_refs():
            name = constraint.name
            col1 = constraint.col1[0]
            table1 = constraint.table1
            col2 = constraint.col2[0]
            table2 = constraint.table2
            relationships.append({
                'name': name,
                'col1': col1,
                'table1': table1,
                'col2': col2,
                'table2': table2,
                'bi_directional': True,
            })

        tables.append({
            'table_name': table_name,
            'columns': columns,
            'relationships': relationships,
        })
        print(table_name)
        print('COLUMNS:', columns)
        print('RELATIONSHIPS:', relationships)
    # print(tables)
    return tables


def generate_models(tables):
    with open('models.py', 'w') as f:
        f.write('from flask_appbuilder import Model\n')
        f.write('from sqlalchemy import Column, Integer, String, ForeignKey\n')
        f.write('from sqlalchemy.orm import relationship\n')
        f.write('from sqlalchemy.ext.associationproxy import association_proxy\n\n')

        for x in tables:
            table_name = x['table_name']
            table_data = x
        # for table_name, table_data in tables.items():
            pascal_case_table_name = ''.join(word.capitalize() for word in table_name.split('_'))
            f.write(f'class {pascal_case_table_name}(Model):\n')
            f.write(f'    __tablename__ = "{table_name}"\n\n')

            for col_name, col_data in table_data['columns'].items():
                col_type = col_data['type']
                col_type_str =  'String'
                f.write(f'    {col_name} = Column({col_type_str}')
                if col_data['nullable']:
                    f.write(', nullable=True')
                if col_data['unique']:
                    f.write(', unique=True')
                if col_data['primary_key']:
                    f.write(', primary_key=True')
                f.write(')\n')

            f.write('\n')

            for relationship in table_data['relationships']:
                if not relationship['bi_directional']:
                    continue

                name = relationship['name']
                col1 = relationship['col1']
                table1 = relationship['table1']
                col2 = relationship['col2']
                table2 = relationship['table2']
                is_association_table = False

                for foreign_key in table_data['relationships']:
                    if foreign_key['col1'] == col1 and foreign_key['table2'] == table2:
                        association_table_name = f'{table_name}_{table2}'
                        association_table_pascal_case_name = ''.join(word.capitalize() for word in association_table_name.split('_'))

                        f.write(f'    {table2} = relationship("{pascal_case_table_name}",\n')
                        f.write(f'                    secondary="{association_table_pascal_case_name}",\n')
                        f.write(f'                    backref="{table_name}")\n')
                        f.write(f'\n    {table_name} = association_proxy("{association_table_name}", "{table_name}")\n\n')

                        is_association_table = True
                        break

                if not is_association_table:
                    f.write(f'    {table2} = relationship("{table2}",\n')
                    f.write(f'                    backref="{table1}",\n')
                    f.write(f'                    primaryjoin="{pascal_case_table_name}.{col1} == {table2}.id")\n')
                    f.write('\n')

        f.write('\n')



def generate_views(tables: Dict) -> str:
    views = []

    # create views for each table
    for x in tables:
        table_name = x['table_name']
        table_data = x
    # for table_name, table_data in tables.items():
        # create list view
        template = Template("""
class {{table_name}}ListView(ModelView):
    datamodel = SQLAInterface({{table_name}})
    list_columns = {{list(table_data['columns'].keys())}}
    related_views = [
    {% for relationship in table_data['relationships'] %}
        {% if relationship['bi_directional'] %}
        {'name': '{{relationship['name']}}', 'view': '{{relationship['table2']}}ListView', 'label': '{{relationship['table2']}}', 'category': 'Related'},
        {% endif %}
    {% endfor %}
    ]
    """
        )
        view = template.render(table_name=table_name, table_data=table_data)
        views.append(view)

        # create detail views for each relationship
        for relationship in table_data['relationships']:
            if not relationship['bi_directional']:
                continue
            related_table = relationship['table2']
            template = Template("""
class {{table_name}}{{related_table}}DetailView(ModelView):
    datamodel = SQLAInterface({{related_table}})
    related_views = [
        {'name': '{{table_name}}', 'view': '{{table_name}}ListView', 'label': '{{table_name}}', 'category': 'Related'},
    ]
    """
            )
            view = template.render(table_name=table_name, related_table=related_table)
            views.append(view)

    return '\n\n'.join(views)

if __name__ == '__main__':
    print('Hello')
    tables = parse_dbml("test.dbml")
    print(tables)
    generate_models(tables)
    generate_views(tables)