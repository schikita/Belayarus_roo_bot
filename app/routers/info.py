import re
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from app.utils.docx_to_html import docx_to_html

router = Router()

# --- Функция очистки HTML от неподдерживаемых тегов ---
def sanitize_html(text: str) -> str:
    """Удаляет неподдерживаемые Telegram HTML-теги."""
    text = re.sub(r"</?(p|div|span|br)[^>]*>", "", text)
    text = text.replace("&nbsp;", " ")
    return text.strip()

# --- Меню "Информация" ---
def get_info_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="О нас", callback_data="info_about")],
        [InlineKeyboardButton(text="Наши инициативы", callback_data="info_initiatives")],
        [InlineKeyboardButton(text="Прием граждан", callback_data="info_citizens")],
        [InlineKeyboardButton(text="Устав", callback_data="info_statute")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


@router.callback_query(F.data == "info_menu")
async def info_menu(query: CallbackQuery):
    await query.message.edit_text("📘 Выберите раздел:", reply_markup=get_info_keyboard())


# --- Отдельные документы ---
@router.callback_query(F.data == "info_about")
async def info_about(query: CallbackQuery):
    html = sanitize_html(docx_to_html("data/О нас.docx"))
    await query.message.answer(html, parse_mode="HTML")


@router.callback_query(F.data == "info_initiatives")
async def info_initiatives(query: CallbackQuery):
    html = sanitize_html(docx_to_html("data/Наши инициативы.docx"))
    await query.message.answer(html, parse_mode="HTML")


@router.callback_query(F.data == "info_citizens")
async def info_citizens(query: CallbackQuery):
    html = sanitize_html(docx_to_html("data/Прием граждан.docx"))
    await query.message.answer(html, parse_mode="HTML")


@router.callback_query(F.data == "info_statute")
async def info_statute(query: CallbackQuery):
    """Отправляет PDF-файл Устава пользователю."""
    try:
        pdf_path = "data/Устав РОО «Белая Русь».pdf"
        pdf_file = InputFile(pdf_path)
        await query.message.answer_document(pdf_file, caption="📜 Устав РОО «Белая Русь»")
    except FileNotFoundError:
        await query.message.answer("⚠️ Файл Устава временно недоступен. Попробуйте позже.")
