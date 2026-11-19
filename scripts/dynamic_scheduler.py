"""Dynamic Scheduler CLI for GTA 6 Master Upload Timeline.

Commands:
- list: Show schedule overview
- next: Show next pending clip details ready to post
- mark <ID> --delete: Mark clip as uploaded and permanently delete local video
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEDULE_JSON = BASE_DIR / "data" / "master_schedule.json"
SCHEDULE_MD = BASE_DIR / "MASTER_UPLOAD_SCHEDULE.md"

def load_data() -> dict:
    if not SCHEDULE_JSON.exists():
        print(f"Error: {SCHEDULE_JSON} not found. Run scripts/build_master_schedule.py first.")
        sys.exit(1)
    with open(SCHEDULE_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    with open(SCHEDULE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # Re-sync markdown
    from scripts.build_master_schedule import build_master_timeline
    # Update md status directly
    items = data.get("items", [])
    if SCHEDULE_MD.exists():
        with open(SCHEDULE_MD, "r", encoding="utf-8") as f:
            content = f.read()
        for it in items:
            cid = it["id"]
            if it["status"] == "UPLOADED":
                content = content.replace(f"| `{cid}` |", f"| `{cid}` |")
        # We can re-generate cleanly
        with open(SCHEDULE_MD, "w", encoding="utf-8") as f:
            f.write(content)

def mark_item(item_id: str, auto_delete: bool = True):
    data = load_data()
    target = None
    for it in data.get("items", []):
        if it["id"].lower() == item_id.lower() or it["file_name"].lower() == item_id.lower():
            target = it
            break

    if not target:
        print(f"Error: Item '{item_id}' not found in schedule.")
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

    # Save JSON
    with open(SCHEDULE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Update Markdown table line
    if SCHEDULE_MD.exists():
        with open(SCHEDULE_MD, "r", encoding="utf-8") as f:
            text = f.read()
        # Replace badge in table
        cid = target["id"]
        # Find line with cid and replace [READY] with [UPLOADED]
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            if f"`{cid}`" in line and "⏳ [READY]" in line:
                line = line.replace("⏳ [READY]", "✅ [UPLOADED]")
            new_lines.append(line)
        with open(SCHEDULE_MD, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))

    print(f"✅ Slot '{target['id']}' marked as UPLOADED in {SCHEDULE_MD}!")

def show_next():
    data = load_data()
    pending = [it for it in data.get("items", []) if it["status"] != "UPLOADED"]
    if not pending:
        print("🎉 Congratulations! All 42 clips have been uploaded!")
        return

    nxt = pending[0]
    print("\n" + "="*60)
    print(f"🚀 NEXT CLIP TO POST: Slot #{nxt['queue_num']:02d} ({nxt['id']})")
    print("="*60)
    print(f"Category: {nxt['category']}")
    print(f"Scheduled Time: {nxt['scheduled_time']} (Gap to next: {nxt['interval_to_next']})")
    print(f"Video File: {nxt['file_path']}")
    print("\n--- COPY-PASTE TITLE ---")
    print(nxt["title"])
    print("\n--- COPY-PASTE CAPTION ---")
    print(nxt["caption"])
    print("\n--- HASHTAGS ---")
    print(nxt["hashtags"])
    print("\n--- PINNED COMMENT ---")
    print(nxt["pinned_comment"])
    print("="*60 + "\n")

def list_items():
    data = load_data()
    items = data.get("items", [])
    print(f"\n=== MASTER SCHEDULE ({len(items)} TOTAL CLIPS) ===")
    for it in items:
        badge = "✅ [UPLOADED]" if it["status"] == "UPLOADED" else "⏳ [READY]"
        print(f"{badge} #{it['queue_num']:02d} [{it['id']}] {it['scheduled_time']} (Gap: {it['interval_to_next']}) -> {it['title'][:40]}")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic Scheduler CLI")
    sub = parser.add_subparsers(dest="action")

    p_mark = sub.add_parser("mark", help="Mark item as uploaded")
    p_mark.add_argument("item_id", help="Item ID (e.g. GP-01, CLIP-01)")
    p_mark.add_argument("--delete", action="store_true", default=True, help="Auto-delete local file (default: True)")
    p_mark.add_argument("--no-delete", action="store_false", dest="delete", help="Do not delete local file")

    sub.add_parser("next", help="Show next clip to upload")
    sub.add_parser("list", help="List all scheduled clips")

    args = parser.parse_args()
    if args.action == "mark":
        mark_item(args.item_id, auto_delete=args.delete)
    elif args.action == "next":
        show_next()
    elif args.action == "list":
        list_items()
    else:
        show_next()
