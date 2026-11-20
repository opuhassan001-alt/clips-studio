"""
Boundary Reverse-Tracking (The Catalyst Lock Rule).
Stage 4 of Universal Master Spec 3.0.
"""

from typing import List, Dict, Any, Tuple


def find_catalyst_boundary(
    segments: List[Any],
    peak_timestamp: float,
    min_clip_duration: float = 25.0,
    max_pre_roll: float = 25.0
) -> Tuple[float, str]:
    """
    Given a detected peak timestamp (screaming, laughter, big game event at peak_timestamp),
    scans backwards through the transcript to locate the exact catalyst sentence or setup question
    that caused the moment.
    
    Returns:
        (catalyst_start_time, catalyst_text)
    """
    if not segments:
        return max(0.0, peak_timestamp - 15.0), "Action Moment"

    # Find the segment closest to the peak
    peak_idx = 0
    for idx, s in enumerate(segments):
        s_start = getattr(s, "start", s.get("start", 0.0) if isinstance(s, dict) else 0.0)
        s_end = getattr(s, "end", s.get("end", 0.0) if isinstance(s, dict) else 0.0)
        if s_start <= peak_timestamp <= s_end:
            peak_idx = idx
            break
        elif s_start > peak_timestamp:
            peak_idx = max(0, idx - 1)
            break

    # Look backwards from peak_idx to find the start of the thought / setup sentence
    earliest_allowed = max(0.0, peak_timestamp - max_pre_roll)
    best_start = earliest_allowed
    catalyst_text = ""

    # Reverse iterate to find question marks, sentence breaks, or topic initiators
    for i in range(peak_idx, -1, -1):
        seg = segments[i]
        s_start = getattr(seg, "start", seg.get("start", 0.0) if isinstance(seg, dict) else 0.0)
        s_text = getattr(seg, "text", seg.get("text", "") if isinstance(seg, dict) else "").strip()

        if s_start < earliest_allowed:
            break

        # Check if the previous segment had a natural pause or completed sentence
        prev_has_boundary = False
        if i > 0:
            prev_seg = segments[i - 1]
            prev_end = getattr(prev_seg, "end", prev_seg.get("end", 0.0) if isinstance(prev_seg, dict) else 0.0)
            prev_text = getattr(prev_seg, "text", prev_seg.get("text", "") if isinstance(prev_seg, dict) else "").strip()
            if (s_start - prev_end > 1.2) or (prev_text and prev_text[-1] in (".", "?", "!", "…")):
                prev_has_boundary = True

        if prev_has_boundary or i == 0:
            best_start = max(0.0, s_start - 0.3)
            catalyst_text = s_text
            break

    # Ensure minimum pre-roll duration so clip has room to breathe
    if (peak_timestamp - best_start) < 4.0:
        best_start = max(0.0, peak_timestamp - 12.0)

    return best_start, catalyst_text
