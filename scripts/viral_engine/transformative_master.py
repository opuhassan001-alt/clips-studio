"""
TikTok CRP Transformative Obfuscation & Broadcast Audio Mastering.
Modules 6 & 7 of Universal Master Spec 3.0.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional


def build_transformative_command(
    input_video: str,
    output_video: str,
    ass_subtitle_path: Optional[str] = None,
    scale_factor: float = 1.02,
    tempo_factor: float = 1.01,
    target_lufs: float = -14.0,
    ffmpeg_bin: str = "ffmpeg"
) -> list:
    """
    Constructs the FFmpeg command applying the Transformative Filter Chain:
    - Scale 1.02x crop to neutralize video border/hash fingerprint
    - Unsharp mask to disrupt high-frequency pixel distribution
    - Contrast +5% & Saturation +10% boost
    - Audio atempo 1.01x pitch-neutral warp
    - EBU R128 loudness normalization (-14 LUFS, true peak -1.0 dBFS)
    - Optional burned-in .ASS subtitles
    """
    inv = Path(input_video).resolve()
    outv = Path(output_video).resolve()

    # Base video filter chain
    v_filters = [
        f"scale={scale_factor}*iw:-1",
        f"crop=iw/{scale_factor}:ih/{scale_factor}",
        "unsharp=5:5:0.8:5:5:0.0",
        "eq=contrast=1.05:saturation=1.1"
    ]

    if ass_subtitle_path:
        ass_clean = str(Path(ass_subtitle_path).resolve().as_posix()).replace(":", "\\:")
        v_filters.append(f"ass={ass_clean}")

    video_filter_str = ",".join(v_filters)
    audio_filter_str = f"atempo={tempo_factor},loudnorm=I={target_lufs}:LRA=7:tp=-1.0"

    cmd = [
        ffmpeg_bin, "-y",
        "-i", str(inv),
        "-filter_complex", f"[0:v]{video_filter_str}[v_out];[0:a]{audio_filter_str}[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        str(outv)
    ]
    return cmd


def master_and_transform_clip(
    input_video: str,
    output_video: str,
    ass_subtitle_path: Optional[str] = None,
    ffmpeg_bin: str = "ffmpeg"
) -> bool:
    """Executes the transformative filter command."""
    cmd = build_transformative_command(
        input_video,
        output_video,
        ass_subtitle_path=ass_subtitle_path,
        ffmpeg_bin=ffmpeg_bin
    )
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"⚠️ FFmpeg Transform Error: {res.stderr[-300:]}")
        return False
    return Path(output_video).exists() and Path(output_video).stat().st_size > 0
