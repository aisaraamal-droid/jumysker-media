# jumysker-media

Публичные файлы для Instagram [@jumysker_ai](https://www.instagram.com/jumysker_ai/) — ИИ-помощники для бизнеса [jumysker.com](https://jumysker.com).

Instagram API забирает картинки и видео по прямым ссылкам, поэтому файлы лежат здесь и открываются через `raw.githubusercontent.com`.

> Всё в этом репозитории видно всем, в том числе публикации на будущие даты. Секретов здесь нет: токен Instagram хранится в секретах облачного окружения (заголовок `Authorization: Bearer` для graph.instagram.com) и в репозиторий не попадает.

## Структура

| Путь | Что внутри |
|---|---|
| `content/schedule.json` | План: дата, тип, файлы, подпись, сторис-анонс |
| `content/posts/pXX/` | Карусели 1080×1350 и `caption.txt` |
| `content/reels/` | Рилсы 1080×1920 с ведущими Ерланом (RU) и Даной (KZ), обложки и подписи |
| `content/stories/` | Сторис-анонсы к каждой публикации |
| `content/published.json` | Что уже опубликовано, со ссылками |
| `scripts/publish.py` | Публикация по ссылке через graph.instagram.com |
| `scripts/today.py` | Публикация по плану на сегодня (дата по UTC+5) |

## Запуск

```bash
python3 scripts/publish.py check              # аккаунт и квота
python3 scripts/today.py post --dry-run       # что выйдет сегодня
python3 scripts/today.py post                 # опубликовать пост или рилс на сегодня
python3 scripts/today.py story                # сторис-анонс, через ~20 минут после поста
```

Скрипт публикует только в @jumysker_ai: если токен от другого аккаунта, он останавливается.
