import mysql.connector
from mysql.connector import Error
import json
import datetime
import hashlib

DB_CONFIG = {
    'host': 'localhost',
    'database': 'restaurant_db',
    'user': 'root',
    'password': 'kalharamax'  
}