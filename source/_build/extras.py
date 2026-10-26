# -*- coding: utf-8 -*-
"""Аватар профиля, обложки хайлайтов, шаблоны сторис и тексты подписей.
python3 extras.py && node render_extras.js"""
import json, os

from build import CSS, LOGO, icon, art, ty, ROOT, HERE
from content import POSTS, REELS

PORTRAIT = {"Ерлан": "file://" + os.path.join(ROOT, "avatar", "erlan-v1.png"),
            "Дана": "file://" + os.path.join(ROOT, "avatar", "dana-v1.png")}

X = """
.x { position: relative; overflow: hidden; margin-bottom: 30px; font-family: Inter; color: var(--ink); }
.av { width: 1080px; height: 1080px; display: grid; place-items: center;
  background: radial-gradient(700px 600px at 30% 20%, #ffffff 0%, #eef4ff 60%, #dfeaff 100%); }
.av .logo { width: 560px; height: 560px; }
.hl { width: 1080px; height: 1920px; display: grid; place-items: center; background: linear-gradient(165deg, #1a6dff, #064ddd); }
.hl .in { width: 760px; height: 760px; border-radius: 50%; display: grid; place-items: center; color: #fff; background: rgba(255,255,255,.12); }
.hl .in svg { width: 330px; height: 330px; stroke-width: 1.6; }
.hl .face { width: 760px; height: 760px; border-radius: 50%; overflow: hidden; border: 18px solid rgba(255,255,255,.9); }
.hl .face img, .st .face img, .pill .pic img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 32%; transform: scale(1.6); }
.st { width: 1080px; height: 1920px; padding: 230px 80px 0;
  background: radial-gradient(900px 800px at 90% 5%, #dfeaff 0%, rgba(223,234,255,0) 60%), radial-gradient(800px 700px at 0% 100%, #e3f9f0 0%, rgba(227,249,240,0) 60%), #f6f9ff; }
.st .brand { position: absolute; top: 110px; left: 80px; }
.pill { position: absolute; top: 96px; right: 80px; display: flex; align-items: center; gap: 16px; background: #fff; border: 2px solid var(--border);
  border-radius: 999px; padding: 8px 26px 8px 8px; box-shadow: 0 14px 40px rgba(16,23,53,.08); }
.pill .pic { width: 76px; height: 76px; border-radius: 50%; overflow: hidden; background: #dfeaff; }
.pill b { font: 700 30px Inter; display: block; } .pill small { font: 500 22px Inter; color: var(--muted); }
.st h1 { font-size: 96px; margin-top: 70px; }
.st .lead { font-size: 42px; }
.st .hint { position: absolute; left: 80px; right: 80px; bottom: 360px; text-align: center; font: 600 34px Inter; color: var(--muted); }
.st .chat { margin-top: 50px; }
.st .chat .msg { font-size: 36px; }
.st.blue { background: linear-gradient(165deg, #1a6dff 0%, #0860ff 35%, #064ddd 75%, #0a3fb8 100%); color: #fff; text-align: center; padding-top: 300px; }
.st.blue .brand { color: #fff; }
.st.blue .face { width: 460px; height: 460px; margin: 0 auto 60px; border-radius: 50%; overflow: hidden; border: 12px solid rgba(255,255,255,.9); box-shadow: 0 40px 80px rgba(0,20,80,.35); }
.st.blue h1 { font-size: 104px; margin-top: 0; }
.st.blue .lead { color: rgba(255,255,255,.9); margin-top: 34px; }
.st.blue .btn { display: inline-block; margin-top: 60px; background: #fff; color: var(--blue); font: 800 62px Inter; padding: 34px 70px; border-radius: 999px; }
.st.blue .hint { color: rgba(255,255,255,.85); bottom: 330px; }
"""


def chat(who, ic, status, msgs, sample):
    m = "".join(f'<div class="msg {w}">{ty(t)}</div>' for w, t in msgs)
    return (f'<div class="card chat"><div class="head"><div class="ic">{icon(ic)}</div><div><b>{who}</b><small>{status}</small></div>'
            f'<span class="smp">{sample}</span></div>{m}</div>')


def pill(host, role):
    return f'<div class="pill"><div class="pic"><img src="{PORTRAIT[host]}"></div><div><b>{host}</b><small>{role}</small></div></div>'


def main():
    os.makedirs(os.path.join(HERE, "html"), exist_ok=True)
    items = []  # (id, out_path, html)
    prof = os.path.join(ROOT, "profile")
    os.makedirs(os.path.join(prof, "highlights"), exist_ok=True)
    stories = os.path.join(ROOT, "stories"); os.makedirs(stories, exist_ok=True)
    items.append(("avatar", os.path.join(prof, "avatar-1080.jpg"), f'<div class="x av">{LOGO.format(c="#2463ff")}</div>'))
    for n, (name, ic) in enumerate([("start", "rocket"), ("pomoshniki", "users"), ("tarify", "wallet"),
                                    ("erlan", "Ерлан"), ("dana", "Дана"), ("faq", "message-circle")], 1):
        inner = (f'<div class="face"><img src="{PORTRAIT[ic]}"></div>' if ic in PORTRAIT else f'<div class="in">{icon(ic)}</div>')
        items.append((f"hl{n}", os.path.join(prof, "highlights", f"{n}-{name}.jpg"), f'<div class="x hl">{inner}</div>'))
    brand = f'<div class="brand">{LOGO.format(c="#2463ff")}<span>jumysker</span></div>'
    brand_w = f'<div class="brand">{LOGO.format(c="#ffffff")}<span>jumysker</span></div>'
    items.append(("s1", os.path.join(stories, "s1-opros-ru.jpg"),
                  f'<div class="x st">{brand}{pill("Ерлан", "ведущий")}<div class="kicker">Опрос</div>'
                  f'<h1>{ty("Какая задача отнимает у вас <em>больше всего</em> времени?")}</h1>'
                  f'<div class="hint">Добавьте стикер «Опрос»: Документы · Клиенты · Соцсети · Отчёты</div></div>'))
    items.append(("s2", os.path.join(stories, "s2-zadacha-dnya-kz.jpg"),
                  f'<div class="x st">{brand}{pill("Дана", "жүргізуші")}<div class="kicker">Күн тапсырмасы</div>'
                  f'<h1 style="font-size:84px">{ty("Прайсты <em>қазақшаға</em> аудару")}</h1>'
                  + chat("Аудармашы", "languages", "ЖИ көмекшісі · онлайн",
                         [("u", "Переведи на казахский: «Маникюр с покрытием — 8 000 ₸. Наращивание ресниц — 12 000 ₸»."),
                          ("b", "Жабынмен маникюр — 8 000 ₸.\nКірпік ұзарту — 12 000 ₸.")], "мысал")
                  + '<div class="hint">Сілтеме стикерін осында қойыңыз ↓</div></div>'))
    for code, host, title, lead, hint in [
        ("ru", "Ерлан", "Попробуйте 7&nbsp;дней бесплатно", "До 3 помощников · без банковской карты", "Добавьте стикер-ссылку на jumysker.com ↓"),
        ("kz", "Дана", "7&nbsp;күн тегін байқап көріңіз", "3 көмекшіге дейін · банк картасынсыз", "jumysker.com сілтеме стикерін қосыңыз ↓")]:
        items.append((f"s3{code}", os.path.join(stories, f"s3-cta-{code}.jpg"),
                      f'<div class="x st blue">{brand_w}<div class="face"><img src="{PORTRAIT[host]}"></div>'
                      f'<h1>{ty(title)}</h1><p class="lead">{ty(lead)}</p><div class="btn">jumysker.com</div><div class="hint">{hint}</div></div>'))
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{X}</style></head><body>' + "".join(
        h.replace('class="x', f'id="{i}" class="x', 1) for i, _, h in items) + "</body></html>"
    open(os.path.join(HERE, "html", "extras.html"), "w").write(page)
    json.dump([[i, p] for i, p, _ in items], open(os.path.join(HERE, "extras.json"), "w"), ensure_ascii=False)

    # подписи: готовый текст для вставки в Instagram
    for p in POSTS:
        txt = f'{p["caption"]}\n\n🇰🇿 {p["caption_kz"]}\n\n{p["tags"]}\n'
        open(os.path.join(ROOT, "posts", p["id"], "caption.txt"), "w").write(txt)
    os.makedirs(os.path.join(ROOT, "reels"), exist_ok=True)
    for r in REELS:
        txt = f'{r["caption"]}\n\n{r["caption_alt"]}\n\n{r["tags"]}\n'
        open(os.path.join(ROOT, "reels", f'{r["id"]}-caption.txt'), "w").write(txt)
    print(len(items), "extras;", len(POSTS), "post captions;", len(REELS), "reel captions")


if __name__ == "__main__":
    main()
