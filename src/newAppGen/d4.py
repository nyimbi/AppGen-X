#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the d3

"""

import argparse
from pathlib import Path

from pydbml import PyDBML


def generate_models(dbml_file, output_file):
    parsed = PyDBML(Path(dbml_file))
    tables = {}

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
            col1 = constraint.col1
            table1 = constraint.table1
            col2 = constraint.col2
            table2 = constraint.table2
            relationships.append({
                'name': name,
                'col1': col1,
                'table1': table1,
                'col2': col2,
                'table2': table2,
                'bi_directional': True
            })

            for ref_table in tables:
                if ref_table != table_name:
                    if col1 in tables[ref_table]['columns']:
                        relationships.append({
                            'name': name,
                            'col1': col1,
                            'table1': table_name,
                            'col2': col2,
                            'table2': ref_table,
                            'bi_directional': True
                        })

        tables[table_name] = {
            'columns': columns,
            'relationships': relationships,
        }

    with open(output_file, 'w') as f:
        f.write('from flask_appbuilder import Model\n')
        f.write('from sqlalchemy import Column, Integer, String, ForeignKey\n\n')

        for table_name, table_data in tables.items():
            f.write(f'class {table_name}(Model):\n')
            f.write(f'    __tablename__ = "{table_name}"\n\n')

            for col_name, col_data in table_data['columns'].items():
                col_type = col_data['type']
                col_type_str = f'String({col_type.upper()})' if col_type == 'varchar' else col_type.title()
                f.write(f'    {col_name} = Column({col_type_str}')
                if col_data['nullable']:
                    f.write(', nullable=True')
                if col_data['unique']:
                    f.write(', unique=True')
                if col_data['primary_key']:
                    f.write(', primary_key=True')
                f.write(')\n')

            f.write('\n')

        for table_name, table_data in tables.items():
            for relationship in table_data['relationships']:
                if not relationship['bi_directional']:
                    continue
                name = relationship['name']
                col1 = relationship['col1']
                table1 = relationship['table1']
                col2 = relationship['col2']
                table2 = relationship['table2']
                f.write(f'{table_name}.{name} = relationship("{table2}", '
                        f'backref="{table1}", '
                        f'primaryjoin=foreign({table_name}.{col1}) == remote({table2}.{col2}))\n')
            f.write('\n')

        with open('views.py', 'w') as f:
            f.write('from flask_appbuilder.views import ModelView\n\n')
            for table_name, table_info in tables.items():
                f.write(f'class {table_name}View(ModelView):\n')
                f.write(f'    datamodel = SQLAInterface({table_name})\n')
                f.write(f'    list_columns = {list(table_info["columns"].keys())}\n\n')


if __name__ == '__main__':
    dbml_file = 'test.dbml'
    output_file = 'mtest.py'
    generate_models(dbml_file, output_file)





