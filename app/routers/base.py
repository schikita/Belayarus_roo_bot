from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

router = Router()

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ℹ️ Информация", callback_data="info_menu"),
            InlineKeyboardButton(text="🧾 Вступить в РОО", callback_data="join_menu"),
        ],
        [InlineKeyboardButton(text="✉️ Обратная связь", callback_data="feedback_form")],
        [
            InlineKeyboardButton(text="📅 Мероприятия", callback_data="events"),
            InlineKeyboardButton(text="📜 Устав", callback_data="info_statute"),
        ],
    ],
)


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "🇧🇾 Приветствую! Я — официальный бот Республиканского общественного объединения «Белая Русь»!\n\n"
        "Здесь Вы можете узнать о нашей деятельности, ознакомиться с процессом вступления в наши ряды и написать нам сообщение.\n\n"
        "Выберите один из разделов ниже:",
        reply_markup=main_kb,
    )


@router.callback_query(F.data == "events")
async def show_events(query: CallbackQuery):
    await query.message.answer("📅 Здесь будет информация о мероприятиях.")
    await query.answer()


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(query: CallbackQuery):
    """Возвращает пользователя в главное меню."""
    await query.message.edit_text(
        "🇧🇾 Приветствую! Я — официальный бот Республиканского общественного объединения «Белая Русь»!\n\n"
        "Здесь Вы можете узнать о нашей деятельности, ознакомиться с процессом вступления в наши ряды и написать нам сообщение.\n\n"
        "Выберите один из разделов ниже:",
        reply_markup=main_kb,
    )
    await query.answer()
