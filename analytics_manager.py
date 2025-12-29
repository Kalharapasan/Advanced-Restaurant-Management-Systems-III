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
    
    def generate_sample_data(self):
        current_time = datetime.now()
        self.analytics_data = {
            'today_sales': 1547.82,
            'yesterday_sales': 1378.45,
            'week_sales': 8945.75,
            'last_week_sales': 8256.30,
            'month_sales': 35784.50,
            'last_month_sales': 31056.75,
            
            'today_orders': 23,
            'yesterday_orders': 19,
            'avg_order_value': 67.30,
            'peak_hour': '12:00-13:00',
            'peak_orders': 9,
            
            'active_customers': 18,
            'new_customers': 3,
            'new_customer_names': ['John Doe', 'Sarah Wilson', 'Mike Johnson'],
            'retention_rate': 78,
            'avg_visit_frequency': 2.3,
            'vip_customers': 5,
            
            'top_seller': {'name': 'Cappuccino', 'units': 18},
            'revenue_leader': {'name': 'Grilled Chicken', 'revenue': 245.50},
            'most_profitable': {'name': 'Caesar Salad', 'margin': 85},
            'low_stock': {'name': 'Green Tea', 'units': 2},
            'new_item': {'name': 'Smoothie Bowl', 'orders': 12},
            
            'avg_service_time': 4.2,
            'table_turnover': 2.8,
            'staff_efficiency': 94,
            'kitchen_accuracy': 98.5,
            'waste_percentage': 2.1,
            
            'avg_rating': 4.8,
            'reviews_today': 12,
            'positive_reviews': 11,
            'neutral_reviews': 1,
            'complaints': 0,
            'recommendation_rate': 89,
            
            'daily_target': 1200,
            'weekly_target': 8500,
            'monthly_target': 32000,
            
            'payment_methods': {
                'card': 65,
                'cash': 30,
                'mobile': 5
            },
            
            'last_updated': current_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_card_data(self):
        return [
            ("📈 Today's Sales", f"${self.analytics_data['today_sales']:.2f}", "#27ae60"),
            ("🛒 Total Orders", str(self.analytics_data['today_orders']), "#3498db"),
            ("👥 Customers", str(self.analytics_data['active_customers']), "#9b59b6"),
            ("⭐ Avg Rating", str(self.analytics_data['avg_rating']), "#f39c12")
        ]
    
    def get_detailed_report(self):
        data = self.analytics_data
        sales_growth = ((data['today_sales'] - data['yesterday_sales']) / data['yesterday_sales']) * 100
        week_growth = ((data['week_sales'] - data['last_week_sales']) / data['last_week_sales']) * 100
        month_growth = ((data['month_sales'] - data['last_month_sales']) / data['last_month_sales']) * 100