import config
from content.loader import get_pages_for_lang

def register_generators(freezer):
    @freezer.register_generator
    def index_generator():
        for lang in config.SUPPORTED_LANGS:
            yield "main.index", {"lang": lang}

    @freezer.register_generator
    def blog_generator():
        for lang in config.SUPPORTED_LANGS:
            for p in get_pages_for_lang(lang, config.POST_DIR):
                yield "main.blog", {"lang": lang, "name": p.path.split("/")[-1]}

    @freezer.register_generator
    def portfolio_generator():
        for lang in config.SUPPORTED_LANGS:
            for c in get_pages_for_lang(lang, config.PORT_DIR):
                yield "main.portfolio", {"lang": lang, "name": c.path.split("/")[-1]}
