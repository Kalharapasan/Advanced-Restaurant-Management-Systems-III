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
        
        create_customers_table = """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id VARCHAR(20) UNIQUE,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) UNIQUE,
            email VARCHAR(100),
            address TEXT,
            date_of_birth DATE,
            gender ENUM('Male', 'Female', 'Other'),
            total_orders INT DEFAULT 0,
            total_spent DECIMAL(10,2) DEFAULT 0.00,
            loyalty_points INT DEFAULT 0,
            loyalty_tier ENUM('Bronze', 'Silver', 'Gold', 'Platinum') DEFAULT 'Bronze',
            preferred_payment ENUM('Cash', 'Card', 'Digital'),
            dietary_preferences JSON,
            last_visit DATE,
            notes TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_phone (phone),
            INDEX idx_email (email),
            INDEX idx_loyalty_tier (loyalty_tier)
        )
        """
        cursor.execute(create_customers_table)
        
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('Admin', 'Manager', 'Cashier', 'Waiter', 'Chef') DEFAULT 'Cashier',
            full_name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            hire_date DATE,
            is_active BOOLEAN DEFAULT TRUE,
            last_login TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            permissions JSON,
            INDEX idx_username (username),
            INDEX idx_role (role)
        )
        """
        cursor.execute(create_users_table)
        
        create_inventory_table = """
        CREATE TABLE IF NOT EXISTS inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            sku VARCHAR(50) UNIQUE,
            category VARCHAR(50),
            current_stock INT DEFAULT 0,
            min_stock_level INT DEFAULT 10,
            max_stock_level INT DEFAULT 100,
            unit VARCHAR(20) DEFAULT 'pieces',
            unit_price DECIMAL(8,2),
            supplier VARCHAR(100),
            supplier_contact VARCHAR(100),
            last_restocked DATE,
            expiry_date DATE,
            location VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_sku (sku),
            INDEX idx_category (category),
            INDEX idx_stock_level (current_stock)
        )
        """
        cursor.execute(create_inventory_table)
        
        create_tables_table = """
        CREATE TABLE IF NOT EXISTS restaurant_tables (
            id INT AUTO_INCREMENT PRIMARY KEY,
            table_number INT UNIQUE NOT NULL,
            capacity INT NOT NULL,
            location VARCHAR(50),
            table_type ENUM('Regular', 'VIP', 'Outdoor', 'Bar') DEFAULT 'Regular',
            is_available BOOLEAN DEFAULT TRUE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_tables_table)
        
        create_reservations_table = """
        CREATE TABLE IF NOT EXISTS reservations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            table_id INT,
            reservation_date DATE NOT NULL,
            reservation_time TIME NOT NULL,
            party_size INT NOT NULL,
            status ENUM('Confirmed', 'Seated', 'Completed', 'Cancelled', 'No-show') DEFAULT 'Confirmed',
            special_requests TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (table_id) REFERENCES restaurant_tables(id)
        )
        """
        cursor.execute(create_reservations_table)
        
        create_feedback_table = """
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            order_id INT,
            rating INT CHECK (rating BETWEEN 1 AND 5),
            comments TEXT,
            feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
        """
        cursor.execute(create_feedback_table)
    
    def insert_default_data(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        if cursor.fetchone()[0] == 0:
            self.insert_default_menu_items(cursor)
        
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            self.insert_default_users(cursor)
        
        cursor.execute("SELECT COUNT(*) FROM restaurant_tables")
        if cursor.fetchone()[0] == 0:
            self.insert_default_tables(cursor)
    
    def insert_default_menu_items(self, cursor):
        menu_items = [
            ('Latte', 'drinks', 2.20, 0.80, 'Creamy espresso with steamed milk and foam', 
             'Espresso, Steamed milk, Milk foam', 'Milk', 
             '{"calories": 120, "protein": 8, "carbs": 12, "fat": 4}',
             None, 5, True, False, False, 'None'),
            ('Cappuccino', 'drinks', 2.45, 0.85, 'Classic Italian coffee with equal parts espresso, steamed milk, and foam',
             'Espresso, Steamed milk, Milk foam', 'Milk',
             '{"calories": 80, "protein": 4, "carbs": 6, "fat": 3}',
             None, 5, True, False, False, 'None'),
            ('Americano', 'drinks', 1.95, 0.60, 'Espresso shots topped with hot water',
             'Espresso, Hot water', None,
             '{"calories": 5, "protein": 0, "carbs": 1, "fat": 0}',
             None, 3, True, True, True, 'None'),
            ('Green Tea', 'drinks', 1.75, 0.40, 'Organic green tea with antioxidants',
             'Green tea leaves, Hot water', None,
             '{"calories": 0, "protein": 0, "carbs": 0, "fat": 0}',
             None, 3, True, True, True, 'None'),
            ('Iced Coffee', 'drinks', 2.15, 0.75, 'Cold brew coffee served over ice',
             'Cold brew coffee, Ice', None,
             '{"calories": 10, "protein": 0, "carbs": 2, "fat": 0}',
             None, 2, True, True, True, 'None'),
            
            
            
         ]
        