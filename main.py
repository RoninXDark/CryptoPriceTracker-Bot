import asyncio 
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = "YOUR_TOKEN_HERE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_crypto_data(crypto_name):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url, timeout=10) 
        
        
        if response.status_code == 429:
            print("⚠️ API Rate Limit! Зачекай хвилину.")
            return None, None

        data = response.json()

        if crypto_name in data:
            price = data[crypto_name]['usd']
            

            change = data[crypto_name].get('usd_24h_change', 0)
            
            return price, change 
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None 
    

def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="Bitcoin (BTC)", callback_data="check_bitcoin"),
            InlineKeyboardButton(text="Ethereum (ETH)", callback_data="check_ethereum")
        ],
        [
            InlineKeyboardButton(text="Solana (SOL)", callback_data="check_solana"),
            InlineKeyboardButton(text="Tether (USDT)", callback_data="check_tether")
        ],
        [
            InlineKeyboardButton(text="🔍 Search other", callback_data="search_manual")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_refresh_keyboard(crypto_name):
    keyboard = [[
        InlineKeyboardButton(text="🔄 Refresh", callback_data=f"check_{crypto_name}"),
        InlineKeyboardButton(text="🔙 Main Menu", callback_data="back_to_menu")
    ]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)



@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 **Welcome back!**\n\n"
        "Choose a coin to check the price:",
        reply_markup=get_main_keyboard()
    )
    

@dp.callback_query(F.data.startswith("check_"))
async def process_coin_callback(callback: types.CallbackQuery):
    coin_id = callback.data.split("_", 1)[1]

    
    await callback.answer()

    price, change = get_crypto_data(coin_id)

    if price is not None:
        emoji = "📈" if change >= 0 else "📉"
        text = (
            f"💰 **{coin_id.capitalize()}**\n"
            f"━━━━━━━━━━━━\n"
            f"💵 Price: **${price:,.2f}**\n"
            f"📊 24h Change: {emoji} **{change:.2f}%**"
        )

        
        await callback.message.answer(
            text,
            reply_markup=get_refresh_keyboard(coin_id),
        )
    else:
        # Якщо API заблокував або помилка
        await callback.message.answer("⚠️ Too many requests or error. Please wait 1 minute.")


@dp.callback_query(F.data == "back_to_menu")
async def process_back(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "📂 **Main Menu**\nSelect a cryptocurrency:",
        reply_markup=get_main_keyboard()
    )


@dp.callback_query(F.data == "search_manual")
async def process_search(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("⌨️ Please type the name of the coin (e.g., **dogecoin**)")
                                  

@dp.message()
async def process_text_search(message: types.Message):
    coin_id = message.text.lower().strip()
    
    
    status_msg = await message.answer(f"🔍 Searching for **{coin_id}**...")
    
    price, change = get_crypto_data(coin_id)
    
    
    try:
        await status_msg.delete()
    except:
        pass
    
    if price is not None:
        emoji = "📈" if change >= 0 else "📉"
        text = (
            f"💰 **{coin_id.capitalize()}**\n"
            f"━━━━━━━━━━━━\n"
            f"💵 Price: **${price:,.2f}**\n"
            f"📊 24h Change: {emoji} **{change:.2f}%**"
        )

        await message.answer(
            text, reply_markup=get_refresh_keyboard(coin_id))
    else:
        await message.answer(
            f"❌ Coin **'{coin_id}'** not found.\nTry entering the full name (e.g. 'bitcoin').",
            reply_markup=get_main_keyboard()
        )
    
async def main():
    print("Bot is starting... (Press Ctrl+C to stop)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")