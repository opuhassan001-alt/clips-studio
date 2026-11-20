"""
TikTok SEO: The Blue Search Bar & The Rule of Three.
Section 11 of Universal Master Spec 3.0.
"""

from typing import Dict, Any, List


def generate_rule_of_three_seo(
    topic: str,
    key_event: str,
    creator_tag: str = "@amir_man_point"
) -> Dict[str, str]:
    """
    Generates exact matched triplets across all three modalities:
    1. Spoken Hook (ASR): Spoken within the first 3 seconds
    2. On-Screen Title (OCR): Displayed on frame 1 in bold typography
    3. Caption Description (NLP): First sentence of the written post description
    
    When all three modalities match an existing high-volume query,
    TikTok binds the video to the clickable Blue Search Bar.
    """
    topic_clean = topic.strip()
    event_clean = key_event.strip()

    # Exact high-volume search term (3 to 6 words)
    blue_search_term = f"{topic_clean} {event_clean}".title()

    spoken_hook = f"Watch this insane {topic_clean} {event_clean}!"
    on_screen_title = f"{topic_clean.upper()} {event_clean.upper()}"
    caption_desc = (
        f"Here is the {topic_clean} {event_clean} moment everyone is talking about! "
        f"Watch until the end to see the full climax. Follow {creator_tag} for daily clips! "
        f"#{topic_clean.replace(' ', '')} #Gaming #ViralClips #Shorts #Reels"
    )

    return {
        "blue_search_term": blue_search_term,
        "spoken_hook": spoken_hook,
        "on_screen_title": on_screen_title,
        "caption_description": caption_desc
    }
