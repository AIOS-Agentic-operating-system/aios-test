# aios-visualization.py
import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PostgreSQL Database Configuration
DB_HOST = os.getenv('POSTGRES_HOST', 'aws-0-ap-northeast-2.pooler.supabase.com')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'postgres')
DB_USER = os.getenv('POSTGRES_USER', 'postgres.nrxcirnofmlimhjjntjv')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'kQnVfD92RVoTHa99')

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode='prefer'
    )

def generate_insights():
    with get_connection() as conn:
        sql = 'SELECT p.product_name, SUM(oi.quantity) as total_qty, SUM(oi.line_total) as total_revenue FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.product_name ORDER BY total_revenue DESC LIMIT 10;'
        df_products = pd.read_sql_query(sql, conn)
        print('Top 10 Products by Revenue:')
        print(df_products)

        # Plot bar chart
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_products, x='product_name', y='total_revenue', palette='Blues_r')
        plt.title('Top 10 Products by Revenue (PostgreSQL)')
        plt.xlabel('Product Name')
        plt.ylabel('Total Revenue ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('top_products_revenue.png')
        print('Saved visualization: top_products_revenue.png')

if __name__ == '__main__':
    generate_insights()
