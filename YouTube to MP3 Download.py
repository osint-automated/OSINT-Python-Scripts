import yt_dlp

def download_youtube_video_ydl(url, output_path='.'):
    """Downloads a YouTube video using yt-dlp.
    FFMPEG must be installed and in your PATH for audio extraction to work.
    """
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'video')
            print(f"Downloading audio for: {video_title}...")
            ydl.download([url])
            print("Audio download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")

video_url = input("Enter the YouTube video URL: ")
download_youtube_video_ydl(video_url)