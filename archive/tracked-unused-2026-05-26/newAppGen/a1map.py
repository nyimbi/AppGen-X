#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the a1map

"""

from sqlalchemy import create_engine, MetaData

# Define the SQLAlchemy engine and metadata
engine = create_engine('postgresql:///plat')
metadata = MetaData(bind=engine)

# Reflect the database schema
metadata.reflect()

# Generate Python code for all the tables
for table_name, table in metadata.tables.items():
    table_code = f"""
class {table_name}(Base):
    __tablename__ = '{table_name}'

"""
    for column in table.columns:
        column_code = f"    {column.name} = Column({str(column.type)})"
        if column.primary_key:
            column_code += ", primary_key=True"
        if column.foreign_keys:
            column_code += f", ForeignKey('{list(column.foreign_keys)[0].column.table.name}.{list(column.foreign_keys)[0].column.name}')"
        column_code += "\n"
        table_code += column_code
    print(table_code)



