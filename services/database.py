import sqlite3
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    """Database service for the Crypto Exchange Bot"""
    
    def __init__(self, db_path='data/database.db'):
        """Initialize the database connection"""
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def __enter__(self):
        """Context manager entry point"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        # Users table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                is_banned INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TEXT
            )
        """)
        
        # Payment methods table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS payment_methods (
                name TEXT PRIMARY KEY,
                type TEXT
            )
        """)
        
        # Currencies table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
                name TEXT PRIMARY KEY,
                type TEXT,
                min_amount TEXT,
                max_amount TEXT,
                details TEXT
            )
        """)
        
        # Channels table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                channel_id TEXT PRIMARY KEY,
                url TEXT
            )
        """)
        
        # Banners table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS banners (
                id TEXT PRIMARY KEY,
                text TEXT
            )
        """)
        
        # Bot status table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS bot_status (
                id TEXT PRIMARY KEY,
                status TEXT
            )
        """)
        
        # Exchange history table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS exchange_history (
                amount TEXT,
                user_id TEXT,
                exchange TEXT,
                date TEXT
            )
        """)
        
        # Initialize bot status if not exists
        try:
            self.cursor.execute('INSERT INTO bot_status VALUES (?, ?)', ['1', 'on'])
            self.connection.commit()
        except sqlite3.IntegrityError:
            pass
    
    # User management methods
    
    def add_user(self, user_id, full_name, username):
        """Add a new user to the database"""
        try:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
                [str(user_id), full_name, username, 0, 1, created_at]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding user to database: {e}")
            return False
    
    def ban_user(self, user_id):
        """Ban a user"""
        try:
            self.cursor.execute(
                'UPDATE users SET is_banned = ? WHERE id = ?',
                [1, str(user_id)]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error banning user: {e}")
            return False
    
    def unban_user(self, user_id):
        """Unban a user"""
        try:
            self.cursor.execute(
                'UPDATE users SET is_banned = ? WHERE id = ?',
                [0, str(user_id)]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error unbanning user: {e}")
            return False
    
    def is_user_banned(self, user_id):
        """Check if a user is banned"""
        try:
            result = self.cursor.execute(
                'SELECT is_banned FROM users WHERE id = ?',
                [str(user_id)]
            ).fetchone()
            return result and result[0] == 1
        except Exception as e:
            logger.error(f"Error checking if user is banned: {e}")
            return False
    
    def deactivate_user(self, user_id):
        """Deactivate a user"""
        try:
            self.cursor.execute(
                'UPDATE users SET is_active = ? WHERE id = ?',
                [0, str(user_id)]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error deactivating user: {e}")
            return False
    
    def get_user_stats(self):
        """Get user statistics"""
        try:
            result = self.cursor.execute('SELECT id, is_active FROM users').fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting user statistics: {e}")
            return []
    
    def get_all_user_ids(self):
        """Get all user IDs"""
        try:
            result = self.cursor.execute('SELECT id FROM users').fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting all user IDs: {e}")
            return []
    
    # Bot status methods
    
    def get_bot_status(self):
        """Get the current bot status"""
        try:
            result = self.cursor.execute('SELECT * FROM bot_status').fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting bot status: {e}")
            return []
    
    def set_bot_status(self, status):
        """Set the bot status (on/off)"""
        try:
            self.cursor.execute(
                'UPDATE bot_status SET status = ? WHERE id = ?',
                [status, '1']
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error setting bot status: {e}")
            return False
    
    # Banner methods
    
    def get_banner(self):
        """Get the current banner"""
        try:
            result = self.cursor.execute('SELECT * FROM banners').fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting banner: {e}")
            return []
    
    def manage_banner(self, action, text=None):
        """Add or remove a banner"""
        try:
            if action == 'add' and text:
                try:
                    self.cursor.execute('INSERT INTO banners VALUES (?, ?)', ['1', text])
                    self.connection.commit()
                    return True
                except Exception:
                    return False
            elif action == 'remove':
                try:
                    self.cursor.execute('DELETE FROM banners WHERE id = ?', ['1'])
                    self.connection.commit()
                    return True
                except Exception:
                    return False
            return False
        except Exception as e:
            logger.error(f"Error managing banner: {e}")
            return False
    
    # Channel methods
    
    def add_channel(self, channel_id, url):
        """Add a channel that users need to subscribe to"""
        try:
            self.cursor.execute(
                'INSERT INTO channels VALUES (?, ?)',
                [str(channel_id), str(url)]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding channel: {e}")
            return False
    
    def delete_channel(self, channel_id):
        """Delete a channel"""
        try:
            self.cursor.execute(
                'DELETE FROM channels WHERE channel_id = ?',
                [str(channel_id)]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting channel: {e}")
            return False
    
    def get_channels(self):
        """Get all channels"""
        try:
            result = self.cursor.execute('SELECT * FROM channels').fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting channels: {e}")
            return []
    
    # Currency methods
    
    def add_currency(self, name, type_, min_amount, max_amount, details):
        """Add a new currency"""
        try:
            self.cursor.execute(
                'INSERT INTO currencies VALUES (?, ?, ?, ?, ?)',
                [name, type_, min_amount, max_amount, details]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding currency: {e}")
            return False
    
    def delete_currency(self, name):
        """Delete a currency"""
        try:
            self.cursor.execute('DELETE FROM currencies WHERE name = ?', [name])
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting currency: {e}")
            return False
    
    def get_currencies_by_type(self, currency_type):
        """Get currencies by type (crypto/fiat)"""
        try:
            result = self.cursor.execute(
                'SELECT name, type FROM currencies WHERE type = ?',
                [currency_type]
            ).fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting currencies by type: {e}")
            return []
    
    def get_currency_details(self, name):
        """Get currency details"""
        try:
            result = self.cursor.execute(
                'SELECT details FROM currencies WHERE name = ?',
                [name]
            ).fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting currency details: {e}")
            return []
    
    def get_currency_limits(self, name):
        """Get min and max amounts for a currency"""
        try:
            result = self.cursor.execute(
                'SELECT min_amount, max_amount FROM currencies WHERE name = ?',
                [name]
            ).fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting currency limits: {e}")
            return []
    
    # Payment method methods
    
    def add_payment_method(self, name, type_):
        """Add a new payment method"""
        try:
            self.cursor.execute(
                'INSERT INTO payment_methods VALUES (?, ?)',
                [str(name), str(type_)]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding payment method: {e}")
            return False
    
    def delete_payment_method(self, name):
        """Delete a payment method"""
        try:
            self.cursor.execute('DELETE FROM payment_methods WHERE name = ?', [name])
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting payment method: {e}")
            return False
    
    def get_payment_methods_by_type(self, type_):
        """Get payment methods by type"""
        try:
            result = self.cursor.execute(
                'SELECT * FROM payment_methods WHERE type = ?',
                [type_]
            ).fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting payment methods by type: {e}")
            return []
    
    # Exchange history methods
    
    def add_exchange_history(self, amount, user_id, exchange_name):
        """Add an exchange to history"""
        try:
            week_number = datetime.today().isocalendar()[1]
            today = date.today()
            date_str = f'{today}-{week_number}'
            
            self.cursor.execute(
                'INSERT INTO exchange_history VALUES (?, ?, ?, ?)',
                [str(amount), str(user_id), str(exchange_name), date_str]
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding exchange to history: {e}")
            return False
    
    def get_exchange_history(self):
        """Get all exchange history"""
        try:
            result = self.cursor.execute('SELECT * FROM exchange_history').fetchall()
            return result
        except Exception as e:
            logger.error(f"Error getting exchange history: {e}")
            return []
