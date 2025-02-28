from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from keyboards import inline
from services.database import Database
from states.exchange_states import FiatToCryptoExchange

@dp.callback_query_handler(text="fiat_to_crypto")
async def fiat_to_crypto_handler(call: types.CallbackQuery):
    """
    Handle fiat to crypto exchange selection
    """
    # Get fiat currencies from database
    with Database() as db:
        fiat_currencies = db.get_currencies_by_type(currency_type='fiat')
    
    # Check if there are any fiat currencies
    if not fiat_currencies:
        await call.message.edit_text(
            "There are no fiat currencies available for exchange yet.\n"
            "Please contact the administrator to add some fiat currencies.",
            reply_markup=inline.back_to_menu
        )
        await call.answer()
        return
    
    # Set state to select fiat currency
    await FiatToCryptoExchange.select_fiat.set()
    
    # Show fiat currency selection keyboard
    await call.message.edit_text(
        "Выберите валюту, которую Вы хотите обменять:",
        reply_markup=inline.currency_selection_keyboard(fiat_currencies, 'fiat')
    )
    await call.answer()

@dp.callback_query_handler(Text(startswith="currency_"), state=FiatToCryptoExchange.select_fiat)
async def select_fiat_handler(call: types.CallbackQuery, state: FSMContext):
    """
    Handle fiat currency selection
    """
    # Get selected fiat currency
    fiat = call.data.replace("currency_", "")
    
    # Save to state
    async with state.proxy() as data:
        data['fiat'] = fiat
    
    # Get cryptocurrencies from database
    with Database() as db:
        cryptocurrencies = db.get_currencies_by_type(currency_type='crypto')
    
    # Check if there are any cryptocurrencies
    if not cryptocurrencies:
        await call.message.edit_text(
            "There are no cryptocurrencies available for exchange yet.\n"
            "Please contact the administrator to add some cryptocurrencies.",
            reply_markup=inline.back_to_menu
        )
        await call.answer()
        await state.finish()
        return
    
    # Set state to select cryptocurrency
    await FiatToCryptoExchange.select_crypto.set()
    
    # Show cryptocurrency selection keyboard
    await call.message.edit_text(
        f"You selected {fiat}.\n\n"
        "Now select the cryptocurrency you want to receive:",
        reply_markup=inline.currency_selection_keyboard(cryptocurrencies, 'crypto')
    )
    await call.answer()

@dp.callback_query_handler(Text(startswith="currency_"), state=FiatToCryptoExchange.select_crypto)
async def select_crypto_handler(call: types.CallbackQuery, state: FSMContext):
    """
    Handle cryptocurrency selection
    """
    # Get selected cryptocurrency
    crypto = call.data.replace("currency_", "")
    
    # Save to state
    async with state.proxy() as data:
        data['crypto'] = crypto
        fiat = data['fiat']
    
    # Get payment methods from database
    with Database() as db:
        payment_methods = db.get_payment_methods_by_type(type_='fiat')
    
    # Check if there are any payment methods
    if not payment_methods:
        await call.message.edit_text(
            "There are no payment methods available for this exchange yet.\n"
            "Please contact the administrator to add some payment methods.",
            reply_markup=inline.back_to_menu
        )
        await call.answer()
        await state.finish()
        return
    
    # Set state to select payment method
    await FiatToCryptoExchange.select_payment_method.set()
    
    # Show payment method selection keyboard
    await call.message.edit_text(
        f"You selected {fiat} → {crypto}.\n\n"
        "Now select the payment method you want to use:",
        reply_markup=inline.payment_method_keyboard(payment_methods)
    )
    await call.answer()

@dp.callback_query_handler(Text(startswith="payment_"), state=FiatToCryptoExchange.select_payment_method)
async def select_payment_method_handler(call: types.CallbackQuery, state: FSMContext):
    """
    Handle payment method selection
    """
    # Get selected payment method
    payment_method = call.data.replace("payment_", "")
    
    # Save to state
    async with state.proxy() as data:
        data['payment_method'] = payment_method
        fiat = data['fiat']
    
    # Get currency limits from database
    with Database() as db:
        limits = db.get_currency_limits(fiat)
    
    # Check if limits exist
    if not limits:
        await call.message.edit_text(
            "Could not retrieve currency limits.\n"
            "Please contact the administrator.",
            reply_markup=inline.back_to_menu
        )
        await call.answer()
        await state.finish()
        return
    
    min_amount, max_amount = limits[0]
    
    # Set state to enter amount
    await FiatToCryptoExchange.enter_amount.set()
    
    # Ask for amount
    await call.message.edit_text(
        f"Minimum amount for {fiat}: {min_amount}\n"
        f"Maximum amount for {fiat}: {max_amount}\n\n"
        f"Enter the amount of {fiat} you want to exchange:",
        reply_markup=inline.back_to_menu
    )
    await call.answer()

@dp.message_handler(state=FiatToCryptoExchange.enter_amount)
async def enter_amount_handler(message: types.Message, state: FSMContext):
    """
    Handle amount input
    """
    try:
        # Try to convert input to float
        amount = float(message.text.strip())
        
        # Get fiat from state
        async with state.proxy() as data:
            fiat = data['fiat']
        
        # Get currency limits from database
        with Database() as db:
            limits = db.get_currency_limits(fiat)
        
        min_amount = float(limits[0][0])
        max_amount = float(limits[0][1])
        
        # Check if amount is within limits
        if amount < min_amount or amount > max_amount:
            await message.answer(
                f"Amount must be between {min_amount} and {max_amount}.\n"
                f"Please enter a valid amount:",
                reply_markup=inline.back_to_menu
            )
            return
        
        # Save amount to state
        async with state.proxy() as data:
            data['amount'] = amount
        
        # Set state to enter wallet address
        await FiatToCryptoExchange.enter_wallet_address.set()
        
        # Ask for wallet address
        await message.answer(
            "Please enter your cryptocurrency wallet address:",
            reply_markup=inline.back_to_menu
        )
    
    except ValueError:
        # Handle invalid input
        await message.answer(
            "Please enter a valid number.",
            reply_markup=inline.back_to_menu
        )

@dp.message_handler(state=FiatToCryptoExchange.enter_wallet_address)
async def enter_wallet_address_handler(message: types.Message, state: FSMContext):
    """
    Handle wallet address input
    """
    # Save wallet address to state
    async with state.proxy() as data:
        data['wallet_address'] = message.text.strip()
    
    # Set state to enter comment
    await FiatToCryptoExchange.enter_comment.set()
    
    # Ask for comment
    await message.answer(
        "Please enter an optional comment for this exchange request,\n"
        "or type 'none' if you don't have any comments:",
        reply_markup=inline.back_to_menu
    )

@dp.message_handler(state=FiatToCryptoExchange.enter_comment)
async def enter_comment_handler(message: types.Message, state: FSMContext):
    """
    Handle comment input and show exchange summary
    """
    # Save comment to state
    async with state.proxy() as data:
        data['comment'] = message.text.strip()
        fiat = data['fiat']
        crypto = data['crypto']
        payment_method = data['payment_method']
        amount = data['amount']
        wallet_address = data['wallet_address']
    
    # Set state to confirm
    await FiatToCryptoExchange.confirm.set()
    
    # Show exchange summary
    summary = (
        "📝 <b>Exchange Request Summary</b>\n\n"
        f"<b>Exchange:</b> {fiat} → {crypto}\n"
        f"<b>Amount:</b> {amount} {fiat}\n"
        f"<b>Payment Method:</b> {payment_method}\n"
        f"<b>Wallet Address:</b> {wallet_address}\n"
        f"<b>Comment:</b> {data['comment']}\n\n"
        "Please review the details above. Do you want to submit this exchange request?"
    )
    
    await message.answer(summary, reply_markup=inline.send_to_admin)

@dp.callback_query_handler(text="send_request", state=FiatToCryptoExchange.confirm)
async def send_request_handler(call: types.CallbackQuery, state: FSMContext):
    """
    Handle exchange request submission
    """
    # Get data from state
    async with state.proxy() as data:
        fiat = data['fiat']
        crypto = data['crypto']
        payment_method = data['payment_method']
        amount = data['amount']
        wallet_address = data['wallet_address']
        comment = data['comment']
    
    # Finish state
    await state.finish()
    
    # Send confirmation to user
    await call.message.edit_text(
        "✅ Your exchange request has been submitted.\n"
        "An administrator will review it shortly.\n"
        "You will be notified when your request is processed.",
        reply_markup=inline.back_to_menu
    )
    
    # Send request to admins
    from data.config import EXCHANGE_REQUEST_IDS
    
    user_id = call.from_user.id
    username = call.from_user.username or "N/A"
    full_name = call.from_user.full_name
    
    admin_message = (
        "🔄 <b>New Exchange Request</b>\n\n"
        f"<b>User ID:</b> <code>{user_id}</code>\n"
        f"<b>Username:</b> @{username}\n"
        f"<b>Name:</b> {full_name}\n\n"
        f"<b>Exchange:</b> {fiat} → {crypto}\n"
        f"<b>Amount:</b> {amount} {fiat}\n"
        f"<b>Payment Method:</b> {payment_method}\n"
        f"<b>Wallet Address:</b> {wallet_address}\n"
        f"<b>Comment:</b> {comment}"
    )
    
    exchange_id = f"{fiat}_{crypto}"
    
    for admin_id in EXCHANGE_REQUEST_IDS:
        try:
            await bot.send_message(
                admin_id,
                admin_message,
                reply_markup=inline.exchange_request_keyboard(user_id, exchange_id, amount)
            )
        except Exception as e:
            print(f"Failed to send message to admin {admin_id}: {e}")
    
    # Add to exchange history
    with Database() as db:
        db.add_exchange_history(amount, user_id, f"{fiat} → {crypto}")
    
    await call.answer()
