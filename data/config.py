import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Admin IDs - comma-separated list of admin user IDs
ADMIN_IDS = [int(id) for id in os.getenv('ADMIN_ID', '').split(',') if id]

# IDs to receive exchange requests
EXCHANGE_REQUEST_IDS = [int(id) for id in os.getenv('ANKET_SEND', '').split(',') if id]

# Support and subscription links
SUPPORT_LINK = os.getenv('SUPPORT_LINK', 'https://t.me/crypto_exchange_support')
SUBSCRIPTION_LINK = os.getenv('SUBSCRIPTION_LINK', 'https://t.me/crypto_exchange_channel')

# FAQ text (max 4000 characters)
FAQ = """
Frequently Asked Questions:

What is Crypto Exchange Bot?
- A Telegram bot that helps you exchange cryptocurrencies and fiat currencies.

How does it work?
- Select the exchange option from the main menu
- Choose the currency you want to exchange
- Choose the currency you want to receive
- Enter the amount and your payment details
- Wait for admin approval

What currencies are supported?
- The bot supports various cryptocurrencies and fiat currencies
- The available currencies can be viewed in the exchange menu

Who developed this bot?
- Developed by: @crypto_exchange_dev
"""

# Version
VERSION = "1.0.0"

# Author
AUTHOR = "@crypto_exchange_dev"
