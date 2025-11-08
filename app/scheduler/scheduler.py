import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from aiogram import Bot

# Get a logger for the scheduler
scheduler_logger = logging.getLogger(__name__)


async def send_periodic_message(bot: Bot, chat_id: str):
    """
    An example job that sends a message to a specific chat.

    You would replace this with whatever task you want to run periodically.
    """
    try:
        scheduler_logger.info(
            f"Attempting to send a scheduled message to chat_id: {chat_id}"
        )
        await bot.send_message(chat_id, "This is a periodic message from your bot!")
        scheduler_logger.info("Message sent successfully.")
    except Exception as e:
        scheduler_logger.error(
            f"Failed to send scheduled message to chat_id: {chat_id}. Error: {e}"
        )


def schedule_jobs(bot: Bot):
    """
    Initializes and starts the scheduler for bot jobs.
    """
    # Initialize the scheduler
    scheduler = AsyncIOScheduler()

    # The chat ID where the message will be sent.
    # You MUST replace this with the actual chat ID you want to use.
    # You can get a chat ID by sending a message to your bot and checking the update object.
    your_chat_id = "7401668825"

    # Add the job to the scheduler.
    # This job will call the `send_periodic_message` function every 60 seconds.
    # The arguments `bot` and `your_chat_id` are passed to the function.
    scheduler.add_job(
        send_periodic_message,
        trigger=IntervalTrigger(seconds=60),
        kwargs={"bot": bot, "chat_id": your_chat_id},
        id="periodic_message_job",
    )

    # Start the scheduler
    scheduler.start()
    scheduler_logger.info("Scheduler started successfully.")
