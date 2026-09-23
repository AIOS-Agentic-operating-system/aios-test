import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import os

def generate_visualizations():
    # Database Connection parameters
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')
    
    try:
        conn = psycopg2.connect(db_url)
        print("Successfully connected to PostgreSQL database.")
        
        # 1. Top Products by Total Sales Revenue
        query_top_products = """
            SELECT p.product_name, SUM(oi.line_total) AS total_revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY p.product_name
            ORDER BY total_revenue DESC
            LIMIT 10;
        """
        df_products = pd.read_sql_query(query_top_products, conn)
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_products, x='total_revenue', y='product_name', palette='viridis')
        plt.title('Top 10 Products by Total Revenue')
        plt.xlabel('Revenue ($)')
        plt.ylabel('Product Name')
        plt.tight_layout()
        plt.savefig('top_products_revenue.png')
        plt.close()
        
        # 2. Customer Segment Distribution
        query_customers = """
            SELECT customer_segment, COUNT(customer_id) AS total_customers
            FROM customers
            GROUP BY customer_segment;
        """
        df_customers = pd.read_sql_query(query_customers, conn)
        plt.figure(figsize=(8, 5))
        sns.barplot(data=df_customers, x='customer_segment', y='total_customers', palette='magma')
        plt.title('Customer Distribution by Segment')
        plt.xlabel('Segment')
        plt.ylabel('Customer Count')
        plt.tight_layout()
        plt.savefig('customer_segments.png')
        plt.close()
        
        # 3. Monthly Order Volume and Revenue Trends
        query_orders = """
            SELECT DATE_TRUNC('month', ordered_at) AS order_month,
                   COUNT(order_id) AS total_orders,
                   SUM(order_total) AS total_revenue
            FROM orders
            WHERE order_status = 'completed'
            GROUP BY order_month
            ORDER BY order_month;
        """
        df_orders = pd.read_sql_query(query_orders, conn)
        if not df_orders.empty:
            df_orders['order_month'] = pd.to_datetime(df_orders['order_month']).dt.strftime('%Y-%m')
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df_orders, x='order_month', y='total_revenue', marker='o', color='b', label='Revenue')
            plt.title('Monthly Completed Orders Revenue Trend')
            plt.xlabel('Month')
            plt.ylabel('Total Revenue ($)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('monthly_revenue_trend.png')
            plt.close()
        
        conn.close()
        print("Visualizations generated successfully.")
    except Exception as e:
        print(f"Error processing visualizations: {e}")

if __name__ == '__main__':
    generate_visualizations()
