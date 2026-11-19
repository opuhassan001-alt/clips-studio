import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(r"E:\work station\gta 6")
TRACKER_JSON = BASE_DIR / "data" / "upload_tracker.json"
SCHEDULE_JSON = BASE_DIR / "data" / "master_schedule.json"
SCHEDULE_MD = BASE_DIR / "MASTER_UPLOAD_SCHEDULE.md"

with open(TRACKER_JSON, "r", encoding="utf-8") as f:
    tracker = json.load(f)

clips = tracker.get("clips", [])
start = datetime(2026, 11, 20, 8, 0)
gaps = [45, 46, 50, 55, 60]

scheduled_items = []
curr = start

for i, c in enumerate(clips):
    gap = gaps[i % len(gaps)]
    time_str = curr.strftime("%I:%M %p (%d %b %Y)")
    scheduled_items.append({
        "slot": i + 1,
        "id": c["id"],
        "category": "CarryMinati Viral 80+",
        "file_name": c["file_name"],
        "file_path": c["file_path"],
        "scheduled_time": time_str,
        "scheduled_dt": curr.strftime("%Y-%m-%d %H:%M:%S"),
        "next_gap_minutes": gap,
        "status": "READY",
        "score": c["score"],
        "duration": c["duration"],
        "title": c["title"],
        "caption": c["caption"],
        "hashtags": c["hashtags"],
        "pinned_comment": c["pinned_comment"]
    })
    curr += timedelta(minutes=gap)

with open(SCHEDULE_JSON, "w", encoding="utf-8") as f:
    json.dump({"total_clips": len(scheduled_items), "items": scheduled_items}, f, indent=2, ensure_ascii=False)

# Build Markdown
lines = []
lines.append("# 🗓️ CarryMinati GTA 6 Viral Clips — Master Schedule (Starting Tomorrow 8:00 AM)\n")
lines.append("> **Total Viral Clips**: `31 Clips` (All 80+ Virality Score)")
lines.append("> **Start Time**: `20 Nov 2026, 08:00 AM BDT`")
lines.append("> **Anti-Bot Dynamic Interval**: `45m -> 46m -> 50m -> 55m -> 60m -> repeat`")
lines.append("> **Status**: `All Prepared with Captions & Optimized Metadata`\n")
lines.append("---\n")
lines.append("## ⏱️ সম্পূর্ণ পোস্টিং টাইমলাইন\n")
lines.append("| স্লট | আইডি | ভিডিও ফাইল | নির্ধারিত সময় (BDT) | বিরতি | স্কোর | স্ট্যাটাস |")
lines.append("|---|---|---|---|---|---|---|")

for it in scheduled_items:
    file_uri = Path(it["file_path"]).as_uri()
    lines.append(f"| **#{it['slot']:02d}** | `{it['id']}` | [{it['file_name']}]({file_uri}) | **{it['scheduled_time']}** | `{it['next_gap_minutes']} মি.` | `{it['score']}/100` | ⏳ [{it['status']}] |")

lines.append("\n---\n")
lines.append("## 📝 বিস্তারিত ক্যাপশন ও হ্যাশট্যাগ (প্রতিটি ক্লিপের জন্য প্রস্তুত)\n")

for it in scheduled_items:
    file_uri = Path(it["file_path"]).as_uri()
    lines.append(f"### স্লট #{it['slot']:02d} — `{it['id']}`: {it['title']}")
    lines.append(f"- **ভিডিও ফাইল**: [{it['file_name']}]({file_uri})")
    lines.append(f"- **নির্ধারিত সময়**: **{it['scheduled_time']}** (বিরতি: `{it['next_gap_minutes']} মিনিট`)")
    lines.append(f"- **স্কোর**: `{it['score']}/100` | **দৈর্ঘ্য**: `{it['duration']}s`\n")
    lines.append("#### 📌 Copy Title:")
    lines.append(f"```text\n{it['title']}\n```\n")
    lines.append("#### 💬 Caption & Hashtags:")
    lines.append(f"```text\n{it['caption']}\n\n{it['hashtags']}\n```\n")
    lines.append(f"#### 💬 Pinned Comment Booster:\n`{it['pinned_comment']}`\n")
    lines.append("---\n")

with open(SCHEDULE_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Master schedule updated successfully!")
