---
lang: en
title: Getting Started with Flask
date: 2022-06-12
description: Reviewing the core concepts and capabilities of the framework
tag: flask
project: Flask Course for Beginners
platform: Flask Workshop
link: http://example.com
---

## Creating a Flask application

Every Flask application needs an instance of the `Flask` class. This instance is a WSGI application: the server forwards incoming requests to it for processing.

```python
from flask import Flask

app = Flask(__name__)
```

In the first line, we import `Flask` from the `flask` package. In the second line, we create an application object and pass `__name__` to the constructor so Flask can locate templates and static files.

## Creating routes

A route binds a URL to a view function that returns a response.

```python
@app.route('/')
def index():
    return 'Hello World'
```

This code assigns `index()` to the root URL (`/`). Whenever the application receives a request to `/`, Flask calls this function and returns the result.
