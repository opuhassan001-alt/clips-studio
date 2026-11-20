"""
The 5-Point Viral Litmus Test & Dynamic Zero-Quota Gate.
Sections 2 & 8 of Universal Master Spec 3.0.
"""

from typing import Dict, Any, List, Tuple


def evaluate_5point_litmus_test(
    clip_metadata: Dict[str, Any],
    acoustic_score: float = 0.0,
    chat_entropy_score: float = 0.0,
    emotional_score: float = 0.0
) -> Dict[str, Any]:
    """
    Evaluates a candidate clip against the 5-Point Viral Litmus Test:
    1. Zero-Context Check: Can a complete stranger understand within 3 seconds?
    2. High Arousal: Does it trigger peak emotion (laugh, shock, rage)?
    3. Group Chat Shareability: Would someone DM this to a friend?
    4. Curiosity Gap: Does the opening create an open loop?
    5. Climax Payoff: Does it finish with a clean punchline or resolution?
    
    Returns structured scores (1.0 - 10.0 scale) and verdict.
    """
    transcript = clip_metadata.get("transcript", "")
    duration = clip_metadata.get("duration", 45.0)

    # 1. Zero-Context Score
    # Deduct if dialogue refers to unnamed past events or long background exposition
    zero_context = 8.5
    if any(w in transcript.lower() for w in ["as i said before", "like we mentioned yesterday", "hours ago"]):
        zero_context -= 3.0
    if duration > 90.0:
        zero_context -= 1.0

    # 2. High Arousal Score (fueled by acoustic peaks & emotional markers)
    high_arousal = min(10.0, 5.0 + (acoustic_score * 0.25) + (emotional_score * 0.25))

    # 3. Group Chat Shareability (fueled by chat consensus and taboo/humor triggers)
    shareability = min(10.0, 5.5 + (chat_entropy_score * 0.3) + (1.5 if emotional_score > 10 else 0.0))

    # 4. Curiosity Gap (evaluated from opening hook)
    curiosity_gap = 8.0 if any(q in transcript[:60].lower() for q in ["why", "how", "what", "wait", "look", "no way"]) else 6.5

    # 5. Climax Payoff (evaluated from closing 15 seconds)
    closing = transcript[-60:].lower() if len(transcript) > 60 else transcript.lower()
    climax_payoff = 8.5 if any(p in closing for p in ["omg", "wasted", "dead", "done", "win", "lost", "hahaha", "crying"]) else 7.0

    # Weighted Composite Score (1.0 to 10.0)
    composite_score = (
        (0.25 * zero_context) +
        (0.25 * high_arousal) +
        (0.20 * shareability) +
        (0.15 * curiosity_gap) +
        (0.15 * climax_payoff)
    )

    passed_all = (
        zero_context >= 6.0 and
        high_arousal >= 6.5 and
        shareability >= 6.0 and
        curiosity_gap >= 6.0 and
        climax_payoff >= 6.0 and
        composite_score >= 8.5
    )

    return {
        "composite_score": round(composite_score, 2),
        "passed": passed_all,
        "zero_context": round(zero_context, 1),
        "high_arousal": round(high_arousal, 1),
        "shareability": round(shareability, 1),
        "curiosity_gap": round(curiosity_gap, 1),
        "climax_payoff": round(climax_payoff, 1)
    }


def enforce_zero_quota_gate(
    candidates: List[Dict[str, Any]],
    threshold: float = 8.5
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Enforces the Zero-Quota Principle:
    If no candidate achieves score >= threshold (8.5/10), return an empty list.
    Logs explicit reasoning to protect account standing.
    """
    approved = [c for c in candidates if c.get("virality_score", 0.0) >= threshold]

    if not approved:
        msg = (
            f"[ZERO-QUOTA ENFORCED]: Analyzed {len(candidates)} candidates, but 0 cleared "
            f"the strict virality threshold ({threshold}/10.0). Output set to 0 clips "
            f"to protect algorithmic account reputation from low-retention dilution."
        )
        return [], msg

    msg = f"[GATE PASSED]: {len(approved)} of {len(candidates)} candidates cleared virality threshold (>= {threshold}/10.0)."
    return approved, msg
