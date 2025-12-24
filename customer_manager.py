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
        active_customers = sum(1 for c in customers if c[10]) 
        self.stats_label.config(text=f"Total Customers: {total_customers} | Active: {active_customers}")
    
    def on_search_change(self, event=None):
        self.parent_frame.after(300, self.search_customers)
    
    def search_customers(self):
        search_term = self.search_var.get().strip()
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        customers = self.db_manager.get_all_customers(search_term if search_term else None)
        
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
    
    def on_customer_select(self, event):
        selection = self.customer_tree.selection()
        if selection:
            item = selection[0]
            customer_id = self.customer_tree.item(item, 'tags')[0]
            self.selected_customer = customer_id
            self.load_customer_details(customer_id)
    
    def load_customer_details(self, customer_id):
        if not self.db_manager.is_connected():
            return
        try:
            cursor = self.db_manager.get_connection().cursor()
            query = """
            SELECT * FROM customers WHERE id = %s
            """
            cursor.execute(query, (customer_id,))
            customer = cursor.fetchone()
            
            if customer:
                self.populate_customer_form(customer)
                self.load_customer_orders(customer_id)
                self.load_loyalty_info(customer)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customer details: {e}")
    
    def populate_customer_form(self, customer):
        for field_name, field_widget in self.customer_fields.items():
            if hasattr(field_widget, 'delete'):
                if isinstance(field_widget, tk.Text):
                    field_widget.delete("1.0", tk.END)
                else:
                    field_widget.delete(0, tk.END)
            elif hasattr(field_widget, 'set'):
                field_widget.set("")
            elif hasattr(field_widget, 'config'):
                field_widget.config(text="")
        
        field_mapping = {
            1: 'customer_id',    
            2: 'name',           
            3: 'phone',          
            4: 'email',        
            5: 'address',      
            6: 'date_of_birth', 
            7: 'gender',         
            13: 'preferred_payment',  
            14: 'dietary_preferences',  
            16: 'notes'         
        }
        
        for index, field_name in field_mapping.items():
            value = customer[index] if customer[index] is not None else ""
            
            if field_name in self.customer_fields:
                widget = self.customer_fields[field_name]
                
                if field_name == 'customer_id':
                    widget.config(text=str(value))
                elif field_name == 'date_of_birth' and value:
                    if isinstance(value, str):
                        widget.set_date(datetime.strptime(value, '%Y-%m-%d').date())
                    else:
                        widget.set_date(value)
                elif field_name == 'address' or field_name == 'notes':
                    widget.insert("1.0", str(value))
                elif field_name == 'dietary_preferences':
                    if value:
                        try:
                            prefs = json.loads(value) if isinstance(value, str) else value
                            for pref_key, var in self.dietary_vars.items():
                                var.set(prefs.get(pref_key, False))
                        except:
                            pass
                elif hasattr(widget, 'set'):
                    widget.set(str(value))
                elif hasattr(widget, 'insert'):
                    widget.insert(0, str(value))
    
    def load_customer_orders(self, customer_id):
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        orders = self.db_manager.get_customer_orders(customer_id)
        
        total_orders = len(orders)
        total_value = 0
        
        for order in orders:
            receipt_ref, order_date, order_time, items_json, total_cost, status = order
            try:
                items = json.loads(items_json) if items_json else {}
                item_count = len(items)
            except:
                item_count = 0
            
            total_value += float(total_cost or 0)
            
            self.order_tree.insert('', 'end', values=(
                receipt_ref,
                order_date.strftime('%Y-%m-%d') if order_date else 'N/A',
                order_time.strftime('%H:%M') if order_time else 'N/A',
                f"{item_count} items",
                f"£{float(total_cost or 0):.2f}",
                status
            ))
        avg_order = total_value / total_orders if total_orders > 0 else 0
        self.order_summary_label.config(
            text=f"Total Orders: {total_orders} | Total Value: £{total_value:.2f} | Average Order: £{avg_order:.2f}"
        )
    
    def load_loyalty_info(self, customer):
        loyalty_tier = customer[12] or "Bronze"
        loyalty_points = customer[11] or 0
        total_orders = customer[8] or 0
        total_spent = customer[9] or 0
        self.loyalty_fields['tier'].config(text=loyalty_tier, foreground=self.get_tier_color(loyalty_tier))
        self.loyalty_fields['points'].config(text=str(loyalty_points))
        self.loyalty_fields['total_orders'].config(text=str(total_orders))
        self.loyalty_fields['total_spent'].config(text=f"£{float(total_spent):.2f}")
        benefits = self.get_tier_benefits(loyalty_tier)
        self.benefits_text.delete("1.0", tk.END)
        self.benefits_text.insert("1.0", benefits)
        self.benefits_text.config(state=tk.DISABLED)
    
    def get_tier_benefits(self, tier):
        benefits = {
            'Bronze': """Bronze Tier Benefits:
• Welcome to our loyalty program!
• Earn 1 point per £1 spent
• Birthday discount: 5%
• Special member-only offers

Spend £100 more to reach Silver tier!""",
            
            'Silver': """Silver Tier Benefits:
• Earn 1.5 points per £1 spent
• Birthday discount: 10%
• Priority reservations
• Free appetizer on birthday
• Monthly exclusive offers

Spend £250 more to reach Gold tier!""",
            
            'Gold': """Gold Tier Benefits:
• Earn 2 points per £1 spent
• Birthday discount: 15%
• Complimentary valet parking
• Free dessert with main course
• Early access to new menu items
• Dedicated customer service line

Spend £500 more to reach Platinum tier!""",
            
            'Platinum': """Platinum Tier Benefits:
• Earn 3 points per £1 spent
• Birthday discount: 20%
• Complimentary champagne service
• Private dining room access
• Personal chef consultation
• Annual dining credit: £100
• VIP event invitations"""
        }
        return benefits.get(tier, "No benefits information available.")
    
    def add_new_customer(self):
        self.customer_dialog(title="Add New Customer", mode="add")
    
    def edit_selected_customer(self, event=None):
        if not self.selected_customer:
            messagebox.showwarning("No Selection", "Please select a customer to edit.")
            return
        
        self.customer_dialog(title="Edit Customer", mode="edit")
    
    def customer_dialog(self, title, mode):
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(title)
        dialog.geometry("600x700")
        dialog.resizable(False, False)
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.grab_set()
        dialog.geometry("+%d+%d" % (
            dialog.winfo_toplevel().winfo_rootx() + 50,
            dialog.winfo_toplevel().winfo_rooty() + 50
        ))
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        contact_tab = ttk.Frame(notebook)
        notebook.add(contact_tab, text="Contact & Preferences")
        dialog_fields = {}
        self.setup_personal_tab(personal_tab, dialog_fields)
        self.setup_contact_tab(contact_tab, dialog_fields)
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Save", 
                  command=lambda: self.save_customer_dialog(dialog, dialog_fields, mode)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        if mode == "edit" and self.selected_customer:
            self.populate_dialog_fields(dialog_fields)
    
    def setup_personal_tab(self, parent, fields):
        ttk.Label(parent, text="Full Name *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        fields['name'] = ttk.Entry(parent, width=30)
        fields['name'].grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(parent, text="Phone *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        fields['phone'] = ttk.Entry(parent, width=20)
        fields['phone'].grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(parent, text="Email:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        fields['email'] = ttk.Entry(parent, width=30)
        fields['email'].grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(parent, text="Date of Birth:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        fields['date_of_birth'] = DateEntry(parent, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, year=1990)
        fields['date_of_birth'].grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(parent, text="Gender:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        fields['gender'] = ttk.Combobox(parent, width=15, values=['Male', 'Female', 'Other'])
        fields['gender'].grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(parent, text="Address:").grid(row=5, column=0, sticky=tk.NW, padx=5, pady=5)
        fields['address'] = tk.Text(parent, width=35, height=4)
        fields['address'].grid(row=5, column=1, columnspan=2, padx=5, pady=5)
    
    
    def setup_contact_tab(self, parent, fields):
        ttk.Label(parent, text="Preferred Payment:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        fields['preferred_payment'] = ttk.Combobox(parent, width=15, values=['Cash', 'Card', 'Digital'])
        fields['preferred_payment'].grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(parent, text="Dietary Preferences:").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        dietary_frame = ttk.Frame(parent)
        dietary_frame.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        fields['dietary_vars'] = {}
        dietary_options = ['Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free']
        
        for i, option in enumerate(dietary_options):
            var = tk.BooleanVar()
            fields['dietary_vars'][option.lower().replace('-', '_')] = var
            ttk.Checkbutton(dietary_frame, text=option, variable=var).grid(row=i//3, column=i%3, padx=5, sticky=tk.W)
        
        ttk.Label(parent, text="Notes:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        fields['notes'] = tk.Text(parent, width=35, height=6)
        fields['notes'].grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        ttk.Label(parent, text="* Required fields", font=('Segoe UI', 8), 
                 foreground='red').grid(row=3, column=0, columnspan=3, padx=5, pady=10)

    def populate_dialog_fields(self, fields):
        if not self.selected_customer:
            return
        
        try:
            cursor = self.db_manager.get_connection().cursor()
            cursor.execute("SELECT * FROM customers WHERE id = %s", (self.selected_customer,))
            customer = cursor.fetchone()
            if customer:
                if customer[2]:  
                    fields['name'].insert(0, customer[2])
                if customer[3]:  
                    fields['phone'].insert(0, customer[3])
                if customer[4]: 
                    fields['email'].insert(0, customer[4])
                if customer[5]:  
                    fields['address'].insert("1.0", customer[5])
                if customer[6]:  
                    fields['date_of_birth'].set_date(customer[6])
                if customer[7]:  
                    fields['gender'].set(customer[7])
                if customer[13]:  
                    fields['preferred_payment'].set(customer[13])
                if customer[16]:  
                    fields['notes'].insert("1.0", customer[16])
            if customer[14]:
                    try:
                        prefs = json.loads(customer[14])
                        for pref_key, var in fields['dietary_vars'].items():
                            var.set(prefs.get(pref_key, False))
                    except:
                        pass
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customer data: {e}")
    
    def save_customer_dialog(self, dialog, fields, mode):
        if not fields['name'].get().strip():
            messagebox.showerror("Validation Error", "Name is required.")
            return
        
        if not fields['phone'].get().strip():
            messagebox.showerror("Validation Error", "Phone number is required.")
            return
        
        customer_data = {
            'name': fields['name'].get().strip(),
            'phone': fields['phone'].get().strip(),
            'email': fields['email'].get().strip() or None,
            'address': fields['address'].get("1.0", tk.END).strip() or None,
            'date_of_birth': fields['date_of_birth'].get_date(),
            'gender': fields['gender'].get() or None,
            'preferred_payment': fields['preferred_payment'].get() or None,
            'notes': fields['notes'].get("1.0", tk.END).strip() or None,
            'dietary_preferences': {key: var.get() for key, var in fields['dietary_vars'].items()}
        }
        
        try:
            if mode == "add":
                success = self.db_manager.add_customer(customer_data)
                message = "Customer added successfully!"
            else:
                success = self.db_manager.update_customer(self.selected_customer, customer_data)
                message = "Customer updated successfully!"
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_customer_list()
                if mode == "edit":
                    self.load_customer_details(self.selected_customer)
            else:
                messagebox.showerror("Error", "Failed to save customer.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {e}")
    
    def save_customer_changes(self):
        if not self.selected_customer:
            messagebox.showwarning("No Selection", "Please select a customer first.")
            return

        name = self.customer_fields['name'].get().strip()
        phone = self.customer_fields['phone'].get().strip()
        
        if not name or not phone:
            messagebox.showerror("Validation Error", "Name and phone are required fields.")
            return
        
        customer_data = {
            'name': name,
            'phone': phone,
            'email': self.customer_fields['email'].get().strip() or None,
            'address': self.customer_fields['address'].get("1.0", tk.END).strip() or None,
            'date_of_birth': self.customer_fields['date_of_birth'].get_date(),
            'gender': self.customer_fields['gender'].get() or None,
            'preferred_payment': self.customer_fields['preferred_payment'].get() or None,
            'notes': self.customer_fields['notes'].get("1.0", tk.END).strip() or None,
            'dietary_preferences': {key: var.get() for key, var in self.dietary_vars.items()}
        }
        
        success = self.db_manager.update_customer(self.selected_customer, customer_data)
        
        if success:
            messagebox.showinfo("Success", "Customer updated successfully!")
            self.refresh_customer_list()
        else:
            messagebox.showerror("Error", "Failed to update customer.")
    
    def refresh_customer_details(self):
        if self.selected_customer:
            self.load_customer_details(self.selected_customer)
        
    def view_customer_orders(self):
        if not self.selected_customer:
            messagebox.showwarning("No Selection", "Please select a customer first.")
            return
        self.details_notebook.select(1)
    
    def send_customer_email(self):
        if not self.selected_customer:
            messagebox.showwarning("No Selection", "Please select a customer first.")
            return
        
        email = self.customer_fields['email'].get().strip()
        if not email:
            messagebox.showwarning("No Email", "Customer does not have an email address.")
            return
        messagebox.showinfo("Email", f"Email functionality would send message to: {email}")