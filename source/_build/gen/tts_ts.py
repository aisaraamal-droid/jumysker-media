"""ElevenLabs TTS c таймингами символов (для субтитров). Голоса и настройки — как одобрено в reelio-bot.
python3 tts_ts.py OUT_BASENAME female|male "текст"  ->  OUT_BASENAME.mp3 + OUT_BASENAME.json (слова с временем)"""
import base64, json, sys, urllib.request

def voices():
    """ID голосов не храним в открытом репозитории: переменные JUMYSKER_VOICE_MALE / JUMYSKER_VOICE_FEMALE
    или настройки reelio-bot (reelio/config.py: elevenlabs_voice_male / elevenlabs_voice_female)."""
    import os, re
    found = {"male": os.environ.get("JUMYSKER_VOICE_MALE", ""), "female": os.environ.get("JUMYSKER_VOICE_FEMALE", "")}
    cfg = os.path.expanduser(os.environ.get("REELIO_CONFIG", "/home/user/reelio-bot/reelio/config.py"))
    if os.path.exists(cfg):
        text = open(cfg, encoding="utf-8").read()
        for who in ("male", "female"):
            m = re.search(rf'elevenlabs_voice_{who}: str = "([A-Za-z0-9]+)"', text)
            if m and not found[who]:
                found[who] = m.group(1)
    missing = [w for w, v in found.items() if not v]
    if missing:
        raise SystemExit("Нет ID голоса ElevenLabs: задайте JUMYSKER_VOICE_" + "/".join(w.upper() for w in missing)
                         + " или подключите репозиторий reelio-bot")
    return found



def tts(out, who, text):
    body = {"text": text, "model_id": "eleven_v3",
            "voice_settings": {"stability": 0.44, "similarity_boost": 0.70, "speed": 1.0}}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voices()[who]}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=180))
    open(out + ".mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    a = d["alignment"]
    words, cur, start, end = [], "", None, None
    for ch, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append({"w": cur, "s": start, "e": end})
            cur, start = "", None
            continue
        if start is None:
            start = s
        cur += ch
        end = e
    if cur:
        words.append({"w": cur, "s": start, "e": end})
    json.dump({"text": text, "words": words}, open(out + ".json", "w"), ensure_ascii=False, indent=1)
    return words


if __name__ == "__main__":
    w = tts(sys.argv[1], sys.argv[2], sys.argv[3])
    print("ok", sys.argv[1], len(w), "words, ends", w[-1]["e"])
