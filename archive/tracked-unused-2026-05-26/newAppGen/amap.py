#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the amap

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

# Define the SQLAlchemy engine and session
engine = create_engine('postgresql:///plat')
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the database schema using automap_base
Base = automap_base()
Base.prepare(engine, reflect=True)

# Generate Python code for all the tables
for table_name in Base.classes.keys():
    table_class = Base.classes[table_name]
    table_code = f"""
class {table_name}(Base):
    __tablename__ = '{table_class.__tablename__}'

"""
    for column in table_class.__table__.columns:
        column_code = f"    {column.name} = Column({str(column.type)})"
        if column.primary_key:
            column_code += ", primary_key=True"
        if column.foreign_keys:
            column_code += f", ForeignKey('{list(column.foreign_keys)[0].column.table.name}.{list(column.foreign_keys)[0].column.name}')"
        column_code += "\n"
        table_code += column_code
    print(table_code)



