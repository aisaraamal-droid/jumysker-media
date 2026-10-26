# -*- coding: utf-8 -*-
"""Страница контент-плана (artifact): python3 page.py -> ../plan/index.html (медиа в ../plan/media)."""
import datetime as dt, html, os

from content import POSTS, REELS, STORIES_WEEK

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
E = html.escape
DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]


def d(s):
    x = dt.date.fromisoformat(s)
    return f"{x.day:02d}.{x.month:02d}", DAYS[x.weekday()]


def copybtn(text, label="Скопировать"):
    return f'<button type="button" class="copy" data-copy="{E(text)}">{label}</button>'


def strip_tags(t):
    import re
    return re.sub(r"<[^>]+>", " ", t).replace("  ", " ")


BIO = "24 ИИ-помощника для бизнеса и личных задач 🇰🇿\nБухгалтер · юрист · продажи · сайты · турагент\nRU · ҚАЗ · EN\n7 дней бесплатно, без карты 👇"
LINK = "https://jumysker.com/?utm_source=instagram&utm_medium=social&utm_campaign=bio"

REPLIES = [
    ("Сколько стоит?", "Здравствуйте! Помощники — от 7 700 ₸ в месяц, эксперты (юрист, бухгалтер) — 19 900 ₸. Можно и без подписки: пополнить баланс через Kaspi от 2 000 ₸ и платить за задачи. Первые 7 дней — бесплатно: jumysker.com 🙌"),
    ("Это заменит бухгалтера / юриста?", "ИИ-помощник берёт на себя рутину: счета, расчёты, проекты договоров, напоминания о сроках. Результат нужно проверять, а важные решения остаются за вами или вашим специалистом. Многие используют его как помощника своего бухгалтера."),
    ("На казахском работает?", "Да! Помощники отвечают на казахском, русском и английском 🇰🇿 Иә, көмекшілер қазақша да жауап береді."),
    ("Нужна карта для пробного?", "Нет, 7 дней бесплатно без банковской карты: до 3 помощников, кроме контент-мейкера и веб-разработчика."),
    ("Безопасно ли отправлять данные?", "Как мы обрабатываем данные, описано в Политике конфиденциальности: jumysker.com/privacy. Не отправляйте в чат пароли и данные банковских карт."),
    ("Негатив / жалоба", "Жаль, что так вышло. Напишите нам, пожалуйста, в директ или в WhatsApp +7 701 120 4528 — разберёмся и ответим."),
    ("Ведущие — живые люди?", "Ерлан и Дана — наши ИИ-ведущие. Ерлан рассказывает о фишках Jumysker на русском, Дана — на казахском 🙂"),
]


def main():
    items = sorted([("post", p) for p in POSTS] + [("reel", r) for r in REELS], key=lambda x: x[1]["date"])
    ready_reels = [r for r in REELS if r["status"] == "готов"]
    out = []
    w = out.append

    # ── шапка
    w(f'''<header class="hero"><div class="wrap">
<p class="eyebrow">Instagram · план на 4 недели · 28 октября — 22 ноября 2026</p>
<h1>Instagram Jumysker</h1>
<p class="lead">Контент для jumysker.com: стратегия, два ИИ-ведущих, 12 каруселей, 8 рилсов, сторис и ответы на комментарии. Цены и условия во всех текстах взяты с сайта.</p>
<div class="stats">
<div><b>12</b><span>постов · 78 слайдов</span></div>
<div><b>8</b><span>рилсов · {len(ready_reels)} готовы</span></div>
<div><b>2</b><span>ведущих · RU и KZ</span></div>
<div><b>5</b><span>публикаций в неделю</span></div>
</div>
<div class="alert"><b>Публикация ждёт двух шагов:</b> публичный репозиторий для файлов и токен @jumysker_ai из Meta for Developers. Скрипты и расписание готовы — подробности в разделе <a href="#launch">«Запуск»</a>.</div>
</div></header>
<nav class="toc"><div class="wrap">
<a href="#hosts">Ведущие</a><a href="#strategy">Стратегия</a><a href="#profile">Профиль</a><a href="#calendar">Календарь</a><a href="#posts">Посты</a><a href="#reels">Рилсы</a><a href="#stories">Сторис</a><a href="#replies">Комментарии</a><a href="#launch">Запуск</a>
</div></nav><main class="wrap">''')

    # ── ведущие
    w('''<section id="hosts"><p class="eyebrow">Лица бренда</p><h2>Ведущие: Ерлан и Дана</h2>
<p class="sec-lead">Два ИИ-ведущих в фирменном стиле сайта: синий пиджак, белая футболка, зелёный значок, светлая студия со стеклянными сферами. Каждый рилс — одна фишка Jumysker: ведущий в кадре → демо в чате → призыв.</p>
<div class="hosts">''')
    hosts = [
        ("Ерлан", "erlan", "r1-erlan", "Ведёт контент на русском", "Около 30 лет. Спокойный практик — «старший коллега, который уже всё попробовал». Говорит коротко, на «вы», с лёгким юмором; объясняет фишку на примере реальной задачи ИП.",
         "«У вас ИП, а бухгалтера нет? Я Ерлан из Jumysker. Покажу…»", "«Попробуйте Jumysker 7 дней бесплатно. Ссылка в профиле!»", "Мужской голос ElevenLabs из настроек reelio-bot", "«Фишка за минуту» — вт или чт"),
        ("Дана", "dana", "r2-dana", "Жүргізуші — қазақ тіліндегі контент", "Около 28 лет. Тёплая и энергичная, «своя» для казахоязычной аудитории. Простой разговорный казахский без канцелярита.",
         "«Сәлем! Мен Дана, Jumysker жүргізушісі…»", "«Jumysker-ді 7 күн тегін байқап көріңіз. Сілтеме профильде!»", "Женский голос ElevenLabs из настроек reelio-bot", "«Апта фишкасы» — сб"),
    ]
    for name, key, reel, role, character, hello, bye, voice, rubric in hosts:
        w(f'''<article class="host card"><video controls playsinline preload="none" poster="media/reels/{reel}-cover.jpg" src="media/reels/{reel}.mp4"></video>
<div class="host-body"><h3>{name}</h3><p class="role">{role}</p><p>{character}</p>
<dl><dt>Открывает</dt><dd>{hello}</dd><dt>Закрывает</dt><dd>{bye}</dd><dt>Голос</dt><dd>{voice}</dd><dt>Рубрика</dt><dd>{rubric}</dd></dl></div></article>''')
    w('''</div>
<div class="two">
<div class="card pad"><h3>Правила ведущих</h3><ul class="ticks">
<li>Одна фишка на ролик: хук до 3 секунд, демонстрация, один призыв.</li>
<li>Говорят только то, что есть на сайте: цены, лимиты и условия — из jumysker.com.</li>
<li>Не называют ИИ заменой специалиста; в темах налогов и договоров напоминают проверять результат.</li>
<li>Не показывают реальных клиентов и их данные без согласия — в демо пометка «пример».</li>
<li>На вопрос «вы живые?» честно отвечаем: это ИИ-ведущие Jumysker.</li></ul></div>
<div class="card pad"><h3>Как делается новый выпуск</h3><ol class="steps">
<li>Текст из трёх частей: A — ведущий в кадре, B — закадр к демо, C — призыв.</li>
<li>Голос: ElevenLabs с таймингами слов — из них же субтитры.</li>
<li>Картинка ведущего: Seedance 2.0 mini по портрету, голос подаётся только как ориентир для губ. Звук Seedance не используется.</li>
<li>Демо в чате и финальная карточка рендерятся из шаблона, затем сборка 1080×1920, громкость −14 LUFS.</li>
<li>Команда: <code>python3 _build/gen/build_reel.py r3</code></li></ol>
<p class="note">Клип ведущего (8 с, 720p) обходится примерно в $0,6 в BytePlus. Синхрон губ приблизительный: время клипа подгоняется под речь. Для точного синхрона нужна отдельная модель lip-sync.</p></div>
</div></section>''')

    # ── стратегия
    w('''<section id="strategy"><p class="eyebrow">Зачем и для кого</p><h2>Стратегия</h2>
<div class="grid3">
<div class="card pad"><h3>Цель</h3><p>Регистрации на 7-дневный пробный период из Instagram. Ссылка в профиле с UTM-меткой — переходы видны в аналитике сайта.</p></div>
<div class="card pad"><h3>Позиционирование</h3><p>AI-команда для бизнеса в Казахстане: задача в чате — готовый черновик, а проверка и решение остаются за вами.</p></div>
<div class="card pad"><h3>Тон</h3><p>На «вы», просто и по делу. Без «ИИ заменит всех». Местные детали: тенге, Kaspi, 2ГИС, hh.kz, Enbek, БИН. Подпись поста — по-русски с коротким блоком на казахском.</p></div>
</div>
<h3 class="sub">Аудитория</h3>
<div class="grid3">
<div class="card pad"><h4>ИП и малый бизнес</h4><p>Салоны, мастерские, кофейни, онлайн-продавцы. Всё делают сами: счета, ответы клиентам, посты. Нужен результат за минуты и понятная цена.</p></div>
<div class="card pad"><h4>ТОО и команды</h4><p>Продажи, документы, HR, тендеры. Нужны готовые роли и командный тариф со скидкой.</p></div>
<div class="card pad"><h4>Для себя</h4><p>Фрилансеры и частные лица: резюме, переводы, сайт личного проекта, отпуск с турагентом.</p></div>
</div>
<h3 class="sub">Рубрики и ритм</h3>
<div class="tablewrap"><table class="mix">
<thead><tr><th>Рубрика</th><th>Доля</th><th>Зачем</th><th>Формат</th></tr></thead><tbody>
<tr><td>Полезное: чек-листы и шаблоны</td><td class="num">35 %</td><td>Сохранения и репосты</td><td>Карусель</td></tr>
<tr><td>Фишка с ведущим / Помощник недели</td><td class="num">35 %</td><td>Показать продукт в деле</td><td>Рилс, карусель</td></tr>
<tr><td>Тарифы и старт</td><td class="num">20 %</td><td>Снять вопросы о цене, привести на пробный период</td><td>Карусель, закреп</td></tr>
<tr><td>Для себя: сайт, турагент</td><td class="num">10 %</td><td>Расширить аудиторию</td><td>Карусель, рилс</td></tr>
</tbody></table></div>
<div class="grid3">
<div class="card pad"><h4>Частота</h4><p>3 карусели в неделю (пн, ср, пт), 2 рилса (Ерлан — будни, Дана — суббота), сторис каждый день по 3–5 кадров.</p></div>
<div class="card pad"><h4>Время</h4><p>Стартовая гипотеза: 12:30–13:30 и 19:00–21:00 по Астане (UTC+5). Через 2 недели сверяем со статистикой аккаунта.</p></div>
<div class="card pad"><h4>Хэштеги и метрики</h4><p>5 точных хэштегов на пост: #Jumysker и 4 тематических. Каждую неделю смотрим охват, сохранения, досмотры рилсов, переходы по ссылке и регистрации.</p></div>
</div></section>''')

    # ── профиль
    hl = ["1-start", "2-pomoshniki", "3-tarify", "4-erlan", "5-dana", "6-faq"]
    hln = ["Старт", "Помощники", "Тарифы", "Ерлан", "Дана", "FAQ"]
    w(f'''<section id="profile"><p class="eyebrow">Оформление</p><h2>Профиль</h2>
<div class="profile">
<div class="card pad phone">
<div class="ph-top"><img src="media/extra/avatar-1080.jpg" alt="Аватар профиля"><div><b>jumysker_ai</b><span>Jumysker | ИИ-помощники</span><small>Программное обеспечение</small></div></div>
<pre class="bio">{E(BIO)}</pre><p class="ph-link">jumysker.com</p>
<div class="hls">{"".join(f'<figure><img src="media/extra/{h}.jpg" alt=""><figcaption>{n}</figcaption></figure>' for h, n in zip(hl, hln))}</div>
</div>
<div class="kv">
<div class="row"><span>Имя пользователя</span><b>@jumysker_ai</b></div>
<div class="row"><span>Имя (ищется в поиске)</span><b>Jumysker | ИИ-помощники</b>{copybtn("Jumysker | ИИ-помощники")}</div>
<div class="row"><span>Био, 136 знаков</span><b class="pre">{E(BIO)}</b>{copybtn(BIO)}</div>
<div class="row"><span>Ссылка</span><b class="mono">{E(LINK)}</b>{copybtn(LINK)}</div>
<div class="row"><span>Кнопка связи</span><b>WhatsApp +7 701 120 4528</b><em>номер с сайта</em></div>
<div class="row"><span>Закрепить</span><b>3 поста первой недели</b><em>«Знакомьтесь», «Как начать», «Сколько стоит»</em></div>
<div class="row"><span>Файлы</span><b class="mono">profile/avatar-1080.jpg, profile/highlights/</b></div>
</div></div></section>''')

    # ── календарь
    w('<section id="calendar"><p class="eyebrow">28.10 — 22.11</p><h2>Календарь</h2><div class="tablewrap"><table class="cal"><thead><tr><th>Дата</th><th>Формат</th><th>Тема</th><th>Рубрика / ведущий</th><th>Статус</th></tr></thead><tbody>')
    week = 0
    names = {1: "Неделя 1 · запуск", 2: "Неделя 2 · продажи и деньги", 3: "Неделя 3 · документы и команда", 4: "Неделя 4 · рост"}
    for kind, x in items:
        if x["week"] != week:
            week = x["week"]
            w(f'<tr class="wk"><td colspan="5">{names[week]}</td></tr>')
        dd, day = d(x["date"])
        if kind == "post":
            st = '<span class="pill ok">Готов</span>' + (' <span class="pill">Закрепить</span>' if x.get("pin") else "")
            w(f'<tr><td class="num">{dd} <small>{day}</small></td><td>Карусель · {len(x["slides"])}</td><td><a href="#{x["id"]}">{E(x["title"])}</a></td><td>{E(x["rubric"])}</td><td>{st}</td></tr>')
        else:
            st = '<span class="pill ok">Видео готово</span>' if x["status"] == "готов" else '<span class="pill warn">Сценарий</span>'
            w(f'<tr><td class="num">{dd} <small>{day}</small></td><td>Рилс · {x["lang"]}</td><td><a href="#{x["id"]}">{E(x["title"])}</a></td><td>{x["host"]} · {E(x["assistant"])}</td><td>{st}</td></tr>')
    w('</tbody></table></div><p class="note">К каждой публикации через 20 минут выходит сторис-анонс, остальные сторис — по ритму из раздела «Сторис». Если аккаунт подключат позже, все даты сдвигаются на одинаковое число дней.</p></section>')

    # ── посты
    w('<section id="posts"><p class="eyebrow">Лента</p><h2>Посты</h2><p class="sec-lead">Каждый пост — карусель 1080×1350 (4:5) и готовая подпись. Полноразмерные слайды лежат в <code>posts/pXX/</code>, подпись — в <code>caption.txt</code> там же.</p>')
    for p in POSTS:
        dd, day = d(p["date"])
        full = f'{p["caption"]}\n\n🇰🇿 {p["caption_kz"]}\n\n{p["tags"]}'
        imgs = "".join(f'<img loading="lazy" src="media/posts/{p["id"]}/slide-{i:02d}.jpg" alt="Слайд {i}">' for i in range(1, len(p["slides"]) + 1))
        pin = '<span class="pill">Закрепить</span>' if p.get("pin") else ""
        w(f'''<article class="post card" id="{p["id"]}">
<div class="post-head"><div><p class="meta"><span class="num">{dd}</span> {day} · {E(p["rubric"])} · {len(p["slides"])} слайдов {pin}</p><h3>{E(p["title"])}</h3><p class="goal">{E(p["goal"])}</p></div>{copybtn(full, "Скопировать подпись")}</div>
<div class="strip">{imgs}</div>
<details><summary>Подпись</summary><pre class="cap">{E(full)}</pre></details></article>''')
    w('</section>')

    # ── рилсы
    w('<section id="reels"><p class="eyebrow">Ерлан — RU · Дана — KZ</p><h2>Рилсы</h2><p class="sec-lead">Схема: A — ведущий в кадре, B — демо в чате под голос, C — финальная карточка. Готовые ролики лежат в <code>reels/</code>, остальные собираются по сценарию той же командой.</p><div class="reels">')
    for r in REELS:
        dd, day = d(r["date"])
        full = f'{r["caption"]}\n\n{r["caption_alt"]}\n\n{r["tags"]}'
        file = f'{r["id"]}-{"erlan" if r["host"] == "Ерлан" else "dana"}'
        media = (f'<video controls playsinline preload="none" poster="media/reels/{file}-cover.jpg" src="media/reels/{file}.mp4"></video>'
                 if r["status"] == "готов" else "")
        status = '<span class="pill ok">Видео готово</span>' if r["status"] == "готов" else '<span class="pill warn">Сценарий</span>'
        demo = f'<p class="demo"><b>Демо:</b> {E(r["demo"])}</p>' if r.get("demo") else ""
        w(f'''<article class="reel card" id="{r["id"]}">{media}<div class="reel-body">
<p class="meta"><span class="num">{dd}</span> {day} · {r["host"]} · {r["lang"]} · {E(r["assistant"])} {status}</p><h3>{E(r["title"])}</h3>
<dl class="script"><dt>A · в кадре</dt><dd>{E(r["a"])}</dd><dt>B · демо</dt><dd>{E(r["b"])}</dd><dt>C · финал</dt><dd>{E(r["c"])}</dd></dl>{demo}
<details><summary>Подпись</summary><pre class="cap">{E(full)}</pre></details>{copybtn(full, "Скопировать подпись")}</div></article>''')
    w('</div></section>')

    # ── сторис
    w('<section id="stories"><p class="eyebrow">Каждый день</p><h2>Сторис</h2><div class="stories"><div class="tablewrap"><table class="cal"><thead><tr><th>День</th><th>Формат</th><th>Что делаем</th></tr></thead><tbody>')
    for day, fmt, what, tpl in STORIES_WEEK:
        w(f'<tr><td>{day}</td><td>{E(fmt)}</td><td>{E(what)}</td></tr>')
    w('</tbody></table></div><div class="tpls">')
    for f, cap in [("s1-opros-ru", "Опрос · Ерлан"), ("s2-zadacha-dnya-kz", "Күн тапсырмасы · Дана"), ("s3-cta-ru", "Призыв · RU"), ("s3-cta-kz", "Призыв · KZ")]:
        w(f'<figure><img loading="lazy" src="media/extra/{f}.jpg" alt="{cap}"><figcaption>{cap}</figcaption></figure>')
    w('</div></div><p class="note">Шаблоны 1080×1920 лежат в <code>stories/</code>. Стикеры «Опрос» и «Ссылка» добавляются в приложении Instagram — через API их поставить нельзя.</p></section>')

    # ── ответы
    w('<section id="replies"><p class="eyebrow">Комьюнити</p><h2>Ответы на комментарии и директ</h2><div class="replies">')
    for q, a in REPLIES:
        w(f'<div class="card pad reply"><h4>{E(q)}</h4><p>{E(a)}</p>{copybtn(a)}</div>')
    w('</div></section>')

    # ── запуск
    w('''<section id="launch"><p class="eyebrow">Как в проекте Reelio</p><h2>Запуск и публикация</h2>
<p class="sec-lead">Публикуем сами через Instagram API (graph.instagram.com) из облачной сессии Claude. Файлы берутся из публичного репозитория GitHub, сторонние сервисы не нужны.</p><ol class="launch">
<li class="card pad"><h4>Аккаунт @jumysker_ai</h4><p>Профессиональный: «Бизнес» или «Автор». Страница Facebook не нужна.</p></li>
<li class="card pad"><h4>Токен в Meta for Developers</h4><p>Приложение Reelio (уже Live) → Instagram → API setup with Instagram login → добавить @jumysker_ai → Generate token. Разрешения: instagram_business_basic и instagram_business_content_publish.</p></li>
<li class="card pad"><h4>Токен — в окружение, не в чат</h4><p>Настройки облачного окружения → переменная <code>JUMYSKER_INSTAGRAM_TOKEN</code>. Скрипт публикует только в @jumysker_ai и сам проверяет аккаунт перед каждой публикацией.</p></li>
<li class="card pad"><h4>Публичный репозиторий</h4><p><code>aisaraamal-droid/jumysker-media</code> с README. Всё в нём видно всем, включая публикации на будущие даты.</p></li>
</ol>
<div class="two">
<div class="card pad"><h3>Расписание</h3><ul class="ticks">
<li>Пост или рилс — в 13:00 по Алматы, сторис-анонс — через 20 минут.</li>
<li>Одна публикация в день: два рилса подряд отбирают охват друг у друга.</li>
<li>Рилс на следующий день монтируется и проверяется накануне.</li>
<li>После каждой публикации — ссылка одной строкой в чате.</li></ul></div>
<div class="card pad"><h3>Подтверждение</h3><ul class="ticks">
<li>Первая публикация — только после вашего «да» в этом чате.</li>
<li>Дальше — по одному разрешению с рамками, например «публикуй по плану до 22.11».</li>
<li>Ответы в комментариях и директ, внеплановые посты и удаление — отдельно.</li>
<li>«Стоп» — сразу останавливаемся.</li></ul>
<p class="note">Вручную в приложении: стикер-ссылка в сторис, музыка из библиотеки Instagram, закрепление постов, правка подписи после публикации.</p></div>
</div></section>
</main><footer class="wrap"><p>Jumysker · ИП EVISA · материалы для Instagram. Тексты сверены с jumysker.com на 26.10.2026.</p></footer>''')

    page = TEMPLATE.replace("%%BODY%%", "\n".join(out))
    os.makedirs(os.path.join(ROOT, "plan"), exist_ok=True)
    open(os.path.join(ROOT, "plan", "index.html"), "w").write(page)
    print("ok", len(page) // 1024, "KB")


TEMPLATE = r'''<title>Instagram Jumysker</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Inter+Tight:wght@700;800&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: одна колонка 1120px в фирменных цветах jumysker.com; карусели и таблицы прокручиваются внутри карточек */
:root {
  --bg: #f5f8fe; --surface: #ffffff; --ink: #101735; --muted: #5d6788; --line: #deebfa;
  --accent: #0860ff; --accent-ink: #ffffff; --accent-soft: #e6efff; --ok: #07936a; --ok-soft: #e2f8ef; --warn: #a15c07; --warn-soft: #fff1dc;
  --display: "Inter Tight", "Inter", system-ui, sans-serif; --body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif; --mono: "JetBrains Mono", ui-monospace, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0b1020; --surface: #131b31; --ink: #e8edfb; --muted: #9aa6c7; --line: #243257; --accent: #5b93ff; --accent-ink: #0b1020; --accent-soft: #17264b;
  --ok: #3fd3a0; --ok-soft: #0f2e26; --warn: #f2b84b; --warn-soft: #33260d; color-scheme: dark; } }
:root[data-theme="dark"] { --bg: #0b1020; --surface: #131b31; --ink: #e8edfb; --muted: #9aa6c7; --line: #243257; --accent: #5b93ff; --accent-ink: #0b1020; --accent-soft: #17264b;
  --ok: #3fd3a0; --ok-soft: #0f2e26; --warn: #f2b84b; --warn-soft: #33260d; color-scheme: dark; }
body { background: var(--bg); color: var(--ink); font: 16px/1.55 var(--body); }
.wrap { max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
h1, h2, h3 { font-family: var(--display); letter-spacing: -0.02em; text-wrap: balance; margin: 0; }
h1 { font-size: clamp(2.4rem, 6vw, 4rem); line-height: 1.02; }
h2 { font-size: clamp(1.7rem, 3.4vw, 2.4rem); line-height: 1.1; margin-bottom: 0.6rem; }
h3 { font-size: 1.25rem; line-height: 1.25; }
h4 { margin: 0 0 0.35rem; font-size: 1.02rem; }
p { margin: 0; }
a { color: var(--accent); }
code, .mono { font-family: var(--mono); font-size: 0.86em; }
code { background: var(--accent-soft); padding: 0.1em 0.4em; border-radius: 6px; }
.eyebrow { font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.5rem; }
.hero { padding-block: 56px 28px; }
.hero .lead { font-size: 1.15rem; color: var(--muted); max-width: 62ch; margin-top: 1rem; }
.stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 28px; }
.stats div { background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 14px 16px; }
.stats b { display: block; font: 800 2rem/1 var(--display); font-variant-numeric: tabular-nums; }
.stats span { color: var(--muted); font-size: 0.9rem; }
.alert { margin-top: 18px; background: var(--warn-soft); color: var(--ink); border-radius: 14px; padding: 14px 16px; }
.alert b { color: var(--warn); }
.toc { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); border-bottom: 1px solid var(--line); }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }
.toc .wrap { display: flex; gap: 4px; overflow-x: auto; padding-block: 10px; scrollbar-width: none; }
.toc a { white-space: nowrap; text-decoration: none; color: var(--muted); font-weight: 600; font-size: 0.92rem; padding: 6px 12px; border-radius: 999px; }
.toc a:hover, .toc a:focus-visible { background: var(--accent-soft); color: var(--accent); outline: none; }
main section { padding-block: 48px 8px; scroll-margin-top: 56px; display: flex; flex-direction: column; gap: 16px; }
.sec-lead { color: var(--muted); max-width: 70ch; }
.sub { margin-top: 12px; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 20px; }
.pad { padding: 20px 22px; display: flex; flex-direction: column; gap: 8px; }
.pad p { color: var(--muted); }
.grid3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.two { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.note { color: var(--muted); font-size: 0.9rem; }
.pill { display: inline-block; font-size: 0.74rem; font-weight: 700; padding: 3px 9px; border-radius: 999px; background: var(--accent-soft); color: var(--accent); white-space: nowrap; vertical-align: 1px; }
.pill.ok { background: var(--ok-soft); color: var(--ok); }
.pill.warn { background: var(--warn-soft); color: var(--warn); }
.num { font-variant-numeric: tabular-nums; }
/* ведущие */
.hosts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.host { display: grid; grid-template-columns: 220px minmax(0, 1fr); overflow: hidden; }
.host video, .reel video { width: 100%; aspect-ratio: 9 / 16; object-fit: cover; background: var(--accent-soft); display: block; max-width: 100%; }
.host-body { padding: 18px 20px; display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.host-body > p { color: var(--muted); font-size: 0.95rem; }
.host .role { color: var(--accent); font-weight: 700; }
dl { margin: 4px 0 0; display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 6px 12px; font-size: 0.92rem; }
dt { color: var(--muted); font-weight: 600; }
dd { margin: 0; }
ul.ticks, ol.steps { margin: 0; padding-left: 1.2rem; display: flex; flex-direction: column; gap: 6px; }
/* таблицы */
.tablewrap { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 20px; }
table { border-collapse: collapse; width: 100%; font-size: 0.94rem; }
th { text-align: left; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); padding: 12px 16px; border-bottom: 1px solid var(--line); }
td { padding: 11px 16px; border-bottom: 1px solid var(--line); vertical-align: top; }
tr:last-child td { border-bottom: 0; }
td small { color: var(--muted); }
tr.wk td { background: var(--accent-soft); color: var(--accent); font-weight: 700; font-size: 0.86rem; }
.cal a { color: var(--ink); text-decoration: none; font-weight: 600; }
.cal a:hover { color: var(--accent); }
/* профиль */
.profile { display: grid; grid-template-columns: 360px minmax(0, 1fr); gap: 14px; align-items: start; }
.phone .ph-top { display: flex; gap: 14px; align-items: center; }
.phone .ph-top img { width: 72px; height: 72px; border-radius: 50%; border: 1px solid var(--line); }
.phone .ph-top b { display: block; }
.phone .ph-top span { display: block; font-weight: 600; font-size: 0.92rem; }
.phone .ph-top small { color: var(--muted); }
.bio { white-space: pre-wrap; font: 0.92rem/1.45 var(--body); margin: 6px 0 0; color: var(--ink); }
.ph-link { color: var(--accent) !important; font-weight: 600; }
.hls { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 6px; margin-top: 8px; }
.hls figure { margin: 0; text-align: center; }
.hls img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 50%; border: 2px solid var(--line); }
.hls figcaption { font-size: 0.6rem; color: var(--muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.kv { display: flex; flex-direction: column; gap: 8px; }
.kv .row { display: grid; grid-template-columns: 170px minmax(0, 1fr) auto; gap: 4px 14px; align-items: start; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 12px 14px; }
.kv .row span { color: var(--muted); font-size: 0.88rem; }
.kv .row b { overflow-wrap: anywhere; font-weight: 600; }
.kv .row b.pre { white-space: pre-wrap; }
.kv .row em { grid-column: 2 / -1; font-style: normal; color: var(--muted); font-size: 0.86rem; }
/* посты */
.post { padding: 18px 0 14px; display: flex; flex-direction: column; gap: 12px; scroll-margin-top: 60px; overflow: hidden; }
.post-head { display: flex; justify-content: space-between; gap: 14px; align-items: flex-start; padding: 0 20px; }
.post-head > div { min-width: 0; }
.meta { color: var(--muted); font-size: 0.86rem; margin-bottom: 4px; }
.goal { color: var(--muted); font-size: 0.92rem; margin-top: 4px; }
.strip { display: flex; gap: 10px; overflow-x: auto; padding: 0 20px 6px; scroll-snap-type: x mandatory; }
.strip img { width: 230px; flex: none; aspect-ratio: 4 / 5; border-radius: 12px; border: 1px solid var(--line); scroll-snap-align: start; max-width: 70vw; height: auto; }
details { padding: 0 20px; }
summary { cursor: pointer; font-weight: 600; color: var(--accent); }
pre.cap { white-space: pre-wrap; font: 0.92rem/1.5 var(--body); background: var(--bg); border: 1px solid var(--line); border-radius: 12px; padding: 14px; margin: 10px 0 0; max-width: 72ch; }
.copy { font: 600 0.86rem var(--body); color: var(--accent-ink); background: var(--accent); border: 0; border-radius: 999px; padding: 8px 14px; cursor: pointer; white-space: nowrap; flex: none; align-self: flex-start; }
.copy:hover { filter: brightness(1.08); }
.copy:focus-visible { outline: 3px solid var(--accent-soft); outline-offset: 2px; }
.copy.done { background: var(--ok); }
/* рилсы */
.reels { display: flex; flex-direction: column; gap: 14px; }
.reel { display: grid; grid-template-columns: 220px minmax(0, 1fr); overflow: hidden; scroll-margin-top: 60px; }
.reel:not(:has(video)) { grid-template-columns: minmax(0, 1fr); }
.reel-body { padding: 18px 20px; display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.reel-body details { padding: 0; }
.script dd { color: var(--ink); }
.demo { color: var(--muted); font-size: 0.9rem; }
/* сторис */
.stories { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 14px; align-items: start; }
.tpls { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }
.tpls figure { margin: 0; }
.tpls img { width: 100%; aspect-ratio: 9 / 16; border-radius: 12px; border: 1px solid var(--line); }
.tpls figcaption { font-size: 0.74rem; color: var(--muted); margin-top: 4px; }
.replies { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.reply p { color: var(--ink); }
.launch { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; counter-reset: s; }
.launch li { counter-increment: s; }
.launch li::before { content: counter(s); font: 800 1.6rem var(--display); color: var(--accent); }
footer { padding-block: 40px 56px; color: var(--muted); font-size: 0.86rem; }
@media (max-width: 860px) {
  .stats, .launch { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .grid3, .two, .hosts, .replies, .stories, .profile { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 560px) {
  .host, .reel { grid-template-columns: minmax(0, 1fr); }
  .host video, .reel video { max-height: 70vh; }
  .kv .row { grid-template-columns: minmax(0, 1fr); }
  .kv .row em { grid-column: auto; }
  .post-head { flex-direction: column; }
  .tpls { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; } }
</style>
%%BODY%%
<script>
document.addEventListener('click', async (e) => {
  const b = e.target.closest('.copy'); if (!b) return;
  const text = b.dataset.copy, label = b.textContent;
  try { await navigator.clipboard.writeText(text); }
  catch (err) {
    const t = document.createElement('textarea'); t.value = text; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
    document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (_) {} t.remove();
  }
  b.textContent = 'Скопировано'; b.classList.add('done');
  setTimeout(() => { b.textContent = label; b.classList.remove('done'); }, 1600);
});
</script>
'''

if __name__ == "__main__":
    main()
