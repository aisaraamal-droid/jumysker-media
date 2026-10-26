"""Seedance через BytePlus ModelArk: отправка задачи, ожидание, скачивание MP4 (ключ подставляет прокси окружения).
Звук Seedance не используем: по умолчанию generate_audio=false, голос — только ElevenLabs.
python3 seedance.py OUT.mp4 MODEL DURATION "prompt" [image:role:path] [audio:role:path]"""
import base64, json, sys, time, urllib.request, mimetypes
API = "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks"
out, model, duration, prompt = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
content = [{"type": "text", "text": prompt}]
for spec in sys.argv[5:]:
    kind, role, path = spec.split(":", 2)
    mt = mimetypes.guess_type(path)[0] or ("audio/mpeg" if kind == "audio" else "image/png")
    url = f"data:{mt};base64," + base64.b64encode(open(path, "rb").read()).decode()
    content.append({"type": f"{kind}_url", f"{kind}_url": {"url": url}, "role": role})
body = {"model": model, "content": content, "resolution": "720p", "ratio": "9:16", "duration": duration,
        "generate_audio": __import__("os").environ.get("SEEDANCE_AUDIO", "0") == "1", "watermark": False}
def call(req):
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read()[:800].decode(errors="ignore")); sys.exit(1)
task = call(urllib.request.Request(API, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}))
tid = task["id"]; print("task", tid, flush=True)
while True:
    time.sleep(10)
    d = call(urllib.request.Request(f"{API}/{tid}"))
    if d.get("status") in ("succeeded", "failed", "cancelled", "expired"):
        break
print("status", d.get("status"), d.get("error"), d.get("usage"))
if d.get("status") == "succeeded":
    urllib.request.urlretrieve(d["content"]["video_url"], out); print("saved", out)
