import matplotlib.pyplot as plt
import pandas as pd
import graphviz

def generate_schema_visualization():
    """Generates a hierarchical architectural diagram of the PostgreSQL database schema."""
    dot = graphviz.Digraph('PostgreSQL_Schema', comment='AIOS PostgreSQL Relational Schema')
    dot.attr(rankdir='TB', size='10,8')
    
    # Tables & Columns
    tables = {
        'customers': ['customer_id (PK)', 'created_at', 'country_code', 'acquisition_channel', 'customer_segment'],
        'orders': ['order_id (PK)', 'customer_id (FK)', 'ordered_at', 'order_status', 'currency', 'subtotal', 'tax_amount', 'shipping_amount', 'order_total'],
        'order_items': ['order_item_id (PK)', 'order_id (FK)', 'product_id (FK)', 'quantity', 'unit_price', 'discount_amount', 'line_total'],
        'products': ['product_id (PK)', 'sku', 'product_name', 'category', 'unit_cost', 'list_price'],
        'payments': ['payment_id (PK)', 'order_id (FK)', 'paid_at', 'payment_method', 'payment_status', 'amount'],
        'refunds': ['refund_id (PK)', 'payment_id (FK)', 'order_id (FK)', 'refunded_at', 'refund_reason', 'amount']
    }
    
    for table, cols in tables.items():
        label = f"<<TABLE BORDER='1' CELLBORDER='0' CELLSPACING='0'><TR><TD BGCOLOR='lightgrey'><B>{table}</B></TD></TR>"
        for col in cols:
            label += f"<TR><TD ALIGN='LEFT'>{col}</TD></TR>"
        label += "</TABLE>>"
        dot.node(table, label=label, shape='plaintext')
        
    # Relationships
    dot.edge('customers', 'orders', label='1 : N')
    dot.edge('orders', 'order_items', label='1 : N')
    dot.edge('products', 'order_items', label='1 : N')
    dot.edge('orders', 'payments', label='1 : N')
    dot.edge('orders', 'refunds', label='1 : N')
    dot.edge('payments', 'refunds', label='1 : N')
    
    return dot

if __name__ == '__main__':
    print('Generating database schema visualization...')
    dot = generate_schema_visualization()
    print('Schema diagram constructed successfully.')
