from pathlib import Path
import yaml

SOURCE_LANG = 'ru'
TARGET_LANGS = ['en', 'uk']
CONTENT_DIR = Path('content')
POST_DIR = 'posts'
PORT_DIR = 'portfolio'

def process_files(subdir):
    source_path = CONTENT_DIR / SOURCE_LANG / subdir

    for target_lang in TARGET_LANGS:
        target_path = CONTENT_DIR / target_lang / subdir
        target_path.mkdir(parents=True, exist_ok=True)

        for md_file in source_path.glob("*.md"):
            with md_file.open("r", encoding="utf8") as f:
                content = f.read()

            # Разделяем front-matter и тело
            if content.startswith("---"):
                parts = content.split("---", 2)
                front_matter = yaml.safe_load(parts[1])
                body = parts[2].strip()
            else:
                front_matter = {}
                body = content

            # Обновляем front-matter
            front_matter['lang'] = target_lang

            # Сохраняем новый файл (пока с тем же русским текстом)
            new_content = f"---\n{yaml.safe_dump(front_matter, allow_unicode=True)}---\n{body}\n"
            target_file = target_path / md_file.name

            with target_file.open("w", encoding="utf8") as f:
                f.write(new_content)

            print(f"Создан i18n-файл: {target_file}")

# Применяем к posts и portfolio
process_files(POST_DIR)
process_files(PORT_DIR)

print("Подготовка структуры i18n завершена.")