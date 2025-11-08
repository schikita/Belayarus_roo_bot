from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.docx_to_html import docx_to_html, sanitize_html, split_message

router = Router()

# --- Меню "Вступить в РОО" ---
def get_join_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="Инструкция о приеме в члены", callback_data="join_accept")],
        [InlineKeyboardButton(text="Инструкция о членском билете", callback_data="join_card")],
        [InlineKeyboardButton(text="Инструкция об уплате взносов", callback_data="join_payment")],
        [InlineKeyboardButton(text="Инструкция об учетной карточке", callback_data="join_registry")],
        # эта "Назад" ведёт в главное меню
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# --- Клавиатура "Назад в главное меню" после инструкции ---
def back_to_main_menu_keyboard() -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


@router.callback_query(F.data == "join_menu")
async def join_menu(query: CallbackQuery):
    await query.message.edit_text("🧾 Выберите инструкцию:", reply_markup=get_join_keyboard())


# --- Универсальная отправка DOCX ---
async def send_docx_as_messages(query: CallbackQuery, path: str):
    html = sanitize_html(docx_to_html(path))
    parts = split_message(html)

    for i, part in enumerate(parts, start=1):
        header = f"📄 Часть {i}/{len(parts)}\n\n" if len(parts) > 1 else ""
        if i == len(parts):
            # последняя часть — с кнопкой "Назад" в ГЛАВНОЕ меню
            await query.message.answer(
                header + part,
                parse_mode="HTML",
                reply_markup=back_to_main_menu_keyboard(),
            )
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
