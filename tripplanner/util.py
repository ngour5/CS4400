import pymysql.cursors
import os
# Connect to the database

def db_connection():
    return pymysql.connect(host=os.getenv('DB_HOST'),
                           user=os.getenv('DB_USER'),
                           password=os.getenv('DB_PASSWD'),
                           db=os.getenv('DB_NAME'),
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)