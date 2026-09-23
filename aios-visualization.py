# aios-visualization.py
"""
Python script to connect to the PostgreSQL database (connector:conn-jdbc-postgres),
retrieve top‑5 products by total sales, and generate a bar chart using matplotlib.
The script is self‑contained and can be run directly from the workspace.
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import pandas as pd

# Use psycopg2 for PostgreSQL connection (available in the AIOS environment)
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection parameters are resolved automatically by the connector.
# The connector identifier is passed via an environment variable for safety.
DB_CONNECTOR = os.getenv("AIOS_DB_CONNECTOR", "connector:conn-jdbc-postgres")

def get_connection():
    # In the AIOS runtime, the connector string is interpreted by the underlying driver.
    # Here we assume a DSN‑style connection string is provided via the environment.
    dsn = os.getenv("AIOS_POSTGRES_DSN")
    if not dsn:
        raise RuntimeError("Environment variable AIOS_POSTGRES_DSN not set. Provide a valid PostgreSQL DSN.")
    return psycopg2.connect(dsn, cursor_factory=RealDictCursor)

def fetch_top_products(limit=5):
    query = """
        SELECT p.product_name,
               SUM(oi.quantity * oi.unit_price) AS total_sales
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_sales DESC
        LIMIT %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()
    return pd.DataFrame(rows)

def plot_sales(df):
    plt.figure(figsize=(10, 6))
    plt.bar(df['product_name'], df['total_sales'], color='steelblue')
    plt.xlabel('Product')
    plt.ylabel('Total Sales (USD)')
    plt.title('Top {} Products by Sales'.format(len(df)))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    output_path = 'top_products_sales.png'
    plt.savefig(output_path)
    print(f"Bar chart saved to {output_path}")

def main():
    try:
        df = fetch_top_products()
        if df.empty:
            print("No sales data found.")
            sys.exit(0)
        print("Top products data:\n", df)
        plot_sales(df)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
