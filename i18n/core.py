from flask import request
import config

def detect_lang_from_request():
    lang = request.view_args.get("lang") if request.view_args else None
    if lang in config.SUPPORTED_LANGS:
        return lang

    path_lang = request.path.strip("/").split("/", 1)[0]
    if path_lang in config.SUPPORTED_LANGS:
        return path_lang

    return config.DEFAULT_LANG
