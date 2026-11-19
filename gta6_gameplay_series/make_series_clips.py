import os
import sys
import subprocess
import json
from pathlib import Path

SERIES_DIR = Path(r"E:\work station\gta 6\gta6_gameplay_series")
SOURCE_FILE = SERIES_DIR / "source" / "gta6_gameplay_source.mp4"
CLIPS_DIR = SERIES_DIR / "clips"
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/calibrib.ttf"

def get_video_duration(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def render_part(src, out_path, start_time, duration, part_num, total_parts):
    end_time = start_time + duration
    time_label = f"{format_time(start_time)} - {format_time(end_time)}"
    print(f"\n[+] Rendering Part {part_num:02d} ({time_label}) -> {out_path.name}...")

    # Escaped font path for ffmpeg filter
    escaped_font = FONT_PATH.replace("\\", "/").replace(":", "\\:")

    # Top header badge styling
    # Top bar title: "GTA 6 GAMEPLAY"
    # Subtitle: "PART XX • FULL GAMEPLAY"
    # Bottom watermark: "Next Part ->"
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:3,eq=brightness=-0.18[bg];"
        f"[0:v]scale=1080:-2[fg];"
        f"[bg][fg]overlay=0:(H-h)/2[comp];"
        # Top banner background box
        f"[comp]drawbox=x=0:y=60:w=1080:h=220:color=black@0.65:t=fill[b1];"
        # Top title text
        f"[b1]drawtext=fontfile='{escaped_font}':text='GTA 6 GAMEPLAY':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=95,"
        f"drawtext=fontfile='{escaped_font}':text='PART {part_num:02d}':fontcolor=0xFFC800:fontsize=76:x=(w-text_w)/2:y=180,"
        # Bottom call to action banner
        f"drawbox=x=0:y=1700:w=1080:h=120:color=black@0.6:t=fill,"
        f"drawtext=fontfile='{escaped_font}':text='WATCH NEXT PART >>':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=1738[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-t", str(duration),
        "-i", str(src),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a?",
        "-c:v", "h264_nvenc",
        "-preset", "p5",
        "-cq", "21",
        "-b:v", "6500k",
        "-maxrate", "8000k",
        "-bufsize", "12000k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(out_path)
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("[!] NVENC failed, falling back to libx264...")
        cmd[cmd.index("h264_nvenc")] = "libx264"
        idx_p = cmd.index("-preset")
        cmd[idx_p + 1] = "faster"
        cmd.remove("-cq")
        cmd.remove("21")
        cmd.extend(["-crf", "20"])
        subprocess.run(cmd, check=True)

    print(f"[OK] Completed Part {part_num:02d} successfully!")

def main():
    if not SOURCE_FILE.exists():
        print(f"[ERROR] Source file not found: {SOURCE_FILE}")
        sys.exit(1)

    total_duration = get_video_duration(SOURCE_FILE)
    print(f"[*] Source video duration: {total_duration:.2f} seconds ({format_time(total_duration)})")

    # Target clip duration: 55 seconds (safe < 60s for YouTube Shorts & Reels)
    clip_duration = 55.0
    start = 0.0
    part_idx = 1
    parts_metadata = []

    # Calculate how many parts
    total_parts = int(total_duration // clip_duration)
    if total_parts < 1:
        total_parts = 1

    print(f"[*] Generating {total_parts} continuous sequential parts (each {clip_duration}s)...")

    while start + 10.0 <= total_duration:  # at least 10s for last part
        cur_duration = min(clip_duration, total_duration - start)
        out_name = f"GTA6_Gameplay_Part_{part_idx:02d}.mp4"
        out_path = CLIPS_DIR / out_name

        render_part(SOURCE_FILE, out_path, start, cur_duration, part_idx, total_parts)

        parts_metadata.append({
            "part": part_idx,
            "filename": out_name,
            "start": format_time(start),
            "end": format_time(start + cur_duration),
            "duration": round(cur_duration, 1),
            "title": f"GTA 6 Gameplay - Part {part_idx:02d} (Full Gameplay Series)",
            "caption": (
                f"GTA 6 Full Gameplay Walkthrough Part {part_idx} 🔥\n"
                f"Part {part_idx+1} coming next! Follow for the full series.\n\n"
                f"#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Viral #Shorts #Reels #TikTok"
            )
        })

        # Exact seamless continuation: next clip starts where this one ended
        start += cur_duration
        part_idx += 1

    # Write POSTING_GUIDE.md
    guide_path = SERIES_DIR / "POSTING_GUIDE.md"
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write("# GTA 6 Gameplay Sequential Clips - Posting Guide\n\n")
        f.write("Generated for YouTube Shorts, Instagram Reels, Facebook Reels, and TikTok.\n")
        f.write("All clips are continuous (55s each) in 1080x1920 (9:16 vertical HD).\n\n")
        f.write("---\n\n")
        for item in parts_metadata:
            f.write(f"## Part {item['part']:02d} ({item['filename']})\n")
            f.write(f"- **Timestamp**: `{item['start']}` to `{item['end']}` (Duration: {item['duration']}s)\n")
            f.write(f"- **Title**: `{item['title']}`\n")
            f.write(f"- **Recommended Caption & Hashtags**:\n")
            f.write("```text\n")
            f.write(item['caption'] + "\n")
            f.write("```\n\n")

    print(f"\n[DONE] All {len(parts_metadata)} sequential clips created in:\n{CLIPS_DIR}")
    print(f"[DONE] Posting guide saved at:\n{guide_path}")

if __name__ == "__main__":
    main()
