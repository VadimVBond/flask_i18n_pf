import sys, json
from flask import Flask, render_template, abort, redirect, url_for
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

app = Flask(__name__)
app.config.from_object(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)


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
        data = config.read()
        settings = json.loads(data)

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