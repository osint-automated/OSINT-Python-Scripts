from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('google_api_key')

def comment_scraper(youtube, video_id, max_results=100):
    """
    Fetches top-level comments from a YouTube video using the YouTube Data API.

    Args:
        youtube: An authenticated YouTube Data API client instance.
        video_id (str): The ID of the YouTube video to retrieve comments from.
        max_results (int, optional): Maximum number of comments to retrieve. Defaults to 100.

    Returns:
        list of dict: A list of dictionaries, each containing 'User' (author's display name) and 'Comment' (comment text).

    Raises:
        googleapiclient.errors.HttpError: If the API request fails.
    """
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=max_results
    )
    response = request.execute()

    comments = []

    for item in response['items']:
        comment_data = {
            'User': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            'Comment': item['snippet']['topLevelComment']['snippet']['textDisplay']
        }
        comments.append(comment_data)

    return comments

youtube = build('youtube', 'v3', developerKey=api_key)
video_id = input('Enter video ID here: (e.g., bxRh0NjlqjA): ')

comments_data = comment_scraper(youtube, video_id)

df = pd.DataFrame(comments_data)

print(df)