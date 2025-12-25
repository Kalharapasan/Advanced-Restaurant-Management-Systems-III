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
        