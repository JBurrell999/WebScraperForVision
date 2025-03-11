import subprocess
import os

def download_youtube_video(url, save_path='downloads/youtube/raw'):
    os.makedirs(save_path, exist_ok=True)

    cmd = [
        'yt-dlp',
        '--no-check-certificate',  # explicitly disable SSL checks
        '-f', 'best',
        '-o', f'{save_path}/%(id)s.%(ext)s',
        url
    ]

    try:
        subprocess.run(cmd, check=True)
        video_id = url.split('=')[-1]
        video_filename = os.path.join(save_path, f"{video_id}.mp4")
        print(f"[INFO] Downloaded to: {video_filename}")
        return video_filename
    except Exception as e:
        print(f"[ERROR] Download failed explicitly: {e}")
        return None