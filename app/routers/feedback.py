import os
import ast
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from app.db import session_scope
from app import models
from aiogram import Bot
from aiogram.types import CallbackQuery

router = Router()

# --- Загружаем список админов из .env ---
BOT_ADMINS = ast.literal_eval(os.getenv("BOT_ADMINS", "[]"))


class FeedbackFSM(StatesGroup):
    waiting_message = State()


@router.callback_query(F.data == "feedback_form")
async def feedback_start_callback(query: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Обратная связь' в меню."""
    await state.set_state(FeedbackFSM.waiting_message)
    await query.message.answer("✉️ Напишите ваше сообщение одним текстом и отправьте.")
    await query.answer()

@router.message(F.text.in_({'✉️ Обратная связь', '/feedback'}))
async def feedback_entry(message: Message, state: FSMContext):
    await state.set_state(FeedbackFSM.waiting_message)
    await message.answer('Опишите вашу обратную связь одним сообщением и отправьте:')


@router.message(FeedbackFSM.waiting_message)
async def feedback_save(message: Message, state: FSMContext, bot: Bot):
    text = (message.text or "").strip()
    if not text:
        await message.answer('Пустое сообщение не принимается, пожалуйста, напишите текст.')
        return

    # Сохраняем в БД
    async with session_scope() as s:
        user = await s.get(models.User, message.from_user.id)
        if not user:
            user = models.User(
                id=message.from_user.id,
                username=message.from_user.username
            )
            s.add(user)
        fb = models.FeedBack(user_id=message.from_user.id, message=text)
        s.add(fb)

    await state.clear()
    await message.answer('Спасибо! Ваше сообщение получено. Мы свяжемся с вами при необходимости.')

    # --- Отправляем администраторам ---
    for admin_id in BOT_ADMINS:
        try:
            user_info = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    f"📬 *Новое сообщение обратной связи:*\n\n"
                    f"{text}\n\n"
                    f"👤 От пользователя: {user_info}"
                ),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение админу {admin_id}: {e}")
