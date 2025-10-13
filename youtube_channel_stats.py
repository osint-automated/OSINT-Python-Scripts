from googleapiclient.discovery import build

api_key = input('Enter your YouTube API key here: ')
channel_id = input('Enter channel ID here: ')
youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_stats(youtube, channel_id):
    """
    Retrieves statistics and metadata for a specified YouTube channel.

    Args:
        youtube: An instance of the Google API client for YouTube.
        channel_id (str): The unique identifier of the YouTube channel.

    Returns:
        dict: A dictionary containing the channel's name, country, creation date,
              subscriber count, view count, and video count. If a field is missing,
              default values are provided.
    """
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    )
    response = request.execute()

    data = {
        'channel_name': response['items'][0]['snippet'].get('title', 'N/A'),
        'country': response['items'][0]['snippet'].get('country', 'N/A'),
        'creation_date': response['items'][0]['snippet'].get('publishedAt', 'N/A'),
        'subscriber_count': response['items'][0]['statistics'].get('subscriberCount', 0),
        'view_count': response['items'][0]['statistics'].get('viewCount', 0),
        'video_count': response['items'][0]['statistics'].get('videoCount', 0)
    }

    return data

channel_statistics = get_channel_stats(youtube, channel_id)

print(channel_statistics)