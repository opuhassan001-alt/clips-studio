"""
Information Theory in Live Chat: Shannon Entropy Collapse.
Section 6 of Universal Master Spec 3.0.
"""

import math
from collections import Counter
from typing import List, Dict, Any, Tuple


def calculate_shannon_entropy(tokens_or_messages: List[str]) -> float:
    """
    Computes Shannon Entropy of token distribution:
    H(X) = -sum( P(x_i) * log2(P(x_i)) )
    
    High Entropy (>= 3.5): Normal diverse conversation.
    Low Entropy (< 1.5): Consensus swarm spam (e.g. everyone spamming '💀' or 'LMAO' or 'W').
    """
    if not tokens_or_messages:
        return 0.0

    total_count = len(tokens_or_messages)
    counts = Counter(tokens_or_messages)

    entropy = 0.0
    for token, count in counts.items():
        prob = count / total_count
        entropy -= prob * math.log2(prob)

    return entropy


def is_chat_entropy_collapsed(
    recent_messages: List[str],
    current_mps: float,
    baseline_mps: float,
    baseline_entropy: float = 4.0,
    mps_multiplier_threshold: float = 3.5,
    entropy_ratio_threshold: float = 0.8
) -> Tuple[bool, float, float]:
    """
    Validates the Mathematical Highlight Condition:
    (MPS / BaselineMPS >= 3.5) AND (Entropy <= 0.8 * BaselineEntropy)
    
    Returns:
        (is_viral_spike, current_entropy, mps_ratio)
    """
    if baseline_mps <= 0.01:
        baseline_mps = 1.0

    mps_ratio = current_mps / baseline_mps
    current_entropy = calculate_shannon_entropy(recent_messages)

    is_collapsed = (
        mps_ratio >= mps_multiplier_threshold and
        current_entropy <= (entropy_ratio_threshold * baseline_entropy)
    )

    return is_collapsed, current_entropy, mps_ratio
