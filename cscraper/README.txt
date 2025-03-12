Youtube Scraper and Preprocessor

This project automates the scraping, downloading, and preprocessing of Youtube videos
using a combination of Python scripts and external tools like yt-dlp, OpenCV, and
face_recognition. It gathers video URLs via automated searches, downloads videos, validates
face visibility, trims videos to specific durations and maintains organized metadata logs.

STRUCTURE:

cscraper/
├── scripts/
│   ├── url_gather.py      # Searches YouTube and gathers video URLs
│   ├── scraper.py         # Downloads, validates, and processes videos
│   └── preprocess.py      # Batch processing script for video downloads
├── downloads/
│   └── youtube/
│       ├── raw/           # Directory for raw downloaded videos
│       └── video_metadata.csv # Metadata for downloaded videos
├── video_urls.txt         # List of YouTube URLs
└── .venv/                 # Virtual Python environment

SETUP:

Prerequesuites: Install Homebrew

1. Install Python 3.12:
brew install python@3.12

2. Set up Python Virtual Environment:
python3.12 -m venv .venv
source .venv/bin/activate

3.	Install Python Dependencies:
pip install requests moviepy==1.0.3 imageio imagio-ffmpeg opencv-python face_recognition

4. Install external tools
brew install yt-dlp ffmpeg	

USE:

Make sure all the urls are there by customizing your request for video pulling with the
use of SERPAPI and your key. You run it and all your URLS will be put into video_urls.txt
keep in mind each keyword frame will be n amount of request specified so if your cap is 20
and you have n keyterm combinations expect n(20) URLs.

Also keep in mind for research purposes you may disable and enable FILTER_CREATIVE_COMMONS
by toggling True or False as seen in the code. The same applies for aggregate running of the
program by toggling on and off of CLEAR_CSV in preprocess.py for metadata logging.

Commands:
source .venv/bin/activate
python scripts/url_gather.py
python scripts/preprocess.py
