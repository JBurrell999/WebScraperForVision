import os
import torch
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper import download_youtube_video

CLEAR_CSV = True
METADATA_CSV = 'downloads/youtube/video_metadata.csv'

def batch_partial_download(url_file='video_urls.txt', raw_path='downloads/youtube/raw', partial_duration=20, max_workers=16):
    os.makedirs(raw_path, exist_ok=True)

    if CLEAR_CSV and os.path.exists(METADATA_CSV):
        os.remove(METADATA_CSV)

    with open(url_file, "r") as file:
        urls = [line.strip() for line in file if line.strip()]
    
    device = "cuda" if torch.cuda.is_avaiable() else "cpu"
    print(f"Using device: {device}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(download_youtube_video, url, raw_path, METADATA_CSV, partial_duration): url
            for url in urls
        }

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    print(f"[SUCCESS] Processed {url}")
                else:
                    print(f"[FAILED] Face visibility failed: {url}")
            except Exception as e:
                print(f"[ERROR] {url}: {e}")

if __name__ == "__main__":
    batch_partial_download(max_workers=16)