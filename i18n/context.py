from .core import detect_lang_from_request
from .translations import get_translation

def inject_i18n_helpers():
    lang = detect_lang_from_request()

    def t(key):
        return get_translation(lang, key)

    return {"t": t, "current_lang": lang}
