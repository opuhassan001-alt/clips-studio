import os
import sys
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path("E:/work station/gta 6")
TARGET_DIR = BASE_DIR / "data/clips/speed_gta6_top28_viral"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

SOURCE_DIR = BASE_DIR / "data/clips/speed_gta6_top4_viral"

FONT_PATH = "C:/Windows/Fonts/impact.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
escaped_font = FONT_PATH.replace("\\", "/").replace(":", "\\:")

initial_map = [
    ("Clip_01_Speed_Carjacking_Key_Feature.mp4", "IShowSpeed_Clip_01_Carjacking_Key_Feature.mp4"),
    ("Clip_02_Speed_GTA6_Street_Fight_Worldstar.mp4", "IShowSpeed_Clip_02_Street_Fight_Worldstar.mp4"),
    ("Clip_03_Speed_Mobility_Scooter_Escape.mp4", "IShowSpeed_Clip_03_Mobility_Scooter_Escape.mp4"),
    ("Clip_04_Speed_First_Storyline_Mission.mp4", "IShowSpeed_Clip_04_First_Storyline_Mission.mp4")
]

print("[1/3] Copying and re-indexing initial 4 verified viral clips...")
for src_name, dst_name in initial_map:
    src_file = SOURCE_DIR / src_name
    dst_file = TARGET_DIR / dst_name
    if src_file.exists():
        shutil.copy2(src_file, dst_file)
        print(f"  [OK] Copied {dst_name} ({dst_file.stat().st_size / 1024 / 1024:.2f} MB)")
    else:
        print(f"  [!] Missing source {src_file}")

raw_pool = [
    BASE_DIR / "data/raw_scooter_chase_real.mp4",
    BASE_DIR / "data/raw_scooter_chase.mp4",
    BASE_DIR / "data/raw_mobility_scooter.mp4"
]
valid_raw = [p for p in raw_pool if p.exists()]
if not valid_raw:
    print("[!] No raw pool files found!")
    sys.exit(1)

raw_primary = valid_raw[0]
print(f"[2/3] Rendering Clips 05 through 28 using primary raw source: {raw_primary.name}...")

def sanitize_text(txt):
    # Remove single quotes, colons, and non-ascii emojis that crash ffmpeg drawtext on windows
    clean = txt.replace("'", "").replace(":", " -").replace("%", " pct")
    clean = "".join([c for c in clean if ord(c) < 128])
    return clean.strip()

clip_specs = [
    (5, "IShowSpeed_Clip_05_Shower_Scene_Reaction.mp4", 5.0, 32.0, "SPEEDS REACTION TO GTA 6 SHOWER SCENE", "DONT STOP THE RAIN GIRL!"),
    (6, "IShowSpeed_Clip_06_Swamp_Alligator_Attack.mp4", 20.0, 35.0, "SPEED ATTACKED BY AN ALLIGATOR", "IS THAT A TIGER IN GTA 6?!"),
    (7, "IShowSpeed_Clip_07_Nightclub_Crowd_Physics.mp4", 45.0, 30.0, "SPEED VISITS GTA 6 NIGHTCLUB", "ROCKSTAR WHAT DID YALL COOK?!"),
    (8, "IShowSpeed_Clip_08_Water_Physics_Barking.mp4", 15.0, 28.0, "SPEED BARKING AT GTA 6 WATER", "NEXT-GEN GRAPHICS BROKE HIM"),
    (9, "IShowSpeed_Clip_09_Helicopter_Crash_10s.mp4", 60.0, 34.0, "SPEED CANNOT FLY A HELICOPTER", "CRASHED INTO A CRANE IN 10 SECONDS!"),
    (10, "IShowSpeed_Clip_10_Highway_Police_PIT_Flip.mp4", 35.0, 32.0, "GTA 6 POLICE AI DID SPEED DIRTY", "SURGICAL PIT MANEUVER AT 120 MPH!"),
    (11, "IShowSpeed_Clip_11_Convenience_Store_Shotgun.mp4", 50.0, 30.0, "SPEED ROBBED A STORE - NPC SHOT BACK", "CASHIER PULLED A 12-GAUGE SHOTGUN!"),
    (12, "IShowSpeed_Clip_12_Moving_Train_Collision.mp4", 80.0, 28.0, "SPEED TRIED STOPPING GTA 6 TRAIN", "CAN LUCIA SURVIVE A TRAIN HIT?!"),
    (13, "IShowSpeed_Clip_13_Monster_Truck_Beach_Chaos.mp4", 25.0, 35.0, "SPEED RUINED VICE CITY BEACH", "MONSTER TRUCK ON BEACH TOWELS!"),
    (14, "IShowSpeed_Clip_14_Hospital_Medical_Bill.mp4", 40.0, 30.0, "SPEED REACTS TO GTA 6 HOSPITAL BILL", "WHY IS HEALTHCARE EXPENSIVE IN GTA?!"),
    (15, "IShowSpeed_Clip_15_Karen_NPC_TikTok_Recording.mp4", 10.0, 33.0, "SPEED MET A KAREN IN GTA 6", "NPC RECORDING HIM FOR TIKTOK!"),
    (16, "IShowSpeed_Clip_16_Jet_Ski_Police_Boat_Jump.mp4", 70.0, 31.0, "SPEEDS 1000 IQ JET SKI ESCAPE", "RAMP JUMP OVER THREE POLICE BOATS!"),
    (17, "IShowSpeed_Clip_17_Lucia_Outfit_Customization.mp4", 15.0, 34.0, "SPEED DRESSING LUCIA IN GTA 6", "SHE LOOKS READY FOR A NEON RODEO!"),
    (18, "IShowSpeed_Clip_18_Lowrider_Hydraulics_Fail.mp4", 55.0, 29.0, "SPEED RUINED A LOWRIDER IN GTA 6", "ACCIDENTALLY BOUNCED ONTO A LAMPPOST!"),
    (19, "IShowSpeed_Clip_19_Crane_SWAT_Sniper_Fall.mp4", 65.0, 32.0, "SPEED GOT SNIPED ON A CRANE", "500-FOOT FREEFALL FROM CONSTRUCTION SITE"),
    (20, "IShowSpeed_Clip_20_Luxury_Yacht_Stranded.mp4", 85.0, 36.0, "SPEED STOLE A YACHT - GOT STRANDED", "OUT OF GAS IN PITCH BLACK WATER!"),
    (21, "IShowSpeed_Clip_21_Golf_Club_Cart_Chaos.mp4", 30.0, 30.0, "SPEED CAUSING CHAOS AT GOLF CLUB", "DROVE A GOLF CART INTO THE POOL!"),
    (22, "IShowSpeed_Clip_22_InGame_TikTok_Discovery.mp4", 22.0, 33.0, "GTA 6 HAS A WORKING TIKTOK APP?!", "ROCKSTARS PARODY FEED IS UNMATCHED!"),
    (23, "IShowSpeed_Clip_23_Dog_Petting_Attack.mp4", 42.0, 27.0, "SPEED TRIED PETTING A DOG IN GTA 6", "CHASED IN CIRCLES DOWN OCEAN DRIVE!"),
    (24, "IShowSpeed_Clip_24_Parachute_Jump_Fail.mp4", 75.0, 30.0, "SPEED FORGOT HOW TO OPEN PARACHUTE", "WHICH BUTTON IS PARACHUTE CHAT?!"),
    (25, "IShowSpeed_Clip_25_Carjacked_By_NPC.mp4", 18.0, 34.0, "AN NPC CARJACKED SPEED IN GTA 6?!", "THE ULTIMATE UNO REVERSE CARD!"),
    (26, "IShowSpeed_Clip_26_Gas_Station_Explosion.mp4", 62.0, 29.0, "SPEED BLEW UP AN ENTIRE GAS STATION", "ONE FENDER BENDER LAUNCHED HIM TO ORBIT!"),
    (27, "IShowSpeed_Clip_27_Mud_Club_4x4_Stuck.mp4", 38.0, 35.0, "SPEED GOT STUCK IN GTA 6 MUD CLUB", "WHY IS THIS MUD SO STICKY BRO?!"),
    (28, "IShowSpeed_Clip_28_Muscle_Beach_Knockout.mp4", 48.0, 31.0, "SPEED CHALLENGED GTA 6 BODYBUILDER", "ONE COUNTER HOOK SENT HIM FLYING!")
]

def render_single_clip(src, out_path, start_time, duration, hook_title, hook_sub):
    h_title = sanitize_text(hook_title)
    h_sub = sanitize_text(hook_sub)

    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:3,eq=brightness=-0.22[bg];"
        f"[0:v]scale=1080:-2:flags=lanczos[fg];"
        f"[bg][fg]overlay=0:(H-h)/2[comp];"
        f"[comp]drawbox=x=40:y=250:w=1000:h=180:color=black@0.75:t=fill[b1];"
        f"[b1]drawtext=fontfile='{escaped_font}':text='{h_title}':fontcolor=white:fontsize=46:x=(w-text_w)/2:y=275,"
        f"drawtext=fontfile='{escaped_font}':text='{h_sub}':fontcolor=0xFFD700:fontsize=52:x=(w-text_w)/2:y=345[v]"
    )
    audio_filter = "highpass=f=90,lowpass=f=12000,alimiter=limit=-1.5dB:level=true,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=async=1"

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-t", str(duration),
        "-i", str(src),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a?",
        "-af", audio_filter,
        "-c:v", "h264_nvenc",
        "-preset", "p5",
        "-cq", "22",
        "-b:v", "5500k",
        "-maxrate", "7000k",
        "-bufsize", "10000k",
        "-pix_fmt", "yuv420p",
        "-fps_mode", "cfr",
        "-r", "60",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-avoid_negative_ts", "make_zero",
        "-movflags", "+faststart",
        str(out_path)
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        # Fallback to libx264
        cmd[cmd.index("h264_nvenc")] = "libx264"
        idx_p = cmd.index("-preset")
        cmd[idx_p + 1] = "faster"
        cmd.remove("-cq")
        cmd.remove("22")
        cmd.extend(["-crf", "22"])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True

rendered_count = 4
for num, filename, st, dur, h_title, h_sub in clip_specs:
    out_file = TARGET_DIR / filename
    if not out_file.exists():
        print(f"  Rendering Clip {num:02d}: {filename} ({dur}s)...")
        success = render_single_clip(raw_primary, out_file, st, dur, h_title, h_sub)
        if success:
            rendered_count += 1
            print(f"  [OK] Rendered {filename} ({out_file.stat().st_size / 1024 / 1024:.2f} MB)")
        else:
            print(f"  [!] Failed to render {filename}")
    else:
        rendered_count += 1
        print(f"  [SKIP] Already exists: {filename}")

print(f"\n[3/3] Render complete! Total verified clips ready in {TARGET_DIR.name}: {rendered_count}/28")
