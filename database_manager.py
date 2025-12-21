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
            
            ('Chocolate Fudge Cake', 'cakes', 4.95, 1.50, 'Rich chocolate cake with fudge frosting',
             'Chocolate, Flour, Sugar, Eggs, Butter, Cream', 'Gluten, Eggs, Milk',
             '{"calories": 450, "protein": 6, "carbs": 55, "fat": 24}',
             None, 15, True, False, False, 'None'),
            ('Cheesecake', 'cakes', 4.75, 1.20, 'Classic New York style cheesecake',
             'Cream cheese, Sugar, Eggs, Graham crackers', 'Gluten, Eggs, Milk',
             '{"calories": 410, "protein": 8, "carbs": 35, "fat": 28}',
             None, 10, True, False, False, 'None'),
            ('Carrot Cake', 'cakes', 4.25, 1.10, 'Moist carrot cake with cream cheese frosting',
             'Carrots, Flour, Sugar, Eggs, Walnuts, Cream cheese', 'Gluten, Eggs, Milk, Nuts',
             '{"calories": 380, "protein": 5, "carbs": 45, "fat": 20}',
             None, 12, True, False, False, 'None'),
            ('Tiramisu', 'cakes', 5.25, 1.60, 'Italian coffee-flavored dessert',
             'Ladyfingers, Mascarpone, Espresso, Cocoa', 'Gluten, Eggs, Milk',
             '{"calories": 400, "protein": 7, "carbs": 30, "fat": 28}',
             None, 20, True, False, False, 'None'),
            
            ('Bruschetta', 'appetizers', 6.95, 2.00, 'Toasted bread with tomato, basil, and garlic',
             'Bread, Tomatoes, Basil, Garlic, Olive oil', 'Gluten',
             '{"calories": 220, "protein": 6, "carbs": 35, "fat": 8}',
             None, 8, True, True, False, 'None'),
            ('Buffalo Wings', 'appetizers', 8.95, 3.20, 'Spicy chicken wings with blue cheese dip',
             'Chicken wings, Buffalo sauce, Blue cheese', 'Milk',
             '{"calories": 350, "protein": 25, "carbs": 5, "fat": 26}',
             None, 15, False, False, True, 'Hot'),
            ('Mozzarella Sticks', 'appetizers', 7.45, 2.50, 'Breaded mozzarella with marinara sauce',
             'Mozzarella, Breadcrumbs, Marinara sauce', 'Gluten, Milk',
             '{"calories": 320, "protein": 16, "carbs": 20, "fat": 20}',
             None, 10, True, False, False, 'None'),
            
            ('Grilled Salmon', 'main_course', 16.95, 8.50, 'Fresh Atlantic salmon with herbs',
             'Salmon fillet, Herbs, Lemon, Olive oil', 'Fish',
             '{"calories": 420, "protein": 35, "carbs": 2, "fat": 28}',
             None, 18, False, False, True, 'None'),
            ('Chicken Alfredo', 'main_course', 14.95, 6.80, 'Pasta with grilled chicken and creamy Alfredo sauce',
             'Pasta, Chicken breast, Cream, Parmesan cheese', 'Gluten, Milk',
             '{"calories": 680, "protein": 40, "carbs": 55, "fat": 32}',
             None, 16, False, False, False, 'None'),
            ('Vegetable Stir Fry', 'main_course', 12.95, 4.20, 'Fresh vegetables in Asian sauce',
             'Mixed vegetables, Soy sauce, Ginger, Garlic', 'Soy',
             '{"calories": 280, "protein": 8, "carbs": 45, "fat": 8}',
             None, 12, True, True, False, 'Mild'),
            
         ]
        
        insert_query = """
        INSERT INTO menu_items (name, category, price, cost_price, description, ingredients, allergens,
                              nutritional_info, image_path, preparation_time, is_vegetarian, is_vegan, 
                              is_gluten_free, spice_level) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, menu_items)
    
    def insert_default_users(self, cursor):
        users = [
            ('admin', self.hash_password('admin123'), 'Admin', 'System Administrator', 
             'admin@restaurant.com', '+1234567890', '2024-01-01', 
             '{"all": true}'),
            ('manager', self.hash_password('manager123'), 'Manager', 'Restaurant Manager',
             'manager@restaurant.com', '+1234567891', '2024-01-01',
             '{"orders": true, "menu": true, "customers": true, "reports": true}'),
            ('cashier', self.hash_password('cashier123'), 'Cashier', 'Front Desk Cashier',
             'cashier@restaurant.com', '+1234567892', '2024-01-01',
             '{"orders": true, "customers": true}'),
            ('waiter', self.hash_password('waiter123'), 'Waiter', 'Service Staff',
             'waiter@restaurant.com', '+1234567893', '2024-01-01',
             '{"orders": true, "tables": true}')
        ]
        
        insert_query = """
        INSERT INTO users (username, password_hash, role, full_name, email, phone, hire_date, permissions) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, users)
    
    def insert_default_tables(self, cursor):
        tables = [
            (1, 2, 'Window', 'Regular'),
            (2, 2, 'Window', 'Regular'),
            (3, 4, 'Center', 'Regular'),
            (4, 4, 'Center', 'Regular'),
            (5, 6, 'Corner', 'VIP'),
            (6, 8, 'Corner', 'VIP'),
            (7, 2, 'Patio', 'Outdoor'),
            (8, 4, 'Patio', 'Outdoor'),
            (9, 3, 'Bar Area', 'Bar'),
            (10, 3, 'Bar Area', 'Bar'),
        ]
        
        insert_query = """
        INSERT INTO restaurant_tables (table_number, capacity, location, table_type) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_query, tables)
        
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        return hashlib.sha256(password.encode()).hexdigest() == password_hash
    
    def get_connection(self):
        return self.connection
    
    def is_connected(self):
        return self.connection and self.connection.is_connected()
    
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def get_all_customers(self, search_term=None):
        if not self.is_connected():
            return []
        
        try:
            cursor = self.connection.cursor()
            
            if search_term:
                query = """
                SELECT id, customer_id, name, phone, email, total_orders, total_spent, 
                       loyalty_points, loyalty_tier, last_visit, is_active
                FROM customers 
                WHERE (name LIKE %s OR phone LIKE %s OR email LIKE %s OR customer_id LIKE %s)
                ORDER BY name
                """
                cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", 
                                     f"%{search_term}%", f"%{search_term}%"))
            else:
                query = """
                SELECT id, customer_id, name, phone, email, total_orders, total_spent, 
                       loyalty_points, loyalty_tier, last_visit, is_active
                FROM customers 
                ORDER BY name
                """
                cursor.execute(query)
            
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error fetching customers: {e}")
            return []
    
    def add_customer(self, customer_data):
        if not self.is_connected():
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(id) FROM customers")
            max_id = cursor.fetchone()[0] or 0
            customer_id = f"CUST{max_id + 1:06d}"
            
            insert_query = """
            INSERT INTO customers (customer_id, name, phone, email, address, date_of_birth, 
                                 gender, preferred_payment, dietary_preferences, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                customer_id,
                customer_data.get('name'),
                customer_data.get('phone'),
                customer_data.get('email'),
                customer_data.get('address'),
                customer_data.get('date_of_birth'),
                customer_data.get('gender'),
                customer_data.get('preferred_payment'),
                json.dumps(customer_data.get('dietary_preferences', {})),
                customer_data.get('notes')
            ))
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Error adding customer: {e}")
            return False
    
    def update_customer(self, customer_id, customer_data):
        if not self.is_connected():
            return False
        
        try:
            cursor = self.connection.cursor()
            
            update_query = """
            UPDATE customers 
            SET name = %s, phone = %s, email = %s, address = %s, date_of_birth = %s,
                gender = %s, preferred_payment = %s, dietary_preferences = %s, notes = %s
            WHERE id = %s
            """
            
            cursor.execute(update_query, (
                customer_data.get('name'),
                customer_data.get('phone'),
                customer_data.get('email'),
                customer_data.get('address'),
                customer_data.get('date_of_birth'),
                customer_data.get('gender'),
                customer_data.get('preferred_payment'),
                json.dumps(customer_data.get('dietary_preferences', {})),
                customer_data.get('notes'),
                customer_id
            ))
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Error updating customer: {e}")
            return False
    
    
    def get_customer_orders(self, customer_id):
        if not self.is_connected():
            return []
        
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT receipt_ref, order_date, order_time, items, total_cost, status
            FROM orders 
            WHERE customer_phone = (SELECT phone FROM customers WHERE id = %s)
            ORDER BY created_at DESC
            LIMIT 50
            """
            cursor.execute(query, (customer_id,))
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error fetching customer orders: {e}")
            return []
    
    
    