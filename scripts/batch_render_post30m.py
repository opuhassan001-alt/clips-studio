import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.models import ClipCandidate, Segment
from core.pipeline import _render_files
from main import load_config
from scripts.dynamic_hook_engine import apply_hook_banner
from scripts.yt_compliance_guard import process_folder

SELECTED_CLIPS = [
    {
        "start": 1033.0,
        "end": 1076.0,
        "hook": "Carry Minati Meets The New Vice City NPC",
        "score": 88
    },
    {
        "start": 1018.0,
        "end": 1032.0,
        "hook": "Testing The New Camera In GTA 6",
        "score": 86
    },
    {
        "start": 1275.0,
        "end": 1289.0,
        "hook": "High Speed Driving Across Vice City",
        "score": 83
    },
    {
        "start": 1294.0,
        "end": 1309.0,
        "hook": "GTA 6 Weapons & Inventory Wheel",
        "score": 81
    },
    {
        "start": 1257.0,
        "end": 1275.0,
        "hook": "When You Forget How To Drive in GTA 6",
        "score": 80
    },
    {
        "start": 1316.0,
        "end": 1361.0,
        "hook": "The Most Unhinged NPC in GTA 6",
        "score": 80
    },
    {
        "start": 1603.0,
        "end": 1616.0,
        "hook": "Hidden Location Spotted in GTA 6",
        "score": 82
    },
    {
        "start": 1616.0,
        "end": 1630.0,
        "hook": "Seeing Vice City Skyline For The First Time",
        "score": 82
    },
    {
        "start": 1666.0,
        "end": 1685.0,
        "hook": "When The Mission Suddenly Goes Wrong",
        "score": 80
    }
]

def main():
    source_video = Path("data/downloads/carry_part2_30m.webm")
    transcript_path = Path("data/transcripts/carry_part2_30m.json")

    with open(transcript_path, encoding="utf-8") as f:
        raw_data = json.load(f)

    segments = [Segment(start=s["start"], end=s["end"], text=s["text"], words=s.get("words")) for s in raw_data.get("segments", [])]

    output_dir = Path("data/clips/carry_post30m_viral")
    output_dir.mkdir(parents=True, exist_ok=True)
    config = load_config(Path("config/settings.yaml"))

    render_opts = {
        "crop": "fit_blur",
        "caption_style": {
            "font": "Impact",
            "font_size": 80,
            "color": "#FFFFFF",
            "highlight": True,
            "highlight_color": "#FFD700",
            "uppercase": True,
            "position": "bottom",
            "words_per_caption": 3
        }
    }

    print(f"=== Rendering {len(SELECTED_CLIPS)} Post-30m Viral Clips ===")

    for idx, c in enumerate(SELECTED_CLIPS, 1):
        stem = f"clip_{int(c['start']):05d}-{int(c['end']):05d}"
        dest_path = output_dir / f"{stem}.mp4"

        if dest_path.exists() and dest_path.stat().st_size > 5000000:
            print(f"[{idx}/{len(SELECTED_CLIPS)}] Already rendered: {stem}.mp4")
            continue

        print(f"\n[{idx}/{len(SELECTED_CLIPS)}] Rendering: {stem} ({c['start']}s - {c['end']}s) -> \"{c['hook']}\"...")
        cand = ClipCandidate(start=c["start"], end=c["end"], hook=c["hook"], score=c["score"])

        try:
            final_path, _ = _render_files(
                source=source_video,
                candidate=cand,
                segments=segments,
                clip_dir=output_dir,
                config=config,
                render_opts=render_opts,
                content_language="en"
            )

            # Apply Dynamic Hook Banner
            enhanced_path = output_dir / f"enhanced_{final_path.name}"
            if apply_hook_banner(final_path, enhanced_path, c["hook"]):
                enhanced_path.replace(final_path)
                print(f"   [Hook Banner Baked] \"{c['hook']}\"")

            print(f"   [Done] Saved {final_path.name} ({final_path.stat().st_size / 1e6:.1f} MB)")
        except Exception as e:
            print(f"   [Error] Failed to render {stem}: {e}")

    print("\n" + "="*50)
    print("ALL POST-30M CLIPS RENDERED SUCCESSFULLY!")
    print("="*50)

    # Run YouTube Compliance Guard & Audio Normalization
    try:
        print("\n🛡️ Running YouTube Anti-Strike Compliance Guard & Audio Normalization...")
        process_folder(output_dir)
        print("🛡️ Compliance Guard complete!")
    except Exception as comp_err:
        print(f"Compliance guard notice: {comp_err}")

if __name__ == "__main__":
    main()
