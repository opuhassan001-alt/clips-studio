"""
Dynamic Kinetic Karaoke Subtitle Engine (.ASS).
Module 5 of Universal Master Spec 3.0.
"""

from pathlib import Path
from typing import List, Dict, Any


def format_ass_timestamp(seconds: float) -> str:
    """Converts seconds float to ASS timestamp format: H:MM:SS.cs"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def generate_viral_ass_subtitles(
    aligned_segments: List[Dict[str, Any]],
    ass_output_path: str,
    font_name: str = "TheBoldFont",
    font_size: int = 85,
    highlight_color: str = "&H0000FFFF",  # Yellow in BGR hex: &H00BBGGRR (Yellow = 0x00FFFF)
    base_color: str = "&H00FFFFFF",       # White
    scale_pop_pct: int = 115,             # 115% scale pop
    margin_v: int = 280                   # Safe central oval baseline
) -> Path:
    """
    Generates word-by-word kinetic .ASS subtitles where each active spoken word
    pops up in scale and glows in dynamic highlight color.
    """
    output_path = Path(ass_output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Alignment, MarginL, MarginR, MarginV
Style: ViralPop,{font_name},{font_size},{base_color},{highlight_color},&H00000000,&H80000000,-1,2,100,100,{margin_v}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    dialogues = []

    for seg in aligned_segments:
        # Check if segment has word-level timestamps (Faster-Whisper / WhisperX alignment)
        words = seg.get("words", [])
        if not words:
            # Fallback to segment-level caption
            s_start = seg.get("start", 0.0)
            s_end = seg.get("end", s_start + 2.0)
            text = seg.get("text", "").strip().upper()
            if text:
                line = f"Dialogue: 0,{format_ass_timestamp(s_start)},{format_ass_timestamp(s_end)},ViralPop,,0,0,0,,{text}"
                dialogues.append(line)
            continue

        for w in words:
            if "start" not in w or "end" not in w:
                continue
            start_str = format_ass_timestamp(w["start"])
            end_str = format_ass_timestamp(w["end"])
            word_str = w["word"].strip().upper()
            if not word_str:
                continue

            # Kinetic scale pop + glow highlight effect
            line = (
                f"Dialogue: 0,{start_str},{end_str},ViralPop,,0,0,0,,"
                f"{{\\c{highlight_color}\\fscx{scale_pop_pct}\\fscy{scale_pop_pct}}}{word_str}"
            )
            dialogues.append(line)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(dialogues))

    return output_path
