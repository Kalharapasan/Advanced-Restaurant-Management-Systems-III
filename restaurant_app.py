import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import datetime
import json
import random
import os
import sys

try:
    from database_manager import DatabaseManager
    from customer_manager import CustomerManager
    from menu_manager import MenuManager
    from analytics_manager import AnalyticsManager, AnalyticsDisplay
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all module files are in the same directory as this script")
    sys.exit(1)
    
try:
    from tkcalendar import DateEntry
except ImportError:
    print("Warning: tkcalendar not installed. Some features may be limited.")
    DateEntry = None

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import pandas as pd
    ANALYTICS_AVAILABLE = True
except ImportError:
    print("Warning: matplotlib/pandas not installed. Analytics features will be limited.")
    ANALYTICS_AVAILABLE = False

class RestaurantManagementSystem:
    
    
    def setup_variables(self):
        self.item_vars = {}
        self.item_entries = {}
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.payment_method = tk.StringVar(value="Cash")
        self.discount_percent = tk.StringVar(value="0")
        self.DateofOrder = tk.StringVar()
        self.Receipt_Ref = tk.StringVar()
        self.PaidTax = tk.StringVar()
        self.SubTotal = tk.StringVar()
        self.TotalCost = tk.StringVar()
        self.CostofCakes = tk.StringVar()
        self.CostofDrinks = tk.StringVar()
        self.ServiceCharge = tk.StringVar()
        self.DiscountAmount = tk.StringVar()
        for var in [self.PaidTax, self.SubTotal, self.TotalCost, self.CostofCakes, 
                   self.CostofDrinks, self.ServiceCharge, self.DiscountAmount]:
            var.set("$0.00")
        
        self.text_Input = tk.StringVar()
        self.text_Input.set("0")
        self.DateofOrder.set(time.strftime("%d/%m/%Y"))
        self.menu_items = {}
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 16, 'bold'),
                           background='#2c3e50',
                           foreground='white')
        
        self.style.configure('Heading.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           background='#ecf0f1')
        
        self.style.configure('Custom.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           padding=(10, 5))
    
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Order", command=self.new_order, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Export Orders", command=self.export_orders)
        file_menu.add_command(label="Import Menu", command=self.import_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application, accelerator="Ctrl+Q")
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Sales Analytics", command=self.show_analytics)
        view_menu.add_command(label="Order History", command=self.show_order_history)
        view_menu.add_command(label="Menu Management", command=self.show_menu_management)
        view_menu.add_command(label="Customer Database", command=self.show_customer_database)
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="User Management", command=self.show_user_management)
        tools_menu.add_command(label="Reports", command=self.show_reports)
        tools_menu.add_command(label="Settings", command=self.show_settings)
        tools_menu.add_command(label="Backup Database", command=self.backup_database)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Manual", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        self.root.bind('<Control-n>', lambda e: self.new_order())
        self.root.bind('<Control-q>', lambda e: self.exit_application())
    
    def setup_ui(self):
        self.root.title("🍽️ Advanced Restaurant Management System - Professional Edition v3.0")
        self.root.configure(background='#f0f0f0')
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(1800, int(screen_width * 0.95))
        window_height = min(1000, int(screen_height * 0.9))
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1400, 800)
        self.setup_title_frame()
        self.setup_main_content()
        self.setup_status_bar()
    
    def setup_title_frame(self):
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.grid_columnconfigure(1, weight=1)
        title_frame.grid_propagate(False)
        logo_label = tk.Label(title_frame, 
                            text="🍽️",
                            font=('Segoe UI', 32),
                            bg='#2c3e50', fg='white')
        logo_label.grid(row=0, column=0, padx=20, pady=15)
        title_label = tk.Label(title_frame, 
                             text="Advanced Restaurant Management System",
                             font=('Segoe UI', 24, 'bold'),
                             bg='#2c3e50', fg='white')
        title_label.grid(row=0, column=1, pady=15)
        info_frame = tk.Frame(title_frame, bg='#2c3e50')
        info_frame.grid(row=0, column=2, padx=20, pady=15)
        
        user_label = tk.Label(info_frame,
                            text=f"User: {self.current_user}",
                            font=('Segoe UI', 12),
                            bg='#2c3e50', fg='white')
        user_label.pack()
        
        self.time_label = tk.Label(info_frame,
                                 text=time.strftime("%H:%M:%S"),
                                 font=('Segoe UI', 14, 'bold'),
                                 bg='#2c3e50', fg='white')
        self.time_label.pack()
    
    def setup_main_content(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.create_order_tab()
        self.create_analytics_tab()
        self.create_menu_management_tab()
        self.create_customer_management_tab()
        self.create_reports_tab()
    
    def create_order_tab(self):
        self.order_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.order_frame, text="📋 Order Management")
        self.order_frame.grid_rowconfigure(0, weight=1)
        self.order_frame.grid_columnconfigure(0, weight=2)
        self.order_frame.grid_columnconfigure(1, weight=1)
        left_panel = tk.Frame(self.order_frame, bg='#ecf0f1', relief=tk.RIDGE, bd=2)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        right_panel = tk.Frame(self.order_frame, bg='#ecf0f1', relief=tk.RIDGE, bd=2)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.setup_order_left_panel(left_panel)
        self.setup_order_right_panel(right_panel)
        
    def setup_order_left_panel(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.setup_customer_info_section(parent)
        self.setup_menu_items_section(parent)
        self.setup_order_summary_section(parent)
        self.setup_action_buttons(parent)
    
    def setup_customer_info_section(self, parent):
        customer_frame = tk.LabelFrame(parent, text="👤 Customer Information",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg='#e8f4fd', fg='#2c3e50',
                                     relief=tk.RIDGE, bd=2)
        customer_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        customer_frame.grid_columnconfigure(1, weight=1)
        customer_frame.grid_columnconfigure(3, weight=1)
        tk.Label(customer_frame, text="Name:", bg='#e8f4fd', 
                font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        tk.Entry(customer_frame, textvariable=self.customer_name,
                font=('Segoe UI', 10), width=20).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        tk.Label(customer_frame, text="Phone:", bg='#e8f4fd',
                font=('Segoe UI', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        tk.Entry(customer_frame, textvariable=self.customer_phone,
                font=('Segoe UI', 10), width=15).grid(row=0, column=3, sticky=tk.EW, padx=5, pady=2)
        tk.Label(customer_frame, text="Payment:", bg='#e8f4fd',
                font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        payment_combo = ttk.Combobox(customer_frame, textvariable=self.payment_method,
                                   values=["Cash", "Card", "Digital"], state="readonly", width=18)
        payment_combo.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        tk.Label(customer_frame, text="Discount %:", bg='#e8f4fd',
                font=('Segoe UI', 10, 'bold')).grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        discount_entry = tk.Entry(customer_frame, textvariable=self.discount_percent,
                                font=('Segoe UI', 10), width=8)
        discount_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        discount_entry.bind('<KeyRelease>', self.on_discount_change)
    
    def setup_menu_items_section(self, parent):
        menu_frame = tk.LabelFrame(parent, text="🍽️ Menu Items",
                                 font=('Segoe UI', 12, 'bold'),
                                 bg='#f8f9fa', fg='#2c3e50',
                                 relief=tk.RIDGE, bd=2)
        menu_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        menu_frame.grid_rowconfigure(0, weight=1)
        menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_notebook = ttk.Notebook(menu_frame)
        self.menu_notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.menu_tab_frames = {}
    
    def setup_order_summary_section(self, parent):
        summary_frame = tk.LabelFrame(parent, text="💰 Order Summary",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg='#f8f9fa', fg='#2c3e50',
                                    relief=tk.RIDGE, bd=2)
        summary_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        for i in range(4):
            summary_frame.grid_columnconfigure(i, weight=1)
        
        summary_data = [
            ("Subtotal:", self.SubTotal, 0, 0),
            ("Discount:", self.DiscountAmount, 0, 2),
            ("Service Charge:", self.ServiceCharge, 1, 0),
            ("Tax (15%):", self.PaidTax, 1, 2),
            ("Total Cost:", self.TotalCost, 2, 0)
        ]
        
        for label_text, var, row, col in summary_data:
            tk.Label(summary_frame, text=label_text, bg='#f8f9fa',
                    font=('Segoe UI', 10, 'bold')).grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            cost_entry = tk.Entry(summary_frame, textvariable=var, state='readonly',
                                font=('Segoe UI', 10), width=12)
            cost_entry.grid(row=row, column=col+1, sticky=tk.EW, padx=5, pady=2)
        
    def setup_action_buttons(self, parent):
        button_frame = tk.Frame(parent, bg='#ecf0f1')
        button_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)
        buttons = [
            ("🧮 Calculate", self.calculate_total, '#27ae60'),
            ("🧾 Receipt", self.generate_receipt, '#3498db'),
            ("💾 Save Order", self.save_order, '#9b59b6'),
            ("🔄 Reset", self.reset_order, '#f39c12'),
            ("❌ Clear", self.clear_all, '#e74c3c')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command,
                          font=('Segoe UI', 10, 'bold'),
                          bg=color, fg='white', relief=tk.RAISED, bd=2,
                          width=12, height=2)
            btn.grid(row=0, column=i, padx=2)
        
    def setup_order_right_panel(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.setup_quick_stats(parent)
        self.setup_receipt_section(parent)
        self.setup_calculator_section(parent)
    
    def setup_quick_stats(self, parent):
        stats_frame = tk.LabelFrame(parent, text="📊 Today's Stats",
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#e8f4fd', fg='#2c3e50',
                                  relief=tk.RIDGE, bd=1)
        stats_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.stats_label = tk.Label(stats_frame, text="Loading statistics...",
                                   font=('Segoe UI', 9),
                                   bg='#e8f4fd', fg='#2c3e50')
        self.stats_label.pack(pady=5)
        self.update_quick_stats()
    
    def setup_receipt_section(self, parent):
        receipt_frame = tk.LabelFrame(parent, text="🧾 Receipt Preview",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg='#f8f9fa', fg='#2c3e50',
                                    relief=tk.RIDGE, bd=2)
        receipt_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        receipt_frame.grid_rowconfigure(0, weight=1)
        receipt_frame.grid_columnconfigure(0, weight=1)
        text_frame = tk.Frame(receipt_frame)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        self.receipt_text = tk.Text(text_frame,
                                  font=('Courier New', 9),
                                  bg='#ffffff', fg='#2c3e50',
                                  wrap=tk.WORD, relief=tk.SOLID, bd=1)
        self.receipt_text.grid(row=0, column=0, sticky="nsew")
        receipt_scrollbar = tk.Scrollbar(text_frame, command=self.receipt_text.yview)
        receipt_scrollbar.grid(row=0, column=1, sticky="ns")
        self.receipt_text.config(yscrollcommand=receipt_scrollbar.set)
        receipt_btn_frame = tk.Frame(receipt_frame, bg='#f8f9fa')
        receipt_btn_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        tk.Button(receipt_btn_frame, text="🖨️ Print",
                 command=self.print_receipt,
                 bg='#34495e', fg='white',
                 font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        
        tk.Button(receipt_btn_frame, text="📧 Email",
                 command=self.email_receipt,
                 bg='#16a085', fg='white',
                 font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=2)
    
    def setup_calculator_section(self, parent):
        calc_frame = tk.LabelFrame(parent, text="🧮 Calculator",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg='#f8f9fa', fg='#2c3e50',
                                 relief=tk.RIDGE, bd=2)
        calc_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        calc_display = tk.Entry(calc_frame, textvariable=self.text_Input,
                              font=('Segoe UI', 14, 'bold'), justify='right',
                              state='readonly', bg='#2c3e50', fg='white')
        calc_display.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 2), ('=', 5, 3)
        ]
        for (text, row, col) in buttons:
            if text == '0':
                self.create_calc_button(calc_frame, text, row, col).grid(
                    row=row, column=col, columnspan=2, sticky="ew", padx=1, pady=1)
            else:
                self.create_calc_button(calc_frame, text, row, col).grid(
                    row=row, column=col, sticky="ew", padx=1, pady=1)
        
        for i in range(4):
            calc_frame.grid_columnconfigure(i, weight=1)
    
    def create_calc_button(self, parent, text, row, col):
        color_map = {
            'C': '#e74c3c', '±': '#f39c12', '%': '#f39c12', '/': '#3498db',
            '*': '#3498db', '-': '#3498db', '+': '#3498db', '=': '#27ae60'
        }
        
        bg_color = color_map.get(text, '#95a5a6')
        
        if text == 'C':
            command = self.calc_clear
        elif text == '±':
            command = self.calc_negate
        elif text == '=':
            command = self.calc_equals
        else:
            command = lambda t=text: self.calc_input(t)
        
        return tk.Button(parent, text=text, command=command,
                        font=('Segoe UI', 12, 'bold'),
                        bg=bg_color, fg='white',
                        relief=tk.RAISED, bd=2, width=3, height=1)
    
    def create_analytics_tab(self):
        self.analytics_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.analytics_frame, text="📊 Analytics")
        tk.Label(self.analytics_frame, text="📊 Sales Analytics Dashboard",
                font=('Segoe UI', 16, 'bold'), bg='#f0f0f0').pack(pady=20)
        self.setup_analytics_content()
    
    def create_menu_management_tab(self):
        self.menu_mgmt_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.menu_mgmt_frame, text="🍽️ Menu")
        self.setup_menu_management_content()
    
    def refresh_menu(self):
        self.populate_menu_management()
        self.update_status("Menu refreshed successfully")
    
    def setup_menu_management_content(self):
        title_frame = tk.Frame(self.menu_mgmt_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(title_frame, text="🍽️ Menu Management",
                font=('Segoe UI', 18, 'bold'), bg='#f0f0f0').pack(side='left')
        
        btn_frame = tk.Frame(title_frame, bg='#f0f0f0')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text="➕ Add Item", 
                 font=('Segoe UI', 10, 'bold'),
                 bg='#27ae60', fg='white',
                 command=self.add_menu_item).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔄 Refresh", 
                 font=('Segoe UI', 10, 'bold'),
                 bg='#3498db', fg='white',
                 command=self.refresh_menu).pack(side='left', padx=5)
        categories_frame = tk.LabelFrame(self.menu_mgmt_frame, text="Menu Categories",
                                       font=('Segoe UI', 12, 'bold'), bg='#f0f0f0')
        categories_frame.pack(fill='both', expand=True, padx=20, pady=10)
        columns = ('Name', 'Category', 'Price', 'Available')
        self.menu_tree = ttk.Treeview(categories_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.menu_tree.heading(col, text=col)
            self.menu_tree.column(col, width=150)
        v_scrollbar_menu = ttk.Scrollbar(categories_frame, orient=tk.VERTICAL, command=self.menu_tree.yview)
        h_scrollbar_menu = ttk.Scrollbar(categories_frame, orient=tk.HORIZONTAL, command=self.menu_tree.xview)
        self.menu_tree.configure(yscrollcommand=v_scrollbar_menu.set, xscrollcommand=h_scrollbar_menu.set)
        self.menu_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar_menu.pack(side='right', fill='y')
        self.refresh_menu()
    
    def populate_menu_management(self):
        if not hasattr(self, 'menu_tree') or not self.menu_tree:
            return
        
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
        for category, items in self.menu_items.items():
            for item in items:
                name = item.get('name', 'Unknown')
                price = f"${item.get('price', 0):.2f}"
                available = 'Yes' if item.get('available', True) else 'No'
                
                self.menu_tree.insert('', 'end', values=(
                    name, category.replace('_', ' ').title(), price, available
                ))
    
    def create_customer_management_tab(self):
        self.customer_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.customer_frame, text="👥 Customers")
        self.setup_customer_management_content()
    
    def setup_customer_management_content(self):
        title_frame = tk.Frame(self.customer_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(title_frame, text="👥 Customer Management",
                font=('Segoe UI', 18, 'bold'), bg='#f0f0f0').pack(side='left')
        
        btn_frame = tk.Frame(title_frame, bg='#f0f0f0')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text="➕ Add Customer", 
                 font=('Segoe UI', 10, 'bold'),
                 bg='#27ae60', fg='white',
                 command=self.add_customer).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔍 Search", 
                 font=('Segoe UI', 10, 'bold'),
                 bg='#3498db', fg='white',
                 command=self.search_customers).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔄 Refresh", 
                 font=('Segoe UI', 10, 'bold'),
                 bg='#e67e22', fg='white',
                 command=self.force_refresh_customers).pack(side='left', padx=5)
        
        search_frame = tk.Frame(self.customer_frame, bg='#f0f0f0')
        search_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(search_frame, text="Search:", font=('Segoe UI', 10, 'bold'), 
                bg='#f0f0f0').pack(side='left')
        
        self.customer_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.customer_search_var,
                              font=('Segoe UI', 10), width=30)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', self.on_customer_search)
        
        customers_frame = tk.LabelFrame(self.customer_frame, text="Customer Database",
                                      font=('Segoe UI', 12, 'bold'), bg='#f0f0f0')
        customers_frame.pack(fill='both', expand=True, padx=20, pady=10)
        cust_columns = ('Name', 'Phone', 'Email', 'Total Orders', 'Total Spent')
        self.customer_tree = ttk.Treeview(customers_frame, columns=cust_columns, show='headings', height=15)
        for col in cust_columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=150)
        v_scrollbar_cust = ttk.Scrollbar(customers_frame, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=v_scrollbar_cust.set)
        self.customer_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar_cust.pack(side='right', fill='y')
        self.refresh_customers()
    
    def load_sample_customers(self):
        self.sample_customers = [
            {
                'name': 'John Smith',
                'phone': '555-0101',
                'email': 'john.smith@email.com',
                'total_orders': 15,
                'total_spent': 285.50
            },
            {
                'name': 'Sarah Johnson',  
                'phone': '555-0102',
                'email': 'sarah.j@email.com',
                'total_orders': 8,
                'total_spent': 124.75
            },
            {
                'name': 'Mike Wilson',
                'phone': '555-0103', 
                'email': 'mike.wilson@email.com',
                'total_orders': 22,
                'total_spent': 456.20
            },
            {
                'name': 'Emily Davis',
                'phone': '555-0104',
                'email': 'emily.d@email.com', 
                'total_orders': 5,
                'total_spent': 89.25
            },
            {
                'name': 'David Brown',
                'phone': '555-0105',
                'email': 'david.brown@email.com',
                'total_orders': 12,
                'total_spent': 198.80
            },
            {
                'name': 'Lisa Anderson',
                'phone': '555-0106', 
                'email': 'lisa.a@email.com',
                'total_orders': 18,
                'total_spent': 334.65
            },
            {
                'name': 'Robert Martinez',
                'phone': '555-0107',
                'email': 'robert.m@email.com', 
                'total_orders': 25,
                'total_spent': 567.40
            },
            {
                'name': 'Jennifer Lee',
                'phone': '555-0108',
                'email': 'jennifer.lee@email.com',
                'total_orders': 11,
                'total_spent': 223.15
            },
            {
                'name': 'Michael Garcia',
                'phone': '555-0109',
                'email': 'michael.g@email.com',
                'total_orders': 19,
                'total_spent': 412.90
            },
            {
                'name': 'Amanda Taylor',
                'phone': '555-0110',
                'email': 'amanda.t@email.com',
                'total_orders': 7,
                'total_spent': 156.85
            }
        ]
    
    def force_refresh_customers(self):
        print("DEBUG: Force refreshing customers")
        self.load_sample_customers()
        print(f"DEBUG: Loaded {len(self.sample_customers)} customers")