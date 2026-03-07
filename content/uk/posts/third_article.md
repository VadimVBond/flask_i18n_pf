---
lang: uk
title: Flask з нуля
date: 2022-06-14
description: Функції представлення та маршрути
tag: flask
project: Курс Flask для початківців
platform: Flask Практикум
link: http://example.com
---

Почати знайомство з Flask можна з простого застосунку “Hello World”:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == "__main__":
    app.run()
```

Запуск:

```bash
python main.py
```
