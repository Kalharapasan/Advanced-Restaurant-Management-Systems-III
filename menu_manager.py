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
    
    def update_menu_statistics(self):
        try:
            menu_items = self.db_manager.get_all_menu_items()
            
            total_items = len(menu_items)
            available_items = sum(1 for item in menu_items if item[13]) 
            categories = len(set(item[2] for item in menu_items)) 
            
            avg_price = sum(float(item[3] or 0) for item in menu_items) / total_items if total_items > 0 else 0
            
            stats_text = f"Total Items: {total_items} | Available: {available_items} | Categories: {categories} | Avg Price: £{avg_price:.2f}"
            self.stats_label.config(text=stats_text)
            
        except Exception as e:
            self.stats_label.config(text="Error loading statistics")
    
    def on_filter_change(self, event=None):
        self.search_menu_items()
        
    def on_search_change(self, event=None):
        self.parent_frame.after(300, self.search_menu_items)
    
    def search_menu_items(self):
        category = self.category_filter.get()
        search_term = self.search_var.get().strip()
        if category and category != 'All':
            category = category.lower()
        else:
            category = None
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
        
        menu_items = self.db_manager.get_all_menu_items(category, search_term)
        
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
    
    def on_menu_item_select(self, event):
        selection = self.menu_tree.selection()
        if selection:
            item = selection[0]
            item_id = self.menu_tree.item(item, 'tags')[0]
            self.selected_item = item_id
            self.load_menu_item_details(item_id)
    
    def load_menu_item_details(self, item_id):
        if not self.db_manager.is_connected():
            return
        
        try:
            cursor = self.db_manager.get_connection().cursor()
            query = """
            SELECT * FROM menu_items WHERE id = %s
            """
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()
            
            if item:
                self.populate_menu_item_form(item)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load menu item details: {e}")
    
    def populate_menu_item_form(self, item):
        for field_name, field_widget in self.menu_fields.items():
            if hasattr(field_widget, 'delete'):
                if isinstance(field_widget, tk.Text):
                    field_widget.delete("1.0", tk.END)
                else:
                    field_widget.delete(0, tk.END)
            elif hasattr(field_widget, 'set'):
                field_widget.set("")
        
        for var in self.dietary_vars.values():
            var.set(False)
        for var in self.availability_vars.values():
            var.set(False)
        
        field_mapping = {
            1: 'name',
            2: 'category',
            3: 'price',
            4: 'cost_price',
            5: 'description',
            6: 'ingredients', 
            7: 'allergens',
            9: 'preparation_time',
            14: 'spice_level'
        }
        
        for index, field_name in field_mapping.items():
            if item[index] is not None and field_name in self.menu_fields:
                widget = self.menu_fields[field_name]
                value = str(item[index])
                
                if isinstance(widget, tk.Text):
                    widget.insert("1.0", value)
                elif hasattr(widget, 'set'):
                    widget.set(value)
                elif hasattr(widget, 'insert'):
                    widget.insert(0, value)
        if item[10]: 
            self.dietary_vars['is_vegetarian'].set(True)
        if item[11]: 
            self.dietary_vars['is_vegan'].set(True)
        if item[12]:  
            self.dietary_vars['is_gluten_free'].set(True)    
        
        if item[13]:  
            self.availability_vars['is_available'].set(True)
        if item[14]: 
            self.availability_vars['is_active'].set(True)
        
        self.update_pricing_analysis()
        
        if item[8]: 
            self.load_nutrition_info(item[8])
    
    def calculate_margin(self, event=None):
        try:
            price = float(self.menu_fields['price'].get() or 0)
            cost = float(self.menu_fields['cost_price'].get() or 0)
            
            self.update_pricing_display(price, cost)
        except ValueError:
            pass
    
    def update_pricing_display(self, price, cost):
        profit = price - cost
        margin = (profit / price * 100) if price > 0 else 0
        
        self.pricing_fields['selling_price'].config(text=f"£{price:.2f}")
        self.pricing_fields['cost_price'].config(text=f"£{cost:.2f}")
        self.pricing_fields['gross_profit'].config(text=f"£{profit:.2f}")
        self.pricing_fields['margin_percent'].config(text=f"{margin:.1f}%")
        
        if margin < 20:
            color = 'red'
        elif margin < 40:
            color = 'orange'
        else:
            color = 'green'
        
        self.pricing_fields['gross_profit'].config(foreground=color)
        self.pricing_fields['margin_percent'].config(foreground=color)
        self.update_pricing_suggestions(price, cost, margin)
    
    def update_pricing_suggestions(self, price, cost, margin):
        self.suggestions_text.delete("1.0", tk.END)
        suggestions = "PRICING ANALYSIS & SUGGESTIONS:\n\n"
        if margin < 20:
            suggestions += "⚠️  LOW MARGIN WARNING!\n"
            suggestions += f"Current margin of {margin:.1f}% is below recommended 20% minimum.\n\n"
        elif margin < 40:
            suggestions += "⚡ MODERATE MARGIN\n"
            suggestions += f"Current margin of {margin:.1f}% is acceptable but could be improved.\n\n"
        else:
            suggestions += "✅ HEALTHY MARGIN\n"
            suggestions += f"Current margin of {margin:.1f}% is excellent!\n\n"
        
        suggestions += "RECOMMENDED ACTIONS:\n\n"
        
        if cost > 0:
            target_margin_price = cost / 0.6  
            optimal_price = cost / 0.5  
            
            suggestions += f"• For 40% margin: £{target_margin_price:.2f}\n"
            suggestions += f"• For 50% margin: £{optimal_price:.2f}\n\n"
        
        suggestions += "MARKET POSITIONING:\n\n"
        if price < 5:
            suggestions += "• BUDGET CATEGORY: Focus on volume and efficiency\n"
        elif price < 15:
            suggestions += "• MID-RANGE CATEGORY: Balance quality and value\n"
        else:
            suggestions += "• PREMIUM CATEGORY: Emphasize quality and experience\n"
        
        suggestions += "\n"
        suggestions += "OPTIMIZATION TIPS:\n"
        suggestions += "• Review ingredient costs regularly\n"
        suggestions += "• Consider portion size adjustments\n"
        suggestions += "• Monitor competitor pricing\n"
        suggestions += "• Track customer price sensitivity\n"
        
        self.suggestions_text.insert("1.0", suggestions)
    
    def update_pricing_analysis(self):
        try:
            price = float(self.menu_fields['price'].get() or 0)
            cost = float(self.menu_fields['cost_price'].get() or 0)
            self.update_pricing_display(price, cost)
        except ValueError:
            pass
    
    def compare_pricing(self):
        try:
            our_price = float(self.menu_fields['price'].get() or 0)
            competitor_price = float(self.competitor_price.get() or 0)
            
            if competitor_price > 0:
                difference = our_price - competitor_price
                percentage = (difference / competitor_price * 100)
                
                comparison_text = f"\nCOMPETITOR COMPARISON:\n\n"
                comparison_text += f"Our Price: £{our_price:.2f}\n"
                comparison_text += f"Competitor: £{competitor_price:.2f}\n"
                comparison_text += f"Difference: £{difference:.2f} ({percentage:+.1f}%)\n\n"
                
                if percentage > 10:
                    comparison_text += "⚠️ We are significantly more expensive\n"
                elif percentage > 0:
                    comparison_text += "💰 We are moderately more expensive\n"
                elif percentage > -10:
                    comparison_text += "✅ Competitive pricing\n"
                else:
                    comparison_text += "💸 We are significantly cheaper\n"
                
                current_text = self.suggestions_text.get("1.0", tk.END)
                self.suggestions_text.insert(tk.END, comparison_text)
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid prices for comparison")
    
    def load_nutrition_info(self, nutrition_json):
        try:
            if isinstance(nutrition_json, str):
                nutrition_data = json.loads(nutrition_json)
            else:
                nutrition_data = nutrition_json
            
            for key, field in self.nutrition_fields.items():
                if key in nutrition_data:
                    field.delete(0, tk.END)
                    field.insert(0, str(nutrition_data[key]))
        except:
            pass
    
    def calculate_nutrition(self):
        messagebox.showinfo("Feature", "Nutrition calculator feature coming soon!")
    
    def add_new_menu_item(self):
        self.menu_item_dialog(title="Add New Menu Item", mode="add")
    
    def edit_selected_item(self, event=None):
        if not self.selected_item:
            messagebox.showwarning("No Selection", "Please select a menu item to edit.")
            return
        
        self.menu_item_dialog(title="Edit Menu Item", mode="edit")
    
    def menu_item_dialog(self, title, mode):
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(title)
        dialog.geometry("800x600")
        dialog.resizable(True, True)
        dialog.configure(bg='#f0f0f0')
        
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (
            dialog.winfo_toplevel().winfo_rootx() + 50,
            dialog.winfo_toplevel().winfo_rooty() + 50
        ))
        
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        basic_tab = ttk.Frame(notebook)
        notebook.add(basic_tab, text="Basic Info")
        advanced_tab = ttk.Frame(notebook)
        notebook.add(advanced_tab, text="Advanced")
        dialog_fields = {}
        self.setup_basic_dialog_tab(basic_tab, dialog_fields)
        self.setup_advanced_dialog_tab(advanced_tab, dialog_fields)
    
    