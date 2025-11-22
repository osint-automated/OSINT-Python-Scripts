from youtube_transcript_api import YouTubeTranscriptApi

def youtube_transcript_search(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    transcript_text = ''
    for snippet in transcript:
        transcript_text += snippet.text + '\n'

    return transcript_text

if __name__== "__main__":
    video_id = input('Enter video ID: (not the full URL) ')
    results = youtube_transcript_search(video_id)
    with open('transcript.txt', 'w') as f:
        f.write(results)
    print('Video transcript saved in transcript.txt')
