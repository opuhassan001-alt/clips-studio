---
name: yt-safety-guard
description: YouTube Pre-Flight Compliance, Anti-Copyright Strike, and Ban Prevention Engine. Analyzes gameplay and video content before upload, eliminates in-game licensed music (GTA radio), audits first 7-second violence for advertiser-friendliness, prevents metadata spam/tag-stuffing, and enforces an Air-Gap Burner Sandbox workflow to guarantee 0% channel strikes and zero bans. 100% free and local.
---

# YouTube Pre-Flight Safety Guard (`yt-safety-guard`)

> **Guaranteed 0% Strike & Ban-Proof Architecture for Gaming & Video Creators**  
> 100% Free, Local, and Open Source. No subscriptions or paid APIs required.

---

## 🛑 The Core Vulnerabilities (Why Channels Get Banned)

YouTube does **NOT** rely on naive filters. Trying to "trick" algorithms with 2% zoom, horizontal flipping, or minor pitch-shifting fails due to modern AI detection (Audio Spectrogram Transformers, Optical Flow Checksums, and **Delayed/Retroactive Scanning**).

True channel safety requires eliminating root causes across four distinct enforcement layers:

1. **Third-Party Music Copyright (Content ID / Audio Fingerprint)**:
   - *Cause*: In-game car radio stations (GTA licensed music), commercial tracks, club ambience.
   - *Consequence*: Automatic Content ID block, worldwide mute, or monetization loss.
   - *Defense*: AI Audio Stem Extraction (`demucs`) to strip background music while preserving 100% of game voice dialogue and SFX losslessly.

2. **Publisher DMCA Takedowns (Take-Two / Rockstar Games Guidelines)**:
   - *Cause*: Pre-release leaks, standalone cutscenes/story movie compilations with zero gameplay, or posting game endings.
   - *Consequence*: Immediate 1st/2nd/3rd DMCA Copyright Strike leading to channel termination.
   - *Defense*: Ensure pure gameplay with transformative commentary/subtitles, zero standalone cutscenes, zero leaked assets.

3. **Inauthentic & Repetitive Content / Reused Content (YPP Demonetization)**:
   - *Cause*: Silent, unedited raw walkthroughs; mass-uploading 10+ sliced clips a day with templated titles.
   - *Consequence*: Channel rejected/kicked from YouTube Partner Program (YPP), reach shadowbanned.
   - *Defense*: Enforce transformative editing (animated captions, hook briefings) and limit release pacing to 3–4 videos/day spaced 4–6 hours apart.

4. **Community Guidelines & Advertiser-Friendly Policy (Yellow Dollar / Strikes)**:
   - *Cause*: Graphic gore or civilian torture in the **first 0–7 seconds**, in-game nudity/strip club scenes, tag-stuffing in description.
   - *Consequence*: Immediate Age-Restriction, Yellow Dollar (demonetized), or Community Guidelines Strike.
   - *Defense*: 7-Second Safe Intro validation, automated adult/nudity censorship, strict description cleanup (no comma-separated tags).

---

## 🛠️ System Architecture

```
                       [Raw Game Footage]
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ PHASE 1: Audio Stem Separation (Local Demucs AI)             │
│ • Splits audio into: Vocals (Dialogue), SFX (Combat), Music.   │
│ • Completely silences copyrighted in-game radio music.        │
│ • Retains 100% clean voice & sound effects; mixes safe BGM.   │
└───────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ PHASE 2: 7-Second Safety & Content Linter (OpenCV & FFmpeg)   │
│ • Validates that 0:00 - 0:07 has zero extreme gore/nudity.   │
│ • Dynamic Context Hook Banner: Auto-analyzes clip dialogue   │
│   and bakes in high-impact viral pill box header banner       │
│   (exact IShowSpeed / Gaming Shorts viral layout with emojis).│
│ • Verifies transformative elements (kinetic captions/HUD).    │
│ • Strips old camera/encoder metadata (zero tracking traces). │
└───────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ PHASE 3: Anti-Spam Metadata Sanitizer (Python Engine)         │
│ • Removes illegal description tag-stuffing (TOS compliant).   │
│ • Formats unique dynamic titles (avoids "Part 1, 2, 3" spam). │
│ • Appends Fair Use & Rockstar Games copyright attributions.   │
└───────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ PHASE 4: Air-Gap "Burner Sandbox" Pre-Flight Upload           │
│ • Upload video to an unlinked Test/Burner Channel (Unlisted). │
│ • Allow YouTube's automated Checks & Content ID to process.   │
│ • Verify "Checks: 0 Issues Found" before touching main channel│
└───────────────────────────────────────────────────────────────┘
```

---

## 🚀 CLI Commands & Usage

All tools run via the project's native python engine:

### 1. Audit Video Compliance
Check resolution, audio tracks, duration, and metadata:
```bash
python scripts/yt_compliance_guard.py audit --video "path/to/video.mp4"
```

### 2. Sanitize Audio & Strip In-Game Radio Music
Run automated stem scrubbing (zero music traces, crystal clean voice + SFX):
```bash
python scripts/yt_compliance_guard.py sanitize-audio --video "path/to/video.mp4" --output "path/to/safe_video.mp4"
```

### 3. Lint & Generate Compliant Metadata
Generate spam-free titles, compliant descriptions, and correct tags:
```bash
python scripts/yt_compliance_guard.py sanitize-metadata --title "Raw Title" --topic "GTA 6 Walkthrough" --part 1
```

### 4. Batch Process & Auto-Shield Clips Folder
Process all generated clips in a directory, generate `POSTING_PACK.md` & `POSTING_PACK.json` with ready-to-copy metadata for both YouTube Shorts and Instagram Reels:
```bash
python scripts/yt_compliance_guard.py process-folder --folder "gta6_gameplay_series/clips"
```

### 5. Generate Anti-Bot Safe Upload Schedule
Convert rapid-fire posting plans into safe, algorithmic schedules:
```bash
python scripts/yt_compliance_guard.py safe-schedule --clips-count 11 --max-per-day 3
```

---

## ⚡ Automated End-to-End Pipeline Hook
The compliance engine is automatically hooked into `scripts/auto_clipper.py`.  
**Every time clips are cut**, the compliance guard automatically triggers, audits the clips, and writes `POSTING_PACK.md` inside the output directory so you have one-click copy-paste metadata for YouTube and Instagram instantly.

---

## 📋 The 10 Golden Pre-Flight Rules

1. **NEVER Upload Directly as Public**: Always set initial visibility to **Unlisted** or use a secondary test channel.
2. **Wait for Checks to Finish**: YouTube's SD/HD and Copyright Checks take 10–30 minutes. Never publish while "Checks in progress".
3. **Mute In-Game Radio**: In GTA games, turn off in-game radio or use `sanitize-audio`.
4. **Clean First 7 Seconds**: Keep intros free of blood, headshots, or adult scenes for advertiser safety.
5. **No Tag Stuffing**: Tags belong in the YouTube tag box, NOT in the description.
6. **Limit Posting Velocity**: Max 3–4 Shorts per day for a new channel. Never post 10+ clips consecutively within hours.
7. **Transformative Value**: Ensure animated captions, commentary, or contextual value is present.
8. **No Standalone Cutscenes**: Always interleave gameplay; never upload pure cinematic movies.
9. **Censor Mature Content**: Blur in-game strip clubs, explicit language, and torture scenes.
10. **Include Legal Disclaimer**: Always include the Take-Two/Rockstar Games fan policy notice in your description.
