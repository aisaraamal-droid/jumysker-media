# -*- coding: utf-8 -*-
"""Сторис-анонсы к каждой публикации: python3 stories_auto.py
Карусель -> JPEG 1080x1920 (первый слайд + плашка). Рилс -> первые 11 с ролика + плашки (MP4)."""
import json, os, subprocess

from build import CSS, LOGO, ROOT, HERE
from content import POSTS, REELS

OUT = os.path.join(ROOT, "stories", "auto")
X = """
body { background: transparent; }
.s { width: 1080px; height: 1920px; position: relative; overflow: hidden; margin-bottom: 20px;
  background: radial-gradient(900px 800px at 90% 5%, #dfeaff 0%, rgba(223,234,255,0) 60%), radial-gradient(800px 700px at 0% 100%, #e3f9f0 0%, rgba(227,249,240,0) 60%), #f6f9ff; }
.s.ov { background: transparent; }
.s .shot { position: absolute; left: 60px; top: 330px; width: 960px; height: 1200px; border-radius: 40px; overflow: hidden; box-shadow: 0 40px 100px rgba(16,23,53,.22); }
.s .shot img { width: 100%; height: 100%; display: block; }
.badge { position: absolute; left: 50%; transform: translateX(-50%); white-space: nowrap; font: 800 50px Inter; padding: 26px 48px; border-radius: 999px; }
.badge.new { top: 190px; background: var(--blue); color: #fff; box-shadow: 0 24px 60px rgba(8,96,255,.35); }
.badge.cta { top: 1590px; background: #fff; color: var(--ink); border: 3px solid var(--border); box-shadow: 0 20px 50px rgba(16,23,53,.14); font-size: 44px; }
.badge.cta b { color: var(--blue); }
.ov .badge.new { top: 1548px; font-size: 44px; padding: 22px 42px; }
.ov .badge.cta { top: 1670px; font-size: 40px; padding: 20px 40px; }
"""


def reel_path(r):
    host = "erlan" if r["host"] == "Ерлан" else "dana"
    return os.path.join(ROOT, "reels", f'{r["id"]}-{host}.mp4')


def main():
    os.makedirs(os.path.join(HERE, "html"), exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    blocks, jobs = [], []
    for p in POSTS:
        if not os.path.exists(os.path.join(ROOT, "posts", p["id"], "slide-01.jpg")):
            continue   # в репозитории карусели лежат в content/, их сторис уже готовы
        img = "file://" + os.path.join(ROOT, "posts", p["id"], "slide-01.jpg")
        blocks.append(f'<div class="s" id="{p["id"]}"><div class="shot"><img src="{img}"></div>'
                      f'<div class="badge new">Новый пост уже в профиле</div>'
                      f'<div class="badge cta">7 дней бесплатно · <b>jumysker.com</b></div></div>')
        jobs.append([p["id"], os.path.join(OUT, f'{p["id"]}-story.jpg'), False])
    for r in REELS:
        if not os.path.exists(reel_path(r)):
            continue
        kz = r["lang"] == "KZ"
        new = "Жаңа рилс профильде" if kz else "Новый рилс уже в профиле"
        cta = "7 күн тегін · <b>jumysker.com</b>" if kz else "7 дней бесплатно · <b>jumysker.com</b>"
        blocks.append(f'<div class="s ov" id="{r["id"]}"><div class="badge new">{new}</div><div class="badge cta">{cta}</div></div>')
        jobs.append([r["id"], os.path.join(HERE, "html", f'{r["id"]}-overlay.png'), True])
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{X}</style></head><body>{"".join(blocks)}</body></html>'
    open(os.path.join(HERE, "html", "stories_auto.html"), "w").write(page)
    json.dump(jobs, open(os.path.join(HERE, "stories_auto.json"), "w"))
    subprocess.run(["node", os.path.join(HERE, "render_stories.js")], check=True)
    # рилсы: первые 11 секунд + плашки
    for r in REELS:
        src = reel_path(r)
        if not os.path.exists(src):
            continue
        dst = os.path.join(OUT, f'{r["id"]}-story.mp4')
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-t", "11", "-i", src, "-i", os.path.join(HERE, "html", f'{r["id"]}-overlay.png'),
                        "-filter_complex", "[0:v][1:v]overlay=0:0,format=yuv420p[v]", "-map", "[v]", "-map", "0:a",
                        "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", dst], check=True)
    print("ok", len(jobs), "->", OUT)


if __name__ == "__main__":
    main()
