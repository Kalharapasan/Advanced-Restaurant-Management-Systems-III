from analytics_manager import AnalyticsManager, AnalyticsDisplay
def test_analytics_manager():
    print("Testing Analytics Manager...")
    analytics_manager = AnalyticsManager()
    analytics_manager.refresh_data()
    card_data = analytics_manager.get_card_data()
    print("\n📊 Analytics Cards:")
    for title, value, color in card_data:
        print(f"  {title}: {value} (Color: {color})")