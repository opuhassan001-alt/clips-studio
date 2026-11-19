"""Direct runner script to generate a 9:16 vertical GTA 6 clip using Clips Studio engine."""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.models import ClipCandidate, Segment
from core.pipeline import _render_files
from main import load_config
import yaml

def main():
    print("=== Clips Studio GTA 6 Automated Clip Generator ===")
    config_path = Path("config/settings.yaml")
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Disable outro for quick test if desired, or keep it
    config["clips"]["outro"] = False
    config["clips"]["vertical"] = True

    source_video = Path("data/downloads/gta6_trailer.mp4")
    if not source_video.exists():
        print(f"Error: {source_video} does not exist!")
        return

    # Load segments from data/transcripts/gta6_trailer.json
    transcript_path = Path("data/transcripts/gta6_trailer.json")
    if transcript_path.exists():
        with open(transcript_path, encoding="utf-8") as f:
            raw_data = json.load(f)
            segments = [
                Segment(
                    start=s["start"],
                    end=s["end"],
                    text=s["text"],
                    words=s.get("words", [])
                )
                for s in raw_data.get("segments", [])
            ]
    else:
        from transcription.transcriber import transcribe
        segments = transcribe(source_video, "gta6_trailer", Path("data/transcripts"), model_size="base")

    print(f"Loaded {len(segments)} transcript segments.")

    # Select the iconic climax of the trailer (62.0s to 77.5s)
    # Lucia & Jason: "We're gonna get through this. It's by sticking together. Being a team. Trust. Trust."
    candidate = ClipCandidate(
        start=62.0,
        end=77.5,
        score=98,
        hook="GTA 6 - Lucia & Jason Climax: Trust",
        reason="Iconic relationship dialogue and action climax"
    )

    output_dir = Path("data/clips/RockstarGames/GTA_6_Clips")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Rendering clip: {candidate.start}s - {candidate.end}s ({candidate.duration:.1f}s)...")
    
    # Render options: custom caption style (bold yellow highlight), fit_blur / track
    render_opts = {
        "crop": "fit_blur", # Ensures beautiful 9:16 layout without cropping wide-screen cinematic shots
        "caption_style": {
            "font": "Impact",
            "font_size": 90,
            "color": "#FFFFFF",
            "highlight": True,
            "highlight_color": "#FFCC00",
            "uppercase": True,
            "position": "middle",
            "words_per_caption": 3
        }
    }

    final_path, opts_json = _render_files(
        source=source_video,
        candidate=candidate,
        segments=segments,
        clip_dir=output_dir,
        config=config,
        render_opts=render_opts,
        content_language="en"
    )

    print("\n[SUCCESS] Clip generated successfully!")
    print(f"Output File: {final_path}")
    print(f"File Size: {final_path.stat().st_size / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    main()
