import asyncio
import logging
from functools import partial

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncEngine

from app.config import settings
from app.db import engine, Base
from app.scheduler.scheduler import schedule_jobs

# Импорт всех роутеров
from app.routers import base, info, feedback, promo, join
from aiogram.client.default import DefaultBotProperties

# Настройка логирования
logging.basicConfig(level=logging.INFO)
bot_logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, engine: AsyncEngine):
    """
    Создает таблицы БД при запуске (если их ещё нет).
    """
    bot_logger.info("Bot is starting up...")
    async with engine.begin() as conn:
        bot_logger.info("Creating database tables if they do not exist...")
        await conn.run_sync(Base.metadata.create_all)
    bot_logger.info("Startup complete!")


async def main():
    """
    Главная функция запуска Telegram-бота.
    """
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode="HTML"))

    # Настройка хранилища состояния (Redis или память)
    if settings.redis_url:
        try:
            r = redis.from_url(settings.redis_url)
            storage = RedisStorage(r)
            bot_logger.info("Using Redis for storage.")
        except Exception as e:
            bot_logger.error(
                f"Failed to connect to Redis, using MemoryStorage. Error: {e}"
            )
            storage = MemoryStorage()
    else:
        storage = MemoryStorage()
        bot_logger.info("Using MemoryStorage.")

    dp = Dispatcher(storage=storage)

    # Подключаем все роутеры (важно: порядок не критичен)
    dp.include_routers(
        base.router,
        info.router,
        feedback.router,
        promo.router,
        join.router,
    )

    # Регистрируем startup-хук
    dp.startup.register(partial(on_startup, bot, engine))

    # Запускаем планировщик (если нужен)
    schedule_jobs(bot)

    # Запуск бота
    bot_logger.info("Starting bot polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        bot_logger.info("Bot stopped by user.")
