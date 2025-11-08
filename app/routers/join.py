import re
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.docx_to_html import docx_to_html, sanitize_html, split_message


router = Router()


# --- Главное меню "Вступить в РОО" ---
def get_join_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="Инструкция о приеме в члены", callback_data="join_accept")],
        [InlineKeyboardButton(text="Инструкция о членском билете", callback_data="join_card")],
        [InlineKeyboardButton(text="Инструкция об уплате взносов", callback_data="join_payment")],
        [InlineKeyboardButton(text="Инструкция об учетной карточке", callback_data="join_registry")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# --- Клавиатура "Назад" ---
def back_to_join_menu_keyboard() -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(text="⬅️ Назад", callback_data="join_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


@router.callback_query(F.data == "join_menu")
async def join_menu(query: CallbackQuery):
    await query.message.edit_text("🧾 Выберите инструкцию:", reply_markup=get_join_keyboard())


# --- Универсальная функция для отправки DOCX ---
async def send_docx_as_messages(query: CallbackQuery, path: str):
    """Читает DOCX, чистит HTML, делит на части и отправляет в Telegram"""
    html = sanitize_html(docx_to_html(path))
    parts = split_message(html)

    # Отправляем все части по очереди
    for i, part in enumerate(parts, start=1):
        header = f"📄 Часть {i}/{len(parts)}\n\n" if len(parts) > 1 else ""
        # Только последняя часть содержит кнопку "Назад"
        if i == len(parts):
            await query.message.answer(header + part, parse_mode="HTML", reply_markup=back_to_join_menu_keyboard())
        else:
            await query.message.answer(header + part, parse_mode="HTML")


# --- Отдельные инструкции ---
@router.callback_query(F.data == "join_accept")
async def join_accept(query: CallbackQuery):
    await send_docx_as_messages(query, "data/Инструкция о приеме в члены.docx")


@router.callback_query(F.data == "join_card")
async def join_card(query: CallbackQuery):
    await send_docx_as_messages(query, "data/Инструкция о членском билете.docx")


@router.callback_query(F.data == "join_payment")
async def join_payment(query: CallbackQuery):
    await send_docx_as_messages(query, "data/Инструкция об уплате членских взносов.docx")


@router.callback_query(F.data == "join_registry")
async def join_registry(query: CallbackQuery):
    await send_docx_as_messages(query, "data/Инструкция об учетной карточке.docx")
