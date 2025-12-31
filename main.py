#!/usr/bin/env python3
import sys
import tkinter as tk
from tkinter import messagebox
import traceback

def check_dependencies():
    missing_modules = []
    
    try:
        import mysql.connector
    except ImportError:
        missing_modules.append("mysql-connector-python")
    
    try:
        import matplotlib
    except ImportError:
        missing_modules.append("matplotlib")
    
    try:
        import pandas
    except ImportError:
        missing_modules.append("pandas")
    
    try:
        from PIL import Image
    except ImportError:
        missing_modules.append("Pillow")
    
    return missing_modules

def show_dependency_error(missing_modules):
    root = tk.Tk()
    root.title("Missing Dependencies")
    root.geometry("500x300")
    root.configure(bg='#f0f0f0')
    
    error_text = "Missing Required Modules:\n\n"
    error_text += "\n".join(f"• {module}" for module in missing_modules)
    error_text += "\n\nInstall using:\n"
    error_text += f"pip install {' '.join(missing_modules)}"
    error_text += "\n\nThen restart the application."
    
    error_label = tk.Label(root, text=error_text,
                          font=('Segoe UI', 11),
                          bg='#f0f0f0', fg='#e74c3c',
                          justify=tk.LEFT)
    error_label.pack(expand=True, padx=20, pady=20)
    
    install_btn = tk.Button(root, text="Copy Install Command",
                           font=('Segoe UI', 10, 'bold'),
                           bg='#3498db', fg='white',
                           command=lambda: root.clipboard_append(f"pip install {' '.join(missing_modules)}"))
    install_btn.pack(pady=10)
    
    root.mainloop()
    
def main():