import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import ADMIN_IDS
from services.database import Database
from keyboards.inline import channel_subscription_keyboard

logger = logging.getLogger(__name__)

class BotStatusMiddleware(BaseMiddleware):
    """
    Middleware to check if the bot is enabled or disabled
    """
    
    async def on_process_message(self, message: types.Message, data: dict):
        """Check bot status for messages"""
        # Skip check for admins
        if message.from_user.id in ADMIN_IDS:
            return
        
        # Check bot status
        with Database() as db:
            status = db.get_bot_status()
        
        # If bot is off, cancel handler and notify user
        if status and status[0][1] == 'off':
            await message.answer('🛑 Bot is currently disabled.')
            raise CancelHandler()
    
    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        """Check bot status for callback queries"""
        # Skip check for admins
        if callback_query.from_user.id in ADMIN_IDS:
            return
        
        # Check bot status
        with Database() as db:
            status = db.get_bot_status()
        
        # If bot is off, cancel handler and notify user
        if status and status[0][1] == 'off':
            await callback_query.answer('🛑 Bot is currently disabled.', show_alert=True)
            raise CancelHandler()


class BanCheckMiddleware(BaseMiddleware):
    """
    Middleware to check if user is banned
    """
    
    async def on_process_message(self, message: types.Message, data: dict):
        """Check if user is banned for messages"""
        # Skip check for admins
        if message.from_user.id in ADMIN_IDS:
            return
        
        # Check if user is banned
        with Database() as db:
            is_banned = db.is_user_banned(message.from_user.id)
        
        # If user is banned, cancel handler and notify user
        if is_banned:
            await message.answer('You have been banned from using this bot.')
            raise CancelHandler()
    
    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        """Check if user is banned for callback queries"""
        # Skip check for admins
        if callback_query.from_user.id in ADMIN_IDS:
            return
        
        # Check if user is banned
        with Database() as db:
            is_banned = db.is_user_banned(callback_query.from_user.id)
        
        # If user is banned, cancel handler and notify user
        if is_banned:
            await callback_query.answer('You have been banned from using this bot.', show_alert=True)
            raise CancelHandler()


class ChannelSubscriptionMiddleware(BaseMiddleware):
    """
    Middleware to check if user is subscribed to required channels
    """
    
    async def on_process_message(self, message: types.Message, data: dict):
        """Check channel subscription for messages"""
        # Skip check for admins
        if message.from_user.id in ADMIN_IDS:
            return
        
        # Get required channels
        with Database() as db:
            channels = db.get_channels()
        
        # If no channels required, skip check
        if not channels:
            return
        
        # Check if user is subscribed to all channels
        from loader import bot
        
        url_list = []
        for channel in channels:
            channel_id = channel[0]
            url = channel[1]
            url_list.append(url)
            
            try:
                member = await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)
                if member.status == 'left':
                    # User is not subscribed to at least one channel
                    await message.answer(
                        '⁉️ You need to subscribe to our channels to use this bot. '
                        'Please subscribe and then press /start again.',
                        reply_markup=channel_subscription_keyboard(url_list)
                    )
                    raise CancelHandler()
            except Exception as e:
                logger.error(f"Error checking channel subscription: {e}")
                # Continue even if there's an error checking the channel
                continue
    
    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        """Check channel subscription for callback queries"""
        # Skip check for admins
        if callback_query.from_user.id in ADMIN_IDS:
            return
        
        # Get required channels
        with Database() as db:
            channels = db.get_channels()
        
        # If no channels required, skip check
        if not channels:
            return
        
        # Check if user is subscribed to all channels
        from loader import bot
        
        url_list = []
        for channel in channels:
            channel_id = channel[0]
            url = channel[1]
            url_list.append(url)
            
            try:
                member = await bot.get_chat_member(chat_id=channel_id, user_id=callback_query.from_user.id)
                if member.status == 'left':
                    # User is not subscribed to at least one channel
                    await bot.send_message(
                        callback_query.from_user.id,
                        '⁉️ You need to subscribe to our channels to use this bot. '
                        'Please subscribe and then press /start again.',
                        reply_markup=channel_subscription_keyboard(url_list)
                    )
                    await callback_query.answer()
                    raise CancelHandler()
            except Exception as e:
                logger.error(f"Error checking channel subscription: {e}")
                # Continue even if there's an error checking the channel
                continue


class BannerMiddleware(BaseMiddleware):
    """
    Middleware to show banner for specific actions
    """
    
    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        """Show banner for exchange action"""
        # Skip for admins
        if callback_query.from_user.id in ADMIN_IDS:
            return
        
        # Only show banner for exchange action
        if callback_query.data != 'exchange':
            return
        
        # Get banner
        with Database() as db:
            banner = db.get_banner()
        
        # If banner exists, show it
        if banner:
            await callback_query.answer(banner[0][1], show_alert=True)
