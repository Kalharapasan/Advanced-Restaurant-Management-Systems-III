import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from PIL import Image, ImageTk
import os

class MenuManager:
    
    
    def setup_menu_interface(self):
        self.parent_frame.grid_rowconfigure(0, weight=1)
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.paned_window = ttk.PanedWindow(self.parent_frame, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.setup_menu_list_panel()
        self.setup_menu_details_panel()
    
    def setup_menu_list_panel(self):
        left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(left_frame, weight=1)
        header_frame = ttk.Frame(left_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="🍽️ Menu Management", 
                 font=('Segoe UI', 14, 'bold')).pack(side=tk.LEFT)
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=(0, 5))
        self.category_filter = ttk.Combobox(filter_frame, width=12, state="readonly")
        self.category_filter.pack(side=tk.LEFT, padx=(0, 10))
        self.category_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=15)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        ttk.Button(filter_frame, text="🔍", 
                  command=self.search_menu_items).pack(side=tk.LEFT, padx=2)
        ttk.Button(filter_frame, text="🔄", 
                  command=self.refresh_menu_list).pack(side=tk.LEFT, padx=2)
        
        action_frame = ttk.Frame(left_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(action_frame, text="➕ Add Item", 
                  command=self.add_new_menu_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="✏️ Edit Item", 
                  command=self.edit_selected_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="🗑️ Delete Item", 
                  command=self.delete_selected_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="📋 Duplicate", 
                  command=self.duplicate_selected_item).pack(side=tk.LEFT, padx=2)
        
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('Name', 'Category', 'Price', 'Cost', 'Margin', 'Available', 'Vegetarian')
        self.menu_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        column_widths = {'Name': 150, 'Category': 100, 'Price': 70, 'Cost': 70,'Margin': 70, 'Available': 70, 'Vegetarian': 80}
        
        for col in columns:
            self.menu_tree.heading(col, text=col, anchor=tk.CENTER)
            self.menu_tree.column(col, width=column_widths[col], anchor=tk.CENTER)
            
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                   command=self.menu_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, 
                                   command=self.menu_tree.xview)
        
        self.menu_tree.configure(yscrollcommand=v_scrollbar.set, 
                                xscrollcommand=h_scrollbar.set)
        
        self.menu_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        self.menu_tree.bind('<<TreeviewSelect>>', self.on_menu_item_select)
        self.menu_tree.bind('<Double-1>', self.edit_selected_item)
        
        stats_frame = ttk.LabelFrame(left_frame, text="📊 Menu Statistics")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="Loading statistics...")
        self.stats_label.pack(pady=10)
        
        import_export_frame = ttk.Frame(left_frame)
        import_export_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(import_export_frame, text="📥 Import CSV", 
                  command=self.import_menu_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(import_export_frame, text="📤 Export CSV", 
                  command=self.export_menu_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(import_export_frame, text="🖨️ Print Menu", 
                  command=self.print_menu).pack(side=tk.LEFT, padx=2)
    
    def setup_menu_details_panel(self):
        right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(right_frame, weight=1)
        self.details_notebook = ttk.Notebook(right_frame)
        self.details_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.details_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(self.details_frame, text="📝 Item Details")
        self.pricing_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(self.pricing_frame, text="💰 Pricing")
        self.nutrition_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(self.nutrition_frame, text="🥗 Nutrition")
        
        self.setup_details_tab()
        self.setup_pricing_tab()
        self.setup_nutrition_tab()
    
    def setup_details_tab(self):
        """Setup item details tab"""
           