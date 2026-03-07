---
lang: en
title: Flask from Scratch
date: 2022-06-14
description: View functions and routes
tag: flask
project: Flask Course for Beginners
platform: Flask Workshop
link: http://example.com
---

You can start learning Flask with a simple “Hello World” application:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == "__main__":
    app.run()
```

Run the application with:

```bash
python main.py
```
