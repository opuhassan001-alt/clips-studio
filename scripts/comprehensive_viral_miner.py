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

# Load and parse cues
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

# Fast sliding window indexing (2-pointer)
window_sec = 48.0
step_sec = 15.0

viral_keywords = {
    # Absurd vehicle / chase
    'chase': ['police', 'cops', 'siren', 'pursuit', 'car', 'fast', 'drive', 'speed', 'jump', 'crash', 'flip', 'scooter', 'bike', 'helicopter'],
    # Combat / NPC fight
    'combat': ['punch', 'fight', 'hit', 'beat', 'knock', 'gun', 'shoot', 'shotgun', 'sniper', 'kill', 'dead', 'wasted', 'bitch'],
    # Speed high arousal / scream
    'arousal': ['no', 'hell no', 'stop', 'help', 'omg', 'god damn', 'holy', 'what the', 'crazy', 'bro', 'shut up', 'bitch', 'run', 'get out'],
    # Lucia / Jason / Storyline
    'story': ['lucia', 'jason', 'mission', 'vice city', 'loyal', 'money', 'heist', 'bank', 'store', 'robbery'],
    # Slapstick / Absurdity
    'absurd': ['alligator', 'dog', 'chop', 'train', 'beach', 'club', 'dance', 'fall', 'drown', 'water', 'boat', 'yacht', 'explode', 'gas']
}

windows = []
t = 0.0
max_t = cues[-1]['end'] if cues else 0.0
cue_i = 0
num_cues = len(cues)

while t < max_t:
    win_end = t + window_sec
    while cue_i < num_cues and cues[cue_i]['end'] < t:
        cue_i += 1
    
    # collect cues in [t, win_end]
    cur = cue_i
    win_cues = []
    while cur < num_cues and cues[cur]['start'] <= win_end:
        win_cues.append(cues[cur]['text'])
        cur += 1
    
    text = ' '.join(win_cues)
    words = text.split()
    if len(words) >= 25:
        # Score against Internet Viral Elements
        element_hits = {}
        total_kw_score = 0
        for cat, kws in viral_keywords.items():
            count = sum(len(re.findall(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE)) for kw in kws)
            element_hits[cat] = count
            total_kw_score += count
        
        # High arousal signals: CAPS and exclamations
        caps_count = sum(1 for w in words if w.isupper() and len(w) > 2)
        excl_count = text.count('!') + text.count('?')
        
        # Calculate Base Virality Score (0 - 100)
        # 1. Zero-Context Hook (0-20)
        first_15 = ' '.join(words[:15]).lower()
        zero_context_score = 16.0
        if any(w in first_15 for w in ['look', 'yo', 'bro', 'no way', 'what', 'wait', 'run', 'watch']):
            zero_context_score = 20.0
            
        # 2. High Arousal & Audio Spike (0-25)
        arousal_score = min(25.0, 10.0 + (element_hits['arousal'] * 1.5) + (caps_count * 0.8) + (excl_count * 0.5))
        
        # 3. Conflict / Trending Tropes (0-25)
        trope_score = min(25.0, (element_hits['chase'] * 1.8) + (element_hits['combat'] * 2.0) + (element_hits['story'] * 1.5) + (element_hits['absurd'] * 2.0))
        
        # 4. Group Chat Shareability (0-15)
        share_score = min(15.0, 7.0 + (1.5 if element_hits['absurd'] > 0 else 0) + (1.5 if element_hits['combat'] > 0 else 0) + (1.5 if element_hits['story'] > 0 else 0))
        
        # 5. Climax / Punchline Payoff (0-15)
        last_15 = ' '.join(words[-15:]).lower()
        climax_score = 11.0
        if any(w in last_15 for w in ['dead', 'wasted', 'lost', 'done', 'hell no', 'died', 'kill', 'crash', 'god damn']):
            climax_score = 15.0
            
        final_score = round(zero_context_score + arousal_score + trope_score + share_score + climax_score, 1)
        final_score = min(99.0, max(50.0, final_score))
        
        # Determine dominant viral category
        dom_cat = max(element_hits.items(), key=lambda x: x[1])[0]
        
        windows.append({
            'start': t,
            'end': win_end,
            'score': final_score,
            'dom_cat': dom_cat,
            'element_hits': element_hits,
            'text': text
        })
    t += step_sec

# Sort by score descending and pick non-overlapping clips (min 15 mins apart) across all 24 hours
windows.sort(key=lambda x: x['score'], reverse=True)

selected_clips = []
min_gap = 1200.0  # 20 minutes apart! Guarantees 100% unique scenes across the 24 hours

for w in windows:
    if len(selected_clips) >= 22: # Pick Top 22 Viral Clips!
        break
    overlap = False
    for sc in selected_clips:
        if abs(w['start'] - sc['start']) < min_gap:
            overlap = True
            break
    if not overlap and w['score'] >= 80.0:
        selected_clips.append(w)

selected_clips.sort(key=lambda x: x['start'])

# Map to trending internet tropes
trope_map = {
    'chase': 'High-Speed Police Chase / Vehicle Wreck',
    'combat': 'Florida NPC Brawl / Street Gunfight',
    'arousal': 'Speed Signature Screaming / Chaos Outburst',
    'story': 'Lucia & Jason Dynamic / Vice City Storyline',
    'absurd': 'Open World Glitch / Absurd Animal & Environmental Slapstick'
}

results = []
for i, c in enumerate(selected_clips, 1):
    st_fmt = format_time(c['start'])
    en_fmt = format_time(c['end'])
    trope_name = trope_map.get(c['dom_cat'], 'GTA 6 Open World Viral Moment')
    
    # Clean text preview
    w_list = c['text'].split()
    preview = ' '.join(w_list[:25])
    
    results.append({
        'clip_no': i,
        'start_sec': c['start'],
        'end_sec': c['end'],
        'time_str': f"{st_fmt} - {en_fmt}",
        'score': c['score'],
        'category': trope_name,
        'preview': preview
    })

print(f"Extracted {len(results)} Top-Tier Viral Clips from 24h stream:\n")
for r in results:
    print(f"Clip {r['clip_no']:02d} | {r['time_str']} | Score: {r['score']}/100 | {r['category']}")

with open('data/viral_22_evaluated.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
