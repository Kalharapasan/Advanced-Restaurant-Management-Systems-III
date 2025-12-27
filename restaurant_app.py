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
        if hasattr(self, 'customer_tree') and self.customer_tree:
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            print("DEBUG: Cleared existing treeview items")
            for i, customer in enumerate(self.sample_customers):
                values = (
                    customer['name'],
                    customer['phone'],
                    customer['email'], 
                    customer['total_orders'],
                    f"${customer['total_spent']:.2f}"
                )
                self.customer_tree.insert('', 'end', values=values)
                print(f"DEBUG: Added customer {i+1}: {customer['name']} - {customer['phone']}")
            
            self.update_status(f"✅ Refreshed: {len(self.sample_customers)} customers loaded")
            messagebox.showinfo("Refresh Complete", f"Loaded {len(self.sample_customers)} customers with updated data")
            
        else:
            print("DEBUG: No customer_tree found!")
            self.update_status("❌ Error: Customer table not found")
    
    def refresh_customers(self):
        self.load_sample_customers()
        self.populate_customer_data()
        self.update_status(f"Customers refreshed - {len(self.sample_customers)} customers loaded")
        print(f"DEBUG: Loaded {len(self.sample_customers)} customers")
        for i, customer in enumerate(self.sample_customers):
            print(f"DEBUG: Customer {i+1}: {customer['name']} - {customer['phone']}")
    
    def populate_customer_data(self):
        if not hasattr(self, 'customer_tree') or not self.customer_tree:
            print("DEBUG: No customer_tree found")
            return
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        print(f"DEBUG: Adding {len(self.sample_customers)} customers to treeview")
        for customer in self.sample_customers:
            values = (
                customer['name'],
                customer['phone'], 
                customer['email'],
                customer['total_orders'],
                f"${customer['total_spent']:.2f}"
            )
            print(f"DEBUG: Adding customer: {values}")
            self.customer_tree.insert('', 'end', values=values)
    
    def on_customer_search(self, event=None):
        search_term = self.customer_search_var.get().lower()
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        for customer in self.sample_customers:
            if (search_term in customer['name'].lower() or 
                search_term in customer['phone'] or
                search_term in customer['email'].lower()):
                
                self.customer_tree.insert('', 'end', values=(
                    customer['name'],
                    customer['phone'],
                    customer['email'],
                    customer['total_orders'],
                    f"${customer['total_spent']:.2f}"
                ))
    
    def search_customers(self):
        search_term = tk.simpledialog.askstring("Search Customers", "Enter name, phone, or email:")
        if search_term:
            self.customer_search_var.set(search_term)
            self.on_customer_search()
    
    def add_customer(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Customer")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        tk.Label(dialog, text="Add New Customer", font=('Segoe UI', 16, 'bold'), 
                bg='#f0f0f0').pack(pady=10)
        fields = [
            ('Name:', 'name'),
            ('Phone:', 'phone'),
            ('Email:', 'email')
        ]
        
        entries = {}
        for label_text, field_name in fields:
            frame = tk.Frame(dialog, bg='#f0f0f0')
            frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(frame, text=label_text, bg='#f0f0f0', 
                    font=('Segoe UI', 10, 'bold')).pack(side='left')
            
            entry = tk.Entry(frame, font=('Segoe UI', 10), width=30)
            entry.pack(side='right')
            entries[field_name] = entry
        btn_frame = tk.Frame(dialog, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        def save_customer():
            new_customer = {
                'name': entries['name'].get(),
                'phone': entries['phone'].get(),
                'email': entries['email'].get(),
                'total_orders': 0,
                'total_spent': 0.0
            }
            
            if new_customer['name'] and new_customer['phone']:
                self.sample_customers.append(new_customer)
                self.populate_customer_data()
                self.update_status(f"Customer {new_customer['name']} added successfully")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Name and phone are required fields")
        
        tk.Button(btn_frame, text="Save", command=save_customer,
                 bg='#27ae60', fg='white', font=('Segoe UI', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 bg='#e74c3c', fg='white', font=('Segoe UI', 10, 'bold')).pack(side='left', padx=5)
    
    def create_reports_tab(self):
        self.reports_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.reports_frame, text="📈 Reports")
        self.setup_reports_content()
    
    def setup_reports_content(self):
        tk.Label(self.reports_frame, text="📈 Business Reports & Insights",
                font=('Segoe UI', 18, 'bold'), bg='#f0f0f0').pack(pady=20)
        reports_btn_frame = tk.Frame(self.reports_frame, bg='#f0f0f0')
        reports_btn_frame.pack(pady=20)
        reports = [
            ("📊 Daily Sales Report", self.generate_daily_report, '#3498db'),
            ("📅 Weekly Report", self.generate_weekly_report, '#9b59b6'),
            ("📆 Monthly Report", self.generate_monthly_report, '#e67e22'),
            ("🏆 Top Items Report", self.generate_top_items_report, '#27ae60')
        ]
        
        for i, (text, command, color) in enumerate(reports):
            btn = tk.Button(reports_btn_frame, text=text, command=command,
                          font=('Segoe UI', 12, 'bold'),
                          bg=color, fg='white', relief=tk.RAISED, bd=2,
                          width=20, height=2)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
        self.reports_text_frame = tk.LabelFrame(self.reports_frame, text="Report Results",
                                              font=('Segoe UI', 12, 'bold'), bg='#f0f0f0')
        self.reports_text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.reports_text = tk.Text(self.reports_text_frame,
                                  font=('Courier New', 10),
                                  bg='#ffffff', fg='#2c3e50',
                                  wrap=tk.WORD, relief=tk.SOLID, bd=1)
        
        reports_scrollbar = tk.Scrollbar(self.reports_text_frame, command=self.reports_text.yview)
        self.reports_text.configure(yscrollcommand=reports_scrollbar.set)
        
        self.reports_text.pack(side='left', fill='both', expand=True)
        reports_scrollbar.pack(side='right', fill='y')
    
    def setup_analytics_content(self):
        self.analytics_display = AnalyticsDisplay(self.analytics_frame, self.analytics_manager)
    
    def setup_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        self.status_frame.grid(row=2, column=0, sticky="ew")
        self.status_frame.grid_propagate(False)
        self.status_frame.grid_columnconfigure(1, weight=1)
        self.status_label = tk.Label(self.status_frame, text="Ready",
                                   font=('Segoe UI', 10),
                                   bg='#34495e', fg='white', anchor=tk.W)
        self.status_label.grid(row=0, column=0, sticky="ew", padx=10)
        db_status = "Connected" if self.db_manager.is_connected() else "Disconnected"
        self.db_status_label = tk.Label(self.status_frame, text=f"DB: {db_status}",
                                      font=('Segoe UI', 10),
                                      bg='#34495e', fg='#2ecc71' if self.db_manager.is_connected() else '#e74c3c')
        self.db_status_label.grid(row=0, column=1, sticky="e", padx=10)
    
    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def load_menu_from_database(self):
        try:
            if not self.db_manager.is_connected():
                self.load_sample_menu()
                return
            menu_data = self.db_manager.get_all_menu_items()
            self.menu_items = {}
            for item in menu_data:
                category = item.get('category', 'other')
                if category not in self.menu_items:
                    self.menu_items[category] = []
                self.menu_items[category].append(item)
            if not self.menu_items:
                self.load_sample_menu()
                return
            self.update_all_displays()
        except Exception as e:
            print(f"Database menu loading failed: {e}")
            self.load_sample_menu()
    
    def load_sample_menu(self):
        self.menu_items = {
            'drinks': [
                {'name': 'Espresso', 'price': 2.50, 'description': 'Rich and strong coffee', 'available': True, 'id': 1},
                {'name': 'Cappuccino', 'price': 3.50, 'description': 'Coffee with steamed milk foam', 'available': True, 'id': 2},
                {'name': 'Latte', 'price': 4.00, 'description': 'Coffee with steamed milk', 'available': True, 'id': 3},
                {'name': 'Americano', 'price': 3.00, 'description': 'Espresso with hot water', 'available': True, 'id': 4},
                {'name': 'Hot Chocolate', 'price': 3.25, 'description': 'Rich chocolate drink', 'available': True, 'id': 5},
                {'name': 'Green Tea', 'price': 2.75, 'description': 'Fresh green tea', 'available': True, 'id': 6}
            ],
            'main_courses': [
                {'name': 'Grilled Chicken', 'price': 15.99, 'description': 'Seasoned grilled chicken breast', 'available': True, 'id': 7},
                {'name': 'Pasta Carbonara', 'price': 12.50, 'description': 'Creamy pasta with bacon', 'available': True, 'id': 8},
                {'name': 'Caesar Salad', 'price': 8.99, 'description': 'Fresh romaine with caesar dressing', 'available': True, 'id': 9},
                {'name': 'Fish & Chips', 'price': 14.75, 'description': 'Battered fish with crispy fries', 'available': True, 'id': 10},
                {'name': 'Burger Deluxe', 'price': 13.00, 'description': 'Premium beef burger with sides', 'available': True, 'id': 11}
            ],
            'desserts': [
                {'name': 'Chocolate Cake', 'price': 4.99, 'description': 'Moist chocolate cake with frosting', 'available': True, 'id': 12},
                {'name': 'Cheesecake', 'price': 5.99, 'description': 'Creamy New York style cheesecake', 'available': True, 'id': 13},
                {'name': 'Red Velvet', 'price': 5.49, 'description': 'Classic red velvet with cream cheese', 'available': True, 'id': 14},
                {'name': 'Tiramisu', 'price': 6.49, 'description': 'Italian coffee-flavored dessert', 'available': True, 'id': 15},
                {'name': 'Ice Cream', 'price': 3.99, 'description': 'Vanilla, chocolate, or strawberry', 'available': True, 'id': 16}
            ],
            'appetizers': [
                {'name': 'Bruschetta', 'price': 6.99, 'description': 'Toasted bread with tomatoes', 'available': True, 'id': 17},
                {'name': 'Mozzarella Sticks', 'price': 7.99, 'description': 'Fried cheese with marinara', 'available': True, 'id': 18},
                {'name': 'Buffalo Wings', 'price': 9.99, 'description': 'Spicy wings with ranch dressing', 'available': True, 'id': 19},
                {'name': 'Loaded Nachos', 'price': 8.49, 'description': 'Tortilla chips with cheese and jalapeños', 'available': True, 'id': 20}
            ]
            
        }
        
        self.update_all_displays()
    
    def update_all_displays(self):
        print("DEBUG: Updating all displays")
        self.populate_order_menu()
        self.populate_menu_management()
        self.refresh_customers()
        if hasattr(self, 'analytics_manager') and self.analytics_manager:
            self.analytics_manager.refresh_data()
            if hasattr(self, 'analytics_display') and self.analytics_display:
                self.analytics_display.refresh_display()
    
    def populate_order_menu(self):
        if not hasattr(self, 'menu_notebook') or not self.menu_notebook:
            return
        for tab in self.menu_notebook.tabs():
            self.menu_notebook.forget(tab)
        self.menu_tab_frames = {}
        self.item_vars = {}
        self.item_entries = {}
        for category, items in self.menu_items.items():
            self.create_order_menu_tab(category, items)
    
    def create_order_menu_tab(self, category, items):
        tab_frame = tk.Frame(self.menu_notebook, bg='#f8f9fa')
        self.menu_notebook.add(tab_frame, text=category.replace('_', ' ').title())
        self.menu_tab_frames[category] = tab_frame
        canvas = tk.Canvas(tab_frame, bg='#f8f9fa', height=300)
        scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        ) 
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        row = 0
        for item in items:
            item_name = item['name']
            item_price = item.get('price', 0)
            item_desc = item.get('description', '')
            item_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RIDGE, bd=1)
            item_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
            scrollable_frame.grid_columnconfigure(0, weight=1)
            item_frame.grid_columnconfigure(1, weight=1)
            var = tk.BooleanVar()
            self.item_vars[item_name] = var
            check = tk.Checkbutton(item_frame, variable=var, bg='white',
                                 command=self.calculate_total)
            check.grid(row=0, column=0, padx=5, pady=5)
            details_frame = tk.Frame(item_frame, bg='white')
            details_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
            details_frame.grid_columnconfigure(0, weight=1)
            name_price = f"{item_name} - ${item_price:.2f}"
            tk.Label(details_frame, text=name_price, font=('Segoe UI', 11, 'bold'),
                    bg='white', fg='#2c3e50').grid(row=0, column=0, sticky="w")
            if item_desc:
                tk.Label(details_frame, text=item_desc, font=('Segoe UI', 9),
                        bg='white', fg='#7f8c8d', wraplength=200).grid(row=1, column=0, sticky="w")
            qty_frame = tk.Frame(item_frame, bg='white')
            qty_frame.grid(row=0, column=2, padx=5, pady=5)
            
            tk.Label(qty_frame, text="Qty:", font=('Segoe UI', 9),
                    bg='white').pack(side='left')
            qty_entry = tk.Entry(qty_frame, width=5, font=('Segoe UI', 9))
            qty_entry.insert(0, "1")
            qty_entry.bind('<KeyRelease>', lambda e: self.calculate_total())
            qty_entry.pack(side='left', padx=2)
            self.item_entries[item_name] = qty_entry
            
            row += 1
    
    def create_menu_category_tab(self, category, items):
        tab_frame = tk.Frame(self.menu_notebook, bg='#f8f9fa')
        self.menu_notebook.add(tab_frame, text=category.title())
        self.menu_tab_frames[category] = tab_frame
        canvas = tk.Canvas(tab_frame, bg='#f8f9fa')
        scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        for i, item in enumerate(items):
            self.create_menu_item_widget(scrollable_frame, item, i)
    
    def create_menu_item_widget(self, parent, item, row):
        item_frame = tk.Frame(parent, bg='#ffffff', relief=tk.RIDGE, bd=1)
        item_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        parent.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=1)
        item_name = item.get('name', 'Unknown Item')
        var = tk.BooleanVar()
        self.item_vars[item_name] = var
        
        checkbox = tk.Checkbutton(item_frame, variable=var,
                                command=lambda: self.toggle_item(item_name),
                                bg='#ffffff', font=('Segoe UI', 10))
        checkbox.grid(row=0, column=0, padx=5, pady=5)
        details_frame = tk.Frame(item_frame, bg='#ffffff')
        details_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        details_frame.grid_columnconfigure(0, weight=1)
        name_price_frame = tk.Frame(details_frame, bg='#ffffff')
        name_price_frame.grid(row=0, column=0, sticky="ew")
        name_price_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(name_price_frame, text=item_name,
                font=('Segoe UI', 11, 'bold'), bg='#ffffff',
                anchor="w").grid(row=0, column=0, sticky="ew")
        
        tk.Label(name_price_frame, text=f"${item.get('price', 0.00):.2f}",
                font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#27ae60',
                anchor="e").grid(row=0, column=1, sticky="e")
        description = item.get('description', '')
        if description:
            tk.Label(details_frame, text=description[:100] + "..." if len(description) > 100 else description,
                    font=('Segoe UI', 9), bg='#ffffff', fg='#7f8c8d',
                    anchor="w", justify="left").grid(row=1, column=0, sticky="ew")
        qty_frame = tk.Frame(item_frame, bg='#ffffff')
        qty_frame.grid(row=0, column=2, padx=5, pady=5)
        
        tk.Label(qty_frame, text="Qty:", bg='#ffffff',
                font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        qty_var = tk.StringVar(value="1")
        self.item_entries[item_name] = qty_var
        
        qty_entry = tk.Entry(qty_frame, textvariable=qty_var, width=5,
                           font=('Segoe UI', 10), justify='center')
        qty_entry.pack(side=tk.LEFT, padx=(2, 0))
    
    def toggle_item(self, item_name):
        if self.item_vars[item_name].get():
            self.update_status(f"Added {item_name} to order")
        else:
            self.update_status(f"Removed {item_name} from order")

    def calculate_total(self):
        try:
            subtotal = 0.0
            cost_of_drinks = 0.0
            cost_of_cakes = 0.0
            for item_name, var in self.item_vars.items():
                if var.get():  
                    try:
                        qty = int(self.item_entries[item_name].get() or 1)
                        for category, items in self.menu_items.items():
                            for item in items:
                                if item['name'] == item_name:
                                    price = float(item.get('price', 0))
                                    item_total = price * qty
                                    subtotal += item_total
                                    
                    except (ValueError, TypeError):
                        continue
        
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error calculating totals: {e}")