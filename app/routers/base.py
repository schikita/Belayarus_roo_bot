from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from app.keyboards import get_info_keyboard # Make sure to import the keyboard function

router = Router()

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='ℹ️ Справка', callback_data='info_menu'),
            InlineKeyboardButton(text='🗳 Агитация', callback_data='promo_info')
        ],
        [
            InlineKeyboardButton(text='✉️ Обратная связь', callback_data='feedback_form')
        ],
        [
            InlineKeyboardButton(text='📅 Мероприятия', callback_data='events'),
            InlineKeyboardButton(text='📜 Устав', callback_data='statute')
        ],
    ],
)

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    """
    Handles the /start command and sends a welcome message with a keyboard.
    """
    await message.answer(
        "Привет! Я готов к работе. Выбери одну из опций ниже:",
        reply_markup=main_kb
    )

@router.callback_query(F.data == "info_menu")
async def show_info_menu(query: CallbackQuery):
    """
    Handles the "ℹ️ Справка" button click and shows the info menu keyboard.
    """
    await query.message.answer(
        "Справочная информация:",
        reply_markup=get_info_keyboard()
    )
    await query.answer()

@router.callback_query(F.data == "promo_info")
async def show_promo_info(query: CallbackQuery):
    """
    Handles the "🗳 Агитация" button click.
    """
    await query.message.answer("Здесь будет информация об агитации.")
    await query.answer()

@router.callback_query(F.data == "feedback_form")
async def show_feedback_form(query: CallbackQuery):
    """
    Handles the "✉️ Обратная связь" button click.
    """
    await query.message.answer("Здесь будет форма обратной связи.")
    await query.answer()

@router.callback_query(F.data == "events")
async def show_events(query: CallbackQuery):
    """
    Handles the "Мероприятия" button click.
    """
    await query.message.answer("Здесь будет информация о предстоящих мероприятиях.")
    await query.answer()

@router.callback_query(F.data == "statute")
async def show_statute(query: CallbackQuery):
    """
    Handles the "Устав" button click.
    """
    await query.message.answer("Здесь будет текст устава.")
    await query.answer()
