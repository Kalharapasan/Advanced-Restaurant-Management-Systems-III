from analytics_manager import AnalyticsManager, AnalyticsDisplay
def test_analytics_manager():
    print("Testing Analytics Manager...")
    analytics_manager = AnalyticsManager()
    analytics_manager.refresh_data()
    card_data = analytics_manager.get_card_data()
    print("\n📊 Analytics Cards:")
    for title, value, color in card_data:
        print(f"  {title}: {value} (Color: {color})")
    report = analytics_manager.get_detailed_report()
    print("\n📋 Report Preview (first 500 characters):")
    print(report[:500] + "...")
    hourly_sales = analytics_manager.get_hourly_sales()
    print(f"\n⏰ Hourly Sales Data Points: {len(hourly_sales)}")
    print(f"Sample: {hourly_sales[:3]}")
    top_items = analytics_manager.get_top_items(5)
    print(f"\n🏆 Top 5 Items:")
    for item in top_items:
        print(f"  {item['name']}: {item['sales']} sales, ${item['revenue']:.2f} revenue")
    
    print("\n✅ Analytics Manager test completed successfully!")

if __name__ == "__main__":
    test_analytics_manager()