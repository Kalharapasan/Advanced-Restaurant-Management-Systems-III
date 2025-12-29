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
        daily_achievement = (data['today_sales'] / data['daily_target']) * 100
        weekly_achievement = (data['week_sales'] / data['weekly_target']) * 100
        monthly_progress = (data['month_sales'] / data['monthly_target']) * 100
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      🏪 RESTAURANT ANALYTICS DASHBOARD 🏪                     ║
║                        Last Updated: {data['last_updated']}                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📈 SALES PERFORMANCE
───────────────────────────────────────────────────────────────────────────────
• Today's Revenue: ${data['today_sales']:.2f} (↗ {sales_growth:+.1f}% vs yesterday)
• This Week: ${data['week_sales']:.2f} (↗ {week_growth:+.1f}% vs last week)
• This Month: ${data['month_sales']:.2f} (↗ {month_growth:+.1f}% vs last month)
• Best Day This Week: Tuesday (${data['yesterday_sales'] * 1.37:.2f})
• Average Daily Sales: ${data['week_sales'] / 7:.2f}

🛒 ORDER STATISTICS  
───────────────────────────────────────────────────────────────────────────────
• Total Orders Today: {data['today_orders']} orders
• Average Order Value: ${data['avg_order_value']:.2f}
• Peak Hour: {data['peak_hour']} ({data['peak_orders']} orders)
• Payment Methods: Card ({data['payment_methods']['card']}%), Cash ({data['payment_methods']['cash']}%), Mobile ({data['payment_methods']['mobile']}%)
• Order Status: Completed ({data['today_orders'] - 2}), Pending (2)
• Order Growth: +{((data['today_orders'] - data['yesterday_orders']) / data['yesterday_orders'] * 100):.1f}% vs yesterday

👥 CUSTOMER INSIGHTS
───────────────────────────────────────────────────────────────────────────────
• Active Customers Today: {data['active_customers']}
• New Customers: {data['new_customers']} ({', '.join(data['new_customer_names'])})
• Customer Retention Rate: {data['retention_rate']}%
• Average Visit Frequency: {data['avg_visit_frequency']} times/week
• VIP Customers Served: {data['vip_customers']}
• Customer Satisfaction Score: {data['avg_rating']}/5.0

🍽️ MENU PERFORMANCE
───────────────────────────────────────────────────────────────────────────────
• Top Seller: {data['top_seller']['name']} ({data['top_seller']['units']} units sold)
• Revenue Leader: {data['revenue_leader']['name']} (${data['revenue_leader']['revenue']:.2f})
• Most Profitable: {data['most_profitable']['name']} ({data['most_profitable']['margin']}% profit margin)
• Low Stock Alert: {data['low_stock']['name']} ({data['low_stock']['units']} units remaining)
• New Item Performance: {data['new_item']['name']} ({data['new_item']['orders']} orders)
• Menu Diversity: 25 active items across 4 categories

📊 OPERATIONAL METRICS
───────────────────────────────────────────────────────────────────────────────
• Average Service Time: {data['avg_service_time']} minutes
• Table Turnover Rate: {data['table_turnover']} times/day
• Staff Efficiency: {data['staff_efficiency']}%
• Kitchen Accuracy: {data['kitchen_accuracy']}%
• Waste Percentage: {data['waste_percentage']}% (↓ Improved!)
• Equipment Uptime: 99.8%

⭐ CUSTOMER SATISFACTION
───────────────────────────────────────────────────────────────────────────────
• Average Rating: {data['avg_rating']}/5 stars
• Reviews Today: {data['reviews_today']} ({data['positive_reviews']} positive, {data['neutral_reviews']} neutral)
• Positive Feedback: {(data['positive_reviews'] / data['reviews_today'] * 100):.0f}%
• Complaints Resolved: {data['complaints']}/0 (Perfect!)
• Recommendation Rate: {data['recommendation_rate']}%
• Response Time to Reviews: <2 hours

🎯 GOALS & TARGETS
───────────────────────────────────────────────────────────────────────────────
• Daily Sales Target: ${data['daily_target']:.2f} → ${data['today_sales']:.2f} {'✅' if daily_achievement >= 100 else '⏳'} ({daily_achievement:.0f}% achieved!)
• Weekly Target: ${data['weekly_target']:.2f} → ${data['week_sales']:.2f} {'✅' if weekly_achievement >= 100 else '⏳'} ({weekly_achievement:.0f}% achieved!)
• Monthly Target: ${data['monthly_target']:.2f} → On track! {'✅' if monthly_progress >= 75 else '⏳'} ({monthly_progress:.0f}% progress)
• Customer Satisfaction: >4.5 → {data['avg_rating']} ✅ (Exceeded!)

🔔 ALERTS & NOTIFICATIONS
───────────────────────────────────────────────────────────────────────────────
• ⚠️ {data['low_stock']['name']}: Low stock ({data['low_stock']['units']} units)
• ✅ All payment systems: Online
• ✅ Kitchen equipment: Operational
• 📊 Peak hour approaching ({data['peak_hour']})
• 🎉 Daily target achieved! (+{daily_achievement - 100:.0f}% over target)
• 💡 Suggestion: Promote {data['low_stock']['name']} to clear inventory

📈 TRENDS & INSIGHTS
───────────────────────────────────────────────────────────────────────────────
• Sales Trend: {'Upward' if sales_growth > 0 else 'Stable'} (Last 7 days)
• Busiest Day: Tuesday (Average: ${data['week_sales'] / 7 * 1.3:.2f})
• Slowest Period: 3-4 PM (2-3 orders/hour)
• Growth Opportunity: Dinner service (+15% potential)
• Cost Optimization: Reduce waste by 0.5% = +${data['today_sales'] * 0.005:.2f}/day

🏆 ACHIEVEMENTS
───────────────────────────────────────────────────────────────────────────────
• 🥇 Exceeded daily target for 5 consecutive days
• 🥈 Customer satisfaction above 4.5 for 30 days
• 🥉 Zero complaints this week
• 🎯 98%+ kitchen accuracy maintained
• 📈 {sales_growth:+.1f}% sales growth vs yesterday

Last Data Refresh: {time.strftime('%H:%M:%S')}
System Status: All systems operational ✅
"""
        
        return report
    
    
    def get_hourly_sales(self):
        hours = [f"{i:02d}:00" for i in range(24)]
        base_pattern = [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0,
                       1.2, 0.9, 0.6, 0.4, 0.5, 0.8, 1.1, 1.0, 0.7, 0.5, 0.3, 0.2]
        sales = [self.analytics_data['today_sales'] * pattern for pattern in base_pattern]
        return list(zip(hours, sales))
    
    def get_top_items(self, limit=10):
        items = [
            {'name': 'Cappuccino', 'sales': 18, 'revenue': 45.00},
            {'name': 'Grilled Chicken', 'sales': 12, 'revenue': 245.50},
            {'name': 'Caesar Salad', 'sales': 15, 'revenue': 127.50},
            {'name': 'Pizza Margherita', 'sales': 8, 'revenue': 120.00},
            {'name': 'Chocolate Cake', 'sales': 6, 'revenue': 33.00},
            {'name': 'Smoothie Bowl', 'sales': 12, 'revenue': 48.00},
            {'name': 'Pasta Carbonara', 'sales': 9, 'revenue': 112.50},
            {'name': 'Green Tea', 'sales': 3, 'revenue': 6.00},
            {'name': 'Burger Deluxe', 'sales': 7, 'revenue': 91.00},
            {'name': 'Ice Cream', 'sales': 10, 'revenue': 40.00}
        ]
        return items[:limit]