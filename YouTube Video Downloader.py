import yt_dlp

def download_youtube_video_ydl(url, output_path='.'):
    """Downloads a YouTube video using yt-dlp.

    FFMPEG must be installed. (apt-get install -y ffmpeg)

    Args:
        video_url (str): The URL of the YouTube video to download.
    """
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'video')
            print(f"Downloading: {video_title}...")
            ydl.download([url])
            print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")

video_url = input("Enter the YouTube video URL: ")
download_youtube_video_ydl(video_url)


