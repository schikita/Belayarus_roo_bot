from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.docx_to_html import docx_to_html

router = Router()

# --- Меню "Вступить в РОО" ---
def get_join_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="Инструкция о приеме в члены", callback_data="join_accept")],
        [InlineKeyboardButton(text="Инструкция о членском билете", callback_data="join_card")],
        [InlineKeyboardButton(text="Инструкция об уплате взносов", callback_data="join_payment")],
        [InlineKeyboardButton(text="Инструкция об учетной карточке", callback_data="join_registry")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


@router.callback_query(F.data == "join_menu")
async def join_menu(query: CallbackQuery):
    await query.message.edit_text("🧾 Выберите инструкцию:", reply_markup=get_join_keyboard())


# --- Отдельные документы ---
@router.callback_query(F.data == "join_accept")
async def join_accept(query: CallbackQuery):
    html = docx_to_html("data/Инструкция о приеме в члены.doc")
    await query.message.answer(html, parse_mode="HTML")


@router.callback_query(F.data == "join_card")
async def join_card(query: CallbackQuery):
    html = docx_to_html("data/Инструкция о членском билете.doc")
    await query.message.answer(html, parse_mode="HTML")


@router.callback_query(F.data == "join_payment")
async def join_payment(query: CallbackQuery):
    html = docx_to_html("data/Инструкция об уплате членских взносов.docx")
    await query.message.answer(html, parse_mode="HTML")


@router.callback_query(F.data == "join_registry")
async def join_registry(query: CallbackQuery):
    html = docx_to_html("data/Инструкция об учетной карточке.doc")
    await query.message.answer(html, parse_mode="HTML")
