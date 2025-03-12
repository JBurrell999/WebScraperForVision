import subprocess
from concurrent.futures import ThreadPoolExecutor
import os

def download_video(args):
    url, index = args
    filename = f"video_{index}.mp4"
    subprocess.run([
        "ffmpeg", "-hwaccel", "cuda", "-http_persistent", "0", "-i", url, 
        "-c:v", "h264_nvenc", "-b:v", "5M", "-c:a", "aac", filename
    ])

def main():
    with open("video_urls.txt", "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    os.makedirs("downloads", exist_ok=True)
    os.chdir("downloads")

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_video, zip(urls, range(len(urls))))

if __name__ == "__main__":
    main()