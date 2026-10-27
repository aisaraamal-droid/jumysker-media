# Исходники контента Jumysker

Из этих файлов собраны карусели, сторис и рилсы в `content/`. Все цены и условия сверены с jumysker.com на 27.10.2026 (новый прайс, 27 помощников).

| Путь | Что внутри |
|---|---|
| `_build/content.py` | Все тексты: слайды и подписи 16 постов, сценарии 10 рилсов, ритм сторис |
| `_build/build.py`, `render.js` | Карусели 1080×1350 в стиле сайта (HTML → JPEG через Playwright) |
| `_build/extras.py`, `stories_auto.py` | Профиль, хайлайты, шаблоны и анонсы сторис |
| `_build/release.py` | Выпуск готового рилса в `content/` и в расписание |
| `_build/gen/` | Рилсы с ведущими: голос, клип ведущего, монтаж |
| `_build/icons/`, `_build/art/` | Иконки Lucide (ISC) и иллюстрации с jumysker.com |
| `avatar/` | Портреты ведущих Ерлана и Даны |

## Ведущие

- **Ерлан** — контент на русском, мужской голос ElevenLabs из reelio-bot.
- **Дана** — контент на казахском, женский голос ElevenLabs из reelio-bot.
- Звук в роликах — только ElevenLabs. Seedance делает только картинку ведущего (голос подаётся как ориентир для губ, его звук не используется).

## Как пересобрать

```bash
cd _build
python3 build.py && node render.js           # карусели -> source/posts (затем скопировать в content/posts)
python3 extras.py && node render_extras.js   # профиль, хайлайты, шаблоны сторис
```

Новый рилс с ведущим (тексты A/B/C и демо — в `_build/gen/reels_hosted.py`):

```bash
cd _build/gen
python3 make_host.py r3     # голос ElevenLabs + клип ведущего Seedance (без звука), ≈ $0,6
python3 build_reel.py r3    # монтаж 1080×1920 с субтитрами
cd .. && python3 release.py r3
```

Ключей и ID голосов в этих файлах нет: ключи подставляет прокси окружения, ID голосов берутся из reelio-bot
или из переменных `JUMYSKER_VOICE_MALE` / `JUMYSKER_VOICE_FEMALE`.
