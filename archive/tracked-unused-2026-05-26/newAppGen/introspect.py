#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2023

"""A one line summary of the introspect
Introspect a postgresql database by examining the information schema.
"""

import psycopg2

def introspect_postgres(conn):
    cursor = conn.cursor()

    # Fetch table names
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
    """)
    tables = [table[0] for table in cursor.fetchall()]

    # Fetch column names, data types, and constraints
    for table in tables:
        cursor.execute(f"""
            SELECT column_name, data_type, is_nullable, column_default, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = '{table}'
        """)
        columns = cursor.fetchall()



        cursor.execute("""
            SELECT conname, confrelid::regclass, confkey, confupdtype, confdeltype, confmatchtype
            FROM information_schema.pg_constraint
            WHERE public.{}'::regclass AND confrelid IS NOT NULL;
        """.format(table))
        foreign_keys = cursor.fetchall()

        cursor.execute(f"""
            SELECT constraint_name, column_name
            FROM information_schema.constraint_column_usage
            WHERE table_name = '{table}'
        """)
        constraints = cursor.fetchall()

        def get_foreign_keys(conn, schema, table_name):
            cursor = conn.cursor()
            cursor.execute("""
                SELECT conname, confrelid::regclass, confkey, confupdtype, confdeltype, confmatchtype
                FROM pg_constraint 
                WHERE confrelid = '{}.{}'::regclass AND confrelid IS NOT NULL;
            """.format(schema, table_name))
            foreign_keys = cursor.fetchall()

            keys = []
            for key in foreign_keys:
                cursor.execute("""
                    SELECT attname 
                    FROM pg_attribute 
                    WHERE attrelid = '{}' AND attnum = {};
                """.format(key[1], key[2][0]))
                referred_column = cursor.fetchone()[0]
                keys.append({
                    'constraint_name': key[0],
                    'referred_table': key[1],
                    'referred_column': referred_column,
                    'update_action': key[3],
                    'delete_action': key[4],
                    'match_type': key[5]
                })

            return keys

        print(f'Table name: {table}')
        print('Columns:')
        for column in columns:
            print(f'\t{column[0]} ({column[1]})')
        print('Constraints:')
        for constraint in constraints:
            print(f'\t{constraint[0]} ({constraint[1]})')
        print('\n')

# Connect to postgres database
conn = psycopg2.connect(
    host="localhost",
    database="plat"
)

introspect_postgres(conn)



