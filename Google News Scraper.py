from pygooglenews import GoogleNews
from datetime import datetime, timedelta

def search_recent_news(topic):
    """
    Searches Google News for a given topic within the last 30 days.
    """
    print(f"\nSearching for articles on '{topic}' from the last 30 days...")

    gn = GoogleNews(lang='en', country='US')

    try:
        search_results = gn.search(topic, when='30d')

        if not search_results['entries']:
            print("No articles found for this topic in the last 30 days.")
            return

        print("\n--- Results ---")
        for item in search_results['entries'][:30]:
            print(f"Title: {item.title}")
            print(f"Link: {item.link}")
            print(f"Published: {item.published}\n")
            print("-" * 20)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    search_topic = input("Enter a topic to research: ")
    if search_topic:
        search_recent_news(search_topic)
    else:
        print("No topic entered. Exiting.")


