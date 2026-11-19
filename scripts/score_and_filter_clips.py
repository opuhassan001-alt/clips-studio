"""Score and Partition Clips based on Excitement, Audio Dynamics, and Comedy Cadence.

Uses dynamic virality curve normalization:
- Clips scoring >= 80 are promoted to selected_viral_80_plus/
- Clips scoring < 80 are placed in review_under_80/ and logged in delete_candidates.txt.
"""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

def get_audio_stats(clip_path: Path) -> dict:
    cmd = [
        "ffmpeg", "-y", "-i", str(clip_path),
        "-af", "astats=metadata=1:reset=1",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    peaks = re.findall(r"Peak level dB:\s+([-\d.]+)", res.stderr)
    rmss = re.findall(r"RMS level dB:\s+([-\d.]+)", res.stderr)
    dyns = re.findall(r"Dynamic range:\s+([-\d.]+)", res.stderr)
    
    peak = float(peaks[-1]) if peaks else -50.0
    rms = float(rmss[-1]) if rmss else -50.0
    dyn = float(dyns[-1]) if dyns else 30.0
    crest = peak - rms
    
    return {
        "peak_db": peak,
        "rms_db": rms,
        "dynamic_range_db": dyn,
        "crest_factor_db": crest
    }

def get_transcript_metrics(clip_name: str, transcript_data: dict) -> dict:
    m = re.search(r"clip_(\d+)-(\d+)", clip_name)
    if not m:
        return {"words_per_sec": 2.5, "punct_count": 0, "text_sample": "", "duration": 20.0}
    
    start_s = float(m.group(1))
    end_s = float(m.group(2))
    duration = max(1.0, end_s - start_s)
    
    segments = transcript_data.get("segments", [])
    clip_text = []
    word_count = 0
    punct_count = 0
    
    for seg in segments:
        s = seg.get("start", 0)
        e = seg.get("end", 0)
        if s >= start_s - 1.0 and e <= end_s + 1.0:
            txt = seg.get("text", "")
            clip_text.append(txt)
            words = seg.get("words", [])
            word_count += len(words) if words else len(txt.split())
            punct_count += sum(txt.count(p) for p in ("!", "?", "...", ","))
    
    wps = word_count / duration
    full_text = " ".join(clip_text).strip()
    
    return {
        "duration": duration,
        "word_count": word_count,
        "words_per_sec": wps,
        "punct_count": punct_count,
        "text_sample": full_text[:90]
    }

def calculate_raw_score(astats: dict, tmetrics: dict) -> float:
    # 1. Audio Peak & Dynamic Spikes (0 - 45)
    peak = astats["peak_db"]
    if peak >= -8.0:
        peak_score = 25.0
    elif peak >= -15.0:
        peak_score = 20.0
    elif peak >= -25.0:
        peak_score = 14.0
    else:
        peak_score = 6.0
        
    crest = astats["crest_factor_db"]
    if crest >= 10.0:
        crest_score = 20.0
    elif crest >= 6.0:
        crest_score = 15.0
    elif crest >= 3.5:
        crest_score = 10.0
    else:
        crest_score = 5.0
    audio_score = peak_score + crest_score
    
    # 2. Speech Pacing & Cadence (0 - 35)
    wps = tmetrics["words_per_sec"]
    if 2.0 <= wps <= 4.2:
        pacing_score = 20.0
    elif 1.3 <= wps < 2.0:
        pacing_score = 14.0
    else:
        pacing_score = 7.0
        
    punct_score = min(15.0, tmetrics["punct_count"] * 3.0)
    speech_score = pacing_score + punct_score
    
    # 3. Viral Keywords & Hype Bonus (0 - 15)
    text_lower = tmetrics.get("text_sample", "").lower()
    hype_keywords = ["crazy", "let's go", "bhai", "maro", "money", "jason", "damn", "fucking", "car", "haha", "omg", "look", "wait"]
    keyword_hits = sum(1 for kw in hype_keywords if kw in text_lower)
    hype_score = min(15.0, keyword_hits * 5.0)
    
    # 4. Duration Sweet Spot (0 - 15)
    dur = tmetrics["duration"]
    if 15.0 <= dur <= 35.0:
        dur_score = 15.0
    elif 12.0 <= dur < 15.0 or 35.0 < dur <= 50.0:
        dur_score = 11.0
    else:
        dur_score = 6.0
        
    return audio_score + speech_score + hype_score + dur_score

def run_scoring(clips_dir: Path, transcript_path: Path):
    if not clips_dir.exists():
        print(f"Directory {clips_dir} not found.")
        return
        
    transcript_data = {}
    if transcript_path.exists():
        with open(transcript_path, encoding="utf-8") as f:
            transcript_data = json.load(f)
            
    viral_dir = clips_dir / "selected_viral_80_plus"
    review_dir = clips_dir / "review_under_80"
    viral_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all mp4 clips wherever they currently sit
    mp4_files = sorted(clips_dir.glob("clip_*.mp4"))
    mp4_files += sorted(viral_dir.glob("clip_*.mp4"))
    mp4_files += sorted(review_dir.glob("clip_*.mp4"))
    # Deduplicate by name
    seen = {}
    for p in mp4_files:
        if p.name not in seen:
            seen[p.name] = p
    mp4_files = list(seen.values())
    
    print(f"Analyzing and scoring {len(mp4_files)} clips...")
    
    raw_results = []
    for clip in mp4_files:
        astats = get_audio_stats(clip)
        tmetrics = get_transcript_metrics(clip.name, transcript_data)
        raw = calculate_raw_score(astats, tmetrics)
        raw_results.append({
            "path": clip,
            "name": clip.name,
            "raw_score": raw,
            "duration": tmetrics["duration"],
            "hook": tmetrics["text_sample"],
            "peak_db": astats["peak_db"],
            "words_per_sec": round(tmetrics["words_per_sec"], 2)
        })
        
    raw_scores = [r["raw_score"] for r in raw_results]
    min_raw = min(raw_scores) if raw_scores else 0
    max_raw = max(raw_scores) if raw_scores else 100
    spread = max(1.0, max_raw - min_raw)
    
    high_score_clips = []
    delete_candidates = []
    
    for r in raw_results:
        # Standardized 0-100 virality distribution curve
        norm_score = round(55.0 + ((r["raw_score"] - min_raw) / spread) * 42.0, 1)
        r["score"] = norm_score
        
        if norm_score >= 80.0:
            target_path = viral_dir / r["name"]
            high_score_clips.append(r)
        else:
            target_path = review_dir / r["name"]
            delete_candidates.append(r)
            
        if r["path"].resolve() != target_path.resolve():
            shutil.move(str(r["path"]), str(target_path))
            r["path"] = target_path
            
    # Sort
    high_score_clips.sort(key=lambda x: x["score"], reverse=True)
    delete_candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # Save ledger JSON
    ledger_json = clips_dir / "delete_candidates.json"
    with open(ledger_json, "w", encoding="utf-8") as f:
        json.dump({
            "total_clips": len(raw_results),
            "high_score_count": len(high_score_clips),
            "delete_candidate_count": len(delete_candidates),
            "high_score_clips": [{k: v for k, v in c.items() if k != "path"} for c in high_score_clips],
            "delete_candidates": [{k: v for k, v in c.items() if k != "path"} for c in delete_candidates]
        }, f, indent=2, ensure_ascii=False)
        
    # Save human-readable text ledger
    ledger_txt = clips_dir / "delete_candidates.txt"
    with open(ledger_txt, "w", encoding="utf-8") as f:
        f.write("="*70 + "\n")
        f.write("CLIPS WITH SCORE UNDER 80 (CANDIDATES TO REVIEW & DELETE)\n")
        f.write(f"Total Under-80 Clips: {len(delete_candidates)}\n")
        f.write(f"Folder: {review_dir.resolve()}\n")
        f.write("="*70 + "\n\n")
        for idx, c in enumerate(delete_candidates, 1):
            f.write(f"[{idx:02d}] {c['name']} | Score: {c['score']}/100 | Dur: {c['duration']:.1f}s | Peak: {c['peak_db']:.1f}dB\n")
            f.write(f"     Hook: \"{c['hook']}\"\n\n")
            
        f.write("\n" + "="*70 + "\n")
        f.write("HOW TO DELETE ALL UNDER-80 CLIPS WHEN YOU DECIDE:\n")
        f.write("In PowerShell, run this command:\n")
        f.write("Remove-Item -Recurse -Force 'data\\clips\\carry_action_15m\\review_under_80\\*'\n")
        f.write("="*70 + "\n")
        
    print(f"\nProcessing Complete!")
    print(f"⭐ High Score (>=80): {len(high_score_clips)} clips in {viral_dir.name}/")
    for h in high_score_clips:
        print(f"   - {h['name']} | Score: {h['score']} | {h['duration']:.1f}s | {h['hook'][:40]}")
    print(f"\n⚠️ Under-80 Clips: {len(delete_candidates)} clips in {review_dir.name}/")
    print(f"📋 Delete candidate record: {ledger_txt}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        target_dir = Path(sys.argv[1])
        transcript_file = Path(sys.argv[2])
    else:
        target_dir = Path("data/clips/carry_action_15m")
        transcript_file = Path("data/transcripts/carry_action_15m.json")
        
    run_scoring(target_dir, transcript_file)
