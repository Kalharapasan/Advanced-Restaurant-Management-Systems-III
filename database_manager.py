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
    
    def create_tables(self, cursor):
        create_orders_table = """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            receipt_ref VARCHAR(50) UNIQUE NOT NULL,
            order_date DATE NOT NULL,
            order_time TIME NOT NULL,
            customer_name VARCHAR(100),
            customer_phone VARCHAR(20),
            customer_email VARCHAR(100),
            payment_method ENUM('Cash', 'Card', 'Digital') DEFAULT 'Cash',
            items JSON NOT NULL,
            cost_of_drinks DECIMAL(10,2),
            cost_of_cakes DECIMAL(10,2),
            service_charge DECIMAL(10,2),
            discount DECIMAL(10,2) DEFAULT 0.00,
            discount_percent DECIMAL(5,2) DEFAULT 0.00,
            subtotal DECIMAL(10,2),
            tax_paid DECIMAL(10,2),
            total_cost DECIMAL(10,2),
            status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
            served_by VARCHAR(50),
            table_number INT,
            order_type ENUM('Dine-in', 'Takeaway', 'Delivery') DEFAULT 'Dine-in',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_order_date (order_date),
            INDEX idx_customer_phone (customer_phone),
            INDEX idx_status (status)
        )
        """
        cursor.execute(create_orders_table)
        
        create_menu_table = """
        CREATE TABLE IF NOT EXISTS menu_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category ENUM('drinks', 'cakes', 'appetizers', 'main_course', 'desserts', 'specials') NOT NULL,
            price DECIMAL(8,2) NOT NULL,
            cost_price DECIMAL(8,2) DEFAULT 0.00,
            description TEXT,
            ingredients TEXT,
            allergens VARCHAR(255),
            nutritional_info JSON,
            image_path VARCHAR(255),
            preparation_time INT DEFAULT 10,
            is_vegetarian BOOLEAN DEFAULT FALSE,
            is_vegan BOOLEAN DEFAULT FALSE,
            is_gluten_free BOOLEAN DEFAULT FALSE,
            spice_level ENUM('None', 'Mild', 'Medium', 'Hot', 'Very Hot') DEFAULT 'None',
            is_available BOOLEAN DEFAULT TRUE,
            is_active BOOLEAN DEFAULT TRUE,
            popularity_score INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_category (category),
            INDEX idx_available (is_available, is_active)
        )
        """
        cursor.execute(create_menu_table)