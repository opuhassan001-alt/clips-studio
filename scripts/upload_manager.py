"""Upload Manager & Auto-Delete Tracker for Clips Studio.

Manages the queue of 80+ viral clips:
- Provides copy-paste metadata (Title, Caption, Hashtags, Pinned Comment, Algorithm tips)
- Marks clips as [UPLOADED]
- Automatically deletes the local video file once uploaded to free up disk space
- Updates UPLOAD_MANAGER.md and metadata JSON
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRACKER_JSON = BASE_DIR / "data" / "upload_tracker.json"
TRACKER_MD = BASE_DIR / "UPLOAD_MANAGER.md"

def load_tracker() -> dict:
    if TRACKER_JSON.exists():
        with open(TRACKER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"clips": []}

def save_tracker(data: dict):
    TRACKER_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    generate_markdown(data)

def generate_markdown(data: dict):
    clips = data.get("clips", [])
    ready_count = sum(1 for c in clips if c["status"] == "READY")
    uploaded_count = sum(1 for c in clips if c["status"] == "UPLOADED")

    lines = [
        "# 🚀 GTA 6 Viral Clips — Upload Queue & Algorithm Optimizer",
        "",
        f"> **Queue Summary**: Total 80+ Clips: `{len(clips)}` | Ready: `{ready_count}` | Uploaded & Deleted: `{uploaded_count}`",
        "",
        "---",
        "",
        "### 💡 Upload Management Commands:",
        "- **List Pending Clips**: `.venv\\Scripts\\python.exe scripts\\upload_manager.py list`",
        "- **Mark Uploaded & Auto-Delete File**: `.venv\\Scripts\\python.exe scripts\\upload_manager.py mark <CLIP_ID> --delete`",
        "",
        "---",
        ""
    ]

    for c in clips:
        cid = c["id"]
        status_box = "[x] UPLOADED (DELETED)" if c["status"] == "UPLOADED" else "[ ] READY TO UPLOAD"
        file_path_str = c.get("file_path", "")
        file_uri = Path(file_path_str).as_uri() if file_path_str and Path(file_path_str).exists() else ""
        file_link = f"[{c['file_name']}]({file_uri})" if file_uri else f"`{c['file_name']}` (File Deleted)"

        lines.extend([
            f"## {status_box} — `{cid}`: {c['title']}",
            f"- **Video File**: {file_link}",
            f"- **Virality Score**: `{c.get('score', 80)}/100` | **Duration**: `{c.get('duration', 0):.1f}s`",
            f"- **Status**: `{c['status']}`" + (f" (Uploaded at: {c.get('uploaded_at')})" if c.get("uploaded_at") else ""),
            "",
            "#### 📝 Copy-Paste Title (YouTube Shorts / Reels / TikTok):",
            "```text",
            c["title"],
            "```",
            "",
            "#### 💬 Optimized Caption & Description:",
            "```text",
            c["caption"],
            "```",
            "",
            "#### 🏷️ High-Reach Hashtags:",
            "```text",
            c["hashtags"],
            "```",
            "",
            "#### 📌 Algorithm Booster Strategy:",
            f"- **Pinned Comment**: `{c.get('pinned_comment', 'What do you think? Comment below! 👇')}`",
            f"- **Best Posting Window**: `{c.get('posting_window', '6:00 PM - 9:30 PM (Peak Viewer Activity)')}`",
            f"- **Sound Selection**: Use trending sound at 5-10% background volume.",
            "",
            "---",
            ""
        ])

    with open(TRACKER_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Updated {TRACKER_MD}")

def mark_clip(clip_id: str, auto_delete: bool = True):
    data = load_tracker()
    target = None
    for c in data["clips"]:
        if c["id"].lower() == clip_id.lower() or c["file_name"].lower() == clip_id.lower():
            target = c
            break

    if not target:
        print(f"Error: Clip '{clip_id}' not found in upload tracker.")
        return

    target["status"] = "UPLOADED"
    target["uploaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_p = Path(target.get("file_path", ""))
    if auto_delete:
        if file_p.exists():
            file_p.unlink()
            print(f"🗑️ [Deleted] Local video file removed from disk: {file_p}")
        else:
            print(f"ℹ️ File already removed or not found: {file_p}")

    save_tracker(data)
    print(f"✅ Clip '{clip_id}' marked as UPLOADED and {TRACKER_MD} updated!")

def list_clips():
    data = load_tracker()
    clips = data.get("clips", [])
    print("\n=== CURRENT UPLOAD QUEUE ===")
    for c in clips:
        mark = "✓ [DONE]" if c["status"] == "UPLOADED" else "⏳ [PENDING]"
        print(f"{mark} {c['id']}: {c['title']} ({c.get('duration', 0):.1f}s) -> Score: {c.get('score')}")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Tracker & Auto-Deleter")
    subparsers = parser.add_subparsers(dest="action")

    p_mark = subparsers.add_parser("mark", help="Mark clip as uploaded")
    p_mark.add_argument("clip_id", help="Clip ID (e.g. CLIP-01) or filename")
    p_mark.add_argument("--delete", action="store_true", default=True, help="Auto-delete local file (default: True)")
    p_mark.add_argument("--no-delete", action="store_false", dest="delete", help="Do not delete local file")

    p_list = subparsers.add_parser("list", help="List all clips in queue")

    args = parser.parse_args()
    if args.action == "mark":
        mark_clip(args.clip_id, auto_delete=args.delete)
    elif args.action == "list":
        list_clips()
    else:
        list_clips()
