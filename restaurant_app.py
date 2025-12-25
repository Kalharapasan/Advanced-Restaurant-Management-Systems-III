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