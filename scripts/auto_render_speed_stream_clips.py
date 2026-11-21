"""
IShowSpeed GTA 6 Stream Viral Clipping & Rendering Pipeline.
Processes top viral moments directly from the 23-hour YouTube stream:
https://www.youtube.com/watch?v=qSyo5d-dVzA

Features:
- Precision section download via yt-dlp (no 80GB full video download)
- 9:16 vertical 1080x1920 layout with fast optimized background blur
- Dynamic safe-zone high-contrast hook banners (Impact/Arial Black)
- Loudnorm & limiter acoustic protection (anti ear-rape for Speed screaming)
- Generates master POSTING_PACK.md
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path("E:/work station/gta 6")
RAW_DIR = BASE_DIR / "data/downloads/speed_raw"
CLIPS_DIR = BASE_DIR / "data/clips/speed_gta6_viral"
RAW_DIR.mkdir(parents=True, exist_ok=True)
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

PYTHON_EXE = str(BASE_DIR / ".venv/Scripts/python.exe")
STREAM_URL = "https://www.youtube.com/watch?v=qSyo5d-dVzA"

FONT_PATH = "C:/Windows/Fonts/impact.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
escaped_font = FONT_PATH.replace("\\", "/").replace(":", "\\:")

# Top viral moments from data/viral_22_evaluated.json
VIRAL_MOMENTS = [
    {
        "clip_no": 1,
        "name": "IShowSpeed_Clip_01_Backflip_Prep_Hype.mp4",
        "start": 390.0,
        "end": 438.0,
        "score": 91.0,
        "hook_title": "SPEED PLAYING GTA 6 FOR THE FIRST TIME",
        "hook_sub": "HE TRIED DOING A BACKFLIP BRO!",
        "desc": "Speed loads into GTA 6 for the first time and gets so hyped he considers doing a backflip on stream."
    },
    {
        "clip_no": 2,
        "name": "IShowSpeed_Clip_02_Vice_City_Freakout.mp4",
        "start": 2175.0,
        "end": 2223.0,
        "score": 92.5,
        "hook_title": "SPEED DISCOVERS VICE CITY IN GTA 6",
        "hook_sub": "THE GRAPHICS BROKE HIS BRAIN!",
        "desc": "Speed witnesses Vice City next-gen lighting and physics, going into full screaming mode."
    },
    {
        "clip_no": 3,
        "name": "IShowSpeed_Clip_03_Veggie_Dance_Shoe_Store.mp4",
        "start": 5475.0,
        "end": 5523.0,
        "score": 92.5,
        "hook_title": "SPEED DOES VEGGIE DANCE IN GTA 6",
        "hook_sub": "LOOKING FOR A SHOE STORE AT 2 AM!",
        "desc": "Speed breaks into a random dance routine looking for custom shoes in the middle of Ocean Drive."
    },
    {
        "clip_no": 4,
        "name": "IShowSpeed_Clip_04_On_The_Run_Panic.mp4",
        "start": 6765.0,
        "end": 6813.0,
        "score": 92.5,
        "hook_title": "SPEED BEING HUNTED BY GTA 6 POLICE",
        "hook_sub": "JUST RUN BRO NO LOOKING BACK!",
        "desc": "Intense police pursuit through back alleys with zero ammunition left."
    },
    {
        "clip_no": 5,
        "name": "IShowSpeed_Clip_05_Reading_Chat_Roasts.mp4",
        "start": 8730.0,
        "end": 8778.0,
        "score": 91.0,
        "hook_title": "SPEED ARGUING WITH HIS CHAT IN GTA 6",
        "hook_sub": "YES I AM READING THE CHAT BRO!",
        "desc": "Chat roasts Speed for terrible driving and he fires back with maximum energy."
    },
    {
        "clip_no": 6,
        "name": "IShowSpeed_Clip_06_Gun_Store_Price_Shock.mp4",
        "start": 10185.0,
        "end": 10233.0,
        "score": 91.0,
        "hook_title": "GTA 6 INFLATION SHOCKED SPEED",
        "hook_sub": "WHY ARE THESE GUNS SO EXPENSIVE?!",
        "desc": "Speed enters Ammu-Nation and realizes Vice City inflation makes rocket launchers unaffordable."
    },
    {
        "clip_no": 7,
        "name": "IShowSpeed_Clip_07_Speedy_Old_Man_Chase.mp4",
        "start": 12495.0,
        "end": 12543.0,
        "score": 91.9,
        "hook_title": "GTA 6 OLD MAN OUTRUNS SPEED?!",
        "hook_sub": "HOW IS THIS NPC THIS FAST BRO!",
        "desc": "Speed tries to mug an elderly NPC who suddenly sprints away at Olympic track speed."
    },
    {
        "clip_no": 8,
        "name": "IShowSpeed_Clip_08_Should_I_Do_It_Dilemma.mp4",
        "start": 15600.0,
        "end": 15648.0,
        "score": 91.0,
        "hook_title": "SPEEDS BIGGEST DILEMMA IN GTA 6",
        "hook_sub": "SHOULD I GO INSIDE OR RUN CHAT?!",
        "desc": "Speed hesitates before triggering a dangerous story mission that traps him inside."
    },
    {
        "clip_no": 9,
        "name": "IShowSpeed_Clip_09_Lucia_Jason_Welcome_Wagon.mp4",
        "start": 18780.0,
        "end": 18828.0,
        "score": 89.5,
        "hook_title": "SPEED INTRODUCES LUCIA AND JASON",
        "hook_sub": "ROLL OUT THE WELCOME WAGON BRO!",
        "desc": "Lucia and Jason team-up sequence with Speed providing hilarious live commentary."
    },
    {
        "clip_no": 10,
        "name": "IShowSpeed_Clip_10_Florida_Gas_Station_Standoff.mp4",
        "start": 21045.0,
        "end": 21093.0,
        "score": 90.5,
        "hook_title": "GTA 6 GAS STATION GONE WRONG",
        "hook_sub": "WHAT IS IT GONNA BE CHAT?!",
        "desc": "Store robbery turns into a 3-way standoff between clerks, gangsters, and Speed."
    },
    {
        "clip_no": 11,
        "name": "IShowSpeed_Clip_11_Shower_Scene_Freakout.mp4",
        "start": 30795.0,
        "end": 30843.0,
        "score": 93.5,
        "hook_title": "SPEED REACTS TO GTA 6 MOTEL SCENE",
        "hook_sub": "BRO JASON WHERE ARE YOU AT?!",
        "desc": "The viral motel scene moment where Speed panics looking for Jason."
    },
    {
        "clip_no": 12,
        "name": "IShowSpeed_Clip_12_Vice_City_100MPH_Chase.mp4",
        "start": 32370.0,
        "end": 32418.0,
        "score": 94.0,
        "hook_title": "SPEED CAUGHT IN 100 MPH POLICE CHASE",
        "hook_sub": "YOU CATCHING UP OR WHAT?!",
        "desc": "High speed freeway shootout with police cruisers flipping over concrete barriers."
    },
    {
        "clip_no": 13,
        "name": "IShowSpeed_Clip_13_Bridge_Flip_Car_Wreck.mp4",
        "start": 36630.0,
        "end": 36678.0,
        "score": 91.0,
        "hook_title": "SPEED TOTALS A 500K CAR IN GTA 6",
        "hook_sub": "OH MY GOD HE MESSED UP BIG TIME!",
        "desc": "Speed takes a drawbridge jump at full speed and spirals into oncoming traffic."
    },
    {
        "clip_no": 14,
        "name": "IShowSpeed_Clip_14_Florida_Woman_NPC_Magic.mp4",
        "start": 40095.0,
        "end": 40143.0,
        "score": 90.0,
        "hook_title": "ONLY IN FLORIDA GTA 6 EDITION",
        "hook_sub": "SHE JUST PULLED WHAT OUT OF WHERE?!",
        "desc": "A wild interaction with a Vice City resident carrying weird street items."
    },
    {
        "clip_no": 15,
        "name": "IShowSpeed_Clip_15_Car_Theft_Fail_Arrest.mp4",
        "start": 46200.0,
        "end": 46248.0,
        "score": 91.0,
        "hook_title": "SPEED TRIES TO STEAL A RUNNING CAR",
        "hook_sub": "NO NO NO DONT GET IN THERE!",
        "desc": "Speed accidentally gets into a parked undercover detective car."
    },
    {
        "clip_no": 16,
        "name": "IShowSpeed_Clip_16_Drop_The_Phone_Panic.mp4",
        "start": 48705.0,
        "end": 48753.0,
        "score": 91.0,
        "hook_title": "SPEEDS CONTROLLER BATTERY DIED",
        "hook_sub": "CHAT IF I DROP THIS WE ARE COOKED!",
        "desc": "Controller battery warnings trigger during an intense escape gunfight."
    },
    {
        "clip_no": 17,
        "name": "IShowSpeed_Clip_17_Searching_For_Lucia_Lost.mp4",
        "start": 53145.0,
        "end": 53193.0,
        "score": 91.0,
        "hook_title": "SPEED CANNOT FIND LUCIA ANYWHERE",
        "hook_sub": "JASON BRO FIND LUCIA RIGHT NOW!",
        "desc": "Speed gets lost in a 3-story Vice City luxury mall calling for Lucia."
    },
    {
        "clip_no": 18,
        "name": "IShowSpeed_Clip_18_Street_Reunion_Brawl.mp4",
        "start": 60750.0,
        "end": 60798.0,
        "score": 96.5,
        "hook_title": "SPEED MEETS HIS OLD FRIEND IN GTA 6",
        "hook_sub": "YOU REMEMBER ME BRO?! 💀",
        "desc": "Top viral score: An NPC that looks suspiciously familiar starts a full street brawl."
    },
    {
        "clip_no": 19,
        "name": "IShowSpeed_Clip_19_Vice_City_Club_Vibes.mp4",
        "start": 64785.0,
        "end": 64833.0,
        "score": 95.0,
        "hook_title": "SPEED VISITING THE MALIBU CLUB",
        "hook_sub": "ROCKSTAR WENT CRAZY ON THIS!",
        "desc": "Inside the vibrant neon nightclub with next-gen crowd rendering."
    },
    {
        "clip_no": 20,
        "name": "IShowSpeed_Clip_20_Mansion_Party_Invader.mp4",
        "start": 74910.0,
        "end": 74958.0,
        "score": 90.0,
        "hook_title": "SPEED CRASHING A GTA 6 MANSION PARTY",
        "hook_sub": "ABOUT TO BE A MOVIE IN HERE!",
        "desc": "Speed sneaks into an elite rooftop party and gets chased by private bodyguards."
    },
    {
        "clip_no": 21,
        "name": "IShowSpeed_Clip_21_Ocean_Drive_Drag_Race.mp4",
        "start": 76845.0,
        "end": 76893.0,
        "score": 90.0,
        "hook_title": "SPEED CHALLENGES STREET RACERS",
        "hook_sub": "SHOW ME SOME MOVES ON THE WAY!",
        "desc": "High stakes midnight drag race along Ocean Drive palm trees."
    },
    {
        "clip_no": 22,
        "name": "IShowSpeed_Clip_22_Hypercar_250MPH_Crash.mp4",
        "start": 84945.0,
        "end": 84993.0,
        "score": 90.9,
        "hook_title": "SPEED FINDS FASTEST CAR IN GTA 6",
        "hook_sub": "THIS CAR IS TOO FAST FOR HIM!",
        "desc": "Final marathon stream climax: Driving at top speed across the cross-county highway."
    }
]

def sec_to_tc(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def download_section(start_sec: float, end_sec: float, raw_path: Path):
    if raw_path.exists() and raw_path.stat().st_size > 1024 * 500:
        return True
    
    st_tc = sec_to_tc(start_sec)
    et_tc = sec_to_tc(end_sec)
    time_range = f"*{st_tc}-{et_tc}"
    print(f"  [yt-dlp] Downloading {time_range} -> {raw_path.name}...")
    
    cmd = [
        PYTHON_EXE, "-m", "yt_dlp",
        "--download-sections", time_range,
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--merge-output-format", "mp4",
        "-o", str(raw_path),
        STREAM_URL
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return raw_path.exists() and raw_path.stat().st_size > 1024 * 500

def sanitize_text(txt: str) -> str:
    clean = txt.replace("'", "").replace(":", " -").replace("%", " pct")
    clean = "".join([c for c in clean if ord(c) < 128])
    return clean.strip()

def render_clip(raw_path: Path, out_path: Path, hook_title: str, hook_sub: str):
    if out_path.exists() and out_path.stat().st_size > 1024 * 500:
        return True
    
    h_title = sanitize_text(hook_title)
    h_sub = sanitize_text(hook_sub)

    # Ultra-fast 2-tier scale + boxblur
    filter_complex = (
        f"[0:v]scale=360:640:force_original_aspect_ratio=increase,crop=360:640,boxblur=12:2,scale=1080:1920:flags=lanczos,eq=brightness=-0.22[bg];"
        f"[0:v]scale=1080:-2:flags=lanczos[fg];"
        f"[bg][fg]overlay=0:(H-h)/2[comp];"
        f"[comp]drawbox=x=40:y=250:w=1000:h=180:color=black@0.75:t=fill[b1];"
        f"[b1]drawtext=fontfile='{escaped_font}':text='{h_title}':fontcolor=white:fontsize=46:x=(w-text_w)/2:y=275,"
        f"drawtext=fontfile='{escaped_font}':text='{h_sub}':fontcolor=0xFFD700:fontsize=52:x=(w-text_w)/2:y=345[v]"
    )
    audio_filter = "highpass=f=90,lowpass=f=12000,alimiter=limit=-1.5dB:level=true,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=async=1"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_path),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a?",
        "-af", audio_filter,
        "-c:v", "h264_nvenc",
        "-preset", "p4",
        "-cq", "23",
        "-b:v", "5500k",
        "-maxrate", "7000k",
        "-bufsize", "10000k",
        "-pix_fmt", "yuv420p",
        "-fps_mode", "cfr",
        "-r", "60",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-avoid_negative_ts", "make_zero",
        "-movflags", "+faststart",
        str(out_path)
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        # Fallback to libx264
        cmd[cmd.index("h264_nvenc")] = "libx264"
        idx_p = cmd.index("-preset")
        cmd[idx_p + 1] = "faster"
        cmd.remove("-cq")
        cmd.remove("23")
        cmd.extend(["-crf", "22"])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True

def generate_posting_pack(clips_list):
    md_lines = [
        "# 🚀 IShowSpeed GTA 6 Top Viral Clips — Master Posting Pack",
        "",
        "> **Creator**: IShowSpeed (@IShowSpeed)  ",
        f"> **Source**: [{STREAM_URL}]({STREAM_URL})  ",
        "> **Format**: 9:16 Vertical Shorts/Reels (1080x1920, 60 FPS)  ",
        "> **Mastering**: Loudnorm -16 LUFS, Limiter -1.5dB  ",
        "",
        "---",
        ""
    ]

    for item in clips_list:
        md_lines.extend([
            f"## Part {item['clip_no']:02d}: {item['hook_title']}",
            f"- **Filename**: `{item['name']}`",
            f"- **Virality Score**: `{item['score']}/100`",
            f"- **Stream Time**: `{sec_to_tc(item['start'])} - {sec_to_tc(item['end'])}`",
            f"- **Hook Banner**: `{item['hook_title']}` | `{item['hook_sub']}`",
            "",
            "### 📋 Copy-Paste Metadata",
            "**Title:**",
            f"```text\n{item['hook_title']} 💀 #IShowSpeed #GTA6 #Shorts\n```",
            "",
            "**Description:**",
            f"```text\n{item['desc']}\n\nSubscribe for daily GTA 6 moments and highlights!\n\n#IShowSpeed #GTA6 #Gaming #Shorts #ViceCity #Viral\n```",
            "",
            "---",
            ""
        ])

    pack_path = CLIPS_DIR / "POSTING_PACK.md"
    pack_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"[OK] Master Posting Pack generated at: {pack_path}")

def main():
    print(f"=== Starting IShowSpeed GTA 6 Stream Clipping Pipeline ===")
    print(f"Target directory: {CLIPS_DIR}")
    print(f"Total viral moments to process: {len(VIRAL_MOMENTS)}")
    
    successful_renders = 0
    for idx, item in enumerate(VIRAL_MOMENTS, 1):
        raw_name = f"raw_speed_clip_{item['clip_no']:02d}.mp4"
        raw_path = RAW_DIR / raw_name
        out_path = CLIPS_DIR / item["name"]
        
        print(f"\n[{idx}/{len(VIRAL_MOMENTS)}] Processing Clip {item['clip_no']:02d}: {item['name']}")
        
        # Step 1: Download segment
        dl_ok = download_section(item["start"], item["end"], raw_path)
        if not dl_ok:
            print(f"  [!] Failed to download section for Clip {item['clip_no']:02d}, skipping...")
            continue
            
        # Step 2: Render
        print(f"  [FFmpeg] Rendering 9:16 vertical video...")
        render_ok = render_clip(raw_path, out_path, item["hook_title"], item["hook_sub"])
        if render_ok:
            successful_renders += 1
            print(f"  [OK] Successfully rendered {out_path.name} ({out_path.stat().st_size / 1024 / 1024:.2f} MB)")
        else:
            print(f"  [!] Render failed for {out_path.name}")
            
    generate_posting_pack(VIRAL_MOMENTS)
    print(f"\n=== Done! Rendered {successful_renders}/{len(VIRAL_MOMENTS)} clips in {CLIPS_DIR} ===")

if __name__ == "__main__":
    main()
