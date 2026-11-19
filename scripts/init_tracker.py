import json
from pathlib import Path
from upload_manager import save_tracker

clips_data = [
    {
        "id": "CLIP-01",
        "file_name": "clip_00415-00430.mp4",
        "file_path": "E:/work station/gta 6/data/clips/carry_action_15m/selected_viral_80_plus/clip_00415-00430.mp4",
        "title": "CARRY MINATIS REACTION TO GTA 6 😂",
        "score": 97.0,
        "duration": 15.0,
        "status": "READY",
        "caption": "CarryMinati's live reaction when seeing the new GTA 6 mechanics and Vice City streets for the first time! Is this the greatest gaming moment of the decade? Watch till the end! #GTA6 #CarryMinati #ViceCity #GTA6Trailer #GamingShorts",
        "hashtags": "#GTA6 #CarryMinati #GrandTheftAuto6 #ViceCity #RockstarGames #Gaming #Shorts #Reels #ViralGaming #GTA6Memes",
        "pinned_comment": "Did Rockstar cook with GTA 6 or what? Rate Carry's reaction from 1-10 👇",
        "posting_window": "6:30 PM - 9:00 PM (Peak Indian / Global Viewer Activity)"
    },
    {
        "id": "CLIP-02",
        "file_name": "clip_00811-00827.mp4",
        "file_path": "E:/work station/gta 6/data/clips/carry_action_15m/selected_viral_80_plus/clip_00811-00827.mp4",
        "title": "WAIT TILL THE END - GTA 6 MONEY GLITCH?! 💀",
        "score": 96.2,
        "duration": 16.0,
        "status": "READY",
        "caption": "CarryMinati gets unlimited money in GTA 6 Vice City?! The funniest dialogue moment from today's stream! #GTA6 #CarryMinati #GamingFunny #RockstarGames",
        "hashtags": "#GTA6 #CarryMinati #GTAVIFunny #GrandTheftAuto #GamingCommunity #ShortsFeed #ViralReels",
        "pinned_comment": "What is the first thing you are buying in GTA 6? 🚗💰",
        "posting_window": "1:00 PM - 3:30 PM or 7:00 PM - 9:30 PM"
    },
    {
        "id": "CLIP-03",
        "file_name": "clip_00142-00156.mp4",
        "file_path": "E:/work station/gta 6/data/clips/carry_action_15m/selected_viral_80_plus/clip_00142-00156.mp4",
        "title": "CARRY MINATI RECALLS HIS FIRST EVER GTA 🔥",
        "score": 91.2,
        "duration": 14.0,
        "status": "READY",
        "caption": "Pure nostalgia! CarryMinati talking about playing his very first GTA game vs GTA 6 today. Who remembers playing GTA Vice City back in the day? #GTA6 #Nostalgia #CarryMinati",
        "hashtags": "#GTA6 #GTA6Nostalgia #CarryMinati #ViceCity #SanAndreas #GamersOfInstagram #TrendingShorts",
        "pinned_comment": "Which GTA game was your childhood favorite? Vice City or San Andreas? 👇",
        "posting_window": "7:30 PM - 10:00 PM"
    },
    {
        "id": "CLIP-04",
        "file_name": "clip_00276-00296.mp4",
        "file_path": "E:/work station/gta 6/data/clips/carry_action_15m/selected_viral_80_plus/clip_00276-00296.mp4",
        "title": "TARGET 10K LIKES FOR GTA 6 🚀",
        "score": 91.2,
        "duration": 20.0,
        "status": "READY",
        "caption": "CarryMinati demanding 10k likes before GTA 6 drops! Let's smash that like button! #CarryMinati #GTA6 #LiveStreamHighlights",
        "hashtags": "#GTA6 #CarryMinatiLive #GamingHumor #GrandTheftAuto6 #YouTubeShorts #FYP",
        "pinned_comment": "Can we hit 10k likes on this short before GTA 6 release date? Hit that subscribe! 🔔",
        "posting_window": "5:00 PM - 8:00 PM"
    },
    {
        "id": "CLIP-05",
        "file_name": "clip_00034-00061.mp4",
        "file_path": "E:/work station/gta 6/data/clips/carry_action_15m/selected_viral_80_plus/clip_00034-00061.mp4",
        "title": "CRAZY GTA 6 HYPE MOMENT 🤯",
        "score": 89.6,
        "duration": 27.0,
        "status": "READY",
        "caption": "The hype is REAL! CarryMinati screaming and losing his mind watching the GTA 6 gameplay reveal! #GTA6 #CarryMinati #InsaneReaction",
        "hashtags": "#GTA6 #GTA6Hype #CarryMinati #RockstarGames #LuciaAndJason #TrendingGaming",
        "pinned_comment": "Who else got goosebumps watching this? 🙋‍♂️🔥",
        "posting_window": "8:00 PM - 10:30 PM"
    },
    {
        "id": "CLIP-06",
        "file_name": "clip_00018-00030.mp4",
        "file_path": "E:/work station/gta 6/data/clips/carry_action_15m/selected_viral_80_plus/clip_00018-00030.mp4",
        "title": "TODAY IS SPECIAL - GTA 6 REVEAL 💥",
        "score": 81.4,
        "duration": 12.0,
        "status": "READY",
        "caption": "Something special is happening today! Carry announces the biggest game of our lifetime! #GTA6 #CarryMinati",
        "hashtags": "#GTA6 #GamingNews #CarryMinati #GTAVIRules #Shorts",
        "pinned_comment": "Are you playing on PS5, Xbox Series X or waiting for PC? 👇",
        "posting_window": "12:00 PM - 2:00 PM"
    },
    {
        "id": "CLIP-07",
        "file_name": "clip_00065-00079.mp4",
        "file_path": "E:/work station/gta 6/data/clips/carry_action_15m/selected_viral_80_plus/clip_00065-00079.mp4",
        "title": "16 YEARS OF WAITING IS OVER 😭",
        "score": 80.5,
        "duration": 14.0,
        "status": "READY",
        "caption": "We waited over a decade for this moment! CarryMinati gets emotional about GTA 6 release timeline! #GTA6 #16YearsWait #CarryMinati",
        "hashtags": "#GTA6 #GTARelease #CarryMinati #GamingCommunity #EmotionalGamer",
        "pinned_comment": "How old will you be when GTA 6 finally releases? Be honest! 💀",
        "posting_window": "6:00 PM - 9:00 PM"
    },
    {
        "id": "CLIP-08",
        "file_name": "clip_00429-00460.mp4",
        "file_path": "E:/work station/gta 6/data/clips/carry_action_15m/selected_viral_80_plus/clip_00429-00460.mp4",
        "title": "GTA 6 GAMEPLAY SETTINGS EXPLAINED 🎮",
        "score": 80.5,
        "duration": 31.0,
        "status": "READY",
        "caption": "CarryMinati breaking down the graphics, framerate, and settings in GTA 6! Everything you need to know in 30 seconds! #GTA6 #GamingTips #Tech",
        "hashtags": "#GTA6 #GTA6Graphics #CarryMinati #GamingTech #Shorts",
        "pinned_comment": "Will your PC/Console run GTA 6 smoothly? Drop your specs! 💻👇",
        "posting_window": "4:00 PM - 7:00 PM"
    }
]

if __name__ == "__main__":
    save_tracker({"clips": clips_data})
    print("Tracker initialized with 8 clips!")
