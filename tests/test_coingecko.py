import pytest

from crypto_tracker.coingecko import (
    CoinNotFoundError,
    CoinQuote,
    format_quote,
    normalize_coin_id,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("BTC", "bitcoin"),
        (" eth ", "ethereum"),
        ("doge", "dogecoin"),
        ("avalanche-2", "avalanche-2"),
        ("USD Coin", "usd-coin"),
    ],
)
def test_normalize_coin_id(value: str, expected: str) -> None:
    assert normalize_coin_id(value) == expected


def test_normalize_coin_id_rejects_unsafe_input() -> None:
    with pytest.raises(CoinNotFoundError):
        normalize_coin_id("<script>")


def test_format_quote_contains_price_and_change() -> None:
    quote = CoinQuote(
        coin_id="bitcoin",
        price_usd=64321.5,
        change_24h=2.345,
    )

    message = format_quote(quote)

    assert "Bitcoin" in message
    assert "$64,321.50" in message
    assert "+2.35%" in message
