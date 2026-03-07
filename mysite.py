import sys
import json
from flask import Flask, render_template, abort, redirect, url_for, request
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
PORT_DIR = 'portfolio'

# Языки
SUPPORTED_LANGS = ['ru', 'en', 'uk']
DEFAULT_LANG = 'ru'

UI_TRANSLATIONS = {
    'ru': {
        'blog_title': 'Блог',
        'blog_subtitle': 'Заметки о проектах',
        'tags': 'Теги',
        'portfolio_title': 'Портфолио',
        'portfolio_subtitle': 'Завершенные проекты',
        'contacts_title': 'Контакты',
        'contacts_subtitle': 'Соцсети и почта',
        'city': 'Город',
        'email': 'Email-адрес',
        'telegram': 'Телеграм',
        'name_placeholder': 'Имя',
        'your_email_placeholder': 'Ваш Email',
        'subject_placeholder': 'Тема',
        'message_placeholder': 'Сообщение',
        'send': 'Отправить',
        'resume_title': 'Резюме',
        'resume_subtitle': 'Опыт и навыки',
        'resume_intro': ('Занимаюсь frontend & backend разработкой на '
                         'HTML & CSS & Javascript, ReactJS, NextJS, Django и '
                         'Flask. Работал над проектами в нескольких областях:'),
        'robotics': 'Робототехника',
        'blockchain': 'Блокчейн',
        'neural_networks': 'Нейронные сети',
        'cryptography': 'Криптография',
        'online_tv': 'Онлайн ТВ',
        'resume_outro': 'Есть опыт фуллстек-разработки на платформах БлаБла Фактори и БлаБла Практикум.',
        'skills': 'Навыки',
        'professional_interests': 'Профессиональные интересы',
        'web_design': 'Веб-дизайн',
        'analytics': 'Аналитика',
        'technical_literature': 'Техническая литература',
        'algorithms': 'Алгоритмы',
        'backend': 'Бэкенд',
        'data_structures': 'Структуры данных',
        'hardware': 'Железо',
        'frontend': 'Фронтенд',
        'big_data': 'Big Data',
        'years_experience': 'Лет опыта',
        'projects': 'Проектов',
        'created_courses': 'Созданных курсов',
        'published_books': 'Опубликованных книг',
        'category': 'Категория',
        'project': 'Проект',
        'published': 'Статья опубликована',
        'platform': 'Платформа',
        'description': 'Описание',
        'notes': 'Примечания',
        'oops': 'Упс!',
        'error_404': 'Ошибка 404',
        'page_not_found': 'К сожалению, страница не найдена',
        'back_home': 'Вернуться на главную',
    },
    'en': {
        'blog_title': 'Blog',
        'blog_subtitle': 'Project notes',
        'tags': 'Tags',
        'portfolio_title': 'Portfolio',
        'portfolio_subtitle': 'Completed projects',
        'contacts_title': 'Contacts',
        'contacts_subtitle': 'Social media and email',
        'city': 'City',
        'email': 'Email',
        'telegram': 'Telegram',
        'name_placeholder': 'Name',
        'your_email_placeholder': 'Your Email',
        'subject_placeholder': 'Subject',
        'message_placeholder': 'Message',
        'send': 'Send',
        'resume_title': 'Resume',
        'resume_subtitle': 'Experience and skills',
        'resume_intro': 'I work in frontend & backend development with HTML & CSS & Javascript, ReactJS, NextJS, Django and Flask. I have worked on projects in several domains:',
        'robotics': 'Robotics',
        'blockchain': 'Blockchain',
        'neural_networks': 'Neural networks',
        'cryptography': 'Cryptography',
        'online_tv': 'Online TV',
        'resume_outro': 'I have full-stack development experience on BlaBla Factory and BlaBla Practicum platforms.',
        'skills': 'Skills',
        'professional_interests': 'Professional interests',
        'web_design': 'Web design',
        'analytics': 'Analytics',
        'technical_literature': 'Technical literature',
        'algorithms': 'Algorithms',
        'backend': 'Backend',
        'data_structures': 'Data structures',
        'hardware': 'Hardware',
        'frontend': 'Frontend',
        'big_data': 'Big Data',
        'years_experience': 'Years of experience',
        'projects': 'Projects',
        'created_courses': 'Courses created',
        'published_books': 'Published books',
        'category': 'Category',
        'project': 'Project',
        'published': 'Published on',
        'platform': 'Platform',
        'description': 'Description',
        'notes': 'Notes',
        'oops': 'Oops!',
        'error_404': 'Error 404',
        'page_not_found': 'Sorry, the page was not found',
        'back_home': 'Back to home',
    },
    'uk': {
        'blog_title': 'Блог',
        'blog_subtitle': 'Нотатки про проєкти',
        'tags': 'Теги',
        'portfolio_title': 'Портфоліо',
        'portfolio_subtitle': 'Завершені проєкти',
        'contacts_title': 'Контакти',
        'contacts_subtitle': 'Соцмережі та пошта',
        'city': 'Місто',
        'email': 'Email',
        'telegram': 'Телеграм',
        'name_placeholder': 'Імʼя',
        'your_email_placeholder': 'Ваш Email',
        'subject_placeholder': 'Тема',
        'message_placeholder': 'Повідомлення',
        'send': 'Надіслати',
        'resume_title': 'Резюме',
        'resume_subtitle': 'Досвід і навички',
        'resume_intro': 'Займаюся frontend & backend розробкою на HTML & CSS & Javascript, ReactJS, NextJS, Django та Flask. Працював над проєктами в кількох сферах:',
        'robotics': 'Робототехніка',
        'blockchain': 'Блокчейн',
        'neural_networks': 'Нейронні мережі',
        'cryptography': 'Криптографія',
        'online_tv': 'Онлайн ТБ',
        'resume_outro': 'Є досвід fullstack-розробки на платформах БлаБла Факторі та БлаБла Практикум.',
        'skills': 'Навички',
        'professional_interests': 'Професійні інтереси',
        'web_design': 'Вебдизайн',
        'analytics': 'Аналітика',
        'technical_literature': 'Технічна література',
        'algorithms': 'Алгоритми',
        'backend': 'Бекенд',
        'data_structures': 'Структури даних',
        'hardware': 'Залізо',
        'frontend': 'Фронтенд',
        'big_data': 'Big Data',
        'years_experience': 'Років досвіду',
        'projects': 'Проєктів',
        'created_courses': 'Створених курсів',
        'published_books': 'Опублікованих книг',
        'category': 'Категорія',
        'project': 'Проєкт',
        'published': 'Статтю опубліковано',
        'platform': 'Платформа',
        'description': 'Опис',
        'notes': 'Примітки',
        'oops': 'Ой!',
        'error_404': 'Помилка 404',
        'page_not_found': 'На жаль, сторінку не знайдено',
        'back_home': 'Повернутися на головну',
    }
}

LOCALIZED_SETTINGS = {
    'en': {
        'site_title': 'Vadym Bondarenko — Frontend & Backend Portfolio',
        'description': 'Vadym Bondarenko — portfolio, resume and blog of a frontend & backend developer',
        'sect1': 'Home',
        'sect2': 'Resume',
        'sect3': 'Portfolio',
        'sect4': 'Blog',
        'sect5': 'Contacts',
        'city': 'Kharkiv'
    },
    'uk': {
        'site_title': 'Вадим Бондаренко — Frontend & Backend портфоліо',
        'description': 'Вадим Бондаренко — портфоліо, резюме та блог frontend & backend розробника',
        'sect1': 'Головна',
        'sect2': 'Резюме',
        'sect3': 'Портфоліо',
        'sect4': 'Блог',
        'sect5': 'Контакти',
        'city': 'Харків'
    }
}

app = Flask(__name__)
app.config.from_object(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)


def _detect_lang_from_request():
    lang = request.view_args.get('lang') if request.view_args else None
    if lang in SUPPORTED_LANGS:
        return lang

    path_lang = request.path.strip('/').split('/', 1)[0]
    if path_lang in SUPPORTED_LANGS:
        return path_lang

    return DEFAULT_LANG


@app.context_processor
def inject_i18n_helpers():
    lang = _detect_lang_from_request()

    def t(key):
        return UI_TRANSLATIONS.get(lang, UI_TRANSLATIONS[DEFAULT_LANG]).get(
            key,
            UI_TRANSLATIONS[DEFAULT_LANG].get(key, key),
        )

    return {'t': t, 'current_lang': lang}


def _get_pages_for_lang(lang, section):
    localized_prefix = f"{lang}/{section}"
    localized_pages = [p for p in flatpages if p.path.startswith(localized_prefix)]
    if localized_pages:
        return localized_pages

    if lang == DEFAULT_LANG:
        return [p for p in flatpages if p.path.startswith(section)]

    default_localized_prefix = f"{DEFAULT_LANG}/{section}"
    fallback_pages = [
        p for p in flatpages
        if p.path.startswith(default_localized_prefix) or p.path.startswith(section)
    ]
    return fallback_pages


def _get_page_by_name(lang, section, name):
    candidates = [f"{lang}/{section}/{name}"]

    if lang == DEFAULT_LANG:
        candidates.append(f"{section}/{name}")
    else:
        candidates.append(f"{DEFAULT_LANG}/{section}/{name}")
        candidates.append(f"{section}/{name}")

    for path in candidates:
        page = flatpages.get(path)
        if page:
            return page

    abort(404)


# --- ROUTES ---

# Корень → редирект на DEFAULT_LANG
@app.route("/")
def root():
    return redirect(url_for("index", lang=DEFAULT_LANG))


# Главная
@app.route("/<lang>/")
def index(lang):
    if lang not in SUPPORTED_LANGS:
        abort(404)

    posts = _get_pages_for_lang(lang, POST_DIR)
    posts.sort(key=lambda item: item.meta.get('date', ''), reverse=True)

    cards = _get_pages_for_lang(lang, PORT_DIR)
    cards.sort(key=lambda item: item.meta.get('title', ''))

    # Настройки
    with open('settings.txt', encoding='utf8') as config:
        settings_config = json.load(config)

    settings = dict(settings_config.get('defaults', {}))

    # Backward compatibility: old flat settings format
    legacy_top_level = {
        key: value
        for key, value in settings_config.items()
        if key not in {'defaults', 'locales'}
    }
    settings.update(legacy_top_level)

    localized_overrides = settings_config.get('locales', {}).get(lang, {})
    settings.update(localized_overrides)

    settings.update(LOCALIZED_SETTINGS.get(lang, {}))

    # Теги
    tags = set()
    for p in posts:
        t = p.meta.get('tag')
        if t:
            tags.add(t.lower())

    return render_template('index.html', posts=posts, cards=cards, bigheader=True, **settings, tags=tags, lang=lang)


# Пост
@app.route('/<lang>/blog/<name>/')
def blog(lang, name):
    if lang not in SUPPORTED_LANGS:
        abort(404)

    post = _get_page_by_name(lang, POST_DIR, name)
    return render_template('post.html', post=post, lang=lang)


# Портфолио
@app.route('/<lang>/portfolio/<name>/')
def portfolio(lang, name):
    if lang not in SUPPORTED_LANGS:
        abort(404)

    card = _get_page_by_name(lang, PORT_DIR, name)
    return render_template('card.html', card=card, lang=lang)


# CSS для Pygments
@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}


# 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# --- Frozen-Flask generators ---
@freezer.register_generator
def index_generator():
    for lang in SUPPORTED_LANGS:
        yield {'lang': lang}

@freezer.register_generator
def blog_generator():
    for lang in SUPPORTED_LANGS:
        for p in _get_pages_for_lang(lang, POST_DIR):
            yield {'lang': lang, 'name': p.path.split('/')[-1]}

@freezer.register_generator
def portfolio_generator():
    for lang in SUPPORTED_LANGS:
        for c in _get_pages_for_lang(lang, PORT_DIR):
            yield {'lang': lang, 'name': c.path.split('/')[-1]}


# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='127.0.0.1', port=8000, debug=True)
