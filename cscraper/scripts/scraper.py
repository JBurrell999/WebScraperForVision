import subprocess
import os
import json
import csv
import re
import random
from datetime import datetime
import cv2
import face_recognition
import uuid

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def validate_face_visibility(video_path: str, threshold=0.6, check_duration=2, frame_skip=2) -> bool:
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(fps * check_duration)

    frames_checked = 0
    frames_with_faces = 0
    current_frame = 0

    gpu_frame = cv2.cuda_GpuMat()

    while frames_checked < total_frames:
        ret, frame = video.read()
        if not ret:
            break

        if current_frame % frame_skip == 0:
            gpu_frame.upload(frame)
            small_frame = cv2.cuda.resize(gpu_frame, (480, 270))
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb_frame, model='hog')

            if faces:
                frames_with_faces += 1

            frames_checked += 1

        current_frame += 1

    video.release()

    visibility_ratio = frames_with_faces / frames_checked if frames_checked else 0
    return visibility_ratio >= threshold

def write_metadata_to_csv(csv_path: str, metadata: dict) -> None:
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = [
            'video_url', 'title', 'channel', 'channel_id', 'duration_seconds',
            'views', 'likes', 'upload_date', 'download_timestamp', 'video_filename',
            'clip_start_seconds', 'clip_end_seconds'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(metadata)

def seconds_to_timestamp(seconds: int) -> str:
    h, m = divmod(seconds, 3600)
    m, s = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}"

def download_youtube_video(url: str, save_path='downloads/youtube/raw',
                           metadata_path='downloads/youtube/video_metadata.csv',
                           partial_duration=20) -> str | None:

    os.makedirs(save_path, exist_ok=True)
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)

    unique_id = uuid.uuid4().hex
    temp_metadata_file = os.path.join(save_path, f'temp_{unique_id}.info.json')

    metadata_cmd = [
        'yt-dlp', '--no-check-certificate', '--write-info-json',
        '--skip-download', '-o', f'{save_path}/temp_{unique_id}', url
    ]
    subprocess.run(metadata_cmd, check=True)

    with open(temp_metadata_file, 'r') as f:
        metadata_json = json.load(f)

    duration = metadata_json.get('duration', 0)
    start_time = 0 if duration <= partial_duration + 60 else random.randint(60, duration - partial_duration)

    title = sanitize_filename(metadata_json.get('title', 'unknown_title'))
    channel = sanitize_filename(metadata_json.get('uploader', 'unknown_channel'))
    channel_id = metadata_json.get('channel_id', 'unknown_channel_id')
    upload_date = metadata_json.get('upload_date', '')
    video_filename = f"{upload_date}_{title}_{channel}_{start_time}s.mp4"
    video_path = os.path.join(save_path, video_filename)

    download_cmd = [
    'yt-dlp', '--no-check-certificate', '-o', video_path,
    '--download-sections', f'*{seconds_to_timestamp(start_time)}-{seconds_to_timestamp(start_time + partial_duration)}',
    '--force-keyframes-at-cuts',
    '--recode-video', 'mp4',
    url
    ]

    subprocess.run(download_cmd, check=True)

    if not validate_face_visibility(video_path):
        print(f"[WARNING] Face validation failed for '{video_filename}'. Removing.")
        os.remove(video_path)
        os.remove(temp_metadata_file)
        return None

    metadata_log = {
        'video_url': url,
        'title': title,
        'channel': channel,
        'channel_id': channel_id,
        'duration_seconds': duration,
        'views': metadata_json.get('view_count'),
        'likes': metadata_json.get('like_count'),
        'upload_date': upload_date,
        'download_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'video_filename': video_filename,
        'clip_start_seconds': start_time,
        'clip_end_seconds': start_time + partial_duration
    }

    write_metadata_to_csv(metadata_path, metadata_log)
    os.remove(temp_metadata_file)

    return video_path