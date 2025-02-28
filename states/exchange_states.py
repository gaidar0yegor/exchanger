from aiogram.dispatcher.filters.state import State, StatesGroup

class CryptoToFiatExchange(StatesGroup):
    """States for crypto to fiat exchange process"""
    select_crypto = State()  # Select cryptocurrency to exchange
    select_fiat = State()    # Select fiat currency to receive
    select_payment_method = State()  # Select payment method
    enter_amount = State()   # Enter amount to exchange
    enter_payment_details = State()  # Enter payment details
    enter_comment = State()  # Enter optional comment
    confirm = State()        # Confirm exchange details

class FiatToCryptoExchange(StatesGroup):
    """States for fiat to crypto exchange process"""
    select_fiat = State()    # Select fiat currency to exchange
    select_crypto = State()  # Select cryptocurrency to receive
    select_payment_method = State()  # Select payment method
    enter_amount = State()   # Enter amount to exchange
    enter_wallet_address = State()  # Enter crypto wallet address
    enter_comment = State()  # Enter optional comment
    confirm = State()        # Confirm exchange details

class AdminCurrencyManagement(StatesGroup):
    """States for admin currency management"""
    select_action = State()  # Add or delete currency
    select_type = State()    # Crypto or fiat
    enter_name = State()     # Enter currency name
    enter_min_amount = State()  # Enter minimum amount
    enter_max_amount = State()  # Enter maximum amount
    enter_details = State()  # Enter currency details

class AdminPaymentMethodManagement(StatesGroup):
    """States for admin payment method management"""
    select_action = State()  # Add or delete payment method
    select_type = State()    # Crypto or fiat
    enter_name = State()     # Enter payment method name

class AdminChannelManagement(StatesGroup):
    """States for admin channel management"""
    select_action = State()  # Add or delete channel
    enter_channel_id = State()  # Enter channel ID
    enter_channel_url = State()  # Enter channel URL

class AdminBannerManagement(StatesGroup):
    """States for admin banner management"""
    select_action = State()  # Add or delete banner
    enter_text = State()     # Enter banner text

class AdminUserManagement(StatesGroup):
    """States for admin user management"""
    select_action = State()  # Ban or unban user
    enter_user_id = State()  # Enter user ID

class AdminBroadcast(StatesGroup):
    """States for admin broadcast message"""
    select_type = State()    # With or without media
    upload_media = State()   # Upload media file
    enter_text = State()     # Enter broadcast text
    confirm = State()        # Confirm broadcast
