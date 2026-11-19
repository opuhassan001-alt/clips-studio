"""optimize_shorts.py - CLI tool for YouTube Shorts hook scoring and mobile title optimization.

Usage:
    python optimize_shorts.py                       # Auto-audits current workspace posting packs
    python optimize_shorts.py --pack <path>         # Audits and creates an optimized pack
    python optimize_shorts.py --title "..."         # Lint and score a title
    python optimize_shorts.py --title "..." --hook "..."
    python optimize_shorts.py --formulas            # Print all 21 hook formulas
"""

import argparse
import os
import sys
from pathlib import Path

# Ensure core/yt is on sys.path
BASE_DIR = Path(__file__).resolve().parent
YT_DIR = BASE_DIR / "core" / "yt"
if str(YT_DIR) not in sys.path:
    sys.path.insert(0, str(YT_DIR))

import shorts_optimizer


def print_formulas():
    print("\n=======================================================")
    print(" 🎯 21 PROVEN YOUTUBE HOOK FORMULAS")
    print("=======================================================\n")
    for f in shorts_optimizer.FORMULAS:
        print(f"• {f.get('name')} (ID: {f.get('id')})")
        print(f"  Shape: {f.get('shape')}")
        print(f"  Example: \"{f.get('example')}\"")
        print(f"  Fails when: {f.get('fails_when')}\n")


def audit_and_save_pack(pack_path: Path):
    if not pack_path.exists():
        print(f"[!] Path not found: {pack_path}")
        return

    content = pack_path.read_text(encoding="utf-8")
    shorts_optimizer.lint_markdown_posting_pack(str(pack_path))

    # Auto-generate optimized version
    import re
    def replace_title(match):
        orig_title = match.group(1)
        opt = shorts_optimizer.optimize_clip(orig_title)
        safe = opt["shorts_title"]
        return f"- **Title**: `{safe}`"

    updated = re.sub(r"-\s*\*\*Title\*\*:\s*`([^`]+)`", replace_title, content)
    out_path = pack_path.with_name(f"{pack_path.stem}_OPTIMIZED.md")
    out_path.write_text(updated, encoding="utf-8")
    print(f"\n[OK] Generated Mobile-Safe Posting Pack -> {out_path.name}")


def main():
    parser = argparse.ArgumentParser(description="YouTube Shorts Optimizer")
    parser.add_argument("--pack", help="Path to POSTING_PACK.md or POSTING.md")
    parser.add_argument("--title", help="Evaluate single title")
    parser.add_argument("--hook", help="Evaluate single hook line")
    parser.add_argument("--formulas", action="store_true", help="List 21 hook formulas")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if args.formulas:
        print_formulas()
        return

    if args.pack:
        audit_and_save_pack(Path(args.pack))
        return

    if args.title or args.hook:
        res = shorts_optimizer.optimize_clip(args.title or "GTA 6 Gameplay", hook=args.hook or args.title)
        if args.json:
            import json
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
        return

    # Default action: Find active posting pack in workspace
    packs = list(BASE_DIR.glob("data/clips/**/POSTING_PACK.md")) + list(BASE_DIR.glob("gta6_gameplay_series/**/POSTING_GUIDE.md"))
    if packs:
        print(f"[*] Found {len(packs)} posting pack(s) in workspace. Auditing the newest:")
        audit_and_save_pack(packs[0])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
