from aiogram import Router, F
from aiogram.types import Message

router = Router()

PROMO_TEXT = "Информационные материалы:\n" "- Ссылка 1\n" "- Ссылка 2\n" "- Ссылка 3"


@router.message(F.text.in_({"🗳 Агитация", "/promo"}))
async def promo(message: Message):
    await message.answer(PROMO_TEXT)
