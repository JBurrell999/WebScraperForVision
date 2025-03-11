from scraper import download_youtube_video
from moviepy.editor import VideoFileClip
import os

def batch_download_and_trim(file_with_urls, raw_path='downloads/youtube/raw', trimmed_path='downloads/youtube/trimmed', max_duration=15):
    os.makedirs(trimmed_path, exist_ok=True)
    os.makedirs(raw_path, exist_ok=True)

    with open(file_with_urls, 'r') as f:
        urls = [url.strip() for url in f.readlines() if url.strip()]

    for url in urls:
        try:
            print(f"[INFO] Downloading video from URL: {url}")
            raw_video_path = download_youtube_video(url, raw_path)

            if raw_video_path:
                video_filename = os.path.basename(raw_video_path)
                trimmed_video_path = os.path.join(trimmed_path, f"trimmed_{video_filename}")

                print(f"[INFO] Trimming video: {video_filename}")
                trim_video(raw_video_path, trimmed_video_path, max_duration=15)
            else:
                print(f"[ERROR] Download failed for URL: {url}")

        except Exception as e:
            print(f"[ERROR] Failed processing URL {url}: {e}")

def trim_video(input_path, output_path, max_duration=15):
    clip = VideoFileClip(input_path)
    if clip.duration > max_duration:
        clip = clip.subclip(0, max_duration)
    clip.write_videofile(output_path, codec="libx264")
    clip.close()

if __name__ == "__main__":
    batch_download_and_trim('video_urls.txt')