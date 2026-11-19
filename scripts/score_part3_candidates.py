import json
import re
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.score_and_filter_clips import calculate_raw_score, detect_emotional_and_crying
from scripts.auto_clipper import discover_candidates
from core.models import Segment

def main():
    transcript_file = Path('data/transcripts/carry_post30m_part3.json')
    with open(transcript_file, 'r', encoding='utf-8') as f:
        tdata = json.load(f)

    raw_segments = tdata.get('segments', [])
    segments = [Segment(start=s['start'], end=s['end'], text=s['text'], words=s.get('words')) for s in raw_segments]
    candidates = discover_candidates(segments, 1800.0)
    source_video = Path('data/downloads/carry_post30m_part3.mp4')

    scored_candidates = []
    print(f"Evaluating and scoring {len(candidates)} candidates...")

    for idx, c in enumerate(candidates):
        dur = c.duration
        clip_text = []
        word_count = 0
        punct_count = 0
        for seg in segments:
            s = seg.start
            e = seg.end
            if s >= c.start - 0.5 and e <= c.end + 0.5:
                txt = seg.text or ''
                clip_text.append(txt)
                words = seg.words or []
                word_count += len(words) if words else len(txt.split())
                punct_count += sum(txt.count(p) for p in ('!', '?', '...', ','))
                
        wps = word_count / max(1.0, dur)
        full_text = ' '.join(clip_text).strip()
        tmetrics = {
            'duration': dur,
            'word_count': word_count,
            'words_per_sec': wps,
            'punct_count': punct_count,
            'text_sample': full_text
        }
        
        cmd = [
            'ffmpeg', '-y', '-ss', str(c.start), '-t', str(dur),
            '-i', str(source_video),
            '-af', 'astats=metadata=1:reset=1',
            '-f', 'null', '-'
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        peaks = re.findall(r'Peak level dB:\s+([-\d.]+)', res.stderr)
        rmss = re.findall(r'RMS level dB:\s+([-\d.]+)', res.stderr)
        dyns = re.findall(r'Dynamic range:\s+([-\d.]+)', res.stderr)
        
        peak = float(peaks[-1]) if peaks else -20.0
        rms = float(rmss[-1]) if rmss else -25.0
        dyn = float(dyns[-1]) if dyns else 20.0
        crest = peak - rms
        
        astats = {
            'peak_db': peak,
            'rms_db': rms,
            'dynamic_range_db': dyn,
            'crest_factor_db': crest
        }
        
        emo_data = detect_emotional_and_crying(clip_path=None, tmetrics=tmetrics, astats=astats)
        score = calculate_raw_score(astats, tmetrics, emo_data)
        scored_candidates.append({
            'index': idx + 1,
            'start': c.start,
            'end': c.end,
            'duration': dur,
            'score': score,
            'text': full_text[:120],
            'astats': astats,
            'is_emotional': emo_data['is_emotional'],
            'is_crying': emo_data['is_crying'],
            'emotional_score': emo_data['emotional_score'],
            'emotional_tags': emo_data['tags']
        })

    scored_candidates.sort(key=lambda x: x['score'], reverse=True)

    viral_80_plus = [c for c in scored_candidates if c['score'] >= 80]
    print(f"\n=== TOP SCORING CANDIDATES (>= 80) ===")
    print(f"Total candidates with Score >= 80: {len(viral_80_plus)}")

    for c in viral_80_plus:
        stream_start_m = int((c['start'] + 1800) // 60)
        stream_start_s = int((c['start'] + 1800) % 60)
        stream_end_m = int((c['end'] + 1800) // 60)
        stream_end_s = int((c['end'] + 1800) % 60)
        tag_str = f" [🔥 EMO: {','.join(c['emotional_tags'])}]" if c.get('is_emotional') else ""
        print(f"Score {c['score']:.1f} | Stream Time: {stream_start_m:02d}:{stream_start_s:02d} - {stream_end_m:02d}:{stream_end_s:02d} ({c['duration']:.1f}s){tag_str} | '{c['text'][:70]}...'")

    with open('data/carry_part3_scored.json', 'w', encoding='utf-8') as f:
        json.dump(scored_candidates, f, indent=2)

if __name__ == '__main__':
    main()
