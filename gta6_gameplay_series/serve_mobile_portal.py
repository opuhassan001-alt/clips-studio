import os
import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

PORT = 8080
CLIPS_DIR = Path(r"E:\work station\gta 6\gta6_gameplay_series\clips")

# Load posting plan details
with open(r"E:\work station\gta 6\gta6_gameplay_series\schedule_manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Read captions from SCHEDULE_POSTING_PLAN.md
plan_file = Path(r"E:\work station\gta 6\gta6_gameplay_series\SCHEDULE_POSTING_PLAN.md").read_text(encoding="utf-8")

# Extract parts and captions
items = []
import re
pattern = r"### Part (\d+)\n- \*\*File\*\*: `([^`]+)`\n- \*\*Time\*\*: `([^`]+)`.*?\n```text\n(.*?)\n```"
matches = re.findall(pattern, plan_file, re.DOTALL)

for m in matches:
    part_num, file_path, time_slot, caption = m
    filename = Path(file_path).name
    items.append({
        "part": int(part_num),
        "filename": filename,
        "time": time_slot,
        "caption": caption.strip()
    })

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GTA 6 Reels Downloader & Scheduler</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: #0f111a; color: #fff; padding: 15px; }
        h1 { text-align: center; font-size: 20px; color: #ff0055; margin-bottom: 5px; }
        p.subtitle { text-align: center; font-size: 13px; color: #888; margin-bottom: 20px; }
        .card { background: #1a1d2e; border: 1px solid #2a2e45; border-radius: 12px; padding: 16px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .part-badge { background: #ff0055; color: #fff; font-weight: bold; font-size: 13px; padding: 4px 10px; border-radius: 6px; }
        .time-badge { background: #23273c; color: #00d2ff; font-size: 12px; padding: 4px 8px; border-radius: 6px; }
        .btn-download { display: block; width: 100%; background: #00b0ff; color: #fff; text-align: center; text-decoration: none; padding: 12px; border-radius: 8px; font-weight: bold; margin-bottom: 10px; font-size: 15px; }
        .btn-download:active { background: #0088cc; }
        .caption-box { background: #121420; border: 1px solid #23273c; border-radius: 8px; padding: 12px; font-size: 12px; color: #ddd; white-space: pre-wrap; word-break: break-word; max-height: 120px; overflow-y: auto; margin-bottom: 10px; }
        .btn-copy { width: 100%; background: #28a745; color: #fff; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px; }
        .btn-copy:active { background: #1e7e34; }
    </style>
</head>
<body>
    <h1>🎬 GTA 6 Mobile Reel Hub</h1>
    <p class="subtitle">Download 1080p Video + Copy Caption directly on Phone</p>
    <div id="cards">
"""

for it in items:
    safe_caption = it['caption'].replace('"', '&quot;').replace('\n', '\\n')
    HTML_TEMPLATE += f"""
        <div class="card">
            <div class="card-header">
                <span class="part-badge">Part {it['part']:02d}</span>
                <span class="time-badge">🕒 {it['time']}</span>
            </div>
            <a href="/video/{it['filename']}" download="{it['filename']}" class="btn-download">⬇️ Download Video (Part {it['part']:02d})</a>
            <div class="caption-box" id="cap_{it['part']}">{it['caption']}</div>
            <button class="btn-copy" onclick="copyCaption({it['part']})">📋 Copy Caption & Hashtags</button>
        </div>
    """

HTML_TEMPLATE += """
    </div>
    <script>
        function copyCaption(part) {
            var text = document.getElementById('cap_' + part).innerText;
            navigator.clipboard.writeText(text).then(function() {
                alert('Part ' + part + ' Caption copied to clipboard!');
            });
        }
    </script>
</body>
</html>
"""

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif self.path.startswith("/video/"):
            filename = self.path.replace("/video/", "")
            filepath = CLIPS_DIR / filename
            if filepath.exists():
                self.send_response(200)
                self.send_header("Content-type", "video/mp4")
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                self.send_header("Content-Length", str(filepath.stat().st_size))
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        else:
            super().do_GET()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), CustomHandler)
    print(f"[*] Mobile Hub Server running at http://0.0.0.0:{PORT}")
    server.serve_forever()
