#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the d2

"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

import argparse
from pydbml import PyDBML
from pathlib import Path


def generate_models(dbml_file, models_file):
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
            })

            # Add bi-directional relationship
            other_table = table1 if table1 != table_name else table2
            relationships.append({
                'name': name,
                'col1': col2,
                'table1': other_table,
                'col2': col1,
                'table2': table_name,
            })

        tables[table_name] = {
            'columns': columns,
            'relationships': relationships,
        }

    with open(models_file, 'w') as f:
        f.write('from flask_appbuilder import Model\n\n')
        for table_name, table in tables.items():
            f.write(f'class {table_name}(Model):\n')
            f.write(f'    id = Column(Integer, primary_key=True)\n')
            for column_name, column in table['columns'].items():
                f.write(f'    {column_name} = Column({column["type"]}')
                if column['nullable']:
                    f.write(', nullable=True')
                if column['unique']:
                    f.write(', unique=True')
                f.write(')\n')
            f.write('\n')



