import os

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"
FLATPAGES_ROOT = "content"
FREEZER_BASE_URL = "https://Vadimchik.github.io/flask_i18n_pf"

POST_DIR = "posts"
PORT_DIR = "portfolio"

SUPPORTED_LANGS = ["ru", "en", "uk"]
DEFAULT_LANG = "ru"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
I18N_DIR = os.path.join(BASE_DIR, "i18n")
