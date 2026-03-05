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

    posts = [p for p in flatpages if p.path.startswith(f"{lang}/{POST_DIR}") or (lang==DEFAULT_LANG and p.path.startswith(POST_DIR))]
    posts.sort(key=lambda item: item['date'], reverse=True)

    cards = [p for p in flatpages if p.path.startswith(f"{lang}/{PORT_DIR}") or (lang==DEFAULT_LANG and p.path.startswith(PORT_DIR))]
    cards.sort(key=lambda item: item['title'])

    # Настройки
    with open('settings.txt', encoding='utf8') as config:
        data = config.read()
        settings = json.loads(data)

    # Теги
    tags = set()
    for p in flatpages:
        t = p.meta.get('tag')
        if t:
            tags.add(t.lower())

    return render_template('index.html', posts=posts, cards=cards, bigheader=True, **settings, tags=tags, lang=lang)

# Пост
@app.route('/<lang>/blog/<name>/')
def blog(lang, name):
    if lang not in SUPPORTED_LANGS:
        abort(404)

    path = f"{lang}/{POST_DIR}/{name}" if lang != DEFAULT_LANG else f"{POST_DIR}/{name}"
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post, lang=lang)

# Портфолио
@app.route('/<lang>/portfolio/<name>/')
def portfolio(lang, name):
    if lang not in SUPPORTED_LANGS:
        abort(404)

    path = f"{lang}/{PORT_DIR}/{name}" if lang != DEFAULT_LANG else f"{PORT_DIR}/{name}"
    card = flatpages.get_or_404(path)
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
        for p in flatpages:
            if p.path.startswith(POST_DIR) or p.path.startswith(f"{DEFAULT_LANG}/{POST_DIR}"):
                yield {'lang': lang, 'name': p.path.split('/')[-1]}

@freezer.register_generator
def portfolio_generator():
    for lang in SUPPORTED_LANGS:
        for c in flatpages:
            if c.path.startswith(PORT_DIR) or c.path.startswith(f"{DEFAULT_LANG}/{PORT_DIR}"):
                yield {'lang': lang, 'name': c.path.split('/')[-1]}

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='127.0.0.1', port=8000, debug=True)