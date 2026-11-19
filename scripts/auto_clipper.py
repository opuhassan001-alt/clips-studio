"""Automated Multi-Clip Generator for Clips Studio.

Takes any video (YouTube URL or local file), extracts all notable moments,
and renders 9:16 vertical shorts where NOTHING is cut off (using fit_blur or smart tracking).
"""

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.binaries import ffmpeg, ffprobe
from core.models import ClipCandidate, Segment
from core.pipeline import _render_files
from main import load_config
import yaml

def get_video_duration(video_path: Path) -> float:
    cmd = [
        ffprobe(), "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def download_video(url: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_template = str(output_dir / "%(id)s.%(ext)s")
    cmd = [
        sys.executable.replace("python.exe", "yt-dlp.exe"),
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--no-playlist",
        url,
        "-o", out_template
    ]
    print(f"Downloading video from {url}...")
    subprocess.run(cmd, check=True)
    # Find downloaded file
    files = sorted(output_dir.glob("*.*"), key=lambda f: f.stat().st_mtime, reverse=True)
    for f in files:
        if f.suffix in (".mp4", ".mkv", ".webm"):
            return f
    raise RuntimeError("Downloaded video file not found!")

def _ends_sentence(text: str) -> bool:
    """Check if dialogue line marks the completion of a full thought or joke."""
    t = text.strip()
    return bool(t) and t[-1] in (".", "!", "?", "…") or t.endswith("...")

def discover_candidates(segments: list[Segment], total_duration: float, min_dur: float = 12.0, max_dur: float = 58.0) -> list[ClipCandidate]:
    """Finds complete, self-contained thought/joke moments without cutting mid-dialogue."""
    candidates = []
    
    if segments:
        i = 0
        while i < len(segments):
            start_seg = segments[i]
            cur_start = start_seg.start
            cur_text = [start_seg.text]
            
            j = i
            while j < len(segments):
                seg = segments[j]
                current_len = seg.end - cur_start
                has_next = (j + 1 < len(segments))
                pause_after = (segments[j+1].start - seg.end) if has_next else 999.0
                
                # Check if this segment completes a sentence/thought
                sentence_finished = _ends_sentence(seg.text) or (pause_after > 1.6)
                
                # We want a self-contained joke or scene (at least min_dur, but under max_dur)
                if current_len >= min_dur and sentence_finished:
                    hook_title = " ".join(cur_text).strip()[:65]
                    candidates.append(ClipCandidate(
                        start=max(0.0, cur_start - 0.2),
                        end=min(total_duration, seg.end + 0.6), # Small tail pad so punchline audio never cuts out
                        score=92,
                        hook=hook_title,
                        reason="Complete self-contained thought/scene"
                    ))
                    i = j + 1
                    break
                elif current_len >= max_dur:
                    # Look backwards for the last finished sentence to avoid chopping mid-word
                    hook_title = " ".join(cur_text).strip()[:65]
                    candidates.append(ClipCandidate(
                        start=max(0.0, cur_start - 0.2),
                        end=min(total_duration, seg.end + 0.4),
                        score=85,
                        hook=hook_title,
                        reason="Maximum duration boundary"
                    ))
                    i = j + 1
                    break
                else:
                    j += 1
                    if j < len(segments):
                        cur_text.append(segments[j].text)
            else:
                # Reached end of segments
                if (segments[-1].end - cur_start) >= min_dur:
                    candidates.append(ClipCandidate(
                        start=max(0.0, cur_start - 0.2),
                        end=min(total_duration, segments[-1].end + 0.5),
                        score=85,
                        hook=" ".join(cur_text).strip()[:65],
                        reason="Final segment boundary"
                    ))
                break
    else:
        # Visual-based highlight chunks (for pure gameplay/action with no talking)
        chunk_size = 28.0
        n_chunks = max(1, math.ceil(total_duration / chunk_size))
        for idx in range(n_chunks):
            start = idx * chunk_size
            end = min(total_duration, start + chunk_size)
            if end - start >= min_dur:
                candidates.append(ClipCandidate(
                    start=start,
                    end=end,
                    score=85,
                    hook=f"Action Moment #{idx + 1}",
                    reason="Visual action interval"
                ))
                
    return candidates

def process_video_into_clips(input_source: str, crop_mode: str = "fit_blur"):
    config_path = Path("config/settings.yaml")
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["clips"]["outro"] = False
    config["clips"]["vertical"] = True

    # 1. Resolve Video Path
    if input_source.startswith("http://") or input_source.startswith("https://"):
        video_path = download_video(input_source, Path("data/downloads"))
    else:
        video_path = Path(input_source)
        if not video_path.exists():
            print(f"Error: Local file '{video_path}' does not exist!")
            sys.exit(1)

    print(f"\n[1/3] Source Video Ready: {video_path}")
    duration = get_video_duration(video_path)
    print(f"      Total Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")

    # 2. Transcription
    print("\n[2/3] Transcribing Speech with Faster-Whisper...")
    from transcription.transcriber import transcribe
    segments = transcribe(
        video_path,
        video_path.stem,
        Path("data/transcripts"),
        model_size="base"
    )
    print(f"      Extracted {len(segments)} spoken dialogue segments.")

    # 3. Candidate Moments Discovery
    candidates = discover_candidates(segments, duration)
    print(f"\n[3/3] Discovered {len(candidates)} potential clip moments:")
    for idx, c in enumerate(candidates, 1):
        print(f"      Clip {idx:02d}: {c.start:05.1f}s - {c.end:05.1f}s ({c.duration:.1f}s) -> \"{c.hook}\"")

    # 4. Rendering all clips
    clip_output_dir = Path("data/clips") / video_path.stem
    clip_output_dir.mkdir(parents=True, exist_ok=True)
    
    render_opts = {
        "crop": crop_mode,  # "fit_blur" ensures ZERO video content is cut off!
        "caption_style": {
            "font": "Impact",
            "font_size": 84,
            "color": "#FFFFFF",
            "highlight": True,
            "highlight_color": "#FFCC00",
            "uppercase": True,
            "position": "bottom",
            "words_per_caption": 3
        }
    }

    print(f"\n=== Rendering All {len(candidates)} Clips (Mode: {crop_mode}) ===")
    rendered_files = []
    for idx, candidate in enumerate(candidates, 1):
        stem = f"clip_{int(candidate.start):05d}-{int(candidate.end):05d}"
        expected_path = clip_output_dir / f"{stem}.mp4"
        if expected_path.exists() and expected_path.stat().st_size > 200000:
            print(f"-> Clip {idx}/{len(candidates)} already rendered: {expected_path.name}")
            rendered_files.append(expected_path)
            continue

        print(f"\n-> Rendering Clip {idx}/{len(candidates)} ({candidate.start:.1f}s - {candidate.end:.1f}s)...")
        try:
            final_path, _ = _render_files(
                source=video_path,
                candidate=candidate,
                segments=segments,
                clip_dir=clip_output_dir,
                config=config,
                render_opts=render_opts,
                content_language="en"
            )
            rendered_files.append(final_path)
            print(f"   [Done] Saved to: {final_path}")
        except Exception as e:
            print(f"   [Warning] Skipped clip {idx} due to error: {e}")

    print("\n" + "="*50)
    print(f"SUCCESS! {len(rendered_files)} vertical clips generated in:")
    print(f"{clip_output_dir.resolve()}")
    print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto multi-clip generator")
    parser.add_argument("source", help="YouTube URL or local video file path")
    parser.add_argument("--crop", default="fit_blur", choices=["fit_blur", "track", "center"],
                        help="Crop mode: fit_blur (default, nothing cut off), track (YOLO face follow), center")
    args = parser.parse_args()

    process_video_into_clips(args.source, crop_mode=args.crop)
