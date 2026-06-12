import re
from dataclasses import dataclass

import aiohttp


COIN_ALIASES = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "usdt": "tether",
    "doge": "dogecoin",
}


class MarketDataError(RuntimeError):
    """Base error for market-data requests."""


class CoinNotFoundError(MarketDataError):
    """Raised when CoinGecko does not recognize a coin."""


class RateLimitError(MarketDataError):
    """Raised when CoinGecko asks the client to slow down."""


@dataclass(frozen=True)
class CoinQuote:
    coin_id: str
    price_usd: float
    change_24h: float


def normalize_coin_id(value: str) -> str:
    coin_id = value.strip().lower().replace(" ", "-")
    coin_id = COIN_ALIASES.get(coin_id, coin_id)
    if not re.fullmatch(r"[a-z0-9-]{1,64}", coin_id):
        raise CoinNotFoundError("Use a CoinGecko coin name such as bitcoin.")
    return coin_id


def format_quote(quote: CoinQuote) -> str:
    direction = "up" if quote.change_24h >= 0 else "down"
    return (
        f"<b>{quote.coin_id.replace('-', ' ').title()}</b>\n"
        f"Price: <b>${quote.price_usd:,.2f}</b>\n"
        f"24h change: <b>{quote.change_24h:+.2f}%</b> ({direction})"
    )


class CoinGeckoClient:
    BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

    def __init__(
        self,
        session: aiohttp.ClientSession,
        timeout_seconds: float = 10.0,
    ) -> None:
        self._session = session
        self._timeout = aiohttp.ClientTimeout(total=timeout_seconds)

    async def get_quote(self, value: str) -> CoinQuote:
        coin_id = normalize_coin_id(value)
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        }

        try:
            async with self._session.get(
                self.BASE_URL,
                params=params,
                timeout=self._timeout,
            ) as response:
                if response.status == 429:
                    raise RateLimitError(
                        "CoinGecko rate limit reached. Try again in a minute."
                    )
                if response.status >= 400:
                    raise MarketDataError(
                        f"CoinGecko returned HTTP {response.status}."
                    )
                payload = await response.json()
        except aiohttp.ClientError as exc:
            raise MarketDataError("Could not reach CoinGecko.") from exc

        coin_data = payload.get(coin_id)
        if not coin_data or "usd" not in coin_data:
            raise CoinNotFoundError(
                f"Coin '{coin_id}' was not found on CoinGecko."
            )

        return CoinQuote(
            coin_id=coin_id,
            price_usd=float(coin_data["usd"]),
            change_24h=float(coin_data.get("usd_24h_change") or 0.0),
        )
