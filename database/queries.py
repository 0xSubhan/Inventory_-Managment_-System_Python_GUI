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
    ORDER BY productid ASC   
    """)
    return cursor.fetchall()

def get_productID_by_productName(cursor,product_Name):
    cursor.execute("""
    SELECT productid FROM product 
    WHERE name = %s    
    """,(product_Name,))

    return cursor.fetchone() # Return None if no record is Found !

def insert_movement(cursor,d_productid,d_stock_quantity,d_movement_type):
    cursor.execute("""
    INSERT INTO stock_movements (product_id,change_quantity,movement_type) VALUES (%s,%s,%s)
    """,(d_productid,d_stock_quantity,d_movement_type))

def increase_quantity(cursor,d_quantity,d_product_id):
    cursor.execute("""
    UPDATE product 
    SET quantity = quantity + %s
    WHERE productid = %s    
    """,(d_quantity,d_product_id))