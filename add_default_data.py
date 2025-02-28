import os
import sys
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_path():
    """Get the absolute path to the database file"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'data', 'database.db')
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    return db_path

def add_default_currencies(conn):
    """Add default cryptocurrencies and fiat currencies"""
    cursor = conn.cursor()
    
    # Default cryptocurrencies
    crypto_currencies = [
        ('Bitcoin (BTC)', 'crypto', '0.001', '10', 'The original cryptocurrency'),
        ('Ethereum (ETH)', 'crypto', '0.01', '100', 'Smart contract platform'),
        ('Tether (USDT)', 'crypto', '10', '10000', 'Stablecoin pegged to USD'),
        ('BNB', 'crypto', '0.1', '100', 'Binance ecosystem token'),
        ('XRP', 'crypto', '10', '10000', 'Fast and low-cost digital asset'),
    ]
    
    # Default fiat currencies
    fiat_currencies = [
        ('USD', 'fiat', '10', '10000', 'US Dollar'),
        ('EUR', 'fiat', '10', '10000', 'Euro'),
        ('RUB', 'fiat', '1000', '1000000', 'Russian Ruble'),
        ('GBP', 'fiat', '10', '10000', 'British Pound'),
        ('JPY', 'fiat', '1000', '1000000', 'Japanese Yen'),
    ]
    
    # Add cryptocurrencies
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
    
    conn.commit()

def add_default_payment_methods(conn):
    """Add default payment methods"""
    cursor = conn.cursor()
    
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
    
    conn.commit()

def main():
    """Main function to add default data to the database"""
    try:
        # Get database path
        db_path = get_db_path()
        logger.info(f"Using database at: {db_path}")
        
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
        
        logger.info("Default data added successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Error adding default data: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
