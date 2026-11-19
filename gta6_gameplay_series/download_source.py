import os
import sys
import subprocess
from pathlib import Path

SERIES_DIR = Path(r"E:\work station\gta 6\gta6_gameplay_series")
SOURCE_DIR = SERIES_DIR / "source"
CLIPS_DIR = SERIES_DIR / "clips"
SOURCE_DIR.mkdir(parents=True, exist_ok=True)
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://youtu.be/RVpApoEkOao"
OUTPUT_VIDEO = SOURCE_DIR / "gta6_gameplay_source.mp4"

def download_video(duration_limit_minutes=10):
    print(f"[*] Downloading source video (first {duration_limit_minutes} minutes)...")
    # Download best video up to 1080p and best audio
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--download-sections", f"*00:00:00-00:{duration_limit_minutes:02d}:00",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--merge-output-format", "mp4",
        "-o", str(OUTPUT_VIDEO),
        URL
    ]
    subprocess.run(cmd, check=True)
    print(f"[+] Download complete: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    download_video(10)
