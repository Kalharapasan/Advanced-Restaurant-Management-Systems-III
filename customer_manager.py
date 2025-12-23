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