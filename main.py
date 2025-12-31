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