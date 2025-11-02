from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('google_api_key')

channel_ids = [
    'UCI6VJI9DuODXAXY4xmhqg9Q', #replace these channel IDs with your desired channels
    'UCbLq9tsbo8peV22VxbDAfXA', #replace these channel IDs with your desired channels
    'UCgDqL4yzXb4BflimZaxL4Vg', #replace these channel IDs with your desired channels
    'UCWsEZ9v1KC8b5VYjYbEewJA', #replace these channel IDs with your desired channels
    'UCzlXf-yUIaOpOjEjPrOO9TA', #replace these channel IDs with your desired channels
]
youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_stats(youtube, channel_ids):
    """
    Retrieves statistics and metadata for multiple YouTube channels.

    Args:
        youtube: An authenticated Google API client for YouTube Data API.
        channel_ids (list of str): List of YouTube channel IDs to fetch data for.

    Returns:
        list of dict: A list where each dictionary contains the following keys:
            - 'channel_name': The name of the channel.
            - 'country': The country associated with the channel (if available).
            - 'creation_date': The date the channel was created.
            - 'subscriber_count': Number of subscribers to the channel.
            - 'view_count': Total number of views for the channel.
            - 'video_count': Total number of videos uploaded to the channel.

    Notes:
        If a particular field is not available, a default value is used ('N/A' for strings, 0 for counts).
    """
    all_data = []
    request = youtube.channels().list(
      part='snippet,contentDetails,statistics',
      id=','.join(channel_ids)
    )
    response = request.execute()

    for i in range(len(response['items'])):
        item = response['items'][i]
        data = {
            'channel_name': item['snippet'].get('title', 'N/A'),
            'country': item['snippet'].get('country', 'N/A'),
            'creation_date': item['snippet'].get('publishedAt', 'N/A'),
            'subscriber_count': item['statistics'].get('subscriberCount', 0),
            'view_count': item['statistics'].get('viewCount', 0),
            'video_count': item['statistics'].get('videoCount', 0)
        }
        all_data.append(data)

    return all_data

channel_statistics = get_channel_stats(youtube, channel_ids)

print(channel_statistics)

channel_data = pd.DataFrame(channel_statistics)

channel_data