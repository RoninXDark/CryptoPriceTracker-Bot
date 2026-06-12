import logging

import aiohttp
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from crypto_tracker.coingecko import (
    CoinGeckoClient,
    CoinNotFoundError,
    MarketDataError,
    RateLimitError,
    format_quote,
)
from crypto_tracker.config import load_settings
from crypto_tracker.keyboards import main_keyboard, quote_keyboard


logger = logging.getLogger(__name__)
router = Router()


async def send_quote(
    target: Message,
    coin_name: str,
    market_client: CoinGeckoClient,
) -> None:
    try:
        quote = await market_client.get_quote(coin_name)
    except CoinNotFoundError:
        await target.answer(
            "Coin not found. Use a CoinGecko name such as "
            "<code>bitcoin</code> or ticker <code>btc</code>.",
            reply_markup=main_keyboard(),
        )
    except RateLimitError as exc:
        await target.answer(str(exc), reply_markup=main_keyboard())
    except MarketDataError:
        logger.exception("Market-data request failed")
        await target.answer(
            "Market data is temporarily unavailable. Please try again later.",
            reply_markup=main_keyboard(),
        )
    else:
        await target.answer(
            format_quote(quote),
            reply_markup=quote_keyboard(quote.coin_id),
        )


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "<b>Crypto Price Tracker</b>\n"
        "Choose a popular asset or type any CoinGecko coin name.",
        reply_markup=main_keyboard(),
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Use the menu or send a coin name such as "
        "<code>bitcoin</code>, <code>ethereum</code>, or <code>sol</code>."
    )


@router.callback_query(F.data.startswith("quote:"))
async def quote_callback(
    callback: CallbackQuery,
    market_client: CoinGeckoClient,
) -> None:
    await callback.answer()
    coin_id = callback.data.split(":", 1)[1]
    await send_quote(callback.message, coin_id, market_client)


@router.callback_query(F.data == "menu")
async def menu_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer(
        "<b>Main menu</b>\nSelect a cryptocurrency:",
        reply_markup=main_keyboard(),
    )


@router.callback_query(F.data == "search")
async def search_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer(
        "Send a coin name or ticker, for example "
        "<code>dogecoin</code> or <code>doge</code>."
    )


@router.message(F.text)
async def text_search(
    message: Message,
    market_client: CoinGeckoClient,
) -> None:
    query = message.text.strip()
    if len(query) > 64:
        await message.answer("Coin name is too long.")
        return
    await send_quote(message, query, market_client)


async def run_bot() -> None:
    settings = load_settings()
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    async with aiohttp.ClientSession() as session:
        market_client = CoinGeckoClient(
            session=session,
            timeout_seconds=settings.request_timeout_seconds,
        )
        logger.info("Crypto Price Tracker started")
        try:
            await dispatcher.start_polling(
                bot,
                market_client=market_client,
            )
        finally:
            await bot.session.close()
