import re
from docx import Document
from pathlib import Path


def docx_to_html(file_path: str) -> str:
    """Преобразует .docx или .doc в HTML для Telegram."""
    path = Path(file_path)
    if not path.exists():
        return f"<b>Файл не найден:</b> {path.name}"

    doc = Document(path)
    html = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            html.append("<br>")
            continue

        style = para.style.name.lower()

        if "heading" in style:
            html.append(f"<h3>{text}</h3>")
        elif "title" in style:
            html.append(f"<h2>{text}</h2>")
        else:
            html.append(f"<p>{text}</p>")

    return "\n".join(html)


def sanitize_html(text: str) -> str:
    """
    Чистит HTML от неподдерживаемых тегов Telegram и исправляет разметку.
    """

    # Заменяем <br> и <br > на переносы строк
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    # Удаляем теги <p>, <div>, <span> и их закрывающие версии
    text = re.sub(
        r"</?(p|div|span|font|strong|em)[^>]*>", "", text, flags=re.IGNORECASE
    )

    # Удаляем любые другие HTML-теги, кроме разрешённых Telegram
    text = re.sub(r"</?(?!b|i|u|a|code|pre)[^>]+>", "", text)

    # Исправляем незакрытые теги <b>, <i> и т.п.
    text = re.sub(r"<b>([^<]*)$", r"<b>\1</b>", text)
    text = re.sub(r"<i>([^<]*)$", r"<i>\1</i>", text)
    text = re.sub(r"<u>([^<]*)$", r"<u>\1</u>", text)

    # Удаляем множественные переводы строк
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Убираем пробелы в начале и конце
    text = text.strip()

    return text


def split_message(text: str, limit: int = 4000) -> list[str]:
    """
    Разбивает длинный текст на части, чтобы не превышать лимит Telegram (4096 символов).
    Разбивает по строкам или пробелам, не обрезая слова.
    """
    parts = []
    while len(text) > limit:
        split_index = text.rfind("\n", 0, limit)
        if split_index == -1:
            split_index = text.rfind(" ", 0, limit)
        if split_index == -1:
            split_index = limit
        parts.append(text[:split_index].strip())
        text = text[split_index:].strip()
    parts.append(text)
    return parts
