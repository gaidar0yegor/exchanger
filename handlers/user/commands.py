from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from keyboards import inline
from services.database import Database
from data.config import FAQ, SUPPORT_LINK, AUTHOR, VERSION

@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    """
    Handle /start command - add user to database and show welcome message
    """
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    
    # Add user to database
    with Database() as db:
        db.add_user(user_id, full_name, username)
    
    # Send welcome message
    await message.answer(
        f"Welcome to Crypto Exchange Bot!\n\n"
        f"This bot allows you to exchange cryptocurrencies and fiat currencies.\n\n"
        f"Use the buttons below to navigate:",
        reply_markup=inline.main_menu
    )

@dp.message_handler(Command("help"))
async def cmd_help(message: types.Message):
    """
    Handle /help command - show help message
    """
    help_text = (
        "🤖 <b>Crypto Exchange Bot Help</b>\n\n"
        "This bot allows you to exchange cryptocurrencies and fiat currencies.\n\n"
        "<b>Available commands:</b>\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/profile - View your profile\n"
        "/exchange - Exchange currencies\n"
        "/faq - Frequently asked questions\n"
        "/support - Contact support\n\n"
        "<b>How to use:</b>\n"
        "1. Select 'Exchange' from the main menu\n"
        "2. Choose the type of exchange (Fiat to Crypto or Crypto to Fiat)\n"
        "3. Select the currencies you want to exchange\n"
        "4. Enter the amount and your payment details\n"
        "5. Wait for admin approval\n\n"
        f"<b>Version:</b> {VERSION}\n"
        f"<b>Developer:</b> {AUTHOR}"
    )
    
    await message.answer(help_text, reply_markup=inline.main_menu)

@dp.message_handler(Command("profile"))
async def cmd_profile(message: types.Message):
    """
    Handle /profile command - show user profile
    """
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username or "Not set"
    
    profile_text = (
        "👤 <b>Your Profile</b>\n\n"
        f"<b>ID:</b> <code>{user_id}</code>\n"
        f"<b>Name:</b> {full_name}\n"
        f"<b>Username:</b> @{username}\n"
    )
    
    await message.answer(profile_text, reply_markup=inline.back_to_menu)

@dp.message_handler(Command("exchange"))
async def cmd_exchange(message: types.Message):
    """
    Handle /exchange command - show exchange options
    """
    await message.answer(
        "🔄 <b>Exchange</b>\n\n"
        "Please select the type of exchange you want to perform:",
        reply_markup=inline.exchange_type
    )

@dp.message_handler(Command("faq"))
async def cmd_faq(message: types.Message):
    """
    Handle /faq command - show FAQ
    """
    await message.answer(FAQ, reply_markup=inline.back_to_menu)

@dp.message_handler(Command("support"))
async def cmd_support(message: types.Message):
    """
    Handle /support command - show support contact
    """
    await message.answer(
        "👁‍🗨 <b>Support</b>\n\n"
        "If you have any questions or issues, please contact our support team:",
        reply_markup=inline.support_button
    )

# Handle callback queries for main menu navigation
@dp.callback_query_handler(text="menu")
async def menu_callback(call: types.CallbackQuery):
    """
    Handle menu callback - return to main menu
    """
    await call.message.edit_text(
        "Main Menu",
        reply_markup=inline.main_menu
    )
    await call.answer()

@dp.callback_query_handler(text="profile")
async def profile_callback(call: types.CallbackQuery):
    """
    Handle profile callback - show user profile
    """
    user_id = call.from_user.id
    full_name = call.from_user.full_name
    username = call.from_user.username or "Not set"
    
    profile_text = (
        "👤 <b>Your Profile</b>\n\n"
        f"<b>ID:</b> <code>{user_id}</code>\n"
        f"<b>Name:</b> {full_name}\n"
        f"<b>Username:</b> @{username}\n"
    )
    
    await call.message.edit_text(profile_text, reply_markup=inline.back_to_menu)
    await call.answer()

@dp.callback_query_handler(text="exchange")
async def exchange_callback(call: types.CallbackQuery):
    """
    Handle exchange callback - show exchange options
    """
    await call.message.edit_text(
        "🔄 <b>Exchange</b>\n\n"
        "Please select the type of exchange you want to perform:",
        reply_markup=inline.exchange_type
    )
    await call.answer()

@dp.callback_query_handler(text="faq")
async def faq_callback(call: types.CallbackQuery):
    """
    Handle FAQ callback - show FAQ
    """
    await call.message.edit_text(FAQ, reply_markup=inline.back_to_menu)
    await call.answer()

@dp.callback_query_handler(text="close")
async def close_callback(call: types.CallbackQuery):
    """
    Handle close callback - delete message
    """
    await call.message.delete()
    await call.answer()
