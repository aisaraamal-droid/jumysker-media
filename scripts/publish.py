"""Публикация в Instagram @jumysker_ai по публичной ссылке на файл (Instagram API со входом через Instagram).

Использование:
  python3 publish.py check
  python3 publish.py reel <video_url> <caption_file> [<cover_url>]
  python3 publish.py image <image_url> <caption_file>
  python3 publish.py story <image_or_video_url>
  python3 publish.py carousel <caption_file> <image_url> [<image_url> ...]

Токен: секрет облачного окружения для graph.instagram.com (прокси сам добавляет заголовок
Authorization: Bearer …), либо переменная JUMYSKER_INSTAGRAM_TOKEN, либо строка JUMYSKER_INSTAGRAM_TOKEN=… в
~/.claude/channels/jumysker/.env (права 600). Значение токена нигде не печатается.
Перед любой публикацией проверяет, что токен от аккаунта @jumysker_ai, и печатает ссылку на пост.
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://graph.instagram.com/v24.0"
EXPECTED = os.environ.get("JUMYSKER_INSTAGRAM_USERNAME", "jumysker_ai")


def token():
    t = os.environ.get("JUMYSKER_INSTAGRAM_TOKEN", "").strip()
    if t:
        return t
    path = os.path.expanduser("~/.claude/channels/jumysker/.env")
    if os.path.exists(path):
        for line in open(path):
            if line.startswith("JUMYSKER_INSTAGRAM_TOKEN="):
                return line.split("=", 1)[1].strip()
    return ""   # токен подставит прокси окружения (секрет для graph.instagram.com)


TOKEN = token()


def call(method, path, retries=2, **params):
    if TOKEN:
        params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = path if path.startswith("http") else f"{API}/{path}"
    for attempt in range(retries + 1):
        req = (urllib.request.Request(url + "?" + data.decode()) if method == "GET"
               else urllib.request.Request(url, data=data, method="POST"))
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="ignore")
            if TOKEN:
                body = body.replace(TOKEN, "***")
            if not TOKEN and "cannot parse access token" in body.lower():
                sys.exit("BAD_TOKEN: секрет для graph.instagram.com подставляется, но это не токен Instagram "
                         "(нужен IGAA… из Generate token; не App ID, не App Secret и не «Bearer» дважды)")
            if not TOKEN and "active access token must be used" in body.lower():
                sys.exit("NO_TOKEN: прокси не подставил токен — проверьте секрет для graph.instagram.com")
            sys.exit(f"API error {e.code}: {body[:500]}")
        except (urllib.error.URLError, TimeoutError) as e:
            if method == "POST" or attempt == retries:
                raise
            time.sleep(10)


def account():
    me = call("GET", "me", fields="user_id,username,account_type,media_count")
    if me.get("username") != EXPECTED:
        sys.exit(f"WRONG_ACCOUNT: токен от @{me.get('username')}, а нужен @{EXPECTED}. Ничего не опубликовано.")
    return me


def wait(cid, what="контейнер"):
    for _ in range(60):
        st = call("GET", cid, fields="status_code,status")
        if st.get("status_code") == "FINISHED":
            return
        if st.get("status_code") in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"{what}: {st}")
        time.sleep(10)
    raise RuntimeError(f"{what}: timeout")


def latest_ids():
    return {m["id"] for m in call("GET", "me/media", fields="id", limit=5).get("data", [])}


def publish(cid):
    """media_publish; при обрыве сети сначала проверяем, не вышел ли пост, чтобы не выложить дубль."""
    before = latest_ids()
    try:
        mid = call("POST", "me/media_publish", creation_id=cid)["id"]
    except (urllib.error.URLError, TimeoutError):
        time.sleep(20)
        new = latest_ids() - before
        if not new:
            raise
        mid = new.pop()
    return call("GET", mid, fields="permalink")["permalink"]


def story(url):
    kind = "video_url" if url.lower().endswith((".mp4", ".mov")) else "image_url"
    for attempt in range(3):
        cid = call("POST", "me/media", media_type="STORIES", **{kind: url})["id"]
        try:
            wait(cid, "сторис")
            return publish(cid)
        except RuntimeError as e:
            if attempt == 2:
                sys.exit(f"STORY_ERROR: {e}")
            time.sleep(30)


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "check"
    me = account()
    if kind == "check":
        quota = call("GET", "me/content_publishing_limit", fields="quota_usage,config").get("data", [{}])[0]
        print(f"@{me['username']} · {me.get('account_type')} · публикаций: {me.get('media_count')} · "
              f"квота за 24 ч: {quota.get('quota_usage')}/{quota.get('config', {}).get('quota_total')}")
        return
    if kind == "story":
        print(story(sys.argv[2]))
        return
    if kind == "reel":
        url, cap = sys.argv[2], open(sys.argv[3]).read().strip()
        params = dict(media_type="REELS", video_url=url, caption=cap, share_to_feed="true")
        if len(sys.argv) > 4:
            params["cover_url"] = sys.argv[4]
        cid = call("POST", "me/media", **params)["id"]
    elif kind == "image":
        url, cap = sys.argv[2], open(sys.argv[3]).read().strip()
        cid = call("POST", "me/media", image_url=url, caption=cap)["id"]
    elif kind == "carousel":
        cap, urls = open(sys.argv[2]).read().strip(), sys.argv[3:]
        if not 2 <= len(urls) <= 10:
            sys.exit("В карусели от 2 до 10 картинок")
        kids = [call("POST", "me/media", image_url=u, is_carousel_item="true")["id"] for u in urls]
        for i, k in enumerate(kids, 1):
            wait(k, f"слайд {i}")
        cid = call("POST", "me/media", media_type="CAROUSEL", children=",".join(kids), caption=cap)["id"]
    else:
        sys.exit(__doc__)
    try:
        wait(cid)
    except RuntimeError as e:
        sys.exit(f"CONTAINER_ERROR: {e}")
    print(publish(cid))


if __name__ == "__main__":
    main()
