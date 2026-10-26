"""ElevenLabs TTS голосами, одобренными в reelio-bot (eleven_v3, stability 0.44, similarity 0.70, speed 1.0).
python3 tts.py OUT.mp3 female|male "текст" """
import json, sys, urllib.request
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

out, who, text = sys.argv[1], sys.argv[2], sys.argv[3]
body = {"text": text, "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.44, "similarity_boost": 0.70, "speed": 1.0}}
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voices()[who]}?output_format=mp3_44100_128",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "Accept": "audio/mpeg"})
try:
    open(out, "wb").write(urllib.request.urlopen(req, timeout=120).read()); print("ok", out)
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read()[:400].decode(errors="ignore")); sys.exit(1)
