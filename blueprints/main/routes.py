import json
from flask import Blueprint, render_template, abort, redirect, url_for
import config
from content.loader import get_pages_for_lang, get_page_by_name
from flask_flatpages import pygments_style_defs

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def root():
    return redirect(url_for("main.index", lang=config.DEFAULT_LANG))

@main_bp.route("/<lang>/")
def index(lang):
    if lang not in config.SUPPORTED_LANGS:
        abort(404)

    posts = get_pages_for_lang(lang, config.POST_DIR)
    posts.sort(key=lambda item: item.meta.get("date", ""), reverse=True)

    cards = get_pages_for_lang(lang, config.PORT_DIR)
    cards.sort(key=lambda item: item.meta.get("title", ""))

    with open("settings.json", encoding="utf8") as f:
        settings_config = json.load(f)

    settings = dict(settings_config.get("defaults", {}))

    legacy_top_level = {
        key: value
        for key, value in settings_config.items()
        if key not in {"defaults", "locales"}
    }
    settings.update(legacy_top_level)

    localized_overrides = settings_config.get("locales", {}).get(lang, {})
    settings.update(localized_overrides)
    
    tags = set()
    for p in posts:
        t = p.meta.get("tag")
        if t:
            tags.add(t.lower())

    return render_template(
        "index.html",
        posts=posts,
        cards=cards,
        bigheader=True,
        **settings,
        tags=tags,
        lang=lang,
    )

@main_bp.route("/<lang>/blog/<name>/")
def blog(lang, name):
    if lang not in config.SUPPORTED_LANGS:
        abort(404)

    post = get_page_by_name(lang, config.POST_DIR, name)
    if not post:
        abort(404)
    return render_template("post.html", post=post, lang=lang)

@main_bp.route("/<lang>/portfolio/<name>/")
def portfolio(lang, name):
    if lang not in config.SUPPORTED_LANGS:
        abort(404)

    card = get_page_by_name(lang, config.PORT_DIR, name)
    if not card:
        abort(404)
    return render_template("card.html", card=card, lang=lang)

@main_bp.route("/pygments.css")
def pygments_css():
    return pygments_style_defs("monokai"), 200, {"Content-Type": "text/css"}

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
