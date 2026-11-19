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
- `#1` [2026-11-19] Cloned and analyzed Clips Studio (`ColinGPT9/clips-studio`) architecture and code pipeline.
- `#2` [2026-11-19] Conducted hardware safety and PC pressure analysis (RTX 4050 6GB VRAM, i5-13420H, 16GB RAM) confirming smooth operation without system throttling.
- `#3` [2026-11-19] Created isolated local virtual environment (`.venv`) restricted exclusively to this workspace folder (`E:\work station\gta 6`).
- `#4` [2026-11-19] Installed and pinned required dependencies (`faster-whisper`, `torch`, `ultralytics`, `yt-dlp`, `rapidocr-onnxruntime`, `av<14`).
- `#5` [2026-11-19] Upgraded FFmpeg argument compatibility from legacy `-vsync` to modern `-fps_mode` in `video/cutter.py` and `video/encoding.py` for FFmpeg 9.0+.
- `#6` [2026-11-19] Ingested official GTA 6 video and performed GPU CUDA-accelerated speech-to-text transcription.
- `#7` [2026-11-19] Generated full HD (1080x1920) 9:16 vertical clip with word-synced animated karaoke captions rendered via NVIDIA NVENC hardware encoder (`data/clips/RockstarGames/GTA_6_Clips/clip_00062-00077.mp4`).
- `#8` [2026-11-19] Built automated multi-clip pipeline (`scripts/auto_clipper.py`) to discover and batch-render all moments from any video with zero content cut-off (`fit_blur`).
- `#9` [2026-11-19] Implemented semantic thought and sentence boundary snapping in `scripts/auto_clipper.py` to prevent joke or punchline truncation across clip cuts.
- `#10` [2026-11-19] Validated WebM container pipeline for crash-resistant video slicing without MP4 moov-atom truncation issues.
- `#11` [2026-11-19] Downloaded and sliced CarryMinati GTA 6 stream action section (00:01:00-00:15:00) cleanly into `data/downloads/carry_action_15m.webm`.
- `#15` [2026-11-19] Unzipped and integrated `stream-clips` skill into `skills/stream-clips` and Gemini skills; initialized environment, downloaded Whisper & YuNet models, verified with `streamclips doctor`.
- `#16` [2026-11-19] Produced dedicated 11-part continuous sequential 9:16 vertical series (55s each) from GTA 6 gameplay in `gta6_gameplay_series/clips` with seamless continuation and posting guide.
- `#17` [2026-11-19] Generated master same-day hourly schedule plan (`SCHEDULE_POSTING_PLAN.md`) and JSON manifest for today (1-hour intervals across all 11 parts).
- `#20` [2026-11-19] Generated 29 vertical 9:16 Shorts/Reels clips from CarryMinati GTA 6 stream using CUDA Faster-Whisper and NVENC hardware encoder with complete punchlines and `fit_blur` layout.
- `#21` [2026-11-19] Built and executed dynamic virality scoring engine (`scripts/score_and_filter_clips.py`) evaluating audio peak dB, dynamic crest factor, speech cadence, and hype keywords; partitioned clips into 8 top-tier viral clips (>=80) and 21 review candidates (<80) with delete ledger.
- `#18` [2026-11-19] Rendered high-impact Viral Hook Headline Banners (safe-zone aligned, Impact typography) on all 8 selected 80+ viral clips.
- `#19` [2026-11-19] Built master upload management and auto-delete tracking system (`UPLOAD_MANAGER.md`, `scripts/upload_manager.py`, and `data/upload_tracker.json`) with one-click metadata copy, algorithm boosting strategies, and automatic disk-cleanup upon upload.
- `#22` [2026-11-19] Processed Part 2 (next 30m, 15:00-45:00) of CarryMinati GTA 6 stream generating 78 clips, scored via virality engine yielding 23 additional 80+ clips, and consolidated all 31 viral clips into master `UPLOAD_MANAGER.md` queue.

## Backlog
- `#12` [ ] Connect local LLM (e.g. Ollama `gemma:7b`) or cloud API (Gemini/OpenRouter) for end-to-end autonomous multi-moment scoring and title generation across full 2-hour gameplay streams.
- `#13` [ ] Test Gaming/Reaction mode split-screen layout for GTA 6 streamer facecam + gameplay separation.
- `#14` [ ] Set up automated channel monitoring / scheduled batch export for new GTA 6 videos.
