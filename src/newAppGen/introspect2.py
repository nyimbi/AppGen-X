#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the introspect2

"""

import psycopg2
import pprint
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker



# Define the SQLAlchemy engine and session
engine = create_engine('postgresql:///plat')
Session = sessionmaker(bind=engine)
session = Session()

# Define the base model class for SQLAlchemy
Base = declarative_base()


# Define the app_Table, app_Column, and app_Relationship tables
class app_Table(Base):
    __tablename__ = 'app_table'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    columns = relationship('app_Column')

class app_Column(Base):
    __tablename__ = 'app_column'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data_type = Column(String)
    table_id = Column(Integer, ForeignKey('app_table.id'))
    table = relationship('app_Table')

class app_Relationship(Base):
    __tablename__ = 'app_relationship'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    source_table_id = Column(Integer, ForeignKey('app_table.id'))
    source_table = relationship('app_Table', foreign_keys=[source_table_id])
    source_column_id = Column(Integer, ForeignKey('app_column.id'))
    source_column = relationship('app_Column', foreign_keys=[source_column_id])
    referred_table_id = Column(Integer, ForeignKey('app_table.id'))
    referred_table = relationship('app_Table', foreign_keys=[referred_table_id])
    referred_column_id = Column(Integer, ForeignKey('app_column.id'))
    referred_column = relationship('app_Column', foreign_keys=[referred_column_id])


def introspect_postgres_db(host, port, dbname, user, password):
    """
    Connects to PostgreSQL database using psycopg2 library and introspects the schema, tables,
    columns, and relationships between tables. Returns an object representation of the database schema.
    """
    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
    cur = conn.cursor()

    # Introspect tables
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        AND table_type='BASE TABLE'
    """)
    tables = [row[0] for row in cur.fetchall()]

    # Introspect columns and data types
    columns = {}
    for table in tables:
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = '{}'
        """.format(table))
        columns[table] = [(row[0], row[1]) for row in cur.fetchall()]

    # Introspect foreign keys and relationships between tables
    relationships = {}
    for table in tables:
        cur.execute("""
            SELECT conrelid::regclass AS source_table, conname, pg_get_constraintdef(c.oid)
            FROM   pg_constraint c
            WHERE  confrelid = '{table}'::regclass AND contype = 'f'
        """.format(table=table))
        relationships[table] = []
        for row in cur.fetchall():
            relationship = {}
            relationship['name'] = row[1]
            relationship['source_table'] = row[0]
            relationship['source_field'] = row[2].split('(')[1].split(')')[0]
            relationship['referred_table'] = row[2].split('REFERENCES ')[1].split('(')[0]
            relationship['referred_column'] = row[2].split('REFERENCES ')[1].split('(')[1].split(')')[0]
            relationships[table].append(relationship)

    # Close database connection
    cur.close()
    conn.close()

    # Return object representation of the database schema
    schema = {
        'tables': tables,
        'columns': columns,
        'relationships': relationships
    }
    return schema

# sch = introspect_postgres_db('','','plat','','')
# print(pprint.pprint(sch))



# Introspect the database schema
def introspect_and_save(host, port, dbname, user, password):
    # schema = introspect_postgres_db(host='localhost', port='5432', dbname='mydatabase', user='myuser', password='mypassword')
    schema = introspect_postgres_db(host=host, port=port, dbname=dbname, user=user, password=password)

    # Insert the tables, columns, and relationships into the database
    for table_name in schema['tables']:
        table = app_Table(name=table_name)
        session.add(table)
        for column_name, data_type in schema['columns'][table_name]:
            column = app_Column(name=column_name, data_type=data_type, table=table)
            session.add(column)
        for relationship in schema['relationships'][table_name]:
            source_table = session.query(app_Table).filter_by(name=relationship['source_table']).one()
            source_column = session.query(app_Column).filter_by(name=relationship['source_field'], table_id=source_table.id).one()
            referred_table = session.query(app_Table).filter_by(name=relationship['referred_table']).one()
            referred_column = session.query(app_Column).filter_by(name=relationship['referred_column'], table_id=referred_table.id).one()
            rel = app_Relationship(
                name=relationship['name'],
                source_table=source_table,
                source_column=source_column,
                referred_table=referred_table,
                referred_column=referred_column
            )
            session.add(rel)

    session.commit()

# # Create the tables if they don't already exist
# Base.metadata.create_all(engine)

if "__name__" == "__main__":
    # Create the tables if they don't already exist
    Base.metadata.create_all(engine)
    sch = introspect_postgres_db('','','plat','','')
    print(pprint.pprint(sch))
    introspect_and_save('localhost',5432,'plat', '','')


