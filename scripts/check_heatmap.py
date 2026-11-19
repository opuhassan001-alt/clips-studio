import json
import subprocess
import sys

cmd = [sys.executable.replace("python.exe", "yt-dlp.exe"), "--dump-single-json", "--skip-download", "https://www.youtube.com/watch?v=irNhWMG560k"]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")

for line in res.stdout.splitlines():
    line = line.strip()
    if line.startswith("{") and line.endswith("}"):
        try:
            d = json.loads(line)
            heatmap = d.get("heatmap")
            print("Heatmap available:", bool(heatmap))
            if heatmap:
                peaks = sorted(heatmap, key=lambda x: x.get("value", 0), reverse=True)[:10]
                print("\nTop 10 Most Replayed (Viral) Moments in this Stream:")
                for p in peaks:
                    s = p.get("start_time", 0)
                    e = p.get("end_time", 0)
                    val = p.get("value", 0)
                    print(f"  [{s/60:05.1f}m - {e/60:05.1f}m] ({int(s//3600)}h {int((s%3600)//60)}m {int(s%60)}s) -> Viral Score: {val:.3f}")
            break
        except Exception as e:
            continue
