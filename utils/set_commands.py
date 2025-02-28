from aiogram import types, Dispatcher
from data.config import ADMIN_IDS

async def set_default_commands(dp: Dispatcher):
    """
    Set default bot commands in the menu
    """
    # Default commands for all users
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start the bot"),
        types.BotCommand("help", "Get help"),
        types.BotCommand("profile", "View your profile"),
        types.BotCommand("exchange", "Exchange currencies"),
        types.BotCommand("faq", "Frequently asked questions"),
        types.BotCommand("support", "Contact support"),
    ])
    
    # Additional commands for admins
    for admin_id in ADMIN_IDS:
        await dp.bot.set_my_commands([
            types.BotCommand("start", "Start the bot"),
            types.BotCommand("help", "Get help"),
            types.BotCommand("profile", "View your profile"),
            types.BotCommand("exchange", "Exchange currencies"),
            types.BotCommand("faq", "Frequently asked questions"),
            types.BotCommand("support", "Contact support"),
            types.BotCommand("admin", "Admin panel"),
            types.BotCommand("stats", "View statistics"),
            types.BotCommand("broadcast", "Send message to all users"),
        ], scope=types.BotCommandScopeChat(admin_id))
