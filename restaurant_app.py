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