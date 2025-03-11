Youtube Scraper and Preprocessor

This project lets you download YouTube videos reliably using a stable command-line setup with yt-dlp,
trim them automatically with MoviePy, and store them in organized folders if needed.
It explicitly avoids common anti-scraping protections on Youtube by using direct system integration.

STRUCTURE:

cscraper/
├── scripts/
│   ├── scraper.py      (video downloader)
│   └── preprocess.py   (video trimmer and batch processor)
├── downloads/
│   └── youtube/
│       ├── raw/        (original downloaded videos)
│       └── trimmed/    (trimmed output videos)
├── video_urls.txt      (paste YouTube URLs here)
└── .venv/              (virtual Python environment)

SETUP:

1.	Install Homebrew if not already installed:
https://brew.sh/

2.	Install Python 3.12 explicitly (recommended):
brew install python@3.12

3.	Set up your Python virtual environment explicitly:
python3.12 -m venv .venv
source .venv/bin/activate

4.	Explicitly install required Python dependencies:
pip install moviepy==1.0.3 imageio imageio-ffmpeg

5.	Explicitly install yt-dlp via Homebrew (critical):
brew install yt-dlp

6.	Ensure ffmpeg is installed explicitly:
brew install ffmpeg

USE:

Place all the urls you will want to scrape and download in video_urls.txt one per line.
Then from your terminal activate the virtual environment. Run the executable and the
files will appear in downloads/youtube/raw/ and the trimmed in /trimmed/

Commands:
source .venv/bin/activate
python scripts/preprocess.py