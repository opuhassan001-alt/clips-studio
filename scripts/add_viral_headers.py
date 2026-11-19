"""Add high-impact viral hook headlines to top-scoring 80+ clips.

Applies a professional YouTube Shorts / TikTok style bold header banner
at the top of each clip with NVENC hardware acceleration.
"""

import subprocess
from pathlib import Path

VIRAL_HOOKS = {
    "clip_00415-00430.mp4": "CARRY MINATIS REACTION TO GTA 6",
    "clip_00811-00827.mp4": "WAIT TILL THE END - GTA 6",
    "clip_00142-00156.mp4": "CARRY RECALLS HIS FIRST GTA",
    "clip_00276-00296.mp4": "TARGET 10K LIKES FOR GTA 6",
    "clip_00034-00061.mp4": "CRAZY GTA 6 HYPE MOMENT",
    "clip_00018-00030.mp4": "TODAY IS SPECIAL - GTA 6 REVEAL",
    "clip_00065-00079.mp4": "16 YEARS OF WAITING IS OVER",
    "clip_00429-00460.mp4": "GTA 6 GAMEPLAY SETTINGS EXPLAINED"
}

def add_headers_to_viral_clips():
    viral_dir = Path("data/clips/carry_action_15m/selected_viral_80_plus")
    if not viral_dir.exists():
        print(f"Error: {viral_dir} not found.")
        return
        
    font_path = "C:/Windows/Fonts/impact.ttf"
    if not Path(font_path).exists():
        font_path = "C:/Windows/Fonts/arialbd.ttf"
    escaped_font = str(Path(font_path).as_posix()).replace(":", "\\:")

    for filename, hook_text in VIRAL_HOOKS.items():
        src_clip = viral_dir / filename
        if not src_clip.exists():
            continue
            
        temp_out = viral_dir / f"enhanced_{filename}"
        
        # Drawtext filter with dark translucent pill box, centered text, Impact bold font
        vf_filter = (
            f"drawtext=text='{hook_text}':"
            f"fontfile='{escaped_font}':"
            f"fontsize=56:"
            f"fontcolor=white:"
            f"box=1:boxcolor=black@0.75:boxborderw=20:"
            f"x=(w-text_w)/2:y=160"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(src_clip),
            "-vf", vf_filter,
            "-c:v", "h264_nvenc", "-preset", "p4", "-cq", "20",
            "-c:a", "copy",
            str(temp_out)
        ]
        
        print(f"Enhancing {filename} with hook: \"{hook_text}\"...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            # Overwrite original with enhanced version
            temp_out.replace(src_clip)
            print(f"  -> [Success] Enhanced and saved {filename}")
        else:
            print(f"  -> [Error] Failed on {filename}: {res.stderr[-200:]}")
            if temp_out.exists():
                temp_out.unlink()

if __name__ == "__main__":
    add_headers_to_viral_clips()
