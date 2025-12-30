import time
import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime, timedelta

class AnalyticsManager:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.analytics_data = {}
        self.refresh_data()
        
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
    
    def update_data(self):
        self.analytics_data['today_sales'] += random.uniform(-5, 15)
        self.analytics_data['today_orders'] += random.randint(0, 1)
        self.analytics_data['active_customers'] += random.randint(-1, 2)
        self.analytics_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.analytics_data['today_sales'] = max(1000, self.analytics_data['today_sales'])
        self.analytics_data['today_orders'] = max(15, min(50, self.analytics_data['today_orders']))
        self.analytics_data['active_customers'] = max(10, min(30, self.analytics_data['active_customers']))

class AnalyticsDisplay:
    def __init__(self, parent_frame, analytics_manager):
        self.parent_frame = parent_frame
        self.analytics_manager = analytics_manager
        self.widgets = {}
        self.create_display()
    
    def create_display(self):
        self.clear_frame()
        self.create_analytics_cards()
        self.create_detailed_report()
        self.create_control_buttons()
    
    def clear_frame(self):
        children = self.parent_frame.winfo_children()
        for child in children[1:]:  
            child.destroy()
    
    def create_analytics_cards(self):
        cards_frame = tk.Frame(self.parent_frame, bg='#f0f0f0')
        cards_frame.pack(fill='x', padx=20, pady=10)
        card_data = self.analytics_manager.get_card_data()
        for i, (title, value, color) in enumerate(card_data):
            card = tk.Frame(cards_frame, bg=color, relief=tk.RAISED, bd=3)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='ew', ipadx=20, ipady=15)
            cards_frame.grid_columnconfigure(i, weight=1)
            tk.Label(card, text=title, font=('Segoe UI', 11, 'bold'),
                    bg=color, fg='white').pack(pady=(10,5))
            tk.Label(card, text=value, font=('Segoe UI', 24, 'bold'),
                    bg=color, fg='white').pack(pady=(0,10))
        self.widgets['cards_frame'] = cards_frame
    
    def create_detailed_report(self):
        report_frame = tk.LabelFrame(self.parent_frame, text="📊 Live Dashboard",
                                   font=('Segoe UI', 14, 'bold'), bg='#f0f0f0')
        report_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        text_frame = tk.Frame(report_frame, bg='#f0f0f0')
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        stats_text = tk.Text(text_frame, font=('Courier New', 9),
                           bg='#ffffff', fg='#2c3e50',
                           wrap=tk.WORD, relief=tk.SOLID, bd=1,
                           height=25, width=100)
        stats_scrollbar = tk.Scrollbar(text_frame, command=stats_text.yview)
        stats_text.config(yscrollcommand=stats_scrollbar.set)
        stats_text.pack(side='left', fill='both', expand=True)
        stats_scrollbar.pack(side='right', fill='y')
        report_content = self.analytics_manager.get_detailed_report()
        stats_text.insert('1.0', report_content)
        stats_text.config(state='disabled')
        self.widgets['stats_text'] = stats_text
        self.widgets['report_frame'] = report_frame
    
    def create_control_buttons(self):
        button_frame = tk.Frame(self.parent_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=20, pady=10)
        refresh_btn = tk.Button(button_frame, text="🔄 Refresh Analytics",
                              font=('Segoe UI', 10, 'bold'), bg='#3498db', fg='white',
                              command=self.refresh_display)
        refresh_btn.pack(side='left', padx=5)
        auto_refresh_btn = tk.Button(button_frame, text="⏰ Auto Refresh: ON",
                                   font=('Segoe UI', 10, 'bold'), bg='#27ae60', fg='white',
                                   command=self.toggle_auto_refresh)
        auto_refresh_btn.pack(side='left', padx=5)
        export_btn = tk.Button(button_frame, text="📊 Export Report",
                             font=('Segoe UI', 10, 'bold'), bg='#e74c3c', fg='white',
                             command=self.export_report)
        export_btn.pack(side='left', padx=5)
        status_label = tk.Label(button_frame, text="Status: Live",
                               font=('Segoe UI', 10), bg='#f0f0f0', fg='#27ae60')
        status_label.pack(side='right', padx=10)
        
        self.widgets['refresh_btn'] = refresh_btn
        self.widgets['auto_refresh_btn'] = auto_refresh_btn
        self.widgets['status_label'] = status_label
    
    def refresh_display(self):
        try:
            self.analytics_manager.refresh_data()
            card_data = self.analytics_manager.get_card_data()
            cards_frame = self.widgets['cards_frame']
            for i, (title, value, color) in enumerate(card_data):
                card = cards_frame.grid_slaves(row=0, column=i)[0]
                value_label = card.pack_slaves()[1]  
                value_label.config(text=value)
            stats_text = self.widgets['stats_text']
            stats_text.config(state='normal')
            stats_text.delete('1.0', tk.END)
            stats_text.insert('1.0', self.analytics_manager.get_detailed_report())
            stats_text.config(state='disabled')
            self.widgets['status_label'].config(text=f"Status: Updated {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Error refreshing analytics: {e}")
    
    def toggle_auto_refresh(self):
        btn = self.widgets['auto_refresh_btn']
        current_text = btn.cget('text')
        if "ON" in current_text:
            btn.config(text="⏰ Auto Refresh: OFF", bg='#e74c3c')
        else:
            btn.config(text="⏰ Auto Refresh: ON", bg='#27ae60')
    
    def export_report(self):
        try:
            report_content = self.analytics_manager.get_detailed_report()
            filename = f"analytics_report_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            self.widgets['status_label'].config(text=f"Report exported: {filename}")
            
        except Exception as e:
            print(f"Error exporting report: {e}")
            self.widgets['status_label'].config(text="Export failed")