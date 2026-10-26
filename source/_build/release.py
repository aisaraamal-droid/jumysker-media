# -*- coding: utf-8 -*-
"""Выпустить готовый рилс в план: python3 release.py r3
После gen/build_reel.py r3: копирует ролик, обложку и сторис-анонс в content/ репозитория
и ставит "ready": true в content/schedule.json. Коммит и push — отдельно (git)."""
import json, os, shutil, subprocess, sys

from build import ROOT, HERE
from content import REELS

REPO = os.path.dirname(ROOT)                       # source/ лежит в корне репозитория jumysker-media
CONTENT = os.path.join(REPO, "content")


def main(rid):
    r = next(x for x in REELS if x["id"] == rid)
    host = "erlan" if r["host"] == "Ерлан" else "dana"
    video = os.path.join(ROOT, "reels", f"{rid}-{host}.mp4")
    cover = os.path.join(ROOT, "reels", f"{rid}-{host}-cover.jpg")
    if not os.path.exists(video):
        sys.exit(f"Нет {video}: сначала python3 gen/build_reel.py {rid}")
    subprocess.run([sys.executable, os.path.join(HERE, "stories_auto.py")], check=True)
    os.makedirs(os.path.join(CONTENT, "reels"), exist_ok=True)
    shutil.copy(video, os.path.join(CONTENT, "reels"))
    shutil.copy(cover, os.path.join(CONTENT, "reels"))
    shutil.copy(os.path.join(ROOT, "stories", "auto", f"{rid}-story.mp4"), os.path.join(CONTENT, "stories", f"{rid}-story.mp4"))
    path = os.path.join(CONTENT, "schedule.json")
    plan = json.load(open(path))
    for it in plan:
        if it["id"] == rid:
            it["ready"] = True
    json.dump(plan, open(path, "w"), ensure_ascii=False, indent=1)
    print(f"{rid} в плане: content/reels/{rid}-{host}.mp4, сторис content/stories/{rid}-story.mp4")


if __name__ == "__main__":
    main(sys.argv[1])
