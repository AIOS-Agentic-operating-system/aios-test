import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Connection parameters are resolved from the AIOS connector 'conn-jdbc-postgres'
# AIOS provides an environment variable or configuration that maps this ID to a DSN.
# For illustration, we use a placeholder DSN; replace with the actual DSN provided by AIOS.
DSN = os.getenv('POSTGRES_DSN', 'dbname=postgres user=postgres host=localhost')

def get_connection():
    return psycopg2.connect(DSN)

def fetch_all_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """)
        tables = [row[0] for row in cur.fetchall()]
    return tables

def fetch_table_data(conn, table_name):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"SELECT * FROM {table_name};")
        rows = cur.fetchall()
    return rows


def fetch_table_details(conn, table_name):
    """Return column metadata for a given table.

    The result is a list of dictionaries, each containing:
        - column_name
        - data_type
        - is_nullable (YES/NO)
        - column_default (may be None)
        - ordinal_position
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default,
                ordinal_position
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
            ORDER BY ordinal_position;
            """,
            (table_name,)
        )
        details = cur.fetchall()
    return details

def main():
    conn = get_connection()
    try:
        tables = fetch_all_tables(conn)
        print(f"Found tables: {tables}\n")
        for tbl in tables:
            # Fetch and display schema details first
            details = fetch_table_details(conn, tbl)
            print(f"--- Schema details for table: {tbl} ---")
            print(json.dumps(details, indent=2, default=str))
            print("\n")

            # Then fetch and display actual data rows
            data = fetch_table_data(conn, tbl)
            print(f"--- Data for table: {tbl} ---")
            print(json.dumps(data, indent=2, default=str))
            print("\n")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
