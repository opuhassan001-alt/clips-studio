import json
import re

with open(r'E:\work station\gta 6\data\clips\speed_gta6_viral\POSTING_PACK.md', 'r', encoding='utf-8') as f:
    text = f.read()

parts = re.split(r'## Part (\d+):', text)[1:]

schedule_map = {
    3:  {'day': 22, 'month': 'Nov', 'time': '11:00'},
    4:  {'day': 22, 'month': 'Nov', 'time': '15:00'},
    5:  {'day': 22, 'month': 'Nov', 'time': '19:00'},
    6:  {'day': 22, 'month': 'Nov', 'time': '22:00'},
    7:  {'day': 23, 'month': 'Nov', 'time': '11:00'},
    8:  {'day': 23, 'month': 'Nov', 'time': '15:00'},
    9:  {'day': 23, 'month': 'Nov', 'time': '19:00'},
    10: {'day': 23, 'month': 'Nov', 'time': '22:00'},
    11: {'day': 24, 'month': 'Nov', 'time': '11:00'},
    12: {'day': 24, 'month': 'Nov', 'time': '15:00'},
    13: {'day': 24, 'month': 'Nov', 'time': '19:00'},
    14: {'day': 24, 'month': 'Nov', 'time': '22:00'},
    15: {'day': 25, 'month': 'Nov', 'time': '11:00'},
    16: {'day': 25, 'month': 'Nov', 'time': '15:00'},
    17: {'day': 25, 'month': 'Nov', 'time': '19:00'},
    18: {'day': 25, 'month': 'Nov', 'time': '22:00'},
    19: {'day': 26, 'month': 'Nov', 'time': '11:00'},
    20: {'day': 26, 'month': 'Nov', 'time': '15:00'},
    21: {'day': 26, 'month': 'Nov', 'time': '19:00'},
    22: {'day': 26, 'month': 'Nov', 'time': '22:00'}
}

clips = []
for i in range(0, len(parts), 2):
    num = int(parts[i])
    content = parts[i+1]
    
    fn_m = re.search(r'\*\*Filename\*\*:\s*`([^`]+)`', content)
    filename = fn_m.group(1) if fn_m else ''
    
    title_m = re.search(r'\*\*Title:\*\*\s*\n```text\s*\n([^\n]+)', content)
    title = title_m.group(1).strip() if title_m else ''
    
    desc_m = re.search(r'\*\*Description:\*\*\s*\n```text\s*\n([\s\S]*?)```', content)
    desc = desc_m.group(1).strip() if desc_m else ''
    
    sched = schedule_map.get(num, {})
    
    clips.append({
        'num': num,
        'filename': filename,
        'title': title,
        'desc': desc,
        'day': sched.get('day'),
        'month': sched.get('month'),
        'time': sched.get('time')
    })

with open(r'E:\work station\gta 6\data\clips\speed_gta6_viral\schedule_queue.json', 'w', encoding='utf-8') as f:
    json.dump(clips, f, indent=2, ensure_ascii=False)

print(f'Parsed {len(clips)} clips successfully!')
