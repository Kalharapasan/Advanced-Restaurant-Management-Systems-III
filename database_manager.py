import mysql.connector
from mysql.connector import Error
import json
import datetime
import hashlib

DB_CONFIG = {
    'host': 'localhost',
    'database': 'restaurant_db',
    'user': 'root',
    'password': 'kalharamax'  
}

class DatabaseManager:
    
    
    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.setup_database()
                print("Database connected successfully")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None
    
    def setup_database(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant_db")
        cursor.execute("USE restaurant_db")
        self.create_tables(cursor)
        self.insert_default_data(cursor)
        self.connection.commit()