import os
import json
import config

_translations_cache = {}

def load_translations():
    global _translations_cache
    for lang in config.SUPPORTED_LANGS:
        filepath = os.path.join(config.I18N_DIR, f"{lang}.json")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                _translations_cache[lang] = json.load(f)
        except Exception as e:
            print(f"Warning: could not load translation for {lang}: {e}")
            _translations_cache[lang] = {}

def get_translation(lang, key):
    if not _translations_cache:
        load_translations()
    
    # Сначала ищем ключ в текущем языке
    if lang in _translations_cache and key in _translations_cache[lang]:
        return _translations_cache[lang][key]
    
    # Fallback на DEFAULT_LANG (ru)
    if config.DEFAULT_LANG in _translations_cache and key in _translations_cache[config.DEFAULT_LANG]:
        return _translations_cache[config.DEFAULT_LANG][key]
    
    # Если перевода нигде нет, возвращаем сам ключ
    return key
