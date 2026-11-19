"""Master Scheduler & Posting Planner Builder for 42 GTA 6 Clips.

Interleaves 11 Gameplay Walkthrough parts with 31 CarryMinati Viral 80+ clips.
Applies the dynamic rotating gap sequence: 45m -> 46m -> 50m -> 55m -> 60m -> repeat.
Generates MASTER_UPLOAD_SCHEDULE.md and syncs data/upload_tracker.json.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRACKER_JSON = BASE_DIR / "data" / "upload_tracker.json"
SCHEDULE_MD = BASE_DIR / "MASTER_UPLOAD_SCHEDULE.md"

DYNAMIC_GAPS = [45, 46, 50, 55, 60]

GAMEPLAY_PARTS = [
    {
        "id": "GP-01",
        "file_name": "GTA6_Gameplay_Part_01.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_01.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 1 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 1 🔥\nThe journey starts now! Continuous walkthrough series.\nFollow for all parts today!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels #Viral",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels #Viral",
        "pinned_comment": "Are you excited for the full GTA 6 release? What graphics detail stood out most? 👇",
    },
    {
        "id": "GP-02",
        "file_name": "GTA6_Gameplay_Part_02.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_02.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 2 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 2 🔥\nContinuing right from where Part 1 ended!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #GamingReels #Reels #Shorts",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #GamingReels #Reels #Shorts",
        "pinned_comment": "Notice the vehicle physics in this part? How does it compare to GTA 5? 🚗👇",
    },
    {
        "id": "GP-03",
        "file_name": "GTA6_Gameplay_Part_03.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_03.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 3 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 3 🔥\nThe action continues! Follow to catch the full series!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "pinned_comment": "Rate Vice City's lighting in this sequence from 1-10! 🔥",
    },
    {
        "id": "GP-04",
        "file_name": "GTA6_Gameplay_Part_04.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_04.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 4 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 4 🔥\nContinuous gameplay walkthrough.\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "pinned_comment": "Lucia and Jason's partnership dynamic in action! What do you think? 💥",
    },
    {
        "id": "GP-05",
        "file_name": "GTA6_Gameplay_Part_05.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_05.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 5 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 5 🔥\nHalfway through the opening mission arc!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #ViralReels #Shorts",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #ViralReels #Shorts",
        "pinned_comment": "Are you playing day one on console or waiting for PC release? 🎮👇",
    },
    {
        "id": "GP-06",
        "file_name": "GTA6_Gameplay_Part_06.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_06.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 6 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 6 🔥\nIntense sequence in Vice City!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "pinned_comment": "Which GTA radio station do you want back in GTA 6? 📻",
    },
    {
        "id": "GP-07",
        "file_name": "GTA6_Gameplay_Part_07.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_07.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 7 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 7 🔥\nIntense Vice City action! Part 8 coming up soon.\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "pinned_comment": "Did you spot the Florida wildlife details in the background? 🐊🌴",
    },
    {
        "id": "GP-08",
        "file_name": "GTA6_Gameplay_Part_08.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_08.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 8 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 8 🔥\nNext gen graphics and details in full 4K!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "pinned_comment": "The NPC crowd density here is unbelievable! Thoughts? 👇",
    },
    {
        "id": "GP-09",
        "file_name": "GTA6_Gameplay_Part_09.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_09.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 9 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 9 🔥\nApproaching the climax of the walkthrough!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "pinned_comment": "Almost at the finale! Subscribe so you don't miss Part 10 & 11! 🔔",
    },
    {
        "id": "GP-10",
        "file_name": "GTA6_Gameplay_Part_10.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_10.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 10 #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 88.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 10 🔥\nClimax mission! The Grand Finale drops next!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "pinned_comment": "Get ready for the final sequence! Drop a like for Part 11! 🔥",
    },
    {
        "id": "GP-11",
        "file_name": "GTA6_Gameplay_Part_11.mp4",
        "file_path": str(BASE_DIR / "gta6_gameplay_series" / "clips" / "GTA6_Gameplay_Part_11.mp4").replace("\\", "/"),
        "title": "GTA 6 Gameplay Walkthrough - Part 11 (Series Finale) #Shorts #GTA6",
        "type": "Gameplay Walkthrough",
        "score": 90.0,
        "duration": 55.0,
        "caption": "GTA 6 Full Gameplay Walkthrough - Part 11 (Series Finale) 🔥\nThe full mission is complete! Watch all 11 parts sequentially on our profile!\n\n#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "hashtags": "#GTA6 #GrandTheftAuto6 #GTA6Gameplay #RockstarGames #Gaming #Shorts #Reels",
        "pinned_comment": "Which part was your absolute favorite? Thank you for watching the series! ❤️",
    }
]

def build_master_timeline(start_time: datetime | None = None):
    if start_time is None:
        start_time = datetime.now()

    # Load 31 CarryMinati clips
    if not TRACKER_JSON.exists():
        print(f"Error: {TRACKER_JSON} not found.")
        return

    with open(TRACKER_JSON, "r", encoding="utf-8") as f:
        tracker_data = json.load(f)
    carry_clips = tracker_data.get("clips", [])

    # Interleave: 1 Gameplay -> 3 Carry -> 1 Gameplay -> 3 Carry ...
    # 11 Gameplay + 31 Carry = 42 clips
    merged_queue = []
    gp_idx = 0
    carry_idx = 0

    while gp_idx < len(GAMEPLAY_PARTS) or carry_idx < len(carry_clips):
        # Add 1 gameplay part
        if gp_idx < len(GAMEPLAY_PARTS):
            merged_queue.append(GAMEPLAY_PARTS[gp_idx])
            gp_idx += 1

        # Add up to 3 carry clips
        for _ in range(3):
            if carry_idx < len(carry_clips):
                merged_queue.append(carry_clips[carry_idx])
                carry_idx += 1

    # Assign dynamic rotating time gaps
    current_time = start_time
    scheduled_items = []

    for i, item in enumerate(merged_queue):
        gap = DYNAMIC_GAPS[i % len(DYNAMIC_GAPS)]
        sched_time_str = current_time.strftime("%I:%M %p")
        sched_date_str = current_time.strftime("%d %b %Y")
        
        file_path_str = item.get("file_path", "")
        file_uri = Path(file_path_str).as_uri() if file_path_str and Path(file_path_str).exists() else ""
        file_link = f"[{item['file_name']}]({file_uri})" if file_uri else f"`{item['file_name']}`"

        entry = {
            "queue_num": i + 1,
            "id": item["id"],
            "category": item.get("type", "CarryMinati Viral 80+"),
            "file_name": item["file_name"],
            "file_path": file_path_str,
            "file_link": file_link,
            "title": item["title"],
            "score": item.get("score", 85.0),
            "duration": item.get("duration", 20.0),
            "scheduled_time": f"{sched_time_str} ({sched_date_str})",
            "interval_to_next": f"{gap} মিনিট",
            "gap_minutes": gap,
            "status": item.get("status", "READY"),
            "caption": item["caption"],
            "hashtags": item["hashtags"],
            "pinned_comment": item.get("pinned_comment", "Rate this GTA 6 moment 1-10! 👇")
        }
        scheduled_items.append(entry)
        current_time += timedelta(minutes=gap)

    # Save to MASTER_UPLOAD_SCHEDULE.md
    md_lines = [
        "# 🗓️ GTA 6 Master Upload Timeline & Dynamic Auto-Scheduler",
        "",
        "> **Total Scheduled Content**: `42 Clips` (11 Gameplay Walkthroughs + 31 CarryMinati Viral 80+ Reactions)  ",
        "> **Anti-Bot Dynamic Interval Rotation**: `45 min ➔ 46 min ➔ 50 min ➔ 55 min ➔ 60 min ➔ (Repeat)`  ",
        "> **Status**: `Ready to Post` | **Local Storage Auto-Delete**: `Enabled on Upload`",
        "",
        "---",
        "",
        "## ⏱️ আজকের ও আগামীকালের পোস্টিং রোটেশন টাইমলাইন (Master Schedule)",
        "",
        "| স্লট | আইডি | ক্যাটাগরি | ভিডিও ফাইল | নির্ধারিত সময় (BDT) | পরবর্তী বিরতি | স্ট্যাটাস |",
        "|---|---|---|---|---|---|---|"
    ]

    for s in scheduled_items:
        stat_badge = "✅ [UPLOADED]" if s["status"] == "UPLOADED" else "⏳ [READY]"
        md_lines.append(
            f"| **#{s['queue_num']:02d}** | `{s['id']}` | {s['category']} | {s['file_link']} | **{s['scheduled_time']}** | `{s['interval_to_next']}` | {stat_badge} |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 🚀 এক ক্লিকে আপলোড ও অটো-ডিলিট কমান্ড",
        "",
        "যেকোনো স্লট আপলোড করা শেষ হলে শুধু এই কমান্ডটি দিন:",
        "```powershell",
        ".venv\\Scripts\\python.exe scripts\\dynamic_scheduler.py mark <ID> --delete",
        "```",
        "*উদাহরণ: `.venv\\Scripts\\python.exe scripts\\dynamic_scheduler.py mark GP-01 --delete`*",
        "*(এটি সাথে সাথে এই ফাইলে স্ট্যাটাস `[UPLOADED]` মার্ক করবে এবং পিসি থেকে ভিডিও ফাইল মুছে জায়গা খালি করবে)*",
        "",
        "---",
        "",
        "## 📝 বিস্তারিত মেটাডাটা ও কপি-পেস্ট কন্টেন্ট (সকল ৪২টি ক্লিপ)",
        ""
    ])

    for s in scheduled_items:
        md_lines.extend([
            f"### স্লট #{s['queue_num']:02d} — `{s['id']}`: {s['title']}",
            f"- **ক্যাটাগরি**: `{s['category']}` | **ভিডিও ফাইল**: {s['file_link']}",
            f"- **নির্ধারিত সময়**: **{s['scheduled_time']}** (পরবর্তী বিরতি: `{s['interval_to_next']}`)",
            f"- **স্কোর**: `{s['score']}/100` | **দৈর্ঘ্য**: `{s['duration']:.1f}s`",
            "",
            "#### 📌 Copy Title:",
            "```text",
            s["title"],
            "```",
            "",
            "#### 💬 Caption / Description:",
            "```text",
            s["caption"],
            "```",
            "",
            "#### 🏷️ Hashtags:",
            "```text",
            s["hashtags"],
            "```",
            "",
            "#### 💬 Pinned Comment Booster:",
            f"`{s['pinned_comment']}`",
            "",
            "---",
            ""
        ])

    with open(SCHEDULE_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Generated {SCHEDULE_MD}")

    # Also save json database
    json_path = BASE_DIR / "data" / "master_schedule.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"total_clips": len(scheduled_items), "items": scheduled_items}, f, indent=2, ensure_ascii=False)
    print(f"Saved {json_path}")

if __name__ == "__main__":
    build_master_timeline()
