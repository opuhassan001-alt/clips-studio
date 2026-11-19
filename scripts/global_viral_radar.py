"""
Global Viral Radar Engine for YouTube Gaming & Longform Streams.
Scrapes worldwide trending gaming videos from the last 24 hours (>= 30 minutes),
calculates view velocity, assigns creator clipping safety ratings, and generates
the daily actionable report with auto-archive on review.
100% Free & Local (yt-dlp powered).
"""

import os
import sys
import json
import base64
import urllib.parse
import subprocess
import argparse
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_FILE = BASE_DIR / "DAILY_VIRAL_REPORT.md"
ARCHIVE_DIR = BASE_DIR / "reports" / "archive"

# YouTube Protobuf search filter constants:
# sort_by_views = 3, time_window: today = 2, duration: long (>20min) = 2
WHEN_TODAY = 2
SORT_BY_VIEWS = 3
LONG_VIDEOS = 2

# Whitelist of top gaming streamers with open community clipping policies
KNOWN_CLIP_SAFE_CREATORS = [
    "ishowspeed", "carryminati", "carryisllive", "xqc", "kaicenat", 
    "moistcr1tikal", "penguinz0", "theradbrad", "tgg", "hollow", 
    "caseoh", "jynxzi", "flightreacts", "tyrone magnus", "adin ross",
    "pewdiepie", "markiplier", "jacksepticeye", "danTDM", "sypherpk"
]


def _build_search_filter():
    """Generates YouTube's protobuf search filter for Today + Long + Sorted by Views."""
    inner = bytes([0x08, WHEN_TODAY, 0x18, LONG_VIDEOS])
    raw = bytes([0x08, SORT_BY_VIEWS, 0x12, len(inner)]) + inner
    return base64.b64encode(raw).decode()


def get_ytdlp_bin():
    """Finds available yt-dlp binary across local virtual environments."""
    candidates = [
        BASE_DIR / ".venv" / "Scripts" / "yt-dlp.exe",
        Path.home() / ".streamclips" / "venv" / "Scripts" / "yt-dlp.exe",
        "yt-dlp"
    ]
    for c in candidates:
        if isinstance(c, Path) and c.exists():
            return str(c)
    return "yt-dlp"


def get_clip_safety(channel_name: str) -> str:
    """Returns a clip-safety rating based on creator profile."""
    ch_clean = channel_name.lower().strip()
    for safe in KNOWN_CLIP_SAFE_CREATORS:
        if safe in ch_clean:
            return "🟢 Safe (Open Clipping Creator)"
    if any(k in ch_clean for k in ["vevo", "records", "music", "sonymusic", "warner", "tseries"]):
        return "🔴 High Risk (Commercial Record Label)"
    return "🟡 Standard (Fair Use Transformative Required)"


def format_duration(seconds: float) -> str:
    """Format seconds into 1h 25m or 45m."""
    s = int(seconds)
    hours = s // 3600
    minutes = (s % 3600) // 60
    if hours > 0:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


def format_views(count: int) -> str:
    """Format view numbers into K/M strings."""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def scan_worldwide_viral_streams(query="GTA 6", min_duration_sec=1800, max_results=5):
    """
    Scrapes YouTube globally for completed videos/streams in the last 24h with duration >= 30m.
    """
    print(f"\n🌍 SCANNING WORLDWIDE YOUTUBE VIRAL RADAR...")
    print(f"   Query: \"{query}\" | Min Duration: {min_duration_sec // 60}m | Time: Last 24 Hours")
    
    search_sp = _build_search_filter()
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}&sp={urllib.parse.quote(search_sp)}"

    cmd = [
        get_ytdlp_bin(),
        "--flat-playlist",
        "--playlist-end", "25",
        "--dump-single-json",
        "--no-warnings",
        search_url
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(f"❌ Error during search: {res.stderr[:200]}")
        return []

    try:
        data = json.loads(res.stdout)
    except Exception as e:
        print(f"❌ Error parsing search output: {e}")
        return []

    entries = data.get("entries", [])
    valid_candidates = []

    for e in entries:
        if not e or not e.get("id"):
            continue

        # Filter 1: Exclude active/ongoing livestreams (Completed VODs or standard uploads only)
        live_status = e.get("live_status")
        if live_status == "is_live":
            continue

        duration = float(e.get("duration") or 0)
        # Filter 2: Duration >= 30 minutes (1800 seconds)
        if duration < min_duration_sec:
            continue

        views = int(e.get("view_count") or 0)
        channel = e.get("channel") or e.get("uploader") or "Unknown"
        title = e.get("title") or "Untitled"
        vid_id = e.get("id")
        url = f"https://www.youtube.com/watch?v={vid_id}"

        # Estimate view velocity (assuming 24h window)
        velocity_per_hr = views // 24

        valid_candidates.append({
            "id": vid_id,
            "title": title,
            "channel": channel,
            "duration": duration,
            "duration_str": format_duration(duration),
            "views": views,
            "views_str": format_views(views),
            "velocity_str": f"~{format_views(velocity_per_hr)}/hr",
            "safety": get_clip_safety(channel),
            "url": url
        })

    # Sort descending by view count
    valid_candidates.sort(key=lambda x: x["views"], reverse=True)
    return valid_candidates[:max_results]


def write_report(candidates, topic="GTA 6"):
    """Generates the DAILY_VIRAL_REPORT.md file."""
    now_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
    
    lines = [
        f"# 🌍 Daily Global Viral Gaming Radar (Last 24 Hours)",
        f"> **Generated at**: `{now_str}`",
        f"> **Topic**: `{topic}` | **Duration Filter**: `Minimum 30 Minutes+` | **Sort**: `Worldwide Top Views`",
        f"> **Status**: `UNREAD 🔔` (Awaiting review)",
        "",
        "---",
        "",
        "## 🏆 Top Viral Long-form Streams & Videos Worldwide",
        "",
        "| Rank | Channel / Streamer | Video Title | Duration | Views (24h) | Velocity | Clip Safety |",
        "|---|---|---|---|---|---|---|",
    ]

    for idx, c in enumerate(candidates, 1):
        lines.append(
            f"| **#{idx}** | **{c['channel']}** | [{c['title']}]({c['url']}) | `{c['duration_str']}` | **{c['views_str']}** | `{c['velocity_str']}` | {c['safety']} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## ⚡ এক ক্লিকে রিলস কাটার অপশন (Action Commands):",
        "",
    ])

    for idx, c in enumerate(candidates, 1):
        lines.append(
            f"- **Clip Rank #{idx} ({c['channel']})**:\n"
            f"  ```bash\n"
            f"  python scripts/auto_clipper.py \"{c['url']}\"\n"
            f"  ```"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🗑️ রিপোর্ট দেখা শেষ হলে ডিলিট / আর্কাইভ করার কমান্ড:",
        "আপনি যখন বলবেন: *\"হ্যাঁ আমি রিপোর্ট দেখেছি\"* অথবা নিচের কমান্ডটি চালাবেন, রিপোর্টটি ক্লিন হয়ে যাবে:",
        "```bash",
        "python scripts/global_viral_radar.py dismiss",
        "```",
        ""
    ])

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n✅ DAILY VIRAL REPORT GENERATED SUCCESSFULLY!")
    print(f"   📄 File: {REPORT_FILE.resolve()}")


def dismiss_report():
    """Archives and clears the current daily report upon user review."""
    if not REPORT_FILE.exists():
        print("ℹ️ No active DAILY_VIRAL_REPORT.md found to dismiss.")
        return True

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dest = ARCHIVE_DIR / f"DAILY_VIRAL_REPORT_{ts}.md"
    
    REPORT_FILE.replace(archive_dest)
    print(f"🧹 Report successfully reviewed and dismissed!")
    print(f"   Archived to: {archive_dest.resolve()}")
    print("   Workspace is now clean for the next cycle.")
    return True


def clip_rank(rank_index: int):
    """Parses the active report, extracts the URL for given rank, and triggers auto_clipper."""
    if not REPORT_FILE.exists():
        print("❌ Error: DAILY_VIRAL_REPORT.md not found. Run scan first.")
        return False

    content = REPORT_FILE.read_text(encoding="utf-8")
    matches = re.findall(r"python scripts/auto_clipper\.py \"(https://[^\"]+)\"", content)
    if not matches or rank_index > len(matches) or rank_index < 1:
        print(f"❌ Error: Rank #{rank_index} not found in report.")
        return False

    chosen_url = matches[rank_index - 1]
    print(f"\n🚀 Launching Auto-Clipper for Rank #{rank_index}: {chosen_url}")
    
    # Run auto_clipper
    cmd = [sys.executable, str(BASE_DIR / "scripts" / "auto_clipper.py"), chosen_url]
    subprocess.run(cmd)

    # Dismiss report after launching clip
    dismiss_report()
    return True


def main():
    parser = argparse.ArgumentParser(description="Global Viral Radar Engine")
    subparsers = parser.add_subparsers(dest="command")

    # Scan command
    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("--query", default="GTA 6", help="Search topic")
    scan_parser.add_argument("--min-duration", type=int, default=1800, help="Min video duration in seconds (default 1800 = 30m)")
    scan_parser.add_argument("--limit", type=int, default=5, help="Number of top candidates to report")

    # Dismiss command
    subparsers.add_parser("dismiss")

    # Clip command
    clip_parser = subparsers.add_parser("clip")
    clip_parser.add_argument("--rank", type=int, required=True, help="Rank number from report to clip")

    args = parser.parse_args()

    if args.command == "scan" or args.command is None:
        query = getattr(args, "query", "GTA 6")
        min_dur = getattr(args, "min_duration", 1800)
        limit = getattr(args, "limit", 5)
        candidates = scan_worldwide_viral_streams(query, min_duration_sec=min_dur, max_results=limit)
        if candidates:
            write_report(candidates, topic=query)
        else:
            print("⚠️ No completed 30m+ streams found matching criteria in the last 24h.")
    elif args.command == "dismiss":
        dismiss_report()
    elif args.command == "clip":
        clip_rank(args.rank)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
