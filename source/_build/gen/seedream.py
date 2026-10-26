"""Seedream 5.0 flash через BytePlus ModelArk (ключ подставляет прокси окружения).
python3 seedream.py OUT.png "prompt" [9:16|16:9|1:1] [reference.png ...]"""
import base64, json, sys, urllib.request, mimetypes
SIZES = {"9:16": "1440x2560", "16:9": "2560x1440", "1:1": "2048x2048", "4:5": "1728x2160"}
out, prompt = sys.argv[1], sys.argv[2]
ratio = sys.argv[3] if len(sys.argv) > 3 else "9:16"
refs = sys.argv[4:]
body = {"model": "dola-seedream-5-0-flash-260915", "prompt": prompt, "size": SIZES[ratio],
        "response_format": "b64_json", "watermark": False}
if refs:
    imgs = []
    for r in refs:
        mt = mimetypes.guess_type(r)[0] or "image/png"
        imgs.append(f"data:{mt};base64," + base64.b64encode(open(r, "rb").read()).decode())
    body["image"] = imgs[0] if len(imgs) == 1 else imgs
    body["sequential_image_generation"] = "disabled"
req = urllib.request.Request("https://ark.ap-southeast.bytepluses.com/api/v3/images/generations",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
try:
    data = json.load(urllib.request.urlopen(req, timeout=180))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read()[:600].decode(errors="ignore")); sys.exit(1)
open(out, "wb").write(base64.b64decode(data["data"][0]["b64_json"]))
print("ok", out, data.get("usage"))
