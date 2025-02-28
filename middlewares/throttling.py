import asyncio
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware for rate limiting user requests
    """
    
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()
    
    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message
        """
        # Get current handler
        handler = current_handler.get()
        
        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        
        # Use Dispatcher.throttle method
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)
            
            # Cancel current handler
            raise CancelHandler()
    
    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        """
        This handler is called when dispatcher receives a callback query
        """
        # Get current handler
        handler = current_handler.get()
        
        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_callback"
        
        # Use Dispatcher.throttle method
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.callback_throttled(callback_query, t)
            
            # Cancel current handler
            raise CancelHandler()
    
    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user when they hit the rate limit
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        
        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta
        
        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await message.reply("Too many requests! Please slow down.")
        
        # Sleep until throttling is over
        await asyncio.sleep(delta)
    
    async def callback_throttled(self, callback: types.CallbackQuery, throttled: Throttled):
        """
        Notify user when they hit the rate limit via callback
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        
        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta
        
        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await callback.answer("Too many requests! Please slow down.", show_alert=True)
        
        # Sleep until throttling is over
        await asyncio.sleep(delta)


def rate_limit(limit: Union[int, float], key=None):
    """
    Decorator for configuring rate limit and key in different functions.
    """
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator
