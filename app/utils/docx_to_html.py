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
