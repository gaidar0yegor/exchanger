from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from keyboards import inline
from data.config import ADMIN_IDS

# Admin command filter
def is_admin(user_id):
    """Check if user is an admin"""
    return user_id in ADMIN_IDS

@dp.message_handler(Command("admin"))
async def cmd_admin(message: types.Message):
    """
    Handle /admin command - show admin panel
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await message.answer("You don't have permission to access the admin panel.")
        return
    
    await message.answer(
        "💻 <b>Admin Panel</b>\n\n"
        "Welcome to the admin panel. Use the buttons below to manage the bot:",
        reply_markup=inline.admin_panel
    )

@dp.message_handler(Command("stats"))
async def cmd_stats(message: types.Message):
    """
    Handle /stats command - show statistics options
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await message.answer("You don't have permission to access statistics.")
        return
    
    await message.answer(
        "📊 <b>Statistics</b>\n\n"
        "Select the time period for statistics:",
        reply_markup=inline.statistics_time
    )

@dp.message_handler(Command("broadcast"))
async def cmd_broadcast(message: types.Message):
    """
    Handle /broadcast command - show broadcast options
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await message.answer("You don't have permission to send broadcasts.")
        return
    
    await message.answer(
        "📣 <b>Broadcast</b>\n\n"
        "Select the type of broadcast message:",
        reply_markup=inline.broadcast_type
    )

# Admin panel navigation
@dp.callback_query_handler(text="back_to_admin")
async def back_to_admin_callback(call: types.CallbackQuery):
    """
    Handle back to admin panel callback
    """
    user_id = call.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await call.answer("You don't have permission to access the admin panel.", show_alert=True)
        return
    
    await call.message.edit_text(
        "💻 <b>Admin Panel</b>\n\n"
        "Welcome to the admin panel. Use the buttons below to manage the bot:",
        reply_markup=inline.admin_panel
    )
    await call.answer()

@dp.callback_query_handler(text="statistics")
async def statistics_callback(call: types.CallbackQuery):
    """
    Handle statistics callback
    """
    user_id = call.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await call.answer("You don't have permission to access statistics.", show_alert=True)
        return
    
    await call.message.edit_text(
        "📊 <b>Statistics</b>\n\n"
        "Select the time period for statistics:",
        reply_markup=inline.statistics_time
    )
    await call.answer()

@dp.callback_query_handler(text="broadcast")
async def broadcast_callback(call: types.CallbackQuery):
    """
    Handle broadcast callback
    """
    user_id = call.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await call.answer("You don't have permission to send broadcasts.", show_alert=True)
        return
    
    await call.message.edit_text(
        "📣 <b>Broadcast</b>\n\n"
        "Select the type of broadcast message:",
        reply_markup=inline.broadcast_type
    )
    await call.answer()

@dp.callback_query_handler(text="change_status")
async def change_status_callback(call: types.CallbackQuery):
    """
    Handle change bot status callback
    """
    user_id = call.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await call.answer("You don't have permission to change bot status.", show_alert=True)
        return
    
    from services.database import Database
    
    # Get current bot status
    with Database() as db:
        status = db.get_bot_status()
    
    current_status = status[0][1] if status else 'on'
    
    await call.message.edit_text(
        f"🔄 <b>Bot Status</b>\n\n"
        f"Current status: <b>{'ON' if current_status == 'on' else 'OFF'}</b>\n\n"
        f"Use the button below to change the bot status:",
        reply_markup=inline.bot_status_keyboard(current_status)
    )
    await call.answer()

@dp.callback_query_handler(text=["bot_on", "bot_off"])
async def toggle_bot_status_callback(call: types.CallbackQuery):
    """
    Handle toggle bot status callback
    """
    user_id = call.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await call.answer("You don't have permission to change bot status.", show_alert=True)
        return
    
    from services.database import Database
    
    # Set new status
    new_status = 'on' if call.data == 'bot_on' else 'off'
    
    # Update status in database
    with Database() as db:
        db.set_bot_status(new_status)
    
    await call.message.edit_text(
        f"🔄 <b>Bot Status</b>\n\n"
        f"Status changed to: <b>{'ON' if new_status == 'on' else 'OFF'}</b>",
        reply_markup=inline.bot_status_keyboard(new_status)
    )
    await call.answer(f"Bot is now {'ON' if new_status == 'on' else 'OFF'}")
