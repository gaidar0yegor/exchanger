import logging
import sys
import os
import sqlite3
from aiogram import executor

from loader import dp, bot
import handlers
from utils.set_commands import set_default_commands
from data.config import AUTHOR, VERSION
from add_default_data import add_default_currencies, add_default_payment_methods

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
    
    # Add default currencies and payment methods
    try:
        # Get database path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'data', 'database.db')
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        
        # Create tables if they don't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
                name TEXT PRIMARY KEY,
                type TEXT,
                min_amount TEXT,
                max_amount TEXT,
                details TEXT
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payment_methods (
                name TEXT PRIMARY KEY,
                type TEXT
            )
        """)
        
        # Add default data
        add_default_currencies(conn)
        add_default_payment_methods(conn)
        
        # Close connection
        conn.close()
        
        logger.info("Default currencies and payment methods added")
    except Exception as e:
        logger.error(f"Error adding default data: {e}")
    
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
