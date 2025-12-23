import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import json
from datetime import datetime, date

class CustomerManager:
    
    
    def setup_customer_interface(self):
        self.parent_frame.grid_rowconfigure(0, weight=1)
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.paned_window = ttk.PanedWindow(self.parent_frame, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.setup_customer_list_panel()
        self.setup_customer_details_panel()
    
    def setup_customer_list_panel(self):
        left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(left_frame, weight=1)
        header_frame = ttk.Frame(left_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="👥 Customer Database", 
                 font=('Segoe UI', 14, 'bold')).pack(side=tk.LEFT)
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        ttk.Button(search_frame, text="🔍 Search", 
                  command=self.search_customers).pack(side=tk.LEFT, padx=2)
        ttk.Button(search_frame, text="🔄 Refresh", 
                  command=self.refresh_customer_list).pack(side=tk.LEFT, padx=2)
        
        action_frame = ttk.Frame(left_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(action_frame, text="➕ Add Customer", 
                  command=self.add_new_customer).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="✏️ Edit Customer", 
                  command=self.edit_selected_customer).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="📊 View Orders", 
                  command=self.view_customer_orders).pack(side=tk.LEFT, padx=2)
        
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('ID', 'Name', 'Phone', 'Email', 'Orders', 'Spent', 'Loyalty', 'Tier')
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        column_widths = {'ID': 80, 'Name': 120, 'Phone': 100, 'Email': 150, 
                        'Orders': 60, 'Spent': 80, 'Loyalty': 60, 'Tier': 80}
        
        for col in columns:
            self.customer_tree.heading(col, text=col, anchor=tk.CENTER)
            self.customer_tree.column(col, width=column_widths[col], anchor=tk.CENTER)
            
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                   command=self.customer_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, 
                                   command=self.customer_tree.xview)
        
        self.customer_tree.configure(yscrollcommand=v_scrollbar.set, 
                                    xscrollcommand=h_scrollbar.set)
        
        self.customer_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        self.customer_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        self.customer_tree.bind('<Double-1>', self.edit_selected_customer)
        
        stats_frame = ttk.LabelFrame(left_frame, text="📈 Quick Stats")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="Select a customer to view details")
        self.stats_label.pack(pady=10)
    
    def setup_customer_details_panel(self):
        right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(right_frame, weight=1)
        self.details_notebook = ttk.Notebook(right_frame)
        self.details_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.info_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(self.info_frame, text="👤 Customer Info")
        self.history_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(self.history_frame, text="📋 Order History")
        self.loyalty_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(self.loyalty_frame, text="⭐ Loyalty")
        self.setup_customer_info_tab()
        self.setup_order_history_tab()
        self.setup_loyalty_tab()
    
    def setup_customer_info_tab(self):
        canvas = tk.Canvas(self.info_frame)
        scrollbar = ttk.Scrollbar(self.info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        personal_frame = ttk.LabelFrame(scrollable_frame, text="Personal Information")
        personal_frame.pack(fill=tk.X, padx=10, pady=5)
        self.customer_fields = {}
        ttk.Label(personal_frame, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.customer_fields['customer_id'] = ttk.Label(personal_frame, text="", font=('Segoe UI', 9, 'bold'))
        self.customer_fields['customer_id'].grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(personal_frame, text="Full Name:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.customer_fields['name'] = ttk.Entry(personal_frame, width=25)
        self.customer_fields['name'].grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        ttk.Label(personal_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.customer_fields['phone'] = ttk.Entry(personal_frame, width=15)
        self.customer_fields['phone'].grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(personal_frame, text="Email:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.customer_fields['email'] = ttk.Entry(personal_frame, width=25)
        self.customer_fields['email'].grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        ttk.Label(personal_frame, text="Date of Birth:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.customer_fields['date_of_birth'] = DateEntry(personal_frame, width=12, 
                                                         background='darkblue',
                                                         foreground='white', 
                                                         borderwidth=2,
                                                         year=1990)
        self.customer_fields['date_of_birth'].grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(personal_frame, text="Gender:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.customer_fields['gender'] = ttk.Combobox(personal_frame, width=10, 
                                                     values=['Male', 'Female', 'Other'])
        self.customer_fields['gender'].grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)
        ttk.Label(personal_frame, text="Address:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.customer_fields['address'] = tk.Text(personal_frame, width=50, height=3)
        self.customer_fields['address'].grid(row=3, column=1, columnspan=3, sticky=tk.W, padx=5, pady=2)
        pref_frame = ttk.LabelFrame(scrollable_frame, text="Preferences & Settings")
        pref_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(pref_frame, text="Preferred Payment:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.customer_fields['preferred_payment'] = ttk.Combobox(pref_frame, width=15,
                                                               values=['Cash', 'Card', 'Digital'])
        self.customer_fields['preferred_payment'].grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(pref_frame, text="Dietary Preferences:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        dietary_frame = ttk.Frame(pref_frame)
        dietary_frame.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=5, pady=2)
        
        self.dietary_vars = {}
        dietary_options = ['Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free']
        
        for i, option in enumerate(dietary_options):
            var = tk.BooleanVar()
            self.dietary_vars[option.lower().replace('-', '_')] = var
            ttk.Checkbutton(dietary_frame, text=option, variable=var).grid(row=0, column=i, padx=5)
        
        notes_frame = ttk.LabelFrame(scrollable_frame, text="Notes")
        notes_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.customer_fields['notes'] = tk.Text(notes_frame, width=50, height=4)
        self.customer_fields['notes'].pack(fill=tk.X, padx=5, pady=5)
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="💾 Save Changes", 
                  command=self.save_customer_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self.refresh_customer_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📧 Send Email", 
                  command=self.send_customer_email).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📱 Send SMS", 
                  command=self.send_customer_sms).pack(side=tk.LEFT, padx=5)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_order_history_tab(self):
        columns = ('Receipt', 'Date', 'Time', 'Items', 'Total', 'Status')
        self.order_tree = ttk.Treeview(self.history_frame, columns=columns, show='headings')
        
        for col in columns:
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, width=120)
        
        order_v_scroll = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL, 
                                      command=self.order_tree.yview)
        order_h_scroll = ttk.Scrollbar(self.history_frame, orient=tk.HORIZONTAL, 
                                      command=self.order_tree.xview)
        
        self.order_tree.configure(yscrollcommand=order_v_scroll.set, 
                                 xscrollcommand=order_h_scroll.set)
        self.order_tree.grid(row=0, column=0, sticky="nsew")
        order_v_scroll.grid(row=0, column=1, sticky="ns")
        order_h_scroll.grid(row=1, column=0, sticky="ew")
        
        self.history_frame.grid_rowconfigure(0, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)
        
        summary_frame = ttk.Frame(self.history_frame)
        summary_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.order_summary_label = ttk.Label(summary_frame, 
                                           text="Select a customer to view order history")
        self.order_summary_label.pack()
    
    def setup_loyalty_tab(self):
        overview_frame = ttk.LabelFrame(self.loyalty_frame, text="Loyalty Overview")
        overview_frame.pack(fill=tk.X, padx=10, pady=5)
        self.loyalty_fields = {}
        ttk.Label(overview_frame, text="Current Tier:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.loyalty_fields['tier'] = ttk.Label(overview_frame, text="", font=('Segoe UI', 10, 'bold'))
        self.loyalty_fields['tier'].grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(overview_frame, text="Loyalty Points:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.loyalty_fields['points'] = ttk.Label(overview_frame, text="", font=('Segoe UI', 10, 'bold'))
        self.loyalty_fields['points'].grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        ttk.Label(overview_frame, text="Total Orders:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.loyalty_fields['total_orders'] = ttk.Label(overview_frame, text="")
        self.loyalty_fields['total_orders'].grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(overview_frame, text="Total Spent:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.loyalty_fields['total_spent'] = ttk.Label(overview_frame, text="")
        self.loyalty_fields['total_spent'].grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        benefits_frame = ttk.LabelFrame(self.loyalty_frame, text="Tier Benefits")
        benefits_frame.pack(fill=tk.X, padx=10, pady=5)
        self.benefits_text = tk.Text(benefits_frame, height=8, wrap=tk.WORD)
        self.benefits_text.pack(fill=tk.X, padx=5, pady=5)
        points_mgmt_frame = ttk.LabelFrame(self.loyalty_frame, text="Points Management")
        points_mgmt_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(points_mgmt_frame, text="Adjust Points:").pack(side=tk.LEFT, padx=5)
        self.points_adjustment = ttk.Entry(points_mgmt_frame, width=10)
        self.points_adjustment.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(points_mgmt_frame, text="Add Points", 
                  command=self.add_loyalty_points).pack(side=tk.LEFT, padx=2)
        ttk.Button(points_mgmt_frame, text="Deduct Points", 
                  command=self.deduct_loyalty_points).pack(side=tk.LEFT, padx=2)
    
    def refresh_customer_list(self):
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        customers = self.db_manager.get_all_customers()
        
        for customer in customers:
            (id, customer_id, name, phone, email, total_orders, 
             total_spent, loyalty_points, loyalty_tier, last_visit, is_active) = customer
            
            formatted_spent = f"£{float(total_spent or 0):.2f}"
            
            self.customer_tree.insert('', 'end', values=(
                customer_id or f"CUST{id:06d}",
                name or "N/A",
                phone or "N/A", 
                email or "N/A",
                total_orders or 0,
                formatted_spent,
                loyalty_points or 0,
                loyalty_tier or "Bronze"
            ), tags=(id,))
        total_customers = len(customers)
        active_customers = sum(1 for c in customers if c[10])  # is_active
        self.stats_label.config(text=f"Total Customers: {total_customers} | Active: {active_customers}")