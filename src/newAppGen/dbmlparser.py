#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the dbmlparser

"""
import json
from pydbml import PyDBML
from pathlib import Path


dbml_file = 'test.dbml'

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
            'name' : name,
            'col1': col1,
            'table1' : table1,
            'col2' : col2,
            'table2' : table2,
        })
        relationships.append(constraint)

    tables[table_name] = {
        'columns': columns,
        'relationships': relationships,
    }

print(tables)


