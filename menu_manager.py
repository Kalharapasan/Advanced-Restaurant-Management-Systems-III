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
        canvas = tk.Canvas(self.details_frame)
        scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        basic_frame = ttk.LabelFrame(scrollable_frame, text="Basic Information")
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        self.menu_fields = {}
        ttk.Label(basic_frame, text="Item Name *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.menu_fields['name'] = ttk.Entry(basic_frame, width=25)
        self.menu_fields['name'].grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(basic_frame, text="Category *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.menu_fields['category'] = ttk.Combobox(basic_frame, width=15, 
                                                   values=self.db_manager.get_menu_categories())
        self.menu_fields['category'].grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(basic_frame, text="Selling Price (£) *:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.menu_fields['price'] = ttk.Entry(basic_frame, width=12)
        self.menu_fields['price'].grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        self.menu_fields['price'].bind('<KeyRelease>', self.calculate_margin)
        
        ttk.Label(basic_frame, text="Cost Price (£):").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.menu_fields['cost_price'] = ttk.Entry(basic_frame, width=12)
        self.menu_fields['cost_price'].grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)
        self.menu_fields['cost_price'].bind('<KeyRelease>', self.calculate_margin)
        
        ttk.Label(basic_frame, text="Prep Time (min):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.menu_fields['preparation_time'] = ttk.Entry(basic_frame, width=12)
        self.menu_fields['preparation_time'].grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(basic_frame, text="Spice Level:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=2)
        self.menu_fields['spice_level'] = ttk.Combobox(basic_frame, width=12,
                                                      values=['None', 'Mild', 'Medium', 'Hot', 'Very Hot'])
        self.menu_fields['spice_level'].grid(row=3, column=3, sticky=tk.W, padx=5, pady=2)
        
        desc_frame = ttk.LabelFrame(scrollable_frame, text="Description & Details")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(desc_frame, text="Description:").grid(row=0, column=0, sticky=tk.NW, padx=5, pady=2)
        self.menu_fields['description'] = tk.Text(desc_frame, width=50, height=3)
        self.menu_fields['description'].grid(row=0, column=1, columnspan=3, padx=5, pady=2)
        
        ttk.Label(desc_frame, text="Ingredients:").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=2)
        self.menu_fields['ingredients'] = tk.Text(desc_frame, width=50, height=3)
        self.menu_fields['ingredients'].grid(row=1, column=1, columnspan=3, padx=5, pady=2)
        
        ttk.Label(desc_frame, text="Allergens:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=2)
        self.menu_fields['allergens'] = tk.Text(desc_frame, width=50, height=2)
        self.menu_fields['allergens'].grid(row=2, column=1, columnspan=3, padx=5, pady=2)
        
        dietary_frame = ttk.LabelFrame(scrollable_frame, text="Dietary Information")
        dietary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.dietary_vars = {}
        dietary_options = ['is_vegetarian', 'is_vegan', 'is_gluten_free']
        dietary_labels = ['Vegetarian', 'Vegan', 'Gluten Free']
        
        for i, (option, label) in enumerate(zip(dietary_options, dietary_labels)):
            var = tk.BooleanVar()
            self.dietary_vars[option] = var
            ttk.Checkbutton(dietary_frame, text=label, variable=var).grid(row=0, column=i, padx=20, pady=5)
        
        avail_frame = ttk.LabelFrame(scrollable_frame, text="Availability")
        avail_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.availability_vars = {}
        avail_options = ['is_available', 'is_active']
        avail_labels = ['Currently Available', 'Active on Menu']
        
        for i, (option, label) in enumerate(zip(avail_options, avail_labels)):
            var = tk.BooleanVar()
            self.availability_vars[option] = var
            ttk.Checkbutton(avail_frame, text=label, variable=var).grid(row=0, column=i, padx=20, pady=5)
        
        image_frame = ttk.LabelFrame(scrollable_frame, text="Item Image")
        image_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.image_label = ttk.Label(image_frame, text="No image selected")
        self.image_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        ttk.Button(image_frame, text="Select Image", 
                  command=self.select_image).grid(row=1, column=0, padx=5, pady=2)
        ttk.Button(image_frame, text="Remove Image", 
                  command=self.remove_image).grid(row=1, column=1, padx=5, pady=2)
        
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="💾 Save Changes", 
                  command=self.save_menu_item_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self.refresh_menu_item_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Copy to New", 
                  command=self.copy_to_new_item).pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_pricing_tab(self):
        overview_frame = ttk.LabelFrame(self.pricing_frame, text="Pricing Analysis")
        overview_frame.pack(fill=tk.X, padx=10, pady=5)
        self.pricing_fields = {}    
        ttk.Label(overview_frame, text="Selling Price:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.pricing_fields['selling_price'] = ttk.Label(overview_frame, text="£0.00", font=('Segoe UI', 10, 'bold'))
        self.pricing_fields['selling_price'].grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(overview_frame, text="Cost Price:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.pricing_fields['cost_price'] = ttk.Label(overview_frame, text="£0.00")
        self.pricing_fields['cost_price'].grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        ttk.Label(overview_frame, text="Gross Profit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.pricing_fields['gross_profit'] = ttk.Label(overview_frame, text="£0.00", foreground='green')
        self.pricing_fields['gross_profit'].grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(overview_frame, text="Margin %:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.pricing_fields['margin_percent'] = ttk.Label(overview_frame, text="0%", foreground='green')
        self.pricing_fields['margin_percent'].grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        
        suggestions_frame = ttk.LabelFrame(self.pricing_frame, text="Pricing Suggestions")
        suggestions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.suggestions_text = tk.Text(suggestions_frame, height=15, wrap=tk.WORD)
        self.suggestions_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        competitive_frame = ttk.Frame(self.pricing_frame)
        competitive_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(competitive_frame, text="Competitor Price:").pack(side=tk.LEFT, padx=5)
        self.competitor_price = ttk.Entry(competitive_frame, width=10)
        self.competitor_price.pack(side=tk.LEFT, padx=5)
        ttk.Button(competitive_frame, text="Compare", 
                  command=self.compare_pricing).pack(side=tk.LEFT, padx=5)
    
    def setup_nutrition_tab(self):
        nutrition_frame = ttk.LabelFrame(self.nutrition_frame, text="Nutritional Information (per serving)")
        nutrition_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.nutrition_fields = {}
        nutrition_items = [
            ('calories', 'Calories'),
            ('protein', 'Protein (g)'),
            ('carbs', 'Carbohydrates (g)'),
            ('fat', 'Fat (g)'),
            ('fiber', 'Fiber (g)'),
            ('sodium', 'Sodium (mg)')
        ]
        
        for i, (key, label) in enumerate(nutrition_items):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(nutrition_frame, text=f"{label}:").grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            self.nutrition_fields[key] = ttk.Entry(nutrition_frame, width=12)
            self.nutrition_fields[key].grid(row=row, column=col+1, sticky=tk.W, padx=5, pady=2)
  
        labels_frame = ttk.LabelFrame(self.nutrition_frame, text="Dietary Labels")
        labels_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.dietary_labels = tk.Text(labels_frame, height=3, wrap=tk.WORD)
        self.dietary_labels.pack(fill=tk.X, padx=5, pady=5)
        
        calc_frame = ttk.LabelFrame(self.nutrition_frame, text="Nutrition Calculator")
        calc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        calc_text = """Nutrition Calculator:
        
Enter ingredient quantities to automatically calculate nutritional values:
• Use standard measurements (grams, ml, etc.)
• Database contains common ingredients
• Results are estimates for menu planning"""
        
        calc_label = ttk.Label(calc_frame, text=calc_text, justify=tk.LEFT)
        calc_label.pack(padx=10, pady=10)
        
        ttk.Button(calc_frame, text="Calculate Nutrition", 
                  command=self.calculate_nutrition).pack(pady=5)
    
    def refresh_menu_list(self):
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
        menu_items = self.db_manager.get_all_menu_items()
        for item in menu_items:
            (id, name, category, price, cost_price, description, ingredients, allergens,
             prep_time, is_vegetarian, is_vegan, is_gluten_free, spice_level,
             is_available, is_active, popularity_score) = item

            price_val = float(price or 0)
            cost_val = float(cost_price or 0)
            margin = ((price_val - cost_val) / price_val * 100) if price_val > 0 else 0
            
            self.menu_tree.insert('', 'end', values=(
                name,
                category.title(),
                f"£{price_val:.2f}",
                f"£{cost_val:.2f}",
                f"{margin:.1f}%",
                "Yes" if is_available else "No",
                "Yes" if is_vegetarian else "No"
            ), tags=(id,))
        
        categories = ['all'] + self.db_manager.get_menu_categories()
        self.category_filter['values'] = [cat.title() for cat in categories]
        if not self.category_filter.get():
            self.category_filter.set('All')
        
        self.update_menu_statistics()
           