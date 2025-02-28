from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from keyboards import inline
from services.database import Database
from states.exchange_states import CryptoToFiatExchange

@dp.callback_query_handler(text="crypto_to_fiat")
async def crypto_to_fiat_handler(call: types.CallbackQuery):
    """
    Handle crypto to fiat exchange selection
    """
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
        return
    
    # Set state to select cryptocurrency
    await CryptoToFiatExchange.select_crypto.set()
    
    # Show cryptocurrency selection keyboard
    await call.message.edit_text(
        "Выберите криптовалюту, которую Вы хотите обменять:",
        reply_markup=inline.currency_selection_keyboard(cryptocurrencies, 'crypto')
    )
    await call.answer()

@dp.callback_query_handler(Text(startswith="currency_"), state=CryptoToFiatExchange.select_crypto)
async def select_crypto_handler(call: types.CallbackQuery, state: FSMContext):
    """
    Handle cryptocurrency selection
    """
    # Get selected cryptocurrency
    crypto = call.data.replace("currency_", "")
    
    # Save to state
    async with state.proxy() as data:
        data['crypto'] = crypto
    
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
        await state.finish()
        return
    
    # Set state to select fiat currency
    await CryptoToFiatExchange.select_fiat.set()
    
    # Show fiat currency selection keyboard
    await call.message.edit_text(
        f"You selected {crypto}.\n\n"
        "Now select the fiat currency you want to receive:",
        reply_markup=inline.currency_selection_keyboard(fiat_currencies, 'fiat')
    )
    await call.answer()

@dp.callback_query_handler(Text(startswith="currency_"), state=CryptoToFiatExchange.select_fiat)
async def select_fiat_handler(call: types.CallbackQuery, state: FSMContext):
    """
    Handle fiat currency selection
    """
    # Get selected fiat currency
    fiat = call.data.replace("currency_", "")
    
    # Save to state
    async with state.proxy() as data:
        data['fiat'] = fiat
        crypto = data['crypto']
    
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
    await CryptoToFiatExchange.select_payment_method.set()
    
    # Show payment method selection keyboard
    await call.message.edit_text(
        f"You selected {crypto} → {fiat}.\n\n"
        "Now select the payment method you want to use:",
        reply_markup=inline.payment_method_keyboard(payment_methods)
    )
    await call.answer()

@dp.callback_query_handler(Text(startswith="payment_"), state=CryptoToFiatExchange.select_payment_method)
async def select_payment_method_handler(call: types.CallbackQuery, state: FSMContext):
    """
    Handle payment method selection
    """
    # Get selected payment method
    payment_method = call.data.replace("payment_", "")
    
    # Save to state
    async with state.proxy() as data:
        data['payment_method'] = payment_method
        crypto = data['crypto']
    
    # Get currency limits from database
    with Database() as db:
        limits = db.get_currency_limits(crypto)
    
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
    await CryptoToFiatExchange.enter_amount.set()
    
    # Ask for amount
    await call.message.edit_text(
        f"Minimum amount for {crypto}: {min_amount}\n"
        f"Maximum amount for {crypto}: {max_amount}\n\n"
        f"Enter the amount of {crypto} you want to exchange:",
        reply_markup=inline.back_to_menu
    )
    await call.answer()

@dp.message_handler(state=CryptoToFiatExchange.enter_amount)
async def enter_amount_handler(message: types.Message, state: FSMContext):
    """
    Handle amount input
    """
    try:
        # Try to convert input to float
        amount = float(message.text.strip())
        
        # Get crypto from state
        async with state.proxy() as data:
            crypto = data['crypto']
        
        # Get currency limits from database
        with Database() as db:
            limits = db.get_currency_limits(crypto)
        
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
        
        # Set state to enter payment details
        await CryptoToFiatExchange.enter_payment_details.set()
        
        # Ask for payment details
        await message.answer(
            "Please enter your payment details (e.g., card number, phone number):",
            reply_markup=inline.back_to_menu
        )
    
    except ValueError:
        # Handle invalid input
        await message.answer(
            "Please enter a valid number.",
            reply_markup=inline.back_to_menu
        )

@dp.message_handler(state=CryptoToFiatExchange.enter_payment_details)
async def enter_payment_details_handler(message: types.Message, state: FSMContext):
    """
    Handle payment details input
    """
    # Save payment details to state
    async with state.proxy() as data:
        data['payment_details'] = message.text.strip()
    
    # Set state to enter comment
    await CryptoToFiatExchange.enter_comment.set()
    
    # Ask for comment
    await message.answer(
        "Please enter an optional comment for this exchange request,\n"
        "or type 'none' if you don't have any comments:",
        reply_markup=inline.back_to_menu
    )

@dp.message_handler(state=CryptoToFiatExchange.enter_comment)
async def enter_comment_handler(message: types.Message, state: FSMContext):
    """
    Handle comment input and show exchange summary
    """
    # Save comment to state
    async with state.proxy() as data:
        data['comment'] = message.text.strip()
        crypto = data['crypto']
        fiat = data['fiat']
        payment_method = data['payment_method']
        amount = data['amount']
        payment_details = data['payment_details']
    
    # Set state to confirm
    await CryptoToFiatExchange.confirm.set()
    
    # Show exchange summary
    summary = (
        "📝 <b>Exchange Request Summary</b>\n\n"
        f"<b>Exchange:</b> {crypto} → {fiat}\n"
        f"<b>Amount:</b> {amount} {crypto}\n"
        f"<b>Payment Method:</b> {payment_method}\n"
        f"<b>Payment Details:</b> {payment_details}\n"
        f"<b>Comment:</b> {data['comment']}\n\n"
        "Please review the details above. Do you want to submit this exchange request?"
    )
    
    await message.answer(summary, reply_markup=inline.send_to_admin)

@dp.callback_query_handler(text="send_request", state=CryptoToFiatExchange.confirm)
async def send_request_handler(call: types.CallbackQuery, state: FSMContext):
    """
    Handle exchange request submission
    """
    # Get data from state
    async with state.proxy() as data:
        crypto = data['crypto']
        fiat = data['fiat']
        payment_method = data['payment_method']
        amount = data['amount']
        payment_details = data['payment_details']
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
        f"<b>Exchange:</b> {crypto} → {fiat}\n"
        f"<b>Amount:</b> {amount} {crypto}\n"
        f"<b>Payment Method:</b> {payment_method}\n"
        f"<b>Payment Details:</b> {payment_details}\n"
        f"<b>Comment:</b> {comment}"
    )
    
    exchange_id = f"{crypto}_{fiat}"
    
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
        db.add_exchange_history(amount, user_id, f"{crypto} → {fiat}")
    
    await call.answer()
