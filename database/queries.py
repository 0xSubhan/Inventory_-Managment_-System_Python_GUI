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

def get_product_price(cursor,productName):
    cursor.execute("""
    SELECT price FROM product
        WHERE name = %s
    """,(productName,))

    return cursor.fetchone() # Return None if no record is found!

def get_product_quantity(cursor,productid):
    cursor.execute("""
    SELECT quantity FROM product
        WHERE productid = %s
    """,(productid,))

    return cursor.fetchone()

def decrease_quantity(cursor,quantity,productID):
    cursor.execute("""
    UPDATE product
    SET quantity = quantity - %s
        WHERE productid = %s
    """,(quantity,productID))

def insert_sale_transaction(cursor,productID,productQuantity,productPrice,sell_total):
    cursor.execute("""
    INSERT INTO sales 
        (productid,quantity,sale_price,total_price)
        VALUES (%s,%s,%s,%s)
    """,(productID,productQuantity,productPrice,sell_total))


def get_productname_by_id(cursor,productID):
    cursor.execute("""
    SELECT name FROM product
        WHERE productid = %s
    """,(productID,))
    return cursor.fetchone()

def get_all_transactions(cursor):
    cursor.execute("""
    SELECT * FROM sales
        ORDER BY sale_id ASC 
    """)

    return cursor.fetchall()

def get_all_transactions_in_order(cursor):
    cursor.execute("""
    SELECT 
        s.sale_id,
        s.sale_date,
        p.name,
        s.quantity,
        s.sale_price,
        s.total_price
    FROM sales s
    JOIN product p ON p.productid = s.productid
    ORDER BY s.sale_id ASC    
    """)
    return cursor.fetchall()

def get_number_of_products(cursor):
    cursor.execute("""
    SELECT COUNT(*) FROM product 
    """)
    return cursor.fetchone() # Returns tuple

def get_total_stocks(cursor):
    cursor.execute("""
    SELECT SUM(quantity) FROM product
    """)
    return cursor.fetchone()

def get_low_stock_count(cursor,threshold=10):
    cursor.execute("""
    SELECT COUNT(*) FROM product WHERE COALESCE(quantity,0) < %s
    """,(threshold,))

    return cursor.fetchone()

def get_total_revenue(cursor):
    cursor.execute("""
    SELECT SUM(total_price) FROM sales
    """)

    return cursor.fetchone()

def get_recent_sales(cursor):
    cursor.execute("""
    SELECT 
        s.sale_date,
        p.name,
        s.quantity,
        s.total_price
    FROM sales s
    JOIN product p ON p.productid = s.productid
    ORDER BY sale_date DESC 
    LIMIT %s    
    """,(5,))

    return cursor.fetchall()