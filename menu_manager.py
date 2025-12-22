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
        
        