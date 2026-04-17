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

def get_transactions_by_date_range(cursor,from_date,to_date):
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
    WHERE s.sale_date::date BETWEEN %s AND %s
    ORDER BY s.sale_date ASC,s.sale_id ASC
    """,(from_date,to_date))
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

def get_low_stock_products(cursor,threshold=10):
    cursor.execute("""
    SELECT
        p.productid,
        p.name,
        p.category,
        COALESCE(p.quantity,0) AS quantity,
        p.price,
        'LOW' AS stock_level
    FROM product p
    WHERE COALESCE(p.quantity,0) < %s
    ORDER BY quantity ASC,p.name ASC
    """,(threshold,))

    return cursor.fetchall()

def get_top_five_products(cursor,limit=5):
    cursor.execute("""
    SELECT
        ROW_NUMBER() OVER (
            ORDER BY SUM(s.quantity) DESC,SUM(s.total_price) DESC,p.name ASC
        ) AS rank,
        p.name,
        p.category,
        SUM(s.quantity) AS units_sold,
        SUM(s.total_price) AS total_revenue,
        COALESCE(p.quantity,0) AS current_stock
    FROM sales s
    JOIN product p ON p.productid = s.productid
    GROUP BY p.productid,p.name,p.category,p.quantity
    ORDER BY units_sold DESC,total_revenue DESC,p.name ASC
    LIMIT %s
    """,(limit,))

    return cursor.fetchall()

def get_top_five_products_by_date_range(cursor,from_date,to_date,limit=5):
    cursor.execute("""
    SELECT
        ROW_NUMBER() OVER (
            ORDER BY SUM(s.quantity) DESC,SUM(s.total_price) DESC,p.name ASC
        ) AS rank,
        p.name,
        p.category,
        SUM(s.quantity) AS units_sold,
        SUM(s.total_price) AS total_revenue,
        COALESCE(p.quantity,0) AS current_stock
    FROM sales s
    JOIN product p ON p.productid = s.productid
    WHERE s.sale_date::date BETWEEN %s AND %s
    GROUP BY p.productid,p.name,p.category,p.quantity
    ORDER BY units_sold DESC,total_revenue DESC,p.name ASC
    LIMIT %s
    """,(from_date,to_date,limit))

    return cursor.fetchall()
 
