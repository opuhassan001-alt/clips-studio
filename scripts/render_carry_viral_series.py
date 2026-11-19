import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.binaries import ffmpeg
from core.models import ClipCandidate, Segment
from core.pipeline import _render_files
from main import load_config
from scripts.dynamic_hook_engine import apply_hook_banner
from scripts.yt_compliance_guard import process_folder

HOOK_MAP = {
    # start_sec: hook_text (Natural, context-accurate, no forced fake humor)
    3394: "Carry Shocked By GTA 6 Rain Graphics 🌧️",        # 56:34 (Score 90.0)
    2949: "Carry Refuses To Shoot & Panics 💀",              # 49:09 (Score 89.0)
    2064: "New GTA 6 Camera Angles In Vice City 🎥",        # 34:24 (Score 88.0)
    2683: "Carry Is Literally Terrified In This Mission 😱",  # 44:43 (Score 87.0)
    1886: "Old GTA Characters Found in Vice City? 📍",       # 31:26 (Score 86.0)
    2160: "Craziest NPC Encounter In Vice City 😂",          # 36:00 (Score 85.0)
    2318: "Exploring The New Hideout in GTA 6 🏢",           # 38:38 (Score 85.0)
    2981: "When You Get Completely Lost In GTA 6 🤦‍♂️",         # 49:41 (Score 84.0)
}

def main():
    source_video = Path("data/downloads/carry_post30m_part3.mp4")
    if not source_video.exists():
        print(f"Source video not found: {source_video}")
        return

    scored_file = Path("data/carry_part3_scored.json")
    with open(scored_file, "r", encoding="utf-8") as f:
        scored_candidates = json.load(f)

    transcript_file = Path("data/transcripts/carry_post30m_part3.json")
    with open(transcript_file, "r", encoding="utf-8") as f:
        tdata = json.load(f)

    raw_segments = tdata.get("segments", [])
    segments = [Segment(start=s["start"], end=s["end"], text=s["text"], words=s.get("words")) for s in raw_segments]

    # Select top-tier candidates with score >= 84 (Peak Quality Viral Set)
    selected = [c for c in scored_candidates if c["score"] >= 84.0]
    print(f"=== Batch Rendering Top {len(selected)} Viral Clips (Score >= 84) ===")

    output_dir = Path("data/clips/carry_post30m_viral")
    output_dir.mkdir(parents=True, exist_ok=True)

    config = load_config(Path("config/settings.yaml"))

    render_opts = {
        "crop": "fit_blur",  # Ensures 100% of the stream, facecam & gameplay are in frame without cropping off edges
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

    rendered_clips = []

    for idx, c in enumerate(selected, 1):
        c_obj = ClipCandidate(
            start=c["start"],
            end=c["end"],
            hook=c["text"][:60],
            score=int(c["score"])
        )
        stem = f"clip_{int(c['start']):05d}-{int(c['end']):05d}"
        dest_path = output_dir / f"{stem}.mp4"

        print(f"\n[{idx}/{len(selected)}] Rendering Clip: {stem} (Score: {c['score']:.1f}, Dur: {c['duration']:.1f}s)...")

        # Determine exact context-accurate hook
        # Map closest start time to HOOK_MAP
        hook_text = None
        for k_start, h_val in HOOK_MAP.items():
            if abs((c["start"] + 1800) - k_start) < 15:
                hook_text = h_val
                break

        if not hook_text:
            txt_sample = c["text"]
            if "rain" in txt_sample.lower():
                hook_text = "GTA 6 Next-Gen Weather Graphics 🌧️"
            elif "shoot" in txt_sample.lower() or "scared" in txt_sample.lower():
                hook_text = "Intense Mission Combat In GTA 6 💥"
            elif "camera" in txt_sample.lower():
                hook_text = "GTA 6 Vice City Camera Features 🎥"
            else:
                hook_text = "CarryMinati Plays GTA 6 Vice City 🎮"

        try:
            final_path, _ = _render_files(
                source=source_video,
                candidate=c_obj,
                segments=segments,
                clip_dir=output_dir,
                config=config,
                render_opts=render_opts,
                content_language="en"
            )

            # Apply Dynamic Hook Headline Banner
            enhanced_path = output_dir / f"enhanced_{final_path.name}"
            if apply_hook_banner(final_path, enhanced_path, hook_text):
                enhanced_path.replace(final_path)
                print(f"   [Hook Banner Baked] \"{hook_text}\"")

            rendered_clips.append({
                "path": final_path,
                "score": c["score"],
                "hook": hook_text,
                "stream_time": f"{int((c['start']+1800)//60):02d}:{int((c['start']+1800)%60):02d}",
                "duration": c["duration"]
            })
            print(f"   [Done] Successfully saved: {final_path.name}")
        except Exception as e:
            print(f"   [Error] Rendering failed for {stem}: {e}")

    print("\n" + "="*60)
    print(f"RENDER COMPLETE! {len(rendered_clips)} clips ready in {output_dir}")
    print("="*60)

    # Post-process with yt_compliance_guard
    try:
        print("\n🛡️ Running YouTube Anti-Strike Compliance Guard & Audio Normalization...")
        process_folder(output_dir)
        print("🛡️ Compliance Guard check completed successfully!")
    except Exception as comp_err:
        print(f"Compliance guard notice: {comp_err}")

if __name__ == "__main__":
    main()
