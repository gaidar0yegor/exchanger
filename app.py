import logging
import sys
import os
import sqlite3
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
        
        # Add default cryptocurrencies
        crypto_currencies = [
            ('Bitcoin (BTC)', 'crypto', '0.001', '10', 'The original cryptocurrency'),
            ('Ethereum (ETH)', 'crypto', '0.01', '100', 'Smart contract platform'),
            ('Tether (USDT)', 'crypto', '10', '10000', 'Stablecoin pegged to USD'),
            ('BNB', 'crypto', '0.1', '100', 'Binance ecosystem token'),
            ('XRP', 'crypto', '10', '10000', 'Fast and low-cost digital asset'),
        ]
        
        # Add default fiat currencies
        fiat_currencies = [
            ('USD', 'fiat', '10', '10000', 'US Dollar'),
            ('EUR', 'fiat', '10', '10000', 'Euro'),
            ('RUB', 'fiat', '1000', '1000000', 'Russian Ruble'),
            ('GBP', 'fiat', '10', '10000', 'British Pound'),
            ('JPY', 'fiat', '1000', '1000000', 'Japanese Yen'),
        ]
        
        # Add cryptocurrencies
        cursor = conn.cursor()
        for currency in crypto_currencies:
            try:
                cursor.execute(
                    'INSERT INTO currencies VALUES (?, ?, ?, ?, ?)',
                    currency
                )
                logger.info(f"Added cryptocurrency: {currency[0]}")
            except sqlite3.IntegrityError:
                logger.info(f"Cryptocurrency already exists: {currency[0]}")
        
        # Add fiat currencies
        for currency in fiat_currencies:
            try:
                cursor.execute(
                    'INSERT INTO currencies VALUES (?, ?, ?, ?, ?)',
                    currency
                )
                logger.info(f"Added fiat currency: {currency[0]}")
            except sqlite3.IntegrityError:
                logger.info(f"Fiat currency already exists: {currency[0]}")
        
        # Default crypto payment methods
        crypto_methods = [
            ('Bitcoin Address', 'crypto'),
            ('Ethereum Address', 'crypto'),
            ('USDT TRC20', 'crypto'),
            ('USDT ERC20', 'crypto'),
            ('BNB BEP20', 'crypto'),
        ]
        
        # Default fiat payment methods
        fiat_methods = [
            ('Bank Transfer', 'fiat'),
            ('Credit Card', 'fiat'),
            ('PayPal', 'fiat'),
            ('Revolut', 'fiat'),
            ('Wise', 'fiat'),
        ]
        
        # Add crypto payment methods
        for method in crypto_methods:
            try:
                cursor.execute(
                    'INSERT INTO payment_methods VALUES (?, ?)',
                    method
                )
                logger.info(f"Added crypto payment method: {method[0]}")
            except sqlite3.IntegrityError:
                logger.info(f"Payment method already exists: {method[0]}")
        
        # Add fiat payment methods
        for method in fiat_methods:
            try:
                cursor.execute(
                    'INSERT INTO payment_methods VALUES (?, ?)',
                    method
                )
                logger.info(f"Added fiat payment method: {method[0]}")
            except sqlite3.IntegrityError:
                logger.info(f"Payment method already exists: {method[0]}")
        
        # Commit changes and close connection
        conn.commit()
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
