import config

PAGES_BY_LANG = {}
_flatpages_ref = None

def init_loader(flatpages):
    global _flatpages_ref
    _flatpages_ref = flatpages

def build_cache():
    global PAGES_BY_LANG
    if not _flatpages_ref:
        return
        
    PAGES_BY_LANG.clear()
    
    for lang in config.SUPPORTED_LANGS:
        PAGES_BY_LANG[lang] = {}
        for section in [config.POST_DIR, config.PORT_DIR]:
            
            localized_prefix = f"{lang}/{section}"
            localized_pages = [p for p in _flatpages_ref if p.path.startswith(localized_prefix)]
            
            if localized_pages:
                PAGES_BY_LANG[lang][section] = localized_pages
                continue
                
            if lang == config.DEFAULT_LANG:
                PAGES_BY_LANG[lang][section] = [p for p in _flatpages_ref if p.path.startswith(section)]
                continue
                
            default_localized_prefix = f"{config.DEFAULT_LANG}/{section}"
            fallback_pages = [
                p
                for p in _flatpages_ref
                if p.path.startswith(default_localized_prefix) or p.path.startswith(section)
            ]
            PAGES_BY_LANG[lang][section] = fallback_pages

def get_pages_for_lang(lang, section):
    if not PAGES_BY_LANG:
        build_cache()
    
    # Защита от неверных входных данных
    if lang not in PAGES_BY_LANG or section not in PAGES_BY_LANG[lang]:
        return []
        
    return PAGES_BY_LANG[lang][section]

def get_page_by_name(lang, section, name):
    candidates = [f"{lang}/{section}/{name}"]

    if lang == config.DEFAULT_LANG:
        candidates.append(f"{section}/{name}")
    else:
        candidates.append(f"{config.DEFAULT_LANG}/{section}/{name}")
        candidates.append(f"{section}/{name}")

    for path in candidates:
        page = _flatpages_ref.get(path)
        if page:
            return page

    return None
