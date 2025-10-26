from aiogram import Router, F
from aiogram.types import Message

router = Router()

INFO_TEXT = (
    'Справочная информация:\n'
    '- Контакты: ...\n'
    '- Адреса отделений ...\n'
    '- Частые вопросы: ...'
)

@router.message(F.text.in_({'ℹ️ Справка', '/info'}))
async def  info(message: Message):
    await message.answer(INFO_TEXT)