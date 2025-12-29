import time
import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime, timedelta

class AnalyticsManager:
    def refresh_data(self):
        try:
            if self.db_manager:
                self.load_real_data()
            else:
                self.generate_sample_data()
        except Exception as e:
            print(f"Error loading analytics data: {e}")
            self.generate_sample_data()
    
    def load_real_data(self):
        self.generate_sample_data()