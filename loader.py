import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Import middlewares
from middlewares.throttling import ThrottlingMiddleware
from middlewares.access import (
    BotStatusMiddleware,
    BanCheckMiddleware,
    ChannelSubscriptionMiddleware,
    BannerMiddleware
)

# Setup middlewares
dp.middleware.setup(ThrottlingMiddleware())
dp.middleware.setup(BotStatusMiddleware())
dp.middleware.setup(BanCheckMiddleware())
dp.middleware.setup(ChannelSubscriptionMiddleware())
dp.middleware.setup(BannerMiddleware())

logger.info("Bot initialized")
