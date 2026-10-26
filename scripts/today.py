"""Публикация по плану на сегодня (дата по Алматы/Астане, UTC+5).

Использование:
  python3 today.py post            пост или рилс на сегодня
  python3 today.py story           сторис-анонс к сегодняшней публикации (через ~20 минут после поста)
  python3 today.py post --dry-run  показать, что будет опубликовано, ничего не отправляя
  python3 today.py post --date 2026-10-28

Берёт файлы из content/ этого репозитория по ссылкам raw.githubusercontent.com, ждёт, пока CDN отдаёт
файл целиком, вызывает publish.py и записывает ссылку в content/published.json (commit + push).
Коды выхода в выводе: NO_ITEM_TODAY, NOT_READY, NO_FILE, ALREADY, затем ссылка на пост.
"""
import datetime, json, os, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CONTENT = os.path.join(REPO, "content")
STATE = os.path.join(CONTENT, "published.json")


def git(*args, check=True):
    return subprocess.run(["git", "-C", REPO, *args], check=check, capture_output=True, text=True).stdout.strip()


def raw_base():
    url = git("remote", "get-url", "origin").removesuffix("/").removesuffix(".git")
    owner, repo = url.replace(":", "/").split("/")[-2:]
    return f"https://raw.githubusercontent.com/{owner}/{repo}/main/"


def wait_cdn(url, local):
    size = os.path.getsize(local)
    for _ in range(30):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
                if int(r.headers.get("Content-Length", 0)) == size:
                    return
        except Exception:
            pass
        time.sleep(10)
    sys.exit(f"CDN_TIMEOUT: {url}")


def main():
    args = sys.argv[1:]
    mode = args[0] if args and not args[0].startswith("--") else "post"
    dry = "--dry-run" in args
    today = (datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5))).date().isoformat()
             if "--date" not in args else args[args.index("--date") + 1])
    items = [x for x in json.load(open(os.path.join(CONTENT, "schedule.json"))) if x["date"] == today]
    if not items:
        sys.exit(f"NO_ITEM_TODAY: {today}")
    item = items[0]
    key = item["id"] + (":story" if mode == "story" else "")
    if not item.get("ready"):
        sys.exit(f"NOT_READY: {item['id']} {item['title']}")
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    if key in state:
        sys.exit(f"ALREADY: {state[key]['permalink']}")
    files = [item["story"]] if mode == "story" else item["files"] + ([item["cover"]] if item.get("cover") else [])
    for f in files + ([] if mode == "story" else [item["caption"]]):
        if not os.path.exists(os.path.join(CONTENT, f)):
            sys.exit(f"NO_FILE: content/{f}")
    base = raw_base() + "content/"
    urls = [base + f for f in files]
    print(f"{today} · {key} · {item['kind']} · {item['title']}")
    if dry:
        print("\n".join(urls))
        if mode != "story":
            print("─" * 40 + "\n" + open(os.path.join(CONTENT, item["caption"])).read().strip())
        return print("DRY_RUN: ничего не опубликовано")
    for u, f in zip(urls, files):
        wait_cdn(u, os.path.join(CONTENT, f))
    pub = [sys.executable, os.path.join(HERE, "publish.py")]
    cap = os.path.join(CONTENT, item.get("caption", ""))
    if mode == "story":
        cmd = pub + ["story", urls[0]]
    elif item["kind"] == "carousel":
        cmd = pub + ["carousel", cap] + urls
    else:
        cmd = pub + ["reel", urls[0], cap] + ([urls[-1]] if item.get("cover") else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit((r.stdout + r.stderr).strip())
    link = r.stdout.strip().splitlines()[-1]
    state[key] = {"permalink": link, "at": datetime.datetime.now().isoformat(timespec="seconds")}
    json.dump(state, open(STATE, "w"), ensure_ascii=False, indent=1)
    g = ["-c", "user.name=jumysker-bot", "-c", "user.email=aisaraamal-droid@users.noreply.github.com"]
    git(*g, "add", STATE)
    git(*g, "commit", "-qm", f"Published {key}", check=False)
    git("push", "-q", "origin", "HEAD:main", check=False)
    print(link)


if __name__ == "__main__":
    main()
