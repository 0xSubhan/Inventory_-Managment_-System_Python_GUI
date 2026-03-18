# function to show
from database import config

def insert_product(d_name,d_category,d_price,d_quantity):
    connection = config.get_db_connection()
    if connection is None:
        return
    else:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO product (name,category,price,quantity) VALUES (%s,%s,%s,%s)
        """,(d_name,d_category,d_price,d_quantity))

        connection.commit()
        cursor.close()
        connection.close()

