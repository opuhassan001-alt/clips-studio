import re
import json

def parse_vtt_time(t_str):
    parts = t_str.strip().split(':')
    if len(parts) == 3:
        h, m, s = parts
        return float(h)*3600 + float(m)*60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return float(m)*60 + float(s)
    return 0.0

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

cues = []
current_start = None
current_end = None
current_text = []

with open('data/speed_stream.en.vtt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        m = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})', line)
        if m:
            if current_start is not None and current_text:
                text = ' '.join(current_text)
                text = re.sub(r'<[^>]+>', '', text)
                cues.append({'start': current_start, 'end': current_end, 'text': text})
            current_start = parse_vtt_time(m.group(1))
            current_end = parse_vtt_time(m.group(2))
            current_text = []
        elif line and not line.startswith('WEBVTT') and not line.startswith('NOTE') and not line.isdigit():
            current_text.append(line)

if current_start is not None and current_text:
    text = ' '.join(current_text)
    text = re.sub(r'<[^>]+>', '', text)
    cues.append({'start': current_start, 'end': current_end, 'text': text})

print(f"Total parsed cues: {len(cues)}")

target_keywords = [
    'lucia', 'jason', 'vice city', 'police', 'run', 'gun', 'car', 'shoot', 
    'heist', 'omg', 'bro', 'no way', 'crazy', 'shut up', 'damn', 'what', 'stop', 'help'
]

window_sec = 50.0
step_sec = 20.0
t = 0.0
max_t = cues[-1]['end'] if cues else 0.0

scored_windows = []

# Map cues to quick search
while t < max_t:
    win_end = t + window_sec
    win_text = []
    for c in cues:
        if c['end'] >= t and c['start'] <= win_end:
            win_text.append(c['text'])
        elif c['start'] > win_end:
            break
    combined = ' '.join(win_text)
    words = combined.split()
    if len(words) >= 25:
        score = 0
        for kw in target_keywords:
            score += len(re.findall(r'\b' + kw + r'\b', combined, re.IGNORECASE)) * 2
        score += combined.count('!') * 1.5
        score += combined.count('?') * 1.0
        score += sum(1 for w in words if w.isupper() and len(w) > 2) * 1.5
        if score > 15:
            scored_windows.append({
                'start': t,
                'end': win_end,
                'score': score,
                'text': combined
            })
    t += step_sec

scored_windows.sort(key=lambda x: x['score'], reverse=True)
selected = []
min_dist = 900.0 # 15 minutes apart! Ensures completely different hours and storylines!

for sw in scored_windows:
    if len(selected) >= 10:
        break
    overlap = False
    for s in selected:
        if abs(sw['start'] - s['start']) < min_dist:
            overlap = True
            break
    if not overlap:
        selected.append(sw)

selected.sort(key=lambda x: x['start'])
print(f"\nTop {len(selected)} Selected Distinct Viral Moments (>= 15 mins apart):")
for i, s in enumerate(selected, 1):
    st_str = format_time(s['start'])
    en_str = format_time(s['end'])
    print(f"[{i}] {st_str} - {en_str} (Score: {s['score']:.1f})")
    print(f"    Excerpt: {s['text'][:140]}...")

with open('data/candidate_moments.json', 'w', encoding='utf-8') as f:
    json.dump(selected, f, indent=2)
