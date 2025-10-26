from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from app.db import session_scope
from app import models

router = Router()

class FeedbackFSM(StatesGroup):
    waiting_message = State()
    
@router.message(F.text.in_({'✉️ Обратная связь', '/feedback'}))
async def feedback_entry(message: Message, state: FSMContext):
    await state.set_state(FeedbackFSM.waiting_message)
    await message.answer('Опишите вашу обратную связь одним сообщением и отправьте:')
    
@router.message(FeedbackFSM.waiting_message)
async def feedback_save(message: Message, state: FSMContext):
    text = message.text or ''
    if not text.strip():
        await message.answer('Пустое сообщение не принимается, пожалуйста, напишите текст.')
        return
    
    async with session_scope() as s:
        user = await s.get(models.User, message.from_user.id)
        if not user:
            user = models.User(
                id=message.from_user.id,
                username=message.from_user.username
            )
            s.add(user)
        fb = models.FeedBack(user_id = message.from_user.id, message=text)
        s.add(fb)
    
    await state.clear()
    await message.answer('Спасибо! Ваше сообщение получено.')
         