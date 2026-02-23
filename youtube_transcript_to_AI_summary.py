from youtube_transcript_api import YouTubeTranscriptApi
import openai
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def youtube_transcript_search(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    transcript_text = ''
    for snippet in transcript:
        transcript_text += snippet.text + '\n'

    return transcript_text

def chatgpt_summary(transcript_text):
    OPENAI_API_KEY = os.getenv('openai_api_key')
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_API_KEY)
    prompt = llm.invoke(transcript_text)
    response = prompt.content
    return response

if __name__== "__main__":
    video_id = input('Enter video ID: (not the full URL) ')
    results = youtube_transcript_search(video_id)
    prompt = f"Summarize the following transcript into an informative summary paragraph, using active voice only and a technical tone only. This is for an intelligence report, write accordingly: {results}"
    summary = chatgpt_summary(prompt)
    print(summary)
