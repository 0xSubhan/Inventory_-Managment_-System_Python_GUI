# function to show
from database import config

def get_product_by_name(cursor,name):
    cursor.execute("""
    SELECT * FROM product 
    WHERE name = %s        
    """,(name,))

    return cursor.fetchone() # returns None if no record !

def insert_product(cursor,d_name,d_category,d_price,d_quantity):

        cursor.execute("""
        INSERT INTO product (name,category,price,quantity) VALUES (%s,%s,%s,%s)
        """,(d_name,d_category,d_price,d_quantity))

def get_all_products(cursor):
    cursor.execute("""
    SELECT * FROM product
    """)
    return cursor.fetchall()