import feedparser
"""
This script searches for a user-provided term in the titles of news articles from a list of RSS feeds.
Modules:
    feedparser: Used to parse RSS feeds.
Variables:
    links (list): A list of RSS feed URLs to search.
    query (str): The search term entered by the user, converted to lowercase.
Workflow:
    1. Prompts the user to enter a search term.
    2. Iterates through each RSS feed URL in 'links'.
    3. Parses the RSS feed and iterates through its entries.
    4. Checks if the search term is present in the entry's title (case-insensitive).
    5. If a match is found, prints the article's title, link, and description.
Usage:
    Run the script and enter a search term when prompted. The script will display matching articles from the provided RSS feeds.
"""

links = ['http://feeds.bbci.co.uk/news/world/rss.xml', 'http://rss.cnn.com/rss/edition_world.rss', 'https://moxie.foxnews.com/google-publisher/latest.xml', 'https://www.aljazeera.com/xml/rss/all.xml', 'https://feeds.thelocal.com/rss/es', 'http://feeds.skynews.com/feeds/rss/world.xml', 'https://www.worldaffairsjournal.org/feed/', 'https://www.vox.com/world-politics', 'https://danielspost.news.blog/feed/', 'https://bbcbreakingnews.com/feed/', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=4912590&q=site:https%3A%2F%2Fifpnews.com%2Ffeed%2F', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=60928&q=site:https%3A%2F%2Frss.csmonitor.com%2Ffeeds%2Fworld', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=4722784&q=site:https%3A%2F%2Fjustworldeducational.org%2Fcategory%2Fblog%2Ffeed%2F', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=4629316&q=site:https%3A%2F%2Fwww.pri.org%2Fstories%2Ffeed%2Feverything', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5329198&q=site:https%3A%2F%2Fhgsmediaplus.com%2Ffeed%2F', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5036647&q=site:https%3A%2F%2Fnewsblaze.com%2Ffeed%2F', 'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=252648&q=site:https%3A%2F%2Fwww.worldaffairsjournal.org%2Ffeed%2F', 'https://www.ctvnews.ca/rss/world/ctvnews-ca-world-public-rss-1.822289', 'https://www.thecipherbrief.com/feed', 'https://www.cnbc.com/id/100727362/device/rss/rss.html', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5170360&q=site:https%3A%2F%2Fwww.worldpresslive.com%2Ffeeds%2Fposts%2Fdefault', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5160768&q=site:https%3A%2F%2F247newsaroundtheworld.com%2Ffeed%2F', 'https://www.express.co.uk/feed/', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5148877&q=site:https%3A%2F%2Ffeeds.bizjournals.com%2Ffeeds%2Fworld', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5135141&q=site:https%3A%2F%2Febysblog.com%2Ffeed', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=1716348&q=site:https%3A%2F%2Fwww.ctvnews.ca%2Frss%2Fworld%2Fctvnews-ca-world-public-rss-1.822289', 'http://www.mirror.co.uk/news/world-news/rss.xml', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5161811&q=site:https%3A%2F%2Fworldupdatedaily.blogspot.com%2Ffeeds%2Fposts%2Fdefault%3Falt%3Drss', 'https://rss.csmonitor.com/feeds/world', 'https://feeds.feedburner.com/ndtvnews-world-news', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5161015&q=site:https%3A%2F%2Fthedetrend.com%2Ffeed%2F', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5145728&q=site:https%3A%2F%2Fweb.neduwealth.com%2Ffeeds%2Fposts%2Fdefault', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5294610&q=site:https%3A%2F%2Finternewscast.com%2Ffeed%2F', 'https://rss.feedspot.com/?_src=footer&_orgin=world_news_rss_feeds', 'https://rss.csmonitor.com/feeds/world', 'https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5082920&q=site:https%3A%2F%2Famnews247.com%2Ffeed%2F']

query = input('Enter search term here: ').lower()

for rss_link in links:
    feed = feedparser.parse(rss_link)
    for entry in feed.entries:
        if query in entry.title.lower():
            title = entry.get('title', 'Unknown title')
            entry_link = entry.get('link', 'Unknown link')
            description = entry.get('description', 'No description available')

            print(f'Title: {title}')
            print(f'Link: {entry_link}')
            print(f'Description: {description}')
            print('------------------------')
