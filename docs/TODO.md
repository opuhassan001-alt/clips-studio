# Project TODO Backlog

## In Progress

Append-only session locks, keyed by each item's permanent `#N` id (one
shared sequence across Backlog and Done — assigned once, shown next to the
item, never a content hash, so editing an item's wording never breaks its
lock). Never edit or delete a line here — union merge can't reconcile
in-place edits across sessions, only unioned appends. Formats:
`- CLAIM #N session <session-id> <timestamp> "optional label"`
`- RELEASE #N session <session-id> <timestamp>` (optional, only if you stop
early — a release from your own session cancels your own claim immediately)
The quoted label is optional but recommended: a future reader sees WHAT was
claimed, not just who/when — a session id alone answers "who," not "why."
Locks auto-expire after 2 hours with no release needed.

When the item is fully finished (moved to `## Done`): delete its CLAIM/
RELEASE line(s) from here entirely, in the same edit that writes the Done
entry — the Done entry is now the permanent record, the lock lines are pure
clutter once resolved. Safe specifically because it's one coordinated edit
by the session that just finished it, not a routine action or a race with
anyone. If only pausing an item that's still open, RELEASE but leave the
pair — it's a progress trail for whoever resumes it next.

If a session that claimed something gets closed, crashes, or is deleted
before finishing: don't wait out the timeout if you don't have to. The
SessionStart message shows which session id holds a locked item — write a
RELEASE line quoting THAT session's id (not your own) and it frees
immediately. The 2h expiry is only the backstop for when
nobody notices.

## Done
- `#263` `#228` `#195` `#163` `#132` `#102` `#74` `#49` `#25` `#1` [2026-11-19] Cloned and analyzed Clips Studio (`ColinGPT9/clips-studio`) architecture and code pipeline.
- `#264` `#229` `#196` `#164` `#133` `#103` `#75` `#50` `#26` `#2` [2026-11-19] Conducted hardware safety and PC pressure analysis (RTX 4050 6GB VRAM, i5-13420H, 16GB RAM) confirming smooth operation without system throttling.
- `#265` `#230` `#197` `#165` `#134` `#104` `#76` `#51` `#27` `#3` [2026-11-19] Created isolated local virtual environment (`.venv`) restricted exclusively to this workspace folder (`E:\work station\gta 6`).
- `#266` `#231` `#198` `#166` `#135` `#105` `#77` `#52` `#28` `#4` [2026-11-19] Installed and pinned required dependencies (`faster-whisper`, `torch`, `ultralytics`, `yt-dlp`, `rapidocr-onnxruntime`, `av<14`).
- `#267` `#232` `#199` `#167` `#136` `#106` `#78` `#53` `#29` `#5` [2026-11-19] Upgraded FFmpeg argument compatibility from legacy `-vsync` to modern `-fps_mode` in `video/cutter.py` and `video/encoding.py` for FFmpeg 9.0+.
- `#268` `#233` `#200` `#168` `#137` `#107` `#79` `#54` `#30` `#6` [2026-11-19] Ingested official GTA 6 video and performed GPU CUDA-accelerated speech-to-text transcription.
- `#269` `#234` `#201` `#169` `#138` `#108` `#80` `#55` `#31` `#7` [2026-11-19] Generated full HD (1080x1920) 9:16 vertical clip with word-synced animated karaoke captions rendered via NVIDIA NVENC hardware encoder (`data/clips/RockstarGames/GTA_6_Clips/clip_00062-00077.mp4`).
- `#270` `#235` `#202` `#170` `#139` `#109` `#81` `#56` `#32` `#8` [2026-11-19] Built automated multi-clip pipeline (`scripts/auto_clipper.py`) to discover and batch-render all moments from any video with zero content cut-off (`fit_blur`).
- `#271` `#236` `#203` `#171` `#140` `#110` `#82` `#57` `#33` `#9` [2026-11-19] Implemented semantic thought and sentence boundary snapping in `scripts/auto_clipper.py` to prevent joke or punchline truncation across clip cuts.
- `#272` `#237` `#204` `#172` `#141` `#111` `#83` `#58` `#34` `#10` [2026-11-19] Validated WebM container pipeline for crash-resistant video slicing without MP4 moov-atom truncation issues.
- `#273` `#238` `#205` `#173` `#142` `#112` `#84` `#59` `#35` `#11` [2026-11-19] Downloaded and sliced CarryMinati GTA 6 stream action section (00:01:00-00:15:00) cleanly into `data/downloads/carry_action_15m.webm`.
- `#274` `#239` `#206` `#174` `#143` `#113` `#85` `#60` `#36` `#15` [2026-11-19] Unzipped and integrated `stream-clips` skill into `skills/stream-clips` and Gemini skills; initialized environment, downloaded Whisper & YuNet models, verified with `streamclips doctor`.
- `#275` `#240` `#207` `#175` `#144` `#114` `#86` `#61` `#37` `#16` [2026-11-19] Produced dedicated 11-part continuous sequential 9:16 vertical series (55s each) from GTA 6 gameplay in `gta6_gameplay_series/clips` with seamless continuation and posting guide.
- `#276` `#241` `#208` `#176` `#145` `#115` `#87` `#62` `#38` `#17` [2026-11-19] Generated master same-day hourly schedule plan (`SCHEDULE_POSTING_PLAN.md`) and JSON manifest for today (1-hour intervals across all 11 parts).
- `#277` `#242` `#209` `#177` `#146` `#116` `#88` `#63` `#39` `#20` [2026-11-19] Generated 29 vertical 9:16 Shorts/Reels clips from CarryMinati GTA 6 stream using CUDA Faster-Whisper and NVENC hardware encoder with complete punchlines and `fit_blur` layout.
- `#278` `#243` `#210` `#178` `#147` `#117` `#89` `#64` `#40` `#21` [2026-11-19] Built and executed dynamic virality scoring engine (`scripts/score_and_filter_clips.py`) evaluating audio peak dB, dynamic crest factor, speech cadence, and hype keywords; partitioned clips into 8 top-tier viral clips (>=80) and 21 review candidates (<80) with delete ledger.
- `#279` `#244` `#211` `#179` `#148` `#118` `#90` `#65` `#41` `#18` [2026-11-19] Rendered high-impact Viral Hook Headline Banners (safe-zone aligned, Impact typography) on all 8 selected 80+ viral clips.
- `#280` `#245` `#212` `#180` `#149` `#119` `#91` `#66` `#42` `#19` [2026-11-19] Built master upload management and auto-delete tracking system (`UPLOAD_MANAGER.md`, `scripts/upload_manager.py`, and `data/upload_tracker.json`) with one-click metadata copy, algorithm boosting strategies, and automatic disk-cleanup upon upload.
- `#281` `#246` `#213` `#181` `#150` `#120` `#92` `#67` `#43` `#22` [2026-11-19] Processed Part 2 (next 30m, 15:00-45:00) of CarryMinati GTA 6 stream generating 78 clips, scored via virality engine yielding 23 additional 80+ clips, and consolidated all 31 viral clips into master `UPLOAD_MANAGER.md` queue.
- `#282` `#247` `#214` `#182` `#151` `#121` `#93` `#68` `#44` `#23` [2026-11-19] Built unified master posting schedule (`MASTER_UPLOAD_SCHEDULE.md`, `scripts/build_master_schedule.py`, `scripts/dynamic_scheduler.py`) harmonizing 11 Gameplay Walkthrough parts with 31 CarryMinati Viral clips (42 clips total) using dynamic rotating anti-bot intervals (45m -> 46m -> 50m -> 55m -> 60m).
- `#283` `#248` `#215` `#183` `#152` `#122` `#94` `#69` `#45` `#24` [2026-11-19] Successfully scheduled all 11 parts of GTA 6 Gameplay Walkthrough Series to Instagram Reels via official Meta Business Suite queue with sequential release times.
- `#284` `#249` `#216` `#184` `#153` `#123` `#95` `#73` [2026-11-19] Built and integrated YouTube Anti-Strike & Pre-Flight Compliance Skill (`skills/yt-safety-guard/SKILL.md` + global config) and local audio-visual compliance processing engine (`scripts/yt_compliance_guard.py`); hooked auto-shielding directly into `scripts/auto_clipper.py` to auto-generate YouTube Shorts & Instagram Reels `POSTING_PACK.md` on every cut; corrected 11-part GTA 6 schedule in `SCHEDULE_POSTING_PLAN.md` into anti-bot 4-day distribution with TOS-compliant metadata and Fair Use disclaimers.
- `#285` `#250` `#217` `#185` `#154` `#124` `#99` [2026-11-19] Built Dynamic Context Hook Banner Engine (`scripts/dynamic_hook_engine.py`) and wired it directly into `scripts/auto_clipper.py` and `skills/yt-safety-guard`; automatically generates context-aware viral headline script with emojis and bakes pill-box banner across facecam/gameplay divider in a single render pass.
- `#286` `#251` `#218` `#186` `#155` `#125` `#100` [2026-11-19] Fully configured and launched YouTube Channel `BOTS gaming` via Creator Studio: updated channel name (`BOTS gaming`), published 30-year veteran copy description, verified 1:1 Lucia & Jason custom avatar, set country (`Bangladesh`), 12 targeted gaming SEO keywords, audience ('Not Made for Kids'), and upload defaults (Gaming / Unlisted / English).
- `#287` `#252` `#219` `#187` `#156` `#126` `#101` [2026-11-19] Successfully scheduled all 31 clips of the CarryMinati GTA 6 80+ Viral Series to Instagram Reels via official Meta Business Suite queue with dynamic rotating anti-bot intervals (45m -> 46m -> 50m -> 55m -> 60m) spanning Nov 20-21, 2026.
- `#288` `#253` `#220` `#188` `#157` `#130` `#102` [2026-11-19] Executed post-upload disk space cleanup: safely purged all 128 local rendered media files, cut clips, and test frames (2.21 GB freed) across `data/clips/` and `gta6_gameplay_series/clips/` while 100% preserving all scripts, skills, configs, and raw downloads.
- `#289` `#254` `#221` `#189` `#158` `#131` [2026-11-19] Built Global Viral Radar Engine (`scripts/global_viral_radar.py`, `skills/global-viral-radar/SKILL.md`, and `.github/workflows/daily_viral_radar.yml`); scrapes worldwide top gaming streams (>= 30 mins) from last 24h, filters completed VODs, computes view velocity, tags creator clipping safety, generates actionable `DAILY_VIRAL_REPORT.md`, and archives/clears upon user review; configured 100% free cloud execution via GitHub Actions for daily automated reports even when laptop is powered off.
- `#290` `#255` `#222` `#190` `#132` [2026-11-19] Sliced Kai Cenat GTA 6 Stream (10:00-40:00, 30 mins) into 87 vertical 9:16 clips with animated captions and dynamic context hook banners; scored via virality engine yielding 39 top-tier 80+ clips in `data/clips/kai_action_30m/selected_viral_80_plus/` with auto-generated YouTube & Instagram `POSTING_PACK.md` and 48 under-80 review candidates in delete ledger.
- `#291` `#256` `#223` `#162` [2026-11-19] Processed CarryMinati GTA 6 Stream strictly after 30-min mark (30:00-45:00), integrated multimodal 3-layer emotional & crying detection, scored moments via 80+ virality engine, and rendered 10 high-impact 9:16 vertical clips in `data/clips/carry_post30m_viral` with context-accurate dynamic hook banners, word-synced animated captions, and YouTube pre-flight compliance guard.
- `#292` `#257` `#227` [2026-11-19] Configured 3-minute (180s) maximum duration limit and dynamic pacing rules across `stream-clips` skill (workspace + global config) and `scripts/auto_clipper.py`: 30-45s for quick punchy cuts, 45-60s standard sweet spot, and continuous extension up to 180s without mid-climax cuts as long as high engagement/fun persists.
- `#293` `#261` [2026-11-19] Successfully uploaded and scheduled 9 YouTube Shorts to channel `BOTS gaming` across 5 days (Nov 19-23) with anti-strike Fair Use disclaimers using randomized anti-bot time slots (~11:00 AM & ~10:00 PM); executed full disk cleanup deleting all 9 uploaded video files, all 48 under-80 clips in `data/clips/kai_action_30m/review_under_80/`, temporary partial downloads, and scoring delete ledger files.
- `#294` `#262` [2026-11-19] Merged all 30 remaining 80+ clips into `data/clips/carry_post30m_viral/`, renumbered them continuously from Part 11 to Part 40, consolidated into unified `POSTING_PACK.md` and `POSTING_PACK.json` (40 clips total with complete copy-paste metadata), and cleanly purged the empty `data/clips/kai_action_30m/` directory.

## Backlog
- `#298` [ ] [REMINDER Nov 24, 2026 10:00 AM BDT] YouTube 9-part upload broadcast finishes (final clip Part 9 goes live Nov 23 at 10:02 PM). Remind user immediately, navigate to YouTube Studio Analytics via Kapture, analyze peak viewer spike hours, top viewed clips & retention drivers, and set data-driven posting schedule for remaining 40 clips in `data/clips/carry_post30m_viral/`.
- `#295` `#258` `#224` `#192` `#159` `#127` `#96` `#70` `#46` `#12` [ ] Connect local LLM (e.g. Ollama `gemma:7b`) or cloud API (Gemini/OpenRouter) for end-to-end autonomous multi-moment scoring and title generation across full 2-hour gameplay streams.
- `#296` `#259` `#225` `#193` `#160` `#128` `#97` `#71` `#47` `#13` [ ] Test Gaming/Reaction mode split-screen layout for GTA 6 streamer facecam + gameplay separation.
- `#297` `#260` `#226` `#194` `#161` `#129` `#98` `#72` `#48` `#14` [ ] Set up automated channel monitoring / scheduled batch export for new GTA 6 videos.
