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