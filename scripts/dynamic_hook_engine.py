"""
Dynamic Context Hook Banner Engine for YouTube Shorts & Instagram Reels.
Automatically analyzes clip context/dialogue and bakes in a high-impact viral headline banner
(exact style: IShowSpeed / Viral Gaming Shorts - solid black box, bold white text, emojis).
100% Free & Local.
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path

# Common fonts on Windows / macOS / Linux
FONT_CANDIDATES = [
    "C:/Windows/Fonts/impact.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "/System/Library/Fonts/Impact.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
]


def get_system_font():
    for f in FONT_CANDIDATES:
        if Path(f).exists():
            return str(Path(f).as_posix()).replace(":", "\\:")
    return "Arial"


def generate_context_hook(transcript_text: str = "", topic: str = "GTA 6", speaker: str = None) -> str:
    """
    Analyzes spoken dialogue and clip metadata to generate a 1-line high-retention hook script.
    """
    text_lower = transcript_text.lower() if transcript_text else ""
    speaker_tag = speaker if speaker else "Player"

    # 1. Action & Hazard Recognition
    if any(k in text_lower for k in ["alligator", "crocodile", "swamp", "lake", "water"]):
        return f"{speaker_tag} almost eaten by a {topic} alligator 🐊😭"
    elif any(k in text_lower for k in ["police", "cop", "cops", "chase", "wanted", "siren"]):
        return f"{speaker_tag} vs 5-Star {topic} Police Chase 🚔💀"
    elif any(k in text_lower for k in ["crash", "car", "speed", "drift", "flip", "vehicle"]):
        return f"Insane High Speed {topic} Car Crash 🚗💥"
    elif any(k in text_lower for k in ["money", "bank", "robbery", "heist", "cash", "steal"]):
        return f"{speaker_tag} Pulled Off The Craziest {topic} Heist 💰😱"
    elif any(k in text_lower for k in ["graphics", "unreal", "real life", "visual", "look at that"]):
        return f"Are {topic} Graphics Even Real Life? 🤯🔥"
    elif any(k in text_lower for k in ["mission", "pass", "fail", "wasted", "busted", "died"]):
        return f"{speaker_tag} Failed The Most Impossible {topic} Mission 💀❌"
    elif any(k in text_lower for k in ["gun", "shoot", "sniper", "fight", "war", "battle"]):
        return f"Intense Showdown In The Streets Of {topic} 🎯⚡"
    elif any(k in text_lower for k in ["secret", "easter egg", "mystery", "hidden", "location"]):
        return f"{speaker_tag} Found A Secret {topic} Mystery Location 📍👀"
    elif any(k in text_lower for k in ["rage", "angry", "screaming", "no way", "omg", "shut up"]):
        return f"{speaker_tag} Lost His Mind Playing {topic} 😭🔥"

    # Default punchy hooks
    if speaker:
        return f"{speaker} Insane Reaction to {topic} 🎮🔥"
    return f"You Won't Believe What Happened In {topic} 😱🔥"


def apply_hook_banner(
    video_path: Path,
    output_path: Path,
    hook_text: str,
    y_pos: int = 180,
    font_size: int = 50,
    use_nvenc: bool = True
) -> bool:
    """
    Bakes the dynamic headline banner into the video using FFmpeg drawtext.
    Renders with a dark solid/semi-translucent pill-box and centered bold white typography.
    """
    video_path = Path(video_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not video_path.exists():
        print(f"❌ Input video not found: {video_path}")
        return False

    font_path = get_system_font()

    # Clean hook text for FFmpeg drawtext escaping
    # FFmpeg requires escaping of ' and :
    clean_text = hook_text.replace("'", "\\'").replace(":", "\\:")
    
    # Text line formatting: wrap if text is long (>42 chars)
    words = clean_text.split()
    lines = []
    current_line = []
    current_len = 0
    for w in words:
        if current_len + len(w) > 36 and current_line:
            lines.append(" ".join(current_line))
            current_line = [w]
            current_len = len(w)
        else:
            current_line.append(w)
            current_len += len(w) + 1
    if current_line:
        lines.append(" ".join(current_line))
    
    formatted_text = "\n".join(lines)

    # FFmpeg drawtext filter with solid black box and white bold font
    # box=1:boxcolor=black@0.88:boxborderw=20
    drawtext_filter = (
        f"drawtext=text='{formatted_text}':"
        f"fontfile='{font_path}':"
        f"fontsize={font_size}:"
        f"fontcolor=white:"
        f"box=1:boxcolor=black@0.90:boxborderw=24:"
        f"line_spacing=14:"
        f"x=(w-text_w)/2:y={y_pos}"
    )

    v_encoder = ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "20"] if use_nvenc else ["-c:v", "libx264", "-crf", "20", "-preset", "veryfast"]

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", drawtext_filter,
        *v_encoder,
        "-c:a", "copy",
        "-map_metadata", "-1",
        str(output_path)
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        return True
    else:
        # Fallback to CPU libx264 if NVENC fails
        if use_nvenc:
            return apply_hook_banner(video_path, output_path, hook_text, y_pos, font_size, use_nvenc=False)
        print(f"❌ Error applying banner: {res.stderr[-300:]}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dynamic_hook_engine.py <input_video> <output_video> [hook_text]")
        sys.exit(1)

    in_vid = sys.argv[1]
    out_vid = sys.argv[2]
    hook = sys.argv[3] if len(sys.argv) > 3 else "GTA 6 Gameplay Walkthrough 🔥"

    print(f"Applying Dynamic Hook Banner: \"{hook}\"")
    success = apply_hook_banner(in_vid, out_vid, hook)
    if success:
        print(f"✅ Success! Saved to: {out_vid}")
    else:
        print("❌ Failed to apply banner.")
