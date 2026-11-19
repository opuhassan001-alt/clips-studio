"""Append Part 2 High Score Clips to Upload Manager."""

import json
from pathlib import Path
from upload_manager import load_tracker, save_tracker

HOOK_SUGGESTIONS = {
    "clip_00387-00401.mp4": "COUNTY LOOKING TO FREE UP BEDS?! 💀 GTA 6",
    "clip_00995-01018.mp4": "WHO IS THIS CHARACTER IN GTA 6?! 🤯",
    "clip_00732-00747.mp4": "BEST BEHAVIOR IN GTA 6 JAIL?! 😂",
    "clip_00870-00887.mp4": "TURNING ON RADIO IN GTA 6 VICE CITY 📻",
    "clip_00364-00387.mp4": "BAD LUCK IN GTA 6 JAIL 😭",
    "clip_01033-01076.mp4": "CARRY MINATI ROASTS NEW GTA 6 NPC 🔥",
    "clip_01018-01032.mp4": "CAMERA MECHANICS IN GTA 6 📸",
    "clip_00414-00428.mp4": "CARRY GETS THE SIGN IN GTA 6 🤣",
    "clip_00092-00118.mp4": "GTA 6 PROLOGUE MISSION REACTION 💥",
    "clip_00183-00196.mp4": "CARRY TALKS ABOUT PS5 & GTA 6 🎮",
    "clip_00400-00414.mp4": "HOW LUCIA GOT IN TROUBLE IN GTA 6 🚔",
    "clip_00809-00857.mp4": "INSANE PSYCHOPATH NPC MOMENT 💀",
    "clip_01603-01616.mp4": "CHECK OUT THE SECRET IN GTA 6 👀",
    "clip_01616-01630.mp4": "SEEING VICE CITY FOR THE FIRST TIME 🌴",
    "clip_00594-00620.mp4": "CARRY APOLOGIZES DURING GTA 6 STREAM 😂",
    "clip_01275-01289.mp4": "HEADING TO THE BRINK IN GTA 6 🚗",
    "clip_00427-00453.mp4": "WAIT TWO MINUTES IN GTA 6 ⏳",
    "clip_00857-00870.mp4": "IS THAT A PLANE IN GTA 6?! ✈️",
    "clip_00901-00925.mp4": "GTA 6 POLICE ENCOUNTER MOMENT 🚨",
    "clip_01294-01309.mp4": "GTA 6 WEAPONS & LOADOUT REVEAL 🔫",
    "clip_01257-01275.mp4": "HILARIOUS ACCIDENT IN GTA 6 😂",
    "clip_01316-01361.mp4": "MEETING THE CRAZIEST NPC IN VICE CITY 💀",
    "clip_01666-01685.mp4": "BIG PROBLEM IN THE MISSION! 😱"
}

def append_part2():
    tracker = load_tracker()
    existing_ids = {c["file_name"] for c in tracker.get("clips", [])}
    
    cand_path = Path("data/clips/carry_part2_30m/delete_candidates.json")
    if not cand_path.exists():
        print("Candidate file not found.")
        return
        
    with open(cand_path, encoding="utf-8") as f:
        data = json.load(f)
        
    high_scores = data.get("high_score_clips", [])
    current_count = len(tracker.get("clips", []))
    
    for c in high_scores:
        fname = c["name"]
        if fname in existing_ids:
            continue
            
        current_count += 1
        cid = f"CLIP-{current_count:02d}"
        hook = HOOK_SUGGESTIONS.get(fname, f"GTA 6 CRAZY MOMENT #{current_count}")
        fpath = str((Path("data/clips/carry_part2_30m/selected_viral_80_plus") / fname).resolve()).replace("\\", "/")
        
        tracker["clips"].append({
            "id": cid,
            "file_name": fname,
            "file_path": fpath,
            "title": hook,
            "score": c.get("score", 85.0),
            "duration": c.get("duration", 20.0),
            "status": "READY",
            "caption": f"CarryMinati experiencing {hook.lower()} in GTA 6! The graphics and dialogues are on another level. What was your favorite moment? #GTA6 #CarryMinati #GrandTheftAuto6 #Gaming #Shorts",
            "hashtags": "#GTA6 #CarryMinati #GTA6Gameplay #GrandTheftAuto6 #RockstarGames #ViceCity #ViralGaming #ShortsFeed",
            "pinned_comment": f"Rate this GTA 6 moment from 1 to 10! 👇🔥",
            "posting_window": "5:30 PM - 9:30 PM (Peak Viral Reach)"
        })
        
    save_tracker(tracker)
    print(f"Total clips in UPLOAD_MANAGER.md: {len(tracker['clips'])}")

if __name__ == "__main__":
    append_part2()
