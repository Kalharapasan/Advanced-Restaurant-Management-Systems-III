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