import logging
import sys
from aiogram import executor

from loader import dp, bot
import handlers
from utils.set_commands import set_default_commands
from data.config import AUTHOR, VERSION

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def on_startup(dispatcher):
    """
    Function that runs when the bot starts
    """
    # Set default commands
    await set_default_commands(dispatcher)
    
    # Log startup
    logger.info("Bot started successfully!")
    
    # Get bot info
    bot_info = await bot.get_me()
    logger.info(f"Bot: {bot_info.full_name} [@{bot_info.username}]")
    logger.info(f"Version: {VERSION}")
    logger.info(f"Developer: {AUTHOR}")

async def on_shutdown(dispatcher):
    """
    Function that runs when the bot shuts down
    """
    logger.info("Bot shutting down...")
    
    # Close storage
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    
    logger.info("Bot shutdown complete!")

if __name__ == '__main__':
    logger.info("Starting bot...")
    
    # Start the bot
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )
