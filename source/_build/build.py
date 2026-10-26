# -*- coding: utf-8 -*-
"""Карусели Instagram Jumysker: content.py -> HTML -> JPEG 1080x1350 (через render.js).
python3 build.py && node render.js"""
import html, json, os, re

from content import POSTS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_HTML = os.path.join(HERE, "html")
LOGO = ('<svg class="logo" viewBox="0 0 64 64"><g fill="{c}"><circle cx="17" cy="32" r="10"/><circle cx="32" cy="17" r="10"/>'
        '<circle cx="47" cy="32" r="10"/><circle cx="32" cy="47" r="10"/></g><circle cx="53" cy="53" r="4" fill="#13bd89"/></svg>')


def icon(name):
    s = open(os.path.join(HERE, "icons", name + ".svg")).read()
    return re.sub(r"<!--.*?-->", "", s, flags=re.S).strip()


def art(name):
    return "file://" + os.path.join(HERE, "art", name)


def ty(text):
    """Типографика: неразрывный пробел после коротких слов и перед тире; HTML-теги (<em>, <br>, <s>) сохраняются."""
    text = text.replace(" — ", "\u00a0— ")
    text = re.sub(r"(?<![\w-])([А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүІі]{1,2}) ", "\\1\u00a0", text)
    text = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", text)          # 7 700
    text = re.sub(r"(\d) (₸|%|м²|кг)", "\\1\u00a0\\2", text)
    text = re.sub(r"(?<!\d)(\d+) ([А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүІі])", "\\1\u00a0\\2", text)   # 3 минуты
    text = text.replace("≈ ", "≈\u00a0").replace("~", "~")
    text = re.sub(r"\b(AI|ИИ|ЖИ)-", "\\1\u2011", text)                                   # AI‑сотрудник
    return text


CSS = """
:root { --ink:#101735; --muted:#5d6788; --blue:#0860ff; --blue-deep:#064ddd; --green:#0abe84; --border:#deebfa; --soft:#eef4ff; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #ccd; font-family: Inter, sans-serif; color: var(--ink); -webkit-font-smoothing: antialiased; }
.slide { width: 1080px; height: 1350px; position: relative; overflow: hidden; display: flex; flex-direction: column; padding: 70px 80px 64px;
  background: radial-gradient(900px 700px at 92% 4%, #dde9ff 0%, rgba(221,233,255,0) 62%),
              radial-gradient(760px 640px at -6% 104%, #dff7ee 0%, rgba(223,247,238,0) 60%), #f8fbff; margin-bottom: 40px; }
.top { display: flex; justify-content: space-between; align-items: center; height: 60px; flex: none; position: relative; z-index: 3; }
.brand { display: flex; align-items: center; gap: 14px; font: 800 36px Inter; letter-spacing: -0.02em; }
.logo { width: 50px; height: 50px; }
.count { font: 700 26px Inter; color: var(--muted); background: rgba(255,255,255,.85); border: 2px solid var(--border); border-radius: 999px; padding: 8px 20px; }
.body { flex: 1; display: flex; flex-direction: column; justify-content: center; position: relative; z-index: 2; min-height: 0; }
.bottom { display: flex; justify-content: space-between; align-items: center; height: 56px; flex: none; position: relative; z-index: 3; }
.url { font: 600 28px Inter; color: var(--muted); }
.swipe { font: 700 28px Inter; color: var(--blue); display: flex; align-items: center; gap: 10px; }
.swipe svg { width: 34px; height: 34px; }
.kicker { align-self: flex-start; font: 700 28px Inter; color: var(--blue); background: #e4eeff; border-radius: 999px; padding: 10px 24px; margin-bottom: 30px; }
h1 { font: 800 92px/1.02 'Inter Display', Inter; letter-spacing: -0.035em; }
h2 { font: 800 66px/1.06 'Inter Display', Inter; letter-spacing: -0.03em; margin-bottom: 40px; }
h1 em, h2 em { font-style: normal; color: var(--blue); }
.lead { font: 500 38px/1.4 Inter; color: var(--muted); margin-top: 30px; }
.chips { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 36px; }
.chip { font: 600 30px Inter; background: #fff; border: 2px solid var(--border); border-radius: 999px; padding: 14px 26px; }
.card { background: #fff; border: 2px solid var(--border); border-radius: 36px; box-shadow: 0 20px 60px rgba(16,23,53,.06); }
.ic { width: 76px; height: 76px; border-radius: 24px; background: linear-gradient(150deg, #2f7bff, #064ddd); color: #fff; display: grid; place-items: center; flex: none; }
.ic svg { width: 40px; height: 40px; }
/* обложка */
.cover .body { justify-content: flex-start; padding-top: 60px; }
.cover h1 { max-width: 920px; }
.cover .lead { max-width: 820px; }
.cover .art { position: absolute; right: -40px; bottom: 130px; width: 580px; z-index: 1; }
.cover .art.big { width: 740px; right: -70px; bottom: 110px; }
.cover .art.knot { mix-blend-mode: multiply; width: 640px; -webkit-mask-image: radial-gradient(closest-side, #000 70%, transparent 100%); }
/* текст + чат */
.chat { padding: 30px 32px; display: flex; flex-direction: column; gap: 18px; margin-top: 10px; }
.chat .head { display: flex; align-items: center; gap: 18px; padding-bottom: 18px; border-bottom: 2px solid #eef3fb; }
.chat .head .ic { width: 64px; height: 64px; border-radius: 20px; }
.chat .head .ic svg { width: 34px; height: 34px; }
.chat .head b { font: 800 32px Inter; display: block; }
.chat .head small { font: 500 24px Inter; color: var(--green); }
.chat .head .smp { margin-left: auto; font: 600 22px Inter; color: var(--muted); background: #f1f5fc; border-radius: 999px; padding: 6px 16px; }
.msg { max-width: 86%; font: 500 32px/1.38 Inter; padding: 22px 28px; border-radius: 30px; }
.msg.u { align-self: flex-end; background: var(--blue); color: #fff; border-bottom-right-radius: 10px; }
.msg.b { align-self: flex-start; background: #f2f6fd; border: 2px solid #e3ebf8; border-bottom-left-radius: 10px; }
.doc { align-self: flex-start; display: flex; align-items: center; gap: 18px; border: 2px solid var(--border); border-radius: 26px; padding: 18px 22px; width: 86%; }
.doc .ic { width: 62px; height: 62px; border-radius: 18px; background: #e8f0ff; color: var(--blue); }
.doc .ic svg { width: 32px; height: 32px; }
.doc b { font: 700 28px Inter; display: block; }
.doc small { font: 500 24px Inter; color: var(--muted); }
.doc .ok { margin-left: auto; background: #e2f8ef; color: #07936a; font: 700 22px Inter; padding: 8px 16px; border-radius: 999px; }
.textbody { font: 500 36px/1.42 Inter; color: var(--muted); margin: -16px 0 34px; }
/* сетка карточек */
.grid { display: grid; gap: 22px; }
.grid.c1 .card { display: flex; gap: 28px; align-items: center; padding: 34px 36px; }
.grid.c1 b { font: 800 40px/1.15 Inter; display: block; margin-bottom: 8px; }
.grid.c1 span { font: 500 32px/1.35 Inter; color: var(--muted); }
.grid.c2 { grid-template-columns: 1fr 1fr; }
.grid.c2 .card { padding: 30px 30px 32px; }
.grid.c2 .ic { width: 68px; height: 68px; border-radius: 20px; margin-bottom: 22px; }
.grid.c2 .ic svg { width: 36px; height: 36px; }
.grid.c2 b { font: 800 36px/1.15 Inter; display: block; margin-bottom: 6px; }
.grid.c2 span { font: 500 28px/1.3 Inter; color: var(--muted); }
.grid.c2.many { gap: 16px; }
.grid.c2.many .card { padding: 22px 24px; display: flex; gap: 18px; align-items: center; }
.grid.c2.many .ic { width: 58px; height: 58px; border-radius: 18px; margin: 0; }
.grid.c2.many .ic svg { width: 30px; height: 30px; }
.grid.c2.many b { font-size: 31px; margin-bottom: 4px; }
.grid.c2.many span { font-size: 25px; }
.prices.many { gap: 16px; }
.prices.many .price { padding: 24px 32px; }
.prices.many .amt { font-size: 50px; }
.prices.one .price { padding: 50px 46px; }
.prices.one .amt { font-size: 72px; }
.prices.one .who { font-size: 34px; }
/* шаги */
.steps { display: flex; flex-direction: column; gap: 22px; }
.step { display: flex; gap: 30px; align-items: center; padding: 34px 36px; }
.num { width: 84px; height: 84px; border-radius: 50%; background: var(--blue); color: #fff; font: 800 42px Inter; display: grid; place-items: center; flex: none; }
.step b { font: 800 40px/1.15 Inter; display: block; margin-bottom: 8px; }
.step span { font: 500 31px/1.35 Inter; color: var(--muted); }
/* большой шаг */
.bigstep .body { justify-content: center; }
.bignum { font: 800 300px/0.9 'Inter Display', Inter; color: var(--blue); letter-spacing: -0.06em; margin-bottom: 20px; }
.bigstep h2 { font-size: 78px; margin-bottom: 30px; }
.bigstep .lead { margin-top: 0; font-size: 40px; }
.bigstep .bgicon { position: absolute; right: 70px; top: 200px; width: 300px; height: 300px; color: #dce8ff; z-index: 1; }
.bigstep .bgicon svg { width: 100%; height: 100%; stroke-width: 1.4; }
/* список */
.list { display: flex; flex-direction: column; gap: 20px; }
.li { display: flex; gap: 28px; align-items: flex-start; padding: 30px 34px; }
.li .mark { width: 64px; height: 64px; border-radius: 50%; background: #e2f8ef; color: #07936a; display: grid; place-items: center; flex: none; font: 800 32px Inter; }
.li .mark svg { width: 36px; height: 36px; stroke-width: 3; }
.li .mark.n { background: #e4eeff; color: var(--blue); }
.li .mark.x { background: #ffe9e6; color: #e2402e; }
.li b { font: 800 38px/1.18 Inter; display: block; margin-bottom: 8px; }
.li span { font: 500 30px/1.36 Inter; color: var(--muted); display: block; }
/* цитаты */
.quote { padding: 32px 36px; border-left: 10px solid var(--blue); border-radius: 20px 36px 36px 20px; }
.quote b { font: 800 40px/1.2 Inter; display: block; margin-bottom: 10px; }
.quote span { font: 500 30px/1.36 Inter; color: var(--muted); }
/* утверждение */
.statement .body { justify-content: center; }
.bigic { width: 132px; height: 132px; border-radius: 40px; background: linear-gradient(150deg, #2f7bff, #064ddd); color: #fff; display: grid; place-items: center; margin-bottom: 44px; box-shadow: 0 30px 60px rgba(8,96,255,.28); }
.bigic svg { width: 70px; height: 70px; }
.statement h2 { font-size: 84px; line-height: 1.04; }
.statement .lead { font-size: 40px; margin-top: 0; max-width: 880px; }
/* цены */
.prices { display: flex; flex-direction: column; gap: 20px; }
.price { padding: 30px 36px; display: grid; grid-template-columns: 1fr auto; gap: 6px 24px; align-items: baseline; }
.price .tag { font: 700 26px Inter; color: var(--blue); }
.price .amt { font: 800 54px Inter; letter-spacing: -0.02em; grid-row: span 2; align-self: center; white-space: nowrap; }
.price .who { font: 600 32px/1.3 Inter; }
.price .lim { font: 500 26px Inter; color: var(--muted); grid-column: 1 / -1; }
.price.hl { background: linear-gradient(150deg, #1a6dff, #064ddd); border-color: transparent; color: #fff; box-shadow: 0 30px 70px rgba(8,96,255,.3); }
.price.hl .tag, .price.hl .lim { color: rgba(255,255,255,.85); }
.price s { opacity: .7; }
.prices.few .price { padding: 40px 40px; }
.prices.few .amt { font-size: 64px; }
/* прайс-лист */
.plist { padding: 12px 40px; }
.prow { display: flex; justify-content: space-between; align-items: center; gap: 30px; padding: 28px 0; border-bottom: 2px dashed #e3ebf8; font: 500 33px/1.3 Inter; }
.prow:last-child { border-bottom: 0; }
.prow b { font: 800 36px Inter; white-space: nowrap; color: var(--ink); }
.prow b.free { color: #07936a; }
.psub { font: 600 32px Inter; color: var(--muted); margin: -24px 0 30px; }
/* сравнение */
.cmp { display: flex; flex-direction: column; gap: 22px; }
.cmp .card { padding: 32px 36px; }
.cmp .lab { display: inline-flex; align-items: center; gap: 10px; font: 800 28px Inter; border-radius: 999px; padding: 8px 20px 8px 12px; margin-bottom: 18px; }
.cmp .lab svg { width: 32px; height: 32px; stroke-width: 2.6; }
.cmp .bad .lab { background: #ffe9e6; color: #e2402e; }
.cmp .good .lab { background: #e2f8ef; color: #07936a; }
.cmp .bad p { font: 600 40px/1.3 Inter; color: var(--muted); }
.cmp .good p { font: 500 32px/1.42 Inter; }
.cmp .good { border-color: #bfe9d6; }
/* вакансия */
.vac { padding: 36px 40px; }
.vac .meta { font: 600 30px Inter; color: var(--blue); margin-bottom: 18px; }
.vac .row { padding: 18px 0; border-top: 2px solid #eef3fb; }
.vac .row b { font: 800 28px Inter; color: var(--muted); display: block; margin-bottom: 6px; text-transform: uppercase; letter-spacing: .04em; }
.vac .row span { font: 500 32px/1.38 Inter; }
/* расчёт */
.math .card { padding: 34px 40px; }
.mrow { display: flex; justify-content: space-between; align-items: baseline; gap: 20px; font: 500 34px Inter; padding: 18px 0; }
.mrow b { font: 800 44px Inter; white-space: nowrap; }
.mres { margin-top: 26px; padding: 34px 40px; border-radius: 36px; background: linear-gradient(150deg, #1a6dff, #064ddd); color: #fff; font: 700 40px/1.3 Inter; box-shadow: 0 30px 70px rgba(8,96,255,.3); }
/* CTA */
.cta { background: linear-gradient(165deg, #1a6dff 0%, #0860ff 35%, #064ddd 75%, #0a3fb8 100%); color: #fff; }
.cta .brand { color: #fff; }
.cta .count { background: rgba(255,255,255,.15); color: #fff; border-color: rgba(255,255,255,.3); }
.cta .ring { position: absolute; border-radius: 50%; background: rgba(255,255,255,.07); z-index: 1; }
.cta h2 { font-size: 100px; line-height: 1.0; margin-bottom: 50px; }
.cta ul { list-style: none; display: flex; flex-direction: column; gap: 22px; margin-bottom: 64px; }
.cta li { display: flex; align-items: center; gap: 20px; font: 600 40px Inter; }
.cta li i { width: 54px; height: 54px; border-radius: 50%; background: rgba(255,255,255,.18); display: grid; place-items: center; flex: none; }
.cta li i svg { width: 32px; height: 32px; stroke-width: 3; }
.cta .btn { align-self: flex-start; background: #fff; color: var(--blue); font: 800 58px Inter; padding: 34px 64px; border-radius: 999px; box-shadow: 0 30px 60px rgba(0,20,80,.3); }
.cta .small { font: 600 34px Inter; opacity: .85; margin-top: 26px; }
.cta .url { color: rgba(255,255,255,.8); }
"""


def esc_keep(t):
    return ty(t)


def chat_html(c):
    out = [f'<div class="card chat"><div class="head"><div class="ic">{icon(c["icon"])}</div><div><b>{c["who"]}</b>'
           f'<small>ИИ-помощник · онлайн</small></div><span class="smp">пример</span></div>']
    for who, text in c["msgs"]:
        out.append(f'<div class="msg {who}">{ty(html.escape(text))}</div>')
    if c.get("doc"):
        out.append(f'<div class="doc card"><div class="ic">{icon("file-text")}</div><div><b>{ty(c["doc"][0])}</b>'
                   f'<small>{ty(c["doc"][1])}</small></div><span class="ok">Готово</span></div>')
    out.append("</div>")
    return "".join(out)


def slide_html(s, i, n):
    t = s["type"]
    cls = {"cover": "cover", "bigstep": "bigstep", "statement": "statement", "cta": "cta", "math": "math"}.get(t, "")
    logo = LOGO.format(c="#ffffff" if t == "cta" else "#2463ff")
    top = f'<div class="top"><div class="brand">{logo}<span>jumysker</span></div><div class="count">{i}/{n}</div></div>'
    last = i == n
    bottom = ('<div class="bottom"><span class="url">jumysker.com</span>'
              + ('' if last else f'<span class="swipe">Листайте {icon("arrow-right")}</span>') + '</div>')
    k = f'<div class="kicker">{ty(s["kicker"])}</div>' if s.get("kicker") else ""
    extra = ""
    if t == "cover":
        a = s.get("art", "")
        acls = "art" + (" big" if s.get("art_big") else "") + (" knot" if a == "knot.png" else "")
        extra = f'<img class="{acls}" src="{art(a)}">' if a else ""
        chips = "".join(f'<span class="chip">{ty(c)}</span>' for c in s.get("chips", []))
        body = f'{k}<h1>{ty(s["title"])}</h1><p class="lead">{ty(s["sub"])}</p><div class="chips">{chips}</div>'
    elif t == "text":
        body = f'{k}<h2>{ty(s["title"])}</h2>' + (f'<p class="textbody">{ty(s["body"])}</p>' if s.get("body") else "") + chat_html(s["chat"])
    elif t == "grid":
        cols = s.get("cols", 1)
        cards = "".join(f'<div class="card"><div class="ic">{icon(ic)}</div><div><b>{ty(h)}</b><span>{ty(x)}</span></div></div>'
                        for ic, h, x in s["cards"])
        many = " many" if len(s["cards"]) > 6 else ""
        body = f'{k}<h2>{ty(s["title"])}</h2><div class="grid c{cols}{many}">{cards}</div>'
    elif t == "steps":
        items = "".join(f'<div class="card step"><div class="num">{j}</div><div><b>{ty(h)}</b><span>{ty(x)}</span></div></div>'
                        for j, (h, x) in enumerate(s["items"], 1))
        body = f'{k}<h2>{ty(s["title"])}</h2><div class="steps">{items}</div>'
    elif t == "bigstep":
        extra = f'<div class="bgicon">{icon(s["icon"])}</div>'
        body = f'<div class="kicker">Шаг {s["n"]}</div><div class="bignum">{s["n"]}</div><h2>{ty(s["title"])}</h2><p class="lead">{ty(s["body"])}</p>'
    elif t == "list":
        start = s.get("start", 1)
        rows = []
        for j, (h, x) in enumerate(s["items"]):
            if s.get("bad"):
                mark = f'<div class="mark x">{icon("circle-x")}</div>'
            elif s.get("numbered"):
                mark = f'<div class="mark n">{start + j}</div>'
            else:
                mark = f'<div class="mark">{icon("check")}</div>'
            rows.append(f'<div class="card li">{mark}<div><b>{ty(h)}</b><span>{ty(x)}</span></div></div>')
        body = f'{k}<h2>{ty(s["title"])}</h2><div class="list">{"".join(rows)}</div>'
    elif t == "quotes":
        rows = "".join(f'<div class="card quote"><b>{ty(h)}</b><span>{ty(x)}</span></div>' for h, x in s["items"])
        body = f'{k}<h2>{ty(s["title"])}</h2><div class="list">{rows}</div>'
    elif t == "statement":
        body = f'<div class="bigic">{icon(s["icon"])}</div>{k}<h2>{ty(s["title"])}</h2><p class="lead">{ty(s["body"])}</p>'
    elif t == "prices":
        few = {1: " few one", 2: " few"}.get(len(s["cards"]), " many" if len(s["cards"]) >= 4 else "")
        cards = "".join(f'<div class="card price{" hl" if hl else ""}"><div class="tag">{ty(tag)}</div><div class="amt">{ty(amt)}</div>'
                        f'<div class="who">{ty(who)}</div><div class="lim">{ty(lim)}</div></div>'
                        for tag, amt, who, lim, hl in s["cards"])
        body = f'{k}<h2>{ty(s["title"])}</h2><div class="prices{few}">{cards}</div>'
    elif t == "pricelist":
        rows = "".join(f'<div class="prow"><span>{ty(a)}</span><b class="{"free" if not any(ch.isdigit() for ch in b) else ""}">{ty(b)}</b></div>'
                       for a, b in s["rows"])
        body = f'{k}<h2>{ty(s["title"])}</h2><p class="psub">{ty(s["sub"])}</p><div class="card plist">{rows}</div>'
    elif t == "compare":
        body = (f'{k}<h2>{ty(s["title"])}</h2><div class="cmp">'
                f'<div class="card bad"><div class="lab">{icon("circle-x")}Было</div><p>«{ty(s["bad"])}»</p></div>'
                f'<div class="card good"><div class="lab">{icon("check")}Стало</div><p>«{ty(s["good"])}»</p></div></div>')
    elif t == "vacancy":
        rows = "".join(f'<div class="row"><b>{ty(h)}</b><span>{ty(x)}</span></div>' for h, x in s["blocks"])
        body = f'{k}<div class="card vac"><h2 style="font-size:54px;margin-bottom:12px">{ty(s["title"])}</h2><div class="meta">{ty(s["meta"])}</div>{rows}</div>'
    elif t == "math":
        rows = "".join(f'<div class="mrow"><span>{ty(a)}</span><b>{ty(b)}</b></div>' for a, b in s["lines"])
        body = f'{k}<h2>{ty(s["title"])}</h2><div class="card">{rows}</div><div class="mres">{ty(s["result"])}</div>'
    elif t == "cta":
        extra = ('<div class="ring" style="width:900px;height:900px;left:-320px;top:-300px"></div>'
                 '<div class="ring" style="width:760px;height:760px;right:-300px;bottom:-260px"></div>')
        lis = "".join(f'<li><i>{icon("check")}</i>{ty(b)}</li>' for b in s["bullets"])
        body = f'<h2>{ty(s["title"])}</h2><ul>{lis}</ul><div class="btn">{s["button"]}</div><div class="small">{ty(s["small"])}</div>'
    else:
        raise ValueError(t)
    return f'<div class="slide {cls}" data-i="{i}">{extra}{top}<div class="body">{body}</div>{bottom}</div>'


def main():
    os.makedirs(OUT_HTML, exist_ok=True)
    jobs = []
    for p in POSTS:
        n = len(p["slides"])
        slides = "".join(slide_html(s, i, n) for i, s in enumerate(p["slides"], 1))
        page = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{slides}</body></html>'
        path = os.path.join(OUT_HTML, p["id"] + ".html")
        open(path, "w").write(page)
        folder = os.path.join(ROOT, "posts", f'{p["id"]}')
        os.makedirs(folder, exist_ok=True)
        jobs.append({"html": path, "out": folder, "n": n})
    json.dump(jobs, open(os.path.join(HERE, "jobs.json"), "w"), indent=1)
    print(len(jobs), "posts,", sum(j["n"] for j in jobs), "slides")


if __name__ == "__main__":
    main()
