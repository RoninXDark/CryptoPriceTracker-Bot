from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Bitcoin (BTC)",
                    callback_data="quote:bitcoin",
                ),
                InlineKeyboardButton(
                    text="Ethereum (ETH)",
                    callback_data="quote:ethereum",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Solana (SOL)",
                    callback_data="quote:solana",
                ),
                InlineKeyboardButton(
                    text="Tether (USDT)",
                    callback_data="quote:tether",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Search another coin",
                    callback_data="search",
                )
            ],
        ]
    )


def quote_keyboard(coin_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Refresh",
                    callback_data=f"quote:{coin_id}",
                ),
                InlineKeyboardButton(
                    text="Main menu",
                    callback_data="menu",
                ),
            ]
        ]
    )
