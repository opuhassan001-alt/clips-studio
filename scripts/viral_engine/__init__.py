"""
Viral Stream Clipping Engine Package.
Implements the universal 3.0 Master Specification.
"""

from .kalman_reframe import KalmanSmoothBox, auto_reframe_to_916
from .ass_karaoke import generate_viral_ass_subtitles
from .transformative_master import build_transformative_command, master_and_transform_clip
from .catalyst_tracker import find_catalyst_boundary
from .shannon_entropy import calculate_shannon_entropy, is_chat_entropy_collapsed
from .adversarial_critic import evaluate_5point_litmus_test, enforce_zero_quota_gate
from .tiktok_seo import generate_rule_of_three_seo

__all__ = [
    "KalmanSmoothBox",
    "auto_reframe_to_916",
    "generate_viral_ass_subtitles",
    "build_transformative_command",
    "master_and_transform_clip",
    "find_catalyst_boundary",
    "calculate_shannon_entropy",
    "is_chat_entropy_collapsed",
    "evaluate_5point_litmus_test",
    "enforce_zero_quota_gate",
    "generate_rule_of_three_seo"
]
