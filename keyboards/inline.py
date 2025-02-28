from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import SUPPORT_LINK, SUBSCRIPTION_LINK

# Main menu keyboard
main_menu = InlineKeyboardMarkup(row_width=2)
main_menu.add(
    InlineKeyboardButton('👤 Profile', callback_data='profile'),
    InlineKeyboardButton('🔄 Exchange', callback_data='exchange')
)
main_menu.add(
    InlineKeyboardButton('ℹ️ FAQ', callback_data='faq'),
    InlineKeyboardButton('👁‍🗨 Support', url=SUPPORT_LINK)
)

# Back to menu button
back_to_menu = InlineKeyboardMarkup()
back_to_menu.add(InlineKeyboardButton('⏪ Back', callback_data='menu'))

# Exchange type selection
exchange_type = InlineKeyboardMarkup()
exchange_type.add(InlineKeyboardButton('Fiat to Crypto', callback_data='fiat_to_crypto'))
exchange_type.add(InlineKeyboardButton('Crypto to Fiat', callback_data='crypto_to_fiat'))
exchange_type.add(InlineKeyboardButton('⏪ Back', callback_data='menu'))

# Close button
close_button = InlineKeyboardMarkup()
close_button.add(InlineKeyboardButton('✖️ Close ✖️', callback_data='close'))

# Support button
support_button = InlineKeyboardMarkup()
support_button.add(InlineKeyboardButton('👁‍🗨 Support', url=SUPPORT_LINK))
support_button.add(InlineKeyboardButton('✖️ Close ✖️', callback_data='close'))

# Send to admin or cancel
send_to_admin = InlineKeyboardMarkup()
send_to_admin.add(
    InlineKeyboardButton('↗️ Send', callback_data='send_request'),
    InlineKeyboardButton('↩️ Cancel', callback_data='menu')
)

# Admin panel main menu
admin_panel = InlineKeyboardMarkup(row_width=2)
admin_panel.add(
    InlineKeyboardButton('➕ Add Fiat', callback_data='add_fiat'),
    InlineKeyboardButton('➕ Add Crypto', callback_data='add_crypto')
)
admin_panel.add(
    InlineKeyboardButton('➖ Delete Fiat', callback_data='delete_fiat'),
    InlineKeyboardButton('➖ Delete Crypto', callback_data='delete_crypto')
)
admin_panel.add(
    InlineKeyboardButton('➕ Fiat Payment Methods', callback_data='payment_fiat'),
    InlineKeyboardButton('➕ Crypto Payment Methods', callback_data='payment_crypto')
)
admin_panel.add(
    InlineKeyboardButton('➖ Delete Fiat Payment', callback_data='delete_payment_fiat'),
    InlineKeyboardButton('➖ Delete Crypto Payment', callback_data='delete_payment_crypto')
)
admin_panel.add(
    InlineKeyboardButton('♻️ Unban User', callback_data='unban_user'),
    InlineKeyboardButton('📛 Ban User', callback_data='ban_user')
)
admin_panel.add(
    InlineKeyboardButton('📊 Statistics', callback_data='statistics'),
    InlineKeyboardButton('📣 Broadcast', callback_data='broadcast')
)
admin_panel.add(
    InlineKeyboardButton('➕ Add Channel', callback_data='add_channel'),
    InlineKeyboardButton('➖ Remove Channel', callback_data='delete_channel')
)
admin_panel.add(
    InlineKeyboardButton('➕ Add Banner', callback_data='add_banner'),
    InlineKeyboardButton('➖ Remove Banner', callback_data='remove_banner')
)
admin_panel.add(InlineKeyboardButton('🔄 Change Bot Status', callback_data='change_status'))

# Back to admin panel
back_to_admin = InlineKeyboardMarkup()
back_to_admin.add(InlineKeyboardButton('⬅️ Back', callback_data='back_to_admin'))

# Statistics time period selection
statistics_time = InlineKeyboardMarkup()
statistics_time.add(InlineKeyboardButton('🕐 Daily', callback_data='stats_day'))
statistics_time.add(InlineKeyboardButton('🕒 Weekly', callback_data='stats_week'))
statistics_time.add(InlineKeyboardButton('🕕 Monthly', callback_data='stats_month'))
statistics_time.add(InlineKeyboardButton('⬅️ Back', callback_data='back_to_admin'))

# Broadcast message type selection
broadcast_type = InlineKeyboardMarkup()
broadcast_type.add(InlineKeyboardButton('📷 With Media', callback_data='broadcast_with_media'))
broadcast_type.add(InlineKeyboardButton('📝 Without Media', callback_data='broadcast_without_media'))
broadcast_type.add(InlineKeyboardButton('⬅️ Back', callback_data='back_to_admin'))

# Confirm broadcast
confirm_broadcast = InlineKeyboardMarkup()
confirm_broadcast.add(InlineKeyboardButton('✅ Start', callback_data='start_broadcast'))
confirm_broadcast.add(InlineKeyboardButton('❌ Cancel', callback_data='back_to_admin'))

# Bot status toggle
def bot_status_keyboard(status):
    keyboard = InlineKeyboardMarkup()
    if status == 'on':
        keyboard.add(InlineKeyboardButton('🔴 Turn Off', callback_data='bot_off'))
    else:
        keyboard.add(InlineKeyboardButton('🟢 Turn On', callback_data='bot_on'))
    keyboard.add(InlineKeyboardButton('⬅️ Back', callback_data='back_to_admin'))
    return keyboard

# Channel subscription keyboard
def channel_subscription_keyboard(channels):
    keyboard = InlineKeyboardMarkup()
    for channel in channels:
        keyboard.add(InlineKeyboardButton('➕ Channel', url=channel))
    return keyboard

# Dynamic keyboards that depend on database data

def currency_selection_keyboard(currencies, currency_type):
    """Create keyboard with currency options based on type"""
    keyboard = InlineKeyboardMarkup()
    
    for currency in currencies:
        if currency[1] == currency_type:
            keyboard.add(InlineKeyboardButton(currency[0], callback_data=f'currency_{currency[0]}'))
    
    keyboard.add(InlineKeyboardButton('⏪ Back', callback_data='menu'))
    return keyboard

def payment_method_keyboard(payment_methods):
    """Create keyboard with payment method options"""
    keyboard = InlineKeyboardMarkup()
    
    for method in payment_methods:
        name = method[0]
        keyboard.add(InlineKeyboardButton(name, callback_data=f'payment_{name}'))
    
    keyboard.add(InlineKeyboardButton('⬅️ Back', callback_data='menu'))
    return keyboard

def delete_currency_keyboard(currencies):
    """Create keyboard for deleting currencies"""
    keyboard = InlineKeyboardMarkup()
    
    for currency in currencies:
        name = currency[0]
        type_ = currency[1]
        keyboard.add(InlineKeyboardButton(name, callback_data=f'delete_currency_{name}_{type_}'))
    
    keyboard.add(InlineKeyboardButton('⬅️ Back', callback_data='back_to_admin'))
    return keyboard

def delete_payment_method_keyboard(payment_methods):
    """Create keyboard for deleting payment methods"""
    keyboard = InlineKeyboardMarkup()
    
    for method in payment_methods:
        name = method[0]
        type_ = method[1]
        keyboard.add(InlineKeyboardButton(name, callback_data=f'delete_payment_{type_}_{name}'))
    
    keyboard.add(InlineKeyboardButton('⬅️ Back', callback_data='back_to_admin'))
    return keyboard

def exchange_request_keyboard(user_id, exchange, amount):
    """Create keyboard for admin to approve/reject exchange request"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('✅ Approve', callback_data=f'approve_{user_id}_{exchange}_{amount}'),
        InlineKeyboardButton('❌ Reject', callback_data=f'reject_{user_id}_{exchange}_{amount}')
    )
    return keyboard

def user_payment_confirmation_keyboard(exchange, amount):
    """Create keyboard for user to confirm payment sent"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('✅ Payment Sent', callback_data=f'payment_sent_{exchange}_{amount}'),
        InlineKeyboardButton('❌ Cancel Exchange', callback_data=f'cancel_exchange_{exchange}_{amount}')
    )
    return keyboard

def admin_exchange_completion_keyboard(user_id, exchange, amount):
    """Create keyboard for admin to complete exchange"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Complete Exchange', callback_data=f'complete_{user_id}_{amount}_{exchange}'))
    keyboard.add(InlineKeyboardButton('Cancel Exchange', callback_data=f'admin_cancel_{user_id}_{amount}_{exchange}'))
    return keyboard
