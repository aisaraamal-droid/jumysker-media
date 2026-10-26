# -*- coding: utf-8 -*-
"""Голос и клип ведущего для рилса: python3 make_host.py r3
1) ElevenLabs: части a, b, c -> work/<id>-a|b|c.mp3/.json (тайминги для субтитров);
2) Seedance 2.0 mini, только картинка (без звука): портрет ведущего + голос части a как ориентир для губ
   -> work/<id>-host-silent.mp4 (≈ $0,6). Дальше: python3 build_reel.py <id> && python3 ../release.py <id>"""
import math, os, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reels_hosted import REELS_HOSTED, HOSTS
from tts_ts import tts

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT = ("{subject} is a friendly presenter in a bright, airy studio with a soft white-to-light-blue background and a few "
          "floating translucent blue glass spheres. Medium close-up, static camera; looks straight into the camera and talks, "
          "lip movements exactly following the speech rhythm of reference audio 1 (mouth closed during its pauses), a warm "
          "confident smile and small natural hand gestures, like a friendly TV host. Keep the face, hair and royal-blue blazer "
          "exactly as in reference image 1. Stylized premium 3D animation look. No text, no subtitles, no logos.")
SUBJECT = {"erlan": "The man from reference image 1", "dana": "The woman from reference image 1"}


def main(rid):
    spec = next(r for r in REELS_HOSTED if r["id"] == rid)
    host = HOSTS[spec["host"]]
    work = os.path.join(HERE, "work")
    os.makedirs(work, exist_ok=True)
    for part in "abc":
        out = os.path.join(work, f"{rid}-{part}")
        if os.path.exists(out + ".json"):
            continue
        for attempt in range(4):
            try:
                w = tts(out, host["voice"], spec[part])
                print(f"голос {rid}-{part}: {w[-1]['e']:.1f} с")
                break
            except Exception as e:          # 429 при параллельных запросах — подождать и повторить
                if attempt == 3:
                    raise
                time.sleep(5 * (attempt + 1))
    clip = os.path.join(work, f"{rid}-host-silent.mp4")
    if os.path.exists(clip):
        return print("клип ведущего уже есть:", clip)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                os.path.join(work, f"{rid}-a.mp3")], capture_output=True, text=True).stdout)
    seconds = min(15, max(4, math.ceil(dur + 0.5)))
    portrait = os.path.join(HERE, "..", "..", "avatar", host["portrait"])
    subprocess.run([sys.executable, os.path.join(HERE, "seedance.py"), clip, "dreamina-seedance-2-0-mini-260615", str(seconds),
                    PROMPT.format(subject=SUBJECT[spec["host"]]), f"image:reference_image:{portrait}",
                    f"audio:reference_audio:{os.path.join(work, rid + '-a.mp3')}"], check=True)


if __name__ == "__main__":
    main(sys.argv[1])
