# Crypto Exchange Bot

A Telegram bot for exchanging cryptocurrencies and fiat currencies.

## Features

- Exchange cryptocurrencies to fiat currencies and vice versa
- Admin panel for managing currencies, payment methods, and users
- User subscription verification for channels
- Broadcast messages to all users
- Statistics and analytics
- Banner advertisements

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_ID=comma_separated_list_of_admin_ids
   ANKET_SEND=comma_separated_list_of_ids_to_receive_exchange_requests
   SUPPORT_LINK=https://t.me/your_support_username
   SUBSCRIPTION_LINK=https://t.me/your_channel_username
   ```
4. Run the bot:
   ```
   python app.py
   ```

## Project Structure

- `app.py`: Main entry point for the bot
- `loader.py`: Bot initialization and middleware setup
- `data/`: Configuration and constants
- `handlers/`: Message and callback handlers
  - `user/`: User command handlers
  - `admin/`: Admin command handlers
- `keyboards/`: Keyboard layouts
- `middlewares/`: Middleware components
- `services/`: Service components (database, etc.)
- `states/`: State definitions for conversations
- `utils/`: Utility functions

## User Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/profile` - View user profile
- `/exchange` - Exchange currencies
- `/faq` - Frequently asked questions
- `/support` - Contact support

## Admin Commands

- `/admin` - Access admin panel
- `/stats` - View statistics
- `/broadcast` - Send message to all users

## Development

To add new features or modify existing ones:

1. Create or modify handlers in the appropriate directory
2. Update the state definitions if needed
3. Add or modify keyboard layouts
4. Import new handlers in the corresponding `__init__.py` file

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Developed by: @crypto_exchange_dev

## Deployment

This bot can be deployed on Railway using the provided railway.json and Procfile.
