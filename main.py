import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncEngine
import logging

from functools import partial

# Set up logging for the bot
logging.basicConfig(level=logging.INFO)
bot_logger = logging.getLogger(__name__)

# Import all necessary components from your project's subdirectories
from app.config import settings
from app.db import engine, Base
from app.routers import base_router, info_router, feedback_router, promo_router
from app.scheduler.scheduler import schedule_jobs 

async def on_startup(bot: Bot, engine: AsyncEngine):
    """
    Performs startup tasks, such as creating database tables.
    This function will be called automatically by the dispatcher when the bot starts.
    """
    bot_logger.info("Bot is starting up...")
    async with engine.begin() as conn:
        bot_logger.info("Creating database tables if they do not exist...")
        await conn.run_sync(Base.metadata.create_all)
    bot_logger.info("Startup complete!")
        
async def main():
    """
    Main function to initialize and start the bot.
    """
    # Initialize the bot with its token from settings
    bot = Bot(token=settings.bot_token)
    
    # Configure storage for your bot's state
    # This checks if you have a Redis URL set up, which is good for larger projects.
    if settings.redis_url:
        try:
            r = redis.from_url(settings.redis_url)
            storage = RedisStorage(r)
            bot_logger.info("Using Redis for storage.")
        except Exception as e:
            bot_logger.error(f"Failed to connect to Redis, using MemoryStorage. Error: {e}")
            storage = MemoryStorage()
    else:
        storage = MemoryStorage()
        bot_logger.info("Using MemoryStorage.")
        
    # Initialize the Dispatcher with the chosen storage
    dp = Dispatcher(storage=storage)
    
    # Include your routers. These contain all the command and message handlers.
    dp.include_router(base_router)
    dp.include_router(info_router)
    dp.include_router(feedback_router)
    dp.include_router(promo_router)
    
    # Register the startup handler. We use a lambda to pass the necessary arguments.
    dp.startup.register(partial(on_startup, bot, engine))
    
    # Start the scheduled jobs (like sending a message at a specific time)
    schedule_jobs(bot)
    
    # Start polling for updates from Telegram
    bot_logger.info("Starting bot polling...")
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        # Run the main function
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        bot_logger.info("Bot stopped by user.")
