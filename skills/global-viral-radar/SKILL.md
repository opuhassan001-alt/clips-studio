---
name: global-viral-radar
description: Worldwide YouTube Viral Long-form Gaming Scanner. Automatically searches for top-performing streams/videos from the last 24 hours (>= 30 minutes duration) globally. Calculates view velocity, tags creator clipping safety, generates an actionable daily report, and provides a one-click review-and-dismiss lifecycle. Runs locally or autonomously in cloud cron (GitHub Actions) while laptop is off.
---

# Global Viral Radar (`global-viral-radar`)

> **Worldwide YouTube Long-form & Stream Discovery Engine**  
> 100% Free, Cloud-Schedulable (GitHub Actions) or Local Execution.

---

## 🎯 What This Skill Does

1. **Worldwide YouTube Scraper (Last 24 Hours)**:
   - Scans global YouTube databases using protobuf parameters for today's highest-viewed videos.
   - Enforces a minimum **30-minute duration filter** (up to multi-hour streams).
   - Skips currently active/ongoing streams; only captures **completed VODs** for stable clipping.

2. **Creator Safety Index**:
   - Classifies creators into `🟢 Safe (Open Clipping)` vs `🟡 Standard Transformative` vs `🔴 High Risk`.

3. **Daily Actionable Report (`DAILY_VIRAL_REPORT.md`)**:
   - Generates a table with Rank, Streamer, Video Title, Duration, 24h Views, and View Velocity.
   - Provides one-click commands to cut reels using `scripts/auto_clipper.py`.

4. **"Seen & Dismiss" Lifecycle**:
   - When the user confirms: *"হ্যাঁ আমি রিপোর্ট দেখেছি"* or runs `python scripts/global_viral_radar.py dismiss`, the report is safely moved to `reports/archive/` and the workspace remains clean.

5. **24/7 Autonomous Cloud Execution (Even When Laptop is Off)**:
   - Configured via `.github/workflows/daily_viral_radar.yml`.
   - Runs every day at 08:00 AM BDT on GitHub's free runners, pushes the report to the repository, and waits for your review.

---

## 🚀 CLI Commands

### 1. Run a Fresh Worldwide Scan
```bash
python scripts/global_viral_radar.py scan --query "GTA 6" --limit 5
```

### 2. Clip a Specific Video by Rank
```bash
python scripts/global_viral_radar.py clip --rank 1
```

### 3. Dismiss & Archive the Report
```bash
python scripts/global_viral_radar.py dismiss
```
