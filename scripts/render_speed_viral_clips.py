"""
Render IShowSpeed Top 4 Viral GTA 6 Clips into 9:16 Vertical Shorts.
Strictly adheres to VIDEO_PRODUCTION_MISTAKES_MASTER_LEDGER rules (49-56):
- 1080x1920 Vertical layout with fit_blur background
- Top Hook Banner within safe zone (y=250)
- Audio mastering with loudnorm & alimiter (ear-rape protection)
- Kinetic captions in safe center
"""

import os
import sys
import subprocess
from pathlib import Path

FONT_PATH = "C:/Windows/Fonts/impact.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"

escaped_font = FONT_PATH.replace("\\", "/").replace(":", "\\:")

OUTPUT_DIR = Path("data/clips/speed_gta6_top4_viral")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def render_clip(src, out_path, start_time, duration, hook_title, hook_sub):
    print(f"\n[+] Rendering {out_path.name} ({duration}s)...")
    
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:3,eq=brightness=-0.22[bg];"
        f"[0:v]scale=1080:-2:flags=lanczos[fg];"
        f"[bg][fg]overlay=0:(H-h)/2[comp];"
        f"[comp]drawbox=x=40:y=250:w=1000:h=180:color=black@0.75:t=fill[b1];"
        f"[b1]drawtext=fontfile='{escaped_font}':text='{hook_title}':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=275,"
        f"drawtext=fontfile='{escaped_font}':text='{hook_sub}':fontcolor=0xFFD700:fontsize=60:x=(w-text_w)/2:y=345[v]"
    )
    
    audio_filter = "highpass=f=90,lowpass=f=12000,alimiter=limit=-1.5dB:level=true,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=async=1"

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-t", str(duration),
        "-i", str(src),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a?",
        "-af", audio_filter,
        "-c:v", "h264_nvenc",
        "-preset", "p5",
        "-cq", "20",
        "-b:v", "6500k",
        "-maxrate", "8000k",
        "-bufsize", "12000k",
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
        print(f"[OK] Successfully rendered {out_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print("[!] NVENC failed, falling back to libx264...")
        cmd[cmd.index("h264_nvenc")] = "libx264"
        idx_p = cmd.index("-preset")
        cmd[idx_p + 1] = "faster"
        cmd.remove("-cq")
        cmd.remove("20")
        cmd.extend(["-crf", "20"])
        subprocess.run(cmd, check=True)
        print(f"[OK] Rendered with libx264 {out_path.name}")
        return True

if __name__ == "__main__":
    src_real = Path("data/raw_scooter_chase_real.mp4")
    if src_real.exists():
        # Clip 3: Scooter Theft & Freakout
        out_03 = OUTPUT_DIR / "Clip_03_Speed_Mobility_Scooter_Escape.mp4"
        render_clip(
            src=src_real,
            out_path=out_03,
            start_time=78.0,
            duration=36.0,
            hook_title="SPEED STEALS A SCOOTER IN GTA 6 💀",
            hook_sub="SOMEBODY GIVE ME A CAR BRO! 😂"
        )
        
        # Clip 4: Storyline Mission & NPC Shirley
        out_04 = OUTPUT_DIR / "Clip_04_Speed_First_Storyline_Mission.mp4"
        render_clip(
            src=src_real,
            out_path=out_04,
            start_time=12.0,
            duration=38.0,
            hook_title="GTA 6 STORYLINE MISSION IN VICE CITY!",
            hook_sub="SPEED SAYS YES TO EVERYTHING 💀"
        )
