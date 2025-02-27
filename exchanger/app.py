import handlers
import logging
from aiogram import executor
from loader import dp
from utils.set_bot_commands import set_default_commands
from data.config import *
from utils.middlware import *
from check_env import check_environment_variables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def on_startup(dispatcher):
    logger.info("Starting bot...")
    await set_default_commands(dispatcher)
    logger.info("Bot started successfully!")

#Разработчики: https://t.me/weaseldev @weaseldev

if __name__ == '__main__':
    # Check environment variables before starting
    if not check_environment_variables():
        logger.error("Environment check failed. Exiting.")
        import sys
        sys.exit(1)
    
    logger.info("Setting up middleware...")
    dp.middleware.setup(OffCallback())
    dp.middleware.setup(OffMessage())
    dp.middleware.setup(SearchBanUserCallback())
    dp.middleware.setup(Ads())
    dp.middleware.setup(SubsribeOnChannelMessage())
    dp.middleware.setup(SubsribeOnChannelCallback())
    dp.middleware.setup(ThrottlingMiddleware())
    
    logger.info("Starting polling...")
    executor.start_polling(dp, on_startup=on_startup)
