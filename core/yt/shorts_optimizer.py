"""shorts_optimizer.py - Unified YouTube Shorts Optimization Engine.

Combines:
  1. Title & Mobile feed linter (from title.py)
  2. 5-property hook scoring & formula classifier (from hookscore.py & hooks.json)
  3. Seamless loop-point generator (from yt-shorts methodology)
  4. Automatic batch linter for POSTING_PACK.md / clips manifests.
"""

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOOKS_FILE = HERE / "hooks.json"

try:
    with open(HOOKS_FILE, "r", encoding="utf-8") as f:
        FORMULAS = json.load(f).get("hooks", [])
except Exception:
    FORMULAS = []

# Rules from title.py
DESKTOP_MAX = 60
MOBILE_MAX = 45  # Stricter for Shorts UI (channel badge & title space)
HARD_MAX = 100
VAGUE_WORDS = {
    "amazing", "incredible", "insane", "crazy", "huge", "massive", "ultimate", "best",
    "powerful", "secret", "revolutionary", "mindblowing", "epic", "perfect", "complete", "everything"
}
STOP_WORDS = {
    "the", "a", "an", "of", "for", "to", "in", "on", "and", "or", "is", "are", "with",
    "your", "you", "my", "i", "this", "that", "it", "how", "what", "why"
}

# Rules from hookscore.py
FILLER_WORDS = {
    "basically", "actually", "literally", "just", "really", "very", "so", "kind", "sort",
    "like", "guys", "hey", "welcome", "today", "video", "subscribe", "channel"
}
CONCRETE_PATTERN = re.compile(
    r"\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?)\b",
    re.I
)
YOU_PATTERN = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
STAKE_PATTERN = re.compile(
    r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead)\b",
    re.I
)
CURIOSITY_PATTERN = re.compile(
    r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually)\b",
    re.I
)

FIX_GUIDES = {
    "SPECIFICITY": "Swap adjectives for numbers, names, or a timestamp/milestone.",
    "ADDRESS": "Target the viewer directly (use 'you' / 'your') in the first 5 words.",
    "STAKES": "Highlight what happens if they look away or miss this.",
    "CURIOSITY": "Cut the half of the sentence that answers the question early.",
    "BREVITY": "Keep spoken hook to 9-20 punchy words.",
}


def words(text: str):
    return re.findall(r"[a-z0-9'%$.]+", text.lower())


def classify_formula(text: str):
    best, hits = None, 0
    for f in FORMULAS:
        n = sum(1 for p in f.get("match", []) if re.search(p, text, re.I))
        if n > hits:
            best, hits = f, n
    return (best["name"] if best else "Unclassified"), hits


def score_hook(hook_text: str):
    """Calculates 5-property hook score (0-100) with weakest-link weighting."""
    if not hook_text or not hook_text.strip():
        return {
            "score": 0,
            "band": "EMPTY",
            "formula": "None",
            "weakest": "None",
            "fix": "No hook text provided."
        }

    t = hook_text.strip()
    w = words(t)
    n_words = len(w)

    # 1. Specificity
    nums = len(CONCRETE_PATTERN.findall(t))
    vague_cnt = sum(1 for x in w if x in VAGUE_WORDS)
    filler_cnt = sum(1 for x in w if x in FILLER_WORDS)
    spec = 34 + nums * 22 - vague_cnt * 16 - filler_cnt * 5
    spec += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    spec = max(0, min(100, spec))

    # 2. Address
    n_you = len(YOU_PATTERN.findall(t))
    first_you = 30 if YOU_PATTERN.search(" ".join(t.split()[:6])) else 0
    addr = max(0, min(100, 26 + n_you * 20 + first_you))

    # 3. Stakes
    n_stakes = len(STAKE_PATTERN.findall(t))
    stk = max(0, min(100, 22 + n_stakes * 26 + (14 if CONCRETE_PATTERN.search(t) else 0)))

    # 4. Curiosity
    n_cur = len(CURIOSITY_PATTERN.findall(t))
    q = 18 if t.endswith("?") else 0
    closed = -18 if re.search(r"\b(because|so that|which means)\b", t, re.I) else 0
    cur = max(0, min(100, 24 + n_cur * 17 + q + closed))

    # 5. Brevity (Shorts sweet spot: 6-18 spoken words in first 3s)
    if 6 <= n_words <= 18:
        brev = 100
    elif n_words < 6:
        brev = max(30, 100 - (6 - n_words) * 12)
    else:
        brev = max(10, 100 - (n_words - 18) * 8)

    props = {
        "SPECIFICITY": spec,
        "ADDRESS": addr,
        "STAKES": stk,
        "CURIOSITY": cur,
        "BREVITY": brev
    }
    vals = list(props.values())
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    band = "VIRAL" if verdict >= 75 else "WORKABLE" if verdict >= 50 else "WEAK"
    formula_name, hits = classify_formula(t)
    weakest = min(props, key=props.get)

    return {
        "score": verdict,
        "band": band,
        "formula": formula_name,
        "props": props,
        "weakest": weakest,
        "fix": FIX_GUIDES.get(weakest, "")
    }


def lint_title(title_text: str, thumb_text: str = None):
    """Lints title against desktop & mobile truncation, shouting, vagueness, etc."""
    t = title_text.strip()
    n = len(t)
    issues, good = [], []

    if n > HARD_MAX:
        issues.append(("length", f"{n} chars: Exceeds hard limit {HARD_MAX}"))
    elif n > DESKTOP_MAX:
        issues.append(("length", f"{n} chars: Desktop cut off near {DESKTOP_MAX}"))
    else:
        good.append(f"{n} chars: Fits desktop cut safely")

    # Mobile check
    if n > MOBILE_MAX:
        head = t[:MOBILE_MAX].rsplit(" ", 1)[0]
        issues.append(("mobile_cutoff", f'Mobile cut after "{head}..." - subject might be lost'))
    else:
        good.append(f"{n} chars: Fully visible on mobile feed")

    # Shouting
    caps = [w for w in t.split() if len(w) > 2 and w.isupper() and w not in {"GTA", "GTA6", "VOD", "POV", "NPC"}]
    if len(caps) > 2:
        issues.append(("shouting", f"{len(caps)} all-caps words - max 2 allowed to prevent spam filter"))
    elif caps:
        good.append(f"{len(caps)} capitalized word for emphasis")

    # Vague words
    v = [w for w in words(t) if w in VAGUE_WORDS]
    if v:
        issues.append(("vague", f"Vague terms: {', '.join(sorted(set(v)))} - replace with specific action/fact"))

    # Concrete figures
    nums = re.findall(r"\d[\d,.]*%?", t)
    if nums:
        good.append(f"Contains concrete numbers: {', '.join(nums[:3])}")
    else:
        issues.append(("no_numbers", "No number, mission, or part ID - concrete markers raise CTR"))

    # Generate mobile-safe clean title if needed
    mobile_safe = t
    if n > MOBILE_MAX:
        # Strip long bracketed metadata or trailing tags for the mobile title
        cleaned = re.sub(r"\(.*?\)", "", t).strip()
        cleaned = re.sub(r"#[A-Za-z0-9_]+", "", cleaned).strip()
        if len(cleaned) <= MOBILE_MAX:
            mobile_safe = cleaned
        else:
            mobile_safe = cleaned[:MOBILE_MAX].rsplit(" ", 1)[0].strip()

    score = max(0, min(100, 100 - 15 * len(issues) + 5 * len(good)))
    return {
        "title": t,
        "mobile_safe": mobile_safe,
        "chars": n,
        "score": score,
        "issues": issues,
        "good": good
    }


def generate_loop_point(title: str, part_num: int = None):
    """Produces the exact loop structure cue so the short loops seamlessly."""
    return {
        "rule": "Ending sentence must create an unanswered setup that the first frame answers.",
        "on_screen_hook_first_2s": f"WATCH TILL END ⚡ ({title[:35]})",
        "audio_loop_tip": "Cut audio right on the last action beat without letting room tone decay.",
        "pinned_comment": f"Drop a 🔥 if you caught that! Part {(part_num + 1) if part_num else 'next'} is up on the channel."
    }


def optimize_clip(title: str, hook: str = None, part_num: int = None):
    t_lint = lint_title(title)
    h_score = score_hook(hook or title)
    loop = generate_loop_point(title, part_num)

    # Format the definitive Shorts title
    base_title = t_lint["mobile_safe"].replace('"', '').strip()
    if not base_title.endswith("#Shorts"):
        if len(base_title) + 8 <= 50:
            shorts_title = f"{base_title} #Shorts"
        else:
            shorts_title = base_title
    else:
        shorts_title = base_title

    return {
        "original_title": title,
        "shorts_title": shorts_title,
        "title_lint": t_lint,
        "hook_eval": h_score,
        "loop_strategy": loop
    }


def lint_markdown_posting_pack(file_path: str):
    """Scans and scores an existing POSTING_PACK.md."""
    path = Path(file_path)
    if not path.exists():
        print(f"[!] File not found: {file_path}")
        return

    content = path.read_text(encoding="utf-8")
    titles = re.findall(r"\*\*Title\*\*:\s*`([^`]+)`", content)
    if not titles:
        titles = re.findall(r"- \*\*Title\*\*:\s*`([^`]+)`", content)

    print(f"\n=======================================================")
    print(f" 🎬 ANALYZING SHORTS POSTING PACK: {path.name}")
    print(f" Found {len(titles)} Shorts clip titles to audit")
    print(f"=======================================================\n")

    for i, t in enumerate(titles, 1):
        opt = optimize_clip(t, part_num=i)
        print(f"[{i:02d}] Original: {t}")
        print(f"     Length: {opt['title_lint']['chars']} chars | Title Score: {opt['title_lint']['score']}/100")
        if opt['title_lint']['issues']:
            for _, msg in opt['title_lint']['issues']:
                print(f"       ⚠️  {msg}")
        print(f"     ✅ Mobile-Optimized: `{opt['shorts_title']}`")
        print(f"     🎯 Hook Formula: {opt['hook_eval']['formula']} | Hook Score: {opt['hook_eval']['score']}/100 ({opt['hook_eval']['band']})")
        print(f"     🔄 Loop Cue: {opt['loop_strategy']['audio_loop_tip']}")
        print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Shorts Optimization Engine")
    parser.add_argument("--title", help="Evaluate single title")
    parser.add_argument("--hook", help="Evaluate single hook line")
    parser.add_argument("--pack", help="Audit and optimize a full POSTING_PACK.md file")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    if args.pack:
        lint_markdown_posting_pack(args.pack)
    elif args.title or args.hook:
        res = optimize_clip(args.title or "GTA 6 Gameplay", hook=args.hook or args.title)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("\n--- SHORTS OPTIMIZATION REPORT ---")
            print(f"Original Title : {res['original_title']}")
            print(f"Shorts Title   : {res['shorts_title']}")
            print(f"Title Score    : {res['title_lint']['score']}/100 ({res['title_lint']['chars']} chars)")
            print(f"Hook Score     : {res['hook_eval']['score']}/100 [{res['hook_eval']['band']}]")
            print(f"Hook Formula   : {res['hook_eval']['formula']}")
            if res['hook_eval']['weakest'] != 'None':
                print(f"Fix Advice     : {res['hook_eval']['fix']}")
            print(f"Loop Tip       : {res['loop_strategy']['audio_loop_tip']}\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
