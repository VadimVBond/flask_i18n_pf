# Personal Portfolio & Blog

🌐 **Languages:**
[English](#english) | [Русский](#русский) | [Українська](#українська)

---

## English

### Personal Portfolio and Blog

This repository contains a **personal portfolio and blog website** built with Flask and Flat-Pages.
The project supports **internationalization (i18n)** and can be deployed as a **static site to GitHub Pages**.

### Features

* **Blog & Portfolio** — clean interface for articles and project showcases
* **Internationalization (i18n)** — English, Russian, Ukrainian
* **Static Site Generation** — powered by Flask-Frozen
* **GitHub Pages Deployment** — automatic deployment via GitHub Actions
* **Markdown Content** — posts and pages written in Markdown

### Installation

Clone the repository:

```bash
git clone https://github.com/Vadimchik/flask_i18n_pf.git
cd flask_i18n_pf
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Usage

Run the development server:

```bash
python mysite.py
```

The site will be available at:

```
http://127.0.0.1:8000/
```

Build the static version:

```bash
python mysite.py build
```

The generated static files will appear in the `build/` directory.

### Deployment

The project automatically deploys to **GitHub Pages** when changes are pushed to the `main` branch.

The workflow configuration is located in:

```
.github/workflows/gh-pages.yml
```

---

## Русский

### Персональное портфолио и блог

Этот репозиторий содержит **персональный сайт-портфолио и блог**, созданный на Flask и Flat-Pages.
Проект поддерживает **многоязычность (i18n)** и может быть развёрнут как **статический сайт на GitHub Pages**.

### Особенности

* **Блог и портфолио** — интерфейс для публикации статей и проектов
* **Поддержка i18n** — английский, русский, украинский
* **Генерация статического сайта** — с использованием Flask-Frozen
* **Автоматическое развёртывание** — через GitHub Actions
* **Markdown-контент** — страницы и статьи пишутся в Markdown

### Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/Vadimchik/flask_i18n_pf.git
cd flask_i18n_pf
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### Использование

Запуск сервера разработки:

```bash
python mysite.py
```

Сайт будет доступен по адресу:

```
http://127.0.0.1:8000/
```

Сборка статического сайта:

```bash
python mysite.py build
```

Статические файлы будут сгенерированы в каталоге `build/`.

### Развёртывание

Сайт автоматически публикуется на **GitHub Pages** при отправке изменений в ветку `main`.

Файл конфигурации workflow:

```
.github/workflows/gh-pages.yml
```

---

## Українська

### Персональне портфоліо та блог

Цей репозиторій містить **персональний сайт-портфоліо та блог**, створений з використанням Flask та Flat-Pages.
Проєкт підтримує **багатомовність (i18n)** і може бути розгорнутий як **статичний сайт на GitHub Pages**.

### Особливості

* **Блог і портфоліо** — інтерфейс для статей і проєктів
* **Підтримка i18n** — англійська, російська, українська
* **Генерація статичного сайту** — через Flask-Frozen
* **Автоматичне розгортання** — GitHub Actions
* **Markdown-контент** — сторінки та статті пишуться у Markdown

### Встановлення

Клонуйте репозиторій:

```bash
git clone https://github.com/Vadimchik/flask_i18n_pf.git
cd flask_i18n_pf
```

Встановіть залежності:

```bash
pip install -r requirements.txt
```

### Використання

Запуск сервера розробки:

```bash
python mysite.py
```

Сайт буде доступний за адресою:

```
http://127.0.0.1:8000/
```

Збірка статичного сайту:

```bash
python mysite.py build
```

Статичні файли будуть створені у каталозі `build/`.

### Розгортання

Сайт автоматично публікується на **GitHub Pages** після пушу у гілку `main`.

Файл workflow:

```
.github/workflows/gh-pages.yml
```
