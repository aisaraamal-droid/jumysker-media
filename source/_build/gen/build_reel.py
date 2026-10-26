# -*- coding: utf-8 -*-
"""Сборка рилса с ведущим: python3 build_reel.py r1 [r2 ...]
Нужно заранее: work/<id>-a|b|c.mp3/.json (tts_ts.py) и work/<id>-host-silent.mp4 (seedance.py, без звука).
Звук в ролике — только ElevenLabs."""
import json, math, os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reels_hosted import REELS_HOSTED, HOSTS, DISPLAY

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FPS = 30
LOGO = ('<svg viewBox="0 0 64 64"><g fill="{c}"><circle cx="17" cy="32" r="10"/><circle cx="32" cy="17" r="10"/>'
        '<circle cx="47" cy="32" r="10"/><circle cx="32" cy="47" r="10"/></g><circle cx="53" cy="53" r="4" fill="#13bd89"/></svg>')


def icon(name):
    s = open(os.path.join(HERE, "..", "icons", name + ".svg")).read()
    return re.sub(r"<!--.*?-->", "", s, flags=re.S).strip()


def run(*cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def duration(path):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path).stdout)


def speech_bounds(path):
    """Начало и конец речи в аудиодорожке (по silencedetect)."""
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    total = duration(path)
    first = ends[0] if starts and starts[0] < 0.05 and ends else 0.0
    last = starts[-1] if starts and (not ends or starts[-1] > ends[-1]) else total
    return first, last


def show_word(w):
    core = w.rstrip(".,!?:;—")
    tail = w[len(core):]
    for a, b in DISPLAY:
        if core == a or (core.startswith(a) and a.startswith("Ж") and not b.endswith("ді")):
            return b + core[len(a):] + tail
    return w


def nbsp(text):
    """Неразрывные пробелы: тире не уходит в начало строки, короткие предлоги не висят в конце."""
    text = text.replace(" — ", "\u00a0— ")
    return re.sub(r"(?<![\w-])([А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүІі]{1,2}) ", "\\1\u00a0", text)


def phrases(words, offset, limit=28):
    """Субтитры: режем по знакам препинания; длинное — по словам, но не оставляем «хвостик» в 1–2 слова."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        text = " ".join(show_word(x["w"]) for x in cur)
        rest = []
        for x in words[i + 1:]:
            rest.append(x["w"])
            if x["w"][-1] in ".!?:,—":
                break
        tail = " ".join(rest)
        nxt = words[i + 1]["w"] if i + 1 < len(words) else ""
        punct = w["w"][-1] in ".!?:" or (w["w"][-1] in ",—" and len(text) > 14)
        too_long = len(text + " " + nxt) > limit and not (len(tail) <= 14 and len(text) + 1 + len(tail) <= 42)
        if punct or too_long or not nxt:
            out.append({"s": round(offset + cur[0]["s"], 3), "e": None, "t": text})
            cur = []
    for i, p in enumerate(out):
        p["e"] = out[i + 1]["s"] if i + 1 < len(out) else None
    return out


def fit_lips(frames, box, audio, clip_fps):
    import numpy as np
    import lipalign as L
    ms = L.mouth_signal(frames, box)
    ms = np.convolve(ms, np.ones(3) / 3, mode="same")
    tclip = np.arange(len(ms)) / clip_fps
    env = L.envelope(audio)
    ts = np.arange(0, len(env) * L.HOP, 1 / clip_fps)
    e = np.interp(ts, np.arange(len(env)) * L.HOP, env)
    best = (-1.0, 1.0, 0.0)
    for sc in np.arange(0.8, 1.101, 0.02):
        for lag in np.arange(-0.3, 0.61, 0.04):
            src = lag + ts * sc
            ok = (src >= 0) & (src <= tclip[-1])
            if ok.mean() < 0.95:
                continue
            c = float(np.corrcoef(np.interp(src[ok], tclip, ms), e[ok])[0, 1])
            if c > best[0]:
                best = (c, float(sc), float(lag))
    return best[1], best[2], best[0]


def build(rid):
    spec = next(r for r in REELS_HOSTED if r["id"] == rid)
    host = HOSTS[spec["host"]]
    work = os.path.join(HERE, "work")
    out = os.path.join(work, rid)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(os.path.join(out, "host")); os.makedirs(os.path.join(out, "f"))
    W = {p: json.load(open(os.path.join(work, f"{rid}-{p}.json")))["words"] for p in "abc"}

    # A: клип ведущего (Seedance, только картинка) + чистый голос ElevenLabs.
    # Губы подгоняем: ищем масштаб времени и сдвиг, при которых движение рта лучше всего совпадает с речью.
    clip = os.path.join(work, f"{rid}-host-silent.mp4")
    a_mp3 = os.path.join(work, f"{rid}-a.mp3")
    raw = os.path.join(out, "raw"); os.makedirs(raw)
    run("ffmpeg", "-y", "-v", "error", "-i", clip, "-q:v", "2", os.path.join(raw, "%05d.jpg"))
    src_frames = sorted(os.listdir(raw))
    clip_fps = 24.0
    a_dur = duration(a_mp3) + 0.35
    scale, lag, corr = fit_lips([os.path.join(raw, f) for f in src_frames], host["mouth"], a_mp3, clip_fps)
    nA = int(round(a_dur * FPS))
    from PIL import Image
    for i in range(nA):
        t = i / FPS
        j = int(round((lag + scale * t) * clip_fps))
        j = min(max(j, 0), len(src_frames) - 1)
        Image.open(os.path.join(raw, src_frames[j])).resize((1080, 1920), Image.LANCZOS).save(
            os.path.join(out, "host", f"{i + 1:05d}.jpg"), quality=93)
    a_dur = nA / FPS
    subsA = phrases(W["a"], 0.0)
    subsA[-1]["e"] = a_dur
    print(f"губы: масштаб {scale:.2f}, сдвиг {lag:+.2f} с, корреляция {corr:.2f}")

    # B + C: демо под закадровый голос, затем финальная карточка
    b_off = 0.3
    b_dur = duration(os.path.join(work, f"{rid}-b.mp3"))
    c_off = b_off + b_dur + 0.45
    c_dur = duration(os.path.join(work, f"{rid}-c.mp3"))
    starts = (spec["anchor"],) if spec.get("anchor") else ("Помощник", "Көмекші")
    anchor = next(w for w in W["b"] if w["w"].strip("«»,.:—").startswith(starts))
    reply = b_off + anchor["s"]
    tl = {"typeStart": 0.35, "send": max(2.0, reply - 1.3), "reply": reply, "doc": reply + 0.9, "end": c_off - 0.15}
    subs = phrases(W["b"], b_off) + phrases(W["c"], c_off)
    total_b = c_off + c_dur + 0.8
    for i, p in enumerate(subs):
        if p["e"] is None:
            p["e"] = (subs[i + 1]["s"] if i + 1 < len(subs) else total_b)
    # между репликами B и C субтитр не висит дольше конца фразы
    tl["subs"] = subs
    tl["subsA"] = subsA
    nB = math.ceil(total_b * FPS)

    d = spec["demo"]; e = spec["end"]
    hook = spec["hook"]
    hook_host = hook.replace("<br>", " ") if len(hook) < 30 else hook
    rep = {
        "__LOGO__": LOGO.format(c="#2463ff"), "__LOGOW__": LOGO.format(c="#ffffff"),
        "__PORTRAIT__": "file://" + os.path.join(ROOT, "avatar", host["portrait"]),
        "__HOSTNAME__": host["name"], "__HOSTROLE__": "ведущий" if host["lang"] == "ru" else "жүргізуші",
        "__HOOK__": hook, "__HOOKHOST__": hook, "__ICON__": icon(d["icon"]), "__WHO__": d["who"], "__STATUS__": d["status"],
        "__SAMPLE__": d["sample"], "__M0__": nbsp(d["msgs"][0][1]), "__M1__": nbsp(d["msgs"][1][1]), "__TYPING__": d["typing"],
        "__DOCICON__": icon("file-text"), "__DOCT__": d["doc"][0], "__DOCS__": d["doc"][1], "__DOCOK__": d["doc"][2],
        "__INPUT__": d["input"], "__SENDICON__": icon("send"),
        "__ENDT__": nbsp(e["title"]), "__ENDS__": nbsp(e["sub"]), "__ENDB__": e["button"], "__ENDSM__": e["small"],
        "__TIMELINE__": json.dumps(tl, ensure_ascii=False),
    }
    html = open(os.path.join(HERE, "demo_template.html")).read()
    for k, v in rep.items():
        html = html.replace(k, v)
    page = os.path.join(out, "page.html")
    open(page, "w").write(html)
    print(run("node", os.path.join(HERE, "frames.js"), page, out, str(FPS), str(nA), str(nB)).stdout.strip())

    # звук: только ElevenLabs — A, затем B и C со сдвигами (звук Seedance не используется)
    total = (nA + nB) / FPS
    audio = os.path.join(out, "audio.m4a")
    run("ffmpeg", "-y", "-v", "error", "-i", a_mp3, "-i", os.path.join(work, f"{rid}-b.mp3"), "-i", os.path.join(work, f"{rid}-c.mp3"),
        "-filter_complex",
        f"[0:a]atrim=0:{a_dur:.3f},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo[a];"
        f"[1:a]adelay={int((a_dur + b_off) * 1000)}|{int((a_dur + b_off) * 1000)},aresample=44100,aformat=channel_layouts=stereo[b];"
        f"[2:a]adelay={int((a_dur + c_off) * 1000)}|{int((a_dur + c_off) * 1000)},aresample=44100,aformat=channel_layouts=stereo[c];"
        f"[a][b][c]amix=inputs=3:duration=longest:normalize=0,apad,atrim=0:{total:.3f},loudnorm=I=-14:TP=-1.5:LRA=11[o]",
        "-map", "[o]", "-c:a", "aac", "-b:a", "192k", audio)
    dest = os.path.join(ROOT, "reels"); os.makedirs(dest, exist_ok=True)
    mp4 = os.path.join(dest, f"{rid}-{spec['host']}.mp4")
    run("ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", os.path.join(out, "f", "%05d.jpg"), "-i", audio,
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
        "-c:a", "copy", "-shortest", mp4)
    # обложка: кадр ведущего с заголовком (0,6 с)
    shutil.copy(os.path.join(out, "f", f"{int(0.6 * FPS):05d}.jpg"), os.path.join(dest, f"{rid}-{spec['host']}-cover.jpg"))
    print("ok", mp4, f"{total:.1f}s", "A", f"{a_dur:.2f}")


if __name__ == "__main__":
    for rid in sys.argv[1:]:
        build(rid)
