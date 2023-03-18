#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the introspect2

"""

import psycopg2
import pprint

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

sch = introspect_postgres_db('','','plat','','')
print(pprint.pprint(sch))

