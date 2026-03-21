import sys
from flask import Flask
from flask_flatpages import FlatPages
from flask_frozen import Freezer

import config
from i18n import inject_i18n_helpers, load_translations
from content.loader import init_loader
from blueprints.main.routes import main_bp
from generators import register_generators

app = Flask(__name__)
app.config.from_object(config)

flatpages = FlatPages(app)
freezer = Freezer(app, with_static_files=True)

# Инициализация
load_translations()
init_loader(flatpages)
register_generators(freezer)

# Подключение Blueprint и Context Processor
app.register_blueprint(main_bp)
app.context_processor(inject_i18n_helpers)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host="127.0.0.1", port=8000, debug=True)
